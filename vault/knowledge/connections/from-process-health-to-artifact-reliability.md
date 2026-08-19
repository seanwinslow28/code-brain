---
title: "From Process Health to Artifact Reliability"
type: connection
connects:
  - Operational Uptime vs. Cognitive Utility Tension
  - SRE Error Budget for Agents
  - The Illusion of Competence in Automated Systems
created: 2026-08-19
updated: 2026-08-19
---

## Synthesis

The tension between monitoring process execution and verifying artifact validity reveals a fundamental flaw in traditional automation design. By shifting focus from 'did the agent run?' to 'is the output valid?', we expose the gap between operational uptime and cognitive utility. This shift requires redefining health metrics to include semantic checks, ensuring that reliability is measured by the value delivered to the user rather than the activity of the underlying processes.

## Threads

### [[Operational Uptime vs. Cognitive Utility Tension]]

> Replace “background routines ran successfully” with a contract such as: “The daily note must exist, pass schema validation, and contain fleet output by 08:35; producer health is diagnostic metadata, not success.”

### [[SRE Error Budget for Agents]]

> This unlocks an executable Fleet Reliability Contract: per-artifact SLIs for freshness, completeness, correctness, and deadline attainment; corresponding SLOs; and alerts keyed to missing outcomes rather than green processes.

### [[The Illusion of Competence in Automated Systems]]

> Monitoring does not improve reliability unless it closes a control loop.

## Implications

- Sean must redesign his monitoring dashboards to prioritize artifact validity over process status, reducing false positives.
- This shift requires implementing schema validation and semantic checks in the daily note generation pipeline.
