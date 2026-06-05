---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/concepts/resilience-engineering-work-as-imagined-vs-work-as-done.md
tags: [auto-generated, phase-6]
created: 2026-06-05
updated: 2026-06-05
---

## Definition

System reliability is determined by detecting the divergence between intended design and actual operational workflow, rather than merely preventing failures in static plans. This gap emerges because the data plane—the living vault—evolves dynamically while the control plane—the scheduler—relies on static assumptions that quickly become obsolete. Agent operations must therefore shift from maintaining green status indicators to actively monitoring for silent drift where automated outputs no longer align with current user intent.

## Context

Sean's job hunt and creative studio workflows depend on agents maintaining consistency across shifting priorities. If agents continue executing outdated templates or ignoring new constraints, downstream artifacts like resumes or creative pieces become misaligned with his actual goals. Monitoring this divergence allows Sean to intervene before the gap widens into systemic noise that degrades the quality of his professional output.

## Evidence

> This framework posits that system reliability is not just about preventing failures in designed workflows, but about detecting when the actual operational workflow diverges from the intended design.

> agent ops is not just keeping agents green; it is detecting when the designed workflow and the real workflow diverge.

## Examples

- An agent continues to generate daily notes based on a template that the user has stopped using, creating a silent divergence between the agent's output and the user's actual practice.

## Related Concepts

[[Control Plane / Data Plane Split for Agent Fleets]] [[Infrastructure Status and Agent Failure]]
