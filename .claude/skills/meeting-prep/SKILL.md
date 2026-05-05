---
name: meeting-prep
description: Meeting prep assistant for Product & Engineering teams. Generates agendas, pre-reads, post-meeting action items, and standup prep. Use when the user mentions "meeting", "standup", "agenda", "1:1", "retro", "pre-read", "action items", or "meeting prep".
---

# Meeting Prep

> **Note:** Configure the team roster, recurring meeting schedule, Jira project keys, and tool references for your organization. The patterns below are organization-agnostic — drop in your specifics.

## Purpose

Automates meeting preparation for recurring Product & Engineering meetings. Generates agendas, pre-reads, and post-meeting action items tailored to each meeting type. Reusable across organizations — fill in the team roster, cadence, and tool stack.

## When to Use

- **Standup Prep:** "Prep for standup" / "What's the team working on?"
- **1:1 Prep:** "Prep for my 1:1 with [Name]"
- **Retro Prep:** "Set up the monthly retro"
- **Design Sync:** "Agenda for the product-design sync"
- **General:** "Create an agenda for [meeting]" / "Write action items from [meeting]"

## Recurring Meeting Templates

Configure in your project context (CLAUDE.md or a local profile):

| Meeting | Cadence | Time | Attendees | Owner |
|---------|---------|------|-----------|-------|
| Daily Standup | Mon-Fri | [time] | [list] | [person] |
| 1:1 with manager | Bi-weekly | Flexible | You + manager | manager |
| 1:1 with peer / report | Weekly | [time] | You + peer | shared |
| Product + Design Sync | Weekly | [day/time] | Product + Design | shared |
| Cross-team check-in | Bi-weekly | [time] | You + team | shared |
| Monthly Retro | Monthly | [time] | Full team | manager |

### Team Roster (template)

Maintain a roster in your project context with name + role + focus area. Skill consults the roster for round-robin order in standup prep and assignee-aware JQL in 1:1 prep.

### Tools (configure)

- **Jira / Linear:** Ticket tracking, standup prep (filter by assignee), sprint boards
- **Confluence / Notion:** Meeting notes, status updates, project documentation
- **Slack:** Quick updates, async follow-ups, meeting summaries
- **Google Docs/Sheets:** Shared trackers, agendas, planning docs
- **Your retro tool:** Monthly retrospectives
- **Figma:** Design handoffs and review

## Examples

**Example 1: Standup Prep**
```
User: "Prep for standup"
Claude: [Uses meeting-prep]

Daily Standup Prep — [Date]

To lead the round-robin, here's each team member's Jira status:
(Querying Jira for in-progress tickets by assignee...)

Suggested run order:
1. [Member 1] — [tickets]
2. [Member 2] — [tickets]
...

Blockers to surface: [any flagged/impeded tickets]

Your updates to share:
- Working on: [your current Jira tickets]
- Flagging: [any blockers or questions for the team]
```

**Example 2: 1:1 with Manager**
```
User: "Prep for my 1:1 with [manager]"
Claude: [Uses meeting-prep]

1:1 with [Manager] — Bi-weekly

Suggested agenda:
1. Status update review
   - Items to flag for review

2. Current focus area
   - Live blockers/timeline

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
Platform: [your retro tool]

Setup:
1. Create new retro board in your retro tool
2. Share link in Slack

Format (team morale + process check-in):
- How are you feeling? (check-in)
- What went well this month?
- What could be improved?
- Any shoutouts?

Post-retro: Capture action items, share summary in Slack,
follow up at next standup.
```

## Core Workflows

### 1. Daily Standup Prep

**Before standup:**
1. Query Jira for in-progress tickets by assignee (use `mcp-atlassian` jira_search preferred, or `claude.ai Atlassian` as fallback)
2. Check for any flagged/impeded tickets
3. Note any PRDs or design tickets that need discussion
4. Prepare your own status update

**JQL template for standup prep** (replace `<PROJECT_KEYS>` with your project keys):
```jql
project IN (<PROJECT_KEYS>)
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

## Career/Growth (for 1:1 with manager)
- [Learning, development, feedback]

## Action Items from Last Time
- [ ] [Carry-forward item]
```

### 3. Product + Design Sync

**Typical agenda:**
1. Design reviews — completed designs ready for dev handoff?
2. Upcoming design needs — new PRDs requiring design?
3. Figma status — open design tickets?
4. Cross-team dependencies

**JQL template for design ticket status:**
```jql
project IN (<PROJECT_KEYS>) AND labels = NeedsDesign
AND status NOT IN (Done, Closed)
ORDER BY priority DESC
```

### 4. Cross-team Check-ins

Configurable templates for SEO, RevOps, AdOps, Data, etc. Each follows the same shape: agenda items, recent metrics, current asks, open follow-ups.

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

**Where to post:** Quick items → Slack | Formal decisions → Confluence/Notion | Ticket-related → Jira/Linear comments

**Action item tracking:** After each meeting, update the status column. At the next meeting, review open items first. If an action item stalls for >1 week, escalate or convert to a Jira ticket via `jira-automation`.

### 6. Post-Retro Synthesis

After the monthly retro, synthesize outcomes:

**Step 1 — Extract themes:**
1. Export or screenshot the retro board
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
| 1 | [Improvement] | @[name] | [date] | [TICKET-ID] |

## Shoutouts
- [Name] — [reason]

## Carry-Forward
- [Unresolved items from last retro]
```

**Step 3 — Link to backlog:**
- Convert process improvements to Jira tickets (use `jira-automation`)
- Add "Retro Follow-up" as a standing standup agenda item for the following week
- Post synthesis to Confluence/Notion and share link in Slack

**Step 4 — Track at next retro:**
- Open with "Last month we said we'd..." review
- Mark completed items, escalate stalled ones

### 7. Meeting Necessity Check

Before creating any new meeting:
1. **Could this be a Slack message?** → Write it in Slack instead
2. **Could this be a doc with async comments?** → Write it up
3. **Does it need real-time discussion?** → Schedule the meeting
4. **Is it a recurring need?** → Add to the regular schedule

Protect deep-work days from meeting creep. Concentrate meetings on 2-3 days when possible.

## Success Criteria

- [ ] Standup prep queries Jira/Linear for team member status
- [ ] 1:1 agendas include carry-forward items from previous meeting
- [ ] Meeting type correctly identified (standup vs 1:1 vs retro vs sync)
- [ ] Action items have owners AND due dates
- [ ] Post-meeting output posted to correct channel (Slack/Confluence/Jira)
- [ ] Monthly retro synthesis produces themed action items

## Copy/Paste Ready

```
"Prep for standup"
"Prep for my 1:1 with [name]"
"Prep for my [day] meeting with [name]"
"Set up the monthly retro"
"Agenda for the product-design sync"
"Write action items from today's standup"
"What meetings do I have this week?"
```
