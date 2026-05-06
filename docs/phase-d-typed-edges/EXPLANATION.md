---
artifact: phase-d-typed-reasoning-edges
created: 2026-05-06
ai-context: "Comprehension artifact for Phase D typed reasoning edges (Superuser Pack v3.20.0). 4-question template per Nate B Jones / ADR convention. Source: claude-nate-prompt-2-analysis.md §2a verbatim."
---

# Phase D — Typed Reasoning Edges — Explanation

## What is this?

A `concept_edges` SQLite table layered on top of the vault's existing chunk index. Six relation types (`supports`, `contradicts`, `evolved_into`, `supersedes`, `depends_on`, `related_to`) populated by the nightly synthesizer as a side effect of writing connection articles, and read by the weekly knowledge-lint pass for zero-LLM-cost contradiction detection.

## Why this approach?

Three options on the table: (a) keep contradiction detection as a pure LLM scan every Sunday — works but wastes tokens re-discovering known contradictions every week; (b) move to a graph DB like Neo4j — overkill for a single-user vault, adds operational surface; (c) extend the existing SQLite index with a typed-edge table and let the synthesizer write to it as it works. Chose (c) because it kept the local-first / zero-cloud constraint, added one table to a DB that already exists, and made the LLM's reasoning cumulative instead of repeated. Taxonomy is borrowed deliberately from Nate B Jones's OB1 `thought_edges` schema — interoperable if I ever federate the vault with someone else's.

## What would break?

Three failure modes. (1) If the synthesizer's LLM emits relation values outside the allowed set, the helper raises `ValueError` and the connection article writes anyway — graceful, but the edge is lost. (2) The dedupe key is `frozenset({from_slug, to_slug})`, which means LLM and SQL contradictions sharing a pair collapse correctly but bidirectional edges with different relations don't. (3) `valid_until IS NULL` partial-index assumes a future invalidation pass — the `decay_pass()` is currently stubbed.

## What did I learn?

That OB1's typed-reasoning-edges schema is the right layer of abstraction for personal knowledge graphs — concepts are nodes, relations are edges, time is a column. Also learned that LLM outputs are wildly more reliable when you give them an OPTIONAL field rather than a required one — making `relations` optional in the prompt schema kept the article-writing path unbroken even when the synthesizer didn't feel confident enough to declare a relation type.

---

## Where the code lives

- Implementation: [`agents-sdk/lib/concept_edges.py`](../../agents-sdk/lib/concept_edges.py) (helper module, schema enforcement)
- Schema: `concept_edges` table in `vault/.vault-index.db` (created idempotently by `vault_indexer.init_db()`)
- Producer: [`agents-sdk/agents/vault_synthesizer.py`](../../agents-sdk/agents/vault_synthesizer.py) (writes edges as a side effect of connection articles)
- Consumer: [`agents-sdk/agents/knowledge_lint.py`](../../agents-sdk/agents/knowledge_lint.py) Tier 2 SQL fast path (reads edges for contradiction detection)
- Manifest: `vault/health/synth-manifest-{date}.json` per-run counts (concepts, connections, edges, rejected, duration)

## Source

§2a verbatim from the [unified roadmap's source synthesis](../../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/reference-synthesis-docs/claude-nate-prompt-2-analysis.md). Frontmatter follows [the 4Q EXPLANATION template](../../vault/40_knowledge/templates/EXPLANATION-template.md).
