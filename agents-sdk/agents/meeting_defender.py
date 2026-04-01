#!/usr/bin/env python3
"""Meeting Defender Agent — autonomous calendar audit and meeting optimization.

Routes to: Mac Mini for pre-classification (phi4-mini-reasoning),
           Claude Haiku for synthesis.
Reads calendar for the upcoming week, identifies meetings that could be
declined or shortened. Drafts Slack DMs — NEVER auto-declines.

Usage:
    python3 agents/meeting_defender.py
    python3 agents/meeting_defender.py --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import date, timedelta
from pathlib import Path

# Add agents-sdk/ to Python path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config
from lib.logging_setup import record_run, setup_logger
from lib.skill_loader import load_skills

AGENT_NAME = "meeting-defender"

# Safety limits — lightweight analysis, Haiku for synthesis
MAX_TURNS = 10
MAX_BUDGET_USD = 0.25

# Both calendars must be queried
CALENDARS = [
    "sean.winslow28@gmail.com",
    "swinslow@theblock.co",
]


def build_preamble(config) -> str:
    """Build the autonomous agent preamble."""
    today = date.today().isoformat()
    week_end = (date.today() + timedelta(days=7)).isoformat()

    return (
        f"You are Sean's autonomous Meeting Defender agent.\n"
        f"Current date: {today}\n"
        f"Vault root: {config.vault_root}\n"
        f"\n"
        f"ZERO-INTERACTION MANDATE:\n"
        f"You are running autonomously via launchd on Monday mornings.\n"
        f"No human is available. Make best-judgment decisions autonomously.\n"
        f"\n"
        f"CRITICAL SAFETY RULE:\n"
        f"You MUST NEVER auto-decline, cancel, or modify any calendar event.\n"
        f"You ONLY produce a report with recommendations and draft messages.\n"
        f"Sean will review the report and take action manually.\n"
        f"\n"
        f"CALENDARS TO QUERY (always check BOTH in parallel):\n"
        f"  - {CALENDARS[0]} (personal)\n"
        f"  - {CALENDARS[1]} (work)\n"
        f"\n"
        f"DATE RANGE: {today} to {week_end}\n"
    )


def build_prompt(config) -> str:
    """Build the task prompt for meeting defense analysis."""
    today = date.today().isoformat()
    week_end = (date.today() + timedelta(days=7)).isoformat()
    output_path = config.vault_root / "02_Areas" / "Work" / f"meeting-defender-{today}.md"

    return (
        f"Execute the Meeting Defender protocol.\n"
        f"\n"
        f"Step 1: Read this week's calendar events.\n"
        f"  - Query BOTH calendars: {CALENDARS[0]} AND {CALENDARS[1]}\n"
        f"  - Date range: {today} to {week_end}\n"
        f"  - Use the Google Calendar MCP tools (gcal_list_events)\n"
        f"  - Collect: event name, start/end time, organizer, attendee count,\n"
        f"    recurring status, description/agenda (if present)\n"
        f"\n"
        f"Step 2: Classify each meeting into one of:\n"
        f"  - KEEP: Essential — has clear agenda, you're a required participant,\n"
        f"    or it's a 1:1 with your manager/reports\n"
        f"  - DECLINE: Can be skipped — no agenda, >6 attendees where you're\n"
        f"    optional, FYI-only status meetings, or duplicate of another meeting\n"
        f"  - SHORTEN: Could be 15min instead of 30, or 30 instead of 60 —\n"
        f"    meetings with thin agendas or recurring syncs that rarely fill time\n"
        f"  - ASYNC: Could be replaced with a Slack message or document\n"
        f"\n"
        f"Step 3: For each DECLINE/SHORTEN/ASYNC meeting, draft a polite\n"
        f"  Slack DM to the organizer explaining:\n"
        f"  - Why you'd like to skip/shorten (be specific and constructive)\n"
        f"  - An alternative (async update, shorter slot, read the notes after)\n"
        f"  - Keep the tone warm and professional — Sean is a PM who values\n"
        f"    relationships. Never be dismissive about anyone's meeting.\n"
        f"\n"
        f"Step 4: Write the report to: {output_path}\n"
        f"  Format:\n"
        f"  - Header with date range and total meeting hours\n"
        f"  - Markdown table: Meeting | Day/Time | Duration | Organizer |\n"
        f"    Recommendation | Reason\n"
        f"  - Estimated hours saved if all recommendations are followed\n"
        f"  - Draft Slack messages section (one per declinable meeting)\n"
        f"\n"
        f"Step 5: Output the report path and summary stats to stdout.\n"
        f"\n"
        f"IMPORTANT:\n"
        f"- Query BOTH calendars (personal + work) — events may be on either\n"
        f"- NEVER call any tool that modifies, declines, or deletes events\n"
        f"- Draft messages only — you are a recommendation engine, not an executor\n"
        f"- If calendar access fails, report the error and exit gracefully\n"
    )


def build_options(config):
    """Build ClaudeAgentOptions for the meeting defender agent."""
    from claude_agent_sdk import ClaudeAgentOptions
    from lib.custom_tools import create_vault_mcp_server

    agent_cfg = config.agent_config("meeting_defender")
    skills_prompt = load_skills(
        agent_cfg.skills or ["meeting-prep", "vault-read-write"],
        config.skills_dir,
    )

    vault_server = create_vault_mcp_server()

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
            "Read", "Write", "Edit", "Glob", "Grep",
            "mcp__vault-tools__vault_inject",
            # Google Calendar MCP — READ ONLY
            "mcp__claude_ai_Google_Calendar__gcal_list_events",
            "mcp__claude_ai_Google_Calendar__gcal_list_calendars",
            "mcp__claude_ai_Google_Calendar__gcal_get_event",
            # Explicitly NOT included: gcal_create_event, gcal_delete_event,
            # gcal_update_event, gcal_respond_to_event
        ],
        permission_mode=config.safety.permission_mode,
        max_turns=MAX_TURNS,
        max_budget_usd=MAX_BUDGET_USD,
        cwd=str(config.repo_root),
        mcp_servers={"vault-tools": vault_server},
        setting_sources=["project"],
        env=env,
    )


async def run(dry_run: bool = False) -> None:
    """Run the meeting defender agent."""
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir)

    agent_cfg = config.agent_config("meeting_defender")
    if not agent_cfg.enabled:
        logger.warning("Meeting defender agent is disabled in config.toml")
        return

    logger.info("Starting meeting defender agent")

    preamble = build_preamble(config)
    prompt = preamble + "\n\n" + build_prompt(config)

    if dry_run:
        skills_list = agent_cfg.skills or ["meeting-prep", "vault-read-write"]
        print("=== DRY RUN — Meeting Defender Agent ===")
        print(f"\nMax turns: {MAX_TURNS}")
        print(f"Max budget: ${MAX_BUDGET_USD}")
        print(f"Permission mode: {config.safety.permission_mode}")
        print(f"CWD: {config.repo_root}")
        print(f"Skills: {skills_list}")
        print(f"Calendars: {CALENDARS}")
        print(f"\n--- Safety ---")
        print(f"Calendar tools: READ ONLY (list, get)")
        print(f"Excluded tools: create, delete, update, respond")
        print(f"NEVER auto-declines meetings")
        print(f"\n--- Task Prompt ---")
        print(prompt)
        print(f"\n--- Routing ---")
        print(f"Pre-classification: Mac Mini / phi4-mini-reasoning")
        print(f"Synthesis: Claude Haiku via API")
        print(f"Schedule: Monday 07:00 via launchd")
        print("\n=== END DRY RUN ===")
        return

    # SDK imports deferred to live run only
    from claude_agent_sdk import ResultMessage, query

    options = build_options(config)

    result_msg = None
    try:
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, ResultMessage):
                result_msg = message
                logger.info(
                    f"Completed: status={message.subtype}, "
                    f"turns={message.num_turns}, "
                    f"cost=${message.total_cost_usd}"
                )

        record_run(
            log_dir=config.log_dir,
            agent_name=AGENT_NAME,
            mode=None,
            status=result_msg.subtype if result_msg else "unknown",
            cost_usd=result_msg.total_cost_usd if result_msg else None,
            duration_ms=result_msg.duration_ms if result_msg else None,
            turns=result_msg.num_turns if result_msg else None,
            notes=result_msg.result[:200] if result_msg and result_msg.result else "",
        )

    except Exception as e:
        logger.error(f"Agent failed: {e}")
        record_run(
            log_dir=config.log_dir,
            agent_name=AGENT_NAME,
            mode=None,
            status="error",
            cost_usd=None,
            duration_ms=None,
            turns=None,
            notes=str(e)[:200],
        )
        raise


def main():
    parser = argparse.ArgumentParser(description="Meeting Defender Agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the prompt without calling the API",
    )
    args = parser.parse_args()

    asyncio.run(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
