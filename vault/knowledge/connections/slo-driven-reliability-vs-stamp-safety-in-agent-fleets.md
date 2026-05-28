---
title: "SLO-Driven Reliability vs. STAMP Safety in Agent Fleets"
type: connection
connects:
  - Agent Health
  - Intent Engineering
  - Infrastructure Status
created: 2026-05-28
updated: 2026-05-28
---

## Synthesis

The tension lies between measuring agent health by its output utility (SLOs) versus its control-loop safety (STAMP). SLOs ensure the agent is useful, but STAMP ensures the agent doesn't cause latent failures by acting on a bad mental model. The consequence is that Sean must build a dual-layer monitoring system: one for freshness/errors (SLO) and one for intent/model correctness (STAMP). This prevents the 'silent compensation' where an agent runs successfully but produces dangerous or stale insights.

## Threads

### [[Agent Health]]

> Define agent health as a small SLO contract: freshness, successful completion, output usefulness, dependency readiness, and downstream consumer impact.

### [[Intent Engineering]]

> Model each scheduled agent as a controller in a feedback system: controller, controlled process, sensor signal, actuator, process model, unsafe control actions.

### [[Infrastructure Status]]

> The missing question is not “did the synthesizer run?” but “what incorrect model of the world caused the fleet to keep depending on an asleep MBP?”

## Implications

- Sean must define 'unsafe control actions' for his job-hunt agents, not just 'errors'.
- Monitoring must track both 'freshness' (SLO) and 'model correctness' (STAMP) to prevent silent failures.
- The 'Agent Fleet SLO one-pager' must include safety constraints from STAMP analysis.
