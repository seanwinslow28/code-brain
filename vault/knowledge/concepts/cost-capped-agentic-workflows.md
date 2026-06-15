---
title: "Cost-Capped Agentic Workflows"
type: concept
sources:
  - 02_Areas/Agent-Fleet/daily-fleet-status-2026-06-12.md
tags: [auto-generated, phase-6]
created: 2026-06-15
updated: 2026-06-15
---

## Definition

This mechanism describes a hard constraint architecture where financial limits act as the primary failure mode for operational continuity, rather than technical errors. When an agent's execution exceeds its allocated budget threshold, the system halts immediately to prevent uncontrolled spending, effectively treating cost exhaustion as a critical error state that breaks downstream dependencies. This creates a fragile link between financial governance and daily information synthesis, where the absence of funds directly causes data staleness in the user's primary interface.

## Context

Sean relies on the 'daily-driver morning' agent to generate his daily note, which serves as the central hub for his operational context. The failure of this specific agent due to budget exhaustion ($0.9107 cost vs. limit) means the entire day's synthesis is missing, forcing Sean to manually reconstruct context or operate without the automated brief he depends on.

## Evidence

> daily-driver morning failed due to budget exhaustion (max_budget_usd), halting key operational synthesis.

> cost=$0.9107 · notes='Command failed with exit code 1 (exit code: 1) Error output: Check stderr out...'

> Immediately stabilize agent budgets (e.g., daily-driver) to prevent operational context loss from hitting hard limits.

## Examples

- The daily-driver morning agent incurred a cost of $0.9107 before triggering the max_budget_usd error, resulting in an exit code 1 and no output for the daily note.
- Other agents like vault-indexer and vault-synthesizer run at $0.00/run, indicating that only high-cost API calls (like Claude) are subject to these hard financial caps.

## Related Concepts

[[Agent Health Monitoring]] [[Automation Failure and Daily Note Disruption]] [[Infrastructure Status]]
