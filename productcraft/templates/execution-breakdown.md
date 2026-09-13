# Execution breakdown template

Owned by the **Delivery & Execution Lead** (seat contract, [#266](https://github.com/seanwinslow28/code-brain/issues/266)). The artifact of the **execution-breakdown engagement**: Delivery only, opened when Systemcraft's return has landed in `handoff/inbound/`, receiving the complete design train plus the frozen return. Delivery runs the **intake check** first (per [the handoff contract](handoff-contract.md)), writes `informed_by` and flips overturned entries, then turns the design into buildable work: **epics → stories with subtasks in a design set and an implementation set → a first sprint plan**, filed as issues in the target's tracker. One ledger entry; **no audit cycle, no gate** — this engagement creates the implementation candidate that Systemcraft's Gate 3 waits for. A one-off Delivery pass mid-build (stories, release notes, retros) uses the story and sprint sections of this template alone.

Design-set stories are a **flagged placeholder** until a Designcraft team exists. An overturn that demands a new *product* decision is a loopback to the owning seat as a one-off, never answered here. Header fields per [artifact-header.md](artifact-header.md).

```markdown
---
id: pc-eng-002.breakdown
engagement: pc-eng-002-16bitfit-execution-breakdown
date: 2026-10-06
seat: delivery-execution
stage: 0
model: claude-sonnet-5
grounding: full
thin_lane: []
adjacent_lanes: []
revision: 1
stale_from: null
status: draft
cosign: n/a
auditor: none                      # no audit cycle on a breakdown
audit: n/a
design_train: pc-eng-001-16bitfit-revisit
return_note: eng-004.return        # Systemcraft's return note id
crossing_state: accepted           # written after the intake check: accepted | input-required | rejected
informed_by: [eng-004.d12, eng-004.d15]
tracker: seanwinslow28/16bitfit    # where the issues are filed
---

## Intake check

Can this seat do its job from the return? State the crossing state and, if `input-required`, exactly what is missing by ask id. A check, not an audit — it never judges Systemcraft's decision.

## Overturned assumptions

| Systemcraft entry | Productcraft entry it overturns | What changes here | Needs a product decision? (→ one-off to which seat) |
|---|---|---|---|

## Epics

| Epic | Outcome served (id) | Key result (id) | In first slice? | Systemcraft hold it closes |
|---|---|---|---|---|

## Stories

Every story names its epic, its acceptance in observable terms, its set, and its tracker issue once filed.

**Design set** — *placeholder until Designcraft exists; flagged, not delegated.*

| Id | Epic | Story | Acceptance | Size | Depends on | Issue |
|---|---|---|---|---|---|---|

**Implementation set**

| Id | Epic | Story | Acceptance | Size | Depends on | Issue |
|---|---|---|---|---|---|---|

Subtasks live in the tracker under their story, never here.

## First sprint plan

Goal in one line, the key result it moves, capacity, the stories in, the stories consciously out, and the risk that would end the sprint early.

| In | Out (and why) | Risk |
|---|---|---|

## Filed

| Issue | Story id | Filed at |
|---|---|---|

## Implementation candidate

Which stories, once shipped, constitute the candidate Systemcraft's Gate 3 will fire on, and who writes its `candidate-note.md` per the contract.

## Moves

- kept — <upstream item> from pc-eng-001.roadmap
- added — <story> from eng-004.return ask Q2
- …

meter: <runtime> · <tokens> · <wall-clock>
```

## Red-team checklist (no gate fires here; the close gate of the *next* full train and Systemcraft's Gate 3 look back at it)

- **A story with no outcome** — an epic serving no key result; scope that walked in during the wait.
- **Product decisions taken in the breakdown** — an overturned assumption resolved here instead of looped back.
- **Holds that never close** — a Systemcraft implementation hold no epic names.
- **Acceptance by feeling** — an acceptance cell that cannot be observed.
- **Design work delegated** — a design-set story assigned as if a Designcraft seat existed.
- **A candidate nobody defined** — the implementation-candidate section empty.
