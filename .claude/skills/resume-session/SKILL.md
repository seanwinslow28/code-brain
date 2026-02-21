---
name: resume-session
description: Synthesize a "here's where you left off" briefing from CLAUDE.md, vault project note, and today's daily note
---

# Resume Session

## Purpose

When starting a new Claude Code session, read all available context sources and synthesize a concise briefing so you can pick up exactly where the last session left off.

## When to Use

- Starting work on a project ("where did I leave off?", "resume", "catch me up")
- After a break or context reset
- When opening a project you haven't touched in a while

## Protocol

### Step 1: Read Context Sources

Read these files in order (skip any that don't exist):

1. **Project CLAUDE.md** — the current working directory's `CLAUDE.md`
   - Look for `## Session Log` section, especially the latest entry
   - Extract: decisions, blockers, next steps, files modified

2. **Vault Project Note** — find the matching note in `vault/20_projects/`
   - Match by directory name or `context` field
   - Extract: `ai-context` from frontmatter, `<!-- status-update -->` content, blockers, key decisions

3. **Today's Daily Note** — `vault/10_timeline/daily/YYYY-MM-DD.md`
   - Extract: focus item, any related Claude Code session entries, open tasks

4. **Yesterday's Daily Note** — if today's doesn't exist yet
   - Extract: carry-forward items, open loops

### Step 2: Synthesize Briefing

Produce a structured briefing:

```markdown
## Session Briefing — <project-name>

**Last session:** <date and time from Session Log>
**Domain:** <domain>

### Where You Left Off
<1-2 sentence summary of last session's state>

### Open Blockers
- <blocker 1>
- <blocker 2>

### Next Steps (from last session)
- [ ] <next step 1>
- [ ] <next step 2>

### Recent Decisions
- <decision> (rationale: <why>)

### Today's Context
- Focus: <from daily note>
- Related tasks: <any relevant items from daily note>

### Suggested First Action
> <concrete suggestion for what to do first>
```

### Step 3: Offer to Continue

After presenting the briefing, ask:
- "Want to pick up from the next steps, or do you have something else in mind?"

## Important Constraints

- Read-only operation — this skill never writes files
- If no context sources exist, say so honestly and ask the user to describe where they are
- Keep the briefing scannable — use bullet points, not paragraphs
- Highlight anything that's time-sensitive (deadlines, review dates, expiring blockers)
