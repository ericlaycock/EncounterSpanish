from typing import List, Optional
from app.models import Word, Situation
from app.data.grammar_situations import get_grammar_config


def get_language_mode(encounter_number: int, vocab_level: int) -> str:
    """Derive language mode from encounter number (1-50) and vocab level.

    VL < 300:
      encounters 1-20  → "english"
      encounters 21-40 → "spanish_text"
      encounters 41-50 → "spanish_audio"
    VL >= 300:
      encounters 1-40  → "spanish_text"
      encounters 41-50 → "spanish_audio"
    """
    if vocab_level >= 300:
        return "spanish_audio" if encounter_number > 40 else "spanish_text"
    else:
        if encounter_number <= 20:
            return "english"
        elif encounter_number <= 40:
            return "spanish_text"
        else:
            return "spanish_audio"


def build_grammar_system_prompt(situation_id: str) -> Optional[str]:
    """Build a system prompt for grammar conversation phases (2/3).

    Returns None if not a grammar situation.
    """
    config = get_grammar_config(situation_id)
    if not config:
        return None

    tense = config["tense"]
    title = config["title"]
    p2_config = config.get("phase_2_config")

    if tense == "pronouns":
        agent_type = "grammar_pronouns_agent"
    elif tense == "gustar":
        agent_type = "grammar_gustar_agent"
    else:
        agent_type = "grammar_conjugation_agent"

    from app.services.llm_gateway import load_prompt
    base_prompt = load_prompt(agent_type, "v1")

    details = f"\n\nGrammar Situation: {title}\nTense: {tense}\n"
    if p2_config:
        details += f"Goal: {p2_config.get('description', '')}\n"
        if "targets" in p2_config and isinstance(p2_config["targets"], list):
            target_strs = []
            for t in p2_config["targets"]:
                if "verb" in t and "pronoun" in t:
                    target_strs.append(f"{t['pronoun']} + {t['verb']}")
                elif "word" in t:
                    target_strs.append(t["word"])
            details += f"Target combos to practice: {', '.join(target_strs)}\n"
        elif "verbs" in p2_config:
            details += f"Verbs: {', '.join(p2_config['verbs'])}\n"
            details += f"Pronoun pattern: {p2_config.get('pronoun_pattern', 'all')}\n"

    return base_prompt + details


def build_grammar_user_prompt(
    situation_title: str,
    used_spoken_word_ids: List[str],
    user_transcript: str,
    config: dict,
) -> str:
    """Build user prompt for grammar conversation turn."""
    p2_config = config.get("phase_2_config", {}) or {}
    targets = p2_config.get("targets", [])
    description = p2_config.get("description", "Practice grammar structures")

    return (
        f"Grammar Situation: {situation_title}\n"
        f"Goal: {description}\n"
        f"User said: {user_transcript}\n\n"
        f"Continue the practice session. Return JSON only."
    )


def build_transcription_prompt(situation_title: str, words: List[Word], catalan_mode: bool = False) -> str:
    """Build a context prompt for STT transcription (whisper-style format).

    Benchmark showed this format gives 0.997 accuracy + 100% Spanish word
    detection on gpt-4o-mini-transcribe, beating both whisper-1 and
    gpt-4o-transcribe.
    """
    target_words_list = ", ".join([w.spanish for w in words])
    lang = "Catalan" if catalan_mode else "Spanish"
    return (
        f"This is a conversation about {situation_title}. "
        f"The user is learning {lang} and may use these {lang} words: {target_words_list}. "
        f"The conversation is in {lang} and English."
    )


def get_conversation_system_prompt(language_mode: str = "english", catalan_mode: bool = False) -> str:
    """Load the appropriate conversation agent prompt based on language mode."""
    from app.services.llm_gateway import load_prompt
    if catalan_mode:
        if language_mode in ("catalan_text", "catalan_audio"):
            return load_prompt("conversation_agent_catalan", "v1")
        return load_prompt("conversation_agent_catalan_english", "v1")
    if language_mode in ("spanish_text", "spanish_audio"):
        return load_prompt("conversation_agent_spanish", "v1")
    return load_prompt("conversation_agent", "v1")


def build_conversation_prompt(
    situation_title: str,
    words: List[Word],
    used_spoken_word_ids: List[str],
    user_transcript: str,
    catalan_mode: bool = False,
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
        f"Ask a natural question requiring a missing {'Catalan' if catalan_mode else 'Spanish'} word. Do NOT mention the {'Catalan' if catalan_mode else 'Spanish'} word. Return JSON only."
    )
