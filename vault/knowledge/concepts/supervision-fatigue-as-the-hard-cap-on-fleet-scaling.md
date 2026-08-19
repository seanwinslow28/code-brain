---
title: "Supervision Fatigue as the Hard Cap on Fleet Scaling"
type: concept
sources:
  - knowledge/expansions/supervision-fatigue-as-the-hard-cap-on-fleet-scaling.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

This concept defines a non-linear failure mode where human cognitive load, specifically 'supervision fatigue,' acts as the absolute bottleneck for agent fleet utility. Rather than scaling linearly with automation, the value of additional agents diminishes once the human reviewer's capacity to maintain taste and calibration is exhausted. The mechanism relies on the tension between automated throughput and the finite bandwidth of human judgment, creating a hard ceiling on effective system size.

## Context

Sean is currently running a fleet of synthesizer agents that generate significant volume (100+ concepts/run). Without accounting for his review capacity, he risks accumulating 'legibility debt' or accepting lower-quality outputs simply to clear the queue. Understanding this cap prevents him from over-investing in automation that outpaces his ability to curate.

## Evidence

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[supervision-fatigue-as-the-hard-cap-on-fleet-scaling]].

> The cited runs measure machine duration and artifact count—not Sean’s attention, fatigue, rejection rate, or trust.

> Supervision fatigue is currently an untested causal story.

## Examples

- Instrument three nightly conditions—5, 15, and 30 candidates—and record review time, raw TLX, acceptance rate, and delayed usefulness after seven days.
- Specify periodic blind ranking, manually authored synthesis rounds, and recovery drills where Sean must diagnose a deliberately corrupted connection without agent explanation.

## Related Concepts

[[The Taste-Throughput Trade-off in Agentic Synthesis]] [[Legibility Debt as a Supervision Failure Mode]]
