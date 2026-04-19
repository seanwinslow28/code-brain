# Prioritization Frameworks Reference

## Table of Contents

- RICE Scoring - Complete Guide
- MoSCoW Method - Decision Rules
- Impact/Effort Matrix - Categorization
- Weighted Scoring Model
- Kano Model
- Framework Selection Guide

## RICE Scoring - Complete Guide

### Factor Definitions

**Reach:** How many users will this affect in a defined time period (usually per quarter)?
- Use actual data when possible (MAU, segment size, support ticket volume)
- For new features, use projected reach based on similar features
- Document your source: "Reach based on Q3 active users in enterprise segment"

**Impact:** How much will each user be affected?
| Score | Label | Definition |
|-------|-------|-----------|
| 3 | Massive | Fundamental change to user workflow |
| 2 | High | Significant improvement to common task |
| 1 | Medium | Noticeable improvement |
| 0.5 | Low | Minor improvement, most users won't notice |
| 0.25 | Minimal | Barely perceptible change |

**Confidence:** How sure are you about Reach and Impact estimates?
| Score | Label | Evidence Required |
|-------|-------|------------------|
| 100% | High | Data from experiments, research, or analogous features |
| 80% | Medium | Strong qualitative signal (user interviews, competitor analysis) |
| 50% | Low | Gut feeling or limited data |

**Effort:** Person-weeks of work across all disciplines (engineering, design, QA).
- Include design, development, QA, and documentation time
- Round to nearest 0.5 weeks
- If uncertain, estimate high (bias toward caution)

### Worked Example

Feature: Add CSV export to dashboard

| Factor | Value | Reasoning |
|--------|-------|-----------|
| Reach | 2,000/quarter | Based on dashboard MAU of 5,000, 40% of users export data |
| Impact | 2 (High) | Currently users screenshot tables - major friction |
| Confidence | 80% | 15 support tickets/month requesting this feature |
| Effort | 1.5 weeks | Backend serialization + UI button + tests |

**RICE Score:** (2000 x 2 x 0.8) / 1.5 = **2,133**

### Comparison Table Template

| Feature | Reach | Impact | Confidence | Effort | RICE | Rank |
|---------|-------|--------|-----------|--------|------|------|
| Feature A | [N] | [0.25-3] | [50-100%] | [weeks] | [calc] | [#] |
| Feature B | [N] | [0.25-3] | [50-100%] | [weeks] | [calc] | [#] |

### Common Pitfalls

- **Inflating Reach:** Use actual data, not "all users could benefit"
- **Impact bias:** Compare to existing features of known impact
- **Confidence theater:** 50% is fine. Don't pretend certainty you don't have
- **Effort underestimation:** Include design, QA, documentation, not just development

## MoSCoW Method - Decision Rules

### Category Definitions

| Category | Test Question | Sprint Rule |
|----------|--------------|-------------|
| **Must Have** | "Will the sprint fail without this?" | Always included first |
| **Should Have** | "Is this important but survivable without?" | Include if capacity remains |
| **Could Have** | "Would this be nice but not missed?" | Stretch goal only |
| **Won't Have** | "Can we explicitly defer this?" | Exclude with documented reason |

### Application Rules

1. **Must Haves** should never exceed 60% of sprint capacity
2. **Should Haves** fill the next 20% of capacity
3. **Could Haves** use remaining 20% (stretch goals)
4. Every **Won't Have** gets a target sprint for re-evaluation

### Worked Example

Sprint capacity: 30 story points

| Item | Category | Points | Running Total |
|------|----------|--------|---------------|
| Auth bug fix | Must | 5 | 5 (17%) |
| Payment integration | Must | 13 | 18 (60%) |
| Error logging | Should | 5 | 23 (77%) |
| Dashboard filter | Could | 5 | 28 (93%) |
| Dark mode | Won't | 8 | - (deferred to Sprint 26) |

## Impact/Effort Matrix - Categorization

### Quadrant Definitions

```
                High Impact
                    |
     QUICK WINS     |    BIG BETS
     (Do First)     |    (Plan Carefully)
     Low effort,    |    High effort,
     high return    |    high return
  ------------------|------------------
     FILL-INS       |    TIME SINKS
     (Do If Idle)   |    (Avoid/Defer)
     Low effort,    |    High effort,
     low return     |    low return
                    |
                Low Impact
        Low Effort ----- High Effort
```

### Scoring Guide

**Impact (1-5):**
- 5: Directly moves primary KPI
- 4: Affects multiple user segments
- 3: Improves one important workflow
- 2: Minor improvement
- 1: Cosmetic or edge case

**Effort (1-5):**
- 1: <1 day
- 2: 1-3 days
- 3: 1-2 weeks
- 4: 2-4 weeks
- 5: >1 month

## Weighted Scoring Model

For decisions with multiple criteria beyond RICE:

| Feature | User Value (x3) | Revenue (x2) | Effort (x-1) | Strategic (x2) | Total |
|---------|-----------------|--------------|--------------|-----------------|-------|
| Feature A | 4 x3 = 12 | 3 x2 = 6 | 3 x-1 = -3 | 5 x2 = 10 | 25 |
| Feature B | 5 x3 = 15 | 2 x2 = 4 | 4 x-1 = -4 | 3 x2 = 6 | 21 |

Customize weights based on current company priorities.

## Kano Model

Categorize features by user satisfaction curve:

| Category | Definition | Example | Priority |
|----------|-----------|---------|----------|
| **Must-be** | Expected, absence causes dissatisfaction | Login works | Always implement |
| **Performance** | More is better, linear satisfaction | Faster load times | ROI-based |
| **Attractive** | Unexpected delight, absence is fine | Dark mode | Differentiation |
| **Indifferent** | User doesn't care either way | Internal refactor | Skip unless technical need |
| **Reverse** | Some users actively dislike it | Auto-play videos | Avoid or make optional |

## Framework Selection Guide

| Situation | Recommended Framework |
|-----------|----------------------|
| Comparing 5+ features with data | RICE |
| Sprint planning with fixed capacity | MoSCoW |
| Quick triage of a large backlog | Impact/Effort Matrix |
| Multiple stakeholder perspectives | Weighted Scoring |
| Understanding user satisfaction drivers | Kano Model |
| Startup with limited data | Impact/Effort (simplest) |
| Enterprise with compliance requirements | Weighted Scoring (add compliance weight) |
