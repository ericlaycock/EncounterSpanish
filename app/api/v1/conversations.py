from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.responses import StreamingResponse
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
from app.services.openai_service import generate_text, stream_text, transcribe_audio, generate_speech
from app.services.word_detection import detect_words_in_text, get_words_by_ids
from app.services.conversation_service import (
    check_conversation_complete,
    update_user_word_stats,
    get_missing_word_ids
)
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
    
    # For voice mode, try to reuse words from existing text conversation
    # This ensures both text and voice chat use the same high-frequency words
    if request.mode == "voice":
        existing_text_conv = db.query(Conversation).filter(
            Conversation.user_id == current_user.id,
            Conversation.situation_id == request.situation_id,
            Conversation.mode == "text"
        ).order_by(Conversation.created_at.desc()).first()
        
        if existing_text_conv and existing_text_conv.target_word_ids:
            # Reuse the same words from text conversation
            target_word_ids = existing_text_conv.target_word_ids
            words = get_words_by_ids(db, target_word_ids)
            
            # Create voice conversation with same words
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
            
            # Sort words: encounter words first, then high frequency
            word_dict = {w.id: w for w in words}
            # Get encounter words
            situation_words = db.query(SituationWord).filter(
                SituationWord.situation_id == request.situation_id
            ).order_by(SituationWord.position).all()
            encounter_word_ids = [sw.word_id for sw in situation_words]
            high_freq_word_ids = [wid for wid in target_word_ids if wid not in encounter_word_ids]
            
            sorted_encounter_words = [word_dict[wid] for wid in encounter_word_ids if wid in word_dict]
            sorted_high_freq_words = [word_dict[wid] for wid in high_freq_word_ids if wid in word_dict]
            final_words = sorted_encounter_words + sorted_high_freq_words
            
            return CreateConversationResponse(
                conversation_id=conversation.id,
                words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english) for w in final_words]
            )
    
    # For text mode: reuse existing conversation created by startSituation
    # startSituation is the single source of truth - it creates the conversation
    existing_text_conv = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.situation_id == request.situation_id,
        Conversation.mode == "text"
    ).order_by(Conversation.created_at.desc()).first()
    
    if existing_text_conv and existing_text_conv.target_word_ids:
        # Reuse existing conversation's words
        target_word_ids = existing_text_conv.target_word_ids
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
        
        return CreateConversationResponse(
            conversation_id=existing_text_conv.id,
            words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english) for w in final_words]
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
        
        return CreateConversationResponse(
            conversation_id=conversation.id,
            words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english) for w in final_words]
        )


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: str,
    message: MessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in text mode conversation"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation.mode != "text":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This endpoint is for text mode only"
        )
    
    # Get all words to detect
    words = get_words_by_ids(db, conversation.target_word_ids)
    
    # Detect words in user message
    detected_word_ids = detect_words_in_text(message.text, words)
    
    # Update used_typed_word_ids
    current_used = set(conversation.used_typed_word_ids or [])
    current_used.update(detected_word_ids)
    conversation.used_typed_word_ids = list(current_used)
    
    # Update user word stats
    update_user_word_stats(db, str(current_user.id), detected_word_ids, "text")
    
    # Check if complete
    if check_conversation_complete(conversation, "text"):
        conversation.status = "complete"
    
    db.commit()
    
    # Get missing words
    missing_word_ids = get_missing_word_ids(conversation, "text")
    
    return MessageResponse(
        detected_word_ids=detected_word_ids,
        missing_word_ids=missing_word_ids
    )


@router.get("/{conversation_id}/stream")
async def stream_conversation(
    conversation_id: str,
    token: str = Query(..., description="JWT token for authentication"),
    current_user: User = Depends(get_current_user_from_query),
    db: Session = Depends(get_db)
):
    """Stream assistant response for text mode conversation (SSE)
    Note: Token must be passed as query parameter since EventSource doesn't support headers"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation.mode != "text":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This endpoint is for text mode only"
        )
    
    # Get situation and words
    situation = db.query(Situation).filter(Situation.id == conversation.situation_id).first()
    words = get_words_by_ids(db, conversation.target_word_ids)
    
    # Format target words for prompt
    target_words = [f"{w.spanish} ({w.english})" for w in words]
    used_words = [w.spanish for w in words if w.id in (conversation.used_typed_word_ids or [])]
    missing_words = [w.spanish for w in words if w.id not in (conversation.used_typed_word_ids or [])]
    
    # Clean, concise system prompt
    system_prompt = """You are a helpful assistant at a Spanish-speaking location helping an English-speaking expat.
