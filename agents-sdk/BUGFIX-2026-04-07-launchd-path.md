# Bugfix: launchd agents failing with TaskGroup / CLIConnectionError

**Date:** 2026-04-07
**Affected:** All Claude Agent SDK agents running via launchd (daily-driver, process-inbox, pr-digest, etc.)
**Status:** Fixed

## Symptoms

Every agent run via launchd failed immediately (~6 seconds) with:

```
ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
```

The run history showed continuous failures since 2026-04-01:

```
2026-04-01,17:00:09,daily-driver,evening,error,,,,unhandled errors in a TaskGroup (1 sub-exception)
2026-04-02,06:00:06,daily-driver,morning,error,,,,unhandled errors in a TaskGroup (1 sub-exception)
...12 consecutive failures across daily-driver, process-inbox, pr-digest...
```

Meanwhile, `vault-indexer` (which doesn't use the Claude Agent SDK / CLI subprocess) continued to succeed.

## Root Cause

The `TaskGroup` error was a wrapper. The actual exception buried inside it was:

```
claude_agent_sdk._errors.CLIConnectionError: ProcessTransport is not ready for writing
```

**What happened:** The Claude Agent SDK spawns the `claude` CLI as a subprocess and communicates via stdin/stdout. The SDK tried to write to the subprocess, but it had already crashed.

**Why the CLI crashed:** macOS launchd runs scheduled jobs with a minimal `PATH` — typically just `/usr/bin:/bin:/usr/sbin:/sbin`. The `claude` CLI is installed at `/Users/seanwinslow/.local/bin/claude`, which is not in launchd's default PATH. When the SDK tried to spawn `claude`, the OS couldn't find the binary, the subprocess died immediately, and the SDK's transport layer threw `CLIConnectionError` when it tried to write to the dead process.

**Why vault-indexer was unaffected:** It uses local Python libraries (sentence-transformers, etc.) and doesn't spawn the Claude CLI subprocess.

**Contributing factor:** The SDK was also outdated — `0.1.39` vs latest `0.1.56` (17 versions behind). While the PATH issue was the primary cause, the newer SDK may have better error handling for this scenario.

## Fix Applied

### 1. Added `PATH` to all 9 launchd plists

Added an `EnvironmentVariables` block with PATH to every plist in `schedules/`:

```xml
<key>EnvironmentVariables</key>
<dict>
    <key>PATH</key>
    <string>/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
</dict>
```

Critical entry: `/Users/seanwinslow/.local/bin` — where `claude` CLI lives.
Also includes `/opt/homebrew/bin` for `gh` (GitHub CLI, needed by pr-digest) and other Homebrew tools.

**Files modified:**
- `com.sean.agent.daily-morning.plist` — added EnvironmentVariables
- `com.sean.agent.daily-evening.plist` — added EnvironmentVariables
- `com.sean.agent.daily-morning-baton.plist` — added EnvironmentVariables
- `com.sean.agent.process-inbox.plist` — added EnvironmentVariables
- `com.sean.agent.pr-digest.plist` — added EnvironmentVariables
- `com.sean.agent.vault-indexer.plist` — added EnvironmentVariables
- `com.sean.agent.weekly-review.plist` — added EnvironmentVariables
- `com.sean.agent.sprint-health.plist` — added PATH to existing EnvironmentVariables
- `com.sean.agent.meeting-defender.plist` — added PATH to existing EnvironmentVariables

### 2. Upgraded Claude Agent SDK

```
0.1.39 → 0.1.56
```

All existing imports (`ClaudeAgentOptions`, `ResultMessage`, `query`, `create_sdk_mcp_server`, `tool`) verified compatible.

### 3. Reloaded all launchd agents

```bash
for plist in ~/Library/LaunchAgents/com.sean.agent.*.plist; do
    launchctl unload "$plist"
    launchctl load "$plist"
done
```

## Verification

**2026-04-08 morning run:** PATH fix confirmed working — agent connected, ran 9 turns, spent $0.29. However, it failed with `error_max_budget_usd` because the morning budget was set to $0.25. This is a tuning issue, not a connectivity issue.

### Follow-up fix (2026-04-08)

- **Bumped morning budget:** $0.25 → $0.50 in `config.toml`
- **Changed morning schedule:** 6:00 AM → 8:45 AM (both `config.toml` and launchd plist)
- Reloaded plist via `launchctl unload/load`

To verify:

```bash
# View latest run status
tail -5 vault/90_system/agent-logs/agent-run-history.csv

# Check evening run log (fires at 5 PM)
cat vault/90_system/agent-logs/daily-driver-$(date +%Y-%m-%d)-evening.log

# Manual test (outside Claude Code session to avoid nesting detection)
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode evening --dry-run
```

## Lessons Learned

1. **launchd has a minimal PATH** — any scheduled job that spawns external CLIs needs explicit PATH in the plist. This is a common macOS gotcha.
2. **The SDK's error reporting is poor** — `TaskGroup (1 sub-exception)` hides the real cause. The actual `CLIConnectionError` is only visible in the full traceback from stderr, not in the Python logger output. The `record_run` function captures only `str(e)[:200]` which gets the wrapper, not the inner exception.
3. **vault-indexer succeeding was a red herring** — it masked the systemic PATH issue because it doesn't use the Claude CLI subprocess.

## Future Prevention

When adding new launchd plists, always include the `EnvironmentVariables` block with PATH. Consider adding this to the `install_schedules.sh` script as a validation check.
