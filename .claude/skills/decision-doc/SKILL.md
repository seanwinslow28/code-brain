---
name: decision-doc
description: Structured decision documentation. Captures context, options, and rationale so future-you understands past decisions.
---

# Decision Doc Skill

## Purpose

Document decisions so you (or your team) never ask "why did we do it this way?" again. Lightweight enough to actually use.

## Clarifying Interview

```
Decision Doc Setup:

1. **Decision type:** Technical | Product | Process | Hiring | Investment | Personal
2. **Reversibility:** One-way door | Two-way door | Easily reversible
3. **Stakeholders:** Just me | Team | Cross-functional | Leadership
4. **Timeline:** Need to decide by ___
5. **Context:** [1-2 sentences on what prompted this]
```

## Output Format

### Standard Decision Doc

```markdown
# Decision: [Clear, specific title]

**Status:** 🟡 Proposed | 🟢 Decided | 🔴 Superseded
**Date:** [YYYY-MM-DD]
**Owner:** [Name]
**Stakeholders:** [Names/roles]

---

## Context

[2-3 sentences: What situation led to this decision? What problem are we solving?]

## Decision

**We will:** [One sentence stating the decision clearly]

## Options Considered

### Option A: [Name] ✅ Selected
**Description:** [What this option entails]

| Pros | Cons |
|------|------|
| + Pro 1 | - Con 1 |
| + Pro 2 | - Con 2 |

**Estimated effort/cost:** [if relevant]

### Option B: [Name]
**Description:** [What this option entails]

| Pros | Cons |
|------|------|
| + Pro 1 | - Con 1 |
| + Pro 2 | - Con 2 |

**Why not chosen:** [1 sentence]

### Option C: Do Nothing
**Why not chosen:** [What happens if we don't decide]

## Rationale

[2-3 sentences explaining WHY Option A was chosen. What was the deciding factor?]

## Consequences

**What this enables:**
- [Benefit 1]
- [Benefit 2]

**What this requires:**
- [Commitment 1]
- [Tradeoff 1]

**What we're explicitly NOT doing:**
- [Scope exclusion]

## Success Criteria

How will we know this was the right decision?
- [ ] Metric/outcome 1
- [ ] Metric/outcome 2

## Review Date

Revisit this decision on: [Date, if applicable]

---

## Changelog
| Date | Change | Author |
|------|--------|--------|
| YYYY-MM-DD | Initial decision | [Name] |
```

### Lightweight Version (for smaller decisions)

```markdown
# Decision: [Title]

**Date:** [Date] | **Owner:** [Name]

## Context
[1-2 sentences]

## Decision
[One clear sentence]

## Why
[1-2 sentences on rationale]

## Alternatives Rejected
- [Option B]: [Why not, one line]
- [Option C]: [Why not, one line]
```

### ADR Format (Architecture Decision Record)

```markdown
# ADR-[number]: [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-[n]
**Date:** [YYYY-MM-DD]

## Context
[Technical context and problem statement]

## Decision
[The decision and its justification]

## Consequences
[Positive and negative consequences of this decision]
```

## Decision Types & Templates

| Type | Key Questions | Template |
|------|--------------|----------|
| **Technical** | Performance? Maintainability? Scalability? | Full ADR |
| **Product** | User value? Business impact? Opportunity cost? | Standard |
| **Process** | Team efficiency? Sustainability? Adoption? | Lightweight |
| **Hiring** | Skills needed? Culture fit? Growth potential? | Standard |
| **Personal** | Alignment with goals? Reversibility? Regret minimization? | Lightweight |

## Success Criteria

- [ ] A new team member can understand the decision without asking questions
- [ ] The rationale is captured (not just the what, but the why)
- [ ] Rejected options are documented (prevents re-litigating)
- [ ] Decision is findable (in shared location with clear naming)

## Verification Steps

1. **Clarity Test:** Can someone not in the room understand this?
2. **Completeness Test:** Are the top 2-3 alternatives documented?
3. **Rationale Test:** Is the "why" clear, not just the "what"?
4. **Future Test:** Will this be useful in 6 months when context is forgotten?

## Naming Convention

```
YYYY-MM-DD-[type]-[brief-description].md

Examples:
2024-01-15-tech-use-postgres-over-mongodb.md
2024-01-20-product-launch-with-invite-only.md
2024-02-01-process-switch-to-weekly-sprints.md
```

## Storage Location

```
docs/
├── decisions/
│   ├── technical/
│   │   ├── 2024-01-15-database-selection.md
│   │   └── 2024-02-01-api-versioning.md
│   ├── product/
│   └── process/
```

## Copy/Paste Ready

```
/decision-doc tech: Should we use PostgreSQL or MongoDB?
/decision-doc product: Launch strategy for new feature
/decision-doc process: Switching from Jira to Linear
/decision-doc personal: Should I take the new role?
/decision-doc lightweight: Which testing framework to use
```

## Anti-Patterns

- Decisions without rationale ("we just decided")
- Missing alternatives (looks like there was no analysis)
- Too much detail (nobody will read a 10-page decision doc)
- Not findable (decisions buried in Slack threads or email)
- Never revisited (outdated decisions treated as permanent)
