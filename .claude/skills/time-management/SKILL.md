---
name: time-management
description: Time management and calendar optimization assistant. Plans daily schedules around Sean's 4:45 AM routine and 45/35/20 work split, audits calendar for meeting overload, facilitates daily planning (`/today`), and resolves scheduling conflicts using energy mapping. Use this skill when the user mentions "calendar", "audit my time", "schedule", "plan my day", "today", "time blocking", "meetings", "deep work", or "when should I".
---

# Time Management & Calendar Optimization

## Purpose

Optimizes Sean's most scarce resource — attention. Built around his actual daily structure (4:45 AM anchor, PPL gym split, 8-4/9-5 remote work block), energy patterns, and 45/35/20 work split at The Block. Audits calendar data for meeting creep, automates daily planning, and protects deep work windows.

## When to Use

- **Daily Planning:** "Plan my day" / `/today`
- **Time Audit:** "Where did my time go last week?" / "Am I in too many meetings?"
- **Conflict Resolution:** "I have overlapping meetings" / "Should I skip this meeting?"
- **Deep Work:** "When should I schedule focused work?" / "Protect my morning"
- **Weekly Review:** "How was my time split this week?"

## Sean's Actual Schedule

### Daily Structure (Weekdays)

```
4:45 AM  — Wake up, coffee
5:15 AM  — Gym (PPL split, 60-70 min)
~6:30 AM — Post-gym: shower, breakfast
~7:00 AM — Pre-work window (1-2 hours)
           Side projects, meal prep, learning, AI news/tutorials
8:00/9:00 AM — Work starts (flexible, depends on meeting schedule)
           8 hours remote at The Block
~1:00 PM — Energy lull (post-meeting fatigue)
~2:00 PM — Energy returns
4:00/5:00 PM — Work ends
5:00-6:00 PM — Lounge, decompress
6:00-9:00 PM — TV, personal projects/research on laptop,
               quality time with girlfriend
~9:00 PM — Bed (target 6-8 hours sleep)
```

### Energy Map

| Time Block | Energy Level | Best For |
|-----------|-------------|----------|
| 5:15-6:30 AM | HIGH (gym) | Physical training |
| 7:00-9:00 AM | PEAK (post-workout) | Deep work, creative tasks, side projects |
| 9:00-12:00 PM | HIGH | Focused work, building, automation |
| 12:00-1:00 PM | MEDIUM | Lunch, light admin |
| 1:00-2:00 PM | LOW (post-meeting lull) | Low-stakes tasks, email, Slack |
| 2:00-4:00 PM | MEDIUM-HIGH | Meetings, collaboration, code review |
| 5:00-9:00 PM | MEDIUM | Personal projects, learning, relaxation |

### Work Week Pattern (The Block)

**45/35/20 Split:**
- **45% Building** — Zapier automations, Campus 201 features, dev coordination, Claude Skills for work
- **35% Meetings** — Concentrated Tue-Thu, ~7-8 per week, leads daily standup
- **20% Firefighting** — Reactive issue resolution, Slack fires

**Day Types:**

| Day | Type | Character |
|-----|------|-----------|
| Monday | Focus Day | Meeting-light. Deep work on automation, Jira, tickets, Campus ops, side projects |
| Tuesday | Meeting Day | Meeting-heavy. Standup + scheduled syncs |
| Wednesday | Meeting Day | Meeting-heavy. Standup + scheduled syncs |
| Thursday | Meeting Day | Meeting-heavy. Standup + scheduled syncs |
| Friday | Focus Day | Meeting-light. Wrap-up, side projects, planning |

### Current Task Management

- **Current system:** Mental list + Apple Notes (migrating to Obsidian vault)
- **Target system:** Obsidian daily notes + Claude Code `/today` planning
- **Calendar:** Personal Google Calendar with work calendar synced (Google Calendar OAuth planned)

## Examples

