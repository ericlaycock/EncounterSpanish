"""Role definitions for AI conversation agents.

Each situation has an ai_role, user_role, and situation_description used to
build the system prompt for voice chat phases 2 & 3.

Grammar situations map to one of the 10 main scenes via GRAMMAR_SCENE_MAP,
and have additional grammar_structure + example prompts.
"""

# ── Main situation roles (keyed by animation_type) ───────────────────────────

SITUATION_ROLES = {
    "airport": {
        "ai_role": "airline check-in agent",
        "user_role": "traveler at the airport",
        "situation_description": "the traveler is checking in for their flight. You are helping them at the airline counter.",
    },
    "banking": {
        "ai_role": "bank teller",
        "user_role": "customer at the bank",
        "situation_description": "the customer needs help with their bank account. You are assisting them at the counter.",
    },
    "clothing": {
        "ai_role": "shop assistant",
        "user_role": "customer shopping for clothes",
        "situation_description": "the customer is looking for clothes in your store. You are helping them find what they need.",
    },
    "contractor": {
        "ai_role": "contractor",
        "user_role": "homeowner hiring a contractor",
        "situation_description": "the homeowner wants work done on their house. You are discussing the renovation project.",
    },
    "groceries": {
        "ai_role": "supermarket cashier",
        "user_role": "customer at the supermarket",
        "situation_description": "the customer is buying groceries. You are helping them at checkout.",
    },
    "mechanic": {
        "ai_role": "mechanic",
        "user_role": "customer at the garage",
        "situation_description": "the customer's car is not working correctly. You are talking to the customer in your garage.",
    },
    "police": {
        "ai_role": "police officer",
        "user_role": "driver pulled over",
        "situation_description": "you have pulled over the driver for a routine traffic stop. You are speaking to them through the car window.",
    },
    "restaurant": {
        "ai_role": "waiter",
        "user_role": "diner at a restaurant",
        "situation_description": "the diner is ordering food. You are their server for the evening.",
    },
    "small_talk": {
        "ai_role": "neighbor",
        "user_role": "new resident in the neighborhood",
        "situation_description": "you just met your new neighbor. You are making friendly small talk.",
    },
    "internet": {
        "ai_role": "internet technician",
        "user_role": "customer setting up WiFi",
        "situation_description": "the customer needs help setting up their home internet. You are the technician on site.",
    },
}

# ── Grammar situation → main scene mapping ───────────────────────────────────
# Round-robin over 4 scenes matching grammar_a/b/c/d background videos:
#   grammar_a → small_talk,  grammar_b → mechanic,
#   grammar_c → banking,     grammar_d → clothing

GRAMMAR_SCENE_MAP = {
    "grammar_pronouns": "small_talk",
    "grammar_gender": "mechanic",
    "grammar_regular_present": "banking",
    "grammar_irregular_present": "clothing",
    "grammar_irregular_present_ii": "small_talk",
    "grammar_spelling_changes": "mechanic",
    "grammar_present_o_ue": "banking",
    "grammar_present_e_ie": "clothing",
    "grammar_present_e_i": "small_talk",
    "grammar_preterite_regular": "mechanic",
    "grammar_preterite_irregular": "banking",
    "grammar_gerund": "clothing",
    "grammar_gustar_1": "small_talk",
    "grammar_gustar_2": "mechanic",
    "grammar_gustar_3": "banking",
    "grammar_ir_a_inf": "clothing",
}

# ── Grammar structure definitions ────────────────────────────────────────────
# Each grammar situation has a grammar_structure the user must deploy,
# plus bespoke example questions that naturally elicit that structure.

