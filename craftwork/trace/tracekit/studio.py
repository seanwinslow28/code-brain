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
studio from the engagement it was handed.

**Every profile lives with its studio, never in the kit** (kit 0.9.0, #325). A
-craft team writes `<team>/trace/studio.py` defining `STUDIO`; Productcraft's is
`productcraft/trace/studio.py`. The content machine keeps its own beside the
machine (`.claude/skills/content-machine/trace/machine.py` in its repo) and
passes it explicitly. `resolve_studio` finds the profile for an engagement in
this order: the one passed in, then the nearest `trace/studio.py` walking up
from the engagement folder (a team's ledger sits inside the team's folder, so
`productcraft/ledger/engagements/pc-eng-001/` finds Productcraft's), then the
file `$TRACEKIT_STUDIO` names. With none of the three it refuses rather than
guess a studio.

A structure check is registered by key rather than held on the profile, so the
profile module imports nothing from the checker and the checker can import the
profile: `tracekit.checker.STRUCTURE_CHECKS[studio.key] = fn`. A profile that
writes its own check registers it when the file is loaded.
"""
from __future__ import annotations

import importlib.util
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

__all__ = ["Studio", "StudioNotFound", "PROFILE_FILE", "PROFILE_ENV", "load_profile", "find_profile", "resolve_studio"]

PROFILE_FILE = "studio.py"          # <team>/trace/studio.py, defining STUDIO
PROFILE_ENV = "TRACEKIT_STUDIO"     # a profile file to fall back on when the walk finds none


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
    taxonomy_path: Optional[Path] = None       # the studio's tracked taxonomy.md (its own modes)
    shared_taxonomy: bool = True               # also read the kit's shared families (craftwork/trace/taxonomy.md)
    withheld_required: Optional[str] = "the drafting conversation"
    brief_file: str = "brief.md"               # the header file at the engagement root
    checks_dir: str = "audits"                 # where check records (audits, gate findings) sit
    structure_check_name: str = "Stage structure"
    check_implications: tuple[str, ...] = ()   # one sentence per rung-0 line, in check order
    review_prompts: tuple[tuple[str, str], ...] = ()
    review_prompts_version: str = ""
    root_markers: tuple[str, ...] = ("craftwork", ".claude")   # a repo root holds CLAUDE.md and one of these

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
# finding an engagement's profile
# --------------------------------------------------------------------------- #


class StudioNotFound(LookupError):
    """No profile was passed, none sits above the engagement, and `$TRACEKIT_STUDIO` names none."""


_LOADED: dict[Path, Studio] = {}


def load_profile(path: Union[Path, str]) -> Studio:
    """Load a profile file and return its `STUDIO`. One load per file, so a studio is one object."""
    p = Path(path).expanduser().resolve()
    if p in _LOADED:
        return _LOADED[p]
    if not p.is_file():
        raise StudioNotFound(f"no studio profile at {p}")
    name = "tracekit_profile_" + re.sub(r"\W", "_", str(p))
    spec = importlib.util.spec_from_file_location(name, p)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    studio = getattr(module, "STUDIO", None)
    if not isinstance(studio, Studio):
        raise StudioNotFound(f"{p} defines no STUDIO profile")
    _LOADED[p] = studio
    return studio


def find_profile(start: Union[Path, str]) -> Optional[Path]:
    """The nearest `<dir>/trace/studio.py` at or above `start`, or None."""
    here = Path(start).expanduser().resolve()
    for d in [here] + list(here.parents):
        candidate = d / "trace" / PROFILE_FILE
        if candidate.is_file():
            return candidate
    return None


def resolve_studio(path: Union[Path, str], studio: Optional[Studio] = None) -> Studio:
    """The studio an engagement belongs to: passed in, found above it, or named by `$TRACEKIT_STUDIO`."""
    if studio is not None:
        return studio
    found = find_profile(path)
    if found is not None:
        return load_profile(found)
    named = os.environ.get(PROFILE_ENV)
    if named:
        return load_profile(named)
    raise StudioNotFound(
        f"no studio profile for {path}: none was passed, no trace/{PROFILE_FILE} sits above it, "
        f"and ${PROFILE_ENV} is unset. A team's profile is <team>/trace/{PROFILE_FILE}; pass --studio <file> "
        f"for an engagement that lives outside its team's folder."
    )

