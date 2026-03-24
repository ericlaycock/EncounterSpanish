"""Grammar situation configuration — single source of truth.

Each entry defines the grammar situation's word workload, drill type,
phase availability, and conversation config for phases 2/3.
"""

GRAMMAR_WORD_TRANSLATIONS = {
    # Pronouns
    "yo": "I (subject pronoun)",
    "tú": "you (informal)",
    "tu": "your (informal)",
    "él": "he/him",
    "ella": "she/her",
    "usted": "you (formal)",
    "nosotros": "we (masc./mixed)",
    "nosotras": "we (all fem.)",
    "ellos": "they (masc./mixed)",
    "ellas": "they (all fem.)",
    "ustedes": "you all (formal plural)",
    "su": "his/her/your/their",
    # Articles
    "el": "the (masculine)",
    "los": "the (masc. plural)",
    "la": "the (feminine)",
    "las": "the (fem. plural)",
    "un": "a (masc.)",
    "unos": "some (masc.)",
    "una": "a (fem.)",
    "unas": "some (fem.)",
    # Verbs
    "hablar": "to speak",
    "escuchar": "to listen",
    "beber": "to drink",
    "comer": "to eat",
    "vivir": "to live",
    "escribir": "to write",
    "ser": "to be (permanent)",
    "estar": "to be (temporary)",
    "ir": "to go",
    "dar": "to give",
    "tener": "to have",
    "venir": "to come",
    "caer": "to fall",
    "traer": "to bring",
    "hacer": "to do/make",
    "poner": "to put",
    "salir": "to leave/go out",
    "valer": "to be worth",
    "decir": "to say/tell",
    "oír": "to hear",
    "conseguir": "to get/obtain",
    "recoger": "to pick up",
    "dirigir": "to direct",
    "convencer": "to convince",
    "conocer": "to know (person/place)",
    "producir": "to produce",
    "construir": "to build",
    "continuar": "to continue",
    "mover": "to move",
    "almorzar": "to have lunch",
    "morir": "to die",
    "cerrar": "to close",
    "entender": "to understand",
    "pedir": "to ask for",
    "repetir": "to repeat",
    "encontrar": "to find",
    "unir": "to join/unite",
    "ver": "to see",
    "dormir": "to sleep",
    "caminar": "to walk",
    "charlar": "to chat",
    "inhibir": "to inhibit",
    "prohibir": "to prohibit",
    "gusta": "is pleasing (sing.)",
    "gustan": "are pleasing (pl.)",
}

PRONOUNS = ["yo", "tú", "él", "ella", "usted", "nosotros", "nosotras", "ellos", "ellas", "ustedes"]

