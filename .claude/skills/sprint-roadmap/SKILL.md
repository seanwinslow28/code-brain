---
name: sprint-roadmap
description: Sprint planning and roadmap assistant for product managers. Handles backlog prioritization with RICE/MoSCoW/Impact-Effort frameworks, sprint capacity planning, roadmap generation, dependency mapping, and release planning. Use when asked about sprint planning, roadmaps, backlog grooming, prioritization, release planning, capacity planning, or velocity tracking.
---

# Sprint & Roadmap Planning

## Purpose

Structure sprint planning, roadmap generation, backlog grooming, and release planning workflows. Apply prioritization frameworks consistently, track velocity for capacity planning, and manage dependencies across teams. Works with any Jira-based agile setup.

## When to Use

- **Sprint planning:** "Help me plan Sprint 24" / "Calculate capacity"
- **Prioritization:** "Prioritize these features using RICE" / "Apply MoSCoW to backlog"
- **Roadmap:** "Generate a Q2 roadmap" / "Map out the next quarter"
- **Backlog grooming:** "Groom the backlog" / "Flag stale items"
- **Dependencies:** "Map dependencies for this epic" / "What's blocking what?"
- **Release planning:** "Create a release plan for v2.1"

## Sprint Planning Workflow

### Step 1: Calculate Capacity

```
Capacity Formula:
  Team members: [N]
  Sprint length: [days]
  PTO/holidays: [days off across team]
  Overhead (meetings, reviews): 20%

  Available dev-days = (N x sprint_days - PTO) x 0.8
  Story point capacity = Available dev-days x (velocity / prev_dev-days)
```

**Rule:** Plan to 80-90% of average velocity. Never plan to 100%.

### Step 2: Review Velocity

Track velocity across last 3-5 sprints:

| Sprint | Planned | Completed | Velocity | Notes |
|--------|---------|-----------|----------|-------|
| Sprint N-2 | [pts] | [pts] | [pts] | [context] |
| Sprint N-1 | [pts] | [pts] | [pts] | [context] |
| Sprint N | [pts] | [pts] | [pts] | [context] |
| **Average** | | | **[pts]** | Use for planning |

Pull velocity data from Jira sprint reports or calculate from completed story points per sprint.

### Step 3: Select Sprint Items

1. Start with P0 (must-have) items that align with sprint goal
2. Fill remaining capacity with P1 items
3. Add one P2 item as a stretch goal
4. Verify no item exceeds 50% of sprint capacity (decompose if so)

### Step 4: Define Sprint Goal

Write sprint goals that are:
- **Specific:** "Ship SSO login for enterprise customers" not "Work on auth"
- **Testable:** Can verify yes/no whether it was achieved
- **Aligned:** Connects to quarterly objective or roadmap theme

## Prioritization Frameworks

### RICE Scoring

| Factor | Definition | Scale |
|--------|-----------|-------|
| **Reach** | Users affected per quarter | Absolute number |
| **Impact** | Effect on each user | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal |
| **Confidence** | How sure are you | 100%=high, 80%=medium, 50%=low |
| **Effort** | Person-weeks of work | Absolute number |

**Formula:** `RICE = (Reach x Impact x Confidence) / Effort`

**Worked example:**

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|-----------|--------|-----------:|
| SSO Login | 5,000/q | 3 | 90% | 3 wks | 4,500 |
| CSV Export | 2,000/q | 2 | 80% | 1 wk | 3,200 |
| Dark Mode | 8,000/q | 1 | 70% | 2 wks | 2,800 |
| Notifications | 3,000/q | 2 | 85% | 2 wks | 2,550 |
| API v2 | 500/q | 3 | 60% | 4 wks | 225 |

Recommended order: SSO > CSV Export > Dark Mode > Notifications > API v2

### MoSCoW Method

| Category | Definition | Sprint Rule |
|----------|-----------|-------------|
| **Must have** | Sprint fails without it | Always included |
| **Should have** | Important but not critical | Include if capacity allows |
| **Could have** | Nice to have | Stretch goal only |
| **Won't have** | Explicitly deferred | Document why, set future date |

### Impact/Effort Matrix

```
         High Impact
              |
   Quick Wins | Big Bets
   (Do First) | (Plan Carefully)
  ------------|------------
   Fill-ins   | Time Sinks
   (Do Later) | (Avoid/Defer)
              |
         Low Impact
    Low Effort --- High Effort
```

## Backlog Grooming

### Grooming Checklist

For each item, verify:

1. **Clarity:** Description clear enough to estimate?
2. **Acceptance criteria:** Defined and testable?
3. **Dependencies:** Identified and documented?
4. **Size:** Estimated in story points? Items >13 pts flagged for decomposition?
5. **Alignment:** Connected to an epic or quarterly goal?

### Cleanup Actions

- Close stale items (no activity >60 days, no champion)
- Merge duplicates
- Ensure every item has an epic parent
- Re-prioritize based on current quarter goals

### JQL for Grooming

