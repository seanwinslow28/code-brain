# Changelog

All notable changes to the Claude Code Superuser Pack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.11.0] - 2026-03-08

### Added

- `writing-voice-modes` — 5 writing voice modes calibrated to Sean's personal style through interview and writing exercises. Modes: Domestic Observer (Sedaris-tuned), Gonzo Technical (Thompson-tuned), Beat Flow (Kerouac-tuned), Minimalist Absurdist (Vonnegut-tuned), and Sean Mode (calibrated hybrid default). Includes signature moves (Hard Cut/Deflation, Rule of Three with Emotional Pivot, Callback Closers, Sensory Before Numbers, Screenwriting Cut-To), professional dial (20-100% intensity by context), content type → mode mapping, complementary technique pairs, and anti-patterns. Works alongside `creative-writing` (format) and `technical-writing` (audience). References `vault/40_knowledge/references/ref-voice-mechanics-research.md` for deep author mechanics.

### Changed

- Skill count: 107 → 108

## [3.10.0] - 2026-02-28

### Added

- `intent-engineering` — Intent specification design, review, and retrofit skill for AI agents. 9-section unified template (Objective, User Goal, Outcomes, Health Metrics, Strategic Context, Constraints, Decision Authority, Edge Cases, Stop Rules), 4 autonomy levels mapped to architecture (full-autonomous/guarded-autonomous/proposal-first/human-required), Minimum Viable Retrofit guide (3 conversion levels for existing 107 skills), 5 fatal anti-patterns (Klarna Intent Gap, prompt-based hard constraints, activity vs outcome confusion, vibe-coded edge cases, missing stop rules), validation checklist. Includes `references/intent-spec-template.md` with blank YAML template and completed daily-driver worked example.

### Changed

- `agents-sdk/agents/daily_driver.py` — Enhanced `build_preamble()` with Zero-Interaction Mandate (formalized with schedule time from config), Safe Deferral Protocol (max 2 retries, error note at `<!-- agent-error -->` anchor), and Health Metric Awareness (data non-destruction, truth anchoring, content integrity). Added mode-aware execution limits in `build_options()` — reads per-mode overrides from `config.toml [agents.daily_driver.modes.*]`.
- `agents-sdk/config.toml` — Added per-mode execution limits for daily_driver: morning (15 turns/$0.25), evening (10 turns/$0.25), weekly (20 turns/$0.50).
- Skill count: 106 → 107

## [3.9.2] - 2026-03-04

### Changed

- **`daily-driver` Slack overnight scan** — Added Step 1b to morning planning protocol. Scans DMs, @mentions, and key channels since last EOD (~5 PM). Classifies messages as Action Required / FYI / Skip. Writes digest to new `<!-- slack-overnight -->` anchor in daily notes. Filters out Jira bot noise and already-replied messages. Uses native Slack plugin (`plugin:slack:slack`), not Zapier.
- **Daily note template** — Added `## Slack Overnight` section with `<!-- slack-overnight -->` anchor to `vault/90_system/templates/tpl-daily.md`, positioned above Morning Focus.

## [3.9.1] - 2026-03-04

### Changed

- **Native MCP preference over Zapier** — Updated 6 skills and Agent SDK docs to prefer native MCPs over Zapier equivalents where both exist. Skills updated: `daily-driver`, `time-management`, `meeting-prep`, `personal-finance`, `data-analysis`. Agent SDK docs (`docs/agents-adk-docs/agents-sdk.md`) "Tools, APIs, and MCPs" section fully rewritten with current connected MCP inventory and native-vs-Zapier preference table.
- **Slack plugin installed and authenticated** — Native Slack MCP plugin (`plugin:slack:slack`) installed and OAuth-authenticated to The Block Crypto Inc workspace. No admin approval required. Replaces Zapier Slack tools for interactive sessions.
- **Standalone Context7 MCP removed** — Redundant standalone `context7` MCP removed; `plugin:context7:context7` is the sole instance.
- **`.env` cleaned** — Removed stale command on line 43, orphaned bare key on line 61, fixed doubled Runware key, standardized variable naming (`Gemini_API` → `GEMINI_API_KEY`, consolidated ElevenLabs keys).

