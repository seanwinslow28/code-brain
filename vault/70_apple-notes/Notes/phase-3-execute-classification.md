# Phase 3: Execute Apple Notes Classification & Routing

## Context

You are continuing a multi-phase Apple Notes triage process. Phases 0-2 and pre-classification have been completed in a prior session. This prompt covers **Phase 3: Classify & Route** — the final phase that moves 1,005 notes from `vault/70_apple-notes/Notes/` into their correct Obsidian vault destinations with proper YAML frontmatter.

### What Has Been Done

| Phase | Description | Result |
|-------|-------------|--------|
| Phase 0 | MCP connection test | All 5 operations succeeded |
| Phase 1 | Read-only inventory of 1,462 imported Apple Notes | Categorized by size, theme, and structure |
| Phase 2a | Archive empty/near-empty notes (<3 non-blank lines) | 311 moved to `60_archive/apple-notes-empty/` |
| Phase 2b | Resolve `-1.md` duplicate pairs (keep longer version) | 23 moved to `60_archive/apple-notes-duplicates/` |
| Phase 2c | Archive expired reminders, NYL job stubs, dated checklists | 59 moved to `60_archive/apple-notes-expired/` |
| Pre-classification | Automated regex classifier scored all 1,005 remaining notes | Output: `vault/70_apple-notes/classification-report.tsv` |

### What Needs to Happen Now

Move the remaining ~1,005 notes from `vault/70_apple-notes/Notes/` into their vault destinations. Each note gets:
1. **Renamed** to kebab-case with appropriate prefix (`ref-`, `prj-`, `idea-`)
2. **YAML frontmatter injected** at the top
3. **Moved** to the correct vault destination folder
4. **Wikilinks** added where obvious connections exist

---

## CRITICAL: Restore Notes Before Processing

The `vault/70_apple-notes/Notes/` directory was deleted after the pre-classifier ran. You MUST restore it from git before processing:

```bash
# Restore the Notes directory from the commit just before deletion
git checkout 7ba806a -- vault/70_apple-notes/Notes/
```

This will restore **629 .md files**. The original 1,005 in the TSV included files that were moved to archive during Phase 2 auto-commits. After restoration:

1. Run: `ls vault/70_apple-notes/Notes/*.md | wc -l` to confirm file count
2. Cross-reference restored files against the TSV: any file in the TSV but NOT on disk was already archived in Phase 2 — skip it
3. Any file on disk but NOT in the TSV should be classified manually (unlikely)

---

## Reference Documents

### Classification Report (TSV)
- **Path**: `vault/70_apple-notes/classification-report.tsv`
- **Columns**: `filename`, `lines`, `domain`, `type`, `project`, `destination`, `confidence`, `ai_hint`
- **1,005 rows** classified with HIGH/MEDIUM/LOW confidence

### Classification Rubric
- **Path**: `vault/40_knowledge/references/ref-apple-notes-classification-rubric.md`
- Contains: domain keyword tables, type signal patterns, project context mapping, destination priority rules, ambiguity resolution rules, confidence level definitions, YAML frontmatter template

### Pre-Classifier Script (for re-running if needed)
- **Path**: `scripts/classify-apple-notes.py`
- Run with: `python3 scripts/classify-apple-notes.py`
- Regenerates the TSV from the current Notes/ directory

---

## Destination Distribution (from TSV)

| Destination | Count | Confidence |
|-------------|-------|------------|
| `40_knowledge/references/` | 277 | Mixed |
| `00_inbox/` | 225 | Mostly LOW |
| `20_projects/prj-16bitfit/` | 209 | Mostly HIGH |
| `20_projects/prj-campus-201/` | 71 | Mostly HIGH |
| `60_archive/apple-notes-nyl/` | 63 | Mixed |
| `60_archive/apple-notes-personal/` | 56 | Mixed |
| `60_archive/apple-notes-prompts/` | 25 | Mixed |
| `40_knowledge/concepts/` | 20 | Mixed |
| `50_sources/data/` | 16 | Mixed |
| `20_projects/prj-superuser-pack/` | 15 | HIGH |
| `50_sources/finance/` | 13 | Mixed |
| `20_projects/prj-boston-move/` | 11 | MEDIUM |
| `20_projects/prj-personal-finance/` | 3 | MEDIUM |

**Confidence breakdown**: 470 HIGH, 385 MEDIUM, 149 LOW

