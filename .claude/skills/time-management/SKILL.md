---
name: time-management
description: Time management and calendar optimization assistant for Sean's job-hunt sprint (post-Block, 2026-05). Plans daily schedules around the 5:30 AM wake / 8:30 AM–12:30 PM deep-work block / 5:30 PM hard stop, organizes the week into Track A (logistics) / Track B (pipeline) / Track C (MCP server) shape, and runs the Friday weekly retro. Use this skill when the user mentions "calendar", "audit my time", "schedule", "plan my day", "today", "time blocking", "weekly retro", "deep work", or "when should I".
---

# Time Management & Calendar Optimization (Job-Hunt Mode)

## Purpose

Optimizes Sean's most scarce resource — attention — during the 8-week job-hunt sprint that started 2026-05-04 (post-Block layoff). Calibrated to the rhythm in `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md` Phase 7 (the master plan's daily/weekly rhythm section is the source of truth). When Sean signs an offer and enters a new role, this skill should be re-rewritten then.

## When to Use

- **Daily Planning:** "Plan my day" / `/today`
- **Weekly Retro:** "Run the Friday retro" / "Weekly review"
- **Time Audit:** "Where did my time go last week?" / "Am I drowning in applications?"
- **Conflict Resolution:** "I have an interview that conflicts with deep-work block"
- **Deep Work Protection:** "Protect my morning"
- **Hard-stop enforcement:** "What should I drop after 5:30 PM?"

## Sean's Schedule (Job-Hunt Mode)

### Daily Rhythm (Weekdays)

```
5:30 AM   — Wake
5:30–6:30 AM — Sacred first hour (coffee, breakfast prep, green juice, vitamins)
6:30–7:00 AM — Movement / gym (when energy allows)
7:00–8:30 AM — Morning routine completion + intent review
8:30 AM–12:30 PM — DEEP WORK BLOCK (track-of-the-day work)
12:30–1:30 PM — Lunch
1:30–5:30 PM — Flexible PM (interviews, async work, lighter tasks)
5:30 PM   — HARD STOP (non-negotiable)
5:30–9:30 PM — Mary / dinner / decompression / optional creative
~9:30 PM  — Bed
```

**The 8:30 AM–12:30 PM block is sacred.** If a recruiter or interview can't be moved out of this window, accept it but flag the displacement and reschedule the deep work to a flexible PM slot.

**5:30 PM hard stop is non-negotiable.** The daily-driver agent should respect this — no proposing tasks past 5:30 PM, no nag-style reminders that breach it. Job-hunt logistics that arrive after 5:30 PM go on tomorrow's plan.

### Weekly Track Structure

Don't try to multitask the three tracks in a single day. Each day has one dominant track.

| Day | Track | Focus |
|-----|-------|-------|
| **Monday** | Track A logistics + Track B positioning | Severance / health / runway admin AM. PM: refine resume / LinkedIn / portfolio narrative for the week's applications. |
| **Tuesday** | Track B applications | Apply to N companies (target 5-10 quality apps). Tailor each cover letter to the role. |
| **Wednesday** | Track A + Track B positioning | Same shape as Monday — second logistics window mid-week, second positioning pass for late-week apps. |
| **Thursday** | Track B applications | Second weekly application batch. Outreach to warm-20 list (LinkedIn DMs, intro asks). |
| **Friday** | Track C MCP server + retro | MCP server / portfolio differentiation work AM. **Weekly retro 4:30–5:30 PM.** |

Weekend: rest. Optional creative if energy is high. No application-pushing on weekends — applicants get reviewed Monday anyway.

### Weekly Retro (Friday 4:30–5:30 PM)

The cadence anchor for the entire job hunt. Three numbers + three reflections + one headline goal:

**Three numbers (the leading indicators):**
1. **Applications submitted this week:** N
2. **Conversations had** (recruiter calls, intros, networking coffees): N
3. **Interviews booked / completed:** N

