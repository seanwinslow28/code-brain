# Stakeholder Communication Templates Reference

## Table of Contents

- Quarterly Business Review (QBR)
- Release Announcement (External)
- Incident Post-Mortem Summary
- Monthly Product Review
- Board/Investor Update
- Crypto/Fintech Market Context Template

## Quarterly Business Review (QBR)

```markdown
# Q[N] Business Review: [Product/Team Name]
**Date:** [Date] | **Presenter:** [Name]

## Quarter Summary
[3-4 sentences capturing the quarter's narrative arc]

## Key Metrics

| Metric | Q[N-1] | Q[N] Target | Q[N] Actual | Delta |
|--------|--------|-------------|-------------|-------|
| [KPI 1] | [Value] | [Target] | [Actual] | [+/-] |
| [KPI 2] | [Value] | [Target] | [Actual] | [+/-] |
| [KPI 3] | [Value] | [Target] | [Actual] | [+/-] |

## What We Shipped
1. **[Feature 1]:** [Impact in business terms]
2. **[Feature 2]:** [Impact in business terms]
3. **[Feature 3]:** [Impact in business terms]

## What We Learned
- [Insight from user research or data]
- [Insight from experiments or A/B tests]
- [Insight from incidents or failures]

## What Didn't Ship (and Why)
- **[Deferred item]:** [Reason and new target]

## Q[N+1] Plan
| Priority | Initiative | Expected Impact | Investment |
|----------|-----------|----------------|------------|
| P0 | [Must-do] | [Impact] | [Effort] |
| P1 | [Should-do] | [Impact] | [Effort] |
| P2 | [Could-do] | [Impact] | [Effort] |

## Risks and Asks
- **Risk:** [Description and mitigation]
- **Ask:** [What you need from leadership]
```

## Release Announcement (External)

```markdown
# [Product Name] [Version] Release Notes

**Release Date:** [Date]

## What's New

### [Feature Name]
[User-friendly description focused on benefit, not implementation]

**How to use it:**
1. [Step 1]
2. [Step 2]

### [Feature Name]
[Description]

## Improvements
- [Improvement 1 in user terms]
- [Improvement 2 in user terms]

## Bug Fixes
- Fixed an issue where [user-visible symptom]
- Resolved [user-visible symptom]

## Breaking Changes
- **[Change]:** [What users need to do differently]
- **Migration guide:** [Link or inline steps]

## Coming Soon
- [Teaser for next release]
```

## Incident Post-Mortem Summary

```markdown
# Incident Post-Mortem: [Incident Title]
**Date:** [Date] | **Severity:** P[0-3] | **Duration:** [Time]

## Summary
[1-2 sentences: what happened and user impact]

## Timeline
| Time (UTC) | Event |
|------------|-------|
| [HH:MM] | [First alert or user report] |
| [HH:MM] | [Investigation started] |
| [HH:MM] | [Root cause identified] |
| [HH:MM] | [Fix deployed] |
| [HH:MM] | [Full recovery confirmed] |

## Impact
- **Users affected:** [Number or percentage]
- **Duration:** [Total downtime]
- **Revenue impact:** [If applicable]

## Root Cause
[Technical explanation, adapted to audience]

## What Went Well
- [Effective response or detection]

## What Went Wrong
- [Gap in monitoring, process, or system]

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Preventive measure] | [Name] | [Date] | Open |
| [Monitoring improvement] | [Name] | [Date] | Open |
```

## Monthly Product Review

```markdown
# Monthly Product Review: [Month Year]
**Team:** [Team Name] | **Author:** [Name]

## Scorecard

| Category | Status | Notes |
|----------|--------|-------|
| Feature Delivery | On Track / Behind / Ahead | [Context] |
| Quality | Green / Yellow / Red | [Bug count trend] |
| User Satisfaction | [Score/Trend] | [Source: NPS, CSAT] |
| Technical Health | Green / Yellow / Red | [Debt, performance] |

## Shipped This Month
- [Feature 1 with adoption data if available]
- [Feature 2]

## In Progress
- [Feature with expected completion]

## User Feedback Themes
1. **[Theme]:** [Quote or summary] - [Action taken]
2. **[Theme]:** [Quote or summary] - [Action planned]

## Next Month Priorities
1. [Priority 1 with rationale]
2. [Priority 2]
```

## Board/Investor Update

```markdown
# [Company/Product] Update: [Month Year]

## Highlights
- [Most impressive metric or milestone]
- [Second highlight]

## Key Metrics
| Metric | Last Period | This Period | Trend |
|--------|-----------|-------------|-------|
| MAU | [Value] | [Value] | [Arrow] |
| Revenue | [Value] | [Value] | [Arrow] |
| [Custom] | [Value] | [Value] | [Arrow] |

## Product Progress
[2-3 sentences on what shipped and why it matters]

## Market Context
[1-2 sentences on industry trends affecting strategy]

## Challenges
- [Challenge with mitigation plan]

## Capital/Resource Needs
- [If applicable]
```

## Crypto/Fintech Market Context Template

Add this section to any report when market conditions are relevant:

```markdown
## Market Context
- **BTC:** $[Price] ([Change]% this period)
- **Market sentiment:** [Fear & Greed Index or qualitative]
- **Regulatory:** [Recent regulatory developments affecting product]
- **Competitive:** [Competitor launches or market shifts]
- **Impact on product:** [How market conditions affect our priorities]
```

## Tone Guide by Audience

| Audience | Lead With | Avoid | Format |
|----------|-----------|-------|--------|
| CEO/Board | Revenue, growth, market position | Technical details, jargon | 1-page max, bullets |
| VP Engineering | Risk, velocity, technical debt | Marketing language | Metrics-heavy, tables |
| Product Team | User impact, experiment results | Implementation details | Narrative with data |
| Sales Team | Customer-facing features, competitive edge | Internal process, bugs | Feature-benefit pairs |
| Design Team | UX improvements, research findings | Backend changes | Visual emphasis |
| External Users | Benefits, how-to, what changed | Internal reasoning | Simple, scannable |
