#!/usr/bin/env python3
"""Rebuild baseline.json from the git-ignored content-machine corpus.

Why this script exists (#177). The previous baseline was generated from a
TRACKED file, `baseline-corpus.md`, holding a copy of Sean's prose. Two things
went wrong with that:

  1. Its contents were never provenance-checked. All 58 sentences turned out to
     be quarantined material - mode-applied machine essays presented as Sean's
     voice - and nothing in the pipeline could have noticed.
  2. Committing verbatim Sean to a public repo is a rule-9 violation the moment
     the text is real corpus rather than machine prose.

So there is no corpus copy any more. This script reads the private brain
directly, selects named segments, and writes ONLY aggregate statistics plus a
provenance block. No prose is stored, printed, or committed.

Usage:
    python3 build_baseline.py                  # writes ./baseline.json
    python3 build_baseline.py --check          # verify the committed baseline still matches
    python3 build_baseline.py --out other.json

Requires the corpus at creative-studio/content-machine/corpus/ (git-ignored,
local only). On a machine without it, this exits 2 and says so; it never
fabricates a baseline.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
CORPUS = REPO / "creative-studio" / "content-machine" / "corpus"

# The admitted set, ruled 2026-08-26 (#177). Selection rules, in order:
#   - tier A (unmixed verbatim; see the corpus MANIFEST)
#   - sustained prose, >= 300 words, because the analyzer's variance signals are
#     meaningless below that and the corpus's short fragments are diction
#     evidence rather than evidence of how he sustains prose
#   - nothing produced through the content machine, so the yardstick can never
#     be calibrated on the thing it measures
# Each entry is (corpus file, '## ' heading prefix). A heading that no longer
# matches is a hard error: a silently changed baseline is how #177 happened.
SEGMENTS = [
    ("03-prose-anchors.md", '"Start Here"'),
    ("03-prose-anchors.md", '"About"'),
    ("03-prose-anchors.md", "Pre-AI screenplay prose"),
    ("06-short-form-and-exercises.md", "Exercise rewrites"),
    ("04-hand-edits-and-reasons.md", "VoicePrint refine loop"),
]

# Gate shape, ruled 2026-08-26 (#177). One-sided low, in population sigmas.
# 1.0 was the original and false-flagged 5 of 6 of Sean's own passages under
# leave-one-out: four one-sided 1-sigma tests OR'd together flag roughly half of
# any population by construction. 2.0 measures 0 of 5 false and still separates
# the machine draft from his hand-rewrite.
SIGMA = 2.0
# Metrics that may raise a flag. opener_other_pct is REPORT-ONLY: it was the
# last remaining false-positive source at 2 sigma.
FLAG_METRICS = ["cv", "mattr", "first_person_rate"]

MIN_WORDS = 300


def verbatim(path: Path, prefix: str) -> str:
    """Return one segment's verbatim Sean text.

    The corpus rule: every '>' blockquote line is Sean's words, everything else
    is metadata. Anything unquoted is dropped here rather than trusted.
    """
    text = path.read_text(encoding="utf-8")
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, body = block.split("\n", 1)
        if not head.strip().startswith(prefix):
            continue
        quoted = [
            re.sub(r"^\s*>\s?", "", line)
            for line in body.splitlines()
            if line.lstrip().startswith(">")
        ]
        return "\n".join(quoted).strip()
    raise SystemExit(f"ERROR: no '## {prefix}...' heading in {path.name}. "
                     f"The corpus moved; fix SEGMENTS rather than the numbers.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(Path(__file__).with_name("baseline.json")))
    ap.add_argument("--check", action="store_true",
                    help="rebuild in memory and diff against the committed baseline")
    args = ap.parse_args()

    if not CORPUS.is_dir():
        print(f"ERROR: corpus not found at {CORPUS}\n"
              "It is git-ignored and local-only, so this machine cannot rebuild "
              "the baseline. Nothing was written.", file=sys.stderr)
        return 2

    segments, manifest = [], []
    for fname, prefix in SEGMENTS:
        text = verbatim(CORPUS / fname, prefix)
        words = len(text.split())
        if words < MIN_WORDS:
            raise SystemExit(f"ERROR: '{prefix}' is {words} words, below the "
                             f"{MIN_WORDS}-word floor. Ruling changed, or the corpus did.")
        segments.append(text)
        manifest.append({
            "file": fname,
            "heading_prefix": prefix,
            "words": words,
            # Content hash, not content: proves which text produced these numbers
            # without putting a syllable of it in a tracked file.
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        })

    # analyze.py --emit-baseline wants one file, '## ' per segment. Build it in a
    # temp file that is deleted immediately; it never touches the repo.
    sys.path.insert(0, str(Path(__file__).parent))
    import analyze  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        corpus_file = Path(tmp) / "corpus.md"
        corpus_file.write_text(
            "\n".join(f"## seg{i}\n\n{t}\n" for i, t in enumerate(segments)),
            encoding="utf-8",
        )
        out_file = Path(tmp) / "baseline.json"
        baseline = analyze.emit_baseline(str(corpus_file), str(out_file))

    baseline["generated_from"] = "content-machine corpus (git-ignored); see provenance"
    baseline["gate"] = {"sigma": SIGMA, "flag_metrics": FLAG_METRICS,
                        "report_only": ["opener_other_pct"]}
    baseline["provenance"] = {
        "ruled": "2026-08-26",
        "ticket": "https://github.com/seanwinslow28/code-brain/issues/177",
        "tier": "A (unmixed verbatim, per corpus MANIFEST)",
        "min_words": MIN_WORDS,
        "excludes": "anything produced through the content machine, to avoid "
                    "calibrating the yardstick on what it measures",
        "rebuild": "python3 build_baseline.py   (needs the local corpus)",
        "segments": manifest,
    }

    rendered = json.dumps(baseline, indent=2) + "\n"
    if args.check:
        committed = Path(args.out)
        if not committed.exists():
            print("no committed baseline to check against", file=sys.stderr)
            return 1
        same = committed.read_text(encoding="utf-8") == rendered
        print("baseline matches the corpus" if same
              else "DRIFT: committed baseline does not match a fresh build")
        return 0 if same else 1

    Path(args.out).write_text(rendered, encoding="utf-8")
    print(f"Wrote baseline ({baseline['segments']} segments, "
          f"{sum(m['words'] for m in manifest)} words) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
