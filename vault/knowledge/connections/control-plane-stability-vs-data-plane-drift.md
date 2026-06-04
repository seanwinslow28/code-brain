---
title: "Control Plane Stability vs. Data Plane Drift"
type: connection
connects:
  - Control Plane / Data Plane Split for Agent Fleets
  - Resilience Engineering: Work-as-Imagined vs Work-as-Done
  - Infrastructure Status and Agent Failure
created: 2026-06-04
updated: 2026-06-04
---

## Synthesis

The tension lies between the need for a stable, predictable control plane and the inherent volatility of the data plane where agents interact with a living vault. When the control plane assumes a static environment but the data plane experiences drift due to user changes or agent mutations, the system fails not because of control logic errors, but because of unmanaged divergence. This pattern reveals that resilience in agentic systems requires monitoring the gap between intended and actual workflows, not just the health of the control processes themselves. The consequence is that traditional uptime monitoring is insufficient; Sean must monitor the consistency of agent outputs against expected vault states.

## Threads

### [[Control Plane / Data Plane Split for Agent Fleets]]

> distinguish the control plane that schedules, routes, authorizes, observes, and halts agents from the data plane where agents actually read/write vault artifacts, run research, generate summaries, or mutate files.

### [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]

> agent ops is not just keeping agents green; it is detecting when the designed workflow and the real workflow diverge.

### [[Infrastructure Status and Agent Failure]]

> This concept defines the architectural necessity of distinguishing between the control plane, which dictates desired state and routing policies, and the data plane, which executes local actions.

## Implications

- Sean should implement monitoring that tracks not just agent uptime, but the consistency of agent outputs against expected vault states to detect drift early.
- Interview discussions should emphasize how separating control and data planes allows for more targeted debugging of agent failures, distinguishing between scheduling errors and artifact mutation errors.