## [3.9.0] - 2026-02-22

### Added

- `prompt-engineering` — Prompt engineering skill applying Anthropic's official 9-technique checklist. Covers clarity, multishot examples, chain of thought, XML tags, role prompting, prefilling, chaining, long context, and validation loops. Includes detailed techniques-guide.md reference.
- **Agents SDK layer** (`agents-sdk/`) — Autonomous agents powered by the Claude Agent SDK (Python). Runs outside Claude Code sessions on macOS launchd schedules. Skills are loaded as system prompts — no content duplication.
- `agents-sdk/agents/daily_driver.py` — Daily Driver agent with three modes:
  - **Morning** (6:00 AM): Read yesterday's note, create today's from template, write 1-3-5 priority plan
  - **Evening** (5:00 PM): Summarize day's progress, write Evening Reflection (Win/Lesson/Carry Forward)
  - **Weekly** (Friday 4:00 PM): Aggregate 7 daily notes into weekly review at `vault/10_timeline/weekly/`
- `agents-sdk/lib/config.py` — Configuration loader: reads `config.toml` + `.env`, returns typed `Config` dataclass with per-agent settings and safety limits
- `agents-sdk/lib/skill_loader.py` — Skill-to-prompt bridge: reads `.claude/skills/*/SKILL.md`, strips YAML frontmatter, concatenates multiple skills with headers
- `agents-sdk/lib/vault_io.py` — Vault I/O utilities: path conventions (daily/weekly notes), anchor injection (`inject_at_anchor`), template creation, frontmatter reading
- `agents-sdk/lib/logging_setup.py` — Structured logging: per-run log files + append-only `agent-run-history.csv` with cost/duration/turns tracking
- `agents-sdk/lib/custom_tools.py` — MCP tool definitions: `vault_inject` tool for PATCH-style writes to vault anchors
- `agents-sdk/config.toml` — Central configuration: vault paths, per-agent settings (enabled, skills, max_turns, max_budget_usd), safety limits, logging config
- `agents-sdk/schedules/` — 3 launchd `.plist` files (morning, evening, weekly) + `install_schedules.sh` installer
- `agents-sdk/tests/` — 33 pytest tests covering config, skill loading, vault I/O, and logging
- `agents-sdk/pyproject.toml` — Python package with deps: `claude-agent-sdk>=0.1.39`, `python-dotenv`, `pandas`, `tomli`
- `docs/agents-sdk.md` — Comprehensive guide: architecture, usage, expansion, recommended integrations, troubleshooting

- **Granola meeting sync** — Installed `obsidian-granola-sync` community plugin for automatic meeting transcript sync from Granola into the vault. Notes land in `vault/30_domains/product-management/the-block-meetings-granola-notes/` with subfolders: `adops-revops`, `daily-standup`, `david-sean-one-on-ones`, `design-sync`, `ed-sean-one-on-ones`, `other`. Plugin syncs to a single destination folder; manual sorting into subfolders for now. **TODO**: Build auto-sort script/automation that routes Granola notes into subfolders based on meeting title keywords.

### Changed

- `CLAUDE.md` — Added Agents SDK section with commands, architecture diagram updated to include `agents-sdk/`
- `README.md` — Added Agents SDK section, updated skill count (89 → 106), added adobe-creative export group
- Skill count: 102 → 106 (+1 prompt-engineering, +3 from plugin/superpower installations)
- `CLAUDE.md` — Added mandatory doc-update rule: CHANGELOG.md, CLAUDE.md, and README.md must be updated whenever a new Skill, Agent, Sub-Agent, Hook, or Script is created
- Authentication: SDK uses Claude Code CLI's existing OAuth auth (`claude login`) — no separate API key required

