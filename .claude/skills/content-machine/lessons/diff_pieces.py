#!/usr/bin/env python3
"""Lessons loop, mechanical layer (#168).

Aligns the machine's handoff draft against Sean's published final and emits the
change list. That list is raw material, not lessons: naming why a change happened
is judgment, and asking him for his reason is the whole point of the loop (L9).

  python3 diff_pieces.py <handoff.md> <final.md> [--json]

Alignment is per sentence rather than per word, because a lesson is about a beat,
not a token. A reworded sentence should arrive as one change to ratify, not as
six insertions and four deletions.
"""

import argparse
import difflib
import json
import re
import sys


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :]
    return text


def sentences(text):
    out = []
    for block in strip_frontmatter(text).split("\n\n"):
        # block-quote markers are formatting, not words he wrote or cut
        block = "\n".join(re.sub(r"^\s*>\s?", "", ln) for ln in block.split("\n"))
        block = " ".join(block.split())
        if not block:
            continue
        for s in re.split(r"(?<=[.!?])\s+", block):
            s = s.strip()
            if s:
                out.append(s)
    return out


def norm(s):
    """Compare on shape, not punctuation. Export artifacts and smart quotes
    should never register as edits Sean made."""
    s = s.lower().replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[^a-z0-9' ]+", " ", s).split()


def word_delta(old, new):
    """The specific words that moved, so a candidate lesson can quote them."""
    o, n = norm(old), norm(new)
    sm = difflib.SequenceMatcher(a=o, b=n, autojunk=False)
    cut, added = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            cut.extend(o[i1:i2])
        if tag in ("replace", "insert"):
            added.extend(n[j1:j2])
    return {"cut": cut, "added": added, "similarity": round(sm.ratio(), 3)}


def diff(handoff, final):
    a, b = sentences(handoff), sentences(final)
    sm = difflib.SequenceMatcher(a=[" ".join(norm(s)) for s in a],
                                 b=[" ".join(norm(s)) for s in b], autojunk=False)
    changes = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        old = a[i1:i2]
        new = b[j1:j2]
        entry = {"kind": {"replace": "rewritten", "delete": "cut", "insert": "added"}[tag],
                 "was": old, "now": new}
        if tag == "replace" and len(old) == 1 and len(new) == 1:
            entry["words"] = word_delta(old[0], new[0])
        changes.append(entry)
    kept = sum(1 for t, i1, i2, _, _ in sm.get_opcodes() if t == "equal" for _ in range(i1, i2))
    return {"sentences_handoff": len(a), "sentences_final": len(b),
            "sentences_untouched": kept, "changes": changes}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("handoff")
    ap.add_argument("final")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    result = diff(open(args.handoff, encoding="utf-8").read(),
                  open(args.final, encoding="utf-8").read())

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"HANDOFF -> FINAL  ({len(result['changes'])} changes, "
          f"{result['sentences_untouched']} of {result['sentences_handoff']} sentences untouched)")
    print()
    for i, c in enumerate(result["changes"], 1):
        print(f"  [{i}] {c['kind'].upper()}")
        for s in c["was"]:
            print(f"       was: {s}")
        for s in c["now"]:
            print(f"       now: {s}")
        w = c.get("words")
        if w:
            if w["cut"]:
                print(f"       words out: {' '.join(w['cut'])}")
            if w["added"]:
                print(f"       words in : {' '.join(w['added'])}")
        print()
    print("These are changes, not lessons. Naming the reason is his; the machine")
    print("proposes candidates and never adopts one on its own (L9).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
