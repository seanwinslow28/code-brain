---
name: org-definition-of-done
description: Definition of Done validator for features, bug fixes, and releases. Checks code quality, testing, documentation, accessibility, security, and stakeholder sign-off against configurable criteria. Use when asked "is this done?", "DoD check", "ready to ship?", "validate completion", "pre-merge check", or "definition of done".
---

# Definition of Done

## Purpose

Validate work against structured Definition of Done (DoD) criteria before marking tickets complete, merging PRs, or deploying to production. Provides configurable checklists for different work types (feature, bug fix, refactor, spike) and catches gaps before stakeholders do.

## When to Use

- **Feature completion:** "Is this feature done?" / "DoD check for PROJ-123"
- **Pre-merge:** "Is this PR ready to merge?"
- **Pre-deploy:** "Is this ready to deploy?"
- **Ticket closure:** "Can I close this ticket?"
- **Sprint review:** "Which items meet DoD?"

## DoD by Work Type

### Feature (Story)

```markdown
## Definition of Done — Feature

### Code
- [ ] Code written and compiles without errors
- [ ] Code reviewed and approved (PR approved by 1+ reviewer)
- [ ] No TODO/FIXME/HACK comments left unresolved
- [ ] No unnecessary code duplication introduced

### Testing
- [ ] Unit tests written for new logic
- [ ] Integration tests cover key flows
- [ ] Edge cases tested (empty states, errors, boundaries)
- [ ] All existing tests still pass
- [ ] Manual QA completed on staging

### Documentation
- [ ] Public API changes documented
- [ ] README updated if setup/usage changed
- [ ] Inline comments for non-obvious logic
- [ ] Changelog entry added (if applicable)

### Quality
- [ ] Linter passes with no new warnings
- [ ] No new security vulnerabilities introduced
- [ ] Performance acceptable (no regressions)
- [ ] Accessible (keyboard nav, screen reader, contrast)

### Process
- [ ] Acceptance criteria from ticket met
- [ ] Stakeholder/PO reviewed and approved
- [ ] Jira ticket updated with final status
```

### Bug Fix

```markdown
## Definition of Done — Bug Fix

### Fix
- [ ] Root cause identified and documented
- [ ] Fix addresses root cause (not just symptoms)
- [ ] Fix verified on staging environment
- [ ] No regressions in related functionality

### Testing
- [ ] Regression test added to prevent recurrence
- [ ] All existing tests pass
- [ ] Manual verification on staging

### Documentation
- [ ] Bug ticket updated with root cause analysis
- [ ] Fix description in PR/commit message

### Process
- [ ] Original reporter confirmed fix (if applicable)
- [ ] Related tickets checked for same issue
```

### Refactor

```markdown
## Definition of Done — Refactor

### Code
- [ ] Behavior unchanged (verified by existing tests)
- [ ] All existing tests pass without modification
- [ ] Code measurably improved (complexity, duplication, readability)

### Testing
- [ ] No new tests needed (behavior unchanged)
- [ ] If tests were modified, changes are cosmetic only

### Documentation
- [ ] Architecture decision documented (if structural change)
- [ ] No public API changes (or documented if unavoidable)
```

### Spike / Research

```markdown
## Definition of Done — Spike

### Deliverables
- [ ] Original question answered with evidence
- [ ] Findings documented (Confluence, ADR, or ticket comment)
- [ ] Recommendation provided with trade-offs
- [ ] Follow-up tickets created for implementation (if applicable)
- [ ] Time-box respected (did not exceed allocated time)
```

## Release DoD

For production deployments, additional checks:

```markdown
## Definition of Done — Release

### Pre-Release
- [ ] All sprint items meet their individual DoD
- [ ] QA sign-off on staging environment
- [ ] Release notes drafted
- [ ] Stakeholders notified of upcoming release
- [ ] Rollback plan documented and tested

### Deploy
- [ ] Deployed to production successfully
- [ ] Smoke tests pass on production
- [ ] Error rates normal for 1 hour post-deploy
- [ ] Performance metrics within expected range

### Post-Release
- [ ] Jira tickets closed with fixVersion
- [ ] Release notes published
- [ ] Stakeholders notified of completion
- [ ] Monitoring alerts configured for new features
```

