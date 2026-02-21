---
name: preserve-session
description: Save current session state to CLAUDE.md and the corresponding vault project note before ending work
---

# Preserve Session

## Purpose

Capture the current session's context before it's lost. Updates the project's CLAUDE.md with blockers, decisions, and next steps, and appends a summary to the corresponding vault project note so future sessions can pick up where you left off.

## When to Use

- End of a work session ("save my progress", "preserve context")
- Before switching to a different project
- When context window is getting large and you want to compress
- Before a long break

## Protocol

### Step 1: Gather Session Context

Review the current conversation and extract:

1. **Decisions made** — choices and their rationale
2. **Blockers encountered** — things that stopped progress
3. **Files modified** — list of created/edited files
4. **Next steps** — what should happen next session
5. **Open questions** — unresolved items needing user input

### Step 2: Update Project CLAUDE.md

Read the current project's `CLAUDE.md`. Append or update a `## Session Log` section:

```markdown
## Session Log

### <YYYY-MM-DD HH:MM>
**Decisions:**
- <decision 1>
- <decision 2>

**Blockers:**
- <blocker>

**Next Steps:**
- [ ] <next step 1>
- [ ] <next step 2>

**Files Modified:**
- `path/to/file1`
- `path/to/file2`
```

If CLAUDE.md doesn't have a Session Log section, create one. If it does, append a new timestamped entry.

### Step 3: Update Vault Project Note

Find the corresponding project note in `vault/20_projects/`. Match by:
- The project directory name (e.g., working in `16bitfit/` → `vault/20_projects/prj-16bitfit/prj-16bitfit.md`)
- The `context` field in CLAUDE.md frontmatter

Update the project note:
1. Insert latest status into `<!-- status-update -->` anchor
2. Update `ai-context` in frontmatter with current state
3. Add any new key decisions to the decisions table
4. Update blockers list

### Step 4: Update Daily Note

If today's daily note exists at `vault/10_timeline/daily/YYYY-MM-DD.md`, append a session entry to the `<!-- claude-sessions -->` anchor:

```markdown
- [time:: HH:MM] | [domain:: <domain>] | [context:: <project>] | **Outcomes:** <1-sentence summary>. Link: [[prj-<project>]]
```

### Step 5: Confirm

Output a summary of what was saved and where:
- CLAUDE.md: updated/created
- Vault project note: updated/skipped (with reason)
- Daily note: appended/skipped

## Important Constraints

- Never overwrite existing CLAUDE.md content — append only
- Use `<!-- anchor -->` pattern for vault note updates (PATCH, not PUT)
- If no matching vault project note exists, report it but don't create one automatically
- Keep ai-context under 200 characters
