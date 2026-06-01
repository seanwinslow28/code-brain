---
title: "Agent Health"
type: concept
sources:
  - 02_Areas/Agent-Fleet/daily-fleet-status-2026-05-31.md
tags: [auto-generated, phase-6]
created: 2026-06-01
updated: 2026-06-01
---

## Definition

Agent health is a measure of the successful execution of scheduled tasks by autonomous agents, indicating their operational readiness and reliability. It is determined by the status of daily runs, such as indexing or synthesis, and the absence of errors during these processes. This metric reflects the internal consistency of the agent fleet but does not account for external dependencies or hardware availability.

## Context

The consistent healthy status of agents like vault-indexer and vault-synthesizer suggests that the core automation logic is robust. However, this health is isolated to the agents' internal processes and does not guarantee the successful completion of broader, multi-step workflows that depend on external resources.

## Evidence

> vault-indexer (2:00 AM daily, Mac Mini, $0.00/run) - Status: healthy

> vault-synthesizer (2:30 AM daily, MBP (when awake), $0.00/run) - Status: healthy

## Examples

- The vault-indexer successfully processed 406 chunks with zero errors during its daily run.
- The vault-synthesizer completed its run with 28 concepts and 16 connections, indicating successful synthesis.

## Related Concepts

[[Agent Health Monitoring]] [[Agent Ops / FDP Backup Track]] [[Infrastructure Status]]
