# JQL Query Patterns Reference

## Table of Contents

- Sprint Management Queries
- Backlog Health Queries
- Team Productivity Queries
- Release Planning Queries
- Crypto/Fintech PM Queries
- Advanced Compound Queries

## Sprint Management Queries

| Goal | JQL |
|------|-----|
| Current sprint items | `sprint in openSprints() AND project = PROJ` |
| Sprint blockers | `sprint in openSprints() AND (priority = Highest OR flag = Impeded)` |
| Unestimated in sprint | `sprint in openSprints() AND "Story Points" is EMPTY` |
| Added mid-sprint | `sprint in openSprints() AND created > startOfSprint()` |
| Carried over | `sprint in closedSprints() AND sprint in openSprints()` |
| Sprint velocity | `sprint = "Sprint 23" AND status = Done` |
| Not started in sprint | `sprint in openSprints() AND status = "To Do"` |
| Overdue items | `sprint in openSprints() AND duedate < now()` |

## Backlog Health Queries

| Goal | JQL |
|------|-----|
| Stale backlog (30+ days) | `project = PROJ AND status = Backlog AND updated < -30d` |
| Ungroomed items | `project = PROJ AND status = Backlog AND "Story Points" is EMPTY` |
| Orphaned (no epic) | `project = PROJ AND "Epic Link" is EMPTY AND issuetype in (Story, Task)` |
| High priority backlog | `project = PROJ AND status = Backlog AND priority in (High, Highest) ORDER BY created ASC` |
| Bugs without assignee | `project = PROJ AND issuetype = Bug AND assignee is EMPTY AND status != Done` |
| Duplicate candidates | `project = PROJ AND status != Done AND summary ~ "login error"` |

## Team Productivity Queries

| Goal | JQL |
|------|-----|
| My open items | `assignee = currentUser() AND status not in (Done, Closed) ORDER BY priority DESC` |
| Team workload | `project = PROJ AND sprint in openSprints() AND assignee is not EMPTY ORDER BY assignee` |
| Blocked items | `project = PROJ AND status = "Blocked" OR flag = Impeded` |
| Recently resolved | `project = PROJ AND status changed to Done AFTER -7d` |
| Long-running items | `project = PROJ AND status = "In Progress" AND updated < -7d` |
| Items I created | `reporter = currentUser() AND project = PROJ ORDER BY created DESC` |

## Release Planning Queries

| Goal | JQL |
|------|-----|
| Release candidates | `project = PROJ AND fixVersion = "v2.1" AND status = Done` |
| Not done for release | `project = PROJ AND fixVersion = "v2.1" AND status != Done` |
| Release blockers | `project = PROJ AND fixVersion = "v2.1" AND priority = Highest AND status != Done` |
| Changelog items | `project = PROJ AND fixVersion = "v2.1" AND status = Done AND labels in (changelog)` |
| Missing fix version | `project = PROJ AND status = Done AND fixVersion is EMPTY AND resolved > -30d` |

## Crypto/Fintech PM Queries

| Goal | JQL |
|------|-----|
| Compliance items | `project = PROJ AND labels in (compliance, regulatory, KYC, AML)` |
| Security-critical | `project = PROJ AND labels in (security) AND priority in (High, Highest)` |
| API integration work | `project = PROJ AND labels in (api, integration, blockchain) AND sprint in openSprints()` |
| Data pipeline tasks | `project = PROJ AND component = "Data Pipeline" AND status != Done` |
| Token/pricing features | `project = PROJ AND (summary ~ "token" OR summary ~ "pricing" OR labels in (tokenomics))` |

## Advanced Compound Queries

**Sprint health dashboard** (combine for a full picture):
```
sprint in openSprints() AND project = PROJ AND (
  (status = "In Progress" AND updated < -3d) OR
  (priority = Highest AND status != Done) OR
  (assignee is EMPTY)
) ORDER BY priority DESC, updated ASC
```

**Tech debt audit**:
```
project = PROJ AND labels in (tech-debt) AND status not in (Done, Closed)
ORDER BY priority DESC, created ASC
```

**Quarterly review** (items completed in Q4):
```
project = PROJ AND status = Done AND resolved >= "2026-10-01" AND resolved <= "2026-12-31"
ORDER BY resolved DESC
```

**Cross-team dependencies**:
```
project = PROJ AND issueFunction in linkedIssuesOf("project = OTHER_PROJ", "blocks")
```

## Query Modifiers

| Modifier | Purpose | Example |
|----------|---------|---------|
| `ORDER BY` | Sort results | `ORDER BY priority DESC, created ASC` |
| `AND updated <` | Time-based filtering | `updated < -14d` (14 days ago) |
| `startOfDay()` | Relative date | `created > startOfDay("-7d")` |
| `startOfWeek()` | Week boundary | `created > startOfWeek()` |
| `currentUser()` | Dynamic user | `assignee = currentUser()` |
| `membersOf()` | Team filter | `assignee in membersOf("frontend-team")` |
