"""The content machine's studio profile for the shared trace kit (#291, designed on #261 / #272).

The kit lives at `productcraft/trace/` (the first copy, #290); this module is the
one thing the machine writes for itself — its stages, kinds, seats, the shape of a
rep id in a `## Moves` line, and rung-0 line 8: *each shape ran in the clean
context, was gated, and reached the pick*. Everything else — the record grammar,
the hash chain, the labels file, the viewer — is imported, never copied.

Importing this module is the whole setup: it puts `productcraft/trace/` on
`sys.path` when `tracekit` is not already importable, builds the profile, and
registers the structure check. `check.py` and `render.py` beside it are the two
Close-ritual commands; `tests/deck_synth.py` builds the invented run they are tested on.
Nothing here reads the private brain; the scripts read a run folder at run time.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]                       # trace → content-machine → skills → .claude → repo
KIT_DIR = REPO / "productcraft" / "trace"


def bootstrap() -> Path:
    """Make `tracekit` importable from the first copy's folder. Idempotent."""
    try:
        import tracekit  # noqa: F401
    except ModuleNotFoundError:
        if not (KIT_DIR / "tracekit").is_dir():
            raise SystemExit(
                f"the shared trace kit is not at {KIT_DIR} — the content machine imports it from "
                f"productcraft/trace/ rather than carrying a copy (#291)"
            )
        sys.path.insert(0, str(KIT_DIR))
    return KIT_DIR


bootstrap()

from tracekit.checker import STRUCTURE_CHECKS, Check  # noqa: E402
from tracekit.engagement import Engagement, Record  # noqa: E402
from tracekit.studio import Studio  # noqa: E402

__all__ = ["CONTENT_MACHINE", "BANNED_FROM_SHAPING", "STORY_SLOTS", "shapes_check", "bootstrap", "KIT_DIR", "REPO"]

# --------------------------------------------------------------------------- #
# the machine's vocabulary
# --------------------------------------------------------------------------- #

# SKILL.md § Stages, the machine's own numbering — stage 0 is a real stage here, not a coordinator column
STAGES = {0: "Oracle", 1: "Topic", 2: "Interview", 3: "Shape", 4: "Gates", 5: "Ship", 6: "Lessons"}

# what an invocation was — the filename is pass-NN-<seat>-<kind>.md
KINDS = (
    "sweep",       # 0 · the Oracle run, or X route 1's sweep: a pool and a ranked deck
    "pick",        # 0 · Sean picks a card from an Oracle deck · 5 · Sean picks from a draft deck
    "topic",       # 1 · the TOPIC CARD and the value gate
    "stimulus",    # 2 · x/stimulus.py writes a block (X's stage 2 is not an interview)
    "interview",   # 2 · one lens, one question at a time; the transcript is the output
    "shape",       # 3 · the clean-context draft — the one kind that owns a `## Moves` section
    "gate",        # 4 · one record per gate that ran: origin, coined-lines, humanity, critique, analyzer
    "rewrite",     # 5 · his hand-rewrite (mandatory; the final is corpus)
    "proofread",   # 5 · the mechanical proofread on his final
    "lesson",      # 6 · the lessons-loop entry (a deck entry, or a routed lesson)
)
FORWARD_KINDS = ("shape",)
# every kind but the shaper's has no drafting conversation to withhold — the interview's conversation
# *is* its output, a gate is a script, a pick is Sean
COORDINATOR_KINDS = tuple(k for k in KINDS if k != "shape")

GATE_SEATS = ("value-gate", "origin-gate", "coined-lines-gate", "humanity-gate", "critique-gate", "analyzer")
SEAT_NAMES = {
    "oracle": "Oracle", "x-sweep": "X sweep", "sean": "Sean", "orchestrator": "Orchestrator",
    "stimulus": "Stimulus", "interviewer": "Interviewer", "shaper": "Shaper", "proofread": "Proofread",
    "value-gate": "Value gate", "origin-gate": "Origin gate", "coined-lines-gate": "Coined-lines gate",
    "humanity-gate": "Humanity gate", "critique-gate": "Critique gate", "analyzer": "Analyzer",
}

