#!/usr/bin/env python3
"""Phase C — terminal Q&A against the synthesized knowledge base.

Two-pass orchestration:

  1. Selection pass: send `vault/knowledge/index.md` + the question to the
     LLM. Ask for 3-N article paths most likely to contain the answer,
     each tagged with a similarity score in [0, 1].
  2. Answer pass:    read the selected article files, send them along with
     the question, ask for an answer that cites at least one [[wikilink]].

Model routing mirrors vault_synthesizer's local-first pattern via
`lib.hybrid_router.HybridRouter`. `--model auto` (default) tries the
local route first (Qwen3-14B on MacBook Pro via the `vault_synthesis`
task) and falls back to Anthropic Sonnet 4.6 if the MBP is unreachable.
`--model local` forces the local path; `--model api` forces the API path.

`--file-back` persists the answer as a third-tier knowledge article at
`vault/knowledge/qa/<slug>.md` and appends one JSONL line to
`vault/knowledge/qa/.manifest.json` (C.M2). The qa/ frontmatter (C.M1)
captures `chunk_id` (SHA-256 prefix-12 of the consulted file_path|chunk
tuple read from `vault/.vault-index.db`'s `chunks` table) and the
similarity score returned by the selection pass.

Empty-state behavior: when `vault/knowledge/index.md` is the empty stub
(no concept/connection articles yet), the selection pass emits zero
candidates and the answer pass reports cleanly that no articles match.
The CLI exits 0; no qa/ file is written even if `--file-back` is set.

Usage:
    python3 scripts/query.py "What's my error handling pattern?"
    python3 scripts/query.py "..." --file-back
    python3 scripts/query.py "..." --model api
    python3 scripts/query.py "..." --max-articles 5
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import sqlite3
import sys
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable

import httpx

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config
from lib.filelock import FileLock
from lib.hybrid_router import HybridRouter, RoutingDecision, WOLUnavailable
from lib.logging_setup import record_run, setup_logger

AGENT_NAME = "knowledge-query"

DEFAULT_MAX_ARTICLES = 10
DEFAULT_SELECTION_MAX_TOKENS = 600
DEFAULT_ANSWER_MAX_TOKENS = 1500
DEFAULT_TASK_KEY = "vault_synthesis"
DEFAULT_QA_DIR = "vault/knowledge/qa"
DEFAULT_MANIFEST_PATH = "vault/knowledge/qa/.manifest.json"

API_FALLBACK_MODEL = "claude-sonnet-4-6"

_SLUG_RE = re.compile(r"[^a-z0-9]+")
_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
_INDEX_LINK_RE = re.compile(r"\[\[([^\]|]+)\|([^\]]+)\]\]")


# ─── data shapes ──────────────────────────────────────────────────────────


@dataclass
class ConsultedArticle:
    path: str            # vault/knowledge/-relative, e.g. "concepts/error-handling.md"
    chunk_id: str        # SHA-256 prefix-12 over (file_path, chunk_index) tuple
    similarity: float    # selection-pass similarity score in [0, 1]
    title: str = ""      # frontmatter title or filename stem


@dataclass
class QueryResult:
    question: str
    answer: str
    consulted: list[ConsultedArticle]
    model: str = ""
    model_route: str = ""    # "auto→local" / "auto→api" / "local" / "api"
    duration_ms: int = 0
    qa_file: Path | None = None
    empty_index: bool = False
    warnings: list[str] = field(default_factory=list)


# ─── pure helpers ─────────────────────────────────────────────────────────


def slugify(text: str, max_len: int = 80) -> str:
    s = _SLUG_RE.sub("-", text.lower()).strip("-")
    return (s or "untitled")[:max_len]


def parse_index(index_text: str) -> list[dict[str, str]]:
    """Extract (path, title) pairs from `vault/knowledge/index.md`.

    Recognises lines of the form `- [[path/to/file|Title]]` produced by
    `vault_synthesizer.regenerate_index`. The empty-state stub has no such
    lines and parses to `[]`.
    """
    entries: list[dict[str, str]] = []
    for line in index_text.splitlines():
        m = _INDEX_LINK_RE.search(line)
        if not m:
            continue
        path = m.group(1).strip()
        title = m.group(2).strip()
        if path and not path.endswith(".md"):
            path = f"{path}.md"
        entries.append({"path": path, "title": title})
    return entries


def is_empty_index(entries: list[dict[str, str]]) -> bool:
    return len(entries) == 0


def compute_chunk_id(file_path: str, chunk_index: int) -> str:
    """Stable identifier for a single chunk in the embedding index.

    Hashes `f"{file_path}|{chunk_index}"` and returns the first 12 hex
    characters. Matches the (file_path, chunk_index) UNIQUE key in
    `vault_indexer.init_db`'s `chunks` table.
    """
    raw = f"{file_path}|{chunk_index}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12]


def lookup_chunk_id_for_file(db_path: Path, vault_rel_path: str) -> str | None:
    """Read the lowest chunk_index for `vault_rel_path` from the chunks table.

    Returns `None` if the DB is missing, the table is missing, or the file
    has no chunks (e.g., qa/ articles aren't always indexed). The selection
    pass operates on file paths; this helper resolves the first chunk so
    the qa/ frontmatter can cite a stable chunk_id.
    """
    if not db_path.exists():
        return None
    try:
        conn = sqlite3.connect(str(db_path))
        try:
            cur = conn.execute(
                "SELECT MIN(chunk_index) FROM chunks WHERE file_path = ?",
                (vault_rel_path,),
            )
            row = cur.fetchone()
        finally:
            conn.close()
    except sqlite3.Error:
        return None
    if row is None or row[0] is None:
        return None
    return compute_chunk_id(vault_rel_path, int(row[0]))


def article_relpath_from_index(index_path: str, knowledge_root: Path) -> Path:
    """Convert an index entry path to an absolute filesystem path."""
    return knowledge_root / index_path


def vault_relpath_for_chunks(article_path: str) -> str:
    """Return the path under vault_root that `chunks.file_path` would store.

    `vault_indexer.discover_vault_files` writes `file_path` as
    vault-relative POSIX (e.g., `knowledge/concepts/foo.md`). Index entries
    in `index.md` are knowledge-relative (e.g., `concepts/foo.md`), so we
    prepend `knowledge/` here.
    """
    return f"knowledge/{article_path}"


# ─── prompt builders ──────────────────────────────────────────────────────


SELECTION_SYSTEM = (
    "You select knowledge-base articles likely to answer a question. "
    "You return STRICT JSON only — no prose, no fencing."
)


def build_selection_prompt(
    *,
    question: str,
    index_entries: list[dict[str, str]],
    max_articles: int,
) -> str:
    listing = "\n".join(
        f"- {e['path']} :: {e['title']}" for e in index_entries
    ) or "(none)"
    return (
        f"Question: {question}\n\n"
        f"Available knowledge articles (path :: title):\n{listing}\n\n"
        f"Pick up to {max_articles} articles most likely to contain the "
        f"answer. Score each from 0.0 (irrelevant) to 1.0 (definitely "
        f"contains the answer). Return ONLY a JSON object of the form:\n"
        f"{{\n"
        f"  \"selected\": [\n"
        f"    {{\"path\": \"<path from listing>\", \"similarity\": <float>}}\n"
        f"  ]\n"
        f"}}\n"
        f"If no article looks relevant, return {{\"selected\": []}}."
    )


def build_answer_prompt(
    *,
    question: str,
    articles: list[tuple[str, str]],
) -> str:
    """Compose the answer-pass prompt.

    `articles` is a list of `(rel_path, body)` tuples for the LLM to read.
    The model is asked to answer with at least one `[[wikilink]]` citation
    so the qa/ article connects back to the graph (and so knowledge_lint
    Tier 1 doesn't flag it as orphan-by-content even though it's already
    in the orphan-exclude list).
    """
    blocks = []
    for rel_path, body in articles:
        blocks.append(f"### {rel_path}\n\n{body[:3500]}")
    materials = "\n\n".join(blocks) if blocks else "(no articles selected)"
    return (
        f"Question: {question}\n\n"
        f"Reference articles:\n\n{materials}\n\n"
        f"Write a concise answer that cites at least one article using "
        f"`[[<knowledge-relative-path-without-md>]]` wikilink syntax "
        f"(e.g., `[[concepts/error-handling]]`). If the references do not "
        f"answer the question, say so explicitly."
    )


# ─── orchestration ────────────────────────────────────────────────────────


def run_selection_pass(
    *,
    question: str,
    index_text: str,
    llm_caller: Callable[[str, int], dict],
    max_articles: int,
    selection_max_tokens: int,
) -> tuple[list[ConsultedArticle], list[dict[str, str]]]:
    """Selection pass — returns (consulted, raw_index_entries)."""
    entries = parse_index(index_text)
    if is_empty_index(entries):
        return [], entries

    prompt = build_selection_prompt(
        question=question,
        index_entries=entries,
        max_articles=max_articles,
    )
    try:
        parsed = llm_caller(prompt, selection_max_tokens)
    except Exception:
        return [], entries

    selected = parsed.get("selected", []) if isinstance(parsed, dict) else []
    valid_paths = {e["path"]: e["title"] for e in entries}
    consulted: list[ConsultedArticle] = []
    seen: set[str] = set()
    for item in selected:
        if not isinstance(item, dict):
            continue
        path = str(item.get("path", "")).strip()
        if not path or path in seen:
            continue
        if path not in valid_paths:
            continue
        try:
            similarity = float(item.get("similarity", 0.0))
        except (TypeError, ValueError):
            similarity = 0.0
        similarity = max(0.0, min(1.0, similarity))
        consulted.append(
            ConsultedArticle(
                path=path,
                chunk_id="",  # filled in by the answer pass once we've read the file
                similarity=similarity,
                title=valid_paths[path],
            )
        )
        seen.add(path)
        if len(consulted) >= max_articles:
            break
    return consulted, entries


def load_articles(
    knowledge_root: Path,
    consulted: list[ConsultedArticle],
    db_path: Path | None,
) -> list[tuple[str, str]]:
    """Read consulted article bodies and stamp chunk_id values onto each.

    Returns `(rel_path, body)` tuples for the answer prompt. Mutates
    `consulted` in place to set `chunk_id` from the SQLite chunks table
    (or a deterministic fallback if the DB has no entry for the file).
    """
    pairs: list[tuple[str, str]] = []
    for ca in consulted:
        path = (knowledge_root / ca.path).resolve()
        if not path.exists():
            ca.chunk_id = compute_chunk_id(vault_relpath_for_chunks(ca.path), 0)
            continue
        try:
            body = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            body = ""
        pairs.append((ca.path, body))
        vault_rel = vault_relpath_for_chunks(ca.path)
        ca.chunk_id = (
            (lookup_chunk_id_for_file(db_path, vault_rel) if db_path else None)
            or compute_chunk_id(vault_rel, 0)
        )
    return pairs


def run_answer_pass(
    *,
    question: str,
    articles: list[tuple[str, str]],
    llm_caller: Callable[[str, int], str],
    answer_max_tokens: int,
) -> str:
    prompt = build_answer_prompt(question=question, articles=articles)
    try:
        return llm_caller(prompt, answer_max_tokens).strip()
    except Exception as exc:
        return f"(query failed: {exc})"


# ─── qa/ writer (C.M1) + manifest (C.M2) ──────────────────────────────────


def format_qa_article(
    *,
    question: str,
    answer: str,
    consulted: list[ConsultedArticle],
    model: str,
    today: str,
    synth_run: str,
) -> str:
    safe_question = question.replace('"', "'").strip()
    consulted_yaml_lines = []
    if consulted:
        for ca in consulted:
            consulted_yaml_lines.append(f"  - path: knowledge/{ca.path}")
            consulted_yaml_lines.append(f"    chunk_id: {ca.chunk_id}")
            consulted_yaml_lines.append(f"    similarity: {ca.similarity:.2f}")
    consulted_yaml = "\n".join(consulted_yaml_lines) or "  []"

    consulted_md_lines = []
    for ca in consulted:
        wikilink = ca.path[:-3] if ca.path.endswith(".md") else ca.path
        consulted_md_lines.append(
            f"- [[{wikilink}]] (chunk_id: {ca.chunk_id}, "
            f"similarity: {ca.similarity:.2f})"
        )
    consulted_md = "\n".join(consulted_md_lines) or "- (none)"

    title = f"Q: {safe_question}"
    return (
        f"---\n"
        f"title: \"{title}\"\n"
        f"question: \"{safe_question}\"\n"
        f"filed: {today}\n"
        f"type: qa\n"
        f"synth_run: {synth_run}\n"
        f"model: {model}\n"
        f"consulted:\n{consulted_yaml}\n"
        f"---\n\n"
        f"# {title}\n\n"
        f"## Answer\n\n{answer}\n\n"
        f"## Consulted articles\n\n{consulted_md}\n"
    )


def write_qa_article(
    *,
    qa_dir: Path,
    question: str,
    answer: str,
    consulted: list[ConsultedArticle],
    model: str,
    synth_run: str,
    now_iso: str | None = None,
) -> Path:
    qa_dir.mkdir(parents=True, exist_ok=True)
    today = (now_iso or date.today().isoformat())[:10]
    body = format_qa_article(
        question=question,
        answer=answer,
        consulted=consulted,
        model=model,
        today=today,
        synth_run=synth_run,
    )
    path = qa_dir / f"{slugify(question)}.md"
    lock_path = qa_dir / ".lock"
    with FileLock(lock_path, exclusive=True, timeout=10.0):
        path.write_text(body, encoding="utf-8")
    return path


def append_manifest(
    *,
    manifest_path: Path,
    record: dict[str, Any],
) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = manifest_path.parent / ".manifest.lock"
    line = json.dumps(record, sort_keys=True) + "\n"
    with FileLock(lock_path, exclusive=True, timeout=10.0):
        with open(manifest_path, "a", encoding="utf-8") as f:
            f.write(line)


# ─── default LLM caller wiring (production path) ──────────────────────────


def _local_chat_completion(
    decision: RoutingDecision,
    prompt: str,
    max_tokens: int,
    *,
    timeout: float = 120.0,
) -> str:
    if decision.runtime == "ollama":
        resp = httpx.post(
            f"{decision.base_url}/api/generate",
            json={
                "model": decision.model,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": max_tokens},
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        return resp.json().get("response", "")
    resp = httpx.post(
        f"{decision.base_url}/v1/chat/completions",
        json={
            "model": decision.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "stream": False,
        },
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _api_chat_completion(prompt: str, max_tokens: int) -> str:
    """Anthropic API fallback via claude_agent_sdk OAuth (no API key needed)."""
    from claude_agent_sdk import (  # type: ignore[import-not-found]
        ClaudeAgentOptions,
        query as sdk_query,
    )

    async def run() -> str:
        options = ClaudeAgentOptions(model=API_FALLBACK_MODEL, max_turns=1)
        chunks: list[str] = []
        async for msg in sdk_query(prompt=prompt, options=options):
            cls_name = type(msg).__name__
            if cls_name != "AssistantMessage":
                continue
            for block in getattr(msg, "content", []) or []:
                text = getattr(block, "text", None)
                if text:
                    chunks.append(text)
        return "".join(chunks)

    return asyncio.run(run())


def _parse_json_blob(text: str) -> dict:
    if not text:
        return {}
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return {}
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return {}


def make_default_llm_callers(
    *,
    router: HybridRouter | None,
    model_choice: str,
    task_key: str,
) -> tuple[Callable[[str, int], dict], Callable[[str, int], str], dict[str, str]]:
    """Build (selection_caller, answer_caller, meta) for production use.

    `meta` carries the resolved model name + route label so the qa/
    frontmatter and manifest record reflect what actually ran.
    """
    meta = {"model": "", "route": ""}

    def _route_local() -> RoutingDecision | None:
        if router is None:
            return None
        try:
            async def _go() -> RoutingDecision:
                return await router.route(task_key)
            return asyncio.run(_go())
        except (WOLUnavailable, Exception):
            return None

    def _selection(prompt: str, max_tokens: int) -> dict:
        return _parse_json_blob(_call(prompt, max_tokens))

    def _answer(prompt: str, max_tokens: int) -> str:
        return _call(prompt, max_tokens)

    def _call(prompt: str, max_tokens: int) -> str:
        nonlocal meta
        if model_choice == "api":
            meta["model"] = API_FALLBACK_MODEL
            meta["route"] = "api"
            return _api_chat_completion(prompt, max_tokens)
        if model_choice == "local":
            decision = _route_local()
            if decision is None or decision.machine == "claude_api":
                raise RuntimeError(
                    "local model unavailable (machine asleep or unreachable)"
                )
            meta["model"] = decision.model
            meta["route"] = "local"
            return _local_chat_completion(decision, prompt, max_tokens)
        # auto: local first, fall back to API
        decision = _route_local()
        if decision is not None and decision.machine != "claude_api":
            try:
                meta["model"] = decision.model
                meta["route"] = "auto→local"
                return _local_chat_completion(decision, prompt, max_tokens)
            except Exception:
                # local failed mid-call — fall back to API
                pass
        meta["model"] = API_FALLBACK_MODEL
        meta["route"] = "auto→api"
        return _api_chat_completion(prompt, max_tokens)

    return _selection, _answer, meta


# ─── top-level entrypoint ─────────────────────────────────────────────────


def run_query(
    *,
    question: str,
    vault_root: Path,
    selection_caller: Callable[[str, int], dict],
    answer_caller: Callable[[str, int], str],
    file_back: bool = False,
    max_articles: int = DEFAULT_MAX_ARTICLES,
    selection_max_tokens: int = DEFAULT_SELECTION_MAX_TOKENS,
    answer_max_tokens: int = DEFAULT_ANSWER_MAX_TOKENS,
    qa_dir: Path | None = None,
    manifest_path: Path | None = None,
    db_path: Path | None = None,
    model_label: str = "",
    model_route: str = "",
    now_iso: str | None = None,
) -> QueryResult:
    """Run selection + answer passes; optionally persist as qa/ article."""
    start_ms = time.monotonic_ns() // 1_000_000
    knowledge_root = vault_root / "knowledge"
    index_path = knowledge_root / "index.md"

    if not index_path.exists():
        return QueryResult(
            question=question,
            answer=(
                "The knowledge index does not exist yet. Run "
                "`agents/vault_synthesizer.py` to populate "
                "`vault/knowledge/index.md`."
            ),
            consulted=[],
            model=model_label,
            model_route=model_route,
            duration_ms=(time.monotonic_ns() // 1_000_000) - start_ms,
            empty_index=True,
            warnings=["index.md missing"],
        )

    index_text = index_path.read_text(encoding="utf-8", errors="replace")
    consulted, _entries = run_selection_pass(
        question=question,
        index_text=index_text,
        llm_caller=selection_caller,
        max_articles=max_articles,
        selection_max_tokens=selection_max_tokens,
    )

    if not consulted:
        # Empty index OR LLM returned no candidates. Either way, surface
        # the empty-state cleanly without faking an answer.
        result = QueryResult(
            question=question,
            answer=(
                "No knowledge articles match this question yet. "
                "The synthesized index is empty or contains no relevant entries."
            ),
            consulted=[],
            model=model_label,
            model_route=model_route,
            duration_ms=(time.monotonic_ns() // 1_000_000) - start_ms,
            empty_index=True,
        )
        return result

    db_for_chunk_lookup = db_path if db_path is not None else (vault_root / ".vault-index.db")
    article_pairs = load_articles(knowledge_root, consulted, db_for_chunk_lookup)
    answer = run_answer_pass(
        question=question,
        articles=article_pairs,
        llm_caller=answer_caller,
        answer_max_tokens=answer_max_tokens,
    )

    duration_ms = (time.monotonic_ns() // 1_000_000) - start_ms
    result = QueryResult(
        question=question,
        answer=answer,
        consulted=consulted,
        model=model_label,
        model_route=model_route,
        duration_ms=duration_ms,
    )

    if file_back:
        synth_run = (now_iso or datetime.now().isoformat(timespec="seconds"))
        qa_dir_resolved = qa_dir or (vault_root / "knowledge" / "qa")
        manifest_resolved = manifest_path or (qa_dir_resolved / ".manifest.json")
        qa_path = write_qa_article(
            qa_dir=qa_dir_resolved,
            question=question,
            answer=answer,
            consulted=consulted,
            model=model_label or "unknown",
            synth_run=synth_run,
            now_iso=now_iso,
        )
        result.qa_file = qa_path
        record = {
            "run_id": synth_run,
            "question": question,
            "model": model_label,
            "model_route": model_route,
            "consulted": [
                {
                    "path": ca.path,
                    "chunk_id": ca.chunk_id,
                    "similarity": round(ca.similarity, 4),
                }
                for ca in consulted
            ],
            "duration_ms": duration_ms,
            "answer_chars": len(answer),
            "qa_file": qa_path.relative_to(vault_root).as_posix(),
        }
        append_manifest(manifest_path=manifest_resolved, record=record)
    return result


# ─── CLI ──────────────────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ad-hoc Q&A against the synthesized vault knowledge base."
    )
    parser.add_argument("question", help="Free-form question.")
    parser.add_argument("--file-back", action="store_true",
                        help="Persist the answer at vault/knowledge/qa/<slug>.md "
                             "and append a manifest line.")
    parser.add_argument("--model", choices=("auto", "local", "api"), default=None,
                        help="Override default_model from config.toml [agents.query].")
    parser.add_argument("--max-articles", type=int, default=None,
                        help="Override max_articles from config.toml [agents.query].")
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    cfg = load_config()
    logger = setup_logger(AGENT_NAME, cfg.log_dir, cfg.log_level)

    query_cfg = cfg.agents.get("query", {}) if isinstance(cfg.agents, dict) else {}
    model_choice = args.model or query_cfg.get("default_model", "auto")
    max_articles = args.max_articles or query_cfg.get("max_articles", DEFAULT_MAX_ARTICLES)
    selection_max_tokens = query_cfg.get("selection_max_tokens", DEFAULT_SELECTION_MAX_TOKENS)
    answer_max_tokens = query_cfg.get("answer_max_tokens", DEFAULT_ANSWER_MAX_TOKENS)
    task_key = query_cfg.get("task_key", DEFAULT_TASK_KEY)
    qa_dir_cfg = query_cfg.get("qa_dir", DEFAULT_QA_DIR)
    manifest_cfg = query_cfg.get("manifest_path", DEFAULT_MANIFEST_PATH)
    qa_dir = (cfg.repo_root / qa_dir_cfg).resolve()
    manifest_path = (cfg.repo_root / manifest_cfg).resolve()

    # Build router (best-effort — if config parse fails, run API-only).
    router: HybridRouter | None = None
    try:
        import tomllib
        with open(Path(__file__).parent.parent / "config.toml", "rb") as f:
            raw_cfg = tomllib.load(f)
        router = HybridRouter.from_config(raw_cfg)
    except Exception as exc:
        logger.warning("router init failed: %s — API-only mode", exc)

    selection_caller, answer_caller, meta = make_default_llm_callers(
        router=router,
        model_choice=model_choice,
        task_key=task_key,
    )

    start_ns = time.monotonic_ns()
    try:
        result = run_query(
            question=args.question,
            vault_root=cfg.vault_root,
            selection_caller=selection_caller,
            answer_caller=answer_caller,
            file_back=args.file_back,
            max_articles=max_articles,
            selection_max_tokens=selection_max_tokens,
            answer_max_tokens=answer_max_tokens,
            qa_dir=qa_dir,
            manifest_path=manifest_path,
            db_path=cfg.vault_root / ".vault-index.db",
            model_label=meta.get("model", model_choice),
            model_route=meta.get("route", model_choice),
        )
    except Exception as exc:
        logger.error("query failed: %s", exc)
        record_run(cfg.log_dir, AGENT_NAME, mode=None, status="error",
                   cost_usd=0.0, duration_ms=None, turns=None,
                   notes=str(exc)[:200])
        return 1

    # Stamp meta (which the callers populated lazily on first invocation).
    if not result.model:
        result.model = meta.get("model", model_choice)
    if not result.model_route:
        result.model_route = meta.get("route", model_choice)

    print(result.answer)
    if result.consulted:
        print()
        print("Consulted:")
        for ca in result.consulted:
            print(f"  - {ca.path} (similarity: {ca.similarity:.2f}, chunk_id: {ca.chunk_id})")
    if result.qa_file:
        print()
        print(f"Filed: {result.qa_file}")

    duration_ms = (time.monotonic_ns() - start_ns) // 1_000_000
    record_run(
        cfg.log_dir, AGENT_NAME, mode=None,
        status="success" if not result.warnings else "partial",
        cost_usd=0.0, duration_ms=duration_ms, turns=None,
        notes=(
            f"route={result.model_route} model={result.model} "
            f"consulted={len(result.consulted)} "
            f"empty_index={result.empty_index}"
        ),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
