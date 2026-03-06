from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import authenticate_user, create_access_token, create_user
from app.schemas import LoginRequest, LoginResponse, RegisterRequest

router = APIRouter()


@router.post("/register", response_model=LoginResponse)
async def register(credentials: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user and return JWT token"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Registration attempt for email: {credentials.email}")
        
        # Validate passwords match
        if credentials.password != credentials.confirm_password:
            logger.warning(f"Registration failed: passwords do not match for {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        
        # Validate password length
        if len(credentials.password) < 8:
            logger.warning(f"Registration failed: password too short for {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters"
            )
        
        # Create user
        user = create_user(db, credentials.email, credentials.password)
        logger.info(f"User created successfully: {user.id} ({user.email})")
        
        # Generate token
        access_token = create_access_token(data={"sub": str(user.id)})
        logger.info(f"Registration successful for user: {user.id}")
        return LoginResponse(access_token=access_token, user_id=user.id)
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        logger.error(f"Registration error for {credentials.email}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration. Please try again."
        )


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Login attempt for email: {credentials.email}")
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        logger.warning(f"Login failed for email: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    logger.info(f"Login successful for user: {user.id}")
    access_token = create_access_token(data={"sub": str(user.id)})
    return LoginResponse(access_token=access_token, user_id=user.id)



