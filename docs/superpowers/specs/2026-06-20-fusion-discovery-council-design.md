# fusion-discovery-council — Design Spec

**Date:** 2026-06-20
**Status:** Approved design, pre-implementation
**Author:** Sean Winslow (brainstormed with Claude)
**Type:** New skill + backing CLI

---

## 1. Problem

Sean's existing research tooling has a gap:

- **`gemini-deep-research`** produces cited reports but "isn't pulling from the most recent and relevant articles" — its freshness and source selection underwhelm.
- **`last30days`** nails *social* recency (Reddit top comments, X, YouTube, HN, etc.) but synthesizes with a single model and doesn't touch review sites, GitHub issues, or fresh authoritative articles.
- **`llm-council`** gives multi-vendor blind-spot coverage but only *critiques text you already have* — it has no web access and gathers nothing new.
- The **local LDR path** (Qwen3-14B + SearXNG) is $0 but fabricates citations on compound topics (canonical bad specimen: invented `PureMCPClient`, fake `learn.microsoft.com` URLs).

Nothing today fuses **multi-model web research** + **recency-weighted pain-point mining** into one assistant. That's the gap `fusion-discovery-council` fills.

## 2. Goal

A discovery research skill that mines **fresh, real user pain points** across the broadest possible source surface, reasons over them with a **multi-vendor model panel** (different RLHF lineages → blind-spot + whitespace coverage), enforces a **hard anti-fabrication gate**, and frames the survivors as **concrete ideas** — PM opportunities or Substack post angles — each traceable back to the evidence that justifies it.

**Core deliverable:** an *evidence → idea pipeline*. Not a report, not a raw list — a ranked **idea ledger** where every idea carries its pain, its verbatim evidence (quotes + links + dates), and a freshness/confidence score.

## 3. Non-Goals (YAGNI for v1)

- **No autonomous launchd agent.** Interactive skill + backing CLI only. (A queued/overnight mode is a documented future, not v1.)
- **No paid review-scraper dependency** (Apify, etc.). Review sites are covered via site-targeted web search + WebFetch in v1. Apify actors are a noted future enhancement if coverage proves thin.
- **No new spend-tracking system.** Reuse the council spend module/file with independent per-tool caps.
- **No new vault auto-commit.** Per CLAUDE.md rule 8, Obsidian-Git owns vault commits; the skill never `git add`s the vault.

## 4. Name & Invocation

**Name:** `fusion-discovery-council` (parallels `llm-council`, but hunts fresh real-world evidence instead of critiquing supplied text).

**Invocation:**
```
fusion-discovery-council <topic> --lens pm|substack --tier quick|standard|deep
```
- `topic` — a product space, audience, competitor, or theme to investigate.
- `--lens pm` (default) — frames ideas as feature/JTBD opportunities.
- `--lens substack` — frames ideas as post angles + emits a handoff brief for the `substack-value-engine → storytelling-architecture → writing-voice-modes → writing-humanity-pass` chain.
- `--tier standard` (default) — controls panel size, source breadth, `max_tool_calls`, and the per-run cost cap.

Trigger phrases (for the SKILL.md description): "mine pain points", "discovery research", "what are users complaining about", "find substack ideas", "fresh research on X", "opportunity discovery", "where do competitors fail".

## 5. Architecture — Four-Stage Pipeline

```
  topic + lens + tier
        │
        ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  1. GATHER      │──▶│  2. FUSE        │──▶│  3. VERIFY      │──▶│  4. FRAME       │
│  evidence       │   │  multi-model    │   │  fabrication    │   │  lens → ideas   │
│  bundle (real   │   │  panel (Fusion) │   │  gate (drop     │   │  + idea ledger  │
│  URLs only)     │   │  + judge        │   │  ungrounded)    │   │  + quote bank   │
└─────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────────┘
        │                                                                  │
   deterministic                                                      output + spend
   (our code)                                                         (vault md)
```

### Stage 1 — GATHER (deterministic, our code; real evidence only)

Builds a structured **evidence bundle**: a list of records, each
`{source_type, source_name, url, date, verbatim_quote, engagement_signal}`. Only real, fetched URLs enter the bundle.

**1a — Social backbone (reuse last30days):**
- Shell out to `last30days <topic> --agent --emit=compact` → Reddit (top comments weighted), X, YouTube (transcripts), HN, optionally TikTok/IG/Polymarket.
- Parse its output into evidence records.

**1b — Fresh-article + citation harvest:**
- `perplexity/sonar-reasoning-pro` (standard) / `perplexity/sonar-deep-research` (deep) → cited, search-native fresh-article answers. Sonar is a search engine with citations — this is the direct fix for the "most recent and relevant articles" gap.
- Plus neural web search (Exa/Brave) with a recency filter for breadth.
- WebFetch top hits → extract verbatim complaint/insight quotes + URLs + dates.

