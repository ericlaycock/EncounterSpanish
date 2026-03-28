from datetime import datetime, timezone, time
from sqlalchemy.orm import Session
from app.models import DailyEncounterLog

DAILY_ENCOUNTER_LIMIT = 30


def get_daily_encounter_usage(db: Session, user_id) -> dict:
    """Count encounters consumed today (UTC)."""
    today_start = datetime.combine(datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc)

    count = db.query(DailyEncounterLog).filter(
        DailyEncounterLog.user_id == user_id,
        DailyEncounterLog.created_at >= today_start,
    ).count()

    return {
        "encounters_used": count,
        "encounters_limit": DAILY_ENCOUNTER_LIMIT,
        "encounters_remaining": max(0, DAILY_ENCOUNTER_LIMIT - count),
    }


def check_daily_limit(db: Session, user_id) -> tuple[bool, str | None]:
    """Returns (allowed, error_message)."""
    usage = get_daily_encounter_usage(db, user_id)
    if usage["encounters_remaining"] <= 0:
        return False, "DAILY_LIMIT_REACHED"
    return True, None


def record_encounter(db: Session, user_id, situation_id: str):
    """Record one daily encounter consumed."""
    log = DailyEncounterLog(user_id=user_id, situation_id=situation_id)
    db.add(log)
