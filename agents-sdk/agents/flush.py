#!/usr/bin/env python3
"""SessionEnd flush agent — extract session knowledge into daily logs.

Triggered by `.claude/hooks/session-end-flush.sh` on every Claude Code
session close, passed the transcript path. Parses the JSONL, routes by
message count (<100 → gemma4:e4b on Mac Mini via inbox_triage routing;
≥100 → Qwen3-14B on MacBook Pro), asks the LLM for a 5-section structured
summary, and appends a new block to `vault/daily/YYYY-MM-DD.md` (creating
the file if missing).

Phase 2 (2026-04-27): when `[artifacts.per_agent.flush]` lists `SOUL` in
its `on_demand` array, the prompt is prefixed with all three domain SOUL
bodies (the-block, creative-studio, life-systems) so the local model can
cross-reference new entries against established Tier-A items. ~46K-char
prepend, well within both gemma4:e4b's 32K and Qwen3-14B's 40K+ windows.

All writes serialize through a FileLock on `vault/daily/.lock`.

Recursion guard: the hook and this agent both respect the env var
CLAUDE_INVOKED_BY — when set, run_flush() exits cleanly so flush-inside-
flush can't happen.

Usage:
    python3 agents/flush.py --transcript <path-to.jsonl>
    python3 agents/flush.py --latest            # auto-discover newest
    python3 agents/flush.py --dry-run           # no write
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable

import httpx

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.artifact_loader import DOMAINS, load_artifact
from lib.config import Config, load_config
from lib.filelock import FileLock
from lib.hybrid_router import HybridRouter, RoutingDecision, WOLUnavailable
from lib.logging_setup import record_run, setup_logger
from lib.session_transcript import (
    TranscriptMessage,
    message_count,
    parse_transcript,
)

AGENT_NAME = "flush"
MAX_TURNS = 15
MAX_BUDGET_USD = 0.00

COMPLEX_MESSAGE_THRESHOLD = 100  # §7.3 decision (locked)

DAILY_LOG_TEMPLATE_HEADER = """# Daily Log — {date}

"""

EXTRACTION_PROMPT = """You are summarizing a single Claude Code session for a daily vault log.

Return ONLY a JSON object with these five keys. Each value is a list of
short strings (≤120 chars). Omit obvious filler. Quotes must be verbatim
from the transcript.

{{
  "decisions": [...],   // concrete decisions made this session
  "lessons":   [...],   // durable lessons learned
  "actions":   [...],   // open follow-ups (imperative form)
  "patterns":  [...],   // meta observations worth reusing
  "quotes":    [...]    // 2–3 verbatim snippets
}}

Session transcript (concatenated user + assistant text):

{transcript_text}

