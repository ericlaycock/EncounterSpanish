from openai import OpenAI
from typing import AsyncGenerator, List, Dict, Union
import json
import io
from app.config import settings

MODEL = "gpt-4.1-mini"

# Lazy initialization to avoid import-time errors
_client = None

def get_client() -> OpenAI:
    """Get or create OpenAI client"""
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


async def generate_text(
    system_prompt: str,
    user_prompt: str,
    return_json: bool = False
) -> Union[str, Dict]:
    """Generate text using OpenAI chat completions"""
    client = get_client()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"} if return_json else None
    )
    
    content = response.choices[0].message.content
    if return_json:
        return json.loads(content)
    return content


async def stream_text(
    system_prompt: str,
    user_prompt: str
) -> AsyncGenerator[str, None]:
    """Stream text using OpenAI chat completions for SSE"""
    client = get_client()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.mp3", prompt: str = None) -> str:
    """Transcribe audio using OpenAI STT with optional prompt for better accuracy"""
    client = get_client()
    # Create a file-like object from bytes
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = filename
    
    params = {
        "model": "whisper-1",
        "file": audio_file,
        "language": "es"  # Spanish language hint
    }
    
    # Add prompt if provided to help with context and specific vocabulary
    if prompt:
        params["prompt"] = prompt
    
    transcript = client.audio.transcriptions.create(**params)
    return transcript.text


async def generate_speech(text: str, output_path: str) -> str:
    """Generate speech using OpenAI TTS and save to file"""
    client = get_client()
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    
    # Save to file
    with open(output_path, "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
    
    return output_path


    with open(output_path, "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
    
    return output_path


    with open(output_path, "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
    
    return output_path

