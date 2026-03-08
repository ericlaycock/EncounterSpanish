"""Central seed bank — single source of truth for all word and situation data.

All encounter words, high-frequency words, situations, and their links
are defined here. Grammar situations are in grammar_situations.py.
The seed script (scripts/seed_qa.py) reads from this module.
"""

from app.data.hf_words import HIGH_FREQUENCY_WORDS  # noqa: F401 — re-exported

# --- Category display names (used by API and onboarding) ---

CATEGORY_NAMES = {
    "airport": "Airport",
    "banking": "Banking",
    "clothing": "Clothing Shopping",
    "internet": "Internet",
    "small_talk": "Small Talk",
    "contractor": "Home Renovation",
    "groceries": "Groceries",
    "mechanic": "Mechanic",
    "police": "Police Stop",
    "restaurant": "Eating Out",
}

# HIGH_FREQUENCY_WORDS is imported from app.data.hf_words (1000 entries)

# --- Encounter words by category ---

ENCOUNTER_WORDS = {
    "banking": [
        {"id": "enc_bank_1", "spanish": "cuenta", "english": "account"},
        {"id": "enc_bank_2", "spanish": "depositar", "english": "to deposit"},
        {"id": "enc_bank_3", "spanish": "retirar", "english": "to withdraw"},
        {"id": "enc_bank_4", "spanish": "transferencia", "english": "transfer"},
        {"id": "enc_bank_5", "spanish": "saldo", "english": "balance"},
        {"id": "enc_bank_6", "spanish": "prestamo", "english": "loan"},
    ],
    "restaurant": [
        {"id": "enc_rest_1", "spanish": "mesa", "english": "table"},
        {"id": "enc_rest_2", "spanish": "menu", "english": "menu"},
        {"id": "enc_rest_3", "spanish": "propina", "english": "tip"},
        {"id": "enc_rest_4", "spanish": "cuenta", "english": "bill/check"},
        {"id": "enc_rest_5", "spanish": "mesero", "english": "waiter"},
        {"id": "enc_rest_6", "spanish": "reservacion", "english": "reservation"},
    ],
    "airport": [
        {"id": "enc_air_1", "spanish": "pasaporte", "english": "passport"},
        {"id": "enc_air_2", "spanish": "equipaje", "english": "luggage"},
        {"id": "enc_air_3", "spanish": "vuelo", "english": "flight"},
    ],
    "groceries": [
        {"id": "enc_groc_1", "spanish": "carrito", "english": "cart"},
        {"id": "enc_groc_2", "spanish": "cajero", "english": "cashier"},
        {"id": "enc_groc_3", "spanish": "bolsa", "english": "bag"},
    ],
    "mechanic": [
        {"id": "enc_mech_1", "spanish": "llanta", "english": "tire"},
        {"id": "enc_mech_2", "spanish": "aceite", "english": "oil"},
        {"id": "enc_mech_3", "spanish": "frenos", "english": "brakes"},
    ],
    "clothing": [
        {"id": "enc_cloth_1", "spanish": "talla", "english": "size"},
        {"id": "enc_cloth_2", "spanish": "probador", "english": "fitting room"},
        {"id": "enc_cloth_3", "spanish": "descuento", "english": "discount"},
    ],
    "internet": [
        {"id": "enc_int_1", "spanish": "contrasena", "english": "password"},
        {"id": "enc_int_2", "spanish": "wifi", "english": "WiFi"},
        {"id": "enc_int_3", "spanish": "plan", "english": "plan"},
    ],
    "small_talk": [
        {"id": "enc_talk_1", "spanish": "vecino", "english": "neighbor"},
        {"id": "enc_talk_2", "spanish": "barrio", "english": "neighborhood"},
        {"id": "enc_talk_3", "spanish": "tiempo", "english": "weather"},
    ],
    "contractor": [
        {"id": "enc_contr_1", "spanish": "presupuesto", "english": "budget/quote"},
        {"id": "enc_contr_2", "spanish": "pintura", "english": "paint"},
        {"id": "enc_contr_3", "spanish": "plomero", "english": "plumber"},
    ],
    "police": [
        {"id": "enc_police_1", "spanish": "licencia", "english": "license"},
        {"id": "enc_police_2", "spanish": "seguro", "english": "insurance"},
        {"id": "enc_police_3", "spanish": "multa", "english": "fine/ticket"},
    ],
}

# --- Situations (main encounters) ---

