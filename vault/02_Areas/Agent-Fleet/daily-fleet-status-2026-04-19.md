# Fleet Status — 2026-04-19

**Generated:** 2026-04-19 08:35 by Meta-Agent
**Active agents:** 2 of 8 | **Disabled:** 6

## Active Agent Health

### vault-indexer (2:00 AM daily, Mac Mini, $0.00/run)
- **Status:** no-data
- **Last run:** N/A
- **Details:** No baton files or logs found

### daily-driver morning (8:45 AM daily, Claude API, ~$0.40/run)
- **Status:** no-data
- **Last run:** N/A
- **Details:** No baton files or logs found
- **Daily note exists:** No (`/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/01_Journals/Daily Notes/2026-04-19.md`)

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

- vault-indexer: $0.00/month (local Ollama)
- daily-driver morning: ~$12.00/month ($0.40/day x 30)
- meta-agent: ~$3.00/month ($0.10/day x 30)
- **Total active fleet:** ~$15.00/month
