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
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).parent.parent))

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

_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
_SLUG_RE = re.compile(r"[^a-z0-9]+")


@dataclass
class SynthesisResult:
    status: str                       # "ok" | "partial" | "budget-exhausted" | "wol-deferred" | "error"
    concepts_written: int = 0
    connections_written: int = 0
    rejected_count: int = 0
    files_processed: int = 0
    duration_seconds: float = 0.0
    error: str = ""
    warnings: list[str] = field(default_factory=list)


# ─── pure helpers ──────────────────────────────────────────────────────────

def extract_wikilinks(body: str) -> list[str]:
    return _WIKILINK_RE.findall(body)


def count_wikilinks(body: str) -> int:
    return len(extract_wikilinks(body))


def validate_article_body(body: str) -> bool:
    return count_wikilinks(body) >= MIN_WIKILINKS_PER_ARTICLE


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
    today: str,
) -> str:
    sources = sources or []
    yaml_sources = "\n".join(f"  - {s}" for s in sources) or "  - "
    related_links = " ".join(f"[[{r}]]" for r in related) or ""
    ex_block = "\n".join(f"- {e}" for e in examples) or "- (no examples captured yet)"

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
        f"## Examples\n\n{ex_block}\n\n"
        f"## Related Concepts\n\n{related_links}\n"
    )


def format_connection_article(
    *,
    title: str,
    synthesis: str,
    concepts: list[str],
    implications: list[str],
    today: str,
) -> str:
    connects_yaml = "\n".join(f"  - {c}" for c in concepts) or "  - "
    threads = "\n\n".join(f"### [[{c}]]\n\nEvidence pending." for c in concepts)
    implications_block = "\n".join(f"- {i}" for i in implications) or "- (to be filled)"

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
    """Rebuild `vault/knowledge/index.md` from disk."""
    index_path = knowledge_root / "index.md"
    concepts_dir = knowledge_root / CONCEPTS_SUBDIR
    connections_dir = knowledge_root / CONNECTIONS_SUBDIR

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

    index_path.write_text("\n".join(body) + "\n", encoding="utf-8")
    return index_path


# ─── orchestration ────────────────────────────────────────────────────────

