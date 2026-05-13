#!/usr/bin/env python3
"""Vault Synthesizer — nightly concept + connection article generator (D.2.b).

Runs on MacBook Pro via hybrid_router.route_to_macbook (Qwen3-14B through
LM Studio by default; whatever `routing.task_map["vault_synthesis"]` says
at runtime). For each changed file, retrieves the top-K semantically
similar vault files (via the existing nomic-embed-text index managed by
vault_indexer.py), asks the LLM for concepts + connections, validates
the ≥2 wikilink invariant, writes articles to
`vault/knowledge/concepts/*.md` and `vault/knowledge/connections/*.md`,
and regenerates `vault/knowledge/index.md`.

All writes serialize via FileLock on `vault/knowledge/.lock`.

Design notes:
- Article bodies REQUIRE ≥2 `[[wikilinks]]` — rejected articles are
  counted but not written (no orphan nodes).
- Budget: honors a `budget_seconds` ceiling (plan §3: 45 min). If the
  clock runs out mid-file, returns `status=partial` without writing the
  in-progress article.
- Input changed_files comes from vault_indexer.detect_changed_files().
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
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib import concept_edges
from lib.config import load_config
from lib.filelock import FileLock
from lib.hybrid_router import HybridRouter, WOLUnavailable
from lib.logging_setup import record_run, setup_logger

AGENT_NAME = "vault-synthesizer"
MAX_TURNS = 25
MAX_BUDGET_USD = 0.00
DEFAULT_BUDGET_SECONDS = 45 * 60  # plan §3 (45 min)

MIN_WIKILINKS_PER_ARTICLE = 2
KNOWLEDGE_SUBDIR = "knowledge"
CONCEPTS_SUBDIR = "concepts"
CONNECTIONS_SUBDIR = "connections"
# Phase C (2026-05-01): qa/ is the third article tier, populated by
# `scripts/query.py --file-back`. The synthesizer doesn't write qa/
# articles itself, but it lists them in `index.md` so SessionStart
# injection and downstream consumers see them alongside concepts/connections.
QA_SUBDIR = "qa"

_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
_SLUG_RE = re.compile(r"[^a-z0-9]+")

# --- model_used enum (vs-018) ---
# The valid set of values for SynthesisResult.model_used. The "none" sentinel
# is used when no LLM call completed during the run (e.g., MBP asleep, network
# refused). Downstream consumers (daily-driver brief, manifest readers) can
# branch on the enum without the empty-string sentinel.
MODEL_USED_VALUES = frozenset({"qwen3-14b", "claude-sonnet-4-6", "claude-haiku-4-5", "none"})
MODEL_USED_NONE = "none"

# --- status taxonomy (vs-015, vs-016, vs-017) ---
# The valid set of values for SynthesisResult.status. New in v3.30: "success-empty"
# (ran cleanly, produced no output) and "partial-empty" (some files processed,
# none produced articles). These give downstream consumers (daily-driver brief,
# manifest readers) the signal they need to distinguish "healthy and quiet" from
# "broken and quiet" — which was the Mode 1 silent-empty regression.
STATUS_OK = "ok"
STATUS_PARTIAL = "partial"
STATUS_PARTIAL_EMPTY = "partial-empty"
STATUS_SUCCESS_EMPTY = "success-empty"
STATUS_ERROR = "error"
STATUS_BUDGET_EXHAUSTED = "budget-exhausted"
STATUS_WOL_DEFERRED = "wol-deferred"
STATUS_VALUES = frozenset({
    STATUS_OK, STATUS_PARTIAL, STATUS_PARTIAL_EMPTY, STATUS_SUCCESS_EMPTY,
    STATUS_ERROR, STATUS_BUDGET_EXHAUSTED, STATUS_WOL_DEFERRED,
})


def _normalize_model_name(name: str) -> str:
    """Map raw model strings (which may include version suffixes) to the eval enum."""
    if not name:
        return MODEL_USED_NONE
    n = name.lower()
    if "qwen" in n:
        return "qwen3-14b"
    if "haiku" in n:
        return "claude-haiku-4-5"
    if "sonnet" in n:
        return "claude-sonnet-4-6"
    return MODEL_USED_NONE


@dataclass
class SynthesisResult:
    status: str                       # see STATUS_VALUES: "ok" | "partial" | "partial-empty" | "success-empty" | "budget-exhausted" | "wol-deferred" | "error"
    concepts_written: int = 0
    connections_written: int = 0
    rejected_count: int = 0
    files_processed: int = 0
    duration_seconds: float = 0.0
    error: str = ""
    warnings: list[str] = field(default_factory=list)
    # Phase D (v3.20.0, 2026-05-01) — typed reasoning edges + manifest.
    edges_written: int = 0
    edges_rejected: int = 0
    model_used: str = MODEL_USED_NONE
    wol_status: str = ""              # "mbp_awake" | "api_fallback" | "wol_deferred"
    run_id: str = ""                  # ISO timestamp; matches synth-manifest run_id


# ─── pure helpers ──────────────────────────────────────────────────────────

def extract_wikilinks(body: str) -> list[str]:
    return _WIKILINK_RE.findall(body)


def count_wikilinks(body: str) -> int:
    return len(extract_wikilinks(body))


# Forbidden placeholder strings — if the body contains any of these, the article
# was emitted without real evidence and must be rejected (Tier 1 retrofit
# 2026-05-13). "Evidence pending" was previously hardcoded by
# format_connection_article — defense in depth catches any path that still
# leaks placeholder copy.
_FORBIDDEN_PLACEHOLDERS = ("Evidence pending", "(to be filled)")


def validate_article_body(body: str) -> bool:
    if count_wikilinks(body) < MIN_WIKILINKS_PER_ARTICLE:
        return False
    return not any(p in body for p in _FORBIDDEN_PLACEHOLDERS)


def _slugify(title: str) -> str:
    s = _SLUG_RE.sub("-", title.lower()).strip("-")
    return s or "untitled"


def format_concept_article(
    *,
    title: str,
    definition: str,
    context: str,
    examples: list[str],
    related: list[str],
    sources: list[str] | None = None,
    evidence: list[str] | None = None,
    today: str,
) -> str:
    sources = sources or []
    evidence = evidence or []
    yaml_sources = "\n".join(f"  - {s}" for s in sources) or "  - "
    related_links = " ".join(f"[[{r}]]" for r in related) or ""
    ex_block = "\n".join(f"- {e}" for e in examples) or "- (no examples captured yet)"
    # Tier 1 retrofit (2026-05-13): render verbatim quotes from source files as
    # blockquotes. When the LLM provided no evidence, render nothing — the
    # validator will reject the article on the connection side via the
    # forbidden-placeholder check.
    if evidence:
        ev_block = "\n\n".join(f"> {q}" for q in evidence)
    else:
        ev_block = "_No verbatim evidence captured this run._"

    return (
        f"---\n"
        f"title: \"{title}\"\n"
        f"type: concept\n"
        f"sources:\n{yaml_sources}\n"
        f"tags: [auto-generated, phase-6]\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        f"---\n\n"
        f"## Definition\n\n{definition}\n\n"
        f"## Context\n\n{context}\n\n"
        f"## Evidence\n\n{ev_block}\n\n"
        f"## Examples\n\n{ex_block}\n\n"
        f"## Related Concepts\n\n{related_links}\n"
    )


def format_connection_article(
    *,
    title: str,
    synthesis: str,
    concepts: list[str],
    implications: list[str],
    evidence: dict[str, list[str]] | None = None,
    today: str,
) -> str:
    """Render a connection article with per-concept evidence blocks.

    Tier 1 retrofit (2026-05-13): `evidence` is a {concept_title: [quotes]}
    mapping. When the LLM supplies verbatim quotes per linked concept, they
    render as blockquotes under each thread. When `evidence=None` or a
    concept is missing from the map, the thread surfaces an honest
    "no evidence supplied" line — which `validate_article_body` then catches
    via the forbidden-placeholder check, rejecting the article. The prior
    behavior of hardcoding "Evidence pending." per concept was the root
    cause of the empty-thread regression.
    """
    evidence = evidence or {}
    connects_yaml = "\n".join(f"  - {c}" for c in concepts) or "  - "
    thread_blocks: list[str] = []
    for c in concepts:
        quotes = evidence.get(c) or []
        if quotes:
            quote_block = "\n\n".join(f"> {q}" for q in quotes)
        else:
            # Honest, non-forbidden placeholder. Article still gets rejected
            # by the validator if all threads are empty (no quotes) — see
            # _FORBIDDEN_PLACEHOLDERS for the exact failure surface.
            quote_block = "_No verbatim evidence supplied._"
        thread_blocks.append(f"### [[{c}]]\n\n{quote_block}")
    threads = "\n\n".join(thread_blocks)
    implications_block = "\n".join(f"- {i}" for i in implications) or "_(implications not supplied)_"

    return (
        f"---\n"
        f"title: \"{title}\"\n"
        f"type: connection\n"
        f"connects:\n{connects_yaml}\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        f"---\n\n"
        f"## Synthesis\n\n{synthesis}\n\n"
        f"## Threads\n\n{threads}\n\n"
        f"## Implications\n\n{implications_block}\n"
    )


def regenerate_index(knowledge_root: Path) -> Path:
    """Rebuild `vault/knowledge/index.md` from disk.

    Phase C (2026-05-01): includes a third `## Q&A` section listing files
    in `qa/`, which `scripts/query.py --file-back` populates. qa/ is
    skipped silently if the directory does not exist yet.
    """
    index_path = knowledge_root / "index.md"
    concepts_dir = knowledge_root / CONCEPTS_SUBDIR
    connections_dir = knowledge_root / CONNECTIONS_SUBDIR
    qa_dir = knowledge_root / QA_SUBDIR

    def _collect(sub: Path, label: str) -> list[str]:
        if not sub.exists():
            return []
        lines: list[str] = []
        for p in sorted(sub.glob("*.md")):
            text = p.read_text(encoding="utf-8", errors="replace")
            title_match = re.search(r'^title:\s*"?([^"\n]+)"?', text, flags=re.MULTILINE)
            title = title_match.group(1).strip() if title_match else p.stem
            rel = p.relative_to(knowledge_root).as_posix()
            lines.append(f"- [[{rel}|{title}]]")
        return lines

    body = ["# Knowledge Index\n", "_Auto-generated by vault_synthesizer. Do not edit by hand._\n"]
    body.append("\n## Concepts\n")
    body += _collect(concepts_dir, "concept") or ["- _(none yet)_"]
    body.append("\n## Connections\n")
    body += _collect(connections_dir, "connection") or ["- _(none yet)_"]
    if qa_dir.exists():
        body.append("\n## Q&A\n")
        body += _collect(qa_dir, "qa") or ["- _(none yet)_"]

    index_path.write_text("\n".join(body) + "\n", encoding="utf-8")
    return index_path


def write_synth_manifest(
    *,
    vault_root: Path,
    result: "SynthesisResult",
    today: str,
) -> Path:
    """Write `vault/health/synth-manifest-{today}.json` from a result.

    Phase D — mirrors OB1's per-run manifest pattern. The synth-manifest
    is the canonical "what did the synthesizer do this run?" record. The
    daily-driver morning brief reads the latest one via `lib.lint_report`.

    Pure function — no I/O state outside the named output path. Atomic
    write via tmp-then-rename so partial files never surface.
    """
    health = vault_root / "health"
    health.mkdir(parents=True, exist_ok=True)
    path = health / f"synth-manifest-{today}.json"
    payload = {
        "run_id": result.run_id,
        "files_processed": result.files_processed,
        "concepts_written": result.concepts_written,
        "connections_written": result.connections_written,
        "edges_written": result.edges_written,
        "edges_rejected": result.edges_rejected,
        "rejected_count": result.rejected_count,
        "duration_seconds": round(result.duration_seconds, 2),
        "model_used": result.model_used,
        "wol_status": result.wol_status,
        "status": result.status,
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
    )
    tmp.replace(path)
    return path


# ─── orchestration ────────────────────────────────────────────────────────

def _load_existing_concept_titles(knowledge_root: Path, cap: int = 200) -> list[str]:
    """Read existing concept titles from frontmatter for canonicalization hints.

    Tier 1 retrofit (2026-05-13): the LLM previously had no visibility into
    what concept slugs already existed, which is why we ended up with
    daily-drive-agent vs daily-driver-agent and five vibe-coding variants.
    Injecting current titles into the prompt lets the model reuse the
    canonical name rather than minting a new one. Cap at 200 to keep the
    prompt under budget.
    """
    concepts_dir = knowledge_root / CONCEPTS_SUBDIR
    if not concepts_dir.exists():
        return []
    titles: list[str] = []
    for f in sorted(concepts_dir.glob("*.md")):
        try:
            head = f.read_text(encoding="utf-8", errors="replace")[:300]
        except OSError:
            continue
        m = re.search(r'^title:\s*"?([^"\n]+)"?', head, flags=re.MULTILINE)
        if m:
            titles.append(m.group(1).strip())
        if len(titles) >= cap:
            break
    return titles


# Top-level vault folders the synthesizer treats as distinct PARA-style
# domains for the cross-domain preference rule. A connection that links
# concepts whose source files originate in different folders here is
# considered "cross-domain" and preferred over within-domain connections.
_CROSS_DOMAIN_FOLDERS = (
    "00_inbox",
    "10_timeline",
    "20_projects",
    "40_knowledge",
    "05_atlas",
)


def _build_synthesis_prompt(
    *,
    primary_file_rel: str,
    primary_text: str,
    similar: list[dict[str, Any]],
    existing_titles: list[str] | None = None,
) -> str:
    """Construct the synthesis LLM prompt.

    Tier 1 retrofit (2026-05-13) — see
    `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/
    job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md`
    for the full intent spec. Key changes from v1:
      1. Quote-first — every concept needs ≥2 verbatim quotes from sources,
         every connection needs per-concept evidence quotes, before any prose.
      2. Canonicalization — existing concept titles are injected so the LLM
         reuses slugs rather than minting near-duplicates.
      3. Cross-domain preference — model is told to prefer connections whose
         member concepts span different top-level vault folders.
      4. Chunk excerpt grew 200 → 800 chars so the LLM sees arguments, not
         fragments.
      5. Forbidden-phrase list explicit; rejection happens in
         `validate_article_body`.
    """
    existing_titles = existing_titles or []
    primary_folder = primary_file_rel.split("/", 1)[0] if "/" in primary_file_rel else ""

    sim_block_parts: list[str] = []
    for s in similar:
        sim_path = s.get("file_path", "")
        sim_folder = sim_path.split("/", 1)[0] if "/" in sim_path else ""
        sim_block_parts.append(
            f"- file: {sim_path}\n"
            f"  folder: {sim_folder}\n"
            f"  excerpt: {str(s.get('chunk_text', ''))[:800]}"
        )
    sim_block = "\n".join(sim_block_parts) or "  (no similar files retrieved)"

    if existing_titles:
        titles_inline = ", ".join(f'"{t}"' for t in existing_titles)
        canonical_block = (
            "EXISTING CONCEPT TITLES (use these slugs verbatim if your synthesis "
            "matches one of them — do NOT mint a near-duplicate slug; the "
            "synthesizer rejects duplicates downstream):\n"
            f"{titles_inline}\n\n"
        )
    else:
        canonical_block = ""

    return (
        "You are the vault synthesizer for Sean Winslow's personal knowledge "
        "vault. Your job is not to summarize. Your job is to surface "
        "**non-obvious cross-domain patterns** that Sean would not notice "
        "manually — connections across life-systems, creative-studio, "
        "job-hunt-2026, and Superuser Pack infrastructure.\n\n"
        "Three rules govern every article you emit:\n"
        "  1. EVIDENCE FIRST — every claim must be grounded in a verbatim "
        "quote from a source file. No verbatim quote → no claim.\n"
        "  2. REUSE > REMINT — if a concept already has a slug in the "
        "canonical list below, reuse the exact title. Do not invent "
        "near-duplicate names.\n"
        "  3. CROSS-DOMAIN > WITHIN-DOMAIN — when proposing connections, "
        "prefer those whose member concepts originate in DIFFERENT top-level "
        "vault folders (life-systems × creative-studio × job-hunt × 40_knowledge "
        "× 05_atlas). A connection of three concepts all from the same folder "
        "is a within-domain summary, not a discovery.\n\n"
        f"Primary file: {primary_file_rel}  (folder: {primary_folder})\n"
        f"---\n{primary_text[:3000]}\n---\n\n"
        "Semantically similar vault files (note the `folder` field — use it "
        "to identify cross-domain pairs):\n"
        f"{sim_block}\n\n"
        f"{canonical_block}"
        "FORBIDDEN PHRASES — articles containing any of these are rejected:\n"
        '  - "Evidence pending"\n'
        '  - "(to be filled)"\n\n'
        "Return ONLY a JSON object with this shape (lists may be empty):\n\n"
        "{\n"
        "  \"concepts\": [\n"
        "    {\n"
        "      \"title\": string,                   // reuse from canonical list if applicable\n"
        "      \"definition\": string,              // 2-3 sentences, grounded in the quotes below\n"
        "      \"context\": string,                 // why it matters to Sean specifically\n"
        "      \"evidence\": [string],              // ≥2 VERBATIM quotes from the primary or similar files\n"
        "      \"examples\": [string],              // concrete from source material\n"
        "      \"related\": [string]                // ≥2 exact titles of related concepts\n"
        "    }\n"
        "  ],\n"
        "  \"connections\": [\n"
        "    {\n"
        "      \"title\": string,\n"
        "      \"synthesis\": string,               // 1-2 sentences naming the cross-domain pattern\n"
        "      \"concepts\": [string],              // exact titles, ≥3\n"
        "      \"evidence\": {                      // per-concept verbatim quotes\n"
        "        \"<concept title>\": [string]      // ≥1 verbatim quote from a source file that grounds this concept's role\n"
        "      },\n"
        "      \"implications\": [string],          // how this informs future work\n"
        "      \"source_folders\": [string],        // the distinct top-level vault folders the member concepts span\n"
        "      \"relations\": [                     // OPTIONAL — typed edges between concept pairs\n"
        "        {\n"
        "          \"from\": string,                // exact concept title\n"
        "          \"to\": string,                  // exact concept title (must differ from `from`)\n"
        "          \"relation\": \"supports|contradicts|evolved_into|supersedes|depends_on|related_to\",\n"
        "          \"confidence\": number           // optional, 0.0-1.0\n"
        "        }\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "CRITICAL CONSTRAINTS:\n"
        "  - every concept MUST list ≥2 verbatim quotes in `evidence` AND ≥2 related titles\n"
        "  - every connection MUST list ≥3 concept titles AND provide `evidence` for at least each concept it lists\n"
        "  - quotes MUST be exact substrings of the primary or similar file content shown above — paraphrasing is rejected downstream\n"
        "  - if you cannot find ≥2 verbatim quotes for a concept, OMIT that concept rather than guessing\n"
        "  - if you cannot identify a clear typed relation between two concepts, omit that pair from `relations`\n"
        "  - prefer fewer, well-grounded articles over many shallow ones — empty arrays are valid output"
    )


def run_synthesis(
    *,
    vault_root: Path,
    changed_files: list[Path],
    llm_caller: Callable[..., dict],
    retriever: Callable[..., list[dict[str, Any]]],
    now_iso: str | None = None,
    budget_seconds: int = DEFAULT_BUDGET_SECONDS,
    top_k: int = 5,
    db_conn: sqlite3.Connection | None = None,
    classifier_version: str | None = None,
    logger: logging.Logger | None = None,
) -> SynthesisResult:
    """Drive the synthesis pass end-to-end.

    `llm_caller(prompt)` must return a dict with `concepts` and `connections`.
    `retriever(query, top_k)` returns [{file_path, chunk_text, similarity}].

    Phase D (v3.20.0): when `db_conn` is provided, parses each connection's
    `relations` payload and inserts typed edges into `concept_edges` via
    `lib.concept_edges.insert_edge()`. Bad relation values are logged and
    dropped — articles still write. When `db_conn=None`, edge writes are
    skipped silently (pure unit-test path / fresh-vault path before
    vault_indexer has run).
    """
    # Fail loud if Pushover creds are missing — the notification subsystem is
    # how this agent communicates failures. Without creds, downstream failures
    # become invisible (vs-019).
    from lib.pushover import ensure_credentials_or_raise
    ensure_credentials_or_raise()

    start = time.monotonic()
    today = now_iso or date.today().isoformat()
    knowledge_root = vault_root / KNOWLEDGE_SUBDIR
    concepts_dir = knowledge_root / CONCEPTS_SUBDIR
    connections_dir = knowledge_root / CONNECTIONS_SUBDIR
    concepts_dir.mkdir(parents=True, exist_ok=True)
    connections_dir.mkdir(parents=True, exist_ok=True)
    lock_path = knowledge_root / ".lock"
    log = logger or logging.getLogger(AGENT_NAME)

    result = SynthesisResult(status="ok")
    # Phase D: a single ISO timestamp for the whole run, used as the
    # `source_synth_run` value on every edge row written by this run AND
    # as the `run_id` field in the synth-manifest. They match by construction.
    result.run_id = datetime.now().isoformat(timespec="seconds")

    if budget_seconds <= 0 or not changed_files:
        result.status = "budget-exhausted" if budget_seconds <= 0 else "ok"
        result.duration_seconds = time.monotonic() - start
        # Still regen index so downstream consumers see something.
        with FileLock(lock_path, exclusive=True, timeout=10.0):
            regenerate_index(knowledge_root)
        return result

    # Tier 1 retrofit (2026-05-13): load existing concept titles once per
    # run for canonicalization hints in the prompt. Cap at 200 to keep
    # prompt size bounded.
    existing_titles = _load_existing_concept_titles(knowledge_root)

    files_attempted = 0
    files_succeeded = 0

    for fp in changed_files:
        if time.monotonic() - start >= budget_seconds:
            result.status = STATUS_PARTIAL
            result.warnings.append(f"budget ran out after {result.files_processed} files")
            break

        files_attempted += 1

        try:
            primary_text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            result.warnings.append(f"read failed {fp}: {exc}")
            continue
        result.files_processed += 1

        try:
            similar = retriever(primary_text[:2000], top_k)
        except Exception as exc:
            similar = []
            result.warnings.append(f"retrieval failed for {fp.name}: {exc}")

        prompt = _build_synthesis_prompt(
            primary_file_rel=str(fp.relative_to(vault_root)),
            primary_text=primary_text,
            similar=similar,
            existing_titles=existing_titles,
        )
        try:
            parsed = llm_caller(prompt)
        except Exception as exc:
            result.warnings.append(f"LLM call failed for {fp.name}: {exc}")
            continue

        files_succeeded += 1

        concepts = parsed.get("concepts", []) or []
        connections = parsed.get("connections", []) or []

        with FileLock(lock_path, exclusive=True, timeout=30.0):
            for c in concepts:
                title = c.get("title", "").strip()
                if not title:
                    result.rejected_count += 1
                    continue
                body = format_concept_article(
                    title=title,
                    definition=c.get("definition", ""),
                    context=c.get("context", ""),
                    examples=list(c.get("examples", [])),
                    related=list(c.get("related", [])),
                    sources=[str(fp.relative_to(vault_root))],
                    evidence=list(c.get("evidence", [])),
                    today=today,
                )
                if not validate_article_body(body):
                    result.rejected_count += 1
                    continue
                (concepts_dir / f"{_slugify(title)}.md").write_text(body, encoding="utf-8")
                result.concepts_written += 1

            for conn in connections:
                title = conn.get("title", "").strip()
                concept_list = list(conn.get("concepts", []))
                if not title or len(concept_list) < 3:
                    result.rejected_count += 1
                    continue
                # Tier 1 retrofit (2026-05-13): route per-concept evidence
                # quotes from the LLM into the formatter. The LLM is now
                # required to emit `evidence: {<concept_title>: [quotes]}`
                # per the new prompt schema. Defensive cast in case the
                # model returns a non-dict.
                raw_evidence = conn.get("evidence") or {}
                if not isinstance(raw_evidence, dict):
                    raw_evidence = {}
                connection_evidence: dict[str, list[str]] = {
                    str(k): [str(q) for q in (v or []) if isinstance(q, str)]
                    for k, v in raw_evidence.items()
                }
                body = format_connection_article(
                    title=title,
                    synthesis=conn.get("synthesis", ""),
                    concepts=concept_list,
                    implications=list(conn.get("implications", [])),
                    evidence=connection_evidence,
                    today=today,
                )
                if not validate_article_body(body):
                    result.rejected_count += 1
                    continue
                (connections_dir / f"{_slugify(title)}.md").write_text(body, encoding="utf-8")
                result.connections_written += 1

                # Phase D — typed reasoning edges. After the article writes,
                # parse the LLM's typed `relations` and INSERT OR IGNORE
                # rows into concept_edges. Each bad relation is logged and
                # dropped; the article still writes. db_conn=None means
                # the caller opted out of edge writes (test path / fresh
                # vault before vault_indexer ran).
                if db_conn is None:
                    continue
                for edge in conn.get("relations", []) or []:
                    raw_from = (edge.get("from") or "").strip()
                    raw_to = (edge.get("to") or "").strip()
                    relation = (edge.get("relation") or "").strip()
                    if not (raw_from and raw_to and relation):
                        continue
                    from_slug = _slugify(raw_from)
                    to_slug = _slugify(raw_to)
                    if from_slug == to_slug:
                        # Self-edge — silently skip rather than count as
                        # rejected, since this is usually a slug-collision
                        # artefact of the LLM emitting near-duplicate titles.
                        continue
                    confidence_raw = edge.get("confidence")
                    try:
                        confidence = (
                            float(confidence_raw) if confidence_raw is not None else None
                        )
                    except (TypeError, ValueError):
                        confidence = None
                    try:
                        inserted = concept_edges.insert_edge(
                            db_conn,
                            from_slug=from_slug,
                            to_slug=to_slug,
                            relation=relation,
                            confidence=confidence,
                            classifier_version=classifier_version,
                            source_synth_run=result.run_id,
                        )
                    except ValueError as exc:
                        result.edges_rejected += 1
                        log.warning(
                            "edge rejected (from=%s to=%s relation=%s): %s",
                            from_slug, to_slug, relation, exc,
                        )
                        continue
                    if inserted:
                        result.edges_written += 1

    with FileLock(lock_path, exclusive=True, timeout=10.0):
        regenerate_index(knowledge_root)

    # --- run-level status promotion (vs-015, vs-016, vs-017) ---
    # Promote result.status based on what actually happened during the per-file loop.
    # Done at the end so the existing "set status=partial on budget timeout" path
    # can compose with this (if status is already an error-class value, leave it).
    if result.status not in {STATUS_ERROR, STATUS_BUDGET_EXHAUSTED, STATUS_WOL_DEFERRED}:
        if files_attempted == 0:
            # Nothing to do this run; no signal to promote
            pass
        elif files_succeeded == 0:
            # Every per-file LLM call failed → run-level error
            result.status = STATUS_ERROR
        elif files_succeeded < files_attempted and result.concepts_written == 0:
            # Some files processed, none produced articles → partial-empty
            result.status = STATUS_PARTIAL_EMPTY
        elif files_succeeded < files_attempted:
            # Some files succeeded with output, some failed → partial
            result.status = STATUS_PARTIAL
        elif result.concepts_written == 0:
            # All files succeeded but no concept articles were written → success-empty
            result.status = STATUS_SUCCESS_EMPTY
        else:
            result.status = STATUS_OK

    result.duration_seconds = time.monotonic() - start
    return result


# ─── CLI entry point (production path) ────────────────────────────────────

def _default_llm_caller_factory(
    router: HybridRouter,
    manifest_state: dict[str, str] | None = None,
) -> Callable[..., dict]:
    """Return an LLM caller that hits the routed MacBook Pro endpoint.

    Phase D: when `manifest_state` is provided, the first successful
    routing decision mutates `model_used` and `wol_status` on the dict
    so the synthesizer can later persist them in the synth-manifest.
    Caller path: main() builds the dict, passes it in, and reads from
    it after run_synthesis returns.
    """
    import httpx

    def _call(prompt: str, max_tokens: int = 2000) -> dict:
        async def go():
            return await router.route_to_macbook(
                task="vault_synthesis", wake_timeout_s=90.0
            )
        decision = asyncio.run(go())
        if manifest_state is not None and not manifest_state.get("model_used"):
            manifest_state["model_used"] = _normalize_model_name(decision.model)
            manifest_state["wol_status"] = (
                "mbp_awake" if decision.machine == "macbook_pro"
                else "api_fallback"
            )
        resp = httpx.post(
            f"{decision.base_url}/v1/chat/completions",
            json={
                "model": decision.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "stream": False,
            },
            timeout=600.0,
        )
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"]
        start_ = text.find("{")
        end_ = text.rfind("}")
        if start_ == -1 or end_ == -1:
            return {"concepts": [], "connections": []}
        try:
            return json.loads(text[start_ : end_ + 1])
        except json.JSONDecodeError:
            return {"concepts": [], "connections": []}

    return _call


def _default_retriever_factory(vault_root: Path) -> Callable[..., list[dict[str, Any]]]:
    """Re-use the existing vault_indexer search() against the live SQLite index."""
    from agents.vault_indexer import get_db_path, search

    def _retrieve(query: str, top_k: int = 5) -> list[dict[str, Any]]:
        db = get_db_path(vault_root)
        if not db.exists():
            return []
        return asyncio.run(search(query, db, top_k=top_k))

    return _retrieve


def main() -> int:
    parser = argparse.ArgumentParser(description="Vault Synthesizer Agent")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--budget-seconds", type=int, default=DEFAULT_BUDGET_SECONDS)
    args = parser.parse_args()

    cfg = load_config()
    logger = setup_logger(AGENT_NAME, cfg.log_dir, cfg.log_level)

    # Import lazily so tests needn't stand up config
    from agents.vault_indexer import detect_changed_files, read_indexer_state, write_indexer_state, INDEXER_STATE_FILENAME

    state_path = cfg.vault_root / INDEXER_STATE_FILENAME
    prior = read_indexer_state(state_path)
    changed, new_state = detect_changed_files(cfg.vault_root, prior)

    logger.info("synthesis: %d changed files (budget %ds, dry_run=%s)",
                len(changed), args.budget_seconds, args.dry_run)

    if args.dry_run:
        for p in changed[:20]:
            logger.info("  - %s", p.relative_to(cfg.vault_root))
        return 0

    try:
        import tomllib
        with open(Path(__file__).parent.parent / "config.toml", "rb") as f:
            raw_cfg = tomllib.load(f)
        router = HybridRouter.from_config(raw_cfg)
    except Exception as exc:
        logger.error("Router init failed: %s", exc)
        return 1

    # Phase D — capture model_used / wol_status for the synth-manifest.
    manifest_state: dict[str, str] = {}
    llm = _default_llm_caller_factory(router, manifest_state=manifest_state)
    retriever = _default_retriever_factory(cfg.vault_root)

    # Phase D — open the .vault-index.db connection so run_synthesis can
    # write concept_edges rows. concept_edges.get_connection() applies
    # init_db() (idempotent) so the table exists even on a fresh vault.
    from agents.vault_indexer import get_db_path
    db_path = get_db_path(cfg.vault_root)
    db_conn = concept_edges.get_connection(db_path)
    today_iso = date.today().isoformat()

    start_ns = time.monotonic_ns()
    try:
        result = run_synthesis(
            vault_root=cfg.vault_root,
            changed_files=changed,
            llm_caller=llm,
            retriever=retriever,
            budget_seconds=args.budget_seconds,
            db_conn=db_conn,
            classifier_version=(
                f"{manifest_state.get('model_used', 'unknown')}/{today_iso}"
            ),
            logger=logger,
        )
    except WOLUnavailable as exc:
        logger.warning("WOL unavailable — deferring: %s", exc)
        # Phase D: still write a manifest so the daily-driver brief sees
        # the deferral, not silent absence.
        deferred_result = SynthesisResult(status="wol-deferred")
        deferred_result.run_id = datetime.now().isoformat(timespec="seconds")
        deferred_result.wol_status = "wol_deferred"
        try:
            write_synth_manifest(
                vault_root=cfg.vault_root, result=deferred_result, today=today_iso
            )
        except OSError as werr:
            logger.warning("synth-manifest write failed on deferral: %s", werr)
        db_conn.close()
        record_run(cfg.log_dir, AGENT_NAME, mode=None, status="deferred",
                   cost_usd=0.0, duration_ms=None, turns=None,
                   notes="wol-unavailable")
        return 0
    except Exception as exc:
        logger.error("synthesis failed: %s", exc)
        db_conn.close()
        record_run(cfg.log_dir, AGENT_NAME, mode=None, status="error",
                   cost_usd=0.0, duration_ms=None, turns=None, notes=str(exc)[:200])
        return 1
    finally:
        # Idempotent close — safe even after the except branches above.
        try:
            db_conn.close()
        except Exception:
            pass

    duration_ms = (time.monotonic_ns() - start_ns) // 1_000_000

    # Phase D — copy model_used / wol_status into the result, write manifest.
    result.model_used = manifest_state.get("model_used", MODEL_USED_NONE)
    result.wol_status = manifest_state.get("wol_status", "")
    try:
        manifest_path = write_synth_manifest(
            vault_root=cfg.vault_root, result=result, today=today_iso
        )
        logger.info("synth-manifest written: %s", manifest_path)
    except OSError as werr:
        logger.warning("synth-manifest write failed: %s", werr)

    # Persist new state only on a successful / partial run
    if result.status in {"ok", "partial"}:
        write_indexer_state(state_path, new_state)

    logger.info(
        "synthesis %s concepts=%d connections=%d rejected=%d "
        "edges=%d edges_rejected=%d duration=%.1fs",
        result.status, result.concepts_written, result.connections_written,
        result.rejected_count, result.edges_written, result.edges_rejected,
        result.duration_seconds,
    )

    record_run(cfg.log_dir, AGENT_NAME, mode=None,
               status="success" if result.status in {"ok", "partial"} else result.status,
               cost_usd=0.0, duration_ms=duration_ms, turns=None,
               notes=(
                   f"concepts={result.concepts_written} "
                   f"connections={result.connections_written} "
                   f"rejected={result.rejected_count} "
                   f"edges={result.edges_written}"
               ))

    return 0


if __name__ == "__main__":
    sys.exit(main())
