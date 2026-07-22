---
type: research
status: complete
tags: [fusion-discovery-council, pm3, verdict]
---

# PM3 t1 — The Trend-Signal-vs-Noise Verdict (the Phase-2 gate)

> **Verdict: KILL the trend-tracking premise (RESCOPE-worthy dedup value is contingent — see §6). Do NOT build PM3-as-specified now.**
> The single paid t1 run + the 4a-validated matcher show the t0→t1 movement is **≤ sampling/panel/gather noise**, not a trend signal. Red-team #5's objection lands. The $0 groundwork gate did its job: we spent the clustering test (4a, $0) + one paid run to make this call, instead of building the whole persistence feature on an unvalidated premise.

## What ran

- **t1:** `fusion-discovery-council`, topic **"AI coding assistants"**, tier **standard**, lens **pm** — the exact t0 config. Session `20260722-122152-4b67cc`. **6 verified pains, 0 dropped.**
- **Cost:** **$6.81** (estimated; `provenance: estimated`, no `generation_id`) — a **3.7× overshoot vs t0's $1.85** for the identical config. Cost incident logged as a ticket (§7). Plus ~$0.02 of failed-attempt gather cost while diagnosing an OpenRouter outage (§7, the `max_price` fusion bug).
- **t0 (frozen baseline):** `pm3-t0-ai-coding-assistants-2026-06-30.json` — 8 verified, 2 dropped, $1.85, 93 evidence records. **22-day gap** t0→t1 (past the ~7/21 threshold — a real signal window).
- **Matcher:** the 4a-validated two-stage matcher, reused exactly — candidate gen = **exact-shared-evidence-URL ∪ lexical top-1** (E3's `pain_similarity`, top-1 only, no band) → **temp-0 local LLM judge** (`qwen3.6_35b-a3b-32k`, Ollama, strict SAME/RELATED/DIFFERENT). $0. No cloud fallback. Full recipe + why naive matching lies: [[2026-07-09-pm3-4a-pain-key-clustering-validation]].

## The movement table (t0 → t1)

| t0 pain (imp · domains · freshness · score) | identity in t1 | via | note |
|---|---|---|---|
| #1 Context blindness (4 · 2 · aging · 54) | **RELATED** → t1#1 | shared-url | absorbed into "Ecosystem Fragmentation" |
| #2 Near-correct/unreliable code (5 · 3 · aging · 44) | **SAME** → t1#2 (72) | 3 shared URLs + lexical top-1 | persistent core pain |
| #3 Context window degradation (3 · 1 · aging · 42) | **RELATED** → t1#1 | shared-url | absorbed into "Ecosystem Fragmentation" |
| #4 Tool choice confusion (3 · 2 · fresh · 39) | **ABSENT** | (top-1 was DIFFERENT) | vanished as standalone |
| #5 Missing agent features (3 · 1 · aging · 36) | **RELATED** → t1#6 | shared-url | granularity shift → security framing |
| #6 OSS backlash vs low-effort AI (3 · 1 · aging · 34) | **ABSENT** | (top-1 was DIFFERENT) | vanished |
| #7 Cost/pricing pain (3 · 1 · fresh · 30) | **ABSENT** | (top-1 was DIFFERENT) | vanished standalone (theme folded into t1#5, no SAME) |
| #8 Security & data leakage (4 · 1 · aging · 25) | **SAME** → t1#6 (52) | lexical top-1, sim 0.15 | persistent core pain |

**Emerged in t1 (no SAME/RELATED to any t0 pain):**
- t1#3 **Skill Atrophy & Over-Reliance** (imp5 · 3 domains · fresh · 67)
- t1#4 **Enterprise ROI Failure & Corporate Gaslighting** (imp5 · 2 domains · fresh · 62)

**Tally:** 2 SAME · 3 RELATED · 3 ABSENT · 2 EMERGED. Surface turnover: **0 of 6 t1 titles match any t0 title**; count 8→6.

## The verdict reasoning — is the movement > noise? (adversarial with myself)

**No. The movement is dominated by the exact noise modes 4a already documented, plus a gather-recency artifact. Three independent reasons:**

1. **The score rise is a recency artifact, not intensity.** Mean score jumped **38 → 65**, and a naive trend-tracker would shout "everything is intensifying." But t0 was **6/8 "aging" (recency 0.30)** and t1 is **6/6 "fresh" (recency 0.71–1.00)** — for the trivial reason that a run 3 weeks later gathers current-dated posts. The `value` composite multiplies in recency, so the score inflation is **mechanical**, not a real-world signal. Even the two SAME pains (near-correct 44→72, security 25→52) rise mostly because recency flipped aging→fresh; corroboration ticked up only within sampling variance (3→4 domains, 1→2 domains). **A trend feature reading these scores would systematically lie.**

2. **The count/granularity churn is the 4a noise signature, reproduced across time.** 4a proved that even *same-day, same-topic* re-runs turn over titles and framing almost completely and split coarse pains into fine ones (and vice-versa). Here: t1 merged t0#1+t0#3 into one "Ecosystem Fragmentation" pain, folded cost into "False Productivity," and 0/6 titles carried over. That is framing/granularity drift — the documented noise mode — not "3 pains got solved."

3. **The vanished & emerged pains are within the sampling envelope.** The 3 ABSENT pains are all **low-corroboration** (imp3, single-source or two-source) — exactly the unstable class 4a's within-run probe flagged. Their disappearance is consistent with a panel simply not re-sampling a thin source, not with resolution. The 2 EMERGED pains are strong (imp5, multi-domain, fresh) and *feel* like real 2026-mid backlash themes (r/antiai) — **but from n=1 interval we cannot separate "newly real" from "t0's panel didn't sample r/antiai and t1's did."** Critically, a human reading the two ledgers side-by-side spotted "skill-atrophy discourse emerged" **for free** — the PM3 *machinery* is not required to get that insight, which undercuts its keep-its-keep argument.

**What DID hold up (and it matters):** the **two-stage matcher itself worked**. It cleanly resolved 2 SAME / 3 RELATED / 3 ABSENT with sensible judge reasons, and **correctly rejected all 3 cheap-signal (lexical-top-1) false candidates** (T0#4/#6/#7 → DIFFERENT) — 3-for-3, consistent with 4a's 8-for-8 complementarity result. So cross-run pain **identity** is reliably establishable. That validates *matching/dedup*, which is separable from the *trend* claim.

**The honest noise-floor caveat:** the cleanest noise control would be a same-time replicate (t1′) to measure run-to-run variance directly; we didn't run one (another ~$6.81). **4a is the proxy noise floor** (same-day A/B → high surface variance, ~1 clean duplicate), and it is enough to conclude this single 3-week interval's movement does not exceed it.

## §6 — KILL vs RESCOPE (the one open decision)

- **Not GO.** The headline value of PM3 — *watch pains rise/fall over time and have that mean something* — is **not** shown to exceed noise on this interval, and the score axis it would surface is a recency artifact. Building the trend-labeling machinery (velocity into ledger + dashboard trend slot) on this premise is exactly the momentum trap the $0 gate exists to catch.
- **KILL (primary):** close PM3-as-specified. The gate did its job cheaply.
- **RESCOPE (contingent, Sean's call):** the matcher is a real asset and *novelty-detection* ("what is genuinely new since last run vs a repeat") has value **if Sean actually re-runs same-topic discovery often enough** to want it automated. If discovery is mostly one-off across *different* topics (the current pattern — t0/t1 were a deliberate experiment, not organic re-runs), automated same-topic persistence has little real use and RESCOPE collapses back to KILL. That contingency is Sean's information, so it's surfaced as a decision, not decided here.

## Implications
- **Phase 2 closes** without building the full persistence spec. Do NOT build `docs/superpowers/specs/2026-07-09-pm3-persistence-design.md` as-is.
- **Phase 3** (paid, was gated behind Phase 2) is now next for a future session: E5 (decouple from one machine) · D5 (interactive triage) · PM1+PM5 (gate scorecard as brand + packaging) · Step F buyer conversations (the paid wedge, red-team #2/#3).
- **Incidental win:** diagnosing the blocked run surfaced + fixed a **fleet-blocking OpenRouter bug** (`max_price` on `openrouter:fusion` → HTTP 500). Fix shipped separately (§7).

## §7 — Incidents captured (see `vault/00_inbox/tickets.md`)
1. **OpenRouter `max_price` fusion 500 (fixed).** Attaching a `max_price` provider filter to the `openrouter:fusion` tool now 500s (confirmed by A/B on an otherwise-identical body; t0 ran fine with it on 6/30 → provider-side change). Scoped fix in `council/discovery/fusion.py::_build_body` (drop `max_price` for the fusion call only; cost safety preserved by model-pinning + `max_tool_calls` + enforced F8b ledger caps). Tests updated; full suite 745 pass / 1 skip. Blocked ALL paid discovery until fixed.
2. **Cost overshoot ($6.81 vs $1.85, 3.7×).** Likely dominated by fusion server-side web-tool spend (never bounded by `max_price`; capped only by `max_tool_calls=5` × 3 panelists). Consider lowering `max_tool_calls` for standard tier or adding a fusion-compatible cost bound. Under the $30/day cap, so not a breach — but a real efficiency regression to investigate.
3. **Ledger reservation reconcile question (F8b).** `council-spend-2026-07-22.json` `total` reads **$17.25** = 4 × $4.31 worst-case *reservations*, while `actuals` settled ~$6.84. Failed-run reservations don't appear released. If the daily-cap check reads `total`, stale reservations over-consume headroom. Flag for the F8b owners.
