"""Strip-then-hash: the frozen copy a handoff crosses (#326, ruled on #282 decision 6).

A handoff crosses typed artifacts, never reasoning. A seat's artifact carries
both: the product content the receiving studio designs from, and the process
trace of how it got there (Moves, repair notes, audit dispositions, loopbacks).
The binding between two studios names the process parts in a fenced `strip`
block; this module removes exactly those, hashes what is left, and stamps the
copy with that hash and the full source artifact's hash beside it. Nothing is
stripped that the binding does not name: a binding with no `strip` block is an
error, never a guess.

The `strip` block, one directive per line:

    heading: ## Moves              the section under a heading of that level whose
                                   text is the name, or starts with it plus a space
    heading-ending: ## dispositioned   ... whose text ends with the word
    heading-tag: [Δ                a bracketed span opening with this, removed from
                                   every kept heading line (the heading stays)
    paragraph: **Repair note       a blank-line-delimited paragraph whose first
                                   line opens with this text
    key: audit                     a frontmatter key, with its continuation lines

A section runs to the next heading of the same or a higher level. Headings and
paragraphs inside fenced code are never matched.

The copy is the stripped text with five stamp lines at the top of its
frontmatter. `sha256` is the hash of the stripped text without those lines, so
`verify` removes them and re-hashes. A copy frozen before this rule (three
stamps, no `source_sha256`) is a verbatim copy and verifies the same way.

Stdlib only, no model, no network.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

__all__ = [
    "BindingError",
    "FrozenCopy",
    "StripRules",
    "STAMP_KEYS",
    "freeze",
    "read_rules",
    "strip",
    "unstamp",
    "verify",
]

STAMP_KEYS = ("frozen_from", "sha256", "source_sha256", "frozen_at", "stripped")

_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_DIRECTIVES = ("heading", "heading-ending", "heading-tag", "paragraph", "key")


class BindingError(ValueError):
    """The binding names no process parts, or names them in a form this module does not read."""


@dataclass(frozen=True)
class StripRules:
    headings: tuple[tuple[int, str], ...] = ()
    heading_endings: tuple[tuple[int, str], ...] = ()
    heading_tags: tuple[str, ...] = ()
    paragraphs: tuple[str, ...] = ()
    keys: tuple[str, ...] = ()


def _parse_heading_name(value: str, line_no: int) -> tuple[int, str]:
    m = _HEADING.match(value)
    if not m or not m.group(2):
        raise BindingError(f"strip block line {line_no}: a heading directive needs a level and a name, e.g. '## Moves'")
    return len(m.group(1)), m.group(2)


def read_rules(binding: Path) -> StripRules:
    """Read every fenced `strip` block in a binding file. No block is an error."""
    lines = binding.read_text().split("\n")
    found = False
    inside = False
    acc: dict[str, list] = {d: [] for d in _DIRECTIVES}
    for n, raw in enumerate(lines, 1):
        s = raw.strip()
        if not inside:
            if s in ("```strip", "~~~strip"):
                inside, found = True, True
            continue
        if s in ("```", "~~~"):
            inside = False
            continue
        if not s:
            continue
        name, sep, value = s.partition(":")
        name, value = name.strip(), value.strip()
        if not sep or name not in _DIRECTIVES or not value:
            raise BindingError(f"{binding.name} line {n}: expected one of {', '.join(_DIRECTIVES)} followed by ': <value>', got {s!r}")
        if name in ("heading", "heading-ending"):
            acc[name].append(_parse_heading_name(value, n))
        else:
            acc[name].append(value)
    if inside:
        raise BindingError(f"{binding.name}: a strip block is never closed")
    if not found:
        raise BindingError(f"{binding.name} names no process parts (no fenced `strip` block); nothing is stripped by guess")
    return StripRules(
        headings=tuple(acc["heading"]),
        heading_endings=tuple(acc["heading-ending"]),
        heading_tags=tuple(acc["heading-tag"]),
        paragraphs=tuple(acc["paragraph"]),
        keys=tuple(acc["key"]),
    )


def _split(text: str) -> tuple[list[str] | None, list[str]]:
    """(frontmatter lines without the fences, body lines). None when there is no frontmatter."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], lines[i + 1:]
    return None, lines


