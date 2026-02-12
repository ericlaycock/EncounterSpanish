from sqlalchemy.orm import Session
from app.models import User, Subscription, UserSituation, Situation

FREE_SITUATIONS_LIMIT = 5


def get_subscription_status(db: Session, user_id: str) -> dict:
    """Get subscription status and free situations info"""
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    
    if not subscription:
        # Create default subscription if it doesn't exist
        subscription = Subscription(user_id=user_id, active=False)
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
    
    # Count completed free situations
    completed_free_situations = db.query(UserSituation).join(Situation).filter(
        UserSituation.user_id == user_id,
        UserSituation.completed_at.isnot(None),
        Situation.is_free == True
    ).count()
    
    free_situations_remaining = max(0, FREE_SITUATIONS_LIMIT - completed_free_situations)
    
    return {
        "active": subscription.active,
        "free_situations_limit": FREE_SITUATIONS_LIMIT,
        "free_situations_completed": completed_free_situations,
        "free_situations_remaining": free_situations_remaining
    }


def check_paywall(db: Session, user_id: str, situation_id: str) -> tuple[bool, str]:
    """
    Check if user can access a situation.
    Returns (allowed, error_message)
    Business rule: First 5 situations are free. If subscription.active = false 
    AND user completed >= 5 situations, any non-free situation returns PAYWALL.
    """
    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if not situation:
        return False, "SITUATION_NOT_FOUND"
    
    # Free situations are always accessible
    if situation.is_free:
        return True, None
    
    # For non-free situations, check subscription
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    
    # If subscription is active, allow access
    if subscription and subscription.active:
        return True, None
    
    # If no active subscription, check if user has completed 5+ situations
    completed_situations = db.query(UserSituation).filter(
        UserSituation.user_id == user_id,
        UserSituation.completed_at.isnot(None)
    ).count()
    
    # If user completed 5+ situations without active subscription, block non-free
    if completed_situations >= FREE_SITUATIONS_LIMIT:
        return False, "PAYWALL"
    
    # User hasn't completed 5 yet, allow access to non-free situations
    return True, None