Respond with ONLY the JSON object, no prose.
"""


class RoutingTier(Enum):
    SIMPLE = "simple"   # <100 msg → gemma4:e4b on Mac Mini (inbox_triage routing)
    COMPLEX = "complex"  # ≥100 msg → Qwen3-14B on MacBook Pro


@dataclass
class FlushResult:
    status: str                    # "ok" | "error" | "recursion-guard" | "deferred"
    date: str = ""
    tier: RoutingTier | None = None
    messages: int = 0
    sections_written: int = 0
    error: str = ""
    duration_ms: int = 0


def pick_routing_tier(n_messages: int) -> RoutingTier:
    """<100 messages → Mac Mini, ≥100 → MacBook Pro."""
    return RoutingTier.SIMPLE if n_messages < COMPLEX_MESSAGE_THRESHOLD else RoutingTier.COMPLEX


def build_soul_prepend(config: Config | None) -> str:
    """Three-domain SOUL bodies, framed as a reference block.

    Locked decision (2026-04-23, plan §9 Q3): every flush run prepends
    all three domain SOULs. No domain-inference helper. Returns "" when
    `[artifacts].enabled = false`, when the meta_agent has no per-agent
    entry, or when `flush.on_demand` doesn't include `SOUL` — that path
    is the instant-rollback per `[artifacts.per_agent.flush] = {}`.
    """
    if config is None:
        return ""
    cfg = config.artifact_config("flush")
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
        "--- BEGIN OPERATING-MODEL SOUL CONTEXT (reference) ---\n\n"
        + "\n".join(sections)
        + "\n--- END OPERATING-MODEL SOUL CONTEXT ---\n\n"
        "--- BEGIN SESSION TRANSCRIPT EXTRACTION ---\n\n"
    )


def _concat_messages(messages: list[TranscriptMessage], max_chars: int = 40000) -> str:
    """Flatten transcript to plain text for the extractor prompt.

    Truncates to `max_chars` so the combined prompt (SOUL prepend + body)
    stays within both gemma4:e4b's 32K and Qwen3-14B's 40K+ context windows.
    """
    parts: list[str] = []
    total = 0
    for m in messages:
        snippet = f"[{m.role}] {m.text}\n"
        if total + len(snippet) > max_chars:
            parts.append("…[truncated]…\n")
            break
        parts.append(snippet)
        total += len(snippet)
    return "".join(parts)


def format_daily_log_body(
    *,
    session_summary: dict[str, Any],
    extracted: dict[str, list[str]],
) -> str:
    """Render the session block markdown (everything below the file header)."""
    tool = session_summary.get("tool", "claude-code")
    duration = session_summary.get("duration", "unknown")
    messages = session_summary.get("messages", "?")
    tag = session_summary.get("tag", "general")
    time_str = session_summary.get("time", datetime.now().strftime("%H:%M"))

    lines: list[str] = []
    lines.append(f"\n---\n\n## Sessions\n- {tool}: {duration}, {messages} messages, tag: {tag} ({time_str})\n")

    def _render(section: str, items: list[str], bullet_prefix: str = "-") -> None:
        if not items:
            return
        lines.append(f"\n## {section}\n")
        for it in items:
            lines.append(f"{bullet_prefix} {it}\n")

    _render("Decisions", extracted.get("decisions", []))
    _render("Lessons", extracted.get("lessons", []))
    _render("Action Items", extracted.get("actions", []), bullet_prefix="- [ ]")
    _render("Patterns", extracted.get("patterns", []))
    quotes = extracted.get("quotes", [])
    if quotes:
        lines.append("\n## Quotes\n")
        for q in quotes:
            lines.append(f"> {q}\n")
    return "".join(lines)


def append_to_daily_log(
    daily_log_path: Path,
    body: str,
    *,
    lock_dir: Path | None = None,
    lock_timeout_s: float = 30.0,
) -> None:
    """Append a session block to today's daily log, filelocked.

    If the file doesn't exist, write the header first. Lock file lives at
    `<lock_dir>/.lock` (default: parent of daily_log_path).
    """
    lock_dir = lock_dir or daily_log_path.parent
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / ".lock"

    with FileLock(lock_path, exclusive=True, timeout=lock_timeout_s):
        if not daily_log_path.exists():
            daily_log_path.write_text(
                DAILY_LOG_TEMPLATE_HEADER.format(date=date.today().isoformat()),
                encoding="utf-8",
            )
        with open(daily_log_path, "a", encoding="utf-8") as fh:
            fh.write(body)


def _default_llm_caller(prompt: str, tier: RoutingTier) -> dict[str, list[str]]:
    """Default LLM caller — hits Ollama (simple) or LM Studio (complex) directly.

    Returns a parsed dict with the 5 extraction keys. On parse failure,
    returns empty lists (never raises — flush.py prefers a thin log to
    crashing the SessionEnd path).
    """
    try:
        config_path = Path(__file__).parent.parent / "config.toml"
        import tomllib
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
        router = HybridRouter.from_config(config)

        if tier == RoutingTier.SIMPLE:
            async def go() -> RoutingDecision:
                # inbox_triage routes to gemma4:e4b on Mac Mini per
                # config.toml task_map (swapped 2026-04-18, v3.14.3).
                return await router.route("inbox_triage")
            decision = asyncio.run(go())
        else:
            async def go2() -> RoutingDecision:
                return await router.route_to_macbook(
                    task="vault_synthesis", wake_timeout_s=30.0
                )
            decision = asyncio.run(go2())
    except (WOLUnavailable, Exception):
        return {"decisions": [], "lessons": [], "actions": [], "patterns": [], "quotes": []}

    try:
        if decision.runtime == "ollama":
            resp = httpx.post(
                f"{decision.base_url}/api/generate",
                json={"model": decision.model, "prompt": prompt, "stream": False},
                timeout=60.0,
            )
            resp.raise_for_status()
            text = resp.json().get("response", "")
        else:
            resp = httpx.post(
                f"{decision.base_url}/v1/chat/completions",
                json={
                    "model": decision.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
                timeout=120.0,
            )
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return {"decisions": [], "lessons": [], "actions": [], "patterns": [], "quotes": []}

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return {"decisions": [], "lessons": [], "actions": [], "patterns": [], "quotes": []}
    try:
        parsed = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return {"decisions": [], "lessons": [], "actions": [], "patterns": [], "quotes": []}
    return {
        "decisions": list(parsed.get("decisions", [])),
        "lessons": list(parsed.get("lessons", [])),
        "actions": list(parsed.get("actions", [])),
        "patterns": list(parsed.get("patterns", [])),
        "quotes": list(parsed.get("quotes", [])),
    }


def run_flush(
    *,
    transcript_path: Path,
    vault_daily_dir: Path,
    llm_caller: Callable[[str, RoutingTier], dict[str, list[str]]] | None = None,
    dry_run: bool = False,
    config: Config | None = None,
    trigger: str = "session-end",
) -> FlushResult:
    """Top-level flush entrypoint (sync, easy to test).

    Recursion-guards on CLAUDE_INVOKED_BY. Parses transcript. Picks tier.
    Calls `llm_caller(prompt, tier)` (defaults to hitting local models over
    HTTP — can be overridden for tests). Appends to the daily log.

    When `config` is provided and the artifacts wiring is on, the prompt
    is prefixed with all three domain SOUL bodies. `config=None` keeps the
    pre-Phase-2 behavior (no SOUL prepend) — used by existing tests.

    `trigger` flows into the daily-log session block's `tag:` field so
    post-hoc analysis can distinguish session-end from pre-compact (Phase A)
    and manual flushes.
    """
    start_ns = time.monotonic_ns()

    if os.environ.get("CLAUDE_INVOKED_BY") == "flush":
        return FlushResult(status="recursion-guard")

    transcript_path = Path(transcript_path)
    if not transcript_path.exists():
        return FlushResult(
            status="error",
            error=f"transcript not found: {transcript_path}",
        )

    try:
        messages = parse_transcript(transcript_path)
    except Exception as exc:
        return FlushResult(status="error", error=f"parse failed: {exc}")

    n = len(messages)
    tier = pick_routing_tier(n)
    transcript_text = _concat_messages(messages)
    soul_prepend = build_soul_prepend(config)
    prompt = soul_prepend + EXTRACTION_PROMPT.format(transcript_text=transcript_text)

    caller = llm_caller or _default_llm_caller

    # Invoke extractor while advertising we are flush (recursion guard for
    # any nested sub-agent that would call us again).
    env_before = os.environ.get("CLAUDE_INVOKED_BY")
    os.environ["CLAUDE_INVOKED_BY"] = "flush"
    try:
        extracted = caller(prompt, tier)
    finally:
        if env_before is None:
            os.environ.pop("CLAUDE_INVOKED_BY", None)
        else:
            os.environ["CLAUDE_INVOKED_BY"] = env_before

    today = date.today().isoformat()
    session_summary = {
        "tool": "claude-code",
        "duration": f"{len(messages)} msg",
        "messages": n,
        "tag": trigger,
        "time": datetime.now().strftime("%H:%M"),
    }
    body = format_daily_log_body(
        session_summary=session_summary, extracted=extracted
    )

    if not dry_run:
        daily_path = vault_daily_dir / f"{today}.md"
        append_to_daily_log(daily_path, body, lock_dir=vault_daily_dir)

    sections = sum(1 for k in ("decisions", "lessons", "actions", "patterns", "quotes") if extracted.get(k))
    duration_ms = (time.monotonic_ns() - start_ns) // 1_000_000

    return FlushResult(
        status="ok",
        date=today,
        tier=tier,
        messages=n,
        sections_written=sections,
        duration_ms=duration_ms,
    )


def _find_latest_transcript() -> Path | None:
    base = Path.home() / ".claude" / "projects"
    if not base.exists():
        return None
    candidates = list(base.rglob("*.jsonl"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def main() -> int:
    parser = argparse.ArgumentParser(description="SessionEnd flush agent")
    parser.add_argument("--transcript", type=Path, default=None, help="Path to session JSONL transcript")
    parser.add_argument("--latest", action="store_true", help="Auto-discover most recent transcript")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--trigger",
        choices=["session-end", "pre-compact", "manual"],
        default="session-end",
        help="What event invoked this flush; flows into the daily-log session tag.",
    )
    args = parser.parse_args()

    cfg = load_config()
    logger = setup_logger(AGENT_NAME, cfg.log_dir, cfg.log_level)

    transcript = args.transcript
    if transcript is None and args.latest:
        transcript = _find_latest_transcript()
    if transcript is None:
        logger.error("No --transcript path provided and --latest found nothing")
        return 2

    vault_daily_dir = cfg.vault_root / "daily"

    start_ns = time.monotonic_ns()
    result = run_flush(
        transcript_path=transcript,
        vault_daily_dir=vault_daily_dir,
        llm_caller=None,
        dry_run=args.dry_run,
        config=cfg,
        trigger=args.trigger,
    )
    duration_ms = (time.monotonic_ns() - start_ns) // 1_000_000

    logger.info(
        "flush %s messages=%d tier=%s sections=%d duration=%dms",
        result.status,
        result.messages,
        result.tier.value if result.tier else "n/a",
        result.sections_written,
        duration_ms,
    )

    record_run(
        cfg.log_dir,
        AGENT_NAME,
        mode=result.tier.value if result.tier else None,
        status=result.status,
        cost_usd=0.0,
        duration_ms=duration_ms,
        turns=None,
        notes=result.error or f"{result.messages} msgs",
    )

    return 0 if result.status in ("ok", "recursion-guard", "deferred") else 1


if __name__ == "__main__":
    sys.exit(main())
