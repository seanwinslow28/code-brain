#!/usr/bin/env python3
"""Daily Driver Agent — autonomous morning planning, EOD review, and weekly review.

Loads the daily-driver and vault-read-write skills as system prompts, then
uses the Claude Agent SDK to execute the protocol against the Obsidian vault.

Usage:
    python3 agents/daily_driver.py --mode morning
    python3 agents/daily_driver.py --mode evening
    python3 agents/daily_driver.py --mode weekly
    python3 agents/daily_driver.py --mode morning --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from datetime import date, timedelta
from pathlib import Path

# Add agents-sdk/ to Python path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from lib.artifact_loader import load_heartbeats
from lib.config import load_config
from lib.custom_tools import create_vault_mcp_server
from lib.logging_setup import record_run, setup_logger
from lib.skill_loader import load_skills
from lib.vault_io import (
    daily_note_path,
    recent_daily_notes,
    weekly_note_path,
    yesterday_note_path,
)

AGENT_NAME = "daily-driver"

# Re-exported for backwards compatibility; canonical home is lib.lint_report.
# Phase D (v3.20.0): synth_health_summary added alongside vault_health_summary.
from lib.lint_report import (  # noqa: E402
    latest_lint_report,
    synth_health_summary,
    vault_health_summary,
)


def _parse_top_n_from_roll_up(path: Path, n: int = 3) -> list[tuple[str, str, str, str, str]]:
    """Return up to n entries from the roll-up's '## Top Fits' section.

    Each tuple: (idx, company, title, location, score_str).
    """
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    # Slice from '## Top Fits' to the next '##' header
    m = re.search(r"## Top Fits[^\n]*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    out: list[tuple[str, str, str, str, str]] = []
    for line in block.splitlines():
        hm = re.match(r"### (\d+)\. ([^—]+?) — (.+?) · ⭐ (\d+/\d+)", line)
        if hm:
            idx, company, title, score = hm.group(1, 2, 3, 4)
            out.append((idx.strip(), company.strip(), title.strip(), "", score.strip()))
            if len(out) >= n:
                break
    return out


def _append_job_feed_summary(config, today: str) -> str:
    """Return a Markdown block summarizing today's job-feed roll-up, or '' if none."""
    feed_path = Path(config.vault_root) / "20_projects/prj-job-hunt-2026/job-feed" / f"{today}.md"
    if not feed_path.exists():
        return ""

    from lib.job_renderer import read_roll_up_frontmatter
    fm = read_roll_up_frontmatter(feed_path) or {}

    rel_link = f"./job-feed/{today}.md"

    if fm.get("complete") is False:
        return (
            f"\n## Job Feed ({today}) · Scoring deferred\n"
            f"MBP was asleep at 8 AM. Agent will retry hourly until 11 AM.\n"
            f"{fm.get('unscored', 0)} postings fetched and rules-filtered; "
            f"LLM scoring pending.\n"
            f"[Refresh the roll-up after MBP wakes →]({rel_link})\n"
        )

    top_3 = _parse_top_n_from_roll_up(feed_path, n=3)
    strong = fm.get("top_fits", 0)
    medium = fm.get("medium_fits", 0)
    weak = fm.get("weak_fits", 0)

    lines = [
        f"\n## Job Feed ({today}) · {strong} strong / {medium} medium / {weak} weak\n"
    ]
    for idx, company, title, _loc, score in top_3:
        anchor = f"#{idx}-" + company.lower().replace(" ", "-")
        lines.append(f"- **{company}** — {title} · {score} · [→]({rel_link}{anchor})\n")
    lines.append(f"\n[Full roll-up →]({rel_link})\n")
    return "".join(lines)


