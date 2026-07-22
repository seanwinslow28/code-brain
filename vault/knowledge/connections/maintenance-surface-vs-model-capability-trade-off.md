---
title: "Maintenance Surface vs. Model Capability Trade-off"
type: connection
connects:
  - Harness Engineering Invariant
  - The Illusion of Health in Autonomous Systems
  - Agent Health Monitoring
created: 2026-07-20
updated: 2026-07-20
---

## Synthesis

There is a fundamental tension between increasing an agent's capability by adding tools and maintaining its reliability, as the harness complexity grows faster than model intelligence can compensate. This trade-off means that upgrading to more powerful models like qwen3.6-35b often masks underlying failures rather than resolving them, because the expanded maintenance surface introduces new points of silent drift. The consequence is a false sense of progress where operational metrics improve while semantic quality degrades, requiring Sean to prioritize harness pruning over model upgrades.

## Threads

### [[Harness Engineering Invariant]]

> This invariant posits that agent reliability is inversely proportional to the complexity of its surrounding harness, as every added tool or permission expands the failure surface non-linearly.

### [[The Illusion of Health in Autonomous Systems]]

> The agents you have already built will keep producing work long after they stop being right.

### [[Agent Health Monitoring]]

> You look at lines, fittings, pumps, batteries, corrosion, and weather differently when the thing you are maintaining is also the thing that has to bring you back.

## Implications

- Sean should prioritize pruning his synthesizer's toolset and reference files before attempting to upgrade models, as reducing the harness surface area will improve reliability more than raw compute power.
- Monitoring 'health' metrics like run duration or error codes is insufficient; Sean must implement semantic verification of the synthesizer's output to detect when it 'stops being right' while still completing successfully.
