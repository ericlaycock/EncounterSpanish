from openai import OpenAI
from typing import AsyncGenerator, List, Dict, Union
import json
import io
import tempfile
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)
MODEL = "gpt-4.1-mini"


async def generate_text(
    system_prompt: str,
    user_prompt: str,
    return_json: bool = False
) -> Union[str, Dict]:
    """Generate text using OpenAI chat completions"""
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


async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.mp3") -> str:
    """Transcribe audio using OpenAI STT"""
    # Create a file-like object from bytes
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = filename
    
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text


async def generate_speech(text: str, output_path: str) -> str:
    """Generate speech using OpenAI TTS and save to file"""
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

