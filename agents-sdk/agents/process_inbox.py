#!/usr/bin/env python3
"""Process Inbox Agent — autonomous vault inbox triage.

Runs on Mac Mini (192.168.68.200), 100% local via phi4-mini-reasoning (3.8B).
Reads unprocessed inbox notes from vault, classifies and tags them.
On success, creates a baton file for Daily Driver dependency chain.

Usage:
    python3 agents/process_inbox.py
    python3 agents/process_inbox.py --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import date
from pathlib import Path

# Add agents-sdk/ to Python path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from lib.baton import create_baton
from lib.config import load_config
from lib.custom_tools import create_vault_mcp_server
from lib.logging_setup import record_run, setup_logger
from lib.skill_loader import load_skills

AGENT_NAME = "process-inbox"

# Safety limits — tighter than defaults for a simple triage agent
MAX_TURNS = 15
MAX_BUDGET_USD = 0.25


def build_preamble(config) -> str:
    """Build the autonomous agent preamble."""
    today = date.today().isoformat()

    return (
        f"You are Sean's autonomous inbox triage agent.\n"
        f"Current date: {today}\n"
        f"Vault root: {config.vault_root}\n"
        f"Inbox path: {config.vault_root / '00_inbox/'}\n"
        f"\n"
        f"ZERO-INTERACTION MANDATE:\n"
        f"You are running autonomously via launchd on Mac Mini. No human is available.\n"
        f"Any attempt to ask a clarifying question will cause a silent timeout hang.\n"
        f"You MUST make best-judgment decisions autonomously.\n"
        f"\n"
        f"CONFIDENCE-THRESHOLD ROUTING:\n"
        f"For each file you classify:\n"
        f"- If you are ≥80% confident in the classification → auto-tag and move\n"
        f"- If you are <80% confident → tag with `#triage/human` and set\n"
        f"  `status: needs-review`. Leave in inbox for manual review.\n"
        f"- NEVER ask for confirmation. Process ALL files in a single batch.\n"
        f"\n"
        f"SAFE DEFERRAL PROTOCOL:\n"
        f"If any file operation fails:\n"
        f"1. Log the error with full context.\n"
        f"2. Skip that file and continue with the rest.\n"
        f"3. Include failed files in the summary report.\n"
        f"4. Never retry a failed operation more than 2 times.\n"
        f"\n"
        f"HEALTH METRICS:\n"
        f"- Data Non-Destruction: Never delete files. Only move or tag them.\n"
        f"- Content Integrity: Preserve original content — only add/update frontmatter.\n"
        f"- Frontmatter: All YAML must be flat (no nested objects).\n"
    )


def build_prompt(config) -> str:
    """Build the task prompt for inbox processing."""
    inbox_path = config.vault_root / "00_inbox/"

    return (
        f"Execute the Process Inbox protocol from the process-inbox skill.\n"
        f"\n"
        f"Step 1: Scan `{inbox_path}` for all files.\n"
        f"  - Skip .gitkeep and hidden files.\n"
        f"  - If the inbox is empty, output 'Inbox empty — no files to process.'\n"
        f"    and stop.\n"
        f"\n"
        f"Step 2: For each file:\n"
        f"  a) Read the content\n"
        f"  b) Classify: type, domain, ai-context\n"
        f"  c) Apply confidence threshold:\n"
        f"     - ≥80%: Add frontmatter, rename, move to destination\n"
        f"     - <80%: Add frontmatter with `status: needs-review` and\n"
        f"       `tags: [triage/human]`, leave in inbox\n"
        f"\n"
        f"Step 3: Output a summary table with columns:\n"
        f"  File | Type | Domain | Confidence | Destination | Status\n"
        f"\n"
        f"Output the summary to stdout when done."
    )


def build_options(config) -> ClaudeAgentOptions:
    """Build ClaudeAgentOptions for the process inbox agent."""
    agent_cfg = config.agent_config("process_inbox")
    skills_prompt = load_skills(
        agent_cfg.skills or ["process-inbox", "vault-read-write"],
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
    """Run the process inbox agent."""
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir, config.log_level)

    agent_cfg = config.agent_config("process_inbox")
    if not agent_cfg.enabled:
        logger.warning("Process inbox agent is disabled in config.toml")
        return

    logger.info("Starting process inbox agent")

    preamble = build_preamble(config)
    prompt = preamble + "\n\n" + build_prompt(config)
    options = build_options(config)

    if dry_run:
        print("=== DRY RUN — Process Inbox Agent ===")
        print(f"\nMax turns: {options.max_turns}")
        print(f"Max budget: ${options.max_budget_usd}")
        print(f"Permission mode: {options.permission_mode}")
        print(f"CWD: {options.cwd}")
        print(f"Allowed tools: {options.allowed_tools}")
        print(f"Inbox path: {config.vault_root / '00_inbox/'}")
        print(f"\n--- System Prompt (appended skills) ---")
        print(options.system_prompt.get("append", "")[:500] + "...")
        print(f"\n--- Task Prompt ---")
        print(prompt)
        print(f"\n--- Routing ---")
        print(f"Target machine: Mac Mini (192.168.68.200)")
        print(f"Target model: phi4-mini-reasoning (3.8B)")
        print(f"Baton on success: ~/.claude/batons/inbox_done.flag")
        print("\n=== END DRY RUN ===")
        return

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

        # On success, create baton file for Daily Driver dependency chain
        if result_msg and result_msg.subtype == "success":
            baton_meta = (
                f"files_processed: see log\n"
                f"cost: ${result_msg.total_cost_usd}\n"
                f"turns: {result_msg.num_turns}"
            )
            create_baton("inbox_done", metadata=baton_meta)
            logger.info("Baton file created: inbox_done.flag")

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
    parser = argparse.ArgumentParser(description="Process Inbox Agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the prompt without calling the API",
    )
    args = parser.parse_args()

    asyncio.run(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
