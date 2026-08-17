---
title: "Silent Failure Propagation in Agent Fleets"
type: concept
sources:
  - knowledge/expansions/connections/agent-health-and-automation-failure.md
tags: [auto-generated, phase-6]
created: 2026-08-17
updated: 2026-08-17
---

## Definition

This pattern describes how a minor, undetected failure in one agent (such as a missing credential or empty output) propagates through the fleet by corrupting the context passed to downstream agents. Because each agent assumes its input is valid, it produces garbage that appears structurally correct but semantically void, making the failure invisible until the final user-facing artifact is reviewed. This creates a cascading effect where the root cause is buried deep in the dependency chain, requiring manual reconstruction to identify.

## Context

Sean’s fleet relies on a chain of agents (synthesizer, daily drive, etc.) where each depends on the previous day's note. A silent failure in the synthesizer means the daily drive agent has nothing to work with, leading to empty or stale outputs that Sean only notices when he checks his morning brief.

## Evidence

> Complex systems normally operate in degraded states, catastrophes require multiple contributing conditions, and 'root cause' stories are usually hindsight compression.

> Every automated recovery path must preserve diagnosis evidence and periodically exercise the operator’s manual recovery path.

## Examples

- The transition from log-only monitoring to black-box SLOs is necessary because logs can show success while the artifact is missing.
- A portfolio-grade incident reconstruction showing how individually reasonable components combine to miss a note.

## Related Concepts

[[Agent Health and Automation Failure]] [[Control Room Observability]]
