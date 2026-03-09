#!/usr/bin/env python3
"""Generate 50 encounter word sets (3 words each) for each of the 14 situations.

Uses GPT-4.1-mini to generate contextually relevant Spanish vocabulary.
Cross-references against HF word list to avoid overlap.
Outputs updated seed_bank.py data structures.

Usage: python scripts/generate_encounter_words.py
"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
from app.data.hf_words import HIGH_FREQUENCY_WORDS
from app.data.seed_bank import SITUATIONS, ENCOUNTER_WORDS, CATEGORY_NAMES

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY") or __import__("app.config", fromlist=["settings"]).settings.openai_api_key)

# Build set of all HF spanish words for dedup
HF_SPANISH = {w["spanish"].lower() for w in HIGH_FREQUENCY_WORDS}

# Map situation titles by their category + series_number
SITUATION_MAP = {}
for s in SITUATIONS:
    key = f"{s['category']}_{s['series_number']}"
    SITUATION_MAP[key] = s

# Existing encounter words to keep as encounter #1
EXISTING_ENC_WORDS = {}
for cat, words in ENCOUNTER_WORDS.items():
    EXISTING_ENC_WORDS[cat] = [w["spanish"].lower() for w in words]


def generate_words_for_situation(situation_title: str, category: str, existing_words: list[str], batch_start: int, batch_size: int) -> list[dict]:
    """Generate encounter word sets for a batch of encounters."""

    existing_str = ", ".join(existing_words) if existing_words else "none yet"

    prompt = f"""You are generating Spanish vocabulary for a language learning app.

Situation: "{situation_title}" (category: {CATEGORY_NAMES.get(category, category)})

Generate exactly {batch_size * 3} unique Spanish words/short phrases relevant to this situation.
These will be split into {batch_size} groups of 3 for encounters {batch_start+1} through {batch_start+batch_size}.

