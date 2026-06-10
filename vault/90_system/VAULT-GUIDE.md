---
type: reference
domain:
  - vault
status: active
ai-context: "Comprehensive guide to Sean's Obsidian vault: architecture, conventions, knowledge-loop infrastructure, SDK-agent contracts, and operational workflows. 2026-05-06 refresh."
created: 2026-02-21
updated: 2026-05-06
---

# Sean's Obsidian Vault — Complete Guide

> **Last refreshed: 2026-05-06.** The vault has changed substantially since the original 2026-02-21 guide. Major additions: 14 SDK agents (7 active), the operating-models artifact system at `05_atlas/operating-models/`, the knowledge-loop infrastructure (`vault/knowledge/`, `vault/health/`, `.vault-index.db`), the agent-fleet workspace at `02_Areas/Agent-Fleet/`, and a job-hunt-2026 project added 2026-05-04 after Sean was laid off from The Block. Apple Notes archives have been collapsed. See [Changelog](#changelog) at the bottom for the timeline.
>
> **Authoritative cross-reference:** Repo-level architecture, SDK-agent details, hook list, and non-negotiable rules live in `/CLAUDE.md`. This guide focuses on the vault interior — folder semantics, frontmatter schema, agent producer/consumer contracts, and the daily/weekly workflows. When in doubt, CLAUDE.md wins.

This document describes everything about this vault: its architecture, how it connects to Claude Code and the autonomous SDK agents, and how to work within it effectively. It is written for both human operators and AI agents.

## Quick Reference for AI Agents

If you read **only one section**, read this one.

### Where do I put new content?

| What you have | Where it goes | Filename pattern |
|---|---|---|
| New capture, can't classify yet | `00_inbox/` | (your choice; will be re-named on triage) |
| Reference / how-to / guide | `40_knowledge/references/` | `ref-<kebab>.md` |
| Concept, framework, idea | `40_knowledge/concepts/` | `idea-<kebab>.md` |
| Active project work | `20_projects/<prj-name>/` | depends on project |
| Synthesized concept article (LLM-generated) | `knowledge/concepts/` | auto-named by `vault_synthesizer` |
| Synthesized connection article (LLM-generated) | `knowledge/connections/` | auto-named by `vault_synthesizer` |
| Q&A answer (terminal `query.py` output) | `knowledge/qa/` | auto-named by `query.py --file-back` |
| Daily note | `10_timeline/daily/` | `YYYY-MM-DD.md` |
| Granola meeting (auto-synced) | `30_domains/product-management/the-block-meetings-granola-notes/` | `mtg-YYYY-MM-DD-<slug>.md` (post-process) |
| Operating-model artifact | `05_atlas/operating-models/<domain>/` | `HEARTBEAT.md` / `USER.md` / `SOUL.md` / `operating-model.md` / `schedule-recommendations.md` |
| Daily fleet status (autonomous) | `02_Areas/Agent-Fleet/` | `daily-fleet-status-YYYY-MM-DD.md` |
| Health telemetry (synth manifest, lint, spend) | `health/` | `synth-manifest-YYYY-MM-DD.json`, `YYYY-MM-DD-lint-report.md`, `gemini-spend-YYYY-MM.json` |
| Deep-research output (overnight queue) | `20_projects/research/` | `YYYY-MM-DD-<topic-slug>.md` |

### What must I never do?

1. Never delete vault files without explicit user permission.
2. Never use nested objects in frontmatter — flat YAML only (Dataview will break).
3. Never re-enable Obsidian-Git auto-commit / auto-pull / auto-push (issue #22, 2026-04-23: shell-level hook is sole owner).
4. Never write to `60_archive/` (read-only; archived items are done).
5. Never push to git from inside Claude Code — Obsidian-Git plugin or manual commits only.
6. Never invent paths for `vault/knowledge/` — those files are LLM-written by `vault_synthesizer`, never hand-written.
7. Never skip the kebab-case + type-prefix naming rule (`ref-`, `idea-`, `mtg-`, `prj-`, `tpl-`, `moc-`).

### What's the YAML frontmatter shape?

```yaml
---
type: reference          # one of: project, reference, idea, daily, weekly, meeting, moc, dashboard, archive
domain:                  # list, never nested object
  - claude-mastery       # one of 6 domains (see below)
status: active           # backlog | draft | active | blocked | review | completed | archived
context: 16bitfit        # OPTIONAL short identifier
ai-context: "One-sentence summary under 120 chars."
created: 2026-05-06
source: apple-notes-import   # OPTIONAL provenance
---
```

The 6 domains are: `claude-mastery`, `product-management`, `creative-studio`, `life-systems`, `design-team`, `vault`.
(This is the **vault frontmatter taxonomy** — distinct from the 3 repo workspace domains documented in `/CLAUDE.md`: `the-block/`, `creative-studio/`, `life-systems/`.)

### How do I find existing content?

1. **MOC first:** read `vault/05_atlas/moc-<domain>.md` to see what exists in a domain.
2. **Knowledge index:** read `vault/knowledge/index.md` for synthesized concepts and connections (auto-generated nightly).
3. **SQLite chunks:** the `.vault-index.db` SQLite file at the vault root has `chunks` and `concept_edges` tables — query directly only if you're an SDK agent. Claude Code agents should use Grep/Glob.
4. **Grep for backlinks:** `Grep "\[\[concept-name\]\]" --path vault/`.
5. **Frontmatter filter:** `Grep "status: active" --path vault/20_projects/`.

### How do I write into a daily note?

Use the **PATCH pattern** with HTML comment anchors. Today's daily note has 6 anchors (in template order):

```
<!-- slack-overnight -->
<!-- meetings -->
<!-- jira-log -->
<!-- claude-sessions -->
<!-- side-projects -->
<!-- research-digest -->
```

Insert content on the line **directly below** the anchor. Never remove the anchor. Never rewrite the whole file.

## Table of Contents

- [Quick Reference for AI Agents](#quick-reference-for-ai-agents)
- [Architecture](#architecture)
- [Folder-by-Folder Reference](#folder-by-folder-reference)
- [YAML Frontmatter Schema](#yaml-frontmatter-schema)
- [Naming Conventions](#naming-conventions)
- [Templates](#templates)
- [Maps of Content (MOCs)](#maps-of-content-mocs)
- [Operating Models](#operating-models)
- [Knowledge Loop Infrastructure](#knowledge-loop-infrastructure)
- [Health Telemetry](#health-telemetry)
- [Agent Fleet Workspace](#agent-fleet-workspace)
- [Obsidian Plugins](#obsidian-plugins)
- [Claude Code Integration](#claude-code-integration)
- [SDK Agents That Touch the Vault](#sdk-agents-that-touch-the-vault)
- [How to Read from the Vault](#how-to-read-from-the-vault)
- [How to Write to the Vault](#how-to-write-to-the-vault)
- [Inbox Processing](#inbox-processing)
- [Knowledge Graph Navigation](#knowledge-graph-navigation)
- [Semantic Search](#semantic-search)
- [Daily Workflow](#daily-workflow)
- [Granola Meeting Sync](#granola-meeting-sync)
- [Content Statistics](#content-statistics)
- [Rules and Constraints](#rules-and-constraints)
- [Appendix: Related Files Outside the Vault](#appendix-related-files-outside-the-vault)
- [Changelog](#changelog)

## Architecture

```text
vault/
├── Home.md                           # Dataview dashboard — entry point
├── Sean-Winslow-Full-Personal-Context-v2.0.md   # Tier-0 identity (above all operating models)
│
├── 00_inbox/                         # Raw captures, quick ideas, needs-review items
│   ├── research-queue.md             # Topics queued for nightly deep_researcher
│   └── gemini-research-queue.md      # Topics queued for gemini-researcher (opt-in)
│
├── 02_Areas/                         # Ongoing areas (PARA "Areas") — NEW since 2026-04
│   ├── Agent-Fleet/                  # Autonomous-agent telemetry surfaced into vault
│   │   ├── fleet-state.md            # Latest fleet snapshot (overwritten daily)
│   │   └── daily-fleet-status-YYYY-MM-DD.md   # Per-day fleet summaries
│   └── Work/                         # Misc PR digests, ad-hoc work artifacts
│
├── 05_atlas/                         # MOCs (Maps of Content) + operating models
│   ├── moc-claude-mastery.md
│   ├── moc-product-management.md
│   ├── moc-creative-studio.md
│   ├── moc-life-systems.md
│   ├── moc-design-team.md
│   ├── moc-vault.md
│   └── operating-models/             # NEW — 5-artifact bundles per domain (see "Operating Models")
│       ├── README.md
│       ├── INTERVIEW-PLAYBOOK.md
│       ├── creative-studio/          # HEARTBEAT, USER, SOUL, operating-model, schedule-recommendations
│       ├── life-systems/             #   "
│       └── job-hunt-2026/            #   " (replaces the-block bundle, archived 2026-05)
│
├── 10_timeline/
│   ├── daily/                        # YYYY-MM-DD.md
│   ├── weekly/                       # YYYY-Www.md
│   └── monthly/                      # YYYY-MM.md
│
├── 20_projects/                      # Active, time-bound projects
│   ├── prj-job-hunt-2026/            # NEW — 8-week post-Block search (added 2026-05-04)
│   │   ├── README.md
│   │   ├── The-Block-Contacts-After-Layoff.md
│   │   └── onwards-and-upwards-5-4-26/   # Migration + master plan + audit
│   ├── prj-code-brain/           # This repo's active development
│   ├── prj-16bitfit/                 # Game project (most content moved to creative-studio/16bitfit-battle-mode/)
│   ├── prj-campus-201/               # Campus LMS (mostly archived after Block layoff)
│   ├── prj-boston-move/              # Boston relocation
│   ├── prj-personal-finance/         # Personal finance automation
│   ├── prj-animation-pipeline/       # Animation pipeline
│   ├── prj-sw-portfolio-and-hubs-designs/   # NEW — portfolio site
│   └── research/                     # NEW — overnight deep_researcher output
│
├── 30_domains/                       # Domain workspace folders
│   ├── claude-mastery/               # (mostly empty — domain-level reference notes)
│   ├── product-management/
│   │   ├── the-block-meetings-granola-notes/   # Granola plugin landing zone (auto-sync)
│   │   ├── prompts/
│   │   └── media-team-ideas/
│   ├── creative-studio/
│   ├── design-team/
│   ├── life-systems/
│   └── vault/
│
├── 40_knowledge/                     # Permanent reference material
│   ├── concepts/                     # Hand-written ideas, frameworks
│   ├── references/                   # How-tos, guides, docs
│   └── notebooklm-exports/           # Synthesized research from NotebookLM
│
├── 50_sources/                       # Raw data and assets
│   ├── data/
│   ├── finance/                      # CSVs gitignored
│   ├── health/                       # NEW — workout/health CSVs
│   └── assets/
│
├── 60_archive/                       # Completed/inactive items (READ-ONLY)
│   ├── apple-notes-personal/         # 5 sentimental items (was 52; collapsed 2026-04)
│   ├── inbox-archive-2026-04-25/     # NEW — inbox cleanup snapshot
│   ├── operating-models-the-block-2026-05/   # NEW — Block bundle archived after layoff
│   ├── old-mocs/                     # Superseded MOC drafts
│   ├── old-projects/                 # Superseded project folders
│   ├── old-prompts/
│   ├── old-rag/
│   └── old-templates/
│   #  Note: apple-notes-empty/expired/nyl/duplicates/prompts subfolders from the Phase 2/3 import were removed in the 2026-04 cleanup. The classification rubric reference at 40_knowledge/references/ref-apple-notes-classification-rubric.md preserves the historical methodology.
│
├── 70_apple-notes/                   # Import staging (effectively empty; attachments folder kept)
│   └── Notes/
│       ├── attachments/
│       └── images/
│
├── 90_system/                        # Vault infrastructure
│   ├── VAULT-GUIDE.md                # ← this file
│   ├── templates/                    # tpl-daily, tpl-weekly, tpl-project, tpl-meeting, tpl-idea, tpl-knowledge
│   ├── scripts/                      # process-granola-notes.py
│   ├── agent-logs/                   # NEW — SDK-agent run logs + agent-run-history.csv
│   ├── css-snippets/
│   └── mcp-configs/                  # (currently empty)
│
├── Excalidraw/                       # NEW — Excalidraw plugin storage
│
├── health/                           # NEW — vault telemetry (NOT to be confused with 50_sources/health/)
│   ├── synth-manifest-YYYY-MM-DD.json   # Per-run synthesizer counts
│   ├── YYYY-MM-DD-lint-report.md     # Weekly knowledge_lint output
│   ├── gemini-spend-YYYY-MM.json     # Gemini DR/DR-Max spend ledger ($7 task / $10 day / $20 month caps)
│   ├── .gemini-ledger.lock           # FileLock for spend ledger
│   └── .lock                         # FileLock for synth runs
│
├── knowledge/                        # NEW — knowledge-loop output (LLM-written, never hand-edited)
│   ├── index.md                      # Auto-generated index (loaded on SessionStart by hook)
│   ├── concepts/                     # One file per synthesized concept
│   ├── connections/                  # One file per synthesized connection
│   └── qa/                           # NEW (v3.19.0) — terminal Q&A answer endpoints (cite outward only)
│
├── .vault-index.db                   # SQLite index (chunks + concept_edges tables) — written by vault_indexer
├── .indexer-state.json               # Mtime cursor for vault_indexer
└── .obsidian/                        # Obsidian app config
```

### Why this structure

- **Numbered prefixes** (`00_`, `02_`, `05_`, `10_`...) control sidebar sort order in Obsidian.
- **`02_Areas/`** is PARA's "Areas" tier — ongoing responsibilities that aren't time-bound projects.
- **`05_atlas/operating-models/`** sits inside the atlas because operating-model bundles are *navigational meta* — they describe *how* Sean works, just like MOCs describe *what* lives in a domain.
- **`vault/knowledge/`** is the LLM-output zone. Hand-written knowledge lives in `40_knowledge/`; synthesized knowledge lives in `vault/knowledge/`. They never mix.
- **`vault/health/`** is operational telemetry — separate from `50_sources/health/`, which is Sean's actual fitness/wellness data.
- **The unnumbered top-level dirs** (`Excalidraw/`, `health/`, `knowledge/`, plus the Tier-0 context file) sit outside the numbered hierarchy because they were added later and didn't fit cleanly. This is a known asymmetry; do not "fix" it without a project-level decision.

## Folder-by-Folder Reference

Counts as of 2026-05-06 (refresh this table any time the guide is rewritten):

| Folder | Files | Purpose | Who writes here |
|---|---:|---|---|
| `00_inbox/` | 2 | Raw captures + research queues | Humans, Zapier captures, agents queueing research |
| `02_Areas/Agent-Fleet/` | ~19 | Daily fleet snapshots | `meta_agent` (autonomous, 8:35 AM daily) |
| `02_Areas/Work/` | 1 | Ad-hoc work artifacts | Humans |
| `05_atlas/` (root) | 6 | MOCs (one per domain) | Humans, occasional agent updates |
| `05_atlas/operating-models/` | 17 | 5-artifact bundles + index | `work-operating-model` skill (Sean-driven interview) |
| `10_timeline/daily/` | ~60 | Daily notes | `daily-note-appender` hook (auto), `daily_driver` agent (morning), humans |
| `10_timeline/weekly/` | ~3 | Weekly reviews | Humans, deprecated `daily_driver` weekly mode |
| `20_projects/` | 53 | Active projects | Humans + project-specific agents |
| `30_domains/` | 317 | Domain workspaces (heaviest is Granola meeting notes) | Humans, Granola plugin |
| `40_knowledge/concepts/` | small | Hand-written concepts | Humans |
| `40_knowledge/references/` | majority of 81 | Hand-written references | Humans, `process-inbox` skill (manual triage) |
| `40_knowledge/notebooklm-exports/` | small | NotebookLM synthesis dumps | Humans (manual export) |
| `50_sources/data/` | small | Lists, raw data | Humans |
| `50_sources/finance/` | 0 .md (CSVs gitignored) | Bank/credit-card exports | Humans (manual import) |
| `50_sources/health/` | small | Workout / fitness CSVs | Humans (manual import), `health-habits` skill |
| `50_sources/assets/` | n/a (binaries) | Images, sprites | Humans (Obsidian attachment default) |
| `60_archive/` (READ-ONLY) | 24 | Done items | Nobody. Treat as immutable. |
| `70_apple-notes/` | 1 | Vestigial import staging | Nobody (kept for attachment paths only) |
| `90_system/templates/` | 6 | Templater templates | Humans (rare); auto-applied by Obsidian |
| `90_system/scripts/` | 1 | `process-granola-notes.py` post-processor | Humans (cron / manual) |
| `90_system/agent-logs/` | n/a (logs) | SDK-agent run logs + `agent-run-history.csv` | All SDK agents (write-only from agent side) |
| `Excalidraw/` | 1 | Excalidraw drawings | Excalidraw plugin |
| `health/` | n/a (json + .md reports) | Vault telemetry | `vault_synthesizer`, `knowledge_lint`, `gemini_dr.run` |
| `knowledge/` | 1 (index.md) + concepts/ + connections/ + qa/ | Synthesized knowledge | `vault_synthesizer` (concepts, connections), `query.py --file-back` (qa) |
| **Total .md files** | **~608** | (was 1,431 in Feb 2026 — Apple Notes archive collapse + content consolidation) | |

## YAML Frontmatter Schema

**CRITICAL RULE: Flat YAML only.** Never use nested objects in frontmatter. Dataview queries will break.

### Standard Fields

```yaml
---
type: reference              # REQUIRED: See type values below
domain:                      # REQUIRED: List format (not nested object)
  - creative-studio
  - product-management
status: active               # REQUIRED: See status values below
context: 16bitfit            # OPTIONAL: Short project/topic identifier
ai-context: "One-sentence summary for AI retrieval and Dataview display."
created: 2026-02-20          # REQUIRED: ISO date
source: apple-notes-import   # OPTIONAL: Where the content came from
---
```

### Type Values

| Value | Description | Typical Location |
|-------|-------------|------------------|
| `project` | Active project material | `20_projects/prj-*/` |
| `reference` | Reusable knowledge, how-tos, guides | `40_knowledge/references/` |
| `idea` | Concepts worth exploring | `40_knowledge/concepts/` or `00_inbox/` |
| `daily` | Daily notes | `10_timeline/daily/` |
| `weekly` | Weekly reviews | `10_timeline/weekly/` |
| `meeting` | Meeting notes | Domain folder or daily note |
| `moc` | Map of Content index | `05_atlas/` |
| `dashboard` | Dataview-powered overview | `Home.md` |
| `archive` | Completed/inactive items | `60_archive/` |

### Status Values

| Value | Meaning |
|-------|---------|
| `backlog` | Not started |
| `draft` | Initial content, needs work |
| `active` | In use, regularly referenced |
| `blocked` | Stalled, needs attention |
| `review` | Content complete, needs validation |
| `completed` | Done, may move to archive |
| `archived` | No longer active |

### Domain Values (exactly 6)

```
claude-mastery
product-management
creative-studio
life-systems
design-team
vault
```

These map directly to the 6 domain workspaces in the parent `claude-code-superuser-pack` repository and the MOCs in `05_atlas/`.

### The `ai-context` Field

A single sentence (under 120 characters) that summarizes the note's content. This field is the most important for AI workflows because:
- It provides instant context without reading the full note
- It appears in Dataview table queries on the Home dashboard
- It enables filtered retrieval: "find notes where ai-context contains 'animation'"
- It should be a proper sentence starting with a capital letter and ending with a period

### Per-Type Field Requirements

| Type | Required | Optional |
|------|----------|----------|
| `daily` | type, date | energy-peak, mood |
| `weekly` | type, week, date-start, date-end | |
| `project` | type, domain, status, context, ai-context, created | energy-level, review-date |
| `meeting` | type, date, domain, attendees, context | `granola_id`, `granola_type`, `transcript` (when from Granola sync) |
| `reference` | type, domain, status, ai-context, created | source |
| `idea` | type, domain, status, ai-context, created | energy-level |
| `moc` | type, domain | |

## Naming Conventions

| Scope | Convention | Example |
|-------|-----------|---------|
| Top-level folders | `NN_name` (numbered, underscores) | `00_inbox`, `10_timeline` |
| Everything inside folders | kebab-case | `prj-16bitfit`, `moc-creative-studio` |
| Daily notes | ISO date as filename | `2026-02-20.md` |
| Weekly notes | ISO week | `2026-W08.md` |
| Templates | `tpl-` prefix | `tpl-daily.md` |
| MOCs | `moc-` prefix | `moc-claude-mastery.md` |
| Projects | `prj-` prefix | `prj-boston-move.md` |
| References/Knowledge | `ref-` prefix | `ref-api-rate-limits.md` |
| Ideas | `idea-` prefix | `idea-gamified-onboarding.md` |
| Meetings | `mtg-` prefix | `mtg-2026-02-20-standup.md` |

### Filename Rules

1. Lowercase everything
2. Replace spaces and underscores with hyphens
3. Remove emoji, special punctuation, and Unicode characters
4. Strip leading `#`, `-`, `.`, `$`, `@`
5. Truncate to 60 characters (before `.md` extension)
6. If a collision exists, append `-2`, `-3`, etc.

## Templates

Templates live in `vault/90_system/templates/` and are auto-applied by the Templater plugin when creating notes in specific folders.

### Template-to-Folder Mapping

| Template | Auto-Applied In | Description |
|----------|----------------|-------------|
| `tpl-daily.md` | `10_timeline/daily/` | Daily note with focus, tasks, sessions, reflection |
| `tpl-weekly.md` | `10_timeline/weekly/` | Weekly review with Dataview task aggregation |
| `tpl-project.md` | `20_projects/` | Project dashboard with status, decisions, links |
| `tpl-meeting.md` | (manual) | Meeting notes with agenda, action items, decisions |
| `tpl-idea.md` | (manual) | Idea capture with context and next steps |
| `tpl-knowledge.md` | (manual) | Reference material with summary and connections |

### HTML Comment Anchors

Templates include invisible anchors for programmatic content injection:

```markdown
<!-- anchor-name -->
```

Claude Code injects content **below** the anchor using Edit or sed, leaving the comment in place for future writes. This enables PATCH-style updates instead of full-file rewrites.

**Anchors by template:**

| Template | Anchors |
|----------|---------|
| `tpl-daily` | `<!-- slack-overnight -->`, `<!-- meetings -->`, `<!-- jira-log -->`, `<!-- claude-sessions -->`, `<!-- side-projects -->`, `<!-- research-digest -->` |
| `tpl-weekly` | `<!-- auto-wins -->`, `<!-- auto-blockers -->`, `<!-- auto-decisions -->` |
| `tpl-project` | `<!-- status-update -->`, `<!-- git-commits -->` |

**Example — Querying daily-note Claude Code sessions:**

```dataview
TABLE time, domain, context, tag
FROM "10_timeline/daily"
WHERE domain = "claude-mastery" AND tag = "pre-compact"
```

(The `tag` field was added to session entries in v3.18.0 to distinguish `session-end` / `pre-compact` / `manual` triggers.)

## Maps of Content (MOCs)

Six MOCs in `vault/05_atlas/` provide domain-level navigation using auto-populating Dataview queries. Each MOC:

1. Lists **active projects** in that domain (from `20_projects/` where `domain` contains the MOC's domain)
2. Lists **knowledge base** entries (from `40_knowledge/` matching the domain)
3. Lists **recent daily mentions** (daily notes that link to the MOC)

MOCs are the recommended starting point for AI context-gathering. Instead of searching the entire vault, read a MOC first to understand what exists in a domain, then follow specific links.

### Home Dashboard (`Home.md`)

The vault opens to `Home.md`, which uses Dataview queries to show:
- Active projects across all domains
- Today's daily note
- This week's completed tasks
- Quick links to all 6 domain MOCs
- Blocked projects (if any)

## Operating Models

The `vault/05_atlas/operating-models/` directory holds **five-artifact bundles** per domain that capture how Sean actually works. Downstream SDK agents (`daily_driver`, `meta_agent`, `flush`, `knowledge_lint`) load these on-demand to act with real context instead of generic boilerplate.

### The five artifacts per domain

| File | Captures | Layer |
|---|---|---|
| `HEARTBEAT.md` | Operating rhythms (daily / weekly / monthly) | 1 |
| `USER.md` | Recurring decisions and prioritization criteria | 2 |
| `SOUL.md` | Dependencies (Part A) + institutional knowledge (Part B) | 3+4 |
| `operating-model.md` | Synthesized one-file profile | (synthesis) |
| `schedule-recommendations.md` | Friction-derived calendar/automation rules | 5 |

### Active bundles (2026-05-06)

| Domain | Status | Notes |
|---|---|---|
| `creative-studio/` | confirmed | 16BitFit, Remotion, art, writing |
| `life-systems/` | confirmed | Finance, health, learning, time, career |
| `job-hunt-2026/` | confirmed | 8-week post-Block search; AI/Tech/Creative PM. Tier-A truths + relocation overrides + agent-message boundary rule live |
| `the-block/` | **archived 2026-05** | Moved to `vault/60_archive/operating-models-the-block-2026-05/` after Sean's layoff. Not loaded by active agents. |

### Tier-0 identity

Sits above all three domain bundles: `Sean-Winslow-Full-Personal-Context-v2.0.md` (vault root). Bumped from v1.1 on 2026-05-02 (interview-driven refresh). All operating-model artifacts cross-reference this file.

### Producing artifacts

Run the `work-operating-model` skill:

> "Run the work-operating-model interview for `<domain>`."

The skill walks the 5-layer interview (`/.claude/skills/work-operating-model/interview-questions.md`) and writes outputs to the matching subfolder. Artifacts progress through statuses: `awaiting-interview` → `draft` → `confirmed`.

### Consuming artifacts (agent contracts)

Loaded via `agents-sdk/lib/artifact_loader.py` with mtime-keyed caching. Controlled by `[artifacts]` in `agents-sdk/config.toml`; instant rollback = `enabled = false`.

| Agent | Loads | Purpose |
|---|---|---|
| `daily_driver` (morning) | All 3 HEARTBEATs in preamble; on-demand Read pointers for USER / SOUL / operating-model / schedule-recommendations | Phase 1 wiring (v3.16.0) |
| `meta_agent` | All 3 `schedule-recommendations.md` bodies | Domain-aware insights ranking against Protect/Automate/Decline lists (Phase 2 wiring, v3.17.0) |
| `flush.py` | All 3 SOULs prepended to `EXTRACTION_PROMPT` | Cross-reference new entries against Tier-A items |
| `knowledge_lint.py` | 3-domain SOUL context block in Tier-2 prompt | Adds `soul-tier-a-conflict` lint issue at HIGH severity |

**Phase 3 was closed 2026-04-27.** `meeting_defender` was deleted (Daily Driver morning already covers calendar surfacing); `sprint_health` autonomous wiring was superseded by the new `sprint-health` skill (interactive Atlassian MCP, no headless-MCP gymnastics).

### Reading order for new agents

1. Tier-0: `Sean-Winslow-Full-Personal-Context-v2.0.md` (always, as preamble)
2. Domain HEARTBEAT(s) for the active task
3. Domain USER if the task involves prioritization or trade-off decisions
4. Domain SOUL for dependency-aware or knowledge-gap-aware reasoning
5. Domain `schedule-recommendations.md` only when scheduling or recommending automation

Do not load all 5 artifacts for every task — `artifact_loader` is on-demand by design.

## Knowledge Loop Infrastructure

The vault has a **producer/consumer knowledge loop** that compounds insight over time. The producer side runs nightly; the consumer side runs on every Claude Code session start. All components are local-first (Mac Mini Ollama + intermittently MBP Qwen3-14B). No cloud egress unless Sean opts into Gemini DR.

### Producers (write to `vault/knowledge/`, `vault/.vault-index.db`, `vault/health/`)

```text
SessionEnd flush  ──►  Vault Indexer  ──►  Vault Synthesizer  ──►  Knowledge Lint
(hook-triggered)      (2:00 AM daily)    (2:30 AM daily)         (Sun 22:00 weekly)
```

| Producer | Schedule | Output |
|---|---|---|
| `flush.py` | SessionEnd hook + PreCompact hook (v3.18.0+) | Daily-log session blocks; tag is `session-end` / `pre-compact` / `manual` (v3.18.0 added the trigger field) |
| `vault_indexer.py` | 2:00 AM daily (launchd, Mac Mini) | `vault/.vault-index.db` (`chunks` + `concept_edges` tables); `vault/.indexer-state.json` mtime cursor |
| `vault_synthesizer.py` | 2:30 AM daily (launchd, MBP if awake) | `vault/knowledge/concepts/<slug>.md`, `vault/knowledge/connections/<slug>.md`, `vault/knowledge/index.md`, `vault/health/synth-manifest-YYYY-MM-DD.json`, `concept_edges` rows (Phase D, v3.20.0) |
| `knowledge_lint.py` | Sunday 22:00 (launchd) | `vault/health/YYYY-MM-DD-lint-report.md` |
| `query.py --file-back` | Manual (terminal Q&A) | `vault/knowledge/qa/<slug>.md` + append to `vault/knowledge/qa/.manifest.json` (Phase C, v3.19.0) |

### Consumers (read `vault/knowledge/index.md` and friends)

| Consumer | Trigger | What it reads |
|---|---|---|
| `session-start-inject-index.sh` hook | New Claude Code session | `vault/knowledge/index.md` injected as `additionalContext` (≤15,000 chars, 5s timeout) |
| Any agent doing context-gathering | Manual | The index pointers, then the cited concept/connection/qa articles |
| `vault_synthesizer.py` itself | Each run | Reads its own prior outputs to detect supersedence |

### The SQLite layer

`vault/.vault-index.db` has two tables:

| Table | Schema highlights | Written by | Read by |
|---|---|---|---|
| `chunks` | `(file_path, chunk_index, chunk_text, embedding, file_mtime, indexed_at)` with `UNIQUE(file_path, chunk_index)` | `vault_indexer` | `query.py`, `vault_synthesizer` |
| `concept_edges` | `(from_slug, to_slug, relation, confidence, valid_until, classifier_version, source_synth_run, created_at)` with relation in `{supports, contradicts, evolved_into, supersedes, depends_on, related_to}` | `vault_synthesizer` (Phase D) | `knowledge_lint` (SQL fast path for contradictions) |

Taxonomy mirrors OB1's `schemas/typed-reasoning-edges/schema.sql`; SQLite-local. Bad relation values are logged + dropped via `agents-sdk/lib/concept_edges.py:insert_edge` (raises `ValueError` so the article still writes). LLM contradictions and SQL contradictions are deduped by normalized `frozenset({from_slug, to_slug})`; SQL hits win when both surface the same pair.

### The qa/ tier (v3.19.0)

`agents-sdk/scripts/query.py` adds terminal Q&A with two-pass orchestration:

1. **Selection pass:** picks 3-N article paths with similarity scores from `chunks` table.
2. **Answer pass:** reads the selected bodies and emits a `[[wikilink]]`-citing answer.

`--file-back` persists answers as a third article tier at `vault/knowledge/qa/<slug>.md`. The qa frontmatter cites each consulted article with a 12-char SHA-256 chunk_id over `(file_path, chunk_index)` from the `chunks` table plus the selection-pass similarity score — gives the synthesizer a cheap "did this specific chunk change?" check on the next nightly run.

`knowledge_lint._ORPHAN_EXCLUDE_DIRS` includes `qa` because qa/ articles are answer endpoints (cite outward, never receive inbound wikilinks).

### Current state (2026-05-06)

- `vault/knowledge/index.md`: 141 bytes ("_(none yet)_" placeholders).
- `vault/knowledge/concepts/` and `vault/knowledge/connections/`: empty — synthesizer has not produced articles yet (MBP must be awake at 2:30 AM for synthesis to succeed; v3.14.3 retired the WOL escalation).
- Latest synth manifest (`synth-manifest-2026-05-06.json`): `concepts_written: 0, connections_written: 0, status: "partial"` (files_processed: 30, duration: 2720s).
- The producer pipeline runs nightly; the consumer pipeline (SessionStart hook injection) is wired and waiting for content.

### Rollback procedures

| Phase | Rollback |
|---|---|
| Phase B (consumer hook) | Remove `SessionStart` block from `.claude/settings.json` |
| Phase C (qa tier) | Delete `agents-sdk/scripts/query.py` + revert qa/ entries in `regenerate_index` and `_ORPHAN_EXCLUDE_DIRS` |
| Phase D (typed edges) | `DROP TABLE concept_edges` + revert four MODIFY files; LLM still writes connection articles unchanged because `relations` is OPTIONAL in the prompt schema |

## Health Telemetry

`vault/health/` is the operational telemetry directory for vault-touching agents. **Not to be confused with `vault/50_sources/health/`**, which holds Sean's actual fitness/wellness data.

| File pattern | Producer | Purpose | Consumer |
|---|---|---|---|
| `synth-manifest-YYYY-MM-DD.json` | `vault_synthesizer.py` | Per-run counts (concepts, connections, edges, rejected, duration, model, wol_status) | `daily_driver` morning brief surfaces under "Vault Health" |
| `YYYY-MM-DD-lint-report.md` | `knowledge_lint.py` (Sunday 22:00) | Tier-1 structural + Tier-2 LLM lint findings | Humans (review weekly); future `knowledge_lint` runs (dedupe) |
| `gemini-spend-YYYY-MM.json` | `agents-sdk/scripts/gemini_dr.py` | Monthly Gemini DR / DR-Max spend ledger | `gemini_dr.run` (enforces $7 task / $10 day / $20 month caps) |
| `.gemini-ledger.lock` | `gemini_dr.py` | FileLock for spend ledger | (lock-only) |
| `.lock` | `vault_synthesizer.py` | FileLock for synth runs | (lock-only) |

### synth-manifest schema

```json
{
  "concepts_written": 0,
  "connections_written": 0,
  "duration_seconds": 2720.17,
  "edges_rejected": 0,
  "edges_written": 0,
  "files_processed": 30,
  "model_used": "",
  "rejected_count": 0,
  "run_id": "2026-05-06T02:30:03",
  "status": "partial",
  "wol_status": ""
}
```

`status` values: `success`, `partial`, `error`, `skipped`. An empty `model_used` (as in the live 2026-05-06 manifest above) means the synthesizer ran but never engaged the LLM — typically because the MBP wasn't awake when the run fired (WOL was retired in v3.14.3, so MBP-hosted Qwen3-14B is best-effort). Empty `wol_status` is consistent with that retirement.

### gemini-spend ledger schema

A single JSON array (NOT JSONL) of run records, one object per Gemini DR / DR-Max invocation. Each record carries `interaction_id`, `agent_id`, `tier` (`dr` | `dr_max`), `cost_predicted_usd`, `cost_actual_usd`, `cost_usd`, `wall_seconds`, the full `query`, `created` timestamp, and `output_path` to the saved research artifact under `vault/20_projects/research/`. `gemini_dr.run` reads the array, sums `cost_usd` for the current day / month, and refuses to start a new run if the $7 task / $10 day / $20 month caps would be breached.

## Agent Fleet Workspace

`vault/02_Areas/Agent-Fleet/` surfaces autonomous-agent telemetry into the vault so Sean can browse fleet health from Obsidian without leaving the editor.

| File | Producer | Cadence | Contents |
|---|---|---|---|
| `fleet-state.md` | `meta_agent` | 8:35 AM daily (overwritten) | Latest snapshot of all 7 active SDK agents — last run timestamp, exit code, cost, status |
| `daily-fleet-status-YYYY-MM-DD.md` | `meta_agent` | 8:35 AM daily (append) | Per-day fleet summary; gemma4:e4b on Mac Mini generates a "Domain-Aware Insights" section ranking activity against schedule-recommendations Protect/Automate/Decline lists |

These files are **read-only from Claude Code's perspective** — only `meta_agent` writes here. Edit them only to fix typos in Sean's manual annotations.

`vault/02_Areas/Work/` is a sibling area for ad-hoc work artifacts (e.g., `pr-digest-2026-04-08.md`). Manual humans only.

## Obsidian Plugins

11 community plugins are installed:

| Plugin | Purpose | Key Config |
|--------|---------|------------|
| **Dataview** | Query engine for MOCs and dashboards | DQL + DataviewJS enabled, inline fields enabled |
| **Templater** | Smart note templates with dynamic content | Folder-template mapping, `tp.*` functions |
| **Obsidian Git** | Manual commits + status bar | **All auto-features OFF** (issue #22, 2026-04-23). `autoSaveInterval: 0`, `autoPushInterval: 0`, `autoPullInterval: 0`. Shell-level hook is sole owner of vault git ops. |
| **Obsidian Linter** | Markdown formatting and YAML automation | Auto-adds `created`/`updated` timestamps, auto-adds title from H1, ignores `70_apple-notes/` and `60_archive/` |
| **Local REST API** | MCP server endpoint for AI access | HTTPS on port 27124, self-signed SSL |
| **Remotely Save** | Cloud sync (encrypted config) | Encrypted credentials |
| **Homepage** | Opens vault to Home.md | Set to `Home` note |
| **Granola Sync** | Syncs meeting notes + transcripts from Granola | Individual files, `linkFromDailyNotes: true`, landing at `30_domains/product-management/the-block-meetings-granola-notes/`. Desktop only. |
| **Calendar** | NEW — Sidebar calendar widget | Standard config |
| **Excalidraw** | NEW — Hand-drawn diagrams stored at `Excalidraw/` | Standard config |
| **Image Converter** | NEW — Auto-convert pasted images (PNG → WebP, etc.) | Standard config |

### Obsidian app settings

| Setting | Value | Why |
|---|---|---|
| New file location | `00_inbox/` folder | All new captures go to inbox first |
| Attachment folder | `50_sources/assets/` | Centralized asset storage |
| Auto-update links | Enabled | Links survive file renames |
| Daily notes folder | `10_timeline/daily/` | ISO date format (YYYY-MM-DD) |

## Claude Code Integration

Six channels connect Claude Code to the vault:

### Channel 1: Direct filesystem access

Read, Write, Edit, Grep, Glob operate directly on vault files. The vault is just a directory of markdown files — no special API needed. Examples:

```text
Read "vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md"
Grep "operating-model" --path vault/
Glob "vault/20_projects/**/*.md"
Grep "\[\[Sean-Winslow-Full-Personal-Context-v2.0\]\]" --path vault/
```

### Channel 2: MCP server (Obsidian Local REST API)

The Local REST API plugin exposes vault operations over HTTPS on port 27124. The `mcp-obsidian` MCP server translates these into tools: `read_note`, `write_note`, `patch_note`, `move_note`, `delete_note`, `search_notes`, `list_directory`, `read_multiple_notes`, `update_frontmatter`, `get_frontmatter`, `manage_tags`, `get_vault_stats`.

Use MCP for: PATCH operations, frontmatter extraction, tag management.
Use direct filesystem for: bulk operations, when speed matters, when Obsidian isn't running.

### Channel 3: Native MCP integrations (preferred over Zapier)

As of 2026-03-01, native MCPs replaced Zapier for most services. **Always use native first.**

| Service | Native MCP | Zapier fallback |
|---|---|---|
| Google Calendar | `claude.ai Google Calendar` / `google-workspace` | `google_calendar_*` |
| Gmail | `claude.ai Gmail` / `google-workspace` | `gmail_*` |
| Google Sheets/Docs/Drive | `google-workspace` | `google_sheets_*`, `google_docs_*` |
| Jira + Confluence | `mcp-atlassian` / `claude.ai Atlassian` | `jira_software_cloud_*` |
| Slack | Slack plugin (pending Block admin approval; **The Block layoff 2026-05 means this may be moot**) | `slack_*` |
| GitHub | `github` MCP (Docker) | n/a |
| Granola | `claude.ai Granola` | n/a |
| NotebookLM | `notebooklm-mcp` | n/a |
| Figma | `claude.ai Figma` | n/a |

**Calendar rule (post-2026-05-04):** single calendar — `sean.winslow28@gmail.com`. The Block work calendar (`swinslow@theblock.co`) was archived after Sean's layoff; do NOT query it.

**Still Zapier-only:** Salesforce, GA4, Webhooks, code execution.

### Channel 4: Hooks (automatic)

5 of the 13 hooks touch the vault. See [SDK Agents That Touch the Vault](#sdk-agents-that-touch-the-vault) for the hook table.

### Channel 5: Skills (on-demand)

7 vault-specific skills in `.claude/skills/`. See Appendix below.

### Channel 6: SDK Agents (autonomous)

7 active SDK agents, scheduled via launchd. See [SDK Agents That Touch the Vault](#sdk-agents-that-touch-the-vault).

## SDK Agents That Touch the Vault

The `agents-sdk/` directory in the parent repo runs 14 autonomous agents on macOS launchd schedules; **7 are active**. This section covers only the vault-touching subset and what they read/write. For full agent details, schedules, and cost caps, see `/CLAUDE.md` "Agents SDK" section.

### Read/Write contract by agent

| Agent | Reads | Writes |
|---|---|---|
| `vault_indexer` | All vault `.md` files | `vault/.vault-index.db` (chunks + concept_edges schema), `vault/.indexer-state.json` |
| `vault_synthesizer` | `vault/.vault-index.db` chunks | `vault/knowledge/concepts/`, `vault/knowledge/connections/`, `vault/knowledge/index.md`, `vault/health/synth-manifest-*.json`, `concept_edges` rows |
| `meta_agent` | `90_system/agent-logs/agent-run-history.csv`; all 3 `schedule-recommendations.md` | `02_Areas/Agent-Fleet/fleet-state.md`, `02_Areas/Agent-Fleet/daily-fleet-status-*.md` |
| `daily_driver` (morning) | All 3 HEARTBEATs (preamble); on-demand USER/SOUL/operating-model/schedule-recommendations; latest synth-manifest | Today's daily note (creates if missing); appends to anchored sections |
| `flush.py` | Recent transcript; all 3 SOULs (extraction prompt); current daily note | Daily-log session blocks below `<!-- claude-sessions -->` |
| `knowledge_lint` | All vault `.md`; `vault/.vault-index.db` (concept_edges); 3-domain SOULs | `vault/health/YYYY-MM-DD-lint-report.md` |
| `deep_researcher` | `vault/00_inbox/research-queue.md` | `vault/20_projects/research/YYYY-MM-DD-<topic-slug>.md` |
| `gemini_researcher` (opt-in) | `vault/00_inbox/gemini-research-queue.md`; `vault/health/gemini-spend-*.json` | Research output dir TBD; updates spend ledger |
| `process_inbox` | **PAUSED 2026-04-29** — see `agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`. Manual triage via `process-inbox` skill is the working path. | (n/a, paused) |

### Hooks that touch the vault

5 of the 13 hooks in `.claude/hooks/`:

| Hook | Trigger | Vault effect |
|---|---|---|
| `daily-note-appender.sh` | Stop (session end) | Creates today's daily note; appends session entry below `<!-- claude-sessions -->` with Dataview inline fields |
| `session-end-flush.sh` | SessionEnd (richer than Stop) | Spawns `flush.py --trigger session-end`; writes daily-log session block tagged `session-end` |
| `pre-compact-flush.sh` | PreCompact (before auto-compaction) | Spawns `flush.py --trigger pre-compact`; tag distinguishes from session-end so post-hoc analysis can sort flushes |
| `session-start-inject-index.sh` | SessionStart | Reads `vault/knowledge/index.md`; injects as `additionalContext` (≤15,000 chars, 5s timeout) |
| `vault-integrity.py` | (configured in settings.json) | Read-only validation; fails with exit code 2 if frontmatter or naming rules are violated |

### Authentication boundary

**SDK agents in headless mode cannot use OAuth-based MCP servers** (Slack, Google Calendar, Gmail, Atlassian). Those require browser-based OAuth available only in interactive Claude Code sessions. The morning `daily_driver` therefore creates the daily-note skeleton with empty anchors; Slack/calendar/Gmail/Jira data is backfilled when Sean starts an interactive session.

### Vault-sync ownership rule (issue #22, 2026-04-23)

The shell-level Obsidian-Git auto-commit hook is the **sole** owner of vault git operations. Obsidian-Git plugin auto-features (autoSaveInterval, autoPushInterval, autoPullInterval) **must stay 0 on every machine**. Running two auto-commit systems against the same vault caused the v3.15.0 merge conflicts. Manual commits from the Obsidian-Git command palette are fine; auto-features must never run.

## How to Read from the Vault

### Pattern A: Direct Search

```
# Find a specific note
Read "vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md"

# Read the latest fleet snapshot
Read "vault/02_Areas/Agent-Fleet/fleet-state.md"

# Read today's synth manifest
Read "vault/health/synth-manifest-$(date +%Y-%m-%d).json"

# Keyword search across all content
Grep "battle system" --path vault/

# Find files by name pattern
Glob "vault/40_knowledge/**/*.md"

# Find backlinks to a concept
Grep "\[\[Strategic Planning\]\]" --path vault/
```

### Pattern B: MOC-First Navigation

Start with a MOC to understand what exists, then follow links:

1. Read `vault/05_atlas/moc-creative-studio.md`
2. Identify relevant linked notes from the Dataview tables
3. Read those specific notes for detailed context
4. Follow their wiki-links for deeper context (multi-hop traversal)

### Pattern C: Context Injection

Read specific notes before a task to prime context:

```
"Read vault/20_projects/prj-16bitfit/prj-16bitfit.md and
vault/05_atlas/moc-creative-studio.md. Using that context,
draft a sprint plan for the next 2 weeks."
```

### Pattern D: Frontmatter-Based Filtering

Use Grep to find notes by metadata:

```
# Find all active projects
Grep "status: active" --path vault/20_projects/

# Find all notes in a domain
Grep "creative-studio" --path vault/ --glob "*.md"

# Find notes with a specific context
Grep "context: 16bitfit" --path vault/
```

## How to Write to the Vault

> **Hard rule (issue #22, 2026-04-23):** Never push to git from Claude Code. The shell-level Obsidian-Git auto-commit hook is the **sole** owner of vault git operations. Manual commits from Obsidian's command palette are allowed; automated commits must come from the hook only.

### Creating New Notes

1. **Check for existing notes first** — search before creating
2. **Choose the correct destination folder** based on note type
3. **Apply the naming convention** — kebab-case with appropriate prefix
4. **Include flat YAML frontmatter** with all required fields
5. **Add `[[wikilinks]]`** to connect to related existing notes

### Updating Existing Notes

Use the **PATCH pattern** with HTML comment anchors:

1. Find the `<!-- anchor-name -->` comment in the file
2. Insert new content on the line directly below it
3. Leave the anchor comment in place for future writes
4. Never replace or remove the anchor

**Do not rewrite entire files** unless the content itself needs to change. Use Edit tool for targeted modifications.

### Frontmatter-Only Updates

When only metadata needs to change (e.g., updating status), use the Edit tool to modify only the frontmatter block:

```yaml
# Change status from draft to active
old: "status: draft"
new: "status: active"
```

### Multi-Source Synthesis

When creating notes from multiple sources, use this structure:

```markdown
## Source Material
- Web: [Article Title](https://example.com) - accessed 2026-02-20
- Vault: [[ref-existing-note]] - key insight about X
- Session: Claude Code research session - synthesized from 5 sources
```

## Inbox Processing

> **Status note (2026-04-29):** The `process_inbox` SDK agent is **paused**. The cloud-Sonnet path was validated as functionally working (~3 files/run) but cost-inefficient ($1.16/file vs $0/file local). A Path B rewrite to local `gemma4:e4b` is scoped at `agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`. The working alternative is **manual triage via the `process-inbox` skill in an interactive Claude Code session.**

The `00_inbox/` folder is the default landing zone for all new captures. Notes accumulate here from:
- Manual creation in Obsidian (new file default location)
- Bulk imports (Apple Notes, Zapier webhooks)
- Quick captures from Claude Code sessions
- Items that couldn't be confidently classified

### Processing Workflow

Use the `process-inbox` skill or follow this manual process:

1. **Scan** — Read all files in `vault/00_inbox/`
2. **Classify** — Determine type, domain, and destination for each
3. **Frontmatter** — Add or update YAML frontmatter
4. **Rename** — Apply kebab-case naming with type prefix
5. **Move** — Transfer to the correct destination folder
6. **Report** — Output a summary table of what was processed

### Classification Guide

| If the content is... | Type | Destination |
|---------------------|------|-------------|
| Reusable knowledge, guide, how-to | `reference` | `40_knowledge/references/` |
| Creative concept, framework, idea | `idea` | `40_knowledge/concepts/` |
| Related to a specific project | `project` | `20_projects/prj-<name>/` |
| Raw data, list, collection | `reference` | `50_sources/data/` |
| Financial record | `reference` | `50_sources/finance/` |
| Personal, sentimental, journal | `archive` | `60_archive/apple-notes-personal/` |
| Can't determine | leave as-is | `00_inbox/` with `status: needs-review` |

## Knowledge Graph Navigation

The vault's power comes from its interconnected notes via `[[wikilinks]]`. Claude Code can traverse these connections to build rich context.

### Forward Traversal

Read a note, find its wiki-links, read those notes, synthesize combined context.

### Backlink Discovery

Find all notes referencing a concept:
```
Grep "\[\[Animation Pipeline\]\]" --path vault/
```

### MOC Navigation

MOCs are curated navigation hubs. Point Claude at a MOC instead of the whole vault:
```
"Read vault/05_atlas/moc-creative-studio.md, then select
the 3 most relevant linked notes and summarize them."
```

### Multi-Hop Traversal

Build progressively deeper context:

| Depth | What Gets Read | Use Case |
|-------|---------------|----------|
| 0 | Entry note only | Quick reference |
| 1 | Entry + directly linked notes | Standard context |
| 2 | Entry + links + links-of-links | Deep research |

**Warning:** Depth-2 traversals consume significant context. Limit to 3-5 first-hop notes and 2-3 second-hop notes per branch.

## Semantic Search

The vault supports two levels of semantic search:

### Level 1: Smart Connections Plugin (In Obsidian)

The Smart Connections plugin is installed and stores embeddings in `.smart-env/`. It provides in-app "similar notes" suggestions using local embedding models (BGE-micro-v2 or nomic-embed-text). No API keys needed — everything runs on-device.

### Level 2: MCP-Based Semantic Search (For Claude Code)

Connect Smart Connections embeddings to Claude via the `smart-connections-mcp` server for meaning-based retrieval from Claude Code sessions. See the `obsidian-semantic-search` skill for setup instructions.

### Hybrid Search Strategy

| Query Type | Strategy |
|-----------|----------|
| Specific terms ("JWT auth error") | Keyword search (Grep) |
| Conceptual ("notes about productivity") | Semantic search (MCP) |
| Exploratory ("related to this note") | Vector similarity |

## Daily Workflow

### Morning

1. Open Obsidian — `Home.md` loads automatically
2. Check active projects on the dashboard
3. Open or create today's daily note (`10_timeline/daily/YYYY-MM-DD.md`)
4. Fill in the **Morning Focus** section (< 2 minutes)

### During the Day

- Dataview automatically pulls active tasks from `20_projects/`
- Work log entries can be added below `<!-- jira-log -->`
- Side project notes go below `<!-- side-projects -->`
- Claude Code sessions are auto-logged by the `daily-note-appender.sh` hook

### Evening

- Fill in the **Evening Reflection** section
- Note one win, one lesson, and one item to carry forward

### Weekly

- Create a weekly review note in `10_timeline/weekly/`
- Dataview auto-aggregates task completion from daily notes
- Review domain progress and set next week's priorities
- Check for stale notes (active status but not modified in 30+ days)

## Granola Meeting Sync

> **Post-2026-05-04 caveat:** Granola was Sean's primary meeting transcription tool at The Block. After the layoff, future meetings (job-hunt interviews, networking calls) may continue to use Granola or pivot to a different tool. The plugin and post-processor remain installed and functional.

[Granola](https://granola.ai/) is a meeting transcription app that runs on Sean's MacBook Pro during Google Meetings at The Block. The `obsidian-granola-sync` community plugin ([GitHub](https://github.com/tomelliot/obsidian-granola-sync)) automatically syncs both TLDR notes and full transcripts into the vault.

**Plugin config** (`vault/.obsidian/plugins/granola-sync/data.json`):
- `saveAsIndividualFiles: true` — each meeting gets its own file
- `linkFromDailyNotes: true` — daily notes get `[[wiki-links]]` under `## Meetings`
- `customBaseFolder: "30_domains/product-management/the-block-meetings-granola-notes"` — landing zone
- `transcriptHandling: "same-location"` — transcripts co-locate with notes
- `syncDaysBack: 7` — re-syncs recent files (processing script waits 7 days before processing)

**Processing script:** `vault/90_system/scripts/process-granola-notes.py`

The processing script post-processes Granola-synced files:
1. Injects vault-schema YAML frontmatter (resolves `type` collision: Granola's `type: note` → `granola_type: note`, vault `type: meeting`)
2. Renames to kebab-case: `Unified Daily Standup.md` → `mtg-2026-03-03-unified-daily-standup.md`
3. Auto-sorts into subfolders by title/attendee keyword matching
4. Resolves speaker names in transcripts (`You` → `Sean`, `Guest` → actual name for 1:1 meetings)
5. Updates transcript↔note cross-links after rename

```bash
python3 vault/90_system/scripts/process-granola-notes.py              # Process files older than 7 days
python3 vault/90_system/scripts/process-granola-notes.py --dry-run    # Preview changes
python3 vault/90_system/scripts/process-granola-notes.py --migrate    # One-time migration (all files)
```

**Subfolder structure (auto-sorted):**

| Subfolder | Keywords | Meeting Type |
|-----------|----------|-------------|
| `adops-revops/` | adops, salesforce, case queue, revenue, sales | AdOps and RevOps meetings |
| `all-hands/` | all hands, town hall, 401k, company | Company-wide meetings |
| `campus-conversations/` | campus, sponsored course, .co > campus | Campus team syncs |
| `daily-standup/` | standup, unified daily | Daily standups |
| `david-sean-one-on-ones/` | david (+ ≤2 attendees) | 1:1s with David |
| `design-sync/` | design sync, product + design, design weekly | Design sync meetings |
| `ed-sean-one-on-ones/` | ed, biweekly update (+ ≤2 attendees) | 1:1s with Ed |
| `other/` | *(no match)* | Uncategorized meetings |

**Frontmatter schema (processed meeting notes):**
```yaml
---
granola_id: 17f84a9f-...        # Preserved from Granola (dedup key)
granola_type: note               # Original Granola type (note or transcript)
type: meeting                    # Vault type (resolves collision)
domain:
  - product-management
status: active
ai-context: "Daily standup covering unified daily standup."
context: the-block
created: 2026-03-03
source: granola-sync             # "granola-manual" for pre-plugin notes
attendees:
  - bmendoza@theblock.co
transcript: "[[mtg-2026-03-03-unified-daily-standup-transcript]]"
---
```

**Multi-device note:** Granola runs on the MacBook Pro only (work laptop for meetings). The plugin is desktop-only and does not work on mobile.

## Content Statistics

As of 2026-05-06 (down from 1,431 in Feb 2026 due to the Apple-Notes archive collapse + content consolidation):

| Location | File count |
|----------|-----------:|
| **Total vault `.md` files** | **~608** |
| `00_inbox/` | 2 |
| `02_Areas/` (Agent-Fleet + Work) | ~20 |
| `05_atlas/` (MOCs + operating-models) | 23 |
| `10_timeline/` (daily + weekly + monthly) | ~65 |
| `20_projects/` (all 9 projects + research) | 53 |
| `30_domains/` (Granola + prompts + media-team-ideas) | 317 |
| `40_knowledge/` (concepts + references + notebooklm) | 81 |
| `50_sources/` (data + finance + health + assets) | 7 |
| `60_archive/` (collapsed; mostly Block-related) | 24 |
| `70_apple-notes/` (vestigial) | 1 |
| `90_system/` (templates + scripts + agent-logs) | 8 |
| `Excalidraw/` | 1 |
| `health/` (telemetry; .json + .md reports) | 3 |
| `knowledge/` (LLM-output; currently mostly empty) | 1 |
| Tier-0 + Home.md | 2 |

### Project breakdown (`20_projects/`)

| Project | Files |
|---|---:|
| `prj-code-brain` | 26 |
| `prj-job-hunt-2026` | 8 (NEW 2026-05-04) |
| `research/` | 6 (deep-researcher overnight queue) |
| `prj-16bitfit` | 3 (most content moved to `creative-studio/16bitfit-battle-mode/` outside vault) |
| `prj-boston-move` | 3 |
| `prj-campus-201` | 3 (mostly archived) |
| `prj-personal-finance` | 2 |
| `prj-animation-pipeline` | 1 |
| `prj-sw-portfolio-and-hubs-designs` | 1 (NEW) |

### Archive breakdown (`60_archive/` — read-only)

| Archive subfolder | Files | Origin |
|---|---:|---|
| `operating-models-the-block-2026-05` | 6 | Block bundle archived after layoff |
| `old-mocs` | 6 | Superseded MOC drafts |
| `apple-notes-personal` | 5 | Sentimental items (down from 52 — collapsed 2026-04) |
| `old-templates` | 4 | Superseded templates |
| `inbox-archive-2026-04-25` | 1 | Inbox cleanup snapshot |
| `old-prompts` | 1 | Legacy prompts |
| `old-rag` | 1 | Legacy RAG configs |
| `old-projects` | 0 | (empty placeholder for future archives) |

**The Phase 2/3 Apple-Notes import archives** (`apple-notes-empty` 310, `apple-notes-nyl` 63, `apple-notes-expired` 59, `apple-notes-prompts` 24, `apple-notes-duplicates` 23) were **removed in the 2026-04 cleanup**. The classification methodology is preserved at `40_knowledge/references/ref-apple-notes-classification-rubric.md`.

## Rules and Constraints

### For AI Agents

1. **Never delete vault files** without explicit user permission
2. **Search before creating** — check for existing notes to avoid duplicates
3. **Flat YAML only** — no nested objects in frontmatter, ever
4. **Use `[[wikilinks]]`** for internal references, not markdown links
5. **Kebab-case everywhere** — consistent filenames inside vault folders
6. **PATCH, don't PUT** — use anchors to inject content, don't rewrite files
7. **Don't modify `60_archive/`** — archived items are done
8. **Don't push to git** — the Obsidian Git plugin handles auto-commits
9. **Preserve original content** — when adding frontmatter or renaming, never lose the note body
10. **Flag sensitive content** — if a note contains cleartext passwords or secrets, flag it but don't leave it unprocessed
11. **Never re-enable Obsidian-Git auto-features** (issue #22, 2026-04-23). The shell-level auto-commit hook is the sole owner. `autoSaveInterval`, `autoPushInterval`, `autoPullInterval` must all stay 0.
12. **Never write to `vault/knowledge/`** by hand. That directory is LLM-output only (`vault_synthesizer` writes concepts/connections/index; `query.py --file-back` writes qa/).
13. **Never write to `vault/health/` or `vault/02_Areas/Agent-Fleet/`** by hand (except to fix typos in Sean's manual annotations). Those are agent-output telemetry.
14. **Operating-model artifacts are loaded on-demand.** Don't load all 5 per domain unless the task needs them. Use the agent contract table in [SDK Agents That Touch the Vault](#sdk-agents-that-touch-the-vault) to decide which artifacts to load.

### For Humans

1. **New captures go to `00_inbox/`** — process them periodically with the process-inbox skill
2. **One idea per note** — atomic notes improve both browsing and AI retrieval
3. **Link aggressively** — every `[[concept]]` in brackets is a traversable edge in the knowledge graph
4. **Use templates** — creating notes in the right folder auto-applies the right template
5. **Review your daily note** — the morning focus and evening reflection take < 2 minutes each
6. **Check Home.md** — the dashboard shows active projects and blockers at a glance

### Git and Sync

- Obsidian Git auto-commits every 10 seconds (format: `vault: auto-commit YYYY-MM-DD HH:mm:ss`)
- Obsidian Git auto-pulls every 5 seconds
- **Obsidian Git is only active on the Mac Mini** — the MacBook Pro accesses the vault through Google Drive and does not run Git operations (to avoid `.git/` directory corruption from dual-machine sync)
- Financial CSVs in `50_sources/finance/` are gitignored
- Obsidian workspace state, plugin installations, and Smart Connections cache are gitignored
- The `daily-note-appender.sh` hook writes to the vault but does not commit — Obsidian Git handles that

## Appendix: Related Files Outside the Vault

These files in the parent `claude-code-superuser-pack` repository support vault operations:

| File | Purpose |
|------|---------|
| `scripts/classify-apple-notes.py` | Regex-based note pre-classifier (used in Phase 3) |
| `vault/90_system/scripts/process-granola-notes.py` | Granola meeting note post-processor (auto-sort, frontmatter, speaker names) |
| `.claude/skills/vault-read-write/SKILL.md` | Read/write workflow skill |
| `.claude/skills/vault-architecture/SKILL.md` | Architecture design skill |
| `.claude/skills/vault-automation/SKILL.md` | Templater + Dataview automation skill |
| `.claude/skills/obsidian-mcp-setup/SKILL.md` | MCP connection setup skill |
| `.claude/skills/obsidian-semantic-search/SKILL.md` | Semantic search skill |
| `.claude/skills/process-inbox/SKILL.md` | Inbox processing skill |
| `.claude/skills/knowledge-graph-nav/SKILL.md` | Knowledge graph navigation skill |
| `.claude/hooks/daily-note-appender.sh` | Auto-logs sessions to daily notes |
| `vault/40_knowledge/references/ref-apple-notes-classification-rubric.md` | Apple Notes classification rubric |
| `agents-sdk/agents/vault_indexer.py` | SQLite indexer (chunks + concept_edges) |
| `agents-sdk/agents/vault_synthesizer.py` | LLM synthesizer for concepts/connections/index |
| `agents-sdk/agents/knowledge_lint.py` | Weekly lint (Tier-1 structural + Tier-2 LLM) |
| `agents-sdk/agents/flush.py` | SessionEnd / PreCompact transcript-to-daily-log |
| `agents-sdk/agents/meta_agent.py` | Daily fleet status writer |
| `agents-sdk/agents/daily_driver.py` | Morning daily-note skeleton creator |
| `agents-sdk/agents/deep_researcher.py` | Overnight research queue processor |
| `agents-sdk/scripts/query.py` | Terminal Q&A; writes to `vault/knowledge/qa/` |
| `agents-sdk/scripts/gemini_dr.py` | Gemini Deep Research wrapper; updates spend ledger |
| `agents-sdk/lib/artifact_loader.py` | On-demand operating-model artifact loader |
| `agents-sdk/lib/concept_edges.py` | Typed-edge insert helper for `concept_edges` table |
| `agents-sdk/config.toml` | Agent enablement, paths, safety limits |
| `.claude/hooks/session-start-inject-index.sh` | Injects `vault/knowledge/index.md` at session start |
| `.claude/hooks/session-end-flush.sh` | Triggers `flush.py --trigger session-end` |
| `.claude/hooks/pre-compact-flush.sh` | Triggers `flush.py --trigger pre-compact` (v3.18.0+) |
| `.claude/hooks/vault-integrity.py` | Frontmatter + naming-rule validator |

## Changelog

This guide's content history (the file's git log captures finer-grained edits):

| Date | What changed in the vault (and reflected in this guide) |
|---|---|
| 2026-02-21 | Original guide written. Vault had ~1,431 .md files post Apple Notes import. |
| 2026-02 → 2026-04 | Phase 4–6 SDK-agent work: vault_indexer, vault_synthesizer, knowledge_lint shipped. `vault/.vault-index.db` and `vault/knowledge/` directories created. |
| 2026-04-09 | Six SDK agents disabled (`process_inbox`, `daily_driver` evening/weekly, `pr_digest`, `spending_analysis`, `health_audit`, `md_to_anki`) per `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`. |
| 2026-04-18 | Operating-models Phase 1 wiring (v3.16.0): `daily_driver` morning loads HEARTBEATs in preamble. |
| 2026-04-23 | **Vault-sync ownership rule (issue #22):** shell-level hook becomes sole vault git owner; Obsidian-Git auto-features turned off everywhere. |
| 2026-04-25 | Knowledge-loop consumer activation (Phase B): `session-start-inject-index.sh` hook live. |
| 2026-04 cleanup | Apple Notes archive subfolders (`apple-notes-empty/expired/nyl/duplicates/prompts`) removed. Total .md count drops from ~1,431 to ~608. |
| 2026-04-27 | Operating-models Phase 2 wiring (v3.17.0): `meta_agent`, `flush`, `knowledge_lint` consume schedule-recommendations and SOULs. |
| 2026-04-28 → 2026-04-29 | `process_inbox` re-enabled briefly (v3.17.2/v3.17.3) then paused (v3.17.4) — see `agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`. |
| 2026-05-01 | Knowledge-loop Phase A (PreCompact safety net, v3.18.0): `pre-compact-flush.sh` hook + `flush.py --trigger` field. |
| 2026-05-01 | Knowledge-loop Phase C (qa tier, v3.19.0): `query.py` + `vault/knowledge/qa/` directory. |
| 2026-05-01 | Knowledge-loop Phase D (typed reasoning edges, v3.20.0): `concept_edges` SQLite table; `knowledge_lint` SQL fast path. |
| 2026-05-02 | Tier-0 identity bump: `Sean-Winslow-Full-Personal-Context-v2.0.md` (interview-driven refresh from v1.1). |
| 2026-05-04 | **Sean laid off from The Block.** `the-block/` workspace archived. `prj-job-hunt-2026/` created. The-Block calendar archived (single calendar now: `sean.winslow28@gmail.com`). The-Block operating-model bundle archived to `60_archive/operating-models-the-block-2026-05/`. |
| 2026-05-05 | Job-hunt-2026 operating-model bundle confirmed (status: confirmed). |
| 2026-05-06 | This guide rewritten end-to-end. |
