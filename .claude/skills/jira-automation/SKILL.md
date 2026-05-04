---
name: jira-automation
description: Jira automation for Product & Engineering teams. Creates Epics, Design Stories ([Design] prefix), and Implementation Stories ([Implementation] prefix) from PRDs or natural language. Runs JQL queries, manages sprints, and handles bulk operations via Atlassian MCP. Use when asked to "create a ticket", "write Jira tickets", "break down this PRD", "JQL query", "bulk create", "sprint management", or any Jira workflow task.
---

# Jira Automation

> **Configure:** Set the project keys, components, labels, team roster, and Jira instance URL for your organization in your project context (CLAUDE.md or local profile). Patterns below are organization-agnostic.

## Purpose

Automate Jira workflows for Product & Engineering teams. Create properly formatted Epics, Design Stories, and Implementation Stories following team conventions. Run JQL queries, manage sprints, and handle bulk operations — all via Atlassian MCP without leaving Claude Code.

## When to Use

- **Ticket creation:** "Create a Jira ticket for [feature]" / "Break down this PRD into tickets"
- **Bulk operations:** "Create all the stories for this Epic" / "Update these tickets"
- **JQL queries:** "Find stale tickets" / "Show me unassigned work in the sprint"
- **Sprint management:** "Move these to Sprint 24" / "Sprint health check"
- **Templates:** "Create a Design story for [feature]" / "Write an Implementation ticket"

## Jira Configuration (set per project)

### Instance

- **URL:** `https://<your-instance>.atlassian.net`
- **Browse:** `https://<your-instance>.atlassian.net/browse/`

### Project Keys (configure)

| Key | Name | Use |
|-----|------|-----|
| **<PROJECT_KEY>** | Primary P&E project | Most tickets go here (set as default) |
| **<SECONDARY_KEY>** | Secondary P&E project | Cross-team work |
| **<CONTENT_KEY>** | Content/marketing | Editorial / CMS |
| **<DESIGN_KEY>** | Design | Design requests |
| **<DATA_KEY>** | Data Engineering | Data pipeline work |
| **<INFRA_KEY>** | Infrastructure | DevOps / Infra |

**Default project:** `<PROJECT_KEY>` (unless user specifies otherwise).

### Components (configure)

Components are team-specific. Common shapes:

| Component | Description | Use When |
|-----------|-------------|----------|
| `<surface-1>` | LMS / education platform | Course features, learning paths, certificates |
| `<surface-2>` | Public site | Homepage, articles, navigation, public pages |
| `<surface-3>` | Premium tier | Subscriber-gated features |
| `<surface-4>` | API | External API endpoints |
| `<surface-5>` | CMS | Content management |

**Rule:** If a feature spans multiple surfaces, add all relevant components.

### Labels

| Label | Use When |
|-------|----------|
| `NeedsDesign` | Story requires design work before implementation can begin |
| `ToGroom` | Ticket needs grooming by product team |
| `frontend` | Story involves UI/frontend development |
| `BACKEND` | Story involves backend/API/database work |

### Issue Types

| Type | ID | Title Format | Example |
|------|----|--------------|---------|
| Epic | 10000 | `{Feature Name}` | `Sponsored Courses Integration` |
| Story (Design) | 10001 | `[Design] {Feature Name}` | `[Design] Job Board Pages` |
| Story (Implementation) | 10001 | `[Implementation] {Feature Name}` | `[Implementation] Homepage Module` |
| Story (Database) | 10001 | `DB > {Feature Name}` | `DB > Jobs database on Laravel` |
| Task | 10002 | `[Implementation] {Task Name}` | `[Implementation] Email Template` |
| Bug | 10003 | `[Bug] {Issue Description}` | `[Bug] Login 500 error` |

### Priorities

| Name | ID | Use For |
|------|----|---------|
| Highest | 1 | Critical path, launch blockers, security issues |
| High | 2 | Core functionality, significant user impact, MVP features |
| Medium | 3 | Important enhancements, quality improvements |
| Low | 4 | Nice to have, future consideration |
| Lowest | 5 | Backlog items, someday/maybe |

## Ticket Templates

### Epic Template

```markdown
{One-sentence summary of what we're building}

**Problem:** {What problem are we solving? Include data if available}

**Solution:** {High-level approach to solving the problem}

**Scope:**
* {Major deliverable 1}
* {Major deliverable 2}
* {Major deliverable 3}

**Success Metrics:**
* {Metric 1 with target, e.g., "Completion rate >60%"}
* {Metric 2 with target}

{Optional: Attach diagram, mockup, or flow image}
```

**Required fields:** Summary, Description, Components, Priority

### Design Story Template

Title: `[Design] {Feature or Component Name}`

