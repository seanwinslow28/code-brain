"""Build stylometry baseline from voice-samples.md + a generic baseline corpus.

Run once at pre-flight time. Re-run if voice-samples.md changes.
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "agents-sdk"))

from lib.skill_optimizer.stylometry import (
    extract_features,
    extract_distinctive_ngrams,
    save_baseline,
)

VOICE_SAMPLES = REPO / ".claude/skills/writing-voice-modes/references/voice-samples.md"
OUTPUT = REPO / "agents-sdk/data/skill-optimizer/stylometry_baseline.json"

# Generic baseline corpus — short, public-domain prose for the n-gram contrast.
# (Brown corpus excerpt or similar; embedded inline to avoid NLTK dependency.)
GENERIC_BASELINE = """
The fox jumped over the dog. The man went to the store and bought a newspaper.
She was thinking about what to say next when the phone rang again. The conference
ended with a series of dry resolutions, none of which addressed the underlying
issue. He found himself wondering what would happen if no one showed up.
""" * 20  # repeat to reach ~3000 words


def _extract_sean_corpus(samples_path: Path) -> str:
    """Return the unedited+rewrites+full-passages content as a single string."""
    text = samples_path.read_text()
    # Strip frontmatter quote blocks but keep prose. Naïve approach: take everything.
    return text


def main() -> None:
    sean_corpus = _extract_sean_corpus(VOICE_SAMPLES)
    sean_features = extract_features(sean_corpus)

    # Compute per-feature stdev across split chunks of the corpus (~150 words each).
    chunks = [sean_corpus[i : i + 800] for i in range(0, len(sean_corpus), 800)]
    chunks = [c for c in chunks if len(c.split()) >= 30]
    chunk_features = [extract_features(c) for c in chunks]

    stdevs = {}
    for key in sean_features:
        vals = [cf[key] for cf in chunk_features]
        stdevs[key] = statistics.stdev(vals) if len(vals) >= 2 else 1.0

    ngrams = extract_distinctive_ngrams(
        target_corpus=sean_corpus,
        baseline_corpora=[GENERIC_BASELINE],
        top_n=30,
        ns=(2, 3, 4),
    )

    baseline = {
        **sean_features,
        "_stdevs": stdevs,
        "_ngrams": [list(ng) for ng in ngrams],
        "_threshold": None,  # filled in by Task 3.6 (calibration)
        "_corpus_word_count": len(sean_corpus.split()),
    }
    save_baseline(baseline, OUTPUT)
    print(f"wrote baseline to {OUTPUT}")
    print(f"  features: {sean_features}")
    print(f"  top n-grams (first 10): {ngrams[:10]}")


if __name__ == "__main__":
    main()
