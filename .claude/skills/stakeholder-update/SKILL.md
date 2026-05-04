---
name: stakeholder-update
description: Stakeholder communication generator for Product & Engineering teams. Primary use case is the bi-weekly status update (Jira → Confluence → Slack). Also generates executive summaries, cross-functional updates, and standup notes. Use when asked for "bi-weekly update", "stakeholder update", "status report", "biweekly", "what shipped", or "leadership update".
---

# Stakeholder Update

> **Configure:** Set `<PROJECT_KEYS>` to your team's Jira project keys, fill in the team roster, and adjust product/area prefixes for your organization.

## Purpose

Generates recurring Product & Engineering bi-weekly status updates and other stakeholder communications. The primary workflow queries Jira for completed, in-progress, and upcoming work, then formats it for Confluence publication with a Slack summary. Also handles executive summaries, cross-functional updates, and ad hoc communications.

## When to Use

- **Bi-weekly update:** "Generate the bi-weekly update" / "What shipped in the last 2 weeks?"
- **Status report:** "Write a status report for [manager]" / "P&E update"
- **Executive summary:** "Summarize this sprint for [VP]"
- **Cross-functional:** "Write an update for the design team"
- **Ad hoc:** "Generate a standup update from my recent work"

## The Bi-Weekly Update

### Overview

The bi-weekly update is the primary stakeholder communication shape: a Done / In-flight / Upcoming structure plus a Slack summary. Posted to Confluence with a Slack summary. Done / In-flight / Upcoming is a universal PM communication primitive.

### Team Scope

Configure the team roster in your project context. Include tickets assigned to the active P&E team members. The skill consults the roster to filter results.

**Projects to search:** `<PROJECT_KEYS>` (set in project context)

### Status Mappings

| Section | Jira Statuses | Description |
|---------|--------------|-------------|
| Done (past 2 weeks) | Done, Closed, Completed | Tickets marked complete in last 14 days |
| In Progress | In Progress, Ready for Review, Ready for Testing, In Test, Awaiting Deploy | Past design, with devs or QA |
| Upcoming (next months) | To Do, Backlog | Planned work not yet in dev |

### JQL Queries (Exactly 3)

**Query 1 — Completed Work:**
```jql
project IN (<PROJECT_KEYS>)
AND status IN (Done, Closed, Completed)
AND updated >= -14d
ORDER BY updated DESC
```

**Query 2 — In-Progress Work:**
```jql
project IN (<PROJECT_KEYS>)
AND status IN ("In Progress", "Ready for Review", "Ready for Testing", "In Test", "Awaiting Deploy")
ORDER BY status ASC, updated DESC
```

**Query 3 — Upcoming Work:**
```jql
project IN (<PROJECT_KEYS>)
AND status IN ("To Do", Backlog)
ORDER BY priority DESC, created DESC
```

All queries: `maxResults=100`. Use **only** `Atlassian:searchJiraIssuesUsingJql`. No Confluence searches, no individual ticket lookups, no pagination.

### Formatting Rules

**Product/Area Prefixes (configure for your team):**
Use short prefixes per surface — e.g. `Web`, `App`, `LMS`, `Ad Server`, `Analytics`, `CMS`, `Email`. Whatever maps cleanly to your stakeholders' mental model.

**Status Tags (inline):**
- "in test" — for Ready for Testing, In Test, Ready for Review
- "awaiting deploy" — for Awaiting Deploy

**Consolidation:** Combine related tickets into single bullets. Focus on user/business impact, not technical implementation.

### Output Template

```
[Month DD, YYYY]

Things we've done in the past two weeks:
● [Product] - [Accomplishment]
● [Product] - [Accomplishment]
● [Cross-cutting] - Visual bugs, UX improvements, SEO fixes

Things being worked on, likely to be released in the next few weeks:
● [Product] - [Feature], in test
● [Product] - [Feature], awaiting deploy
● [Product] - [Feature]
● Chart improvements & bug fixes

A few of the things we're focused on for upcoming months:
● [Initiative]
● [Initiative]
● Tech Debt
```

**Section rules:**
- **Section 1 (Done):** Always include a "visual bugs, UX improvements, SEO fixes" catch-all bullet
- **Section 2 (In Progress):** Typically longest (10-15 items). Always include a "bug fixes" bullet
- **Section 3 (Upcoming):** Higher-level initiatives (3-5 items). Always end with "Tech Debt"

### Quality Checks

1. All three sections populated (min 3-4 items each)
2. No duplicates across sections
3. Bullets start with product prefix
4. Date accuracy (Section 1 = past 14 days only)
5. Recurring items included

## Examples

