#!/usr/bin/env python3
"""Origin-fidelity gate, mechanical layer (#164).

The constitution's own test: point at any vivid phrase in the draft and name the
transcript line it came from. This script does the cheap half of that, with no
dependencies and no model call. It finds every atom in the draft that has no
counterpart in the transcript, ranked by how hard the law is on that kind of atom.

It reports. It never rewrites, never scores, and never loops (L8).

  python3 origin_check.py <draft.md> <transcript.md> [--lane expressive|professional] [--json]

Exit codes:
  0  no untraced atoms, or Expressive lane (always advisory)
  0  Professional lane with untraced atoms that are not claims
  1  Professional lane with at least one untraced CLAIM (number, date, proper noun)
     -> the delivery block. Clear it by confirming the fact or striking it.
"""

import argparse
import json
import re
import sys

# Words that carry no claim and no image. An unmatched stopword is never a leak,
# because the law explicitly permits connective tissue.
STOP = set("""
a about above after again against all am an and any are aren't as at be because been
before being below between both but by can cannot could couldn't did didn't do does
doesn't doing don't down during each few for from further had hadn't has hasn't have
haven't having he he'd he'll he's her here here's hers herself him himself his how
how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most
mustn't my myself no nor not of off on once only or other ought our ours ourselves out
over own same shan't she she'd she'll she's should shouldn't so some such than that
that's the their theirs them themselves then there there's these they they'd they'll
they're they've this those through to too under until up very was wasn't we we'd we'll
we're we've were weren't what what's when when's where where's which while who who's
whom why why's with won't would wouldn't you you'd you'll you're you've your yours
yourself yourselves just now also get got go goes going went gone come came thing
things something anything nothing everything one two really actually basically then
still even much many make made makes back way ways take takes took give gives gave
put puts see saw seen say says said know knew known think thought want wanted need
needed use used using find found tell told ask asked look looked keep kept let lets
turn turns turned start started end ends ended run runs ran little big long short new
old good bad first last next another every any own around here there again always never
ever yet already off out up down over under between through during before after above
below since while until because although though unless whether either neither both
each other others another such same different
""".split())

CLAIM_RE = re.compile(r"^\d[\d,.:/-]*$")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*|\d[\d,.:/-]*")


def stem(w):
    """Crude suffix stripper. No deps, and precision matters more than linguistics
    here: over-stemming causes a missed leak, which is the failure we can afford
    least, so we stem conservatively."""
    w = w.lower().replace("’", "'")
    for suf in ("'s", "s'"):
        if w.endswith(suf) and len(w) > len(suf) + 2:
            w = w[: -len(suf)]
    for suf in ("ing", "edly", "ed", "ly", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            base = w[: -len(suf)]
            # restore a doubled consonant ("dropped" -> "drop")
            if len(base) > 2 and base[-1] == base[-2]:
                base = base[:-1]
            return base
    return w


def variants(w):
    """Every form a word might reduce to, plus the silent-e it may have come from.

    Stemming has to repeat, not run once. A single pass sent "morning" to "morn"
    but "mornings" only as far as "morning", so his own word failed to match
    itself and the gate reported his line as a leak. Bounded at two extra passes,
    which is enough for a plural of a gerund and short of collapsing real words
    into each other.
    """
    out, cur = set(), w
    for _ in range(3):
        st = stem(cur)
        out |= {st, st + "e"}
        if st == cur:
            break
        cur = st
    return out


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :]
    return text


def sentences(text):
    out = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        for s in re.split(r"(?<=[.!?])\s+", block.replace("\n", " ")):
            s = s.strip()
            if s:
                out.append(s)
    return out