def build_artifact_preamble(config) -> str:
    """Build the operating-model artifact context block.

    Two sections:
      1. Always-loaded HEARTBEAT bodies for all three domains (small,
         always relevant for morning prioritization).
      2. On-demand pointer to full artifact paths for USER / SOUL /
         operating-model / schedule-recommendations, plus the
         life-systems tone rule and capture-and-defer default.

    Returns "" when [artifacts].enabled is false or the per-agent entry
    is missing, so disabling the section is a one-config-flip rollback.
    """
    agent_cfg = config.artifact_config("daily_driver")
    if not agent_cfg:
        return ""

    sections: list[str] = []

    if agent_cfg.get("heartbeats", False):
        subpath = config.artifacts.get("vault_subpath", "05_atlas/operating-models")
        require_confirmed = config.artifacts.get("require_confirmed", True)
        hb = load_heartbeats(
            config.vault_root,
            subpath=subpath,
            require_confirmed=require_confirmed,
        )

        heartbeat_lines = ["OPERATING-MODEL CONTEXT (always loaded — HEARTBEATs for today's rhythm):", ""]
        for domain, body in hb.items():
            heartbeat_lines.append(f"## {domain}")
            if body is None:
                heartbeat_lines.append(f"_(artifact unavailable — fall back to general judgment for {domain})_")
            else:
                heartbeat_lines.append(body.strip())
            heartbeat_lines.append("")
        sections.append("\n".join(heartbeat_lines))

    on_demand = agent_cfg.get("on_demand", [])
    if on_demand:
        subpath = config.artifacts.get("vault_subpath", "05_atlas/operating-models")
        artifact_base = config.vault_root / subpath
        pointer_lines = [
            "OPERATING-MODEL CONTEXT (on-demand — use the Read tool on these paths when the task requires deeper context):",
        ]
        for domain in ("creative-studio", "life-systems", "job-hunt-2026"):
            kinds_csv = ",".join(on_demand)
            pointer_lines.append(f"- {artifact_base}/{domain}/{{{kinds_csv}}}.md")
        sections.append("\n".join(pointer_lines))

    # Tone rule + capture-and-defer default are authored here (not dumped
    # from SOUL.md) because they are short, stable, and life-systems SOUL
    # is otherwise local-only per the Phase 1 decision matrix.
    sections.append(
        "TONE RULE: calm, factual, zen. No scolding. No imperatives aimed at "
        "the reader. No nagging on missed habits. Treat any resume or restart "
        "as a neutral next step."
    )
    sections.append(
        "CAPTURE-AND-DEFER DEFAULT: new ideas go to the inbox; do not promise "
        "to act on them today."
    )

    return "\n\n".join(sections)


def build_preamble(mode: str, config) -> str:
    """Build the autonomous agent preamble for the system prompt."""
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    # Mode-to-schedule-time mapping for Zero-Interaction Mandate
    mode_times = {
        "morning": config.agents.get("daily_driver", {}).get("morning_time", "06:00"),
        "evening": config.agents.get("daily_driver", {}).get("evening_time", "17:00"),
        "weekly": config.agents.get("daily_driver", {}).get("weekly_time", "16:00"),
    }
    schedule_time = mode_times.get(mode, "scheduled time")

    base = (
        f"You are Sean's autonomous daily driver agent running in {mode} mode.\n"
        f"Current date: {today} ({date.today().strftime('%A')})\n"
        f"Vault root: {config.vault_root}\n"
        f"Repo root: {config.repo_root}\n"
        f"\n"
        f"Key paths:\n"
        f"- Yesterday's daily note: {daily_note_path(config.vault_root, date.today() - timedelta(days=1))}\n"
        f"- Today's daily note: {daily_note_path(config.vault_root)}\n"
        f"- Daily note template: {config.vault_root / '90_system/templates/tpl-daily.md'}\n"
        f"- Weekly note template: {config.vault_root / '90_system/templates/tpl-weekly.md'}\n"
        f"\n"
        f"ZERO-INTERACTION MANDATE:\n"
        f"You are running at {schedule_time} via macOS launchd. No human is available.\n"
        f"Any attempt to ask a clarifying question will cause a silent timeout hang.\n"
        f"You MUST make best-judgment decisions autonomously.\n"
        f"If you cannot proceed, create an error note and halt — never wait for input.\n"
        f"\n"
        f"SAFE DEFERRAL PROTOCOL:\n"
        f"If any MCP tool or file operation fails:\n"
        f"1. Log the error with full context.\n"
        f"2. If today's daily note exists, append an error entry below the\n"
        f"   <!-- agent-error --> anchor with: timestamp, mode, error description.\n"
        f"   If the note doesn't exist yet, create a minimal one first.\n"
        f"3. Continue with remaining tasks if possible, or halt gracefully.\n"
        f"4. Never retry a failed operation more than 2 times.\n"
        f"\n"
        f"HEALTH METRICS:\n"
        f"- Data Non-Destruction: Never overwrite existing text in any vault note.\n"
        f"  Use PATCH operations only — inject at anchors, append sections.\n"
        f"  If a note already exists for today, read it first and only add new content.\n"
        f"- Truth Anchoring: Do not hallucinate calendar events or task completions.\n"
        f"  If a source is unavailable, note the gap explicitly with [ERROR] tag.\n"
        f"- Content Integrity: All frontmatter must remain valid YAML.\n"
        f"  If existing frontmatter cannot be parsed, do NOT modify it — log the error.\n"
    )

    # Phase 6 D.3.d — surface Vault Health in morning mode only.
    # Phase D (v3.20.0, 2026-05-01) — append the latest synth-manifest
    # summary line under Vault Health when one exists. Empty string when
    # no manifest yet (suppresses the line entirely on a fresh vault).
    if mode == "morning":
        today_iso = date.today().isoformat()
        job_feed_block = _append_job_feed_summary(config, today_iso)
        if job_feed_block:
            base += job_feed_block
        base += "\n" + vault_health_summary(config.vault_root) + "\n"
        synth_line = synth_health_summary(config.vault_root)
        if synth_line:
            base += synth_line + "\n"
        artifact_block = build_artifact_preamble(config)
        if artifact_block:
            base += "\n" + artifact_block + "\n"

    return base


