"""Better Stack log shipping client"""
import os
import asyncio
import httpx
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Singleton async client
_client: Optional[httpx.AsyncClient] = None


def get_client() -> Optional[httpx.AsyncClient]:
    """Get or create singleton httpx.AsyncClient"""
    global _client
    
    # Check if Better Stack is configured
    host = os.environ.get("BETTERSTACK_HOST")
    token = os.environ.get("BETTERSTACK_TOKEN")
    
    if not host or not token:
        return None
    
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=httpx.Timeout(1.5, connect=0.8),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
    
    return _client


async def ship_log(log_entry: Dict[str, Any]) -> None:
    """
    Ship log entry to Better Stack asynchronously (fire-and-forget).
    
    Args:
        log_entry: The log entry dictionary (will be sent as JSON)
    """
    host = os.environ.get("BETTERSTACK_HOST")
    token = os.environ.get("BETTERSTACK_TOKEN")
    
    if not host or not token:
        # Better Stack not configured, skip shipping
        return
    
    # Remove large payloads that should only be in Postgres
    # Keep only metadata for Better Stack
    filtered_entry = log_entry.copy()
    
    # Remove large fields
    fields_to_remove = [
        "messages_json",
        "response_json",
        "transcript_text",
        "audio_bytes",
        "audio_path",
        "output_json",
    ]
    
    for field in fields_to_remove:
        filtered_entry.pop(field, None)
    
    # If we have IDs, keep those instead of full content
    # (e.g., llm_request_id, stt_request_id, tts_request_id)
    # These are already in the extra dict if present
    
    client = get_client()
    if client is None:
        return
    
    try:
        url = f"https://{host}"
        response = await client.post(
            url,
            json=filtered_entry,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )
        # Fire-and-forget: don't wait for response or raise on error
        # Just log if there's an issue (but don't crash)
        if response.status_code >= 400:
            logger.debug(f"Better Stack log shipping returned {response.status_code}: {response.text}")
    except Exception as e:
        # Swallow errors - don't crash the app
        logger.debug(f"Better Stack log shipping failed: {e}")


def schedule_ship_log(log_entry: Dict[str, Any]) -> None:
    """
    Schedule log shipping to Better Stack if event loop is running.
    Fire-and-forget, non-blocking.
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Event loop is running, schedule async task
            asyncio.create_task(ship_log(log_entry))
        else:
            # No running loop, skip shipping (stdout still works)
            pass
    except RuntimeError:
        # No event loop exists, skip shipping
        pass

