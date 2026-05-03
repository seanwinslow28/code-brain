#!/usr/bin/env python3
"""Gemini Researcher Agent — Phase 3 (v3.25.0).

Processes vault/00_inbox/gemini-research-queue.md via the Phase 1
gemini_dr.run helper. Picks the first unchecked item, resolves its tier
marker, delegates to gemini_dr.run (no_confirm=True — autonomous; cost
gates are the protection), marks done with timestamp + wikilink.

This is a thin wrapper — gemini_dr.run does all heavy lifting.

Usage:
    python3 agents/gemini_researcher.py --mode queue
    python3 agents/gemini_researcher.py --mode queue --dry-run
    python3 agents/gemini_researcher.py --mode oneshot --query "Your question" --tier dr
    python3 agents/gemini_researcher.py --mode oneshot --query "Your question" --tier max
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path

# Add agents-sdk/ to Python path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config
from lib.logging_setup import record_run, setup_logger

# Import the Phase 1 helper — never duplicate logic
from scripts.gemini_dr import run as run_research
from scripts.gemini_dr import slugify

AGENT_NAME = "gemini-researcher"

# Tier marker patterns in queue items.
# Recognized formats: `tier: dr`, `tier: dr-max`, `tier: max`
_TIER_PATTERN = re.compile(r"\btier:\s*(dr-max|dr|max)\b", re.IGNORECASE)

# Maps the raw tier-marker value to the canonical tier understood by gemini_dr.run
_TIER_MAP = {
    "dr": "dr",
    "dr-max": "max",
    "max": "max",
}


def _next_unchecked(queue_path: Path) -> str | None:
    """Return the first `- [ ] ...` line text from the queue file, or None."""
    if not queue_path.exists():
        return None
    for line in queue_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*-\s*\[\s\]\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def _extract_tier(queue_item: str, default_tier: str) -> tuple[str, str]:
    """Extract tier from a queue item and return (canonical_tier, clean_query).

    Supported formats:
        tier: dr   → ("dr", <text without marker>)
        tier: max  → ("max", <text without marker>)
        tier: dr-max → ("max", <text without marker>)
        (no marker) → (default_tier, <original text>)

    The clean_query strips the tier marker so gemini_dr.run gets a pure question.
    """
    m = _TIER_PATTERN.search(queue_item)
    if m:
        raw = m.group(1).lower()
        tier = _TIER_MAP.get(raw, default_tier)
        # Strip the tier marker from the query
        clean = _TIER_PATTERN.sub("", queue_item).strip().strip("-").strip()
        return tier, clean  # may be empty string — caller must guard
    return default_tier, queue_item


def _mark_done(
    queue_path: Path, queue_item: str, vault_root: Path, tier: str, query: str
) -> bool:
    """Mark `- [ ] queue_item` as done with timestamp + wikilink.

    The wikilink target is derived from the slugified query so it matches the
    file gemini_dr.run will write to vault/20_projects/research/.

    Returns True if a line was rewritten.
    """
    if not queue_path.exists():
        return False
    text = queue_path.read_text(encoding="utf-8")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = date.today().isoformat()
    slug = slugify(query)
    # Vault-relative wikilink — Obsidian resolves [[wikilinks]] relative to
    # vault root, so we must strip the leading "vault/" prefix.
    topical_path = vault_root / "20_projects" / "research" / f"{today}-{slug}.md"
    rel_link = topical_path.relative_to(vault_root).with_suffix("").as_posix()
    note_link = f"[[{rel_link}]]"
    needle = re.compile(
        r"^(\s*-\s*\[)\s(\]\s+" + re.escape(queue_item) + r")\s*$",
        re.MULTILINE,
    )
    new_text, n = needle.subn(rf"\1x\2 — done {timestamp} → {note_link}", text, count=1)
    if n == 0:
        return False
    queue_path.write_text(new_text, encoding="utf-8")
    return True


def run(
    mode: str,
    dry_run: bool = False,
    oneshot_query: str | None = None,
    cli_tier: str | None = None,
) -> int:
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir, config.log_level, mode=mode)

    raw_cfg = config.agents.get("gemini_researcher", {})
    if not raw_cfg.get("enabled", False):
        logger.warning("gemini_researcher disabled in config.toml — exiting")
        return 0

    # Resolve queue path from config
    queue_path = config.repo_root / raw_cfg["queue_path"]

    # Resolve default tier from [gemini] section via a minimal TOML read.
    # We don't re-import _load_gemini_cfg to avoid tight coupling to its internals;
    # instead we pull it from config.agents fallback or read [gemini] directly.
    import tomllib
    config_path = Path(__file__).parent.parent / "config.toml"
    with open(config_path, "rb") as f:
        raw_toml = tomllib.load(f)
    default_tier = raw_toml.get("gemini", {}).get("default_tier", "dr")

    if mode == "oneshot":
        if not oneshot_query:
            logger.error("--mode oneshot requires --query")
            return 2
        # CLI --tier flag wins for oneshot
        if cli_tier:
            tier = _TIER_MAP.get(cli_tier, cli_tier)
        else:
            tier = default_tier
        query = oneshot_query.strip()
        queue_item = None  # not from queue — no mark-done
    else:  # queue
        queue_item = _next_unchecked(queue_path)
        if not queue_item:
            logger.info(f"Queue empty at {queue_path} — nothing to do")
            record_run(
                config.log_dir, AGENT_NAME, mode,
                status="empty-queue", cost_usd=0.0, duration_ms=0, turns=0,
                notes="no unchecked items",
            )
            return 0

        # CLI --tier flag overrides the queue marker for one-off queue runs too.
        # Always strip the tier marker from the queue item so the API receives
        # a clean question (not "tier: max Extended question...").
        if cli_tier:
            tier = _TIER_MAP.get(cli_tier, cli_tier)
            _, query = _extract_tier(queue_item, default_tier)  # strip marker; ignore extracted tier
        else:
            tier, query = _extract_tier(queue_item, default_tier)

    # Guard against marker-only queue lines (e.g. "tier: dr-max" with no question).
    # _extract_tier returns empty string in that case — refuse rather than waste spend.
    if not query:
        logger.error(f"Queue item has no query after stripping tier marker: {queue_item!r}")
        record_run(
            config.log_dir, AGENT_NAME, mode,
            status="empty-query", cost_usd=0.0, duration_ms=0, turns=0,
            notes=f"queue item: {queue_item!r}",
        )
        return 2

    logger.info(f"Selected query: {query!r}  tier={tier}  mode={mode}")

    if dry_run:
        print("=== DRY RUN — Gemini Researcher ===")
        print(f"Mode:    {mode}")
        print(f"Query:   {query}")
        print(f"Tier:    {tier}")
        print(f"Queue:   {queue_path}")
        print(f"Would call: gemini_dr.run(query={query!r}, tier={tier!r}, no_confirm=True)")
        print("=== END DRY RUN ===")
        return 0

    # Delegate fully to Phase 1 helper.
    # no_confirm=True because this is an autonomous agent — cost gates protect.
    t_start = time.time()
    exit_code = run_research(
        query=query,
        tier=tier,
        dry_run=False,
        no_confirm=True,
    )
    duration_ms = int((time.time() - t_start) * 1000)

    if exit_code == 0:
        # Mark queue item done after a successful run (queue mode only)
        if mode == "queue" and queue_item is not None:
            ok = _mark_done(queue_path, queue_item, config.vault_root, tier, query)
            if not ok:
                logger.warning(
                    f"Could not mark queue item done — line not found in {queue_path}. "
                    f"Research note was still written."
                )
        record_run(
            config.log_dir, AGENT_NAME, mode,
            status="success", cost_usd=None,
            duration_ms=duration_ms, turns=0,
            notes=f"tier={tier} query={query[:80]!r}",
        )
    elif exit_code == 1:
        # Cap refusal — record and exit cleanly (not an error)
        record_run(
            config.log_dir, AGENT_NAME, mode,
            status="cap-refused", cost_usd=0.0,
            duration_ms=duration_ms, turns=0,
            notes=f"tier={tier} query={query[:80]!r}",
        )
    else:
        # Error (exit 2 = usage, 3 = API failure)
        record_run(
            config.log_dir, AGENT_NAME, mode,
            status="error", cost_usd=0.0,
            duration_ms=duration_ms, turns=0,
            notes=f"gemini_dr.run exit={exit_code} tier={tier} query={query[:80]!r}",
        )

    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description="Gemini Researcher Agent")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["queue", "oneshot"],
        help="queue: pick first unchecked from gemini-research-queue.md. oneshot: use --query.",
    )
    parser.add_argument("--query", help="Question to research (oneshot mode only).")
    parser.add_argument(
        "--tier",
        choices=["dr", "max"],
        default=None,
        help=(
            "Model tier override: 'dr' (Deep Research) or 'max' (DR Max). "
            "In oneshot mode this sets the tier directly. "
            "In queue mode this overrides the tier marker in the queue item. "
            "Default: read from queue item marker, or [gemini].default_tier if absent."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print intended call without making any API request.",
    )
    args = parser.parse_args()
    return run(
        mode=args.mode,
        dry_run=args.dry_run,
        oneshot_query=args.query,
        cli_tier=args.tier,
    )


if __name__ == "__main__":
    sys.exit(main())