## [3.8.1] - 2026-02-19

### Fixed

- `SKILLS-AUDIT-v2.md` — Fixed version drift: updated Final Skill Count table (v3.6.0 no longer marked CURRENT, v3.8.0 now CURRENT), updated all skill/agent/hook inventory sections with Phase 5-6 additions, marked all Gap Analysis items as DONE, updated section headers with correct counts, updated footer to reflect v3.8.0 state.
- `SKILLS-AUDIT-v2.md` — Updated Lessons Learned #1: background subagent limitation documented with full tool compatibility table (Read/Glob/Grep work, Write/Edit/Bash blocked with explicit error, not silent). Added workaround pattern.
- `export-groups/07-technical-stack/playground.json` — Fixed duplicate `agents` key (had both `"agents": ["code-reviewer"]` and `"agents": []`).
- Synced `docs/Superuser-Pack-Skills-Audit.md` mirror with updated audit doc.

## [3.8.0] - 2026-02-18

### Added

- `comfyui-workflows` — Dedicated ComfyUI workflow design, debugging, and automation skill. Covers workflow JSON structure, node wiring patterns (KSampler, LoRA, ControlNet, IPAdapter), API queuing/polling, batch generation, model management, and debugging common issues.
- `daily-note-appender` hook (Stop) — Appends session summary to today's Obsidian daily note when Claude Code stops.
- `network-access-control` hook (PreToolUse Bash) — Blocks curl/wget/nc to non-whitelisted domains.

### Changed

- `block-secrets.py` — Narrowed patterns to eliminate false positives. Replaced `*key*` with `*api_key*`, `*api-key*`, `*apikey*`, `*private_key*`, `*private-key*`. Replaced `*password*` with `*_password*`, `*passwd*`. Added `*secret_key*`, `*_secret*`, `*client_secret*`. No longer blocks files containing "keyboard", "keynote", "keyframe", etc.
- Skill count: 101 → 102 (+1 new)
- Hook count: 5 → 7 (+2 new)

## [3.7.0] - 2026-02-18

### Added

- `animation-pipeline` — End-to-end 2D animation production pipeline with AI-assisted generation. 12-stage pipeline (Script→Final Render) with QA gates (blocker vs warning), shot packet structure, ComfyUI integration for character/background generation, frame interpolation (RIFE/FILM), style profiles, asset naming conventions.
- `script-writing` — Screenplay writing for animated short films. Industry-standard format, beat sheet structure (6-8 beats for shorts, 10-12 for longer), dialogue craft rules, animation-specific additions (timing cues, SFX notation), production handoff with shot breakdown tables, table read protocol.
- `creative-writing` — Multi-format writing assistant for blog posts, social media (Twitter/X threads, LinkedIn, Instagram), pitch documents (festival submissions, grant applications), artist bios/statements, portfolio narratives. Cross-format adaptation guide and voice consistency profile.
- `career-transition` — PM → Animation PM/Producer transition guide. Terminology bridge (40+ term translations), role map with title-level equivalencies, festival circuit (Tier 1/2/3), production tools comparison, transition narrative template, 90-day plan.
- `personal-app-patterns` — Opinionated starter patterns for React + Vite + Tailwind + Supabase personal apps. Canonical folder structure, auth context, protected routes, common database tables, dark mode toggle, deployment checklist.
- `technical-writing` — Audience-aware document craft. Templates for API getting-started guides, system design docs, onboarding guides, runbooks, release notes, internal RFCs. Differentiated from doc-workflows (automated generation) and tech-spec (engineering blueprints).
- `rn-architecture` — React Native app architecture and project setup. Covers Expo SDK 52+, Expo Router (file-based), Zustand, TanStack Query, EAS Build profiles, feature-based folder structure. Complements rn-debug (diagnosis).
- `comfyui-workflows` — (see 3.8.0 for this entry, created alongside Phase 6)
- `animation-director` agent — Read-only reviewer for animation assets and pipeline outputs. Applies QA gates from animation-pipeline and 2d-animation-principles.
- `code-reviewer` agent — Read-only code reviewer for architecture, patterns, performance, security. Complements design-team agents (UI-focused).
- Skill count: 94 → 101 (+7 new skills)
- Agent count: 11 → 13 (+2 new agents)
- All new skills at Q:5 quality level
- Updated export-group manifests: 03-creative-projects, 02-pm-workflows, 05-life-optimization, 07-technical-stack

