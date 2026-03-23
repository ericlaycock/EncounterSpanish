from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
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
from app.services.voice_turn_service import build_transcription_prompt, build_conversation_prompt, build_grammar_system_prompt, build_grammar_user_prompt, get_language_mode, get_conversation_system_prompt
from app.data.grammar_situations import get_grammar_config
from app.services.catalan_service import apply_catalan_mode
from app.utils.audio import generate_audio_filename, get_audio_path, get_audio_url, upload_to_r2
router = APIRouter()

# OpenAI TTS voice + instructions per situation — keyed by animation_type
_ACCENT = "Speak with a Mexican Spanish accent, mixing English and Spanish words naturally."
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
}


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

        # Generate TTS for initial message
        initial_audio_url = None
        if initial_message:
            try:
                init_audio_filename = generate_audio_filename()
                init_audio_path = get_audio_path(init_audio_filename)
                tts_cfg = SITUATION_VOICE_CONFIG.get(situation.animation_type, {})
                tts_voice = tts_cfg.get("voice", "alloy")
                tts_instructions = tts_cfg.get("instructions")
                await gateway_synthesize_speech(
                    text=initial_message,
                    output_path=str(init_audio_path),
                    voice=tts_voice,
                    instructions=tts_instructions,
                    request_id=str(voice_conv.id),
                    user_id=str(current_user.id),
                    db=db,
                )
                r2_url = upload_to_r2(str(init_audio_path), init_audio_filename)
                initial_audio_url = r2_url or get_audio_url(init_audio_filename)
                logger.info(f"[Create Conv] Initial message TTS: {initial_audio_url}")
            except Exception as e:
                logger.error(f"[Create Conv] Initial message TTS failed: {e}")

        return CreateConversationResponse(
            conversation_id=voice_conv.id,
            words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english, notes=w.notes) for w in final_words],
            initial_message=initial_message,
            initial_audio_url=initial_audio_url,
            language_mode=language_mode,
            vocab_level=vocab_level,
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

        # Generate TTS for initial message
        initial_audio_url = None
        if initial_message:
            try:
                init_audio_filename = generate_audio_filename()
                init_audio_path = get_audio_path(init_audio_filename)
                tts_cfg = SITUATION_VOICE_CONFIG.get(situation.animation_type, {})
                tts_voice = tts_cfg.get("voice", "alloy")
                tts_instructions = tts_cfg.get("instructions")
                await gateway_synthesize_speech(
                    text=initial_message,
                    output_path=str(init_audio_path),
                    voice=tts_voice,
                    instructions=tts_instructions,
                    request_id=str(conversation.id),
                    user_id=str(current_user.id),
                    db=db,
                )
                r2_url = upload_to_r2(str(init_audio_path), init_audio_filename)
                initial_audio_url = r2_url or get_audio_url(init_audio_filename)
            except Exception as e:
                logger.error(f"[Create Conv] Initial message TTS failed: {e}")

        return CreateConversationResponse(
            conversation_id=conversation.id,
            words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english) for w in final_words],
            initial_message=initial_message,
            initial_audio_url=initial_audio_url,
            language_mode=language_mode,
            vocab_level=vocab_level,
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
        filename=audio.filename or "audio.webm",
        prompt=f"The user is saying a Spanish word or phrase: {expected_word}. Transcribe exactly what they say.",
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
    is_correct = norm_expected in norm_transcript or norm_transcript in norm_expected

    logger.info(f"[PronCheck] transcript='{transcript}' norm='{norm_transcript}' expected_norm='{norm_expected}' correct={is_correct}")

    return {"transcript": transcript, "is_correct": is_correct}


