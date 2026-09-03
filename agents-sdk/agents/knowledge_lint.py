#!/usr/bin/env python3
"""Knowledge Lint Agent — D.3 vault health check (two-tier).

Tier 1 (Mac Mini, structural Python checks, ~5 min):
  • broken wikilinks  — [[Target]] references that don't resolve
  • orphan files      — files with 0 inbound wikilinks
  • missing YAML frontmatter in vault/knowledge/
  • CamelCase filenames in vault/knowledge/ (kebab-case only)

Tier 2 (semantic, ~15 min):
  • staleness detection (time-sensitive model/API refs) — Mac-Mini-local regex
  • contradiction fast path — SQL over the synthesizer's `concept_edges` (local)
  • LLM leg (MacBook Pro, `qwen3.6_35b-a3b-32k` via route_to_macbook): semantic
    contradiction discovery the synthesizer missed + soul-tier-a-conflict —
    flags articles whose claims contradict any Tier-A SOUL item across the
    active domains (creative-studio, life-systems, job-hunt-2026).

    BT5 C3 (2026-07-05) wired this leg into production for the first time:
    main() now resolves the Tier-2 route once (probe-first), injects the
    `knowledge/concepts/*.md` corpus into the prompt in 32K-context batches,
    and reports the leg's actual outcome (reviewed N batches / deferred / failed
    / gate-skipped) instead of the old silent skip. A down host defers honestly;
    the regex + SQL fast paths always run regardless of MBP state.

Output: `vault/health/YYYY-MM-DD-lint-report.md` with severity buckets
(CRITICAL / HIGH / MEDIUM / LOW).

Tier 2 only runs if Tier 1 surfaced issues OR the `--full` flag is set,
matching the Sunday-22:00 launchd schedule from install_schedules.sh.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import re
import sqlite3
import sys
import time
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
from lib.hybrid_router import HybridRouter, RoutingDecision, WOLUnavailable
from lib.logging_setup import record_run, setup_logger

# BT5 C3 (2026-07-05) — Tier-2 corpus injection budgets. The prompt now carries
# the actual concept articles to review (it previously carried none, so a wired
# caller reviewed nothing). Digests are batched to fit the 32K-token context of
# `qwen3.6_35b-a3b-32k` with headroom for SOUL context + instructions + the JSON
# response; multiple LLM calls per run are bounded by a wall-clock budget.
TIER2_BATCH_MAX_CHARS = 40_000   # ~12–14K tokens per batch — safe under 32K
TIER2_BUDGET_SECONDS = 900       # ~15 min per the module docstring
_CONCEPT_DIGEST_MAX_CHARS = 700  # title + Definition section per concept

AGENT_NAME = "knowledge-lint"
MAX_TURNS_TIER1 = 20
MAX_TURNS_TIER2 = 30
MAX_BUDGET_USD = 0.00

_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
_FRONTMATTER_RE = re.compile(r"^---\n.*?\n---", re.DOTALL)
_KEBAB_RE = re.compile(r"^[a-z0-9]+(?:[-_][a-z0-9]+)*\.md$")
# `[[10]]` / `[[42]]` patterns from LLM-generated research notes (Gemini DR,
# LDR) are footnote / citation markers, not wikilinks. Filter them out
# before broken-link reporting.
_CITATION_TARGET_RE = re.compile(r"^\d+$")

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
    "the-block-resume-info",
    "media-team-ideas",
    "daily",
    "qa",
    "references",
    "health",
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

# Directories skipped during broken-wikilink scanning. The Granola meeting
# archive was slug-renamed (e.g. `Alex_Sean sync.md` →
# `mtg-2026-03-XX-alex-sean-sync.md`) but the internal cross-references
# inside each note still point to the pre-rename names. The archive is
# read-only post-2026-05-04 Block layoff — fix the lint scope, not the
# data. Re-enable scanning here only if you rewrite the stale link
# targets in a one-shot migration pass.
_BROKEN_LINK_EXCLUDE_DIRS = {
    "the-block-meetings-granola-notes",
}

# Directories excluded from stale-reference scanning. Lint reports themselves
# legitimately quote retired model names in their report bodies (the names
# Sean is auditing). Archived employer material is historical record; the
# Block job ended 2026-05 and those docs aren't being maintained.
_STALE_REF_EXCLUDE_DIRS = {
    "health",
    "the-block-meetings-granola-notes",
    "the-block-resume-info",
    "_archive",
    "60_archive",
}


def _is_orphan_excluded(rel_parts: tuple[str, ...], name: str) -> bool:
    """Return True if a file should be skipped by orphan detection."""
    if any(part in _ORPHAN_EXCLUDE_DIRS for part in rel_parts):
        return True
    if any(name.endswith(sfx) for sfx in _ORPHAN_EXCLUDE_SUFFIXES):
        return True
    return False


def _is_broken_link_excluded(rel_parts: tuple[str, ...]) -> bool:
    """Return True if a file should be skipped by broken-wikilink scanning."""
    return any(part in _BROKEN_LINK_EXCLUDE_DIRS for part in rel_parts)


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
        if any(part in {".obsidian", ".trash", "node_modules"} or part.startswith(".") for part in rel_parts):
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
        rel_parts = fp.relative_to(vault_root).parts
        if _is_broken_link_excluded(rel_parts):
            continue
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scan = _strip_code(text)
        for target in _WIKILINK_RE.findall(scan):
            target_stripped = target.strip()
            if _CITATION_TARGET_RE.match(target_stripped):
                continue
            if not _resolve_wikilink(vault_root, target_stripped, files):
                issues.append(
                    LintIssue(
                        kind="broken-wikilink",
                        severity=LintSeverity.HIGH,
                        file=fp,
                        detail=target_stripped,
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
    """Scope: `vault/knowledge/**.md` must have YAML frontmatter.

    Excludes auto-generated hub files (`index.md`) which are rewritten
    plain-markdown by `vault_synthesizer.regenerate_index` on every nightly
    run — adding frontmatter to them would be wiped immediately.
    """
    knowledge = vault_root / "knowledge"
    if not knowledge.exists():
        return []
    issues: list[LintIssue] = []
    for fp in knowledge.rglob("*.md"):
        if fp.stem.lower() in {"index", "readme"}:
            continue
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
    """Scope: `vault/knowledge/**.md` filenames must be kebab- or snake-case.

    Snake_case is permitted for files that mirror a Python identifier or SQL
    table name (e.g. `concept_edges.md`, `knowledge_loop.md`, `job_feed.md`)
    where the wikilink target written by the synthesizer is snake_case because
    the source domain (Python/SQL) is snake_case. Mixed-case and PascalCase
    still violate.
    """
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


def _extract_concept_digest(text: str, max_chars: int = _CONCEPT_DIGEST_MAX_CHARS) -> str:
    """Compact per-concept digest for the Tier-2 corpus: title + Definition
    section (the semantic core for contradiction detection). Falls back to a
    leading slice of the body when there's no Definition heading."""
    body = _FRONTMATTER_RE.sub("", text).strip()
    title = ""
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    definition = ""
    m = re.search(r"^##\s+Definition\s*\n(.*?)(?=^##\s|\Z)", body, re.DOTALL | re.MULTILINE)
    if m:
        definition = m.group(1).strip()
    digest = (f"# {title}\n" if title else "") + (definition or body)
    return digest[:max_chars].strip()


