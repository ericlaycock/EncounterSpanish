#!/usr/bin/env python3
"""Generate per-encounter initial messages using GPT-4.1-mini.

One-time script. Output: app/services/encounter_messages_generated.py

Usage: .venv/bin/python scripts/generate_encounter_messages.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
from app.data.seed_bank import _SUB_SITUATIONS
from app.data.grammar_situations import GRAMMAR_SITUATIONS, GRAMMAR_WORD_TRANSLATIONS

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

ROLE_MAP = {
    "airport": "airline check-in agent",
    "banking": "bank teller",
    "clothing": "clothing store clerk",
    "contractor": "the homeowner (the learner is hiring a plumber)",
    "groceries": "supermarket employee",
    "internet": "internet service technician",
    "mechanic": "auto mechanic",
    "police": "police officer",
    "restaurant": "waiter/server",
    "small_talk": "friendly neighbor",
}


def generate_encounter_message(
    title: str,
    goal: str,
    category: str,
    encounter_num: int,
    words: list[tuple[str, str, str]],
) -> str:
    role = ROLE_MAP.get(category, "service worker")
    word_list = ", ".join(f"{w[0]} ({w[1]})" for w in words)

    prompt = f"""You are writing the opening line for an NPC in a Spanish learning app.

Situation: "{title}" — {goal}
You are playing the role of: {role}
The learner's 3 target Spanish words for this encounter are: {word_list}
This is encounter #{encounter_num} of 50 in this situation.

Write a 1-2 sentence opening line IN ENGLISH that:
- Is in-character as the {role}
- Sets up the scenario naturally so the conversation flows toward the target words
- Creates an obvious opportunity for the learner to use at least one target word in their response
- Does NOT contain the Spanish target words — the learner must produce those
- Feels natural and conversational, not robotic or generic
- Is specific enough to guide the conversation (not just "How can I help you?")

Reply with ONLY the opening line, nothing else."""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip().strip('"')


def generate_grammar_message(sid: str, cfg: dict) -> str:
    title = cfg["title"]
    words = cfg["word_workload"]
    word_list = ", ".join(
        f"{w} ({GRAMMAR_WORD_TRANSLATIONS.get(w, w)})" for w in words
    )

    prompt = f"""You are a friendly Spanish tutor starting a grammar practice conversation in a learning app.

Grammar topic: {title}
Target words/structures: {word_list}

Write a 1-2 sentence opener IN ENGLISH that:
- Naturally sets up a scenario where the student will need to use the target grammar structures
- Is warm and encouraging
- Does NOT directly say "conjugate this verb" or "use this pronoun" — instead create a relatable situation
- Is specific to the grammar topic

Reply with ONLY the opening line, nothing else."""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip().strip('"')


def main():
    messages: dict[str, str] = {}
    total = sum(50 for _ in _SUB_SITUATIONS for _ in _SUB_SITUATIONS[_]) + len(GRAMMAR_SITUATIONS)
    done = 0

    # --- Encounter situations (700) ---
    for category, sub_situations in _SUB_SITUATIONS.items():
        for sub in sub_situations:
            prefix = sub["word_prefix"]
            title = sub["title"]
            goal = sub["goal"]
            words = sub["words"]

            for enc in range(50):
                enc_num = enc + 1
                sid = f"{prefix}_{enc_num}"
                idx = enc * 3
                enc_words = words[idx : idx + 3]

                msg = generate_encounter_message(title, goal, category, enc_num, enc_words)
                messages[sid] = msg
                done += 1

                if done % 25 == 0 or done <= 3:
                    print(f"[{done}/{total}] {sid}: {msg[:80]}...")

    # --- Grammar situations (16) ---
    for sid, cfg in GRAMMAR_SITUATIONS.items():
        # Skip grammar_gender — it has no phase 2
        if "2" not in cfg.get("phases", {}) or not cfg["phases"].get("2", False):
            # Still generate a message for completeness
            pass
        msg = generate_grammar_message(sid, cfg)
        messages[sid] = msg
        done += 1
        print(f"[{done}/{total}] {sid}: {msg[:80]}...")

    # --- Write output ---
    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "app",
        "services",
        "encounter_messages_generated.py",
    )

    with open(out_path, "w") as f:
        f.write('"""Auto-generated per-encounter initial messages.\n\n')
        f.write("Generated by scripts/generate_encounter_messages.py using GPT-4.1-mini.\n")
        f.write(f"Total: {len(messages)} messages.\n")
        f.write('"""\n\n')
        f.write("ENCOUNTER_MESSAGES: dict[str, str] = {\n")
        for sid, msg in messages.items():
            escaped = msg.replace("\\", "\\\\").replace('"', '\\"')
            f.write(f'    "{sid}": "{escaped}",\n')
        f.write("}\n")

    print(f"\nDone! Wrote {len(messages)} messages to {out_path}")


if __name__ == "__main__":
    main()
