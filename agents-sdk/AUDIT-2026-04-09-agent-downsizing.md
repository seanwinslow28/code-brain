# Agent Fleet Audit & Downsizing — 2026-04-09

## Summary

On 2026-04-09, Sean and Claude conducted a full audit of all Agent SDK agents. Of 10 enabled agents, only 2 were producing value. The other 8 were disabled, their launchd schedules unloaded, and their logs cleaned up.

**Do NOT re-enable any disabled agent without Sean's explicit approval.** This decision was deliberate, not accidental.

## What Stays Active

| Agent | Schedule | Cost/Run | Why It Stays |
|:------|:---------|:---------|:-------------|
| **vault-indexer** | 2:00 AM daily | $0.00 (local Ollama on Mac Mini) | 100% success rate across all logged runs. Generates embeddings for vault semantic search. Zero cost — runs entirely on local hardware. |
| **daily-driver (morning)** | 8:45 AM daily | ~$0.40 | Creates the daily note skeleton with carry-forwards from yesterday. First successful run on 2026-04-09 after v3.12.1 PATH fix + v3.12.2 budget bump. Limited value without MCP access (see below), but still saves ~5 min of manual daily note setup. |

## What Was Disabled and Why

### process-inbox — DISABLED (was burning ~$9.30/month)

- **Schedule:** 5:30 AM daily
- **Budget:** $0.25 (was exceeding it every run at ~$0.31)
- **Success rate:** 0/6 (April 1–9)
- **Error:** `CLIConnectionError: ProcessTransport is not ready for writing` followed by `error_max_budget_usd`. The agent would connect, start working, hit the SDK subprocess transport bug, and then burn through budget retrying before crashing.
- **Impact:** ~$0.31/day wasted = ~$9.30/month for zero output.

### daily-driver (evening) — DISABLED (noisy failures)

- **Schedule:** 5:00 PM daily
- **Success rate:** 0/6 (April 1–9)
- **Error:** Same `CLIConnectionError` as process-inbox. Crashes before making API calls, so $0 cost but generates large error logs.
- **Additional reason:** Even if fixed, the evening wrap-up ("wrap up my day") is better done interactively where Claude has access to Slack, calendar, and the full conversation context from the day's work.

### daily-driver (weekly) — DISABLED (no evidence of working)

- **Schedule:** Friday 4:00 PM
- **Success rate:** No logs found in the entire audit period.
- **Reason:** Either never triggered or crashed silently. Weekly reviews are better done interactively anyway.

### pr-digest — DISABLED (unreliable, low value)

- **Schedule:** 8:00 AM daily
- **Budget:** $0.00 (uses `gh` CLI locally)
- **Success rate:** 1/3 — worked once on 4/8 but found 0 PRs across 3 repos.
- **Error:** `gh CLI not available` — the launchd PATH fix (v3.12.1) doesn't reliably make `gh` discoverable. Works only when the machine has an active shell session.
- **Additional reason:** Sean's personal repos rarely have open PRs. The one successful run found nothing.

### sprint-health — DISABLED (never produced output)

- **Schedule:** Friday 3:00 PM
- **Success rate:** 0/1 — only log entry is "Starting sprint health monitor agent" with no completion.
- **Reason:** Likely the same CLIConnectionError but crashes before even logging the error. Never produced a single sprint health report.

### meeting-defender — DISABLED (never produced output)

- **Schedule:** Monday 7:00 AM
- **Success rate:** 0/1 — same as sprint-health, just "Starting..." with no completion.
- **Reason:** Same failure pattern.

### preserve-session — DISABLED (manual-only, no schedule)

- **Config:** enabled but no launchd schedule
- **Reason:** Was never automated. Preserve-session is inherently interactive (saves context from the current Claude Code session). No value as a scheduled agent.

### spending-analysis — DISABLED (manual-only, no schedule)

- **Config:** enabled but no launchd schedule
- **Reason:** Was never automated. Better run on-demand when Sean imports new bank CSVs.

## Root Causes

### 1. CLIConnectionError (affects 4+ agents)

The Claude Agent SDK spawns `claude` as a subprocess. The `subprocess_cli.py` transport has a race condition or timing issue where `ProcessTransport is not ready for writing` at query close time. This surfaces as an `ExceptionGroup` / `TaskGroup` error. The v3.12.1 PATH fix resolved the binary-not-found variant, but this transport readiness bug persists. It seems timing-dependent — the morning agent started working at 8:45 AM (machine is awake, user is active) while 5:30 AM and 5:00 PM runs consistently fail.

### 2. MCP Servers Unavailable in Headless Mode

The Agent SDK runs `claude` CLI in non-interactive/headless mode. MCP servers that require browser-based OAuth (Slack, Google Calendar, Gmail, Google Workspace, Atlassian, GitHub) are **not available** to headless agents. This is a fundamental architectural limitation, not a bug to fix. It means:

- Daily driver morning cannot pull calendar or Slack data
- Meeting defender cannot check calendar
- Sprint health cannot query Jira
- PR digest needs `gh` CLI as a workaround (fragile)

The practical solution: headless agents handle vault-only tasks (file reads/writes, embeddings). Interactive sessions handle everything requiring MCP access.

### 3. gh CLI PATH Issue

The `gh` CLI installed via Homebrew lives at `/opt/homebrew/bin/gh`. The launchd PATH includes `/opt/homebrew/bin`, but `gh` also requires authentication state that may not be available when launchd runs the agent outside a user shell session. The intermittent success (1/3) suggests it works when the user has an active terminal session.

## Cost Impact

**Before audit:** ~$12-15/month in wasted agent runs (process-inbox ~$9.30 + failed daily-driver morning attempts ~$3-5)

**After audit:** ~$12/month for one working agent (daily-driver morning at ~$0.40/day)

**Vault indexer:** Always $0 (local Ollama)

## Log Cleanup

Removed all logs for disabled agents and truncated rolling stderr files:
- **Before:** 44 files, ~160KB of mostly repeated `CLIConnectionError` stack traces
- **After:** 12 files — vault-indexer history, today's daily-driver log, trimmed CSV

## Re-enabling Agents

If Sean wants to re-enable any agent in the future:

1. Fix the underlying issue first (CLIConnectionError for SDK agents, gh auth for pr-digest)
2. Set `enabled = true` in `agents-sdk/config.toml`
3. Reload the launchd plist: `launchctl bootstrap gui/$(id -u) agents-sdk/schedules/<plist-file>`
4. Monitor the next 3 runs before considering it stable

The SDK transport bug (`CLIConnectionError`) is in the `claude_agent_sdk` package, not our code. It may be fixed in a future SDK release (currently on v0.1.56).
