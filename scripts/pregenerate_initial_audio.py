#!/usr/bin/env python3
"""Pre-generate TTS audio for all initial greeting messages and upload to R2.

Uses deterministic filenames (initial_msg_{situation_id}.mp3) so the backend
can return the R2 URL instantly without calling TTS at runtime.

Usage:
    python scripts/pregenerate_initial_audio.py          # all situations
    python scripts/pregenerate_initial_audio.py bank_1    # specific situation
    python scripts/pregenerate_initial_audio.py --force   # regenerate even if exists

Requires R2 env vars: R2_ENDPOINT_URL, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY,
                       R2_BUCKET_NAME, R2_PUBLIC_URL
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from openai import OpenAI
from app.config import settings
from app.data.seed_bank import SITUATIONS
from app.data.grammar_situations import GRAMMAR_SITUATIONS
from app.services.encounter_messages import get_initial_message_for_encounter
from app.utils.audio import upload_to_r2, _get_s3_client

AUDIO_DIR = Path("/tmp/initial_audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Import voice config from conversations.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module


# Voice config per animation_type (mirrored from conversations.py)
_ACCENT = "Speak with a Mexican Spanish accent, mixing English and Spanish words naturally."
VOICE_CONFIG = {
    "airport": ("nova", f"{_ACCENT} Use a professional, clear female voice."),
    "banking": ("shimmer", f"{_ACCENT} Use a professional, composed female voice with a warm undertone."),
    "clothing": ("coral", f"{_ACCENT} Use a casual, charming female voice."),
    "contractor": ("onyx", f"{_ACCENT} Use a deep, husky baritone male voice."),
    "core": ("echo", f"{_ACCENT} Use a casual, friendly male voice."),
    "groceries": ("echo", f"{_ACCENT} Use a casual, charming male voice."),
    "internet": ("nova", f"{_ACCENT} Use a young, energetic female voice."),
    "mechanic": ("onyx", f"{_ACCENT} Use a deep male voice."),
    "police": ("nova", f"{_ACCENT} Use an authoritative female voice, firm but professional."),
    "restaurant": ("echo", f"{_ACCENT} Use a suave, charming male voice."),
    "small_talk": ("shimmer", f"{_ACCENT} Use a warm, older female voice with a friendly, neighborly tone."),
    "grammar": ("shimmer", f"{_ACCENT} Use a warm, friendly female voice."),
}


def r2_file_exists(filename: str) -> bool:
    """Check if a file already exists in R2."""
    client = _get_s3_client()
    if not client:
        return False
    try:
        client.head_object(Bucket=settings.r2_bucket_name, Key=filename)
        return True
    except Exception:
        return False


def generate_and_upload(situation_id: str, title: str, animation_type: str, force: bool = False):
    """Generate TTS for one situation's initial message and upload to R2."""
    filename = f"initial_msg_{situation_id}.mp3"

    if not force and r2_file_exists(filename):
        return "skip"

    message = get_initial_message_for_encounter(situation_id, title)
    if not message:
        return "no_message"

    voice, instructions = VOICE_CONFIG.get(animation_type, ("alloy", _ACCENT))

    # Generate TTS
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=message,
        instructions=instructions,
    )

    # Save locally
    local_path = AUDIO_DIR / filename
    with open(local_path, "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)

    # Upload to R2
    r2_url = upload_to_r2(str(local_path), filename)
    if not r2_url:
        return "r2_fail"

    return "ok"


def main():
    force = "--force" in sys.argv
    specific = [a for a in sys.argv[1:] if not a.startswith("--")]

    # Collect all situations
    all_situations = []
    for s in SITUATIONS:
        all_situations.append((s["id"], s["title"], s["animation_type"]))
    for sid, cfg in GRAMMAR_SITUATIONS.items():
        all_situations.append((sid, cfg["title"], "grammar"))

    if specific:
        all_situations = [(sid, t, a) for sid, t, a in all_situations if sid in specific]

    if not all_situations:
        print("No situations found.")
        sys.exit(1)

    print(f"Pre-generating TTS for {len(all_situations)} situations (force={force})")
    start = time.time()

    stats = {"ok": 0, "skip": 0, "no_message": 0, "r2_fail": 0}
    for i, (sid, title, anim_type) in enumerate(all_situations, 1):
        result = generate_and_upload(sid, title, anim_type, force)
        stats[result] += 1
        if i % 50 == 0 or i == len(all_situations):
            elapsed = time.time() - start
            print(f"  [{i}/{len(all_situations)}] {elapsed:.0f}s — ok={stats['ok']} skip={stats['skip']} no_msg={stats['no_message']} fail={stats['r2_fail']}")

    total = time.time() - start
    print(f"\nDone in {total:.0f}s: {stats}")


if __name__ == "__main__":
    main()
