---
title: "How to make `concept_edges` better"
type: expansion
parent: "[[concept_edges]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-15
updated: 2026-08-15
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[concept_edges]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Replace article-level edges with claim-level argument graphs

**Add:** An `argument_nodes` layer containing atomic claims, with edges typed by an argumentation scheme and accompanied by scheme-specific critical questions. `concept_A supports concept_B` is too coarse: one paragraph may support one claim while contradicting another.

**Anchor:** Douglas Walton, Christopher Reed, and Fabrizio Macagno’s *Argumentation Schemes*. Their key move is to represent defeasible reasoning patterns—expert testimony, analogy, causal inference, practical reasoning—alongside the standard questions that can defeat each pattern. [Cambridge University Press](https://www.cambridge.org/core/books/argumentation-schemes/contents/33A7DF3C6F001EC4CE9E7CC53EDE7F77)

**Concrete addition:**

```text
claim → inference_scheme → conclusion
                   ↘ critical_question
```

Store `claim_text`, `source_span`, `scheme`, `premise_ids`, and `critical_questions`, rather than treating a whole Markdown file as the unit of reasoning.

**Unlocks:** An executable **Vault Cross-Examiner** agent spec: select an important conclusion, identify its inference scheme, ask the corresponding critical questions, and produce a “strongest unresolved objection” brief. That creates genuinely adversarial Substack essays and decision memos instead of inventories of neighboring concepts.

## 2. Treat contradictions as belief-revision events, not permanent binary facts

**Add:** A justification-based Truth Maintenance System: every accepted claim records the assumptions and evidence supporting it; when an assumption changes, the system retracts only the conclusions that depend on it. A `contradicts` row plus `valid_until` records disagreement but cannot determine what the vault should now believe.

**Anchor:** Jon Doyle’s 1979 paper *A Truth Maintenance System*, which introduced recorded justifications, dependency-directed backtracking, and revision of beliefs after contradictory discoveries. [Artificial Intelligence](https://www.sciencedirect.com/science/article/abs/pii/0004370279900080)

**Concrete addition:** Introduce `justifications`, `assumptions`, and `belief_status` tables. Make the critic emit:

```text
IN because {A, B}
OUT because B was defeated by C
alternative environment: {A, not-B}
```

This directly contradicts the article’s implicit model that contradiction is merely an edge to query: contradiction should trigger a controlled state transition.

**Unlocks:** A **belief-change runbook** and executable demo showing what conclusions, agent policies, and portfolio claims must be reconsidered when a canonical reference is superseded. It would make Code-Brain demonstrate non-monotonic reasoning rather than graph storage.

## 3. Add provenance and decision-time semantics

**Add:** Evidence-bearing edges with `asserted_by`, `generated_by_run`, `source_span`, `confidence`, `observed_at`, and separate `valid_time` versus `recorded_at`. `valid_until` alone conflates “this stopped being true” with “the fleet learned later that it had stopped being true.”

**Anchor:** The W3C’s *PROV-O: The PROV Ontology*, especially `Entity`, `Activity`, `Agent`, `wasDerivedFrom`, `wasRevisionOf`, and `hadPrimarySource`. [W3C Recommendation](https://www.w3.org/TR/prov-o/)

**Concrete addition:** Model every edge assertion as its own entity, attributed to a human or agent activity and linked to quoted evidence. Preserve revisions rather than overwriting them.

**Unlocks:** A recruiter-grade **reasoning replay**: “Why did the fleet believe this on May 20, which agent introduced it, what evidence supported it, and what later changed?” That becomes a portfolio one-pager or interactive governance demo—far stronger evidence of agentic-engineering judgment than another knowledge-graph description.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
