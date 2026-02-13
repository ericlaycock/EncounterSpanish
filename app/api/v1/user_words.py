from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User, UserWord, Word
from app.schemas import UserWordSchema, TypedCorrectRequest

router = APIRouter()


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



