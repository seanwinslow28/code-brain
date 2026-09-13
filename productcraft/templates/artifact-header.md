# Artifact header — the shared frontmatter and the shared sections

Every seat-owned artifact in this folder opens with the same machine-readable header and closes with the same two sections. Defined once here; each template shows it filled for its seat and adds only its own fields. Ratified on the build map's [Artifact templates per seat](https://github.com/seanwinslow28/code-brain/issues/274) ticket (2026-09-13), on the contracts of [#266](https://github.com/seanwinslow28/code-brain/issues/266), the ladder of [#267](https://github.com/seanwinslow28/code-brain/issues/267), and the trace record of [#272](https://github.com/seanwinslow28/code-brain/issues/272).

Filled artifacts are **private** (`ledger/engagements/<eng-id>/artifacts/`); templates are public machinery. Brevity law applies: every section reads in a breath. Book-derived text never lands in a filled artifact's tracked copy because there is no tracked copy.

```markdown
---
id: pc-eng-001.strategy            # <engagement>.<artifact-slug> — permanent; the frozen-copy and handoff ids
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-20
seat: product-strategist           # the one seat that may write this file
stage: 1                           # fixed train numbering 1–7; 0 for a one-off, an audit lane, or the breakdown
model: claude-opus-5               # the runtime that actually ran, plus any deviation: "claude-opus-5 → codex gpt-5.6-sol high: gate FAIL"
grounding: full                    # full | manifest-only | none — see the ledger template's ladder
thin_lane: []                      # topics with no manifest pointer, found mid-pass; finish at baseline, flag here
adjacent_lanes: []                 # lanes noticed and not drafted — named, never written
revision: 1                        # bumps on every redraft; a redraft overwrites in place, the pass records keep the history
stale_from: null                   # the pass id of the loopback that staled the previous revision, else null
status: draft                      # draft | co-signed | final | audited | stale — written by the coordinator, not the seat
cosign: n/a                        # n/a | pending | co-signed <date> → pc-eng-001.cosign-<slug>
auditor: discovery-lead            # fixed by the audit cycle; never chosen per engagement
audit: pending                     # pending | landed <date> → pc-eng-001.audit-<slug>
---
```

## Who writes which field

The **seat** writes everything above `revision:` plus its own sections. The **coordinator** writes `revision:`, `stale_from:`, `status:`, `cosign:` and `audit:` as the train moves — the seat never declares its own artifact final, co-signed or audited. A seat that finds itself editing another seat's file has broken rule 7 of `productcraft/CLAUDE.md`.

## Status lifecycle

`draft` — the seat has returned it · `co-signed` — every required co-sign touch landed with no open bounce (only artifacts with a co-sign pass through this state) · `final` — the coordinator has marked it done; the trailing audit fires now · `audited` — the audit landed with no open material defect · `stale` — a loopback above it changed an upstream artifact; the redraft bumps `revision:`, sets `stale_from:`, and re-enters at `draft`.

## Artifact ids, auditors, co-signs

| Stage | Artifact id | Template | Auditor (fixed) | Co-sign |
|---|---|---|---|---|
| 1 | `<eng>.strategy` | [strategy-pov.md](strategy-pov.md) | discovery-lead | none at draft; stage 3 bounces outcomes without a metric |
| 2 | `<eng>.discovery` | [discovery-packet.md](discovery-packet.md) | product-leadership | insights-analytics, touch one → `<eng>.cosign-discovery` |
| 3 | `<eng>.insights` | [metrics-evidence-plan.md](metrics-evidence-plan.md) | delivery-execution | its own outcome-to-metric table is the stage-3 check |
| 4 | `<eng>.growth` | [growth-gtm.md](growth-gtm.md) | insights-analytics | none — the experiment section is the audit's anchor |
| 5 | `<eng>.business` | [business-case.md](business-case.md) | growth-distribution | none |
| 6 | `<eng>.roadmap` | [outcome-roadmap.md](outcome-roadmap.md) | business-economics | product-strategist on the OKR translation → `<eng>.cosign-okr` |
| 6 | `<eng>.handoff` | [handoff-brief.md](handoff-brief.md) | Gate 2 (Codex), not a seat | none |
| 7 | `<eng>.leadership` + `<eng>.memo-NN` | [leadership-packet.md](leadership-packet.md), [decision-memo.md](decision-memo.md) | product-strategist (anchor: the memos) | none |
| 0 | `<eng>.breakdown` | [execution-breakdown.md](execution-breakdown.md) | none — no audit cycle | none |
| — | `<eng>.cosign-<slug>`, `<eng>.audit-<slug>` | [check-record.md](check-record.md) | — | — |
| — | `<eng>.gate-1`, `<eng>.gate-2`, `<eng>.gate-close` | [gate-findings.md](gate-findings.md) | — | — |

Seat slugs, as used in `seat:` and `auditor:`: `product-strategist`, `discovery-lead`, `insights-analytics`, `growth-distribution`, `business-economics`, `delivery-execution`, `product-leadership`, plus `coordinator` and `red-team-gate`.

## The two closing sections, on every artifact

**`## Moves`** — what this pass did to the upstream material, one line each, from the fixed vocabulary **kept / added / split / merged / dropped**, each line naming the upstream item and its source artifact; a split names every source. The Strategist's origin draft writes "origin draft, no upstream" and lists what it leaned on. Moves are claims until a replay confirms them (#272). The lines are machine-read by the trace kit's rung-0 checker ([productcraft/trace/](../trace/README.md), #290), so they follow one grammar — an em dash after the op, ` from ` before the source:

```markdown
- kept — O1 from pc-eng-001.strategy
- added — E1–E5 from evidence/interviews-01-08.md
- split — OC-1 → OC-1a, OC-1b from pc-eng-001.strategy
- merged — C2 + C3 → C2 from pc-eng-001.strategy
- dropped — Action 4 from pc-eng-001.strategy; no source survived the split
origin draft, no upstream — leaned on: Rumelt's kernel; the brief §2
```

Items are the ids the artifacts already use (`O2`, `OC-1a`, `KR-2`; ranges `E1–E5` expand) or a short quoted phrase; the checker looks for each in the pass's inputs, and for a split's children in the artifact itself.

**Meter line** — the last line of the file: `meter: <runtime> · <tokens as reported> · <wall-clock>` or `meter: UNMEASURED`. Never an estimate.

## The red-team checklist, on every template

Each template ends with a **Red-team checklist**: the attacks the gate runs on that artifact, each naming the section where it lands. The protocol is inherited from [systemcraft/templates/red-team-protocol.md](../../systemcraft/templates/red-team-protocol.md); Productcraft's schedule is the master skill's (Gate 1 on the Strategy doc after stage 3, Gate 2 on the brief, the close gate on the whole train). The whole-train attacks live in [gate-findings.md](gate-findings.md). An attack with no named home in a template is a defect in this folder, not in the gate.
