---
name: deep-research-queue
description: Queue research topics into vault/00_inbox/research-queue.md for the autonomous deep_researcher agent to process overnight. Use when Sean asks to "queue research", "add to research queue", "research this later", or surfaces a question during work that needs ≥5 min of multi-source synthesis. Triggers when the question is not answerable in-session OR would consume too many tokens vs deferring to local LDR + Qwen3-14B at $0/run. Skip for simple factual lookups, code questions, or anything Sean wants answered now.
---

# Deep Research Queue

## Purpose

Defer research-worthy questions to the autonomous `deep_researcher` agent that runs nightly at 02:45 on the always-on Mac Mini. Each queued question becomes a multi-source synthesis report (≈800–1500 words, ≥3 citations) at $0/run via local LDR + Qwen3-14B + SearXNG, with the digest landing on the next morning's daily note.

This skill is the **interactive write-side** of the deep-research pipeline; it does not run research itself. It only edits the queue file. The agent does the work overnight.

## When to Queue vs Answer in Session

Use this decision tree before queuing:

| Situation | Action |
|---|---|
| Single-fact lookup ("when did X ship?", "what's Y's price?") | **Answer in session** (or use WebSearch/WebFetch directly) |
| Code or syntax question | **Answer in session** — wrong tool for LDR |
| Multi-source synthesis with ≥3 citations needed | **Queue** |
| Question with a deadline within an hour | **Answer in session** even if expensive — queue would miss the window |
| Sean explicitly says "queue" / "add to research queue" / "research this later" | **Always queue** — defer to user intent |
| Question requires reasoning over time-sensitive market data (prices, TVL, etc.) | **Don't queue** — the 02:45 fire would use stale-by-morning data; answer now or recommend a paid Perplexity/Claude.ai run |
| Question is exploratory ("what should we think about X?") | **Queue** if the answer would benefit from breadth; otherwise discuss in session |

## What Makes a Good Research-Queue Question

Good queue questions are:
- **Specific:** *"What are the practical differences between Ollama Modelfile SYSTEM prompts and runtime system messages for Qwen3?"* not *"How does Ollama work?"*
- **Falsifiable:** Has at least one cite-able answer the model + sources can converge on. Not *"Is X better than Y?"* in the absolute — frame as *"On {dimension}, how does X compare to Y for {use case}?"*
- **Time-scoped if relevant:** *"How has the LDR project's release cadence changed in the last 6 months?"* — anchors LDR's search to the right window.
- **Citation-friendly:** Topics with public web coverage (open-source tools, recent papers, vendor docs). Not deeply private/behind-paywall topics SearXNG can't reach.

Anti-patterns:
- Vague: *"Tell me about AI."* — too broad, the 14B model will produce vague generalities.
- Unanswerable: *"Predict what crypto will do next quarter."* — no model can do this honestly; the report will hallucinate confidence.
- Single-fact lookups: *"What is the population of Boston?"* — wastes 5 minutes of Mac Mini compute on something a one-shot search resolves.
- Multi-question bundles: *"Compare A and B and also explain C and recommend D."* — split into separate queue lines so each gets its own synthesis budget.

## How to Queue

1. Read `vault/00_inbox/research-queue.md` (it has a header + an existing list).
2. Refine Sean's question per the rules above (specific, falsifiable, time-scoped if relevant) — show him the refined version and confirm before adding if the refinement is non-trivial.
3. Append `- [ ] {refined question}` on a new line under the `## Pending` section. Use `Edit` (not `Write` — never overwrite the file).
4. Confirm the addition back to Sean with the exact line you appended.

**Do NOT:**
- Add timestamps, metadata, or wikilinks — the agent rewrites the line on completion with its own timestamp + backlink.
- Reorder existing items — the agent picks the FIRST unchecked, so reordering changes the next-night execution order.
- Mark items done — only the agent does that.
- Add a question that's already in the queue (check first via grep).

## What Happens After Queueing

The `deep_researcher` agent fires nightly at **02:45 on Mac Mini** (after vault-indexer 02:00 and vault-synthesizer 02:30; before meta-agent 06:30 and daily-driver morning 08:45 — zero overlap window). The agent:

