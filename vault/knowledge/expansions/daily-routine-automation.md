---
title: "How to make `Daily Routine Automation` better"
type: expansion
parent: "[[daily-routine-automation]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-04
updated: 2026-06-04
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[daily-routine-automation]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “exception handling as the real routine” mode.**  
   Anchor it on Lucy Suchman, *Plans and Situated Actions: The Problem of Human-Machine Communication*.

   Current concept treats routine automation as repeating known tasks reliably. That misses Suchman’s core contradiction: plans do not determine action; they are resources people improvise from when the world misbehaves.

   Add a facet like: “A daily routine agent is not mature because it executes the happy path. It is mature when it recognizes breakdowns, preserves context, and offers recoverable next moves.”

   This unlocks a stronger **agent reliability runbook**: not “my morning agent creates a note,” but “my morning agent handles missing calendar OAuth, stale job feeds, unavailable MBP inference, and partial overnight critic output without corrupting the day.” It also gives Sean a sharper Substack essay: **routine automation fails when it automates the plan instead of the recovery surface**.

2. **Add “habit loop instrumentation” instead of task automation.**  
   Anchor it on Wendy Wood, *Good Habits, Bad Habits*, plus B.J. Fogg, *Tiny Habits*.

   The missing facet is behavioral scaffolding. “Automated email sorting” and “routine task scheduling” are weak examples because they describe task throughput, not habit formation. Wood/Fogg would push the concept toward cue, friction, reward, environment design, and tiny repeatable actions.

   Add a pattern like: “Daily routine automation should instrument the cue-action-reward loop, not merely complete chores. The agent should make the desired behavior easier to start, harder to forget, and visible enough to reinforce.”

   This unlocks a **life-systems agent spec** Sean cannot currently write from this concept: a daily-driver that does not just generate tasks, but shapes behavior around job hunting, writing cadence, health logging, and portfolio shipping. It also gives him interview-ready language for AI-PM roles: agents as **behavioral product surfaces**, not background scripts.

3. **Add “normalization of deviance” as the anti-pattern.**  
   Anchor it on Diane Vaughan, *The Challenger Launch Decision*.

   The concept currently implies consistency is good by default. Vaughan gives Sean the missing critique: repeated successful operation can hide drift. Small failures become accepted as normal until the system’s operating envelope has quietly changed.

   Add a named failure mode: “Routine automation can launder abnormal conditions into normal process. If the daily note is late, the critic is partial, the index is stale, or the local model route silently falls back, the routine may keep producing reassuring artifacts while system truth decays.”

   This unlocks a much stronger **Agent Fleet Observability artifact**: not just health checks, but “deviance budget,” drift ledger, and escalation thresholds. It would let Sean produce a portfolio one-pager titled something like **I built a personal agent fleet, then designed the controls that prevent it from lying to me politely**.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
