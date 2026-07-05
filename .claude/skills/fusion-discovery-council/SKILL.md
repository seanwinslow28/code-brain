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

## 2. The five stages

The pipeline runs in a fixed order; each stage feeds the next.

1. **GATHER** — Collect fresh evidence into a real-URL bundle:
   - `last30days` social backbone (recent user complaints / discussion).
   - Perplexity **Sonar** article harvest (tier-scaled: `sonar` → `sonar-reasoning-pro` → `sonar-deep-research`).
   - A **web collector** (Exa if `EXA_API_KEY` set, else Brave) for supplementary fresh articles, with a full-page fetch fallback for quote density.
   - **Extended collectors (tier-gated):** review sites + competitor-weakness mining, GitHub Issues, and Stack Exchange Q&A. `standard` adds review sites + GitHub Issues; `deep` adds those plus Stack Exchange Q&A. Each emits a real URL + a verbatim quote, so the Stage-3 gate still governs everything.
   Every piece of evidence carries the URL it was fetched from. Nothing enters the pipeline without a source.

2. **FUSE** — Run the gathered evidence through an OpenRouter **Fusion panel** (GPT / Gemini / Grok at standard tier) plus an outer **judge** model (Opus at standard/deep, GPT at quick). The panel reads the evidence and proposes candidate pain points; the judge consolidates and de-duplicates them. **E2 invariant:** the judge's model family is deliberately disjoint from every panelist's, so no model grades its own family's output (self-preference debias — see [the E2 research note](../../../vault/20_projects/research/2026-06-30-llm-judge-self-preference-debias-research.md)).

3. **VERIFY** — The **anti-fabrication gate** (see §4). Every candidate pain point must trace to a quote whose URL exists in the gathered evidence. Untraceable candidates are dropped or marked `unverified` — never quietly kept.

3.5. **DEDUP** *(post-VERIFY, pre-FRAME; $0/deterministic)* — A shared lexical token-Jaccard similarity collapses near-duplicate gate-survived pain points via bounded **merge-to-canonical** (bias-to-under-merge; no transitive closure). Evidence is unioned honestly, with corroboration kept keyed on distinct domains — so merging two pains that cite the same site doesn't inflate the corroboration count. When merges occur, both renderers show a `merged N near-duplicate pain point(s)` note. D4's whitespace gaps are also **ranked most-distinct-first** (MMR — Carbonell & Goldstein 1998, λ=0.3) at this stage, so the Whitespace Map leads with the most novel gap rather than panel order. No model call; gate untouched. (See [dedup.py](../../../tools/llm-council/council/discovery/dedup.py).)

4. **FRAME** — Apply the lens to each *distinct, verified* pain point: `pm` → ranked, evidence-linked **PRD-grade opportunity cards**; `substack` → ranked post angles + a substack-value-engine handoff brief. Each card carries a research-grounded **`score = value × confidence`** composite (0–100): `value` = weighted importance(intensity)/reach(log-damped engagement)/recency(exp-decay), `confidence` = independent-source corroboration (dominant) + model-consensus (light, separate) — so a thin-evidence pain is discounted, never propped up by high importance (RICE pattern; see [scoring.py](../../../tools/llm-council/council/discovery/scoring.py)). The card shows the full **honest breakdown** (importance · reach · recency · sources · domains · the `value × conf` arithmetic), leads with the verbatim quote, states **why-now** (deterministic from recency), and ends with a **proposed bet** — a labeled *heuristic* riskiest-assumption + cheapest-test derived from the pain shape, with a human fill-in slot (it never fabricates a specific insight; see [bet.py](../../../tools/llm-council/council/discovery/bet.py)). Both lenses share one `score_opportunity` helper. The ledger reflects **distinct** pains only (near-duplicates merged in DEDUP), so corroboration counts are honest — a merged card's evidence union never double-counts the same domain. Each ranked card also carries a compact **receipts line** under its heading (🧾) — a two-axis evidence-depth gradient: **corroboration** (independent source domains: 1 = single-source, 2 = corroborated, 3+ = well-corroborated) and **freshness** (fresh / recent / aging, or undated when no evidence date is available). A one-time legend rendered above the ranked list (in both ledgers) frames receipts as evidence *depth*, not a verdict — every card already cleared the anti-fabrication gate; freshness is a recency signal, not proof. Deterministic, $0; the precise floats stay in the Size:/Confidence: detail lines (see [receipts.py](../../../tools/llm-council/council/discovery/receipts.py)). The CLI then renders the **idea ledger** markdown (+ the brief for substack) and exits — this is its final output.