def build_prompt(mode: str, config) -> str:
    """Build the task prompt for the given mode."""
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    if mode == "morning":
        return (
            f"Execute the Morning Planning Protocol from the daily-driver skill.\n"
            f"\n"
            f"Step 1: Read yesterday's daily note at {daily_note_path(config.vault_root, date.today() - timedelta(days=1))}\n"
            f"  - Extract open loops, carry-forward items, and any unfinished tasks.\n"
            f"  - If yesterday's note doesn't exist, note that and proceed.\n"
            f"\n"
            f"Step 2: Read any active project notes referenced in yesterday's log from {config.vault_root / '20_projects/'}\n"
            f"  - Look for [[wikilinks]] in yesterday's note to find relevant project files.\n"
            f"\n"
            f"Step 3: Create today's daily note at {daily_note_path(config.vault_root)}\n"
            f"  - Use the template at {config.vault_root / '90_system/templates/tpl-daily.md'}\n"
            f"  - Replace '<% tp.file.title %>' with '{today}'\n"
            f"\n"
            f"Step 4: Write the 1-3-5 priority plan in the Morning Focus section.\n"
            f"  - 1 big thing (deep work)\n"
            f"  - 3 medium things\n"
            f"  - 5 small things\n"
            f"  - Base priorities on carry-forward items and project status.\n"
            f"\n"
            f"Output a brief completion summary to stdout when done."
        )

    elif mode == "evening":
        return (
            f"Execute the End-of-Day Protocol from the daily-driver skill.\n"
            f"\n"
            f"Step 1: Read today's daily note at {daily_note_path(config.vault_root)}\n"
            f"  - Review the morning plan and any session entries.\n"
            f"\n"
            f"Step 2: Summarize the day's progress.\n"
            f"  - Check for entries at <!-- claude-sessions --> and <!-- jira-log --> anchors.\n"
            f"  - Count completed vs planned tasks.\n"
            f"\n"
            f"Step 3: Write the Evening Reflection section:\n"
            f"  - **Win:** The biggest accomplishment today.\n"
            f"  - **Lesson:** What you'd do differently.\n"
            f"  - **Carry forward:** Unfinished tasks and follow-ups for tomorrow.\n"
            f"\n"
            f"Output a brief completion summary to stdout when done."
        )

    elif mode == "weekly":
        recent = recent_daily_notes(config.vault_root, days=7)
        recent_list = "\n".join(f"  - {p}" for p in recent) if recent else "  (no recent daily notes found)"

        return (
            f"Execute the Weekly Review Integration from the daily-driver skill.\n"
            f"\n"
            f"Step 1: Read the last 7 daily notes:\n"
            f"{recent_list}\n"
            f"\n"
            f"Step 2: Aggregate across the week:\n"
            f"  - Tasks completed\n"
            f"  - Decisions made\n"
            f"  - Open loops and carry-forwards\n"
            f"  - Patterns (what kept slipping? what energized?)\n"
            f"\n"
            f"Step 3: Create the weekly review note at {weekly_note_path(config.vault_root)}\n"
            f"  - Use template at {config.vault_root / '90_system/templates/tpl-weekly.md'}\n"
            f"  - If template doesn't exist, create a structured weekly note with:\n"
            f"    - Wins This Week (<!-- auto-wins -->)\n"
            f"    - Blockers & Open Loops (<!-- auto-blockers -->)\n"
            f"    - Decisions Made (<!-- auto-decisions -->)\n"
            f"    - Next Week's Top 3 Priorities\n"
            f"\n"
            f"Output a brief completion summary to stdout when done."
        )

    else:
        raise ValueError(f"Unknown mode: {mode}. Use morning, evening, or weekly.")


