#!/usr/bin/env python3
"""
fingerprint.py — VoicePrint's "more you, less generic-AI" measurement wrapper.

Wraps the bundled writing-critique analyzer (analyze.py) to compute a writer's
quantitative fingerprint — sentence-length burstiness (variety) and lexical
diversity (MATTR) — and compare three things:
  - the reader's own voice samples (who they are)
  - a draft written in their voice (what the skill produced)
  - a shipped generic-AI baseline (what we're moving away from)

The honest claim it supports: is the draft's fingerprint closer to the reader's own
samples than to generic-AI prose? Pure standard library; no network, no API key.

Modes:
  # full comparison (used by /voiceprint-proof):
  python3 fingerprint.py --samples voice-samples.md --draft draft.md --out proof_fp.json

  # compute one file's fingerprint (used to build the generic-AI baseline):
  python3 fingerprint.py --compute-only generic-ai-corpus.md
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYZER = HERE.parent / "skills" / "writing-critique" / "references" / "analyze.py"
DEFAULT_GENERIC = HERE / "generic-ai-baseline.json"


def _find_key(obj, key):
    """Depth-first search for the first occurrence of `key` in a nested dict/list."""
    if isinstance(obj, dict):
        if key in obj and not isinstance(obj[key], (dict, list)):
            return obj[key]
        for v in obj.values():
            r = _find_key(v, key)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = _find_key(v, key)
            if r is not None:
                return r
    return None


def fingerprint_file(path: Path) -> dict:
    """Run the analyzer on a file and pull burstiness (cv) + MATTR."""
    if not ANALYZER.exists():
        raise FileNotFoundError(f"analyzer not found at {ANALYZER}")
    out = subprocess.run(
        [sys.executable, str(ANALYZER), str(path), "--json"],
        capture_output=True, text=True,
    )
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        return {"burstiness_cv": None, "mattr": None, "note": "analyzer returned no JSON"}
    return {
        "burstiness_cv": _find_key(data, "cv"),
        "mattr": _find_key(data, "mattr"),
    }


def _closer(draft, reader, generic):
    """Which baseline is the draft's value nearer? Returns 'reader' | 'generic' | None."""
    if draft is None or reader is None or generic is None:
        return None
    return "reader" if abs(draft - reader) <= abs(draft - generic) else "generic"


def main(argv=None):
    p = argparse.ArgumentParser(description="VoicePrint fingerprint comparison.")
    p.add_argument("--compute-only", help="print one file's fingerprint and exit")
    p.add_argument("--samples", help="the reader's voice-samples.md")
    p.add_argument("--draft", help="a draft written in the reader's voice")
    p.add_argument("--generic-baseline", default=str(DEFAULT_GENERIC),
                   help="generic-AI baseline json (default: sibling generic-ai-baseline.json)")
    p.add_argument("--out", help="write the comparison JSON here too")
    args = p.parse_args(argv)

    if args.compute_only:
        print(json.dumps(fingerprint_file(Path(args.compute_only)), indent=2))
        return 0

    if not args.samples or not args.draft:
        p.error("need --samples and --draft (or --compute-only)")

    reader = fingerprint_file(Path(args.samples))
    draft = fingerprint_file(Path(args.draft))
    generic = {"burstiness_cv": None, "mattr": None}
    gp = Path(args.generic_baseline)
    if gp.exists():
        try:
            generic = json.loads(gp.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    result = {
        "reader_burstiness": reader["burstiness_cv"],
        "draft_burstiness": draft["burstiness_cv"],
        "generic_ai_burstiness": generic.get("burstiness_cv"),
        "reader_mattr": reader["mattr"],
        "draft_mattr": draft["mattr"],
        "generic_ai_mattr": generic.get("mattr"),
        "draft_burstiness_closer_to": _closer(
            draft["burstiness_cv"], reader["burstiness_cv"], generic.get("burstiness_cv")),
        "note": ("Burstiness = sentence-length variety. Generic AI is flat (low); "
                 "human prose is bursty. 'closer_to: reader' is the win."),
    }
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
