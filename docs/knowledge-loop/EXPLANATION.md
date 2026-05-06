---
artifact: knowledge-loop-phase-6
created: 2026-05-06
ai-context: "Comprehension artifact for the Phase 6 knowledge loop (producer + consumer side, spans Phases A–D). 4-question template per Nate B Jones / ADR convention. Source: claude-nate-prompt-2-analysis.md §2e verbatim."
---

# Knowledge-Loop Phase 6 — Explanation

## What is this?

A closed loop that turns Claude Code session transcripts into a queryable knowledge graph the LLM maintains. Producer side: SessionEnd hook flushes decisions/lessons/quotes from each session into the daily note; nightly synthesizer reads new daily notes and writes concept + connection articles; weekly knowledge-lint scans for orphans, broken wikilinks, and SOUL-conflicts. Consumer side: SessionStart hook injects `vault/knowledge/index.md` as `additionalContext` so every new session opens with the synthesized graph pre-loaded; `query.py` runs terminal Q&A with two-pass orchestration (article-selection pass → answer pass); `--file-back` persists answers as a third article tier with chunk-id provenance.

## Why this approach?

The pile of session transcripts was accumulating value I couldn't access. Three options: (a) just dump transcripts into the vault and grep — works at small scale, doesn't compound; (b) buy a memory product like mem0 — adds a dependency, sends my data out, can't lint or synthesize; (c) build a producer/consumer loop where every session both *writes* to the graph (flush + synthesizer) and *reads* from it (SessionStart injection + query.py). Chose (c) because the LLM becomes its own librarian — concept articles are written by the LLM, indexed by the LLM, and consumed by the next LLM session.

## What would break?

(1) The synthesizer runs on Qwen3-14B on the MBP, which is asleep most nights — Phase D was a partial mitigation (typed edges populate during whatever runs do happen) but the consumer side reads stale data on dry days. (2) The dedupe between LLM-found and SQL-found contradictions normalizes by `frozenset` — if the synthesizer ever emits asymmetric directional relations, dedupe collapses them incorrectly. (3) Index injection adds tokens to every session start; index growth is unbounded.

## What did I learn?

That Claude is happy to be its own RAG layer if you give it the schema. The consumer-side `additionalContext` injection was a four-line settings.json change but unlocks the entire compounding effect — without it, the synthesizer is writing to a graveyard.

---

## Where the code lives

- **Producer side:**
  - SessionEnd hook: [`.claude/hooks/session-end-flush.sh`](../../.claude/hooks/session-end-flush.sh)
  - PreCompact safety net (Phase A, v3.18.0): [`.claude/hooks/pre-compact-flush.sh`](../../.claude/hooks/pre-compact-flush.sh)
  - Flush agent: [`agents-sdk/agents/flush.py`](../../agents-sdk/agents/flush.py)
  - Vault Indexer (2:00 AM daily): [`agents-sdk/agents/vault_indexer.py`](../../agents-sdk/agents/vault_indexer.py)
  - Vault Synthesizer (2:30 AM daily): [`agents-sdk/agents/vault_synthesizer.py`](../../agents-sdk/agents/vault_synthesizer.py)
  - Knowledge Lint (Sunday 22:00): [`agents-sdk/agents/knowledge_lint.py`](../../agents-sdk/agents/knowledge_lint.py)
- **Consumer side:**
  - SessionStart injection (Phase B, 2026-04-25): [`.claude/hooks/session-start-inject-index.sh`](../../.claude/hooks/session-start-inject-index.sh)
  - Q&A script (Phase C, v3.19.0): [`agents-sdk/scripts/query.py`](../../agents-sdk/scripts/query.py)
  - Q&A persistence: `vault/knowledge/qa/<slug>.md` + append-only manifest at `vault/knowledge/qa/.manifest.json`
- **Typed reasoning edges** (Phase D, v3.20.0): see [the Phase D EXPLANATION](../phase-d-typed-edges/EXPLANATION.md) for the cumulative-reasoning layer.

## Phase history

- **Phase 6 producer (v3.14.3, 2026-04):** SessionEnd flush → Vault Synthesizer v2 → Knowledge Lint
- **Phase B consumer read-side (2026-04-25):** SessionStart `additionalContext` injection
- **Phase C terminal Q&A (v3.19.0, 2026-05-01):** `query.py` two-pass orchestration + qa/ tier with chunk-id provenance
- **Phase D typed edges (v3.20.0, 2026-05-01):** `concept_edges` SQL fast path
- **Phase A PreCompact safety net (v3.18.0, 2026-05-01):** flush before auto-compact
- **D.4 autoresearch feedback:** descoped pending upstream autoresearch-harness stability

## Source

§2e verbatim from the [unified roadmap's source synthesis](../../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/reference-synthesis-docs/claude-nate-prompt-2-analysis.md). Frontmatter follows [the 4Q EXPLANATION template](../../vault/40_knowledge/templates/EXPLANATION-template.md).
