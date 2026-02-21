---
name: sprint-roadmap
description: Sprint planning and roadmap management assistant. Handles capacity calculation, story point estimation, sprint goals, backlog grooming, prioritization with RICE and MoSCoW frameworks, dependency mapping, and release planning. Use when asked about sprint planning, roadmaps, backlog grooming, prioritization, release planning, or capacity planning.
---

# Sprint and Roadmap Planning

## Purpose

Automate and structure sprint planning, roadmap generation, backlog grooming, and release planning workflows. Apply prioritization frameworks consistently, track velocity for capacity planning, and manage dependencies across teams. Guide beginner PMs through agile ceremonies with structured prompts and templates.

## When to Use

- User asks to plan a sprint or calculate capacity
- User needs to groom or prioritize the backlog
- User wants to generate or update a roadmap
- User asks to apply RICE, MoSCoW, or impact/effort scoring
- User needs to map dependencies between features or teams
- User asks about release planning or go-to-market coordination

## Examples

**Example 1: Sprint planning**
```
User: "Help me plan Sprint 24"
Claude: [Uses sprint-roadmap] Let me gather the inputs:

1. What's the sprint duration? (1 week / 2 weeks)
2. Team size and any PTO this sprint?
3. What's your average velocity? (story points per sprint)
4. Sprint goal - what's the ONE thing that must ship?

[After answers]

Sprint 24 Plan:
- Capacity: 4 devs x 2 weeks = 8 dev-weeks, minus 2 days PTO = ~35 story points
- Historical velocity: 32 pts avg (last 3 sprints)
- Recommended load: 30 pts (leave buffer for unplanned work)

Priority items from backlog:
| Ticket | Points | Priority | Fits? |
|--------|--------|----------|-------|
| PROJ-201 | 8 | P0 - Must | Yes (8/30) |
| PROJ-205 | 5 | P0 - Must | Yes (13/30) |
| PROJ-210 | 13 | P1 - Should | Yes (26/30) |
| PROJ-215 | 5 | P2 - Could | Stretch (31/30) |

Recommendation: Commit to PROJ-201, 205, 210 (26 pts). PROJ-215 as stretch goal.
```

**Example 2: Backlog prioritization with RICE**
```
User: "Prioritize these 5 features using RICE"
Claude: [Uses sprint-roadmap]

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|-----------|--------|-----------|
| SSO Login | 5000/q | 3 | 90% | 3 weeks | 4,500 |
| CSV Export | 2000/q | 2 | 80% | 1 week | 3,200 |
| Dark Mode | 8000/q | 1 | 70% | 2 weeks | 2,800 |
| API v2 | 500/q | 3 | 60% | 4 weeks | 225 |
| Notifications | 3000/q | 2 | 85% | 2 weeks | 2,550 |

Recommended order: SSO Login > CSV Export > Dark Mode > Notifications > API v2
```

**Example 3: Roadmap generation**
```
User: "Generate a Q2 roadmap from our backlog"
Claude: [Uses sprint-roadmap]

# Q2 2026 Roadmap

## Theme: Scale and Reliability

### April (Sprint 24-25)
- [P0] SSO Login (Epic PROJ-200)
- [P0] Database migration (Epic PROJ-190)

### May (Sprint 26-27)
- [P1] CSV Export (Epic PROJ-210)
- [P1] Dashboard redesign (Epic PROJ-220)

### June (Sprint 28-29)
- [P1] API v2 launch (Epic PROJ-230)
- [P2] Dark mode (Epic PROJ-240)

Dependencies: Database migration must complete before API v2.
Risk: SSO depends on identity provider contract (ETA: March 28).
```

## Sprint Planning Workflow

### Step 1: Calculate Capacity

```
Capacity Formula:
  Team members: [N]
  Sprint length: [days]
  PTO/holidays: [days]
  Overhead (meetings, reviews): 20%

  Available dev-days = (N x sprint_days - PTO) x 0.8
  Story point capacity = Available dev-days x (velocity / prev_dev-days)
```

### Step 2: Review Velocity

Track velocity across sprints for accurate planning:

| Sprint | Planned | Completed | Velocity | Notes |
|--------|---------|-----------|----------|-------|
| Sprint 21 | 35 | 30 | 30 | Holiday week |
| Sprint 22 | 32 | 34 | 34 | Over-delivered |
| Sprint 23 | 33 | 32 | 32 | Normal |
| **Average** | | | **32** | Use for planning |

**Rule:** Plan to 80-90% of average velocity. Never plan to 100%.

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

For the complete prioritization framework reference with worked examples, see `references/frameworks.md`.

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

## Backlog Grooming Workflow

Run grooming sessions with this checklist:

1. **Review each item:**
   - Is the description clear enough to estimate?
   - Are acceptance criteria defined?
   - Are dependencies identified?

2. **Estimate effort:**
   - Use planning poker or T-shirt sizing
   - Compare to previously completed items of similar complexity
   - Flag items >13 points for decomposition

3. **Prioritize:**
   - Apply chosen framework (RICE, MoSCoW, or impact/effort)
   - Verify alignment with quarterly goals
   - Identify items that can be cut or deferred

4. **Clean up:**
   - Close stale items (no activity >60 days, no champion)
   - Merge duplicates
   - Ensure every item has an epic parent

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

Track dependencies using a simple table:

| Ticket | Depends On | Type | Status | Risk |
|--------|-----------|------|--------|------|
| PROJ-201 | PROJ-190 | Technical | PROJ-190 in progress | Medium |
| PROJ-210 | Legal sign-off | External | Waiting | High |
| PROJ-220 | Design complete | Cross-team | Done | Low |

Use JQL to find blocking relationships:
```
issueFunction in linkedIssuesOf("project = PROJ AND sprint in openSprints()", "blocks")
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
- [ ] Schedule retrospective
```

## Success Criteria

- [ ] Sprint plan does not exceed 90% of average velocity
- [ ] Every sprint item has story points and acceptance criteria
- [ ] Sprint goal is specific and testable
- [ ] Prioritization framework applied consistently
- [ ] Dependencies documented with owners and dates
- [ ] Roadmap connects to quarterly objectives
- [ ] Release checklist completed before deploy

## Copy/Paste Ready

```
"Help me plan Sprint 24"
"Prioritize these features using RICE scoring"
"Generate a Q2 roadmap from our backlog"
"Groom the backlog and flag stale items"
"Map dependencies for the payment feature epic"
"Create a release plan for v2.1"
```
