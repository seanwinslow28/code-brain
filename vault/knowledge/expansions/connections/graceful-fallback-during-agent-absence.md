---
title: "How to make `Graceful Fallback During Agent Absence` better"
type: expansion
parent: "[[graceful-fallback-during-agent-absence]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-14
updated: 2026-06-14
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[graceful-fallback-during-agent-absence]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “maintenance window semantics,” not just trip mode.**  
   Anchor it on John Allspaw’s essay/talk **“The Infinite Hows”** and the SRE idea of **error budgets** from Betsy Beyer et al., **_Site Reliability Engineering_**, especially the chapters on managing reliability as a product decision.

   Current concept treats MBP absence as an operational exception: “agent down, but expected.” Missing move: planned absence should consume a different budget than unplanned failure. Add a distinction like:

   > `status=planned_unavailable` is not a failed run; it is a declared maintenance window with bounded blast radius, skipped obligations, and catch-up rules.

   This unlocks a **fleet reliability runbook** or **portfolio-grade ops artifact**: “How my $0 local agent fleet handles planned compute absence.” That is stronger than “trip mode,” because it shows Sean can translate SRE practice into personal agent infrastructure.

2. **Add “degraded mode contracts.”**  
   Anchor it on Michael Nygard’s **_Release It!_**, specifically the stability patterns around **circuit breakers**, **bulkheads**, and **graceful degradation**.

   The article says fallback is needed, but it does not specify what the system is still obligated to do when the MBP is gone. Add explicit contracts per agent:

   > When heavy local compute is unavailable, `vault_synthesizer` must skip synthesis but still write a manifest; `daily_driver` must surface absence as context; `job_feed` must preserve queue freshness but avoid paid fallback; `flush` must degrade to Mini-local summarization.

   This unlocks an **agent spec** Sean currently cannot produce: a table of “normal mode / degraded mode / forbidden fallback / recovery action” for each scheduled agent. That becomes directly useful for `intent-engineering`: intent is not only what the agent wants in ideal conditions, but what it must preserve when capabilities disappear.

3. **Add “control-plane vs data-plane failure.”**  
   Anchor it on Brendan Burns, Brian Grant, David Oppenheimer, Eric Brewer, and John Wilkes, **“Borg, Omega, and Kubernetes”** / Google’s cluster-management lineage, plus Kubernetes’ explicit separation between desired state and reconciler loops.

   Right now the concept blends three things: MBP availability, agent execution, and interpretation of health. Missing distinction:

   > The control plane should know the MBP is scheduled absent; the data plane may still fail to execute work; the observability layer must not collapse those into one red failure state.

   This unlocks a **systems architecture diagram** or **Substack essay**: “My second brain needs Kubernetes-style desired state, not more cron jobs.” It also gives Sean a sharper contradiction to his current design: launchd schedules jobs, but it does not encode desired fleet state. The next artifact could be a small `fleet-state.yaml` or SQLite table with `desired_status`, `actual_status`, `reason`, `next_reconcile_at`, and `operator_note`.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