## [3.6.0] - 2026-02-18

### Added

- `etf-page-creator` — WordPress ETF page creation assistant for The Block. Guides data collection (Track Insight IDs, TradingView symbols, issuers, fees, categories), validates inputs, auto-generates SEO metadata using Block's standard formats, and produces copy-paste checklist matching WordPress field order.

### Changed

- `meeting-prep` — Full Block rewrite: standup format (10-10:45 AM ET, round-robin by Jira board), full team roster (17 members organized by Product/Design/Engineering/QA/DevOps), 7 recurring meetings with cadence/time/attendees, JQL queries for standup prep, 1:1 templates for Ed and David, Retros.work integration, meeting necessity check. Quality: 4→5.
- `data-analysis` — Full Block rewrite: tools access table (GA4 via Zapier MCP, Looker view-only, Jira full, Google Sheets), key metrics tracking (content, data pages, ad revenue, Campus, SEO), Ed's 6 analytics questions, Zapier MCP GA4 query patterns, pandas analysis pipeline, report templates (weekly/monthly), distribution workflow (Confluence → Slack → vault). Quality: 4→5.
- `stakeholder-update` — Merged biweekly-jira-update skill: team scope (16 members), 3 JQL queries with exact statuses, product/area prefixes (.Co, Campus, SFMC, Ad Server, Crypto IQ), status tags, output template with 3 sections, recurring patterns, quality checks. Retained general comms framework. Quality: 4→5.
- `jira-automation` — Merged the-block-jira-ticket-writer skill: Block Jira config (PRO/GD/DE/OP/BE project keys, component IDs, labels), ticket templates (Epic with Problem/Solution/Scope/Metrics, Design Story with [Design] prefix, Implementation Story with [Implementation] prefix), PRD-to-tickets workflow, real examples (PRO-4354 Sponsored Courses, PRO-3513 Job Board), quality checklist. Quality: 4→5.
- `sprint-roadmap` — Refocused as general PM sprint planning tool: capacity calculation, velocity tracking, RICE/MoSCoW/Impact-Effort prioritization with worked examples, backlog grooming workflow with JQL patterns, roadmap generation template, dependency mapping, release planning checklist. Quality: 4→5.
- `commit-checklist` — Expanded from stub to comprehensive skill: pre-commit validation checklist (security, code quality, completeness, scope), conventional commit message format with type reference table, good/bad examples, multi-commit strategy, full workflow with git commands. Quality: 3→5.
- `org-definition-of-done` — Expanded from stub to comprehensive skill: DoD templates for 4 work types (Feature, Bug Fix, Refactor, Spike), Release DoD with pre/deploy/post checklists, evidence-gathering workflow, status reporting format, customization guide for different team contexts. Quality: 3→5.
- `team-styleguide` — Expanded from stub to comprehensive skill: auto-detection from config files (ESLint, Prettier, tsconfig, .editorconfig, pyproject.toml), universal rules (naming, imports, comments, file structure), language-specific rules (TypeScript, Python, CSS/Tailwind), review workflow with pass/warn/fail output, style guide setup for new projects. Quality: 3→5.
- Skill count: 93 → 94 (+1 new etf-page-creator)
- All 94 skills now at Q:4-5 (100% quality threshold met)

## [3.5.0] - 2026-02-18

### Changed

