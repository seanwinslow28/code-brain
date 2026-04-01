#!/usr/bin/env python3
"""Spending Analysis Agent — autonomous financial CSV analysis.

Runs on MacBook Pro (localhost), 100% local via Qwen3-14B (MLX-LM).
Reads sanitized financial CSVs, analyzes spending patterns, outputs
structured markdown to vault. No interactive review — all anomalies
are reported as tables.

Usage:
    python3 agents/spending_analysis.py
    python3 agents/spending_analysis.py --dry-run
    python3 agents/spending_analysis.py --csv path/to/statement.csv
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

from lib.config import load_config
from lib.csv_sanitizer import sanitize_to_json
from lib.custom_tools import create_vault_mcp_server
from lib.logging_setup import record_run, setup_logger
from lib.skill_loader import load_skills

AGENT_NAME = "spending-analysis"

# Safety limits
MAX_TURNS = 20
MAX_BUDGET_USD = 0.25


def build_preamble(config, sanitized_json_path: Path | None = None) -> str:
    """Build the autonomous agent preamble."""
    today = date.today().isoformat()
    output_dir = config.vault_root / "50_sources" / "finance"

    preamble = (
        f"You are Sean's autonomous spending analysis agent.\n"
        f"Current date: {today}\n"
        f"Vault root: {config.vault_root}\n"
        f"Output directory: {output_dir}\n"
        f"\n"
        f"ZERO-INTERACTION MANDATE:\n"
        f"You are running autonomously on MacBook Pro. No human is available.\n"
        f"Any attempt to ask a clarifying question will cause a silent timeout hang.\n"
        f"You MUST make best-judgment decisions autonomously.\n"
        f"\n"
        f"OUTPUT FORMAT:\n"
        f"Do NOT ask the user to review results. Output ALL analysis as structured\n"
        f"markdown tables in a report file at:\n"
        f"  {output_dir / f'spending-report-{today}.md'}\n"
        f"\n"
        f"ANOMALY HANDLING:\n"
        f"Report all anomalies as a `## Flagged Anomalies` section with columns:\n"
        f"  Date | Description | Amount | Category | Severity | Category Avg\n"
        f"Severity: HIGH (z-score > 5), MEDIUM (z-score > 3).\n"
        f"The user will review the table asynchronously — never wait for input.\n"
        f"\n"
        f"FINANCIAL DATA AIRGAP:\n"
        f"You only receive pre-sanitized JSON — no raw account numbers, no card\n"
        f"numbers, no full transaction IDs. This is by design.\n"
    )

    if sanitized_json_path:
        preamble += (
            f"\nSANITIZED DATA FILE:\n"
            f"Read the sanitized transaction data from: {sanitized_json_path}\n"
        )

    return preamble


def build_prompt(config, sanitized_json_path: Path | None = None) -> str:
    """Build the task prompt for spending analysis."""
    today = date.today().isoformat()
    output_dir = config.vault_root / "50_sources" / "finance"

    data_source = ""
    if sanitized_json_path:
        data_source = f"Read the sanitized JSON data from: {sanitized_json_path}\n"
    else:
        data_source = (
            f"Look for the most recent .sanitized.json file in:\n"
            f"  {config.repo_root / 'life-systems' / 'finance'}\n"
        )

    return (
        f"Execute the spending analysis workflow from the personal-finance\n"
        f"and subscription-audit skills.\n"
        f"\n"
        f"Step 1: Load Data\n"
        f"  {data_source}\n"
        f"\n"
        f"Step 2: Categorize Transactions\n"
        f"  Apply the regex categorization rules from the personal-finance skill.\n"
        f"  Track uncategorized transactions separately.\n"
        f"\n"
        f"Step 3: Generate Monthly Report\n"
        f"  Create a structured markdown report at:\n"
        f"  {output_dir / f'spending-report-{today}.md'}\n"
        f"\n"
        f"  Include these sections:\n"
        f"  - ## Summary (total spend, net income $5,741, savings rate)\n"
        f"  - ## Category Breakdown (table with Actual, Budget, Variance, Status)\n"
        f"  - ## Subscription Tracker (recurring charges, totals)\n"
        f"  - ## Flagged Anomalies (z-score outliers, HIGH/MEDIUM severity)\n"
        f"  - ## Debt Dashboard (interest charges, paydown projection)\n"
        f"  - ## Action Items (bullet list, no interactive prompts)\n"
        f"\n"
        f"Step 4: Output completion summary to stdout."
    )


def build_options(config) -> ClaudeAgentOptions:
    """Build ClaudeAgentOptions for the spending analysis agent."""
    agent_cfg = config.agent_config("spending_analysis")
    skills_prompt = load_skills(
        agent_cfg.skills or ["personal-finance", "subscription-audit", "vault-read-write"],
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


async def run(dry_run: bool = False, csv_path: str | None = None) -> None:
    """Run the spending analysis agent."""
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir, config.log_level)

    agent_cfg = config.agent_config("spending_analysis")
    if not agent_cfg.enabled:
        logger.warning("Spending analysis agent is disabled in config.toml")
        return

    logger.info("Starting spending analysis agent")

    # If a CSV path was provided, sanitize it first
    sanitized_path = None
    if csv_path:
        logger.info(f"Sanitizing CSV: {csv_path}")
        sanitized_path = sanitize_to_json(csv_path)
        logger.info(f"Sanitized output: {sanitized_path}")

    preamble = build_preamble(config, sanitized_path)
    prompt = preamble + "\n\n" + build_prompt(config, sanitized_path)
    options = build_options(config)

    if dry_run:
        print("=== DRY RUN — Spending Analysis Agent ===")
        print(f"\nMax turns: {options.max_turns}")
        print(f"Max budget: ${options.max_budget_usd}")
        print(f"Permission mode: {options.permission_mode}")
        print(f"CWD: {options.cwd}")
        print(f"Allowed tools: {options.allowed_tools}")
        if csv_path:
            print(f"Input CSV: {csv_path}")
            print(f"Sanitized JSON: {sanitized_path}")
        print(f"\n--- System Prompt (appended skills) ---")
        print(options.system_prompt.get("append", "")[:500] + "...")
        print(f"\n--- Task Prompt ---")
        print(prompt)
        print(f"\n--- Routing ---")
        print(f"Target machine: MacBook Pro (localhost)")
        print(f"Target model: Qwen3-14B via MLX-LM")
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
    parser = argparse.ArgumentParser(description="Spending Analysis Agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the prompt without calling the API",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Path to a bank CSV to sanitize and analyze",
    )
    args = parser.parse_args()

    asyncio.run(run(dry_run=args.dry_run, csv_path=args.csv))


if __name__ == "__main__":
    main()
