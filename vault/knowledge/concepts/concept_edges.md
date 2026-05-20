---
title: "concept_edges"
type: concept
sources:
  - CLAUDE.md
  - agents-sdk/lib/concept_edges.py
  - agents-sdk/agents/vault_indexer.py
tags: [reference, hand-written, infrastructure]
created: 2026-05-20
updated: 2026-05-20
---

## Definition

`concept_edges` is the SQLite table in `vault/.vault-index.db` that stores typed reasoning relationships between concept articles in Sean's knowledge vault. Each row is a tuple of `(from_slug, to_slug, relation)` where `relation` is one of six allowed values: `supports`, `contradicts`, `evolved_into`, `supersedes`, `depends_on`, `related_to`. The table was added in v3.20.0 (Phase D of the knowledge loop) to promote contradiction and supersedence detection from a Sunday LLM lint scan that prose-writes findings to a report into queryable SQL rows that can be consulted at synthesis time.

## Context

The table is the data layer that lets the weekly Knowledge Lint do a SQL fast-path for contradictions (`SELECT ... WHERE relation='contradicts' AND valid_until IS NULL`) instead of re-running an LLM scan, and it lets future agents (the eventual vault-knowledge-mcp server) answer questions like "what does X support?" or "what supersedes Y?" without re-reading articles. The schema includes `valid_until` as a soft-delete column so historical contradictions stay queryable while no longer surfacing as current.

## Evidence

> Phase D promotes contradiction / supersedence detection from "Sunday LLM lint scan that prose-writes findings to a report" to "queryable SQL row at synthesis time." `vault_indexer.init_db()` gained a `concept_edges` SQLite table with six allowed relation values.

> The synthesizer parses each relation pair and `INSERT OR IGNORE`s a row inside the existing FileLock window. Bad relation values are logged and dropped via the `agents-sdk/lib/concept_edges.py` helper.

## Examples

- The 8 CRITICAL contradictions in the 2026-05-17 lint report are rows in this table flagged by the SQL fast-path.
- Closing stale contradictions is `UPDATE concept_edges SET valid_until = ? WHERE relation='contradicts' AND valid_until IS NULL`.
- The taxonomy mirrors OB1's `schemas/typed-reasoning-edges/schema.sql`, kept SQLite-local rather than a separate service.

## Related Concepts

[[knowledge_loop]]