def _join(fm: list[str] | None, body: list[str]) -> str:
    if fm is None:
        return "\n".join(body)
    return "\n".join(["---", *fm, "---", *body])


def _drop_keys(fm: list[str], keys: tuple[str, ...], removed: list[str]) -> list[str]:
    out: list[str] = []
    dropping = False
    for line in fm:
        top = line[:1] not in (" ", "\t", "-", "")
        if top:
            key = line.split(":", 1)[0].strip()
            dropping = key in keys
            if dropping:
                removed.append(f"key: {key}")
        elif dropping and line.strip() == "":
            dropping = False
        if not dropping:
            out.append(line)
    return out


def _tag_pattern(tag: str) -> re.Pattern:
    return re.compile(r"\s*" + re.escape(tag) + r"[^\]]*\]")


def _matches(level: int, text: str, rules: StripRules) -> bool:
    for lv, name in rules.headings:
        if lv == level and (text == name or text.startswith(name + " ")):
            return True
    for lv, name in rules.heading_endings:
        if lv == level and (text == name or text.endswith(" " + name)):
            return True
    return False


def _strip_body(body: list[str], rules: StripRules, removed: list[str]) -> list[str]:
    tags = [(t, _tag_pattern(t)) for t in rules.heading_tags]
    tag_counts = {t: 0 for t, _ in tags}

    # Pass 1: sections and heading tags.
    out: list[str] = []
    in_fence = False
    cut_level: int | None = None
    for line in body:
        if _FENCE.match(line):
            in_fence = not in_fence
            if cut_level is None:
                out.append(line)
            continue
        m = None if in_fence else _HEADING.match(line)
        if m:
            level = len(m.group(1))
            if cut_level is not None and level <= cut_level:
                cut_level = None
            if cut_level is None:
                text = m.group(2)
                for t, pat in tags:
                    text, n = pat.subn("", text)
                    tag_counts[t] += n
                text = text.strip()
                if _matches(level, text, rules):
                    cut_level = level
                    removed.append(f"{m.group(1)} {text}")
                    continue
                line = f"{m.group(1)} {text}" if text != m.group(2) else line
        if cut_level is None:
            out.append(line)
    for t, n in tag_counts.items():
        if n:
            removed.append(f"tag: {t} ×{n}")

    # Pass 2: named paragraphs, outside fences.
    kept: list[str] = []
    in_fence = False
    skipping = False
    prev_blank = True
    for line in out:
        blank = line.strip() == ""
        if skipping:
            if blank:
                skipping = False
                prev_blank = True
            continue
        if _FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence and prev_blank and not blank:
            hit = next((p for p in rules.paragraphs if line.startswith(p)), None)
            if hit is not None:
                removed.append(f"paragraph: {hit}")
                skipping = True
                continue
        kept.append(line)
        prev_blank = blank

    # Collapse the blank runs a removal leaves behind (outside fences only; markdown reads them as one).
    final: list[str] = []
    in_fence = False
    for line in kept:
        if _FENCE.match(line):
            in_fence = not in_fence
        if not in_fence and line.strip() == "" and final and final[-1].strip() == "":
            continue
        final.append(line)
    while len(final) > 1 and final[-1].strip() == "" and final[-2].strip() == "":
        final.pop()
    return final


