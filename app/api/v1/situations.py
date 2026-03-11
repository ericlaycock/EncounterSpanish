from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.auth import get_current_user
from app.models import User, Situation, UserSituation, UserWord, Word, Conversation
from app.services.subscription_service import check_paywall
from app.schemas import (
    SituationListItem,
    SituationDetail,
    StartSituationResponse,
    CompleteSituationResponse,
    GrammarConfigResponse,
    WordSchema
)
from app.services.word_selection_service import (
    select_words_for_situation,
    sort_words_encounter_first,
    ensure_user_words,
)
from app.data.grammar_situations import get_grammar_config, get_all_grammar_situation_ids, GRAMMAR_SITUATIONS
from app.data.seed_bank import ANIMATION_NAMES
from app.services.catalan_service import apply_catalan_mode
from app.services.refresh_service import set_initial_mastery
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class AdminSituationItem(BaseModel):
    id: str
    title: str
    animation_type: str
    situation_type: str
    encounter_number: int


@router.get("/admin/all", response_model=List[AdminSituationItem])
async def get_admin_all_situations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Return all situations for admin users (no paywall/lock checks)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    situations = db.query(Situation).order_by(Situation.animation_type, Situation.order_index).all()
    return [
        AdminSituationItem(
            id=s.id,
            title=s.title,
            animation_type=s.animation_type,
            situation_type=s.situation_type,
            encounter_number=s.encounter_number,
        )
        for s in situations
    ]


def get_vocab_level(db: Session, user_id) -> int:
    """Count of high-frequency words with mastery_level >= 2 (refreshed at least once)."""
    return db.query(UserWord).join(Word).filter(
        UserWord.user_id == user_id,
        Word.word_category == 'high_frequency',
        UserWord.mastery_level >= 2,
    ).count()



class SelectedSituationProgress(BaseModel):
    animation_type: str
    animation_name: str
    current_situation_id: str
    current_situation_title: str
    current_situation_goal: Optional[str] = None
    progress: int  # e.g., 2/50
    total_encounters: int = 50
    vocab_level: int = 0


@router.get("/selected", response_model=List[SelectedSituationProgress])
async def get_selected_situations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's selected situations with progress"""
    if not current_user.onboarding_completed or not current_user.selected_animation_types:
        return []

    selected_categories = current_user.selected_animation_types
    vocab_level = get_vocab_level(db, current_user.id)
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
            Situation.animation_type == category_id
        ).order_by(Situation.encounter_number).all()

        if not category_situations:
            continue

        # Find the next situation to complete (first uncompleted)
        next_situation = None
        for situation in category_situations:
            if situation.id not in completed_situations:
                next_situation = situation
                break

        # If all are completed, use the last one
        if next_situation is None:
            next_situation = category_situations[-1]

        # Count progress within the current sub-situation (same title)
        sub_situations = [s for s in category_situations if s.title == next_situation.title]
        sub_completed = sum(1 for s in sub_situations if s.id in completed_situations)

        result.append(SelectedSituationProgress(
            animation_type=category_id,
            animation_name=ANIMATION_NAMES.get(category_id, category_id.replace("_", " ").title()),
            current_situation_id=next_situation.id,
            current_situation_title=next_situation.title,
            current_situation_goal=next_situation.goal,
            progress=sub_completed,
            total_encounters=len(sub_situations),
            vocab_level=vocab_level,
        ))
    
    return result


