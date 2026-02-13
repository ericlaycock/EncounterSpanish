from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt via passlib"""
    import logging
    logger = logging.getLogger(__name__)
    
    # Ensure password is a plain string
    if not isinstance(password, str):
        password = str(password)
    
    # Debug: log password info
    password_bytes = password.encode('utf-8')
    logger.info(f"Password length: {len(password)} chars, {len(password_bytes)} bytes")
    
    # Bcrypt has a 72-byte limit - check and truncate if needed
    if len(password_bytes) > 72:
        logger.warning(f"Password exceeds 72 bytes, truncating from {len(password_bytes)} to 72")
        # Truncate to 72 bytes, ensuring we don't break UTF-8 sequences
        truncated = password_bytes[:72]
        # Remove any incomplete UTF-8 sequences at the end
        while truncated and (truncated[-1] & 0xC0) == 0x80:
            truncated = truncated[:-1]
        password = truncated.decode('utf-8', errors='ignore')
        logger.info(f"Truncated password length: {len(password)} chars")
    
    # Hash with passlib (which uses bcrypt)
    try:
        result = pwd_context.hash(password)
        logger.info("Password hashed successfully")
        return result
    except Exception as e:
        logger.error(f"Password hashing failed: {e}, password type: {type(password)}, length: {len(password)}")
        raise


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def create_user(db: Session, email: str, password: str) -> User:
    """Create a new user with hashed password"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    password_hash = get_password_hash(password)
    user = User(email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create default subscription
    from app.models import Subscription
    subscription = Subscription(user_id=user.id, active=False)
    db.add(subscription)
    db.commit()
    
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user