5. **BACKFILL** *(agent-layer; the default flow)* — After the CLI writes the ledger, **the orchestrating Claude Code session backfills the blind-spot map itself** using its own `WebSearch`/`WebFetch` tools (on Sean's Anthropic subscription — **$0 marginal API**). It reads each ledger's `## ⭐ Whitespace Map` (D4 — now the **lead** section, with a "Sharpen the next run" action list and a per-gap `→ Backfill` next-action), runs a **solution/evidence-side** search for each gap (not a complaint query), reads the candidate pages, and appends a clearly-separate `## Web Supplement (gap-fill)` section. An agent search→read→synthesize vets **relevance natively** (the deterministic in-CLI version couldn't), so the leads are higher-quality. Same anti-fabrication discipline as §6: **every item is a verbatim quote from a real fetched URL**, or it's rendered `still open — not filled` — never papered over. The supplement stays **OUT** of the panel-ranked list (it never bypasses FUSE consensus) and is labeled **gap-fill LEADS, not consensus-verified claims**. The full single-session recipe is §4.1; the `verify_supplement` backstop (§6) re-checks every quote is verbatim. *(Opt-in `--supplement` runs a deterministic in-CLI Exa/Brave version of this stage for the future headless/no-agent path — default **off**; see §3.)*

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
--supplement / --no-supplement   Opt-in in-CLI Stage 5 BACKFILL (Exa/Brave), for the headless/no-agent path (default: OFF)
```

**`--supplement` / `--no-supplement`** — **Default OFF.** In a normal Claude Code session, leave it off and let the agent do BACKFILL via `WebSearch`/`WebFetch` ($0, higher-quality, relevance-vetted — see §2 stage 5 + §4.1). `--supplement` turns on the **deterministic in-CLI Exa/Brave** version of the stage, which exists for a **future headless / autonomous mode with no agent** to drive the web tools. It requires `EXA_API_KEY` or `BRAVE_API_KEY` — with neither set it degrades to a "skipped" note (see §8), never a crash — and it adds the tier-capped web-query cost (see §5). It uses deterministic keyword extraction (relevance: mixed), so prefer the agent flow whenever an agent is in the loop.

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

### 4.1 Single-session agent-driven flow (the standard run)

One Claude Code session does it all. The council CLI is the paid part; the BACKFILL is the agent
using its own web tools on the subscription ($0). The copy-paste template lives at
[`references/run-template.md`](references/run-template.md) — model new runs on it.

1. **Run the council CLI** (the §4 invocation) for each topic. It writes the ledger (+ brief for
   substack) and prints `Verified ideas: N · dropped: M · $X.XX`. *Leave `--supplement` off.*
2. **Read the blind-spot map.** Open each ledger and read its `## ⭐ Whitespace Map` (the lead section). Its "Sharpen the next run" list also tells you which gap to backfill first, and whether to reframe / add `--segment` / raise tier.
3. **Backfill each gap with your own web tools.** For every gap bullet, run `WebSearch` on the
   **solution/evidence side** (what would fill the gap, not a complaint query), `WebFetch` the
   most promising results, and pull a **verbatim quote** that actually speaks to the gap. You are
   the relevance filter — only keep a quote if it genuinely addresses the gap.
4. **Append the `## Web Supplement (gap-fill)` section** to the ledger, one `### <gap>` subsection
   per gap. Format each finding as a single line: `- "<verbatim quote>" — <URL>`. A gap you can't
   fill honestly is `- still open — not filled`. Lead the section with the standard LEADS caveat
   (it's leads, not FUSE-consensus claims). **Never fabricate or paraphrase a quote into looking
   sourced** — that breaks the §6 gate.
5. **Run the backstop** to prove every quote is verbatim at its URL:
   ```bash
   cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && \
     uv run python -m council.discovery.verify_supplement <LEDGER ABSOLUTE PATH>
   ```
   Exit 0 = all quotes verbatim-supported. Exit 1 = at least one isn't — **demote each flagged
   item to `still open — not filled`** and re-run until clean.
6. **Report back** verified/dropped counts, gaps filled vs still-open, and the backstop result.

This is subscription-covered ($0 API) and vets relevance natively — strictly better than the
deterministic in-CLI `--supplement` path, which exists only for a future no-agent headless mode.

---

## 5. Cost discipline

- Every CLI invocation does a pre-flight cap check. If the estimated cost would exceed the per-run cap, the CLI refuses with a clear `Budget rejected:` error (exit code 2).
- Per-run caps: **quick $0.50 / standard $1.50 / deep $4.00**.
- **The per-run cap gates the pre-flight ESTIMATE (`0.6 × cap`), not actual spend.** A web-tool-call-heavy topic can *overshoot* its per-run cap — observed 2026-06-21: a `standard` run cost **$2.74** vs the $1.50 cap. Cost is dominated by the panel's web-tool calls and is **high-variance by topic**, so don't assume `deep` ⟹ most expensive (a deep run the same day cost $0.99). **The $10/day cap is the real guardrail** — it's checked against *actual* accumulated spend, so it can't be overshot the same way. Watch the daily total when running several topics in a session.
- Discovery's own daily/monthly caps: **$10/day, $50/month**. These are independent of the council's caps but tracked in the **same** spend file — discovery rows are tagged `tool="discovery"` so the two tools never cross-deplete each other while staying in one coherent ledger (enforced bidirectionally via per-tool pre-flight as of Phase 2).
- Recorded spend uses OpenRouter's authoritative `usage.cost` when available, falling back to a conservative token estimate.
- **Stage 5 BACKFILL is $0 in the default (agent-driven) flow.** The agent uses `WebSearch`/`WebFetch` on Sean's Anthropic subscription — no OpenRouter spend, nothing added to the discovery ledger. The opt-in in-CLI `--supplement` path (headless/no-agent) reuses the free Exa/Brave collector on your own keys ($0 on the OpenRouter ledger) and makes **no** model call; its web queries are priced into recorded spend at the standard per-web-query rate, tier-capped to 2 / 4 / 6 queries (`quick` / `standard` / `deep`) — at most ~$0.07 on `deep`. Either way the $10/day cap still governs the paid council stages.
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
- **The gate also governs Stage 5 BACKFILL — now split across the agent + a code backstop.** The agent-driven supplement (§4.1) is held to the same standard by two complementary checks: **(1) relevance** — the agent reads each page and only keeps a quote that genuinely speaks to the gap (the deterministic in-CLI version couldn't do this; it's the agent's native strength); **(2) verbatim-ness** — the `verify_supplement` backstop (`python -m council.discovery.verify_supplement <ledger>`) re-fetches every cited URL and confirms the quote appears there *verbatim*, routed through the **same** shared primitive (`quote_supported_at_url` in `verify.py`) as the core VERIFY stage. A quote that isn't verbatim at its URL is demoted to `still open — not filled`. The Web Supplement section is still labeled **gap-fill LEADS, not consensus-verified claims** (it never bypassed FUSE).

- **E1 — the core VERIFY stage now does substring→NLI entailment, not substring-only.** Every candidate pain point still must pass the original substring/URL-traceability check *first* (the recall-safety invariant: substring never rejects — E1 only ever adds a stricter check on top, never removes the floor). If a local NLI model is installed, the gate additionally scores whether the cited quote **entails** the claimed pain point (`cross-encoder/nli-deberta-v3-small`, int8 ONNX via `onnxruntime`, in-process, no server) — this catches quotes that are present verbatim but don't actually support the paraphrased claim. **The model is optional and the gate degrades gracefully**: install it with `tools/llm-council/scripts/install_nli_model.sh` (downloads the ONNX + tokenizer to `tools/llm-council/models/nli-deberta-v3-small/`, gitignored) plus `uv pip install -e '.[nli]'` for the `onnxruntime`/`transformers`/`numpy` deps. With no model present (fresh clone, CI, or any load failure), `council/discovery/nli.py::get_scorer()` returns `None` and VERIFY silently runs **substring-only** — never a hard failure. A degraded run is never silent to Sean: the rendered ledger shows a one-line `**Verification:** substring-only — NLI model not loaded` note, and the session JSON records `verify_mode` (`"nli"` or `"substring-only"`) alongside `citation_precision`/`citation_recall` (ALCE-style metrics over the verified set) so degraded runs are auditable after the fact, not just in the moment.

- **The FRAME score honors the gate too.** The `value × confidence` composite is computed only from data already in the verified bundle (intensity, engagement, dates, distinct sources/domains, model consensus) — it never invents a number, and the card shows the full breakdown so the score is auditable, not a black box. The **proposed bet** is a clearly-labeled *heuristic* (riskiest-assumption category + cheapest-test pattern from the pain shape) with a human fill-in slot — it names a structural starting point, never a fabricated specific insight. Treat the bet as a prompt to think, not a finding.

When reporting back to Sean, always surface the **dropped/unverified count** alongside the verified ideas — a high drop rate is signal about evidence thinness, not something to hide. Also point Sean at the ledger's **`## ⭐ Whitespace Map`** — the signature cross-model output that audits what the evidence and the panel *missed* (e.g. "the topic returned generic AI-coding pain, not studio-2D specifics"). As of D4 it **leads** the ledger: it carries a deterministic "Sharpen the next run" action list (reframe · add `--segment` · raise tier · which gap to backfill first) and a per-gap `→ Backfill` next-action. It is honest absence-of-evidence — gaps are framed as what was missed and the action is always to *investigate*, never to *build* — so never report it as verified claims.

---

## 7. Vault rule (never commit)

The skill **writes** the idea ledger to `vault/20_projects/research/...` and stops there. It must **never** run `git add` / `git commit` against `vault/`. Per CLAUDE.md rule 8, the **Obsidian-Git plugin is the sole owner** of vault auto-commit — the new ledger file will be committed automatically. Do not stand up any second commit mechanism for vault paths.

---

## 8. Failure modes

- **Budget rejected** (exit 2) — pre-flight cap hit; surface the error verbatim and offer the options in §5.
- **Discovery failed at fuse** (exit 3) — the Fusion call failed (after SSE-padding-safe decode + one reprompt retry). The CLI **records the spend OpenRouter actually billed** (tagged `tool="discovery"`), **persists the session JSON** with per-collector `gather_status`, and echoes that status — so a failed run is diagnosable and never silently free. No ledger is written.
- **Discovery failed (exit 3, pre-fuse)** — a gather/setup error before any billable call; no spend recorded.
- **High drop rate** — the pipeline ran but most candidates failed the verification gate. This is a *valid* outcome (thin evidence), not a bug. Report the verified vs dropped counts to Sean honestly.
- **Supplement skipped (no web-search key)** — *opt-in `--supplement` path only.* The in-CLI Stage 5 needs `EXA_API_KEY` or `BRAVE_API_KEY`. With neither set it degrades gracefully: no queries, no cost, and the ledger's Web Supplement section reads `supplement skipped: no web-search key configured` — never a crash. The default agent-driven flow (§4.1) has no key dependency: it uses the agent's own `WebSearch`/`WebFetch`.
- **Agent backfill: a gap with no honest fill** — in the §4.1 flow, if the agent can't find a verbatim quote that genuinely addresses a gap, the gap is written `still open — not filled`. That is the correct outcome (honest whitespace), not a failure. The `verify_supplement` backstop exit 1 likewise means *demote, don't paper over* — never invent a quote to clear it.
