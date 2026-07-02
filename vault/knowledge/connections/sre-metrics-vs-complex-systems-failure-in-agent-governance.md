---
title: "SRE Metrics vs. Complex Systems Failure in Agent Governance"
type: connection
connects:
  - SRE Error Budget for Agents
  - Normal Accident Critique
  - Agent Health Monitoring
created: 2026-07-02
updated: 2026-07-02
---

## Synthesis

The tension lies between the desire for deterministic reliability through SRE metrics and the reality of complex systems failing normally due to hidden coupling. While SLOs provide a useful product-facing interface for measuring agent health, they may mask the underlying systemic fragility where incidents are caused by exhausted adaptive capacity rather than component failure. This creates a governance challenge where Sean must balance explicit quality indicators with an understanding that his agentic infrastructure is inherently unstable and requires safety cases rather than just monitoring.

## Threads

### [[SRE Error Budget for Agents]]

> The missing move is to define the daily note and research synthesis as user-facing services with SLIs: daily note exists by 08:45, overnight digest freshness, research synthesis citation-validity rate, critic expansion novelty rate, manual repair time.

### [[Normal Accident Critique]]

> Cook’s sharper frame says complex systems are always running near failure; incidents reveal hidden coupling and exhausted adaptive capacity.

### [[Agent Health Monitoring]]

> The current concept implies healthier agents reduce disruption.

## Implications

- Sean should develop an agent safety case that maps autonomy boundaries and stop rules, rather than relying solely on SLOs for reliability assurance.
- Portfolio demonstrations must include both product-facing quality indicators and a narrative about systemic resilience to avoid the illusion of competence.
