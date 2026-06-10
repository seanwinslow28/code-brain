#!/usr/bin/env python3
"""
diff_metrics.py — measure how much a reader edited a draft VoicePrint wrote in
their voice, and log it so the refine loop can show the diffs shrinking over rounds.

Pure standard library. No network, no API key, no external deps. Runs anywhere
Python 3.8+ is installed. This is the local "measurement" half of VoicePrint's
proof story: lower pct_changed over rounds = the generated voice is converging on
the reader.

Usage:
  python3 diff_metrics.py --before draft.txt --after edited.txt --round 3 \
      --log voiceprint/_work/refine-log.jsonl

  # or pass text inline:
  python3 diff_metrics.py --before-text "..." --after-text "..." --round 1 \
      --log voiceprint/_work/refine-log.jsonl

Prints a JSON object with the metrics and (unless --no-log) appends one JSON line
to the log file. Designed to be called by the /voiceprint-refine command.
"""

import argparse
import datetime
import difflib
import json
import re
import sys
from pathlib import Path


def _read(text_arg, file_arg):
    if text_arg is not None:
        return text_arg
    if file_arg:
        return Path(file_arg).read_text(encoding="utf-8", errors="ignore")
    return None


def _tokens(s):
    # word-level tokens; punctuation folded so rewording (not re-spacing) drives the signal
    return re.findall(r"\w+", s.lower())


def compute(before: str, after: str) -> dict:
    b_tokens, a_tokens = _tokens(before), _tokens(after)
    token_sim = difflib.SequenceMatcher(None, b_tokens, a_tokens).ratio()
    char_sim = difflib.SequenceMatcher(None, before, after).ratio()

    # word-level changed count via the opcodes (replace/delete/insert)
    sm = difflib.SequenceMatcher(None, b_tokens, a_tokens)
    changed = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            changed += max(i2 - i1, j2 - j1)

    pct_changed = round((1.0 - token_sim) * 100, 1)
    return {
        "token_similarity": round(token_sim, 4),
        "char_similarity": round(char_sim, 4),
        "pct_changed": pct_changed,          # headline: % of the draft the reader reworked
        "words_changed": changed,
        "before_words": len(b_tokens),
        "after_words": len(a_tokens),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Measure reader edits to a voice draft.")
    p.add_argument("--before", help="path to the draft VoicePrint generated")
    p.add_argument("--after", help="path to the reader's edited version")
    p.add_argument("--before-text", help="inline draft text (alternative to --before)")
    p.add_argument("--after-text", help="inline edited text (alternative to --after)")
    p.add_argument("--round", type=int, default=None, help="refine round number")
    p.add_argument("--log", help="path to refine-log.jsonl to append to")
    p.add_argument("--no-log", action="store_true", help="print only, do not append")
    args = p.parse_args(argv)

    before = _read(args.before_text, args.before)
    after = _read(args.after_text, args.after)
    if before is None or after is None:
        p.error("need both a before and an after (via --before/--after or --before-text/--after-text)")

    metrics = compute(before, after)
    record = {
        "round": args.round,
        "date": datetime.date.today().isoformat(),
        **metrics,
    }

    if args.log and not args.no_log:
        log_path = Path(args.log)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        record["logged_to"] = str(log_path)

    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