```jql
-- Stale items (no update in 60 days)
project = PROJ AND status NOT IN (Done, Closed) AND updated < -60d

-- Unestimated items
project = PROJ AND sprint IN openSprints() AND story_points IS EMPTY

-- Orphaned items (no epic)
project = PROJ AND issuetype = Story AND "Epic Link" IS EMPTY AND status != Done
```

## Roadmap Generation

### From Backlog to Roadmap

1. Group backlog items by epic/theme
2. Apply prioritization framework to themes
3. Map themes to sprints based on capacity and dependencies
4. Identify critical path and flag risks

### Roadmap Template

```markdown
# [Quarter] Roadmap: [Team/Product]

## Theme: [Overarching narrative]

### Month 1 (Sprint N, N+1)
- [P0] [Epic Name] - [1-line description]
- [P0] [Epic Name] - [1-line description]

### Month 2 (Sprint N+2, N+3)
- [P1] [Epic Name] - [1-line description]

### Month 3 (Sprint N+4, N+5)
- [P1] [Epic Name] - [1-line description]
- [P2] [Epic Name] - [1-line description]

## Dependencies
- [Feature A] blocks [Feature B] (target: [date])
- [External dependency] ETA: [date]

## Risks
- [Risk and mitigation plan]

## Not This Quarter
- [Deferred item] - Reason: [Why]
```

## Dependency Mapping

Track dependencies using:

| Ticket | Depends On | Type | Status | Risk |
|--------|-----------|------|--------|------|
| PROJ-201 | PROJ-190 | Technical | In progress | Medium |
| PROJ-210 | Legal sign-off | External | Waiting | High |
| PROJ-220 | Design complete | Cross-team | Done | Low |

**JQL for blocking relationships:**
```jql
issueFunction IN linkedIssuesOf("project = PROJ AND sprint IN openSprints()", "blocks")
```

## Release Planning

### Release Checklist

```markdown
## Release [Version] Checklist

### Pre-Release
- [ ] All sprint items marked Done
- [ ] QA sign-off on staging
- [ ] Release notes drafted
- [ ] Stakeholder notification sent
- [ ] Rollback plan documented

### Release Day
- [ ] Deploy to production
- [ ] Smoke test critical paths
- [ ] Monitor error rates for 1 hour
- [ ] Update status page

### Post-Release
- [ ] Close Jira tickets with fixVersion
- [ ] Publish release notes
- [ ] Notify stakeholders of completion
- [ ] Schedule retrospective if needed
```

## Examples

**Example 1: Sprint planning**
```
User: "Help me plan Sprint 24"
Claude: [Uses sprint-roadmap]

Let me gather the inputs:
1. Sprint duration? (1 week / 2 weeks)
2. Team size and any PTO this sprint?
3. Average velocity? (story points per sprint)
4. Sprint goal — what's the ONE thing that must ship?

[After answers]

Sprint 24 Plan:
- Capacity: 4 devs x 2 weeks = 8 dev-weeks, minus 2 days PTO = ~35 pts available
- Historical velocity: 32 pts avg (last 3 sprints)
- Recommended load: 28 pts (leave buffer)

Priority items from backlog:
| Ticket | Points | Priority | Cumulative |
|--------|--------|----------|-----------|
| PROJ-201 | 8 | P0 - Must | 8/28 |
| PROJ-205 | 5 | P0 - Must | 13/28 |
| PROJ-210 | 13 | P1 - Should | 26/28 |
| PROJ-215 | 5 | P2 - Could | Stretch |

Recommendation: Commit to 201, 205, 210 (26 pts). PROJ-215 as stretch.
```

**Example 2: Backlog prioritization**
```
User: "Prioritize these 5 features using RICE"
Claude: [Uses sprint-roadmap]

I'll need these inputs for each feature:
- Reach: How many users per quarter?
- Impact: 3 (massive) to 0.25 (minimal)
- Confidence: 100% (high) to 50% (low)
- Effort: Person-weeks

[Generates scored table and recommended order]
```

**Example 3: Quarterly roadmap**
```
User: "Generate a Q2 roadmap from our backlog"
Claude: [Uses sprint-roadmap]

Querying Jira for epics and priorities...

# Q2 2026 Roadmap: [Product]

## Theme: Scale and Reliability
[Maps epics to months with dependencies and risks]
```

## Success Criteria

- [ ] Sprint plan does not exceed 90% of average velocity
- [ ] Every sprint item has story points and acceptance criteria
- [ ] Sprint goal is specific and testable
- [ ] Prioritization framework applied consistently with scored table
- [ ] Dependencies documented with owners and dates
- [ ] Roadmap connects to quarterly objectives
- [ ] Release checklist completed before deploy

## Copy/Paste Ready

```
"Help me plan Sprint 24"
"Prioritize these features using RICE scoring"
"Generate a Q2 roadmap from our backlog"
"Groom the backlog and flag stale items"
"Map dependencies for the [feature] epic"
"Create a release plan for v2.1"
"Calculate sprint capacity for [N] devs over [N] weeks"
```