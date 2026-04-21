# Fleet Status — 2026-04-21

**Generated:** 2026-04-21 08:35 by Meta-Agent
**Active agents:** 6 of 12 | **Disabled:** 6

## Active Agent Health

### vault-indexer (2:00 AM daily, Mac Mini, $0.00/run)
- **Status:** log-only
- **Last run:** 2026-04-21T02:00:06.034659
- **Details:** No baton found, but log exists: vault-indexer-stderr.log

### vault-synthesizer (2:30 AM daily, MBP (when awake), $0.00/run)
- **Status:** log-only
- **Last run:** 2026-04-21T02:36:08.695294
- **Details:** No baton found, but log exists: vault-synthesizer-stderr.log

### daily-driver morning (8:45 AM daily, Claude API, ~$0.40/run)
- **Status:** log-only
- **Last run:** 2026-04-20T08:45:41.440210
- **Details:** No baton found, but log exists: daily-driver-2026-04-20-morning.log
- **Daily note exists:** No (`/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/10_timeline/daily/2026-04-21.md`)

### knowledge-lint (Sunday 22:00, Mac Mini / MBP, $0.00/run)
- **Status:** log-only
- **Last run:** 2026-04-19T22:00:05.849079
- **Details:** No baton found, but log exists: knowledge-lint-stderr.log

### session-end-flush (hook-triggered, Mac Mini / MBP, $0.00/run)
- **Status:** log-only
- **Last run:** 2026-04-20T08:45:41.679919
- **Details:** No baton found, but log exists: session-end-flush.log

### meta-agent (8:35 AM daily, local, $0.00/run)
- **Status:** log-only
- **Last run:** 2026-04-20T13:59:10.519866
- **Details:** No baton found, but log exists: meta-agent-stdout.log

## Infrastructure

| Machine | Endpoint | Status |
|---------|----------|--------|
| Mac Mini | http://192.168.68.200:11434 | Online |
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
