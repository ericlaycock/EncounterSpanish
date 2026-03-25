from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from uuid import UUID


# Auth schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    invite_token: str = ""


class LoginResponse(BaseModel):
    access_token: str
    user_id: UUID
    is_admin: bool = False
    catalan_mode: bool = False
    email: str


class UserProfileResponse(BaseModel):
    email: str
    created_at: datetime
    is_admin: bool = False
    catalan_mode: bool = False


class CatalanModeRequest(BaseModel):
    enabled: bool


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
    notes: Optional[str] = None

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
    encounter_number: int = 1
    animation_type: str = ""
    goal: Optional[str] = None
    words: List[WordSchema]

    class Config:
        from_attributes = True


class StartSituationResponse(BaseModel):
    words: List[WordSchema]
    encounter_number: int = 1
    animation_type: str = ""
    goal: Optional[str] = None


class CompleteSituationResponse(BaseModel):
    next_situation_id: Optional[str] = None


class AdminSkipEncounterResponse(BaseModel):
    situation_id: str
    situation_title: str
    words_set_known: int
    vocab_level: int
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
    mastery_level: int = 0
    next_refresh_at: Optional[datetime] = None
    word_category: Optional[str] = None
    frequency_rank: Optional[int] = None

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
    words: List[WordSchema]  # Return the words used in this conversation
    initial_message: str  # Custom initial message for this encounter
    initial_audio_url: Optional[str] = None  # TTS audio for the initial message
    language_mode: str = "english"  # "english", "spanish_text", or "spanish_audio"
    vocab_level: int = 0
    system_prompt: Optional[str] = None  # System prompt for multi-turn message history


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


# Grammar config schemas
class GrammarConfigResponse(BaseModel):
    situation_type: str
    video_embed_id: Optional[str] = None
    drill_type: Optional[str] = None
    tense: Optional[str] = None
    phases: dict
    drill_config: Optional[dict] = None
    phase_1c_config: Optional[dict] = None
    phase_2_config: Optional[dict] = None


# Refresh (SRS) schemas
class PendingRefreshSituation(BaseModel):
    situation_id: str
    title: str
    animation_type: str
    due_word_count: int

class PendingRefreshesResponse(BaseModel):
    refreshes: List[PendingRefreshSituation]

class StartRefreshResponse(BaseModel):
    conversation_id: UUID
    words: List[WordSchema]
    initial_message: str
    language_mode: str = "english"
    conversation_type: str = "refresh"

class CompleteRefreshResponse(BaseModel):
    words_refreshed: int
    new_mastery_level: int


# Error schemas
class ErrorResponse(BaseModel):
    error: str


