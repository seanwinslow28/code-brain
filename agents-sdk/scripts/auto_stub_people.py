#!/usr/bin/env python3
"""Auto-create minimal person stubs for new [[Name]] wikilinks.

Triggered by the SessionEnd hook after every Claude Code session. Scans
the vault for `[[Name]]` wikilinks appearing in `author:` YAML frontmatter
fields and creates minimal stubs at `vault/40_knowledge/people/<slug>.md`
for any that don't already resolve.

Two filters protect against creating garbage stubs:

  1. The wikilink must live inside an `author:` YAML frontmatter list.
     Web clips put structured `author: - "[[Name]]"` in that slot, so
     this is the strong signal it's a person and not a typo / citation
     marker / folder reference.
  2. The target must match the person-name shape: 1-3 capitalized
     words with optional middle initials / hyphens / apostrophes /
     latin diacritics. Catches "Ali Çevik", "RT Watson", "Brian Danga".
     Rejects "stage", "intent-engineering", "10", "prj-job-hunt-2026".

Stubs are intentionally minimal — `title:` matching the wikilink,
`type: person`, `status: unverified`, the inbound source path, and
a "fill in identity when convenient" line. Run with `--dry-run` to
preview without writing.

Exit codes: always 0 (fire-and-forget hook pattern). Failures are
logged but do not block the session close.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VAULT_ROOT = REPO_ROOT / "vault"
PEOPLE_DIR = VAULT_ROOT / "40_knowledge" / "people"
LOG_FILE = VAULT_ROOT / "90_system" / "agent-logs" / "auto-stub-people.log"

# Directories skipped during scanning — matches knowledge_lint._vault_md_files.
_EXCLUDE_PARTS = {".obsidian", ".trash", "node_modules"}

# Frontmatter block: between leading `---` and the closing `---`.
_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
# `author:` list — captures the block until the next top-level YAML key.
# Tolerates `author: - "[[X]]"` (single value, inline) and the more common
# multi-line list with `  - "[[X]]"` entries.
_AUTHOR_BLOCK_RE = re.compile(
    r"^author:\s*\n((?:[ \t]+-.*\n)+)|^author:\s*(.+)$",
    re.MULTILINE,
)
# Wikilink targets inside the author block.
_AUTHOR_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+?)(?:\|[^\]]+)?\]\]")
# Person-name shape: 1-3 capitalized tokens; latin/diacritic letters,
# apostrophes, hyphens, periods, middle initials allowed.
_PERSON_NAME_RE = re.compile(
    r"^[A-ZÀ-Ý][A-Za-zÀ-ÿ.'\-]*(?: [A-ZÀ-Ý][A-Za-zÀ-ÿ.'\-]*){0,2}$"
)
# Per-run safety cap. If we ever exceed this it likely means something's
# wrong with the filters or someone bulk-imported clips; better to bail
# than blast 100 stubs into the vault.
_MAX_STUBS_PER_RUN = 10


def _slugify(name: str) -> str:
    """ASCII-fold + lowercase + hyphenate. 'Ali Çevik' -> 'ali-cevik'."""
    normalized = unicodedata.normalize("NFKD", name)
    ascii_only = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    lowered = ascii_only.lower()
    return re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")


def _vault_md_files() -> list[Path]:
    files: list[Path] = []
    for p in VAULT_ROOT.rglob("*.md"):
        parts = p.relative_to(VAULT_ROOT).parts
        if any(part in _EXCLUDE_PARTS or part.startswith(".") for part in parts):
            continue
        files.append(p)
    return files


def _extract_author_wikilinks(text: str) -> list[str]:
    """Return raw [[X]] target strings appearing in the file's `author:` frontmatter."""
    fm = _FRONTMATTER_RE.match(text)
    if not fm:
        return []
    fm_body = fm.group(1)
    targets: list[str] = []
    for m in _AUTHOR_BLOCK_RE.finditer(fm_body):
        block = m.group(1) or m.group(2) or ""
        for link in _AUTHOR_WIKILINK_RE.findall(block):
            targets.append(link.strip())
    return targets


