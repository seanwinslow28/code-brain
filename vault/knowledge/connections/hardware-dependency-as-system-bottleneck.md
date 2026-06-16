---
title: "Hardware Dependency as System Bottleneck"
type: connection
connects:
  - Infrastructure Status
  - Vault as Agent Infrastructure
  - Automation Reliability
created: 2026-06-16
updated: 2026-06-16
---

## Synthesis

The agent fleet's reliability is inextricably linked to the physical state of Sean's hardware, creating a bottleneck where software automation cannot outperform hardware availability. Because key agents like vault-synthesizer depend on the MBP being awake, the system's 'always-on' promise is violated by the user's sleep schedule or laptop power management. This tension exposes that infrastructure status is not just a monitoring metric but a functional constraint that limits the scope of autonomous operations.

## Threads

### [[Infrastructure Status]]

> System dependency remains fragile: vault synthesis relies on the MBP being awake, hindering robust 'always-on' system reliability.

### [[Vault as Agent Infrastructure]]

> The health of the autonomous agent fleet, such as vault-indexer and vault-synthesizer, is directly tied to the overall infrastructure health of Sean's systems.

### [[Automation Reliability]]

> The reliability of the agent fleet has a direct impact on the functionality and effectiveness of automation routines across different domains.

## Implications

- Sean should migrate critical synthesis tasks to the always-on Mac Mini to eliminate hardware-dependent failure modes.
- Infrastructure monitoring must include wake/sleep states as a primary health metric, not just process status.
