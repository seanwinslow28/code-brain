---
name: sprint-health
description: Ad-hoc Jira status checks for The Block — answer "where are we on Epic X?", "what's the state of PRO-4354?", "what's stuck in the current sprint?", "is this Story actually shipping?". Pulls live data via Atlassian MCP, surfaces percent complete, stale items, blockers, dependency risk, and what needs Sean's attention next. Use when asked about Epic progress, Story status, sprint health, at-risk work, blocked tickets, stale tickets, or "where things stand" on Block engineering work. Not for ticket creation (use jira-automation) or sprint planning (use sprint-roadmap).
---

# Sprint Health — The Block

## Purpose

Answer ad-hoc "where are we?" questions about Block work without leaving Claude Code. Pull live Jira data via Atlassian MCP, compute the right rollup (Epic / Story / Sprint), and surface the small handful of things that actually need Sean's attention — stalled work, blockers, scope drift, missing approvals — instead of dumping the full ticket list.

This skill is for **status queries on existing work**. For ticket creation, use `jira-automation`. For sprint planning and prioritization frameworks, use `sprint-roadmap`.

## When to Use

- **Epic progress:** "Where are we on the Sponsored Courses Epic?" / "What's left on PRO-4354?"
- **Story status:** "What's the state of [Implementation] Homepage Module?" / "Is PRO-4361 actually moving?"
- **Sprint check:** "Quick health check on the current sprint" / "How's Sprint N going?"
- **Stuck work:** "What's stalled?" / "Anything blocked I should know about?"
- **Stale tickets:** "Any tickets going cold in the sprint?" / "What hasn't moved in a week?"
- **Pre-meeting prep:** Before standup, weekly 1:1 with Ed, bi-weekly P&E update, or CPO check-in
- **NeedsDesign queue:** "What's waiting on design?" / "How big is the design backlog?"

## When NOT to Use

- Creating tickets → use `jira-automation`
- Sprint planning, capacity math, RICE/MoSCoW → use `sprint-roadmap`
- Drafting the bi-weekly P&E stakeholder post → use `stakeholder-update`
- Standup agenda or pre-read → use `meeting-prep`

## Examples

**Example 1: Epic rollup**
```
User: "Where are we on PRO-4354?"
Claude: [Uses sprint-health]

Pulling Epic + child issues via Atlassian MCP...

Epic PRO-4354 — Sponsored/Elective Courses Integration
Status: In Progress · 6 of 9 stories Done (67%) · Target: end of Sprint 26

Done (6):
- [Design] Sponsored Courses Integration (PRO-4355)
- [Implementation] Homepage Sponsored Course Module (PRO-4361)
- [Implementation] Learn Page Courses Module (PRO-4362)
- [Implementation] In-Article Recirculation (PRO-4363)
- [Implementation] Course Description Page (PRO-4364)
- [Implementation] X Authentication Integration (PRO-4365)

In flight (2):
- PRO-4366 [Implementation] Campus Deep Linking — Koray, In Progress, last updated 3 days ago
- PRO-4367 [Implementation] Sponsor Lead Data Export — Maria, Ready for Review

At-risk (1):
- PRO-4368 [Implementation] Completion Shareable Social Card — Unassigned, To Do, NeedsDesign label still attached → design dependency unresolved

Recommendation: PRO-4368 needs an owner this week or it slips. Worth a Slack to Ed?
```

**Example 2: Sprint state**
```
User: "Quick health check on the current sprint"
Claude: [Uses sprint-health]

Querying open sprint in PRO via JQL...

Sprint 26 (PRO) — Day 7 of 10
- 28 issues, 18 Done, 6 In Progress, 4 To Do
- 64% complete by count (story points unavailable for some items)
- Pace: roughly on track — needs 5 issues moving to Done in next 3 days

Stale (>3 days no update):
| Key | Title | Assignee | Status |
|---|---|---|---|
| PRO-4389 | [Implementation] Campus nav update | Nikita O. | In Progress (9 days stale) |
| PRO-4401 | [Implementation] Chart tooltip fix | Koray | In Progress (12 days stale) |

Unassigned (1): PRO-4368

Likely needs your attention before Friday: PRO-4401 (12 days stale, no comment activity).
```

