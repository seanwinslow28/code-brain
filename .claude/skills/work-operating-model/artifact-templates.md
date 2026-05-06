# Artifact Templates — Work Operating Model

Five artifact files per domain, stored at `vault/05_atlas/operating-models/{domain}/`. This file specifies the exact structure to write into each. Preserve existing frontmatter; update only `status` and `last_interviewed`.

---

## 1. `HEARTBEAT.md` — Operating Rhythms (Layer 1)

```markdown
---
type: operating-model
artifact: HEARTBEAT
domain: [{{domain}}]
status: draft                       # or "confirmed" after final read-through
last_interviewed: {{YYYY-MM-DD}}
created: {{original-created-date, preserve}}
review-date: {{optional}}
ai-context: "Operating rhythms for Sean in the {{domain}} domain. Consumed by daily-driver."
---

# HEARTBEAT — {{Domain Display Name}}

## Daily Rhythm
- Wake / first hour: ...
- Deep-work blocks: ...
- Execution / meeting blocks: ...
- Inbox triage windows: ...
- End-of-day wind-down: ...

## Weekly Cadence
| Day | Calendar | Off-calendar rituals |
|---|---|---|
| Mon | ... | ... |
| Tue | ... | ... |
| Wed | ... | ... |
| Thu | ... | ... |
| Fri | ... | ... |
| Sat | ... | ... |
| Sun | ... | ... |

## Monthly / Quarterly
- ...

## Seasonal Shifts
- ...

## Sacred Blocks
- First hour rule: ...
- Any day-of-week rule: ...

## Email Split (this domain)
- Archived prior-employer email usage: ...
- `sean.winslow28@gmail.com` usage: ...
```

---

## 2. `USER.md` — Recurring Decisions (Layer 2)

```markdown
---
type: operating-model
artifact: USER
domain: [{{domain}}]
status: draft
last_interviewed: {{YYYY-MM-DD}}
created: {{preserve}}
ai-context: "Sean's decision-making patterns in {{domain}}. Consumed by daily-driver, process-inbox, sprint-health."
---

# USER — {{Domain Display Name}}

## Decisions Made 3+ Times Weekly
- ...

## Real Prioritization Criteria
_(In Sean's own words — messy is fine.)_
- ...

## Auto-Yes
- ...

## Auto-No
- ...

## Daily Investment Heuristic
- ...

## Agent Delegation
**Already trusted to agents:**
- ...

**Never delegated:**
- ...

## Tiebreakers When Unsure
- ...

## Definition of "Done" in This Domain
- ...
```

---

## 3. `SOUL.md` — Dependencies + Institutional Knowledge (Layers 3+4)

```markdown
---
type: operating-model
artifact: SOUL
domain: [{{domain}}]
status: draft
last_interviewed: {{YYYY-MM-DD}}
created: {{preserve}}
ai-context: "People, tools, tacit knowledge for {{domain}}. Consumed by sprint-health, pr-digest, process-inbox, and all agents as context layer."
---

# SOUL — {{Domain Display Name}}

## Part A — Dependencies (Layer 3)

### Critical-Path Collaborators
| Person | What I go to them for | Blocker if unavailable |
|---|---|---|
| ... | ... | ... |

### Load-Bearing Tools
- ...

### Load-Bearing External APIs / Models
- ...

### Three-Machine Topology (Creative Studio domain has most here)
- Mac Mini halts if: ...
- MacBook Pro halts if: ...
- Alienware halts if: ...

### Single Source of Truth
- Primary: ...
- Secondary: ...

### Who Depends On Me
| Person / team | Cadence | What they need |
|---|---|---|

### Self-Blocking Decisions
_(Decisions only Sean can make that pile up.)_
- ...

---

## Part B — Institutional Knowledge (Layer 4)

### Internal Vocabulary
| Term | Meaning |
|---|---|

### Sacred Cows
- ...

### Unwritten Communication Rules
- ...

### Ask X About Y
| Person | Topic |
|---|---|

### Past Landmines
- ...

### Week-One Tacit Knowledge
_(What a sharp new hire would need day-one but nobody writes down.)_
- ...

### Things Collaborators Have Learned About Sean
- ...
```

