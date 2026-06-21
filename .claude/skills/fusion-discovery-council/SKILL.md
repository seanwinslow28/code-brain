---
name: fusion-discovery-council
description: Multi-model fresh-evidence discovery — mine real user pain points across last30days social + Sonar/web articles, fuse through an OpenRouter Fusion panel (Opus/GPT/Gemini/Grok), drop anything not traceable to a real fetched URL, and frame survivors as ranked, evidence-linked PM opportunities or Substack ideas. Use when Sean says "discovery research", "mine pain points", "what are users complaining about", "find substack ideas", "fresh research on X", "opportunity discovery", or "where do competitors fail". Tiered quick/standard/deep with hard $10/day $50/month caps. Skip for text critique (use llm-council), for code, or for simple lookups.
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Fusion Discovery Council

An evidence→idea discovery pipeline, invocable from inside Claude Code sessions. Where `llm-council` critiques text you already have, this skill goes and *finds* the raw material first: it gathers fresh, real-URL evidence of user pain, fuses it through a multi-vendor OpenRouter Fusion panel, drops anything it can't trace back to a fetched source, and frames the survivors as ranked, evidence-linked opportunities. The output is a markdown **idea ledger** where every pain point cites the URL it came from.

It reuses the council spine (`client.py`, `budget.py`) — same OpenRouter client, same budget guardrails, same shared spend file — so caps stay coherent across the council family.

---

## 0. Path resolution (read first)

This skill's backing CLI lives in code-brain; it is canonical there and must not be duplicated. The skill may be symlinked from `~/.claude/skills/fusion-discovery-council/` so it's invocable from any Claude Code session on Sean's machine, but the code, tier configs, budget guardrails, and spend tracking all live in code-brain.

| Resource | Canonical absolute path |
|---|---|
| CLI working dir | `/Users/seanwinslow/Code-Brain/code-brain/tools/llm-council` |
| Spend tracking | `/Users/seanwinslow/Code-Brain/code-brain/vault/health/council-spend-{YYYY-MM-DD}.json` (shared with council; discovery rows tagged `tool="discovery"`) |
| Idea ledger output | `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/research/<YYYY-MM-DD>-<topic-slug>-<lens>-idea-ledger.md` |
| Session JSON archive | written under the ledger's parent dir at `.discovery-sessions/` |

**API key:** OpenRouter is resolved via `python-dotenv`, which walks up from the CLI working dir to the repo-root `.env` (`OPENROUTER_API_KEY`). No key needs to be passed on the command line.

