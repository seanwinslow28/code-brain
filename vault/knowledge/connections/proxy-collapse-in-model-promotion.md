---
title: "Proxy Collapse in Model Promotion"
type: connection
connects:
  - Benchmarking Artifact
  - Runtime-Model Coupling
  - Agent Health
created: 2026-05-28
updated: 2026-05-28
---

## Synthesis

The tension arises between the need for scalable screening metrics and the inevitable degradation of those metrics as optimization targets. When a benchmark score serves as a trigger for promotion, it ceases to be a neutral measure of capability and becomes a target for manipulation by both models and humans. This Goodhartian collapse forces a structural separation between screening metrics and promotion criteria, requiring a native-harness eval or live task replay to verify actual competence. The consequence is that Sean must design a fleet selection policy that treats initial scores as mere triggers for deeper, more expensive verification rather than final judgments.

## Threads

### [[Benchmarking Artifact]]

> Add the stronger frame: once benchmark scores guide deployment, models and humans optimize to the proxy, and the proxy stops representing capability.

### [[Runtime-Model Coupling]]

> The missing facet is compatibility testing between model-native affordances and evaluator expectations.

### [[Agent Health]]

> A fleet selection policy that separates screening metrics from promotion criteria.

## Implications

- Sean must implement a Tier C Promotion Runbook where benchmark scores only trigger native-harness evals, live task replays, and failure-mode reviews.
- The evaluation harness must be treated as an interface contract with explicit subtypes for different model families to prevent construct validity violations.
- Fleet decision records must explicitly state whether a failure is due to model incompetence or test design flaws to avoid misleading optimization signals.