---

## 4. `operating-model.md` — Structured Profile (synthesis)

```markdown
---
type: operating-model
artifact: operating-model
domain: [{{domain}}]
status: draft
last_interviewed: {{YYYY-MM-DD}}
created: {{preserve}}
ai-context: "Synthesized operating model for {{domain}}. Cross-references HEARTBEAT, USER, SOUL, schedule-recommendations. This is the one-file summary agents should load when starting work in this domain."
---

# Operating Model — {{Domain Display Name}}

## TL;DR
_(2-3 sentences. What would a new collaborator need to know about how Sean works here?)_

## Identity in This Domain
_(Sean's role, stakes, stated goals.)_

## Operating Rhythm Summary
_(1-paragraph compression of HEARTBEAT.md.)_

## Decision Pattern Summary
_(1-paragraph compression of USER.md.)_

## Dependency Map Summary
_(1-paragraph compression of SOUL.md Part A.)_

## Institutional Context Summary
_(1-paragraph compression of SOUL.md Part B.)_

## Active Leverage Points
_(Where small effort produces disproportionate output.)_

## Known Bottlenecks
_(What limits Sean's throughput in this domain — from Layer 5 + SOUL.)_

## Cross-Domain Bleed
_(What in this domain spills into other domains, and vice versa.)_

## Current Open Questions
_(Things Sean himself noted during the interview as "I should figure this out.")_

## Related Artifacts
- HEARTBEAT: [[HEARTBEAT]]
- USER: [[USER]]
- SOUL: [[SOUL]]
- Schedule rules: [[schedule-recommendations]]
- Tier-0 identity: [[Sean-Winslow-Full-Personal-Context-v2.0|Full Personal Context]]
```

---

## 5. `schedule-recommendations.md` — Friction-Derived Rules (Layer 5)

```markdown
---
type: operating-model
artifact: schedule-recommendations
domain: [{{domain}}]
status: draft
last_interviewed: {{YYYY-MM-DD}}
created: {{preserve}}
ai-context: "Actionable schedule and friction-reduction rules for {{domain}}. Consumed by daily-driver, meta-agent, and future calendar agents."
---

# Schedule Recommendations — {{Domain Display Name}}

## Protect
_(When X, then Y. These are calendar-level defenses.)_
- When `{{context}}`, then `{{action}}`
- ...

## Automate
_(Manual work that should become agent-triggered.)_
- ...

## Decline or Defer
_(Patterns of meetings/asks that Sean said he'd rather say no to or push.)_
- ...

## 20-Minutes-to-2-Minutes Candidates
_(High-leverage automation targets from Layer 5 Q1.)_
- ...

## Context-Switch Costs to Minimize
- ...

## Claude Code / Agent-Fleet Friction Points
_(From Layer 5 Q7. These are hooks/agents to fix or build.)_
- ...

## The Extra Hour
_(If Sean had +1 hour/day in this domain, where does he say it goes? This is the north star for the schedule recommendations.)_
- ...
```

---

## Status Lifecycle

`status: awaiting-interview` — fresh placeholder, no content yet.
`status: draft` — interview complete, content written, Sean has not done final read-through.
`status: confirmed` — Sean has read the final artifact end-to-end and confirmed it matches how he actually works.

Update status when all five artifacts for a domain are final; do not mark individual files `confirmed` until the whole bundle has been read together. A contradiction between `HEARTBEAT` and `SOUL` is a common interview artifact that only surfaces on full read-through.

## Cross-File Consistency Checks (run before marking confirmed)

1. Every person named in `HEARTBEAT` (e.g., "Tuesday 1:1 with X") should also appear in `SOUL` Part A
2. Every tool in `SOUL` Part A "Load-Bearing Tools" should be referenced somewhere in `USER` or `HEARTBEAT`
3. Every friction point in `schedule-recommendations` "Automate" section should be traceable back to a Layer 5 interview answer — do not invent recommendations
4. `operating-model.md` summaries should not contradict the source files they compress
