---
name: stakeholder-update
description: Stakeholder communication generator for The Block's Product & Engineering team. Primary use case is the bi-weekly P&E status update (Jira → Confluence → Slack). Also generates executive summaries, cross-functional updates, and standup notes. Use when asked for "bi-weekly update", "stakeholder update", "status report", "biweekly", "update for Ed", "what shipped", "P&E update", or "leadership update".
---

# Stakeholder Update — The Block

## Purpose

Generates The Block's recurring Product & Engineering bi-weekly status updates and other stakeholder communications. The primary workflow queries Jira for completed, in-progress, and upcoming work, then formats it for Confluence publication with a Slack summary. Also handles executive summaries, cross-functional updates, and ad hoc communications.

## When to Use

- **Bi-weekly update:** "Generate the bi-weekly update" / "What shipped in the last 2 weeks?"
- **Status report:** "Write a status report for Ed" / "P&E update"
- **Executive summary:** "Summarize this sprint for Matt"
- **Cross-functional:** "Write an update for the design team"
- **Ad hoc:** "Generate a standup update from my recent work"

## The Block Bi-Weekly Update

### Overview

The bi-weekly update is Sean and Ed's primary stakeholder communication. It summarizes P&E work in three sections: completed, in-progress, and upcoming. Posted to Confluence with a Slack summary.

### Team Scope

Include tickets assigned to these P&E team members:

- Aliaksandr Kryvanosau, Ana Benitez, Bohdan Panasenko, Brian Mendoza
- Cesar Paz, Claudine Daumur, Edvinas Rupkus, Josh Gragg
- Koray Baspinar, Maria Zhynko, Marina Ardytskaya, Nikita Gulis
- Nikita Orobenko, Nikola Pivcevic, Ramuald Vishneuski, Serena Ho

**Projects to search:** PRO, RBS, CM (primary focus on PRO and RBS)

### Status Mappings

| Section | Jira Statuses | Description |
|---------|--------------|-------------|
| Done (past 2 weeks) | Done, Closed, Completed | Tickets marked complete in last 14 days |
| In Progress | In Progress, Ready for Review, Ready for Testing, In Test, Awaiting Deploy | Past design, with devs or QA |
| Upcoming (next months) | To Do, Backlog | Planned work not yet in dev |

### JQL Queries (Exactly 3)

**Query 1 — Completed Work:**
```jql
project IN (PRO, RBS, CM)
AND status IN (Done, Closed, Completed)
AND updated >= -14d
ORDER BY updated DESC
```

**Query 2 — In-Progress Work:**
```jql
project IN (PRO, RBS, CM)
AND status IN ("In Progress", "Ready for Review", "Ready for Testing", "In Test", "Awaiting Deploy")
ORDER BY status ASC, updated DESC
```

**Query 3 — Upcoming Work:**
```jql
project IN (PRO, RBS, CM)
AND status IN ("To Do", Backlog)
ORDER BY priority DESC, created DESC
```

All queries: `maxResults=100`. Use **only** `Atlassian:searchJiraIssuesUsingJql`. No Confluence searches, no individual ticket lookups, no pagination.

### Formatting Rules

**Product/Area Prefixes:**
- `.Co` — Main website (theblock.co)
- `Campus` — Education platform
- `SFMC` — Salesforce Marketing Cloud
- `Ad Server` / `GAM` — Google Ad Manager
- `Crypto IQ` — Competition/quiz feature
- `Analytics` / `Looker` — Data/analytics work
- `Wordpress` / `SEO` — CMS/SEO work
- `Sendgrid` — Email infrastructure
- `Ratings Pages` / `Indices` / `Charts` — Data features

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
● .Co & Campus - Visual bugs, UX improvements, SEO fixes

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
- **Section 1 (Done):** Always include ".Co & Campus - Visual bugs, UX improvements, SEO fixes"
- **Section 2 (In Progress):** Typically longest (10-15 items). Always include "Chart improvements & bug fixes"
- **Section 3 (Upcoming):** Higher-level initiatives (3-5 items). Always end with "Tech Debt"

### Recurring Patterns

Items that appear frequently across updates:
- Nuxt 3/4 migration → GAM Ad support
- Multi-course support, CMI-5
- Tech Debt (always in upcoming)
- Chart improvements & bug fixes (always in progress)
- Visual bugs, UX improvements (always in completed)
- Additional Indices, Job Boards, Sponsored Courses

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

Feb 18, 2026

