---
title: "The Cost-Reliability Decoupling in Agentic Systems"
type: connection
connects:
  - SRE Error Budget for Agents
  - Liability Routing in Agentic Product Design
  - The Illusion of Competence in Automated Systems
created: 2026-08-29
updated: 2026-08-29
---

## Synthesis

There is a fundamental tension between financial cost budgets and reliability error budgets in agentic systems. Financial constraints limit the volume of operations, while reliability constraints limit the quality of outputs; optimizing for one often degrades the other if not explicitly managed. This decoupling means that a system can be cheap to run but unreliable, or reliable but prohibitively expensive, requiring separate governance mechanisms for each.

## Threads

### [[SRE Error Budget for Agents]]

> You have never written down a tolerable failure rate: 'this can be wrong 8% of the time before we stop shipping it.'

### [[Liability Routing in Agentic Product Design]]

> When your synthesizer degrades, you find out. When a claims model degrades, a stranger doesn't get paid.

### [[The Illusion of Competence in Automated Systems]]

> A probabilistic system carries a permanent tax that a deterministic one does not.

## Implications

- Sean must define separate thresholds for cost and reliability to avoid conflating financial efficiency with operational trust.
- Product designs that ignore liability routing risk externalizing failure costs onto users, leading to long-term reputational damage.
