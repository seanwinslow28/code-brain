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
from lib.retrieval_diversity import build_embedding_query, cluster_and_sample

AGENT_NAME = "vault-synthesizer"
MAX_TURNS = 25
MAX_BUDGET_USD = 0.00
DEFAULT_BUDGET_SECONDS = 45 * 60  # plan §3 (45 min)

# Tier 2 retrofit (2026-05-16) — cluster-and-sample retrieval (TopClustRAG,
# SIGIR 2025). Retrieve a larger pool, cluster with HDBSCAN, sample per
# cluster so cross-domain content surfaces structurally instead of being
# crowded out by the densest concept region (agent-health/fleet density).
# See vault/20_projects/prj-job-hunt-2026/.../2026-05-13-vault-synthesizer-
# retrofit-tiers.md §Tier 2 for the full intent spec.
RETRIEVAL_POOL_SIZE = 50
RETRIEVAL_K_PER_CLUSTER = 2
RETRIEVAL_MIN_CLUSTER_SIZE = 3
RETRIEVAL_MAX_NOISE = 3
RETRIEVAL_MAX_TOTAL = 15

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
    # Tier 2 retrofit (2026-05-16) — sum of real HDBSCAN clusters HDBSCAN
    # found across every per-file retrieval pool this run. Surfaces in the
    # synth-manifest as `clusters_sampled`. ≥3 per run is the verification
    # gate that the cluster-and-sample path is doing real work (vs. always
    # falling back to the top-rank slice).
    clusters_sampled: int = 0
    # Tier 1.5 retrofit (2026-05-20) — per-reason rejection counter and
    # thin-source skip counter. `rejected_reasons` is keyed by stable codes
    # returned by `evaluate_article_depth` so manifest consumers can tell
    # "low concept_written tonight because retrieval was thin" from "low
    # because the LLM produced restated-prompt definitions".
    rejected_reasons: dict[str, int] = field(default_factory=dict)
    skipped_thin_source: int = 0


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


# ─── Tier 1.5 — insight-depth gate (2026-05-20) ────────────────────────────
#
# Pre-1.5 the validator only checked wikilink count + the forbidden
# "Evidence pending" string. That let median-quality output through: CLI-
# snippet evidence, restated-prompt definitions, two-sentence stub articles
# (see vault/knowledge/concepts/automation-routines.md written 2026-05-19).
# `evaluate_article_depth` is the new semantic gate. It dispatches by
# `type: concept` / `type: connection` in the frontmatter and returns a
# (passed, reason) tuple. The synth loop attributes rejections to
# `result.rejected_reasons` so the synth-manifest carries operator-grade
# signal about *why* output volume changes night to night.

_MIN_DEFINITION_SENTENCES = 3
_MIN_DEFINITION_CHARS = 250
_MIN_QUOTE_CHARS = 60
_MIN_QUOTES_PER_CONCEPT = 2
_MIN_SYNTHESIS_SENTENCES = 3
_MIN_SYNTHESIS_CHARS = 200
_MIN_THREAD_QUOTE_CHARS = 60
_MIN_IMPLICATIONS = 2
_MIN_IMPLICATION_CHARS = 80
# Cluster pool below this size means the retriever could not surface
# enough cross-domain candidates to ground a real article — skip the LLM
# call entirely rather than produce shallow output (Tier 1.5).
_MIN_SIMILAR_FOR_LLM = 2

# Restatement tells — phrases that almost always indicate the LLM is
# paraphrasing the prompt rather than naming a mechanism. Collected from
# 2026-05-13 → 2026-05-19 nightly output where the median article read like
# "a collection of X designed to Y that ensures Z."
_RESTATEMENT_PHRASES = (
    "a collection of",
    "a set of",
    "a series of",
    "a group of",
    "designed to support",
    "designed to ensure",
    "streamlines his workflow",
    "streamlines the workflow",
    "ensures consistency",
    "ensures efficiency",
    "ensures that",
    "is a process for",
    "is a system that",
    "is the practice of",
    "refers to the idea",
    "encompasses the",
    "this concept is critical",
    "this is critical because",
    "this would benefit sean",
)

