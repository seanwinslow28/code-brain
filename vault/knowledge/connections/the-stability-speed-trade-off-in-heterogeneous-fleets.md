---
title: "The Stability-Speed Trade-off in Heterogeneous Fleets"
type: connection
connects:
  - Runtime-Model Coupling
  - Benchmarking Artifact
  - Agent Health
created: 2026-06-04
updated: 2026-06-04
---

## Synthesis

There is a fundamental tension between the demand for high-throughput interactive agents and the reality of resource-constrained local hardware. When a model like Gemma4 on an RTX 5080 is evaluated, the 'speed' metric from benchmarks often conflicts with the 'stability' metric from soak tests. The insight is that for a heterogeneous fleet, the optimal strategy is to decouple these metrics: assign high-speed tasks to high-resource nodes and high-stability, lower-speed tasks to constrained nodes, rather than forcing a single performance profile across all tiers.

## Threads

### [[Runtime-Model Coupling]]

> Recommend promotion for batch/async workloads; explicitly not for interactive use.

### [[Benchmarking Artifact]]

> The sole soft miss is a 1.2% throughput shortfall against a threshold calibrated on benchmark prompts rather than real batch load — immaterial for an async tier.

### [[Agent Health]]

> 17 / 17 `ok:true`; every output terminates on sentence punctuation. No mid-sentence cutoff at any `num_ctx`.

## Implications

- Sean should stop using benchmark throughput thresholds as hard gates for local models and instead define tier-specific stability thresholds based on soak data.
- The fleet architecture should explicitly route async/batch tasks to constrained nodes like the Alienware, preserving interactive capacity for higher-tier nodes.
