import json as json_module
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, get_current_user_from_query
from app.models import User, Conversation, Situation, Word
from app.services.word_selection_service import select_words_for_situation, sort_words_encounter_first
from app.schemas import (
    CreateConversationRequest,
    CreateConversationResponse,
    MessageRequest,
    MessageResponse,
    VoiceTurnResponse,
    WordSchema
)
from app.services.llm_gateway import generate_conversation, ConversationContext, load_prompt
from app.services.openai_media_gateway import transcribe_audio as gateway_transcribe_audio, synthesize_speech as gateway_synthesize_speech
from fastapi import Request
from app.services.word_detection import detect_words_in_text, get_words_by_ids
from app.services.conversation_service import (
    check_conversation_complete,
    update_user_word_stats,
    get_missing_word_ids
)
from app.services.encounter_messages import get_initial_message_for_encounter
from app.api.v1.situations import get_vocab_level
from app.services.voice_turn_service import build_transcription_prompt, build_conversation_prompt, build_grammar_system_prompt, build_grammar_user_prompt, get_language_mode, get_conversation_system_prompt, build_system_prompt
from app.data.grammar_situations import get_grammar_config
from app.services.catalan_service import apply_catalan_mode
from app.utils.audio import generate_audio_filename, get_audio_path, get_audio_url, upload_to_r2
router = APIRouter()

# Cache for initial message TTS audio URLs — avoids re-synthesizing the same audio
# Key: (situation_id, catalan_mode) → R2/local URL
_initial_tts_cache: dict[tuple[str, bool], str] = {}

# OpenAI TTS voice + instructions per situation — keyed by animation_type
_ACCENT = "Speak with a Mexican Spanish accent, mixing English and Spanish words naturally."
_CATALAN_ACCENT = "Speak with a Catalan accent, mixing English and Catalan words naturally."
SITUATION_VOICE_CONFIG = {
    "police": {
        "voice": "nova",
        "instructions": f"{_ACCENT} Use an authoritative female voice, firm but professional.",
    },
    "banking": {
        "voice": "shimmer",
        "instructions": f"{_ACCENT} Use a professional, composed female voice with a warm undertone.",
    },
    "airport": {
        "voice": "nova",
        "instructions": f"{_ACCENT} Use a professional, clear female voice.",
    },
    "clothing": {
        "voice": "coral",
        "instructions": f"{_ACCENT} Use a casual, charming female voice.",
    },
    "small_talk": {
        "voice": "shimmer",
        "instructions": f"{_ACCENT} Use a warm, older female voice with a friendly, neighborly tone.",
    },
    "internet": {
        "voice": "nova",
        "instructions": f"{_ACCENT} Use a young, energetic female voice.",
    },
    "restaurant": {
        "voice": "echo",
        "instructions": f"{_ACCENT} Use a suave, charming male voice.",
    },
    "mechanic": {
        "voice": "onyx",
        "instructions": f"{_ACCENT} Use a deep male voice.",
    },
    "groceries": {
        "voice": "echo",
        "instructions": f"{_ACCENT} Use a casual, charming male voice.",
    },
    "contractor": {
        "voice": "onyx",
        "instructions": f"{_ACCENT} Use a deep, husky baritone male voice.",
    },
    "core": {
        "voice": "echo",
        "instructions": f"{_ACCENT} Use a casual, friendly male voice.",
    },
}


def get_tts_instructions(animation_type: str, catalan_mode: bool = False) -> tuple[str, str | None]:
    """Return (voice, instructions) for TTS, adjusted for Catalan mode."""
    cfg = SITUATION_VOICE_CONFIG.get(animation_type, {})
    voice = cfg.get("voice", "alloy")
    instructions = cfg.get("instructions")
    if catalan_mode and instructions:
        instructions = instructions.replace(_ACCENT, _CATALAN_ACCENT)
    return voice, instructions


