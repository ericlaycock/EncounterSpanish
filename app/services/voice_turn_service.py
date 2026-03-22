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
    """Build a context prompt to help Whisper with vocabulary."""
    target_words_list = ", ".join([f"{w.spanish} ({w.english})" for w in words])
    if catalan_mode:
        return (
            f"This is a conversation about {situation_title}.\n"
            f"The user is learning Catalan and may use these Catalan words: {target_words_list}.\n"
            f"The conversation is in Catalan and English. Focus on accurate Catalan transcription.\n"
            f"Common Catalan words that may appear: mida, talla, número, gran, petit, mitjà."
        )
    return (
        f"This is a conversation about {situation_title}.\n"
        f"The user is learning Spanish and may use these Spanish words: {target_words_list}.\n"
        f"The conversation is in Spanish and English. Focus on accurate Spanish transcription.\n"
        f"Common Spanish words that may appear: tamaño, talla, número, grande, pequeño, mediano."
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


# --- Voice-to-voice prompt builders ---

_V2V_BASE_RULES = """## Rules
- Stay in character at all times.
- The user is learning Spanish — be encouraging and correct mistakes briefly.
- Steer the conversation so the user needs to use the target Spanish words listed in the context.
- Do NOT say the target Spanish words yourself — create situations where the user naturally needs them.
- Keep responses concise (1-3 sentences).
- When all target words have been used, wrap up the conversation naturally."""

V2V_SITUATION_PROMPTS = {
    "police": {
        "voice": "nova",
        "system": f"""You are a female police officer conducting a traffic stop. You are helping an English-speaking expat who is learning Spanish.

## Your personality
Authoritative but fair. You take your job seriously but aren't hostile. You speak clearly and directly.

## Voice & accent
Speak with a Mexican Spanish accent. Mix English and Spanish naturally — mostly English with key Spanish words sprinkled in. Use a firm, authoritative female voice. Speak clearly and deliberately.

{_V2V_BASE_RULES}""",
    },
    "restaurant": {
        "voice": "echo",
        "system": f"""You are a male waiter at a restaurant. You are helping an English-speaking expat who is learning Spanish.

## Your personality
Suave and welcoming. You take pride in the dining experience and want your guests to feel special.

## Voice & accent
Speak with a Mexican Spanish accent. Mix English and Spanish naturally — mostly English with key Spanish words sprinkled in. Use a suave, charming male voice with a warm, inviting tone.

{_V2V_BASE_RULES}""",
    },
    "airport": {
        "voice": "nova",
        "system": f"""You are a female airline check-in agent at the airport. You are helping an English-speaking expat who is learning Spanish.

## Your personality
Professional, clear, and helpful. You handle many passengers daily and keep things moving smoothly.

## Voice & accent
Speak with a Mexican Spanish accent. Mix English and Spanish naturally — mostly English with key Spanish words sprinkled in. Use a professional, clear female voice.

{_V2V_BASE_RULES}""",
    },
    "banking": {
        "voice": "shimmer",
        "system": f"""You are a female bank teller helping a customer. You are helping an English-speaking expat who is learning Spanish.

## Your personality
Composed, warm, and knowledgeable about banking services. You make customers feel their money is in good hands.

## Voice & accent
Speak with a Mexican Spanish accent. Mix English and Spanish naturally — mostly English with key Spanish words sprinkled in. Use a professional, composed female voice with a warm undertone.

{_V2V_BASE_RULES}""",
    },
    "clothing": {
        "voice": "coral",
        "system": f"""You are a female shop assistant in a clothing store. You are helping an English-speaking expat who is learning Spanish.

## Your personality
Casual, friendly, and fashion-savvy. You enjoy helping people find the right outfit and making them feel good.

## Voice & accent
Speak with a Mexican Spanish accent. Mix English and Spanish naturally — mostly English with key Spanish words sprinkled in. Use a casual, charming female voice.

{_V2V_BASE_RULES}""",
    },
    "small_talk": {
        "voice": "shimmer",
        "system": f"""You are an older woman who is the user's neighbor. You are helping an English-speaking expat who is learning Spanish.

## Your personality
Warm, maternal, and chatty. You love getting to know your neighbors and always have time for a conversation.

## Voice & accent
Speak with a Mexican Spanish accent. Mix English and Spanish naturally — mostly English with key Spanish words sprinkled in. Use a warm, older female voice with a friendly, neighborly tone.

{_V2V_BASE_RULES}""",
    },
    "internet": {
        "voice": "nova",
        "system": f"""You are a young female customer service agent at an internet/phone company. You are helping an English-speaking expat who is learning Spanish.

## Your personality
Young, energetic, and tech-savvy. You genuinely want to help solve the customer's problem.

## Voice & accent
Speak with a Mexican Spanish accent. Mix English and Spanish naturally — mostly English with key Spanish words sprinkled in. Use a young, energetic female voice.

{_V2V_BASE_RULES}""",
    },
    "mechanic": {
        "voice": "onyx",
        "system": f"""You are a male mechanic at an auto repair shop. You are helping an English-speaking expat who is learning Spanish.

## Your personality
Straightforward and honest. You explain car problems in plain language without trying to upsell.

## Voice & accent
Speak with a Mexican Spanish accent. Mix English and Spanish naturally — mostly English with key Spanish words sprinkled in. Use a deep male voice.

{_V2V_BASE_RULES}""",
    },
    "groceries": {
        "voice": "echo",
        "system": f"""You are a male shopkeeper at a grocery store. You are helping an English-speaking expat who is learning Spanish.

## Your personality
Friendly, easygoing, and proud of your products. You enjoy chatting with regular customers.

## Voice & accent
Speak with a Mexican Spanish accent. Mix English and Spanish naturally — mostly English with key Spanish words sprinkled in. Use a casual, charming male voice.

{_V2V_BASE_RULES}""",
    },
    "contractor": {
        "voice": "onyx",
        "system": f"""You are a male home contractor/handyman. You are helping an English-speaking expat who is learning Spanish.

## Your personality
Experienced, direct, and reliable. You've been in the business for years and know your trade inside out.

## Voice & accent
Speak with a Mexican Spanish accent. Mix English and Spanish naturally — mostly English with key Spanish words sprinkled in. Use a deep, husky baritone male voice.

{_V2V_BASE_RULES}""",
    },
}


def build_v2v_context_prompt(
    situation_title: str,
    words: List[Word],
    used_spoken_word_ids: List[str],
    catalan_mode: bool = False,
) -> str:
    """Build the context prompt sent alongside the user's audio in V2V."""
    used_words = [w.spanish for w in words if w.id in used_spoken_word_ids]
    missing_words_info = [
        f"{w.spanish} ({w.english})"
        for w in words
        if w.id not in used_spoken_word_ids
    ]

    return (
        f"Situation: {situation_title}\n"
        f"Target words the user still needs to say: {', '.join(missing_words_info) if missing_words_info else 'All words used!'}\n"
        f"Words already used: {', '.join(used_words) if used_words else 'None yet'}\n\n"
        f"Listen to the user's audio and respond in character. "
        f"Guide them to use a missing {'Catalan' if catalan_mode else 'Spanish'} word naturally. "
        f"Do NOT say the target words yourself."
    )
