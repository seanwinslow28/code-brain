---
title: "Automation Reliability"
type: concept
sources:
  - knowledge/connections/the-latency-of-trust-in-automated-research-pipelines.md
tags: [auto-generated, phase-6]
created: 2026-07-02
updated: 2026-07-02
---

## Definition

This concept refers to the gap between binary operational health metrics (such as exit codes and dashboard status) and the actual functional value delivered by automated systems. When agents report 'healthy' despite producing low-yield or malformed outputs, the system creates an illusion of competence that prevents timely intervention. True reliability requires monitoring yield rates and parsing robustness rather than relying solely on success/failure flags.

## Context

Sean's infrastructure monitors agent health via dashboards, but these tools do not capture semantic quality. This leads to a situation where he believes his automation is working correctly while the actual output degrades silently over time.

## Evidence

> The 'two runs failed' were Phase-2, pre-fix. Residual is confidence only (a few live runs incl. deep).

> Sean cannot rely on binary success/fail metrics to gauge fleet health; he must monitor yield rates and parsing robustness as primary indicators of system reliability.

## Examples

- Phase-2 runs failing before fixes were applied
- Residual confidence issues in live runs including deep research

## Related Concepts

[[Silent Failure Propagation in Agent Fleets]] [[Cost-Capped Agentic Workflows]]
