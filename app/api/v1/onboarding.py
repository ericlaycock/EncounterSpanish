from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app.auth import get_current_user
from app.models import User, Situation

router = APIRouter()


class SaveOnboardingSelectionsRequest(BaseModel):
    selected_categories: List[str]  # e.g., ["banking", "small_talk", "groceries"]


class OnboardingStatusResponse(BaseModel):
    onboarding_completed: bool
    selected_categories: List[str] | None


@router.post("/save-selections")
async def save_onboarding_selections(
    request: SaveOnboardingSelectionsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save user's selected situation categories from onboarding"""
    if len(request.selected_categories) != 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must select exactly 3 categories"
        )
    
    # Validate categories exist
    valid_categories = db.query(Situation.category).distinct().all()
    valid_category_list = [cat[0] for cat in valid_categories]
    
    for category in request.selected_categories:
        if category not in valid_category_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid category: {category}"
            )
    
    current_user.selected_situation_categories = request.selected_categories
    current_user.onboarding_completed = True
    db.commit()
    
    return {"status": "success", "message": "Selections saved"}


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



