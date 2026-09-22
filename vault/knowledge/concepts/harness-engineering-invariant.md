---
title: "Harness Engineering Invariant"
type: concept
sources:
  - 20_projects/research/2026-09-21-harnesses-per-runtime.md
tags: [auto-generated, phase-6]
created: 2026-09-22
updated: 2026-09-22
---

## Definition

A structural constraint where the viability of an agentic workflow is determined not by the model's capability, but by the harness's ability to expose a verifiable meter_source and raw_log that satisfy external auditing requirements. This invariant forces a divergence between 'rich' interfaces (which may lack machine-readable usage data) and 'thin' interfaces (which provide precise telemetry but require configuration wrappers). The system must treat metering fidelity as a first-class dependency, meaning any new runtime adds a fixed wiring cost to the observability layer.

## Context

Sean is building a Productcraft seat-pass system that requires end-to-end token accounting. If the harness cannot report `input` + `output` splits or a `total` via a recognized `meter_source`, the entire trace-kit infrastructure fails to meter the work, rendering the agent's output unbillable and unobservable.

## Evidence

> Every new harness therefore adds one meter_source vocabulary entry to check.py — that is a fixed wiring cost shared by every row below.

> The best-shaped meter is Hermes's --usage-file (split pair, cache, reasoning, cost, an auxiliary block, written even on failure).

## Examples

- Codex CLI provides `--json` output which includes split token counts, making it a credible universal harness despite config complexity.
- Hermes writes usage data to a file even on failure, ensuring the meter is never lost if the agent crashes mid-run.

## Related Concepts

[[Operational Uptime vs. Semantic Value in Agent Fleets]] [[Instrumentation vs. Traces]]
