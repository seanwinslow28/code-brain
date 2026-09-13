"""Load one engagement folder: brief, pass records, labels, notes, artifacts.

Layout the kit reads (private ledger, `ledger/engagements/<eng-id>/`):

    brief.md                     # Open: frontmatter id / name / type / opened / closed / pass_budget
    artifacts/, audits/, gates/  # what the seats wrote; paths in records are relative to this folder
    dNN-<slug>.md                # ledger entries
    trace/pass-NN-<seat>-<kind>.md   # one immutable record per invocation (#272 decision 2)
    trace/labels.md              # Sean's verdicts, apart from the facts (decision 6)
    trace/notes.md               # process notes (viewer growth slot)
    trace/logs/                  # raw transcripts the records index
    trace/eval.html              # the rendered viewer (decision 3)

Paths inside a record resolve against the engagement folder first; a path
that starts with a studio or `.claude/` prefix resolves against the repo
root (found by walking up to a directory holding both CLAUDE.md and
productcraft/, or given explicitly).
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .frontmatter import FrontmatterError, split_frontmatter
from .labels import Label, LabelsError, parse_labels
from .moves import MovesSection, parse_moves

__all__ = [
    "KINDS", "METER_SOURCES", "REQUIRED_FIELDS", "STAGE_SEATS", "FIXED_AUDITORS", "REQUIRED_COSIGNS",
    "InputRef", "OutputRef", "CheckRef", "Record", "Engagement",
    "load_engagement", "resolve_path", "sha256_path", "find_repo_root",
]

KINDS = ("draft", "audit", "co-sign", "gate", "repair", "trial", "close")
METER_SOURCES = ("Agent-tool usage", "codex footer", "UNMEASURED")
REQUIRED_FIELDS = (
    "pass", "seat", "kind", "stage", "runtime", "launch", "effort", "launched", "completed",
    "wall_clock_s", "meter_source", "inputs", "withheld", "outputs", "raw_log", "checks",
    "triggered_by", "shadow_of",
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

_REPO_PREFIXES = ("productcraft/", "systemcraft/", ".claude/")
_RECORD_NAME = re.compile(r"^(pass-\d{2,})-([a-z0-9\-]+)-(draft|audit|co-sign|gate|repair|trial|close)\.md$")


@dataclass(frozen=True)
class InputRef:
    path: str
    sha256: str


@dataclass(frozen=True)
class OutputRef:
    path: Optional[str] = None
    sha256: Optional[str] = None
    id: Optional[str] = None


@dataclass(frozen=True)
class CheckRef:
    pass_id: str
    kind: str
    verdict: str


@dataclass
class Record:
    pass_id: str
    file: Path
    seat: str = ""
    kind: str = ""
    stage: int = 0
    runtime: str = ""
    launch: str = ""
    effort: str = ""
    launched: str = ""
    completed: str = ""
    wall_clock_s: Optional[int] = None
    meter: Optional[dict[str, Any]] = None
    meter_source: str = ""
    inputs: list[InputRef] = field(default_factory=list)
    withheld: list[str] = field(default_factory=list)
    outputs: list[OutputRef] = field(default_factory=list)
    raw_log: str = ""
    checks: list[CheckRef] = field(default_factory=list)
    triggered_by: Optional[str] = None
    shadow_of: Optional[str] = None
    corpus_read: list[str] = field(default_factory=list)
    moves_pointer: str = ""
    notes: str = ""
    raw: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    @property
    def artifact_outputs(self) -> list[OutputRef]:
        return [o for o in self.outputs if o.path]

    @property
    def hands_forward(self) -> bool:
        return self.kind in ("draft", "repair", "trial")


@dataclass
class Engagement:
    root: Path
    trace_dir: Path
    repo: Optional[Path]
    brief: dict[str, Any] = field(default_factory=dict)
    records: list[Record] = field(default_factory=list)
    labels: dict[str, Label] = field(default_factory=dict)
    labels_error: Optional[str] = None
    notes: Optional[str] = None
    errors: list[str] = field(default_factory=list)
    _texts: dict[str, Optional[str]] = field(default_factory=dict, repr=False)
    _hashes: dict[str, Optional[str]] = field(default_factory=dict, repr=False)
    _moves: dict[str, Optional[MovesSection]] = field(default_factory=dict, repr=False)

    @property
    def by_id(self) -> dict[str, Record]:
        return {r.pass_id: r for r in self.records}

    @property
    def id(self) -> str:
        return str(self.brief.get("id") or self.root.name.split("-", 3)[:3] and "-".join(self.root.name.split("-")[:3]))

    @property
    def name(self) -> str:
        return str(self.brief.get("name") or self.root.name)

    def resolve(self, rel: str) -> Optional[Path]:
        return resolve_path(self.root, self.repo, rel)

    def read_text(self, rel: str) -> Optional[str]:
        """Text of a path in the engagement (or repo), cached; None if absent or binary."""
        if rel not in self._texts:
            p = self.resolve(rel)
            text: Optional[str] = None
            if p is not None and p.is_file():
                try:
                    text = p.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    text = None
            self._texts[rel] = text
        return self._texts[rel]

    def hash_of(self, rel: str) -> Optional[str]:
        """sha256 of a path in the engagement (or repo) as it stands now, cached; None if absent."""
        if rel not in self._hashes:
            p = self.resolve(rel)
            self._hashes[rel] = sha256_path(p) if p is not None else None
        return self._hashes[rel]

    def output_state(self, o: OutputRef) -> str:
        """`current` (disk matches the recorded hash) · `superseded` (a later revision overwrote it in
        place, per #274) · `missing` · `unhashed` (the record carries no hash for it)."""
        if not o.path:
            return "missing"
        h = self.hash_of(o.path)
        if h is None:
            return "missing"
        if not o.sha256:
            return "unhashed"
        return "current" if h == o.sha256 else "superseded"

    def moves_artifact(self, record: Record) -> Optional[OutputRef]:
        """The output artifact whose `## Moves` section this pass owns, if any."""
        if not record.hands_forward:
            return None
        for o in record.artifact_outputs:
            text = self.read_text(o.path)
            if text is not None and parse_moves(text) is not None:
                return o
        return record.artifact_outputs[0] if record.artifact_outputs else None

    def moves_state(self, record: Record) -> str:
        """`current` · `origin` · `none-kind` (hands nothing forward) · `superseded` · `missing`."""
        if not record.hands_forward:
            return "none-kind"
        o = self.moves_artifact(record)
        if o is None:
            return "missing"
        state = self.output_state(o)
        if state in ("missing", "superseded"):
            return state
        mv = self.moves_for(record)
        if mv is None:
            return "missing"
        return "origin" if mv.origin else "current"

    def moves_for(self, record: Record) -> Optional[MovesSection]:
        """The pass's Moves, read from its artifact — only when that artifact is the revision on disk."""
        if record.pass_id not in self._moves:
            o = self.moves_artifact(record)
            section: Optional[MovesSection] = None
            if o is not None and self.output_state(o) in ("current", "unhashed"):
                text = self.read_text(o.path)
                section = parse_moves(text) if text is not None else None
            self._moves[record.pass_id] = section
        return self._moves[record.pass_id]

    def entry_path(self, entry_id: str) -> Optional[Path]:
        """`pc-eng-000.d03` → the `d03-*.md` file at the engagement root."""
        m = re.match(r"^.+\.d(\d+)$", entry_id)
        if not m:
            return None
        hits = sorted(self.root.glob(f"d{m.group(1)}-*.md"))
        return hits[0] if hits else None


# --------------------------------------------------------------------------- #
# paths and hashes
# --------------------------------------------------------------------------- #


def find_repo_root(start: Path) -> Optional[Path]:
    for p in [start] + list(start.parents):
        if (p / "CLAUDE.md").is_file() and (p / "productcraft").is_dir():
            return p
    return None


def resolve_path(root: Path, repo: Optional[Path], rel: str) -> Optional[Path]:
    rel = rel.strip()
    if not rel or rel in ("—", "-", "none"):
        return None
    candidate = root / rel
    if candidate.exists():
        return candidate
    if repo is not None and rel.startswith(_REPO_PREFIXES):
        candidate = repo / rel
        if candidate.exists():
            return candidate
    return None


def sha256_path(p: Path) -> str:
    """sha256 of a file, or of a directory as sorted (relpath, filehash) pairs."""
    if p.is_dir():
        h = hashlib.sha256()
        for f in sorted(x for x in p.rglob("*") if x.is_file()):
            h.update(f"{f.relative_to(p).as_posix()}\0{hashlib.sha256(f.read_bytes()).hexdigest()}\n".encode())
        return h.hexdigest()
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --------------------------------------------------------------------------- #
# loading
# --------------------------------------------------------------------------- #


def _section(body: str, title: str) -> str:
    m = re.search(rf"^##\s+{re.escape(title)}\s*$", body, re.M)
    if not m:
        return ""
    rest = body[m.end():]
    nxt = re.search(r"^##\s", rest, re.M)
    return (rest[: nxt.start()] if nxt else rest).strip()


def _list_items(section: str) -> list[str]:
    items = []
    for line in section.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items


def _as_str(v: Any) -> str:
    return "" if v is None else str(v)


def _record_from(fm: dict[str, Any], body: str, file: Path) -> Record:
    r = Record(pass_id=_as_str(fm.get("pass")), file=file, raw=fm)
    for key in REQUIRED_FIELDS:
        if key not in fm:
            r.errors.append(f"{file.name}: missing required field `{key}`")
    r.seat = _as_str(fm.get("seat"))
    r.kind = _as_str(fm.get("kind"))
    if r.kind and r.kind not in KINDS:
        r.errors.append(f"{file.name}: kind `{r.kind}` is not one of {', '.join(KINDS)}")
    stage = fm.get("stage")
    if isinstance(stage, int) and 0 <= stage <= 7:
        r.stage = stage
    elif "stage" in fm:
        r.errors.append(f"{file.name}: stage must be an integer 0–7, got {stage!r}")
    r.runtime, r.launch, r.effort = _as_str(fm.get("runtime")), _as_str(fm.get("launch")), _as_str(fm.get("effort"))
    r.launched, r.completed = _as_str(fm.get("launched")), _as_str(fm.get("completed"))
    wc = fm.get("wall_clock_s")
    r.wall_clock_s = wc if isinstance(wc, int) else None
    if "wall_clock_s" in fm and r.wall_clock_s is None:
        r.errors.append(f"{file.name}: wall_clock_s must be an integer")
    meter = fm.get("meter")
    r.meter = meter if isinstance(meter, dict) else None
    if meter is not None and not isinstance(meter, dict):
        r.errors.append(f"{file.name}: meter must be a block of input / output / cached")
    r.meter_source = _as_str(fm.get("meter_source"))
    for item in fm.get("inputs") or []:
        if isinstance(item, dict) and item.get("path"):
            r.inputs.append(InputRef(str(item["path"]), _as_str(item.get("sha256"))))
        else:
            r.errors.append(f"{file.name}: inputs entries are `- path:` + `sha256:` blocks, got {item!r}")
    if fm.get("inputs") is not None and not isinstance(fm.get("inputs"), list):
        r.errors.append(f"{file.name}: inputs must be a list")
    withheld = fm.get("withheld")
    r.withheld = [str(w) for w in withheld] if isinstance(withheld, list) else []
    if "withheld" in fm and "the drafting conversation" not in r.withheld and r.kind != "close":
        r.errors.append(f"{file.name}: withheld must include `the drafting conversation`")
    for item in fm.get("outputs") or []:
        if isinstance(item, dict) and item.get("path"):
            r.outputs.append(OutputRef(path=str(item["path"]), sha256=_as_str(item.get("sha256")) or None))
        elif isinstance(item, dict) and item.get("id"):
            r.outputs.append(OutputRef(id=str(item["id"])))
        elif isinstance(item, str):
            r.outputs.append(OutputRef(path=item) if ("/" in item or item.endswith(".md")) else OutputRef(id=item))
        else:
            r.errors.append(f"{file.name}: outputs entries are `- path:` (+ `sha256:`) or `- id:` blocks, got {item!r}")
    r.raw_log = _as_str(fm.get("raw_log"))
    for item in fm.get("checks") or []:
        if isinstance(item, dict) and item.get("pass"):
            r.checks.append(CheckRef(str(item["pass"]), _as_str(item.get("kind")), _as_str(item.get("verdict"))))
        else:
            r.errors.append(f"{file.name}: checks entries are `- pass:` + `kind:` + `verdict:` blocks, got {item!r}")
    r.triggered_by = fm.get("triggered_by") or None
    r.shadow_of = fm.get("shadow_of") or None
    corpus = _section(body, "Corpus read")
    r.corpus_read = _list_items(corpus)
    r.moves_pointer = _section(body, "Moves").split("\n")[0].strip() if _section(body, "Moves") else ""
    r.notes = _section(body, "Notes")
    if r.notes.lower() == "none":
        r.notes = ""
    return r


def _locate(path: Path) -> tuple[Path, Path]:
    path = path.resolve()
    if path.name == "trace" and path.is_dir():
        return path.parent, path
    if (path / "trace").is_dir():
        return path, path / "trace"
    if list(path.glob("pass-*.md")):
        return path.parent, path
    return path, path / "trace"


def load_engagement(path: Path | str, repo: Optional[Path] = None) -> Engagement:
    root, trace_dir = _locate(Path(path))
    eng = Engagement(root=root, trace_dir=trace_dir, repo=repo or find_repo_root(root))
    brief = root / "brief.md"
    if brief.is_file():
        try:
            eng.brief, _ = split_frontmatter(brief.read_text(encoding="utf-8"))
        except FrontmatterError as e:
            eng.errors.append(f"brief.md: {e}")
    for f in sorted(trace_dir.glob("pass-*.md")):
        try:
            fm, body = split_frontmatter(f.read_text(encoding="utf-8"))
        except (FrontmatterError, UnicodeDecodeError) as e:
            eng.errors.append(f"{f.name}: {e}")
            continue
        rec = _record_from(fm, body, f)
        m = _RECORD_NAME.match(f.name)
        if not m:
            rec.errors.append(f"{f.name}: filename is not pass-NN-<seat>-<kind>.md")
        elif (m.group(1), m.group(2), m.group(3)) != (rec.pass_id, rec.seat, rec.kind):
            rec.errors.append(
                f"{f.name}: filename says {m.group(1)} {m.group(2)} {m.group(3)}, the record says "
                f"{rec.pass_id or '?'} {rec.seat or '?'} {rec.kind or '?'}"
            )
        if not rec.pass_id:
            rec.pass_id = m.group(1) if m else f.stem
        eng.records.append(rec)
    eng.records.sort(key=lambda r: r.pass_id)
    labels = trace_dir / "labels.md"
    if labels.is_file():
        try:
            eng.labels = parse_labels(labels.read_text(encoding="utf-8"))
        except LabelsError as e:
            eng.labels_error = str(e)
    notes = trace_dir / "notes.md"
    if notes.is_file():
        eng.notes = notes.read_text(encoding="utf-8")
    return eng
