---
title: "The Tension Between Protocol Instrumentation and Regulatory Ambiguity in Agent Supervision"
type: connection
connects:
  - Supervision as the New AI Edge
  - SRE Error Budget for Agents
  - Resilience Engineering: Work-as-Imagined vs Work-as-Done
created: 2026-06-30
updated: 2026-06-30
---

## Synthesis

This connection reveals a fundamental tension between the need for precise, executable supervision specs (like Erlang/OTP's Supervisor Behaviour) and the ambiguity of defining SLOs for personal automation. While protocol instrumentation allows for detailed monitoring and restart policies, regulatory ambiguity arises when determining what level of unreliability is acceptable for different agents. This tension manifests in the difficulty of creating a unified error budget that balances reliability with cognitive load, forcing Sean to choose between rigid control and flexible adaptation.

## Threads

### [[Supervision as the New AI Edge]]

> Every agent has an owner, restart policy, dependency scope, escalation rule, and failure budget.

### [[SRE Error Budget for Agents]]

> The missing facet is deciding what level of unreliability is acceptable before changing architecture.

### [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]

> Failures are not just agent health events; they emerge from control loops, stale assumptions, hidden coupling, and humans adapting around brittle automation.

## Implications

- Sean must define distinct SLOs for each agent based on its criticality to his job hunt and creative work, rather than applying a uniform reliability standard.
- The supervision tree must be flexible enough to handle ambiguous failure modes, such as stale data, which are not easily captured by traditional health checks.