def _dedupe(items: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    for it in items:
        counts[it] = counts.get(it, 0) + 1
    return [k if n == 1 or "×" in k else f"{k} ×{n}" for k, n in counts.items()]


def strip(text: str, rules: StripRules) -> tuple[str, list[str]]:
    """Return (stripped text, what was removed — heading names and directive labels, never content)."""
    removed: list[str] = []
    fm, body = _split(text)
    if fm is not None and rules.keys:
        fm = _drop_keys(fm, rules.keys, removed)
    body = _strip_body(body, rules, removed)
    return _join(fm, body), _dedupe(removed)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def unstamp(text: str) -> str:
    """The copy without its stamp lines: the bytes its `sha256` was taken over."""
    fm, body = _split(text)
    if fm is None:
        return text
    kept = [l for l in fm if l.split(":", 1)[0].strip() not in STAMP_KEYS or l[:1] in (" ", "\t")]
    if not kept:
        return "\n".join(body)
    return _join(kept, body)


def _stamp_value(text: str, key: str) -> str | None:
    fm, _ = _split(text)
    for line in fm or []:
        k, sep, v = line.partition(":")
        if sep and k.strip() == key and line[:1] not in (" ", "\t"):
            return v.strip()
    return None


@dataclass
class FrozenCopy:
    source_id: str
    source: Path
    copy: Path
    sha256: str
    source_sha256: str
    removed: list[str] = field(default_factory=list)

    def manifest_row(self) -> str:
        stripped = ", ".join(self.removed) if self.removed else "nothing named was present"
        return f"| {self.source_id} | {self.copy.parent.name}/{self.copy.name} | `{self.source_sha256}` | `{self.sha256}` | {stripped} |"


MANIFEST_HEADER = "| Source id | Frozen copy | source sha256 | copy sha256 (stripped) | Stripped |\n|---|---|---|---|---|"


def freeze(source: Path, source_id: str, rules: StripRules, out_dir: Path, frozen_at: str) -> FrozenCopy:
    """Write `<out_dir>/<source_id>--<stem>.md`: the stripped text, stamped. Returns its record."""
    raw = source.read_text()
    stripped, removed = strip(raw, rules)
    digest = _sha(stripped)
    source_digest = hashlib.sha256(source.read_bytes()).hexdigest()
    origin = "/".join(source.resolve().parts[-2:])
    stamps = [
        f"frozen_from: {source_id} ({origin})",
        f"sha256: {digest}",
        f"source_sha256: {source_digest}",
        f"frozen_at: {frozen_at}",
        f"stripped: {json.dumps(removed, ensure_ascii=False)}",
    ]
    fm, body = _split(stripped)
    copy_text = _join(stamps + (fm or []), body)
    out_dir.mkdir(parents=True, exist_ok=True)
    copy = out_dir / f"{source_id}--{source.stem}.md"
    copy.write_text(copy_text)
    if _sha(unstamp(copy_text)) != digest:   # the stamp must come off exactly
        raise AssertionError(f"{copy}: unstamped bytes do not hash to the stamped value")
    return FrozenCopy(source_id, source, copy, digest, source_digest, removed)


@dataclass
class Verdict:
    copy: Path
    ok: bool
    lines: list[str]


def verify(copy: Path, source: Path | None = None) -> Verdict:
    """Does the copy still hash to its stamp? With a source: is the source still the bytes it was frozen from?"""
    text = copy.read_text()
    stamped = _stamp_value(text, "sha256")
    if stamped is None:
        return Verdict(copy, False, [f"{copy.name}: no sha256 stamp — not a frozen copy"])
    lines: list[str] = []
    ok = True
    actual = _sha(unstamp(text))
    if actual == stamped:
        lines.append(f"{copy.name}: copy matches its stamp")
    else:
        ok = False
        lines.append(f"{copy.name}: HASH DRIFT — stamped {stamped[:12]}…, bytes hash to {actual[:12]}…")
    if source is not None:
        # A copy frozen before strip-then-hash has no source_sha256: it is verbatim, so its sha256 is the source's.
        expected = _stamp_value(text, "source_sha256") or stamped
        now = hashlib.sha256(source.read_bytes()).hexdigest()
        if now == expected:
            lines.append(f"{copy.name}: source {source.name} unchanged since the freeze")
        else:
            ok = False
            lines.append(f"{copy.name}: SOURCE MOVED — {source.name} no longer hashes to the frozen source; a material change is a new crossing")
    return Verdict(copy, ok, lines)
