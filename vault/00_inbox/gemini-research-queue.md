---
type: research-queue
description: Questions for Gemini Deep Research. Tier markers indicate which model to use. Agent picks the first unchecked item, calls the Interactions API, writes a topical note to vault/20_projects/research/, injects a digest into today's daily note, and marks done with timestamp + output link.
---

# Gemini Deep Research Queue

Drop research questions here as `- [ ] {tier} {refined question}`.

**Tier markers:**
- `dr` — Deep Research (~$2–4/query, ~20-30 min): standard iterative web research
- `max` — Deep Research Max (~$5–10/query, ~30-60 min): extended synthesis, more sources, higher quality

The `gemini-dr` script (Phase 2 skill + Phase 3 agent) reads this queue,
calls Gemini's Interactions API in background mode, polls until completion,
and writes the full report to `vault/20_projects/research/`.

Budget caps from `agents-sdk/config.toml [gemini.budget]`:
- Per-task: $7.00 max
- Daily: $10.00
- Monthly: $20.00

## Pending

## Done
