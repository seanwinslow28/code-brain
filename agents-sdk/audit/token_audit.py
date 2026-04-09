"""Active Fleet Token Audit — analyzes the 3 active agents for token usage.

Audits: vault-indexer, daily-driver morning, meta-agent.
Ignores the 6 disabled agents per AUDIT-2026-04-09-agent-downsizing.md.

Usage:
    python3 audit/token_audit.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

SDK_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SDK_ROOT))


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English text."""
    return len(text) // 4


def audit_vault_indexer() -> dict:
    """Audit vault-indexer agent token usage."""
    agent_path = SDK_ROOT / "agents" / "vault_indexer.py"
    agent_code = agent_path.read_text() if agent_path.exists() else ""

    # Vault indexer is 100% local (Ollama nomic-embed-text)
    # No Claude API tokens consumed
    return {
        "name": "vault-indexer",
        "schedule": "2:00 AM daily",
        "machine": "Mac Mini",
        "model": "nomic-embed-text (local Ollama)",
        "prompt_tokens": 0,
        "output_tokens": 0,
        "cost_per_run": 0.00,
        "cost_per_month": 0.00,
        "agent_code_size": len(agent_code),
        "notes": "100% local inference. Zero API cost. Generates embeddings for vault semantic search.",
    }


def audit_daily_driver() -> dict:
    """Audit daily-driver morning agent token usage."""
    agent_path = SDK_ROOT / "agents" / "daily_driver.py"
    agent_code = agent_path.read_text() if agent_path.exists() else ""

    # Skills loaded as system prompt
    skills_dir = SDK_ROOT.parent / ".claude" / "skills"
    skill_files = ["daily-driver", "vault-read-write"]
    skill_text = ""
    for skill_name in skill_files:
        skill_path = skills_dir / f"{skill_name}.md"
        if skill_path.exists():
            skill_text += skill_path.read_text()

    prompt_tokens = estimate_tokens(agent_code + skill_text)

    # Typical output: daily note skeleton (~500 words = ~2000 chars = ~500 tokens)
    output_tokens = 500

    # Claude API pricing (Sonnet for daily driver): $3/$15 per MTok
    # Actually uses headless claude CLI which routes to Sonnet by default
    input_cost = (prompt_tokens / 1_000_000) * 3.0
    output_cost = (output_tokens / 1_000_000) * 15.0
    cost_per_run = input_cost + output_cost

    # Actual observed cost is ~$0.40/run (from audit doc)
    # The estimate above is the prompt-only cost; actual includes multi-turn
    actual_cost_per_run = 0.40

    return {
        "name": "daily-driver (morning)",
        "schedule": "8:45 AM daily",
        "machine": "Mac Mini → Claude API",
        "model": "Claude Sonnet (via headless CLI)",
        "prompt_tokens_estimated": prompt_tokens,
        "output_tokens_estimated": output_tokens,
        "cost_per_run_estimated": round(cost_per_run, 4),
        "cost_per_run_observed": actual_cost_per_run,
        "cost_per_month": round(actual_cost_per_run * 30, 2),
        "agent_code_size": len(agent_code),
        "skill_prompt_size": len(skill_text),
        "notes": (
            "Most expensive active agent. ~$0.40/run observed, ~$12/month. "
            "Multi-turn conversation drives cost above single-prompt estimate. "
            "Limited value without MCP access (no calendar/Slack data in headless mode)."
        ),
    }


def audit_meta_agent() -> dict:
    """Audit meta-agent token usage."""
    agent_path = SDK_ROOT / "agents" / "meta_agent.py"
    agent_code = agent_path.read_text() if agent_path.exists() else ""

    # Meta-agent targets Mac Mini phi4-mini-reasoning for summary gen
    # But the headless CLI currently routes through Claude API
    # If running via direct Python script: $0.00 (local checks only, no LLM needed)
    # If running via claude CLI: ~$0.10/run (budget cap)

    return {
        "name": "meta-agent",
        "schedule": "6:30 AM daily",
        "machine": "Mac Mini (phi4-mini-reasoning target)",
        "model": "phi4-mini-reasoning (local) or Claude API (via CLI)",
        "prompt_tokens_estimated": estimate_tokens(agent_code),
        "cost_per_run_script": 0.00,
        "cost_per_run_cli": 0.10,
        "cost_per_month_script": 0.00,
        "cost_per_month_cli": round(0.10 * 30, 2),
        "agent_code_size": len(agent_code),
        "notes": (
            "When run as Python script directly: $0.00 (no LLM needed, just HTTP checks + file writes). "
            "When run via claude CLI headless: $0.10/run budget cap = ~$3/month. "
            "RECOMMENDATION: Run as direct Python script to avoid API cost."
        ),
    }


