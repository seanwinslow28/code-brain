#!/usr/bin/env python3
"""Generate move-licensing.md, the shared licensing matrix (#162).

36 moves x 9 mediums is 324 cells. Ruling them one at a time is not a thing
anyone should do, so two axes settle 321 and Sean ruled the rest:

  HEAT  how much register the move carries   (0 resume-safe .. 3 hot)
  ROOM  how much space it needs to land      (1 sentence .. 4 whole-piece)

A cell is BANNED iff the move's heat exceeds the medium's budget, or it needs
more room than the form gives. Everything else is LICENSED. Six cells are ruled
directly, on evidence the axes cannot see.

The roster is READ FROM writing-voice-modes/SKILL.md rather than copied, so the
matrix cannot drift from the guide. A move added or renamed there fails this
script until it is rated here, which is the point: an unrated move is an
unlicensed move.

Usage:
    python3 build_licensing.py            # regenerate move-licensing.md
    python3 build_licensing.py --check    # verify the committed file is current
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUIDE = HERE.parents[1] / "writing-voice-modes" / "SKILL.md"
OUT = HERE / "move-licensing.md"

# heat 0 none | 1 wit | 2 voice | 3 hot        room 1 sentence | 2 beat | 3 runway | 4 piece
# Rated 2026-08-26 from each move's mechanic in the guide. These ratings are the
# whole matrix: a roster that comes out wrong is nearly always a move rated one
# step too hot, not a medium's budget.
RATINGS = {
    "Funniest Word Last": (2, 1), "Unsignposted Pivot": (2, 2), "Tool-as-Character": (2, 2),
    "Expectation / Instead": (1, 2), "Mid-Action Open": (1, 4), "Shout-Caps": (3, 1),
    "Breath-Mark Rhythm": (1, 3), "Jewel Center": (1, 3), "Sensory Cascade": (3, 3),
    "Then / Now Narrator": (1, 2), "Flat Collision": (2, 2), "Short Declarative Drop": (1, 2),
    "Anaphoric Stack": (1, 2),
    "Hard Cut / Deflation": (2, 2), "Rule of Three + Emotional Pivot": (2, 1),
    "Callback Closer": (1, 4), "Sensory Before Numbers": (2, 3), "Pop Culture Anchoring": (2, 1),
    "Hyper-Specific Anecdote": (3, 2), "Screenwriting Cut-To": (3, 2),
    "Humor as Trojan Horse": (2, 3), "Self-Deprecation as Structure": (2, 4),
    "Blunt-Literal Description": (1, 1), "Reader-Dismissal": (2, 1),
    "Equation / Formula Defamiliarizer": (2, 1), "Inverted Refrain": (2, 4),
    "Borrowed Canon Line": (2, 1), "Faux-Ignorance Aside": (2, 1),
    "Affectionate-Insult Epithet": (3, 1), "Comic Under-Reaction": (2, 2),
    "Sincerity Punished by the World": (2, 4), "Fumbled Idiom": (2, 1),
    "Zeugma Paint": (2, 1), "Buried Rotten Beat": (3, 3),
    "Character-Intro Verdict": (3, 1), "Rhetorical Catechism": (1, 2),
}

# (lane, heat budget, room). Ruled by Sean 2026-08-26, unchanged from the proposal.
MEDIA = {
    "Substack": ("Expressive", 3, 4),
    "X": ("Expressive", 3, 1),
    "YouTube / Reels": ("Expressive", 3, 4),
    "Portfolio write-up": ("Expressive", 2, 2),
    "LinkedIn": ("Professional", 2, 2),
    "Cover letter": ("Professional", 1, 2),
    "Email": ("Professional", 1, 2),
    "Questionnaire": ("Professional", 1, 2),
    "Resume": ("Professional", 0, 1),
}

# Cells the axes cannot see. verdict, condition (for conditional), and the evidence.
RULINGS = {
    ("Screenwriting Cut-To", "Substack"): (
        "conditional",
        "The juxtaposition is licensed. The literal screenplay notation is not. Write the "
        "hard turn from stated intent to actual reality in prose; do not carry it with "
        "`HARD CUT TO:` or a bare italic *cut to*.",
        "Ruled by Sean 2026-08-26. #175 confirmed the move at origin in the scripts and in "
        "prose, but prose has exactly one instance and it used literal screenplay notation "
        "outside a screenplay.",
    ),
    ("Screenwriting Cut-To", "X"): (
        "banned", "",
        "Ruled by Sean 2026-08-26, against the axes, which licensed it. A single post has no "
        "room to establish the stated intent before turning on it, so the notation ends up "
        "doing work the setup should have done.",
    ),
    ("Screenwriting Cut-To", "YouTube / Reels"): (
        "licensed", "",
        "#172: the screenplay-derived moves are most at home in a script.",
    ),
    ("Shout-Caps", "YouTube / Reels"): (
        "conditional",
        "Licensed in narration the voice actually performs. Banned in the production layer: "
        "all-caps in scene headings, character names, or action lines is screenplay format "
        "convention and not this move.",
        "Ruled by Sean 2026-08-26, extending #161's prose-form-only rule to the one medium "
        "where a script's format convention and the prose move collide on the page.",
    ),
    ("Equation / Formula Defamiliarizer", "Substack"): (
        "banned", "",
        "#175: restricted to short-form. Two instances, one source, both tweet-shaped.",
    ),
    ("Equation / Formula Defamiliarizer", "YouTube / Reels"): (
        "banned", "",
        "#175's short-form restriction. A spoken script is not short-form.",
    ),
}

MARKS = {"licensed": "L", "conditional": "C", "banned": "-"}


def roster_from_guide() -> list[tuple[str, str]]:
    """(move, origin) pairs, read from the voice guide's two tables."""
    text = GUIDE.read_text(encoding="utf-8")
    out = []
    for section, nxt, origin in (
        ("## Technique Moves", "**Deleted in the same pass", "technique"),
        ("## Sean's Signature Moves", "Nine of these rows were mined", "signature"),
    ):
        if section not in text:
            raise SystemExit(f"ERROR: '{section}' missing from {GUIDE.name}. "
                             "The guide moved; fix this script rather than the matrix.")
        body = text.split(section, 1)[1].split(nxt, 1)[0]
        for line in body.splitlines():
            m = re.match(r"\| \*\*(.+?)\*\*", line)
            if m:
                out.append((m.group(1), origin))
    return out


