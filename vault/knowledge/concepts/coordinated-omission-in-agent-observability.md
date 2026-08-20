---
title: "Coordinated Omission in Agent Observability"
type: concept
sources:
  - knowledge/connections/the-tension-between-operational-uptime-and-semantic-value-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

This mechanism occurs when monitoring systems fail to record events that did not happen, specifically the absence of expected outputs or actions. It creates a gap where the lack of activity is invisible because the system only logs successful completions rather than tracking the presence or absence of work items. This leads to a distorted view of system health where silence is interpreted as stability rather than potential failure.

## Context

The fleet’s monitoring dashboard needs to distinguish between 'no work done' and 'work completed successfully' to prevent false confidence. Sean should implement semantic health checks that flag empty or low-quality outputs as critical failures, not just operational successes.

## Evidence

> Job Feed report noted 'scored=0 mbp=False,' suggesting the pipeline may not be actively finding or scoring opportunities.

> The fleet's binary health reporting creates a dangerous blind spot where semantic decay is invisible to the operator.

## Examples

- Pipeline not actively finding or scoring opportunities
- Semantic decay being invisible to the operator

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Silent Failure Propagation in Agent Fleets]]
