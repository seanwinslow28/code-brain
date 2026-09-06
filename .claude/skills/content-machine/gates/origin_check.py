#!/usr/bin/env python3
"""Origin-fidelity gate, mechanical layer (#164).

The constitution's own test: point at any vivid phrase in the draft and name the
transcript line it came from. This script does the cheap half of that, with no
dependencies and no model call. It finds every atom in the draft that has no
counterpart in the transcript, ranked by how hard the law is on that kind of atom.

It reports. It never rewrites, never scores, and never loops (L8).

  python3 origin_check.py <draft.md> <transcript.md> [--lane expressive|professional] [--json]

INVERTED MODE (X's reactive route, #249/#250):

  python3 origin_check.py <draft.md> --stimulus <block.md> [--transcript <mini.md>]

A cold reactive post has no transcript. The stimulus block is someone else's
post, and it must NEVER be indexed in a transcript's place: the gate clears
whatever it finds in the indexed region, so pointing it at the stimulus would
clear every phrase lifted from the person being answered, turning a
leak-catcher into a leak-licenser. So the block is a **forbidden-strings**
source, the question flips from *did these words come from him* to *did these
words come from the post he is answering, and is he claiming something about
himself he never said*, and passing a block as the transcript is refused
outright (exit 2) rather than warned about.

Exit codes:
  0  no untraced atoms, or Expressive lane (always advisory)
  0  Professional lane with untraced atoms that are not claims
  1  Professional lane with at least one untraced CLAIM (number, date, proper noun),
     or, in inverted mode, a lifted run or an unsourced first-person claim
     -> the delivery block. Clear it by confirming the fact or striking it.
  2  Refusal: a stimulus block was handed over as a transcript. Not a finding
     about the draft — a wiring mistake, and the one that breaks the gate.
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
# A number token must END in a digit. The separators are only meaningful between
# digits ("1,000", "3.5", "2026-09-05", "10:30"), and letting one trail meant a
# number at the end of a sentence tokenized as "33." and could never match the
# transcript's "33" — an untraced CLAIM every time, which BLOCKS the Professional
# lane. Found by the #246 X run, on a draft ending "...than books in 33."
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*|\d(?:[\d,.:/-]*\d)?")


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


# ------------------------------------------------------ inverted mode ----
#
# X's reactive route (#249, built #250). Everything below runs against a
# STIMULUS BLOCK, which has the opposite polarity to a transcript.

STIMULUS_SENTINEL = "STIMULUS BLOCK"

# Checked against the raw lowercase token, before the stoplist, because most
# of these are stopwords: the law's own phrase is "first person plus a number,
# date, or proper noun", and the first person is exactly the connective tissue
# the stoplist exists to forgive.
FIRST_PERSON = set("""
i i'm i've i'd i'll me my mine myself we we're we've we'd we'll us our ours ourselves
""".split())

# A lifted run is a contiguous stretch of CONTENT words shared with the post
# being answered, stopwords collapsed out. Three is the shortest run that can
# carry a joke's construction rather than its subject; two is a noun phrase and
# would fire on the shared topic every time, which is the point of replying.
LIFT_RUN = 3


class StimulusPassedAsTranscript(Exception):
    """The one wiring mistake that silently disarms the gate."""


def looks_like_stimulus(text):
    for line in text.splitlines():
        if line.strip():
            return line.startswith(STIMULUS_SENTINEL)
    return False


def stimulus_post_text(text):
    """The verbatim `Post:` field of a block. Only that field is forbidden
    strings — the header, the Media gloss and the block's own footer are our
    words about the post, not the post."""
    if not looks_like_stimulus(text):
        raise ValueError(f"not a stimulus block (first line must start with {STIMULUS_SENTINEL!r})")
    out, in_post = [], False
    for raw in text.splitlines()[1:]:
        m = re.match(r"^(Source|Author|Post|Media|Surface|Fetch):\s?(.*)$", raw)
        if m:
            if in_post:
                break
            if m.group(1) == "Post":
                in_post, out = True, [m.group(2)]
            continue
        if in_post:
            if raw.startswith("      "):
                out.append(raw[6:])
            elif raw.strip() == "":
                break
            else:
                out.append(raw)
    return "\n".join(out).strip()


def stimulus_field(text, name):
    for raw in text.splitlines():
        m = re.match(rf"^{name}:\s?(.*)$", raw)
        if m:
            return m.group(1).strip()
    return ""


def content_stems(text):
    """Stems in order, stopwords and short tokens dropped. The sequence is what
    a lifted run is measured over; collapsing the connective tissue is what
    makes a lightly reworded lift still match."""
    seq = []
    for tok in WORD_RE.findall(text):
        low = tok.lower().replace("’", "'")
        if low in STOP:
            continue
        if len(low) < 3 and not CLAIM_RE.match(low):
            continue
        seq.append(stem(low))
    return seq


def _runs(seq, n):
    return {tuple(seq[i:i + n]) for i in range(max(len(seq) - n + 1, 0))}


def check_stimulus(draft_text, stimulus_text, transcript_text=None):
    """Returns (findings, post_text).

    Two kinds, and they are different failures with different remedies:

      lifted           — a run of content words taken from the post he is
                         answering. Remedy: write the line himself.
      unsourced_claim  — first person plus a number, date or name, with nothing
                         behind it. Remedy: ASK LIST, one question, one line
                         back as a mini-transcript. Not "untraced": out of
                         scope for the form. A cold reactive post asserts
                         nothing about his fleet, his numbers, his month.

    A claim token that appears in the stimulus is exempt: the post supplies the
    subject, so a number he is answering is not a claim about his week. A
    lifted run is caught separately and is the check that owns that case.

    Two more exemptions, and note that they widen the CLAIM set only — never
    the forbidden-strings set, which stays the `Post:` field alone. The block's
    author handle is not a claim about his week (naming the person you are
    answering is the form), and neither is the `Media:` gloss, which is our own
    description of a picture both of them can see.
    """
    post = stimulus_post_text(stimulus_text)
    stim_seq = content_stems(post)
    stim_runs = _runs(stim_seq, LIFT_RUN)
    stim_stems = set(stim_seq)
    for extra in (stimulus_field(stimulus_text, "Author"),
                  stimulus_field(stimulus_text, "Media")):
        stim_stems |= set(content_stems(extra))

    traced = build_index(transcript_text)["stems"] if transcript_text else set()

    findings = []
    for sent in sentences(strip_frontmatter(draft_text)):
        tokens = WORD_RE.findall(sent)
        lows = [t.lower().replace("’", "'") for t in tokens]

        lifted = []
        seq = content_stems(sent)
        for i in range(max(len(seq) - LIFT_RUN + 1, 0)):
            run = tuple(seq[i:i + LIFT_RUN])
            if run in stim_runs:
                lifted.append(" ".join(run))

        claims = []
        if any(l in FIRST_PERSON for l in lows):
            for i, tok in enumerate(tokens):
                low = lows[i]
                if low in FIRST_PERSON:
                    continue
                capitalized = tok[:1].isupper() and i > 0
                if not (CLAIM_RE.match(low) or capitalized):
                    continue
                if variants(tok) & stim_stems:      # the post supplies the subject
                    continue
                if traced and (variants(tok) & traced):   # the mini-transcript answered it
                    continue
                claims.append(tok)

        if lifted or claims:
            findings.append({"sentence": sent,
                             "lifted": sorted(set(lifted)),
                             "claims": claims})
    return findings, post


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("transcript", nargs="?", default=None,
                    help="the interview transcript (omit in inverted mode)")
    ap.add_argument("--transcript", dest="transcript_opt", default=None,
                    help="mini-transcript for an ASK LIST answer, alongside --stimulus")
    ap.add_argument("--stimulus", default=None,
                    help="X stimulus block: forbidden strings, never vocabulary (#250)")
    ap.add_argument("--lane", choices=["expressive", "professional"], default="expressive")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    draft = open(args.draft, encoding="utf-8").read()
    transcript_path = args.transcript_opt or args.transcript
    if not transcript_path and not args.stimulus:
        ap.error("give a transcript, or --stimulus for X's reactive route")

    transcript = None
    if transcript_path:
        transcript = open(transcript_path, encoding="utf-8").read()
        if looks_like_stimulus(transcript):
            print(f"REFUSED: {transcript_path} is a STIMULUS BLOCK, not a transcript.",
                  file=sys.stderr)
            print("", file=sys.stderr)
            print("Indexing a block as permitted vocabulary would clear every phrase lifted",
                  file=sys.stderr)
            print("from the person being answered — the gate would license the leak it exists",
                  file=sys.stderr)
            print("to catch. Pass it as --stimulus instead.", file=sys.stderr)
            return 2

    if args.stimulus:
        stim_text = open(args.stimulus, encoding="utf-8").read()
        try:
            findings, post = check_stimulus(draft, stim_text, transcript)
        except ValueError as exc:
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 2
        lifted_n = sum(len(f["lifted"]) for f in findings)
        claim_n = sum(len(f["claims"]) for f in findings)
        blocked = args.lane == "professional" and bool(lifted_n or claim_n)

        if args.json:
            print(json.dumps({"mode": "inverted", "lane": args.lane,
                              "stimulus_words": len(post.split()),
                              "mini_transcript": bool(transcript),
                              "findings": findings, "lifted_count": lifted_n,
                              "claim_count": claim_n, "blocked": blocked}, indent=2))
            return 1 if blocked else 0

        print(f"ORIGIN CHECK (inverted — X reactive route) — lane: {args.lane}")
        print(f"  stimulus: {len(post.split())} words of someone else's post, "
              f"scanned as FORBIDDEN strings")
        print(f"  mini-transcript: {'yes' if transcript else 'none'}")
        print(f"  lifted runs: {lifted_n}   unsourced first-person claims: {claim_n}")
        print()
        if not findings:
            print("  Nothing lifted, nothing claimed. The reading pass still owns recombination:")
            print("  the question is not whether a word is his, but whether he put these words")
            print("  in this order.")
        for f in findings:
            print(f"  · {f['sentence']}")
            if f["lifted"]:
                print(f"      lifted from the post: {', '.join(f['lifted'])}")
            if f["claims"]:
                print(f"      claims about his week: {', '.join(f['claims'])}")
            print()
        if lifted_n:
            print("A lifted run is borrowed strings, not borrowed structure. Write the line.")
        if claim_n:
            print("A cold reactive post asserts nothing about his fleet, his numbers, his month.")
            print("If the post genuinely needs the fact: ASK LIST, one question, one line back,")
            print("stored as a mini-transcript and passed here with --transcript. Deleting the")
            print("beat is the more expensive mistake.")
        if blocked:
            print()
            print("PROFESSIONAL LANE: delivery blocked. The gate does not revise.")
        return 1 if blocked else 0

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
