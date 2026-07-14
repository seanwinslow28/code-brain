---
title: "Agent Fleet Observability Dashboard"
type: concept
sources:
  - knowledge/connections/velocity-vs-legibility-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-14
updated: 2026-07-14
---

## Definition

This concept defines the necessary architectural shift from monitoring operational metrics (uptime, latency) to monitoring semantic integrity and verification gaps. A true observability layer for agentic work must treat silence, missing data, or unverified outputs as critical errors rather than successes. It requires a feedback loop where the system explicitly flags when human judgment is required, rather than assuming that completion equals correctness.

## Context

Sean's current metrics show 'concepts_written' and 'duration', but lack a clear signal for 'semantic verification needed'. The dashboard needs to highlight when the ratio of rejected concepts or unverified clusters exceeds a threshold, forcing a pause in automation.

## Evidence

> Automated dashboards should be designed to highlight missing data or silence as critical errors, not just successful completions.

> The tension between operational visibility and semantic value reveals a critical flaw: agents can report 'healthy' status while the knowledge pipeline is effectively stalled.

## Examples

- The current manifest shows 'concepts_written' counts but does not indicate whether those concepts were verified by Sean, leaving the 'health' metric ambiguous.

## Related Concepts

[[Legibility Debt as a Supervision Failure Mode]] [[Agent Health Monitoring]]