```markdown
As the product team, we need {what designs are needed} so that {why engineering needs them}.

**Summary:** {1-2 sentence overview of design deliverables}

**Acceptance Criteria:**
* {Specific design deliverable 1}
* {Specific design deliverable 2}
* {Mobile/responsive requirements}
* Design specs handed off in Figma with component documentation
```

**Required fields:** Summary (with `[Design]` prefix), Description, Components, Priority, Labels: `NeedsDesign`, Epic Link

### Implementation Story Template

Title: `[Implementation] {Feature or Component Name}`

```markdown
As a user, I want to {action/capability} so that {benefit/value}.

**Summary:** {1-2 sentence technical overview of what's being built}

**Acceptance Criteria:**
* {Functional requirement 1}
* {Functional requirement 2}
* {Analytics/tracking requirement}
* {Responsive/cross-browser requirement}
* {Error handling requirement}

**Technical Notes:**
* {Implementation detail 1}
* {Dependency or integration note}
* {Data source or API note}
```

**Required fields:** Summary (with `[Implementation]` prefix), Description, Components, Priority, Labels: `frontend` and/or `BACKEND`, Epic Link

### Bug Report Template

Title: `[Bug] {Issue Description}`

```markdown
**Environment**: Production / Staging / Dev
**Component**: {Detected from error or user input}
**Browser/Device**: {If applicable}

**Reproduction Steps**:
1. {Step 1}
2. {Step 2}

**Expected**: {Expected behavior}
**Actual**: {Error message or observed behavior}

**Root Cause Analysis**:
{Summary if known, otherwise "Investigation needed"}

**Logs/Screenshots**:
{Attach relevant data}
```

**Required fields:** Summary, Description, Components, Priority, Labels as appropriate

## Workflow: PRD to Tickets

When given a PRD, follow this sequence:

### Step 1: Create the Epic

Extract from the PRD:
- Problem statement
- Solution overview
- Scope items (become the deliverables list)
- Success metrics (measurable KPIs)

### Step 2: Create Design Story

One `[Design]` story covering all UI/UX deliverables for the feature. Always include:
- All surfaces that need design (homepage, article page, etc.)
- Mobile-responsive variants
- Figma handoff requirement

### Step 3: Create Implementation Stories

Break down by:
- **User-facing surfaces** (Homepage module, Learn page, Article page, etc.)
- **Technical systems** (Auth, Deep linking, Data export, etc.)

Each story should be completable by one developer in roughly one sprint or less.

### Step 4: Link Everything