def _load_concept_corpus(vault_root: Path) -> list[tuple[str, str]]:
    """Return [(repo-relative path, digest)] for every `knowledge/concepts/*.md`.

    BT5 C3 — the material the Tier-2 LLM scan actually reviews. Empty (not an
    error) on a fresh vault before the synthesizer has written any concepts.
    """
    concepts_dir = vault_root / "knowledge" / "concepts"
    if not concepts_dir.is_dir():
        return []
    corpus: list[tuple[str, str]] = []
    for fp in sorted(concepts_dir.glob("*.md")):
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        corpus.append((fp.relative_to(vault_root).as_posix(), _extract_concept_digest(text)))
    return corpus


def _batch_corpus(
    corpus: list[tuple[str, str]],
    max_chars: int = TIER2_BATCH_MAX_CHARS,
) -> list[list[tuple[str, str]]]:
    """Greedily pack concept digests into batches whose combined size fits the
    32K-context budget. Never drops an entry (a lone oversized digest gets its
    own batch)."""
    batches: list[list[tuple[str, str]]] = []
    cur: list[tuple[str, str]] = []
    cur_len = 0
    for rel, digest in corpus:
        entry_len = len(rel) + len(digest) + 16
        if cur and cur_len + entry_len > max_chars:
            batches.append(cur)
            cur, cur_len = [], 0
        cur.append((rel, digest))
        cur_len += entry_len
    if cur:
        batches.append(cur)
    return batches