@router.post("", response_model=CreateConversationResponse)
async def create_conversation(
    request: CreateConversationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"🔍 POST /v1/conversations - User: {current_user.id}, Situation: {request.situation_id}, Mode: {request.mode}")
    situation = db.query(Situation).filter(Situation.id == request.situation_id).first()
    if not situation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Situation not found"
        )
    
    # Voice mode only - reuse words from existing conversation created by startSituation
    # startSituation creates a "text" mode conversation as the source of truth for words
    existing_conv = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.situation_id == request.situation_id,
        Conversation.mode == "text"
    ).order_by(Conversation.created_at.desc()).with_for_update().first()
    
    if existing_conv and existing_conv.target_word_ids:
        # Reuse existing conversation's words
        target_word_ids = existing_conv.target_word_ids
        words = get_words_by_ids(db, target_word_ids)
        final_words = sort_words_encounter_first(words, request.situation_id, db, target_word_ids)
        
        # Create or get voice conversation with same words
        voice_conv = db.query(Conversation).filter(
            Conversation.user_id == current_user.id,
            Conversation.situation_id == request.situation_id,
            Conversation.mode == "voice",
            Conversation.status == "active"
        ).order_by(Conversation.created_at.desc()).with_for_update().first()
        
        if not voice_conv:
            voice_conv = Conversation(
                user_id=current_user.id,
                situation_id=request.situation_id,
                mode="voice",
                target_word_ids=target_word_ids,
                used_typed_word_ids=[],
                used_spoken_word_ids=[]
            )
            db.add(voice_conv)
            db.commit()
            db.refresh(voice_conv)
        
        initial_message = get_initial_message_for_encounter(situation.id, situation.title)
        vocab_level = get_vocab_level(db, current_user.id)
        language_mode = get_language_mode(situation.encounter_number, vocab_level)

        # Catalan mode: swap words + adjust language_mode
        if current_user.catalan_mode:
            final_words = apply_catalan_mode(final_words, db)
            if language_mode in ("spanish_text", "spanish_audio"):
                language_mode = language_mode.replace("spanish_", "catalan_")

        # Use pre-generated R2 audio for initial message (no TTS call needed).
        # Audio files are uploaded by scripts/pregenerate_initial_audio.py with
        # deterministic filenames: initial_msg_{situation_id}.mp3
        from app.config import settings as _settings
        initial_audio_url = f"{_settings.r2_public_url}/initial_msg_{situation.id}.mp3" if _settings.r2_public_url else None

        system_prompt = build_system_prompt(
            situation.animation_type, situation.id, language_mode,
            catalan_mode=current_user.catalan_mode,
        )
        return CreateConversationResponse(
            conversation_id=voice_conv.id,
            words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english, notes=w.notes) for w in final_words],
            initial_message=initial_message,
            initial_audio_url=initial_audio_url,
            language_mode=language_mode,
            vocab_level=vocab_level,
            system_prompt=system_prompt,
        )
    else:
        # No existing conversation - this shouldn't happen if startSituation was called first
        # But create one anyway as fallback
        encounter_word_ids, high_freq_word_ids = select_words_for_situation(db, current_user.id, request.situation_id)
        target_word_ids = encounter_word_ids + high_freq_word_ids
        all_words = db.query(Word).filter(Word.id.in_(target_word_ids)).all()
        final_words = sort_words_encounter_first(all_words, request.situation_id, db, target_word_ids)
        
        conversation = Conversation(
            user_id=current_user.id,
            situation_id=request.situation_id,
            mode=request.mode,
            target_word_ids=target_word_ids,
            used_typed_word_ids=[],
            used_spoken_word_ids=[]
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        initial_message = get_initial_message_for_encounter(situation.id, situation.title)
        vocab_level = get_vocab_level(db, current_user.id)
        language_mode = get_language_mode(situation.encounter_number, vocab_level)

        # Catalan mode: swap words + adjust language_mode
        if current_user.catalan_mode:
            final_words = apply_catalan_mode(final_words, db)
            if language_mode in ("spanish_text", "spanish_audio"):
                language_mode = language_mode.replace("spanish_", "catalan_")

        # Use pre-generated R2 audio for initial message
        initial_audio_url = f"{_settings.r2_public_url}/initial_msg_{situation.id}.mp3" if _settings.r2_public_url else None

        system_prompt = build_system_prompt(
            situation.animation_type, situation.id, language_mode,
            catalan_mode=current_user.catalan_mode,
        )
        return CreateConversationResponse(
            conversation_id=conversation.id,
            words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english) for w in final_words],
            initial_message=initial_message,
            initial_audio_url=initial_audio_url,
            language_mode=language_mode,
            vocab_level=vocab_level,
            system_prompt=system_prompt,
        )


