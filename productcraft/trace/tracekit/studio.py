"""A studio profile — the one place a studio's shape is written down (kit 0.6.0, #291).

The kit was built for Productcraft's fixed seven-stage train (#290). The content
machine shares the code rather than forking it (#272 decision 8), and the two
studios differ in exactly the things this object holds: the numbered stages a
record's `stage` may take, the kinds an invocation can be, which kinds hand an
artifact forward and so own a `## Moves` section, which seats are gates, which
path prefixes resolve against the repo, how item ids look in a Moves line, where
the studio's taxonomy file is, and one structure check of its own (rung-0 line 8).

Everything else — the record grammar, the hash chain, the labels file, the Moves
parser, the meter vocabulary, the viewer — is studio-agnostic and reads its
studio from the engagement it was handed. `PRODUCTCRAFT` is the default profile,
so every existing call keeps its meaning; the machine's profile lives beside the
machine (`.claude/skills/content-machine/trace/machine.py`), because a studio
owns its own stage list.

A structure check is registered by key rather than held on the profile, so the
profile module imports nothing from the checker and the checker can import the
profile: `tracekit.checker.STRUCTURE_CHECKS[studio.key] = fn`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

__all__ = ["Studio", "PRODUCTCRAFT", "PRODUCTCRAFT_CHECK_IMPLICATIONS"]

_KIT_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Studio:
    key: str                                   # short id; the structure-check registry key
    name: str                                  # shown in the viewer footer
    stages: dict[int, str]                     # stage number → name, in train order
    kinds: tuple[str, ...]                     # every value `kind:` may take
    forward_kinds: tuple[str, ...]             # kinds that hand an artifact forward and own `## Moves`
    coordinator_kinds: tuple[str, ...] = ()    # kinds with no drafting conversation to withhold
    coordinator_stage: Optional[int] = None    # a stage number reserved for the coordinator's own passes; drawn last
    coordinator_label: str = "close"           # how that column is labelled
    gate_seats: tuple[str, ...] = ()           # seats drawn as "gate" in the train
    seat_names: dict[str, str] = field(default_factory=dict)
    repo_prefixes: tuple[str, ...] = ()        # input paths with these prefixes resolve against the repo root
    corpus_path_re: Optional[re.Pattern] = None   # how an artifact cites a corpus file; None = the studio's artifacts cite none
    id_re: Optional[re.Pattern] = None         # item ids in a Moves line; None = the kit's `O2` / `KR-1a` default
    taxonomy_path: Optional[Path] = None       # the studio's tracked taxonomy.md
    withheld_required: Optional[str] = "the drafting conversation"
    brief_file: str = "brief.md"               # the header file at the engagement root
    checks_dir: str = "audits"                 # where check records (audits, gate findings) sit
    structure_check_name: str = "Stage structure"
    check_implications: tuple[str, ...] = ()   # one sentence per rung-0 line, in check order
    review_prompts: tuple[tuple[str, str], ...] = ()
    review_prompts_version: str = ""
    root_markers: tuple[str, ...] = ("productcraft", ".claude")   # a repo root holds CLAUDE.md and one of these

    # ---- derived ------------------------------------------------------------
    @property
    def stage_numbers(self) -> list[int]:
        return sorted(self.stages)

    @property
    def first_stage(self) -> int:
        return self.stage_numbers[0]

    @property
    def last_stage(self) -> int:
        return self.stage_numbers[-1]

    @property
    def all_stage_numbers(self) -> list[int]:
        """The stages plus the coordinator's column, when the studio has one."""
        out = set(self.stage_numbers)
        if self.coordinator_stage is not None:
            out.add(self.coordinator_stage)
        return sorted(out)

    def stage_name(self, n: int) -> str:
        if self.coordinator_stage is not None and n == self.coordinator_stage:
            return self.coordinator_label
        return self.stages.get(n, str(n))

    def stage_label(self, n: int) -> str:
        if self.coordinator_stage is not None and n == self.coordinator_stage:
            return self.coordinator_label
        return f"{n} {self.stage_name(n)}"

    def seat_name(self, slug: str) -> str:
        return self.seat_names.get(slug, slug)

    def record_name_re(self) -> re.Pattern:
        kinds = "|".join(re.escape(k) for k in self.kinds)
        return re.compile(rf"^(pass-\d{{2,}})-([a-z0-9\-]+)-({kinds})\.md$")


# --------------------------------------------------------------------------- #
# Productcraft — the first copy's shape, unchanged
# --------------------------------------------------------------------------- #

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
)

PRODUCTCRAFT = Studio(
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
    repo_prefixes=("productcraft/", "systemcraft/", ".claude/"),
    corpus_path_re=re.compile(r"(?<![\w/])((?:productcraft/|systemcraft/)?corpus/[\w\-./]+?\.md)"),
    id_re=None,
    taxonomy_path=_KIT_DIR / "taxonomy.md",
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
)