def _build_tier2_prompt(
    soul_context: str,
    corpus_batch: list[tuple[str, str]] | None = None,
) -> str:
    """Tier-2 LLM prompt — semantic contradictions + Tier-A SOUL conflicts.

    BT5 C3: `corpus_batch` (a slice of `_load_concept_corpus`) is injected so the
    model has the actual articles to review. Called with only `soul_context`
    (corpus_batch=None) the prompt degrades to instructions + SOUL, preserving
    the pre-C3 signature.
    """
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
    corpus_block = ""
    if corpus_batch:
        parts = ["--- BEGIN CONCEPT CORPUS (review these articles) ---\n"]
        for rel, digest in corpus_batch:
            parts.append(f"### {rel}\n{digest}\n")
        parts.append("--- END CONCEPT CORPUS ---\n\n")
        corpus_block = "\n".join(parts)
    return (soul_context or "") + corpus_block + instructions


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
    report_notes: list[str] | None = None,
    tier2_batch_max_chars: int = TIER2_BATCH_MAX_CHARS,
    tier2_budget_seconds: int = TIER2_BUDGET_SECONDS,
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
        rel_parts = fp.relative_to(vault_root).parts
        if any(part in _STALE_REF_EXCLUDE_DIRS for part in rel_parts):
            continue
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

    # BT5 C3 — LLM-powered contradiction + SOUL Tier-A conflict, now over a
    # real concept corpus injected in token-budgeted batches (the prompt used
    # to carry none, so this leg reviewed nothing). Phase D dedupe still holds:
    # contradictions dedupe against the SQL fast path AND across batches; SOUL
    # conflicts have no SQL substitute and always surface. A per-batch failure
    # is logged + reported (never the old silent `except: pass`), and the loop
    # stops — a connection-class error means the host went away.
    batches = _batch_corpus(_load_concept_corpus(vault_root), max_chars=tier2_batch_max_chars)
    if not batches:
        # One-call floor: even with no concept corpus, run a single scan so the
        # SOUL-conflict leg (which reasons over the SOUL context, not the
        # corpus) still fires — preserves the pre-C3 single-call contract.
        batches = [[]]

    start = time.monotonic()
    reviewed = 0
    for batch in batches:
        if reviewed > 0 and (time.monotonic() - start) >= tier2_budget_seconds:
            if report_notes is not None:
                report_notes.append(
                    f"Tier-2 LLM scan: reviewed {reviewed}/{len(batches)} concept "
                    f"batches (time budget {tier2_budget_seconds}s reached; "
                    f"{len(batches) - reviewed} deferred to next run)."
                )
            break
        try:
            resp = llm_caller(_build_tier2_prompt(soul_context, batch))
        except Exception as exc:
            log.warning("Tier 2 LLM scan failed on batch %d/%d: %s",
                        reviewed + 1, len(batches), exc)
            if report_notes is not None:
                report_notes.append(
                    f"Tier-2 LLM scan: failed — {type(exc).__name__} "
                    f"(after {reviewed}/{len(batches)} batches)"
                )
            break
        reviewed += 1
        for c in resp.get("contradictions", []):
            files = c.get("files", [])
            if not files:
                continue
            pair = _slugs_from_contradiction_files(files)
            if pair and frozenset(pair) in seen_contradiction_pairs:
                log.info(
                    "Tier 2 contradiction: source=llm dropped (already seen) "
                    "%s vs %s", pair[0], pair[1],
                )
                continue
            if pair:
                seen_contradiction_pairs.add(frozenset(pair))
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
    else:
        # Loop completed without break — all batches reviewed.
        if report_notes is not None:
            report_notes.append(
                f"Tier-2 LLM scan: reviewed {reviewed}/{len(batches)} concept batches."
            )
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