def _build_synthesis_prompt(
    *,
    primary_file_rel: str,
    primary_text: str,
    similar: list[dict[str, Any]],
) -> str:
    sim_block = "\n".join(
        f"- {s.get('file_path')}: {str(s.get('chunk_text',''))[:200]}"
        for s in similar
    )
    return (
        "You are synthesizing knowledge articles for a personal vault.\n\n"
        f"Primary file: {primary_file_rel}\n"
        f"---\n{primary_text[:3000]}\n---\n\n"
        "Semantically similar vault files:\n"
        f"{sim_block}\n\n"
        "Return ONLY a JSON object with this shape (lists may be empty):\n\n"
        "{\n"
        "  \"concepts\": [\n"
        "    {\n"
        "      \"title\": string,\n"
        "      \"definition\": string,  // 2-3 sentences\n"
        "      \"context\": string,     // why it matters\n"
        "      \"examples\": [string],  // concrete from source material\n"
        "      \"related\": [string]    // ≥2 exact titles of related concepts\n"
        "    }\n"
        "  ],\n"
        "  \"connections\": [\n"
        "    {\n"
        "      \"title\": string,\n"
        "      \"synthesis\": string,      // 1-2 sentences\n"
        "      \"concepts\": [string],     // exact titles, ≥3\n"
        "      \"implications\": [string]  // how this informs future work\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "CRITICAL: every concept MUST list ≥2 related titles and every\n"
        "connection MUST list ≥3 concept titles — articles without enough\n"
        "wikilinks will be discarded."
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
) -> SynthesisResult:
    """Drive the synthesis pass end-to-end.

    `llm_caller(prompt)` must return a dict with `concepts` and `connections`.
    `retriever(query, top_k)` returns [{file_path, chunk_text, similarity}].
    """
    start = time.monotonic()
    today = now_iso or date.today().isoformat()
    knowledge_root = vault_root / KNOWLEDGE_SUBDIR
    concepts_dir = knowledge_root / CONCEPTS_SUBDIR
    connections_dir = knowledge_root / CONNECTIONS_SUBDIR
    concepts_dir.mkdir(parents=True, exist_ok=True)
    connections_dir.mkdir(parents=True, exist_ok=True)
    lock_path = knowledge_root / ".lock"

    result = SynthesisResult(status="ok")

    if budget_seconds <= 0 or not changed_files:
        result.status = "budget-exhausted" if budget_seconds <= 0 else "ok"
        result.duration_seconds = time.monotonic() - start
        # Still regen index so downstream consumers see something.
        with FileLock(lock_path, exclusive=True, timeout=10.0):
            regenerate_index(knowledge_root)
        return result

    for fp in changed_files:
        if time.monotonic() - start >= budget_seconds:
            result.status = "partial"
            result.warnings.append(f"budget ran out after {result.files_processed} files")
            break

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
        )
        try:
            parsed = llm_caller(prompt)
        except Exception as exc:
            result.warnings.append(f"LLM call failed for {fp.name}: {exc}")
            continue

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
                body = format_connection_article(
                    title=title,
                    synthesis=conn.get("synthesis", ""),
                    concepts=concept_list,
                    implications=list(conn.get("implications", [])),
                    today=today,
                )
                if not validate_article_body(body):
                    result.rejected_count += 1
                    continue
                (connections_dir / f"{_slugify(title)}.md").write_text(body, encoding="utf-8")
                result.connections_written += 1

    with FileLock(lock_path, exclusive=True, timeout=10.0):
        regenerate_index(knowledge_root)

    result.duration_seconds = time.monotonic() - start
    return result


# ─── CLI entry point (production path) ────────────────────────────────────

def _default_llm_caller_factory(router: HybridRouter) -> Callable[..., dict]:
    import httpx

    def _call(prompt: str, max_tokens: int = 2000) -> dict:
        async def go():
            return await router.route_to_macbook(
                task="vault_synthesis", wake_timeout_s=90.0
            )
        decision = asyncio.run(go())
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

    llm = _default_llm_caller_factory(router)
    retriever = _default_retriever_factory(cfg.vault_root)

    start_ns = time.monotonic_ns()
    try:
        result = run_synthesis(
            vault_root=cfg.vault_root,
            changed_files=changed,
            llm_caller=llm,
            retriever=retriever,
            budget_seconds=args.budget_seconds,
        )
    except WOLUnavailable as exc:
        logger.warning("WOL unavailable — deferring: %s", exc)
        record_run(cfg.log_dir, AGENT_NAME, mode=None, status="deferred",
                   cost_usd=0.0, duration_ms=None, turns=None,
                   notes="wol-unavailable")
        return 0
    except Exception as exc:
        logger.error("synthesis failed: %s", exc)
        record_run(cfg.log_dir, AGENT_NAME, mode=None, status="error",
                   cost_usd=0.0, duration_ms=None, turns=None, notes=str(exc)[:200])
        return 1

    duration_ms = (time.monotonic_ns() - start_ns) // 1_000_000

    # Persist new state only on a successful / partial run
    if result.status in {"ok", "partial"}:
        write_indexer_state(state_path, new_state)

    logger.info("synthesis %s concepts=%d connections=%d rejected=%d duration=%.1fs",
                result.status, result.concepts_written, result.connections_written,
                result.rejected_count, result.duration_seconds)

    record_run(cfg.log_dir, AGENT_NAME, mode=None,
               status="success" if result.status in {"ok", "partial"} else result.status,
               cost_usd=0.0, duration_ms=duration_ms, turns=None,
               notes=f"concepts={result.concepts_written} connections={result.connections_written} rejected={result.rejected_count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
