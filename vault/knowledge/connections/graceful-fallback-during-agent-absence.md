---
title: "Graceful Fallback During Agent Absence"
type: connection
connects:
  - Agent Health Monitoring
  - Autonomous Agent Fleets
  - Automation Reliability
created: 2026-05-14
updated: 2026-05-14
---

## Synthesis

A cross-domain pattern where agent reliability systems (from `Autonomous Agent Fleets`) leverage automation reliability and health monitoring systems to handle fleet disruptions during scheduled MBP trips.

## Threads

### [[Agent Health Monitoring]]

> Raises `WOLUnavailable` from `route_to_macbook()`, exits cleanly, logs status=fail in synth-manifest

> The fallback work in Part 2 is not yet implemented — check the Status Tracker.

### [[Autonomous Agent Fleets]]

> `vault_synthesizer`, `job_feed`, and `flush` agents are hosted on the MBP, which is off the home LAN during travel

> The system has no notion of scheduled MBP absences — every failure looks identical to 'MBP happened to be asleep.'

### [[Automation Reliability]]

> If today is between 2026-05-14 and 2026-05-16 and the fleet looks broken, that's expected — see Part 1.

> The fallback work in Part 2 is not yet implemented — check the Status Tracker.

## Implications

- Future design of agent systems must include scheduled absence handling to prevent misinterpretation of failures.
- Automation reliability requires a centralized 'trip mode' toggle or fallback strategy to avoid confusion between planned and unplanned outages.
