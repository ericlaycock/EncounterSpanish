from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app.auth import get_current_user
from app.models import User, Situation

router = APIRouter()


class SaveOnboardingSelectionsRequest(BaseModel):
    selected_category: str | None = None  # FE sends this name
    selected_animation_type: str | None = None  # Legacy name

    @property
    def animation_type(self) -> str:
        value = self.selected_category or self.selected_animation_type
        if not value:
            raise ValueError("Either selected_category or selected_animation_type is required")
        return value

    dialect: str  # 'mexico', 'colombia', 'costa_rica'
    grammar_score: str | None = None  # Quiz grammar score
    vocab_score: str | None = None  # Quiz vocab score


class OnboardingStatusResponse(BaseModel):
    onboarding_completed: bool
    selected_animation_types: List[str] | None


@router.post("/save-selections")
async def save_onboarding_selections(
    request: SaveOnboardingSelectionsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save user's selected animation type, dialect, and quiz scores from onboarding"""
    # Validate animation type exists
    valid_types = db.query(Situation.animation_type).distinct().all()
    valid_type_list = [t[0] for t in valid_types]

    if request.animation_type not in valid_type_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid animation type: {request.animation_type}"
        )

    # Validate dialect
    valid_dialects = ['mexico', 'colombia', 'costa_rica']
    if request.dialect not in valid_dialects:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid dialect: {request.dialect}"
        )

    current_user.selected_animation_types = [request.animation_type]
    current_user.dialect = request.dialect
    current_user.grammar_score = request.grammar_score
    current_user.vocab_score = request.vocab_score
    current_user.onboarding_completed = True
    db.commit()

    return {"status": "success", "message": "Onboarding data saved"}


@router.get("/status", response_model=OnboardingStatusResponse)
async def get_onboarding_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's onboarding status"""
    return OnboardingStatusResponse(
        onboarding_completed=current_user.onboarding_completed,
        selected_animation_types=current_user.selected_animation_types or []
    )


@router.get("/available-categories")
async def get_available_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of available animation types for onboarding"""

    # Only show these 10 animation types for onboarding
    allowed_types = {
        "airport": {
            "name": "Airport",
            "description": "Checking in, going through security"
        },
        "banking": {
            "name": "Banking",
            "description": "Withdrawing cash, currency exchange"
        },
        "clothing": {
            "name": "Clothing Shopping",
            "description": "Finding sizes, trying on clothes"
        },
        "internet": {
            "name": "Internet",
            "description": "Setting up WiFi, phone plans"
        },
        "small_talk": {
            "name": "Small Talk",
            "description": "Meeting neighbors, casual conversations"
        },
        "contractor": {
            "name": "Home Renovation",
            "description": "Hiring contractors, discussing work"
        },
        "groceries": {
            "name": "Groceries",
            "description": "Shopping for food, asking for items"
        },
        "mechanic": {
            "name": "Mechanic",
            "description": "Car repairs, maintenance issues"
        },
        "police": {
            "name": "Police Stop",
            "description": "Traffic stops, document checks"
        },
        "restaurant": {
            "name": "Eating Out",
            "description": "Ordering food, reading menus"
        },
    }

    result = []
    for type_id, type_info in allowed_types.items():
        # Verify animation type exists in database
        exists = db.query(Situation).filter(Situation.animation_type == type_id).first()
        if exists:
            result.append({
                "id": type_id,
                "name": type_info["name"],
                "description": type_info["description"]
            })

    # Sort by name for consistent ordering
    result.sort(key=lambda x: x["name"])

    return {"categories": result}


class UpdateAnimationTypesRequest(BaseModel):
    animation_type: str
    action: str  # 'add' or 'remove'


@router.patch("/animation-types")
async def update_animation_types(
    request: UpdateAnimationTypesRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add or remove an animation type from the user's selected list."""
    # Validate animation type exists in DB
    exists = db.query(Situation).filter(Situation.animation_type == request.animation_type).first()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid animation type: {request.animation_type}"
        )

    current = list(current_user.selected_animation_types or [])

    if request.action == "add":
        if request.animation_type not in current:
            current.append(request.animation_type)
    elif request.action == "remove":
        if request.animation_type in current:
            current.remove(request.animation_type)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove last animation type"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="action must be 'add' or 'remove'"
        )

    current_user.selected_animation_types = current
    db.commit()

    return {"selected_animation_types": current}
