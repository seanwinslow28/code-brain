---
name: daily-driver
description: Daily personal assistant for morning planning, task prioritization, and end-of-day review. Integrates with Obsidian daily notes for continuity. Use when user says "start my day", "daily plan", "morning routine", "EOD review", "what should I focus on", or "wrap up my day".
---

# Daily Driver

## Purpose

Act as a personal assistant that bookends each day: morning planning to set priorities, mid-day check-ins for course correction, and end-of-day reviews to capture progress. Integrates with Obsidian daily notes so nothing is lost between sessions.

## When to Use

- Starting the day (morning planning, priority setting)
- Mid-day check-in (re-prioritize based on what happened)
- End of day (review, compress context, plan tomorrow)
- Weekly planning (review the week's daily notes, set next week's goals)

## Vault Paths

```
vault/10_timeline/daily/YYYY-MM-DD.md    # Daily notes
vault/10_timeline/weekly/YYYY-Www.md     # Weekly reviews
vault/90_system/templates/tpl-daily.md   # Daily note template
vault/90_system/templates/tpl-weekly.md  # Weekly review template
```

## HTML Comment Anchors

Daily notes use these anchors for programmatic injection (PATCH, not PUT):

| Anchor | Section | What Gets Injected |
|--------|---------|-------------------|
| `<!-- slack-overnight -->` | Slack Overnight | DMs, @mentions, and channel activity since last EOD |
| `<!-- jira-log -->` | Work Log | Jira activity summaries |
| `<!-- claude-sessions -->` | Claude Code Sessions | Session entries with inline Dataview fields |
| `<!-- side-projects -->` | Side Project Notes | Creative/R&D progress |

Weekly notes use:

| Anchor | Section | What Gets Injected |
|--------|---------|-------------------|
| `<!-- auto-wins -->` | Wins This Week | Aggregated wins from daily notes |
| `<!-- auto-blockers -->` | Blockers & Open Loops | Unresolved items |
| `<!-- auto-decisions -->` | Decisions Made | Key choices and rationale |

## Examples

**Example 1: Morning Start (Job-Hunt + Deep-Work mode)**
```
User: "Start my day"
Claude: [Uses daily-driver]
Good morning! Let me pull up your context.

Reading yesterday's daily note... Found 2 open loops:
1. Follow up on Anthropic AI PM application (sent 3 days ago, no response)
2. Finish v0 of intent-engineering MCP server (60% done)

Reading your calendar... 1 recruiter screen today at 2pm.

## Today's Plan
1. [Deep Work] Intent-engineering MCP server v0 — analyze_intent_spec tool (90 min)
2. [Pipeline] 2 quality applications to Tier-1 targets (60 min)
3. [Meeting Prep] 1:45pm — read recruiter's LinkedIn, prep 5 questions to ask (15 min)
4. [Quick Win] Reply to 2 warm-20 contacts awaiting >5 days (15 min)

Based on prj-job-hunt-2026/README.md, your #1 focus today is: ship the analyze_intent_spec tool — that's the Track-C unblocker for the public MCP server release.
```

**Example 2: EOD Review**
```
User: "Wrap up my day"
Claude: [Uses daily-driver]
Updating today's daily note at vault/10_timeline/daily/2026-02-20.md...

## Session Summary
- Completed: PR review, subscription email sent
- In progress: Animation prototype (60% done)
- Blocked: Waiting on API access from DevOps

## Open Loops for Tomorrow
- [ ] Follow up on API access request
- [ ] Finish animation prototype
- [ ] Prep for Wednesday 1:1

Appended to vault/10_timeline/daily/2026-02-20.md
```

## Morning Planning Protocol

### Step 1: Gather Context

1. Read yesterday's daily note from `vault/10_timeline/daily/`
2. Read `vault/20_projects/prj-job-hunt-2026/README.md` for current job-hunt status, weekly retro, and any Status checkboxes due in the next 7 days
3. Read any other active project notes referenced in yesterday's log from `vault/20_projects/`
4. Check calendar via Google Calendar MCP — query `sean.winslow28@gmail.com` only. (The prior work calendar was archived 2026-05 and access has been or is being revoked.) Use `claude.ai Google Calendar` (gcal_list_events) or `google-workspace` (get_events) tools.
5. Scan Slack for overnight activity (see Step 1b below — currently no-op pending personal Slack workspace)
6. Check `vault/02_Areas/Focus.md` for current focus areas and priority goals. Use these to inform today's priorities instead of asking.

### Step 1a: Job-Hunt + Deep-Work Morning Brief (job-hunt-2026 active phase)

The 8:45 AM agent surfaces five things while Sean is in active job hunt:

1. **Job-hunt status** — applications submitted yesterday, follow-ups due today, warm-20 messages awaiting reply > 5 days. Pull from `vault/20_projects/prj-job-hunt-2026/applications.md` (when it exists) and `warm-20.md`.
2. **Today's interview-related calendar events** — anything tagged `interview`, `recruiter`, `screen`, or with a target-company name from `target-companies.md`. Surface these first, before any other meetings.
3. **Deep-work focus** — pick from current week's MCP server task (Track C in `2026-05-04-onwards-and-upwards-plan.md` Phase 4) + master plan checklist + portfolio-piece work (June 11 short, animation pipeline). Default block: 8:30 AM–12:30 PM Mon–Fri.
4. **Status checkboxes due** — anything in `prj-job-hunt-2026/README.md` "Status" or "Migration checklist" sections due in next 7 days.
5. **Yesterday's wins** — what got shipped (counterbalance to the application-rejection emotional ride). Pull from yesterday's daily note "Completed" section.

When the job hunt closes (offer accepted), this Step 1a is retired or rewritten for the new role's rhythm.

