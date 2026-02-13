from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User, Situation, SituationWord, UserSituation, UserWord, Word
from app.services.subscription_service import check_paywall
from app.schemas import (
    SituationListItem,
    SituationDetail,
    StartSituationResponse,
    CompleteSituationResponse,
    WordSchema
)

router = APIRouter()


@router.get("", response_model=list[SituationListItem])
async def list_situations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all situations with lock/completion status"""
    situations = db.query(Situation).order_by(Situation.order_index).all()
    user_situations = {
        us.situation_id: us
        for us in db.query(UserSituation).filter(
            UserSituation.user_id == current_user.id
        ).all()
    }
    
    result = []
    for situation in situations:
        user_situation = user_situations.get(situation.id)
        completed = user_situation is not None and user_situation.completed_at is not None
        
        # Check if locked (paywall)
        allowed, _ = check_paywall(db, str(current_user.id), situation.id)
        is_locked = not allowed
        
        result.append(SituationListItem(
            id=situation.id,
            title=situation.title,
            is_locked=is_locked,
            completed=completed,
            free=situation.is_free
        ))
    
    return result


@router.get("/{situation_id}", response_model=SituationDetail)
async def get_situation(
    situation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get situation details with words"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"🔍 GET /v1/situations/{situation_id} - User: {current_user.id}")
    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if not situation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Situation not found"
        )
    
    # Check paywall
    allowed, error = check_paywall(db, str(current_user.id), situation_id)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": error}
        )
    
    # Get words for this situation
    situation_words = db.query(SituationWord).filter(
        SituationWord.situation_id == situation_id
    ).order_by(SituationWord.position).all()
    
    word_ids = [sw.word_id for sw in situation_words]
    words = db.query(Word).filter(Word.id.in_(word_ids)).all()
    
    # Sort words by position
    word_dict = {w.id: w for w in words}
    sorted_words = [word_dict[sw.word_id] for sw in situation_words]
    
    return SituationDetail(
        id=situation.id,
        title=situation.title,
        free=situation.is_free,
        words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english) for w in sorted_words]
    )


@router.post("/{situation_id}/start", response_model=StartSituationResponse)
async def start_situation(
    situation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a situation: upsert user_words and increment seen_count"""
    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if not situation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Situation not found"
        )
    
    # Check paywall
    allowed, error = check_paywall(db, str(current_user.id), situation_id)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": error}
        )
    
    # Get words for this situation
    situation_words = db.query(SituationWord).filter(
        SituationWord.situation_id == situation_id
    ).order_by(SituationWord.position).all()
    
    word_ids = [sw.word_id for sw in situation_words]
    words = db.query(Word).filter(Word.id.in_(word_ids)).all()
    
    # Upsert user_words and increment seen_count
    for word in words:
        user_word = db.query(UserWord).filter(
            UserWord.user_id == current_user.id,
            UserWord.word_id == word.id
        ).first()
        
        if user_word:
            user_word.seen_count += 1
        else:
            user_word = UserWord(
                user_id=current_user.id,
                word_id=word.id,
                seen_count=1
            )
            db.add(user_word)
    
    # Create or update user_situation
    user_situation = db.query(UserSituation).filter(
        UserSituation.user_id == current_user.id,
        UserSituation.situation_id == situation_id
    ).first()
    
    if not user_situation:
        user_situation = UserSituation(
            user_id=current_user.id,
            situation_id=situation_id
        )
        db.add(user_situation)
    
    db.commit()
    
    # Sort words by position
    word_dict = {w.id: w for w in words}
    sorted_words = [word_dict[sw.word_id] for sw in situation_words]
    
    return StartSituationResponse(
        words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english) for w in sorted_words]
    )


@router.post("/{situation_id}/complete", response_model=CompleteSituationResponse)
async def complete_situation(
    situation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark situation as completed and return next situation ID"""
    user_situation = db.query(UserSituation).filter(
        UserSituation.user_id == current_user.id,
        UserSituation.situation_id == situation_id
    ).first()
    
    if not user_situation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Situation not started"
        )
    
    from datetime import datetime
    user_situation.completed_at = datetime.utcnow()
    db.commit()
    
    # Find next situation
    current_situation = db.query(Situation).filter(Situation.id == situation_id).first()
    next_situation = db.query(Situation).filter(
        Situation.order_index > current_situation.order_index
    ).order_by(Situation.order_index).first()
    
    next_situation_id = next_situation.id if next_situation else None
    
    return CompleteSituationResponse(next_situation_id=next_situation_id)

