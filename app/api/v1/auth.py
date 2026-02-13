from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import authenticate_user, create_access_token, create_user
from app.schemas import LoginRequest, LoginResponse, RegisterRequest

router = APIRouter()


@router.post("/register", response_model=LoginResponse)
async def register(credentials: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user and return JWT token"""
    # Validate passwords match
    if credentials.password != credentials.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # Validate password length
    if len(credentials.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    # Create user
    user = create_user(db, credentials.email, credentials.password)
    
    # Generate token
    access_token = create_access_token(data={"sub": str(user.id)})
    return LoginResponse(access_token=access_token, user_id=user.id)


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return LoginResponse(access_token=access_token, user_id=user.id)



