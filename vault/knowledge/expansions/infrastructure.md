---
title: "How to make `Infrastructure` better"
type: expansion
parent: "[[infrastructure]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-16
updated: 2026-08-16
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[infrastructure]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add “serviceability, not machine status”

**What to add:** Replace the binary `ONLINE/OFFLINE` model with black-box service checks, white-box diagnostics, and the four golden signals: latency, traffic, errors, and saturation. The crucial contradiction is: **a reachable machine is not necessarily delivering useful work, while an offline optional node may not impair the system at all.**

**Anchor:** Rob Ewaschuk’s chapter [“Monitoring Distributed Systems” in Google’s *Site Reliability Engineering*](https://sre.google/sre-book/monitoring-distributed-systems/), especially its symptom-versus-cause and black-box-versus-white-box distinctions.

**What this unlocks:** A **Fleet Serviceability Contract** defining user-visible capabilities—“nightly synthesis completes before 08:00,” “sprite QA returns within five minutes”—with SLIs, SLOs, dependency probes, and degradation rules. This produces a portfolio-grade reliability one-pager and an executable probe suite; the current concept can only produce a device inventory.

## 2. Add “capability-aware scheduling”

**What to add:** Model each machine as a pool of schedulable capabilities rather than a named endpoint. Jobs declare resources, latency class, placement constraints, fallback policy, and whether interruption is acceptable. Sentence pattern: **“Task T requires capability C under constraint K; node N is merely one eligible placement.”**

**Anchor:** Abhishek Verma et al., [“Large-scale Cluster Management at Google with Borg”](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)—specifically declarative job specifications, admission control, heterogeneous workloads, task packing, and policies that reduce correlated failure.

**What this unlocks:** A **local-agent scheduler specification and executable demo** that decides whether a workload belongs on the always-on Mini, awake-only MacBook, manual-wake Alienware, or nowhere. It would force explicit decisions about queueing, preemption, affinity, retry budgets, and `fallback = none`. That is a much stronger agentic-engineering artifact than “Alienware is offline.”

## 3. Add “reproducible infrastructure closure”

**What to add:** Treat infrastructure as the complete, immutable closure of inputs required to reproduce an execution: model digest, quantization, runtime, CUDA/PyTorch versions, prompts, adapters, configuration, credentials interface, and machine constraints. Contradict the article’s hardware-centric definition with: **infrastructure is not where a run happened; it is what must be reconstructed for the run to happen again.**

**Anchor:** Eelco Dolstra, [*The Purely Functional Software Deployment Model*](https://dspace.library.uu.nl/bitstream/handle/1874/7540/?sequence=7), the foundational Nix thesis on isolated components, complete dependency closures, atomic upgrades, and rollback.

**What this unlocks:** A **Reproducible Agent Run Manifest** plus cold-machine recovery runbook: given a run ID, rebuild its environment, verify model and configuration hashes, replay it, and roll back safely. That supports a sharp Substack essay—“Your Agent Fleet Is Not Infrastructure Until You Can Reconstitute It”—and demonstrates operational maturity the current status-note concept cannot express.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