SITUATIONS = [
    {"id": "banking_1", "title": "Opening a Bank Account", "category": "banking", "series_number": 1, "order_index": 1, "is_free": True},
    {"id": "banking_2", "title": "Wire Transfer", "category": "banking", "series_number": 2, "order_index": 2, "is_free": False},
    {"id": "banking_3", "title": "Currency Exchange", "category": "banking", "series_number": 3, "order_index": 3, "is_free": False},
    {"id": "restaurant_1", "title": "Ordering Food", "category": "restaurant", "series_number": 1, "order_index": 4, "is_free": True},
    {"id": "restaurant_2", "title": "Making a Reservation", "category": "restaurant", "series_number": 2, "order_index": 5, "is_free": False},
    {"id": "restaurant_3", "title": "Asking for the Bill", "category": "restaurant", "series_number": 3, "order_index": 6, "is_free": False},
    {"id": "airport_1", "title": "Checking In", "category": "airport", "series_number": 1, "order_index": 7, "is_free": True},
    {"id": "clothing_1", "title": "Finding the Right Size", "category": "clothing", "series_number": 1, "order_index": 8, "is_free": True},
    {"id": "internet_1", "title": "Setting Up WiFi", "category": "internet", "series_number": 1, "order_index": 9, "is_free": True},
    {"id": "small_talk_1", "title": "Meeting a Neighbor", "category": "small_talk", "series_number": 1, "order_index": 10, "is_free": True},
    {"id": "contractor_1", "title": "Hiring a Plumber", "category": "contractor", "series_number": 1, "order_index": 11, "is_free": True},
    {"id": "groceries_1", "title": "At the Supermarket", "category": "groceries", "series_number": 1, "order_index": 12, "is_free": True},
    {"id": "mechanic_1", "title": "Oil Change", "category": "mechanic", "series_number": 1, "order_index": 13, "is_free": True},
    {"id": "police_1", "title": "Traffic Stop", "category": "police", "series_number": 1, "order_index": 14, "is_free": True},
]

# --- SituationWord links (encounter words per situation) ---

SITUATION_WORDS = [
    # Banking
    {"situation_id": "banking_1", "word_id": "enc_bank_1", "position": 1},
    {"situation_id": "banking_1", "word_id": "enc_bank_2", "position": 2},
    {"situation_id": "banking_1", "word_id": "enc_bank_3", "position": 3},
    {"situation_id": "banking_2", "word_id": "enc_bank_4", "position": 1},
    {"situation_id": "banking_2", "word_id": "enc_bank_5", "position": 2},
    {"situation_id": "banking_2", "word_id": "enc_bank_6", "position": 3},
    {"situation_id": "banking_3", "word_id": "enc_bank_1", "position": 1},
    {"situation_id": "banking_3", "word_id": "enc_bank_4", "position": 2},
    {"situation_id": "banking_3", "word_id": "enc_bank_5", "position": 3},
    # Restaurant
    {"situation_id": "restaurant_1", "word_id": "enc_rest_1", "position": 1},
    {"situation_id": "restaurant_1", "word_id": "enc_rest_2", "position": 2},
    {"situation_id": "restaurant_1", "word_id": "enc_rest_3", "position": 3},
    {"situation_id": "restaurant_2", "word_id": "enc_rest_4", "position": 1},
    {"situation_id": "restaurant_2", "word_id": "enc_rest_5", "position": 2},
    {"situation_id": "restaurant_2", "word_id": "enc_rest_6", "position": 3},
    {"situation_id": "restaurant_3", "word_id": "enc_rest_1", "position": 1},
    {"situation_id": "restaurant_3", "word_id": "enc_rest_4", "position": 2},
    {"situation_id": "restaurant_3", "word_id": "enc_rest_5", "position": 3},
    # Airport
    {"situation_id": "airport_1", "word_id": "enc_air_1", "position": 1},
    {"situation_id": "airport_1", "word_id": "enc_air_2", "position": 2},
    {"situation_id": "airport_1", "word_id": "enc_air_3", "position": 3},
    # Clothing
    {"situation_id": "clothing_1", "word_id": "enc_cloth_1", "position": 1},
    {"situation_id": "clothing_1", "word_id": "enc_cloth_2", "position": 2},
    {"situation_id": "clothing_1", "word_id": "enc_cloth_3", "position": 3},
    # Internet
    {"situation_id": "internet_1", "word_id": "enc_int_1", "position": 1},
    {"situation_id": "internet_1", "word_id": "enc_int_2", "position": 2},
    {"situation_id": "internet_1", "word_id": "enc_int_3", "position": 3},
    # Small Talk
    {"situation_id": "small_talk_1", "word_id": "enc_talk_1", "position": 1},
    {"situation_id": "small_talk_1", "word_id": "enc_talk_2", "position": 2},
    {"situation_id": "small_talk_1", "word_id": "enc_talk_3", "position": 3},
    # Contractor
    {"situation_id": "contractor_1", "word_id": "enc_contr_1", "position": 1},
    {"situation_id": "contractor_1", "word_id": "enc_contr_2", "position": 2},
    {"situation_id": "contractor_1", "word_id": "enc_contr_3", "position": 3},
    # Groceries
    {"situation_id": "groceries_1", "word_id": "enc_groc_1", "position": 1},
    {"situation_id": "groceries_1", "word_id": "enc_groc_2", "position": 2},
    {"situation_id": "groceries_1", "word_id": "enc_groc_3", "position": 3},
    # Mechanic
    {"situation_id": "mechanic_1", "word_id": "enc_mech_1", "position": 1},
    {"situation_id": "mechanic_1", "word_id": "enc_mech_2", "position": 2},
    {"situation_id": "mechanic_1", "word_id": "enc_mech_3", "position": 3},
    # Police
    {"situation_id": "police_1", "word_id": "enc_police_1", "position": 1},
    {"situation_id": "police_1", "word_id": "enc_police_2", "position": 2},
    {"situation_id": "police_1", "word_id": "enc_police_3", "position": 3},
]
