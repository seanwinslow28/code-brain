---
title: "How to make `Agent Accountability and System Constraints` better"
type: expansion
parent: "[[agent-accountability-and-system-constraints]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-31
updated: 2026-08-31
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-accountability-and-system-constraints]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Capability-Confinement Mode”: constraints must remove authority, not merely describe forbidden behavior.** Anchor it in Mark S. Miller’s dissertation, [*Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control*](https://jscholarship.library.jhu.edu/bitstreams/c2c3ea50-2613-47a7-b33c-9383c706ee63/download). Miller’s object-capability model replaces ambient access with narrow, delegable capabilities: an agent that never receives the private-vault capability cannot leak private notes, regardless of prompt failure. Sentence pattern: **“Agent A may perform action B on resource C until condition D; it possesses no reference to E.”** This would unlock an **executable intent-engineering demo**: compile an Intent Charter into per-agent capability grants, then show a compromised critic failing to read or export job-hunt material. It also gives Sean a sharp Substack thesis: *prompt prohibitions are documentation; withheld authority is security.*

2. **Add “Runtime-Assurance Mode”: monitoring should transfer control before damage, not report failure afterward.** Use Seto, Krogh, Sha, and Chutinan’s [*The Simplex Architecture for Safe On-Line Control System Upgrades*](https://experts.illinois.edu/en/publications/the-simplex-architecture-for-safe-on-line-control-system-upgrades/) and Lui Sha’s *Using Simplicity to Control Complexity*. Simplex separates an ambitious, unverified controller from a minimal safe controller; a decision module switches authority when safety boundaries are approached. Translate that directly: generative agent → deterministic safety kernel → read-only fallback/quarantine. Sentence pattern: **“When invariant X approaches threshold Y, revoke Agent A’s write capability and route the task to baseline procedure B.”** This unlocks a **fleet containment runbook and replayable failure demo**—for example, a vault agent attempting a private-to-public write, getting intercepted, downgraded, and leaving a recovery baton. The current concept can describe health; Simplex lets Sean specify intervention.

3. **Add “Contestability Mode”: logs create evidence, but accountability requires a forum, a standard, and a remedy.** Anchor it in Kroll, Huey, Barocas, Felten, Reidenberg, Robinson, and Yu’s [*Accountable Algorithms*](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2765268). Their key contradiction is that transparency alone does not produce accountability; systems need prior specifications and mechanisms that can verify compliance afterward. Sentence pattern: **“Decision D was authorized under rule R using evidence E; reviewer H can overturn it through remedy M.”** This unlocks an **agent decision record and incident-appeal artifact**, not another observability dashboard: signed intent version, capability snapshot, decision trace, affected resource, accountable human, reversal procedure, and proof of remediation. For Sean’s portfolio, that becomes a governance one-pager demonstrating not merely that his fleet is observable, but that its consequential actions are reviewable and reversible.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
