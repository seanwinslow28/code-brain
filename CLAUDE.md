# CLAUDE.md

This is Sean's personal command center — a second brain for Claude Code.

## What This Repo Is

111 skills, 16 agents, 8 hooks, 7 domain workspaces, an Obsidian vault, and an Agent SDK layer for autonomous operation. Everything is active and auto-loaded. The installer exports subsets to other projects.

## Domain Workspaces

| Domain | Purpose | Skills |
|--------|---------|--------|
| `claude-mastery/` | CLI, hooks, MCP, settings, tech stack, prompt engineering | 40 |
| `product-management/` | PRDs, sprints, stakeholder comms, data analysis, technical writing | 19 |
| `creative-studio/` | Phaser game dev, Remotion video, pixel art, Adobe MCP, animation, writing | 25 |
| `life-systems/` | Finance, health, learning, tasks, time, career | 9 |
| `design-team/` | Design system + 4 review agents + design arena | 11 |
| `vault/` | Obsidian vault (notes, prompts, RAG, Granola meeting sync) | 7 |
| `16bitfit-battle-mode/` | 16BitFit Battle Mode: sprite pipeline, agent fleet, autoresearch | Project CLAUDE.md |

## Design Team Agents

| Agent | Role |
|-------|------|
| UI Reviewer | Layout, spacing, color, typography, hierarchy |
| Accessibility Checker | WCAG 2.1 AA, contrast, keyboard nav, ARIA |
| Design System Enforcer | Token compliance, naming, component patterns |
| Visual Polish Auditor | Animations, loading/empty/error states, polish |

All read-only (disallowedTools: Edit, Write, Bash).

## Connected MCPs (Native — No Zapier)

Skills and agents prefer native MCPs over Zapier. When both exist, always use native first.

| Service | Native MCP | Zapier Fallback |
|---------|-----------|----------------|
| Google Calendar | `claude.ai Google Calendar` / `google-workspace` | `google_calendar_*` |
| Gmail | `claude.ai Gmail` / `google-workspace` | `gmail_*` |
| Google Sheets/Docs/Drive | `google-workspace` | `google_sheets_*` / `google_docs_*` |
| Jira + Confluence | `mcp-atlassian` / `claude.ai Atlassian` | `jira_software_cloud_*` |
| Slack | Slack plugin (pending Block admin approval) | `slack_*` |
| GitHub | `github` MCP (Docker) | N/A |

**Still Zapier-only:** Salesforce, GA4, Webhooks, Code execution.

**Calendar rule:** Always query BOTH `sean.winslow28@gmail.com` AND `swinslow@theblock.co` in parallel.

## Commands

```bash
# Validate everything
python3 scripts/validate.py

# Export skills to another project
./scripts/install.sh /path/to/project --preset starter|power|enterprise|creative
./scripts/install.sh /path/to/project pm-workflows remotion-mastery
./scripts/install.sh --list
```

## Agents SDK (Autonomous Layer)

The `agents-sdk/` directory adds scheduled, autonomous agents powered by the Claude Agent SDK. These run **outside** Claude Code sessions on macOS launchd schedules. Skills are loaded as system prompts — no duplication.

**Active agents (5 of 13):**

| Agent | Schedule | Skills/Model | Cost/Run |
|-------|----------|---------------|----------|
| Vault Indexer | 2:00 AM daily | nomic-embed-text (Mac Mini Ollama) | $0.00 (local) |
| Vault Synthesizer | 2:30 AM daily | Qwen3-14B via route_to_macbook | $0.00 (local) |
| Daily Driver (morning) | 8:45 AM daily | daily-driver, vault-read-write | ~$0.40 |
| Knowledge Lint | Sunday 22:00 | Tier 1 phi4-mini (Mac Mini), Tier 2 Qwen3-14B (MBP) | $0.00 (local) |
| Flush (SessionEnd) | hook-triggered | phi4-mini or Qwen3-14B (by msg count) | $0.00 (local) |

Phase 6 (v3.14.0) added the knowledge compounding loop: SessionEnd flush → Vault Synthesizer v2 → Knowledge Lint → autoresearch feedback. All three new agents run 100% local.

