---
title: "The Cost of Legibility in Agentic Workflows"
type: connection
connects:
  - The Efficiency-Quality Inversion in Automated Synthesis
  - Trajectory Evaluation vs. Final-State Grading
  - Supervision as the New AI Edge
created: 2026-08-31
updated: 2026-08-31
---

## Synthesis

There is a fundamental tension between the desire for cheap, disposable execution environments and the need for durable, inspectable state to support high-fidelity evaluation. As Sean moves from short, low-stakes runs to longer, more complex synthesis tasks, the 'cheapness' of corrections becomes irrelevant if the environment does not preserve the evidence needed to verify those corrections. The consequence is that infrastructure must shift from being purely disposable to being selectively durable, where only the state relevant to evaluation is preserved, creating a hybrid architecture that balances cost with epistemic integrity.

## Threads

### [[The Efficiency-Quality Inversion in Automated Synthesis]]

> The new production accounts converge on a separable substrate: durable session/event state, a replaceable agent loop, isolated or disposable execution, deterministic nodes around model calls, curated tools, and inspectable artifacts.

### [[Trajectory Evaluation vs. Final-State Grading]]

> Basis argues that a correct result reached through an unsupported or non-compliant path is not trustworthy and uses sparse BEHAVIOR.md contracts plus an agentic judge over the trajectory.

### [[Supervision as the New AI Edge]]

> Only Uber publishes this dual use in a first-party fleet account; most company accounts describe gates but no live eval monitors.

## Implications

- Sean should prioritize building 'inspectable artifacts' in his vault runs over simply increasing the number of concepts generated, as legibility is the prerequisite for any meaningful evaluation.
- The cost of maintaining durable state must be weighed against the risk of silent failure in long-horizon tasks, suggesting a need for explicit 'state checkpoints' rather than continuous logging.
