---
name: quick-prd
description: Rapid PRD generation with smart clarifying questions. Gets you from idea to spec in under 5 minutes.
---

# Quick PRD Skill

## Purpose

Generate actionable PRDs fast. Asks only the questions that matter, outputs structured specs ready for engineering.

## Clarifying Interview (Always Run First)

Before generating any PRD, ask these questions in a single prompt:

```
Quick PRD Interview:

1. **What?** One-sentence feature description:
2. **Who?** Primary user persona (or "internal team"):
3. **Why now?** What's the trigger/urgency?
4. **Scope:** S/M/L (S = days, M = weeks, L = months)
5. **Blockers?** Any known dependencies or constraints?
6. **Success metric?** How do we know it worked?

Optional (skip if unknown):
- Existing related tickets/docs:
- Technical constraints:
```

## Output Format

Generate a PRD with these sections ONLY:

```markdown
# [Feature Name] PRD

**Status:** Draft | **Owner:** [User] | **Created:** [Date]

## TL;DR
[2-3 sentences max]

## Problem
- What's broken/missing
- Who it affects
- Cost of inaction

## Solution
- Core functionality (bullet points)
- What's explicitly OUT of scope

## User Stories
[ ] As a [persona], I want [action] so that [outcome]
[ ] ...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] ...

## Technical Notes
[Only if relevant - keep to 3 bullets max]

## Success Metrics
| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| ...    | ...     | ...    | ...       |

## Open Questions
- [ ] Question 1
- [ ] Question 2
```

## Success Criteria

The PRD is successful when:
- [ ] Engineering can start working with no follow-up questions
- [ ] All acceptance criteria are testable (yes/no answers)
- [ ] Success metrics are measurable numbers
- [ ] Scope is clear (what's in AND what's out)
- [ ] Takes < 5 minutes to read

## Verification Steps

1. **Testability check:** Can QA write test cases from acceptance criteria?
2. **Scope check:** Is there exactly ONE way to interpret "done"?
3. **Metric check:** Can you query a dashboard for success metrics?
4. **Handoff check:** Would you feel comfortable sending this to eng without a meeting?

## Anti-Patterns to Avoid

- Vague requirements ("improve UX")
- Missing edge cases
- Requirements that are actually solutions
- Success metrics you can't measure
- PRDs longer than 2 pages

## Copy/Paste Ready

```
/quick-prd Login with SSO
/quick-prd "User can export data to CSV"
/quick-prd Budget notification feature - triggered by Q1 planning
```
