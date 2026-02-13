from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    onboarding_completed = Column(Boolean, default=False, nullable=False)
    selected_situation_categories = Column(JSONB, nullable=True)  # List of category IDs user selected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    user_words = relationship("UserWord", back_populates="user")
    user_situations = relationship("UserSituation", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    active = Column(Boolean, default=False, nullable=False)
    tier = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscription")


class Word(Base):
    __tablename__ = "words"
    
    id = Column(String, primary_key=True)
    spanish = Column(String, nullable=False)
    english = Column(String, nullable=False)
    
    # Relationships
    situation_words = relationship("SituationWord", back_populates="word")
    user_words = relationship("UserWord", back_populates="word")


class Situation(Base):
    __tablename__ = "situations"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)  # e.g., "banking", "small_talk", "groceries"
    series_number = Column(Integer, nullable=False)  # e.g., 1, 2, 3 for Banking 1, Banking 2, etc.
    order_index = Column(Integer, nullable=False, index=True)
    is_free = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    situation_words = relationship("SituationWord", back_populates="situation", order_by="SituationWord.position")
    user_situations = relationship("UserSituation", back_populates="situation")
    conversations = relationship("Conversation", back_populates="situation")


class SituationWord(Base):
    __tablename__ = "situation_words"
    
    situation_id = Column(String, ForeignKey("situations.id"), primary_key=True)
    word_id = Column(String, ForeignKey("words.id"), primary_key=True)
    position = Column(Integer, nullable=False)
    
    # Relationships
    situation = relationship("Situation", back_populates="situation_words")
    word = relationship("Word", back_populates="situation_words")


class UserWord(Base):
    __tablename__ = "user_words"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    word_id = Column(String, ForeignKey("words.id"), primary_key=True)
    seen_count = Column(Integer, default=0, nullable=False)
    typed_correct_count = Column(Integer, default=0, nullable=False)
    spoken_correct_count = Column(Integer, default=0, nullable=False)
    status = Column(String, default="learning", nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="user_words")
    word = relationship("Word", back_populates="user_words")


class UserSituation(Base):
    __tablename__ = "user_situations"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    situation_id = Column(String, ForeignKey("situations.id"), primary_key=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="user_situations")
    situation = relationship("Situation", back_populates="user_situations")


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    situation_id = Column(String, ForeignKey("situations.id"), nullable=False)
    mode = Column(String, nullable=False)  # 'text' or 'voice'
    target_word_ids = Column(JSONB, nullable=False)
    used_typed_word_ids = Column(JSONB, default=list, nullable=False)
    used_spoken_word_ids = Column(JSONB, default=list, nullable=False)
    status = Column(String, default="active", nullable=False)  # 'active' or 'complete'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    situation = relationship("Situation", back_populates="conversations")



