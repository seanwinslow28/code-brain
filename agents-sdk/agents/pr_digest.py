#!/usr/bin/env python3
"""PR Digest Agent — daily GitHub PR summary to vault.

Runs on MacBook Pro (localhost), 100% local via Qwen2.5-Coder-32B through MLX-LM.
Summarizes recent GitHub PRs across configured repos into a daily digest note.

Usage:
    python3 agents/pr_digest.py
    python3 agents/pr_digest.py --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

# Add agents-sdk/ to Python path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config
from lib.logging_setup import record_run, setup_logger

AGENT_NAME = "pr-digest"

# Safety limits — $0.00 budget (100% local, gh CLI doesn't cost anything)
MAX_TURNS = 15
MAX_BUDGET_USD = 0.00

# Default repos to watch (configurable in config.toml)
DEFAULT_REPOS = [
    "seanwinslow28/16BitFit-V3",
    "seanwinslow28/sprite-sheet-automation-2026",
    "seanwinslow28/claude-code-superuser-pack",
]


def get_repos(config: Any) -> list[str]:
    """Get the list of repos to watch from config or defaults."""
    agent_cfg = config.agents.get("pr_digest", {})
    return agent_cfg.get("repos", DEFAULT_REPOS)


def check_gh_cli() -> bool:
    """Check if the gh CLI is installed and authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def fetch_prs_for_repo(
    repo: str,
    since_date: str,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Fetch recent PRs for a repo using gh CLI.

    Args:
        repo: Owner/repo format (e.g., "seanwinslow28/16BitFit-V3").
        since_date: ISO date string to filter PRs updated since.
        limit: Maximum number of PRs to fetch.

    Returns:
        List of PR dicts with title, author, state, url, etc.
    """
    try:
        result = subprocess.run(
            [
                "gh", "pr", "list",
                "--repo", repo,
                "--state", "all",
                "--limit", str(limit),
                "--json", "number,title,author,state,url,createdAt,updatedAt,headRefName,additions,deletions",
                "--search", f"updated:>={since_date}",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return []
        return json.loads(result.stdout) if result.stdout.strip() else []
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return []


def format_pr_digest(all_prs: dict[str, list[dict]], today: str) -> str:
    """Format all PRs into a markdown digest note."""
    lines = [
        "---",
        "type: pr-digest",
        f"date: {today}",
        "status: complete",
        "tags: [pr-digest, github]",
        "---",
        "",
        f"# PR Digest — {today}",
        "",
    ]

    total_prs = sum(len(prs) for prs in all_prs.values())

    if total_prs == 0:
        lines.append("No PR activity across watched repos in the last 24 hours.")
        return "\n".join(lines)

    lines.append(f"**{total_prs} PRs** across {len(all_prs)} repos.\n")

    for repo, prs in all_prs.items():
        if not prs:
            continue

        repo_short = repo.split("/")[-1]
        lines.append(f"## {repo_short}")
        lines.append("")
        lines.append("| # | Title | Author | Status | +/- |")
        lines.append("|---|-------|--------|--------|-----|")

        for pr in prs:
            number = pr.get("number", "?")
            title = pr.get("title", "Untitled")[:60]
            author = pr.get("author", {}).get("login", "?") if isinstance(pr.get("author"), dict) else "?"
            state = pr.get("state", "?").upper()
            additions = pr.get("additions", 0)
            deletions = pr.get("deletions", 0)
            url = pr.get("url", "")

            state_emoji = {"OPEN": "🟢", "CLOSED": "🔴", "MERGED": "🟣"}.get(state, "⚪")

            lines.append(
                f"| [#{number}]({url}) | {title} | {author} | {state_emoji} {state} | +{additions}/-{deletions} |"
            )

        lines.append("")

    return "\n".join(lines)


async def run(dry_run: bool = False) -> None:
    """Run the PR digest agent."""
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir, config.log_level)

    agent_cfg = config.agent_config("pr_digest")
    if not agent_cfg.enabled:
        logger.warning("PR digest agent is disabled in config.toml")
        return

    logger.info("Starting PR digest agent")
    start_time = time.monotonic()

    repos = get_repos(config)
    today = date.today().isoformat()
    since = (date.today() - timedelta(days=1)).isoformat()

    # Check gh CLI availability
    gh_available = check_gh_cli()

    if dry_run:
        print("=== DRY RUN — PR Digest Agent ===")
        print(f"\nRepos to watch: {repos}")
        print(f"Since date: {since}")
        print(f"gh CLI available: {gh_available}")
        print(f"Output path: {config.vault_root / '02_Areas' / 'Work' / f'pr-digest-{today}.md'}")
        print(f"\n--- Routing ---")
        print(f"Target machine: MacBook Pro (localhost)")
        print(f"Target model: Qwen2.5-Coder-32B via MLX-LM")
        print(f"Cost: $0.00 (100% local + gh CLI)")
        print(f"Schedule: daily 08:00 via launchd")

        if gh_available:
            print(f"\n--- PR Preview (fetching live data) ---")
            for repo in repos:
                prs = fetch_prs_for_repo(repo, since, limit=5)
                print(f"\n{repo}: {len(prs)} recent PRs")
                for pr in prs[:3]:
                    print(f"  #{pr.get('number', '?')} {pr.get('title', '?')[:50]} [{pr.get('state', '?')}]")
        else:
            print("\n⚠ gh CLI not available — install with: brew install gh && gh auth login")

        print("\n=== END DRY RUN ===")
        return

    if not gh_available:
        logger.error("gh CLI not installed or not authenticated. Run: gh auth login")
        record_run(
            log_dir=config.log_dir,
            agent_name=AGENT_NAME,
            mode=None,
            status="error",
            cost_usd=0.00,
            duration_ms=int((time.monotonic() - start_time) * 1000),
            turns=None,
            notes="gh CLI not available",
        )
        return

    try:
        # Fetch PRs from all repos
        all_prs: dict[str, list[dict]] = {}
        for repo in repos:
            prs = fetch_prs_for_repo(repo, since)
            all_prs[repo] = prs
            logger.info(f"Fetched {len(prs)} PRs from {repo}")

        # Format digest
        digest_content = format_pr_digest(all_prs, today)

        # Write to vault
        output_dir = config.vault_root / "02_Areas" / "Work"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"pr-digest-{today}.md"
        output_path.write_text(digest_content, encoding="utf-8")

        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        total_prs = sum(len(prs) for prs in all_prs.values())

        logger.info(
            f"PR digest written to {output_path}: "
            f"{total_prs} PRs across {len(repos)} repos, {elapsed_ms}ms"
        )

        record_run(
            log_dir=config.log_dir,
            agent_name=AGENT_NAME,
            mode=None,
            status="success",
            cost_usd=0.00,
            duration_ms=elapsed_ms,
            turns=None,
            notes=f"prs={total_prs}, repos={len(repos)}",
        )

    except Exception as e:
        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        logger.error(f"PR digest agent failed: {e}")
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
    parser = argparse.ArgumentParser(description="PR Digest Agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch PRs and show what would be written, without writing to vault",
    )
    args = parser.parse_args()

    asyncio.run(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
