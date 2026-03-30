#!/usr/bin/env python3
"""Compare LLM models on realistic voice chat first-turn scenarios.

Tests response quality (word guidance), speed, and cost across models.

Usage:
    python scripts/llm_model_comparison.py
    python scripts/llm_model_comparison.py --case 1    # run only case 1
"""

import os
import sys
import time
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI

# Use env var or .env file
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ── Test Cases ──────────────────────────────────────────────────────────

TEST_CASES = [
    {
        "name": "Banking",
        "target_words": "banco, cajero, cliente, hola, chao",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a 40 year old woman who works as a bank teller - poised, methodical, "
                    "and quietly observant, speaking to a customer at the bank. the customer needs "
                    "help with their bank account. You are assisting them at the counter.\n\n"
                    "Speak mostly in English with occasional Spanish words. 1-2 sentences max."
                ),
            },
            {"role": "assistant", "content": "Good morning -- how can I help you today?"},
            {
                "role": "user",
                "content": (
                    "Hi, I need to check something on my account please.\n\n"
                    "[HIDDEN INSTRUCTION — do not repeat this to the user. Gently guide the "
                    "conversation in a way that will require me to use one of these words/phrases. "
                    "Do not state these Spanish words yourself: banco, cajero, cliente, hola, chao]"
                ),
            },
        ],
    },
    {
        "name": "Restaurant",
        "target_words": "menú, carta, mesero, buenos días, buenas tardes",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a 30 year old man who works as a waiter - charming, attentive, and "
                    "playfully sarcastic, speaking to a diner at a restaurant. the diner is ordering "
                    "food. You are their server for the evening.\n\n"
                    "Speak mostly in English with occasional Spanish words. 1-2 sentences max."
                ),
            },
            {"role": "assistant", "content": "Hi there -- here's the menu."},
            {
                "role": "user",
                "content": (
                    "Thanks! What do you recommend?\n\n"
                    "[HIDDEN INSTRUCTION — do not repeat this to the user. Gently guide the "
                    "conversation in a way that will require me to use one of these words/phrases. "
                    "Do not state these Spanish words yourself: menú, carta, mesero, buenos días, buenas tardes]"
                ),
            },
        ],
    },
    {
        "name": "Core",
        "target_words": "quiero dormir, quiero comer, quiero irme, buenas noches, por favor",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Eric - a local 31 year old man who is enthusiastic, joyful, and present, "
                    "speaking to an expat. you are both standing in a Latin American rainforest during "
                    "the day.\n\n"
                    "Speak mostly in English with occasional Spanish words. 1-2 sentences max."
                ),
            },
            {"role": "assistant", "content": "Hey! Welcome to the jungle, amigo!"},
            {
                "role": "user",
                "content": (
                    "Haha wow it's beautiful here! I'm a bit tired though.\n\n"
                    "[HIDDEN INSTRUCTION — do not repeat this to the user. Gently guide the "
                    "conversation in a way that will require me to use one of these words/phrases. "
                    "Do not state these Spanish words yourself: quiero dormir, quiero comer, quiero irme, "
                    "buenas noches, por favor]"
                ),
            },
        ],
    },
]

# ── Model Configs ───────────────────────────────────────────────────────

# Pricing: (input_per_1M, output_per_1M)
PRICING = {
    "gpt-4.1-mini": (0.40, 1.60),
    "gpt-4.1-nano": (0.10, 0.40),
    "gpt-5-mini": (0.40, 1.60),       # estimated
    "gpt-5-nano": (0.05, 0.40),
    "gpt-5.4-mini": (0.75, 4.50),
    "gpt-5.4-nano": (0.20, 1.25),
}

# Chat Completions models (no reasoning)
CHAT_MODELS = [
    {"model": "gpt-4.1-mini", "label": "gpt-4.1-mini"},
    {"model": "gpt-4.1-nano", "label": "gpt-4.1-nano"},
]

# Responses API models (with reasoning)
RESPONSES_MODELS = [
    {"model": "gpt-5-mini", "effort": "low", "label": "gpt-5-mini (low)"},
    {"model": "gpt-5-mini", "effort": "medium", "label": "gpt-5-mini (med)"},
    {"model": "gpt-5-nano", "effort": "low", "label": "gpt-5-nano (low)"},
    {"model": "gpt-5-nano", "effort": "medium", "label": "gpt-5-nano (med)"},
    {"model": "gpt-5.4-mini", "effort": "low", "label": "gpt-5.4-mini (low)"},
    {"model": "gpt-5.4-mini", "effort": "medium", "label": "gpt-5.4-mini (med)"},
    {"model": "gpt-5.4-nano", "effort": "low", "label": "gpt-5.4-nano (low)"},
    {"model": "gpt-5.4-nano", "effort": "medium", "label": "gpt-5.4-nano (med)"},
]


