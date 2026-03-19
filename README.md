# Claude Code Superuser Pack

A personal command center and second brain for Claude Code. 111 skills, 13 interactive agents, 7 hooks, 6 domain workspaces, an Obsidian vault, and an autonomous Agent SDK layer — all active and auto-loaded.

## What's Inside

### Domain Workspaces

| Domain | What Lives There |
|--------|-----------------|
| **claude-mastery/** | CLI shortcuts, hooks, MCP, settings, tech stack reference |
| **product-management/** | PRD templates, sprint frameworks, stakeholder comms, active projects |
| **creative-studio/** | Phaser game dev, Remotion video production, pixel art, sprite pipelines |
| **life-systems/** | Finance tracking, health habits, learning drills, task management, automation scripts |
| **design-team/** | Design system, brand guidelines, 4 read-only review agents |
| **vault/** | Obsidian vault with PARA structure, MOCs, prompt library, RAG knowledge |

### Design Team (4 Review Agents)

- **UI Reviewer** — Visual consistency, layout, spacing, color, typography
- **Accessibility Checker** — WCAG 2.1 AA compliance, contrast, keyboard nav, ARIA
- **Design System Enforcer** — Token compliance, naming conventions, component patterns
- **Visual Polish Auditor** — Animations, loading/empty/error states, micro-interactions

All read-only. They audit, you fix.

### Agents SDK (Autonomous Layer)

The `agents-sdk/` directory adds scheduled, autonomous agents powered by the [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview). These run **outside** Claude Code sessions on macOS launchd schedules — no human required.

| Agent | Schedule | What It Does |
|-------|----------|-------------|
| Daily Driver (morning) | 6:00 AM | Read yesterday's note, create today's, write 1-3-5 priorities |
| Daily Driver (evening) | 5:00 PM | Summarize day, write reflection, carry forward items |
| Daily Driver (weekly) | Friday 4:00 PM | Aggregate 7 daily notes into weekly review |

**Key design:** Skills are prompts, agents are runners. SKILL.md files are loaded as system prompts — no content duplication. Skill improvements automatically flow to autonomous agents.

```bash
# Dry run (free)
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run

# Live run
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning

# Install/remove launchd schedules
./agents-sdk/schedules/install_schedules.sh
```

Safety: 30 turn cap, $0.50/run budget, inherits block-secrets hook, no Bash access. Auth: uses existing `claude login` session (no API key needed). Full docs: [docs/agents-sdk.md](docs/agents-sdk.md).

### Native MCP Integrations

Skills and agents prefer native MCPs over Zapier where both exist. Currently connected:

| Service | MCP | Status |
|---------|-----|--------|
| Google Calendar | `claude.ai Google Calendar` + `google-workspace` | Connected |
| Gmail | `claude.ai Gmail` + `google-workspace` | Connected |
| Google Sheets/Docs/Drive | `google-workspace` | Connected |
| Jira + Confluence | `mcp-atlassian` + `claude.ai Atlassian` | Connected |
| Slack | Slack plugin (OAuth) | Installed, pending workspace admin |
| GitHub | `github` MCP (Docker) | Connected |
| Obsidian Vault | `obsidian-vault` | Connected |
| NotebookLM | `notebooklm-mcp` | Connected |
| Figma | `claude.ai Figma` | Connected |
| Hugging Face | `claude.ai Hugging Face` | Connected |

Zapier retained only for services with no native MCP: Salesforce, GA4, Webhooks, Code execution.

### 109 Skills Across 12 Domains

All skills auto-load from `.claude/skills/`. Reference them naturally in prompts.

| Export Group | Skills | Highlights |
|-------------|--------|------------|
| core-features | 12 | CLI mastery, hooks, subagents, MCP, settings |
| pm-workflows | 13 | PRDs, tickets, stakeholder updates, data analysis |
| creative-projects | 7 | Phaser 3, sprite pipelines, pixel art, AI tools |
| advanced-techniques | 7 | Multi-instance, context management, Plan Mode |
| life-optimization | 8 | Finance, tasks, learning, health tracking |
| obsidian-integration | 6 | Vault architecture, MCP setup, semantic search |
| technical-stack | 9 | React/Vite/Tailwind, Python, Supabase, Git, Docker |
| domain-specific | 5 | Crypto/Web3, education, API PM, RevOps |
| community-resources | 6 | Learning paths, troubleshooting, case studies |
| master-designer | 9 | Animations, micro-interactions, Tailwind, Figma, design arena |
| remotion-mastery | 8 | Programmatic video, typography, data viz |
| adobe-creative | 6 | Photoshop, Premiere, After Effects, Illustrator |

## Export to Other Projects

The installer copies skill subsets to any project:

```bash
# See what's available
./scripts/install.sh --list

# Install a preset
./scripts/install.sh /path/to/project --preset starter

# Install specific export groups
./scripts/install.sh /path/to/project 02-pm-workflows 11-remotion-mastery

# Apply enterprise security
./scripts/install.sh /path/to/project 02-pm-workflows --security enterprise

# Windows
.\scripts\install.ps1 -TargetDir "C:\path" -Preset "power"
```

### Presets

| Preset | Skills | Best For |
|--------|--------|----------|
| **starter** | 18 | Getting started safely |
| **power** | 89 | Full productivity |
| **enterprise** | 30 | Maximum security |
| **creative** | 44 | Game dev and design |

## Validation

```bash
python3 scripts/validate.py
```

Checks: root .claude/ structure, export-group manifests, domain workspaces, vault, presets, plugin, shared integrity, and secret scanning.

## Key Rules

- **Plan Mode** = double `Shift+Tab` or `/plan` (not single Tab)
- **Extended Thinking** = single `Tab`
- Agent tool restrictions use **deny-list** (`disallowedTools`)
- Hook blocking uses **exit code 2**
- Settings precedence: Enterprise > Local > Project > User

## License

See [LICENSE](LICENSE) file for details.