Things we've done in the past two weeks:
● Campus - Multi-course support backend complete
● .Co - Job Board v1 launched
● Analytics - Monthly reporting dashboard for LMAX
● .Co & Campus - Visual bugs, UX improvements, SEO fixes

Things being worked on, likely to be released in the next few weeks:
● Campus - Marketing site Stripe checkout, in test
● .Co - Sponsored Courses homepage module, in test
● .Co - Nuxt 4 migration, remaining pages → GAM Ad support
● Ad Server - New ad hosting experience, awaiting deploy
● SFMC - Migration of Marketo forms
● Chart improvements & bug fixes

A few of the things we're focused on for upcoming months:
● Campus - Prerequisite Schema & Knowledge Token Taxonomy
● .Co - Multi-language support
● Tech Debt

Ready to post? I'll format this for Confluence and draft
a Slack summary.
```

**Example 2: Executive summary for Matt**
```
User: "Summarize this sprint for Matt"
Claude: [Uses stakeholder-update]

## P&E Executive Summary — Feb 18, 2026

### Highlights
- Campus multi-course support shipped (enables revenue diversification)
- Job Board v1 live (new revenue stream, 50+ listings target)
- Nuxt 4 migration 85% complete (enables GAM ad support)

### Risks
- Campus 201 public launch depends on Stripe checkout (in test)
- Nuxt 4 migration affecting some page load times (monitoring)

### Next 30 Days
- Sponsored Courses MVP launch
- Campus 201 public launch (if Stripe clears QA)
- Complete Nuxt 4 migration + GAM full rollout
```

## General Communication Templates

### What-Why-How Framework

| Layer | What (Technical) | Why (Business Value) | How (Process) |
|-------|-------------------|---------------------|---------------|
| Executive (Matt) | "Launched Job Board v1" | "New revenue stream targeting crypto employers" | "50+ listings in pipeline" |
| Manager (Ed) | "Job Board search and filter complete" | "Users can now find relevant jobs" | "Indexed by location, company, role type" |
| Cross-functional | "Job Board is live on .Co" | "Sales can now pitch job listings to clients" | "Share posting flow with sales team" |

### Audience Rules

- **Ed/Matt:** Lead with business metrics and risk. Include asks.
- **Engineering:** Include Jira ticket keys, architecture decisions, trade-offs.
- **Design/Sales:** Focus on timelines, deliverables, dependencies.
- **Slack summary:** 3-4 bullets max with Confluence link.

### Metrics by Audience

Use this table to select which metrics to highlight for each audience. Avoid drowning stakeholders in data they don't care about.

| Audience | Primary Metrics | Secondary Metrics | Avoid |
|:---------|:----------------|:------------------|:------|
| **Matt (VP)** | Revenue impact, subscriber growth, launch dates | Sprint velocity, major risks | Individual ticket details, technical jargon |
| **Ed (PM)** | Sprint completion %, blocker count, scope changes | Feature adoption (post-launch), bug escape rate | Low-level implementation details |
| **Design (Josh, Claudine, Serena)** | Design ticket throughput, handoff queue depth | Figma coverage, NeedsDesign backlog size | Backend metrics, revenue numbers |
| **Sales/Revenue** | Feature launch timelines, customer-facing changes | API uptime, data freshness | Sprint internals, tech debt items |
| **Engineering** | Ticket count by status, deploy frequency, bug rate | PR cycle time, test coverage delta | Business strategy, revenue projections |
| **Full Team (Slack)** | Top 3 shipped items, top blocker, next milestone | — | Anything requiring >30 seconds to read |

**How to use:** Before drafting any update, identify the audience → pick their primary metrics → lead with those. Pull metric data using `data-analysis` or `analytics-workarounds` skills.

### Tone Templates

**Formal (Leadership):**
> "The Nuxt 4 migration remains on track. Key milestone: article pages fully migrated. Primary risk: GAM ad support requires final Nuxt 4 pages to complete."

**Casual (Slack):**
> "Bi-weekly update is up! TL;DR: Job Board launched, Campus multi-course is done, Nuxt 4 almost there. Full details: [Confluence link]"

**Urgent (Escalation):**
> "BLOCKED: Stripe checkout integration for Campus 201 public launch. Need Stripe support escalation. Impact: delays public launch by 1-2 weeks if not resolved by Friday."

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
"Write a status report for Ed"
"Summarize this sprint for Matt"
"Write an update for the design team"
"Generate my standup update"
"Draft a Slack summary for the bi-weekly"
```