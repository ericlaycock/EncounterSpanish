"""Frontend logging endpoint"""
from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.core.logger import log_event

router = APIRouter()


class FrontendLogRequest(BaseModel):
    """Schema for frontend log events"""
    level: str
    event: str
    message: str
    request_id: str
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = {}


@router.post("")
async def log_frontend_event(
    log_data: FrontendLogRequest,
    request: Request
):
    """
    Receive and log frontend events.
    Only emits to stdout (Better Stack), does not store in Postgres.
    """
    # Get user_id from request state if available (from auth)
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        user_id = str(user_id)
    elif log_data.user_id:
        user_id = log_data.user_id
    
    # Merge metadata into extra fields
    extra = log_data.metadata.copy()
    
    # Log the event
    log_event(
        level=log_data.level,
        event=log_data.event,
        message=log_data.message,
        request_id=log_data.request_id,
        user_id=user_id,
        extra=extra
    )
    
    return {"status": "logged"}

