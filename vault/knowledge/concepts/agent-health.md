---
title: "Agent Health"
type: concept
sources:
  - 02_Areas/Agent-Fleet/fleet-state.md
tags: [auto-generated, phase-6]
created: 2026-05-27
updated: 2026-05-27
---

## Definition

Agent health is a metric of temporal freshness and execution success, where 'stale' indicates a failure to complete a scheduled cycle within the expected window, regardless of whether the agent is technically enabled. A healthy agent produces output that updates the state of the vault, while a stale agent represents a broken dependency chain where downstream processes cannot rely on its data. This distinction is crucial because it separates the *potential* for work (enabled status) from the *actualization* of work (freshness of output).

## Context

Sean monitors agent health to ensure his daily routine and knowledge base remain current. The difference between a 'healthy' daily-driver and a 'stale' synthesizer highlights the fragility of automated workflows when they depend on specific conditions (like the MBP being awake) that are not guaranteed.

## Evidence

> vault-synthesizer (2:30 AM daily, MBP (when awake), $0.00/run) - Status: stale

> daily-driver morning (8:45 AM daily, Claude API, ~$0.40/run) - Status: healthy

> deep-researcher (2:45 AM daily, Mac Mini, $0.00/run) - Status: stale

## Examples

- The daily-driver morning agent runs successfully and creates a daily note.
- The vault-indexer runs successfully but is considered stale because it is 30.7 hours old.

## Related Concepts

[[Agent Health Monitoring]] [[Daily Routine Automation]] [[Infrastructure Status]]