### Step 1b: Slack Overnight Scan

> **2026-05 status:** No-op for the job-hunt domain. Sean's Block Slack workspace was archived with the rest of his Block access; no personal Slack workspace is wired in yet. Skip this step entirely until either a personal Slack workspace is configured or a new role brings a new workspace ID.

When this step is re-enabled (new workspace exists), the historical pattern is preserved below for reference:

**Run these searches in parallel:**

1. **DMs to you** — `slack_search_public_and_private` with query `to:me`, channel_types `im`, sorted by timestamp desc, filtered to after 5 PM yesterday
2. **@mentions** — `slack_search_public_and_private` with query `<@USER_ID>` (replace with active workspace user ID), sorted by timestamp desc, filtered to after 5 PM yesterday
3. **Key channels** — `slack_read_channel` on high-priority channels (check recent messages for anything urgent)

**Classify each message as:**
- **Action Required** — needs a reply, decision, or task from Sean
- **FYI** — informational, no action needed but good to know
- **Skip** — bot noise, automated notifications, irrelevant threads

**Write to daily note** at the `<!-- slack-overnight -->` anchor, grouped by priority (Action Required first), then by sender. Include channel name or "DM" prefix, sender name, time, and a 1-line summary.

**Rules (when active):**
- Do NOT include Jira bot notifications (those go in `<!-- jira-log -->`)
- Do NOT include messages Sean already replied to (check for Sean's replies in context)

### Step 2: Prioritize with the 1-3-5 Rule

Structure the day as:
- **1** big thing (deep work, 60-90 min block)
- **3** medium things (30 min each)
- **5** small things (5-15 min each, batch together)

Categorize tasks by type:
| Type | Icon | Description |
|:-----|:-----|:------------|
| Deep Work | [DW] | Requires focus, no meetings |
| Quick Win | [QW] | Can finish in under 15 min |
| Meeting Prep | [MP] | Pre-reads, agendas, follow-ups |
| Creative | [CR] | Side projects, learning, R&D |
| Admin | [AD] | Email, Slack, approvals |

### Step 3: Write to Daily Note

Create or update `vault/10_timeline/daily/YYYY-MM-DD.md` using the template at `vault/90_system/templates/tpl-daily.md`. The template includes:

- YAML frontmatter: `type: daily`, `date`, `energy-peak`, `mood`
- Slack Overnight with `<!-- slack-overnight -->` anchor
- Morning Focus section with single-priority prompt
- Dataview task query from `20_projects/`
- Work Log with `<!-- jira-log -->` anchor
- Claude Code Sessions with `<!-- claude-sessions -->` anchor
- Side Projects with `<!-- side-projects -->` anchor
- Evening Reflection section

### Writing to Anchors

When injecting content at an anchor, find the `<!-- anchor-name -->` comment and insert content directly below it. Do NOT replace the anchor comment itself — leave it in place for future writes.

```markdown
## Claude Code Sessions
<!-- claude-sessions -->
- [time:: 14:30] | [domain:: creative-studio] | [context:: 16bitfit] | **Outcomes:** Completed sprite pipeline refactor. Link: [[prj-16bitfit]]
```

## End-of-Day Protocol

### Step 1: Review

1. Read today's daily note from `vault/10_timeline/daily/`
2. Review today's daily note entries (claude-sessions, jira-log, side-projects anchors) to determine what was accomplished. Do NOT ask — infer from the written record.
3. Mark tasks complete/incomplete

### Step 2: Capture

Update the daily note with:
- **Completed:** What got done
- **Decisions:** Any choices made and their rationale
- **Open Loops:** Unfinished tasks, waiting-on items, follow-ups needed
- **Files Modified:** If this was a coding session

### Step 3: Stage Tomorrow

Add a `**Carry forward:**` entry in Evening Reflection with:
- Carry-over tasks (uncompleted must-dos)
- New items that surfaced during the day
- Any time-sensitive deadlines

## Mid-Day Check-In

When the user asks "how's my day going" or "check in":

1. Read today's daily note from `vault/10_timeline/daily/`
2. Count completed vs planned tasks
3. Flag any carry-overs that are becoming urgent
4. Suggest re-prioritization if the day shifted (meetings ran long, fire drill, etc.)

## Weekly Review Integration

On Friday or Sunday, prompt:

> "Want to do a weekly review? I'll read the last 7 daily notes and summarize your week."

1. Read `vault/10_timeline/daily/` for the past 7 days
2. Aggregate: tasks completed, decisions made, open loops
3. Identify patterns (what kept slipping? what energized you?)
4. Draft next week's top 3 priorities
5. Create weekly review note at `vault/10_timeline/weekly/YYYY-Www.md` using `vault/90_system/templates/tpl-weekly.md`

## Success Criteria

- [ ] Morning planning produces a prioritized daily note
- [ ] Job-hunt + deep-work brief surfaces the five Step 1a signals (status / interview events / deep-work focus / status-checkboxes due / yesterday's wins) when the job hunt is active
- [ ] Slack overnight scan no-op is honored (no errors against revoked workspaces); when re-enabled, classifies messages as Action Required / FYI / Skip and writes to `<!-- slack-overnight -->` anchor (excludes bot noise + already-replied messages)
- [ ] EOD review captures open loops and stages tomorrow
- [ ] Carry-over tasks are tracked (not silently dropped)
- [ ] Weekly review synthesizes patterns from daily notes
- [ ] Daily notes follow the vault frontmatter schema
- [ ] Claude Code session entries use Dataview inline fields

## Copy/Paste Ready

```
"Start my day"
"What should I focus on today?"
"Check in on my progress"
"Wrap up my day"
"Do a weekly review"
```
