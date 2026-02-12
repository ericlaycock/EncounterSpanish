from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from uuid import UUID


# Auth schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    user_id: UUID


# Subscription schemas
class SubscriptionStatusResponse(BaseModel):
    active: bool
    free_situations_limit: int = 5
    free_situations_completed: int
    free_situations_remaining: int


# Situation schemas
class WordSchema(BaseModel):
    id: str
    spanish: str
    english: str

    class Config:
        from_attributes = True


class SituationListItem(BaseModel):
    id: str
    title: str
    is_locked: bool
    completed: bool
    free: bool

    class Config:
        from_attributes = True


class SituationDetail(BaseModel):
    id: str
    title: str
    free: bool
    words: List[WordSchema]

    class Config:
        from_attributes = True


class StartSituationResponse(BaseModel):
    words: List[WordSchema]


class CompleteSituationResponse(BaseModel):
    next_situation_id: Optional[str] = None


# User Words schemas
class UserWordSchema(BaseModel):
    word_id: str
    spanish: str
    english: str
    seen_count: int
    typed_correct_count: int
    spoken_correct_count: int
    status: str

    class Config:
        from_attributes = True


class TypedCorrectRequest(BaseModel):
    word_ids: List[str]


# Conversation schemas
class CreateConversationRequest(BaseModel):
    situation_id: str
    mode: str  # 'text' or 'voice'


class CreateConversationResponse(BaseModel):
    conversation_id: UUID


class MessageRequest(BaseModel):
    text: str


class MessageResponse(BaseModel):
    detected_word_ids: List[str]
    missing_word_ids: List[str]


class VoiceTurnResponse(BaseModel):
    user_transcript: str
    detected_word_ids: List[str]
    missing_word_ids: List[str]
    assistant_text: str
    assistant_audio_url: str
    conversation_complete: bool


# Error schemas
class ErrorResponse(BaseModel):
    error: str