Speak only in English. Keep responses to 1-2 sentences.
Naturally ask questions that require the user to use specific Spanish words - but NEVER mention the Spanish words directly.
Encourage natural conversation where the user can use multiple Spanish words together.
Once a word has been used, move on to asking about the remaining words."""
    
    # Build concise context - only missing words
    missing_words_info = []
    for word in words:
        if word.id not in (conversation.used_typed_word_ids or []):
            missing_words_info.append(f"{word.spanish} ({word.english})")
    
    # Concise user prompt
    if missing_words_info:
        user_prompt = f"""Situation: {situation.title}
Still need to elicit: {', '.join(missing_words_info)}
Already used: {', '.join(used_words) if used_words else 'None'}

Ask a natural question about one of the missing words. Do NOT mention the Spanish word. Move the conversation forward naturally."""
    else:
        user_prompt = f"""Situation: {situation.title}
All words have been used. Continue the conversation naturally to complete the interaction."""
    
    async def generate():
        async for chunk in stream_text(system_prompt, user_prompt):
            # Frontend expects {text: string} format
            yield f"data: {json.dumps({'text': chunk})}\n\n"
        # Frontend expects {done: true} format
        yield f"data: {json.dumps({'done': True})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post("/{conversation_id}/voice-turn", response_model=VoiceTurnResponse)
async def voice_turn(
    conversation_id: str,
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process a voice turn: STT → detect → update → generate → TTS"""
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
    audio_bytes = await audio.read()
    
    # Get words and situation for prompt context
    words = get_words_by_ids(db, conversation.target_word_ids)
    situation = db.query(Situation).filter(Situation.id == conversation.situation_id).first()
    
    # Build prompt to help Whisper with Spanish vocabulary and context
    # Include target words and situation context to improve transcription accuracy
    target_words_list = ", ".join([f"{w.spanish} ({w.english})" for w in words])
    transcription_prompt = f"""This is a conversation about {situation.title if situation else 'a situation'}.
The user is learning Spanish and may use these Spanish words: {target_words_list}.
The conversation is in Spanish and English. Focus on accurate Spanish transcription.
Common Spanish words that may appear: tamaño, talla, número, grande, pequeño, mediano."""
    
    user_transcript = await transcribe_audio(
        audio_bytes, 
        filename=audio.filename or "audio.mp3",
        prompt=transcription_prompt
    )
    
    # Step 2: Detect word_ids
    detected_word_ids = detect_words_in_text(user_transcript, words)
    
    # Step 3: Update used_spoken_word_ids
    current_used = set(conversation.used_spoken_word_ids or [])
    current_used.update(detected_word_ids)
    conversation.used_spoken_word_ids = list(current_used)
    
    # Step 4: Update user_words.spoken_correct_count
    update_user_word_stats(db, str(current_user.id), detected_word_ids, "voice")
    
    # Step 5: Generate assistant_text via OpenAI
    # Situation already loaded above
    target_words = [f"{w.spanish} ({w.english})" for w in words]
    used_words = [w.spanish for w in words if w.id in (conversation.used_spoken_word_ids or [])]
    missing_words = [w.spanish for w in words if w.id not in (conversation.used_spoken_word_ids or [])]
    
    system_prompt = """You are a helpful assistant at a Spanish-speaking location helping an English-speaking expat.
Speak only in English. Keep replies to 1-2 sentences.
Naturally ask questions that require specific Spanish words - but NEVER mention the Spanish words directly.
Return JSON: {{"assistant_text": "...", "end_conversation": false}}"""
    
    missing_words_info = []
    for word in words:
        if word.id not in (conversation.used_spoken_word_ids or []):
            missing_words_info.append(f"{word.spanish} ({word.english})")
    
    user_prompt = f"""Situation: {situation.title}
Still need: {', '.join(missing_words_info) if missing_words_info else 'All words used'}
Already used: {', '.join(used_words) if used_words else 'None'}
User said: {user_transcript}

Ask a natural question requiring a missing Spanish word. Do NOT mention the Spanish word. Return JSON only."""
    
    assistant_response = await generate_text(system_prompt, user_prompt, return_json=True)
    assistant_text = assistant_response.get("assistant_text", "")
    end_conversation = assistant_response.get("end_conversation", False)
    
    # Step 6: TTS generate audio file
    audio_filename = generate_audio_filename()
    audio_path = get_audio_path(audio_filename)
    await generate_speech(assistant_text, str(audio_path))
    assistant_audio_url = get_audio_url(audio_filename)
    
    # Check if conversation is complete
    conversation_complete = check_conversation_complete(conversation, "voice") or end_conversation
    if conversation_complete:
        conversation.status = "complete"
    
    db.commit()
    
    # Get missing words
    missing_word_ids = get_missing_word_ids(conversation, "voice")
    
    return VoiceTurnResponse(
        user_transcript=user_transcript,
        detected_word_ids=detected_word_ids,
        missing_word_ids=missing_word_ids,
        assistant_text=assistant_text,
        assistant_audio_url=assistant_audio_url,
        conversation_complete=conversation_complete
    )

