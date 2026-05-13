---
artifact: knowledge-loop-phase-6
created: 2026-05-12
ai-context: "Comprehension artifact for the Phase 6 producer/consumer knowledge loop in the Superuser Pack. 4-question template per Nate B Jones / ADR convention."
related:
  - "[[flush.py]]"
  - "[[vault_indexer.py]]"
  - "[[vault_synthesizer.py]]"
  - "[[knowledge_lint.py]]"
  - "[[query.py]]"
  - "[[session-start-inject-index.sh]]"
  - "[[pre-compact-flush.sh]]"
---

# Knowledge-Loop Phase 6 (Producer + Consumer Side) — Explanation

## What is this?

A closed loop that turns Claude Code session transcripts into a queryable knowledge graph the LLM maintains. Producer side: SessionEnd hook flushes decisions/lessons/quotes from each session into the daily note; nightly synthesizer reads new daily notes and writes concept + connection articles; weekly knowledge-lint scans for orphans, broken wikilinks, and SOUL-conflicts. Consumer side: SessionStart hook injects `vault/knowledge/index.md` as `additionalContext` so every new session opens with the synthesized graph pre-loaded; `query.py` runs terminal Q&A with two-pass orchestration (article-selection pass → answer pass); `--file-back` persists answers as a third article tier with chunk-id provenance.

## Why this approach?

The pile of session transcripts was accumulating value I couldn't access. Three options: (a) just dump transcripts into the vault and grep — works at small scale, doesn't compound; (b) buy a memory product like mem0 — adds a dependency, sends my data out, can't lint or synthesize; (c) build a producer/consumer loop where every session both *writes* to the graph (flush + synthesizer) and *reads* from it (SessionStart injection + query.py). Chose (c) because the LLM becomes its own librarian — concept articles are written by the LLM, indexed by the LLM, and consumed by the next LLM session.

## What would break?

(1) The synthesizer runs on Qwen3-14B on the MBP, which is asleep most nights — Phase D was a partial mitigation (typed edges populate during whatever runs do happen) but the consumer side reads stale data on dry days. (2) The dedupe between LLM-found and SQL-found contradictions normalizes by `frozenset` — if the synthesizer ever emits asymmetric directional relations, dedupe collapses them incorrectly. (3) Index injection adds tokens to every session start; index growth is unbounded.

## What did I learn?

That Claude is happy to be its own RAG layer if you give it the schema. The consumer-side `additionalContext` injection was a four-line `settings.json` change but unlocks the entire compounding effect — without it, the synthesizer is writing to a graveyard.
