---
title: "How to make `Agent Health and Operational Resilience` better"
type: expansion
parent: "[[agent-health-and-operational-resilience]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-17
updated: 2026-08-17
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-health-and-operational-resilience]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Replace binary “agent health” with user-centered SLOs and error budgets

**What to add:** A service-level model separating **process health**, **task success**, and **workflow outcome**. An offline endpoint is not automatically unhealthy: the question is whether it consumed an agreed reliability budget or prevented a promised outcome.

**Canonical anchor:** Marc Alvidrez and Mark Roth, [“Embracing Risk” in *Site Reliability Engineering*](https://sre.google/sre-book/embracing-risk/). Its error-budget model explicitly rejects maximum uptime as the goal.

**Sentence pattern:** “`vault-synthesizer` deferred because the MBP was unavailable; the system remained healthy because the work re-queued without violating the 24-hour freshness SLO.”

**What this unlocks:** An executable **Fleet SLO Contract** and portfolio-grade observability demo: freshness, completion, recovery-time, and data-integrity indicators for each agent, plus rules such as “freeze new fleet features when the weekly knowledge-freshness budget is exhausted.” The current article can report status; this addition can govern investment and release decisions.

## 2. Replace “hardening” with graceful extensibility at saturation boundaries

**What to add:** **Graceful extensibility**—designing the fleet to preserve essential functions when capacity, context, dependencies, or operator attention saturate. Hardening asks how to stop failure; graceful extensibility asks what the system does after its assumptions fail.

**Canonical anchor:** David D. Woods, [“The Theory of Graceful Extensibility: Basic Rules That Govern Adaptive Systems”](https://www.researchgate.net/publication/327427067_The_Theory_of_Graceful_Extensibility_Basic_rules_that_govern_adaptive_systems), and his shorter [“Resilience as Graceful Extensibility to Overcome Brittleness”](https://www.irgc.org/wp-content/uploads/2018/09/Woods-Resilience-as-Graceful-Extensibility-to-Overcome-Brittleness-1.pdf).

**Sentence pattern:** “When Tier C disappears, preserve manifest truth and bounded backlog growth; shed visual QA before provenance, and never disguise deferred work as successful work.”

**What this unlocks:** A **degraded-mode specification** for Code-Brain: essential/nonessential capability tiers, load-shedding order, backlog ceilings, recovery semantics, and dependency-loss drills. It would also produce a strong Substack essay: *Your Agent Fleet Is Not Resilient Because Everything Is Online*.

## 3. Add operator readiness as a health dimension

**What to add:** The **Ironies of Automation** critique: automation removes humans from routine work but leaves them responsible for rare, poorly rehearsed failures—the moments when their situational awareness and manual skill are weakest.

**Canonical anchor:** Lisanne Bainbridge, [“Ironies of Automation”](https://www.sciencedirect.com/science/article/pii/0005109883900468/pdf), *Automatica* 19(6), 1983.

**Sentence pattern:** “A fleet is unhealthy when Sean cannot reconstruct, override, or safely resume its behavior—even if every scheduled job is green.”

**What this unlocks:** A concrete **operator-readiness runbook and game-day demo**: inject stale credentials, partial writes, poisoned manifests, and unavailable models; then measure time-to-diagnosis, override clarity, and recovery confidence. This turns the concept from machine uptime reporting into an argument about whether one human can still govern 7 autonomous agents under surprise.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
