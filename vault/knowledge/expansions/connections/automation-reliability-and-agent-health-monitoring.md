---
title: "How to make `Automation Reliability and Agent Health Monitoring` better"
type: expansion
parent: "[[automation-reliability-and-agent-health-monitoring]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-26
updated: 2026-06-26
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[automation-reliability-and-agent-health-monitoring]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “supervision-tree reliability,” not generic health checks.**  
   Anchor it on Joe Armstrong’s dissertation, [_Making Reliable Distributed Systems in the Presence of Software Errors_](https://erlang.org/download/armstrong_thesis_2003.pdf), plus Erlang/OTP’s [_Supervisor Behaviour_](https://www.erlang.org/doc/system/sup_princ.html). The missing pattern is: every agent has an owner, restart policy, dependency scope, escalation rule, and failure budget. Sentence pattern: “Agent X is supervised by Y; on failure mode Z, restart / isolate / escalate according to policy P.” This unlocks an **agent-fleet runbook** and an **executable supervision spec** for launchd agents, where the current concept only says “better monitoring.”

2. **Add “SLO/error-budget mode” for personal automation.**  
   Anchor it on Google SRE’s [_Monitoring Distributed Systems_](https://sre.google/sre-book/monitoring-distributed-systems/) and [_Alerting on SLOs_](https://sre.google/workbook/alerting-on-slos/). The missing facet is deciding what level of unreliability is acceptable before changing architecture. For Sean: “Daily note freshness SLO: 95% available by 8:45 AM; error budget burn triggers simplification, not more alerts.” This unlocks a **portfolio-grade reliability one-pager**: concrete service indicators for Vault Indexer, Synthesizer, Critic, Daily Driver, Job Feed, and Flush. It also supports real decisions like “do I add redundancy, delete an agent, or accept occasional failure?”

3. **Add “socio-technical accident analysis” to contradict the dashboard instinct.**  
   Anchor it on Nancy Leveson’s [_Engineering a Safer World_](https://mitpress.mit.edu/9780262533690/engineering-a-safer-world/) / STAMP-STPA, and Richard Cook’s [_How Complex Systems Fail_](https://how.complexsystems.fail/). The missing argument: failures are not just agent health events; they emerge from control loops, stale assumptions, hidden coupling, and humans adapting around brittle automation. Sentence pattern: “The hazardous control action was not ‘agent failed’; it was ‘system trusted stale vault state as current truth.’” This unlocks a **postmortem template** and a stronger **Substack essay**: “My Second Brain Failed Like a Production System,” where Sean sounds like an operator analyzing control failure, not a hobbyist describing cron jobs.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
