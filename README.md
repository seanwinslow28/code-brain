# Claude Code Superuser Pack

An open-source agentic engineering practitioner's toolkit — **119** skills, 13 subagents, **14** hooks, **17** autonomous SDK agents (8 currently running on launchd by default, 2 opt-in disabled-by-default, 1 manual-trigger), **3 primary domains**, an Obsidian vault, and a Claude Agent SDK runtime, all auto-loaded. Every component is in active use; every scheduled agent has a launchd schedule; every skill is a prompt and every prompt has a job. If you've read Karpathy's "agentic engineering" framing and wondered what one looks like in the wild, this is one.

## What's Inside

### Domain Workspaces (v3.15.0 structure)

The repo is organized so domain-owned folders live inside their domain. Open one folder, find everything for that domain.

| Domain | CLAUDE.md | What Lives There |
|--------|-----------|-----------------|
| **the-block/** | `the-block/CLAUDE.md` | **Archived 2026-05** — reference templates from prior PM role at The Block (crypto/ETF). |
| **creative-studio/** | `creative-studio/CLAUDE.md` | Phaser game dev, Remotion video production, pixel art, sprite pipelines, animation, writing. Nested: `16bitfit-battle-mode/` (project), `design-team/` (design system + 5 review agent support) |
| **life-systems/** | `life-systems/CLAUDE.md` | Finance tracking, health habits, learning drills, task management, time, career transition |
| **vault/20_projects/prj-job-hunt-2026/** | (project, not a domain workspace) | Active 8-week job-hunt sprint (post-Block, 2026-05-04). Master plan + migration plan + status tracker. |

Cross-cutting (no domain CLAUDE.md):

| Folder | What Lives There |
|--------|-----------------|
| **claude-mastery/** | CLI shortcuts, hooks, MCP, settings, tech stack reference (used by all domains) |
| **vault/** | Obsidian vault with PARA structure, MOCs, prompt library, RAG knowledge, operating-model artifacts |
| **agents-sdk/** | Autonomous Claude Agent SDK layer (Python + launchd) |
| **evals/vault-synthesizer/** | 10-case binary eval suite for the vault synthesizer agent (v3.30.1) |
| **.claude/** | Canonical skills, agents, hooks, settings (auto-loaded) |

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
| Vault Indexer | 2:00 AM daily | Incremental nomic-embed-text index of all vault notes |
| Vault Synthesizer | 2:30 AM daily | Generates concept + connection articles from changed vault files (100% local, Qwen3-14B on MBP when awake; intermittent since v3.14.3). **v3.34.0 retrofit (Tier 1):** quote-first prompt + canonical-slug reuse + cross-domain preference; killed the hardcoded `Evidence pending.` regression. Tiers 2-4 (cluster-and-sample retrieval, EDC canonicalization, three-pass agentic synthesis) gated behind nightly-run signal — see [retrofit plan](vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md). |
| Deep Researcher (v3.23.0) | 2:45 AM daily | Pulls one question from `vault/00_inbox/research-queue.md`, runs LearningCircuit LDR locally (SearXNG + Qwen3-14B GGUF Q4_K_M `qwen3-14b-research:latest` Modelfile via Ollama on **Mac Mini** `:5050`), writes a topical note + injects digest into today's daily note. 100% local, $0/run |
| Meta-Agent | 8:35 AM daily | Fleet self-monitoring — checks active-agent recency + infra health, writes fleet-status note that feeds Daily Driver |
| Daily Driver (morning) | 8:45 AM | Read yesterday's note, create today's, write 1-3-5 priorities, surface Vault Health + fleet alerts. v3.16.0: loads operating-model HEARTBEATs for all 3 domains + on-demand USER/SOUL/schedule-recs reads. v3.27.0: injects a 7-line Fleet Overnight Digest under `<!-- fleet-overnight -->` and the daily-note template carries four live Dataview blocks (today's fleet status, new knowledge, new research, latest lint report) |
| Knowledge Lint | Sunday 22:00 | Two-tier vault health scan (structural + semantic). Reports surface in the morning brief. |
| Flush (SessionEnd) | on session close | Extracts decisions/lessons/actions/quotes from transcripts into `vault/daily/YYYY-MM-DD.md` |
| Job Feed (v3.28.0) | 8:00–11:00 AM (7 fires) | Scrapes 4 public feeds + ~40-company ATS watchlist, scores PM/APM roles with Qwen3-14B, writes daily roll-up to `vault/20_projects/prj-job-hunt-2026/job-feed/` and surfaces 3-line summary in morning brief. 100% local, $0/run |

**Key design:** Skills are prompts, agents are runners. SKILL.md files are loaded as system prompts — no content duplication. Skill improvements automatically flow to autonomous agents.

**Phase 6 knowledge compounding loop** (v3.14.3): SessionEnd flush → Vault Synthesizer v2 → Knowledge Lint. The vault becomes a living graph the LLM maintains instead of a static archive. The autoresearch-feedback consumer side (D.4) is descoped pending upstream autoresearch-harness stability — re-open spec in the Phase 6 Super Plan §10.1. **Knowledge-loop Phase B** (2026-04-25, branch `knowledge-loop/phase-b`) adds a SessionStart hook that injects the synthesizer-produced `vault/knowledge/index.md` as `additionalContext` on every new Claude Code session, closing the consumer loop on the read side. **Knowledge-loop Phase C** (v3.19.0, 2026-05-01) adds `agents-sdk/scripts/query.py` for terminal Q&A against the index with two-pass orchestration (selection → answer). `--file-back` persists answers as a third article tier at `vault/knowledge/qa/<slug>.md` with OB1-inspired chunk_id + similarity provenance in frontmatter (C.M1) and an append-only JSONL manifest at `vault/knowledge/qa/.manifest.json` (C.M2). **Knowledge-loop Phase D** (v3.20.0, 2026-05-01) adds a queryable typed-edge layer: vault_indexer's SQLite gains a `concept_edges` table with six relation values (`supports`, `contradicts`, `evolved_into`, `supersedes`, `depends_on`, `related_to`) populated by vault_synthesizer as a side effect of each connection article, and read by knowledge_lint Tier 2's SQL fast path for zero-LLM-cost contradiction detection. `vault/health/synth-manifest-{date}.json` captures per-run counts (concepts, connections, edges, rejected) surfaced in the daily-driver morning brief.

**Agent-wiring Phase 2** (v3.17.0, 2026-04-27): `meta_agent` / `flush` / `knowledge_lint` consume operating-model artifacts so their local-model prompts are domain-aware. `meta_agent` calls gemma4:e4b on Mac Mini with all three `schedule-recommendations.md` bodies to produce a "Domain-Aware Insights" section ranking fleet activity against Sean's Protect / Automate / Decline lists. `flush.py` prepends all three domain SOULs to its extraction prompt; `knowledge_lint.py` Tier-2 gains a SOUL context block and a new `soul-tier-a-conflict` issue kind at HIGH severity. All local-only, no cloud egress. Pre-flight against five historical session transcripts produced 5 / 5 valid JSON with the SOUL prepend.

```bash
# Dry run (free)
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run

# Live run
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning

# Install/remove launchd schedules
./agents-sdk/schedules/install_schedules.sh
```

Safety: 30 turn cap, default $0.50/run budget (daily-driver morning is $0.60 in v3.16.0 to absorb the operating-model preamble), inherits block-secrets hook, no Bash access. Auth: uses existing `claude login` session (no API key needed). Full docs: [docs/agents-sdk.md](docs/agents-sdk.md).

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

### 119 Skills Across 12 Export Groups

> The 12 export groups roll up 118 of the 119 skills. The new `llm-council` skill (v3.35.0) is not in any export group — it's a personal-use multi-vendor critique tool dependent on the in-tree `tools/llm-council/` Python CLI, so it doesn't ship via the installer. See [`tools/llm-council/README.md`](tools/llm-council/README.md) for details.

All skills auto-load from `.claude/skills/`. Reference them naturally in prompts.

| Export Group | Skills | Highlights |
|-------------|--------|------------|
| core-features | 12 | CLI mastery, hooks, subagents, MCP, settings |
| pm-workflows | 15 | PRDs, tickets, stakeholder updates, data analysis, Jira status checks, Gemini DR |
| creative-projects | 8 | Phaser 3, sprite pipelines, pixel art, AI tools, Gemini image gen |
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
