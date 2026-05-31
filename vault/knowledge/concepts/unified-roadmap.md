---
title: "Unified Roadmap"
type: concept
sources:
  - knowledge/connections/archival-offloading-as-context-optimization.md
tags: [auto-generated, phase-6]
created: 2026-05-31
updated: 2026-05-31
---

## Definition

The Unified Roadmap functions as a dynamic control plane that must be strictly decoupled from its historical log to maintain operational integrity. This pattern reveals that maintaining a 'living' document requires active pruning of completed work to preserve signal-to-noise ratio for agents. The mechanism relies on a separation of concerns where the active roadmap focuses exclusively on open and in-flight work, while historical outcomes are offloaded to a separate archival store. This decoupling prevents the active roadmap from becoming a bloated, unmanageable artifact that hinders rather than helps strategic planning.

## Context

Sean's current roadmap is suffering from bloat because it accumulates outcomes alongside active tasks. This conflation forces his agents to process irrelevant historical data, leading to the token waste described in the related concept. The immediate implication is that Sean must enforce strict conventions for moving tasks to the completion log to prevent the parent roadmap from bloating again.

## Evidence

> The parent roadmap stays focused on open + in-flight work; this file accumulates outcomes.

> This pattern reveals that maintaining a 'living' document requires active pruning of completed work to preserve signal-to-noise ratio for agents.

## Examples

- The parent roadmap staying focused on open + in-flight work while a separate file accumulates outcomes.

## Related Concepts

[[Token Waste]] [[Vault as Agent Infrastructure]]