**Example 3: Cross-cutting "what's stuck"**
```
User: "What's stuck across our active work?"
Claude: [Uses sprint-health]

Running blocker + stale + NeedsDesign queries across PRO + RBS + BE...

Blockers (flagged):
- PRO-4412 [Bug] Mobile menu overlap — flagged: impediment, owner Maria

Stale >5 days in active sprints:
- PRO-4389 In Progress 9d, PRO-4401 In Progress 12d

NeedsDesign waiting:
- 4 stories with NeedsDesign label, none assigned to a designer
- Oldest: PRO-4350 (created 18 days ago)

Recommendation: NeedsDesign queue is the loudest signal. Worth raising in Wednesday's Brand/Media/Product sync.
```

## The Block Jira Configuration

| Field | Value |
|---|---|
| Instance | `https://theblockcrypto.atlassian.net` |
| Cloud ID | `9660d87e-3943-45c9-82bd-ce963410b29e` |
| Primary projects | `PRO` (P&E, default), `RBS`, `BE` (Block Engineering), `CM`, `GD` (Design), `DE`, `OP` |
| Default project | `PRO` unless user specifies |
| Sprint board source | Open sprints via `sprint in openSprints()` |

For full project / component / label / issue-type config, see [`jira-automation`](../jira-automation/SKILL.md).

## Workflow

### Step 1 — Identify the rollup level

Match the user's request to one of three rollup shapes. If ambiguous, ask once before querying.

| Phrase | Rollup | JQL anchor |
|---|---|---|
| "where are we on PRO-XXXX" (an Epic) | Epic rollup | `parent = PRO-XXXX` |
| "where are we on PRO-XXXX" (a Story) | Story detail | `key = PRO-XXXX` + linked issues |
| "sprint health", "current sprint", "how's the sprint" | Sprint rollup | `sprint in openSprints() AND project = PRO` |
| "what's stuck", "anything blocked", "stale tickets" | Cross-cutting risk scan | multiple queries below |

### Step 2 — Run the right query

| Goal | JQL | MCP tool |
|---|---|---|
| Epic children | `parent = {EPIC} ORDER BY status, updated DESC` | `searchJiraIssuesUsingJql` |
| Story detail | `key = {STORY}` then `getJiraIssue` for full fields | `getJiraIssue` |
| Story sub-tasks / links | `"Epic Link" = {STORY} OR parent = {STORY}` | `searchJiraIssuesUsingJql` |
| Sprint state | `sprint in openSprints() AND project = PRO` | `searchJiraIssuesUsingJql` |
| Stale in sprint | `sprint in openSprints() AND status NOT IN (Done, Closed) AND updated < -3d` | `searchJiraIssuesUsingJql` |
| Blocked | `sprint in openSprints() AND flagged = impediment` | `searchJiraIssuesUsingJql` |
| Unassigned in sprint | `sprint in openSprints() AND assignee IS EMPTY` | `searchJiraIssuesUsingJql` |
| NeedsDesign queue | `project IN (PRO, RBS) AND labels = NeedsDesign AND status NOT IN (Done, Closed) ORDER BY created ASC` | `searchJiraIssuesUsingJql` |
| Cross-project stale | `project IN (PRO, RBS, CM) AND status NOT IN (Done, Closed) AND updated < -7d` | `searchJiraIssuesUsingJql` |

Always pull these fields: `summary, status, assignee, priority, updated, created, labels, components, parent`.

### Step 3 — Compute health signals

For Epic and Sprint rollups, compute:

- **Percent complete** = Done / Total (by issue count; flag if story points are missing)
- **Stale** = In Progress / To Do AND `updated < -3d` for sprint, `< -5d` for cross-project scans
- **At-risk** = stale OR unassigned OR `NeedsDesign` label still attached on a non-Design story
- **Blockers** = `flagged = impediment` OR title/description contains "blocked" / "waiting on"
- **Dependency risk** = linked issues in `Blocks` / `Is blocked by` relationships not yet Done

For Story detail, compute:
- Days since last update + last comment author
- Sub-task / linked-issue completion ratio
- Whether all required fields per `jira-automation` template are populated

### Step 4 — Synthesize the report

Lead with the headline number, then list only items that need attention. Default format:

```markdown
{Rollup name} — {key}
Status: {status} · {N of M} {unit} {state} ({pct}%) · {timing context}

Done ({n}):
- {key} {title}

In flight ({n}):
- {key} {title} — {assignee}, {status}, last updated {Xd} ago

At-risk ({n}):
- {key} {title} — {reason}

Recommendation: {one sentence — what Sean should do or who he should ping}
```

**Rules:**
- Keep "Done" lists tight — collapse to a count + one-line summary if >10 items.
- Always end with a one-sentence recommendation. If nothing needs attention, say so explicitly.
- Reference Block conventions (Ed, the bi-weekly P&E post, Wednesday Brand/Media sync) when surfacing actions.
- Never invent ticket data. If a field is missing in Jira, say "missing" rather than guessing.

### Step 5 — Offer the next step

After the report, offer at most one follow-up action:

- "Want me to draft a Slack to {assignee} asking for a status update?" → `slack-messaging` skill
- "Should I post this to {channel}?" → manual paste, never auto-send
- "Want me to add a comment to {key} flagging the staleness?" → `addCommentToJiraIssue`
- "Want me to break down {Epic} into the missing stories?" → `jira-automation`

Never chain-execute. Wait for confirmation.

## Sean-Specific Cadences (when this skill is most valuable)

These are the natural trigger moments — surface them proactively if the user asks for "a sanity check" or "anything I should know":

| Cadence | When | What to check |
|---|---|---|
| Pre-standup | Tue / Wed / Thu 9:55 AM | "Anything stale or blocked I should mention at standup?" |
| Pre-1:1 with Ed | Weekly | Open Epics + at-risk items in PRO |
| Pre-bi-weekly P&E post | Post day 3:00–4:00 PM | Done / In-flight / Upcoming across PRO + RBS + CM (also see `stakeholder-update`) |
| ETF pipeline check | When `#research-etf` post hits | Status of any open ETF tickets in PRO |
| End of week | Friday afternoon (your lighter day) | Cross-project stale scan, NeedsDesign queue depth |

## MCP Tools Used

| Tool | Purpose |
|---|---|
| `mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql` | All multi-issue rollups |
| `mcp__claude_ai_Atlassian__getJiraIssue` | Story detail, comment thread, full description |
| `mcp__claude_ai_Atlassian__getTransitionsForJiraIssue` | When the user asks "what would move this forward" |
| `mcp__claude_ai_Atlassian__addCommentToJiraIssue` | Only after user confirms |

The `mcp-atlassian` (Docker) variant exposes the same shapes under different names — fall back to those if the `claude_ai_Atlassian` variant is unavailable in the session.

## Anti-Patterns

- **Don't dump every ticket.** Summarize Done lists; spell out only the items that need attention.
- **Don't speculate about "why" a ticket is stuck.** Say "stale 9 days, no comments since [date]" — let Sean infer the cause.
- **Don't auto-comment, auto-transition, or auto-message.** This skill is read-only by default. Writes require explicit confirmation per turn.
- **Don't run a full cross-project scan when the user asked about one Epic.** Match query scope to question scope.
- **Don't substitute for `sprint-roadmap`.** If the user asks for capacity math, RICE scoring, or roadmap generation, hand off.

## Success Criteria

- [ ] Query scope matches the user's question (Epic / Story / Sprint / cross-cutting)
- [ ] Report leads with the headline metric, not a wall of tickets
- [ ] Only at-risk / stale / blocked items get individual lines; Done is summarized
- [ ] Every at-risk line states a reason (stale Xd, unassigned, NeedsDesign waiting, etc.)
- [ ] Closes with exactly one recommendation or "nothing needs attention right now"
- [ ] No tickets created, transitioned, or commented on without explicit confirmation
- [ ] Block conventions (project keys, components, labels, ritual cadences) used correctly

## Copy/Paste Ready

```
"Where are we on PRO-4354?"
"Quick health check on the current sprint"
"What's the state of the Sponsored Courses Epic?"
"Anything stale or blocked I should know about before standup?"
"How big is the NeedsDesign queue right now?"
"What hasn't moved in the sprint this week?"
"Where do things stand on the ETF tracker work?"
"Pre-1:1 with Ed sanity check"
```