1. Picks the first `- [ ]` item from `research-queue.md`.
2. Calls Local Deep Research (LDR) via REST at `localhost:5050` — LDR runs Qwen3-14B (Q4_K_M GGUF) on Ollama with `/no_think` baked into the Modelfile, search via local SearXNG container.
3. Writes a topical report at `vault/20_projects/research/{YYYY-MM-DD}-{slug}.md` (typical 800–1500 words, ≥3 citations).
4. Injects a one-line digest under `<!-- research-digest -->` in today's daily note.
5. Rewrites the queue line: `- [x] {question} — done {ts} → [[topical-note]]`.
6. Logs to `vault/90_system/agent-logs/agent-run-history.csv` with status + wall time.

If Mac Mini is asleep at 02:45 the run is missed (no make-up) — but Mac Mini is always-on per `[routing.machines.mac_mini].always_on = true`, so this should be a non-issue.

## Cost / Latency Expectation

- **Cost:** $0/run (entirely local — Ollama + SearXNG + LDR all on Mac Mini).
- **Latency:** queued tonight → digest available tomorrow morning's daily note (~03:00 typical completion).
- **Wall time per run:** 5–12 min on Mac Mini M4 Pro 24 GB. The patched `qwen3-14b-research:latest` Modelfile suppresses Qwen3 thinking mode, so generation is direct (no internal reasoning overhead).
- **Throughput:** one question per night. Backlog is fine but compounds — if Sean queues 10 questions, expect 10 nights to clear at the current rate.

## Quality Expectations (Important)

This is a **first-draft research engine**, not a Perplexity DR replacement. Realistic expectations:
- ≥3 citations almost always; URL accuracy is good but **not validated** — Sean should spot-check 2 URLs before relying on numbers in any report.
- Synthesis coherence is high for well-scoped questions; degrades on vague prompts.
- Citation hallucination is a known risk with 14B-class models — the agent does not yet run a URL-checker post-processor.
- Numeric figures should be cross-checked against the cited source before quoting in stakeholder docs.

Treat outputs as starting points: the report saves Sean ~30 min of solo-research bootstrapping per question, but isn't authoritative.

## Allowed Tools

This skill should only use:
- `Read` — to inspect the queue file before appending.
- `Edit` — to append a new `- [ ]` line.

Do **not** use:
- `Write` — would overwrite the file and lose existing queue items.
- `Bash` — no need; everything is file-edit.
- The agent itself or `launchctl` — let the schedule handle execution.

## Examples

**Example 1: Sean surfaces a question mid-task**

```
User: "actually, do we know whether Qwen3.6's MoE variant runs on Apple Silicon yet? add that to research"

Skill action:
1. Refine to: "What is the current Apple Silicon support status for Qwen3.6 MoE variants
   (35B-A3B, etc.) in Ollama, MLX, and llama.cpp as of mid-2026?"
2. Read research-queue.md, confirm not already there.
3. Edit to append `- [ ] What is the current Apple Silicon support status for Qwen3.6
   MoE variants (35B-A3B, etc.) in Ollama, MLX, and llama.cpp as of mid-2026?` under
   ## Pending.
4. Confirm: "Queued — refined to specify the runtimes you actually use. Will run
   tonight at 02:45; digest in tomorrow's daily note."
```

**Example 2: Sean asks something better answered now**

```
User: "queue: what's the docker run command for searxng"

Skill action:
- Don't queue. This is a one-shot lookup.
- Respond: "That's a single-fact lookup — not worth queuing. The command is:
  `docker run -d --name searxng -p 8080:8080 searxng/searxng`. Want me to queue
  something deeper, like a comparison of SearXNG vs Whoogle for self-hosted
  meta-search?"
```

**Example 3: Already-queued duplicate**

```
User: "queue research on MLX vs GGUF speed on M4 Pro"

Skill action:
- Read research-queue.md, find that line was added 2026-04-26 and already has [x].
- Respond: "That one's already done — see [[20_projects/research/2026-04-26-what-are-the-key-differences-between-apples-mlx-and-gguf-for]].
  Want me to queue a follow-up that's narrower or more recent?"
```

## Related

- Producer agent: `agents-sdk/agents/deep_researcher.py` (Mac Mini, 02:45 nightly)
- Plan: `vault/20_projects/prj-superuser-pack/open-source-deep-research/macmini-migration-plan-2026-05-02.md`
- Sibling skill: `research-synthesis` (synthesizes EXISTING research artifacts; this skill QUEUES new research)
- Anchor target in daily note: `<!-- research-digest -->` at `vault/90_system/templates/tpl-daily.md:37`
- For paid cloud research (Gemini DR / DR Max) when local LDR is too thin, see `gemini-deep-research`.
