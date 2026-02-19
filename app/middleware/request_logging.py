"""Request logging middleware for structured API logging"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import traceback
from app.core.logger import log_event


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs all API requests and exceptions"""
    
    async def dispatch(self, request: Request, call_next):
        # Get request_id from state (set by RequestIDMiddleware)
        request_id = getattr(request.state, "request_id", "unknown")
        
        # Extract user_id from request.state if available (set by auth)
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            user_id = str(user_id)
        
        # Record start time
        start_time = time.time()
        
        # Extract request metadata
        method = request.method
        path = request.url.path
        status_code = 200  # Default, will be updated
        
        try:
            # Process request
            response = await call_next(request)
            status_code = response.status_code
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Log successful request
            log_event(
                level="info",
                event="api_request",
                message=f"{method} {path} - {status_code}",
                request_id=request_id,
                user_id=user_id,
                extra={
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                }
            )
            
            return response
            
        except Exception as e:
            # Calculate duration even on error
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Get error details
            error_type = type(e).__name__
            error_message = str(e)
            error_traceback = traceback.format_exc()
            
            # Log exception
            log_event(
                level="error",
                event="api_exception",
                message=f"{method} {path} - {error_type}: {error_message}",
                request_id=request_id,
                user_id=user_id,
                extra={
                    "method": method,
                    "path": path,
                    "status_code": 500,
                    "duration_ms": duration_ms,
                    "error_type": error_type,
                    "error_message": error_message,
                    "traceback": error_traceback,
                }
            )
            
            # Re-raise to let FastAPI handle it
            raise

