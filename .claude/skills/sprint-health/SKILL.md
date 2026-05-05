---
name: sprint-health
description: Ad-hoc Jira status checks — answer "where are we on Epic X?", "what's the state of [TICKET-ID]?", "what's stuck in the current sprint?", "is this Story actually shipping?". Pulls live data via Atlassian MCP, surfaces percent complete, stale items, blockers, dependency risk, and what needs attention next. Use when asked about Epic progress, Story status, sprint health, at-risk work, blocked tickets, stale tickets, or "where things stand" on engineering work. Not for ticket creation (use jira-automation) or sprint planning (use sprint-roadmap).
---

# Sprint Health

> **Configure:** Set `<PROJECT_KEY>` and `<PROJECT_KEYS>` to match your team's Jira projects (e.g. PROJ, ENG, RBS). Set the Atlassian instance URL + cloud ID in your project context (CLAUDE.md or local profile). Patterns below are organization-agnostic.

## Purpose

Answer ad-hoc "where are we?" questions about engineering work without leaving Claude Code. Pull live Jira data via Atlassian MCP, compute the right rollup (Epic / Story / Sprint), and surface the small handful of things that actually need attention — stalled work, blockers, scope drift, missing approvals — instead of dumping the full ticket list.

This skill is for **status queries on existing work**. For ticket creation, use `jira-automation`. For sprint planning and prioritization frameworks, use `sprint-roadmap`.

## When to Use

- **Epic progress:** "Where are we on the [Epic Name]?" / "What's left on [TICKET-ID]?"
- **Story status:** "What's the state of [Implementation] [Story Name]?" / "Is [TICKET-ID] actually moving?"
- **Sprint check:** "Quick health check on the current sprint" / "How's Sprint N going?"
- **Stuck work:** "What's stalled?" / "Anything blocked I should know about?"
- **Stale tickets:** "Any tickets going cold in the sprint?" / "What hasn't moved in a week?"
- **Pre-meeting prep:** Before standup, weekly 1:1, or a stakeholder update
- **NeedsDesign queue:** "What's waiting on design?" / "How big is the design backlog?"

## When NOT to Use

- Creating tickets → use `jira-automation`
- Sprint planning, capacity math, RICE/MoSCoW → use `sprint-roadmap`
- Drafting a stakeholder update → use `stakeholder-update`
- Standup agenda or pre-read → use `meeting-prep`

## Examples

**Example 1: Epic rollup**
```
User: "Where are we on <PROJECT_KEY>-XXXX?"
Claude: [Uses sprint-health]

Pulling Epic + child issues via Atlassian MCP...

Epic <PROJECT_KEY>-XXXX — [Epic Name]
Status: In Progress · 6 of 9 stories Done (67%) · Target: end of Sprint N

Done (6):
- [Design] [Story 1] (<PROJECT_KEY>-XXXX)
- [Implementation] [Story 2] (<PROJECT_KEY>-XXXX)
...

In flight (2):
- <PROJECT_KEY>-XXXX [Implementation] [Story Title] — [assignee], In Progress, last updated 3 days ago
- <PROJECT_KEY>-XXXX [Implementation] [Story Title] — [assignee], Ready for Review

At-risk (1):
- <PROJECT_KEY>-XXXX [Implementation] [Story Title] — Unassigned, To Do, NeedsDesign label still attached → design dependency unresolved

Recommendation: <PROJECT_KEY>-XXXX needs an owner this week or it slips. Worth a Slack to the manager?
```

**Example 2: Sprint state**
```
User: "Quick health check on the current sprint"
Claude: [Uses sprint-health]

Querying open sprint via JQL...

Sprint N — Day 7 of 10
- 28 issues, 18 Done, 6 In Progress, 4 To Do
- 64% complete by count (story points unavailable for some items)
- Pace: roughly on track — needs 5 issues moving to Done in next 3 days

Stale (>3 days no update):
| Key | Title | Assignee | Status |
|---|---|---|---|
| <PROJECT_KEY>-XXXX | [Implementation] [Title] | [name] | In Progress (9 days stale) |

Likely needs attention before Friday: [stalest ticket]
```

**Example 3: Cross-cutting "what's stuck"**
```
User: "What's stuck across our active work?"
Claude: [Uses sprint-health]

Running blocker + stale + NeedsDesign queries across all active projects...

Blockers (flagged):
- <PROJECT_KEY>-XXXX [Bug] [Title] — flagged: impediment, owner [name]

Stale >5 days in active sprints:
- ...

NeedsDesign waiting:
- N stories with NeedsDesign label, none assigned to a designer
- Oldest: <PROJECT_KEY>-XXXX (created 18 days ago)
```

## Jira Configuration (set per project)

| Field | Value |
|---|---|
| Instance | `https://<your-instance>.atlassian.net` |
| Cloud ID | (from `getAccessibleAtlassianResources`) |
| Primary projects | `<PROJECT_KEY>` (default), plus any others your team uses |
| Default project | `<PROJECT_KEY>` unless user specifies |
| Sprint board source | Open sprints via `sprint in openSprints()` |