**Example 1: Daily Planning (`/today`)**
```
User: "Plan my day"
Claude: [Uses time-management]

It's Tuesday — Meeting Day. Here's your plan:

PEAK ENERGY (7:00-9:00 AM) - Pre-work window
  [1] Side project: 16BitFit sprint work (60 min)
  [2] Review Jira board for standup prep (15 min)

MORNING BLOCK (9:00-12:00)
  [3] Daily standup (leads) — 9:30
  [4] Deep work: Campus 201 ticket writing (90 min)
  [5] Sprint sync — 11:00

MIDDAY (12:00-1:00)
  [6] Lunch + light Slack catch-up

LOW ENERGY (1:00-2:00)
  [7] Email triage, Slack responses, admin

AFTERNOON (2:00-4:00)
  [8] 1:1 with PM manager — 2:00
  [9] Zapier automation build (remaining time)

3 meetings today | 2.5 hours deep work protected
```

**Example 2: Time Audit**
```
User: "How was my time split this week?"
Claude: [Uses time-management]

Week of Feb 10-14:
Building:  [==================--] 42% (target: 45%)
Meetings:  [================----] 38% (target: 35%) -- slightly over
Firefight: [========------------] 20% (target: 20%)

Meeting Load: 9 meetings (target: 7-8)
Deep Work Blocks: 4 (Mon AM, Mon PM, Fri AM, Fri PM)
Fragmentation: 2 "Swiss Cheese" days (gaps < 30 min between meetings)

Recommendation: Wednesday has 4 back-to-back meetings with
15-min gaps. Consider consolidating or declining the 2pm optional sync.
```

**Example 3: Pre-work Window Protection**
```
User: "Someone wants to schedule a 7:30 AM meeting tomorrow"
Claude: [Uses time-management]

That's your pre-work window (PEAK energy).
This is your best deep work time — post-workout, before meetings start.

Options:
1. Decline and offer 9:30 AM instead (after standup)
2. Accept only if it's a hard external dependency
3. Accept but block 2:00-3:30 PM as replacement deep work

Recommendation: Option 1. Your pre-work window is sacred.
Tomorrow is Wednesday (meeting-heavy day), so protecting morning
focus time is critical.
```

## Core Workflows

### 1. Daily Planning Ritual (`/today`)

When Sean says "plan my day" or `/today`:

1. **Check the day type** (Focus Day or Meeting Day)
2. **Pull calendar events** (from Google Calendar when connected, or ask Sean to list them)
3. **Identify P0 task** — the single most important thing for today
4. **Slot P0 into peak energy** (7:00-9:00 AM pre-work or first available deep block)
5. **Fill remaining blocks** based on energy map
6. **Output** the plan with time blocks and meeting count

**Planning rules:**
- P0 task ALWAYS goes in peak energy slot (post-workout, pre-work window or early morning)
- Never schedule creative work during the 1-2 PM lull
- Mon/Fri: Protect at least 4 hours of uninterrupted deep work
- Tue-Thu: Accept meeting reality, but batch meetings and protect at least 1.5 hours deep work
- Evening personal project time is optional — don't over-schedule it

### 2. Calendar Audit

Analyze calendar data (CSV/ICS export or Google Calendar API) using Python:

```python
import pandas as pd

def audit_calendar(df: pd.DataFrame) -> dict:
    """Analyze calendar for time allocation and meeting load."""
    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])
    df['duration_hours'] = (df['end'] - df['start']).dt.total_seconds() / 3600

    meetings = df[df['event_type'] == 'meeting']
    deep_work = df[df['event_type'] == 'focus']

    total_work_hours = 40  # 8 hours x 5 days

    return {
        'meeting_hours': meetings['duration_hours'].sum(),
        'meeting_pct': meetings['duration_hours'].sum() / total_work_hours * 100,
        'deep_work_hours': deep_work['duration_hours'].sum(),
        'meeting_count': len(meetings),
        'fragmented_days': count_fragmented_days(df),
    }

def count_fragmented_days(df: pd.DataFrame) -> int:
    """Count days with gaps < 30 min between meetings (Swiss Cheese days)."""
    fragmented = 0
    for date, day_events in df.groupby(df['start'].dt.date):
        meetings = day_events.sort_values('start')
        for i in range(1, len(meetings)):
            gap = (meetings.iloc[i]['start'] - meetings.iloc[i-1]['end']).total_seconds() / 60
            if 0 < gap < 30:
                fragmented += 1
                break
    return fragmented
```

