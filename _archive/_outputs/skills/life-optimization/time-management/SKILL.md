---
name: time-management
description: Time management and calendar optimization assistant. Audits calendar exports for fragmentation, facilitates daily planning (`/today`), and resolves scheduling conflicts using the PEARL framework. Use this skill when the user mentions "calendar", "audit my time", "schedule", "meeting prep", or "time blocking".
---

# Time Management & Calendar Optimization

## Purpose

Optimizes your most scarce resource. This skill audits calendar data to find fragmentation, automates daily planning rituals, and resolves scheduling conflicts using explicit prioritization rules.

## When to Use

- **Daily Planning:** Start of day ("Plan my day").
- **Time Audit:** "Where did my time go last month?"
- **Conflict Resolution:** "I have two meetings at 2pm."
- **Meeting Prep:** "Prepare me for the 3pm sync."

## Examples

**Example 1: Time Audit**
```
User: "Audit my calendar for last month. I feel like I got nothing done."
Claude: [Uses time-management] Running `audit_calendar.py` on `calendar_export.csv`...

**Time Audit Results (October):**
- **Deep Work:** 12 hours (Only 8% of work time) 🚨
- **Meetings:** 85 hours (60%!)
- **Fragmentation:** You had 14 "Swiss Cheese" days with gaps < 30 mins.

**Recommendation:** Decline recurring meetings on Tuesday/Thursday mornings to reclaim deep work blocks.
```

**Example 2: Daily Planning (`/today`)**
```
User: "Plan my day."
Claude: [Uses time-management] Analyzing context...
- **Must Do:** Ship PRD (P0).
- **Hard Landscape:** Meetings at 10am, 2pm, 3pm.

**Proposed Schedule:**
- 09:00 - 10:00: Deep Work (Ship PRD)
- 10:00 - 11:00: Meeting (Team Sync)
- 11:00 - 12:00: Admin (Email/Slack)
- 12:00 - 13:00: Lunch
- 13:00 - 14:00: Deep Work (PRD Polish)
- 14:00 - 16:00: Meeting Block
```

## Time Management Workflow

### 1. The Calendar Audit

Use the `audit_calendar.py` script to analyze CSV/ICS exports from Google Calendar.

**Metric Definitions:**
*   **Deep Work:** Events > 90 mins with no "Meeting" keywords.
*   **Context Switch Cost:** 15 mins lost before/after every meeting.
*   **Meeting Load:** Total hours in calls.

```bash
python3 scripts/audit_calendar.py --input calendar.csv --focus "Deep Work"
```

### 2. The PEARL Conflict Resolution

When asked to fix a schedule conflict, apply the **PEARL** logic:
1.  **P**rinciples: Check `CLAUDE.md` (e.g., "Health > Work").
2.  **E**xternal: Is the other party external? (Hard constraint).
3.  **A**genda: Does the meeting have a clear purpose?
4.  **R**anking: Rank by "Cost of Cancellation".
5.  **L**ogistics: Propose specific slots to move usage.

### 3. Daily Planning Ritual

Generate a daily plan that respects **Energy Management**, not just time.
*   *Morning:* Creative / Hardest Task.
*   *Mid-day:* Collaborative / Meetings.
*   *Late Afternoon:* Admin / Low Energy.

### 4. Meeting Prep Automation

When asked to "prepare for X", do not just summarize.
1.  Who is attending? (Read Bio/Context).
2.  What is the goal?
3.  What are the open questions from last time?

## Success Criteria

- [ ] Audit script correctly identifies "Deep Work" blocks (>90m).
- [ ] Daily plans always schedule the "P0" task in the morning (or first available deep slot).
- [ ] Conflict resolution explains *why* one meeting was chosen over another.

## Copy/Paste Ready

```
"Audit my calendar for fragmentation."
"Plan my day based on my todos."
"Resolve this scheduling conflict."
"Prepare me for the weekly sync."
```
