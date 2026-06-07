"""Calibrate the stylometric distance threshold against a 30-example labeled set.

Procedure:
  1. Build 15 real-Sean samples by chunking voice-samples.md.
  2. Generate 15 generic-AI samples by calling Opus 4.7 against varied AI/PM prompts.
  3. Compute compute_distance() for each sample.
  4. Find the threshold that maximizes TPR-FPR (Youden's J / ROC-optimal).
  5. Write threshold back into stylometry_baseline.json.
  6. Persist the labeled set to calibration_set.jsonl.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "agents-sdk"))

from lib.skill_optimizer.stylometry import (
    extract_features,
    compute_distance,
    extract_voice_corpus_chunks,
    load_baseline,
    save_baseline,
)
# The Anthropic SDK is imported LAZILY (only inside the generation path) so the
# default --reuse-existing flow recomputes the threshold from already-captured
# texts with ZERO API calls and ZERO key requirement (cost-safety, 2026-06-06).

VOICE_SAMPLES = REPO / ".claude/skills/writing-voice-modes/references/voice-samples.md"
BASELINE_PATH = REPO / "agents-sdk/data/skill-optimizer/stylometry_baseline.json"
CALIBRATION_OUT = REPO / "agents-sdk/data/skill-optimizer/calibration_set.jsonl"

GENERIC_AI_PROMPTS = [
    "Write a 200-word blog post intro about why product managers should learn Python.",
    "Write a 200-word blog post intro about the rise of AI-native startups in 2026.",
    "Write a 200-word blog post intro about choosing between Claude and GPT for product work.",
    "Write a 200-word blog post intro about the future of crypto product management.",
    "Write a 200-word blog post intro about why every PM needs to understand LLMs.",
    "Write a 200-word blog post intro about hiring the first AI engineer at a startup.",
    "Write a 200-word blog post intro about prompt engineering for product managers.",
    "Write a 200-word blog post intro about measuring AI feature success with users.",
    "Write a 200-word blog post intro about onboarding a new AI tool to your team.",
    "Write a 200-word blog post intro about the trade-offs of fine-tuning vs prompting.",
    "Write a 200-word blog post intro about model context protocols changing PM work.",
    "Write a 200-word blog post intro about the hidden costs of AI infrastructure.",
    "Write a 200-word blog post intro about agentic workflows in modern SaaS products.",
    "Write a 200-word blog post intro about the difference between AI features and AI products.",
    "Write a 200-word blog post intro about how AI is reshaping the PM role at large companies.",
]


def _extract_real_sean_chunks() -> list[str]:
    """Pull ~15 ~100-word real-Sean chunks from voice-samples.md.

    Delegates to the shared blockquote-isolating extractor so the calibration
    "real Sean" samples are drawn from the SAME corpus the baseline features were
    built on (rebuild_stylometry_baseline.py). The old naive paragraph split swept
    in the document's analytical commentary; that contamination is fixed centrally.
    """
    chunks = extract_voice_corpus_chunks(VOICE_SAMPLES.read_text())
    return chunks[:15]


def _call_with_retries(client, prompt: str, max_attempts: int = 3) -> str:
    """Call the API with up to 3 retries on 429/5xx with 5s backoff."""
    from anthropic import APIStatusError, APIConnectionError, RateLimitError

    last_err = None
    for attempt in range(1, max_attempts + 1):
        try:
            msg = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}],
            )
            return msg.content[0].text
        except (RateLimitError, APIConnectionError) as e:
            last_err = e
            print(f"  attempt {attempt}/{max_attempts} failed ({type(e).__name__}); retrying in 5s...")
            time.sleep(5)
        except APIStatusError as e:
            # Retry only on 5xx
            status = getattr(e, "status_code", None)
            if status and 500 <= status < 600:
                last_err = e
                print(f"  attempt {attempt}/{max_attempts} failed ({status}); retrying in 5s...")
                time.sleep(5)
            else:
                raise
    raise RuntimeError(f"API call failed after {max_attempts} attempts: {last_err}")


def _generate_ai_samples(prompts: list[str]) -> list[str]:
    from anthropic import Anthropic

    client = Anthropic()
    samples = []
    for i, p in enumerate(prompts, 1):
        print(f"  [{i}/{len(prompts)}] generating...")
        samples.append(_call_with_retries(client, p))
    return samples


def _roc_auc(distances: list[tuple[float, int]]) -> tuple[float, float]:
    """Find threshold maximizing TPR-FPR. Returns (best_threshold, best_score).

    Convention: label=1 (real Sean) has LOW distance; label=0 (AI) has HIGH distance.
    A sample is predicted as Sean (positive) iff distance <= threshold.
    """
    distances_sorted = sorted(distances)
    best_t, best_score = 0.0, -1.0
    pos_total = sum(1 for _, label in distances if label == 1)
    neg_total = sum(1 for _, label in distances if label == 0)
    for i in range(len(distances_sorted)):
        t = distances_sorted[i][0]
        tp = sum(1 for d, l in distances if d <= t and l == 1)
        fp = sum(1 for d, l in distances if d <= t and l == 0)
        tpr = tp / pos_total if pos_total else 0
        fpr = fp / neg_total if neg_total else 0
        score = tpr - fpr
        if score > best_score:
            best_score, best_t = score, t
    return best_t, best_score


def _labeled_texts(reuse_existing: bool) -> list[tuple[str, int]]:
    """Return (text, label) pairs. Reuse existing calibration_set.jsonl (no API) or
    rebuild the AI half via Opus generation (needs ANTHROPIC_API_KEY)."""
    if reuse_existing:
        if not CALIBRATION_OUT.exists():
            raise SystemExit(
                f"--reuse-existing needs {CALIBRATION_OUT}; run a full calibration once first."
            )
        pairs: list[tuple[str, int]] = []
        for line in CALIBRATION_OUT.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("text") is not None and rec.get("label") in (0, 1):
                pairs.append((rec["text"], int(rec["label"])))
        print(f"reusing {len(pairs)} existing labeled texts (no API calls)")
        return pairs

    real = _extract_real_sean_chunks()
    print(f"extracted {len(real)} real-Sean chunks")
    print("generating 15 generic-AI samples (Opus 4.7 via API key)...")
    ai = _generate_ai_samples(GENERIC_AI_PROMPTS)
    print(f"generated {len(ai)} AI samples")
    return [(t, 1) for t in real] + [(t, 0) for t in ai]


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--reuse-existing",
        action="store_true",
        help="Recompute distances + threshold from the EXISTING calibration_set.jsonl "
        "texts against the current baseline. Zero API calls, no key needed. Use this "
        "after rebuild_stylometry_baseline.py changes the feature vector.",
    )
    args = ap.parse_args()

    baseline = load_baseline(BASELINE_PATH)
    pairs = _labeled_texts(reuse_existing=args.reuse_existing)

    distances: list[tuple[float, int]] = []
    with open(CALIBRATION_OUT, "w") as f:
        for text, label in pairs:
            d = compute_distance(extract_features(text), baseline, target_text=text)
            distances.append((d, label))
            f.write(json.dumps({"label": label, "distance": d, "text": text}) + "\n")

    threshold, score = _roc_auc(distances)
    print(f"best threshold: {threshold:.2f} (TPR-FPR = {score:.2f})")
    if score < 0.4:
        print("WARNING: low separation. Consider expanding the corpus or adjusting features.")

    baseline["_threshold"] = threshold
    save_baseline(baseline, BASELINE_PATH)
    print(f"updated {BASELINE_PATH} with _threshold = {threshold:.2f}")


if __name__ == "__main__":
    main()
