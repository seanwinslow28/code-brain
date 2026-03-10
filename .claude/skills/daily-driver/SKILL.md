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

**Example 1: Morning Start**
```
User: "Start my day"
Claude: [Uses daily-driver]
Good morning! Let me pull up your context.

Reading yesterday's daily note... Found 2 open loops:
1. PR review for Campus auth flow (assigned yesterday)
2. Draft subscription audit email to finance

Reading your calendar (if available)... 3 meetings today.

## Today's Plan
1. [Deep Work] PR review for Campus auth - 45 min (carry-over)
2. [Quick Win] Draft subscription audit email - 15 min (carry-over)
3. [Meeting Prep] Sprint planning at 2pm - review board first
4. [Creative] Continue animation prototype if time permits

Which should be your #1 focus today?
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
2. Read any active project notes referenced in yesterday's log from `vault/20_projects/`
3. Check calendar via Google Calendar MCP — query BOTH `sean.winslow28@gmail.com` (personal) AND `swinslow@theblock.co` (The Block work) calendars in parallel. Use `claude.ai Google Calendar` (gcal_list_events) or `google-workspace` (get_events) tools.
4. Scan Slack for overnight activity (see Step 1b below)
5. Ask: "Anything new on your plate today?"

### Step 1b: Slack Overnight Scan

Scan Slack for messages that arrived since last EOD (~5 PM yesterday). Uses the native Slack plugin (not Zapier). Sean's Slack user ID is `U09SC58MYDN`.

**Run these searches in parallel:**

1. **DMs to you** — `slack_search_public_and_private` with query `to:me`, channel_types `im`, sorted by timestamp desc, filtered to after 5 PM yesterday
2. **@mentions** — `slack_search_public_and_private` with query `<@U09SC58MYDN>`, sorted by timestamp desc, filtered to after 5 PM yesterday
3. **Key channels** — `slack_read_channel` on high-priority channels (check recent messages for anything urgent)

**Classify each message as:**
- **Action Required** — needs a reply, decision, or task from Sean
- **FYI** — informational, no action needed but good to know
- **Skip** — bot noise, automated notifications, irrelevant threads

**Write to daily note** at the `<!-- slack-overnight -->` anchor:

```markdown
## Slack Overnight
<!-- slack-overnight -->
### Action Required
- **Matt Vitebsky** (DM, 4:02 PM): Campus bug triage process — needs response about backend access
- **Karla Vallecillo** (DM, 3:25 PM): Assigned Salesforce Campus case — review needed

### FYI
- **Claudine Daumur** (DM, 10:55 AM): Confirmed design approach works, no changes needed
- **#campus-eng**: 3 new messages about deploy timeline
```

**Rules:**
- Do NOT include Jira bot notifications (those go in `<!-- jira-log -->`)
- Do NOT include messages Sean already replied to (check for Sean's replies in context)
- Group by priority (Action Required first), then by sender
- Include channel name or "DM" prefix, sender name, time, and a 1-line summary

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
2. Ask: "What did you actually get done today?" (or review conversation history)
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
- [ ] Slack overnight scan classifies messages as Action Required / FYI / Skip
- [ ] Slack digest written to `<!-- slack-overnight -->` anchor (excludes Jira bot noise and already-replied messages)
- [ ] EOD review captures open loops and stages tomorrow
- [ ] Carry-over tasks are tracked (not silently dropped)
- [ ] Weekly review synthesizes patterns from daily notes
- [ ] Daily notes follow the vault frontmatter schema
- [ ] Claude Code session entries use Dataview inline fields

## Temporary Recurring Commitments

### Apartment Cleanup — Daily through March 20, 2026
Sean is cleaning up/throwing away items from a section of his apartment every day through March 20th (packing for the Boston move). Each morning plan should include an afternoon cleanup task targeting a specific area. Remove this section after March 20, 2026.

## Copy/Paste Ready

```
"Start my day"
"What should I focus on today?"
"Check in on my progress"
"Wrap up my day"
"Do a weekly review"
```
