---
name: org-definition-of-done
description: Validates work against organizational Definition of Done criteria before marking complete
---

# Organization Definition of Done Skill

## When to Use

Use this skill when:
- Completing features or tasks
- Preparing code for review
- Validating work before deployment
- Ensuring compliance with organizational standards
- Closing tickets or stories

## Examples

**Example 1: DoD validation**
```
User: "Check if this feature meets our Definition of Done"
Claude: [Uses org-definition-of-done skill] Definition of Done checklist:

✓ Code written and reviewed
✓ Unit tests written (coverage: 85%)
✓ Integration tests passing
✓ Documentation updated
✓ Code follows styleguide
✓ Security review completed
✓ Performance tested
✓ Accessibility requirements met
⚠ Missing: QA sign-off
⚠ Missing: Product owner approval

**Status:** 8/10 criteria met - needs QA and PO approval
```

**Example 2: Pre-deployment check**
```
User: "Is this ready to deploy?"
Claude: [Uses org-definition-of-done skill] Pre-deployment DoD check:

**Code Quality:**
✓ All tests passing
✓ No linter errors
✓ Code review approved

**Documentation:**
✓ README updated
✓ API docs updated
✓ Changelog entry added

**Operations:**
✓ Monitoring configured
✓ Alerts set up
✓ Rollback plan documented

**Ready for deployment:** Yes
```

## Definition of Done Criteria

This skill validates:
- Code complete and reviewed
- Tests written and passing (coverage thresholds)
- Documentation updated
- Code follows styleguide and standards
- Security review completed
- Performance requirements met
- Accessibility compliance
- QA sign-off received
- Product owner approval
- Deployment checklist completed

## Copy/Paste Ready

To use this skill:
- "Check Definition of Done for this feature"
- "Validate work against DoD criteria"
- "Is this ready to mark as done?"
