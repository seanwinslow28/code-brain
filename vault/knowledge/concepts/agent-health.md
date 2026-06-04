---
title: "Agent Health"
type: concept
sources:
  - knowledge/concepts/agent-health.md
tags: [auto-generated, phase-6]
created: 2026-06-04
updated: 2026-06-04
---

## Definition

Agent health is a metric of operational continuity defined by the successful execution of scheduled tasks and the absence of silent failures in the background processing layer. It requires agents to not only run but to produce verifiable outputs (like daily notes or index updates) that feed into the broader knowledge loop. When an agent's status is 'healthy' but its output is empty or stale, it indicates a latent failure in the context management layer rather than a true state of readiness. This distinction separates process completion from data integrity, revealing that a running process does not guarantee a useful result.

## Context

Sean relies on the daily-driver and synthesizer agents to maintain the integrity of his daily notes and knowledge base. The health of these agents determines whether his morning planning is based on fresh data or stale context, directly affecting his daily decision-making efficiency. If the health metric only tracks process uptime, Sean risks making decisions based on outdated information without realizing the data pipeline has broken.

## Evidence

> Agent health is a metric of operational continuity defined by the successful execution of scheduled tasks and the absence of silent failures in the background processing layer.

> When an agent's status is 'healthy' but its output is empty or stale, it indicates a latent failure in the context management layer rather than a true state of readiness.

## Examples

- The Daily Driver executed morning planning and generated today's note, maintaining process hygiene.

## Related Concepts

[[Agent Health Monitoring]] [[Context Management as a Bottleneck]]
