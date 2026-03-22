from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User, Conversation, Situation, Word
from app.schemas import (
    PendingRefreshesResponse,
    PendingRefreshSituation,
    StartRefreshResponse,
    CompleteRefreshResponse,
    WordSchema,
)
from app.services.refresh_service import (
    get_pending_refreshes,
    get_due_word_ids,
    bump_mastery_after_refresh,
)
from app.services.word_detection import get_words_by_ids
from app.services.encounter_messages import get_initial_message_for_encounter
from app.api.v1.situations import get_vocab_level
from app.services.voice_turn_service import get_language_mode

router = APIRouter()


@router.post("/admin/skip-time")
async def admin_skip_time(
    hours: int = 25,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Admin only: move all next_refresh_at timestamps back by N hours.
    Presets: 25 (skip 1 day), 169 (skip 1 week), 745 (skip 1 month).
    Makes time-gated words immediately due for refresh."""
    from app.models import UserWord
    from datetime import timedelta
    import logging

    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    logger = logging.getLogger(__name__)

    result = db.query(UserWord).filter(
        UserWord.user_id == current_user.id,
        UserWord.next_refresh_at.isnot(None),
    ).update(
        {UserWord.next_refresh_at: UserWord.next_refresh_at - timedelta(hours=hours)},
        synchronize_session="fetch",
    )
    db.commit()

    logger.info(f"[Admin] skip-time: moved {result} word refresh timestamps back {hours}h for user {current_user.id}")
    return {"words_updated": result, "hours_skipped": hours}


@router.get("/pending", response_model=PendingRefreshesResponse)
async def pending_refreshes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get situations with words due for refresh."""
    refreshes = get_pending_refreshes(db, current_user.id)
    return PendingRefreshesResponse(
        refreshes=[PendingRefreshSituation(**r) for r in refreshes]
    )


@router.post("/{situation_id}/start", response_model=StartRefreshResponse)
async def start_refresh(
    situation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Start a refresh session for a situation's due words."""
    due_word_ids = get_due_word_ids(db, current_user.id, situation_id)
    if not due_word_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No words due for refresh in this situation",
        )

    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if not situation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Situation not found",
        )

    # Create a refresh conversation
    conversation = Conversation(
        user_id=current_user.id,
        situation_id=situation_id,
        mode="voice",
        conversation_type="refresh",
        target_word_ids=due_word_ids,
        used_typed_word_ids=[],
        used_spoken_word_ids=[],
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    words = get_words_by_ids(db, due_word_ids)
    initial_message = get_initial_message_for_encounter(situation.title)
    vocab_level = get_vocab_level(db, current_user.id)
    language_mode = get_language_mode(situation.encounter_number, vocab_level)

    return StartRefreshResponse(
        conversation_id=conversation.id,
        words=[WordSchema(id=w.id, spanish=w.spanish, english=w.english, notes=w.notes) for w in words],
        initial_message=initial_message,
        language_mode=language_mode,
    )


@router.post("/{situation_id}/complete", response_model=CompleteRefreshResponse)
async def complete_refresh(
    situation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Complete a refresh session — bump mastery for all due words."""
    count, new_level = bump_mastery_after_refresh(db, current_user.id, situation_id)
    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No words due for refresh in this situation",
        )
    db.commit()
    return CompleteRefreshResponse(words_refreshed=count, new_mastery_level=new_level)
