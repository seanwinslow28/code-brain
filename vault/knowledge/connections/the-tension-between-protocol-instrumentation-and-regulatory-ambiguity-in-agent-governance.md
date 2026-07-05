---
title: "The Tension Between Protocol Instrumentation and Regulatory Ambiguity in Agent Governance"
type: connection
connects:
  - SRE Error Budget for Agents
  - Resilience Engineering: Work-as-Imagined vs Work-as-Done
  - Reflexion Loop
created: 2026-07-02
updated: 2026-07-02
---

## Synthesis

There is a fundamental tension between the need for precise protocol instrumentation to measure agent health and the regulatory ambiguity of defining what constitutes an 'unhealthy' state in personal automation. While SLOs provide useful metrics, they often fail to capture the nuanced reality of work-as-done versus work-as-imagined, leading to false positives or negatives in system health assessments. This tension forces a re-evaluation of how we define reliability in autonomous systems, shifting from binary success/failure to managed degradation states that preserve minimum viable context.

## Threads

### [[SRE Error Budget for Agents]]

> Daily context is healthy when TODAY_NOTE_EXISTS, OVERNIGHT_DIGEST_INJECTED, OPEN_TICKETS_VISIBLE, and LAST_AGENT_RUN_STATUS_KNOWN are true by 09:00.

### [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]

> Woods gives Sean a stronger critique: brittle systems fail because they lack adaptive capacity at the boundary, not because one component errors.

### [[Reflexion Loop]]

> Add the saga pattern: split the routine into idempotent steps with explicit compensation: create note shell -> inject template -> attach overnight digest -> update fleet console -> verify backlinks.

## Implications

- Sean must define clear SLOs for context availability while acknowledging that agent failures are inevitable and require managed degradation strategies.
- The system's reliability depends on its ability to adapt to partial failures rather than just preventing them through rigid protocol enforcement.
