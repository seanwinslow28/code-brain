---
title: "Agent Health"
type: concept
sources:
  - 02_Areas/Agent-Fleet/fleet-state.md
tags: [auto-generated, phase-6]
created: 2026-06-03
updated: 2026-06-03
---

## Definition

Agent health is a metric of operational continuity defined by the successful execution of scheduled tasks and the absence of silent failures in the background processing layer. It requires agents to not only run but to produce verifiable outputs (like daily notes or index updates) that feed into the broader knowledge loop. When an agent's status is 'healthy' but its output is empty or stale, it indicates a latent failure in the context management layer rather than a true state of readiness.

## Context

Sean relies on the daily-driver and synthesizer agents to maintain the integrity of his daily notes and knowledge base. The health of these agents determines whether his morning planning is based on fresh data or stale context, directly affecting his daily decision-making efficiency.

## Evidence

> daily-driver morning (8:45 AM daily, Claude API, ~$0.40/run) - Status: healthy - notes='Morning planning complete for Tuesday 2026-06-02.'

> vault-synthesizer (2:30 AM daily, MBP (when awake), $0.00/run) - Status: healthy - notes='concepts=2 connections=1 rejected=4 edges=2'

## Examples

- The Daily Driver executed morning planning and generated today's note, maintaining process hygiene.

## Related Concepts

[[Agent Health Monitoring]] [[Daily Routine Automation]] [[Context Management as a Bottleneck]]
