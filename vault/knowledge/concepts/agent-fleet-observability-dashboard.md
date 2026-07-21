---
title: "Agent Fleet Observability Dashboard"
type: concept
sources:
  - knowledge/concepts/agent-fleet-observability-dashboard.md
tags: [auto-generated, phase-6]
created: 2026-07-21
updated: 2026-07-21
---

## Definition

An observability dashboard is a monitoring interface that aggregates system metrics to provide visibility into agent performance and health. The mechanism involves collecting data points such as concept counts, connection rates, and rejection ratios to create a holistic view of the fleet's activity. Effective dashboards must prioritize signals of semantic integrity and user trust over mere throughput to prevent the illusion of health.

## Context

Sean needs a dashboard that highlights missing data or silence as critical errors, rather than just successful completions. This would help him identify when the fleet is generating volume without value, allowing for timely intervention.

## Evidence

> Automated dashboards should be designed to highlight missing data or silence as critical errors, not just successful completions.

> The fundamental tension lies between the drive for automated throughput and the preservation of epistemic hygiene, leading to a systemic trust deficit.

## Examples

- A dashboard showing a high 'concepts_written' count but low 'connections_written' would indicate a legibility debt issue.
- Tracking the ratio of 'clusters_sampled' to 'concepts_written' could reveal inefficiencies in the sampling process.

## Related Concepts

[[Legibility Debt as a Supervision Failure Mode]] [[The Illusion of Health in Autonomous Systems]]