**1c — Extended pain-point sources (tier-gated; see §6):**
- Review sites: G2, Capterra, TrustRadius, GetApp, Trustpilot, App Store, Google Play, Product Hunt — site-targeted search + WebFetch, with **competitor weakness mining** (harvest 1★/2★ reviews → "where competitors fail = your wedge").
- GitHub Issues + Canny/feature-request boards + public roadmaps — explicit upvoted unmet needs (strongest for `pm` lens).
- Demand/intent mining: Google People-Also-Ask + autocomplete + question harvest.
- Q&A pain: Stack Overflow/Exchange + Quora.
- Trend velocity: Google Trends / Exploding Topics signal (growing vs fading).
- Competitor-Substack/newsletter landscape (`substack` lens) — what's already written, so the angle hits the gap.

### Stage 2 — FUSE (Fusion panel inside the council spine)

- Feed the evidence bundle into one **OpenRouter Fusion** call (`{"type":"openrouter:fusion"}`), with `analysis_models` = the tier panel (§7) and `model` = the tier judge.
- Each panel model clusters the evidence into candidate pain points and may do supplementary `web_search`/`web_fetch` *only to fill gaps* (bounded by `max_tool_calls` per tier).
- The **judge** produces the signature output: consensus pain points, **contradictions** (love/hate, segment splits), **unique per-model insights**, and **blind-spots / whitespace** (what no model addressed). Ranks by frequency × intensity × recency × reach.
- Wrapped in the council CLI's **budget-cap pre-flight + spend tracking + partial-failure handling + transcript** machinery (reused, not rebuilt).

### Stage 3 — VERIFY (the anti-fabrication gate — non-negotiable)

- Every candidate pain point must trace to ≥1 supporting quote that maps to a **real URL present in the evidence bundle**.
- Re-confirm by lookup (and re-fetch if the panel introduced a URL not in the bundle).
- Any pain point whose evidence can't be traced is **dropped** or explicitly marked `unverified` — never silently softened. This is the gate that catches the LDR-specimen failure mode (fabricated entities/URLs).

### Stage 4 — FRAME (lens → idea ledger)

- **`--lens pm`:** each verified cluster → an opportunity card: *who feels it · the pain · current workaround · the opportunity (JTBD/feature hypothesis) · evidence links · score*.
- **`--lens substack`:** each verified cluster → a post angle + hook + value-promise, packaged as a **handoff brief** that drops into `substack-value-engine`.
- Always-on artifacts: the **quote bank** (verbatim, attributed social proof, paste-ready) and **cross-platform corroboration flags** (same pain on Reddit + G2 + GitHub surfaced first).

## 6. Source & Capability Coverage Matrix (tier-gated)

**Always-on (the differentiators — every tier, regardless of `--tier`):**
- Cross-lineage blind-spot + whitespace map (signature feature).
- Fabrication-gated evidence (Stage 3).
- Scored & ranked shortlist (frequency × intensity × recency × reach).
- Quote bank (verbatim, attributed).
- Cross-platform corroboration flags.

**Tier-gated (the matrix below controls breadth per run):**

| Capability / source | quick | standard | deep |
|---|:---:|:---:|:---:|
| last30days social backbone (1a) | ✅ | ✅ | ✅ |
| Sonar fresh-article harvest (1b) | sonar | sonar-reasoning-pro | sonar-deep-research |
| Exa/Brave neural web search (1b) | ✅ | ✅ | ✅ |
| Review sites + competitor weakness mining (1c) | — | ✅ | ✅ |
| GitHub Issues / Canny / roadmaps (1c) | — | ✅ | ✅ |
| Demand/intent mining (PAA/autocomplete) (1c) | — | ✅ | ✅ |
| Q&A pain (Stack Overflow/Quora) (1c) | — | — | ✅ |
| Trend velocity (Trends/Exploding Topics) (1c) | — | — | ✅ |
| Competitor-Substack landscape (substack lens) (1c) | — | lens | lens |

## 7. Model Panels (verified against OpenRouter, 2026-06-20)

