---
title: "The Latency of Learning vs. The Cost of Waiting"
type: connection
connects:
  - Negative Capability / Failure Literacy
  - Context Compounding
  - SRE Error Budget for Agents
created: 2026-06-29
updated: 2026-06-29
---

## Synthesis

There is a fundamental tension between the labs' bet that scaling RL environments will solve AGI and Sean's immediate need for reliable, sample-efficient agents in his job hunt. While labs argue that data inefficiency during training is amortized across billions of sessions, Sean cannot afford the 'one-time cost' of training when he needs results now. This creates a strategic divergence: Sean must rely on models with high 'Negative Capability' out-of-the-box, whereas the industry is betting on post-training scaling to achieve similar resilience.

## Threads

### [[Negative Capability / Failure Literacy]]

> Because such training will create these general problem solving skills (like how to make progress on an open ended task for weeks on end in the face of errors, mistakes, and ambiguity).

### [[Context Compounding]]

> what really matters is how smart and general and sample efficient the model is during a session.

### [[SRE Error Budget for Agents]]

> the data inefficiency of these models or the fact that they lack continual learning, these things can just be steamrolled if we just scale training more.

## Implications

- Sean should prioritize agents with strong few-shot learning capabilities over those requiring extensive fine-tuning for his current job hunt.
- The 'SRE Error Budget' for his personal fleet must be tighter than industry standards because he lacks the compute to retrain models on failure data.