- `health-habits` — Full rewrite with Sean's personal data: PPL split (Mon=Push, Tue=Pull/Arms, Wed=Legs/Abs, Thu=Push, Fri=Pull/Back, Sat/Sun=active recovery), 4:45 AM anchor schedule, 3-4 sets to failure training style, Apple Fitness → CSV pipeline via Shortcuts, XP/level gamification engine (10 levels from Recruit to Immortal, streak bonuses), Obsidian vault integration (daily note checkboxes, weekly summary), supplement stack tracking. Quality: 3→5.
- `personal-finance` — Full rewrite with Sean's financial data: Chase CSV parser (Transaction Date, Post Date, Description, Category, Type, Amount, Memo) + Bilt CSV parser (headerless quoted format), $5,741/mo net income baseline, 19 active subscriptions with keep/cancel status, 7 annual renewal dates, modified 50/30/20 budget framework (30% to debt+savings), debt paydown calculator with interest projection, 40+ Sean-specific regex merchant patterns, anomaly detection (Z-score). Quality: 5→5 (major content upgrade).
- `time-management` — Full rewrite with Sean's schedule: 4:45 AM→9 PM daily structure, 6-block energy map (PEAK post-workout, LOW 1-2 PM lull), 45/35/20 work split at The Block, Focus Day (Mon/Fri) vs Meeting Day (Tue-Thu), `/today` daily planning ritual, PEARL conflict resolution with personalized priority hierarchy, weekly time split review template, Google Calendar OAuth integration plan. Quality: 4→5.
- `life-admin` — Full rewrite with Sean's life context: Boston move March 21 checklist (15 tracked items), medical provider transition Medvidi→Aetna (7-step checklist with continuity of care documentation), address change tracker (financial, shopping, services, government, insurance), annual subscription renewal calendar, file organization audit workflow, Cannes France Sep 2026 trip planning. Quality: 3→5.

## [3.4.0] - 2026-02-17

### Added

- `daily-driver` — Daily personal assistant for morning planning, task prioritization, and EOD review. Integrates with Obsidian daily notes. 1-3-5 prioritization framework, carry-over tracking, weekly review.
- `subscription-audit` — Subscription and recurring expense auditor. Parses bank/credit card exports, identifies recurring charges, evaluates against free alternatives, outputs keep/replace/cancel decision matrix with savings projections.
- `analytics-workarounds` — Analytics data access workarounds for PMs without direct GA4/Looker access. Uses Zapier MCP as a data bridge to Google Sheets. Includes recurring pipeline setup patterns.
- `zapier-mcp-automation` — Master reference for ~175 Zapier MCP tools. Multi-tool workflow recipes (sprint kickoff, standup summary, weekly metrics), task budget optimization (each call = 2 tasks), cross-app automation chains.
- `vault-read-write`: added Multi-Source Synthesis Protocol (4-step framework: salient keywords, consensus, divergence, actionable takeaways; Consensus Matrix table format) and `/compress` session-end context handoff command — both merged from knowledge-management

### Changed

- `ai-creative-tools` — Full rewrite: replaced outdated "CLAUDE.md hooks" with real Claude Code PostToolUse hooks in settings.json format, removed hardcoded API keys (now env vars), added Hugging Face MCP integration (model search, Space inference, paper search), added ComfyUI queue script with polling, updated ElevenLabs to multilingual_v2 model, added asset index management and cross-references to related creative skills
- Skill count: 90 → 93 (+4 new, -1 deleted)
- Export group `02-pm-workflows`: added analytics-workarounds
- Export group `03-creative-projects`: added 2d-animation-principles (was missing from manifest)
- Export group `04-advanced-techniques`: added zapier-mcp-automation
- Export group `05-life-optimization`: added daily-driver and subscription-audit, removed knowledge-management

### Removed

- `knowledge-management` — Unique content (Synthesis Protocol, /compress) merged into vault-read-write. Remaining content (atomic notes, cross-linking, PKM organizing) fully covered by vault-architecture, knowledge-graph-nav, and vault-read-write.

