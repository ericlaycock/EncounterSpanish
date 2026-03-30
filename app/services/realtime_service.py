"""OpenAI Realtime API service for combined LLM + TTS generation.

Uses WebSocket to get streamed text + audio in one call (~0.8s to first audio byte
vs ~5s with separate LLM + TTS).

Audio output is PCM16 24kHz mono, converted to MP3 via ffmpeg.
"""

import asyncio
import base64
import json
import logging
import struct
import subprocess
import time
import tempfile
from pathlib import Path
from typing import Optional

import websockets

from app.config import settings

logger = logging.getLogger(__name__)

REALTIME_MODEL = "gpt-4o-realtime-preview-2025-06-03"
REALTIME_URL = f"wss://api.openai.com/v1/realtime?model={REALTIME_MODEL}"


async def generate_with_realtime(
    messages: list,
    voice: str = "shimmer",
    tts_instructions: Optional[str] = None,
    request_id: str = "unknown",
) -> dict:
    """Generate LLM response + TTS audio via the Realtime API (batch — waits for completion).

    Returns:
        {"text": str, "audio_bytes": bytes, "first_audio_ms": int, "total_ms": int}
    """
    result = {"text": "", "audio_chunks": [], "first_audio_ms": 0, "first_text_ms": 0}
    async for event in stream_realtime(messages, voice, tts_instructions, request_id):
        if event["type"] == "audio":
            result["audio_chunks"].append(event["data"])
            if not result["first_audio_ms"]:
                result["first_audio_ms"] = event.get("elapsed_ms", 0)
        elif event["type"] == "text":
            result["text"] = event["text"]
            result["first_text_ms"] = event.get("elapsed_ms", 0)
        elif event["type"] == "done":
            pass

    audio_bytes = b"".join(result["audio_chunks"])
    return {
        "text": result["text"],
        "audio_bytes": audio_bytes,
        "first_audio_ms": result["first_audio_ms"],
        "first_text_ms": result["first_text_ms"],
        "total_ms": 0,
    }


async def stream_realtime(
    messages: list,
    voice: str = "shimmer",
    tts_instructions: Optional[str] = None,
    request_id: str = "unknown",
):
    """Stream LLM + TTS events from the Realtime API.

    Yields dicts:
        {"type": "audio", "data": bytes, "elapsed_ms": int}  — PCM16 24kHz mono chunk
        {"type": "text", "text": str, "elapsed_ms": int}      — full transcript (when complete)
        {"type": "done", "elapsed_ms": int}
    """
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "OpenAI-Beta": "realtime=v1",
    }

    t0 = time.time()
    full_text = ""

    # Extract system prompt from messages
    system_content = ""
    conversation_items = []
    for msg in messages:
        if msg["role"] == "system":
            system_content = msg["content"]
        else:
            conversation_items.append(msg)

    if tts_instructions:
        system_content += f"\n\n[Voice style: {tts_instructions}]"

    try:
        async with websockets.connect(REALTIME_URL, additional_headers=headers, close_timeout=5) as ws:
            logger.info(f"[Realtime] Connected in {int((time.time()-t0)*1000)}ms (request={request_id})")

            await ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "voice": voice,
                    "instructions": system_content,
                    "output_audio_format": "pcm16",
                    "turn_detection": None,
                }
            }))

            for item in conversation_items:
                role = item["role"]
                content = item["content"]
                if role == "assistant":
                    await ws.send(json.dumps({
                        "type": "conversation.item.create",
                        "item": {"type": "message", "role": "assistant",
                                 "content": [{"type": "text", "text": content}]},
                    }))
                elif role == "user":
                    await ws.send(json.dumps({
                        "type": "conversation.item.create",
                        "item": {"type": "message", "role": "user",
                                 "content": [{"type": "input_text", "text": content}]},
                    }))

            await ws.send(json.dumps({"type": "response.create"}))

            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=30)
                event = json.loads(msg)
                event_type = event.get("type", "")
                elapsed_ms = int((time.time() - t0) * 1000)

                if event_type == "response.audio.delta":
                    chunk = base64.b64decode(event.get("delta", ""))
                    yield {"type": "audio", "data": chunk, "elapsed_ms": elapsed_ms}

                elif event_type == "response.audio_transcript.delta":
                    full_text += event.get("delta", "")

                elif event_type == "response.audio_transcript.done":
                    yield {"type": "text", "text": full_text, "elapsed_ms": elapsed_ms}

                elif event_type == "response.done":
                    # If text wasn't sent via transcript.done, send it now
                    if full_text:
                        yield {"type": "text", "text": full_text, "elapsed_ms": elapsed_ms}
                    yield {"type": "done", "elapsed_ms": elapsed_ms}
                    break

                elif event_type == "error":
                    error_msg = event.get("error", {}).get("message", str(event))
                    logger.error(f"[Realtime] Error: {error_msg}")
                    raise RuntimeError(f"Realtime API error: {error_msg}")

    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f"[Realtime] WebSocket closed: {e}")
        raise

    total_ms = int((time.time() - t0) * 1000)
    logger.info(f"[Realtime] Stream done: {total_ms}ms (request={request_id})")


def pcm16_to_mp3(pcm_bytes: bytes, output_path: str, sample_rate: int = 24000):
    """Convert raw PCM16 audio to MP3 using ffmpeg."""
    result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "s16le",           # raw PCM16
            "-ar", str(sample_rate), # 24kHz
            "-ac", "1",              # mono
            "-i", "pipe:0",          # stdin
            "-codec:a", "libmp3lame",
            "-b:a", "64k",           # 64kbps (plenty for speech)
            output_path,
        ],
        input=pcm_bytes,
        capture_output=True,
        timeout=10,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr.decode()[:200]}")