Reasoning models priced per-million tokens. Web search billed per query. Discovery weights toward **lineage diversity** (the council's blind-spot value) and **native web/real-time grounding** (Grok = X-native).

| Model | ID | In/Out ($/M) | Web search | Context |
|---|---|---|---|---|
| Claude Opus 4.7 | `anthropic/claude-opus-4.7` | $5 / $25 | $0.01/q | 1M |
| GPT-5.5 | `openai/gpt-5.5` | $5 / $30 | $0.01/q | 1.05M |
| Gemini Pro | `google/gemini-pro-latest` | $2 / $12 | $0.014/q | 1.05M |
| Grok 4.3 | `x-ai/grok-4.3` | $1.25 / $2.50 | $0.005/q | 1M |
| DeepSeek v4-pro | `deepseek/deepseek-v4-pro` | $0.44 / $0.87 | — | 1.05M |
| Mistral medium 3.5 | `mistralai/mistral-medium-3.5` | $1.50 / $7.50 | — | 262K |

**Panels by tier:**

| Tier | Panel (`analysis_models`) | Judge (`model`) | `max_tool_calls` | Target / cap |
|---|---|---|:---:|---|
| quick | `gemini-pro` + `grok-4.3` + `deepseek-v4-pro` | `gemini-pro` | 3 | ~$0.20–0.40 / **$0.50** |
| standard | `claude-opus-4.7` + `gpt-5.5` + `gemini-pro` + `grok-4.3` | `claude-opus-4.7` | 5 | ~$0.60–1.20 / **$1.50** |
| deep | standard four + `deepseek-v4-pro` + `mistral-medium-3.5` | `claude-opus-4.7` | 8 | ~$1.50–3.00 / **$4.00** |

**Perplexity Sonar decision:** Sonar is on OpenRouter (5 variants) but **all are `tools=False`** — they cannot accept the Fusion server tools, so they are **not** panel members. Sonar instead serves Stage 1b as a citation-grounded article harvester (`sonar-reasoning-pro` standard, `sonar-deep-research` deep; both $0.005/search, cheap tokens).

`standard` mirrors Sean's proven `premium` council roster (already battle-tested on his OpenRouter key). `deep` adds Chinese + European lineages so cross-vendor disagreement — and therefore the whitespace signal — is maximal.

## 8. Cost Control & Spend Tracking

- **Pre-flight cap check** (reuse council's guard): estimate panel-token + web-query + judge cost; refuse if over the per-run cap; surface the error verbatim.
- The real cost variable is web-tool calls = `panel_size × max_tool_calls × per-query price` → bounded per tier via `max_tool_calls`.
- `deep` **confirms cost before running** (like Gemini DR Max).
- **Spend file:** reuse `vault/health/council-spend-{YYYY-MM-DD}.json` (shared source of truth) but with **independent per-tool daily/monthly caps** (tag records by tool) so discovery runs can't starve the critique budget. Proposed caps: $7/day, $40/month for discovery, separate from council's.

## 9. Output

- **Idea ledger** → `vault/20_projects/research/<YYYY-MM-DD>-<topic-slug>-<lens>-idea-ledger.md`.
  - Ranked ideas; each: pain · evidence (quotes + links + dates) · idea (lens-framed) · freshness/confidence score · cross-platform flag.
  - Appended sections: **blind-spot/whitespace map**, **quote bank**, **contradiction map**, **cost summary** (models used, partial failures named).
- **Substack lens** additionally writes a handoff brief consumable by `substack-value-engine`.
- **Session JSON** archived next to council sessions for machine-readable replay.
- The skill **never** `git add`s the vault (Obsidian-Git owns commits).

## 10. Reuse Map

| Need | Reuse from |
|---|---|
| Social/recency evidence | `last30days --agent` (shell-out) |
| Budget caps + spend tracking + transcript + partial-failure | `tools/llm-council/council/` CLI |
| Multi-model panel + web tools + judge | OpenRouter **Fusion** server tool |
| Fresh cited articles | Perplexity Sonar (Stage 1b) |
| Web search / fetch in-skill | Exa/Brave + WebFetch |
| Substack handoff | `substack-value-engine` → voice chain |

## 11. Failure Modes

- **last30days returns thin/empty** → proceed with web + Sonar evidence; note reduced social coverage in the ledger.
- **One panel model fails in Fusion** → continue with N-1; name the missing model in the cost summary (council pattern).
- **Two+ panel models fail** → abort Fusion, fall back to single-model (judge) synthesis over the evidence bundle; mark ledger `degraded`.
- **Verification drops most candidates** → surface "low verifiable signal" honestly rather than padding with unverified claims.
- **Budget cap hit** → refuse + offer: wait (daily reset) / `--force` (per-query bypass, daily/monthly still enforced) / drop a tier.

## 12. Acceptance Criteria

- [ ] `fusion-discovery-council <topic> --lens pm --tier quick` produces a ranked idea ledger where **every** pain point has ≥1 traceable real-URL quote.
- [ ] A deliberately fabricated/unfetchable URL never survives Stage 3.
- [ ] `--lens substack` emits a handoff brief that `substack-value-engine` accepts.
- [ ] Each tier respects its per-run cost cap; `deep` confirms cost first; spend lands in the shared file tagged by tool.
- [ ] Panel composition matches §7; Sonar appears only in Stage 1b, never the panel.
- [ ] The ledger includes a blind-spot/whitespace map and a quote bank.
- [ ] CHANGELOG.md + CLAUDE.md/README count tables updated (new skill).

## 13. Future Enhancements (deferred)

- Autonomous/queued mode (overnight topic queue, like the fleet agents).
- Apify actors for deeper/gated review-site coverage.
- Verify + slot additional lineages (e.g., Qwen) into `deep`.
- Pain-taxonomy persistence across runs (track whether a pain is growing over time).