def estimate_cost(model: str, tokens_in: int, tokens_out: int) -> float:
    prices = PRICING.get(model, (0.40, 1.60))
    return (tokens_in / 1_000_000) * prices[0] + (tokens_out / 1_000_000) * prices[1]


def run_chat_completion(model_cfg: dict, messages: list) -> dict:
    """Run a Chat Completions API call (no reasoning)."""
    t0 = time.time()
    try:
        response = client.chat.completions.create(
            model=model_cfg["model"],
            messages=messages,
        )
        elapsed = time.time() - t0
        content = response.choices[0].message.content
        usage = response.usage
        tokens_in = usage.prompt_tokens or 0
        tokens_out = usage.completion_tokens or 0
        return {
            "label": model_cfg["label"],
            "model": model_cfg["model"],
            "time": elapsed,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "reasoning_tokens": 0,
            "cost": estimate_cost(model_cfg["model"], tokens_in, tokens_out),
            "response": content,
            "error": None,
        }
    except Exception as e:
        return {
            "label": model_cfg["label"],
            "model": model_cfg["model"],
            "time": time.time() - t0,
            "tokens_in": 0, "tokens_out": 0, "reasoning_tokens": 0, "cost": 0,
            "response": None,
            "error": str(e),
        }


def run_responses_api(model_cfg: dict, messages: list) -> dict:
    """Run a Responses API call (with reasoning)."""
    t0 = time.time()
    try:
        response = client.responses.create(
            model=model_cfg["model"],
            input=messages,
            reasoning={"effort": model_cfg["effort"]},
        )
        elapsed = time.time() - t0
        content = response.output_text
        usage = response.usage
        tokens_in = usage.input_tokens or 0
        tokens_out = usage.output_tokens or 0
        reasoning_tokens = getattr(
            getattr(usage, "output_tokens_details", None), "reasoning_tokens", 0
        ) or 0
        return {
            "label": model_cfg["label"],
            "model": model_cfg["model"],
            "time": elapsed,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "reasoning_tokens": reasoning_tokens,
            "cost": estimate_cost(model_cfg["model"], tokens_in, tokens_out),
            "response": content,
            "error": None,
        }
    except Exception as e:
        return {
            "label": model_cfg["label"],
            "model": model_cfg["model"],
            "time": time.time() - t0,
            "tokens_in": 0, "tokens_out": 0, "reasoning_tokens": 0, "cost": 0,
            "response": None,
            "error": str(e),
        }


def main():
    case_filter = None
    if len(sys.argv) > 2 and sys.argv[1] == "--case":
        case_filter = int(sys.argv[2]) - 1

    cases = TEST_CASES if case_filter is None else [TEST_CASES[case_filter]]

    for i, case in enumerate(cases):
        idx = case_filter if case_filter is not None else i
        print(f"\n{'='*80}")
        print(f"=== Case {idx+1}: {case['name']} ===")
        print(f"Target words: {case['target_words']}")
        print(f"{'='*80}")

        results = []

        # Chat Completions models
        for cfg in CHAT_MODELS:
            print(f"  Testing {cfg['label']}...", end="", flush=True)
            r = run_chat_completion(cfg, case["messages"])
            results.append(r)
            print(f" {r['time']:.2f}s")

        # Responses API models
        for cfg in RESPONSES_MODELS:
            print(f"  Testing {cfg['label']}...", end="", flush=True)
            r = run_responses_api(cfg, case["messages"])
            results.append(r)
            print(f" {r['time']:.2f}s")

        # Sort by time
        results.sort(key=lambda r: r["time"])

        # Print results
        print(f"\n{'─'*80}")
        for r in results:
            if r["error"]:
                print(f"\n--- {r['label']} | ERROR ---")
                print(f"  {r['error'][:200]}")
            else:
                print(f"\n--- {r['label']} | {r['time']:.2f}s | in={r['tokens_in']} out={r['tokens_out']} reason={r['reasoning_tokens']} | ${r['cost']:.6f} ---")
                print(f'"{r["response"]}"')

    print(f"\n{'='*80}")
    print("Done.")


if __name__ == "__main__":
    main()