Requirements:
- All {batch_size * 3} words must be UNIQUE
- Words must be relevant to this specific situation (things you'd actually say/hear in this scenario)
- Include a mix of nouns, verbs, adjectives, and common phrases
- Use Latin American Spanish (not Spain-specific)
- Words should range from beginner to intermediate difficulty
- Short phrases (2-3 words) are OK, e.g. "con tarjeta" (with card), "a la derecha" (to the right)
- Do NOT use any of these words (already used): {existing_str}

Return a JSON object with key "words" containing an array of exactly {batch_size * 3} objects.
Each object has "spanish" and "english" fields.

Example: {{"words": [{{"spanish": "efectivo", "english": "cash"}}, {{"spanish": "firmar", "english": "to sign"}}, ...]}}"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=4000,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    parsed = json.loads(content)

    # Extract the flat word list
    if isinstance(parsed, dict):
        for key in ["words", "data", "results", "vocabulary"]:
            if key in parsed and isinstance(parsed[key], list):
                flat_words = parsed[key]
                break
        else:
            for v in parsed.values():
                if isinstance(v, list):
                    flat_words = v
                    break
            else:
                flat_words = []
    else:
        flat_words = parsed if isinstance(parsed, list) else []

    # Group flat words into sets of 3
    result = []
    for i in range(0, len(flat_words), 3):
        chunk = flat_words[i:i+3]
        if len(chunk) == 3:
            result.append({"words": chunk})

    return result


def generate_all():
    """Generate encounter words for all 14 situations, 50 encounters each."""

    all_encounter_words = {}  # category -> list of word dicts
    all_situations = []       # list of situation dicts
    all_situation_words = []  # list of link dicts

    # Collect all existing encounter spanish words globally for dedup
    global_used_words = set(HF_SPANISH)
    for cat_words in EXISTING_ENC_WORDS.values():
        global_used_words.update(cat_words)

    for situation in SITUATIONS:
        cat = situation["category"]
        title = situation["title"]
        sit_id_base = f"{cat}"
        series = situation["series_number"]

        # ID prefix for encounter words
        cat_prefix = {
            "banking": "bank", "restaurant": "rest", "airport": "air",
            "groceries": "groc", "mechanic": "mech", "clothing": "cloth",
            "internet": "int", "small_talk": "talk", "contractor": "contr",
            "police": "police",
        }[cat]

        print(f"\n{'='*60}")
        print(f"Generating for: {title} ({cat}_{series})")
        print(f"{'='*60}")

        # Track words used within this situation to avoid dups
        situation_used_words = set(global_used_words)

        # Encounter #1 uses existing hardcoded words (keep them)
        if cat in ENCOUNTER_WORDS:
            # For situations with series > 1 (e.g. banking_2, banking_3),
            # the existing words may be shared. Assign first 3 per series.
            existing_cat_words = ENCOUNTER_WORDS[cat]
            start_idx = (series - 1) * 3
            enc1_words = existing_cat_words[start_idx:start_idx + 3]

            if len(enc1_words) == 3:
                # Keep existing encounter #1
                for w in enc1_words:
                    situation_used_words.add(w["spanish"].lower())

                if cat not in all_encounter_words:
                    all_encounter_words[cat] = []
                # Don't re-add existing words, they're already in seed_bank

                # But we do need the situation entry for encounter 1
                enc1_sit_id = f"{cat}_{((series - 1) * 50) + 1}"
                all_situations.append({
                    "id": enc1_sit_id,
                    "title": title,
                    "category": cat,
                    "series_number": ((series - 1) * 50) + 1,
                    "order_index": ((series - 1) * 50) + 1,
                    "is_free": situation["is_free"],
                    "goal": get_goal(title, cat),
                })

                for pos, w in enumerate(enc1_words, 1):
                    all_situation_words.append({
                        "situation_id": enc1_sit_id,
                        "word_id": w["id"],
                        "position": pos,
                    })
            else:
                enc1_words = []
        else:
            enc1_words = []

        # Generate encounters 2-50 in batches of 10
        encounters_to_generate = 49  # encounters 2-50
        batch_size = 10
        generated_count = 0

        word_counter = len(ENCOUNTER_WORDS.get(cat, [])) + 1  # start after existing
        # Adjust for multi-series categories
        word_counter = (series - 1) * 150 + len(enc1_words) + 1

        while generated_count < encounters_to_generate:
            current_batch = min(batch_size, encounters_to_generate - generated_count)

            try:
                batch = generate_words_for_situation(
                    title, cat,
                    list(situation_used_words),
                    generated_count + 1,  # offset (enc #2 = offset 1)
                    current_batch,
                )

                for i, encounter_set in enumerate(batch):
                    enc_num = generated_count + i + 2  # encounter 2, 3, 4, ...
                    global_enc_num = ((series - 1) * 50) + enc_num
                    enc_sit_id = f"{cat}_{global_enc_num}"

                    words = encounter_set.get("words", encounter_set) if isinstance(encounter_set, dict) else encounter_set
                    if not isinstance(words, list):
                        print(f"  WARNING: Unexpected format for encounter {enc_num}, skipping")
                        continue

                    # Create situation entry
                    all_situations.append({
                        "id": enc_sit_id,
                        "title": title,
                        "category": cat,
                        "series_number": global_enc_num,
                        "order_index": global_enc_num,
                        "is_free": enc_num <= 5,  # First 5 encounters free
                        "goal": get_goal(title, cat),
                    })

                    # Create word entries and links
                    if cat not in all_encounter_words:
                        all_encounter_words[cat] = []

                    for pos, word_data in enumerate(words[:3], 1):
                        spanish = word_data["spanish"]
                        english = word_data["english"]

                        # Skip if duplicate
                        if spanish.lower() in situation_used_words:
                            print(f"  DEDUP: Skipping '{spanish}' (already used)")
                            continue

                        situation_used_words.add(spanish.lower())
                        global_used_words.add(spanish.lower())

                        word_id = f"enc_{cat_prefix}_{word_counter:03d}"
                        word_counter += 1

                        all_encounter_words[cat].append({
                            "id": word_id,
                            "spanish": spanish,
                            "english": english,
                        })

                        all_situation_words.append({
                            "situation_id": enc_sit_id,
                            "word_id": word_id,
                            "position": pos,
                        })

                generated_count += len(batch)
                print(f"  Generated encounters {generated_count + 1}/{encounters_to_generate + 1} for {title}")

            except Exception as e:
                print(f"  ERROR generating batch: {e}")
                print(f"  Retrying in 5 seconds...")
                time.sleep(5)
                continue

            # Rate limit
            time.sleep(1)

    return all_encounter_words, all_situations, all_situation_words


def get_goal(title: str, category: str) -> str:
    """Return a pedagogical goal for each situation."""
    goals = {
        "Opening a Bank Account": "Open a bank account by providing your information to the teller",
        "Wire Transfer": "Complete a wire transfer by giving the teller the recipient details",
        "Currency Exchange": "Exchange your currency by negotiating with the teller",
        "Ordering Food": "Order a meal by communicating with the waiter",
        "Making a Reservation": "Make a restaurant reservation by calling or speaking with the host",
        "Asking for the Bill": "Ask for the bill, review the charges, and pay",
        "Checking In": "Complete the airport check-in process with the airline agent",
        "Finding the Right Size": "Find the right clothing size with help from the store clerk",
        "Setting Up WiFi": "Set up your internet service by speaking with the technician",
        "Meeting a Neighbor": "Have a friendly conversation with your new neighbor",
        "Hiring a Plumber": "Hire a plumber by describing the problem and agreeing on a price",
        "At the Supermarket": "Buy groceries by finding items and checking out",
        "Oil Change": "Get your car serviced by explaining what you need to the mechanic",
        "Traffic Stop": "Handle a traffic stop by responding to the officer's questions",
    }
    return goals.get(title, f"Complete the {CATEGORY_NAMES.get(category, category).lower()} scenario")


def write_output(enc_words, situations, sit_words):
    """Write generated data to a JSON file for review before merging into seed_bank."""
    output = {
        "encounter_words": enc_words,
        "situations": situations,
        "situation_words": sit_words,
    }

    output_path = os.path.join(os.path.dirname(__file__), "generated_encounter_data.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Output written to: {output_path}")
    print(f"Situations: {len(situations)}")
    total_words = sum(len(w) for w in enc_words.values())
    print(f"Encounter words: {total_words}")
    print(f"Situation-word links: {len(sit_words)}")
    print(f"{'='*60}")
    print(f"\nReview the JSON file, then run scripts/merge_encounter_data.py to update seed_bank.py")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

    enc_words, situations, sit_words = generate_all()
    write_output(enc_words, situations, sit_words)
