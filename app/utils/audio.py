import os
import uuid
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

AUDIO_DIR = Path("/tmp/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Lazy-initialized S3 client for R2
_s3_client = None


def _get_s3_client():
    """Get or create the boto3 S3 client for R2."""
    global _s3_client
    if _s3_client is None:
        from app.config import settings
        if not settings.r2_endpoint_url:
            return None
        import boto3
        _s3_client = boto3.client(
            "s3",
            endpoint_url=settings.r2_endpoint_url,
            aws_access_key_id=settings.r2_access_key_id,
            aws_secret_access_key=settings.r2_secret_access_key,
            region_name="auto",
        )
    return _s3_client


def generate_audio_filename() -> str:
    """Generate a unique filename for audio file"""
    return f"{uuid.uuid4()}.mp3"


def get_audio_path(filename: str) -> Path:
    """Get full path for audio file"""
    return AUDIO_DIR / filename


def get_audio_url(filename: str, base_url: str = "") -> str:
    """Generate URL for audio file (local fallback)"""
    if base_url:
        return f"{base_url}/audio/{filename}"
    return f"/audio/{filename}"


def upload_to_r2(local_path: str, filename: str) -> str | None:
    """Upload an audio file to R2 and return the public URL.
    Returns None if R2 is not configured or upload fails."""
    from app.config import settings
    if not settings.r2_public_url:
        return None

    client = _get_s3_client()
    if not client:
        return None

    try:
        client.upload_file(
            local_path,
            settings.r2_bucket_name,
            filename,
            ExtraArgs={"ContentType": "audio/mpeg"},
        )
        public_url = f"{settings.r2_public_url}/{filename}"
        logger.info(f"[R2] Uploaded {filename} → {public_url}")
        return public_url
    except Exception as e:
        logger.error(f"[R2] Upload failed for {filename}: {e}")
        return None


def cleanup_old_audio_files(max_age_hours: int = 24):
    """Clean up audio files older than max_age_hours"""
    import time
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600

    for file_path in AUDIO_DIR.glob("*.mp3"):
        file_age = current_time - file_path.stat().st_mtime
        if file_age > max_age_seconds:
            file_path.unlink()