**Three reflections:**
1. **What worked this week?**
2. **What didn't work?**
3. **One non-job-hunt win** (creative ship, family time, health milestone, learning) — keep the cushion-quote north-star alive.

**One thing for next week:**
- **Headline goal for next week:** [single sentence]

Write the output to `vault/20_projects/prj-job-hunt-2026/retros/YYYY-WW.md` (create the folder if needed).

## Examples

**Example 1: Daily Planning (Tuesday — Track B applications day)**
```
User: "Plan my day"
Claude: [Uses time-management]

It's Tuesday — Track B (Applications). Here's your plan:

MORNING ROUTINE (5:30–8:30 AM)
  Sacred first hour, gym, intent review

DEEP WORK BLOCK (8:30 AM–12:30 PM) — Applications
  [1] Tailor cover letters for 5 target roles (90 min)
  [2] Submit applications via company portals (60 min)
  [3] Update prj-job-hunt-2026/applications.md tracker (30 min)
  [4] Buffer / energy reset (30 min)

LUNCH (12:30–1:30 PM)

FLEXIBLE PM (1:30–5:30 PM)
  - Recruiter calls if scheduled
  - Warm-20 outreach (LinkedIn DMs, intro asks)
  - Light admin

HARD STOP (5:30 PM)
  Mary, decompression, optional creative

Today's headline: 5+ quality apps submitted by 12:30.
```

**Example 2: Weekly Retro**
```
User: "Run the Friday retro"
Claude: [Uses time-management]

Weekly Retro — Week of [start date]–[end date]

Three numbers:
1. Applications submitted: ___
2. Conversations: ___
3. Interviews booked / completed: ___

Reflect:
1. What worked this week?
2. What didn't?
3. One non-job-hunt win:

Next week's headline goal:

Writing to vault/20_projects/prj-job-hunt-2026/retros/...
```

**Example 3: Conflict — interview during deep-work block**
```
User: "Recruiter wants a screen Wednesday at 10:30 AM"
Claude: [Uses time-management]

Wednesday 10:30 AM is inside your sacred deep-work block (8:30–12:30).
Track A logistics + Track B positioning is Wednesday's shape — interrupted by a 30-min screen, you'll lose ~90 min total to context switching.

Options:
1. Counter-propose Wednesday 1:30 PM or 2:00 PM (your flexible PM is wide open)
2. Counter-propose Tuesday 1:30 PM (Tuesday is applications day, but PM is flexible)
3. Accept 10:30 AM if it's a hard external constraint, and reschedule Wednesday's positioning work to Wednesday PM

Recommendation: Option 1. Recruiters are generally flexible inside business hours and asking for 1:30 PM signals you have other commitments.
```

## Core Workflows

### 1. Daily Planning Ritual (`/today`)

When Sean says "plan my day" or `/today`:

1. **Identify the day's track** (A logistics + B positioning / B applications / C + retro)
2. **Pull calendar events** from `sean.winslow28@gmail.com` (single calendar — the Block work calendar archived 2026-05)
3. **Confirm 8:30 AM–12:30 PM is protected** for the track's deep work
4. **List interviews / recruiter calls** in the flexible PM slot (1:30–5:30 PM)
5. **Today's headline** — one sentence, what makes today successful
6. **Hard stop reminder** — 5:30 PM, non-negotiable

**Planning rules:**
- Deep work goes in 8:30 AM–12:30 PM. If displaced by an interview, reschedule to PM and flag the displacement count for the weekly retro.
- Friday retro (4:30–5:30 PM) is non-negotiable. Block the rest of Friday afternoon if needed to make room.
- Don't book recruiter calls past 5:00 PM (gives a 30-min buffer to the hard stop).
- Weekend planning: rest by default. Only schedule weekend tasks if Sean explicitly asks.

### 2. Calendar Audit (Job-Hunt Mode)

