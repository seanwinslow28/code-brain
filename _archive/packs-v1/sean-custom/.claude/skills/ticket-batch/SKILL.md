---
name: ticket-batch
description: Batch-create Jira/Linear tickets from PRDs, meeting notes, or brain dumps. Outputs copy-paste ready tickets.
---

# Ticket Batch Skill

## Purpose

Convert unstructured input (PRD, notes, ideas) into structured, ready-to-paste tickets for Jira or Linear. No manual reformatting needed.

## Clarifying Interview

Ask once per batch:

```
Ticket Batch Setup:

1. **Source:** PRD | Meeting notes | Brain dump | Other
2. **Target:** Jira | Linear | GitHub Issues
3. **Ticket type:** Story | Task | Bug | Mixed
4. **Epic/Project:** Link to (or "create new"):
5. **Sprint:** Current | Next | Backlog
6. **Estimation:** Include points? (Y/N, what scale?)
```

## Input Patterns

The skill handles these input types:

**From PRD:** Extract user stories from acceptance criteria
**From Meeting Notes:** Parse action items into tickets
**From Brain Dump:** Structure random thoughts into epics/stories
**From Bug Report:** Create bug ticket with repro steps

## Output Format (Jira)

```markdown
---
### TICKET 1 of N

**Type:** Story | Task | Bug
**Title:** [Verb] [Object] [Context]
**Epic:** [EPIC-123]

**Description:**
As a [persona], I want [action] so that [benefit].

**Acceptance Criteria:**
- [ ] AC1
- [ ] AC2
- [ ] AC3

**Technical Notes:**
- Note 1

**Labels:** [feature-area], [priority]
**Points:** [X]

---
```

## Output Format (Linear)

```markdown
---
### ISSUE 1 of N

**Title:** [Verb] [Object]
**Project:** [Project Name]
**Status:** Backlog

**Description:**
[Clear problem/task statement]

**Acceptance Criteria:**
- [ ] AC1
- [ ] AC2

**Labels:** [feature], [priority]
**Estimate:** [X]

---
```

## Success Criteria

- [ ] Each ticket has a clear, actionable title starting with a verb
- [ ] Acceptance criteria are binary (pass/fail testable)
- [ ] No ticket requires a follow-up conversation to understand
- [ ] Dependencies between tickets are explicitly noted
- [ ] Tickets are right-sized (completable in one sprint)

## Verification Steps

1. **Title Scan:** Can you understand each ticket from title alone?
2. **Size Check:** Would any ticket take > 1 week? If so, split it.
3. **Dependency Check:** Are blocked/blocking relationships explicit?
4. **Completeness:** Can you mark each ticket "Done" without ambiguity?

## Batch Commands

```
/ticket-batch from PRD.md → Jira stories
/ticket-batch "meeting notes: discussed auth, payments, and notifications" → Linear tasks
/ticket-batch split EPIC-100 into sprint-sized stories
```

## Smart Behaviors

- **Auto-numbering:** Tickets numbered 1/N for easy reference
- **Dependency detection:** Flags tickets that block others
- **Size warning:** Warns if ticket scope seems > 1 sprint
- **Duplicate detection:** Notes if similar ticket might exist
- **Epic suggestion:** Proposes epic groupings for orphan tickets

## Anti-Patterns

- Tickets without acceptance criteria
- Vague titles ("Fix the thing", "Update stuff")
- Multiple unrelated tasks in one ticket
- Missing context (assuming reader knows the project)