def author_only(transcript):
    """Strip the interviewer out of the transcript.

    The lens forbids the interviewer contributing a phrase, because a word that
    entered the room in a QUESTION is not the author's word. Indexing the whole
    file quietly launders that contamination into "traced": on the first real run
    the draft used "digging", which appears nowhere except in the interviewer's
    own Q8. Answers and his corrections count. Nothing else does.
    """
    keep, in_answer, last_q = [], False, 0
    for line in transcript.splitlines():
        m_a = re.match(r"^A(\d+):", line)
        m_q = re.match(r"^Q(\d+):", line)
        if m_a:
            in_answer = True
            keep.append(re.sub(r"^A\d+:\s*", "", line))
        elif m_q:
            n = int(m_q.group(1))
            # An author quoting the question number back at us is NOT a new question.
            # Sean's first answer opened with a literal "Q1:" of his own, and a naive
            # parser read his words as the interviewer's and dropped them from his
            # vocabulary, which turns his own lines into false leaks. A question only
            # counts when its number advances.
            if n > last_q:
                last_q, in_answer = n, False
            elif in_answer:
                keep.append(re.sub(r"^Q\d+:\s*", "", line))
        elif re.match(r"^(READ-BACK|TRANSCRIPT|Lens:|Duration:)", line):
            in_answer = False
        elif re.match(r"^CORRECTIONS", line):
            in_answer = True          # corrections are his, and they outrank the answers
        elif in_answer:
            keep.append(line)
    return "\n".join(keep)


def build_index(transcript):
    raw = author_only(transcript).lower().replace("’", "'")
    words = WORD_RE.findall(raw)
    stems = set()
    for w in words:
        stems |= variants(w)
    return {"stems": stems, "raw": raw}


def classify(token, is_capitalized):
    """How hard is the law on this kind of atom? The law names number, name, and
    place explicitly, so those are claims. Everything else is an image at most."""
    if CLAIM_RE.match(token):
        return "claim"
    if is_capitalized:
        return "claim"
    return "image"


def check(draft_text, transcript_text):
    idx = build_index(transcript_text)
    findings = []
    for sent in sentences(strip_frontmatter(draft_text)):
        tokens = WORD_RE.findall(sent)
        untraced = []
        for i, tok in enumerate(tokens):
            low = tok.lower().replace("’", "'")
            if low in STOP:
                continue
            if len(low) < 3 and not CLAIM_RE.match(low):
                continue
            if variants(tok) & idx["stems"]:
                continue
            # a multi-word proper noun or hyphenate may live in the transcript verbatim
            if low in idx["raw"]:
                continue
            capitalized = tok[:1].isupper() and i > 0
            untraced.append({"token": tok, "kind": classify(low, capitalized)})
        if untraced:
            findings.append({"sentence": sent, "untraced": untraced})
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("transcript")
    ap.add_argument("--lane", choices=["expressive", "professional"], default="expressive")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    draft = open(args.draft, encoding="utf-8").read()
    transcript = open(args.transcript, encoding="utf-8").read()
    findings = check(draft, transcript)

    claims = [f for f in findings if any(u["kind"] == "claim" for u in f["untraced"])]
    blocked = args.lane == "professional" and bool(claims)

    if args.json:
        print(json.dumps({"lane": args.lane, "findings": findings,
                          "claim_count": len(claims), "blocked": blocked}, indent=2))
        return 1 if blocked else 0

    print(f"ORIGIN CHECK (mechanical layer) — lane: {args.lane}")
    print(f"  sentences with untraced atoms: {len(findings)}")
    print(f"  of those, carrying an untraced CLAIM (number/date/name): {len(claims)}")
    print()
    if not findings:
        print("  Nothing unmatched. The judgment layer still has to read for compressions")
        print("  and paraphrase, which this layer cannot see.")
    for f in findings:
        marks = ", ".join(f"{u['token']} [{u['kind']}]" for u in f["untraced"])
        print(f"  · {f['sentence']}")
        print(f"      untraced: {marks}")
        print()
    print("This layer flags words with no transcript counterpart. It cannot tell an")
    print("invention from a legitimate connective phrase. That judgment, and the ASK LIST")
    print("for anything worth keeping, belong to the reading layer. Nothing here is a verdict.")
    if blocked:
        print()
        print("PROFESSIONAL LANE: delivery blocked on the untraced claims above.")
        print("Confirm each fact against the transcript or strike it. The gate does not revise.")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
