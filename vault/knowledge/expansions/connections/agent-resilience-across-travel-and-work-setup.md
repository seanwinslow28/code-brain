---
title: "How to make `Agent Resilience Across Travel and Work Setup` better"
type: expansion
parent: "[[agent-resilience-across-travel-and-work-setup]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-07
updated: 2026-06-07
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-resilience-across-travel-and-work-setup]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “graceful degradation modes” as a first-class resilience pattern**

   Anchor it on: **Leslie Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System”** plus **Pat Helland, “Life Beyond Distributed Transactions.”**

   Current concept treats travel as an availability problem: MBP absent, agents fail. Missing move: model the fleet as a distributed system with partial availability, stale reads, and eventual reconciliation.

   Add a mode table:

   `Normal LAN mode -> Travel degraded mode -> Catch-up reconciliation mode -> Human escalation mode`

   This unlocks a **fleet resilience runbook**: which agents must keep running on Mac Mini, which may emit stale-but-labeled outputs, which should queue work, and which should fail closed. Right now the article can only say “unified setup routines”; this would let Sean ship an operational artifact with concrete failure semantics.

2. **Add “planned absence as a calendar-aware chaos test”**

   Anchor it on: **Nora Jones and Casey Rosenthal, _Chaos Engineering_**, specifically the discipline of testing socio-technical failure modes before production incidents.

   The missing facet is that travel should not be detected only after agents fail. It should become a scheduled resilience exercise: “MBP absent from home LAN for N days” is a known fault injection, not an outage surprise.

   Add a pattern:

   `Before travel: simulate MBP unreachable for 24h -> observe agent behavior -> promote failures into tickets -> reroute critical jobs -> mark expected misses separately from incidents`

   This unlocks a **travel preflight checklist and executable dry-run command**. Sean could produce a portfolio-worthy “personal agent fleet chaos drill” showing mature agent ops judgment. The current concept sounds like generic continuity planning; this turns it into an operator-grade reliability practice.

3. **Add “situated action vs centralized plan” as the contradicting framework**

   Anchor it on: **Lucy Suchman, _Plans and Situated Actions_**.

   The concept assumes better unified routines will solve continuity. Suchman’s useful contradiction: plans do not control action; they are resources actors use while responding to local conditions. For Sean, this means the system should not just encode “travel setup.” It should sense the actual situation: machine reachable, calendar context, battery/power state, VPN/LAN status, queue age, agent criticality.

   Add the distinction:

   `Plan: travel mode starts Friday. Situated action: MBP unreachable, Mac Mini reachable, job_feed critical, vault_synthesizer deferrable, queue age 36h, escalate only if daily note blocked.`

   This unlocks an **agent spec for contextual resilience policy**: a declarative intent file where agents choose behavior from observed constraints, not brittle travel checklists. It also gives Sean a sharper Substack angle: “agent ops fails when it treats human context as configuration instead of situation.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
