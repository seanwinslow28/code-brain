---
title: "Context Compounding"
type: concept
sources:
  - knowledge/concepts/context-compounding.md
tags: [auto-generated, phase-6]
created: 2026-07-05
updated: 2026-07-05
---

## Definition

Automated systems accumulate and propagate errors or omissions across sequential runs, where the output of one agent becomes the flawed input for the next. This compounding effect occurs because each agent operates with limited visibility into the systemic failures of its predecessors, treating incomplete data as valid context. The result is a gradual degradation of information quality that remains invisible until the final output diverges significantly from reality.

## Context

Sean’s daily note generation depends on prior synthesis and indexing runs. If the vault-synthesizer or deep-researcher fails silently or produces empty results, the morning brief inherits this degraded context, potentially leading to planning decisions based on incomplete information about his job hunt or creative studio status.

## Evidence

> Automated systems accumulate and propagate errors or omissions across sequential runs, where the output of one agent becomes the flawed input for the next.

> The result is a gradual degradation of information quality that remains invisible until the final output diverges significantly from reality.

## Examples

- The meta-agent generates a fleet status report based on data from agents that may be operating with stale or incomplete context due to infrastructure outages.
- The daily-driver morning agent creates a planning note based on the previous day's synthesis, which might have missed critical updates if the deep-researcher queue was blocked.

## Related Concepts

[[Automation Failure and Daily Note Disruption]] [[Context Management as a Bottleneck]]
