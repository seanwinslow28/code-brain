---
name: vault-read-write
description: Bidirectional Obsidian vault workflows for Claude Code. Query vault content, create structured notes, run daily note routines, synthesize research, and batch process files. Use when searching vault notes, saving outputs to Obsidian, creating daily notes with AI, processing an inbox folder, or building research synthesis workflows.
---

# Bidirectional Read/Write Workflows

## Purpose

Execute bidirectional workflows between Claude Code and Obsidian. Read vault content using filesystem tools or MCP, write structured notes back with proper formatting, run daily note routines, synthesize research from web to vault, and batch process notes for maintenance.

## When to Use

- Searching vault content from a Claude Code session
- Saving Claude Code outputs back to Obsidian as structured notes
- Creating or updating daily notes with AI assistance
- Running research synthesis (web search to Obsidian note)
- Batch processing inbox notes or updating frontmatter

## Examples

**Example 1: Vault search and synthesis**
```
User: "Find notes about mental models and summarize them"
Claude: [Uses vault-read-write] Searches vault using grep for
"mental model" references, reads matching notes, synthesizes
findings into a summary with [[wikilink]] citations to source notes.
```

**Example 2: Save research to vault**
```
User: "Research vector databases and save findings to my vault"
Claude: [Uses vault-read-write] Searches web, creates a new note
in 03_Resources/ with proper frontmatter, links to existing related
vault notes, and updates the relevant MOC.
```

**Example 3: Process inbox**
```
User: "Process my inbox folder"
Claude: [Uses vault-read-write] Reads all notes in 00_Inbox/,
categorizes each by content, adds frontmatter, moves to appropriate
folder, and creates a processing summary.
```

## Reading: Query Patterns

### Pattern A: Direct Filesystem Search (Claude Code CLI)

Run Claude Code from the vault root directory (`cd /path/to/vault && claude`).

```bash
# Find a specific file
Read "Daily Notes/2024-03-20.md"

# Keyword search across vault
Grep "project alpha deadline"

# Find files by pattern
Glob "01_Projects/Alpha/*.md"

# Find backlinks to a concept
grep -r "\[\[Strategic Planning\]\]" .
```

### Pattern B: MCP Semantic Search

For concept-based search ("notes about productivity systems" rather than exact keywords), use an MCP server.

```
"Use the smart-connections tool to find notes semantically related
to 'productivity systems' and summarize the key insights."
```

### Pattern C: Context Injection

Build targeted context by reading specific notes before a task:

```
"Read my CLAUDE.md, then read the project brief at
01_Projects/Beta/brief.md. Using that context, draft a
status update."
```

## Writing: Note Creation Patterns

### Standard Note Creation

When creating notes, always include proper frontmatter and wikilinks:

```markdown
---
type: concept
status: draft
created: 2024-06-15
tags: [research, ai]
keywords: [vector database, embeddings]
related:
  - "[[RAG Architecture]]"
  - "[[Semantic Search]]"
ai-context:
  processed: true
  summary: "Comparison of vector database options for local RAG."
---

# Vector Database Comparison

## Overview

[Content synthesized from research]

## Connections

- Builds on [[Embedding Models]] for vector generation
- Used by [[Semantic Search]] for similarity queries
```

### Source Tracking

When writing research notes, track the source of information:

```markdown
## Sources
- Web: [Article Title](https://example.com) - accessed 2024-06-15
- Vault: [[Related Existing Note]] - key insight about X
- Session: Claude Code research session - synthesized from 5 sources
```

## Slash Commands

Create reusable workflow templates in `.claude/commands/`.

### Daily Note Command (`/day`)

Create `.claude/commands/day.md`:

```markdown
---
description: Create or update today's daily note with tasks and insights
---
# Daily Note Assistant

1. Get today's date in YYYY-MM-DD format.
2. Check if `Daily Notes/[DATE].md` exists.
   - If YES: Read it and show current contents.
   - If NO: Create it using the template below.
3. Ask "What's on your mind?" and wait for response.
4. Process the response:
   - Extract actionable tasks into the `## Tasks` section.
   - Extract insights into `## Notes`.
   - Auto-link key concepts with [[brackets]] if they exist in the vault.

