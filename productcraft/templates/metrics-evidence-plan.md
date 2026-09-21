# Metrics & evidence plan template

Owned by the **Insights & Analytics** seat (seat contract, [#266](https://github.com/seanwinslow28/code-brain/issues/266)). Stage 3, **touch two** — a fresh invocation from the touch-one co-sign, because grading evidence and designing metrics on it are different stances. Receives the Strategy doc and the co-signed Discovery packet in full. **This seat measures and never decides**: it designs the metrics, grades evidence, and sets the rules for reading experiments; the Strategist, Growth and Business seats decide on its measurements, and Sean above them. Its outcome-to-metric table is the train's stage-3 check: **any Strategist outcome it cannot give a metric bounces to the Strategist**, so no third touch on the Strategy doc is needed. Audited fresh-context by the **Delivery & Execution Lead** — stake: *is every metric instrumentable and shippable, not vanity?* Gate 1 fires once this artifact is final.

Header fields per [artifact-header.md](artifact-header.md). Thresholds and go/no-go numbers are not set here — Business sets the economic ones, Delivery the key results.

```markdown
---
id: pc-eng-001.insights
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-22
seat: insights-analytics
stage: 3
model: claude-opus-5
grounding: full
thin_lane: []
adjacent_lanes: []
revision: 1
stale_from: null
status: draft
cosign: n/a
auditor: delivery-execution
audit: pending
---

## Outcome-to-metric table  ⟵ the stage-3 check; a bounce is a loopback to the Strategist

| Outcome id | Metric | Why this metric and not the nearest vanity one | Verdict |
|---|---|---|---|
| O1 | | | pass \| bounce: <what would have to be true to measure it> |

## North-star metric

One. The customer value exchanged, not revenue and not activity. State what it leads and what it lags, and the one way it could go up while customers get worse off.

## Input metrics

The three to five drivers the team can actually move, each with its relationship to the north star stated as a hypothesis, not a fact.

| Metric | Drives north star by | Owner seat | Leading or lagging |
|---|---|---|---|

## Instrumentation requirements

Per metric: the event, its properties, where it fires, the identity it joins on, and what breaks the number (deduplication, bots, timezone, backfill). A metric with no event is a wish. Delivery audits this section for shippability.

| Metric | Event | Properties | Fires when | Identity | Known corruptions |
|---|---|---|---|---|---|

## Evidence-strength rules

How this seat graded the Discovery packet and will grade every later claim: the four-rung scale from [check-record.md](check-record.md) and what each rung may carry. Restated here so the Growth and Business seats grade their own inputs the same way before this seat audits them.

## Experiment-analysis rules

For every experiment the Growth seat will design: minimum detectable effect and how it was chosen; sample and duration arithmetic; the primary metric fixed before launch; guardrail metrics that stop a winner; the peeking rule; who reads the result (never the seat that designed it). These rules are the anchor of this seat's audit of the Growth plan.

## Dashboards and cadence

What is looked at, by whom, how often, and the decision each view feeds. The operating-model doc pulls its metric rituals from here and never re-invents them.

## Moves

<!-- MACHINE-READ. The rung-0 checker (productcraft/trace/check.py) parses this section line by line
     against the pass's recorded inputs. Move lines only, one per line, from the five-op grammar in
     artifact-header.md § Moves — or the single `origin draft, no upstream` line. A sentence of prose
     here is a malformed line and a finding, not a note: put the note in the record's ## Notes. -->

- kept — <upstream item> from pc-eng-001.discovery
- added — <new item> from <source: evidence file, check record, gate finding, brief section>
- split — <upstream item> → <child>, <child> from pc-eng-001.discovery
- merged — <upstream item> + <upstream item> → <item> from pc-eng-001.discovery
- dropped — <upstream item> from pc-eng-001.discovery; <why>

meter: <runtime> · <tokens> · <wall-clock>
```

## Red-team checklist (Gate 1 cross-artifact; close gate)

- **Vanity in the north star** — a number that rises with spend or activity while value is flat.
- **A metric that rewards harm** — an input metric met by dark patterns; the north-star section's "up while worse off" line is empty.
- **Uninstrumentable metrics** — a row with no event, no identity, or a corruption nobody will fix (Delivery's stake).
- **Gameable analysis** — rules that let a designer choose the primary metric after the fact, peek, or stop early.
- **The metric-versus-user gap** — every metric can pass while the point of view stays untested.
- **Unrepresentative evidence rules** — a grading scale the seat did not actually apply in its co-sign record (cross-artifact).
