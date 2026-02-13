from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User


def get_db_session() -> Session:
    """Dependency for database session"""
    return Depends(get_db)


def get_current_user_dependency() -> User:
    """Dependency for current authenticated user"""
    return Depends(get_current_user)



