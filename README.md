# Claude Code Superuser Pack

A personal command center and second brain for Claude Code. 89 skills, 11 agents, 6 domain workspaces, and an Obsidian vault — all active and auto-loaded.

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

### 89 Skills Across 11 Domains

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
| master-designer | 8 | Animations, micro-interactions, Tailwind, Figma |
| remotion-mastery | 8 | Programmatic video, typography, data viz |

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
