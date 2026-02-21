# CLAUDE.md

This is Sean's personal command center — a second brain for Claude Code.

## What This Repo Is

102 skills, 13 agents, 7 hooks, 6 domain workspaces, and an Obsidian vault. Everything is active and auto-loaded. The installer exports subsets to other projects.

## Domain Workspaces

| Domain | Purpose | Skills |
|--------|---------|--------|
| `claude-mastery/` | CLI, hooks, MCP, settings, tech stack | 36 |
| `product-management/` | PRDs, sprints, stakeholder comms, data analysis, technical writing | 20 |
| `creative-studio/` | Phaser game dev, Remotion video, pixel art, Adobe MCP, animation, writing | 25 |
| `life-systems/` | Finance, health, learning, tasks, time, career | 9 |
| `design-team/` | Design system + 4 review agents | 8 |
| `vault/` | Obsidian vault (notes, prompts, RAG) | 6 |

## Design Team Agents

| Agent | Role |
|-------|------|
| UI Reviewer | Layout, spacing, color, typography, hierarchy |
| Accessibility Checker | WCAG 2.1 AA, contrast, keyboard nav, ARIA |
| Design System Enforcer | Token compliance, naming, component patterns |
| Visual Polish Auditor | Animations, loading/empty/error states, polish |

All read-only (disallowedTools: Edit, Write, Bash).

## Commands

```bash
# Validate everything
python3 scripts/validate.py

# Export skills to another project
./scripts/install.sh /path/to/project --preset starter|power|enterprise|creative
./scripts/install.sh /path/to/project pm-workflows remotion-mastery
./scripts/install.sh --list
```

## Architecture

```
.claude/
├── skills/          # ALL 102 skills (canonical, auto-loaded)
├── agents/          # ALL 13 agents (9 domain + 4 design team)
├── hooks/           # 7 hooks (block-secrets, log-tool-use, network-access, etc.)
└── settings.json    # Standard security profile

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
- Update `CHANGELOG.md` for version tracking
