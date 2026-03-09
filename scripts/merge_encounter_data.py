#!/usr/bin/env python3
"""Merge generated encounter data into seed_bank.py.

Reads generated_encounter_data.json and rewrites app/data/seed_bank.py
with the expanded situations, encounter words, and situation-word links.

Usage: python scripts/merge_encounter_data.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

INPUT_PATH = os.path.join(os.path.dirname(__file__), "generated_encounter_data.json")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data", "seed_bank.py")


def main():
    with open(INPUT_PATH) as f:
        data = json.load(f)

    gen_words = data["encounter_words"]  # dict: category -> list of word dicts
    gen_situations = data["situations"]  # list of situation dicts
    gen_sit_words = data["situation_words"]  # list of link dicts

    # Import existing seed_bank to preserve encounter #1 data
    from app.data.seed_bank import ENCOUNTER_WORDS, SITUATIONS, SITUATION_WORDS, CATEGORY_NAMES

    # --- Merge encounter words ---
    merged_words = {}
    for cat, words in ENCOUNTER_WORDS.items():
        merged_words[cat] = list(words)  # copy existing

    for cat, words in gen_words.items():
        if cat not in merged_words:
            merged_words[cat] = []
        existing_ids = {w["id"] for w in merged_words[cat]}
        for w in words:
            if w["id"] not in existing_ids:
                merged_words[cat].append(w)

    # --- Merge situations ---
    existing_sit_ids = {s["id"] for s in SITUATIONS}
    merged_situations = list(SITUATIONS)  # keep originals

    for s in gen_situations:
        if s["id"] not in existing_sit_ids:
            merged_situations.append(s)

    # Sort by category then series_number
    merged_situations.sort(key=lambda s: (s["category"], s["series_number"]))

    # Add goal to existing situations that don't have one
    goals = {}
    for s in gen_situations:
        if "goal" in s:
            goals[s["title"]] = s["goal"]

    for s in merged_situations:
        if "goal" not in s and s["title"] in goals:
            s["goal"] = goals[s["title"]]

    # --- Merge situation-word links ---
    existing_links = {(sw["situation_id"], sw["word_id"]) for sw in SITUATION_WORDS}
    merged_sit_words = list(SITUATION_WORDS)

    for sw in gen_sit_words:
        key = (sw["situation_id"], sw["word_id"])
        if key not in existing_links:
            merged_sit_words.append(sw)

    # Sort by situation_id then position
    merged_sit_words.sort(key=lambda sw: (sw["situation_id"], sw["position"]))

    # --- Write output ---
    lines = []
    lines.append('"""Central seed bank — single source of truth for all word and situation data.')
    lines.append("")
    lines.append("All encounter words, high-frequency words, situations, and their links")
    lines.append("are defined here. Grammar situations are in grammar_situations.py.")
    lines.append("The seed script (scripts/seed_qa.py) reads from this module.")
    lines.append('"""')
    lines.append("")
    lines.append("from app.data.hf_words import HIGH_FREQUENCY_WORDS  # noqa: F401 — re-exported")
    lines.append("")
    lines.append("# --- Category display names (used by API and onboarding) ---")
    lines.append("")
    lines.append("CATEGORY_NAMES = {")
    for k, v in CATEGORY_NAMES.items():
        lines.append(f'    "{k}": "{v}",')
    lines.append("}")
    lines.append("")
    lines.append("# HIGH_FREQUENCY_WORDS is imported from app.data.hf_words (1000 entries)")
    lines.append("")
    lines.append("# --- Encounter words by category ---")
    lines.append("")
    lines.append("ENCOUNTER_WORDS = {")

    for cat in sorted(merged_words.keys()):
        words = merged_words[cat]
        lines.append(f'    "{cat}": [')
        for w in words:
            spanish = w["spanish"].replace('"', '\\"')
            english = w["english"].replace('"', '\\"')
            notes = w.get("notes", "")
            if notes:
                notes_str = f', "notes": "{notes}"'
            else:
                notes_str = ""
            lines.append(f'        {{"id": "{w["id"]}", "spanish": "{spanish}", "english": "{english}"{notes_str}}},')
        lines.append("    ],")

    lines.append("}")
    lines.append("")
    lines.append("# --- Situations (main encounters) ---")
    lines.append("")
    lines.append("SITUATIONS = [")
    for s in merged_situations:
        goal_str = ""
        if "goal" in s:
            goal_str = f', "goal": "{s["goal"]}"'
        free_str = "True" if s.get("is_free") else "False"
        lines.append(
            f'    {{"id": "{s["id"]}", "title": "{s["title"]}", "category": "{s["category"]}", '
            f'"series_number": {s["series_number"]}, "order_index": {s["order_index"]}, '
            f'"is_free": {free_str}{goal_str}}},'
        )
    lines.append("]")
    lines.append("")
    lines.append("# --- SituationWord links (encounter words per situation) ---")
    lines.append("")
    lines.append("SITUATION_WORDS = [")
    current_sit = None
    for sw in merged_sit_words:
        if sw["situation_id"] != current_sit:
            if current_sit is not None:
                lines.append("")  # blank line between situations
            current_sit = sw["situation_id"]
        lines.append(f'    {{"situation_id": "{sw["situation_id"]}", "word_id": "{sw["word_id"]}", "position": {sw["position"]}}},')
    lines.append("]")
    lines.append("")

    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join(lines))

    print(f"Written to {OUTPUT_PATH}")
    print(f"  Categories: {len(merged_words)}")
    print(f"  Total encounter words: {sum(len(w) for w in merged_words.values())}")
    print(f"  Situations: {len(merged_situations)}")
    print(f"  Situation-word links: {len(merged_sit_words)}")


if __name__ == "__main__":
    main()
