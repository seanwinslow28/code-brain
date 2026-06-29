---
title: "The Tension Between Automation Reliability and Adaptive Capacity"
type: connection
connects:
  - SRE Error Budget for Agents
  - Resilience Engineering: Work-as-Imagined vs Work-as-Done
  - Premortem Before Automation
created: 2026-06-29
updated: 2026-06-29
---

## Synthesis

This connection reveals the tension between the desire for fully automated reliability and the finite adaptive capacity of the human-agent system. When an upstream synthesizer fails, the system does not just miss a note; it exhausts all morning-planning slack, leading to a 'going solid' state where no fallback mechanisms are available. This pattern suggests that true reliability requires not just monitoring, but explicit error budgets and pre-mortem rituals to manage the saturation points of the system.

## Threads

### [[SRE Error Budget for Agents]]

> The daily note is not ‘important’; it has an SLO: created by 8:30 AM on 29/30 days, with degraded fallback by 8:45.

### [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]

> The failure was not the missing note; the system went solid when one upstream synthesizer failure exhausted all morning-planning slack.

### [[Premortem Before Automation]]

> It is May 15 again; the daily note did not exist by 8:30. What had to be true yesterday for that to happen?

## Implications

- Sean must define explicit error budgets for his daily note SLO to make reliability trade-offs visible and manageable.
- He should implement pre-flight rituals for new agents to surface hidden dependencies before they cause systemic saturation.