- All stories link to the parent Epic via Epic Link
- Add appropriate components (per your team's surfaces — see Components table)
- Add labels (NeedsDesign for design, frontend/BACKEND for implementation)
- Set priority consistently with the Epic

## Example Epic Breakdown

```
Epic: <Feature Name>
+-- [Design] <Feature> design deliverables (<PROJECT_KEY>-NNNN)
+-- [Implementation] Homepage Module (<PROJECT_KEY>-NNNN)
+-- [Implementation] Detail Page (<PROJECT_KEY>-NNNN)
+-- [Implementation] Recirculation Component (<PROJECT_KEY>-NNNN)
+-- [Implementation] Auth Integration (<PROJECT_KEY>-NNNN)
+-- [Implementation] Deep Linking (<PROJECT_KEY>-NNNN)
+-- [Implementation] Lead Data Export (<PROJECT_KEY>-NNNN)
+-- [Implementation] Completion Shareable Social Card (<PROJECT_KEY>-NNNN)
```

## MCP Integration

### Atlassian Rovo MCP (Primary)

Already configured. Use these tools:

| Action | MCP Tool |
|--------|----------|
| Create ticket | `createJiraIssue` |
| Search tickets | `searchJiraIssuesUsingJql` |
| Get ticket details | `getJiraIssue` |
| Update ticket | `editJiraIssue` |
| Add comment | `addCommentToJiraIssue` |
| Link issues | — (use editJiraIssue with parent field) |
| Transition status | `transitionJiraIssue` |

### Creating a Ticket via MCP

```json
{
  "projectKey": "<PROJECT_KEY>",
  "summary": "[Implementation] Homepage Module",
  "description": "As a user, I want to see [feature] so I can [benefit]...",
  "issueType": "Story",
  "priority": "High",
  "labels": ["frontend"],
  "components": ["<surface>"]
}
```

## JQL Query Patterns

### Common Queries

| Goal | JQL |
|------|-----|
| My open items | `project = <PROJECT_KEY> AND assignee = currentUser() AND status != Done ORDER BY priority DESC` |
| Stale tickets | `project IN (<PROJECT_KEYS>) AND status NOT IN (Done, Closed) AND updated < -14d` |
| Sprint blockers | `sprint IN openSprints() AND priority = High AND flagged = impediment` |
| Unassigned work | `project = <PROJECT_KEY> AND sprint IN openSprints() AND assignee IS EMPTY` |
| Scope creep | `sprint IN openSprints() AND created > startOfDay("-5d")` |
| Epic progress | `parent = <PROJECT_KEY>-NNNN AND status != Done` |
| NeedsDesign tickets | `project = <PROJECT_KEY> AND labels = NeedsDesign AND status NOT IN (Done, Closed)` |
| In-flight work | `project IN (<PROJECT_KEYS>) AND status IN ("In Progress", "Ready for Review", "Ready for Testing", "In Test") ORDER BY status ASC` |

### Bi-Weekly Update Queries

See the `stakeholder-update` skill for the 3 JQL queries used in bi-weekly reporting.

## Bulk Operations

For batch ticket creation (e.g., breaking down an Epic):

1. Verify the parent Epic exists via `getJiraIssue`
2. Create each child story via `createJiraIssue` with Epic Link
3. Confirm all tickets with a summary table showing keys, titles, and links

For batch updates (e.g., commenting on stale tickets):

1. Run a JQL search to get the issue list
2. Iterate through results applying the update
3. Report what was changed

**Rate limit note:** Pause 2 seconds between calls if creating >20 items.

## Relationship to ticket-batch

This skill is **Jira-specific** — it knows the conventions of a configured Jira project (keys, components, labels). For **Linear**, **GitHub Issues**, or **generic multi-platform** ticket batching, use `ticket-batch` instead. For the full PRD-to-launch pipeline connecting this skill with `prd-generator` and `sprint-roadmap`, see `the-block/product-management/templates/prd-to-launch.md`.

## Quality Checklist

Before finalizing tickets, verify:

- [ ] Epic has Problem, Solution, Scope, and Success Metrics
- [ ] Design story covers all UI deliverables with Figma handoff requirement
- [ ] Each Implementation story has user story format ("As a user, I want...")
- [ ] Each Implementation story has clear, testable acceptance criteria
- [ ] Technical Notes included where implementation details matter
- [ ] Components correctly assigned (Campus vs theblock.co vs both)
- [ ] Labels assigned (NeedsDesign, frontend, BACKEND)
- [ ] Stories are sized appropriately (break down if >1 sprint of work)
- [ ] All stories linked to parent Epic
- [ ] Priority set consistently across the Epic

## Examples

**Example 1: Create a ticket from natural language**
```
User: "Create a Jira ticket for the new ratings page redesign"
Claude: [Uses jira-automation]

Before creating, let me confirm:
- Project: <PROJECT_KEY> (default)
- Type: Epic (since this sounds like a multi-story feature)
- Component: <surface>

Creating Epic: "Ratings Page Redesign"

I'll also create:
1. [Design] Ratings Page Redesign — NeedsDesign label
2. [Implementation] Ratings Page Frontend — frontend label

Want me to proceed?
```

**Example 2: PRD to tickets**
```
User: "Here's a PRD for multi-language support. Break it down."
Claude: [Uses jira-automation]

Reading PRD... Creating ticket structure:

Epic: Multi-Language Support
+-- [Design] Multi-Language UI Components
+-- [Implementation] Language Selector Component
+-- [Implementation] Content Translation Pipeline
+-- [Implementation] i18n Framework Integration
+-- [Implementation] RTL Layout Support

Creating 5 tickets in <PROJECT_KEY>...
```

**Example 3: JQL query**
```
User: "Show me stale tickets in the current sprint"
Claude: [Uses jira-automation]

Running: sprint IN openSprints() AND status NOT IN (Done, Closed) AND updated < -7d

Found 3 stale issues:
| Key | Summary | Assignee | Last Updated |
|-----|---------|----------|-------------|
| <PROJECT_KEY>-NNNN | [Implementation] Chart tooltip fix | [name] | 12 days ago |
| <PROJECT_KEY>-NNNN | [Implementation] Nav update | [name] | 9 days ago |
| <PROJECT_KEY>-NNNN | [Bug] Mobile menu overlap | [name] | 8 days ago |

Want me to add a comment to these asking for status updates?
```

## Success Criteria

- [ ] Tickets created with all required fields populated
- [ ] Templates (Epic/Design/Implementation) applied correctly
- [ ] Components and labels match the configured project's conventions
- [ ] PRD-to-tickets workflow produces complete Epic structures
- [ ] JQL queries return expected results
- [ ] All tickets linked to correct Epics
- [ ] No API tokens exposed in prompts

## Copy/Paste Ready

```
"Create a Jira ticket for [describe the feature]"
"Break down this PRD into Jira tickets"
"Create a Design story for [feature]"
"Create an Implementation story for [feature]"
"Find stale tickets in the current sprint"
"Show me NeedsDesign tickets in PRO"
"Create an Epic with child stories for [feature]"
"Run a JQL query: [query]"
```