# Text chat endpoints removed - only voice chat is used now

@router.post("/check-pronunciation")
async def check_pronunciation(
    audio: UploadFile = File(...),
    expected_word: str = Form(...),
    current_user: User = Depends(get_current_user),
):
    """Lightweight pronunciation check: STT + string match. No LLM, no TTS."""
    import logging
    import re
    import unicodedata
    logger = logging.getLogger(__name__)

    audio_bytes = await audio.read()
    logger.info(f"[PronCheck] Checking pronunciation: expected='{expected_word}', audio={len(audio_bytes)} bytes")

    transcript = await gateway_transcribe_audio(
        audio_bytes=audio_bytes,
        filename=audio.filename or "audio.mp3",
        prompt=f"The user is saying a {'Catalan' if current_user.catalan_mode else 'Spanish'} word or phrase: {expected_word}. Transcribe exactly what they say.",
        language=None,
        request_id=str(current_user.id),
        user_id=str(current_user.id),
    )

    # Normalize for comparison: lowercase, strip accents, remove punctuation
    def normalize(s: str) -> str:
        s = s.lower().strip()
        s = unicodedata.normalize('NFD', s)
        s = re.sub(r'[\u0300-\u036f]', '', s)  # Remove accent marks
        s = s.replace('ñ', 'n')
        s = re.sub(r'[.,!?;:\'"¿¡]', '', s)
        s = re.sub(r'\s+', ' ', s).strip()
        return s

    norm_transcript = normalize(transcript)
    norm_expected = normalize(expected_word)
    is_correct = norm_transcript == norm_expected

    logger.info(f"[PronCheck] transcript='{transcript}' norm='{norm_transcript}' expected_norm='{norm_expected}' correct={is_correct}")

    return {"transcript": transcript, "is_correct": is_correct}