The relevant signal in this mode is application + interview throughput, not meetings-as-percentage-of-week. Reframe the audit:

- **Interviews this week:** count
- **Recruiter conversations:** count
- **Applications submitted:** count
- **Deep-work-block completion ratio:** (# of days protected) / (5)
- **Hard-stop violations:** how many days went past 5:30 PM (target: 0)
- **Weekend non-job-hunt time:** target 100% recovery / Mary / creative

When Sean asks "where did my time go last week?", report against these dimensions, not against the old 45/35/20 split.

### 3. Protect / Automate / Decline Triage

Same shape as the prior life-systems schedule-recommendations exercise, recalibrated for job-hunt mode:

**Protect (don't move under any circumstances):**
- 8:30 AM–12:30 PM deep work
- Friday 4:30–5:30 PM retro
- 5:30 PM hard stop

**Automate (delegate to the daily-driver / vault flow):**
- Daily note skeleton creation
- Application tracker updates after submission
- Retro skeleton generation Friday afternoon

**Decline (say no, even if it stings):**
- Networking coffees that don't move toward target archetype (AI PM > Tech PM > Creative PM)
- Cold-recruiter spam for roles outside Boston metro / remote
- Anything that breaches the 5:30 PM hard stop

### 4. PEARL Conflict Resolution (post-Block)

1. **P**rinciples: Health > Mary > Deep Work > Interviews > Recruiter calls > Admin > Networking coffees > Cold outreach
2. **E**xternal: Is the other party a hiring manager / signed-on recruiter? (Hard constraint — keep it)
3. **A**genda: Is there a clear decision or info exchange? (No agenda = decline)
4. **R**anking: Rank by "Cost of Cancellation" (target-archetype companies > tier-2 companies > generic recruiter screens)
5. **L**ogistics: Propose specific alternative slots inside the flexible PM window

### 5. Weekly Retro Workflow

Every Friday 4:30–5:30 PM:

1. Open the retros folder (`vault/20_projects/prj-job-hunt-2026/retros/`)
2. Create `YYYY-WW.md` from the template
3. Pull this week's numbers from the applications tracker
4. Sean fills in the three reflections
5. Sean writes next week's headline goal
6. Save + commit

The retro is the consumer side of the weekly loop — it tells Monday-morning Sean what to focus on.

## Vault Integration

**Daily note** — append today's plan to `vault/10_timeline/daily/YYYY-MM-DD.md`:
```markdown
## Today's Plan
- **Track:** Tuesday — B (Applications)
- **Headline:** 5+ quality apps submitted by 12:30
- **Interviews:** 0 scheduled
- **Deep-work block protected:** Yes / [displaced + new slot]

## Time Blocks
- 5:30–8:30: Morning routine
- 8:30–12:30: Deep work — applications
- 12:30–1:30: Lunch
- 1:30–5:30: Flex PM (recruiter calls + outreach)
- 5:30: HARD STOP
```

**Retro note** — `vault/20_projects/prj-job-hunt-2026/retros/YYYY-WW.md`.

## Success Criteria

- [ ] `/today` plan reflects the day's track (A+B / B / B / B / C+retro)
- [ ] 8:30 AM–12:30 PM deep-work block is always blocked
- [ ] 5:30 PM hard stop is enforced (nothing scheduled past it without explicit override)
- [ ] Friday retro fires every Friday 4:30–5:30 PM
- [ ] Weekly retro captures 3 numbers + 3 reflections + 1 headline goal
- [ ] Single-calendar query (`sean.winslow28@gmail.com` only — no Block work calendar)
- [ ] Audit reframed to job-hunt-mode dimensions, not 45/35/20

## Copy/Paste Ready

```
"Plan my day"
"What's on my calendar today?"
"Run the Friday retro"
"Where did my time go last week?"
"Protect my morning deep work"
"Resolve this scheduling conflict"
"What should I drop after 5:30?"
```
