#!/usr/bin/env python3
"""STT Benchmark: Compare whisper-1 vs gpt-4o-transcribe vs gpt-4o-mini-transcribe.

Budget: ~200 API calls (20 utterances × 3 models × 3 prompts = 180 calls)

Usage: .venv/bin/python scripts/stt_benchmark.py
"""

import os
import io
import csv
import time
import hashlib
from pathlib import Path
from difflib import SequenceMatcher
from openai import OpenAI

AUDIO_DIR = Path("scripts/stt_benchmark_results")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# --- 20 utterances covering all language modes ---
UTTERANCES = [
    # Pure English (3)
    ("Hello, I'd like to order some food please.", "pure_english"),
    ("Can I check in for my flight?", "pure_english"),
    ("I need to speak with someone about my account.", "pure_english"),

    # English + 1 Spanish word (3)
    ("Can I see the menú please?", "en_one_spanish"),
    ("Excuse me, mesero, can I get some water?", "en_one_spanish"),
    ("I'd like to buy a boleto for the next flight.", "en_one_spanish"),

    # English + 2-3 Spanish words (3)
    ("I have my permiso de conducir right here.", "en_multi_spanish"),
    ("Can I get a boleto for vuelo number 234?", "en_multi_spanish"),
    ("The mesero brought the platillo I ordered.", "en_multi_spanish"),

    # English + Spanish phrase (3)
    ("I want to try the especialidad del día.", "en_spanish_phrase"),
    ("Where is the sala de espera?", "en_spanish_phrase"),
    ("I'm waiting at the puerta de embarque.", "en_spanish_phrase"),

    # Mostly Spanish (3)
    ("Sí, quiero el menú por favor.", "mostly_spanish"),
    ("Necesito un boleto para el vuelo.", "mostly_spanish"),
    ("¿Dónde está el mostrador de facturación?", "mostly_spanish"),

    # Short (2)
    ("Boleto, please.", "short"),
    ("Permiso de conducir.", "short"),

    # Natural code-switching (3)
    ("So I was at the banco and the lady asked for my permiso.", "code_switch"),
    ("I showed them my pasaporte and my permiso de conducir at the mostrador.", "code_switch"),
    ("I asked the mesero for the menú and ordered the sopa.", "code_switch"),
]

# --- Prompts (3 to test) ---
VOCAB = "menú, mesero, camarero, platillo, boleto, vuelo, pasaporte, mostrador, permiso de conducir, banco, depósito, saldo, cuenta, equipaje, sopa, especialidad del día, sala de espera, cambio de aceite, puerta de embarque, carro"

PROMPTS = {
    "P0_none": None,
    "P1_verbatim": (
        f"The user is speaking ENGLISH with a few Spanish words mixed in. "
        f"Transcribe exactly what they say — mostly English sentences with occasional Spanish vocabulary. "
        f"Do NOT translate English into Spanish. "
        f"Spanish words they might use: {VOCAB}."
    ),
    "P2_whisper_style": (
        f"This is a conversation about a real-world scenario. "
        f"The user is learning Spanish and may use these Spanish words: {VOCAB}. "
        f"The conversation is in Spanish and English."
    ),
}

MODELS = ["whisper-1", "gpt-4o-transcribe", "gpt-4o-mini-transcribe"]


def generate_audio(text: str, idx: int) -> Path:
    """Generate audio via TTS. Cached by content hash."""
    h = hashlib.md5(text.encode()).hexdigest()[:8]
    fp = AUDIO_DIR / f"utt_{idx:03d}_{h}.mp3"
    if fp.exists():
        return fp
    resp = client.audio.speech.create(model="gpt-4o-mini-tts", voice="nova", input=text)
    with open(fp, "wb") as f:
        for chunk in resp.iter_bytes():
            f.write(chunk)
    return fp