For full project / component / label / issue-type config patterns, see [`jira-automation`](../jira-automation/SKILL.md).

## Workflow

### Step 1 — Identify the rollup level

Match the user's request to one of three rollup shapes. If ambiguous, ask once before querying.

| Phrase | Rollup | JQL anchor |
|---|---|---|
| "where are we on <PROJECT_KEY>-XXXX" (an Epic) | Epic rollup | `parent = <PROJECT_KEY>-XXXX` |
| "where are we on <PROJECT_KEY>-XXXX" (a Story) | Story detail | `key = <PROJECT_KEY>-XXXX` + linked issues |
| "sprint health", "current sprint", "how's the sprint" | Sprint rollup | `sprint in openSprints() AND project = <PROJECT_KEY>` |
| "what's stuck", "anything blocked", "stale tickets" | Cross-cutting risk scan | multiple queries below |

### Step 2 — Run the right query

| Goal | JQL | MCP tool |
|---|---|---|
| Epic children | `parent = {EPIC} ORDER BY status, updated DESC` | `searchJiraIssuesUsingJql` |
| Story detail | `key = {STORY}` then `getJiraIssue` for full fields | `getJiraIssue` |
| Story sub-tasks / links | `"Epic Link" = {STORY} OR parent = {STORY}` | `searchJiraIssuesUsingJql` |
| Sprint state | `sprint in openSprints() AND project = <PROJECT_KEY>` | `searchJiraIssuesUsingJql` |
| Stale in sprint | `sprint in openSprints() AND status NOT IN (Done, Closed) AND updated < -3d` | `searchJiraIssuesUsingJql` |
| Blocked | `sprint in openSprints() AND flagged = impediment` | `searchJiraIssuesUsingJql` |
| Unassigned in sprint | `sprint in openSprints() AND assignee IS EMPTY` | `searchJiraIssuesUsingJql` |
| NeedsDesign queue | `project IN (<PROJECT_KEYS>) AND labels = NeedsDesign AND status NOT IN (Done, Closed) ORDER BY created ASC` | `searchJiraIssuesUsingJql` |
| Cross-project stale | `project IN (<PROJECT_KEYS>) AND status NOT IN (Done, Closed) AND updated < -7d` | `searchJiraIssuesUsingJql` |

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

Recommendation: {one sentence — what to do or who to ping}
```

**Rules:**
- Keep "Done" lists tight — collapse to a count + one-line summary if >10 items.
- Always end with a one-sentence recommendation. If nothing needs attention, say so explicitly.
- Reference your team's conventions (manager, stakeholder cadence) when surfacing actions.
- Never invent ticket data. If a field is missing in Jira, say "missing" rather than guessing.

### Step 5 — Offer the next step

After the report, offer at most one follow-up action:

- "Want me to draft a Slack to {assignee} asking for a status update?" → `slack-messaging` skill
- "Should I post this to {channel}?" → manual paste, never auto-send
- "Want me to add a comment to {key} flagging the staleness?" → `addCommentToJiraIssue`
- "Want me to break down {Epic} into the missing stories?" → `jira-automation`

Never chain-execute. Wait for confirmation.

## Natural Cadences

| Cadence | When | What to check |
|---|---|---|
| Pre-standup | Daily | "Anything stale or blocked I should mention at standup?" |
| Pre-1:1 with manager | Weekly | Open Epics + at-risk items in your default project |
| Pre-stakeholder update | Per cadence | Done / In-flight / Upcoming across active projects (also see `stakeholder-update`) |
| End of week | Friday | Cross-project stale scan, NeedsDesign queue depth |

## MCP Tools Used

| Tool | Purpose |
|---|---|
| `mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql` | All multi-issue rollups |
| `mcp__claude_ai_Atlassian__getJiraIssue` | Story detail, comment thread, full description |
| `mcp__claude_ai_Atlassian__getTransitionsForJiraIssue` | When asked "what would move this forward" |
| `mcp__claude_ai_Atlassian__addCommentToJiraIssue` | Only after user confirms |

The `mcp-atlassian` (Docker) variant exposes the same shapes under different names — fall back to those if the `claude_ai_Atlassian` variant is unavailable in the session.

## Anti-Patterns

- **Don't dump every ticket.** Summarize Done lists; spell out only the items that need attention.
- **Don't speculate about "why" a ticket is stuck.** Say "stale 9 days, no comments since [date]" — let the user infer the cause.
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
- [ ] Project keys / labels / cadences match the configured project

## Copy/Paste Ready

```
"Where are we on <PROJECT_KEY>-XXXX?"
"Quick health check on the current sprint"
"What's the state of the [Epic Name] Epic?"
"Anything stale or blocked I should know about before standup?"
"How big is the NeedsDesign queue right now?"
"What hasn't moved in the sprint this week?"
"Pre-1:1 sanity check"
```
