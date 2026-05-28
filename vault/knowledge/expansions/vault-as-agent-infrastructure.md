---
title: "How to make `Vault as Agent Infrastructure` better"
type: expansion
parent: "[[vault-as-agent-infrastructure]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-28
updated: 2026-05-28
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[vault-as-agent-infrastructure]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “versioned memory as event log,” anchored on Martin Kleppmann’s _Designing Data-Intensive Applications_**

   Add the facet that a vault used by agents should not only store “current beliefs”; it should preserve **append-only belief history**: what changed, when, why, from which run, with which confidence, and what downstream action depended on it.

   Exemplary work: Martin Kleppmann, _Designing Data-Intensive Applications_, especially the chapters on logs, event sourcing, stream processing, and derived data.

   Sentence pattern to add: “A vault-backed agent fleet should treat markdown notes as projections, not the source of truth; the durable substrate is the event history of observations, edits, critiques, failures, and promotions.”

   This unlocks a concrete artifact Sean does not yet have: a **Vault Memory Event Schema** or **agent-memory migration plan**. It would let him decide whether fleet memory belongs in Markdown, SQLite, JSONL manifests, or an append-only log, instead of treating “vault” and “memory” as the same object.

2. **Add “organizational forgetting / transactive memory,” anchored on Daniel Wegner’s paper “Transactive Memory: A Contemporary Analysis of the Group Mind”**

   The concept currently frames the missing problem as retrieval and temporal reasoning. That is too technical. A fleet also needs to know **who knows what**, **which agent owns which kind of memory**, and **when shared memory becomes coordination debt**.

   Exemplary work: Daniel M. Wegner, “Transactive Memory: A Contemporary Analysis of the Group Mind,” in _Theories of Group Behavior_.

   Sentence pattern to add: “The vault is not just long-term memory; it is the fleet’s transactive memory system, where the hard problem is not recall but assignment, trust, and handoff.”

   This unlocks a stronger **agent-fleet operating model**: memory ownership tables, promotion rules, stale-knowledge audits, and “who should remember this?” stop rules. It would also sharpen Sean’s portfolio language, because “I built RAG over Obsidian” sounds common, while “I designed a transactive memory system for scheduled agents” sounds like agentic-engineering IC signal.

3. **Add “boundary objects,” anchored on Susan Leigh Star and James Griesemer’s paper “Institutional Ecology, ‘Translations’ and Boundary Objects”**

   The current concept assumes the vault’s job is to help agents reason better. Missing facet: the vault also mediates between **Sean-as-PM**, **Sean-as-engineer**, **autonomous agents**, **future collaborators**, and **hiring audiences**. The same note must be legible across communities with different standards of proof.

   Exemplary work: Susan Leigh Star and James R. Griesemer, “Institutional Ecology, ‘Translations’ and Boundary Objects: Amateurs and Professionals in Berkeley’s Museum of Vertebrate Zoology.”

   Sentence pattern to add: “A concept note becomes infrastructure when it acts as a boundary object: plastic enough for agents, PM artifacts, and essays to use differently, but structured enough to preserve identity across those uses.”

   This unlocks a publishable **Substack essay / portfolio one-pager**: “My Obsidian Vault Is a Boundary Object for an Agent Fleet.” It gives Sean a better frame than “personal knowledge base plus agents,” and explains why his vault supports PRDs, agent specs, critique loops, job-search artifacts, and autonomous nightly synthesis without collapsing into a private notebook.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
