---
id: pc-eng-000.insights
engagement: pc-eng-000-callboard
date: 2026-10-06
seat: insights-analytics
stage: 3
model: claude-opus-5
grounding: full
thin_lane: []
adjacent_lanes: []
revision: 1
stale_from: null
status: final
auditor: delivery-execution
audit: pending
---

# Metrics & evidence plan — Callboard

## Outcome-to-metric table

| Outcome | Metric | Instrumentation |
|---|---|---|
| OC-1a — time to cast | M1 median days audition → cast list | event: cast_list_exported |
| OC-1b — callback no-shows | M2 no-show share per callback | event: callback_attended |
| OC-2 — directors return | M3 second-production rate at 12 months | account: productions |
| OC-2 — directors return | M4 slot acceptance rate | event: slot_accepted |

OC-3 is bounced to the Strategist as unmeasurable by this plan (corpus/insights/trustworthy-online-experiments.md read: no metric without an instrument).

## Moves

- split — OC-1 → OC-1a, OC-1b from pc-eng-000.strategy
- kept — OC-2 from pc-eng-000.strategy
- added — M1–M4 from OC-1a, OC-1b, OC-2
- dropped — OC-3 from pc-eng-000.strategy; unmeasurable, bounced to the Strategist

meter: claude-opus-5 · 176500 in · 19800 out · 29 min
