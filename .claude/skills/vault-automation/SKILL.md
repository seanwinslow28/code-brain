---
name: vault-automation
description: Obsidian automation with Templater and Dataview for AI-powered knowledge management. Create smart note templates, build AI processing queues, run batch operations, and track note lifecycle status. Use when creating Templater templates, writing Dataview queries, building processing queues, automating vault maintenance, or setting up status tracking workflows.
---

# Automation with Templater and Dataview

## Purpose

Automate Obsidian vault management using Templater for smart note creation and Dataview for AI processing queues. Build status tracking workflows, batch operation patterns, and combine native plugins with Claude Code MCP for hands-off knowledge management.

## When to Use

- Creating note templates with dynamic frontmatter
- Building Dataview dashboards for AI processing queues
- Running batch operations across vault notes
- Tracking note lifecycle (draft to review to processed)
- Combining Templater/Dataview with Claude Code for automation

## Examples

**Example 1: Smart note template**
```
User: "Create a Templater template for AI-friendly notes"
Claude: [Uses vault-automation] Generates a template with tp.system.suggester
for type selection, automatic date stamps, and ai-context frontmatter
initialized to unprocessed state.
```

**Example 2: Processing queue**
```
User: "Show me notes that need AI processing"
Claude: [Uses vault-automation] Creates a Dataview query filtering notes
where ai-context.processed is false, sorted by creation date, displayed
as a table with type and status columns.
```

**Example 3: Batch status update**
```
User: "Mark all reviewed notes as processed"
Claude: [Uses vault-automation] Uses Claude Code to find notes with
status: review, updates their ai-context.processed field to true,
and sets ai-context.last-run to current timestamp.
```

## Templater Templates

### Smart New Note Template

This template prompts for note type and automatically sets AI-tracking fields.

Save as `05_System/Templates/Smart Note.md`:

```markdown
<%*
// 1. Prompt for Note Type
const noteTypes = ["Meeting", "Concept", "Project", "Journal", "Resource"];
const type = await tp.system.suggester(noteTypes, noteTypes);

// 2. Set defaults
const status = "Draft";

// 3. Get title
const title = await tp.system.prompt("Note Title");
await tp.file.rename(title || "Untitled");
-%>
---
title: <% title %>
type: <% type %>
status: <% status %>
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
tags: [inbox]
ai-context:
  processed: false
  summary: ""
  next-actions: []
---

# <% title %>

## Context
<% tp.file.cursor() %>

## Connections

## AI Processing Instructions
- [ ] Synthesize this note
- [ ] Extract action items
```

### Daily Note Template

Save as `05_System/Templates/Daily Note.md`:

```markdown
---
type: journal
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
tags: [daily]
ai-context:
  processed: false
  summary: ""
---

# <% tp.date.now("YYYY-MM-DD dddd") %>

## Priorities
- [ ]

## Tasks
- [ ]

## Notes

## Decisions

## Links
```

### AI Status Toggle Script

Assign to a hotkey to toggle the AI processing status of the current note:

```javascript
<%*
const file = tp.file.find_tfile(tp.file.path(true));
await app.fileManager.processFrontMatter(file, (frontmatter) => {
    if (frontmatter["ai-context"]) {
        frontmatter["ai-context"].processed =
            !frontmatter["ai-context"].processed;
        frontmatter["ai-context"]["last-run"] =
            tp.date.now("YYYY-MM-DD HH:mm");
    } else {
        frontmatter["ai-context"] = {
            processed: true,
            "last-run": tp.date.now("YYYY-MM-DD HH:mm")
        };
    }
});
-%>
```

## Dataview Queries

### AI Processing Queue

Find all notes awaiting AI processing. Place in `Admin/AI Queue.md`:

```dataview
TABLE file.ctime as "Created", type as "Type"
FROM ""
WHERE file.name != this.file.name
  AND (ai-context.processed = false OR !ai-context.processed)
  AND !contains(file.path, "Templates")
SORT file.ctime DESC
LIMIT 20
```

