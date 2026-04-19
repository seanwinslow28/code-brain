# CLAUDE.md

This is Sean's personal command center — a second brain for Claude Code.

## What This Repo Is

113 skills, 13 Claude Code subagents, 11 hooks, 13 autonomous SDK agents (6 active), **3 primary domain folders** + cross-cutting infrastructure, an Obsidian vault, and an Agent SDK layer for autonomous operation. Everything is active and auto-loaded. The installer exports subsets to other projects.

As of v3.15.0, the repo is organized so that domain-owned folders live inside their domain. `the-block/` is Sean's day-job workspace (with `product-management/` nested inside). `creative-studio/` owns 16BitFit and the design-team workspace. `life-systems/` owns personal systems. Cross-cutting infra (`.claude/`, `agents-sdk/`, `vault/`, `claude-mastery/`, installer dirs) stays at root.

## Domain Workspaces

| Domain | CLAUDE.md | What lives here |
|--------|-----------|----------------|
| `the-block/` | [the-block/CLAUDE.md](the-block/CLAUDE.md) | Day-job PM work. Nested: `product-management/` (PRD templates, sprint frameworks, stakeholder comms templates) |
| `creative-studio/` | [creative-studio/CLAUDE.md](creative-studio/CLAUDE.md) | Phaser game dev, Remotion video, pixel art, Adobe MCP, animation, writing. Nested: `16bitfit-battle-mode/` (project), `design-team/` (design system + review agent support) |
| `life-systems/` | [life-systems/CLAUDE.md](life-systems/CLAUDE.md) | Finance, health, learning, tasks, time, career transition |
| `claude-mastery/` | (no CLAUDE.md — cross-cutting reference) | CLI, hooks, MCP, settings, tech stack, prompt-engineering reference |
| `vault/` | (Obsidian, not a workspace) | PARA notes, prompts, RAG, Granola meeting sync, operating-model artifacts |

## Domain Routing

Use this table to decide which CLAUDE.md to load for a given task:

| Task type | Load this CLAUDE.md |
|---|---|
| PM / day-job / Block work | [the-block/CLAUDE.md](the-block/CLAUDE.md) |
| Creative work (Remotion, art, writing, animation) | [creative-studio/CLAUDE.md](creative-studio/CLAUDE.md) |
| 16BitFit Battle Mode specifically | [creative-studio/16bitfit-battle-mode/CLAUDE.md](creative-studio/16bitfit-battle-mode/CLAUDE.md) |
| Personal systems (finance, health, learning, time) | [life-systems/CLAUDE.md](life-systems/CLAUDE.md) |
| Claude Code CLI / hooks / MCP / settings reference | [claude-mastery/](claude-mastery/) |

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

**Active agents (6 of 13):**

| Agent | Schedule | Skills/Model | Cost/Run |
|-------|----------|---------------|----------|
| Vault Indexer | 2:00 AM daily | nomic-embed-text (Mac Mini Ollama) | $0.00 (local) |
| Vault Synthesizer | 2:30 AM daily | Qwen3-14B on MBP (intermittent — succeeds only when MBP awake; v3.14.3 retired WOL) | $0.00 (local) |
| Meta-Agent (fleet health) | 8:35 AM daily | phi4-mini (Mac Mini), local checks only | $0.00 (local) |
| Daily Driver (morning) | 8:45 AM daily | daily-driver, vault-read-write | ~$0.40 |
| Knowledge Lint | Sunday 22:00 | Tier 1 phi4-mini (Mac Mini); Tier 2 Qwen3-14B on MBP if awake | $0.00 (local) |
| Flush (SessionEnd) | hook-triggered | phi4-mini (Mac Mini) always; ≥100-msg sessions attempt Qwen3-14B on MBP if awake | $0.00 (local) |

Phase 6 (v3.14.3) shipped the knowledge compounding loop producer side: SessionEnd flush → Vault Synthesizer v2 → Knowledge Lint. The consumer side (autoresearch feedback, D.4) was **descoped** pending upstream autoresearch harness — re-open spec in `creative-studio/16bitfit-battle-mode/docs/plans/phase6-SUPER-PLAN-2026-04-17.md` §10.1. All agents run 100% local.

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

Config: `agents-sdk/config.toml`. Auth: uses `claude login` OAuth (no API key needed). Safety: max 30 turns, $0.50/run cap. SDK version: `0.1.63` (pinned in `agents-sdk/pyproject.toml` as of v3.15.0). Morning schedule: 8:45 AM (was 6:00 AM as of v3.12.2). Full docs: `docs/agents-sdk.md`.

