---
name: meeting-prep
description: Meeting prep assistant for The Block's Product & Engineering team. Generates agendas, pre-reads, post-meeting action items, and standup prep. Knows Sean's recurring meeting schedule (daily standup, 1:1s, retros, design syncs, SEO check-ins). Use when the user mentions "meeting", "standup", "agenda", "1:1", "retro", "pre-read", "action items", "meeting prep", or any team member name.
---

# Meeting Prep — The Block

> **Note:** This skill is configured for The Block. If exporting to another project, customize the team roster, meeting schedule, Jira project keys, and tool references for your organization.

## Purpose

Automates meeting preparation for Sean's recurring Product & Engineering meetings at The Block. Generates agendas, pre-reads, and post-meeting action items tailored to each meeting type. Knows the team roster, meeting cadence, and tools (Jira, Confluence, Slack, Retros.work).

## When to Use

- **Standup Prep:** "Prep for standup" / "What's the team working on?"
- **1:1 Prep:** "Prep for my 1:1 with Ed" / "1:1 with David"
- **Retro Prep:** "Set up the monthly retro"
- **Design Sync:** "Agenda for tomorrow's product-design sync"
- **General:** "Create an agenda for [meeting]" / "Write action items from [meeting]"

## Sean's Meeting Schedule

### Recurring Meetings

| Meeting | Cadence | Time | Attendees | Owner |
|---------|---------|------|-----------|-------|
| Daily Standup | Mon-Fri | 10:00-10:45 AM ET | Sean, Ed, Dev team | Sean (leads) |
| 1:1 with Ed Rupkus | Bi-weekly | Flexible | Sean + Ed | Ed |
| 1:1 with David Debreczeni | Weekly (Thu) | 8:00 AM ET | Sean + David | David |
| Product + Design Sync | Weekly (Tue) | Flexible | Product team + Design team | Shared |
| SEO Team Check-in | Bi-weekly | Flexible | Sean + SEO team | Shared |
| Ad Manager/Rev-ops Check-in | Bi-weekly | Flexible | Sean + GAM/Rev-ops team | Shared |
| Monthly Retro | Monthly | After standup | Full P&E team | Ed |

### Team Roster