# The kind whose every field is derived from private operating-model text.
SOUL_CONFLICT_KIND = "soul-tier-a-conflict"

# Local-only home for private-derived findings. Gitignored; `vault/health/`
# itself stays tracked so the public report keeps publishing.
PRIVATE_HEALTH_SUBDIR = "private"

# Vault subtrees that are gitignored under the CLAUDE.md rule-9 PRIVATE LAYER.
# A finding ABOUT a file in one of these leaks that file's existence and its
# slug into a tracked report — the same side channel that leaked 69 target
# companies through job-feed manifests in 2026-08. Mirrors .gitignore; keep the
# two in step. Matched against the vault-relative POSIX path.
PRIVATE_VAULT_PREFIXES: tuple[str, ...] = (
    "knowledge/private/",
    "05_atlas/operating-models/",
    "20_projects/prj-job-hunt-2026/",
    "20_projects/prj-job-hunt-2026-REVAMP/",
    "20_projects/prj-boston-move/",
    "20_projects/prj-personal-finance/",
    "20_projects/substack-studio/_private/",
    "30_domains/2026-trips/",
    "30_domains/product-management/the-block-meetings-granola-notes/",
    "10_timeline/",
    "daily/",
    "health/private/",
)

_SOUL_WITHHELD = (
    "detail withheld from this tracked report (SOUL-derived); "
    "see the local-only sidecar named in the header"
)
_PRIVATE_PATH_WITHHELD = (
    "private-subtree finding; path and detail withheld from this tracked "
    "report — see the local-only sidecar named in the header"
)
_PRIVATE_PATH_PLACEHOLDER = "<private vault path withheld>"


def _vault_relative(file: Path) -> str:
    """Best-effort vault-relative POSIX path for a finding's file.

    Tier-1 findings carry absolute paths, Tier-2 vault-relative ones. Anchor on
    the `vault/` segment when present so both shapes compare alike.
    """
    posix = file.as_posix()
    marker = "/vault/"
    if marker in posix:
        return posix.rsplit(marker, 1)[1]
    return posix.lstrip("/")


def is_private_finding(issue: LintIssue) -> bool:
    """True when a finding must not appear in the tracked report.

    Two independent reasons, both observed live in 2026-08 reports:
      1. Its KIND is SOUL-derived — both the quoted `tier_a_item` and the
         model's prose about it reproduce private operating-model text.
      2. Its FILE lives in a gitignored subtree, so merely naming it leaks a
         private note's existence and slug.
    """
    if issue.kind == SOUL_CONFLICT_KIND:
        return True
    rel = _vault_relative(issue.file)
    return any(rel.startswith(prefix) for prefix in PRIVATE_VAULT_PREFIXES)

# Shortest SOUL line worth treating as a fingerprint. Below this, lines are
# generic enough ("Sacred Cows", "Tier-A Truths") that matching them would
# redact ordinary prose.
_SOUL_FINGERPRINT_MIN_CHARS = 40


def _soul_fingerprints(soul_context: str) -> list[str]:
    """Verbatim SOUL lines long enough to identify as quoted private text."""
    seen: set[str] = set()
    for raw in (soul_context or "").splitlines():
        line = raw.strip().lstrip("-*# ").strip()
        if len(line) >= _SOUL_FINGERPRINT_MIN_CHARS:
            seen.add(line)
    return sorted(seen, key=len, reverse=True)


# `health/private/` is deliberately EXCLUDED from the path scrub: the report's
# own header note names the sidecar there, and redacting it would hide the
# pointer to the withheld detail. It stays in the file classifier.
_SCRUBBED_PREFIXES: tuple[str, ...] = tuple(
    prefix for prefix in PRIVATE_VAULT_PREFIXES if prefix != "health/private/"
)


