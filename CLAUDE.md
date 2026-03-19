# CLAUDE.md

This is Sean's personal command center — a second brain for Claude Code.

## What This Repo Is

111 skills, 13 agents, 7 hooks, 6 domain workspaces, an Obsidian vault, and an Agent SDK layer for autonomous operation. Everything is active and auto-loaded. The installer exports subsets to other projects.

## Domain Workspaces

| Domain | Purpose | Skills |
|--------|---------|--------|
| `claude-mastery/` | CLI, hooks, MCP, settings, tech stack, prompt engineering | 38 |
| `product-management/` | PRDs, sprints, stakeholder comms, data analysis, technical writing | 20 |
| `creative-studio/` | Phaser game dev, Remotion video, pixel art, Adobe MCP, animation, writing | 26 |
| `life-systems/` | Finance, health, learning, tasks, time, career | 9 |
| `design-team/` | Design system + 4 review agents + design arena | 11 |
| `vault/` | Obsidian vault (notes, prompts, RAG, Granola meeting sync) | 6 |

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

| Agent | Schedule | Skills Loaded |
|-------|----------|---------------|
| Daily Driver (morning) | 6:00 AM | daily-driver, vault-read-write |
| Daily Driver (evening) | 5:00 PM | daily-driver, vault-read-write |
| Daily Driver (weekly) | Friday 4:00 PM | daily-driver, vault-read-write |

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

Config: `agents-sdk/config.toml`. Auth: uses `claude login` OAuth (no API key needed). Safety: max 30 turns, $0.50/run cap. Full docs: `docs/agents-sdk.md`.

## Architecture

```
.claude/
├── skills/          # ALL 111 skills (canonical, auto-loaded)
├── agents/          # ALL 13 agents (9 domain + 4 design team)
├── hooks/           # 7 hooks (block-secrets, log-tool-use, network-access, etc.)
└── settings.json    # Standard security profile

agents-sdk/          # Autonomous agents (Claude Agent SDK, Python)
├── agents/          # Agent scripts (daily_driver.py, more planned)
├── lib/             # Shared modules (config, skill loader, vault I/O, logging)
├── schedules/       # launchd plists + installer
├── tests/           # pytest suite (33 tests)
└── config.toml      # Agent config, paths, safety limits

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