# SKILL.md § The shaping context — banned from the clean context. An input path that starts with one
# of these is a finding on line 8: the shaper was handed a rulebook.
BANNED_FROM_SHAPING = (
    ".claude/skills/content-machine/SKILL.md",
    ".claude/skills/writing-voice-modes/SKILL.md",
    ".claude/skills/content-machine/contracts/",
    ".claude/skills/content-machine/gates/",
    ".claude/skills/content-machine/lessons/",
    ".claude/skills/content-machine/interview/",
    "creative-studio/content-machine/ledger/",
    "creative-studio/content-machine/cheese-bank/",
)
# slot 1 of the shaping context: the story. A transcript, or (X's reactive route) a stimulus block.
STORY_SLOTS = ("transcripts/", "stimulus/", "applications/", "transcript")

# item ids a `## Moves` line may name — the corpus labels its short-form reps `Rep 7`, `Rep 7e`;
# voice-samples.md labels its worked samples `Sample 3`. Whole-token match, so `Rep 7` never
# satisfies a line that named `Rep 7e`.
REP_ID = re.compile(r"\b(?:Rep|Sample|Exercise|Anchor|Vein)\s+\d+[a-z]?\b")

CHECK_IMPLICATIONS = (
    "A record that will not parse cannot be checked at all, so treat that pass's line on this page as unread.",
    "A stage invocation with no record is work this page cannot show you.",
    "A pass with no row is unfinished review, not a pass.",
    "A hash that no longer matches means the file on disk is not the one the shaper or the gate read.",
    "The machine's drafts cite no corpus file by path; what the shaper leaned on is checked under Moves.",
    "A move naming a rep that was not in the clean context is a claim the record cannot back; the draft may have written from memory.",
    "An unmeasured pass costs the reading nothing; it only means the token figures here are a subtotal.",
    "A shape that saw a banned file, ran ungated, or never reached a pick did not run the machine's own shape.",
    "A blind pair whose runtime is already visible cannot produce an unbiased verdict.",
    "A failure code outside the taxonomy is free text, and free text does not count toward a mode.",
)

REVIEW_PROMPTS = (
    ("stimulus", "Is the block the verbatim post, labelled as the thing being answered, with nothing of his in it?"),
    ("shape", "Is every fact, number, name and event in the draft his — from the transcript or the block — and is the texture a reader would take for his?"),
    ("gate", "Did the gate report what it found without rewriting, and is the finding one he can act on?"),
    ("pick", "Does the pick agree with, extend or answer the post, and would he ship it as it stands?"),
)

CONTENT_MACHINE = Studio(
    key="content-machine",
    name="Content Machine",
    stages=STAGES,
    kinds=KINDS,
    forward_kinds=FORWARD_KINDS,
    coordinator_kinds=COORDINATOR_KINDS,
    coordinator_stage=None,
    gate_seats=GATE_SEATS,
    seat_names=SEAT_NAMES,
    repo_prefixes=("creative-studio/", ".claude/", "vault/"),
    corpus_path_re=None,
    id_re=REP_ID,
    taxonomy_path=HERE / "taxonomy.md",
    withheld_required="the drafting conversation",
    brief_file="run.md",
    checks_dir="gates",
    structure_check_name="Each shape ran in the clean context, was gated, and reached the pick",
    check_implications=CHECK_IMPLICATIONS,
    review_prompts=REVIEW_PROMPTS,
    review_prompts_version="v1 · 2026-09-22",
    root_markers=(".claude",),
)


# --------------------------------------------------------------------------- #
# rung-0 line 8, the machine's own
# --------------------------------------------------------------------------- #


def _is_story(path: str) -> bool:
    return any(s in path for s in STORY_SLOTS)