def generate_report() -> str:
    """Generate the full token audit report."""
    today = datetime.now().strftime("%Y-%m-%d")

    vault = audit_vault_indexer()
    daily = audit_daily_driver()
    meta = audit_meta_agent()

    agents = [vault, daily, meta]

    total_monthly_low = vault["cost_per_month"] + daily["cost_per_month"] + meta["cost_per_month_script"]
    total_monthly_high = vault["cost_per_month"] + daily["cost_per_month"] + meta["cost_per_month_cli"]

    report = f"""# Active Fleet Token Audit — {today}

## Summary

**Active agents audited:** 3 (vault-indexer, daily-driver morning, meta-agent)
**Disabled agents:** 6 (not consuming resources, not audited)
**Monthly cost range:** ${total_monthly_low:.2f} — ${total_monthly_high:.2f}

## Per-Agent Breakdown

### 1. vault-indexer
- **Schedule:** {vault['schedule']}
- **Machine:** {vault['machine']}
- **Model:** {vault['model']}
- **Cost/run:** ${vault['cost_per_run']:.2f}
- **Cost/month:** ${vault['cost_per_month']:.2f}
- **Notes:** {vault['notes']}

### 2. daily-driver (morning)
- **Schedule:** {daily['schedule']}
- **Machine:** {daily['machine']}
- **Model:** {daily['model']}
- **Estimated prompt tokens:** {daily['prompt_tokens_estimated']:,}
- **Estimated output tokens:** {daily['output_tokens_estimated']:,}
- **Cost/run (observed):** ${daily['cost_per_run_observed']:.2f}
- **Cost/month:** ${daily['cost_per_month']:.2f}
- **Notes:** {daily['notes']}

### 3. meta-agent (NEW)
- **Schedule:** {meta['schedule']}
- **Machine:** {meta['machine']}
- **Cost/run (Python script):** ${meta['cost_per_run_script']:.2f}
- **Cost/run (Claude CLI):** ${meta['cost_per_run_cli']:.2f}
- **Cost/month (script vs CLI):** ${meta['cost_per_month_script']:.2f} — ${meta['cost_per_month_cli']:.2f}
- **Notes:** {meta['notes']}

## Disabled Agents (6 total)

These agents are disabled per `AUDIT-2026-04-09-agent-downsizing.md` and are **not consuming any resources**:

| Agent | Root Cause | Re-enable Condition |
|-------|-----------|---------------------|
| process-inbox | CLIConnectionError + budget overrun (~$9.30/mo wasted) | Fix SDK transport bug |
| daily-driver evening | CLIConnectionError | Fix SDK transport bug + questionable value (better interactive) |
| daily-driver weekly | No logs found (silent failure) | Fix SDK transport bug |
| pr-digest | gh CLI PATH issue, low value (0 PRs found) | Fix gh auth in launchd + more active repos |
| sprint-health | CLIConnectionError (never produced output) | Fix SDK transport bug |
| meeting-defender | CLIConnectionError (never produced output) | Fix SDK transport bug + MCP calendar access |

**Common blocker:** `CLIConnectionError: ProcessTransport is not ready for writing` in `claude_agent_sdk` v0.1.56. This is an SDK bug, not our code. May be fixed in future SDK releases.

**MCP limitation:** Headless SDK agents cannot access MCP servers (Slack, Calendar, Gmail, Jira). This is architectural — browser-based OAuth is required. Agents needing MCP data should run in interactive sessions.

## Cost Reduction Recommendations

### daily-driver morning ($12/month — largest cost)

1. **Prompt compression:** The skill files loaded as system prompt are ~{daily['skill_prompt_size']:,} chars. Trimming examples and verbose instructions could reduce prompt tokens by 30-40%.

2. **Local model for vault-only tasks:** The daily note skeleton is mostly file reads + structured output. If MCP data (calendar, Slack) isn't available in headless mode anyway, the daily-driver could run on local Qwen3-14B (MacBook Pro) or phi4-mini-reasoning (Mac Mini) for $0/run. This would reduce monthly cost from ~$12 to ~$0.

3. **Hybrid approach:** Use local model for note skeleton, Claude API only when MCP integration is restored. This preserves quality for complex tasks while eliminating cost for simple ones.

### meta-agent ($0-3/month)

**RECOMMENDATION:** Run as a direct Python script (`python3 agents/meta_agent.py`), not via `claude` CLI. The meta-agent doesn't need LLM reasoning — it performs HTTP health checks and writes Markdown. Running as a script costs $0/month.

### Total optimized projection

| Scenario | vault-indexer | daily-driver | meta-agent | Total |
|----------|--------------|-------------|------------|-------|
| Current | $0.00 | $12.00 | $3.00 | $15.00/mo |
| Meta as script | $0.00 | $12.00 | $0.00 | $12.00/mo |
| Daily-driver local | $0.00 | $0.00 | $0.00 | $0.00/mo |
| Hybrid (recommended) | $0.00 | $6.00 | $0.00 | $6.00/mo |
"""

    return report


def main():
    report = generate_report()

    output_path = SDK_ROOT / "audit" / "token_audit_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)

    print(f"Token audit report saved: {output_path}")
    print(f"\nKey findings:")
    print(f"  - 3 active agents audited (vault-indexer, daily-driver, meta-agent)")
    print(f"  - 6 agents disabled (not consuming resources)")
    print(f"  - Current monthly cost: ~$15")
    print(f"  - Optimized projection: ~$6/mo (hybrid) or $0/mo (all local)")
    print(f"  - Biggest opportunity: move daily-driver to local model")


if __name__ == "__main__":
    main()
