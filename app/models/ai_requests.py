"""SQLAlchemy models for AI request logging (LLM, STT, TTS)"""
from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.database import Base


class LLMRequest(Base):
    """Table for logging LLM chat completion requests"""
    __tablename__ = "llm_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    request_id = Column(String, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    provider = Column(String, nullable=False, default="openai")
    model = Column(String, nullable=False)
    prompt_version = Column(String, nullable=False, index=True)
    agent_id = Column(String, nullable=False, index=True)
    
    messages_json = Column(JSONB, nullable=False)
    response_json = Column(JSONB, nullable=True)
    
    temperature = Column(Float, nullable=True)
    max_tokens = Column(Integer, nullable=True)
    tokens_in = Column(Integer, nullable=True)
    tokens_out = Column(Integer, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    
    latency_ms = Column(Integer, nullable=True)
    success = Column(Boolean, nullable=False, default=False, index=True)
    error_code = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)


class STTRequest(Base):
    """Table for logging Speech-to-Text requests"""
    __tablename__ = "stt_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    request_id = Column(String, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    provider = Column(String, nullable=False, default="openai")
    model = Column(String, nullable=False)
    audio_sha256 = Column(String, nullable=True)  # Hash of audio bytes
    audio_bytes = Column(Integer, nullable=True)  # Size in bytes
    audio_format = Column(String, nullable=True)  # wav/mp3/webm
    language = Column(String, nullable=True)  # es, en, etc.
    
    latency_ms = Column(Integer, nullable=True)
    success = Column(Boolean, nullable=False, default=False, index=True)
    error_code = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    
    transcript_text = Column(Text, nullable=True)
    output_json = Column(JSONB, nullable=True)
    estimated_cost = Column(Float, nullable=True)


class TTSRequest(Base):
    """Table for logging Text-to-Speech requests"""
    __tablename__ = "tts_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    request_id = Column(String, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    provider = Column(String, nullable=False, default="openai")
    model = Column(String, nullable=False)
    voice = Column(String, nullable=True)  # alloy, echo, etc.
    input_text_sha256 = Column(String, nullable=True)  # Hash of input text
    input_chars = Column(Integer, nullable=True)  # Character count
    
    latency_ms = Column(Integer, nullable=True)
    success = Column(Boolean, nullable=False, default=False, index=True)
    error_code = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    
    audio_bytes = Column(Integer, nullable=True)  # Size of generated audio
    output_format = Column(String, nullable=True)  # mp3/wav
    audio_path = Column(String, nullable=True)  # Local file path
    estimated_cost = Column(Float, nullable=True)

