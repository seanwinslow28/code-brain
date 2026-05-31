---
title: "Context Bloat vs. Historical Fidelity in Roadmap Management"
type: connection
connects:
  - Archival Offloading as Context Optimization
  - Unified Roadmap
  - Vault as Agent Infrastructure
created: 2026-05-31
updated: 2026-05-31
---

## Synthesis

The tension lies between the need for a complete, verbatim history of project decisions and the constraint of limited AI context windows. By offloading the 'ship history' to a separate file, Sean optimizes the active context for the agent, but this creates a dependency where the agent must know to look in two places for a complete picture. The consequence is a more efficient agent for current tasks, but a higher cognitive load for Sean to maintain the link between the 'active' and 'archived' states. This pattern suggests that as projects grow, the 'single source of truth' must be logically split to preserve agent performance.

## Threads

### [[Archival Offloading as Context Optimization]]

> The tension between comprehensive record-keeping and efficient AI processing is resolved by decoupling the active roadmap from its historical log.

### [[Unified Roadmap]]

> The parent roadmap stays focused on open + in-flight work; this file accumulates outcomes.

### [[Vault as Agent Infrastructure]]

> This file holds the ship history — dated amendments and the bodies of fully-closed tasks.

## Implications

- Sean must ensure that any agent accessing the roadmap is aware of the companion file to avoid missing historical context.
- The separation allows the parent roadmap to remain 'living' and actionable without becoming a bloated archive, improving agent response times and accuracy for current tasks.
