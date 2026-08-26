---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/connections/operational-metrics-mask-semantic-decay-in-agentic-fleets.md
tags: [auto-generated, phase-6]
created: 2026-08-25
updated: 2026-08-25
---

## Definition

This concept applies Site Reliability Engineering principles to agentic workflows by defining a threshold of acceptable semantic error before halting expansion. It posits that if the rate of low-quality or irrelevant output exceeds a defined budget, the system must pause new deployments and fund reliability work instead. This prevents the accumulation of legibility debt by forcing a trade-off between velocity and integrity.

## Context

Sean needs a concrete metric to decide when to stop adding agents or increasing their frequency. The error budget provides a data-driven trigger for intervention, shifting the focus from 'how much can we automate' to 'how much quality are we willing to lose'.

## Evidence

> If the monthly error budget exceeds Z, pause fleet expansion and fund reliability work.

> Health checks must be decoupled from output validity to prevent masking semantic decay.

## Examples

- The rejection rate for cross-domain connections has exceeded 20% for three consecutive weeks, triggering a halt in new agent onboarding.
- The system pauses daily note generation when the semantic similarity score drops below a defined threshold.

## Related Concepts

[[Operational Visibility vs. Semantic Value in Agent Fleets]] [[The Illusion of Health in Autonomous Systems]]
