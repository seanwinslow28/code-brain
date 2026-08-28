# Eval plan template

Owned by the **Evals & Evidence Architect** (seat contract, [#144](https://github.com/seanwinslow28/code-brain/issues/144)) — the seat's second touch: it already co-signed the PRD's Evaluable success criteria at framing time; this artifact, written with the full design in hand, makes those criteria runnable. Boundary call: **this seat designs the measurements launch gates read; the go/no-go thresholds belong to Ops** — the seat that designs the test doesn't set the passing grade. Audited by Interaction & Trust: the metric-vs-user gap (the "assumed resolution" failure class).

Filled artifacts are **private** (`ledger/engagements/<eng-id>/artifacts/`); this template is public machinery. Brevity law applies.

```markdown
---
id: eng-001.eval
engagement: eng-001-fleet-knowledge-loop-audit
date: 2026-08-24
seat: evals-evidence-architect
model: opus
status: draft                        # draft | audited | final
auditor: interaction-trust-designer  # fixed by the audit cycle
---

## Criteria under test

The PRD's evaluable success criteria, by number. This plan exists to make each one runnable.

## Golden datasets

| Dataset | Source | Size | Covers | Refresh |
|---|---|---|---|---|

Provenance is the audit surface: real traces beat authored fiction; state what each set
under-represents. Include negative and abuse cases — a golden set of only happy paths is theater.

## Metrics

Per criterion: the metric, what it computes over, and the failure it can miss.
Every metric names its blind spot.

## LLM-judge design

For each judged metric: the judge model, the rubric, and how the judge itself was validated
against human labels (agreement rate). A judge nobody has checked is an unmeasured metric.
Name the gameability risk: how could a system score well while being wrong?

## Holdout hygiene

What is held out, from whom, and how leakage is prevented — including "the builder saw the
test set" and "the judge saw the training rubric." State the rule, not just the intent.

## Measurements for launch gates

The numbers Ops' launch criteria will read — measurement, dataset, cadence, where results land.
**No thresholds here**; Ops sets go/no-go in the ops model.

| Measurement | Dataset | Cadence | Reported where |
|---|---|---|---|

## Post-launch cadence

What keeps running after launch, how often, and what triggers an error-analysis pass
(open coding over real traces, not metric-watching alone).
```
