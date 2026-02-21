---
name: tech-spec
description: Generates implementation-ready technical specifications. Bridges PM requirements and engineering execution.
---

# Tech Spec Skill

## Purpose

Create technical specifications that engineers can implement without a kickoff meeting. Covers architecture, data models, APIs, and edge cases.

## Clarifying Interview

```
Tech Spec Interview:

1. **Feature/Component:**
2. **Type:** New feature | Refactor | Integration | Migration
3. **Scope:** Backend | Frontend | Full-stack | Infrastructure
4. **Constraints:**
   - Must integrate with: [systems]
   - Cannot change: [constraints]
   - Performance requirement: [if any]
5. **Reference PRD:** [link or "none"]
6. **Target reviewer:** Senior eng | Tech lead | Architect
```

## Output Format

```markdown
# [Feature] Technical Specification

**Author:** [Name] | **Status:** Draft/Review/Approved | **Date:** [Date]
**Reviewers:** [Names]

## Overview

### Problem Statement
[From PRD or 2-3 sentences]

### Proposed Solution
[High-level approach in 2-3 sentences]

### Out of Scope
- [Explicit exclusions]

---

## System Design

### Architecture Diagram
```
[ASCII diagram or "see attached"]
```

### Components
| Component | Responsibility | Tech Stack |
|-----------|---------------|------------|
| ...       | ...           | ...        |

### Data Flow
1. [Step 1]
2. [Step 2]
3. ...

---

## Data Model

### New Tables/Collections
```sql
-- Example schema
CREATE TABLE example (
  id UUID PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Schema Changes
| Table | Change | Migration Notes |
|-------|--------|-----------------|
| ...   | ...    | ...             |

---

## API Design

### Endpoints
```
POST /api/v1/resource
GET  /api/v1/resource/:id
PUT  /api/v1/resource/:id
```

### Request/Response Examples
```json
// POST /api/v1/resource
// Request
{
  "field": "value"
}

// Response
{
  "id": "uuid",
  "field": "value",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Error Handling
| Error | Code | Response |
|-------|------|----------|
| ...   | 4xx  | ...      |

---

## Edge Cases & Error Handling

| Scenario | Expected Behavior |
|----------|------------------|
| [Edge case 1] | [How to handle] |
| [Edge case 2] | [How to handle] |

---

## Security Considerations

- [ ] Authentication: [approach]
- [ ] Authorization: [approach]
- [ ] Data validation: [approach]
- [ ] Sensitive data handling: [approach]

---

## Testing Strategy

| Type | Coverage | Tools |
|------|----------|-------|
| Unit | [what] | [framework] |
| Integration | [what] | [framework] |
| E2E | [what] | [framework] |

---

## Rollout Plan

1. **Phase 1:** [Feature flag/internal testing]
2. **Phase 2:** [Beta/limited rollout]
3. **Phase 3:** [GA]

### Rollback Plan
[How to revert if issues arise]

---

## Open Questions

- [ ] [Question 1] - Owner: [name]
- [ ] [Question 2] - Owner: [name]

## Dependencies

| Dependency | Type | Status | Owner |
|------------|------|--------|-------|
| [Service X] | Blocking | [status] | [name] |
```

## Implementation Plan Structure

When the tech spec includes an implementation plan, structure tasks for maximum clarity:

### Bite-Sized Task Granularity

Each step should be one action (2-5 minutes):

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**
```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**
```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**
```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

### Precision Requirements

- **Exact file paths** for every file to create or modify
- **Complete code** in the plan (never "add appropriate validation")
- **Exact commands** with expected output
- **Line ranges** for modifications (`file.py:123-145`)

### Plan Header

When generating standalone implementation plans:

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]
**Architecture:** [2-3 sentences about approach]
**Tech Stack:** [Key technologies/libraries]
```

## Execution Handoff

After the spec/plan is approved, offer the execution choice:

1. **Subagent-Driven (this session)** — Use `subagent-driven-development` skill. Fresh subagent per task, two-stage review between tasks, fast iteration.

2. **Parallel Session (separate)** — Open new session with plan file. Batch execution with checkpoints. Use `parallel-instances` skill.

## Success Criteria

- [ ] Engineer can implement without clarification meetings
- [ ] All external dependencies identified with owners
- [ ] Edge cases documented (not discovered during code review)
- [ ] Rollback plan exists
- [ ] Security review checklist complete
- [ ] Implementation plan tasks are 2-5 min each with exact file paths and complete code

## Verification Steps

1. **Implementation Test:** Can a mid-level engineer start coding from this?
2. **Review Test:** Are all API contracts specific enough to mock?
3. **Edge Case Test:** Have you covered empty states, errors, and race conditions?
4. **Security Test:** Would this pass a security review?

## Context Gathering (Minimal)

Only pull these files if they exist:
- `README.md` - Project overview
- `docs/architecture.md` - Existing architecture
- Related API routes (grep for similar endpoints)
- Database schema file (if schema changes needed)

**Do NOT pull:** Entire src directory, all tests, unrelated modules

## Copy/Paste Ready

```
/tech-spec for user authentication with JWT
/tech-spec payment integration with Stripe
/tech-spec migrate from REST to GraphQL
```
