"""trace/cases.md — the guided-reading content, kept apart from the records.

Teaching content is written by hand (see `cases-template.md`), keyed to a pass
and a finding, and pinned to each source's sha256 *at writing time*. The
renderer never invents a story: a missing file renders an honest empty
section, a changed source renders a qualification in place of its excerpt, and
an excerpt that is not in its file is reported on the page rather than shown.

The file's shape, per case:

    ## Case: <title>
    pass: pass-10
    finding: M8
    assist: worked | hint | independent
    question: <one sentence>
    options:
      - key: a
        label: <short choice>
    sources:
      - path: audits/audit-strategy-r3.md
        sha256: <64 hex>
        excerpt: "<short exact quote>"
        label: <what this source is>

    ### Story  ### Hint  ### Reveal  ### Your turn  ### Terms  ### Diagram

The `key: value` head and its two lists are read with the kit's own
frontmatter subset, so a malformed case fails loudly with a line number.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .frontmatter import FrontmatterError, parse_yaml_subset, split_frontmatter

__all__ = [
    "CASES_FILE", "ASSIST_LEVELS", "Option", "Source", "Case", "CasesDoc",
    "parse_cases", "resolve_sources", "load_cases",
]

CASES_FILE = "cases.md"
ASSIST_LEVELS = ("worked", "hint", "independent")
ASSIST_BLURB = {
    "worked": "Worked example — the story, the evidence and the reasoning are open.",
    "hint": "With a hint — the story and the evidence are open; the hint and the reasoning are folded.",
    "independent": "On your own — the goal, the evidence and the question first; the diagnosis and the reasoning stay folded until you answer or ask.",
}
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_CASE_HEAD = re.compile(r"^##\s+Case:\s*(.+?)\s*$", re.M)
_SUBSECTION = re.compile(r"^###\s+(.+?)\s*$", re.M)


@dataclass(frozen=True)
class Option:
    key: str
    label: str


@dataclass
class Source:
    path: str
    sha256: str
    excerpt: str
    label: str = ""
    state: str = "unchecked"          # current | changed | missing | excerpt-missing | unchecked
    current_sha256: Optional[str] = None
    line: Optional[int] = None

    @property
    def qualified(self) -> bool:
        return self.state in ("changed", "missing", "excerpt-missing")

    @property
    def shows_excerpt(self) -> bool:
        return self.state == "current"

    @property
    def qualification(self) -> str:
        if self.state == "changed":
            return "The source changed since this story was written, so its excerpt is withheld."
        if self.state == "missing":
            return "The source is not on disk at that path, so its excerpt is withheld."
        if self.state == "excerpt-missing":
            return "The quoted words are not in the file at that hash, so the excerpt is withheld."
        return ""


@dataclass
class Case:
    key: str
    title: str
    pass_id: str = ""
    finding: str = ""
    assist: str = "worked"
    question: str = ""
    options: list[Option] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    story: list[str] = field(default_factory=list)     # paragraphs
    hint: str = ""
    reveal: list[str] = field(default_factory=list)    # paragraphs
    your_turn: str = ""
    terms: list[tuple[str, str]] = field(default_factory=list)
    diagram: list[tuple[str, str, str]] = field(default_factory=list)   # (kind, branch, label)
    notes: list[str] = field(default_factory=list)     # soft qualifications shown on the page

    @property
    def qualified(self) -> bool:
        return any(s.qualified for s in self.sources)

    @property
    def goal(self) -> str:
        return self.story[0] if self.story else ""

    @property
    def rest_of_story(self) -> list[str]:
        return self.story[1:]


@dataclass
class CasesDoc:
    path: Optional[Path] = None
    engagement: str = ""
    written: str = ""
    status: str = "proposed"
    intro: str = ""
    cases: list[Case] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def reviewed(self) -> bool:
        return self.status == "reviewed"

    @property
    def attribution(self) -> str:
        return ("read by Sean against its sources" if self.reviewed
                else "a proposed explanation, not an answer key, until Sean has read it against its sources")


# --------------------------------------------------------------------------- #
# parsing
# --------------------------------------------------------------------------- #


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "case"


def _paragraphs(text: str) -> list[str]:
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        block = " ".join(line.strip() for line in block.split("\n") if line.strip())
        if block:
            out.append(block)
    return out


def _sections(block: str) -> tuple[str, dict[str, str]]:
    """Split a case body into its head (before the first ###) and its ### sections."""
    marks = list(_SUBSECTION.finditer(block))
    if not marks:
        return block, {}
    head = block[: marks[0].start()]
    out: dict[str, str] = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(block)
        out[m.group(1).strip().lower()] = block[m.end(): end].strip()
    return head, out


def _terms(text: str) -> list[tuple[str, str]]:
    out = []
    for line in text.split("\n"):
        line = line.strip()
        if not line.startswith("- "):
            continue
        term, _, meaning = line[2:].partition(":")
        if meaning.strip():
            out.append((term.strip(), meaning.strip()))
    return out


def _diagram(text: str) -> list[tuple[str, str, str]]:
    """A small text flow: `- step`, `- ? decision`, `- yes: branch`, `- no: branch`."""
    out: list[tuple[str, str, str]] = []
    for line in text.split("\n"):
        line = line.strip()
        if not line.startswith("- "):
            continue
        item = line[2:].strip()
        if item.startswith("?"):
            out.append(("decision", "", item.lstrip("? ").strip()))
            continue
        head, sep, rest = item.partition(":")
        if sep and len(head.split()) <= 2 and out and any(k == "decision" for k, _, _ in out):
            out.append(("branch", head.strip(), rest.strip()))
        else:
            out.append(("step", "", item))
    return out


def _one_line(value: Any) -> str:
    return "" if value is None else " ".join(str(value).split())


def parse_cases(text: str, path: Optional[Path] = None) -> CasesDoc:
    """Parse cases.md. Fatal problems drop that case and are reported in `errors`."""
    doc = CasesDoc(path=path)
    try:
        meta, body = split_frontmatter(text)
    except FrontmatterError as e:
        doc.errors.append(f"cases.md: {e}")
        meta, body = {}, text
    doc.engagement = _one_line(meta.get("engagement"))
    doc.written = _one_line(meta.get("written"))
    status = _one_line(meta.get("status")) or "proposed"
    if status not in ("proposed", "reviewed"):
        doc.errors.append(f"cases.md: status must be `proposed` or `reviewed`, got {status!r}")
        status = "proposed"
    doc.status = status

    heads = list(_CASE_HEAD.finditer(body))
    intro_end = heads[0].start() if heads else len(body)
    intro_block = re.sub(r"^#\s+.*$", "", body[:intro_end], count=1, flags=re.M)
    doc.intro = " ".join(p for p in _paragraphs(intro_block))

    seen: set[str] = set()
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        title = m.group(1).strip()
        case, errors = _parse_case(title, body[m.end(): end], i + 1)
        if errors:
            doc.errors.extend(errors)
            continue
        key = case.key
        n = 2
        while key in seen:
            key, n = f"{case.key}-{n}", n + 1
        seen.add(key)
        case.key = key
        doc.cases.append(case)
    return doc


def _parse_case(title: str, block: str, number: int) -> tuple[Optional[Case], list[str]]:
    where = f"cases.md case {number} ({title!r})"
    head, sections = _sections(block)
    try:
        fm: dict[str, Any] = parse_yaml_subset(head) if head.strip() else {}
    except FrontmatterError as e:
        return None, [f"{where}: {e}"]

    assist = _one_line(fm.get("assist")).lower()
    if assist not in ASSIST_LEVELS:
        return None, [f"{where}: assist must be one of {', '.join(ASSIST_LEVELS)}, got {assist or '(none)'!r}"]
    if not sections.get("story", "").strip():
        return None, [f"{where}: no `### Story` section"]
    pass_id = _one_line(fm.get("pass"))
    if not pass_id:
        return None, [f"{where}: no `pass:` field naming the run this case is about"]

    finding = _one_line(fm.get("finding"))
    finding = "" if finding.lower() in ("none", "") else finding
    case = Case(
        key=_slug(f"{pass_id}-{finding}" if finding else pass_id),
        title=title,
        pass_id=pass_id,
        finding=finding,
        assist=assist,
        question=_one_line(fm.get("question")),
    )
    errors: list[str] = []
    for item in fm.get("options") or []:
        if isinstance(item, dict) and item.get("key") is not None and item.get("label"):
            case.options.append(Option(_one_line(item["key"]), _one_line(item["label"])))
        else:
            errors.append(f"{where}: options entries are `- key:` + `label:` blocks, got {item!r}")
    for item in fm.get("sources") or []:
        if not isinstance(item, dict) or not item.get("path"):
            errors.append(f"{where}: sources entries are `- path:` + `sha256:` + `excerpt:` blocks, got {item!r}")
            continue
        sha = _one_line(item.get("sha256")).lower()
        if not _HEX64.match(sha):
            errors.append(f"{where}: source {item['path']} has no sha256 (got {item.get('sha256')!r})")
            continue
        excerpt = str(item.get("excerpt") or "").strip()
        if not excerpt:
            errors.append(f"{where}: source {item['path']} carries no excerpt")
            continue
        case.sources.append(Source(_one_line(item["path"]), sha, excerpt, _one_line(item.get("label"))))
    if errors:
        return None, errors
    if case.assist == "independent" and len(case.options) < 2:
        return None, [f"{where}: an independent case needs at least two options, so the reader can answer before the reveal"]

    case.story = _paragraphs(sections.get("story", ""))
    case.hint = " ".join(_paragraphs(sections.get("hint", "")))
    case.reveal = _paragraphs(sections.get("reveal", ""))
    case.your_turn = " ".join(_paragraphs(sections.get("your turn", "")))
    case.terms = _terms(sections.get("terms", ""))
    case.diagram = _diagram(sections.get("diagram", ""))
    if not case.reveal:
        case.notes.append("No reasoning has been written for this case yet.")
    if case.assist == "hint" and not case.hint:
        case.notes.append("This case offers a hint but none has been written.")
    if not case.sources:
        case.notes.append("This case names no source, so nothing on it can be checked against a record.")
    return case, []


# --------------------------------------------------------------------------- #
# sources: the hash at writing time against the file now
# --------------------------------------------------------------------------- #


def _normalize(text: str) -> tuple[str, list[int]]:
    """Collapse whitespace runs to single spaces, keeping a map back to raw offsets."""
    out: list[str] = []
    idx: list[int] = []
    prev_space = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if prev_space:
                continue
            out.append(" ")
            idx.append(i)
            prev_space = True
        else:
            out.append(ch)
            idx.append(i)
            prev_space = False
    return "".join(out), idx


def _find_line(text: str, excerpt: str) -> Optional[int]:
    pos = text.find(excerpt)
    if pos >= 0:
        return text.count("\n", 0, pos) + 1
    flat, idx = _normalize(text)
    needle = " ".join(excerpt.split())
    pos = flat.find(needle)
    if pos < 0:
        return None
    return text.count("\n", 0, idx[pos]) + 1


def resolve_sources(doc: CasesDoc, eng) -> CasesDoc:
    """Fill each source's state, current hash and line, and report what does not check out."""
    for case in doc.cases:
        for s in case.sources:
            current = eng.hash_of(s.path)
            s.current_sha256 = current
            if current is None:
                s.state = "missing"
                doc.errors.append(f"cases.md {case.pass_id}: source {s.path} is not on disk")
                continue
            if current != s.sha256:
                s.state = "changed"       # qualified, excerpt withheld — never a confident stale quote
                continue
            text = eng.read_text(s.path) or ""
            line = _find_line(text, s.excerpt)
            if line is None:
                s.state = "excerpt-missing"
                doc.errors.append(f"cases.md {case.pass_id}: the excerpt quoted from {s.path} is not in that file")
                continue
            s.state, s.line = "current", line
    return doc


def load_cases(eng) -> Optional[CasesDoc]:
    """Read and check `trace/cases.md`, or None when no one has written it yet."""
    path = Path(eng.trace_dir) / CASES_FILE
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        doc = CasesDoc(path=path)
        doc.errors.append(f"cases.md: {e}")
        return doc
    return resolve_sources(parse_cases(text, path=path), eng)
