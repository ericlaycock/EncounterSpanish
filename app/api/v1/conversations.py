from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, get_current_user_from_query
from app.models import User, Conversation, Situation, SituationWord, Word, UserWord
from app.schemas import (
    CreateConversationRequest,
    CreateConversationResponse,
    MessageRequest,
    MessageResponse,
    VoiceTurnResponse,
    WordSchema
)
from app.services.openai_service import generate_text, transcribe_audio, generate_speech  # Deprecated, use gateways
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
from app.utils.audio import generate_audio_filename, get_audio_path, get_audio_url
import json

router = APIRouter()


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
    ).order_by(Conversation.created_at.desc()).first()
    
    if existing_conv and existing_conv.target_word_ids:
        # Reuse existing conversation's words
        target_word_ids = existing_conv.target_word_ids
        words = get_words_by_ids(db, target_word_ids)
        
        # Sort words: encounter words first, then high frequency
        word_dict = {w.id: w for w in words}
        situation_words = db.query(SituationWord).filter(
            SituationWord.situation_id == request.situation_id
        ).order_by(SituationWord.position).all()
        encounter_word_ids = [sw.word_id for sw in situation_words]
        high_freq_word_ids = [wid for wid in target_word_ids if wid not in encounter_word_ids]
        
        sorted_encounter_words = [word_dict[wid] for wid in encounter_word_ids if wid in word_dict]
        sorted_high_freq_words = [word_dict[wid] for wid in high_freq_word_ids if wid in word_dict]
        final_words = sorted_encounter_words + sorted_high_freq_words
        
        # Create or get voice conversation with same words
        voice_conv = db.query(Conversation).filter(
            Conversation.user_id == current_user.id,
            Conversation.situation_id == request.situation_id,
            Conversation.mode == "voice"
        ).order_by(Conversation.created_at.desc()).first()
        
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
        
        initial_message = get_initial_message_for_encounter(situation.title)
        return CreateConversationResponse(
            conversation_id=voice_conv.id,
            words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english, notes=w.notes) for w in final_words],
            initial_message=initial_message
        )
    else:
        # No existing conversation - this shouldn't happen if startSituation was called first
        # But create one anyway as fallback
        situation_words = db.query(SituationWord).filter(
            SituationWord.situation_id == request.situation_id
        ).order_by(SituationWord.position).all()
        
        encounter_word_ids = [sw.word_id for sw in situation_words]
        
        learned_word_ids = set(
            word_id[0] for word_id in 
            db.query(UserWord.word_id).filter(UserWord.user_id == current_user.id).all()
        )
        
        high_freq_words = db.query(Word).filter(
            Word.word_category == 'high_frequency',
            ~Word.id.in_(learned_word_ids) if learned_word_ids else True
        ).order_by(Word.frequency_rank.asc().nullslast()).limit(2).all()
        
        high_freq_word_ids = [w.id for w in high_freq_words]
        target_word_ids = encounter_word_ids + high_freq_word_ids
        
        all_word_ids = encounter_word_ids + high_freq_word_ids
        all_words = db.query(Word).filter(Word.id.in_(all_word_ids)).all()
        
        word_dict = {w.id: w for w in all_words}
        sorted_encounter_words = [word_dict[wid] for wid in encounter_word_ids]
        sorted_high_freq_words = [word_dict[wid] for wid in high_freq_word_ids]
        final_words = sorted_encounter_words + sorted_high_freq_words
        
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
        
        initial_message = get_initial_message_for_encounter(situation.title)
        return CreateConversationResponse(
            conversation_id=conversation.id,
            words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english) for w in final_words],
            initial_message=initial_message
        )


# Text chat endpoints removed - only voice chat is used now

@router.post("/{conversation_id}/voice-turn", response_model=VoiceTurnResponse)
async def voice_turn(
    conversation_id: str,
    audio: UploadFile = File(...),
    request: Request,
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
    
    # Build prompt to help Whisper with Spanish vocabulary and context
    # Include target words and situation context to improve transcription accuracy
    target_words_list = ", ".join([f"{w.spanish} ({w.english})" for w in words])
    transcription_prompt = f"""This is a conversation about {situation.title if situation else 'a situation'}.
The user is learning Spanish and may use these Spanish words: {target_words_list}.
The conversation is in Spanish and English. Focus on accurate Spanish transcription.
Common Spanish words that may appear: tamaño, talla, número, grande, pequeño, mediano."""
    
    stt_start = time.time()
    user_transcript = await gateway_transcribe_audio(
        audio_bytes=audio_bytes,
        filename=audio.filename or "audio.mp3",
        prompt=transcription_prompt,
        language="es",
        request_id=request_id,
        user_id=str(current_user.id),
        db=db
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
    # Situation already loaded above
    target_words = [f"{w.spanish} ({w.english})" for w in words]
    used_words = [w.spanish for w in words if w.id in (conversation.used_spoken_word_ids or [])]
    missing_words = [w.spanish for w in words if w.id not in (conversation.used_spoken_word_ids or [])]
    
    # Load system prompt from prompts.json
    system_prompt = load_prompt("conversation_agent", "v1")
    
    missing_words_info = []
    for word in words:
        if word.id not in (conversation.used_spoken_word_ids or []):
            missing_words_info.append(f"{word.spanish} ({word.english})")
    
    user_prompt = f"""Situation: {situation.title}
Still need: {', '.join(missing_words_info) if missing_words_info else 'All words used'}
Already used: {', '.join(used_words) if used_words else 'None'}
User said: {user_transcript}

Ask a natural question requiring a missing Spanish word. Do NOT mention the Spanish word. Return JSON only."""
    
    # Use LLM gateway
    gen_start = time.time()
    context = ConversationContext(
        request_id=request_id,
        user_id=str(current_user.id),
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        agent_id="conversation_agent",
        prompt_version="v1",
        return_json=True
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
    await gateway_synthesize_speech(
        text=assistant_text,
        output_path=str(audio_path),
        voice="alloy",
        request_id=request_id,
        user_id=str(current_user.id),
        db=db
    )
    assistant_audio_url = get_audio_url(audio_filename)
    tts_time = time.time() - tts_start
    logger.info(f"[Voice Turn] TTS generation: {tts_time:.2f}s")
    
    # Check if conversation is complete
    conversation_complete = check_conversation_complete(conversation, "voice") or end_conversation
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