def verdict(move: str, medium: str) -> tuple[str, str, str]:
    if (move, medium) in RULINGS:
        return RULINGS[(move, medium)]
    heat, room = RATINGS[move]
    _, heat_budget, room_budget = MEDIA[medium]
    if heat > heat_budget:
        return ("banned", "", f"heat {heat} over this medium's budget of {heat_budget}")
    if room > room_budget:
        return ("banned", "", f"needs room {room}; this medium gives {room_budget}")
    return ("licensed", "", "")


def render() -> str:
    roster = roster_from_guide()
    names = [n for n, _ in roster]
    if len(names) != 36:
        raise SystemExit(f"ERROR: read {len(names)} moves from the guide, expected 36.")
    missing = [n for n in names if n not in RATINGS]
    if missing:
        raise SystemExit("ERROR: unrated moves, so unlicensable: " + ", ".join(missing))
    stale = [n for n in RATINGS if n not in names]
    if stale:
        raise SystemExit("ERROR: rated moves that no longer exist in the guide: " + ", ".join(stale))

    L = []
    A = L.append
    A("<!-- GENERATED by build_licensing.py. Do not hand-edit: run the script. -->")
    A("")
    A("# Move licensing matrix")
    A("")
    A("**A shared reference, not a per-contract copy** ([#162](https://github.com/seanwinslow28/code-brain/issues/162)). "
      "Every medium contract inherits this and may **narrow** it. No contract may widen it: a move "
      "banned here is banned there.")
    A("")
    A("The roster is read from `writing-voice-modes/SKILL.md` at generation time, so this file cannot "
      "drift from the guide. An unrated move is an unlicensed move and fails the build.")
    A("")
    A("## What this file does, and does not, do")
    A("")
    A("**Advisory in all nine mediums. Nothing enforces it** "
      "([#222](https://github.com/seanwinslow28/code-brain/issues/222), 2026-09-01). Its reader is "
      "the orchestrator at contract-authoring time: this is the input when a medium contract is "
      "written or rewritten, and the durable record of the 324 rulings so a rewrite cannot quietly "
      "drift. It has no per-run role. It is not loaded into the shaping context, no gate checks a "
      "draft against it, and the GATE RECORD has no line for it \u2014 including in the Professional "
      "lane, where the origin gate already blocks on any untraced claim.")
    A("")
    A("**What would give it teeth.** Two ratified permanent lessons routed to a medium contract "
      "(`contracts/<lane>/<medium>.md`) whose reason is that a move was wrong for the room. One is "
      "noise; two is a pattern, and it reopens the enforcement question as a fresh ticket. The "
      "instrument is the lessons ledger, which already records that route and that reason \u2014 nothing "
      "new is tagged and nothing new is counted. Until then a flag here would be a claim that a "
      "check knows something the author does not, made with zero runs behind it, which is the shape "
      "[#219](https://github.com/seanwinslow28/code-brain/issues/219) retired.")
    A("")
    A("## How a cell is decided")
    A("")
    A("Two axes settle 318 of the 324 cells. Six are ruled directly, on evidence the axes cannot see.")
    A("")
    A("| Axis | What it measures | Scale |")
    A("|---|---|---|")
    A("| **Heat** | How much register the move carries | 0 none (resume-safe) &middot; 1 wit &middot; 2 voice &middot; 3 hot (bodily, profane, insult, grotesque) |")
    A("| **Room** | How much space it needs to land | 1 sentence &middot; 2 beat &middot; 3 runway &middot; 4 whole-piece |")
    A("")
    A("A cell is **banned** if the move's heat exceeds the medium's budget, or if it needs more room "
      "than the form gives. Otherwise it is **licensed**. `C` marks a conditional: licensed only "
      "under the condition stated below the table.")
    A("")
    A("**If a roster looks wrong, check the move's rating before the medium's budget.** The rating is "
      "the load-bearing judgement; the budgets are coarse on purpose.")
    A("")
    A("## Budgets, as ruled")
    A("")
    A("| Medium | Lane | Heat | Room | Licensed |")
    A("|---|---|:--:|:--:|--:|")
    for md, (lane, hb, rb) in MEDIA.items():
        lic = sum(1 for n in names if verdict(n, md)[0] == "licensed")
        A(f"| {md} | {lane} | {hb} | {rb} | {lic} / 36 |")
    A("")
    A("**Resume licenses nothing, and that is the ruling, not a gap.** Heat 0 admits no voice move at "
      "all: every claim traces to the transcript and the phrasing stays conventional. Nobody wants a "
      "resume in dive-bar register.")
    A("")
    A("**Portfolio and LinkedIn share a budget, as do Substack and YouTube / Reels**, so each pair "
      "gets an identical roster. That was visible when the budgets were ruled and left standing. "
      "Where a medium genuinely needs to differ from its twin, the difference belongs in that "
      "medium's contract as a narrowing, not in a new budget here.")
    A("")
    A("## The matrix")
    A("")
    A("`L` licensed &middot; `C` conditional &middot; `-` banned")
    A("")
    head = "| Move | Origin | " + " | ".join(m.replace(" / ", "/") for m in MEDIA) + " |"
    A(head)
    A("|---|---|" + ":--:|" * len(MEDIA))
    for name, origin in roster:
        cells = " | ".join(MARKS[verdict(name, md)[0]] for md in MEDIA)
        heat, room = RATINGS[name]
        A(f"| {name} <sub>h{heat} r{room}</sub> | {origin} | {cells} |")
    A("")
    A("## The ruled cells")
    A("")
    A("Six cells do not follow from the axes. Four were ruled by Sean on 2026-08-26; two carry "
      "forward restrictions already made.")
    A("")
    for (move, medium), (v, cond, why) in RULINGS.items():
        A(f"### {move} &times; {medium} &mdash; **{v}**")
        A("")
        if cond:
            A(f"**Condition.** {cond}")
            A("")
        A(f"{why}")
        A("")
    A("**The pattern in the screenplay-derived cells is worth naming, because it will recur.** When a "
      "move originates in screenplay format, the licensing question is always *is this the move, or "
      "is it the notation?* Shout-Caps and Screenwriting Cut-To were both ruled on that distinction, "
      "in opposite directions: the prose move survives, the format convention carrying it does not. "
      "Rate any future screenplay-derived move against that question first.")
    A("")
    A("## Regenerating")
    A("")
    A("```bash")
    A("python3 build_licensing.py            # rewrite this file from the guide")
    A("python3 build_licensing.py --check    # verify it is current")
    A("```")
    A("")
    A("Changing a rating, a budget, or a ruled cell is a **ruling**, not maintenance. Edit "
      "`build_licensing.py` and say so on the ticket.")
    A("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    text = render()
    if args.check:
        if not OUT.exists():
            print("move-licensing.md is missing", file=sys.stderr)
            return 1
        current = OUT.read_text(encoding="utf-8") == text
        print("matrix is current" if current else "DRIFT: move-licensing.md is stale")
        return 0 if current else 1
    OUT.write_text(text, encoding="utf-8")
    licensed = sum(1 for n in RATINGS for md in MEDIA if verdict(n, md)[0] == "licensed")
    print(f"Wrote {OUT.name}: 324 cells, {licensed} licensed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