@router.get("/grammar-gates")
async def get_grammar_gates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get active grammar gates for the current user based on vocab level."""
    vocab_level = get_vocab_level(db, current_user.id)

    completed_situations = {
        us.situation_id
        for us in db.query(UserSituation).filter(
            UserSituation.user_id == current_user.id,
            UserSituation.completed_at.isnot(None)
        ).all()
    }

    gates = []
    for sid in get_all_grammar_situation_ids():
        cfg = GRAMMAR_SITUATIONS[sid]
        if cfg["vocab_level"] <= vocab_level and sid not in completed_situations:
            gates.append({
                "situation_id": sid,
                "title": cfg["title"],
                "vocab_level_required": cfg["vocab_level"],
                "video_embed_id": cfg["video_embed_id"],
            })

    return {
        "vocab_level": vocab_level,
        "gates": gates,
        "is_gated": len(gates) > 0,
    }


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
        
        # Check if locked (paywall) — admin sees everything unlocked
        if current_user.is_admin:
            is_locked = False
        else:
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

    # Check paywall (admin bypasses)
    if not current_user.is_admin:
        allowed, error = check_paywall(db, str(current_user.id), situation_id)
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": error}
            )

    # Select and sort words
    encounter_word_ids, high_freq_word_ids = select_words_for_situation(db, current_user.id, situation_id)
    target_word_ids = encounter_word_ids + high_freq_word_ids
    words = db.query(Word).filter(Word.id.in_(target_word_ids)).all()
    final_words = sort_words_encounter_first(words, situation_id, db, target_word_ids)

    # Catalan mode: swap spanish → catalan for encounter/HF words
    if current_user.catalan_mode:
        final_words = apply_catalan_mode(final_words, db)

    return SituationDetail(
        id=situation.id,
        title=situation.title,
        free=situation.is_free,
        encounter_number=situation.encounter_number,
        animation_type=situation.animation_type,
        goal=situation.goal,
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

    # Check paywall (admin bypasses)
    if not current_user.is_admin:
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
    ).order_by(Conversation.created_at.desc()).with_for_update().first()
    
    if conversation and conversation.target_word_ids:
        # Reuse existing conversation's words
        target_word_ids = conversation.target_word_ids
        words = get_words_by_ids(db, target_word_ids)
    else:
        # Create new conversation with word selection
        encounter_word_ids, high_freq_word_ids = select_words_for_situation(db, current_user.id, situation_id)
        target_word_ids = encounter_word_ids + high_freq_word_ids
        words = db.query(Word).filter(Word.id.in_(target_word_ids)).all()

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
    ensure_user_words(db, current_user.id, words)
    
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
    final_words = sort_words_encounter_first(words, situation_id, db, target_word_ids)

    # Catalan mode: swap spanish → catalan for encounter/HF words
    if current_user.catalan_mode:
        final_words = apply_catalan_mode(final_words, db)

    return StartSituationResponse(
        words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english, notes=w.notes) for w in final_words],
        encounter_number=situation.encounter_number,
        animation_type=situation.animation_type,
        goal=situation.goal,
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

    # Set initial mastery (level 0 → 1) for words from the text conversation
    text_conv = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.situation_id == situation_id,
        Conversation.mode == "text",
    ).order_by(Conversation.created_at.desc()).first()
    if text_conv and text_conv.target_word_ids:
        set_initial_mastery(db, current_user.id, text_conv.target_word_ids, situation_id)

    db.commit()

    # Find next situation in the same animation_type with matching title (same sub-situation)
    current_situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if current_situation and current_situation.animation_type:
        next_situation = db.query(Situation).filter(
            and_(
                Situation.animation_type == current_situation.animation_type,
                Situation.title == current_situation.title,
                Situation.encounter_number > current_situation.encounter_number
            )
        ).order_by(Situation.encounter_number).first()

        next_situation_id = next_situation.id if next_situation else None
    else:
        # Fallback to order_index
        next_situation = db.query(Situation).filter(
            Situation.order_index > current_situation.order_index
        ).order_by(Situation.order_index).first()
        next_situation_id = next_situation.id if next_situation else None
    
    return CompleteSituationResponse(next_situation_id=next_situation_id)


@router.get("/{situation_id}/grammar-config", response_model=GrammarConfigResponse)
async def get_grammar_config_endpoint(
    situation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get grammar config for a situation (phases, drill type, video embed, drill answers)."""
    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if not situation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Situation not found")

    config = get_grammar_config(situation_id)
    if not config:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a grammar situation")

    drill_config = None
    if config["drill_type"] == "article_matching" and "drill_config" in config:
        drill_config = config["drill_config"]
    elif config["drill_type"] in ("gustar", "gustar_prefix"):
        drill_config = config.get("drill_config")

    return GrammarConfigResponse(
        situation_type=situation.situation_type,
        video_embed_id=config["video_embed_id"],
        drill_type=config["drill_type"],
        tense=config["tense"],
        phases=config["phases"],
        drill_config=drill_config,
        phase_1c_config=config.get("phase_1c_config"),
        phase_2_config=config.get("phase_2_config"),
    )