**Product:**
- **Sean Winslow** — Associate Product Manager (leads standup, owns Campus + .Co tickets)
- **Edvinas Rupkus (Ed)** — Product Manager (Sean's manager, owns roadmap + bi-weekly update)

**Design:**
- **Claudine Daumur** — Product Designer
- **Serena Ho** — Product Designer
- **Josh Gragg** — Director of Design, Product Department

**Engineering (Campus focus):**
- **Nikita Orobenko** — Engineering/Development
- **Aliaksandr Kryvanosau** — Engineering/Development
- **Nikita Gulis** — Engineering/Development

**Engineering (.Co focus):**
- **Koray Baspinar** — Engineering/Development
- **Maria Zhynko** — Engineering/Development
- **Marina Ardytskaya** — Engineering/Development
- **Nikola Pivcevic** — Software Engineer
- **Bohdan Panasenko** — Engineering/Development
- **Brian Mendoza** — Software Engineer

**DevOps:**
- **Cesar Paz** — DevOps (Jira/Slack integration, staging environments)

**QA:**
- **Ramuald Vishneuski** — QA/AQA Engineer (Vention)
- **Ana Benitez** — QA Engineer

**Leadership:**
- **Matt Vitebsky** — VP of Product and Engineering

**Campus Stakeholder:**
- **David Debreczeni** — Senior Manager, Course Design & Compliance

### Tools

- **Jira:** Ticket tracking, standup prep (filter by assignee), sprint boards
- **Confluence:** Meeting notes, bi-weekly updates, project documentation
- **Slack:** Quick updates, async follow-ups, meeting summaries
- **Google Docs/Sheets:** Shared trackers, agendas, planning docs
- **Retros.work:** Monthly retrospectives (https://retros.work/)
- **Figma:** Design handoffs and review

## Examples

**Example 1: Standup Prep**
```
User: "Prep for standup"
Claude: [Uses meeting-prep]

Daily Standup Prep — Tuesday, Feb 18

To lead the round-robin, here's each team member's Jira status:
(Querying Jira for in-progress tickets by assignee...)

Suggested run order:
1. Nikita O. (Campus) — [tickets]
2. Aliaksandr (Campus) — [tickets]
3. Nikita G. (Campus) — [tickets]
4. Koray (.Co) — [tickets]
5. Maria (.Co) — [tickets]
...

Blockers to surface: [any flagged/impeded tickets]

Your updates to share:
- Working on: [your current Jira tickets]
- Flagging: [any blockers or questions for the team]

Tip: Today is Tuesday (Meeting Day). You also have
Product+Design sync later — note any design dependencies.
```

**Example 2: 1:1 with Ed**
```
User: "Prep for my 1:1 with Ed"
Claude: [Uses meeting-prep]

1:1 with Ed Rupkus — Bi-weekly

Suggested agenda:
1. Bi-weekly update review
   - Draft status: [check if bi-weekly update is due]
   - Items to flag for Ed's review

2. Campus 201 status
   - Enterprise version: live
   - Public launch: [current blockers/timeline]

3. Current work
   - Your open tickets: [query Jira]
   - Anything to escalate?

4. Career/growth
   - [Any topics you want to raise]

5. Open items
   - [Carry-forward from last 1:1]
```

**Example 3: Monthly Retro**
```
User: "Set up the monthly retro"
Claude: [Uses meeting-prep]

Monthly Retro — [Date]
Platform: Retros.work (https://retros.work/)

Setup:
1. Create new retro board at retros.work
2. Share link in Slack

Format (team morale + process check-in):
- How are you feeling? (check-in)
- What went well this month?
- What could be improved?
- Any shoutouts?

Post-retro: Capture action items in Confluence,
share summary in Slack, follow up at next standup.
```

## Core Workflows

### 1. Daily Standup Prep

Sean leads standup via round-robin through each team member's Jira board.

**Before standup:**
1. Query Jira for in-progress tickets by assignee (use `mcp-atlassian` jira_search preferred, or `claude.ai Atlassian` as fallback)
2. Check for any flagged/impeded tickets
3. Note any PRDs or design tickets that need discussion
4. Prepare Sean's own status update

**JQL for standup prep:**
```jql
project IN (PRO, RBS, CM)
AND status IN ("In Progress", "Ready for Review", "Ready for Testing", "In Test")
AND assignee = "[memberName]"
ORDER BY updated DESC
```

**Standup structure:**
- Round-robin by name (filter each person's Jira board)
- Each person: what they're working on + any blockers
- Surface flagged/impeded tickets
- Note action items for follow-up

### 2. 1:1 Prep Template

```markdown
# 1:1 with [Name] — [Date]

## Status Updates
- [Your recent completed work]
- [Current in-progress items]

## Discussion Topics
- [ ] [Topic 1]
- [ ] [Topic 2]

## Blockers/Escalations
- [Anything that needs their help]

## Career/Growth (for 1:1 with Ed)
- [Learning, development, feedback]

## Action Items from Last Time
- [ ] [Carry-forward item]
```

### 3. Product + Design Sync (Tuesday)

**Typical agenda:**
1. Design reviews — completed designs ready for dev handoff?
2. Upcoming design needs — new PRDs requiring design?
3. Figma status — open design tickets?
4. Cross-team dependencies

**JQL for design ticket status:**
```jql
project IN (PRO, GD) AND labels = NeedsDesign
AND status NOT IN (Done, Closed)
ORDER BY priority DESC
```

### 4. SEO / Ad Manager Check-ins (Bi-weekly)

**SEO topics:** SEO performance (GA4), content optimization, technical SEO (Nuxt 4 migration), page indexing
**Ad Manager topics:** GAM ad unit performance, revenue metrics, new ad placements, advertiser requests

### 5. Post-Meeting Action Items

```markdown
# [Meeting Name] — Action Items — [Date]

## Decisions Made
- [Decision 1]: [outcome]

## Action Items
| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | [Task] | @[name] | [date] | Open |

## Follow-up Needed
- [Item for next meeting]
```

**Where to post:** Quick items → Slack | Formal decisions → Confluence | Ticket-related → Jira comments

**Action item tracking:** After each meeting, update the status column. At the next meeting, review open items first. If an action item stalls for >1 week, escalate or convert to a Jira ticket via `jira-automation`.

### 6. Post-Retro Synthesis

After the monthly retro (run on Retros.work), synthesize outcomes:

**Step 1 — Extract themes:**
1. Export or screenshot the Retros.work board
2. Group feedback into 3-5 themes (e.g., "deploy process", "cross-team communication", "tooling")
3. Count votes/reactions per theme to rank by team priority

**Step 2 — Assign action items:**
```markdown
# Monthly Retro Synthesis — [Month Year]

## Top Themes
1. **[Theme]** (X votes) — [1-sentence summary]
2. **[Theme]** (X votes) — [1-sentence summary]

## Action Items
| # | Action | Owner | Due | Jira |
|---|--------|-------|-----|------|
| 1 | [Improvement] | @[name] | [date] | PRO-XXXX |
| 2 | [Improvement] | @[name] | [date] | — |

## Shoutouts
- [Name] — [reason]

## Carry-Forward
- [Unresolved items from last retro]
```

**Step 3 — Link to backlog:**
- Convert process improvements to Jira tickets (use `jira-automation`, label: `ToGroom`)
- Add "Retro Follow-up" as a standing standup agenda item for the following week
- Post synthesis to Confluence and share link in Slack

**Step 4 — Track at next retro:**
- Open with "Last month we said we'd..." review
- Mark completed items, escalate stalled ones

### 6. Meeting Necessity Check

Before creating any new meeting:
1. **Could this be a Slack message?** → Write it in Slack instead
2. **Could this be a Confluence doc with async comments?** → Write it up
3. **Does it need real-time discussion?** → Schedule the meeting
4. **Is it a recurring need?** → Add to the regular schedule

Sean's meetings are concentrated Tue-Thu. Protect Mon/Fri for deep work.

## Success Criteria

- [ ] Standup prep queries Jira for team member status
- [ ] 1:1 agendas include carry-forward items from previous meeting
- [ ] Meeting type correctly identified (standup vs 1:1 vs retro vs sync)
- [ ] Action items have owners AND due dates
- [ ] Post-meeting output posted to correct channel (Slack/Confluence/Jira)
- [ ] Monthly retro uses Retros.work
- [ ] Team roster accurate (17 members)
- [ ] Meeting schedule respects Mon/Fri deep work days

## Copy/Paste Ready

```
"Prep for standup"
"Prep for my 1:1 with Ed"
"Prep for my Thursday meeting with David"
"Set up the monthly retro"
"Agenda for the product-design sync"
"Write action items from today's standup"
"What meetings do I have this week?"
```