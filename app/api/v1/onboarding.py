from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app.auth import get_current_user
from app.models import User, Situation

router = APIRouter()


class SaveOnboardingSelectionsRequest(BaseModel):
    selected_category: str  # Single category ID
    dialect: str  # 'mexico', 'colombia', 'costa_rica'
    grammar_score: str | None = None  # Quiz grammar score
    vocab_score: str | None = None  # Quiz vocab score


class OnboardingStatusResponse(BaseModel):
    onboarding_completed: bool
    selected_categories: List[str] | None


@router.post("/save-selections")
async def save_onboarding_selections(
    request: SaveOnboardingSelectionsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save user's selected situation category, dialect, and quiz scores from onboarding"""
    # Validate category exists
    valid_categories = db.query(Situation.category).distinct().all()
    valid_category_list = [cat[0] for cat in valid_categories]
    
    if request.selected_category not in valid_category_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category: {request.selected_category}"
        )
    
    # Validate dialect
    valid_dialects = ['mexico', 'colombia', 'costa_rica']
    if request.dialect not in valid_dialects:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid dialect: {request.dialect}"
        )
    
    # Save single category as array for backward compatibility
    current_user.selected_situation_categories = [request.selected_category]
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
        selected_categories=current_user.selected_situation_categories or []
    )


@router.get("/available-categories")
async def get_available_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of available situation categories for onboarding"""
    
    # Only show these 10 categories for onboarding
    allowed_categories = {
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
    for cat_id, cat_info in allowed_categories.items():
        # Verify category exists in database
        exists = db.query(Situation).filter(Situation.category == cat_id).first()
        if exists:
            result.append({
                "id": cat_id,
                "name": cat_info["name"],
                "description": cat_info["description"]
            })
    
    # Sort by name for consistent ordering
    result.sort(key=lambda x: x["name"])
    
    return {"categories": result}



