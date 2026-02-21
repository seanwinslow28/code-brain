# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built (clean, tested, maintainable)

**Only dispatch after spec compliance review passes.**

```
Task tool (code-reviewer):
  description: "Review code quality for Task N"

  Provide to the code-reviewer agent:
  - WHAT_WAS_IMPLEMENTED: [from implementer's report]
  - PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  - BASE_SHA: [commit before task]
  - HEAD_SHA: [current commit]
  - DESCRIPTION: [task summary]
```

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment

**If issues found:** Implementer subagent fixes them, then re-review.
