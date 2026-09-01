---
title: "Evaluation Metrics vs. Production Reality in Agent Fleets"
type: connection
connects:
  - The Illusion of Competence in Automated Systems
  - Probabilistic Reality vs. Deterministic Expectation
  - Supervision as the New AI Edge
created: 2026-08-31
updated: 2026-08-31
---

## Synthesis

There is a fundamental tension between the deterministic expectations of evaluation metrics (like pass/fail rates on synthetic tests) and the probabilistic reality of agent performance in production. Sean's vault synthesizer tracks quantitative outputs (concepts_written, duration_seconds), which creates an illusion of health and competence. However, as Basis highlights, passing 100% of evals does not guarantee generalization to the real world because the test distribution is often narrower than the operational environment. This leads to a 'confidence gap' where Sean may believe his fleet is robust based on internal metrics while it actually suffers from silent failures or poor contextual grounding in live scenarios.

## Threads

### [[The Illusion of Competence in Automated Systems]]

> Even if you got it right a 100 out of 100 times if a person is just getting it right because they're going to Wikipedia the accounting firm wouldn't hire them and so they shouldn't hire us either

### [[Probabilistic Reality vs. Deterministic Expectation]]

> The core tension in AI product management lies in the mismatch between the probabilistic nature of AI models and the deterministic expectations users have for software interfaces.

### [[Supervision as the New AI Edge]]

> Humans are already used to working with nondeterministic systems It's just those systems are normally their co-workers not their computers

## Implications

- Sean must shift his primary success metric from quantitative output counts (concepts_written) to qualitative verification rates or human-in-the-loop acceptance rates.
- The current 'manifest-then-top-5' retrieval pattern may be insufficient if it doesn't provide enough contextual depth to prevent the illusion of competence.
