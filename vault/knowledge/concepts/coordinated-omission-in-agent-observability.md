---
title: "Coordinated Omission in Agent Observability"
type: concept
sources:
  - knowledge/concepts/coordinated-omission-in-agent-observability.md
tags: [auto-generated, phase-6]
created: 2026-08-28
updated: 2026-08-28
---

## Definition

This mechanism occurs when monitoring systems fail to record events that did not happen, specifically the absence of expected outputs or actions. It creates a gap where the lack of activity is invisible because the system only logs successful completions rather than tracking the presence or absence of work items. This leads to a distorted view of system health where silence is interpreted as stability rather than potential failure. The core invariant is that operational uptime metrics are blind to semantic decay, allowing the pipeline to appear healthy while failing to produce value.

## Context

Sean's fleet monitoring dashboard currently relies on binary health reporting which creates a dangerous blind spot for semantic decay. He needs to implement semantic health checks that flag empty or low-quality outputs as critical failures, not just operational successes. Without this distinction, the pipeline may be inactive without Sean realizing it until downstream consequences manifest.

## Evidence

> The fleet's binary health reporting creates a dangerous blind spot where semantic decay is invisible to the operator.

> Job Feed report noted 'scored=0 mbp=False,' suggesting the pipeline may not be actively finding or scoring opportunities.

## Examples

- Pipeline not actively finding or scoring opportunities
- Semantic decay being invisible to the operator

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Silent Failure Propagation in Agent Fleets]]
