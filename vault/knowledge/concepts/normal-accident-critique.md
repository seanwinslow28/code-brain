---
title: "Normal Accident Critique"
type: concept
sources:
  - knowledge/expansions/connections/agent-health-monitoring-and-job-hunt-2026-automation-reliability.md
tags: [auto-generated, phase-6]
created: 2026-06-24
updated: 2026-06-24
---

## Definition

The Normal Accident framework posits that in tightly coupled and complex systems, some failures are inevitable system properties rather than bugs to be eliminated. Adding more monitoring or control layers can paradoxically increase risk by creating false confidence, inducing alarm fatigue, and introducing new coupling paths between previously independent components. This pattern suggests that resilience engineering must focus on designing for graceful degradation and bounded blast radii rather than pursuing dashboard maximalism or perfect observability.

## Context

This insight challenges Sean's current assumption that more monitoring always equals better safety, urging him to design agent fleets that degrade gracefully rather than pretending to be reliable. It provides a sophisticated narrative for his Substack and interviews about why his system is designed to fail safely rather than never failing.

## Evidence

> If agent fleets are complex and tightly coupled, some failures are not bugs to eliminate but system properties to design around.

> In tightly coupled systems, added observability can create false confidence, alarm fatigue, and new coupling paths.

## Examples

- A Substack essay titled 'Why My Agent Fleet Is Designed to Degrade, Not Pretend It Is Reliable.'

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Silent Failure Propagation in Agent Fleets]]
