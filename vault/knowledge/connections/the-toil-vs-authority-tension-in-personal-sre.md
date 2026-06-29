---
title: "The Toil vs. Authority Tension in Personal SRE"
type: connection
connects:
  - SRE Error Budget for Agents
  - Control Room Observability
  - Agent Health Monitoring
created: 2026-06-29
updated: 2026-06-29
---

## Synthesis

There is a fundamental tension between the SRE principle of minimizing toil and the Control Room requirement for explicit human authority. When agents fail, the SRE budget dictates whether to automate the fix or accept manual correction, while the Control Room model demands clear escalation paths and abort criteria. This tension surfaces when Sean must decide if an agent failure is a transient error to be patched or a systemic risk requiring operational intervention.

## Threads

### [[SRE Error Budget for Agents]]

> Example: “daily note freshness SLO: 95% before 9 AM”; “manual correction budget: under 20 minutes/week”; “agent toil: any recurring human patch after automation failure.”

### [[Control Room Observability]]

> This turns the concept from “my agents emit status into my daily note” into an operator runbook: alert classes, named consoles, go/no-go rules, incident drills, and handoff protocols.

### [[Agent Health Monitoring]]

> Current failure mode: the article treats observability as awareness. This adds observability as command authority.

## Implications

- Sean must define explicit abort criteria for agent workflows to prevent silent failures from accumulating into unmanageable toil.
- The error budget for manual corrections directly limits the scope of Control Room escalation, forcing earlier intervention when SLOs are breached.