GRAMMAR_STRUCTURES = {
    "grammar_pronouns": {
        "grammar_structure": "subject pronouns (yo, tú, él, ella, usted, nosotros, ellos, ustedes)",
        "examples": [
            "My wife usually does the gardening but I do the cooking. What about you?",
            "Our kids go to the school down the road. Where do yours go?",
            "My husband and I moved here last year. How long have you lived here?",
        ],
    },
    "grammar_gender": {
        "grammar_structure": "gendered articles (el, la, los, las, un, una)",
        "examples": [
            "I need to check the oil. Can you pop the hood?",
            "The transmission is making a noise. When did it start?",
            "I'll need to order a new part for the engine.",
        ],
    },
    "grammar_regular_present": {
        "grammar_structure": "regular present tense conjugation (-ar, -er, -ir verbs like hablar, comer, vivir)",
        "examples": [
            "How often do you come to this branch?",
            "Do you live near here or do you work in the area?",
            "We open at nine. What time do you usually arrive?",
        ],
    },
    "grammar_irregular_present": {
        "grammar_structure": "irregular present tense (ser, estar, ir, tener, venir, dar)",
        "examples": [
            "This dress is lovely. Are you looking for something for a special occasion?",
            "Do you have your receipt? Where did you get this?",
            "We're going to check in the back. Can you come this way?",
        ],
    },
    "grammar_irregular_present_ii": {
        "grammar_structure": "irregular present tense (hacer, poner, salir, decir, oír, traer, caer, valer)",
        "examples": [
            "What do you usually do on weekends around here?",
            "I always put the recycling out on Tuesdays. When do you put yours out?",
            "My dog makes so much noise. Do you hear him from your place?",
        ],
    },
    "grammar_spelling_changes": {
        "grammar_structure": "spelling-change verbs in present tense (conseguir, conocer, construir, etc.)",
        "examples": [
            "We're trying to get a new alternator. Where do you usually get your parts?",
            "Do you know a good body shop nearby?",
            "They're building a new dealership down the road. Did you know that?",
        ],
    },
    "grammar_present_o_ue": {
        "grammar_structure": "stem-changing verbs O→UE (mover, almorzar, morir, poder, dormir)",
        "examples": [
            "We can move your appointment to Thursday. Can you come in the morning?",
            "Where do you usually eat lunch? We have a break room you can use.",
            "The ATM sometimes dies at night. Does that happen at your branch too?",
        ],
    },
    "grammar_present_e_ie": {
        "grammar_structure": "stem-changing verbs E→IE (cerrar, entender, pensar, querer, preferir)",
        "examples": [
            "We close at eight tonight. Do you want to try anything else before then?",
            "Do you prefer the blue or the green? I think the blue suits you.",
            "I don't understand the return policy. Can you explain it?",
        ],
    },
    "grammar_present_e_i": {
        "grammar_structure": "stem-changing verbs E→I (pedir, repetir, seguir, servir)",
        "examples": [
            "Can you repeat your address for me? I didn't catch the street name.",
            "My kids always ask for ice cream when we walk past the shop. Do yours do that?",
            "I follow the local news group online. Do you follow any neighborhood groups?",
        ],
    },
    "grammar_preterite_regular": {
        "grammar_structure": "regular preterite tense (past tense of -ar, -er, -ir verbs)",
        "examples": [
            "When did you first notice the noise? Did it happen suddenly?",
            "Did you drive here today or did someone drop you off?",
            "I checked the brakes last time. Did you notice any improvement?",
        ],
    },
    "grammar_preterite_irregular": {
        "grammar_structure": "irregular preterite (ser/ir→fui, hacer→hice, decir→dije, tener→tuve, etc.)",
        "examples": [
            "What did you do when the check engine light came on?",
            "Did you go to another mechanic before coming here?",
            "I had a similar problem last week. What did the previous mechanic say?",
        ],
    },
    "grammar_gerund": {
        "grammar_structure": "gerund / present progressive (estar + -ando/-iendo)",
        "examples": [
            "What are you looking for today? Are you shopping for a gift?",
            "I'm checking if we have your size. Are you wearing a medium right now?",
            "The tailor is working on alterations. Are you waiting for something?",
        ],
    },
    "grammar_gustar_1": {
        "grammar_structure": "gustar with singular nouns (me gusta, te gusta, le gusta)",
        "examples": [
            "I love this neighborhood. Do you like living here so far?",
            "My daughter likes the park down the street. Does your family like it?",
            "I like cooking Italian food. What kind of food do you like?",
        ],
    },
    "grammar_gustar_2": {
        "grammar_structure": "gustar with plural nouns (me gustan, te gustan, le gustan)",
        "examples": [
            "Do you like the new brake pads? Some customers prefer the ceramic ones.",
            "I like Japanese cars for reliability. What brands do you like?",
            "Do the warning lights bother you? Some people ignore them.",
        ],
    },
    "grammar_gustar_3": {
        "grammar_structure": "gustar with emphasis pronouns (a mí me gusta, a ti te gusta, a él le gusta)",
        "examples": [
            "I personally prefer to save in a fixed-term account. What about you specifically?",
            "My colleague likes the old system, but I prefer the new one. Which do you prefer?",
            "Some customers like online banking. Do you yourself prefer coming in person?",
        ],
    },
    "grammar_ir_a_inf": {
        "grammar_structure": "ir a + infinitive for near future (voy a hablar, vas a comer, etc.)",
        "examples": [
            "Are you going to try this on? We're going to close soon.",
            "I'm going to check the back for your size. Are you going to wait here?",
            "What are you going to wear it for? We're going to get new stock next week.",
        ],
    },
}


def get_roles_for_situation(animation_type: str, situation_id: str = "") -> dict:
    """Get ai_role, user_role, situation_description for any situation.

    For grammar situations (animation_type='grammar'), looks up the scene
    via GRAMMAR_SCENE_MAP and returns roles from the mapped main situation.
    """
    if animation_type == "grammar" and situation_id in GRAMMAR_SCENE_MAP:
        mapped_scene = GRAMMAR_SCENE_MAP[situation_id]
        return SITUATION_ROLES.get(mapped_scene, SITUATION_ROLES["small_talk"])
    return SITUATION_ROLES.get(animation_type, SITUATION_ROLES["small_talk"])


def get_grammar_structure(situation_id: str) -> dict | None:
    """Get grammar_structure and examples for a grammar situation, or None."""
    return GRAMMAR_STRUCTURES.get(situation_id)
