---
title: "Agent Fleet Observability Dashboard"
type: concept
sources:
  - knowledge/connections/velocity-vs-legibility-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-22
updated: 2026-07-22
---

## Definition

An observability framework that prioritizes the detection of silence, missing data, and semantic gaps over the confirmation of successful task completion. Instead of celebrating high throughput or low error rates in execution, this design pattern treats the absence of expected insight or the presence of unverified output as critical system errors. It shifts the metric of health from 'did the agent finish?' to 'did the agent produce something verifiable and valuable?', thereby aligning automated monitoring with human supervisory needs.

## Context

Sean's current dashboard likely highlights successful run completions, but he needs a view that flags when the synthesizer produces high volume with low semantic density or when manual tickets are ignored, indicating a breakdown in the feedback loop.

## Evidence

> Automated dashboards should be designed to highlight missing data or silence as critical errors, not just successful completions.

> The fundamental tension lies in the trade-off between the drive for automated throughput and the preservation of semantic integrity, leading to a systemic trust deficit.

## Examples

- A dashboard alert that triggers when 'rejected_count' exceeds a threshold relative to 'concepts_written', indicating a collapse in output quality.
- A visual indicator showing the time delta between concept generation and manual verification, highlighting where legibility debt is accumulating.

## Related Concepts

[[Agent Health Monitoring]] [[Control Room Observability]]
