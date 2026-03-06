"""Utility functions for extracting information from requests"""
from starlette.requests import Request
from typing import Optional


def get_user_id_from_request(request: Request) -> Optional[str]:
    """
    Safely get user_id from request state.
    Returns None if not available.
    """
    return getattr(request.state, 'user_id', None)


def get_request_id_from_request(request: Request) -> str:
    """
    Get request_id from request state.
    Returns 'unknown' if not available.
    """
    return getattr(request.state, 'request_id', 'unknown')


