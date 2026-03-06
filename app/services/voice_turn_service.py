from typing import List
from app.models import Word, Situation


def build_transcription_prompt(situation_title: str, words: List[Word]) -> str:
    """Build a context prompt to help Whisper with Spanish vocabulary."""
    target_words_list = ", ".join([f"{w.spanish} ({w.english})" for w in words])
    return (
        f"This is a conversation about {situation_title}.\n"
        f"The user is learning Spanish and may use these Spanish words: {target_words_list}.\n"
        f"The conversation is in Spanish and English. Focus on accurate Spanish transcription.\n"
        f"Common Spanish words that may appear: tamaño, talla, número, grande, pequeño, mediano."
    )


def build_conversation_prompt(
    situation_title: str,
    words: List[Word],
    used_spoken_word_ids: List[str],
    user_transcript: str,
) -> str:
    """Build the user prompt for the conversation LLM."""
    used_words = [w.spanish for w in words if w.id in used_spoken_word_ids]
    missing_words_info = [
        f"{w.spanish} ({w.english})"
        for w in words
        if w.id not in used_spoken_word_ids
    ]

    return (
        f"Situation: {situation_title}\n"
        f"Still need: {', '.join(missing_words_info) if missing_words_info else 'All words used'}\n"
        f"Already used: {', '.join(used_words) if used_words else 'None'}\n"
        f"User said: {user_transcript}\n\n"
        f"Ask a natural question requiring a missing Spanish word. Do NOT mention the Spanish word. Return JSON only."
    )
