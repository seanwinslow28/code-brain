#!/usr/bin/env python3
"""Sprint Health Monitor Agent — autonomous sprint analysis via Jira MCP.

Routes to: Claude Sonnet via API (needs Jira MCP for data access).
Reads current sprint from Jira, analyzes velocity, flags at-risk stories.
Outputs sprint health report to vault.

Usage:
    python3 agents/sprint_health.py
    python3 agents/sprint_health.py --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import date
from pathlib import Path

# Add agents-sdk/ to Python path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.baton import create_baton
from lib.config import load_config
from lib.logging_setup import record_run, setup_logger
from lib.skill_loader import load_skills

AGENT_NAME = "sprint-health"

# Safety limits — needs API for Jira MCP access
MAX_TURNS = 15
MAX_BUDGET_USD = 0.50

# Jira cloud ID for The Block
JIRA_CLOUD_ID = "9660d87e-3943-45c9-82bd-ce963410b29e"

# Primary project key for P&E sprint tracking
PRIMARY_PROJECT_KEY = "BE"


def build_preamble(config) -> str:
    """Build the autonomous agent preamble."""
    today = date.today().isoformat()

    return (
        f"You are Sean's autonomous Sprint Health Monitor agent.\n"
        f"Current date: {today}\n"
        f"Vault root: {config.vault_root}\n"
        f"\n"
        f"ZERO-INTERACTION MANDATE:\n"
        f"You are running autonomously via launchd. No human is available.\n"
        f"Any attempt to ask a clarifying question will cause a silent timeout hang.\n"
        f"You MUST make best-judgment decisions autonomously.\n"
        f"\n"
        f"JIRA CONFIGURATION:\n"
        f"Cloud ID: {JIRA_CLOUD_ID}\n"
        f"Primary project: {PRIMARY_PROJECT_KEY} (Block Engineering)\n"
        f"Site: theblockcrypto.atlassian.net\n"
        f"\n"
        f"SAFE DEFERRAL PROTOCOL:\n"
        f"If any Jira API call fails:\n"
        f"1. Log the error with full context.\n"
        f"2. Skip that query and continue with available data.\n"
        f"3. Include errors in the report.\n"
        f"4. Never retry a failed API call more than 2 times.\n"
    )


def build_prompt(config) -> str:
    """Build the task prompt for sprint health analysis."""
    today = date.today().isoformat()
    output_path = config.vault_root / "02_Areas" / "Work" / f"sprint-health-{today}.md"

    return (
        f"Execute the Sprint Health Monitor protocol.\n"
        f"\n"
        f"Step 1: Read the current active sprint from Jira.\n"
        f"  - Use JQL: `sprint in openSprints() AND project = {PRIMARY_PROJECT_KEY}`\n"
        f"  - Cloud ID: {JIRA_CLOUD_ID}\n"
        f"  - Fetch all issues with fields: summary, status, assignee, priority,\n"
        f"    story_points, created, updated\n"
        f"\n"
        f"Step 2: Analyze sprint health.\n"
        f"  - Count issues by status category: To Do, In Progress, Done\n"
        f"  - Calculate completion percentage (Done / Total)\n"
        f"  - Identify at-risk stories: issues still in 'To Do' or stuck in\n"
        f"    'In Progress' for >3 days without updates\n"
        f"  - Flag any unassigned issues\n"
        f"  - Note any blockers mentioned in issue descriptions\n"
        f"\n"
        f"Step 3: Generate the sprint health report.\n"
        f"  Write a markdown report to: {output_path}\n"
        f"  The report should include:\n"
        f"  - Sprint name and date range (if available from sprint metadata)\n"
        f"  - Summary metrics table (total, done, in progress, to do, % complete)\n"
        f"  - At-risk stories table (key, summary, assignee, status, days stale)\n"
        f"  - Velocity notes (if prior sprint data is accessible)\n"
        f"  - Recommendations (what needs attention this week)\n"
        f"\n"
        f"Step 4: Output the report path and key metrics to stdout.\n"
        f"\n"
        f"IMPORTANT:\n"
        f"- Use the Atlassian MCP tools for Jira access (searchJiraIssuesUsingJql)\n"
        f"- Do NOT attempt to access Jira via REST API directly\n"
        f"- All dates should use ISO format ({today})\n"
        f"- If no active sprint is found, report that and exit gracefully\n"
    )


def build_options(config):
    """Build ClaudeAgentOptions for the sprint health agent."""
    from claude_agent_sdk import ClaudeAgentOptions
    from lib.custom_tools import create_vault_mcp_server

    agent_cfg = config.agent_config("sprint_health")
    skills_prompt = load_skills(
        agent_cfg.skills or ["sprint-roadmap", "vault-read-write"],
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
            # Atlassian MCP tools for Jira access
            "mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql",
            "mcp__claude_ai_Atlassian__getJiraIssue",
            "mcp__claude_ai_Atlassian__getVisibleJiraProjects",
            "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources",
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
    """Run the sprint health monitor agent."""
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir)

    agent_cfg = config.agent_config("sprint_health")
    if not agent_cfg.enabled:
        logger.warning("Sprint health agent is disabled in config.toml")
        return

    logger.info("Starting sprint health monitor agent")

    preamble = build_preamble(config)
    prompt = preamble + "\n\n" + build_prompt(config)

    if dry_run:
        agent_cfg = config.agent_config("sprint_health")
        skills_list = agent_cfg.skills or ["sprint-roadmap", "vault-read-write"]
        print("=== DRY RUN — Sprint Health Monitor Agent ===")
        print(f"\nMax turns: {MAX_TURNS}")
        print(f"Max budget: ${MAX_BUDGET_USD}")
        print(f"Permission mode: {config.safety.permission_mode}")
        print(f"CWD: {config.repo_root}")
        print(f"Skills: {skills_list}")
        print(f"\n--- Jira Config ---")
        print(f"Cloud ID: {JIRA_CLOUD_ID}")
        print(f"Project: {PRIMARY_PROJECT_KEY}")
        print(f"\n--- Task Prompt ---")
        print(prompt)
        print(f"\n--- Routing ---")
        print(f"Target: Claude Sonnet via API (needs Jira MCP)")
        print(f"Baton on success: ~/.claude/batons/sprint_health_done.flag")
        print(f"Schedule: Friday 15:00 via launchd")
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

        # On success, create baton file
        if result_msg and result_msg.subtype == "success":
            baton_meta = (
                f"project: {PRIMARY_PROJECT_KEY}\n"
                f"cost: ${result_msg.total_cost_usd}\n"
                f"turns: {result_msg.num_turns}"
            )
            create_baton("sprint_health_done", metadata=baton_meta)
            logger.info("Baton file created: sprint_health_done.flag")

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
    parser = argparse.ArgumentParser(description="Sprint Health Monitor Agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the prompt without calling the API",
    )
    args = parser.parse_args()

    asyncio.run(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
