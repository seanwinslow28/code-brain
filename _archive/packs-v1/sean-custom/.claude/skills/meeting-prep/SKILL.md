---
name: meeting-prep
description: Generates meeting agendas, pre-reads, and post-meeting action items. Optimized for async-first teams.
---

# Meeting Prep Skill

## Purpose

Make meetings worth having. Generate agendas that respect everyone's time, and action items that actually get done.

## Clarifying Interview

```
Meeting Prep Setup:

1. **Meeting type:** Standup | Sprint planning | Retro | 1:1 | Stakeholder | Kickoff | Decision
2. **Duration:** [X] minutes
3. **Attendees:** [List or "team"]
4. **Goal:** What decision/outcome do we need?
5. **Pre-work needed?** Y/N
6. **Recurring?** Y/N
```

## Output Formats

### Pre-Meeting: Agenda

```markdown
# [Meeting Name] - [Date]

**Duration:** [X] min | **Owner:** [Name] | **Location:** [Link]

## Goal
[One sentence - what must be true when this meeting ends?]

## Pre-Read (5 min)
- [ ] [Document/context to review before meeting]

## Agenda
| Time | Topic | Owner | Type |
|------|-------|-------|------|
| 0:00 | Check-in | All | 2 min |
| 0:02 | [Topic 1] | [Name] | [Discuss/Decide/Inform] |
| 0:15 | [Topic 2] | [Name] | [Discuss/Decide/Inform] |
| 0:25 | Action items & next steps | [Name] | 5 min |

## Decisions Needed
- [ ] Decision 1: [options]
- [ ] Decision 2: [options]

## Parking Lot
[Items to defer if time runs short]
```

### Post-Meeting: Action Items

```markdown
# [Meeting Name] - Action Items - [Date]

## Decisions Made
- ✅ [Decision 1]: [outcome]
- ✅ [Decision 2]: [outcome]

## Action Items
| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | [Specific task] | @[name] | [date] | ⬜ |
| 2 | [Specific task] | @[name] | [date] | ⬜ |

## Parking Lot (for next time)
- [Deferred topic 1]
- [Deferred topic 2]

## Next Meeting
[Date] - [Tentative agenda items]
```

## Meeting Type Templates

### Sprint Planning
```markdown
## Agenda
| Time | Topic | Owner |
|------|-------|-------|
| 0:00 | Sprint goal review | PM |
| 0:05 | Capacity check | Team |
| 0:10 | Backlog grooming | PM + Lead |
| 0:25 | Story pointing | Team |
| 0:45 | Commitment | Team |
| 0:55 | Risks & dependencies | Lead |

## Prep
- [ ] Backlog prioritized
- [ ] Stories have acceptance criteria
- [ ] Team capacity calculated
```

### Retrospective
```markdown
## Agenda
| Time | Topic | Format |
|------|-------|--------|
| 0:00 | Set the stage | Check-in question |
| 0:05 | What went well | Sticky notes (3 min) |
| 0:15 | What could improve | Sticky notes (3 min) |
| 0:25 | Vote & discuss | Dot voting |
| 0:40 | Action items | Commitment |

## Format
- Keep: [practices to continue]
- Stop: [practices to end]
- Start: [new practices to try]
```

### 1:1 Template
```markdown
## Agenda
| Topic | Notes |
|-------|-------|
| Wins this week | |
| Blockers | |
| Feedback (both ways) | |
| Career/Growth | |
| Anything else? | |

## Standing Questions
- What's your biggest blocker right now?
- What should I know that I might not?
- How can I help you this week?
```

## Success Criteria

- [ ] Meeting goal is achievable in allotted time
- [ ] Every agenda item has an owner
- [ ] Decision items are framed as decisions (not open discussions)
- [ ] Action items have owners AND due dates
- [ ] Pre-read takes < 5 minutes

## Verification Steps

1. **Necessity Test:** Could this be an email/Slack instead?
2. **Goal Test:** Can you state the meeting outcome in one sentence?
3. **Time Test:** Does agenda math add up to meeting length?
4. **Action Test:** Are action items specific enough to close as "done"?

## Anti-Patterns

- Agendas with no time allocations
- "Discuss X" without a decision frame
- Action items without owners
- Meetings that could be async
- Back-to-back meetings with no prep time

## Copy/Paste Ready

```
/meeting-prep sprint planning 60min
/meeting-prep 1:1 with [manager name]
/meeting-prep stakeholder review for Auth project
/meeting-prep retro for sprint 23
```
