---
title: "knowledge_loop"
type: concept
sources:
  - CLAUDE.md
  - agents-sdk/agents/vault_synthesizer.py
  - agents-sdk/agents/knowledge_lint.py
  - .claude/hooks/session-end-flush.sh
  - .claude/hooks/session-start-inject-index.sh
tags: [reference, hand-written, infrastructure]
created: 2026-05-20
updated: 2026-05-20
---

## Definition

The `knowledge_loop` is the closed-loop architecture that keeps Sean's vault knowledge graph current. It has a producer side that ingests new material (SessionEnd flush hook → nightly Vault Synthesizer at 02:30 → weekly Knowledge Lint on Sunday at 22:00) and a consumer side that surfaces that material back into working sessions (SessionStart `inject-index.sh` hook reads `vault/knowledge/index.md` into every new Claude Code conversation, plus `agents-sdk/scripts/query.py` for ad-hoc terminal Q&A against the indexed corpus). Phase 6 shipped the producer in v3.14.3; Phase B shipped consumer SessionStart injection in v3.17.0; Phase C added query.py + the qa/ tier in v3.19.0; Phase D added the typed-edges SQL fast-path in v3.20.0.

## Context

The loop's whole point is that knowledge Sean writes once (in a daily note, a research file, a meeting note) gets distilled into reusable concept/connection articles automatically, and those articles get reinjected as context the next time he opens a session. He doesn't have to remember to search the vault — the index arrives pre-loaded. The producer/consumer split is what makes it "compounding" rather than just "indexing."

## Evidence

> Phase 6 (v3.14.3) shipped the knowledge compounding loop producer side: SessionEnd flush → Vault Synthesizer v2 → Knowledge Lint. The consumer side (autoresearch feedback, D.4) was descoped pending upstream autoresearch harness.

> The `.claude/hooks/session-start-inject-index.sh` SessionStart hook reads `vault/knowledge/index.md` and injects it as `additionalContext` on every new Claude Code session, so Claude opens each session knowing the vault's concept and connection articles before you type anything.

## Examples

- A session ends with a flush extracting Tier-A SOUL signal into the daily log; the synthesizer reads that overnight and writes a concept article; next session's SessionStart hook pre-loads the article.
- `agents-sdk/scripts/query.py` lets Sean ask a terminal question that traverses the indexed corpus and writes the answer to `vault/knowledge/qa/<slug>.md` with chunk-ID citations.
- The PreCompact safety net (v3.18.0) fires `flush.py --trigger pre-compact` before Claude Code auto-compacts a long session, closing the failure mode where pre-compact knowledge would silently vanish.

## Related Concepts

[[concept_edges]]
