# Claude Code Prompt: Triage Apple Notes (Phased)

## Context

I just set up the bitbonsai/mcp-obsidian MCP server connected to my vault. I need to test that it works, then use it to help me triage 1,462 imported Apple Notes sitting in `vault/70_apple-notes/`.

My vault follows the shallow-domain folder structure with these destinations:
- `00_inbox/` — Things that need further processing later
- `20_projects/` — Active project material (prefix: `prj-`)
- `40_knowledge/concepts/` — Reusable ideas, frameworks, insights (prefix: `ref-`)
- `40_knowledge/references/` — External reference material, guides, docs (prefix: `ref-`)
- `50_sources/data/` — Raw data, lists, collections
- `60_archive/` — Anything completed, outdated, or not worth keeping in active folders
- **DELETE** — Notes with zero value (empty, duplicates, gibberish, one-word reminders that are expired)

My 6 domains for YAML tagging: `claude-mastery`, `product-management`, `creative-studio`, `life-systems`, `design-team`, `vault`

My active project contexts: `16bitfit`, `campus-201`, `boston-move`, `superuser-pack`, `animation-pipeline`, `personal-finance`

---

## PHASE 0: Test the MCP Connection

Before touching any files, verify the MCP works:

1. Use the Obsidian MCP to list files in `vault/20_projects/`. You should see 6 project notes.
2. Use the Obsidian MCP to read the contents of `vault/Home.md`.
3. Use the Obsidian MCP to create a test note at `vault/00_inbox/test-mcp-connection.md` with this content:
   ```markdown
   ---
   type: idea
   domain: [vault]
   status: active
   ai-context: "MCP connection test — safe to delete"
   created: 2026-02-20
   ---
   # MCP Connection Test
   
   If you can see this note in Obsidian, the MCP bridge is working.
   ```
4. Verify you can read it back.
5. Then delete it.

**STOP and report results before continuing.** If any step fails, troubleshoot the MCP connection.

---

## PHASE 1: Inventory & Categorize (Read-Only)

**Do NOT move or edit any files yet.** This phase is purely analysis.

1. **Scan the structure** of `vault/70_apple-notes/`. Show me:
   - Total file count
   - Folder structure (what subdirectories exist)
   - File types (.md, .html, .txt, images, attachments, etc.)
   - A sample of 20 filenames so I can see the naming patterns

2. **Read a random sample of 30 notes** spread across different subdirectories. For each, note:
   - Filename
   - Approximate length (short = <5 lines, medium = 5-50 lines, long = 50+ lines)
   - Content type (one of: `project-material`, `reference`, `idea`, `list`, `journal`, `code-snippet`, `empty`, `gibberish`, `expired-reminder`, `duplicate`, `personal`, `financial`, `creative`, `work`)

3. **Generate a triage report** with estimated counts:
   - How many notes appear to be **empty or near-empty** (<3 lines of actual content)?
   - How many look like **expired reminders or to-dos** (dates in the past, one-liner tasks)?
   - How many contain **substantive content** worth keeping?
   - What are the most common content themes you see?

**STOP and show me the triage report.** I'll review it and tell you which categories to process first.

---

## PHASE 2: Bulk Clean-Up (Delete/Archive Obvious Junk)

Based on Phase 1 findings, process the easiest categories first:

### 2a. Empty & Near-Empty Notes
- Scan all notes in `70_apple-notes/`
- Any file with fewer than 3 lines of actual content (excluding blank lines) → **move to `60_archive/apple-notes-empty/`**
- Report: how many moved, show 10 examples of what you moved

### 2b. Expired Reminders & One-Liner To-Dos
- Any note that is a single task or reminder referencing a date before 2026 → **move to `60_archive/apple-notes-expired/`**
- Report: how many moved, show 10 examples

### 2c. Duplicates
- Identify notes with identical or near-identical content (>90% match)
- Keep the longest/newest version, move duplicates to `60_archive/apple-notes-duplicates/`
- Report: how many duplicates found

**STOP after 2a-2c. Tell me how many notes remain and the breakdown of what's left.**

---

## PHASE 3: Classify & Route Valuable Notes (Batches of 50)

For the remaining notes, process in batches of 50. For each batch:

1. **Read each note**
2. **Classify it** by determining:
   - Which domain(s) it belongs to
   - What type it is (project, reference, idea, etc.)
   - Whether it relates to an active project context
   - A 1-sentence `ai-context` summary
3. **Apply the action:**

| Classification | Action | Destination |
|---|---|---|
| Related to an active project | Rename with `prj-` prefix, add YAML frontmatter, move | `20_projects/<relevant-project>/` or as standalone in `20_projects/` |
| Reusable knowledge/concept | Rename with `ref-` prefix, add YAML frontmatter, move | `40_knowledge/concepts/` |
| External reference/guide | Rename with `ref-` prefix, add YAML frontmatter, move | `40_knowledge/references/` |
| Raw data, list, collection | Move as-is | `50_sources/data/` |
| Idea worth exploring later | Rename, add YAML frontmatter, move | `00_inbox/` |
| Personal/journal/sentimental | Move as-is | `60_archive/apple-notes-personal/` |
| Financial records | Move as-is | `50_sources/finance/` |
| Can't classify / ambiguous | Move to inbox for manual review | `00_inbox/` |

4. **YAML frontmatter to add** (for notes going to 20_projects/ or 40_knowledge/):
```yaml
---
type: <project|reference|idea>
domain:
  - <detected-domain>
status: active
context: <project-context-if-applicable>
ai-context: "<1-sentence summary>"
created: <original-date-if-detectable OR today>
source: apple-notes-import
---
```

5. **Naming rules:**
   - Convert to kebab-case
   - Add appropriate prefix (`prj-`, `ref-`)
   - Remove Apple Notes artifacts (dates, "Note from...", etc.)
   - Example: `"Meeting notes Jan 15 2025"` → `ref-meeting-notes-jan-2025.md`

6. **After each batch of 50**, report:
   - How many went to each destination
   - 5 example reclassifications (old name → new name → destination)
   - How many remain in `70_apple-notes/`
   - Ask me if I want to continue or adjust the classification rules

---

## Important Rules

1. **Never delete notes permanently** — always move to `60_archive/` subdirectories so I can recover if needed
2. **When in doubt, send to `00_inbox/`** — false positives in inbox are better than misclassified notes
3. **Preserve original content** — only ADD YAML frontmatter to the top, never edit the body text
4. **Handle attachments:** If a note references images or attachments, move those too (keep them together)
5. **Use the Obsidian MCP for all file operations** — this tests the MCP connection thoroughly while doing real work
6. **If the MCP is too slow for bulk operations**, fall back to filesystem commands but tell me you're switching
7. **Track your progress** — after all phases are complete, create a summary note at `vault/40_knowledge/references/ref-apple-notes-triage-log.md` documenting what was processed, how many went where, and what patterns you found

---

## Execution Order

```
Phase 0 (MCP test)     → CHECKPOINT: confirm connection works
Phase 1 (inventory)    → CHECKPOINT: show me the triage report
Phase 2a-c (cleanup)   → CHECKPOINT: show remaining count
Phase 3 batch 1 of N   → CHECKPOINT: show classifications, ask to continue
Phase 3 batch 2 of N   → CHECKPOINT: repeat
...continue until 70_apple-notes/ is empty or I say stop...
```

Start with Phase 0. Let's see if the MCP is working.
