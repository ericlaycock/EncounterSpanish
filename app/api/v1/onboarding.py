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
    categories = db.query(Situation.category).distinct().order_by(Situation.category).all()
    
    # Map category IDs to display names
    category_map = {
        "banking": "Banking",
        "small_talk": "Small Talk",
        "groceries": "Groceries",
        "pharmacy": "Pharmacy",
        "apartment": "Apartment",
        "police": "Police",
        "delivery": "Delivery",
        "restaurant": "Restaurant",
        "transport": "Transport",
        "shopping": "Shopping",
        "internet": "Internet",
        "social": "Social",
        "mechanic": "Mechanic",
        "contractor": "Home Renovation",
        "airport": "Airport",
        "hardware": "Hardware Store",
        "clothing": "Clothing Shopping",
        "chat": "Chat Practice",
    }
    
    result = []
    for cat_tuple in categories:
        cat_id = cat_tuple[0]
        result.append({
            "id": cat_id,
            "name": category_map.get(cat_id, cat_id.replace("_", " ").title()),
            "description": f"Practice {category_map.get(cat_id, cat_id)} situations"
        })
    
    return {"categories": result}