def shapes_check(eng: Engagement) -> Check:
    """Each shape ran in the clean context, was gated, and reached the pick.

    Per `shape` record: (a) no input starts with a banned path, and slot 1 — a
    transcript or a stimulus block — is among the inputs (a shape with no story
    wrote from nothing, which is the constitution's own failure); (b) every input
    the record lists is in its `## Corpus read`, so nothing was handed and never
    opened; (c) at least one `gate` record fired on the draft at the hash the
    shaper returned, and each such gate is transcribed onto the shape's `checks`;
    (d) a stage-5 `pick` or `rewrite` record took the draft as an input — while
    the run is still open (`closed: null` in run.md) a missing pick is a note.
    The story input is expected to be the output of a stage-2 pass in this run;
    when it is not, that is a note (re-used material), never a finding.
    """
    c = Check(CONTENT_MACHINE.structure_check_name)
    shapes = [r for r in eng.records if r.kind == "shape"]
    if not shapes:
        c.notes.append("no shape record yet: nothing to assert on this line")
        return c
    closed = eng.brief.get("closed") not in (None, "", "null")
    gates = [r for r in eng.records if r.kind == "gate"]
    picks = [r for r in eng.records if r.kind in ("pick", "rewrite") and r.stage == 5]
    stage2_outputs = {o.path for r in eng.records if r.kind in ("stimulus", "interview") for o in r.artifact_outputs}
    unpicked: list[str] = []
    reused: list[str] = []
    c.n_total = len(shapes)
    for s in shapes:
        ok = True
        paths = [i.path for i in s.inputs]
        for p in paths:
            if p.startswith(BANNED_FROM_SHAPING):
                c.findings.append(f"{s.pass_id}: {p} was in the shaping context; it is banned from it (SKILL.md § The shaping context)")
                ok = False
        story = [p for p in paths if _is_story(p)]
        if not story:
            c.findings.append(f"{s.pass_id}: no transcript or stimulus block among its inputs — a shape with no story writes from nothing")
            ok = False
        elif not any(p in stage2_outputs for p in story):
            reused.append(s.pass_id)
        opened = set(s.corpus_read)
        unopened = [p for p in paths if p not in opened]
        if unopened and s.corpus_read:
            c.findings.append(f"{s.pass_id}: handed but never opened (not in `## Corpus read`): {', '.join(unopened)}")
            ok = False
        elif not s.corpus_read:
            c.findings.append(f"{s.pass_id}: `## Corpus read` is empty; the record cannot show the shaper opened its context")
            ok = False
        drafts = s.artifact_outputs
        if not drafts:
            c.findings.append(f"{s.pass_id}: no output draft recorded")
            c.n_ok += 0
            continue
        draft = drafts[0]
        fired = [g for g in gates if any(i.path == draft.path and i.sha256 == draft.sha256 for i in g.inputs)]
        if not fired:
            c.findings.append(f"{s.pass_id}: no gate record fired on {draft.path} at the hash the shaper returned")
            ok = False
        transcribed = {ch.pass_id for ch in s.checks if ch.kind == "gate"}
        for g in fired:
            if g.pass_id not in transcribed:
                c.findings.append(f"{s.pass_id}: {g.pass_id} ({g.seat}) gated its draft but is not in its `checks`")
                ok = False
        took = [p for p in picks if any(i.path == draft.path for i in p.inputs)]
        if not took:
            if closed:
                c.findings.append(f"{s.pass_id}: the run is closed and no stage-5 pick or rewrite took {draft.path}")
                ok = False
            else:
                unpicked.append(s.pass_id)
        c.n_ok += 1 if ok else 0
    if unpicked:
        c.notes.append(f"run still open: {len(unpicked)} shape(s) not yet picked: {', '.join(unpicked)}")
    if reused:
        c.notes.append(
            f"{len(reused)} shape(s) took a transcript or block no stage-2 pass in this run wrote "
            f"(re-used material): {', '.join(reused)}"
        )
    return c


STRUCTURE_CHECKS[CONTENT_MACHINE.key] = shapes_check