**Output routing rule:** Always pass `--output` explicitly as an absolute path following the [output convention](#output-path-convention) below. `mkdir -p` is handled by the CLI, but always pass the full absolute path so the ledger lands in the vault research folder rather than the current working directory.

---

## 1. When to run discovery

| Question shape | Use this skill? |
|---|---|
| "What are users actually complaining about in X?" | Yes — this is the core case |
| "Mine fresh pain points / opportunities in this space" | Yes |
| "Where do competitors fail their users?" | Yes |
| "Find me Substack ideas grounded in real reader pain" | Yes — `--lens substack` emits a post-angle ledger + a substack-value-engine handoff brief |
| Critique a draft / spec / cover letter I already wrote | No — use `llm-council` |
| Write or refactor code | No — single-model Claude |
| Simple factual lookup | No — answer in-session |
| Comprehensive cited report across 20+ sources | No — use `gemini-deep-research` |

---

## 2. The four stages

The pipeline runs in a fixed order; each stage feeds the next.

1. **GATHER** — Collect fresh evidence into a real-URL bundle:
   - `last30days` social backbone (recent user complaints / discussion).
   - Perplexity **Sonar** article harvest (tier-scaled: `sonar` → `sonar-reasoning-pro` → `sonar-deep-research`).
   - A **web collector** (Exa if `EXA_API_KEY` set, else Brave) for supplementary fresh articles, with a full-page fetch fallback for quote density.
   - **Extended collectors (tier-gated):** review sites + competitor-weakness mining, GitHub Issues, and Stack Exchange Q&A. `standard` adds review sites + GitHub Issues; `deep` adds those plus Stack Exchange Q&A. Each emits a real URL + a verbatim quote, so the Stage-3 gate still governs everything.
   Every piece of evidence carries the URL it was fetched from. Nothing enters the pipeline without a source.

2. **FUSE** — Run the gathered evidence through an OpenRouter **Fusion panel** (Opus / GPT / Gemini / Grok at standard tier) plus an outer **judge** model. The panel reads the evidence and proposes candidate pain points; the judge consolidates and de-duplicates them.

3. **VERIFY** — The **anti-fabrication gate** (see §4). Every candidate pain point must trace to a quote whose URL exists in the gathered evidence. Untraceable candidates are dropped or marked `unverified` — never quietly kept.

4. **FRAME** — Apply the lens to each *verified* pain point: `pm` → ranked, evidence-linked opportunity cards; `substack` → ranked post angles + a substack-value-engine handoff brief. Render the **idea ledger** markdown (+ the brief for substack).

> The extended collectors are LIVE and tier-gated (above): review sites + competitor-weakness mining and GitHub Issues on `standard`/`deep`, Stack Exchange Q&A on `deep`. NOT included — do **not** claim them: demand-intent (autocomplete/PAA — produces queries, not URL-anchored quotes, so the gate would drop them), trend-velocity feeds (no clean free API), and Quora (anti-scraping). `quick` stays lean (last30days + Sonar + web). The `last30days` backbone contributes Reddit/HN (keyless); HackerNews can come back empty on some runs and degrades safely.

---

## 3. Flags

```
--lens     pm | substack    (default: pm)
--tier     quick | standard | deep    (default: standard)
--segment  <audience>        reshape gather queries toward a target audience (optional)
--output   <ABSOLUTE PATH>   (required)
--force    bypass per-run cap only (daily/monthly still enforced)
--yes      auto-confirm deep-tier cost prompt
```

**`--lens`** — `pm` (default) frames verified pain into ranked PM opportunities. `substack` reframes the same verified pain into ranked post angles and additionally writes a **handoff brief** consumable by the `substack-value-engine` skill (chain: substack-value-engine → storytelling-architecture → writing-voice-modes → writing-critique → writing-humanity-pass). The brief pre-fills the Value-Gate Itch + Transfer + verbatim evidence and leaves the Solution slot for you.

**`--segment`** — optional free-text audience qualifier (e.g. `developer`, `creative`, `pm`) that reshapes the gather queries toward where that audience posts. Use it when a generic topic returns the wrong segment's pain (e.g. generic "creatives" returns developer pain).

**`--tier`** — scales the panel size, per-model web tool-call budget, the Sonar harvester, and the per-run cost cap:

| Tier | Panel | Per-run cap |
|---|---|---|
| `quick` | 3 models | $0.50 |
| `standard` | 4 models (Opus/GPT/Gemini/Grok) | $1.50 |
| `deep` | 6 models | $4.00 (confirms cost before running) |

---

## 4. Exact CLI invocation

Run from the CLI working dir. The base package deps (click/rich/httpx/dotenv) are sufficient — do **not** add `--extra dev` (that's only for pytest).

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council.discovery "<topic>" --lens pm --tier standard --output <ABSOLUTE PATH>
```

Concrete example:

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council.discovery \
    "AI note-taking apps" \
    --lens pm \
    --tier standard \
    --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/research/2026-06-20-ai-note-taking-apps-pm-idea-ledger.md
```

On success the CLI prints the ledger path plus a one-line summary (`Verified ideas: N · dropped: M · $X.XX`).

### Output path convention

```
vault/20_projects/research/<YYYY-MM-DD>-<topic-slug>-<lens>-idea-ledger.md
```

On `--lens substack`, a sibling brief is also written:

```
vault/20_projects/research/<YYYY-MM-DD>-<topic-slug>-substack-brief.md
```

- `<YYYY-MM-DD>` — today's date.
- `<topic-slug>` — the topic, lowercased and hyphenated.
- `<lens>` — `pm` or `substack`.

Always pass this as an **absolute** path under `/Users/seanwinslow/Code-Brain/code-brain/`.

---

## 5. Cost discipline

- Every CLI invocation does a pre-flight cap check. If the estimated cost would exceed the per-run cap, the CLI refuses with a clear `Budget rejected:` error (exit code 2).
- Per-run caps: **quick $0.50 / standard $1.50 / deep $4.00**.
- **The per-run cap gates the pre-flight ESTIMATE (`0.6 × cap`), not actual spend.** A web-tool-call-heavy topic can *overshoot* its per-run cap — observed 2026-06-21: a `standard` run cost **$2.74** vs the $1.50 cap. Cost is dominated by the panel's web-tool calls and is **high-variance by topic**, so don't assume `deep` ⟹ most expensive (a deep run the same day cost $0.99). **The $10/day cap is the real guardrail** — it's checked against *actual* accumulated spend, so it can't be overshot the same way. Watch the daily total when running several topics in a session.
- Discovery's own daily/monthly caps: **$10/day, $50/month**. These are independent of the council's caps but tracked in the **same** spend file — discovery rows are tagged `tool="discovery"` so the two tools never cross-deplete each other while staying in one coherent ledger (enforced bidirectionally via per-tool pre-flight as of Phase 2).
- Recorded spend uses OpenRouter's authoritative `usage.cost` when available, falling back to a conservative token estimate.
- `deep` tier **confirms the cost interactively before running** (pass `--yes` only when Sean has authorized it for this run).
- `--force` bypasses **only the per-run cap** — the daily and monthly caps are still enforced. Use it only when Sean explicitly authorizes it for this query.
- After a successful run the CLI records actual spend to `/Users/seanwinslow/Code-Brain/code-brain/vault/health/council-spend-{YYYY-MM-DD}.json` (canonical — same file across all repos, so daily/monthly caps stay coherent).

If the CLI rejects a query on budget, surface the error verbatim and ask Sean whether to:
1. Wait until tomorrow (daily reset),
2. Drop to a cheaper tier (`standard` → `quick`),
3. Use `--force` (per-run bypass only; daily/monthly still enforced), or
4. Skip discovery for now.

---

## 6. The non-negotiable verification gate

This is the heart of the skill and is **not** softened under any circumstance.

- Every pain point in the ledger must trace to a **quote whose URL exists in the gathered evidence bundle**.
- A candidate the panel proposes but that cannot be traced to a real fetched URL is **dropped** or marked `unverified` — never paraphrased into the ledger as if it were sourced, never "rounded up" to a real claim.
- This is what separates discovery from a model hallucinating plausible-sounding pain. If the evidence isn't there, the idea doesn't ship.

When reporting back to Sean, always surface the **dropped/unverified count** alongside the verified ideas — a high drop rate is signal about evidence thinness, not something to hide. Also point Sean at the ledger's **blind-spot / whitespace map** — the signature cross-model output that audits what the evidence and the panel *missed* (e.g. "the topic returned generic AI-coding pain, not studio-2D specifics"). It is often the highest-signal section and tells you how to sharpen the next run (reframe the topic, add `--segment`, or raise the tier).

---

## 7. Vault rule (never commit)

The skill **writes** the idea ledger to `vault/20_projects/research/...` and stops there. It must **never** run `git add` / `git commit` against `vault/`. Per CLAUDE.md rule 8, the **Obsidian-Git plugin is the sole owner** of vault auto-commit — the new ledger file will be committed automatically. Do not stand up any second commit mechanism for vault paths.

---

## 8. Failure modes

- **Budget rejected** (exit 2) — pre-flight cap hit; surface the error verbatim and offer the options in §5.
- **Discovery failed at fuse** (exit 3) — the Fusion call failed (after SSE-padding-safe decode + one reprompt retry). The CLI **records the spend OpenRouter actually billed** (tagged `tool="discovery"`), **persists the session JSON** with per-collector `gather_status`, and echoes that status — so a failed run is diagnosable and never silently free. No ledger is written.
- **Discovery failed (exit 3, pre-fuse)** — a gather/setup error before any billable call; no spend recorded.
- **High drop rate** — the pipeline ran but most candidates failed the verification gate. This is a *valid* outcome (thin evidence), not a bug. Report the verified vs dropped counts to Sean honestly.
