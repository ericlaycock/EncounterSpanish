from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.database import Base


class LLMRequest(Base):
    __tablename__ = "llm_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(String, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    prompt_version = Column(String, nullable=True)
    agent_id = Column(String, nullable=True)
    messages_json = Column(JSONB, nullable=True)
    temperature = Column(Float, nullable=True)
    max_tokens = Column(Integer, nullable=True)
    success = Column(Boolean, default=False, nullable=False)
    response_json = Column(JSONB, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    tokens_in = Column(Integer, nullable=True)
    tokens_out = Column(Integer, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    error_code = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class STTRequest(Base):
    __tablename__ = "stt_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(String, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    audio_sha256 = Column(String, nullable=True)
    audio_bytes = Column(Integer, nullable=True)
    audio_format = Column(String, nullable=True)
    language = Column(String, nullable=True)
    success = Column(Boolean, default=False, nullable=False)
    transcript_text = Column(Text, nullable=True)
    output_json = Column(JSONB, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    error_code = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TTSRequest(Base):
    __tablename__ = "tts_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(String, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    voice = Column(String, nullable=True)
    input_text_sha256 = Column(String, nullable=True)
    input_chars = Column(Integer, nullable=True)
    output_format = Column(String, nullable=True)
    success = Column(Boolean, default=False, nullable=False)
    audio_bytes = Column(Integer, nullable=True)
    audio_path = Column(String, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    error_code = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