**The 6 agents disabled in v3.12.3** (2026-04-09) remain disabled. See `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md` for rationale. Do NOT re-enable without Sean's explicit approval.

**Key limitation:** Headless SDK agents cannot access MCP servers (Slack, Google Calendar, Gmail, etc.) — those require browser-based OAuth only available in interactive sessions. The morning agent creates the daily note skeleton; Slack/calendar data is backfilled when Sean starts an interactive session.

```bash
# Dry run (free, prints prompt)
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run

# Live run
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning

# Install/remove launchd schedules
./agents-sdk/schedules/install_schedules.sh
./agents-sdk/schedules/install_schedules.sh --remove

# Run tests
cd agents-sdk && PYTHONPATH=. pytest tests/ -v
```

Config: `agents-sdk/config.toml`. Auth: uses `claude login` OAuth (no API key needed). Safety: max 30 turns, $0.50/run cap. SDK version: `0.1.56`. Morning schedule: 8:45 AM (was 6:00 AM as of v3.12.2). Full docs: `docs/agents-sdk.md`.

**launchd requirement:** All plists must include `EnvironmentVariables` with `PATH` set to `/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`. Without this, the `claude` CLI is not discoverable and agents fail with `CLIConnectionError`. See `agents-sdk/BUGFIX-2026-04-07-launchd-path.md`.

## Architecture

```
.claude/
├── skills/          # ALL 111 skills (canonical, auto-loaded)
├── agents/          # ALL 13 agents (9 domain + 4 design team)
├── hooks/           # 8 hooks (block-secrets, log-tool-use, network-access,
│                    #          session-end-flush, run-tests-on-stop, …)
└── settings.json    # Standard security profile

agents-sdk/          # Autonomous agents (Claude Agent SDK, Python)
├── agents/          # Agent scripts (daily_driver.py, more planned)
├── lib/             # Shared modules (config, skill loader, vault I/O, logging)
├── schedules/       # launchd plists + installer
├── tests/           # pytest suite (33 tests)
└── config.toml      # Agent config, paths, safety limits

16bitfit-battle-mode/ # 16BitFit Battle Mode project (sprite pipeline + agent fleet + autoresearch)
{6 domain dirs}/     # Working files, templates, reference, active projects
vault/               # Obsidian vault (PARA + MOCs + Prompts + RAG)
export-groups/       # Metadata-only manifests (for installer export)
shared/hooks/        # Hook source files (for installer)
shared/security/     # Security profiles (standard, enterprise)
presets/             # Export presets (starter, power, enterprise, creative)
scripts/             # install.sh, install.ps1, validate.py
plugin/              # Marketplace distribution
```

## Non-Negotiable Rules

1. **Plan Mode vs Extended Thinking**: Plan Mode = double `Shift+Tab` or `/plan`. Extended Thinking = single `Tab`. Never confuse the two.
2. **Agent tool restrictions**: Use `disallowedTools` (deny-list), not allow-list.
3. **Hooks enforce; subagents judge**: PreToolUse for binary allow/deny; subagents for subjective reviews.
4. **Hook blocking**: Exit code **2** to deny (not 0 or 1).
5. **Settings precedence** (highest wins): Enterprise managed > Project local > Project settings > User settings
6. **Permission evaluation** (first match wins): Deny > Ask > Allow

## Hook Exit Codes

- `0` = Allow
- `1` = Error (logged, operation allowed)
- `2` = **Deny** (blocks the operation)

## When Modifying

- Run `python3 scripts/validate.py` after changes
- Skills live in `.claude/skills/` (not export-groups)
- Agents live in `.claude/agents/` (not shared/agents/)
- Update `export-groups/*/playground.json` manifests when adding/removing skills
- **Mandatory doc updates**: When creating a new Skill, Agent, Sub-Agent, Hook, or Script, you MUST update all three of these files:
  - `CHANGELOG.md` — Add entry under the current version's Added section
  - `CLAUDE.md` — Update counts (skill/agent/hook totals, domain table, architecture comment)
  - `README.md` — Update counts and any affected tables
