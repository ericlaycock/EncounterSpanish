from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User
from app.services.subscription_service import get_subscription_status
from app.schemas import SubscriptionStatusResponse

router = APIRouter()


@router.get("/status", response_model=SubscriptionStatusResponse)
async def get_subscription_status_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get subscription status and free situations info"""
    status_info = get_subscription_status(db, str(current_user.id))
    return SubscriptionStatusResponse(**status_info)



