---
title: "Agent Fleet Observability Dashboard"
type: concept
sources:
  - knowledge/concepts/agent-fleet-observability-dashboard.md
tags: [auto-generated, phase-6]
created: 2026-07-04
updated: 2026-07-04
---

## Definition

A monitoring interface that provides visibility into the health, performance, and output quality of an autonomous agent fleet. It serves as a critical feedback loop for detecting systemic issues like trust deficits or rule failures that are not apparent from individual agent logs. By aggregating critiques and metrics from multiple external reasoners, it enables higher-level diagnosis of fleet-wide behavior patterns.

## Context

Sean needs a way to objectively assess whether his fleet is improving or degrading over time. The dashboard provides the necessary data points to identify when manual intervention or rule changes are required.

## Evidence

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of agent-fleets-supporting-knowledge-synthesis.

> There is a fundamental tension between the fleet's drive for high-throughput sampling and the preservation of insight quality, leading to a systemic trust deficit.

## Examples

- Sean must implement a 'Synthesis Policy Change Record' to track when the fleet's rules need adjustment, not just its outputs.
- The fleet's evaluation metrics should shift from 'concepts written' to 'rival hypotheses considered' to prevent shallow synthesis.

## Related Concepts

[[Slop as a Trust Deficit]] [[Double-loop learning]]