---

## Execution Strategy: Three-Tier Approach

### Tier 1: AUTO-MOVE — HIGH Confidence (470 notes)

These notes have strong keyword matches and clear single-domain classification. Process them automatically without manual review.

**For each HIGH confidence note:**
1. Read the TSV row for the note (filename, domain, type, project, destination, ai_hint)
2. Read the note content (first 30 lines is sufficient for frontmatter generation)
3. Generate a kebab-case filename:
   - Strip special characters, emojis, leading `#`/`-`/`.`
   - Convert to lowercase with hyphens
   - Add prefix based on type: `ref-` for reference, `prj-` for project-material, `idea-` for idea
   - Truncate to 60 chars max (before `.md`)
   - Ensure no filename collisions (append `-2`, `-3` if needed)
4. Inject YAML frontmatter at the top of the file content:
   ```yaml
   ---
   type: <from TSV type field, mapped to: reference|project|idea|archive>
   domain:
     - <primary domain from TSV>
   status: active
   context: <project name if applicable>
   ai-context: "<ai_hint from TSV, cleaned up to a proper sentence>"
   created: 2026-02-20
   source: apple-notes-import
   ---
   ```
5. Write the file to its destination folder with the new filename
6. Delete the original from `vault/70_apple-notes/Notes/`

**Process in batches of 50 notes.** After each batch:
- Print a summary: `Batch N: 50 notes moved. [destination breakdown]`
- Verify no errors occurred
- Continue to next batch

### Tier 2: QUICK-SCAN — MEDIUM Confidence (385 notes)

These notes matched some keywords but may have ambiguous classification. Process in batches of 50 with a brief content scan.

**For each MEDIUM confidence note:**
1. Read the TSV row
2. Read the FULL note content (not just 30 lines)
3. Verify the TSV classification makes sense by checking:
   - Does the content actually match the assigned domain? (A note about "fighters" could be 16bitfit OR creative-writing)
   - Is the type correct? (An AI prompt about 16bitfit should go to the project folder, not the prompts archive)
   - Is there a project context the classifier missed?
4. Apply the **ambiguity resolution rules** from the rubric:
   - 16BitFit PRD/spec → `20_projects/prj-16bitfit/` (project over domain)
   - AI prompt about 16BitFit with reusable design specs → `20_projects/prj-16bitfit/`
   - AI prompt about 16BitFit that's disposable → `60_archive/apple-notes-prompts/`
   - Claude Code config note about this pack → `20_projects/prj-superuser-pack/`
   - NYL notes → archive unless they contain reusable production knowledge
   - Cover letters/resumes → `60_archive/apple-notes-personal/`
   - Hello PM/Aspireship notes with reusable PM frameworks → `40_knowledge/references/`
5. Override the TSV destination if your scan disagrees
6. Generate kebab-case filename, inject frontmatter, move to destination

**After each batch of 50**, print:
- Summary with override count: `Batch N: 50 notes processed. 7 overrides. [destination breakdown]`

### Tier 3: MANUAL REVIEW — LOW Confidence (149 notes)

These notes had few or no keyword matches. They need careful individual reading.

**For each LOW confidence note:**
1. Read the FULL note content
2. Classify manually using the rubric's domain/type tables
3. Check for:
   - Very short notes that are just fragments → `60_archive/apple-notes-empty/` (may have been missed in Phase 2)
   - Notes in languages other than English → `60_archive/apple-notes-personal/`
   - Notes that are just URLs or links → `50_sources/data/` if valuable, otherwise archive
   - Notes that are pure nonsense/garbled text → `60_archive/apple-notes-empty/`
4. For genuinely ambiguous notes: route to `00_inbox/` for Sean's manual review
5. Generate kebab-case filename, inject frontmatter, move to destination

**Process in batches of 25** (smaller batches for more careful work).

---

## Known Misclassification Risks

The prior session identified these patterns to watch for:

| Issue | Example | Correct Action |
|-------|---------|----------------|
| `personal` notes that are creative writing | Comedy bits, story ideas disguised as journal entries | Move to `40_knowledge/concepts/` instead of personal archive |
| `boston-move` false positives | Notes mentioning "Boston" in other contexts (e.g., "Boston beer company") | Don't route to `prj-boston-move/` unless actually about the move |
| `references` that are disposable AI prompts | "Generate a...", "Create a..." prompts with no reusable knowledge | Move to `60_archive/apple-notes-prompts/` instead of references |
| `16bitfit` notes that are generic game dev | Generic pixel art or Phaser notes not specific to 16BitFit | Route to `40_knowledge/references/` instead of the project folder |
| `campus` false positives | Notes mentioning "campus" in non-LMS contexts | Verify content is actually about the Campus education platform |
| NYL notes with reusable production knowledge | Video production techniques, After Effects workflows | Consider `40_knowledge/references/` instead of NYL archive |

---

## YAML Frontmatter Rules

### Type Mapping (TSV type → YAML type)

| TSV `type` | YAML `type` | Notes |
|------------|-------------|-------|
| `reference` | `reference` | Direct mapping |
| `project-material` | `project` | Maps to project type |
| `idea` | `idea` | Direct mapping |
| `ai-prompt` | `reference` if reusable, `archive` if disposable | Judgment call |
| `ai-session-output` | `archive` | Almost always disposable |
| `creative-writing` | `reference` | Goes to concepts/ |
| `code-snippet` | `reference` | Goes to references/ |
| `work-nyl` | `archive` | NYL work |
| `financial` | `reference` | Financial records |
| `personal` | `archive` | Personal items |
| `list` | `reference` | Data/lists |

### Domain Values (use exactly these strings)

```
claude-mastery, product-management, creative-studio, life-systems, design-team, vault
```

### Flat YAML Only

**CRITICAL**: No nested objects in frontmatter. Dataview queries will break.

```yaml
# CORRECT
domain:
  - creative-studio
  - product-management

# WRONG
domain:
  primary: creative-studio
  secondary: product-management
```

### ai-context Field

Take the `ai_hint` from the TSV and clean it into a proper 1-sentence summary:
- Remove leading `#`, `-`, special characters
- Capitalize first letter
- Ensure it ends with a period
- Keep under 120 characters
- If the hint is garbage, write your own based on reading the content

---

## Existing Vault Destinations (Pre-Created)

These directories already exist:

```
vault/
├── 00_inbox/                              # Manual review queue
├── 20_projects/
│   ├── prj-16bitfit/                      # 16BitFit game project
│   ├── prj-animation-pipeline/            # Animation pipeline project
│   ├── prj-boston-move/                    # Boston move planning
│   ├── prj-campus-201/                    # Campus LMS project
│   ├── prj-personal-finance/              # Personal finance automation
│   └── prj-superuser-pack/                # This repo's skills/agents
├── 40_knowledge/
│   ├── concepts/                          # Creative writing, ideas, frameworks
│   └── references/                        # How-tos, guides, reusable knowledge
├── 50_sources/
│   ├── data/                              # Raw data, lists, collections
│   └── finance/                           # Financial records
└── 60_archive/
    ├── apple-notes-duplicates/            # Phase 2b: resolved duplicates (23)
    ├── apple-notes-empty/                 # Phase 2a: empty/near-empty (311)
    ├── apple-notes-expired/               # Phase 2c: expired reminders (59)
    ├── apple-notes-nyl/                   # NYL video production work
    ├── apple-notes-personal/              # Personal/journal/sentimental
    └── apple-notes-prompts/               # Disposable AI prompts
```

---

## Filename Generation Rules

### Kebab-Case Conversion

```
Input:  "# 16BitFit Design System Implementation - PHASE 1- Foundation Setup.md"
Output: "prj-16bitfit-design-system-implementation-phase-1.md"

Input:  "Based on my thorough analysis of the Anthropic Agent Skills documentation….md"
Output: "ref-anthropic-agent-skills-analysis.md"

Input:  "16bitfit idea - we can have houses in a town similar to Pokemon blue….md"
Output: "idea-16bitfit-pokemon-style-town-houses.md"
```

### Rules

1. Strip leading `#`, `-`, `.`, `$`, `@`, digits (unless meaningful like "16bitfit")
2. Remove emoji, Unicode ellipsis (`…`), special punctuation
3. Convert spaces, underscores, and multiple hyphens to single hyphens
4. Lowercase everything
5. Truncate to 60 characters (before `.md` extension)
6. Add prefix: `ref-`, `prj-`, `idea-`, or none for archive items
7. If a file with that name already exists at the destination, append `-2`, `-3`, etc.

### Filenames with Special Characters (IMPORTANT)