# Verbal-claim markers — a substantive quote almost always contains one
# of these. CLI commands and frontmatter slices don't.
_VERB_MARKERS = (
    " is ", " are ", " was ", " were ", " be ", " been ", " being ",
    " do ", " does ", " did ", " has ", " have ", " had ",
    " produces ", " requires ", " causes ", " depends ", " means ",
    " fails ", " enables ", " prevents ", " allows ", " blocks ",
    " improves ", " reduces ", " breaks ", " triggers ", " affects ",
    " surfaces ", " emerges ", " gates ", " forces ", " replaces ",
    " happens ", " becomes ", " remains ", " stops ", " continues ",
    " shifted ", " shows ", " demonstrates ", " indicates ",
)

# Strong tells that a quote is purely code/CLI rather than prose.
_CODE_LINE_PREFIXES = (
    "$", "#!/", "cd ", "ls ", "rm ", "cp ", "mv ", "mkdir ",
    "python ", "python3 ", "node ", "npm ", "pnpm ", "yarn ",
    "pip ", "pip3 ", "uv ", "brew ", "git ", "PYTHONPATH",
    "export ", "echo ", "cat ", "grep ", "sed ", "awk ",
    "curl ", "wget ", "ssh ", "scp ", "make ", "cmake ",
    ">>", "<<", "function ", "def ", "class ", "import ",
    "from ", "{", "}", "[", "]", "//", "/*",
)


_SENTENCE_TERMINATOR_RE = re.compile(r"[.!?](?:\s|$)")


def _count_sentences(text: str) -> int:
    """Cheap sentence counter — counts `.`, `!`, `?` followed by whitespace
    or end-of-string. Good enough for gating prose against thin-stub LLM
    output; not trying to be linguistically precise."""
    return len(_SENTENCE_TERMINATOR_RE.findall(text or ""))


_SECTION_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def _extract_section(body: str, heading: str) -> str:
    """Return the body of `## Heading` up to the next `## ` or end-of-body.

    Returns "" when the heading is absent. Trims surrounding whitespace.
    Used by depth checks to inspect Definition / Synthesis / Threads /
    Implications independently.
    """
    target = heading.strip().lower()
    matches = list(_SECTION_HEADING_RE.finditer(body))
    for i, m in enumerate(matches):
        if m.group(1).strip().lower() != target:
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        return body[start:end].strip()
    return ""


def _strip_blockquote_markers(line: str) -> str:
    """Strip leading `>` characters and spaces from a markdown blockquote line."""
    stripped = line.lstrip()
    while stripped.startswith(">"):
        stripped = stripped[1:].lstrip()
    return stripped


def _quote_blocks(section: str) -> list[str]:
    """Extract one logical quote per contiguous `>` blockquote run."""
    blocks: list[str] = []
    current: list[str] = []
    for line in section.splitlines():
        if line.lstrip().startswith(">"):
            current.append(_strip_blockquote_markers(line))
        elif current and line.strip() == "":
            blocks.append(" ".join(p for p in current if p).strip())
            current = []
        elif current:
            blocks.append(" ".join(p for p in current if p).strip())
            current = []
    if current:
        blocks.append(" ".join(p for p in current if p).strip())
    return [b for b in blocks if b]


def _is_code_or_cli_quote(quote: str) -> bool:
    """Heuristic: does this quote look like a command/code line, not prose?

    The verb-marker heuristic an earlier draft used was too brittle —
    "RIFE controls how the model bridges keyframes" got flagged because
    "controls" / "bridges" aren't in any reasonable hardcoded verb list.
    Two cleaner signals replace it:

      1. Starts with a known code/CLI prefix (`$`, `cd `, `python`,
         `PYTHONPATH=`, etc.) — high-precision CLI detector.
      2. Symbol-density above 30 % — CLI lines like
         `PYTHONPATH=. .venv/bin/python3 scripts/update_status.py <id>` are
         dense in `/`, `=`, `-`, `<`, `>` etc., whereas prose is dense in
         alphanumerics with a few terminal periods/commas.

    Either signal alone classifies the quote as code; otherwise it's prose.
    """
    stripped = quote.strip()
    if not stripped:
        return True
    if any(stripped.startswith(p) for p in _CODE_LINE_PREFIXES):
        return True
    non_word = sum(1 for ch in stripped if not (ch.isalnum() or ch.isspace()))
    if non_word / max(len(stripped), 1) > 0.30:
        return True
    return False


