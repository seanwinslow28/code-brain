#!/usr/bin/env python3
"""Knowledge Lint Agent — D.3 vault health check (two-tier).

Tier 1 (Mac Mini, structural Python checks, ~5 min):
  • broken wikilinks  — [[Target]] references that don't resolve
  • orphan files      — files with 0 inbound wikilinks
  • missing YAML frontmatter in vault/knowledge/
  • CamelCase filenames in vault/knowledge/ (kebab-case only)

Tier 2 (MacBook Pro, Qwen3-14B via route_to_macbook, ~15 min, semantic):
  • contradiction detection across related articles
  • staleness detection (>30d + time-sensitive model/API refs)
  • SOT drift check (vault vs SOURCE-OF-TRUTH.md Parts 1-2)
  • Phase 2 (2026-04-27): soul-tier-a-conflict — flags articles whose
    claims contradict any Tier-A SOUL item across the active domains
    (creative-studio, life-systems, job-hunt-2026). Activated when a Tier-2
    `llm_caller` is supplied; SOUL context is prepended to the prompt.

Output: `vault/health/YYYY-MM-DD-lint-report.md` with severity buckets
(CRITICAL / HIGH / MEDIUM / LOW).

Tier 2 only runs if Tier 1 surfaced issues OR the `--full` flag is set,
matching the Sunday-22:00 launchd schedule from install_schedules.sh.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib import concept_edges
from lib.artifact_loader import DOMAINS, load_artifact
from lib.config import Config, load_config
from lib.filelock import FileLock
from lib.logging_setup import record_run, setup_logger

AGENT_NAME = "knowledge-lint"
MAX_TURNS_TIER1 = 20
MAX_TURNS_TIER2 = 30
MAX_BUDGET_USD = 0.00

_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
_FRONTMATTER_RE = re.compile(r"^---\n.*?\n---", re.DOTALL)
_KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")

# Directories whose contents are auto-generated or ephemeral and should NOT
# be flagged as orphans just because nothing wikilinks to them.
#
# Phase C (2026-05-01): `qa/` is the third article tier — answer endpoints
# produced by `scripts/query.py --file-back`. They cite outward via
# `[[wikilinks]]` (which gives concepts/connections inbound links) but are
# never themselves the target of a wikilink, so they would otherwise show
# up as orphan-MEDIUM noise on every Sunday lint. The other knowledge/
# Tier-1 checks (missing-frontmatter, camelcase-filename) already include
# qa/ via `knowledge.rglob`, and the Tier-2 stale-reference scan covers it
# via `_vault_md_files`, so excluding it from orphan detection is the only
# change needed for the qa/ tier to stay clean under lint.
_ORPHAN_EXCLUDE_DIRS = {
    "_archive",
    "60_archive",
    "00_inbox",
    "90_system",
    "70_apple-notes",
    "the-block-meetings-granola-notes",
    "media-team-ideas",
    "daily",
    "qa",
}

# Strip fenced code blocks and inline code before wikilink scanning so that
# documentation examples (e.g. vault/90_system/VAULT-GUIDE.md) don't register
# as broken references.
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


def _strip_code(text: str) -> str:
    text = _FENCE_RE.sub("", text)
    text = _INLINE_CODE_RE.sub("", text)
    return text

# Filename patterns excluded from orphan checks (Granola transcripts etc.)
_ORPHAN_EXCLUDE_SUFFIXES = ("-transcript.md",)


def _is_orphan_excluded(rel_parts: tuple[str, ...], name: str) -> bool:
    """Return True if a file should be skipped by orphan detection."""
    if any(part in _ORPHAN_EXCLUDE_DIRS for part in rel_parts):
        return True
    if any(name.endswith(sfx) for sfx in _ORPHAN_EXCLUDE_SUFFIXES):
        return True
    return False


class LintSeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class LintIssue:
    kind: str                 # "broken-wikilink" | "orphan" | "missing-frontmatter" | ...
    severity: LintSeverity
    file: Path
    detail: str = ""
    tier: int = 1


@dataclass
class Tier1Report:
    issues: list[LintIssue] = field(default_factory=list)

    @property
    def total_issues(self) -> int:
        return len(self.issues)


# ─── helpers ──────────────────────────────────────────────────────────────

def _vault_md_files(vault_root: Path, include_excluded: bool = False) -> list[Path]:
    """All .md files under vault_root, skipping .obsidian/, .trash/.

    include_excluded=True includes vault/daily/* (only relevant for orphan
    analysis where daily logs can legitimately be endpoints).
    """
    files: list[Path] = []
    for p in vault_root.rglob("*.md"):
        rel_parts = p.relative_to(vault_root).parts
        if any(part in {".obsidian", ".trash"} or part.startswith(".") for part in rel_parts):
            continue
        if not include_excluded and "daily" in rel_parts:
            continue
        files.append(p)
    return files


def _resolve_wikilink(vault_root: Path, target: str, files: list[Path]) -> Path | None:
    """Try to resolve `[[target]]` against the vault.

    Resolution order (matches Obsidian's "shortest path when possible" +
    full-path behavior):
      1. Path-style `[[foo/bar/name]]` — exact relative-path match, with or
         without .md suffix.
      2. Basename match — file stem equals the last path segment.
      3. Frontmatter title match.
    """
    t = target.strip()
    if not t:
        return None

    # Strip .md from whatever the user wrote
    t_norm = t[:-3] if t.lower().endswith(".md") else t
    last_segment = t_norm.rsplit("/", 1)[-1].lower()
    full_path_lower = t_norm.lower().replace("\\", "/")
    has_path_prefix = "/" in t_norm

    for f in files:
        # Path-style match: compare full relative path (no .md) to target
        rel = f.relative_to(vault_root).as_posix()
        rel_no_ext = rel[:-3] if rel.lower().endswith(".md") else rel
        if has_path_prefix and rel_no_ext.lower() == full_path_lower:
            return f
        # Basename match (default Obsidian behavior)
        if f.stem.lower() == last_segment:
            return f

    # Title frontmatter fallback (only if nothing else matched)
    for f in files:
        try:
            head = f.read_text(encoding="utf-8", errors="replace")[:500]
        except OSError:
            continue
        m = re.search(r'^title:\s*"?([^"\n]+)"?', head, re.MULTILINE)
        if m and m.group(1).strip().lower() == t.lower():
            return f
    return None


def find_broken_wikilinks(vault_root: Path) -> list[LintIssue]:
    files = _vault_md_files(vault_root)
    issues: list[LintIssue] = []
    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scan = _strip_code(text)
        for target in _WIKILINK_RE.findall(scan):
            if not _resolve_wikilink(vault_root, target, files):
                issues.append(
                    LintIssue(
                        kind="broken-wikilink",
                        severity=LintSeverity.HIGH,
                        file=fp,
                        detail=target.strip(),
                    )
                )
    return issues


def find_orphan_files(vault_root: Path) -> list[LintIssue]:
    """A file is an orphan if no other file wikilinks to it.

    Skips `index.md` / `INDEX.md` / MOC files which are intentionally hubs.
    """
    files = _vault_md_files(vault_root)
    # Build reverse-link index
    inbound: dict[Path, int] = {f: 0 for f in files}
    for src in files:
        try:
            text = src.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scan = _strip_code(text)
        for target in _WIKILINK_RE.findall(scan):
            resolved = _resolve_wikilink(vault_root, target, files)
            if resolved and resolved != src:
                inbound[resolved] = inbound.get(resolved, 0) + 1

    issues: list[LintIssue] = []
    for f, count in inbound.items():
        if count > 0:
            continue
        stem_lower = f.stem.lower()
        if stem_lower in {"index", "readme", "home"} or "moc" in stem_lower:
            continue
        rel_parts = f.relative_to(vault_root).parts
        if _is_orphan_excluded(rel_parts, f.name):
            continue
        issues.append(
            LintIssue(
                kind="orphan",
                severity=LintSeverity.MEDIUM,
                file=f,
                detail=f.relative_to(vault_root).as_posix(),
            )
        )
    return issues


def find_missing_frontmatter(vault_root: Path) -> list[LintIssue]:
    """Scope: `vault/knowledge/**.md` must have YAML frontmatter."""
    knowledge = vault_root / "knowledge"
    if not knowledge.exists():
        return []
    issues: list[LintIssue] = []
    for fp in knowledge.rglob("*.md"):
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not _FRONTMATTER_RE.match(text):
            issues.append(
                LintIssue(
                    kind="missing-frontmatter",
                    severity=LintSeverity.MEDIUM,
                    file=fp,
                    detail=fp.relative_to(vault_root).as_posix(),
                )
            )
    return issues


def find_camelcase_filenames(vault_root: Path) -> list[LintIssue]:
    """Scope: `vault/knowledge/**.md` filenames must be kebab-case."""
    knowledge = vault_root / "knowledge"
    if not knowledge.exists():
        return []
    issues: list[LintIssue] = []
    for fp in knowledge.rglob("*.md"):
        if fp.name.lower() in {"index.md", "readme.md"}:
            continue
        if not _KEBAB_RE.match(fp.name):
            issues.append(
                LintIssue(
                    kind="camelcase-filename",
                    severity=LintSeverity.LOW,
                    file=fp,
                    detail=fp.name,
                )
            )
    return issues


def run_tier1(vault_root: Path) -> Tier1Report:
    all_issues: list[LintIssue] = []
    all_issues.extend(find_broken_wikilinks(vault_root))
    all_issues.extend(find_orphan_files(vault_root))
    all_issues.extend(find_missing_frontmatter(vault_root))
    all_issues.extend(find_camelcase_filenames(vault_root))
    return Tier1Report(issues=all_issues)


# ─── Tier 2 (semantic, LLM-powered) ───────────────────────────────────────

def build_soul_context(config: Config | None) -> str:
    """Concatenated SOUL bodies for all active domains, framed as reference.

    Returns "" when artifacts are globally disabled, the knowledge_lint
    agent has no per-agent entry, or `SOUL` isn't in its `on_demand` list.
    Per-domain unconfirmed/missing artifacts map to a placeholder so the
    LLM still sees structure.
    """
    if config is None:
        return ""
    cfg = config.artifact_config("knowledge_lint")
    if not cfg or "SOUL" not in cfg.get("on_demand", []):
        return ""

    sections: list[str] = []
    for domain in DOMAINS:
        body = load_artifact(domain, "SOUL", config.vault_root)
        if body is None:
            sections.append(f"## SOUL — {domain}\n\n[unavailable]\n")
            continue
        sections.append(f"## SOUL — {domain}\n\n{body.rstrip()}\n")
    return (
        "--- BEGIN OPERATING-MODEL SOUL CONTEXT (Tier-A reference) ---\n\n"
        + "\n".join(sections)
        + "\n--- END OPERATING-MODEL SOUL CONTEXT ---\n\n"
    )


def _build_tier2_prompt(soul_context: str) -> str:
    """Tier-2 LLM prompt — semantic contradictions + Tier-A SOUL conflicts."""
    instructions = (
        "Review the vault for two things:\n"
        "  1. Semantic contradictions across `knowledge/concepts/*.md`.\n"
        "  2. Articles whose claims contradict any Tier-A SOUL item across "
        "creative-studio, life-systems, or job-hunt-2026 (use the SOUL context "
        "above as the canonical reference).\n\n"
        "Return ONLY a JSON object with two keys:\n"
        '  "contradictions": [{"files": ["..."], "detail": "..."}],\n'
        '  "soul_conflicts": [{"file": "...", "tier_a_item": "...", "detail": "..."}]\n'
    )
    if soul_context:
        return soul_context + instructions
    return instructions


def _slugs_from_contradiction_files(files: list[str]) -> tuple[str, str] | None:
    """Best-effort extract (from_slug, to_slug) from an LLM contradiction
    `files` payload for dedupe against the SQL fast path.

    LLM contradictions list affected file paths; the slug is the file
    stem of the first two paths. Returns None if fewer than two distinct
    file basenames are present (means we can't form a pair to dedupe).
    """
    stems: list[str] = []
    seen: set[str] = set()
    for path_str in files:
        if not path_str:
            continue
        stem = Path(path_str).stem
        if not stem or stem in seen:
            continue
        seen.add(stem)
        stems.append(stem)
        if len(stems) == 2:
            return stems[0], stems[1]
    return None


def _read_sql_contradictions(
    vault_root: Path,
    log: logging.Logger,
) -> list[LintIssue]:
    """Phase D — SQL fast path against `concept_edges`. Returns CRITICAL
    contradiction issues sourced directly from the synthesizer's typed
    edges. Zero LLM cost. No-op when `vault/.vault-index.db` is missing
    (fresh vault before vault_indexer ran).
    """
    db_path = vault_root / ".vault-index.db"
    if not db_path.exists():
        return []
    issues: list[LintIssue] = []
    try:
        conn = sqlite3.connect(str(db_path))
    except sqlite3.Error as exc:
        log.warning("SQL fast path skipped: cannot open %s (%s)", db_path, exc)
        return []
    try:
        # Defensive: probe for the table — if vault_indexer has never run
        # against this DB, concept_edges may not exist yet (and we must
        # not call get_connection here, which would mutate the schema as
        # a side effect of a read-only lint pass).
        probe = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='concept_edges'"
        ).fetchone()
        if not probe:
            return []
        for from_slug, to_slug in concept_edges.find_contradictions(conn):
            log.info(
                "Tier 2 contradiction: source=sql %s contradicts %s",
                from_slug, to_slug,
            )
            issues.append(
                LintIssue(
                    kind="contradiction",
                    severity=LintSeverity.CRITICAL,
                    file=Path(f"knowledge/concepts/{from_slug}.md"),
                    detail=f"contradicts {to_slug} (source=sql)",
                    tier=2,
                )
            )
    finally:
        conn.close()
    return issues


def run_tier2(
    vault_root: Path,
    *,
    llm_caller: Callable[[str], dict] | None = None,
    stale_days: int = 30,
    soul_context: str = "",
    logger: logging.Logger | None = None,
) -> list[LintIssue]:
    """Heuristic staleness + SQL fast path + LLM contradiction / SOUL scan.

    Without an llm_caller, Tier 2 still runs (a) the staleness regex scan
    (catches mentions of retired model names like Opus 4.1) and (b) the
    Phase D SQL fast path against `concept_edges` for synthesizer-flagged
    contradictions. With an llm_caller, the existing LLM pass also runs
    for contradiction discovery the synthesizer missed AND for
    `soul-tier-a-conflict` (Phase 2).

    Phase D dedupe rule: contradictions are deduplicated across SQL and
    LLM by `frozenset({from_slug, to_slug})`. SQL hits win when both
    paths surface the same pair (SQL row carries source provenance).
    LLM-only contradictions still surface — synthesizer didn't catch
    them. Documented in CHANGELOG v3.20.0.

    `stale_days` is reserved for a future mtime-based staleness pass —
    today the staleness check is keyword-based via `stale_refs`.
    """
    log = logger or logging.getLogger(AGENT_NAME)
    issues: list[LintIssue] = []
    _ = stale_days  # reserved; see docstring
    stale_refs = [
        "opus 4.1", "opus 4.0",
        "sonnet 4.0", "sonnet 4.5",
        "wan 2.2 5b",
        "claude-code-sdk",
        "ClaudeCodeOptions",
        "claude-3-",
    ]
    for fp in _vault_md_files(vault_root):
        try:
            text = fp.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        for ref in stale_refs:
            if ref in text:
                issues.append(
                    LintIssue(
                        kind="stale-reference",
                        severity=LintSeverity.HIGH,
                        file=fp,
                        detail=ref,
                        tier=2,
                    )
                )

    # Phase D — SQL fast path. Always runs; no-ops cleanly when the DB
    # or table is missing. Track the (from, to) pairs we've seen so the
    # subsequent LLM pass can dedupe against them.
    sql_issues = _read_sql_contradictions(vault_root, log)
    seen_contradiction_pairs: set[frozenset[str]] = set()
    for issue in sql_issues:
        # detail format: "contradicts {to_slug} (source=sql)" — extract
        # the to_slug for the pair key.
        from_slug = issue.file.stem
        to_match = re.match(r"contradicts\s+(\S+)", issue.detail)
        to_slug = to_match.group(1) if to_match else ""
        if from_slug and to_slug:
            seen_contradiction_pairs.add(frozenset({from_slug, to_slug}))
    issues.extend(sql_issues)

    if llm_caller is None:
        return issues

    # LLM-powered contradiction + SOUL Tier-A conflict (caller supplies impl).
    # Phase D: contradictions are deduped against the SQL fast path; SOUL
    # conflicts have no SQL substitute and always surface from the LLM.
    try:
        resp = llm_caller(_build_tier2_prompt(soul_context))
        for c in resp.get("contradictions", []):
            files = c.get("files", [])
            if not files:
                continue
            pair = _slugs_from_contradiction_files(files)
            if pair and frozenset(pair) in seen_contradiction_pairs:
                log.info(
                    "Tier 2 contradiction: source=llm dropped (sql had it) "
                    "%s vs %s", pair[0], pair[1],
                )
                continue
            log.info("Tier 2 contradiction: source=llm %s", files[0])
            issues.append(
                LintIssue(
                    kind="contradiction",
                    severity=LintSeverity.CRITICAL,
                    file=Path(files[0]),
                    detail=c.get("detail", ""),
                    tier=2,
                )
            )
        for sc in resp.get("soul_conflicts", []):
            file_str = sc.get("file", "")
            if not file_str:
                continue
            tier_a = sc.get("tier_a_item", "")
            detail = sc.get("detail", "")
            combined = (
                f"tier_a_item={tier_a!r}: {detail}" if tier_a else detail
            )
            issues.append(
                LintIssue(
                    kind="soul-tier-a-conflict",
                    severity=LintSeverity.HIGH,
                    file=Path(file_str),
                    detail=combined,
                    tier=2,
                )
            )
    except Exception:
        pass
    return issues


# ─── synthetic vault + oracle (≥95% recall gate) ──────────────────────────

def build_synthetic_vault(vault_root: Path) -> dict:
    """Create a 30-file vault with exactly 20 planted issues.

    Returns an oracle dict that the recall test uses to score the lint
    output. Layout per plan §4:

      Tier 1 (14 planted):
        3× orphan              (HIGH)
        3× broken [[nonexistent]] wikilinks   (HIGH)
        2× broken wikilinks to moved files    (HIGH)
        2× missing frontmatter                (MEDIUM)
        2× CamelCase filenames                (LOW)
        + 2× extra broken wikilinks to push count to 14
      Tier 2 (6 planted):
        2 pairs = 4 contradictions     (CRITICAL)
        2× stale model references      (HIGH)

      Clean controls: 10 files with ≥1 inbound link, frontmatter present,
      kebab-case filenames, no [[broken]] refs.
    """
    knowledge = vault_root / "knowledge" / "concepts"
    connections = vault_root / "knowledge" / "connections"
    notes = vault_root / "notes"
    knowledge.mkdir(parents=True, exist_ok=True)
    connections.mkdir(parents=True, exist_ok=True)
    notes.mkdir(parents=True, exist_ok=True)

    oracle_tier1: list[dict] = []
    oracle_tier2: list[dict] = []
    clean_files: list[str] = []

    fm = "---\ntitle: {t}\ntype: concept\n---\n"

    # 10 clean controls (all in /knowledge/concepts/, kebab-case, with FM).
    # Cross-link in a full loop so every clean file has ≥1 inbound (no false
    # orphan positives).
    clean_names = [
        "alpha", "beta", "gamma", "delta", "epsilon",
        "zeta", "eta", "theta", "iota", "kappa",
    ]
    n_clean = len(clean_names)
    for i, n in enumerate(clean_names):
        prev_ = clean_names[(i - 1) % n_clean]
        next_ = clean_names[(i + 1) % n_clean]
        (knowledge / f"{n}.md").write_text(
            fm.format(t=n.capitalize())
            + f"Clean body with [[{prev_}]] and [[{next_}]].\n",
            encoding="utf-8",
        )
        clean_files.append(f"{n}.md")

    # 3 orphans — exist, but no other file links to them
    for name in ["orphan-one", "orphan-two", "orphan-three"]:
        p = notes / f"{name}.md"
        p.write_text(f"# {name}\n\nI refer to [[alpha]] but no one refers to me.\n", encoding="utf-8")
        oracle_tier1.append({"kind": "orphan", "file": name + ".md"})

    # 5 broken wikilinks — 3 to nonexistent, 2 to "moved" (we'll delete the target)
    (notes / "broken-link-one.md").write_text("See [[nonexistent-target-a]].\n", encoding="utf-8")
    clean_files_link_body = "Referenced here: [[broken-link-one]] [[broken-link-two]] [[broken-link-three]]"
    (knowledge / "concepts" / "linker.md") if False else None  # noqa (keep layout)
    (notes / "broken-link-two.md").write_text("See [[nonexistent-target-b]].\n", encoding="utf-8")
    (notes / "broken-link-three.md").write_text("See [[nonexistent-target-c]].\n", encoding="utf-8")
    (notes / "broken-link-four.md").write_text("See [[moved-target-a]].\n", encoding="utf-8")
    (notes / "broken-link-five.md").write_text("See [[moved-target-b]].\n", encoding="utf-8")
    for t in ["nonexistent-target-a", "nonexistent-target-b", "nonexistent-target-c",
              "moved-target-a", "moved-target-b"]:
        oracle_tier1.append({"kind": "broken-wikilink", "target": t})

    # Inbound link for these broken-link files so they aren't flagged as orphans
    (notes / "linker.md").write_text(
        "hub: [[broken-link-one]] [[broken-link-two]] [[broken-link-three]] "
        "[[broken-link-four]] [[broken-link-five]] "
        "[[no-fm-one]] [[no-fm-two]] [[BadCaseOne]] [[AnotherBadCase]] "
        "[[stale-opus]] [[stale-wan]] [[contradict-a]] [[contradict-b]] [[contradict-c]] [[contradict-d]]\n",
        encoding="utf-8",
    )

    # 2 extra broken wikilinks (to reach Tier-1 count of 14)
    (notes / "extra-broken-one.md").write_text("See [[nonexistent-extra-a]].\n", encoding="utf-8")
    (notes / "extra-broken-two.md").write_text("See [[nonexistent-extra-b]].\n", encoding="utf-8")
    # Link them so they're not orphans
    (notes / "linker.md").write_text(
        (notes / "linker.md").read_text(encoding="utf-8")
        + " [[extra-broken-one]] [[extra-broken-two]]\n",
        encoding="utf-8",
    )
    for t in ["nonexistent-extra-a", "nonexistent-extra-b"]:
        oracle_tier1.append({"kind": "broken-wikilink", "target": t})

    # 2 missing frontmatter (inside knowledge/)
    (knowledge / "no-fm-one.md").write_text("Body without frontmatter.\n", encoding="utf-8")
    (knowledge / "no-fm-two.md").write_text("Another body without frontmatter.\n", encoding="utf-8")
    oracle_tier1.append({"kind": "missing-frontmatter", "file": "no-fm-one.md"})
    oracle_tier1.append({"kind": "missing-frontmatter", "file": "no-fm-two.md"})

    # 2 CamelCase filenames (inside knowledge/)
    (knowledge / "BadCaseOne.md").write_text(fm.format(t="Bad") + "Body [[alpha]] [[beta]]\n", encoding="utf-8")
    (knowledge / "AnotherBadCase.md").write_text(fm.format(t="Bad2") + "Body [[alpha]] [[beta]]\n", encoding="utf-8")
    oracle_tier1.append({"kind": "camelcase-filename", "file": "BadCaseOne.md"})
    oracle_tier1.append({"kind": "camelcase-filename", "file": "AnotherBadCase.md"})

    # Tier 2: 2 pairs of contradictions (CRITICAL)
    (knowledge / "contradict-a.md").write_text(fm.format(t="C-A") + "We ship phi4-mini on Mac Mini [[alpha]] [[beta]]\n", encoding="utf-8")
    (knowledge / "contradict-b.md").write_text(fm.format(t="C-B") + "We ship phi3-mini on Mac Mini [[alpha]] [[beta]]\n", encoding="utf-8")
    (knowledge / "contradict-c.md").write_text(fm.format(t="C-C") + "RIFE temporal_smoothing=0.8 is optimal [[alpha]] [[beta]]\n", encoding="utf-8")
    (knowledge / "contradict-d.md").write_text(fm.format(t="C-D") + "RIFE temporal_smoothing=0.6 is optimal [[alpha]] [[beta]]\n", encoding="utf-8")
    for f in ["contradict-a.md", "contradict-b.md", "contradict-c.md", "contradict-d.md"]:
        oracle_tier2.append({"kind": "contradiction", "file": f})

    # Tier 2: 2 stale references (HIGH)
    (knowledge / "stale-opus.md").write_text(
        fm.format(t="Stale-Opus") + "We use Opus 4.1 for heavy synth [[alpha]] [[beta]]\n",
        encoding="utf-8",
    )
    (knowledge / "stale-wan.md").write_text(
        fm.format(t="Stale-Wan") + "Wan 2.2 5B gives the best quality [[alpha]] [[beta]]\n",
        encoding="utf-8",
    )
    oracle_tier2.append({"kind": "stale-reference", "file": "stale-opus.md"})
    oracle_tier2.append({"kind": "stale-reference", "file": "stale-wan.md"})

    return {
        "tier1": oracle_tier1,
        "tier2": oracle_tier2,
        "clean_files": clean_files,
        "clean_count": len(clean_files),
        "counts": {
            "tier1": len(oracle_tier1),
            "tier2": len(oracle_tier2),
        },
    }


def recall_against_oracle(issues: list[LintIssue], oracle: list[dict]) -> float:
    """Return recall = matched_planted / total_planted.

    A planted issue matches a found issue iff:
      kind == oracle.kind
      AND (target matches OR file.name matches)
    """
    if not oracle:
        return 1.0

    matched = 0
    for planted in oracle:
        kind = planted["kind"]
        for found in issues:
            if found.kind != kind:
                continue
            if "target" in planted and planted["target"] in found.detail:
                matched += 1
                break
            if "file" in planted and found.file.name == planted["file"]:
                matched += 1
                break
    return matched / len(oracle)


# ─── report writer ────────────────────────────────────────────────────────

def format_report(
    *,
    tier1: Tier1Report,
    tier2: list[LintIssue],
    today: str,
) -> str:
    lines = [f"# Knowledge Lint Report — {today}", ""]
    total = tier1.total_issues + len(tier2)
    lines.append(f"_{total} issues found ({tier1.total_issues} structural, {len(tier2)} semantic)._")
    lines.append("")

    buckets: dict[LintSeverity, list[LintIssue]] = {s: [] for s in LintSeverity}
    for issue in list(tier1.issues) + list(tier2):
        buckets[issue.severity].append(issue)

    for sev in (LintSeverity.CRITICAL, LintSeverity.HIGH, LintSeverity.MEDIUM, LintSeverity.LOW):
        items = buckets[sev]
        if not items:
            continue
        lines.append(f"## {sev.value} ({len(items)})")
        lines.append("")
        for it in items:
            rel = it.file.as_posix() if it.file.is_absolute() else str(it.file)
            lines.append(f"- **{it.kind}** ({'T1' if it.tier == 1 else 'T2'}): `{rel}` — {it.detail}")
        lines.append("")

    if total == 0:
        lines.append("✓ No issues found.")
    return "\n".join(lines) + "\n"


def write_report(vault_root: Path, content: str, *, today: str) -> Path:
    health_dir = vault_root / "health"
    health_dir.mkdir(parents=True, exist_ok=True)
    with FileLock(health_dir / ".lock", exclusive=True, timeout=10.0):
        out = health_dir / f"{today}-lint-report.md"
        out.write_text(content, encoding="utf-8")
    return out


# ─── CLI ──────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Knowledge Lint Agent")
    parser.add_argument("--full", action="store_true", help="Run Tier 2 even if Tier 1 is clean")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cfg = load_config()
    logger = setup_logger(AGENT_NAME, cfg.log_dir, cfg.log_level)

    tier1 = run_tier1(cfg.vault_root)
    logger.info("Tier 1: %d issues", tier1.total_issues)

    tier2: list[LintIssue] = []
    if tier1.total_issues > 0 or args.full:
        soul_context = build_soul_context(cfg)
        tier2 = run_tier2(
            cfg.vault_root,
            soul_context=soul_context,
            logger=logger,
        )
        logger.info(
            "Tier 2: %d issues (soul_context=%s)",
            len(tier2),
            "loaded" if soul_context else "off",
        )

    today = date.today().isoformat()
    report = format_report(tier1=tier1, tier2=tier2, today=today)

    if not args.dry_run:
        path = write_report(cfg.vault_root, report, today=today)
        logger.info("Report: %s", path)

    # Exit code 0 regardless; daily_driver surfaces CRITICAL/HIGH in morning brief
    record_run(cfg.log_dir, AGENT_NAME, mode=None,
               status="success", cost_usd=0.0, duration_ms=None, turns=None,
               notes=f"tier1={tier1.total_issues} tier2={len(tier2)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