def _existing_person_titles() -> set[str]:
    """Set of `title:` values from existing people/ stubs, for dedup."""
    if not PEOPLE_DIR.exists():
        return set()
    titles: set[str] = set()
    title_re = re.compile(r'^title:\s*"?([^"\n]+)"?', re.MULTILINE)
    for f in PEOPLE_DIR.glob("*.md"):
        try:
            head = f.read_text(encoding="utf-8", errors="replace")[:500]
        except OSError:
            continue
        m = title_re.search(head)
        if m:
            titles.add(m.group(1).strip())
    return titles


def _stub_path(name: str) -> Path:
    return PEOPLE_DIR / f"{_slugify(name)}.md"


def _stub_body(name: str, source_rel: str) -> str:
    today = date.today().isoformat()
    return (
        "---\n"
        f'title: "{name}"\n'
        f'full-name: "{name}"\n'
        "type: person\n"
        "status: unverified\n"
        "domain: []\n"
        "tags: []\n"
        f"created: {today}\n"
        f"last-updated: {today}\n"
        "ai-context: \"Auto-stub created by auto_stub_people.py — fill in identity when convenient.\"\n"
        "---\n"
        "\n"
        f"# {name}\n"
        "\n"
        f"Auto-stub created by `auto_stub_people.py`. Identity unverified — fill in a one-paragraph bio when you next encounter this person in your research.\n"
        "\n"
        "## First inbound reference\n"
        "\n"
        f"- `{source_rel}`\n"
        "\n"
        "## Why this stub exists\n"
        "\n"
        f"A web-clip or research note landed with `author: - \"[[{name}]]\"` in its YAML frontmatter. The SessionEnd auto-stub hook created this file so the wikilink resolves and the synthesizer can cluster around it on the next nightly run.\n"
    )


def _log(msg: str) -> None:
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{date.today().isoformat()}] {msg}\n")
    except OSError:
        pass


def find_candidates() -> dict[str, str]:
    """Return {person_name: first_source_rel_path} for new candidates."""
    existing_titles = _existing_person_titles()
    files = _vault_md_files()
    candidates: dict[str, str] = {}
    for fp in files:
        # Skip files inside the people/ folder itself.
        try:
            rel_parts = fp.relative_to(VAULT_ROOT).parts
        except ValueError:
            continue
        if "people" in rel_parts and "40_knowledge" in rel_parts:
            continue
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for raw_target in _extract_author_wikilinks(text):
            name = raw_target.strip()
            if not _PERSON_NAME_RE.match(name):
                continue
            if name in existing_titles:
                continue
            if _stub_path(name).exists():
                continue
            if name in candidates:
                continue
            candidates[name] = str(fp.relative_to(VAULT_ROOT))
    return candidates


def create_stubs(candidates: dict[str, str], dry_run: bool = False) -> list[Path]:
    if len(candidates) > _MAX_STUBS_PER_RUN:
        _log(
            f"SAFETY: {len(candidates)} candidates exceeds cap "
            f"({_MAX_STUBS_PER_RUN}); skipping all. Candidates: "
            f"{sorted(candidates)}"
        )
        return []
    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for name, source_rel in sorted(candidates.items()):
        path = _stub_path(name)
        if path.exists():
            continue
        if dry_run:
            created.append(path)
            continue
        try:
            path.write_text(_stub_body(name, source_rel), encoding="utf-8")
            created.append(path)
        except OSError as e:
            _log(f"FAILED to write {path}: {e}")
    return created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing.")
    args = parser.parse_args()

    candidates = find_candidates()
    if not candidates:
        return 0

    created = create_stubs(candidates, dry_run=args.dry_run)
    if not created:
        return 0

    action = "WOULD CREATE" if args.dry_run else "CREATED"
    summary = f"{action} {len(created)} person stub(s): {[p.name for p in created]}"
    _log(summary)
    print(summary, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