## [3.3.0] - 2026-02-17

### Added

- `zapier-chrome-automation` — Zapier workflow automation combining MCP API actions with Chrome browser UI editing. Bridges the gap where MCP can query data but cannot edit Zap step configurations. Includes pre-flight account verification, editor UI patterns, and coordinated MCP+Chrome workflows.

### Fixed

- `security-reviewer` agent: replaced broken Cursor IDE tool names (`write`, `edit`, `search_replace`, `delete_file`, `run_terminal_cmd`) with correct Claude Code names (`Edit`, `Write`, `Bash`)
- `compliance-summarizer` agent: same Cursor→Claude Code tool name fix
- `data-analyst` agent: added missing `disallowedTools: [Edit, Write, Bash]` (was completely unrestricted)
- `game-design-advisor` agent: added missing `disallowedTools: [Edit, Write, Bash]` (was completely unrestricted)
- `python-automation` skill: fixed `title: string` (JS syntax) → `title: str` (Python syntax)

### Changed

- Skill count: 99 → 90 (+1 new, -10 consolidated)
- Agent security: 11/11 properly configured (was 6/11)
- `prd-generator`: added Quick Mode note (from quick-prd merge)
- `config-settings`: absorbed claude-md-optimization content (@import system, monorepo pattern, token budgets, CLAUDE.md vs Skills table, update cadence, security template)
- `stakeholder-update`: absorbed stakeholder-brief content (3 tone templates, 4 verification tests)
- `phaser-game-patterns`: absorbed phaser-pattern content (RN WebView bridge, StateMachine, LoadingScene, Common Gotchas)
- `sprite-asset-pipeline`: absorbed sprite-pipeline content (TexturePacker CLI, free-tex-packer, Aseprite CLI, pngquant/WebP, automation script, frame rates)
- `learning-accelerator`: absorbed learning-drill content (5 drill formats, 4-week progression, tracking log)
- `personal-finance`: absorbed budget-entry content (quick-entry formats, auto-categorization, integrations, monthly review)
- `supabase-backend`: absorbed supabase-python content (Python client setup, auth, queries)
- Updated 7 export-group manifests to remove references to deleted skills

### Removed

- 3 redundant skills (pure deletes): `safe-ops`, `org-security`, `quick-prd`
- 7 merged source skills (content transferred to targets): `supabase-python`, `claude-md-optimization`, `stakeholder-brief`, `phaser-pattern`, `sprite-pipeline`, `learning-drill`, `budget-entry`
- Orphan `plugin/skills/safe-ops/` directory

## [3.2.0] - 2026-02-16

### Added

