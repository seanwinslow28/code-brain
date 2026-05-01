# Fleet Status — 2026-04-27

**Generated:** 2026-04-27 12:26 by Meta-Agent
**Active agents:** 6 of 12 | **Disabled:** 6

## Active Agent Health

### vault-indexer (2:00 AM daily, Mac Mini, $0.00/run)
- **Status:** healthy (dry-run)
- **Last run:** 2026-04-27T12:26:18.024274
- **Details:** Dry run — skipping actual log check

### vault-synthesizer (2:30 AM daily, MBP (when awake), $0.00/run)
- **Status:** healthy (dry-run)
- **Last run:** 2026-04-27T12:26:18.024276
- **Details:** Dry run — skipping actual log check

### daily-driver morning (8:45 AM daily, Claude API, ~$0.40/run)
- **Status:** healthy (dry-run)
- **Last run:** 2026-04-27T12:26:18.024278
- **Details:** Dry run — skipping actual log check
- **Daily note exists:** Yes (`/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/10_timeline/daily/2026-04-27.md`)

### knowledge-lint (Sunday 22:00, Mac Mini / MBP, $0.00/run)
- **Status:** healthy (dry-run)
- **Last run:** 2026-04-27T12:26:18.024278
- **Details:** Dry run — skipping actual log check

### session-end-flush (hook-triggered, Mac Mini / MBP, $0.00/run)
- **Status:** healthy (dry-run)
- **Last run:** 2026-04-27T12:26:18.024279
- **Details:** Dry run — skipping actual log check

### meta-agent (8:35 AM daily, local, $0.00/run)
- **Status:** healthy (dry-run)
- **Last run:** 2026-04-27T12:26:18.024280
- **Details:** Dry run — skipping actual log check

## Domain-Aware Insights

_Dry run — skipped gemma4:e4b call. Schedule-recommendations context loaded for 3 domains (26,150 chars)._


## Infrastructure

| Machine | Endpoint | Status |
|---------|----------|--------|
| Mac Mini | http://192.168.68.200:11434 | Online |
| Alienware | http://192.168.68.201:11434 | Online |
| ComfyUI | http://192.168.68.201:8188 | Online |

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