## Running a DoD Check

### Step 1: Identify Work Type

| Ticket Type | DoD Template |
|-------------|-------------|
| Story / Feature | Feature DoD |
| Bug | Bug Fix DoD |
| Refactor / Tech Debt | Refactor DoD |
| Spike / Research | Spike DoD |
| Release | Release DoD |

### Step 2: Gather Evidence

For each checklist item, check:
- **Code:** `git diff`, PR review status, linter output
- **Tests:** Test runner output, coverage report
- **Docs:** File changes in docs/, README, CHANGELOG
- **Process:** Jira ticket status, reviewer approvals, stakeholder comments

### Step 3: Report Status

```
DoD Check — PROJ-123: Add user authentication

Code:         4/4 PASS
Testing:      4/5 WARN — Missing edge case tests for expired tokens
Documentation: 3/3 PASS
Quality:      3/4 WARN — Accessibility not verified
Process:      2/3 INCOMPLETE — Awaiting PO approval

Overall: 16/19 criteria met — NOT READY
Action needed:
  1. Add edge case tests for token expiration
  2. Verify keyboard navigation on login form
  3. Get PO sign-off
```

## Customizing DoD

Teams should adapt the DoD to their context. Common customizations:

| Team Context | Add | Remove |
|-------------|-----|--------|
| Healthcare/Finance | Compliance review, audit trail | — |
| Startup/MVP | — | Accessibility, full coverage |
| Open source | License check, contributor guide | Stakeholder approval |
| Data pipeline | Data validation, monitoring | UI/accessibility |
| Mobile app | Device testing matrix, app store guidelines | — |

## Examples

**Example 1: Feature DoD check**
```
User: "Is this feature done?"
Claude: [Uses org-definition-of-done]

Running DoD check against your staged changes and PR...

Code:          [PASS] Reviewed, approved, clean
Testing:       [PASS] Unit + integration tests, all green
Documentation: [WARN] API docs not updated — new endpoint undocumented
Quality:       [PASS] Linter clean, no security issues
Process:       [PASS] AC met, PO approved

Status: 4/5 — Update API documentation, then ready to merge.
```

**Example 2: Pre-deploy check**
```
User: "Is this ready to deploy?"
Claude: [Uses org-definition-of-done]

Running Release DoD...

Pre-Release:   [PASS] All items meet DoD, QA signed off
Deploy Plan:   [PASS] Rollback plan documented
Notification:  [WARN] Stakeholder email not sent yet

Ready to deploy after sending stakeholder notification.
```

**Example 3: Sprint review**
```
User: "Which sprint items meet DoD?"
Claude: [Uses org-definition-of-done]

Sprint 24 DoD Status:
| Ticket | Type | DoD Score | Status |
|--------|------|-----------|--------|
| PROJ-201 | Feature | 19/19 | DONE |
| PROJ-205 | Bug | 10/10 | DONE |
| PROJ-210 | Feature | 16/19 | NOT DONE — missing tests |
| PROJ-215 | Spike | 5/5 | DONE |

3/4 items meet DoD. PROJ-210 needs test coverage.
```

## Success Criteria

- [ ] Correct DoD template selected for work type
- [ ] Each checklist item verified with evidence (not assumed)
- [ ] Gaps clearly reported with specific action items
- [ ] Status summary provided (X/Y criteria met)
- [ ] "NOT READY" items have clear remediation steps

## Copy/Paste Ready

```
"Is this feature done? Run DoD check."
"Check Definition of Done for PROJ-123"
"Is this PR ready to merge?"
"Run pre-deploy checklist"
"Which sprint items meet DoD?"
"DoD check for this bug fix"
```