GRAMMAR_SITUATIONS = {
    "grammar_pronouns": {
        "title": "Pronouns",
        "vocab_level": 15,
        "word_workload": ["yo", "tú", "él", "ella", "usted", "nosotros", "nosotras", "ellos", "ellas", "ustedes", "su"],
        "video_embed_id": "bLZk006G5ge",
        "drill_type": "skip",
        "tense": "pronouns",
        "phases": {"0a": True, "0b": False, "1a": True, "1b": True, "1c": False, "2": True, "3": False},
        "phase_2_config": {
            "description": "All pronouns + 'su' in conversation",
            "targets": [{"word": p} for p in ["yo", "tú", "él", "ella", "usted", "nosotros", "nosotras", "ellos", "ellas", "ustedes", "su"]],
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
        "drill_config": {
        "answers": {
                "hablar": {
                        "yo": "hablo",
                        "tú": "hablas",
                        "él": "habla",
                        "ella": "habla",
                        "usted": "habla",
                        "nosotros": "hablamos",
                        "nosotras": "hablamos",
                        "ellos": "hablan",
                        "ellas": "hablan",
                        "ustedes": "hablan"
                },
                "escuchar": {
                        "yo": "escucho",
                        "tú": "escuchas",
                        "él": "escucha",
                        "ella": "escucha",
                        "usted": "escucha",
                        "nosotros": "escuchamos",
                        "nosotras": "escuchamos",
                        "ellos": "escuchan",
                        "ellas": "escuchan",
                        "ustedes": "escuchan"
                },
                "beber": {
                        "yo": "bebo",
                        "tú": "bebes",
                        "él": "bebe",
                        "ella": "bebe",
                        "usted": "bebe",
                        "nosotros": "bebemos",
                        "nosotras": "bebemos",
                        "ellos": "beben",
                        "ellas": "beben",
                        "ustedes": "beben"
                },
                "comer": {
                        "yo": "como",
                        "tú": "comes",
                        "él": "come",
                        "ella": "come",
                        "usted": "come",
                        "nosotros": "comemos",
                        "nosotras": "comemos",
                        "ellos": "comen",
                        "ellas": "comen",
                        "ustedes": "comen"
                },
                "vivir": {
                        "yo": "vivo",
                        "tú": "vives",
                        "él": "vive",
                        "ella": "vive",
                        "usted": "vive",
                        "nosotros": "vivimos",
                        "nosotras": "vivimos",
                        "ellos": "viven",
                        "ellas": "viven",
                        "ustedes": "viven"
                },
                "escribir": {
                        "yo": "escribo",
                        "tú": "escribes",
                        "él": "escribe",
                        "ella": "escribe",
                        "usted": "escribe",
                        "nosotros": "escribimos",
                        "nosotras": "escribimos",
                        "ellos": "escriben",
                        "ellas": "escriben",
                        "ustedes": "escriben"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "drill_config": {
        "answers": {
                "ser": {
                        "yo": "soy",
                        "tú": "eres",
                        "él": "es",
                        "ella": "es",
                        "usted": "es",
                        "nosotros": "somos",
                        "nosotras": "somos",
                        "ellos": "son",
                        "ellas": "son",
                        "ustedes": "son"
                },
                "estar": {
                        "yo": "estoy",
                        "tú": "estás",
                        "él": "está",
                        "ella": "está",
                        "usted": "está",
                        "nosotros": "estamos",
                        "nosotras": "estamos",
                        "ellos": "están",
                        "ellas": "están",
                        "ustedes": "están"
                },
                "ir": {
                        "yo": "voy",
                        "tú": "vas",
                        "él": "va",
                        "ella": "va",
                        "usted": "va",
                        "nosotros": "vamos",
                        "nosotras": "vamos",
                        "ellos": "van",
                        "ellas": "van",
                        "ustedes": "van"
                },
                "dar": {
                        "yo": "doy",
                        "tú": "das",
                        "él": "da",
                        "ella": "da",
                        "usted": "da",
                        "nosotros": "damos",
                        "nosotras": "damos",
                        "ellos": "dan",
                        "ellas": "dan",
                        "ustedes": "dan"
                },
                "tener": {
                        "yo": "tengo",
                        "tú": "tienes",
                        "él": "tiene",
                        "ella": "tiene",
                        "usted": "tiene",
                        "nosotros": "tenemos",
                        "nosotras": "tenemos",
                        "ellos": "tienen",
                        "ellas": "tienen",
                        "ustedes": "tienen"
                },
                "venir": {
                        "yo": "vengo",
                        "tú": "vienes",
                        "él": "viene",
                        "ella": "viene",
                        "usted": "viene",
                        "nosotros": "venimos",
                        "nosotras": "venimos",
                        "ellos": "vienen",
                        "ellas": "vienen",
                        "ustedes": "vienen"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "word_workload": ["caer", "traer", "hacer", "poner", "salir", "valer", "decir", "oír"],
        "video_embed_id": "tPXOw1Rz82y",
        "drill_type": "conjugation",
        "tense": "present",
        "drill_config": {
        "answers": {
                "caer": {
                        "yo": "caigo",
                        "tú": "caes",
                        "él": "cae",
                        "ella": "cae",
                        "usted": "cae",
                        "nosotros": "caemos",
                        "nosotras": "caemos",
                        "ellos": "caen",
                        "ellas": "caen",
                        "ustedes": "caen"
                },
                "traer": {
                        "yo": "traigo",
                        "tú": "traes",
                        "él": "trae",
                        "ella": "trae",
                        "usted": "trae",
                        "nosotros": "traemos",
                        "nosotras": "traemos",
                        "ellos": "traen",
                        "ellas": "traen",
                        "ustedes": "traen"
                },
                "hacer": {
                        "yo": "hago",
                        "tú": "haces",
                        "él": "hace",
                        "ella": "hace",
                        "usted": "hace",
                        "nosotros": "hacemos",
                        "nosotras": "hacemos",
                        "ellos": "hacen",
                        "ellas": "hacen",
                        "ustedes": "hacen"
                },
                "poner": {
                        "yo": "pongo",
                        "tú": "pones",
                        "él": "pone",
                        "ella": "pone",
                        "usted": "pone",
                        "nosotros": "ponemos",
                        "nosotras": "ponemos",
                        "ellos": "ponen",
                        "ellas": "ponen",
                        "ustedes": "ponen"
                },
                "salir": {
                        "yo": "salgo",
                        "tú": "sales",
                        "él": "sale",
                        "ella": "sale",
                        "usted": "sale",
                        "nosotros": "salimos",
                        "nosotras": "salimos",
                        "ellos": "salen",
                        "ellas": "salen",
                        "ustedes": "salen"
                },
                "valer": {
                        "yo": "valgo",
                        "tú": "vales",
                        "él": "vale",
                        "ella": "vale",
                        "usted": "vale",
                        "nosotros": "valemos",
                        "nosotras": "valemos",
                        "ellos": "valen",
                        "ellas": "valen",
                        "ustedes": "valen"
                },
                "decir": {
                        "yo": "digo",
                        "tú": "dices",
                        "él": "dice",
                        "ella": "dice",
                        "usted": "dice",
                        "nosotros": "decimos",
                        "nosotras": "decimos",
                        "ellos": "dicen",
                        "ellas": "dicen",
                        "ustedes": "dicen"
                },
                "oír": {
                        "yo": "oigo",
                        "tú": "oyes",
                        "él": "oye",
                        "ella": "oye",
                        "usted": "oye",
                        "nosotros": "oímos",
                        "nosotras": "oímos",
                        "ellos": "oyen",
                        "ellas": "oyen",
                        "ustedes": "oyen"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
        "phase_1c_config": {"total_items": 5, "mode": "random_pronoun_verb"},
        "phase_2_config": {
            "description": "2 random pronouns per verb",
            "pronoun_pattern": "random_2",
            "verbs": ["caer", "traer", "hacer", "poner", "salir", "valer", "decir", "oír"],
        },
    },
    "grammar_spelling_changes": {
        "title": "Spelling Changes",
        "vocab_level": 70,
        "word_workload": ["conseguir", "recoger", "dirigir", "convencer", "conocer", "producir", "construir", "continuar"],
        "video_embed_id": "dYyywu1hOVp",
        "drill_type": "conjugation",
        "tense": "present",
        "drill_config": {
        "answers": {
                "conseguir": {
                        "yo": "consigo",
                        "tú": "consigues",
                        "él": "consigue",
                        "ella": "consigue",
                        "usted": "consigue",
                        "nosotros": "conseguimos",
                        "nosotras": "conseguimos",
                        "ellos": "consiguen",
                        "ellas": "consiguen",
                        "ustedes": "consiguen"
                },
                "recoger": {
                        "yo": "recojo",
                        "tú": "recoges",
                        "él": "recoge",
                        "ella": "recoge",
                        "usted": "recoge",
                        "nosotros": "recogemos",
                        "nosotras": "recogemos",
                        "ellos": "recogen",
                        "ellas": "recogen",
                        "ustedes": "recogen"
                },
                "dirigir": {
                        "yo": "dirijo",
                        "tú": "diriges",
                        "él": "dirige",
                        "ella": "dirige",
                        "usted": "dirige",
                        "nosotros": "dirigimos",
                        "nosotras": "dirigimos",
                        "ellos": "dirigen",
                        "ellas": "dirigen",
                        "ustedes": "dirigen"
                },
                "convencer": {
                        "yo": "convenzo",
                        "tú": "convences",
                        "él": "convence",
                        "ella": "convence",
                        "usted": "convence",
                        "nosotros": "convencemos",
                        "nosotras": "convencemos",
                        "ellos": "convencen",
                        "ellas": "convencen",
                        "ustedes": "convencen"
                },
                "conocer": {
                        "yo": "conozco",
                        "tú": "conoces",
                        "él": "conoce",
                        "ella": "conoce",
                        "usted": "conoce",
                        "nosotros": "conocemos",
                        "nosotras": "conocemos",
                        "ellos": "conocen",
                        "ellas": "conocen",
                        "ustedes": "conocen"
                },
                "producir": {
                        "yo": "produzco",
                        "tú": "produces",
                        "él": "produce",
                        "ella": "produce",
                        "usted": "produce",
                        "nosotros": "producimos",
                        "nosotras": "producimos",
                        "ellos": "producen",
                        "ellas": "producen",
                        "ustedes": "producen"
                },
                "construir": {
                        "yo": "construyo",
                        "tú": "construyes",
                        "él": "construye",
                        "ella": "construye",
                        "usted": "construye",
                        "nosotros": "construimos",
                        "nosotras": "construimos",
                        "ellos": "construyen",
                        "ellas": "construyen",
                        "ustedes": "construyen"
                },
                "continuar": {
                        "yo": "continúo",
                        "tú": "continúas",
                        "él": "continúa",
                        "ella": "continúa",
                        "usted": "continúa",
                        "nosotros": "continuamos",
                        "nosotras": "continuamos",
                        "ellos": "continúan",
                        "ellas": "continúan",
                        "ustedes": "continúan"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "drill_config": {
        "answers": {
                "mover": {
                        "yo": "muevo",
                        "tú": "mueves",
                        "él": "mueve",
                        "ella": "mueve",
                        "usted": "mueve",
                        "nosotros": "movemos",
                        "nosotras": "movemos",
                        "ellos": "mueven",
                        "ellas": "mueven",
                        "ustedes": "mueven"
                },
                "almorzar": {
                        "yo": "almuerzo",
                        "tú": "almuerzas",
                        "él": "almuerza",
                        "ella": "almuerza",
                        "usted": "almuerza",
                        "nosotros": "almorzamos",
                        "nosotras": "almorzamos",
                        "ellos": "almuerzan",
                        "ellas": "almuerzan",
                        "ustedes": "almuerzan"
                },
                "morir": {
                        "yo": "muero",
                        "tú": "mueres",
                        "él": "muere",
                        "ella": "muere",
                        "usted": "muere",
                        "nosotros": "morimos",
                        "nosotras": "morimos",
                        "ellos": "mueren",
                        "ellas": "mueren",
                        "ustedes": "mueren"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "drill_config": {
        "answers": {
                "cerrar": {
                        "yo": "cierro",
                        "tú": "cierras",
                        "él": "cierra",
                        "ella": "cierra",
                        "usted": "cierra",
                        "nosotros": "cerramos",
                        "nosotras": "cerramos",
                        "ellos": "cierran",
                        "ellas": "cierran",
                        "ustedes": "cierran"
                },
                "entender": {
                        "yo": "entiendo",
                        "tú": "entiendes",
                        "él": "entiende",
                        "ella": "entiende",
                        "usted": "entiende",
                        "nosotros": "entendemos",
                        "nosotras": "entendemos",
                        "ellos": "entienden",
                        "ellas": "entienden",
                        "ustedes": "entienden"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "drill_config": {
        "answers": {
                "pedir": {
                        "yo": "pido",
                        "tú": "pides",
                        "él": "pide",
                        "ella": "pide",
                        "usted": "pide",
                        "nosotros": "pedimos",
                        "nosotras": "pedimos",
                        "ellos": "piden",
                        "ellas": "piden",
                        "ustedes": "piden"
                },
                "repetir": {
                        "yo": "repito",
                        "tú": "repites",
                        "él": "repite",
                        "ella": "repite",
                        "usted": "repite",
                        "nosotros": "repetimos",
                        "nosotras": "repetimos",
                        "ellos": "repiten",
                        "ellas": "repiten",
                        "ustedes": "repiten"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "drill_config": {
        "answers": {
                "hablar": {
                        "yo": "hablé",
                        "tú": "hablaste",
                        "él": "habló",
                        "ella": "habló",
                        "usted": "habló",
                        "nosotros": "hablamos",
                        "nosotras": "hablamos",
                        "ellos": "hablaron",
                        "ellas": "hablaron",
                        "ustedes": "hablaron"
                },
                "encontrar": {
                        "yo": "encontré",
                        "tú": "encontraste",
                        "él": "encontró",
                        "ella": "encontró",
                        "usted": "encontró",
                        "nosotros": "encontramos",
                        "nosotras": "encontramos",
                        "ellos": "encontraron",
                        "ellas": "encontraron",
                        "ustedes": "encontraron"
                },
                "comer": {
                        "yo": "comí",
                        "tú": "comiste",
                        "él": "comió",
                        "ella": "comió",
                        "usted": "comió",
                        "nosotros": "comimos",
                        "nosotras": "comimos",
                        "ellos": "comieron",
                        "ellas": "comieron",
                        "ustedes": "comieron"
                },
                "unir": {
                        "yo": "uní",
                        "tú": "uniste",
                        "él": "unió",
                        "ella": "unió",
                        "usted": "unió",
                        "nosotros": "unimos",
                        "nosotras": "unimos",
                        "ellos": "unieron",
                        "ellas": "unieron",
                        "ustedes": "unieron"
                },
                "beber": {
                        "yo": "bebí",
                        "tú": "bebiste",
                        "él": "bebió",
                        "ella": "bebió",
                        "usted": "bebió",
                        "nosotros": "bebimos",
                        "nosotras": "bebimos",
                        "ellos": "bebieron",
                        "ellas": "bebieron",
                        "ustedes": "bebieron"
                },
                "salir": {
                        "yo": "salí",
                        "tú": "saliste",
                        "él": "salió",
                        "ella": "salió",
                        "usted": "salió",
                        "nosotros": "salimos",
                        "nosotras": "salimos",
                        "ellos": "salieron",
                        "ellas": "salieron",
                        "ustedes": "salieron"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "drill_config": {
        "answers": {
                "ser": {
                        "yo": "fui",
                        "tú": "fuiste",
                        "él": "fue",
                        "ella": "fue",
                        "usted": "fue",
                        "nosotros": "fuimos",
                        "nosotras": "fuimos",
                        "ellos": "fueron",
                        "ellas": "fueron",
                        "ustedes": "fueron"
                },
                "ir": {
                        "yo": "fui",
                        "tú": "fuiste",
                        "él": "fue",
                        "ella": "fue",
                        "usted": "fue",
                        "nosotros": "fuimos",
                        "nosotras": "fuimos",
                        "ellos": "fueron",
                        "ellas": "fueron",
                        "ustedes": "fueron"
                },
                "dar": {
                        "yo": "di",
                        "tú": "diste",
                        "él": "dio",
                        "ella": "dio",
                        "usted": "dio",
                        "nosotros": "dimos",
                        "nosotras": "dimos",
                        "ellos": "dieron",
                        "ellas": "dieron",
                        "ustedes": "dieron"
                },
                "ver": {
                        "yo": "vi",
                        "tú": "viste",
                        "él": "vio",
                        "ella": "vio",
                        "usted": "vio",
                        "nosotros": "vimos",
                        "nosotras": "vimos",
                        "ellos": "vieron",
                        "ellas": "vieron",
                        "ustedes": "vieron"
                },
                "hacer": {
                        "yo": "hice",
                        "tú": "hiciste",
                        "él": "hizo",
                        "ella": "hizo",
                        "usted": "hizo",
                        "nosotros": "hicimos",
                        "nosotras": "hicimos",
                        "ellos": "hicieron",
                        "ellas": "hicieron",
                        "ustedes": "hicieron"
                },
                "decir": {
                        "yo": "dije",
                        "tú": "dijiste",
                        "él": "dijo",
                        "ella": "dijo",
                        "usted": "dijo",
                        "nosotros": "dijimos",
                        "nosotras": "dijimos",
                        "ellos": "dijeron",
                        "ellas": "dijeron",
                        "ustedes": "dijeron"
                },
                "traer": {
                        "yo": "traje",
                        "tú": "trajiste",
                        "él": "trajo",
                        "ella": "trajo",
                        "usted": "trajo",
                        "nosotros": "trajimos",
                        "nosotras": "trajimos",
                        "ellos": "trajeron",
                        "ellas": "trajeron",
                        "ustedes": "trajeron"
                },
                "dormir": {
                        "yo": "dormí",
                        "tú": "dormiste",
                        "él": "durmió",
                        "ella": "durmió",
                        "usted": "durmió",
                        "nosotros": "dormimos",
                        "nosotras": "dormimos",
                        "ellos": "durmieron",
                        "ellas": "durmieron",
                        "ustedes": "durmieron"
                },
                "morir": {
                        "yo": "morí",
                        "tú": "moriste",
                        "él": "murió",
                        "ella": "murió",
                        "usted": "murió",
                        "nosotros": "morimos",
                        "nosotras": "morimos",
                        "ellos": "murieron",
                        "ellas": "murieron",
                        "ustedes": "murieron"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "drill_config": {
        "answers": {
                "hablar": {
                        "yo": "estoy hablando",
                        "tú": "estás hablando",
                        "él": "está hablando",
                        "ella": "está hablando",
                        "usted": "está hablando",
                        "nosotros": "estamos hablando",
                        "nosotras": "estamos hablando",
                        "ellos": "están hablando",
                        "ellas": "están hablando",
                        "ustedes": "están hablando"
                },
                "beber": {
                        "yo": "estoy bebiendo",
                        "tú": "estás bebiendo",
                        "él": "está bebiendo",
                        "ella": "está bebiendo",
                        "usted": "está bebiendo",
                        "nosotros": "estamos bebiendo",
                        "nosotras": "estamos bebiendo",
                        "ellos": "están bebiendo",
                        "ellas": "están bebiendo",
                        "ustedes": "están bebiendo"
                },
                "caminar": {
                        "yo": "estoy caminando",
                        "tú": "estás caminando",
                        "él": "está caminando",
                        "ella": "está caminando",
                        "usted": "está caminando",
                        "nosotros": "estamos caminando",
                        "nosotras": "estamos caminando",
                        "ellos": "están caminando",
                        "ellas": "están caminando",
                        "ustedes": "están caminando"
                },
                "charlar": {
                        "yo": "estoy charlando",
                        "tú": "estás charlando",
                        "él": "está charlando",
                        "ella": "está charlando",
                        "usted": "está charlando",
                        "nosotros": "estamos charlando",
                        "nosotras": "estamos charlando",
                        "ellos": "están charlando",
                        "ellas": "están charlando",
                        "ustedes": "están charlando"
                },
                "comer": {
                        "yo": "estoy comiendo",
                        "tú": "estás comiendo",
                        "él": "está comiendo",
                        "ella": "está comiendo",
                        "usted": "está comiendo",
                        "nosotros": "estamos comiendo",
                        "nosotras": "estamos comiendo",
                        "ellos": "están comiendo",
                        "ellas": "están comiendo",
                        "ustedes": "están comiendo"
                },
                "inhibir": {
                        "yo": "estoy inhibiendo",
                        "tú": "estás inhibiendo",
                        "él": "está inhibiendo",
                        "ella": "está inhibiendo",
                        "usted": "está inhibiendo",
                        "nosotros": "estamos inhibiendo",
                        "nosotras": "estamos inhibiendo",
                        "ellos": "están inhibiendo",
                        "ellas": "están inhibiendo",
                        "ustedes": "están inhibiendo"
                },
                "prohibir": {
                        "yo": "estoy prohibiendo",
                        "tú": "estás prohibiendo",
                        "él": "está prohibiendo",
                        "ella": "está prohibiendo",
                        "usted": "está prohibiendo",
                        "nosotros": "estamos prohibiendo",
                        "nosotras": "estamos prohibiendo",
                        "ellos": "están prohibiendo",
                        "ellas": "están prohibiendo",
                        "ustedes": "están prohibiendo"
                },
                "salir": {
                        "yo": "estoy saliendo",
                        "tú": "estás saliendo",
                        "él": "está saliendo",
                        "ella": "está saliendo",
                        "usted": "está saliendo",
                        "nosotros": "estamos saliendo",
                        "nosotras": "estamos saliendo",
                        "ellos": "están saliendo",
                        "ellas": "están saliendo",
                        "ustedes": "están saliendo"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "drill_config": {
        "items": [
                {
                        "prompt": "I like (el café)",
                        "answer": "me gusta",
                        "hint": "me"
                },
                {
                        "prompt": "You like (la música)",
                        "answer": "te gusta",
                        "hint": "te"
                },
                {
                        "prompt": "He likes (el libro)",
                        "answer": "le gusta",
                        "hint": "le"
                },
                {
                        "prompt": "She likes (la película)",
                        "answer": "le gusta",
                        "hint": "le"
                },
                {
                        "prompt": "We like (el chocolate)",
                        "answer": "nos gusta",
                        "hint": "nos"
                },
                {
                        "prompt": "We like (la playa)",
                        "answer": "nos gusta",
                        "hint": "nos"
                },
                {
                        "prompt": "They like (el fútbol)",
                        "answer": "les gusta",
                        "hint": "les"
                },
                {
                        "prompt": "They like (la comida)",
                        "answer": "les gusta",
                        "hint": "les"
                },
                {
                        "prompt": "You (formal) like (el té)",
                        "answer": "le gusta",
                        "hint": "le"
                },
                {
                        "prompt": "I like (la fruta)",
                        "answer": "me gusta",
                        "hint": "me"
                },
                {
                        "prompt": "You like (el cine)",
                        "answer": "te gusta",
                        "hint": "te"
                },
                {
                        "prompt": "They like (la ciudad)",
                        "answer": "les gusta",
                        "hint": "les"
                }
        ]
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "drill_config": {
        "items": [
                {
                        "prompt": "I like (los gatos)",
                        "answer": "me gustan",
                        "hint": "me"
                },
                {
                        "prompt": "I like (las manzanas)",
                        "answer": "me gustan",
                        "hint": "me"
                },
                {
                        "prompt": "You like (los libros)",
                        "answer": "te gustan",
                        "hint": "te"
                },
                {
                        "prompt": "You like (las flores)",
                        "answer": "te gustan",
                        "hint": "te"
                },
                {
                        "prompt": "He/She likes (los perros)",
                        "answer": "le gustan",
                        "hint": "le"
                },
                {
                        "prompt": "He/She likes (las películas)",
                        "answer": "le gustan",
                        "hint": "le"
                },
                {
                        "prompt": "We like (los coches)",
                        "answer": "nos gustan",
                        "hint": "nos"
                },
                {
                        "prompt": "We like (las canciones)",
                        "answer": "nos gustan",
                        "hint": "nos"
                },
                {
                        "prompt": "They like (los deportes)",
                        "answer": "les gustan",
                        "hint": "les"
                },
                {
                        "prompt": "They like (las frutas)",
                        "answer": "les gustan",
                        "hint": "les"
                },
                {
                        "prompt": "You all like (los árboles)",
                        "answer": "les gustan",
                        "hint": "les"
                },
                {
                        "prompt": "You all like (las montañas)",
                        "answer": "les gustan",
                        "hint": "les"
                }
        ]
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
        "drill_config": {
        "items": [
                {
                        "prompt": "me gusta el gato",
                        "answer": "a mí",
                        "hint": "a mí"
                },
                {
                        "prompt": "te gusta la música",
                        "answer": "a ti",
                        "hint": "a ti"
                },
                {
                        "prompt": "le gusta el fútbol",
                        "answer": "a él",
                        "hint": "a él"
                },
                {
                        "prompt": "le gusta la playa",
                        "answer": "a ella",
                        "hint": "a ella"
                },
                {
                        "prompt": "le gusta el libro",
                        "answer": "a usted",
                        "hint": "a usted"
                },
                {
                        "prompt": "nos gusta la pizza",
                        "answer": "a nosotros",
                        "hint": "a nosotros"
                },
                {
                        "prompt": "les gusta el cine",
                        "answer": "a ellos",
                        "hint": "a ellos"
                },
                {
                        "prompt": "les gusta la clase",
                        "answer": "a ustedes",
                        "hint": "a ustedes"
                },
                {
                        "prompt": "me gusta bailar",
                        "answer": "a mí",
                        "hint": "a mí"
                },
                {
                        "prompt": "te gusta correr",
                        "answer": "a ti",
                        "hint": "a ti"
                },
                {
                        "prompt": "le gusta viajar",
                        "answer": "a ella",
                        "hint": "a ella"
                },
                {
                        "prompt": "les gusta estudiar",
                        "answer": "a ellos",
                        "hint": "a ellos"
                }
        ]
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": False},
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
        "drill_config": {
        "answers": {
                "hablar": {
                        "yo": "voy a hablar",
                        "tú": "vas a hablar",
                        "él": "va a hablar",
                        "ella": "va a hablar",
                        "usted": "va a hablar",
                        "nosotros": "vamos a hablar",
                        "nosotras": "vamos a hablar",
                        "ellos": "van a hablar",
                        "ellas": "van a hablar",
                        "ustedes": "van a hablar"
                },
                "comer": {
                        "yo": "voy a comer",
                        "tú": "vas a comer",
                        "él": "va a comer",
                        "ella": "va a comer",
                        "usted": "va a comer",
                        "nosotros": "vamos a comer",
                        "nosotras": "vamos a comer",
                        "ellos": "van a comer",
                        "ellas": "van a comer",
                        "ustedes": "van a comer"
                },
                "dormir": {
                        "yo": "voy a dormir",
                        "tú": "vas a dormir",
                        "él": "va a dormir",
                        "ella": "va a dormir",
                        "usted": "va a dormir",
                        "nosotros": "vamos a dormir",
                        "nosotras": "vamos a dormir",
                        "ellos": "van a dormir",
                        "ellas": "van a dormir",
                        "ustedes": "van a dormir"
                },
                "vivir": {
                        "yo": "voy a vivir",
                        "tú": "vas a vivir",
                        "él": "va a vivir",
                        "ella": "va a vivir",
                        "usted": "va a vivir",
                        "nosotros": "vamos a vivir",
                        "nosotras": "vamos a vivir",
                        "ellos": "van a vivir",
                        "ellas": "van a vivir",
                        "ustedes": "van a vivir"
                },
                "escribir": {
                        "yo": "voy a escribir",
                        "tú": "vas a escribir",
                        "él": "va a escribir",
                        "ella": "va a escribir",
                        "usted": "va a escribir",
                        "nosotros": "vamos a escribir",
                        "nosotras": "vamos a escribir",
                        "ellos": "van a escribir",
                        "ellas": "van a escribir",
                        "ustedes": "van a escribir"
                }
        }
},
        "phases": {"0a": True, "0b": True, "1a": False, "1b": False, "1c": False, "2": True, "3": True},
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
