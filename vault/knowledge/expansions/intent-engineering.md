---
title: "How to make `Intent Engineering` better"
type: expansion
parent: "[[intent-engineering]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-27
updated: 2026-08-27
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[intent-engineering]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add “designation–authority bundling,” not generic capability enforcement

**What to add:** Object-capability security: every tool invocation must carry the specific authority needed for that resource and purpose. Replace ambient credentials with attenuated, task-scoped, revocable capabilities. Sentence pattern: *“The agent can act only through authorities explicitly passed into this task; naming a resource does not confer authority over it.”*

**Anchor:** Norm Hardy’s *“The Confused Deputy (or why capabilities might have been invented)”*, extended by Mark S. Miller, Ka-Ping Yee, and Jonathan Shapiro’s [*Capability Myths Demolished*](https://erights.org/talks/myths/index.html). Miller et al. make the missing mechanism explicit: capabilities bundle designation with authority and support least-authority operation.

**What this unlocks:** An executable **intent-capability compiler demo** for the MCP server: compile an Intent Charter into short-lived tool handles, run adversarial GitHub-issue payloads, and show that injected text cannot acquire Keychain, filesystem, or network authority. This turns “provable security” from rhetoric into a portfolio artifact with inspectable authority graphs and revocation tests.

## 2. Add decentralized information-flow labels and explicit declassification

**What to add:** Treat control-plane separation as only the first boundary. Data can still leak through permitted calls, logs, summaries, or derived artifacts. Attach labels such as `source=github_issue`, `integrity=untrusted`, and `readers={classifier}` to values; propagate them through transformations; require a named declassification rule before crossing into credential-bearing or outbound sinks. Sentence pattern: *“Permission governs actions; information-flow policy governs what influenced those actions and where derived data may travel.”*

**Anchor:** Andrew C. Myers and Barbara Liskov’s [*A Decentralized Model for Information Flow Control*](https://www.cs.cornell.edu/andru/papers/iflow-sosp97/paper.html), which specifies per-principal labels, controlled declassification, and static checking for systems containing mutually distrustful code.

**What this unlocks:** A **taint-propagation agent spec**, a flow-policy DSL extension for `intent-engineering`, and an adversarial eval suite covering indirect exfiltration. It also forces the concept to replace its unjustified “provable security boundary” claim with named properties: noninterference, permitted declassification, provenance preservation, and sink rejection.

## 3. Add “intent uncertainty” as a contradiction to intent compilation

**What to add:** The article assumes the Intent Charter is correct and complete. Add a corrigibility mode in which intent is a revisable belief, not immutable policy: represent confidence, observe human corrections, preserve shutdown/escalation channels, and reduce autonomy when objective uncertainty or irreversible impact rises. Sentence pattern: *“Constraints may be hard; objectives remain uncertain and corrigible.”*

**Anchor:** Dylan Hadfield-Menell, Anca Dragan, Pieter Abbeel, and Stuart Russell’s [*The Off-Switch Game*](https://mlanthology.org/ijcai/2017/hadfieldmenell2017ijcai-off/). Its central result is that uncertainty about the objective can create an incentive to preserve human intervention, whereas treating the objective as settled can create resistance to correction.

**What this unlocks:** A **corrigible Intent Charter schema** containing confidence, reversibility, evidence thresholds, challenge procedures, and authority-decay rules—plus a Substack essay arguing that “what to want” cannot simply be compiled because legitimate intent changes during execution.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
