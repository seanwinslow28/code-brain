---
title: "How to make `Dominant Resource Fairness` better"
type: expansion
parent: "[[dominant-resource-fairness]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-20
updated: 2026-08-20
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[dominant-resource-fairness]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Add an “axioms, not vibes” contract for fairness

**What to add:** Define DRF through four testable properties: **sharing incentive, strategy-proofness, envy-freeness, and Pareto efficiency**. Queue aging and minimum guarantees are separate policy extensions; they are not evidence that an allocator implements DRF.

**Anchor:** Ali Ghodsi et al., [“Dominant Resource Fairness: Fair Allocation of Multiple Resource Types”](https://people.csail.mit.edu/matei/papers/2011/nsdi_drf.pdf). Those four properties are the paper’s substantive contribution, yet the concept omits all of them.

**What this unlocks:** An executable **Fairness Policy RFC + property-test suite**. Sean could feed synthetic fleet states into candidate allocators and test assertions such as:

- A workload cannot gain by exaggerating its RAM requirement.
- No class prefers another class’s allocation.
- Adding capacity cannot reduce an existing allocation.
- Every class beats an equal static partition.

That turns “fair” from an architectural adjective into falsifiable governance—the kind of agentic-engineering portfolio artifact the current summary cannot produce.

### 2. Add “finish-time fairness” as a contradiction to dominant-share fairness

**What to add:** Model fairness over **completion slowdown**, not merely instantaneous resource shares. Sean’s LoRA runs are long, gang-like, placement-sensitive jobs; daily agents are short deadline jobs. Equal dominant shares can still leave one class waiting many times longer than it would under an isolated machine allocation.

**Anchor:** Kshiteej Mahajan et al., [“Themis: Fair and Efficient GPU Cluster Scheduling”](https://www.usenix.org/conference/nsdi20/presentation/mahajan). Themis introduces **finish-time fairness** and deliberately accepts short-term allocation inequality to achieve long-term completion fairness.

**What this unlocks:** A portfolio-grade **three-machine scheduler simulator** comparing DRFH, priority-plus-aging, and finish-time fairness across Mac Mini, MacBook, and Alienware availability traces. The decisive metric becomes normalized completion time or slowdown—not the vague “unpredictable delays” currently offered. It would also force an explicit product decision: should the fleet treat fairness as equal access, equal waiting pain, or deadline reliability?

### 3. Add a measured “price of fairness” and an efficiency-loss budget

**What to add:** Replace “balance urgent jobs against opportunistic research” with an explicit constraint: *maximize useful completed work subject to a fairness bound*, or *maximize fairness while permitting no more than X% throughput loss*. Otherwise, queue aging can eventually promote an enormous low-value job ahead of several valuable short jobs.

**Anchor:** Dimitris Bertsimas, Vivek Farias, and Nikolaos Trichakis, [“The Price of Fairness”](https://pubsonline.informs.org/doi/10.1287/opre.1100.0865). The paper formalizes fairness as having a quantifiable system-efficiency cost rather than being an unqualified good.

**What this unlocks:** A **scheduler tuning runbook and decision record** with a Pareto frontier: missed morning-agent deadlines, GPU utilization, p95 slowdown, starvation count, and useful jobs completed versus fairness level. Sean could then defend a concrete rule such as: “No workload may exceed 3× isolated completion time, provided the rule costs less than 10% weekly useful throughput.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
