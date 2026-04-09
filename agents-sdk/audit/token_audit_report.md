# Active Fleet Token Audit — 2026-04-09

## Summary

**Active agents audited:** 3 (vault-indexer, daily-driver morning, meta-agent)
**Disabled agents:** 6 (not consuming resources, not audited)
**Monthly cost range:** $12.00 — $15.00

## Per-Agent Breakdown

### 1. vault-indexer
- **Schedule:** 2:00 AM daily
- **Machine:** Mac Mini
- **Model:** nomic-embed-text (local Ollama)
- **Cost/run:** $0.00
- **Cost/month:** $0.00
- **Notes:** 100% local inference. Zero API cost. Generates embeddings for vault semantic search.

### 2. daily-driver (morning)
- **Schedule:** 8:45 AM daily
- **Machine:** Mac Mini → Claude API
- **Model:** Claude Sonnet (via headless CLI)
- **Estimated prompt tokens:** 3,158
- **Estimated output tokens:** 500
- **Cost/run (observed):** $0.40
- **Cost/month:** $12.00
- **Notes:** Most expensive active agent. ~$0.40/run observed, ~$12/month. Multi-turn conversation drives cost above single-prompt estimate. Limited value without MCP access (no calendar/Slack data in headless mode).

### 3. meta-agent (NEW)
- **Schedule:** 6:30 AM daily
- **Machine:** Mac Mini (phi4-mini-reasoning target)
- **Cost/run (Python script):** $0.00
- **Cost/run (Claude CLI):** $0.10
- **Cost/month (script vs CLI):** $0.00 — $3.00
- **Notes:** When run as Python script directly: $0.00 (no LLM needed, just HTTP checks + file writes). When run via claude CLI headless: $0.10/run budget cap = ~$3/month. RECOMMENDATION: Run as direct Python script to avoid API cost.

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

1. **Prompt compression:** The skill files loaded as system prompt are ~0 chars. Trimming examples and verbose instructions could reduce prompt tokens by 30-40%.

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
