---
name: process-inbox
description: Scan vault/00_inbox/ for unprocessed files, classify by domain, apply YAML frontmatter, and move to correct folder
---

# Process Inbox

## Purpose

Triage the vault inbox. For each file in `vault/00_inbox/`, analyze content, determine the correct domain and note type, apply standardized YAML frontmatter, generate a 1-sentence `ai-context`, rename with the proper prefix, and move to the appropriate vault folder.

## When to Use

- Periodically (weekly or daily) to clear the inbox
- After bulk captures (Zapier webhooks, quick notes, Apple Notes imports)
- When the user says "process my inbox" or "triage inbox"

## Vault Path

```
vault/00_inbox/    # Source: unprocessed files land here
```

## Processing Rules

### Step 1: Scan

Read all files in `vault/00_inbox/`. Skip `.gitkeep` and hidden files.

### Step 2: Classify Each File

For each file, determine:

| Field | How to Determine |
|-------|-----------------|
| `type` | Content analysis: is it a concept, meeting notes, project idea, reference, journal entry? |
| `domain` | Match keywords to domains: claude-mastery, product-management, creative-studio, life-systems, design-team, vault |
| `status` | Default to `draft` for new captures |
| `ai-context` | Generate a 1-sentence summary of what the note is about |

### Step 3: Apply Frontmatter

Add or update YAML frontmatter using the vault schema:

```yaml
---
type: <determined-type>
domain: [<determined-domain>]
status: draft
ai-context: "<1-sentence summary>"
created: <file-creation-date or today>
---
```

### Step 4: Rename with Prefix

Apply kebab-case naming with type prefix:

| Type | Prefix | Example |
|------|--------|---------|
| concept | `ref-` | `ref-vector-embeddings.md` |
| project | `prj-` | `prj-new-feature.md` |
| meeting | `mtg-` | `mtg-2026-02-20-standup.md` |
| idea | `idea-` | `idea-gamified-onboarding.md` |
| reference | `ref-` | `ref-api-rate-limits.md` |
| journal | (date) | `2026-02-20.md` |

### Step 5: Move to Destination

| Type | Destination |
|------|-------------|
| concept / reference | `vault/40_knowledge/concepts/` or `vault/40_knowledge/references/` |
| project | `vault/20_projects/<new-prj-folder>/` |
| meeting | `vault/10_timeline/daily/` (append to daily note) or standalone in domain folder |
| idea | `vault/00_inbox/` → `vault/40_knowledge/concepts/` (ideas graduate to concepts) |
| journal | `vault/10_timeline/daily/` |
| unknown | Leave in `vault/00_inbox/` with a `status: needs-review` flag |

### Step 6: Report

Output a summary table:

```
| File | Type | Domain | Destination | ai-context |
|------|------|--------|-------------|------------|
```

## Important Constraints

- Never delete files — only move them
- If classification is uncertain, leave in inbox with `status: needs-review`
- Preserve original content — only add/update frontmatter and rename
- Use `[[wikilinks]]` to connect to existing notes when relevant concepts are detected
- If more than 10 files are queued, process all of them — do NOT pause for confirmation. Log the batch count in the summary report. For any file where classification confidence is below 80%, tag with `#triage/human` and leave in inbox with `status: needs-review` instead of moving.
