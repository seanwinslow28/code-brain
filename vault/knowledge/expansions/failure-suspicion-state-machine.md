---
title: "How to make `Failure Suspicion State Machine` better"
type: expansion
parent: "[[failure-suspicion-state-machine]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-20
updated: 2026-08-20
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[failure-suspicion-state-machine]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Replace “confirmed failure” with detector guarantees: completeness × accuracy.** The current terminal state quietly restores the certainty the concept warns against. Add Chandra–Toueg failure-detector classes, anchored on Tushar Chandra and Sam Toueg’s [“Unreliable Failure Detectors for Reliable Distributed Systems”](https://research.google/pubs/unreliable-failure-detectors-for-reliable-distributed-systems/). Their key separation is between *completeness*—actual failures are eventually suspected—and *accuracy*—healthy processes avoid suspicion. Sentence pattern: “The detector observed X; under guarantee Y, the controller may infer Z.” Reserve `confirmed_failed` for positive evidence such as an exit record or process tombstone; otherwise use `failure_actionable_under_policy`.

   **Unlocks:** an intent-engineering agent spec defining acceptable false-positive/false-negative tradeoffs per agent, plus an ADR explaining why a recovery action is justified without claiming unknowable ground truth. It also gives Sean a sharper Substack thesis: reliable systems can be built from deliberately unreliable judgments.

2. **Replace the single suspicion state with an accrual suspicion score.** Add `suspicion_score`, `threshold_policy`, and `baseline_window`, anchored on Naohiro Hayashibara, Xavier Défago, Rami Yared, and Takuya Katayama’s [“The φ Accrual Failure Detector”](http://hdl.handle.net/10119/4784). φ reports continuously increasing evidence derived from the observed heartbeat-arrival distribution; each consumer chooses its own intervention threshold. Sentence pattern: “At φ≥2 annotate; φ≥5 request corroboration; φ≥8 recover—unless the schedule policy explains the delay.”

   **Unlocks:** an executable SQLite/Python demo replaying launchd history and comparing fixed deadlines against learned per-agent lateness distributions. It also produces a real operator runbook: cheap actions at low suspicion, reversible actions at medium suspicion, destructive recovery only at high suspicion. The present state machine cannot express that proportionality.

3. **Model the observer as a failure source, not an oracle.** Add `observer_health`, `evidence_provenance`, and `independent_corroboration`, anchored on Armon Dadgar, James Phillips, and Jon Currey’s [“Lifeguard: Local Health Awareness for More Accurate Failure Detection”](https://arxiv.org/abs/1707.00788). Lifeguard’s contradiction is crucial: apparent target failure may actually be a slow or unhealthy detector. Sentence pattern: “Before escalating suspicion of agent A, test whether scheduler, host, ledger writer, and monitor are themselves timely; discount evidence from impaired observers.”

   **Unlocks:** a chaos-test runbook that separately injects agent crash, host sleep, ledger-write failure, and delayed monitoring; plus an observability-dashboard evidence card showing *who suspected whom, from which signal, while in what health state*. That turns the concept from a target-status taxonomy into a diagnosable fleet-control mechanism.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