### Status Tracking Dashboard

Track note lifecycle across the vault:

```dataview
TABLE without id
  link(file.link, title) as "Note",
  status as "Current Status",
  ai-context.processed as "AI Ready?"
FROM "01_Projects"
WHERE status != "Archived"
SORT choice(status = "Draft", 1, choice(status = "Review", 2, 3)) ASC
```

### Recently Modified Projects

```dataview
TABLE file.mtime as "Modified", file.tags as "Tags"
FROM "01_Projects"
WHERE file.mtime >= date(today) - dur(7 days)
AND !contains(file.tags, "#done")
SORT file.mtime DESC
```

### Notes by Type Summary

```dataview
TABLE length(rows) as "Count"
FROM ""
WHERE type
GROUP BY type
SORT length(rows) DESC
```

### Stale Notes (No Updates in 30 Days)

```dataview
TABLE file.mtime as "Last Modified", status
FROM "03_Resources"
WHERE file.mtime < date(today) - dur(30 days)
AND status = "active"
SORT file.mtime ASC
LIMIT 15
```

## Status Tracking Workflow

### Lifecycle States

```
Draft --> Review --> Processed --> Permanent
  |                     |
  +---> Archived <------+
```

| Status | Meaning | AI Action |
| :--- | :--- | :--- |
| `seedling` | Raw capture, minimal structure | Categorize, add frontmatter |
| `draft` | Initial content, needs review | Expand, link, verify |
| `review` | Content complete, needs validation | Summarize, extract actions |
| `active` | Ongoing reference, regularly updated | Monitor for staleness |
| `permanent` | Finalized knowledge | No action needed |
| `archived` | No longer active | Exclude from searches |

### Batch Workflow: Inbox Processing

Combine Claude Code + MCP + Dataview for automated inbox processing:

1. **Dataview identifies targets**: AI Queue dashboard shows unprocessed notes
2. **Claude reads the queue**: "Read my AI Queue dashboard and process the top 5 notes"
3. **For each note Claude**:
   - Reads content
   - Adds appropriate type, tags, keywords
   - Sets `ai-context.processed: true`
   - Generates `ai-context.summary`
   - Moves to the appropriate folder
4. **Dashboard auto-updates**: Dataview refreshes to show remaining items

### Automated Weekly Review

**Step 1: Dataview aggregates data (in Obsidian)**
```dataview
TABLE file.link, status
FROM "01_Projects"
WHERE file.mtime >= date(today) - dur(7 days)
```

**Step 2: Claude synthesizes**
> "Read my 'Weekly Stats' note and the project notes listed there. Generate a progress summary, identify stalled projects (status 'Draft' for >7 days), and suggest next steps. Append to my 'Weekly Review' note."

## Plugin Interaction Patterns

### Templater + Claude Code

Templater creates consistently structured notes. Claude Code processes them. The frontmatter schema is the shared contract.

### Dataview + Claude Code

Dataview is read-only (renders at runtime). Claude cannot execute DQL directly but can:
- **Write** valid Dataview queries into dashboard notes
- **Read** dashboard note content to understand current state
- **Act** on the information (process identified notes, update metadata)

### Full Pipeline

```
Templater (creates structured note)
  --> Dataview (surfaces in processing queue)
    --> Claude Code (reads queue, processes notes)
      --> Frontmatter update (marks as processed)
        --> Dataview (removes from queue, appears in dashboard)
```

## Success Criteria

- [ ] Templater templates create notes with consistent AI-friendly frontmatter
- [ ] Dataview queries correctly surface unprocessed notes
- [ ] Status workflow tracks notes from draft through processed
- [ ] Batch operations update frontmatter without modifying note content
- [ ] Weekly review automation produces useful summaries

## Copy/Paste Ready

```
"Create a Templater template for AI-friendly notes"
"Write a Dataview query to find unprocessed notes"
"Set up a processing queue for my vault"
"Batch update frontmatter on my resource notes"
"Automate my weekly vault review"
```