## Template
---
created: ${DATE}
type: journal
status: active
tags: [daily]
---

# ${DATE}

## Priorities
- [ ]

## Tasks
- [ ]

## Notes

## Links
```

### Research Command (`/research`)

Create `.claude/commands/research.md`:

```markdown
---
description: Deep dive research creating linked vault notes
options:
  - topic: The subject to research
---
# Research Protocol for: $topic

1. **Search Vault**: Use grep or MCP search for existing notes on "$topic".
2. **Web Search**: Find recent developments and key sources.
3. **Synthesize**: Create `03_Resources/$topic.md`.
   - Summarize findings with proper citations.
   - Create a "Connections" section linking to existing vault notes.
   - Add frontmatter with `type: concept` and relevant tags.
4. **Update MOC**: Add a link to the relevant Map of Content note.
```

### Inbox Processor Command (`/process-inbox`)

Create `.claude/commands/process-inbox.md`:

```markdown
---
description: Categorize and file inbox notes
---
# Inbox Processor

1. Read CLAUDE.md for vault rules and folder structure.
2. List all files in `00_Inbox/`.
3. For each note:
   a. Read the content.
   b. Determine the appropriate type and folder.
   c. Add or update YAML frontmatter (type, status, tags).
   d. Set `ai-context.processed: true`.
   e. Move to the appropriate folder based on CLAUDE.md rules.
4. Create a processing summary listing what was moved where.
5. Never delete files without explicit permission.
```

## Batch Processing Patterns

### Frontmatter Standardization

> "Find all markdown files in `03_Resources/` missing a `status` field in frontmatter. For each file, add `status: active` to the YAML block. Do not modify the content body."

### Broken Link Audit

> "Find all `[[wikilinks]]` in my vault that point to non-existent files. List them grouped by source file. For each, suggest whether to create the target note or fix the link."

### Dashboard Generation with Dataview

Create dashboard notes with Dataview queries that Claude can read:

```dataview
TABLE file.mtime as "Modified", file.tags as "Tags"
FROM "01_Projects"
WHERE file.mtime >= date(today) - dur(7 days)
AND !contains(file.tags, "#done")
SORT file.mtime DESC
```

Claude cannot execute Dataview queries at runtime, but it can write valid DQL into notes and read rendered output from existing dashboard notes.

## Looping Context Automation

### The Weekly Review Pattern

1. **Capture**: Use `/log "Decided to switch database to Postgres"` to append to daily notes throughout the week
2. **Analyze**: Run weekly:
   > "Read all Daily Notes from the last 7 days. Extract all decisions and open questions. Update `PROJECTS.md` with the current status of each active initiative."
3. **Result**: Self-maintaining project status that evolves from daily captures

## Best Practices

- **Files over apps**: Treat the vault as a codebase. Run Claude Code from the vault root
- **Context is king**: Maintain CLAUDE.md and keep it updated with structure and preferences
- **Plan mode for complex ops**: Use Shift+Tab for operations like folder refactoring to prevent hallucinated paths
- **Atomic changes**: Ask for small, verifiable changes rather than massive batch jobs
- **Search before create**: Always check for existing notes to avoid duplicates
- **Wikilinks over markdown links**: Use `[[Note Name]]` format for Obsidian graph integration

## Success Criteria

- [ ] Can search vault content and get relevant results
- [ ] New notes include proper frontmatter matching the vault schema
- [ ] Slash commands for daily notes and research are functional
- [ ] Inbox processing categorizes and files notes correctly
- [ ] Source tracking is included in research synthesis notes
- [ ] Wikilinks connect new notes to existing knowledge

## Copy/Paste Ready

```
"Search my vault for notes about project alpha"
"Save this research to my Obsidian vault"
"Create today's daily note"
"Process my inbox folder"
"Find all notes modified this week and summarize progress"
```