def build_options(config, mode: str | None = None) -> ClaudeAgentOptions:
    """Build ClaudeAgentOptions for the daily driver agent.

    Args:
        config: Loaded Config object.
        mode: Optional mode name (morning/evening/weekly) for per-mode
              execution limits from config.toml [agents.daily_driver.modes.*].
    """
    agent_cfg = config.agent_config("daily_driver")
    skills_prompt = load_skills(agent_cfg.skills, config.skills_dir)

    vault_server = create_vault_mcp_server()

    # Mode-specific overrides from config.toml [agents.daily_driver.modes.{mode}]
    mode_cfg = {}
    if mode:
        raw_agent = config.agents.get("daily_driver", {})
        mode_cfg = raw_agent.get("modes", {}).get(mode, {})

    max_turns = (
        mode_cfg.get("max_turns")
        or agent_cfg.max_turns
        or config.safety.max_turns_default
    )
    max_budget = (
        mode_cfg.get("max_budget_usd")
        or agent_cfg.max_budget_usd
        or config.safety.max_budget_default
    )

    # Only pass API key if explicitly set; otherwise the SDK uses
    # Claude Code CLI's existing auth (e.g., `claude login` OAuth)
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
        max_turns=max_turns,
        max_budget_usd=max_budget,
        cwd=str(config.repo_root),
        mcp_servers={"vault-tools": vault_server},
        setting_sources=["project"],
        env=env,
    )


async def run(mode: str, dry_run: bool = False) -> None:
    """Run the daily driver agent in the specified mode."""
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir, config.log_level, mode=mode)

    agent_cfg = config.agent_config("daily_driver")
    if not agent_cfg.enabled:
        logger.warning("Daily driver agent is disabled in config.toml")
        return

    logger.info(f"Starting daily driver in {mode} mode")

    preamble = build_preamble(mode, config)
    prompt = preamble + "\n\n" + build_prompt(mode, config)
    options = build_options(config, mode=mode)

    if dry_run:
        print("=== DRY RUN — Daily Driver Agent ===")
        print(f"\nMode: {mode}")
        print(f"Max turns: {options.max_turns}")
        print(f"Max budget: ${options.max_budget_usd}")
        print(f"Permission mode: {options.permission_mode}")
        print(f"CWD: {options.cwd}")
        print(f"Allowed tools: {options.allowed_tools}")
        print(f"\n--- System Prompt (appended skills) ---")
        print(options.system_prompt.get("append", "")[:500] + "...")
        print(f"\n--- Task Prompt ---")
        print(prompt)
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
            mode=mode,
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
            mode=mode,
            status="error",
            cost_usd=None,
            duration_ms=None,
            turns=None,
            notes=str(e)[:200],
        )
        raise


def main():
    parser = argparse.ArgumentParser(description="Daily Driver Agent")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["morning", "evening", "weekly"],
        help="Which protocol to run",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the prompt without calling the API",
    )
    args = parser.parse_args()

    asyncio.run(run(args.mode, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
