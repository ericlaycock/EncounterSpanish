from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from app.database import get_db
from app.auth import get_current_user
from app.models import User, UserWord, Word
from app.schemas import UserWordSchema, TypedCorrectRequest
from pydantic import BaseModel

router = APIRouter()


class UnknownWordSchema(BaseModel):
    word_id: str
    spanish: str
    english: str
    word_category: Optional[str]  # 'high_frequency' or 'encounter'
    frequency_rank: Optional[int]


@router.get("", response_model=list[UserWordSchema])
async def get_user_words(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user word progress"""
    user_words = db.query(UserWord).filter(
        UserWord.user_id == current_user.id
    ).all()
    
    # Get word details
    word_ids = [uw.word_id for uw in user_words]
    words = db.query(Word).filter(Word.id.in_(word_ids)).all()
    word_dict = {w.id: w for w in words}
    
    result = []
    for uw in user_words:
        word = word_dict.get(uw.word_id)
        if word:
            result.append(UserWordSchema(
                word_id=uw.word_id,
                spanish=word.spanish,
                english=word.english,
                seen_count=uw.seen_count,
                typed_correct_count=uw.typed_correct_count,
                spoken_correct_count=uw.spoken_correct_count,
                status=uw.status
            ))
    
    return result


@router.post("/typed-correct")
async def mark_typed_correct(
    request: TypedCorrectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Increment typed_correct_count for specified words"""
    for word_id in request.word_ids:
        user_word = db.query(UserWord).filter(
            UserWord.user_id == current_user.id,
            UserWord.word_id == word_id
        ).first()
        
        if user_word:
            user_word.typed_correct_count += 1
        else:
            # Create if doesn't exist
            user_word = UserWord(
                user_id=current_user.id,
                word_id=word_id,
                typed_correct_count=1
            )
            db.add(user_word)
    
    db.commit()
    return {"message": "Updated"}


@router.get("/unknown", response_model=dict)
async def get_unknown_words(
    category: Optional[str] = Query(None, description="Filter by category: 'high_frequency' or 'encounter'"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get unknown words (words user hasn't learned yet) grouped by category"""
    
    # Get all words user has learned (has UserWord entry)
    learned_word_ids = set(
        word_id[0] for word_id in 
        db.query(UserWord.word_id).filter(UserWord.user_id == current_user.id).all()
    )
    
    # Build query for unknown words
    query = db.query(Word).filter(
        ~Word.id.in_(learned_word_ids) if learned_word_ids else True
    )
    
    # Filter by category if provided
    if category:
        query = query.filter(Word.word_category == category)
    else:
        # Only return words with a category (high_frequency or encounter)
        query = query.filter(Word.word_category.isnot(None))
    
    unknown_words = query.order_by(Word.frequency_rank.asc().nullslast(), Word.spanish.asc()).all()
    
    # Group by category
    high_frequency = []
    encounter = []
    
    for word in unknown_words:
        word_data = UnknownWordSchema(
            word_id=word.id,
            spanish=word.spanish,
            english=word.english,
            word_category=word.word_category,
            frequency_rank=word.frequency_rank
        )
        
        if word.word_category == 'high_frequency':
            high_frequency.append(word_data)
        elif word.word_category == 'encounter':
            encounter.append(word_data)
    
    return {
        "high_frequency": high_frequency,
        "encounter": encounter
    }