def scrub_private_paths(report: str) -> tuple[str, int]:
    """Redact private vault paths quoted anywhere in the tracked report.

    The file-level classifier only inspects a finding's `file`. A private path
    can also arrive inside the DETAIL of a finding about a PUBLIC file — a
    broken wikilink whose target text is `20_projects/prj-job-hunt-2026/...`,
    for instance, which is how one such reference survived the 2026-09-03
    backfill. Returns `(scrubbed_report, redaction_count)`.
    """
    redactions = 0
    for prefix in _SCRUBBED_PREFIXES:
        pattern = re.compile(r"\S*" + re.escape(prefix) + r"\S*")
        report, n = pattern.subn(_PRIVATE_PATH_PLACEHOLDER, report)
        redactions += n
    return report, redactions


def scrub_soul_quotes(report: str, soul_context: str) -> tuple[str, int]:
    """Redact any verbatim SOUL line that survived into the public report.

    Defence in depth behind the structural split. The split routes the one
    KIND whose content is SOUL-derived into a private sidecar; this catches
    private text quoted from anywhere else — a `contradiction` detail that
    happens to cite SOUL, or a future issue kind nobody remembered to route.

    Returns `(scrubbed_report, redaction_count)`.
    """
    redactions = 0
    for fingerprint in _soul_fingerprints(soul_context):
        if fingerprint in report:
            report = report.replace(fingerprint, "[SOUL text redacted]")
            redactions += 1
    return report, redactions


def partition_private_issues(
    issues: list[LintIssue],
) -> tuple[list[LintIssue], list[LintIssue]]:
    """Split `issues` into (public, private) preserving order.

    Every issue lands in exactly one half — see `is_private_finding`.
    """
    public = [i for i in issues if not is_private_finding(i)]
    private = [i for i in issues if is_private_finding(i)]
    return public, private


def format_private_sidecar(issues: list[LintIssue], *, today: str) -> str:
    """Render the local-only companion holding every withheld finding in full.

    This file is gitignored. It exists so the findings keep their analytical
    value on the machine that can read them, while the tracked report carries
    only the file paths — which are already public in the knowledge graph.
    """
    lines = [
        f"# Knowledge Lint — Withheld (Private) Findings — {today}",
        "",
        "**LOCAL-ONLY.** Gitignored (`vault/health/private/`). Each finding below "
        "either quotes `vault/05_atlas/operating-models/` SOUL text or names a "
        "file in a gitignored subtree — both private under CLAUDE.md rule 9. Do "
        "not paste this content into a tracked file, an issue, or a PR.",
        "",
        f"_{len(issues)} finding(s)._",
        "",
    ]
    for it in issues:
        rel = it.file.as_posix() if it.file.is_absolute() else str(it.file)
        lines.append(f"- **{it.kind}** (T{it.tier}): `{rel}` — {it.detail}")
    lines.append("")
    return "\n".join(lines)


def write_private_sidecar(vault_root: Path, content: str, *, today: str) -> Path:
    """Write the sidecar into the gitignored private health directory."""
    private_dir = vault_root / "health" / PRIVATE_HEALTH_SUBDIR
    private_dir.mkdir(parents=True, exist_ok=True)
    out = private_dir / f"{today}-private-findings.md"
    out.write_text(content, encoding="utf-8")
    return out


