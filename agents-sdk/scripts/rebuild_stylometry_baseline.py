"""Rebuild the stylometric baseline feature vector + n-grams from the CURRENT corpus.

Why this exists: `calibrate_stylometry_threshold.py` only re-tunes the *threshold*
against the existing baseline. Nothing rebuilt the baseline *features* themselves,
so `stylometry_baseline.json` drifted stale after the 2026-06 voice overhaul:
  - em_dash_density was computed pre-ban (em dashes were globally removed
    2026-06-02 and normalized to no-dash punctuation), so the old fingerprint
    rewarded a construct the voice no longer uses;
  - the Raw Stories grit anchor was added to voice-samples.md afterward and was
    never reflected in the baseline.

This script recomputes the five features (means + cross-chunk stdevs) and the
top-30 distinctive n-grams from the current voice-samples.md, then sets
`_threshold = null` to FORCE a recalibration (distances shift when the baseline
changes, so the old threshold is no longer valid). Deterministic and
credential-free: it reads only local text, no API calls.

Run order after this:
  1. python agents-sdk/scripts/rebuild_stylometry_baseline.py   (this script — free)
  2. python agents-sdk/scripts/calibrate_stylometry_threshold.py (needs ANTHROPIC_API_KEY; ~15 Opus calls)
  3. python -m agents.skill_optimizer --score-only               (the baseline measurement)
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "agents-sdk"))

from lib.skill_optimizer.stylometry import (  # noqa: E402
    extract_features,
    extract_distinctive_ngrams,
    extract_voice_corpus_chunks,
    load_baseline,
    save_baseline,
)

VOICE_SAMPLES = REPO / ".claude/skills/writing-voice-modes/references/voice-samples.md"
BASELINE_PATH = REPO / "agents-sdk/data/skill-optimizer/stylometry_baseline.json"
CALIBRATION_SET = REPO / "agents-sdk/data/skill-optimizer/calibration_set.jsonl"

FEATURE_KEYS = (
    "sentence_length_mean",
    "sentence_length_stdev",
    "comma_density_per_100w",
    "em_dash_density_per_100w",
    "first_person_freq_per_100w",
)


def _generic_baseline_corpora() -> list[str]:
    """Generic-English contrast corpus for n-gram distinctiveness.

    Uses the label==0 (generic AI) texts already captured in calibration_set.jsonl.
    That is exactly the contrast class we want Sean's n-grams to stand out against.
    Falls back to an empty list (no n-gram component) if the file is absent.
    """
    if not CALIBRATION_SET.exists():
        return []
    out: list[str] = []
    for line in CALIBRATION_SET.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("label") == 0 and rec.get("text"):
            out.append(rec["text"])
    return out


def main() -> None:
    chunks = extract_voice_corpus_chunks(VOICE_SAMPLES.read_text())
    if len(chunks) < 5:
        raise SystemExit(f"too few corpus chunks ({len(chunks)}); check voice-samples.md")
    print(f"corpus: {len(chunks)} chunks from voice-samples.md")

    per_chunk = [extract_features(c) for c in chunks]
    means = {k: statistics.mean(f[k] for f in per_chunk) for k in FEATURE_KEYS}
    stdevs = {
        k: (statistics.stdev(f[k] for f in per_chunk) if len(per_chunk) >= 2 else 0.0)
        for k in FEATURE_KEYS
    }

    baseline_corpora = _generic_baseline_corpora()
    ngrams = extract_distinctive_ngrams(
        target_corpus="\n\n".join(chunks),
        baseline_corpora=baseline_corpora,
        top_n=30,
    )
    print(f"n-gram contrast corpus: {len(baseline_corpora)} generic samples; "
          f"extracted {len(ngrams)} distinctive n-grams")

    # Show the before/after on the most-stale feature.
    old = load_baseline(BASELINE_PATH) if BASELINE_PATH.exists() else {}
    print("\nfeature        old -> new")
    for k in FEATURE_KEYS:
        print(f"  {k:28s} {old.get(k, float('nan')):.3f} -> {means[k]:.3f}")

    new_baseline = dict(means)
    new_baseline["_stdevs"] = stdevs
    new_baseline["_ngrams"] = ngrams
    new_baseline["_threshold"] = None  # force recalibration; distances shifted

    save_baseline(new_baseline, BASELINE_PATH)
    print(f"\nwrote {BASELINE_PATH}")
    print("_threshold set to null -> run calibrate_stylometry_threshold.py next.")


if __name__ == "__main__":
    main()
