# Ops/economics model + incident runbook template

Owned by the **Ops & Economics Modeler** (seat contract, [#144](https://github.com/seanwinslow28/code-brain/issues/144)). Receives the complete upstream design; produces the artifact that decides whether and how it ships and survives. Boundary call: **launch thresholds are set here**, read against the measurements the eval plan designed. Two parts, one artifact: the **ops/economics model** (numbers and gates) and the **incident runbook** (what happens at 3 AM). Audited by the Architecture Advisor: gates and kill switches feasible against the pipeline as designed.

Filled artifacts are **private** (`ledger/engagements/<eng-id>/artifacts/`); this template is public machinery. Brevity law applies.

```markdown
---
id: eng-001.ops
engagement: eng-001-fleet-knowledge-loop-audit
date: 2026-08-24
seat: ops-economics-modeler
model: sonnet
status: draft                        # draft | audited | final
auditor: architecture-advisor        # fixed by the audit cycle
---

# Part 1 — Ops/economics model

## Unit economics

Cost per unit of value (per request, per resolution, per user-month) at expected, best,
and worst case. A model that only works at best case is an audit defect — show all three.

| Scenario | Volume | Cost/unit | Monthly total |
|---|---|---|---|

## Rollout plan

Stages, entry criteria per stage, and what rolls back if a stage fails. Who flips each stage.

## Launch criteria

Go/no-go thresholds against the eval plan's measurements — the numbers are set here, read from there.

| Measurement (from eval plan) | Threshold | Gate |
|---|---|---|

## Kill switches

| Switch | What it stops | Who can pull it | How fast | Last tested |
|---|---|---|---|---|

An untested switch is theater — "Last tested" is a required column, and "never" is a finding.

## Drift monitoring

What's watched for degradation (input drift, output drift, cost drift), the alert
thresholds, and who gets paged. Name the blind spot drift could hide in.

# Part 2 — Incident runbook

## Severity levels

What counts as SEV-1/2/3 here, in observable terms — no judgment calls at 3 AM.

## Per-incident steps

Per failure class: detect → contain → communicate → recover. Every step runnable by
whoever is actually on call — a step requiring a human who won't be there is a defect.

## Escalation and comms

Who is called, in what order, and what users are told while it's broken (honest, per the
failure-UX spec's disclosure surfaces).

## Post-incident

The review loop: what gets written, where it lands (a ledger entry), and how fixes
feed back into the eval plan's datasets.
```
