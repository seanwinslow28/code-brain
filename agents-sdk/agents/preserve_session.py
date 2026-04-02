#!/usr/bin/env python3
"""Preserve Session Agent — save Claude Code session summaries to vault.

Runs on MacBook Pro (localhost), 100% local via Qwen3-14B through MLX-LM.
After a Claude Code session ends, summarizes what was built, decisions made,
and open threads — saves to vault as a structured session note.

Usage:
    python3 agents/preserve_session.py
    python3 agents/preserve_session.py --dry-run
    python3 agents/preserve_session.py --topic "Phase 4 build"
    python3 agents/preserve_session.py --baton-file /path/to/session_summary.md
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any

# Add agents-sdk/ to Python path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config
from lib.logging_setup import record_run, setup_logger
from lib.skill_loader import load_skills

AGENT_NAME = "preserve-session"

# Safety limits — 100% local, no API cost
MAX_TURNS = 10
MAX_BUDGET_USD = 0.00

# Session log discovery
CLAUDE_DIR = Path.home() / ".claude"
SESSION_LOGS_DIR = CLAUDE_DIR / "projects"


def find_latest_session_log() -> Path | None:
    """Find the most recent Claude Code session transcript.

    Claude Code stores session data in ~/.claude/projects/.
    Returns the path to the most recent session file, or None.
    """
    if not SESSION_LOGS_DIR.exists():
        return None

    # Look for session files across project directories
    session_files = []
    for proj_dir in SESSION_LOGS_DIR.iterdir():
        if not proj_dir.is_dir():
            continue
        for f in proj_dir.rglob("*.json"):
            if f.stat().st_size > 100:  # Skip tiny/empty files
                session_files.append(f)

    if not session_files:
        return None

    # Return most recently modified
    return max(session_files, key=lambda f: f.stat().st_mtime)


def read_baton_file(baton_path: Path) -> str | None:
    """Read a manual session summary from a baton file."""
    if baton_path.exists():
        return baton_path.read_text(encoding="utf-8").strip()
    return None


def build_preamble(config: Any) -> str:
    """Build the autonomous agent preamble."""
    today = date.today().isoformat()

    return (
        f"You are Sean's session preservation agent.\n"
        f"Current date: {today}\n"
        f"Vault root: {config.vault_root}\n"
        f"\n"
        f"ZERO-INTERACTION MANDATE:\n"
        f"You are running autonomously. No human is available.\n"
        f"You MUST make best-judgment decisions autonomously.\n"
        f"\n"
        f"PURPOSE:\n"
        f"Summarize the Claude Code session that just ended into a structured\n"
        f"vault note so that future sessions can pick up where this one left off.\n"
        f"\n"
        f"OUTPUT FORMAT:\n"
        f"Create a vault note with YAML frontmatter and these sections:\n"
        f"- ## What Was Built — files created/modified, features implemented\n"
        f"- ## Key Decisions — architectural choices, trade-offs made\n"
        f"- ## Open Questions — unresolved issues, things to investigate\n"
        f"- ## Next Steps — concrete tasks for the next session\n"
        f"\n"
        f"FRONTMATTER:\n"
        f"```yaml\n"
        f"---\n"
        f"type: session-log\n"
        f"date: {today}\n"
        f"status: complete\n"
        f"tags: [session-log]\n"
        f"---\n"
        f"```\n"
    )


def build_prompt(config: Any, session_input: str, topic: str | None = None) -> str:
    """Build the task prompt for session preservation."""
    today = date.today().isoformat()
    topic_slug = topic.lower().replace(" ", "-")[:30] if topic else "session"
    output_path = (
        config.vault_root / "03_Resources" / "Session-Logs"
        / f"session-{today}-{topic_slug}.md"
    )

    return (
        f"Summarize this Claude Code session into a structured vault note.\n"
        f"\n"
        f"SESSION INPUT:\n"
        f"```\n"
        f"{session_input[:8000]}\n"
        f"```\n"
        f"\n"
        f"Topic: {topic or 'auto-detect from session content'}\n"
        f"\n"
        f"Write the session note to: {output_path}\n"
        f"Create the directory if it doesn't exist.\n"
        f"\n"
        f"Keep it concise — focus on decisions and outcomes, not process."
    )


def build_options(config: Any):  # -> ClaudeAgentOptions (imported lazily)
    """Build ClaudeAgentOptions for the preserve session agent."""
    from claude_agent_sdk import ClaudeAgentOptions

    agent_cfg = config.agent_config("preserve_session")
    skills_prompt = load_skills(
        agent_cfg.skills or ["preserve-session", "vault-read-write"],
        config.skills_dir,
    )

    env = {}
    if config.anthropic_api_key:
        env["ANTHROPIC_API_KEY"] = config.anthropic_api_key

    return ClaudeAgentOptions(
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": skills_prompt,
        },
        allowed_tools=[
            "Read", "Write", "Edit", "Glob", "Grep", "Bash",
        ],
        permission_mode=config.safety.permission_mode,
        max_turns=MAX_TURNS,
        max_budget_usd=MAX_BUDGET_USD,
        cwd=str(config.repo_root),
        setting_sources=["project"],
        env=env,
    )


async def run(dry_run: bool = False, topic: str | None = None, baton_file: str | None = None) -> None:
    """Run the preserve session agent."""
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir, config.log_level)

    agent_cfg = config.agent_config("preserve_session")
    if not agent_cfg.enabled:
        logger.warning("Preserve session agent is disabled in config.toml")
        return

    logger.info("Starting preserve session agent")
    start_time = time.monotonic()

    # Determine session input source
    session_input = None

    if baton_file:
        baton_path = Path(baton_file)
        session_input = read_baton_file(baton_path)
        if session_input:
            logger.info(f"Read session summary from baton file: {baton_path}")
        else:
            logger.error(f"Baton file not found or empty: {baton_path}")
            return

    if not session_input:
        # Try to find the latest Claude Code session log
        latest = find_latest_session_log()
        if latest:
            try:
                raw = latest.read_text(encoding="utf-8", errors="replace")
                # Extract just the conversation content (skip binary/metadata)
                if raw.startswith("{"):
                    data = json.loads(raw)
                    # Try common session log formats
                    if "messages" in data:
                        msgs = data["messages"]
                        session_input = "\n\n".join(
                            f"[{m.get('role', '?')}] {m.get('content', '')[:500]}"
                            for m in msgs[-20:]  # Last 20 messages
                        )
                    else:
                        session_input = raw[:8000]
                else:
                    session_input = raw[:8000]
                logger.info(f"Read session log: {latest}")
            except Exception as e:
                logger.warning(f"Failed to read session log {latest}: {e}")

    if not session_input:
        session_input = (
            "No session transcript available. "
            "Generate a minimal session note template with empty sections "
            "that can be filled in manually."
        )
        logger.warning("No session input found — generating template")

    if dry_run:
        today = date.today().isoformat()
        topic_slug = topic.lower().replace(" ", "-")[:30] if topic else "session"
        output_path = (
            config.vault_root / "03_Resources" / "Session-Logs"
            / f"session-{today}-{topic_slug}.md"
        )
        print("=== DRY RUN — Preserve Session Agent ===")
        print(f"\nMax turns: {MAX_TURNS}")
        print(f"Max budget: ${MAX_BUDGET_USD}")
        print(f"Output path: {output_path}")
        print(f"Topic: {topic or 'auto-detect'}")
        print(f"Session input length: {len(session_input)} chars")
        print(f"Session input source: {'baton file' if baton_file else 'auto-detected log'}")
        print(f"\n--- Session Input Preview ---")
        print(session_input[:500] + "..." if len(session_input) > 500 else session_input)
        print(f"\n--- Routing ---")
        print(f"Target machine: MacBook Pro (localhost)")
        print(f"Target model: Qwen3-14B via MLX-LM")
        print(f"Cost: $0.00 (100% local)")
        print(f"Schedule: on-demand (no fixed schedule)")
        print("\n=== END DRY RUN ===")
        return

    preamble = build_preamble(config)
    prompt = preamble + "\n\n" + build_prompt(config, session_input, topic)
    options = build_options(config)

    result_msg = None
    try:
        from claude_agent_sdk import ResultMessage, query

        async for message in query(prompt=prompt, options=options):
            if isinstance(message, ResultMessage):
                result_msg = message
                logger.info(
                    f"Completed: status={message.subtype}, "
                    f"turns={message.num_turns}, "
                    f"cost=${message.total_cost_usd}"
                )

        elapsed_ms = int((time.monotonic() - start_time) * 1000)

        record_run(
            log_dir=config.log_dir,
            agent_name=AGENT_NAME,
            mode=None,
            status=result_msg.subtype if result_msg else "unknown",
            cost_usd=result_msg.total_cost_usd if result_msg else 0.00,
            duration_ms=elapsed_ms,
            turns=result_msg.num_turns if result_msg else None,
            notes=f"topic={topic or 'auto'}",
        )

    except Exception as e:
        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        logger.error(f"Preserve session agent failed: {e}")
        record_run(
            log_dir=config.log_dir,
            agent_name=AGENT_NAME,
            mode=None,
            status="error",
            cost_usd=0.00,
            duration_ms=elapsed_ms,
            turns=None,
            notes=str(e)[:200],
        )
        raise


def main():
    parser = argparse.ArgumentParser(description="Preserve Session Agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without calling the API",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Topic label for the session (e.g., 'Phase 4 build')",
    )
    parser.add_argument(
        "--baton-file",
        type=str,
        default=None,
        help="Path to a baton file with manual session summary",
    )
    args = parser.parse_args()

    asyncio.run(run(dry_run=args.dry_run, topic=args.topic, baton_file=args.baton_file))


if __name__ == "__main__":
    main()
