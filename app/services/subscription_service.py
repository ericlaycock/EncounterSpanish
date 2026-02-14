from sqlalchemy.orm import Session
from app.models import User, Subscription, UserSituation, Situation

FREE_ENCOUNTERS_LIMIT = 25


def get_subscription_status(db: Session, user_id: str) -> dict:
    """Get subscription status and free situations info"""
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    
    if not subscription:
        # Create default subscription if it doesn't exist
        subscription = Subscription(user_id=user_id, active=False)
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
    
    # Count completed encounters (all situations are now encounters)
    completed_encounters = db.query(UserSituation).filter(
        UserSituation.user_id == user_id,
        UserSituation.completed_at.isnot(None)
    ).count()
    
    free_encounters_remaining = max(0, FREE_ENCOUNTERS_LIMIT - completed_encounters)
    
    return {
        "active": subscription.active,
        "free_situations_limit": FREE_ENCOUNTERS_LIMIT,
        "free_situations_completed": completed_encounters,
        "free_situations_remaining": free_encounters_remaining
    }


def check_paywall(db: Session, user_id: str, situation_id: str) -> tuple[bool, str]:
    """
    Check if user can access an encounter.
    Returns (allowed, error_message)
    Business rule: Free users get 25 free encounters total.
    If subscription.active = false AND user completed >= 25 encounters, return PAYWALL.
    """
    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if not situation:
        return False, "SITUATION_NOT_FOUND"
    
    # Check subscription
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    
    # If subscription is active, allow access
    if subscription and subscription.active:
        return True, None
    
    # If no active subscription, check total completed encounters
    completed_encounters = db.query(UserSituation).filter(
        UserSituation.user_id == user_id,
        UserSituation.completed_at.isnot(None)
    ).count()
    
    # If user completed 25+ encounters without active subscription, block
    if completed_encounters >= FREE_ENCOUNTERS_LIMIT:
        return False, "PAYWALL"
    
    # User hasn't completed 25 yet, allow access
    return True, None

