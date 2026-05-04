#!/usr/bin/env python3
"""Process Inbox Agent — autonomous vault inbox triage.

Runs on Mac Mini via macOS launchd, twice weekly (Sun + Wed at 09:00 ET).
Cloud-LLM agent: uses claude_agent_sdk.query() against Sonnet for the
classification quality required to hit the ≥80% confidence threshold on
nuanced web-clip frontmatter. Loads life-systems operating-model artifacts
(HEARTBEAT, SOUL, operating-model) per the SOUL.md "Consumed by …
process-inbox" wiring. On success, creates a baton file.

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

from lib.artifact_loader import load_heartbeats
from lib.baton import create_baton
from lib.config import load_config
from lib.custom_tools import create_vault_mcp_server
from lib.logging_setup import record_run, setup_logger
from lib.skill_loader import load_skills

AGENT_NAME = "process-inbox"

# Safety limits — second adjustment 2026-04-29 after first scheduled fire
# spent $1.23 / 30 turns moving zero files (agent over-read on-demand
# artifact pointers before touching inbox). On-demand pointers dropped from
# config; HEARTBEATs preserved. Caps bumped one more notch: 25→40 turns,
# $1.20→$1.80 budget. Per file ≈ 4 tool calls (Read → Edit → Write → confirm),
# so 40 turns covers ~9 files with headroom. Mirrors SOUL.md Past Landmine
# #4 ("raise the cap, don't retry harder"). If runs STILL trip $1.80, the
# next move is NOT another bump — it's a Path B rewrite to local gemma4:e4b
# via routing.task_map.inbox_triage. That's a rewrite, not a config tweak.
MAX_TURNS = 40
MAX_BUDGET_USD = 1.80


def build_artifact_preamble(config) -> str:
    """Build the operating-model artifact context block for inbox triage.

    Mirrors daily_driver.build_artifact_preamble. Returns "" when
    [artifacts].enabled is false or per-agent entry is missing — silent
    no-op rollback via one config flip.

    Two sections:
      1. Always-loaded HEARTBEAT bodies for all three domains (gives the
         agent the context to route inbox items into the correct domain).
      2. On-demand pointer to SOUL.md and operating-model.md per domain.
         life-systems SOUL is named in its own frontmatter as a process-inbox
         consumer; life-systems operating-model carries the
         "future research fleet" leverage points the triage agent uses
         to flag research-worthy captures.
    """
    agent_cfg = config.artifact_config("process_inbox")
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

        heartbeat_lines = [
            "OPERATING-MODEL CONTEXT (always loaded — HEARTBEATs for domain routing):",
            "",
        ]
        for domain, body in hb.items():
            heartbeat_lines.append(f"## {domain}")
            if body is None:
                heartbeat_lines.append(
                    f"_(artifact unavailable — fall back to general judgment for {domain})_"
                )
            else:
                heartbeat_lines.append(body.strip())
            heartbeat_lines.append("")
        sections.append("\n".join(heartbeat_lines))

    on_demand = agent_cfg.get("on_demand", [])
    if on_demand:
        subpath = config.artifacts.get("vault_subpath", "05_atlas/operating-models")
        artifact_base = config.vault_root / subpath
        pointer_lines = [
            "OPERATING-MODEL CONTEXT (on-demand — Read these when an inbox item needs deeper routing context):",
        ]
        for domain in ("creative-studio", "life-systems", "job-hunt-2026"):
            kinds_csv = ",".join(on_demand)
            pointer_lines.append(f"- {artifact_base}/{domain}/{{{kinds_csv}}}.md")
        pointer_lines.append(
            "Priority for inbox triage: life-systems/SOUL.md (tone + sacred cows + Tier-A learned behaviors) "
            "and life-systems/operating-model.md (Active Leverage Points, especially the future research fleet — "
            "Perplexity, Gemini Deep Research, NotebookLM, agentkit — for flagging research-worthy captures)."
        )
        sections.append("\n".join(pointer_lines))

    sections.append(
        "TONE RULE: calm, factual, zen. No scolding. No imperatives at the reader. "
        "Treat every capture as a neutral signal, never a judgment of past behavior."
    )
    sections.append(
        "RESEARCH-CANDIDATE FLAG: when an inbox item maps to a future research-fleet "
        "topic (crypto, prediction markets, x402, agentic commerce, DeFi yield, AI tooling, "
        "autoresearch, Perplexity / Gemini Deep Research / NotebookLM workflows), add tag "
        "`#triage/research-candidate` to the frontmatter alongside the standard domain tag. "
        "These items become input to Sean's planned research agents."
    )

    return "\n\n".join(sections)


def build_preamble(config) -> str:
    """Build the autonomous agent preamble."""
    today = date.today().isoformat()

    base = (
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

    artifact_block = build_artifact_preamble(config)
    if artifact_block:
        base += "\n" + artifact_block + "\n"

    return base


def build_prompt(config) -> str:
    """Build the task prompt for inbox processing."""
    inbox_path = config.vault_root / "00_inbox/"

    return (
        f"Execute the Process Inbox protocol from the process-inbox skill.\n"
        f"\n"
        f"BUDGET DISCIPLINE (read this before any tool call):\n"
        f"This run has a hard {MAX_TURNS}-turn cap. The 2026-04-29 run before\n"
        f"this one moved ZERO files in 30 turns because the agent over-explored\n"
        f"context. Aim for ≤4 tool calls per file: Read → Edit (frontmatter) →\n"
        f"Write (at destination) → optional Glob to confirm. Skip the confirm\n"
        f"step on high-confidence moves. Do NOT re-read files you already read.\n"
        f"Do NOT read operating-model artifacts unless a specific routing\n"
        f"decision genuinely requires it (the HEARTBEATs in your system prompt\n"
        f"already give you domain context).\n"
        f"\n"
        f"PROCESS FILES SERIALLY — one at a time:\n"
        f"For each file: complete ALL of (Read → Edit → Write) before starting\n"
        f"the next file. Do NOT batch-Read all files first then batch-Edit. The\n"
        f"serial pattern keeps your working memory small and your turn count\n"
        f"predictable.\n"
        f"\n"
        f"Step 1: Scan `{inbox_path}` for all files.\n"
        f"  - Skip .gitkeep and hidden files.\n"
        f"  - Note the count, then process ONE AT A TIME below.\n"
        f"\n"
        f"Step 2: For each file (SERIAL, NOT BATCHED):\n"
        f"  a) Read the content (1 tool call)\n"
        f"  b) Classify in your head: type, domain, ai-context — do NOT\n"
        f"     emit reasoning to stdout, just decide.\n"
        f"  c) Apply confidence threshold:\n"
        f"     - ≥80%: Edit frontmatter in place, then Write to the\n"
        f"       destination path. Single Edit + single Write — no\n"
        f"       re-Reads, no verification Globs.\n"
        f"     - <80%: Edit frontmatter to add `status: needs-review` and\n"
        f"       `tags: [triage/human]`. Leave in inbox.\n"
        f"  d) Move to next file immediately. Do not summarize per-file.\n"
        f"\n"
        f"Step 3: After ALL files are processed, output a summary table:\n"
        f"  File | Type | Domain | Confidence | Destination | Status\n"
        f"\n"
        f"Output the summary to stdout when done. The summary is the only\n"
        f"prose you should emit; per-file thinking belongs in tool calls only."
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

    # Empty-inbox short-circuit — skip the SDK call entirely. Listing files
    # is free; making Sonnet detect "empty folder" through 19 turns of
    # artifact reading costs ~$0.90. Filter the same way the LLM would:
    # exclude .gitkeep and dotfiles.
    inbox_dir = config.vault_root / "00_inbox"
    inbox_files = [
        p for p in inbox_dir.iterdir()
        if p.is_file() and not p.name.startswith(".") and p.name != ".gitkeep"
    ] if inbox_dir.is_dir() else []

    if not inbox_files:
        logger.info("Inbox empty — skipping SDK call (early exit, $0 cost)")
        create_baton(
            "inbox_done",
            metadata="files_processed: 0 (empty inbox short-circuit)\ncost: $0.00\nturns: 0",
        )
        record_run(
            log_dir=config.log_dir,
            agent_name=AGENT_NAME,
            mode=None,
            status="success",
            cost_usd=0.0,
            duration_ms=0,
            turns=0,
            notes="Inbox empty — short-circuited before SDK call",
        )
        return

    logger.info("Found %d inbox file(s) to process", len(inbox_files))

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
        print(f"Execution host: Mac Mini (launchd, twice weekly Sun + Wed 09:00)")
        print(f"LLM: Claude Sonnet via claude_agent_sdk.query() (cloud)")
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
