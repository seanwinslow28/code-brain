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

## Vault Root

```
vault/    # All paths below are relative to this root
```

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
in 40_knowledge/references/ with flat YAML frontmatter, links to
existing vault notes, and updates the relevant MOC in 05_atlas/.
```

**Example 3: Process inbox**
```
User: "Process my inbox folder"
Claude: [Uses vault-read-write] Reads all notes in 00_inbox/,
categorizes each by content, adds frontmatter, moves to appropriate
folder, and creates a processing summary.
```

## Reading: Query Patterns

### Pattern A: Direct Filesystem Search (Claude Code CLI)

```bash
# Find a specific daily note
Read "vault/10_timeline/daily/2026-02-20.md"

# Keyword search across vault
Grep "project alpha deadline" --path vault/

# Find files by pattern
Glob "vault/20_projects/**/*.md"

# Find backlinks to a concept
Grep "\[\[Strategic Planning\]\]" --path vault/
```

### Pattern B: MCP Semantic Search

For concept-based search ("notes about productivity systems" rather than exact keywords), use an MCP server (e.g., bitbonsai/mcp-obsidian or smart-connections-mcp).

### Pattern C: Context Injection

Build targeted context by reading specific notes before a task:

```
"Read vault/20_projects/prj-16bitfit/prj-16bitfit.md and
vault/05_atlas/moc-creative-studio.md. Using that context,
draft a sprint plan for the next 2 weeks."
```

## Writing: Note Creation Patterns

### Flat YAML Frontmatter (CRITICAL)

All vault notes use **flat YAML only** — no nested objects. This ensures Dataview compatibility and simple grep-based parsing.

```yaml
---
type: reference
domain: [claude-mastery]
status: active
ai-context: "Comparison of vector database options for local RAG"
source: "Web research, 2026-02-20"
created: 2026-02-20
---
```

### Naming Conventions

| Type | Prefix | Destination | Example |
|------|--------|-------------|---------|
| concept | `ref-` | `40_knowledge/concepts/` | `ref-vector-embeddings.md` |
| reference | `ref-` | `40_knowledge/references/` | `ref-api-rate-limits.md` |
| project | `prj-` | `20_projects/prj-<name>/` | `prj-16bitfit.md` |
| meeting | `mtg-` | domain folder or daily note | `mtg-2026-02-20-standup.md` |
| idea | `idea-` | `40_knowledge/concepts/` | `idea-gamified-onboarding.md` |
| daily | date | `10_timeline/daily/` | `2026-02-20.md` |

All filenames use **kebab-case**.

### HTML Comment Anchor Pattern (PATCH Writes)

Instead of rewriting entire files, target specific sections using HTML comment anchors:

```markdown
## Claude Code Sessions
<!-- claude-sessions -->
```

**To inject content at an anchor:**
1. Find the `<!-- anchor-name -->` comment in the file
2. Insert new content on the line directly below it
3. Leave the anchor comment in place for future writes
4. Never replace or remove the anchor

**Example: Appending a session entry**
```markdown
## Claude Code Sessions
<!-- claude-sessions -->
- [time:: 14:30] | [domain:: creative-studio] | [context:: 16bitfit] | **Outcomes:** Completed sprite pipeline refactor. Link: [[prj-16bitfit]]
- [time:: 09:15] | [domain:: product-management] | [context:: campus-201] | **Outcomes:** Drafted PRD for auth flow. Link: [[prj-campus-201]]
```

**Available anchors by template:**

| Template | Anchors |
|----------|---------|
| tpl-daily | `<!-- jira-log -->`, `<!-- claude-sessions -->`, `<!-- side-projects -->` |
| tpl-weekly | `<!-- auto-wins -->`, `<!-- auto-blockers -->`, `<!-- auto-decisions -->` |
| tpl-project | `<!-- status-update -->`, `<!-- git-commits -->` |

### Source Tracking

When writing research notes, track the source of information:

```markdown
## Source Material
- Web: [Article Title](https://example.com) - accessed 2026-02-20
- Vault: [[ref-existing-note]] - key insight about X
- Session: Claude Code research session - synthesized from 5 sources
```

## Multi-Source Synthesis Protocol

When synthesizing multiple sources (vault notes, web articles, PDFs, or conversation outputs), use this structured framework:

1. **Salient Keywords:** Terms appearing across multiple sources — conceptual anchors
2. **Consensus Points:** Where sources agree — shared conclusions
3. **Divergence:** Where sources disagree — flag contradictions
4. **Actionable Takeaways:** Concrete next steps

### Consensus Matrix Format

```markdown
| Feature / Claim | Source A | Source B | Source C |
|:----------------|:---------|:---------|:---------|
| Uses vector DB  | Yes      | No       | Yes      |
| Graph-based     | No       | Yes      | No       |
| Local-first     | Yes      | Yes      | No       |
```

## Batch Processing Patterns

### Frontmatter Standardization

> "Find all markdown files in `vault/40_knowledge/` missing a `status` field in frontmatter. For each file, add `status: active` to the YAML block. Do not modify the content body."

### Broken Link Audit

> "Find all `[[wikilinks]]` in my vault that point to non-existent files. List them grouped by source file. For each, suggest whether to create the target note or fix the link."

### Dashboard Queries

Claude cannot execute Dataview queries at runtime, but it can:
- Write valid DQL into notes
- Read rendered output from existing dashboard notes (if exported)
- Use Grep/Glob to query the vault directly

## Best Practices

- **Files over apps**: Treat the vault as a codebase — Read/Write/Edit tools work directly
- **PATCH over PUT**: Use `<!-- anchor -->` pattern to inject content, not rewrite whole files
- **Flat YAML only**: No nested objects in frontmatter (breaks Dataview queries)
- **Search before create**: Always check for existing notes to avoid duplicates
- **Wikilinks over markdown links**: Use `[[Note Name]]` for Obsidian graph integration
- **Kebab-case everywhere**: Consistent naming inside vault folders
- **Plan mode for complex ops**: Use Plan Mode for operations like folder refactoring

## Success Criteria

- [ ] Can search vault content and get relevant results
- [ ] New notes include flat YAML frontmatter matching the vault schema
- [ ] HTML comment anchors enable PATCH-style writes
- [ ] Inbox processing categorizes and files notes correctly
- [ ] Source tracking is included in research synthesis notes
- [ ] Wikilinks connect new notes to existing knowledge
- [ ] Naming conventions (kebab-case, prefixes) are followed

## Copy/Paste Ready

```
"Search my vault for notes about project alpha"
"Save this research to my Obsidian vault"
"Create today's daily note"
"Process my inbox folder"
"Find all notes modified this week and summarize progress"
```