- 6 new Adobe MCP skills for Creative Studio domain (Creative Studio: 15 → 21 skills):
  - `creative-director` — AI Creative Director for planning, interviewing, and critiquing visual projects. Includes critique rubrics and handoff protocol references.
  - `adobe-photoshop-mcp` — Photoshop image editing and compositing via adb-mcp UXP plugin. Includes MCP command reference.
  - `adobe-premiere-mcp` — Premiere Pro video editing and timeline automation via adb-mcp UXP plugin. Includes MCP command reference and editorial grammar (Murch's Rule of Six).
  - `adobe-aftereffects-mcp` — After Effects motion graphics and animation via adb-mcp CEP plugin (ExtendScript). Includes ExtendScript patterns reference.
  - `adobe-illustrator-mcp` — Illustrator vector graphics and SVG automation via adb-mcp CEP plugin (ExtendScript). Includes ExtendScript patterns reference.
  - `adobe-cross-app-workflows` — Cross-app pipeline orchestration, MCP architecture reference, shared guardrails, and troubleshooting.
- New export group: `12-adobe-creative` with all 6 Adobe skills

### Changed

- Skill count: 93 → 99
- Creative Studio domain: 15 → 21 skills

## [3.1.0] - 2026-02-15

### Added

- 3 new skills from Superpowers plugin deep merge:
  - `systematic-debugging` — Four-phase root cause debugging with 5 supporting reference files (root-cause-tracing, defense-in-depth, condition-based-waiting, find-polluter.sh)
  - `subagent-driven-development` — Fresh subagent per task with two-stage review (spec compliance + code quality), includes 3 prompt templates
  - `verification-before-completion` — Iron law: no completion claims without fresh verification evidence

### Enhanced

- `prd-generator` — Deep merged with Superpowers brainstorming: added HARD GATE (no code before design approval), one-question-at-a-time interview style, approach exploration (2-3 options with trade-offs), section-by-section approval for M/L scope
- `tech-spec` — Deep merged with Superpowers writing-plans: added bite-sized task structure (2-5 min RED-GREEN-REFACTOR steps), precision requirements (exact file paths, complete code, exact commands), plan header template, execution handoff (subagent-driven vs parallel session)
- `skill-system-mastery` — Deep merged with Superpowers writing-skills: added Claude Search Optimization (CSO), token efficiency targets, TDD-for-skills methodology (RED-GREEN-REFACTOR for skill creation), rationalization prevention patterns (HARD-GATE blocks, loophole closers, red flags)

### Changed

- Skill count: 89 → 93
- `export-groups/01-core-features/playground.json`: added `subagent-driven-development`
- `export-groups/04-advanced-techniques/playground.json`: added `systematic-debugging`, `verification-before-completion`

## [3.0.0] - 2026-02-08

### Architecture

- **Breaking**: Transformed from skill distribution system to personal command center / second brain
- All 89 skills now live at `.claude/skills/` (canonical, auto-loaded in this repo)
- All 11 agents live at `.claude/agents/` (7 domain + 4 new design team)
- `playgrounds/` renamed to `export-groups/` (metadata-only manifests for installer)
- `shared/agents/` removed (consolidated into `.claude/agents/`)
- Installer reads skill names from manifests, copies from `.claude/skills/`
- Stale `shared_agents`/`shared_hooks` fields removed from presets
- Preset JSON key `playgrounds` renamed to `export_groups`
- All manifest versions bumped to 3.0.0

### Added

- 6 domain workspaces with README, templates, reference materials, and scripts:
  - `claude-mastery/` — CLI, hooks, MCP, settings, tech stack (34 skills)
  - `product-management/` — PRDs, sprints, stakeholder comms (18 skills)
  - `creative-studio/` — Phaser, Remotion, sprites, pixel art (15 skills)
  - `life-systems/` — Finance, health, learning, tasks with 5 automation scripts (8 skills)
  - `design-team/` — Design system + 4 review agents (8 skills)
  - `vault/` — Obsidian vault with PARA structure (6 skills)
- 4 new design team agents (all read-only):
  - UI Reviewer — layout, spacing, color, typography, hierarchy
  - Accessibility Checker — WCAG 2.1 AA, contrast, keyboard nav, ARIA
  - Design System Enforcer — token compliance, naming, component patterns
  - Visual Polish Auditor — animations, loading/empty/error states, micro-interactions
- Obsidian vault with PARA structure, MOCs, Templates, Prompts library, RAG directory
- 5 Maps of Content (MOCs) linking to domain workspaces
- 4 Obsidian note templates (daily, project, meeting, idea)
- Life automation scripts: analyze_spending.py, health_audit.py, md_to_anki.py, organize_inbox.py, audit_calendar.py

### Changed

- `scripts/install.sh` v3.0.0: reads skill names from manifests, copies from `.claude/skills/`
- `scripts/install.ps1` v3.0.0: same changes
- `scripts/validate.py` v3.0.0: validates root .claude/, domains, vault, secret scanning across workspaces
- `CLAUDE.md`: rewritten for personal hub paradigm
- `README.md`: rewritten to reflect second brain architecture
- `.gitignore`: added vault and life-systems data patterns

### Removed

- `playgrounds/*/.claude/` subdirectories (skills moved to root .claude/)
- `playgrounds/` directory name (renamed to `export-groups/`)
- `shared/agents/` directory (agents consolidated into .claude/agents/)
- `shared_agents` and `shared_hooks` fields from presets (unused in v3 installer)

## [2.0.0] - 2025-02-06

### Architecture

- **Breaking**: Replaced tier-based packs (`packs/starter`, `packs/power`, `packs/enterprise`) with 11 domain-specific playgrounds
- New composable architecture: install individual playgrounds or use presets
- Old tier names preserved as presets (`presets/starter.json`, etc.)
- Enterprise is now a security profile applied on top of any preset, not a separate pack
- Templates folded into skill `references/` directories

### Added

- 11 domain-specific playgrounds with 89 total skills:
  - 01-core-features (12 skills): CLI, hooks, subagents, MCP, settings, skill system
  - 02-pm-workflows (13 skills): PRDs, tickets, stakeholder updates, data analysis
  - 03-creative-projects (7 skills): Phaser 3, sprites, pixel art, AI tools
  - 04-advanced-techniques (7 skills): multi-instance, context management, Plan Mode
  - 05-life-optimization (8 skills): finance, tasks, learning, health, time
  - 06-obsidian-integration (6 skills): vault architecture, MCP, semantic search
  - 07-technical-stack (9 skills): React, Python, Supabase, Git, Docker
  - 08-domain-specific (5 skills): crypto, education, API PM, RevOps, AI-native
  - 09-community-resources (6 skills): learning paths, troubleshooting, case studies
  - 10-master-designer (8 skills): animations, micro-interactions, Tailwind, Figma
  - 11-remotion-mastery (8 skills): video creation, typography, data viz, transitions
- `shared/` infrastructure: hooks, agents, and security profiles
- 4 presets: starter, power, enterprise, creative
- 2 security profiles: standard, enterprise
- `playground.json` manifest for each playground with dependencies
- `CLAUDE.section.md` composable fragments for CLAUDE.md generation
- New `scripts/install.sh` composable installer with `--preset`, `--security`, `--list` flags
- New `scripts/install.ps1` PowerShell equivalent
- New `scripts/validate.py` playground-aware validator (10 check categories)
- Creative preset for design/game-dev focused workflows
- 72 new skills generated from NotebookLM extraction pipeline

### Changed

- Install script: `install-pack.sh` replaced by `install.sh` with new CLI
- Validation script: `validate-pack.py` replaced by `validate.py` with playground checks
- Settings composition: installer builds `settings.json` from security profiles
- CLAUDE.md composition: installer concatenates playground section fragments

### Removed

- `packs/` tier-based directory structure (archived to `_archive/packs-v1/`)
- Standalone templates directory (folded into skill `references/`)
- Duplicate skills across packs (consolidated into canonical playgrounds)

## [1.0.0] - 2024-01-XX

### Added
- Initial release of Claude Code Superuser Pack
- Three pack templates: starter, power, and enterprise
- Starter pack with 3 skills (team-styleguide, commit-checklist, safe-ops) and 2 hooks (block-secrets, log-tool-use)
- Power pack with 9 skills, 4 agents, 4 hooks, and 5 templates
- Enterprise pack with 3 skills, 2 agents, and 4 hooks (including require-confirm-highrisk)
- Installation scripts for Unix/macOS (install-pack.sh) and Windows PowerShell (install-pack.ps1)
- Validation script (validate-pack.py) to check JSON validity, required files, markdown headings, and secrets
- Plugin directory with safe, universal components
- Marketplace manifest (.claude-plugin/marketplace.json)

### Security
- block-secrets.py hook blocks edits to sensitive files (.env, **/secrets/**, etc.)
- require-confirm-highrisk.sh hook blocks risky Bash commands in enterprise pack