@router.post("/{conversation_id}/mark-word")
async def mark_word_detected(
    conversation_id: str,
    word_id: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Manually mark a word as detected (user override for STT failures)."""
    import logging
    logger = logging.getLogger(__name__)

    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id,
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    current_used = set(conversation.used_spoken_word_ids or [])
    current_used.add(word_id)
    conversation.used_spoken_word_ids = list(current_used)

    from app.services.conversation_service import update_user_word_stats, check_conversation_complete, get_missing_word_ids
    update_user_word_stats(db, str(current_user.id), [word_id], "voice")

    conversation_complete = check_conversation_complete(conversation, "voice")
    if conversation_complete:
        conversation.status = "complete"

    db.commit()
    missing_word_ids = get_missing_word_ids(conversation, "voice")
    logger.info(f"[MarkWord] User {current_user.id} manually marked word {word_id} in conversation {conversation_id}")

    return {
        "word_id": word_id,
        "missing_word_ids": missing_word_ids,
        "conversation_complete": conversation_complete,
    }


@router.get("/debug/stream-test")
async def stream_test():
    """Diagnostic: test if NDJSON streaming actually flushes through middleware.
    Yields two events 3s apart. If the client receives them 3s apart, streaming works.
    If both arrive together after 3s, middleware is buffering."""
    import asyncio
    async def generate():
        yield json_module.dumps({"type": "ping", "time": "t=0s", "message": "If you see this immediately, streaming works"}) + "\n"
        await asyncio.sleep(3)
        yield json_module.dumps({"type": "pong", "time": "t=3s", "message": "This should arrive 3s after ping"}) + "\n"
    return StreamingResponse(generate(), media_type="application/x-ndjson")


@router.post("/{conversation_id}/voice-turn")
async def voice_turn(
    conversation_id: str,
    request: Request,
    audio: UploadFile = File(...),
    messages_json: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Process a voice turn: STT → detect → update → generate → TTS"""
    import time
    import logging
    logger = logging.getLogger(__name__)
    start_time = time.time()
    logger.info(f"[Voice Turn] Starting voice_turn for conversation {conversation_id}")
    
    # Get request_id from request state (set by middleware)
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Get learning phase from header (Phase 2 or 3 for voice conversations)
    learning_phase = request.headers.get("X-Learning-Phase", "2")  # Default to phase 2 if not provided
    
    # Set user_id in request state for logging middleware
    request.state.user_id = current_user.id
    
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation.mode != "voice":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This endpoint is for voice mode only"
        )
    
    # ── Read audio + prepare context (fast) ──────────────────────────────
    read_start = time.time()
    audio_bytes = await audio.read()
    read_time = time.time() - read_start

    db_start = time.time()
    words = get_words_by_ids(db, conversation.target_word_ids)
    situation = db.query(Situation).filter(Situation.id == conversation.situation_id).first()
    db_time = time.time() - db_start

    catalan_mode = current_user.catalan_mode
    if catalan_mode:
        words = apply_catalan_mode(words, db)

    transcription_prompt = build_transcription_prompt(
        situation.title if situation else "a situation", words,
        catalan_mode=catalan_mode,
    )

    # Parse frontend messages up front (needed for LLM later)
    frontend_messages = None
    if messages_json:
        try:
            frontend_messages = json_module.loads(messages_json)
        except (json_module.JSONDecodeError, TypeError):
            logger.warning("[Voice Turn] Failed to parse messages_json, falling back to single-turn")

    # ── Streaming generator: yields transcript first, then AI response ─
    async def generate():
        nonlocal conversation  # needed for DB updates

        # ── EVENT 1: STT → word detection → DB update → stream transcript ──
        stt_start = time.time()
        user_transcript = await gateway_transcribe_audio(
            audio_bytes=audio_bytes,
            filename=audio.filename or "audio.mp3",
            prompt=transcription_prompt,
            language=None,
            request_id=request_id,
            user_id=str(current_user.id),
            db=db,
            learning_phase=learning_phase,
        )
        stt_time = time.time() - stt_start
        logger.info(f"[Voice Turn] STT transcription: {stt_time:.2f}s, transcript: '{user_transcript}'")
        if stt_time > 2.0:
            logger.warning(f"[Voice Turn] STT exceeded 2s threshold: {stt_time:.2f}s")

        detected_word_ids = detect_words_in_text(user_transcript, words)
        logger.info(f"[Voice Turn] Word detection: detected {detected_word_ids}")

        current_used = set(conversation.used_spoken_word_ids or [])
        current_used.update(detected_word_ids)
        conversation.used_spoken_word_ids = list(current_used)
        update_user_word_stats(db, str(current_user.id), detected_word_ids, "voice")

        missing_word_ids = get_missing_word_ids(conversation, "voice")

        transcript_stream_time = time.time() - start_time
        logger.info(f"[Voice Turn] YIELD transcript at {transcript_stream_time:.2f}s")

        transcript_payload = json_module.dumps({
            "type": "transcript",
            "user_transcript": user_transcript,
            "detected_word_ids": detected_word_ids,
            "missing_word_ids": missing_word_ids,
        }) + "\n"
        logger.info(f"[Voice Turn] Transcript payload size: {len(transcript_payload)} bytes")
        yield transcript_payload
        logger.info(f"[Voice Turn] AFTER transcript yield at {time.time() - start_time:.2f}s")

        # ── EVENT 2: LLM → TTS → stream AI response ───────────────────
        vocab_level = get_vocab_level(db, current_user.id)
        language_mode = get_language_mode(situation.encounter_number, vocab_level)
        if catalan_mode and language_mode in ("spanish_text", "spanish_audio"):
            language_mode = language_mode.replace("spanish_", "catalan_")

        gen_start = time.time()
        if frontend_messages:
            llm_messages = list(frontend_messages)
            llm_messages.append({"role": "user", "content": user_transcript})
            context = ConversationContext(
                request_id=request_id,
                user_id=str(current_user.id),
                system_prompt="",
                user_prompt="",
                agent_id="conversation_agent",
                prompt_version="v2",
                return_json=False,
                learning_phase=learning_phase,
                messages=llm_messages,
            )
            llm_result = await generate_conversation(context, db)
            raw_content = llm_result.get("content", "")
            assistant_text = raw_content if isinstance(raw_content, str) else raw_content.get("assistant_text", str(raw_content))
        else:
            grammar_config = get_grammar_config(conversation.situation_id)
            if grammar_config:
                system_prompt = build_grammar_system_prompt(conversation.situation_id, catalan_mode=catalan_mode)
                user_prompt = build_grammar_user_prompt(
                    situation.title, conversation.used_spoken_word_ids or [],
                    user_transcript, grammar_config,
                )
            else:
                system_prompt = get_conversation_system_prompt(
                    language_mode, catalan_mode=catalan_mode,
                    animation_type=situation.animation_type if situation else "",
                    situation_id=conversation.situation_id,
                )
                user_prompt = build_conversation_prompt(
                    situation.title, words, conversation.used_spoken_word_ids or [],
                    user_transcript, catalan_mode=catalan_mode,
                )
            context = ConversationContext(
                request_id=request_id,
                user_id=str(current_user.id),
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                agent_id="conversation_agent",
                prompt_version="v2",
                return_json=False,
                learning_phase=learning_phase,
            )
            llm_result = await generate_conversation(context, db)
            raw_content = llm_result.get("content", "")
            assistant_text = raw_content if isinstance(raw_content, str) else raw_content.get("assistant_text", str(raw_content))

        gen_time = time.time() - gen_start
        logger.info(f"[Voice Turn] Text generation: {gen_time:.2f}s, text: '{assistant_text[:50]}...'")

        tts_start = time.time()
        audio_filename = generate_audio_filename()
        audio_path = get_audio_path(audio_filename)
        tts_voice, tts_instructions = get_tts_instructions(
            situation.animation_type if situation else "", catalan_mode=catalan_mode,
        )
        await gateway_synthesize_speech(
            text=assistant_text, output_path=str(audio_path),
            voice=tts_voice, instructions=tts_instructions,
            request_id=request_id, user_id=str(current_user.id),
            db=db, learning_phase=learning_phase,
        )
        # Synchronous R2 upload — required for multi-replica setups where local
        # /tmp/audio/ is per-replica. R2 URL works from any replica.
        r2_url = upload_to_r2(str(audio_path), audio_filename)
        assistant_audio_url = r2_url or get_audio_url(audio_filename)
        tts_time = time.time() - tts_start

        conversation_complete = check_conversation_complete(conversation, "voice")
        if conversation_complete:
            conversation.status = "complete"
        db.commit()

        response_stream_time = time.time() - start_time
        logger.info(f"[Voice Turn] YIELD response at {response_stream_time:.2f}s (stt: {stt_time:.2f}s, gen: {gen_time:.2f}s, tts: {tts_time:.2f}s)")
        if response_stream_time > 3.0:
            logger.warning(f"[Voice Turn] AI response exceeded 3s threshold: {response_stream_time:.2f}s")

        yield json_module.dumps({
            "type": "response",
            "assistant_text": assistant_text,
            "assistant_audio_url": assistant_audio_url,
            "conversation_complete": conversation_complete,
        }) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")
