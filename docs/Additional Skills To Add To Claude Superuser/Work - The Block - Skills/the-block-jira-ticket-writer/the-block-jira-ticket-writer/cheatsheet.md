# The Block Jira Ticket Writing - Quick Reference

## Ticket Title Formats

| Type | Format | Example |
|------|--------|---------|
| Epic | `{Feature Name}` | `Sponsored Courses Integration` |
| Design | `[Design] {Feature Name}` | `[Design] Job Board Pages` |
| Implementation | `[Implementation] {Feature Name}` | `[Implementation] Homepage Module` |
| Database | `DB > {Feature Name}` | `DB > Jobs database on Laravel` |

---

## Epic Description Template

```
{One-sentence summary}

**Problem:** {What we're solving}

**Solution:** {How we're solving it}

**Scope:**
• {Deliverable 1}
• {Deliverable 2}

**Success Metrics:**
• {Metric 1 with target}
• {Metric 2 with target}
```

---

## Design Story Template

```
As the product team, we need {designs} so that {engineering can implement}.

**Summary:** {Design deliverables overview}

**Acceptance Criteria:**
• {Design deliverable 1}
• {Design deliverable 2}
• Mobile-responsive variants for all components
• Design specs handed off in Figma with component documentation
```

---

## Implementation Story Template

```
As a user, I want to {action} so that {benefit}.

**Summary:** {Technical overview}

**Acceptance Criteria:**
• {Requirement 1}
• {Requirement 2}
• Analytics events fire on {key interactions}
• Cross-browser testing (Chrome, Safari, Firefox, Edge)

**Technical Notes:**
• {Implementation detail}
• {Dependency note}
```

---

## Component Quick Guide

| Feature Area | Component(s) |
|--------------|--------------|
| Campus/LMS | `Campus` |
| Homepage, articles | `theblock.co` |
| Feature spans both | `Campus` + `theblock.co` |
| Pro subscription | `Pro News`, `Pro Research`, etc. |
| CMS/publishing | `Wordpress` |

---

## Labels

- `NeedsDesign` - Needs design before dev
- `frontend` - UI work
- `BACKEND` - API/DB work

---

## Checklist Before Creating

- [ ] Epic has Problem/Solution/Scope/Metrics
- [ ] Design story lists all Figma deliverables
- [ ] Implementation stories have user story format
- [ ] Acceptance criteria are testable
- [ ] Technical notes included where helpful
- [ ] Correct components assigned
- [ ] Correct labels assigned
