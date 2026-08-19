---
title: "How to make `Fault → Error → Failure Taxonomy` better"
type: expansion
parent: "[[fault-error-failure-taxonomy]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-19
updated: 2026-08-19
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[fault-error-failure-taxonomy]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “recursive impairment-chain mode,” not merely three labels.** Anchor it in Algirdas Avižienis, Jean-Claude Laprie, Brian Randell, and Carl Landwehr’s [“Basic Concepts and Taxonomy of Dependable and Secure Computing”](https://drum.lib.umd.edu/items/6b297ffc-373b-404f-be3a-70cc849e21fd). Their model includes fault activation, dormant versus active faults, error latency, error propagation, and a crucial recursion: one component’s failure becomes a fault in the containing system. Also correct the current claim that failure exists only when a consumer detects it: failure is a service-boundary deviation; detection is a separate epistemic event. Sentence pattern: **“Fault F activated under condition A, corrupted state E after latency L, crossed boundary B as failure X, then entered consumer C as a new fault.”** This unlocks a typed incident-manifest schema and causal fleet timeline capable of explaining how `wol-deferred` propagates—or fails to propagate—into a missed daily note.

2. **Add “failure-detector epistemology” anchored on suspicion, completeness, and accuracy.** Use Tushar Deepak Chandra and Sam Toueg’s [“Unreliable Failure Detectors for Reliable Distributed Systems”](https://www.cs.princeton.edu/courses/archive/fall07/cos518/papers/unreliable.pdf). In an asynchronous system, a monitor generally cannot distinguish a crashed process from a slow process; its output is suspicion, not truth. Their completeness/accuracy vocabulary directly contradicts a dashboard that turns absence of evidence into a categorical health state. Sentence pattern: **“Detector D suspected agent A at T; the observation was complete/incomplete and accurate/inaccurate under timeout assumption S.”** This unlocks a failure-detector contract for the meta-agent, including states such as `suspected`, `confirmed`, `deferred`, and `unknown`; measurable false-positive/false-negative rates; and an explicit decision table for retrying, escalating, or preserving queued work.

3. **Add “recovery-performance mode” to counter the taxonomy’s forensic bias.** Anchor it in David Patterson et al.’s [“Recovery Oriented Computing: Motivation, Definition, Techniques, and Case Studies”](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2002/5574.html), supplemented by George Candea et al.’s [“Microreboot—A Technique for Cheap Recovery”](https://arxiv.org/abs/cs/0406005). ROC treats faults and operator mistakes as inevitable and optimizes mean time to repair rather than merely cataloguing causes; microreboots make recovery granular enough to test. Sentence pattern: **“When failure class X appears, restore component Y from checkpoint Z within R seconds while preserving invariant I.”** This unlocks executable recovery drills, a fleet runbook organized by bounded repair actions, and a strong portfolio demo: inject sleeping-host, corrupted-index, and partial-output faults, then publish measured detection and recovery curves.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
