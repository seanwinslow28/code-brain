#!/usr/bin/env python3
"""Build the synthetic deck run the content machine's trace kit is tested on.

Everything here is invented: three posts by handles that do not exist, a
three-card corpus of made-up short lines labelled the way the real corpus
labels its reps (`Rep 2`, `Rep 7e`, `Sample 2`), drafts that answer the
invented posts, gate output with one advisory finding, a pick and a deck
entry. No transcript, corpus line, block or draft from the real machine is in
it, and the builder refuses to write anywhere under the real private brain.

The builder *simulates* the run: it walks the passes in order, hashes each
pass's inputs from the folder as it stands, then writes that pass's outputs,
so the hash chain the checker verifies is real. Records are written last, with
each gate's verdict transcribed onto the shape it gated and the pick's split
onto every card.

Run from this folder:  python3 tests/deck_synth.py <out-dir>
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

RUN_ID = "cm-run-000"
RUN_SLUG = "2026-10-06-x-deck"
SHAPER = "claude-sonnet-5"
AGENT = "Agent tool, fresh context"
SCRIPT = "x/stimulus.py (no model)"
WITHHELD_SHAPE = [
    "the drafting conversation",
    ".claude/skills/content-machine/SKILL.md",
    ".claude/skills/writing-voice-modes/SKILL.md",
    ".claude/skills/content-machine/contracts/",
    ".claude/skills/content-machine/gates/",
    "creative-studio/content-machine/ledger/",
]
CONTEXT = [   # the six slots minus the story, all local to the synthetic folder
    "corpus/01-raw-interviews.md", "corpus/02-reactions-and-rejections.md", "corpus/03-prose-anchors.md",
    "corpus/04-hand-edits-and-reasons.md", "corpus/05-pointer-veins.md", "corpus/06-short-form-and-exercises.md",
    "voice-samples.md", "reference-universe.md", "do-not-promote.md",
]

# --------------------------------------------------------------------------- #
# invented material
# --------------------------------------------------------------------------- #

CARDS = [
    dict(n=1, slug="quillfeather-terminal-changelog", handle="@quillfeather_dev",
         post="Shipped a tool that turns my terminal history into a weekly changelog. It has opinions about my Tuesdays.",
         draft="Mine would have opinions about the four hours I spent naming the thing.\nTuesdays are where the commits go to think about what they did.",
         moves=["- kept — Rep 2 from corpus/06-short-form-and-exercises.md",
                "- added — the Tuesdays turn from stimulus/1-quillfeather-terminal-changelog.md",
                "- dropped — Rep 4 from corpus/06-short-form-and-exercises.md; dunks on the poster"]),
    dict(n=2, slug="maplecore-show-the-failed-run", handle="@maplecore_lab",
         post="Hot take: every agent demo should show the run that failed, not the one that worked.",
         draft="Every agent demo should show the failed run. The failed run is the demo.\nThe one that worked is the trailer; the one that failed is the film.",
         moves=["- kept — Sample 2 from voice-samples.md",
                "- merged — Rep 1 + Rep 3 → the closing line from corpus/06-short-form-and-exercises.md"]),
    dict(n=3, slug="orrery-forty-lines", handle="@orrery_notes",
         post="Wrote 40 lines of Python to stop writing 400 words of email. Net words saved: negative, I wrote this post.",
         draft="Forty lines to dodge four hundred words is still the best trade on the board.\nThe post is the invoice.",
         moves=["- kept — Rep 7e from corpus/06-short-form-and-exercises.md",
                "- added — the negative-net turn from stimulus/3-orrery-forty-lines.md"]),
]

CORPUS = {
    "corpus/01-raw-interviews.md": "# 01 — raw interviews (synthetic)\n\nInvented interview answers for the trace-kit tests. Not the author's words.\n",
    "corpus/02-reactions-and-rejections.md": "# 02 — reactions and rejections (synthetic)\n\nInvented. One rejected line: the joke that explained itself.\n",
    "corpus/03-prose-anchors.md": "# 03 — prose anchors (synthetic)\n\nInvented anchors. A paragraph that starts mid-action and never looks back.\n",
    "corpus/04-hand-edits-and-reasons.md": "# 04 — hand edits and reasons (synthetic)\n\nInvented. Cut the adverb; the verb was already doing it.\n",
    "corpus/05-pointer-veins.md": "# 05 — pointer veins (synthetic)\n\nInvented. Where the short lines point: at the tool, never at the person.\n",
    "corpus/06-short-form-and-exercises.md": (
        "# 06 — short form and exercises (synthetic)\n\n"
        "### Rep 1 — the trailer line\n\nThe one that worked is the trailer.\n\n"
        "### Rep 2 — the naming hours\n\nFour hours naming the thing, four minutes writing it.\n\n"
        "### Rep 3 — the film line\n\nThe one that failed is the film.\n\n"
        "### Rep 4 — the dunk (withdrawn shape)\n\nCongratulations on automating a thing nobody asked for.\n\n"
        "### Rep 7 — the best trade\n\nStill the best trade on the board.\n\n"
        "### Rep 7e — the invoice\n\nThe post is the invoice.\n"
    ),
    "voice-samples.md": (
        "# voice-samples (synthetic)\n\n"
        "### Sample 1\n\nA sample that opens mid-action.\n\n"
        "### Sample 2\n\nA sample that repeats the claim as the punchline. The failed run is the demo.\n\n"
        "### Sample 3\n\nA sample with the funniest word last.\n"
    ),
    "reference-universe.md": "# reference universe (synthetic)\n\nInvented anchors only: a film, a board game, a bus route.\n",
    "do-not-promote.md": "# do not promote (synthetic)\n\n- nothing about anyone's employer\n",
}


def block(card: dict) -> str:
    return (
        "STIMULUS BLOCK\n"
        f"Slug: {card['slug']}\nSurface: reply\nPosted by: {card['handle']} (invented)\n"
        f"Fetched: 2026-10-06T08:02:00-04:00 via publish.x.com/oembed (simulated)\n\n"
        f"POST (verbatim)\n{card['post']}\n"
    )


def card_text(card: dict) -> str:
    return (
        f"# Card {card['n']} — {card['slug']}\n\n"
        f"Answering: {card['handle']} (invented) · surface: reply\n\n"
        "## Draft\n\n"
        f"{card['draft']}\n\n"
        "## Origin ledger\n\n"
        "Traced: 2 vivid phrases, each to a rep in the clean context\n"
        "Untraced: none\n"
        "ASK LIST: none\n"
        "Verdict: clean\n\n"
        "## Moves\n\n"
        + "\n".join(card["moves"]) + "\n"
    )


def gate_text(kind: str, card: dict, rows: list[tuple[str, str, str]]) -> str:
    head = {"origin": "ORIGIN CHECK (inverted — X reactive route) — lane: expressive",
            "coined": "COINED-LINES SWEEP — lane: expressive"}[kind]
    table = "| finding | severity | disposition |\n|---|---|---|\n" + "".join(
        f"| {f} | {s} | {d} |\n" for f, s, d in rows)
    verdict = "clean" if not rows else f"{len(rows)} advisory"
    return f"# Gate — {kind} — card {card['n']}\n\n{head}\n\nverdict: {verdict}\n\n{table}"


POOL = "# Pool — 2026-10-06 (synthetic)\n\nNine invented candidates across three lanes; the three below ranked into the deck.\n"
DECK = "# Deck — 2026-10-06 (synthetic)\n\n" + "".join(f"{c['n']}. {c['handle']} — {c['post'][:40]}…\n" for c in CARDS)
PICKS = ("# Picks — 2026-10-06-x-deck (synthetic)\n\nPicked: 1, 3\nCut: 2\n\n"
         "Reason (verbatim, invented): the cut one restated the post twice before it said anything.\n")
LESSONS = ("# lessons (synthetic ledger)\n\n"
           "## D-2026-10-06-01\n\nDeck:           2026-10-06-x-deck\nPicked:         1, 3\nCut:            2\n"
           "Reason:         the cut one restated the post twice before it said anything.\n")
RUN_MD = f"""---
id: {RUN_ID}
name: Synthetic deck — three invented posts
type: deck
lane: Expressive
medium: x
route: 1
opened: 2026-10-06
closed: 2026-10-06
synthetic: true
---

