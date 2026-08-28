---
title: "How to make `Agent Health and Automation Failure` better"
type: expansion
parent: "[[agent-health-and-automation-failure]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-16
updated: 2026-08-16
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-health-and-automation-failure]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “outcome health, not process health” via black-box SLOs.** Anchor it in Rob Ewaschuk’s Google SRE chapter, [“Monitoring Distributed Systems”](https://sre.google/sre-book/monitoring-distributed-systems/), especially the distinction between white-box evidence (“the agent logged something”) and black-box evidence (“the promised artifact exists and works”). Sentence pattern: *“A healthy run is not a live process; it is a fresh daily note produced by 08:35, containing the fleet digest, with valid source timestamps.”* This unlocks an **Agent Outcome Contract**—a YAML agent spec, executable probe, and dashboard definition—that can distinguish `process_alive`, `run_completed`, and `user_outcome_delivered`. The current concept cannot make that operational decision.

2. **Add “failure is an emergent trajectory, not a broken component.”** Anchor it in Richard Cook’s [“How Complex Systems Fail”](https://how.complexsystems.fail/): complex systems normally operate in degraded states, catastrophes require multiple contributing conditions, and “root cause” stories are usually hindsight compression. Replace “ensure these agents are healthy” with a contributor map: scheduler timing, credential freshness, host reachability, baton state, write locks, template validity, and consumer expectations. This unlocks a **portfolio-grade incident reconstruction or fault-injection demo** showing how individually reasonable components combine to miss a note—and which recovery margin actually prevents recurrence. It also contradicts the article’s unsupported jump from `log-only` to agent failure.

3. **Add the “ironies of automation” as a human-control constraint.** Anchor it in Lisanne Bainbridge’s 1983 paper, [“Ironies of Automation”](https://www.sciencedirect.com/science/article/pii/0005109883900468): automation leaves the human responsible for rare failures while simultaneously depriving them of the practice and situational awareness needed to recover. For a one-person fleet, silent self-healing can therefore reduce system safety. Add a rule such as: *“Every automated recovery path must preserve diagnosis evidence and periodically exercise the operator’s manual recovery path.”* This unlocks a **fleet recovery runbook plus quarterly game-day drill**—for example, expire the OAuth token, suppress the MBP route, or corrupt a baton, then measure detection and recovery time. It also gives Sean a strong **Substack argument about the operator paradox of personal agent fleets**, rather than another generic observability note.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
