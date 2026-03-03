---
type: reference
domain:
  - vault
status: active
ai-context: "Comprehensive guide to Sean's Obsidian vault: architecture, conventions, Claude Code integration, and operational workflows."
created: 2026-02-21
---

# Sean's Obsidian Vault — Complete Guide

This document describes everything about this vault: its architecture, how it was built, how it connects to Claude Code, and how to work within it effectively. It is written for both human operators and AI agents.

---

## Table of Contents

1. [What This Vault Is](#what-this-vault-is)
2. [How It Was Built](#how-it-was-built)
3. [Architecture](#architecture)
4. [Folder Structure](#folder-structure)
5. [YAML Frontmatter Schema](#yaml-frontmatter-schema)
6. [Naming Conventions](#naming-conventions)
7. [Templates](#templates)
8. [Maps of Content (MOCs)](#maps-of-content-mocs)
9. [Obsidian Plugins](#obsidian-plugins)
10. [Claude Code Integration](#claude-code-integration)
11. [Skills Reference](#skills-reference)
12. [Hooks](#hooks)
13. [How to Read from the Vault](#how-to-read-from-the-vault)
14. [How to Write to the Vault](#how-to-write-to-the-vault)
15. [Inbox Processing](#inbox-processing)
16. [Knowledge Graph Navigation](#knowledge-graph-navigation)
17. [Semantic Search](#semantic-search)
18. [Daily Workflow](#daily-workflow)
19. [Content Statistics](#content-statistics)
20. [Rules and Constraints](#rules-and-constraints)

---

## What This Vault Is

This is Sean Winslow's personal Obsidian vault — a structured knowledge base that serves as a second brain for both human browsing and AI retrieval. It lives inside the `claude-code-superuser-pack` repository at `vault/` and is designed to work seamlessly with Claude Code.

The vault uses the **PARA method** (Projects, Areas/Domains, Resources/Knowledge, Archive) adapted into a numbered folder hierarchy. Every note has flat YAML frontmatter optimized for Dataview queries and AI context injection. Six domain workspaces mirror the skill domains in the parent repository.

**Key design principles:**
- Files over apps — the vault is a codebase that Claude Code reads/writes directly
- Flat YAML only — no nested objects in frontmatter (Dataview compatibility)
- Atomic notes — one idea per note for retrieval precision
- Kebab-case everywhere — consistent, URL-safe filenames
- PATCH over PUT — use HTML comment anchors to inject content, not rewrite files
- Search before create — always check for existing notes before making new ones

---

## How It Was Built

The vault was constructed in multiple phases:

### Phase 0: Architecture Design
The folder structure, frontmatter schema, templates, MOCs, and Home dashboard were designed and created from scratch. The structure follows a shallow-domain model with numbered top-level folders for sidebar ordering.

### Phase 1: Apple Notes Import
1,462 Apple Notes were imported as raw markdown files into `vault/70_apple-notes/Notes/`. These notes spanned Sean's personal and professional life: 16BitFit game development, NYL video production work, Claude Code configurations, PM career materials, creative writing, financial records, and personal items.

### Phase 2: Bulk Cleanup (Automated)
Three automated cleanup passes removed noise before classification:
- **Phase 2a**: 311 empty/near-empty notes (< 3 non-blank lines) archived to `60_archive/apple-notes-empty/`
- **Phase 2b**: 23 duplicate `-1.md` pairs resolved (kept longer version) to `60_archive/apple-notes-duplicates/`
- **Phase 2c**: 59 expired reminders, NYL job stubs, and dated checklists archived to `60_archive/apple-notes-expired/`

### Pre-Classification: Automated Regex Scoring
A Python script (`scripts/classify-apple-notes.py`) scored all 1,005 remaining notes by domain, type, project context, and confidence level using weighted regex pattern matching across 6 domain patterns, 11 type patterns, and 6 project patterns. Output: a 1,005-row TSV report at `vault/70_apple-notes/classification-report.tsv`.

### Phase 3: Classify & Route
The remaining 629 notes (376 had already been archived in Phase 2 auto-commits) were classified and routed in three tiers:
- **Tier 1 (HIGH confidence)**: Auto-moved with generated frontmatter
- **Tier 2 (MEDIUM confidence)**: Quick-scanned with manual overrides where the classifier was wrong
- **Tier 3 (LOW confidence)**: Individually read and manually classified

Each note was: renamed to kebab-case with the appropriate prefix, given YAML frontmatter, and moved to its destination folder. A post-processing audit caught and fixed 268 filename prefix mismatches.

### Result
~1,430 markdown files across the vault, fully tagged and organized. Zero files remaining in the Apple Notes staging directory.

---

## Architecture

```
vault/
├── Home.md                         # Dataview dashboard — entry point
│
├── 00_inbox/                       # Raw captures, quick ideas, needs-review items
├── 05_atlas/                       # MOCs (Maps of Content) — 1 per domain
│   ├── moc-claude-mastery.md
│   ├── moc-product-management.md
│   ├── moc-creative-studio.md
│   ├── moc-life-systems.md
│   ├── moc-design-team.md
│   └── moc-vault.md
│
├── 10_timeline/                    # Temporal notes
│   ├── daily/                      # YYYY-MM-DD.md (daily notes)
│   ├── weekly/                     # YYYY-Www.md (weekly reviews)
│   └── monthly/                    # YYYY-MM.md (monthly reviews)
│
├── 20_projects/                    # Active, time-bound projects
│   ├── prj-16bitfit/               # 16BitFit game project (210 notes)
│   ├── prj-campus-201/             # Campus LMS platform (72 notes)
│   ├── prj-superuser-pack/         # This repo's skills/agents (16 notes)
│   ├── prj-boston-move/             # Boston relocation planning (12 notes)
│   ├── prj-personal-finance/       # Personal finance automation (4 notes)
│   └── prj-animation-pipeline/     # Animation pipeline project (1 note)
│
├── 30_domains/                     # Domain workspace folders (mirror skill domains)
│   ├── claude-mastery/
│   ├── product-management/
│   ├── creative-studio/
│   ├── life-systems/
│   ├── design-team/
│   └── vault/
│
├── 40_knowledge/                   # Permanent reference material
│   ├── concepts/                   # Ideas, frameworks, creative writing (21 notes)
│   ├── references/                 # How-tos, guides, documentation (280 notes)
│   └── notebooklm-exports/        # Synthesized research from NotebookLM
│
├── 50_sources/                     # Raw data and assets
│   ├── data/                       # Lists, collections, raw data (16 notes)
│   ├── finance/                    # Financial records (13 notes, CSVs gitignored)
│   └── assets/                     # Creative assets, images, sprites
│
├── 60_archive/                     # Completed/inactive items
│   ├── apple-notes-empty/          # Phase 2a: empty notes (310)
│   ├── apple-notes-expired/        # Phase 2c: expired reminders (59)
│   ├── apple-notes-nyl/            # NYL video production work (63)
│   ├── apple-notes-personal/       # Personal/sentimental items (52)
│   ├── apple-notes-prompts/        # Disposable AI prompts (24)
│   ├── apple-notes-duplicates/     # Phase 2b: resolved duplicates (23)
│   ├── old-mocs/                   # Superseded MOC drafts (6)
│   ├── old-templates/              # Superseded templates (4)
│   ├── old-prompts/                # Legacy prompts (1)
│   └── old-rag/                    # Legacy RAG configs (1)
│
├── 70_apple-notes/                 # Import staging area
│   ├── classification-report.tsv   # Pre-classifier output (1,005 rows)
│   ├── phase-3-execute-classification.md
│   └── Notes/                      # Empty after Phase 3 (attachments remain)
│       ├── attachments/
│       └── images/
│
├── 90_system/                      # Vault infrastructure
│   ├── templates/                  # Templater templates (tpl-*.md)
│   ├── scripts/                    # Automation helpers
│   ├── css-snippets/               # Custom CSS for Obsidian
│   └── mcp-configs/                # MCP server configuration references
│
└── .obsidian/                      # Obsidian app configuration
```

### Why This Structure

- **Numbered prefixes** (`00_`, `05_`, `10_`...) control sidebar sort order in Obsidian
- **Shallow hierarchy** (max 3 levels) keeps filesystem navigation fast for both humans and AI
- **`30_domains/`** provides workspace folders that mirror the 6 Claude Code skill domains but are currently empty — they exist for future domain-specific working notes that don't belong to a project
- **`70_apple-notes/`** is a staging area for imports, excluded from Obsidian's linter
- **`90_system/`** keeps infrastructure separate from content

---

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
| `meeting` | type, date, domain, attendees, context | |
| `reference` | type, domain, status, ai-context, created | source |
| `idea` | type, domain, status, ai-context, created | energy-level |
| `moc` | type, domain | |

---

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

---

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
| `tpl-daily` | `<!-- jira-log -->`, `<!-- claude-sessions -->`, `<!-- side-projects -->` |
| `tpl-weekly` | `<!-- auto-wins -->`, `<!-- auto-blockers -->`, `<!-- auto-decisions -->` |
| `tpl-project` | `<!-- status-update -->`, `<!-- git-commits -->` |

**Example — Appending a Claude Code session entry to a daily note:**

```markdown
## Claude Code Sessions
<!-- claude-sessions -->
- [time:: 14:30] | [domain:: creative-studio] | [context:: 16bitfit] | **Outcomes:** Completed sprite pipeline refactor.
```

The entry uses Dataview inline fields (`[field:: value]`) so sessions are queryable:

```dataview
TABLE time, domain, context
FROM "10_timeline/daily"
WHERE domain = "product-management"
```

---

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

---

## Obsidian Plugins

Eight community plugins are installed:

| Plugin | Purpose | Key Config |
|--------|---------|------------|
| **Dataview** | Query engine for MOCs and dashboards | DQL + DataviewJS enabled, inline fields enabled |
| **Templater** | Smart note templates with dynamic content | Folder-template mapping, `tp.*` functions |
| **Obsidian Git** | Auto-sync to git repository | 10-second auto-commit, 5-second auto-pull, `vault: auto-commit {{date}}` format. **Only active on Mac Mini** — MacBook Pro accesses vault via Google Drive without Git. |
| **Obsidian Linter** | Markdown formatting and YAML automation | Auto-adds `created`/`updated` timestamps, auto-adds title from H1, ignores `70_apple-notes/` and `60_archive/` |
| **Local REST API** | MCP server endpoint for AI access | HTTPS on port 27124, self-signed SSL |
| **Remotely Save** | Cloud sync (encrypted config) | Encrypted credentials |
| **Homepage** | Opens vault to Home.md | Set to `Home` note |
| **Granola Sync** | Syncs meeting transcripts from [Granola](https://granola.ai/) | Destination: `30_domains/product-management/the-block-meetings-granola-notes/`. Desktop only. |

### Obsidian App Settings

| Setting | Value | Why |
|---------|-------|-----|
| New file location | `00_inbox/` folder | All new captures go to inbox first |
| Attachment folder | `50_sources/assets/` | Centralized asset storage |
| Auto-update links | Enabled | Links survive file renames |
| Daily notes folder | `10_timeline/daily/` | ISO date format (YYYY-MM-DD) |

---

## Claude Code Integration

The vault is bidirectionally integrated with Claude Code through multiple channels:

### Channel 1: Direct Filesystem Access

Claude Code's Read, Write, Edit, Grep, and Glob tools operate directly on vault files. The vault is just a directory of markdown files — no special API needed.

```
# Read a note
Read "vault/20_projects/prj-16bitfit/prj-16bitfit.md"

# Search for a concept
Grep "animation pipeline" --path vault/

# Find all project notes
Glob "vault/20_projects/**/*.md"

# Find backlinks to a note
Grep "\[\[prj-16bitfit\]\]" --path vault/
```

### Channel 2: MCP Server (Obsidian Local REST API)

The Local REST API plugin exposes vault operations over HTTPS on port 27124. An MCP server (`mcp-obsidian`) translates these into Claude-accessible tools:

- `read_note` — Read a note by path
- `write_note` — Create or overwrite a note
- `patch_note` — Append content to a note (PATCH semantics)
- `move_note` — Move/rename a note
- `delete_note` — Delete a note
- `search_notes` — Full-text search
- `list_directory` — List directory contents
- `read_multiple_notes` — Batch read
- `update_frontmatter` — Modify YAML frontmatter
- `get_frontmatter` — Read YAML frontmatter
- `manage_tags` — Add/remove tags
- `get_vault_stats` — Vault statistics

**MCP Config (for `claude_desktop_config.json`):**

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uvx",
      "args": ["mcp-obsidian"],
      "env": {
        "OBSIDIAN_API_KEY": "<key-from-local-rest-api-plugin>",
        "OBSIDIAN_HOST": "127.0.0.1",
        "OBSIDIAN_PORT": "27124",
        "OBSIDIAN_PROTOCOL": "https",
        "OBSIDIAN_VERIFY_SSL": "false"
      }
    }
  }
}
```

**When to use MCP vs direct filesystem:**
- **Direct filesystem** (Read/Write/Edit/Grep/Glob): Faster for bulk operations, available in all Claude Code environments, no dependency on Obsidian running
- **MCP**: Required for semantic search, patch operations, and when Obsidian-specific features are needed (tag management, frontmatter extraction)

### Channel 3: Native MCP Integrations

As of 2026-03-01, Claude Code connects to external services via native MCPs (preferred over Zapier). Key integrations for vault workflows:

- **Google Calendar** (`claude.ai Google Calendar` / `google-workspace`) — Pull meeting schedules for daily notes. Always query both `sean.winslow28@gmail.com` and `swinslow@theblock.co` in parallel.
- **Jira** (`mcp-atlassian`) — Query tickets for standup prep, inject activity summaries at `<!-- jira-log -->` anchors.
- **Slack** (Slack plugin, pending Block admin approval) — Post summaries, read DMs. Falls back to Zapier Slack tools if plugin unavailable.
- **Gmail** (`claude.ai Gmail` / `google-workspace`) — Email digests for inbox processing.
- **Google Sheets** (`google-workspace`) — Export financial data, analytics reports.

These replace earlier Zapier-only recommendations. Zapier is retained only for Salesforce, GA4, Webhooks, and cloud code execution.

### Channel 4: Hooks (Automatic)

The `daily-note-appender.sh` hook runs automatically when Claude Code stops, appending a session summary to today's daily note. See the [Hooks](#hooks) section for details.

### Channel 5: Skills (On-Demand)

Seven vault-specific skills provide structured workflows for common operations. See the [Skills Reference](#skills-reference) section.

---

## Skills Reference

Seven skills in `.claude/skills/` provide vault-specific capabilities:

| Skill | Purpose | Invoke When |
|-------|---------|-------------|
| `vault-read-write` | Bidirectional read/write workflows | Searching vault, saving outputs, processing inbox |
| `vault-architecture` | Folder structure and schema design | Setting up or restructuring the vault |
| `vault-automation` | Templater and Dataview automation | Creating templates, building dashboards, batch ops |
| `obsidian-mcp-setup` | MCP server installation and troubleshooting | Setting up or debugging vault connection |
| `obsidian-semantic-search` | Embedding models and vector search | Setting up semantic search, building RAG pipelines |
| `process-inbox` | Inbox triage and classification | Processing `00_inbox/` contents |
| `knowledge-graph-nav` | Wiki-link traversal and backlink discovery | Following concept links, building context |

### How to Invoke Skills

In Claude Code, skills auto-load based on context. You can also invoke them explicitly:

```
"Using vault-read-write, save this research to my vault"
"Using process-inbox, triage my inbox folder"
"Using knowledge-graph-nav, gather all context for the 16BitFit project"
```

---

## Hooks

### daily-note-appender.sh (Stop Hook)

**Trigger:** Runs automatically when Claude Code stops (session end or manual stop).

**What it does:**
1. Creates today's daily note (`vault/10_timeline/daily/YYYY-MM-DD.md`) if it doesn't exist, using the `tpl-daily` structure
2. Detects the current domain from the working directory name
3. Detects the project context from the directory basename
4. Appends a session entry below the `<!-- claude-sessions -->` anchor with Dataview inline fields

**Session entry format:**
```markdown
- [time:: 14:30] | [domain:: creative-studio] | [context:: 16bitfit] | **Outcomes:** Session ended (manual). Working dir: /path/to/project
```

**Domain detection rules:**
| Working Directory Contains | Detected Domain |
|---------------------------|-----------------|
| `claude-mastery`, `superuser-pack`, `claude-code` | `claude-mastery` |
| `product-management`, `campus`, `block` | `product-management` |
| `creative-studio`, `16bitfit`, `animation`, `remotion` | `creative-studio` |
| `life-systems`, `finance`, `health` | `life-systems` |
| `design-team`, `design` | `design-team` |
| `vault` | `vault` |

---

## How to Read from the Vault

### Pattern A: Direct Search

```
# Find a specific note
Read "vault/20_projects/prj-16bitfit/prj-16bitfit.md"

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

---

## How to Write to the Vault

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

---

## Inbox Processing

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

---

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

---

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

---

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

---

## Content Statistics

As of 2026-02-21:

| Location | File Count |
|----------|-----------|
| **Total vault .md files** | **1,431** |
| `00_inbox/` | 227 |
| `05_atlas/` (MOCs) | 6 |
| `20_projects/` (all projects) | 315 |
| `40_knowledge/` (concepts + references) | 301 |
| `50_sources/` (data + finance) | 29 |
| `60_archive/` (all archive subfolders) | 543 |
| `70_apple-notes/` (staging metadata) | 1 |
| `90_system/` (templates + infra) | 7 |
| `Home.md` | 1 |

### Project Breakdown

| Project | Notes |
|---------|-------|
| `prj-16bitfit` | 210 |
| `prj-campus-201` | 72 |
| `prj-superuser-pack` | 16 |
| `prj-boston-move` | 12 |
| `prj-personal-finance` | 4 |
| `prj-animation-pipeline` | 1 |

### Archive Breakdown

| Archive Subfolder | Notes | Origin |
|-------------------|-------|--------|
| `apple-notes-empty` | 310 | Phase 2a: empty/near-empty notes |
| `apple-notes-nyl` | 63 | NYL video production work |
| `apple-notes-expired` | 59 | Expired reminders and checklists |
| `apple-notes-personal` | 52 | Personal/sentimental items |
| `apple-notes-prompts` | 24 | Disposable AI prompts |
| `apple-notes-duplicates` | 23 | Phase 2b: resolved duplicates |

---

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

### For Humans

1. **New captures go to `00_inbox/`** — process them periodically with the process-inbox skill
2. **One idea per note** — atomic notes improve both browsing and AI retrieval
3. **Link aggressively** — every `[[concept]]` in brackets is a traversable edge in the knowledge graph
4. **Use templates** — creating notes in the right folder auto-applies the right template
5. **Review your daily note** — the morning focus and evening reflection take < 2 minutes each
6. **Check Home.md** — the dashboard shows active projects and blockers at a glance

### Granola Meeting Sync

[Granola](https://granola.ai/) is a meeting transcription app that runs on Sean's MacBook Pro during Google Meetings at The Block. The `obsidian-granola-sync` community plugin ([GitHub](https://github.com/tomelliot/obsidian-granola-sync)) automatically syncs transcribed meeting notes into the vault.

**Destination folder:** `vault/30_domains/product-management/the-block-meetings-granola-notes/`

**Subfolder structure (manually sorted):**

| Subfolder | Meeting Type |
|-----------|-------------|
| `adops-revops/` | AdOps and RevOps meetings |
| `daily-standup/` | Daily standups |
| `david-sean-one-on-ones/` | 1:1s with David |
| `design-sync/` | Design sync meetings |
| `ed-sean-one-on-ones/` | 1:1s with Ed |
| `other/` | Uncategorized meetings |

**Current workflow:** The plugin syncs all Granola notes into the configured destination folder (flat). Sean manually sorts notes into the appropriate subfolder after sync.

**TODO — Auto-sort automation:** Build a script or Templater automation that routes Granola-synced notes into the correct subfolder based on keywords in the meeting title (e.g., "standup" -> `daily-standup/`, "design" -> `design-sync/`, "Ed" -> `ed-sean-one-on-ones/`, "David" -> `david-sean-one-on-ones/`, "AdOps"/"RevOps"/"Salesforce" -> `adops-revops/`). Unmatched notes go to `other/`.

**Multi-device note:** Granola runs on the MacBook Pro only (work laptop for meetings). The plugin is desktop-only and does not work on mobile.

### Git and Sync

- Obsidian Git auto-commits every 10 seconds (format: `vault: auto-commit YYYY-MM-DD HH:mm:ss`)
- Obsidian Git auto-pulls every 5 seconds
- **Obsidian Git is only active on the Mac Mini** — the MacBook Pro accesses the vault through Google Drive and does not run Git operations (to avoid `.git/` directory corruption from dual-machine sync)
- Financial CSVs in `50_sources/finance/` are gitignored
- Obsidian workspace state, plugin installations, and Smart Connections cache are gitignored
- The `daily-note-appender.sh` hook writes to the vault but does not commit — Obsidian Git handles that

---

## Appendix: Related Files Outside the Vault

These files in the parent `claude-code-superuser-pack` repository support vault operations:

| File | Purpose |
|------|---------|
| `scripts/classify-apple-notes.py` | Regex-based note pre-classifier (used in Phase 3) |
| `.claude/skills/vault-read-write/SKILL.md` | Read/write workflow skill |
| `.claude/skills/vault-architecture/SKILL.md` | Architecture design skill |
| `.claude/skills/vault-automation/SKILL.md` | Templater + Dataview automation skill |
| `.claude/skills/obsidian-mcp-setup/SKILL.md` | MCP connection setup skill |
| `.claude/skills/obsidian-semantic-search/SKILL.md` | Semantic search skill |
| `.claude/skills/process-inbox/SKILL.md` | Inbox processing skill |
| `.claude/skills/knowledge-graph-nav/SKILL.md` | Knowledge graph navigation skill |
| `.claude/hooks/daily-note-appender.sh` | Auto-logs sessions to daily notes |
| `vault/40_knowledge/references/ref-apple-notes-classification-rubric.md` | Apple Notes classification rubric |