def transcribe(path: Path, model: str, prompt: str | None) -> tuple[str, int]:
    """Transcribe audio. Returns (transcript, latency_ms)."""
    with open(path, "rb") as f:
        data = f.read()
    af = io.BytesIO(data)
    af.name = path.name
    params = {"model": model, "file": af}
    if prompt is not None:
        params["prompt"] = prompt
    t0 = time.time()
    resp = client.audio.transcriptions.create(**params)
    return resp.text, int((time.time() - t0) * 1000)


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower().strip(" .!?"), b.lower().strip(" .!?")).ratio()


def spanish_hit_rate(gt: str, tr: str, vocab: set) -> tuple[int, int]:
    gl, tl = gt.lower(), tr.lower()
    present = [w for w in vocab if w.lower() in gl]
    found = [w for w in present if w.lower() in tl]
    return len(found), len(present)


def main():
    vocab_set = {w.strip() for w in VOCAB.split(",")}

    # Generate audio
    print(f"Generating {len(UTTERANCES)} audio files...")
    files = []
    for i, (text, cat) in enumerate(UTTERANCES):
        fp = generate_audio(text, i)
        files.append((fp, text, cat))
    print(f"Done. Files in {AUDIO_DIR}\n")

    # Run benchmark
    results = []
    total = len(MODELS) * len(PROMPTS) * len(files)
    call_num = 0

    for model in MODELS:
        for pname, ptext in PROMPTS.items():
            print(f"--- {model} | {pname} ---")
            combo = []
            for fp, gt, cat in files:
                call_num += 1
                try:
                    tr, ms = transcribe(fp, model, ptext)
                    acc = similarity(gt, tr)
                    sf, st = spanish_hit_rate(gt, tr, vocab_set)
                    r = dict(model=model, prompt=pname, category=cat,
                             ground_truth=gt, transcript=tr,
                             accuracy=round(acc, 3), sp_found=sf, sp_total=st, latency_ms=ms)
                    results.append(r)
                    combo.append(r)
                    # Print mismatches
                    if acc < 0.85:
                        print(f"  [{ms}ms] acc={acc:.2f}")
                        print(f"    GT: {gt}")
                        print(f"    TR: {tr}")
                except Exception as e:
                    print(f"  ERROR on {fp.name}: {e}")
                    results.append(dict(model=model, prompt=pname, category=cat,
                                        ground_truth=gt, transcript=f"ERROR: {e}",
                                        accuracy=0, sp_found=0, sp_total=0, latency_ms=0))

            if combo:
                avg_acc = sum(r["accuracy"] for r in combo) / len(combo)
                avg_ms = sum(r["latency_ms"] for r in combo) / len(combo)
                sf = sum(r["sp_found"] for r in combo)
                st = sum(r["sp_total"] for r in combo)
                print(f"  => acc={avg_acc:.3f}  lat={avg_ms:.0f}ms  spanish={sf}/{st} ({sf/st:.0%})\n")

    # Save CSV
    csv_path = AUDIO_DIR / "results.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=results[0].keys())
        w.writeheader()
        w.writerows(results)
    print(f"Results saved to {csv_path}")

    # Summary
    print("\n" + "=" * 100)
    print(f"{'Model':<28} {'Prompt':<16} {'Accuracy':>8} {'Latency':>8} {'Spanish':>10}")
    print("-" * 100)

    combos = {}
    for r in results:
        k = (r["model"], r["prompt"])
        combos.setdefault(k, []).append(r)

    rows = []
    for (m, p), rs in combos.items():
        a = sum(r["accuracy"] for r in rs) / len(rs)
        l = sum(r["latency_ms"] for r in rs) / len(rs)
        sf = sum(r["sp_found"] for r in rs)
        st = sum(r["sp_total"] for r in rs)
        rows.append((m, p, a, l, sf, st))

    rows.sort(key=lambda x: (-x[2], x[3]))
    for m, p, a, l, sf, st in rows:
        print(f"{m:<28} {p:<16} {a:>8.3f} {l:>7.0f}ms {sf}/{st} ({sf/st:.0%})")

    print(f"\nTotal API calls: {call_num}")


if __name__ == "__main__":
    main()
