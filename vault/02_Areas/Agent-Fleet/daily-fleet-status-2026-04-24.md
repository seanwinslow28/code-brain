# Fleet Status — 2026-04-24

**Generated:** 2026-04-24 08:35 by Meta-Agent
**Active agents:** 6 of 12 | **Disabled:** 6

## Active Agent Health

### vault-indexer (2:00 AM daily, Mac Mini, $0.00/run)
- **Status:** log-only
- **Last run:** 2026-04-24T02:00:15.994503
- **Details:** No baton found, but log exists: vault-indexer-stderr.log

### vault-synthesizer (2:30 AM daily, MBP (when awake), $0.00/run)
- **Status:** log-only
- **Last run:** 2026-04-24T03:15:10.609391
- **Details:** No baton found, but log exists: vault-synthesizer-stderr.log

### daily-driver morning (8:45 AM daily, Claude API, ~$0.40/run)
- **Status:** log-only
- **Last run:** 2026-04-23T18:51:27.539804
- **Details:** No baton found, but log exists: daily-driver-2026-04-23-morning.log
- **Daily note exists:** No (`/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/10_timeline/daily/2026-04-24.md`)

### knowledge-lint (Sunday 22:00, Mac Mini / MBP, $0.00/run)
- **Status:** no-data
- **Last run:** N/A
- **Details:** No baton files or logs found

### session-end-flush (hook-triggered, Mac Mini / MBP, $0.00/run)
- **Status:** log-only
- **Last run:** 2026-04-23T17:56:55.279835
- **Details:** No baton found, but log exists: session-end-flush.log

### meta-agent (8:35 AM daily, local, $0.00/run)
- **Status:** log-only
- **Last run:** 2026-04-24T08:35:04.468383
- **Details:** No baton found, but log exists: meta-agent-stderr.log

## Infrastructure

| Machine | Endpoint | Status |
|---------|----------|--------|
| Mac Mini | http://192.168.68.200:11434 | OFFLINE |
| Alienware | http://192.168.68.201:11434 | OFFLINE |
| ComfyUI | http://192.168.68.201:8188 | OFFLINE |

## Disabled Agents Reminder

6 agents disabled per AUDIT-2026-04-09-agent-downsizing.md:
- process-inbox, daily-driver evening/weekly, pr-digest, sprint-health, meeting-defender
- **Root causes:** CLIConnectionError in SDK transport, MCP servers unavailable in headless mode
- **Do NOT re-enable** without Sean's explicit approval and fixing the underlying SDK bug

## Cost Projection

- vault-indexer: $0.00/month (local)
- vault-synthesizer: $0.00/month (local)
- daily-driver morning: ~$12.00/month
- knowledge-lint: $0.00/month (local)
- session-end-flush: $0.00/month (local)
- meta-agent: $0.00/month (local)
- **Total active fleet:** ~$12.00/month