# {RUN_SLUG}

An invented X route-1 deck of three cards, built by `tests/deck_synth.py` for the trace kit's tests.
No real post, transcript, corpus line or draft is in it.
"""
NOTES = ("- 2026-10-06 08:00 Synthetic run built by tests/deck_synth.py; nothing here is real.\n"
         "- 2026-10-06 08:40 Card 2's shape labeled fail at stage 3: it restated the post twice.\n"
         "- 2026-10-06 08:55 Origin gate flagged one advisory 2-gram on card 2; left in, it is a quote of the frame.\n")

# --------------------------------------------------------------------------- #
# the passes, in launch order
# --------------------------------------------------------------------------- #


def P(seat, kind, stage, runtime, launch, minutes, meter, meter_source, inputs, writes, corpus_read,
      withheld, launched, notes="", effort="—", checks=()):
    return dict(seat=seat, kind=kind, stage=stage, runtime=runtime, launch=launch, minutes=minutes,
                meter=meter, meter_source=meter_source, inputs=inputs, writes=writes, corpus_read=corpus_read,
                withheld=withheld, launched=launched, notes=notes, effort=effort, checks=list(checks))


def passes() -> list[dict]:
    out = []
    out.append(P("x-sweep", "sweep", 0, SCRIPT, "python3 .claude/skills/content-machine/x/stimulus.py deck --days 3 --size 3",
                 2, None, "UNMEASURED", [], {"pool.md": POOL, "deck.md": DECK}, [], ["nothing: a script, no context"],
                 "08:00", notes="pool of nine narrowed to three; no two from one account"))
    for c in CARDS:
        out.append(P("stimulus", "stimulus", 2, SCRIPT,
                     f"python3 .claude/skills/content-machine/x/stimulus.py block <status-url> --slug {c['slug']} --surface reply",
                     1, None, "UNMEASURED", ["deck.md"], {f"stimulus/{c['n']}-{c['slug']}.md": block(c)}, [],
                     ["nothing of the author's: the block is someone else's post"], "08:02"))
    for c in CARDS:
        story = f"stimulus/{c['n']}-{c['slug']}.md"
        inputs = [story] + CONTEXT
        out.append(P("shaper", "shape", 3, SHAPER, AGENT, 4, {"total": 41200 + c["n"] * 300}, "Agent-tool usage",
                     inputs, {f"{c['n']}-{c['slug']}.md": card_text(c)}, inputs, WITHHELD_SHAPE, "08:10",
                     notes="clean context: the block labelled as the thing being answered, the substance rule, the X form, the stance sentence",
                     effort="high"))
    for c in CARDS:
        card = f"{c['n']}-{c['slug']}.md"
        story = f"stimulus/{c['n']}-{c['slug']}.md"
        rows = [("“net words” echoes the post — a 2-gram, advisory", "NOTE", "noted — it quotes the frame")] if c["n"] == 2 else []
        out.append(P("origin-gate", "gate", 4, "gates/origin_check.py (no model)",
                     f"python3 .claude/skills/content-machine/gates/origin_check.py {card} --stimulus {story} --lane expressive",
                     1, None, "UNMEASURED", [card, story], {f"gates/{c['n']}-origin.md": gate_text("origin", c, rows)},
                     [card, story], ["nothing: a script, no context"], "08:30"))
        out.append(P("coined-lines-gate", "gate", 4, "gates/coined_lines.py (no model)",
                     f"python3 .claude/skills/content-machine/gates/coined_lines.py {card} --stimulus {story} --lane expressive",
                     1, None, "UNMEASURED", [card, story], {f"gates/{c['n']}-coined.md": gate_text("coined", c, [])},
                     [card, story], ["nothing: a script, no context"], "08:32"))
    cards = [f"{c['n']}-{c['slug']}.md" for c in CARDS]
    out.append(P("sean", "pick", 5, "Sean", "chat, after the HTML pick console", 6, None, "UNMEASURED",
                 cards + [f"stimulus/{c['n']}-{c['slug']}.md" for c in CARDS], {"picks.md": PICKS}, [],
                 ["the drafting conversations of every shape", "the gate output (he reads drafts, not gates)"], "08:45",
                 notes="picked 1 and 3; cut 2; the one question answered"))
    out.append(P("orchestrator", "lesson", 6, "the orchestrating session", "in-session, deck close", 2, None, "UNMEASURED",
                 ["picks.md"] + cards, {"ledger/lessons.md": LESSONS}, [], ["nothing further"], "08:52",
                 notes="deck entry written; no routing (a deck entry files or banks, never routes)"))
    return out


# --------------------------------------------------------------------------- #
# writing
# --------------------------------------------------------------------------- #


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def record_text(pid: str, spec: dict, inputs: list[tuple[str, str]], outputs: list[tuple[str, str]]) -> str:
    hh, mm = map(int, spec["launched"].split(":"))
    end = hh * 60 + mm + spec["minutes"]
    lines = ["---", f"pass: {pid}", f"seat: {spec['seat']}", f"kind: {spec['kind']}", f"stage: {spec['stage']}",
             f"runtime: {spec['runtime']}", f'launch: "{spec["launch"]}"', f"effort: {spec['effort']}",
             f"launched: 2026-10-06T{hh:02d}:{mm:02d}:00-04:00", f"completed: 2026-10-06T{end // 60:02d}:{end % 60:02d}:00-04:00",
             f"wall_clock_s: {spec['minutes'] * 60}"]
    if spec["meter"] is None:
        lines.append("meter: null")
    else:
        lines.append("meter:")
        lines += [f"  {k}: {v}" for k, v in spec["meter"].items()]
    lines.append(f"meter_source: {spec['meter_source']}")
    if inputs:
        lines.append("inputs:")
        for path, h in inputs:
            lines += [f"  - path: {path}", f"    sha256: {h}"]
    else:
        lines.append("inputs: []")
    lines.append("withheld:")
    lines += [f"  - {w}" for w in spec["withheld"]]
    lines.append("outputs:")
    for path, h in outputs:
        lines += [f"  - path: {path}", f"    sha256: {h}"]
    lines.append(f"raw_log: {'—' if spec['seat'] in ('sean',) else f'trace/logs/{pid}.jsonl'}")
    if spec["checks"]:
        lines.append("checks:")
        for cp, ck, cv in spec["checks"]:
            lines += [f"  - pass: {cp}", f"    kind: {ck}", f"    verdict: {cv}"]
    else:
        lines.append("checks: []")
    lines += ["triggered_by: null", "shadow_of: null", "---", "", "## Corpus read", ""]
    lines += [f"- {c}" for c in spec["corpus_read"]] or ["none"]
    lines += ["", "## Moves", ""]
    art = next((p for p, _ in outputs), None)
    lines.append(f"{art} § Moves" if spec["kind"] == "shape" else "none — this kind hands no artifact forward")
    lines += ["", "## Notes", "", spec["notes"] or "none", ""]
    return "\n".join(lines)


def labels_text(pids: list[str], specs: list[dict]) -> str:
    rows = []
    for pid, s in zip(pids, specs):
        if s["kind"] == "shape" and "maplecore" in next(iter(s["writes"])):
            rows.append(f"| {pid} | fail | 3 | Two of three sentences restate the post; the one that is his is the second. Lead with it. | |")
        elif s["kind"] == "lesson":
            rows.append(f"| {pid} | | | | |")
        else:
            rows.append(f"| {pid} | pass | | | |")
    return (f"---\nrun: {RUN_SLUG}\nlabeler: Sean (synthetic)\n---\n\n# Labels — {RUN_ID}\n\n"
            "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")


def _refuse_private(out: Path) -> None:
    s = str(out.resolve())
    if "/creative-studio/content-machine/" in s or "/ledger/" in s or "/transcripts/" in s:
        raise SystemExit(f"refusing to write a synthetic run under a private path: {out}")


def build(out: Path) -> Path:
    out = Path(out)
    _refuse_private(out)
    (out / "trace" / "logs").mkdir(parents=True, exist_ok=True)
    for sub in ("stimulus", "corpus", "gates", "ledger"):
        (out / sub).mkdir(exist_ok=True)
    (out / "run.md").write_text(RUN_MD, encoding="utf-8")
    for rel, text in CORPUS.items():
        (out / rel).write_text(text, encoding="utf-8")
    specs = passes()
    pids = [f"pass-{i:02d}" for i in range(1, len(specs) + 1)]
    hashed_inputs: list[list[tuple[str, str]]] = []
    hashed_outputs: list[list[tuple[str, str]]] = []
    for pid, spec in zip(pids, specs):
        hashed_inputs.append([(rel, sha(out / rel)) for rel in spec["inputs"]])
        outs = []
        for rel, text in spec["writes"].items():
            (out / rel).parent.mkdir(parents=True, exist_ok=True)
            (out / rel).write_text(text, encoding="utf-8")
            outs.append((rel, sha(out / rel)))
        hashed_outputs.append(outs)
        if spec["seat"] != "sean":
            (out / "trace" / "logs" / f"{pid}.jsonl").write_text(
                '{"synthetic": true, "note": "placeholder transcript; the record indexes it"}\n', encoding="utf-8")
    # transcribe: each gate onto the shape it gated; the pick's split onto every shape
    by_output = {rel: i for i, outs in enumerate(hashed_outputs) for rel, _ in outs}
    for i, spec in enumerate(specs):
        if spec["kind"] == "gate":
            card = spec["inputs"][0]
            verdict = next(l.split(":", 1)[1].strip() for l in next(iter(spec["writes"].values())).split("\n") if l.startswith("verdict:"))
            specs[by_output[card]]["checks"].append((pids[i], "gate", f"{spec['seat']}: {verdict}"))
        if spec["kind"] == "pick":
            for card in spec["inputs"]:
                if card in by_output and specs[by_output[card]]["kind"] == "shape":
                    picked = card.split("-")[0] in ("1", "3")
                    specs[by_output[card]]["checks"].append((pids[i], "pick", "picked" if picked else "cut"))
    for pid, spec, ins, outs in zip(pids, specs, hashed_inputs, hashed_outputs):
        (out / "trace" / f"{pid}-{spec['seat']}-{spec['kind']}.md").write_text(record_text(pid, spec, ins, outs), encoding="utf-8")
    (out / "trace" / "labels.md").write_text(labels_text(pids, specs), encoding="utf-8")
    (out / "trace" / "notes.md").write_text(NOTES, encoding="utf-8")
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(build(Path(sys.argv[1])))