def format_report(
    *,
    tier1: Tier1Report,
    tier2: list[LintIssue],
    today: str,
    tier2_notes: list[str] | None = None,
    private_sidecar_path: Path | None = None,
) -> str:
    """Render the TRACKED, public lint report.

    Privacy (2026-09-03), two withholding shapes:

    * `soul-tier-a-conflict` keeps its file path — concepts are already public
      in the knowledge graph — but drops its detail, because the `tier_a_item`
      quote AND the model's own prose both reproduce private SOUL text. The
      2026-08-30 report leaked a base-salary relocation threshold and a named
      target employer through both halves.
    * A finding about a file in a gitignored subtree drops its PATH too: the
      slug alone discloses a private note. Ten reports named
      `knowledge/private/connections/...` this way.

    Full detail for both goes to the gitignored `private_sidecar_path`.

    Counts are unaffected: withheld findings stay in their severity bucket, so
    `lib/lint_report.py:vault_health_summary` still reports them.
    """
    lines = [f"# Knowledge Lint Report — {today}", ""]
    total = tier1.total_issues + len(tier2)
    lines.append(f"_{total} issues found ({tier1.total_issues} structural, {len(tier2)} semantic)._")
    lines.append("")
    # BT5 C3 — surface the Tier-2 LLM leg's actual outcome (ran N batches /
    # deferred / failed / gate-skipped) so a silent skip can never again read
    # as a clean semantic scan.
    if tier2_notes:
        for note in tier2_notes:
            lines.append(f"_{note}_")
        lines.append("")

    _, private_issues = partition_private_issues(list(tier1.issues) + list(tier2))
    if private_issues:
        target = private_sidecar_path.as_posix() if private_sidecar_path else (
            f"vault/health/{PRIVATE_HEALTH_SUBDIR}/{today}-private-findings.md"
        )
        lines.append(
            f"_{len(private_issues)} finding(s) withheld from this tracked report "
            f"(SOUL-derived, or about a file in a gitignored subtree). They remain "
            f"counted below; full detail is in `{target}` (local-only, gitignored)._"
        )
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
            detail = it.detail
            if it.kind == SOUL_CONFLICT_KIND:
                # The concept path is already public in the knowledge graph;
                # only the SOUL-derived detail is withheld.
                detail = _SOUL_WITHHELD
            elif is_private_finding(it):
                # Here the PATH is the leak — naming the file discloses a
                # private note's existence and slug. Withhold both, but keep
                # the row so severity counts stay truthful.
                rel = _PRIVATE_PATH_PLACEHOLDER
                detail = _PRIVATE_PATH_WITHHELD
            lines.append(f"- **{it.kind}** ({'T1' if it.tier == 1 else 'T2'}): `{rel}` — {detail}")
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


