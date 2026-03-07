"""Grammar situation configuration — single source of truth.

Each entry defines the grammar situation's word workload, drill type,
phase availability, and conversation config for phases 2/3.
"""

PRONOUNS = ["yo", "tu", "el", "ella", "usted", "nosotros", "nosotras", "ellos", "ellas", "ustedes"]

GRAMMAR_SITUATIONS = {
    "grammar_pronouns": {
        "title": "Pronouns",
        "vocab_level": 15,
        "word_workload": ["yo", "tu", "el", "ella", "usted", "nosotros", "nosotras", "ellos", "ellas", "ustedes", "su"],
        "video_embed_id": "bLZk006G5ge",
        "drill_type": "skip",
        "tense": "pronouns",
        "phases": {"0a": True, "0b": False, "1a": True, "1b": True, "1c": False, "2": True, "3": False},
        "phase_2_config": {
            "description": "All pronouns + 'su' in conversation",
            "targets": [{"word": p} for p in ["yo", "tu", "el", "ella", "usted", "nosotros", "nosotras", "ellos", "ellas", "ustedes", "su"]],
        },
    },
    "grammar_gender": {
        "title": "Grammatical Gender",
        "vocab_level": 20,
        "word_workload": ["el", "los", "la", "las", "un", "unos", "una", "unas"],
        "video_embed_id": "aJguo8cBgm7",
        "drill_type": "article_matching",
        "tense": "gender",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": False, "3": False},
        "drill_config": {
            "curated_nouns": [
                {"spanish": "libro", "english": "book", "gender": "m", "ending_rule": "LONERS_o"},
                {"spanish": "papel", "english": "paper", "gender": "m", "ending_rule": "LONERS_l"},
                {"spanish": "pan", "english": "bread", "gender": "m", "ending_rule": "LONERS_n"},
                {"spanish": "cafe", "english": "coffee", "gender": "m", "ending_rule": "LONERS_e"},
                {"spanish": "amor", "english": "love", "gender": "m", "ending_rule": "LONERS_r"},
                {"spanish": "lunes", "english": "Monday", "gender": "m", "ending_rule": "LONERS_s"},
                {"spanish": "problema", "english": "problem", "gender": "m", "ending_rule": "MAJE_ma"},
                {"spanish": "viaje", "english": "trip", "gender": "m", "ending_rule": "MAJE_je"},
                {"spanish": "ciudad", "english": "city", "gender": "f", "ending_rule": "DIONZA_d"},
                {"spanish": "television", "english": "television", "gender": "f", "ending_rule": "DIONZA_ion"},
                {"spanish": "voz", "english": "voice", "gender": "f", "ending_rule": "DIONZA_z"},
                {"spanish": "casa", "english": "house", "gender": "f", "ending_rule": "DIONZA_a"},
                {"spanish": "mesa", "english": "table", "gender": "f", "ending_rule": "DIONZA_a"},
                {"spanish": "nacion", "english": "nation", "gender": "f", "ending_rule": "DIONZA_ion"},
                {"spanish": "libertad", "english": "freedom", "gender": "f", "ending_rule": "DIONZA_d"},
                {"spanish": "luz", "english": "light", "gender": "f", "ending_rule": "DIONZA_z"},
                {"spanish": "gato", "english": "cat", "gender": "m", "ending_rule": "LONERS_o"},
                {"spanish": "sistema", "english": "system", "gender": "m", "ending_rule": "MAJE_ma"},
                {"spanish": "carne", "english": "meat", "gender": "f", "ending_rule": "exception_e"},
                {"spanish": "leche", "english": "milk", "gender": "f", "ending_rule": "exception_e"},
            ],
        },
        "phase_2_config": None,
    },
    "grammar_regular_present": {
        "title": "Regular Present",
        "vocab_level": 30,
        "word_workload": ["hablar", "escuchar", "beber", "comer", "vivir", "escribir"],
        "video_embed_id": "6jpCj97AHMN",
        "drill_type": "conjugation",
        "tense": "present",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "All pronouns for hablar, comer, vivir",
            "targets": [
                {"verb": v, "pronoun": p}
                for v in ["hablar", "comer", "vivir"]
                for p in PRONOUNS
            ],
        },
    },
    "grammar_irregular_present": {
        "title": "Irregular Present",
        "vocab_level": 60,
        "word_workload": ["ser", "estar", "ir", "dar", "tener", "venir"],
        "video_embed_id": "sD2tovQc7pB",
        "drill_type": "conjugation",
        "tense": "present",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "All pronouns for all verbs",
            "targets": [
                {"verb": v, "pronoun": p}
                for v in ["ser", "estar", "ir", "dar", "tener", "venir"]
                for p in PRONOUNS
            ],
        },
    },
    "grammar_irregular_present_ii": {
        "title": "Irregular Present II",
        "vocab_level": 65,
        "word_workload": ["caer", "traer", "hacer", "poner", "salir", "valer", "decir", "oir"],
        "video_embed_id": "tPXOw1Rz82y",
        "drill_type": "conjugation",
        "tense": "present",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "2 random pronouns per verb",
            "pronoun_pattern": "random_2",
            "verbs": ["caer", "traer", "hacer", "poner", "salir", "valer", "decir", "oir"],
        },
    },
    "grammar_spelling_changes": {
        "title": "Spelling Changes",
        "vocab_level": 70,
        "word_workload": ["conseguir", "recoger", "dirigir", "convencer", "conocer", "producir", "construir", "continuar"],
        "video_embed_id": "dYyywu1hOVp",
        "drill_type": "conjugation",
        "tense": "present",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "'yo' + 1 random pronoun per verb",
            "pronoun_pattern": "yo_plus_random_1",
            "verbs": ["conseguir", "recoger", "dirigir", "convencer", "conocer", "producir", "construir", "continuar"],
        },
    },
    "grammar_present_o_ue": {
        "title": "Present O→UE",
        "vocab_level": 80,
        "word_workload": ["mover", "almorzar", "morir"],
        "video_embed_id": "My2TaOGsmet",
        "drill_type": "conjugation",
        "tense": "present",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "All pronouns for all verbs",
            "targets": [
                {"verb": v, "pronoun": p}
                for v in ["mover", "almorzar", "morir"]
                for p in PRONOUNS
            ],
        },
    },
    "grammar_present_e_ie": {
        "title": "Present E→IE",
        "vocab_level": 90,
        "word_workload": ["cerrar", "entender"],
        "video_embed_id": "BwvOV8xReZZ",
        "drill_type": "conjugation",
        "tense": "present",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "All pronouns for all verbs",
            "targets": [
                {"verb": v, "pronoun": p}
                for v in ["cerrar", "entender"]
                for p in PRONOUNS
            ],
        },
    },
    "grammar_present_e_i": {
        "title": "Present E→I",
        "vocab_level": 99,
        "word_workload": ["pedir", "repetir"],
        "video_embed_id": "meS3lef4ubp",
        "drill_type": "conjugation",
        "tense": "present",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "All pronouns for all verbs",
            "targets": [
                {"verb": v, "pronoun": p}
                for v in ["pedir", "repetir"]
                for p in PRONOUNS
            ],
        },
    },
    "grammar_preterite_regular": {
        "title": "Preterite Regular",
        "vocab_level": 120,
        "word_workload": ["hablar", "encontrar", "comer", "unir", "beber", "salir"],
        "video_embed_id": "uBOH6A3vO0U",
        "drill_type": "conjugation",
        "tense": "preterite",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "All pronouns for hablar, comer, salir",
            "targets": [
                {"verb": v, "pronoun": p}
                for v in ["hablar", "comer", "salir"]
                for p in PRONOUNS
            ],
        },
    },
    "grammar_preterite_irregular": {
        "title": "Preterite Highly Irregular",
        "vocab_level": 200,
        "word_workload": ["ser", "ir", "dar", "ver", "hacer", "decir", "traer", "dormir", "morir"],
        "video_embed_id": "Ib68zJ3q7i8",
        "drill_type": "conjugation",
        "tense": "preterite",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "All pronouns for all verbs",
            "targets": [
                {"verb": v, "pronoun": p}
                for v in ["ser", "ir", "dar", "ver", "hacer", "decir", "traer", "dormir", "morir"]
                for p in PRONOUNS
            ],
        },
    },
    "grammar_gerund": {
        "title": "Gerund",
        "vocab_level": 210,
        "word_workload": ["hablar", "beber", "caminar", "charlar", "comer", "inhibir", "prohibir", "salir"],
        "video_embed_id": "Xpma6w0jy7m",
        "drill_type": "conjugation",
        "tense": "gerund",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "1 random pronoun per verb",
            "pronoun_pattern": "random_1",
            "verbs": ["hablar", "beber", "caminar", "charlar", "comer", "inhibir", "prohibir", "salir"],
        },
    },
    "grammar_gustar_1": {
        "title": "Gustar Part 1",
        "vocab_level": 220,
        "word_workload": ["gusta"],
        "video_embed_id": "rfPPtJI9prc",
        "drill_type": "gustar",
        "tense": "gustar",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "gustar_singular"},
        "phase_2_config": {
            "description": "5 pronoun+gusta+noun combos",
            "targets": 5,
            "pattern": "pronoun_gusta_singular",
        },
    },
    "grammar_gustar_2": {
        "title": "Gustar Part 2",
        "vocab_level": 225,
        "word_workload": ["gustan"],
        "video_embed_id": "WjOxPPu1uQo",
        "drill_type": "gustar",
        "tense": "gustar",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "gustar_plural"},
        "phase_2_config": {
            "description": "5 pronoun+gustan+noun combos",
            "targets": 5,
            "pattern": "pronoun_gustan_plural",
        },
    },
    "grammar_gustar_3": {
        "title": "Gustar Part 3",
        "vocab_level": 230,
        "word_workload": ["gusta", "gustan"],
        "video_embed_id": "lIAdqI5fpun",
        "drill_type": "gustar_prefix",
        "tense": "gustar",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": False},
        "phase_1c_config": {"total_items": 5, "mode": "gustar_prefix"},
        "phase_2_config": {
            "description": "1 per pronoun type (10 total)",
            "targets": 10,
            "pattern": "a_prefix",
        },
    },
    "grammar_ir_a_inf": {
        "title": "Ir A + Infinitive",
        "vocab_level": 235,
        "word_workload": ["hablar", "comer", "dormir", "vivir", "escribir"],
        "video_embed_id": "geHPDI9tMdH",
        "drill_type": "ir_a_inf",
        "tense": "ir_a_infinitive",
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": True, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "All pronouns for 2 verbs",
            "pronoun_pattern": "all",
            "verb_subset": 2,
            "verbs": ["hablar", "comer", "dormir", "vivir", "escribir"],
        },
    },
}


def get_grammar_config(situation_id: str) -> dict | None:
    """Get grammar config for a situation ID, or None if not a grammar situation."""
    return GRAMMAR_SITUATIONS.get(situation_id)


def get_all_grammar_situation_ids() -> list[str]:
    """Get all grammar situation IDs sorted by vocab_level."""
    return sorted(GRAMMAR_SITUATIONS.keys(), key=lambda k: GRAMMAR_SITUATIONS[k]["vocab_level"])


def get_grammar_gate_for_vocab_level(vocab_level: int) -> str | None:
    """Get the grammar situation ID that should gate at a given vocab level.

    Returns the highest-threshold grammar situation whose vocab_level <= the user's level,
    or None if no gate applies.
    """
    applicable = [
        (cfg["vocab_level"], sid)
        for sid, cfg in GRAMMAR_SITUATIONS.items()
        if cfg["vocab_level"] <= vocab_level
    ]
    if not applicable:
        return None
    applicable.sort(reverse=True)
    return applicable[0][1]