@router.post("/{conversation_id}/voice-turn", response_model=VoiceTurnResponse)
async def voice_turn(
    conversation_id: str,
    request: Request,
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
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
    
    # Step 1: STT transcription with context prompt
    read_start = time.time()
    audio_bytes = await audio.read()
    read_time = time.time() - read_start
    logger.info(f"[Voice Turn] Audio read: {read_time:.2f}s, size: {len(audio_bytes)} bytes")
    
    # Get words and situation for prompt context
    db_start = time.time()
    words = get_words_by_ids(db, conversation.target_word_ids)
    situation = db.query(Situation).filter(Situation.id == conversation.situation_id).first()
    db_time = time.time() - db_start
    logger.info(f"[Voice Turn] DB queries: {db_time:.2f}s")

    # Catalan mode: swap spanish → catalan for word detection + prompts
    catalan_mode = current_user.catalan_mode
    if catalan_mode:
        words = apply_catalan_mode(words, db)

    transcription_prompt = build_transcription_prompt(
        situation.title if situation else "a situation", words,
        catalan_mode=catalan_mode,
    )

    stt_start = time.time()
    user_transcript = await gateway_transcribe_audio(
        audio_bytes=audio_bytes,
        filename=audio.filename or "audio.mp3",
        prompt=transcription_prompt,
        language=None,  # Auto-detect — users mix English + Spanish/Catalan
        request_id=request_id,
        user_id=str(current_user.id),
        db=db,
        learning_phase=learning_phase
    )
    stt_time = time.time() - stt_start
    logger.info(f"[Voice Turn] STT transcription: {stt_time:.2f}s, transcript: '{user_transcript}'")
    
    # Step 2: Detect word_ids
    detect_start = time.time()
    detected_word_ids = detect_words_in_text(user_transcript, words)
    detect_time = time.time() - detect_start
    logger.info(f"[Voice Turn] Word detection: {detect_time:.2f}s, detected: {detected_word_ids}")
    
    # Step 3: Update used_spoken_word_ids
    update_start = time.time()
    current_used = set(conversation.used_spoken_word_ids or [])
    current_used.update(detected_word_ids)
    conversation.used_spoken_word_ids = list(current_used)
    
    # Step 4: Update user_words.spoken_correct_count
    update_user_word_stats(db, str(current_user.id), detected_word_ids, "voice")
    update_time = time.time() - update_start
    logger.info(f"[Voice Turn] DB updates: {update_time:.2f}s")
    
    # Step 5: Generate assistant_text via OpenAI
    # Compute language mode for prompt selection
    vocab_level = get_vocab_level(db, current_user.id)
    language_mode = get_language_mode(situation.encounter_number, vocab_level)

    # Catalan mode: adjust language_mode for prompt selection
    if catalan_mode and language_mode in ("spanish_text", "spanish_audio"):
        language_mode = language_mode.replace("spanish_", "catalan_")

    grammar_config = get_grammar_config(conversation.situation_id)
    if grammar_config:
        system_prompt = build_grammar_system_prompt(conversation.situation_id)
        user_prompt = build_grammar_user_prompt(
            situation.title,
            conversation.used_spoken_word_ids or [],
            user_transcript,
            grammar_config,
        )
    else:
        system_prompt = get_conversation_system_prompt(language_mode, catalan_mode=catalan_mode)
        user_prompt = build_conversation_prompt(
            situation.title,
            words,
            conversation.used_spoken_word_ids or [],
            user_transcript,
            catalan_mode=catalan_mode,
        )
    
    # Use LLM gateway
    gen_start = time.time()
    context = ConversationContext(
        request_id=request_id,
        user_id=str(current_user.id),
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        agent_id="conversation_agent",
        prompt_version="v1",
        return_json=True,
        learning_phase=learning_phase
    )
    llm_result = await generate_conversation(context, db)
    gen_time = time.time() - gen_start
    
    # Extract response (gateway returns dict with 'content')
    assistant_response = llm_result["content"] if isinstance(llm_result["content"], dict) else {"assistant_text": "", "end_conversation": False}
    assistant_text = assistant_response.get("assistant_text", "")
    end_conversation = assistant_response.get("end_conversation", False)
    logger.info(f"[Voice Turn] Text generation: {gen_time:.2f}s, text: '{assistant_text[:50]}...'")
    
    # Step 6: TTS generate audio file
    tts_start = time.time()
    audio_filename = generate_audio_filename()
    audio_path = get_audio_path(audio_filename)
    tts_cfg = SITUATION_VOICE_CONFIG.get(situation.animation_type, {}) if situation else {}
    tts_voice = tts_cfg.get("voice", "alloy")
    tts_instructions = tts_cfg.get("instructions")
    await gateway_synthesize_speech(
        text=assistant_text,
        output_path=str(audio_path),
        voice=tts_voice,
        instructions=tts_instructions,
        request_id=request_id,
        user_id=str(current_user.id),
        db=db,
        learning_phase=learning_phase
    )
    # Upload to R2 (falls back to local URL if R2 not configured)
    r2_url = upload_to_r2(str(audio_path), audio_filename)
    assistant_audio_url = r2_url or get_audio_url(audio_filename)
    tts_time = time.time() - tts_start
    if r2_url:
        logger.info(f"[Voice Turn] TTS generation: {tts_time:.2f}s, audio_url: {assistant_audio_url} (R2)")
    else:
        logger.warning(f"[Voice Turn] TTS generation: {tts_time:.2f}s, audio_url: {assistant_audio_url} (LOCAL FALLBACK — R2 upload failed)")
    
    # Check if conversation is complete
    conversation_complete = check_conversation_complete(conversation, "voice")
    if conversation_complete:
        conversation.status = "complete"
    
    commit_start = time.time()
    db.commit()
    commit_time = time.time() - commit_start
    logger.info(f"[Voice Turn] DB commit: {commit_time:.2f}s")
    
    # Get missing words
    missing_word_ids = get_missing_word_ids(conversation, "voice")
    
    total_time = time.time() - start_time
    logger.info(f"[Voice Turn] Total processing time: {total_time:.2f}s (read: {read_time:.2f}s, db_queries: {db_time:.2f}s, stt: {stt_time:.2f}s, detect: {detect_time:.2f}s, update: {update_time:.2f}s, gen: {gen_time:.2f}s, tts: {tts_time:.2f}s, commit: {commit_time:.2f}s)")
    
    return VoiceTurnResponse(
        user_transcript=user_transcript,
        detected_word_ids=detected_word_ids,
        missing_word_ids=missing_word_ids,
        assistant_text=assistant_text,
        assistant_audio_url=assistant_audio_url,
        conversation_complete=conversation_complete
    )