**launchd requirement:** All plists must include `EnvironmentVariables` with `PATH` set to `/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`. Without this, the `claude` CLI is not discoverable and agents fail with `CLIConnectionError`. See `agents-sdk/BUGFIX-2026-04-07-launchd-path.md`.

## Architecture

```
.claude/
├── skills/          # ALL 113 skills (canonical, auto-loaded)
├── agents/          # ALL 13 agents (8 domain + 5 design team)
├── hooks/           # 11 hooks (block-secrets, cost-watchdog, daily-note-appender,
│                    #           format-on-edit, log-tool-use, loop-detector,
│                    #           network-access-control, require-confirm-highrisk,
│                    #           run-tests-on-stop, session-end-flush, vault-integrity)
└── settings.json    # Standard security profile

agents-sdk/          # Autonomous agents (Claude Agent SDK, Python)
├── agents/          # Agent scripts (daily_driver.py + scheduled launchd agents)
├── lib/             # Shared modules (config, skill loader, vault I/O, logging)
├── schedules/       # launchd plists + installer
├── tests/           # pytest suite
└── config.toml      # Agent config, paths, safety limits

the-block/                            # DOMAIN 1 — day job
├── CLAUDE.md
├── README.md
└── product-management/               # nested workspace (moved from root in v3.15.0)

creative-studio/                      # DOMAIN 2 — creative work
├── CLAUDE.md
├── README.md
├── 16bitfit-battle-mode/             # nested project (moved from root in v3.15.0)
├── design-team/                      # nested workspace (moved from root in v3.15.0)
└── (existing finance/, scripts/, templates/)

life-systems/                         # DOMAIN 3 — personal systems
├── CLAUDE.md
├── README.md
└── (existing reference/)

claude-mastery/      # cross-cutting Claude Code meta-reference (stays at root)
vault/               # Obsidian vault (PARA + MOCs + operating-models + Prompts + RAG)
export-groups/       # Metadata-only manifests (for installer export)
shared/hooks/        # Hook source files (for installer)
shared/security/     # Security profiles (standard, enterprise)
presets/             # Export presets (starter, power, enterprise, creative)
scripts/             # install.sh, install.ps1, validate.py
plugin/              # Marketplace distribution
docs/                # Ecosystem documentation
```

## Non-Negotiable Rules

1. **Plan Mode vs Extended Thinking**: Plan Mode = double `Shift+Tab` or `/plan`. Extended Thinking = single `Tab`. Never confuse the two.
2. **Agent tool restrictions**: Use `disallowedTools` (deny-list), not allow-list.
3. **Hooks enforce; subagents judge**: PreToolUse for binary allow/deny; subagents for subjective reviews.
4. **Hook blocking**: Exit code **2** to deny (not 0 or 1).
5. **Settings precedence** (highest wins): Enterprise managed > Project local > Project settings > User settings
6. **Permission evaluation** (first match wins): Deny > Ask > Allow
7. **3-domain structure (v3.15.0)**: `the-block/`, `creative-studio/`, `life-systems/` are the only workspace folders that house domain-specific content. `product-management/` lives nested inside `the-block/`; `design-team/` and `16bitfit-battle-mode/` live nested inside `creative-studio/`. The prior rule that `product-management/` stayed at the root is **explicitly waived as of v3.15.0**.

## Hook Exit Codes

- `0` = Allow
- `1` = Error (logged, operation allowed)
- `2` = **Deny** (blocks the operation)

## When Modifying

- Run `python3 scripts/validate.py` after changes (v3.15.0: validator hard-enforces the 3 primary domain folders)
- Skills live in `.claude/skills/` (not export-groups)
- Agents live in `.claude/agents/` (not shared/agents/)
- Update `export-groups/*/playground.json` manifests when adding/removing skills
- New domain-specific content goes inside the correct domain folder (`the-block/`, `creative-studio/`, or `life-systems/`)
- **Mandatory doc updates**: When creating a new Skill, Agent, Sub-Agent, Hook, or Script, you MUST update all three of these files:
  - `CHANGELOG.md` — Add entry under the current version's Added section
  - `CLAUDE.md` — Update counts (skill/agent/hook totals, domain table, architecture comment)
  - `README.md` — Update counts and any affected tables
