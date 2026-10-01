"""Systemcraft's studio profile — the one file the shared trace kit reads to know this studio.

Written on the Productcraft build map's craftwork build 4 (#327, 2026-10-01), when
Systemcraft adopted the shared law (#282 decision 4): Systemcraft traces from
eng-005 on, and rung-0 line 11 (recorded runtime vs the transcript's model stamp)
is the guard against the alias drift that decision 2 fixed. Earlier engagements
are not retrofitted.

The shape: the five-seat pipeline (bench/README.md) as stages 1-5, the record
kinds a Systemcraft engagement produces (the handoff modifier's intake check
among them), the one closed audit cycle in which the Evals & Evidence Architect's
co-sign *is* the PRD's audit (the dual-touch law), and rung-0 line 8, the check
that a design engagement ran that shape. Its taxonomy file (`taxonomy.md`,
beside this one) is empty until labels earn a Systemcraft seat mode; the shared
process-waste family is the kit's.

The kit finds this file by walking up from an engagement folder, so
`python3 craftwork/trace/check.py systemcraft/ledger/engagements/<eng-id>` needs
no flag. Loading it registers the structure check.

The brief header the kit reads lives in `open-brief.md` (Systemcraft's Open has
always written that file). Its `type` is one of `design`, `audit`,
`role-support`, `employer-work`, `one-off` (the master skill's five types).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT_DIR = HERE.parents[1] / "craftwork" / "trace"
try:
    import tracekit  # noqa: F401
except ModuleNotFoundError:
    sys.path.insert(0, str(KIT_DIR))

from tracekit.checker import STRUCTURE_CHECKS, Check  # noqa: E402
from tracekit.engagement import Engagement  # noqa: E402
from tracekit.studio import Studio  # noqa: E402

__all__ = ["STUDIO", "SYSTEMCRAFT", "SYSTEMCRAFT_CHECK_IMPLICATIONS", "STAGE_SEATS", "FIXED_AUDITORS", "COSIGN_STAGES"]

SYSTEMCRAFT_CHECK_IMPLICATIONS = (
    "A record that will not parse cannot be checked at all, so treat that pass's line on this page as unread.",
    "A pass with no record is work this page cannot show you.",
    "A pass with no row is unfinished review, not a pass.",
    "A hash that no longer matches means the file on disk is not the one the seat read, so a quotation into it may point at different words.",
    "A cited corpus file the transcript never opened means the citation was not read when it was made.",
    "A move that names nothing upstream means the artifact's history does not add up; an unverifiable move is one an overwritten revision took with it.",
    "An unmeasured pass costs the reading nothing; it only means the token figures here are a subtotal.",
    "A lane missing its draft or its audit, or a pass in a lane its seat does not own, is an engagement that did not run its own shape.",
    "A blind pair whose runtime is already visible cannot produce an unbiased verdict.",
    "A failure code outside the taxonomy is free text, and free text does not count toward a mode.",
    "A pass whose transcript names a different model ran on something the registry never ruled, so its row counts toward the wrong runtime.",
)

# the pipeline (bench/README.md): stage → drafting seat
STAGE_SEATS = {
    1: "design-strategist", 2: "architecture-advisor", 3: "interaction-trust-designer",
    4: "evals-evidence-architect", 5: "ops-economics-modeler",
}
# the closed audit cycle (bench/README.md): stage → the seat that audits it
FIXED_AUDITORS = {
    1: "evals-evidence-architect", 2: "ops-economics-modeler", 3: "design-strategist",
    4: "interaction-trust-designer", 5: "architecture-advisor",
}
# the dual-touch law: the PRD's audit is the Evals co-sign, so stage 1's check is a `co-sign`, never an `audit`
COSIGN_STAGES = {1}

DESIGN_TYPES = ("design", "design a new project", "design a new project or operating model")
AUDIT_TYPES = ("audit", "audit / improve", "audit / improve an existing system")

STUDIO = Studio(
    key="systemcraft",
    name="Systemcraft",
    stages={1: "Strategist", 2: "Architecture", 3: "Trust", 4: "Evals", 5: "Ops"},
    kinds=("draft", "audit", "co-sign", "gate", "repair", "trial", "intake", "open", "close"),
    forward_kinds=("draft", "repair", "trial"),
    coordinator_kinds=("open", "close"),
    coordinator_stage=0,
    coordinator_label="open · close",
    gate_seats=("red-team-gate",),
    seat_names={
        "design-strategist": "Strategist", "architecture-advisor": "Architecture",
        "interaction-trust-designer": "Trust", "evals-evidence-architect": "Evals",
        "ops-economics-modeler": "Ops", "coordinator": "Coordinator", "red-team-gate": "Red-team gate",
    },
    repo_prefixes=("systemcraft/", "craftwork/", ".claude/"),
    corpus_path_re=re.compile(r"(?<![\w/])((?:systemcraft/)?corpus/[\w\-./]+?\.md)"),
    id_re=None,
    taxonomy_path=HERE / "taxonomy.md",
    shared_taxonomy=True,
    withheld_required="the drafting conversation",
    brief_file="open-brief.md",
    checks_dir="artifacts",            # Systemcraft files audits, co-signs and gate findings beside the artifacts
    structure_check_name="Each lane has its draft and its audit, and every pass sits in its own seat's lane",
    check_implications=SYSTEMCRAFT_CHECK_IMPLICATIONS,
    review_prompts=(
        ("draft", "Does its work answer the assigned question within the evidence and constraints?"),
        ("audit", "Is the claimed defect supported, consequential, and explained well enough to act on?"),
        ("co-sign", "Can every success criterion become a runnable test, and is each bounce explained?"),
        ("repair", "Does the new version resolve the identified issue without creating a material contradiction?"),
        ("gate", "Are verification, residuals, and decision authority clear?"),
        ("intake", "Can the seat do its job from this packet, and does the state it issued follow from the gaps it named?"),
    ),
    review_prompts_version="v1 · 2026-10-01",
    root_markers=("systemcraft", ".claude"),
)
SYSTEMCRAFT = STUDIO


def _check_kind(stage: int) -> str:
    return "co-sign" if stage in COSIGN_STAGES else "audit"


def _stages(eng: Engagement) -> Check:
    """Systemcraft's structure line.

    A design engagement: per lane reached, exactly one draft by the lane's seat and at least one
    check by its fixed auditor (the Evals co-sign on the PRD, an audit everywhere else). An audit
    engagement: every seat's pass sits in a lane that seat owns or audits, so no invocation crosses
    lanes (CLAUDE.md rule 5); which lanes the target has is the roster's call, so presence is not
    asserted. Any other type: not asserted, said so.
    """
    c = Check(eng.studio.structure_check_name)
    names = eng.studio.stage_name
    etype = str(eng.brief.get("type") or "").lower().strip()
    if not etype:
        c.notes.append(f"{eng.studio.brief_file} names no type; the lane structure is not asserted")
        return c
    stages = sorted({r.stage for r in eng.records if 1 <= r.stage <= 5})
    c.n_total = len(stages)
    if etype in AUDIT_TYPES:
        for s in stages:
            ok = True
            allowed = {STAGE_SEATS[s], FIXED_AUDITORS[s]}
            for r in (r for r in eng.records if r.stage == s and r.seat not in eng.studio.gate_seats):
                if r.seat not in allowed:
                    c.findings.append(f"{r.pass_id}: {r.seat} at stage {s} {names(s)}, a lane it neither owns "
                                      f"nor audits ({STAGE_SEATS[s]} owns it, {FIXED_AUDITORS[s]} audits it)")
                    ok = False
            c.n_ok += 1 if ok else 0
        c.notes.append("audit engagement: lane ownership asserted; which lanes run is the roster's call")
        return c
    if etype not in DESIGN_TYPES:
        c.notes.append(f"engagement type is {etype}: not a design engagement, the lane structure is not asserted")
        return c
    for s in stages:
        ok = True
        rs = [r for r in eng.records if r.stage == s]
        drafts = [r for r in rs if r.kind == "draft"]
        if len(drafts) != 1:
            c.findings.append(f"stage {s} {names(s)}: {len(drafts)} drafts, expected exactly one (repairs are `kind: repair`)")
            ok = False
        elif drafts[0].seat != STAGE_SEATS[s]:
            c.findings.append(f"stage {s}: draft by {drafts[0].seat}; the drafting seat is {STAGE_SEATS[s]}")
            ok = False
        want = _check_kind(s)
        checks = [r for r in rs if r.kind == want]
        if not checks:
            c.findings.append(f"stage {s} {names(s)}: no {want} pass (the fixed auditor is {FIXED_AUDITORS[s]})")
            ok = False
        for r in checks:
            if r.seat != FIXED_AUDITORS[s]:
                c.findings.append(f"stage {s}: {want} by {r.seat}; the fixed auditor is {FIXED_AUDITORS[s]}")
                ok = False
        c.n_ok += 1 if ok else 0
    missing = [s for s in range(1, 6) if s not in stages]
    if missing:
        c.notes.append(f"stages not yet reached: {', '.join(str(s) for s in missing)}")
    return c


STRUCTURE_CHECKS[STUDIO.key] = _stages
