"""Request ID middleware - generates unique request ID for each request"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import uuid


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to generate and attach a unique request ID to each request"""
    
    async def dispatch(self, request: Request, call_next):
        # Generate or get request ID from header
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Store in request state for use throughout the request lifecycle
        request.state.request_id = request_id
        
        # Add to response headers
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        
        return response


