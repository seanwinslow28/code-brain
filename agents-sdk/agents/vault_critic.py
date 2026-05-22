#!/usr/bin/env python3
"""Vault Critic — nightly generative critique of synthesizer concept articles.

Runs on Mac Mini via launchd at 03:30 daily, after vault_synthesizer (02:30)
and deep_researcher (02:45). For each newly-written concept article from
today's synth-manifest (Mac-Mini-canonical, PR-contamination-filtered), fans
out two parallel subprocess critiques — Codex CLI (gpt-5.5) and Anti-Gravity
CLI (Gemini 3.1 Pro) — and writes a sibling expansion file at
vault/knowledge/expansions/{slug}.md plus a per-run manifest at
vault/health/critic-manifest-{date}.json.

Cost: $0 incremental on existing personal subscriptions. Sonnet fallback is
out of scope for v1; both-CLIs-rate-capped marks the run partial and exits
cleanly.

Schedule sequence:
    02:00  vault-indexer
    02:30  vault-synthesizer
    02:45  deep-researcher
    03:30  vault-critic        <- this agent
    08:30  daily-driver morning
    08:45  meta-agent
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.cli_runners import CLIResponse, run_antigravity, run_codex
from lib.config import load_config
from lib.critic_selector import select_target_articles
from lib.critique_prompt import build_critique_prompt
from lib.filelock import FileLock
from lib.logging_setup import record_run, setup_logger

AGENT_NAME = "vault-critic"

STATUS_OK = "ok"
STATUS_PARTIAL = "partial"
STATUS_SUCCESS_EMPTY = "success-empty"
STATUS_ERROR = "error"
STATUS_VALUES = frozenset({STATUS_OK, STATUS_PARTIAL, STATUS_SUCCESS_EMPTY, STATUS_ERROR})

DEFAULT_MAX_TARGETS = 3
DEFAULT_WALL_BUDGET_S = 600
DEFAULT_PER_CLI_TIMEOUT_S = 120
RECENT_TITLES_CONTEXT_LIMIT = 30

EXPANSIONS_REL = "vault/knowledge/expansions"
HEALTH_REL = "vault/health"
KNOWLEDGE_INDEX_REL = "vault/knowledge/index.md"

_TITLE_FRONTMATTER_RE = re.compile(r'^title:\s*"?([^"\n]+)"?', re.MULTILINE)
_SOURCES_FRONTMATTER_RE = re.compile(
    r"^sources:\s*\n((?:\s*-\s+.+\n?)+)", re.MULTILINE
)


@dataclass
class CritiqueResult:
    """Per-run summary written verbatim into critic-manifest-{date}.json."""
    status: str
    run_id: str
    articles_critiqued: int = 0
    codex_calls: int = 0
    codex_failures: int = 0
    codex_tokens_total: int = 0
    antigravity_calls: int = 0
    antigravity_failures: int = 0
    antigravity_tokens_total: int = 0
    duration_seconds: float = 0.0
    expansions_written: list[str] = field(default_factory=list)
    error: str = ""
    warnings: list[str] = field(default_factory=list)


def write_critic_manifest(
    *,
    repo_root: Path,
    result: CritiqueResult,
    today: str,
) -> Path:
    """Atomic write to vault/health/critic-manifest-{today}.json."""
    if result.status not in STATUS_VALUES:
        raise ValueError(
            f"Invalid status {result.status!r}; expected one of {sorted(STATUS_VALUES)}"
        )
    if not result.run_id:
        raise ValueError("run_id must be non-empty for manifest write")
    health = repo_root / HEALTH_REL
    health.mkdir(parents=True, exist_ok=True)
    path = health / f"critic-manifest-{today}.json"
    payload = {
        "run_id": result.run_id,
        "status": result.status,
        "articles_critiqued": result.articles_critiqued,
        "codex_calls": result.codex_calls,
        "codex_failures": result.codex_failures,
        "codex_tokens_total": result.codex_tokens_total,
        "antigravity_calls": result.antigravity_calls,
        "antigravity_failures": result.antigravity_failures,
        "antigravity_tokens_total": result.antigravity_tokens_total,
        "duration_seconds": round(result.duration_seconds, 2),
        "expansions_written": list(result.expansions_written),
        "warnings": list(result.warnings),
        "error": result.error,
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)
    return path


def format_expansion_body(
    *,
    original_title: str,
    original_slug: str,
    codex_text: str,
    antigravity_text: str,
    today: str,
    codex_failed: bool,
    antigravity_failed: bool,
) -> str:
    """Render the markdown body for vault/knowledge/expansions/{slug}.md.

    Snapshot semantics: one file per critiqued concept; not regenerated when
    the underlying concept is rewritten. Always contains a `[[parent-slug]]`
    wikilink so the file is not orphaned in the knowledge index.

    Backticks in titles are rendered verbatim (Obsidian parses them in
    double-quoted YAML scalars; some Obsidian versions may render the
    inline-code style in graph views — accepted Obsidian-behavior risk).
    Double-quotes in titles are escaped to keep the YAML scalar well-formed.
    """
    safe_title = original_title.replace('"', '\\"')
    codex_block = (
        codex_text.strip()
        if not codex_failed and codex_text.strip()
        else "_Codex rate-capped or failed; no critique this run._"
    )
    antigravity_block = (
        antigravity_text.strip()
        if not antigravity_failed and antigravity_text.strip()
        else "_Anti-Gravity rate-capped or failed; no critique this run._"
    )
    return (
        f"---\n"
        f'title: "How to make `{safe_title}` better"\n'
        f"type: expansion\n"
        f'parent: "[[{original_slug}]]"\n'
        f"sources:\n"
        f"  - codex (gpt-5.5)\n"
        f"  - anti-gravity (gemini-3.1-pro-preview)\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        f"---\n\n"
        f"## What this is\n\n"
        f"Critiques from two external reasoners (gpt-5.5 via Codex CLI, "
        f"Gemini 3 via Anti-Gravity CLI) of [[{original_slug}]]. The "
        f"synthesizer describes what the concept is; this expansion "
        f"proposes what's missing.\n\n"
        f"## From Codex (gpt-5.5)\n\n"
        f"{codex_block}\n\n"
        f"## From Anti-Gravity (Gemini 3)\n\n"
        f"{antigravity_block}\n"
    )


async def critique_one_article(
    *,
    repo_root: Path,
    article_path: Path,
    recent_titles: list[str],
    today: str,
    per_cli_timeout_s: int = DEFAULT_PER_CLI_TIMEOUT_S,
) -> tuple[Path | None, CLIResponse, CLIResponse]:
    """Critique one article via Codex + Anti-Gravity in parallel.

    Returns (expansion_path, codex_resp, antigravity_resp). expansion_path
    is None when BOTH CLIs failed (no point writing a placeholder file).
    The returned CLIResponses let the caller account counts + tokens.
    """
    article_body = article_path.read_text(encoding="utf-8", errors="replace")
    title_match = _TITLE_FRONTMATTER_RE.search(article_body)
    original_title = title_match.group(1).strip() if title_match else article_path.stem
    original_slug = article_path.stem

    # Resolve a source_path the prompt can cite. Prefer the first entry from
    # the article's `sources:` frontmatter; fall back to the concept file
    # path itself when frontmatter is missing or empty.
    source_path = _extract_first_source(article_body) or str(
        article_path.relative_to(repo_root)
    )

    prompt = build_critique_prompt(
        slug=original_slug,
        article_body=article_body,
        source_path=source_path,
        recent_titles=recent_titles,
    )

    codex_task = run_codex(prompt, timeout_s=per_cli_timeout_s)
    ag_task = run_antigravity(prompt, timeout_s=per_cli_timeout_s)
    codex_resp, ag_resp = await asyncio.gather(codex_task, ag_task)

    # If both failed, do not write a useless expansion file.
    if not codex_resp.ok and not ag_resp.ok:
        return None, codex_resp, ag_resp

    body = format_expansion_body(
        original_title=original_title,
        original_slug=original_slug,
        codex_text=codex_resp.text,
        antigravity_text=ag_resp.text,
        today=today,
        codex_failed=not codex_resp.ok,
        antigravity_failed=not ag_resp.ok,
    )

    expansions_dir = repo_root / EXPANSIONS_REL
    expansions_dir.mkdir(parents=True, exist_ok=True)
    lock_path = expansions_dir / ".lock"
    expansion_path = expansions_dir / f"{original_slug}.md"
    with FileLock(lock_path, exclusive=True, timeout=30.0):
        expansion_path.write_text(body, encoding="utf-8")
    return expansion_path, codex_resp, ag_resp


def _extract_first_source(article_body: str) -> str | None:
    """Pull the first entry from the `sources:` YAML list; None if absent."""
    block_match = _SOURCES_FRONTMATTER_RE.search(article_body[:1000])
    if not block_match:
        return None
    for line in block_match.group(1).splitlines():
        line = line.strip()
        if line.startswith("- "):
            return line[2:].strip().strip('"').strip("'") or None
    return None


async def run(
    *,
    repo_root: Path,
    date_iso: str | None = None,
    max_targets: int = DEFAULT_MAX_TARGETS,
    wall_budget_s: float = DEFAULT_WALL_BUDGET_S,
    per_cli_timeout_s: int = DEFAULT_PER_CLI_TIMEOUT_S,
    logger=None,
) -> CritiqueResult:
    """Orchestrate one vault_critic run end-to-end.

    Status promotion (after the loop):
      - No targets selected (no manifest / status=error / nothing fresh) → success-empty
      - All articles produced both-CLIs-failed → error
      - At least one CLI failed across the run → partial
      - Budget exceeded mid-loop → partial (with budget warning)
      - Everything clean → ok
    """
    date_iso = date_iso or date.today().isoformat()
    start = time.monotonic()
    result = CritiqueResult(
        status=STATUS_SUCCESS_EMPTY,
        run_id=datetime.now().isoformat(timespec="seconds"),
    )

    targets = select_target_articles(
        repo_root, date_iso=date_iso, max_targets=max_targets,
    )
    if not targets:
        if logger:
            logger.info("vault_critic: no target articles for %s", date_iso)
        result.duration_seconds = time.monotonic() - start
        write_critic_manifest(repo_root=repo_root, result=result, today=date_iso)
        return result

    recent_titles = _read_recent_titles(repo_root, limit=RECENT_TITLES_CONTEXT_LIMIT)
    any_failure = False
    every_article_both_failed = True

    for fp in targets:
        if time.monotonic() - start >= wall_budget_s:
            result.warnings.append(
                f"wall budget {wall_budget_s}s ran out after "
                f"{result.articles_critiqued} articles"
            )
            any_failure = True
            break

        expansion_path, codex_resp, ag_resp = await critique_one_article(
            repo_root=repo_root,
            article_path=fp,
            recent_titles=recent_titles,
            today=date_iso,
            per_cli_timeout_s=per_cli_timeout_s,
        )

        result.codex_calls += 1
        result.antigravity_calls += 1
        if codex_resp.tokens:
            result.codex_tokens_total += codex_resp.tokens
        if ag_resp.tokens:
            result.antigravity_tokens_total += ag_resp.tokens
        if not codex_resp.ok:
            result.codex_failures += 1
            any_failure = True
        if not ag_resp.ok:
            result.antigravity_failures += 1
            any_failure = True

        if expansion_path is None:
            # Both CLIs failed for this article — don't reset
            # every_article_both_failed; if this stays true across all
            # targets, the run is error-class.
            continue

        every_article_both_failed = False
        result.articles_critiqued += 1
        result.expansions_written.append(
            str(expansion_path.relative_to(repo_root))
        )

    if every_article_both_failed:
        result.status = STATUS_ERROR
    elif any_failure:
        result.status = STATUS_PARTIAL
    elif result.articles_critiqued > 0:
        result.status = STATUS_OK
    # else: result keeps its initial STATUS_SUCCESS_EMPTY (defensive default;
    # unreachable when `targets` was non-empty, because every_article_both_failed
    # covers the zero-articles case).

    result.duration_seconds = time.monotonic() - start
    write_critic_manifest(repo_root=repo_root, result=result, today=date_iso)
    return result


def _read_recent_titles(repo_root: Path, limit: int) -> list[str]:
    """Pull recent concept titles from vault/knowledge/index.md for prompt context.

    The index file's `## Concepts` section is the source of truth; titles
    surface in `[[path|Title]]` form per regenerate_index() in
    vault_synthesizer.py. Empty list on missing/unreadable index.
    """
    index_path = repo_root / KNOWLEDGE_INDEX_REL
    if not index_path.exists():
        return []
    try:
        text = index_path.read_text(encoding="utf-8")
    except OSError:
        return []
    in_concepts = False
    titles: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            in_concepts = line.strip().lower() == "## concepts"
            continue
        if not in_concepts:
            continue
        m = re.search(r"\[\[[^\]|]+\|([^\]]+)\]\]", line)
        if m:
            titles.append(m.group(1).strip())
            if len(titles) >= limit:
                break
    return titles


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Vault Critic Agent")
    parser.add_argument("--dry-run", action="store_true",
                        help="List target articles without invoking CLIs.")
    parser.add_argument("--date", default=None,
                        help="ISO date for the synth-manifest to consume (default: today).")
    parser.add_argument("--max-targets", type=int, default=DEFAULT_MAX_TARGETS)
    parser.add_argument("--wall-budget-seconds", type=float, default=DEFAULT_WALL_BUDGET_S)
    parser.add_argument("--per-cli-timeout-seconds", type=int, default=DEFAULT_PER_CLI_TIMEOUT_S)
    args = parser.parse_args(argv)

    cfg = load_config()
    logger = setup_logger(AGENT_NAME, cfg.log_dir, cfg.log_level)
    date_iso = args.date or date.today().isoformat()

    targets = select_target_articles(
        cfg.repo_root, date_iso=date_iso, max_targets=args.max_targets,
    )

    if args.dry_run:
        print("=== DRY RUN — Vault Critic ===")
        print(f"Date:          {date_iso}")
        print(f"Repo:          {cfg.repo_root}")
        print(f"Max targets:   {args.max_targets}")
        print(f"Wall budget:   {args.wall_budget_seconds}s")
        print(f"CLI timeout:   {args.per_cli_timeout_seconds}s each")
        print(f"Targets ({len(targets)}):")
        for t in targets:
            print(f"  - {t.relative_to(cfg.repo_root)}")
        print("=== END DRY RUN ===")
        return 0

    start_ms = time.monotonic_ns()
    try:
        result = asyncio.run(run(
            repo_root=cfg.repo_root,
            date_iso=date_iso,
            max_targets=args.max_targets,
            wall_budget_s=args.wall_budget_seconds,
            per_cli_timeout_s=args.per_cli_timeout_seconds,
            logger=logger,
        ))
    except Exception as exc:
        logger.exception("vault_critic failed: %s", exc)
        record_run(
            cfg.log_dir, AGENT_NAME, mode=None,
            status="error", cost_usd=0.0,
            duration_ms=int((time.monotonic_ns() - start_ms) // 1_000_000),
            turns=None, notes=str(exc)[:200],
        )
        return 1

    duration_ms = int((time.monotonic_ns() - start_ms) // 1_000_000)
    record_run(
        cfg.log_dir, AGENT_NAME, mode=None,
        status=("success" if result.status in {STATUS_OK, STATUS_PARTIAL, STATUS_SUCCESS_EMPTY}
                else result.status),
        cost_usd=0.0,
        duration_ms=duration_ms,
        turns=None,
        notes=(
            f"status={result.status} "
            f"articles={result.articles_critiqued} "
            f"codex_fail={result.codex_failures} "
            f"ag_fail={result.antigravity_failures}"
        ),
    )
    logger.info(
        "vault_critic %s articles=%d codex_fail=%d ag_fail=%d duration=%.1fs",
        result.status, result.articles_critiqued,
        result.codex_failures, result.antigravity_failures,
        result.duration_seconds,
    )
    print(
        f"OK — vault_critic {result.status}: {result.articles_critiqued} articles "
        f"({result.codex_failures + result.antigravity_failures} CLI failures, "
        f"{result.duration_seconds:.1f}s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