def _normalize_for_dup_check(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


def evaluate_article_depth(body: str) -> tuple[bool, str]:
    """Semantic depth gate for a rendered article body.

    Returns `(True, "")` when the article meets Tier-1.5 depth requirements,
    `(False, reason)` when it doesn't. Dispatches on `type: concept` /
    `type: connection` in the frontmatter.

    Reason codes (stable — keyed by manifest consumers):
      concept: thin-definition, restatement-definition, thin-evidence,
               code-only-evidence, duplicate-examples
      connection: thin-synthesis, thin-threads, thin-implications

    Unknown article type → `(True, "")` (no opinion).
    """
    head = body[:400]
    if "type: concept" in head:
        return _evaluate_concept_depth(body)
    if "type: connection" in head:
        return _evaluate_connection_depth(body)
    return True, ""


def _evaluate_concept_depth(body: str) -> tuple[bool, str]:
    definition = _extract_section(body, "Definition")
    if (
        _count_sentences(definition) < _MIN_DEFINITION_SENTENCES
        or len(definition) < _MIN_DEFINITION_CHARS
    ):
        return False, "thin-definition"

    lowered = definition.lower()
    if any(p in lowered for p in _RESTATEMENT_PHRASES):
        return False, "restatement-definition"

    evidence_section = _extract_section(body, "Evidence")
    quotes = _quote_blocks(evidence_section)
    substantive = [q for q in quotes if len(q) >= _MIN_QUOTE_CHARS]
    if len(substantive) < _MIN_QUOTES_PER_CONCEPT:
        return False, "thin-evidence"
    if all(_is_code_or_cli_quote(q) for q in substantive):
        return False, "code-only-evidence"

    examples_section = _extract_section(body, "Examples")
    example_lines = [
        ln.lstrip("- ").strip()
        for ln in examples_section.splitlines()
        if ln.lstrip().startswith("- ")
    ]
    if example_lines and quotes:
        norm_quotes = {_normalize_for_dup_check(q) for q in quotes}
        if example_lines and all(
            _normalize_for_dup_check(ex) in norm_quotes for ex in example_lines
        ):
            return False, "duplicate-examples"

    return True, ""


_CONNECTION_THREAD_RE = re.compile(r"^###\s+\[\[([^\]|]+)\]\]\s*$", re.MULTILINE)


def _evaluate_connection_depth(body: str) -> tuple[bool, str]:
    synthesis = _extract_section(body, "Synthesis")
    if (
        _count_sentences(synthesis) < _MIN_SYNTHESIS_SENTENCES
        or len(synthesis) < _MIN_SYNTHESIS_CHARS
    ):
        return False, "thin-synthesis"

    threads_section = _extract_section(body, "Threads")
    if not threads_section:
        return False, "thin-threads"

    thread_headings = list(_CONNECTION_THREAD_RE.finditer(threads_section))
    if not thread_headings:
        return False, "thin-threads"

    for i, m in enumerate(thread_headings):
        start = m.end()
        end = (
            thread_headings[i + 1].start()
            if i + 1 < len(thread_headings)
            else len(threads_section)
        )
        thread_body = threads_section[start:end]
        thread_quotes = _quote_blocks(thread_body)
        if not thread_quotes:
            return False, "thin-threads"
        if not any(len(q) >= _MIN_THREAD_QUOTE_CHARS for q in thread_quotes):
            return False, "thin-threads"

    implications_section = _extract_section(body, "Implications")
    impl_lines = [
        ln.lstrip("- ").strip()
        for ln in implications_section.splitlines()
        if ln.lstrip().startswith("- ")
    ]
    substantive_impls = [i for i in impl_lines if len(i) >= _MIN_IMPLICATION_CHARS]
    if len(substantive_impls) < _MIN_IMPLICATIONS:
        return False, "thin-implications"

    return True, ""


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
        # Tier 2 retrofit (2026-05-16) — total real clusters HDBSCAN found
        # across all per-file retrieval pools. ≥3 means the cluster-and-
        # sample path is doing work; 0 means every pool fell back to the
        # top-rank slice (legacy v1 behaviour).
        "clusters_sampled": result.clusters_sampled,
        # Tier 1.5 retrofit (2026-05-20) — per-reason rejection counts and
        # thin-source skip counts. Operator-grade signal for *why* an
        # otherwise-healthy run produced low output volume.
        "rejected_reasons": dict(sorted(result.rejected_reasons.items())),
        "skipped_thin_source": result.skipped_thin_source,
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
        "vault. Your job is not to summarize. Your job is to be Sean's "
        "**thinking partner** — surfacing non-obvious cross-domain patterns "
        "and tensions he would not notice manually. Connections must span "
        "life-systems, creative-studio, job-hunt-2026, and Superuser Pack "
        "infrastructure. **If the chunks below don't support a real insight, "
        "return empty arrays. Do not pad.**\n\n"
        "Four rules govern every article you emit:\n"
        "  1. EVIDENCE FIRST — every claim grounded in a verbatim quote from "
        "a source file. The quote must be prose that contains a claim — not "
        "a CLI command, not a frontmatter slice, not a table cell. If the "
        "only quotable lines are commands, OMIT the article.\n"
        "  2. NAME THE MECHANISM — definitions describe the *underlying "
        "pattern or invariant*, not what the source file does. \"A collection "
        "of automated processes designed to support Sean\" is a restatement, "
        "not a definition. \"A producer/consumer pattern where one agent's "
        "write creates a dependency that another agent's read enforces\" is "
        "a definition.\n"
        "  3. REUSE > REMINT — if a concept already has a slug in the "
        "canonical list below, reuse the exact title. Do not invent "
        "near-duplicate names.\n"
        "  4. CROSS-DOMAIN > WITHIN-DOMAIN — connections whose member "
        "concepts originate in DIFFERENT top-level vault folders "
        "(life-systems × creative-studio × job-hunt × 40_knowledge × "
        "05_atlas) are real discoveries. Three concepts from the same "
        "folder is a within-domain summary; OMIT it.\n\n"
        f"Primary file: {primary_file_rel}  (folder: {primary_folder})\n"
        f"---\n{primary_text[:3000]}\n---\n\n"
        "Semantically similar vault files (note the `folder` field — use it "
        "to identify cross-domain pairs):\n"
        f"{sim_block}\n\n"
        f"{canonical_block}"
        "FORBIDDEN PHRASES — articles containing any of these are rejected:\n"
        '  - "Evidence pending"\n'
        '  - "(to be filled)"\n'
        '  - "a collection of …", "a set of …", "a series of …"\n'
        '  - "designed to support", "designed to ensure"\n'
        '  - "streamlines his workflow", "ensures consistency", "ensures efficiency"\n'
        '  - "is a process for …", "is a system that …", "is the practice of …"\n'
        '  - "this concept is critical", "this would benefit Sean"\n\n'
        "REJECTED-SHAPE EXAMPLES (do not produce output that looks like this):\n"
        "  BAD definition: \"A collection of automated processes designed to "
        "support Sean's job-hunting efforts, including status updates and "
        "application tracking.\"  — restates the prompt, names no mechanism.\n"
        "  BAD evidence quotes: \"cd ~/Code-Brain/...\", \"PYTHONPATH=. python "
        "scripts/update_status.py\"  — CLI commands, not claims.\n"
        "  BAD synthesis: \"Three producers share an MBP dependency.\"  — "
        "describes the linkage but doesn't name the tension or its "
        "consequence.\n\n"
        "ACCEPTED-SHAPE EXAMPLE:\n"
        "  GOOD definition: \"Daily-routine automation depends on agents "
        "successfully reading the previous day's note. When a synthesizer "
        "fails silently overnight, the morning brief inherits stale context, "
        "and the user notices the staleness before the brief flags the "
        "failure. The dependency is invisible in each agent's source.\"\n\n"
        "Return ONLY a JSON object with this shape (lists may be empty):\n\n"
        "{\n"
        "  \"concepts\": [\n"
        "    {\n"
        "      \"title\": string,                   // reuse from canonical list if applicable\n"
        "      \"definition\": string,              // **3–5 sentences, ≥250 chars**, naming the mechanism not the surface description\n"
        "      \"context\": string,                 // **2–3 sentences** on why it matters to Sean specifically\n"
        "      \"evidence\": [string],              // ≥2 VERBATIM quotes from the primary or similar files. Each quote ≥60 chars AND contains a verbal claim (an `is`/`does`/`causes`/`requires`/etc). NO CLI commands.\n"
        "      \"examples\": [string],              // concrete from source material — MUST be distinct from `evidence` (no duplicate strings)\n"
        "      \"related\": [string]                // ≥2 exact titles of related concepts\n"
        "    }\n"
        "  ],\n"
        "  \"connections\": [\n"
        "    {\n"
        "      \"title\": string,\n"
        "      \"synthesis\": string,               // **3–5 sentences, ≥200 chars**: name the cross-domain TENSION or PATTERN and its CONSEQUENCE. Not a description of how the concepts relate; the underlying insight that links them.\n"
        "      \"concepts\": [string],              // exact titles, ≥3, from ≥2 different top-level folders\n"
        "      \"evidence\": {                      // per-concept verbatim quotes; each quote ≥60 chars of prose\n"
        "        \"<concept title>\": [string]      // ≥1 substantive verbatim quote that anchors this concept's role in the tension\n"
        "      },\n"
        "      \"implications\": [string],          // ≥2 entries, each ≥80 chars naming a downstream consequence or decision this surfaces\n"
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
        "CRITICAL CONSTRAINTS (depth gate downstream rejects violators):\n"
        "  - every concept's `definition` ≥3 sentences AND ≥250 chars AND avoids the forbidden phrases above\n"
        "  - every concept's `evidence` ≥2 quotes, each ≥60 chars, each containing a verbal claim — not a CLI snippet\n"
        "  - every connection's `synthesis` ≥3 sentences AND ≥200 chars, naming the tension/pattern + its consequence\n"
        "  - every connection's per-concept `evidence` block contains ≥1 substantive prose quote (≥60 chars)\n"
        "  - every connection has ≥2 `implications`, each ≥80 chars\n"
        "  - quotes MUST be exact substrings of the primary or similar file content shown above — paraphrasing is rejected downstream\n"
        "  - if you cannot meet these depth requirements with the chunks available, OMIT the article entirely\n"
        "  - **prefer fewer, deeper articles over many shallow ones — empty arrays are the correct output when nothing crosses the bar**"
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

        # Tier 2 retrofit (2026-05-16) — cluster-and-sample retrieval.
        # 1. Build a high-signal embedding query (headings + frontmatter +
        #    first paragraph) instead of the raw first-2000-chars slice,
        #    which used to be mostly frontmatter + intro.
        # 2. Retrieve a wide pool (RETRIEVAL_POOL_SIZE chunks) instead of
        #    top-K, asking the indexer to include embeddings so we can
        #    cluster downstream.
        # 3. Cluster + sample per cluster so the LLM sees cross-domain
        #    candidates structurally, not just whatever the densest region
        #    happens to be similar to. Falls back to the top-N-by-rank
        #    slice cleanly when the retriever can't provide embeddings
        #    (test mocks, degraded indexer), when the pool is too small,
        #    or when HDBSCAN finds <2 real clusters.
        retrieval_query = build_embedding_query(primary_text)
        try:
            pool = retriever(
                retrieval_query,
                RETRIEVAL_POOL_SIZE,
                include_embeddings=True,
            )
        except TypeError:
            # Backward-compat: caller-supplied retriever (legacy / test
            # mock) doesn't accept include_embeddings. Fall back to the
            # original positional call signature; the pool will be
            # embedding-less and the cluster path will be skipped below.
            try:
                pool = retriever(retrieval_query, RETRIEVAL_POOL_SIZE)
            except Exception as exc:
                pool = []
                result.warnings.append(f"retrieval failed for {fp.name}: {exc}")
        except Exception as exc:
            pool = []
            result.warnings.append(f"retrieval failed for {fp.name}: {exc}")

        if pool and isinstance(pool[0].get("embedding"), (list, tuple)):
            cluster_result = cluster_and_sample(
                [p["embedding"] for p in pool],
                k_per_cluster=RETRIEVAL_K_PER_CLUSTER,
                min_cluster_size=RETRIEVAL_MIN_CLUSTER_SIZE,
                max_noise=RETRIEVAL_MAX_NOISE,
                max_total=RETRIEVAL_MAX_TOTAL,
            )
            similar = [pool[i] for i in cluster_result.indices]
            # Strip embeddings before passing downstream — the prompt
            # builder only consumes file_path / folder / chunk_text and
            # 50 × 768-dim vectors would balloon the LLM context budget.
            for chunk in similar:
                chunk.pop("embedding", None)
            result.clusters_sampled += cluster_result.clusters_found
        else:
            # No embeddings in pool → legacy top-K-by-rank behaviour.
            similar = pool[:top_k]

        # Tier 1.5 (2026-05-20) — skip thin-source files before the LLM
        # call. If the diversified pool can't surface at least 2 candidate
        # chunks, the LLM has nothing to ground a cross-domain article
        # against. Better to produce no article than a shallow one.
        if len(similar) < _MIN_SIMILAR_FOR_LLM:
            result.skipped_thin_source += 1
            log.info(
                "skipping %s — only %d candidate chunks (threshold %d)",
                fp.name, len(similar), _MIN_SIMILAR_FOR_LLM,
            )
            continue

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
                    result.rejected_reasons["wikilinks-or-placeholder"] = (
                        result.rejected_reasons.get("wikilinks-or-placeholder", 0) + 1
                    )
                    continue
                # Tier 1.5 (2026-05-20) — semantic depth gate. Catches
                # restated-prompt definitions, code-only evidence, and
                # duplicate-Examples shape that the legacy validator can't
                # see. Reason recorded for manifest attribution.
                depth_ok, depth_reason = evaluate_article_depth(body)
                if not depth_ok:
                    result.rejected_count += 1
                    result.rejected_reasons[depth_reason] = (
                        result.rejected_reasons.get(depth_reason, 0) + 1
                    )
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
                    result.rejected_reasons["wikilinks-or-placeholder"] = (
                        result.rejected_reasons.get("wikilinks-or-placeholder", 0) + 1
                    )
                    continue
                # Tier 1.5 (2026-05-20) — semantic depth gate on the
                # connection side: rejects thin synthesis, empty / short
                # per-concept threads, and casual one-liner implications.
                depth_ok, depth_reason = evaluate_article_depth(body)
                if not depth_ok:
                    result.rejected_count += 1
                    result.rejected_reasons[depth_reason] = (
                        result.rejected_reasons.get(depth_reason, 0) + 1
                    )
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
        if decision.runtime == "ollama":
            # Ollama /api/chat: think:false suppresses Qwen3.5/3.6 thinking
            # tokens that LM Studio's MLX integration silently leaked.
            # num_ctx=32768 matches the qwen3.6_35b-a3b-32k variant's modelfile.
            resp = httpx.post(
                f"{decision.base_url}/api/chat",
                json={
                    "model": decision.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "think": False,
                    "options": {"num_ctx": 32768, "temperature": 0.0, "num_predict": max_tokens},
                },
                timeout=600.0,
            )
            resp.raise_for_status()
            text = resp.json()["message"]["content"]
        else:
            # LM Studio / mlx-lm / any OpenAI-compat runtime.
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
    """Re-use the existing vault_indexer search() against the live SQLite index.

    Accepts ``include_embeddings`` as a passthrough so the Tier 2 retrofit
    (2026-05-16) cluster-and-sample path is reachable from the live agent.
    Without this, the synthesizer's ``retriever(query, k, include_embeddings=True)``
    call raised ``TypeError`` and silently fell back to legacy top-K — the
    bug that left ``clusters_sampled=0`` in the 2026-05-17 manifest.
    """
    from agents.vault_indexer import get_db_path, search

    def _retrieve(
        query: str,
        top_k: int = 5,
        *,
        include_embeddings: bool = False,
    ) -> list[dict[str, Any]]:
        db = get_db_path(vault_root)
        if not db.exists():
            return []
        return asyncio.run(
            search(query, db, top_k=top_k, include_embeddings=include_embeddings)
        )

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
