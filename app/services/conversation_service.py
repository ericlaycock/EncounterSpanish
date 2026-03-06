from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models import Conversation, UserWord, Word
from app.config import settings
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
        if mode == "text":
            stmt = insert(UserWord).values(
                user_id=user_id,
                word_id=word_id,
                seen_count=1,
                typed_correct_count=1,
                spoken_correct_count=0,
                status="learning"
            ).on_conflict_do_update(
                index_elements=["user_id", "word_id"],
                set_={"typed_correct_count": UserWord.typed_correct_count + 1}
            )
            db.execute(stmt)
        else:  # voice
            stmt = insert(UserWord).values(
                user_id=user_id,
                word_id=word_id,
                seen_count=1,
                typed_correct_count=0,
                spoken_correct_count=1,
                status="learning"
            ).on_conflict_do_update(
                index_elements=["user_id", "word_id"],
                set_={"spoken_correct_count": UserWord.spoken_correct_count + 1}
            )
            db.execute(stmt)
            # Update status if mastery threshold met
            db.query(UserWord).filter(
                UserWord.user_id == user_id,
                UserWord.word_id == word_id,
                UserWord.spoken_correct_count >= settings.mastery_spoken_threshold
            ).update({"status": "mastered"})

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



