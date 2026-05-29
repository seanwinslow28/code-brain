---
title: "Agentic Engineering Signal"
type: concept
sources:
  - 40_knowledge/references/ref-agent-product-analytics-runs-not-sessions.md
tags: [auto-generated, phase-6]
created: 2026-05-29
updated: 2026-05-29
---

## Definition

The unit of product behavior shifts from the session to the agent run, requiring analytics to track the specific steps an agent takes, the tools it touches, and the boundaries it hits. This mechanism collapses the feedback loop from weeks to minutes, allowing developers to shape and steer agent behavior mid-flight. Without this granular signal, powerful automation becomes dangerous because the consequences of decisions land in real time without visibility. The core invariant is that completion of a task does not equal user trust; the gap between finishing and being accepted is where autonomy is earned.

## Context

Sean is building an eval suite and job-hunting for AI PM roles. Understanding that 'completion' is not 'acceptance' is critical for designing the right metrics for his portfolio projects and for evaluating AI products in interviews. He needs to distinguish between workflows that are merely functional and those that have earned enough trust to operate autonomously.

## Evidence

> When the user is an agent, the unit of product behavior is becoming the agent run: the work a user handed over, the steps the agent took, the tools it touched, the boundaries it hit, the corrections it got back, and whether anyone accepted the result.

> Speed is the engine. Analytics is the rudder. A database that vanishes in nine seconds is what happens when you have a powerful engine and no way to steer.

## Examples

- Tracking agent_run_started + task_completed + user_correction_submitted joined on agent_run_id to separate completion from acceptance.

## Related Concepts

[[Eval Vocabulary]] [[Agentic Engineering]]