### 3. The PEARL Conflict Resolution

When schedule conflicts arise:

1. **P**rinciples: Health > Deep Work > External Meetings > Internal Meetings > Admin
2. **E**xternal: Is the other party outside The Block? (Hard constraint — keep it)
3. **A**genda: Does the meeting have a clear purpose? (No agenda = decline)
4. **R**anking: Rank by "Cost of Cancellation" (stakeholder impact, deadline proximity)
5. **L**ogistics: Propose specific alternative slots

**Sean's priority hierarchy:**
- Pre-work window (7-9 AM) > Standup (non-negotiable) > 1:1 with manager > Sprint ceremonies > Optional syncs

### 4. Weekly Review Template

Generate in `vault/Areas/Productivity/weekly/`:

```markdown
# Week Review: [Date Range]

## Time Split
- Building: XX% (target: 45%)
- Meetings: XX% (target: 35%)
- Firefighting: XX% (target: 20%)

## Meeting Load
- Total meetings: X (target: 7-8)
- Standup: 5x (daily)
- Other: Xx

## Deep Work Score
- Total deep work hours: XX
- Deep work blocks (>90 min): X
- Fragmented days: X

## Energy Alignment
- Peak energy tasks in AM: X/5 days
- Low-energy lull (1-2 PM) used for admin: X/5 days

## Wins
-

## Friction Points
-

## Next Week Adjustments
- [ ]
```

### 5. Google Calendar Integration

**Current state:** Will connect personal Google Calendar via OAuth (work calendar is synced to personal).

**When connected:**
- Pull events directly for `/today` planning
- Run automated weekly time audits
- Set reminders for subscription renewals (from personal-finance skill)
- Detect meeting creep early (alert if meetings exceed 35% weekly)

**Setup steps (when ready):**
1. Configure Google Calendar MCP server or Zapier Google Calendar tools
2. Grant read access to primary calendar
3. Test with: "What's on my calendar today?"
4. Enable weekly audit automation

### 6. Vault Integration

**Daily note** — append time plan to `vault/Daily/`:
```markdown
## Today's Plan
- **Day type:** Tuesday (Meeting Day)
- **P0:** Campus 201 ticket writing
- **Meetings:** 3 scheduled
- **Deep work:** 2.5 hours protected

## Time Blocks
- 7:00-8:30: Side project (pre-work)
- 9:00-9:30: Standup
- 9:30-11:00: Deep work — Campus 201
- 11:00-12:00: Sprint sync
- 12:00-1:00: Lunch
- 1:00-2:00: Admin/Slack (low energy)
- 2:00-2:30: 1:1
- 2:30-4:00: Zapier automation build
```

## Success Criteria

- [ ] `/today` generates a plan respecting energy map and day type
- [ ] P0 task is always scheduled in peak energy window
- [ ] Time audit correctly calculates 45/35/20 split
- [ ] Fragmentation detection identifies Swiss Cheese days
- [ ] PEARL conflict resolution explains reasoning
- [ ] Weekly review template populated with actual data
- [ ] Pre-work window (7-9 AM) flagged as protected when conflicts arise
- [ ] Google Calendar integration documented for setup

## Copy/Paste Ready

```
"Plan my day"
"What's on my calendar today?"
"How was my time split this week?"
"Am I in too many meetings?"
"Audit my calendar for fragmentation"
"Resolve this scheduling conflict"
"Protect my morning deep work"
"Generate weekly time review"
```