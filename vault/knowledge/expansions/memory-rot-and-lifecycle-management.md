---
title: "How to make `Memory Rot and Lifecycle Management` better"
type: expansion
parent: "[[memory-rot-and-lifecycle-management]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-28
updated: 2026-08-28
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[memory-rot-and-lifecycle-management]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Add “justification-based retirement,” not age-based decay

**What to add:** Model each memory as a belief with dependencies: `claim → supporting observations → applicable conditions`. When evidence changes, mark the claim `out`, `superseded`, or `contested`; do not assume old means rotten.

**Anchor:** Jon Doyle’s [“A Truth Maintenance System”](https://www.sciencedirect.com/science/article/pii/0004370279900080) (1979). Doyle’s key move is maintaining the reasons beliefs are held so contradictions can retract conclusions without indiscriminately deleting history.

**What this unlocks:** An executable **belief-revision agent spec** for Knowledge Lint: detect invalidated premises, traverse `supports` edges, and open targeted reconciliation tickets. It also gives Sean a strong Substack argument: **“Your Second Brain Doesn’t Need Pruning; It Needs Reasons.”** The current concept can only say “remove stale material”; it cannot decide *which conclusions became invalid and why*.

### 2. Replace “ruthless pruning” with an event-sourced memory lifecycle

**What to add:** Separate the canonical read model from the historical record. Use lifecycle events such as `asserted`, `challenged`, `superseded`, `merged`, and `retired`; retrieval sees the current projection, while audits retain the append-only history.

**Anchor:** Martin Fowler’s [“Event Sourcing”](https://www.martinfowler.com/eaaDev/EventSourcing.html), especially complete rebuild, temporal query, and event replay. This directly contradicts the article’s deletion-first framing: obsolete state should disappear from the active view without destroying the evidence needed to reconstruct past decisions.

**What this unlocks:** A **memory-migration runbook and portfolio demo**: replay six months of vault events under a new taste policy, compare the resulting active graph, then roll back. It also enables “What did the fleet believe on June 1?”—a governance question the current concept cannot answer after pruning.

### 3. Add a causal test for “rot” before treating rejection counts as evidence

**What to add:** Define memory rot operationally as a measured decline in task performance caused by retained artifacts. Build a fixed query suite and run ablations across memory age, retrieval rank, context position, and lifecycle state. Track context precision/recall and answer faithfulness—not raw rejection volume. A 106-rejection run may indicate an effective gate, poor candidate generation, or positional neglect; it does not establish rot.

**Anchor:** Shahul Es et al.’s [“RAGAS: Automated Evaluation of Retrieval Augmented Generation”](https://aclanthology.org/2024.eacl-demo.16.pdf) separates retrieval relevance from generation faithfulness. Pair it with Liu et al.’s [“Lost in the Middle”](https://arxiv.org/abs/2307.03172), which shows that relevant evidence can be ignored because of prompt position rather than semantic age.

**What this unlocks:** A reproducible **Memory Rot Benchmark** for Code-Brain: baseline, prune, rerank, and position-shuffle treatments with regression thresholds. That becomes both a portfolio one-pager and an executable counterfactual: **“Does deletion improve answers, or merely shorten prompts?”**

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
