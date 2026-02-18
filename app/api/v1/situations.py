from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
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
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class SelectedSituationProgress(BaseModel):
    category: str
    category_name: str
    current_situation_id: str
    current_situation_title: str
    progress: int  # e.g., 2/50
    total_in_series: int = 50


@router.get("/selected", response_model=List[SelectedSituationProgress])
async def get_selected_situations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's selected situations with progress"""
    if not current_user.onboarding_completed or not current_user.selected_situation_categories:
        return []
    
    selected_categories = current_user.selected_situation_categories
    result = []
    
    # Get all completed situations for this user
    completed_situations = {
        us.situation_id: us
        for us in db.query(UserSituation).filter(
            and_(
                UserSituation.user_id == current_user.id,
                UserSituation.completed_at.isnot(None)
            )
        ).all()
    }
    
    for category_id in selected_categories:
        # Get all situations in this category
        category_situations = db.query(Situation).filter(
            Situation.category == category_id
        ).order_by(Situation.series_number).all()
        
        if not category_situations:
            continue
        
        # Find the next situation to complete
        next_situation = None
        completed_count = 0
        
        for situation in category_situations:
            if situation.id in completed_situations:
                completed_count += 1
            elif next_situation is None:
                next_situation = situation
        
        # If all are completed, use the last one
        if next_situation is None:
            next_situation = category_situations[-1]
        
        # Map category ID to display name
        category_map = {
            "airport": "Airport",
            "banking": "Banking",
            "clothing": "Clothing Shopping",
            "internet": "Internet",
            "small_talk": "Small Talk",
            "contractor": "Home Renovation",
            "groceries": "Groceries",
            "mechanic": "Mechanic",
            "police": "Police Stop",
            "restaurant": "Eating Out",
        }
        
        result.append(SelectedSituationProgress(
            category=category_id,
            category_name=category_map.get(category_id, category_id.replace("_", " ").title()),
            current_situation_id=next_situation.id,
            current_situation_title=next_situation.title,
            progress=completed_count + 1,  # +1 because we're showing the next one
            total_in_series=50
        ))
    
    return result


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
    
    # Get 3 encounter words for this situation
    situation_words = db.query(SituationWord).filter(
        SituationWord.situation_id == situation_id
    ).order_by(SituationWord.position).all()
    
    encounter_word_ids = [sw.word_id for sw in situation_words]
    encounter_words = db.query(Word).filter(Word.id.in_(encounter_word_ids)).all()
    
    # Get 2 highest frequency words user hasn't learned yet
    learned_word_ids = set(
        word_id[0] for word_id in 
        db.query(UserWord.word_id).filter(UserWord.user_id == current_user.id).all()
    )
    
    # Get high frequency words user hasn't learned, ordered by frequency_rank
    high_freq_words = db.query(Word).filter(
        Word.word_category == 'high_frequency',
        ~Word.id.in_(learned_word_ids) if learned_word_ids else True
    ).order_by(Word.frequency_rank.asc().nullslast()).limit(2).all()
    
    # Combine: 3 encounter words + 2 high frequency words = 5 total
    all_words = list(encounter_words) + list(high_freq_words)
    
    # Sort encounter words by position, then append high frequency words
    word_dict = {w.id: w for w in encounter_words}
    sorted_encounter_words = [word_dict[sw.word_id] for sw in situation_words]
    final_words = sorted_encounter_words + list(high_freq_words)
    
    return SituationDetail(
        id=situation.id,
        title=situation.title,
        free=situation.is_free,
        words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english, notes=w.notes) for w in final_words]
    )


@router.post("/{situation_id}/start", response_model=StartSituationResponse)
async def start_situation(
    situation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a situation: create/get conversation (single source of truth for words), upsert user_words, create user_situation"""
    from app.models import Conversation
    from app.services.word_detection import get_words_by_ids
    
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
    
    # Get or create conversation - THIS IS THE SINGLE SOURCE OF TRUTH FOR WORDS
    conversation = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.situation_id == situation_id,
        Conversation.mode == "text"
    ).order_by(Conversation.created_at.desc()).first()
    
    if conversation and conversation.target_word_ids:
        # Reuse existing conversation's words
        target_word_ids = conversation.target_word_ids
        words = get_words_by_ids(db, target_word_ids)
    else:
        # Create new conversation with word selection
        # Get 3 encounter words for this situation
        situation_words = db.query(SituationWord).filter(
            SituationWord.situation_id == situation_id
        ).order_by(SituationWord.position).all()
        
        encounter_word_ids = [sw.word_id for sw in situation_words]
        
        # Get 2 highest frequency words user hasn't learned yet
        learned_word_ids = set(
            word_id[0] for word_id in 
            db.query(UserWord.word_id).filter(UserWord.user_id == current_user.id).all()
        )
        
        # Get high frequency words user hasn't learned, ordered by frequency_rank
        high_freq_words = db.query(Word).filter(
            Word.word_category == 'high_frequency',
            ~Word.id.in_(learned_word_ids) if learned_word_ids else True
        ).order_by(Word.frequency_rank.asc().nullslast()).limit(2).all()
        
        # Combine: 3 encounter words + 2 high frequency words = 5 total
        high_freq_word_ids = [w.id for w in high_freq_words]
        target_word_ids = encounter_word_ids + high_freq_word_ids
        
        # Get all words
        all_word_ids = encounter_word_ids + high_freq_word_ids
        words = db.query(Word).filter(Word.id.in_(all_word_ids)).all()
        
        # Create conversation with these words (text mode as source of truth for words)
        conversation = Conversation(
            user_id=current_user.id,
            situation_id=situation_id,
            mode="text",  # Text mode conversation stores the word selection (even though text chat UI is removed)
            target_word_ids=target_word_ids,
            used_typed_word_ids=[],
            used_spoken_word_ids=[]
        )
        db.add(conversation)
    
    # Upsert user_words and increment seen_count for all words
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
    db.refresh(conversation)
    
    # Sort words: encounter words by position, then high frequency words
    word_dict = {w.id: w for w in words}
    situation_words = db.query(SituationWord).filter(
        SituationWord.situation_id == situation_id
    ).order_by(SituationWord.position).all()
    encounter_word_ids = [sw.word_id for sw in situation_words]
    high_freq_word_ids = [wid for wid in target_word_ids if wid not in encounter_word_ids]
    
    sorted_encounter_words = [word_dict[wid] for wid in encounter_word_ids if wid in word_dict]
    sorted_high_freq_words = [word_dict[wid] for wid in high_freq_word_ids if wid in word_dict]
    final_words = sorted_encounter_words + sorted_high_freq_words
    
    return StartSituationResponse(
        words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english, notes=w.notes) for w in final_words]
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
    
    # Find next situation in the same category
    current_situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if current_situation and current_situation.category:
        next_situation = db.query(Situation).filter(
            and_(
                Situation.category == current_situation.category,
                Situation.series_number > current_situation.series_number
            )
        ).order_by(Situation.series_number).first()
        
        next_situation_id = next_situation.id if next_situation else None
    else:
        # Fallback to old behavior
        next_situation = db.query(Situation).filter(
            Situation.order_index > current_situation.order_index
        ).order_by(Situation.order_index).first()
        next_situation_id = next_situation.id if next_situation else None
    
    return CompleteSituationResponse(next_situation_id=next_situation_id)