Many Apple Notes filenames contain:
- Unicode ellipsis `…` (U+2026) — appears as `\342\200\246` in git
- Curly quotes `'` `'` `"` `"` — strip these
- Leading `-` — causes `mv` to interpret as flags. Always use `mv -- "source" "dest"`
- Emoji characters — strip entirely

When using bash to move files with these characters, ALWAYS:
- Quote the full path with double quotes
- Use `mv --` to prevent flag interpretation
- Test with `ls -- "filename"` before moving

---

## Checkpoints

After completing each tier, pause and report:

### After Tier 1 (HIGH confidence auto-move):
```
TIER 1 COMPLETE
- Notes processed: [N]
- Successful moves: [N]
- Errors: [N]
- Destination breakdown:
  [destination]: [count]
  ...
```

### After Tier 2 (MEDIUM confidence quick-scan):
```
TIER 2 COMPLETE
- Notes processed: [N]
- Overrides from TSV: [N]
- Destination breakdown:
  [destination]: [count]
  ...
- Override summary:
  [original destination] → [new destination]: [count]
  ...
```

### After Tier 3 (LOW confidence manual review):
```
TIER 3 COMPLETE
- Notes processed: [N]
- Sent to inbox for manual review: [N]
- Destination breakdown:
  [destination]: [count]
  ...
```

### Final Report:
```
PHASE 3 COMPLETE
- Total notes processed: [N]
- Notes remaining in vault/70_apple-notes/Notes/: [should be 0]
- Destination totals (including Phase 2 archives):
  [destination]: [count]
  ...
```

---

## Important Technical Notes

1. **Use the `vault-read-write` skill** — invoke it at the start of your session for vault writing patterns
2. **Obsidian MCP (bitbonsai/mcp-obsidian)** is available for vault operations: `write_note`, `move_note`, `read_note`, `list_directory`, `delete_note`. However, for bulk operations, bash `mv` with proper quoting is faster.
3. **Do NOT push to git** — the user will handle git commits
4. **Do NOT modify** the classification-report.tsv or the rubric
5. **Do NOT process** files in `60_archive/` — those are already handled
6. **If a note contains cleartext passwords or secrets**: flag it in the checkpoint report but still move it. Do NOT leave it in Notes/.
7. **Wikilinks**: When a note clearly references another note or project, add `[[wikilink]]` references. Don't force this — only add when the connection is obvious.
8. **Images/attachments**: The `vault/70_apple-notes/Notes/attachments/` directory may contain referenced images. Leave these in place for now — they'll be handled in a separate pass.

---

## Quick Start Checklist

```
[ ] Invoke the vault-read-write skill
[ ] Restore Notes/ from git: git checkout 7ba806a -- vault/70_apple-notes/Notes/
[ ] Confirm file count: ls vault/70_apple-notes/Notes/*.md | wc -l
[ ] Read the TSV: vault/70_apple-notes/classification-report.tsv
[ ] Read the rubric: vault/40_knowledge/references/ref-apple-notes-classification-rubric.md
[ ] Create any missing destination directories
[ ] Begin Tier 1 processing (HIGH confidence, batches of 50)
[ ] Checkpoint after Tier 1
[ ] Begin Tier 2 processing (MEDIUM confidence, batches of 50)
[ ] Checkpoint after Tier 2
[ ] Begin Tier 3 processing (LOW confidence, batches of 25)
[ ] Checkpoint after Tier 3
[ ] Final report
[ ] Verify vault/70_apple-notes/Notes/ is empty (or only contains attachments/)
```

---

## Skill to Invoke

At the start of your session, invoke the `vault-read-write` skill to load the vault writing patterns, naming conventions, and frontmatter template. This is mandatory.

---

## File Counts for Verification

| Location | Expected Count |
|----------|---------------|
| Restored `vault/70_apple-notes/Notes/*.md` | ~629 (from git restore) |
| `vault/70_apple-notes/classification-report.tsv` rows | 1,005 |
| TSV rows matching restored files | ~629 (process these) |
| TSV rows NOT matching restored files | ~376 (already archived in Phase 2, skip) |
| `60_archive/apple-notes-empty/` | 311 |
| `60_archive/apple-notes-duplicates/` | 23 |
| `60_archive/apple-notes-expired/` | 59 |
| **Total original Apple Notes** | ~1,398 |
