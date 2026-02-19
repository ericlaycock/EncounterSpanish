"""Request ID middleware for correlation tracking"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import uuid


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware that ensures every request has a request_id"""
    
    async def dispatch(self, request: Request, call_next):
        # Read X-Request-Id header or generate UUID4
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Store in request.state
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add X-Request-Id to response headers
        response.headers["X-Request-Id"] = request_id
        
        return response

