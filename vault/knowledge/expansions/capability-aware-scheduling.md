---
title: "How to make `Capability-Aware Scheduling` better"
type: expansion
parent: "[[capability-aware-scheduling]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-18
updated: 2026-08-18
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[capability-aware-scheduling]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add two-sided matchmaking and a separate claim phase

**What to add:** Replace one-way “job requirements → capable node” matching with HTCondor-style **ClassAds**: both jobs and machines publish hard `Requirements` and soft `Rank` expressions. Treat a match only as a proposal; immediately revalidate availability and policy while claiming the node.

**Canonical anchor:** Rajesh Raman, Miron Livny, and Marvin Solomon, [“Matchmaking: Distributed Resource Management for High Throughput Computing”](https://htcondor.org/doc/hpdc98.pdf). Their crucial move is separating **matching from claiming**, which tolerates stale advertisements and lets resource owners express whom they will serve—not merely what they can run.

**What this unlocks:** An executable `job_ad × machine_ad → match → claim` demo for the intent-engineering MCP server. The accompanying agent spec could encode rules such as “Alienware accepts interruptible GPU work only during its manual-awake window” and “MacBook rejects batch claims during interactive use.” The current concept cannot express machine-side intent or detect a node whose advertised capability became stale before dispatch.

## 2. Add an explicit fairness and starvation policy

**What to add:** Define a **DRFH-inspired allocation policy** across workload classes—interactive, scheduled-critical, opportunistic research, and creative batch. Track each class’s dominant share of scarce resources such as GPU time, RAM, latency budget, and awake-machine hours; add queue aging and minimum service guarantees.

**Canonical anchor:** Wei Wang, Baochun Li, and Ben Liang, [“Dominant Resource Fairness in Cloud Computing Systems with Heterogeneous Servers”](https://researchportal.hkust.edu.hk/en/publications/dominant-resource-fairness-in-cloud-computing-systems-with-hetero/). DRFH extends Ghodsi et al.’s DRF specifically because pretending heterogeneous machines form one interchangeable resource pool produces poor allocations.

**What this unlocks:** A scheduler-policy RFC plus a trace-replay benchmark comparing greedy “best available” placement against DRFH-lite. Sean could demonstrate whether the Substack drafter, knowledge lint, or LoRA experiments starve after urgent jobs repeatedly seize the scarce machine. “Best available resource” currently hides this product decision inside an undefined ranking function.

## 3. Add desired-state reconciliation—not merely placement

**What to add:** Model every dispatch as a reconciled lifecycle: `Pending → Claimed → Running → Checkpointed/Succeeded/Failed`. Require claim leases, idempotency keys, retry budgets, checkpoint boundaries, and an explicit response when a node disappears mid-run. The sentence pattern should be: **“Placement is a hint; completion is a continuously reconciled obligation.”**

**Canonical anchor:** Brendan Burns, Brian Grant, David Oppenheimer, Eric Brewer, and John Wilkes, [“Borg, Omega, and Kubernetes”](https://research.google/pubs/borg-omega-and-kubernetes/)—their decade-spanning comparison makes declarative desired state and controller-driven reconciliation the durable abstraction above scheduling.

**What this unlocks:** A failure-injection demo and operator runbook: kill the MacBook route during synthesis, expire its lease, preserve the checkpoint, and prove deterministic defer/resume without duplicate output. The current article decides where work starts; it says almost nothing about who remains responsible for ensuring that work finishes.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
