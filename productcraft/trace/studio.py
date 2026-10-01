"""Productcraft's studio profile — the one file the shared trace kit reads to know this studio.

The kit lives at `craftwork/trace/` (moved from here on #325, kit 0.9.0) and reads
every studio's shape from a profile beside the studio, never from itself. This is
Productcraft's: the seven-stage train (#266, #273), the record kinds (#290, #297),
the two closed audit cycles, the co-signs at stages 2 and 6, and rung-0 line 8,
the check that the full train ran its own shape. Its taxonomy file
(`taxonomy.md`, beside this one) holds the seat failure modes ratified on #299;
the shared process-waste family is the kit's.

The kit finds this file by walking up from an engagement folder, so
`python3 craftwork/trace/check.py productcraft/ledger/engagements/<eng-id>` needs
no flag. Loading it registers the structure check.
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

__all__ = ["STUDIO", "PRODUCTCRAFT", "PRODUCTCRAFT_CHECK_IMPLICATIONS", "STAGE_SEATS", "FIXED_AUDITORS", "REQUIRED_COSIGNS"]

PRODUCTCRAFT_CHECK_IMPLICATIONS = (
    "A record that will not parse cannot be checked at all, so treat that pass's line on this page as unread.",
    "A pass with no record is work this page cannot show you.",
    "A pass with no row is unfinished review, not a pass.",
    "A hash that no longer matches means the file on disk is not the one the seat read, so a quotation into it may point at different words.",
    "A cited corpus file the transcript never opened means the citation was not read when it was made.",
    "A move that names nothing upstream means the artifact's history does not add up; an unverifiable move is one an overwritten revision took with it.",
    "An unmeasured pass costs the reading nothing; it only means the token figures here are a subtotal.",
    "A stage missing its draft, its audit or its co-sign is a train that did not run its own shape.",
    "A blind pair whose runtime is already visible cannot produce an unbiased verdict.",
    "A failure code outside the taxonomy is free text, and free text does not count toward a mode.",
    "A pass whose transcript names a different model ran on something the registry never ruled, so its row counts toward the wrong runtime.",
)

# the fixed train (#266, #273): stage → drafting seat
STAGE_SEATS = {
    1: "product-strategist", 2: "discovery-lead", 3: "insights-analytics", 4: "growth-distribution",
    5: "business-economics", 6: "delivery-execution", 7: "product-leadership",
}
# the two closed audit cycles (artifact-header.md): stage → the seat that audits it
FIXED_AUDITORS = {
    1: "discovery-lead", 2: "product-leadership", 3: "delivery-execution", 4: "insights-analytics",
    5: "growth-distribution", 6: "business-economics", 7: "product-strategist",
}
# the co-sign touches that produce a pass (#266): stage → co-signing seat
REQUIRED_COSIGNS = {2: "insights-analytics", 6: "product-strategist"}

STUDIO = Studio(
    key="productcraft",
    name="Productcraft",
    stages={1: "Strategist", 2: "Discovery", 3: "Insights", 4: "Growth", 5: "Business", 6: "Delivery", 7: "Leadership"},
    kinds=("draft", "audit", "co-sign", "gate", "repair", "trial", "open", "readout", "close"),
    forward_kinds=("draft", "repair", "trial"),
    coordinator_kinds=("open", "readout", "close"),
    coordinator_stage=0,
    coordinator_label="close",
    gate_seats=("red-team-gate",),
    seat_names={
        "product-strategist": "Strategist", "discovery-lead": "Discovery", "insights-analytics": "Insights",
        "growth-distribution": "Growth", "business-economics": "Business", "delivery-execution": "Delivery",
        "product-leadership": "Leadership", "coordinator": "Coordinator", "red-team-gate": "Red-team gate",
    },
    repo_prefixes=("productcraft/", "systemcraft/", "craftwork/", ".claude/"),
    corpus_path_re=re.compile(r"(?<![\w/])((?:productcraft/|systemcraft/)?corpus/[\w\-./]+?\.md)"),
    id_re=None,
    taxonomy_path=HERE / "taxonomy.md",
    shared_taxonomy=True,
    withheld_required="the drafting conversation",
    brief_file="brief.md",
    checks_dir="audits",
    structure_check_name="Each drafting stage has one draft, an audit, and its required co-signs",
    check_implications=PRODUCTCRAFT_CHECK_IMPLICATIONS,
    review_prompts=(
        ("draft", "Does its work answer the assigned question within the evidence and constraints?"),
        ("audit", "Is the claimed defect supported, consequential, and explained well enough to act on?"),
        ("repair", "Does the new version resolve the identified issue without creating a material contradiction?"),
        ("gate", "Are verification, residuals, and decision authority clear?"),
    ),
    review_prompts_version="v1 · 2026-09-20",
    root_markers=("productcraft", ".claude"),
)
PRODUCTCRAFT = STUDIO


def _stages(eng: Engagement) -> Check:
    """Productcraft's structure line: the fixed train's draft / audit / co-sign shape per stage."""
    c = Check(eng.studio.structure_check_name)
    names = eng.studio.stage_name
    etype = str(eng.brief.get("type") or "").lower()
    if etype and etype not in ("full-train", "full train"):
        c.notes.append(f"engagement type is {etype}: not a full train, the stage structure is not asserted")
        return c
    if not etype:
        c.notes.append("brief.md names no type; asserting the full-train structure")
    stages = sorted({r.stage for r in eng.records if 1 <= r.stage <= 7})
    c.n_total = len(stages)
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
        audits = [r for r in rs if r.kind == "audit"]
        if not audits:
            c.findings.append(f"stage {s} {names(s)}: no audit pass (the fixed auditor is {FIXED_AUDITORS[s]})")
            ok = False
        for a in audits:
            if a.seat != FIXED_AUDITORS[s]:
                c.findings.append(f"stage {s}: audit by {a.seat}; the fixed auditor is {FIXED_AUDITORS[s]}")
                ok = False
        if s in REQUIRED_COSIGNS:
            cosigns = [r for r in rs if r.kind == "co-sign"]
            if not cosigns:
                c.findings.append(f"stage {s}: no co-sign pass (required from {REQUIRED_COSIGNS[s]})")
                ok = False
            for cs in cosigns:
                if cs.seat != REQUIRED_COSIGNS[s]:
                    c.findings.append(f"stage {s}: co-sign by {cs.seat}; the co-signing seat is {REQUIRED_COSIGNS[s]}")
                    ok = False
        c.n_ok += 1 if ok else 0
    missing = [s for s in range(1, 8) if s not in stages]
    if missing:
        c.notes.append(f"stages not yet reached: {', '.join(str(s) for s in missing)}")
    return c


STRUCTURE_CHECKS[STUDIO.key] = _stages
