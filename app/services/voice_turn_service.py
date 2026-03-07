from typing import List, Optional
from app.models import Word, Situation
from app.data.grammar_situations import get_grammar_config


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