def _default_lint_llm_caller_factory(decision: RoutingDecision) -> Callable[[str], dict]:
    """LLM caller bound to a pre-resolved routing decision (BT5 C3), mirroring
    the synthesizer's factory: fast connect / long read, tolerant JSON
    extraction. Returns {} on a response with no JSON object so a malformed
    reply is an empty (not failed) batch."""
    import httpx

    _timeout = httpx.Timeout(600.0, connect=10.0)

    def _call(prompt: str) -> dict:
        if decision.runtime == "ollama":
            resp = httpx.post(
                f"{decision.base_url}/api/chat",
                json={
                    "model": decision.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "think": False,
                    "options": {"num_ctx": 32768, "temperature": 0.0},
                },
                timeout=_timeout,
            )
            resp.raise_for_status()
            text = resp.json()["message"]["content"]
        else:
            resp = httpx.post(
                f"{decision.base_url}/v1/chat/completions",
                json={
                    "model": decision.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
                timeout=_timeout,
            )
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"]
        start_ = text.find("{")
        end_ = text.rfind("}")
        if start_ == -1 or end_ == -1:
            return {"contradictions": [], "soul_conflicts": []}
        try:
            return json.loads(text[start_ : end_ + 1])
        except json.JSONDecodeError:
            return {"contradictions": [], "soul_conflicts": []}

    return _call


def _resolve_lint_tier2_caller(
    logger: logging.Logger,
) -> tuple[Callable[[str], dict] | None, str | None]:
    """BT5 C3 — probe the Tier-2 host once, up front (like the synthesizer).

    Returns (llm_caller, deferral_note). On an unreachable/misconfigured host,
    llm_caller is None and deferral_note carries the honest report line so the
    scan degrades to SQL/regex-only instead of silently claiming a clean run.
    """
    try:
        import tomllib
        with open(Path(__file__).parent.parent / "config.toml", "rb") as f:
            raw_cfg = tomllib.load(f)
        router = HybridRouter.from_config(raw_cfg)
        cfg_notify_on = raw_cfg.get("notifications", {}).get("notify_on")

        async def _preflight() -> RoutingDecision:
            return await router.route_to_macbook(
                task="lint_tier2", wake_timeout_s=90.0, notify_on=cfg_notify_on
            )
        decision = asyncio.run(_preflight())
        return _default_lint_llm_caller_factory(decision), None
    except WOLUnavailable:
        logger.warning("Tier-2 LLM host unreachable — SQL/regex only this run")
        return None, "Tier-2 LLM scan: deferred (host unreachable)."
    except Exception as exc:  # router/config init failure must not kill Tier 1
        logger.warning("Tier-2 LLM router init failed: %s", exc)
        return None, f"Tier-2 LLM scan: unavailable — {type(exc).__name__}."


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
    tier2_notes: list[str] = []
    # Bound unconditionally: the gate below can skip, and the post-report SOUL
    # scrub reads this on every path.
    soul_context = ""
    if tier1.total_issues > 0 or args.full:
        soul_context = build_soul_context(cfg)
        # BT5 C3 — wire the Tier-2 LLM leg for real (probe-first). A down host
        # defers honestly; SQL/regex always run regardless.
        llm_caller, deferral_note = _resolve_lint_tier2_caller(logger)
        if deferral_note:
            tier2_notes.append(deferral_note)
        tier2 = run_tier2(
            cfg.vault_root,
            llm_caller=llm_caller,
            soul_context=soul_context,
            logger=logger,
            report_notes=tier2_notes,
        )
        logger.info(
            "Tier 2: %d issues (soul_context=%s, llm=%s)",
            len(tier2),
            "loaded" if soul_context else "off",
            "wired" if llm_caller else "deferred",
        )
    else:
        # Distinguish "gate-skipped" from "ran without LLM" (BT5 C3).
        tier2_notes.append("Tier-2 LLM scan: skipped by gate (Tier 1 clean, no --full).")

    today = date.today().isoformat()

    # Privacy split (2026-09-03): findings that are SOUL-derived, or that name
    # a file in a gitignored subtree, never enter the tracked report. Both
    # classes leaked live in the 2026-07/08 reports (CLAUDE.md rule 9).
    _, private_issues = partition_private_issues(list(tier1.issues) + list(tier2))
    sidecar_path = (
        cfg.vault_root / "health" / PRIVATE_HEALTH_SUBDIR / f"{today}-private-findings.md"
        if private_issues
        else None
    )
    report = format_report(
        tier1=tier1,
        tier2=tier2,
        today=today,
        tier2_notes=tier2_notes,
        private_sidecar_path=sidecar_path,
    )

    # Defence in depth behind the structural split, for private text that
    # arrives in a field the classifier does not inspect.
    report, soul_redactions = scrub_soul_quotes(report, soul_context)
    report, path_redactions = scrub_private_paths(report)
    if soul_redactions:
        logger.warning(
            "Redacted %d verbatim SOUL quote(s) from the public report — a "
            "non-soul issue kind is leaking private text; fix its emitter.",
            soul_redactions,
        )
    if path_redactions:
        logger.info(
            "Redacted %d private vault path(s) quoted in finding details.",
            path_redactions,
        )

    if not args.dry_run:
        path = write_report(cfg.vault_root, report, today=today)
        logger.info("Report: %s", path)
        if private_issues:
            written = write_private_sidecar(
                cfg.vault_root,
                format_private_sidecar(private_issues, today=today),
                today=today,
            )
            logger.info(
                "Private sidecar (local-only): %s — %d finding(s) withheld from %s",
                written, len(private_issues), path.name,
            )

    # Exit code 0 regardless; daily_driver surfaces CRITICAL/HIGH in morning brief
    notes = f"tier1={tier1.total_issues} tier2={len(tier2)}"
    if tier2_notes:
        notes += " | " + "; ".join(tier2_notes)
    record_run(cfg.log_dir, AGENT_NAME, mode=None,
               status="success", cost_usd=0.0, duration_ms=None, turns=None,
               notes=notes[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
