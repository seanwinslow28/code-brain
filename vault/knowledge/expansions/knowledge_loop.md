---
title: "How to make `knowledge_loop` better"
type: expansion
parent: "[[knowledge_loop]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-15
updated: 2026-08-15
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[knowledge_loop]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Add a **double-loop learning gate**

**What:** The architecture is currently a circulation loop, not necessarily a learning loop. It improves and reinjects knowledge, but nothing described tests whether the vault’s governing assumptions, agent policies, or synthesis criteria should change. Add a periodic rule: *“When outcomes repeatedly contradict an assumption, revise the rule that produced it—not merely the concept article.”*

**Anchor:** Chris Argyris, [“Double Loop Learning in Organizations”](https://hbr.org/1977/09/double-loop-learning-in-organizations). Argyris distinguishes correcting errors within existing rules from questioning the rules themselves.

**Unlock:** An executable **Knowledge Loop Review** runbook: select three decisions influenced by injected knowledge, compare predicted versus observed outcomes, and propose changes to prompts, routing rules, or ontology. This would also support a strong Substack argument: *“Your second brain is not learning if it cannot change its theory of you.”*

### 2. Add **truth maintenance**, not merely contradiction detection

**What:** `concept_edges` can say that two concepts contradict, but the loop has no explicit mechanism for determining which downstream beliefs become unsupported when one premise is superseded. Add justification records—`belief → supporting sources/assumptions`—plus dependency-directed invalidation and statuses such as `believed`, `contested`, `out`, and `unsupported`.

**Anchor:** Jon Doyle, [“A Truth Maintenance System”](https://www.sciencedirect.com/science/article/abs/pii/0004370279900080) (1979). Doyle’s key move is recording *reasons for beliefs* so a system can retract conclusions when their assumptions fail, rather than accumulating mutually inconsistent statements forever.

**Unlock:** A portfolio-grade **belief-revision demo**: change one source assumption, visualize every affected concept, and require revalidation before those concepts can be injected. It also yields an agent specification for “epistemic garbage collection”—something the present producer pipeline cannot express.

### 3. Add a **counterfactual retrieval evaluation** against automatic index injection

**What:** Challenge the claim that loading the index into every session creates compounding. Persistent global context can cause anchoring, suppress novelty, and bury relevant evidence. Add an A/B/C harness: no vault context versus full index versus task-conditioned retrieval. Shuffle evidence positions and include a deliberately contradicting document; score factual accuracy, source use, novelty, and resistance to stale beliefs.

**Anchor:** Nelson F. Liu et al., [“Lost in the Middle: How Language Models Use Long Contexts”](https://arxiv.org/abs/2307.03172). Their experiments show that relevant information can become substantially less usable depending on where it appears inside long context.

**Unlock:** A publishable **evaluation report and executable benchmark** establishing whether SessionStart injection helps, harms, or merely creates the feeling of continuity. It would turn “compounding knowledge” from an architectural story into a falsifiable product claim—and provide evidence for replacing universal preload with query-conditioned context assembly if the results demand it.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
