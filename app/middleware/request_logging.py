"""Request logging middleware - extracts user_id from JWT and logs requests"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def extract_user_id_from_request(request: Request) -> Optional[str]:
    """
    Safely extract user_id from JWT token in request.
    Returns None if token is missing, invalid, or user cannot be determined.
    """
    try:
        # Try to get user_id from request state (set by endpoints that use get_current_user)
        if hasattr(request.state, 'user_id'):
            return str(request.state.user_id)
        
        # Try to extract from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.replace("Bearer ", "")
        
        # Decode JWT without database lookup (lightweight)
        from jose import jwt, JWTError
        from app.config import settings
        
        try:
            payload = jwt.decode(
                token, 
                settings.jwt_secret, 
                algorithms=[settings.jwt_algorithm]
            )
            user_id_str = payload.get("sub")
            if user_id_str:
                return str(user_id_str)
        except (JWTError, ValueError):
            # Token invalid or expired - that's okay, we'll return None
            pass
        
        return None
    except Exception as e:
        # Silently fail - don't break request processing
        logger.debug(f"Failed to extract user_id: {e}")
        return None


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to extract user_id from JWT and store in request state"""
    
    async def dispatch(self, request: Request, call_next):
        # Extract and store user_id early in request lifecycle
        user_id = extract_user_id_from_request(request)
        if user_id:
            request.state.user_id = user_id
        
        response = await call_next(request)
        return response