**Example 1: Bi-weekly update**
```
User: "Generate the bi-weekly update"
Claude: [Uses stakeholder-update]

Running 3 Jira queries...

[Date]

Things we've done in the past two weeks:
● [Product] - [Feature] backend complete
● Web - [Feature] launched
● Analytics - Monthly reporting dashboard
● Cross-cutting - Visual bugs, UX improvements, SEO fixes

Things being worked on, likely to be released in the next few weeks:
● [Product] - Stripe checkout, in test
● Web - [Feature] homepage module, in test
● Web - Framework migration, remaining pages
● Ad Server - New ad hosting experience, awaiting deploy
● Chart improvements & bug fixes

A few of the things we're focused on for upcoming months:
● [Product] - [Initiative]
● Web - Multi-language support
● Tech Debt

Ready to post? I'll format this for Confluence and draft
a Slack summary.
```

**Example 2: Executive summary for a VP**
```
User: "Summarize this sprint for the VP"
Claude: [Uses stakeholder-update]

## P&E Executive Summary — [Date]

### Highlights
- [Feature] shipped (enables revenue diversification)
- [Feature] live (new revenue stream)
- Framework migration 85% complete

### Risks
- [Feature] launch depends on [Dependency] (in test)
- Migration affecting some page load times (monitoring)

### Next 30 Days
- [MVP launch]
- [Feature launch] (if [Dependency] clears QA)
- Complete framework migration
```

## General Communication Templates

### What-Why-How Framework

| Layer | What (Technical) | Why (Business Value) | How (Process) |
|-------|-------------------|---------------------|---------------|
| Executive | "Launched [Feature] v1" | "New revenue stream targeting [segment]" | "[N] in pipeline" |
| Manager | "Search and filter complete" | "Users can now find relevant items" | "Indexed by location, type" |
| Cross-functional | "[Feature] is live" | "Sales can now pitch [Feature] to clients" | "Share posting flow with sales team" |

### Audience Rules

- **Executives:** Lead with business metrics and risk. Include asks.
- **Engineering:** Include Jira ticket keys, architecture decisions, trade-offs.
- **Design/Sales:** Focus on timelines, deliverables, dependencies.
- **Slack summary:** 3-4 bullets max with Confluence link.

### Metrics by Audience

Use this table to select which metrics to highlight for each audience. Avoid drowning stakeholders in data they don't care about.

| Audience | Primary Metrics | Secondary Metrics | Avoid |
|:---------|:----------------|:------------------|:------|
| **VP / Executive** | Revenue impact, growth, launch dates | Sprint velocity, major risks | Individual ticket details, technical jargon |
| **PM / Manager** | Sprint completion %, blocker count, scope changes | Feature adoption (post-launch), bug escape rate | Low-level implementation details |
| **Design** | Design ticket throughput, handoff queue depth | Figma coverage, NeedsDesign backlog size | Backend metrics, revenue numbers |
| **Sales/Revenue** | Feature launch timelines, customer-facing changes | API uptime, data freshness | Sprint internals, tech debt items |
| **Engineering** | Ticket count by status, deploy frequency, bug rate | PR cycle time, test coverage delta | Business strategy, revenue projections |
| **Full Team (Slack)** | Top 3 shipped items, top blocker, next milestone | — | Anything requiring >30 seconds to read |

**How to use:** Before drafting any update, identify the audience → pick their primary metrics → lead with those. Pull metric data using `data-analysis` or `analytics-workarounds` skills.

### Tone Templates

**Formal (Leadership):**
> "The framework migration remains on track. Key milestone: article pages fully migrated. Primary risk: ad-server support requires final pages to complete."

**Casual (Slack):**
> "Bi-weekly update is up! TL;DR: [Feature] launched, [Feature 2] is done, migration almost there. Full details: [Confluence link]"

**Urgent (Escalation):**
> "BLOCKED: [Dependency] integration for [Feature] launch. Need [Vendor] support escalation. Impact: delays public launch by 1-2 weeks if not resolved by Friday."

### Standup Update

```markdown
**Yesterday:**
- [Completed item 1]
- [Completed item 2]

**Today:**
- [Planned item 1]
- [Planned item 2]

**Blockers:**
- [Blocker with owner and expected resolution]
```

## Verification Tests

1. **Skim Test:** Read only headers. Do you know the status?
2. **Action Test:** Is every "ask" specific enough to act on today?
3. **Surprise Test:** Would any stakeholder be surprised by this content?
4. **Evidence Test:** Can every claim be backed by a Jira ticket?

## Success Criteria

- [ ] Bi-weekly update generated from exactly 3 JQL queries
- [ ] All three sections populated with appropriate items
- [ ] Product prefixes applied consistently
- [ ] Status tags (in test, awaiting deploy) included
- [ ] Recurring items present (Tech Debt, bug fixes, visual fixes)
- [ ] Executive summaries lead with business impact
- [ ] Slack summary is 3-4 bullets max with Confluence link
- [ ] Reports match audience level (no jargon for execs)

## Copy/Paste Ready

```
"Generate the bi-weekly update"
"What shipped in the last 2 weeks?"
"Write a status report for [manager]"
"Summarize this sprint for the VP"
"Write an update for the design team"
"Generate my standup update"
"Draft a Slack summary for the bi-weekly"
```
