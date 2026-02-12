from sqlalchemy.orm import Session
from app.models import Conversation, UserWord, Word
from typing import List


def check_conversation_complete(conversation: Conversation, mode: str) -> bool:
    """Check if conversation is complete based on mode"""
    if mode == "text":
        used_word_ids = set(conversation.used_typed_word_ids or [])
    else:  # voice
        used_word_ids = set(conversation.used_spoken_word_ids or [])
    
    target_word_ids = set(conversation.target_word_ids or [])
    
    return target_word_ids.issubset(used_word_ids)


def update_user_word_stats(
    db: Session,
    user_id: str,
    word_ids: List[str],
    mode: str
):
    """Update user word statistics"""
    for word_id in word_ids:
        user_word = db.query(UserWord).filter(
            UserWord.user_id == user_id,
            UserWord.word_id == word_id
        ).first()
        
        if user_word:
            if mode == "text":
                user_word.typed_correct_count += 1
            else:  # voice
                user_word.spoken_correct_count += 1
                # If spoken_correct_count >= 2, mark as mastered
                if user_word.spoken_correct_count >= 2:
                    user_word.status = "mastered"
        else:
            # Create new user_word entry
            user_word = UserWord(
                user_id=user_id,
                word_id=word_id,
                seen_count=1,
                typed_correct_count=1 if mode == "text" else 0,
                spoken_correct_count=1 if mode == "voice" else 0,
                status="mastered" if mode == "voice" else "learning"
            )
            db.add(user_word)
    
    db.commit()


def get_missing_word_ids(conversation: Conversation, mode: str) -> List[str]:
    """Get list of word IDs that haven't been used yet"""
    if mode == "text":
        used_word_ids = set(conversation.used_typed_word_ids or [])
    else:  # voice
        used_word_ids = set(conversation.used_spoken_word_ids or [])
    
    target_word_ids = set(conversation.target_word_ids or [])
    missing = target_word_ids - used_word_ids
    
    return list(missing)

