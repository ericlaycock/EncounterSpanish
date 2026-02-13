import os
import uuid
from pathlib import Path

AUDIO_DIR = Path("/tmp/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def generate_audio_filename() -> str:
    """Generate a unique filename for audio file"""
    return f"{uuid.uuid4()}.mp3"


def get_audio_path(filename: str) -> Path:
    """Get full path for audio file"""
    return AUDIO_DIR / filename


def get_audio_url(filename: str, base_url: str = "") -> str:
    """Generate URL for audio file"""
    # For MVP, we'll return a path that can be served statically
    # In production, this would be a CDN URL or Railway static file URL
    if base_url:
        return f"{base_url}/audio/{filename}"
    return f"/audio/{filename}"


def cleanup_old_audio_files(max_age_hours: int = 24):
    """Clean up audio files older than max_age_hours"""
    import time
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for file_path in AUDIO_DIR.glob("*.mp3"):
        file_age = current_time - file_path.stat().st_mtime
        if file_age > max_age_seconds:
            file_path.unlink()



