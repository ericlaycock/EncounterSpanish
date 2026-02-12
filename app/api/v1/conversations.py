from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User, Conversation, Situation, SituationWord, Word
from app.schemas import (
    CreateConversationRequest,
    CreateConversationResponse,
    MessageRequest,
    MessageResponse,
    VoiceTurnResponse
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
    situation = db.query(Situation).filter(Situation.id == request.situation_id).first()
    if not situation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Situation not found"
        )
    
    # Get target words for this situation
    situation_words = db.query(SituationWord).filter(
        SituationWord.situation_id == request.situation_id
    ).all()
    target_word_ids = [sw.word_id for sw in situation_words]
    
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
    
    return CreateConversationResponse(conversation_id=conversation.id)


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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Stream assistant response for text mode conversation (SSE)"""
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
    
    # System prompt for Screen 2
    system_prompt = """You are a language coach in an expat survival Spanish app.
You always speak in English.
You guide the user to insert specific Spanish target words exactly as provided.
Keep responses short (1–2 sentences).
Do not introduce new Spanish.
Do not mention target words explicitly."""
    
    # Developer template
    user_prompt = f"""Situation: {situation.title}
Target Spanish words: {', '.join(target_words)}
Already used: {', '.join(used_words) if used_words else 'None'}
Missing words: {', '.join(missing_words) if missing_words else 'None'}

Reply in English with a short question that nudges use of missing words."""
    
    async def generate():
        async for chunk in stream_text(system_prompt, user_prompt):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
        yield "data: [DONE]\n\n"
    
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
    
    # Step 1: STT transcription
    audio_bytes = await audio.read()
    user_transcript = await transcribe_audio(audio_bytes, filename=audio.filename or "audio.mp3")
    
    # Step 2: Detect word_ids
    words = get_words_by_ids(db, conversation.target_word_ids)
    detected_word_ids = detect_words_in_text(user_transcript, words)
    
    # Step 3: Update used_spoken_word_ids
    current_used = set(conversation.used_spoken_word_ids or [])
    current_used.update(detected_word_ids)
    conversation.used_spoken_word_ids = list(current_used)
    
    # Step 4: Update user_words.spoken_correct_count
    update_user_word_stats(db, str(current_user.id), detected_word_ids, "voice")
    
    # Step 5: Generate assistant_text via OpenAI
    situation = db.query(Situation).filter(Situation.id == conversation.situation_id).first()
    target_words = [f"{w.spanish} ({w.english})" for w in words]
    used_words = [w.spanish for w in words if w.id in (conversation.used_spoken_word_ids or [])]
    missing_words = [w.spanish for w in words if w.id not in (conversation.used_spoken_word_ids or [])]
    
    system_prompt = """You are a voice conversation coach in an expat survival Spanish app.
You always speak in English.
Keep replies short (max 15 words).
Ask a question that forces use of missing Spanish target words.
Do not introduce new Spanish.
Return JSON with keys:
- assistant_text
- end_conversation"""
    
    user_prompt = f"""Situation: {situation.title}
Target Spanish words: {', '.join(target_words)}
Already spoken: {', '.join(used_words) if used_words else 'None'}
User transcript: {user_transcript}

Return JSON only."""
    
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

