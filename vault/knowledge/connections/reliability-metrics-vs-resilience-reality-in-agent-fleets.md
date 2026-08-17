---
title: "Reliability Metrics vs. Resilience Reality in Agent Fleets"
type: connection
connects:
  - SRE Error Budget for Agents
  - Resilience Engineering: Work-as-Imagined vs Work-as-Done
  - Agent Health Monitoring
created: 2026-08-15
updated: 2026-08-15
---

## Synthesis

Sean’s current monitoring relies on component health metrics that assume healthy agents guarantee routine success, but this ignores the reality of degraded operations. By contrasting SRE error budgets with resilience potentials, we see a tension between measuring uptime and measuring adaptive capacity. The consequence is that Sean may have a 'healthy' fleet that fails silently under edge cases, while missing the valuable data on how his system actually recovers from those failures.

## Threads

### [[SRE Error Budget for Agents]]

> A reliability contract for the completed routine, not component uptime. Example: “By 8:45 AM, a usable daily note contains current fleet status and no fabricated data on 29 of 30 days.”

### [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]

> Reject the concept’s implied equation `healthy agents → reliable routine`. Score four resilience potentials instead: respond, monitor, learn, anticipate.

### [[Agent Health Monitoring]]

> The synthesizer describes what the concept is; this expansion proposes what's missing.

## Implications

- Sean should stop relying solely on green dashboards and start tracking error budgets to decide when to freeze feature work for repair.
- He needs to record successful adaptations during failures to understand his system's true resilience rather than just its uptime.
