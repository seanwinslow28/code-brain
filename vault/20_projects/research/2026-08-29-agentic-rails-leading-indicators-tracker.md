---
title: "Agentic-rails leading-indicators tracker"
date: 2026-08-29
project: agentic-web-startup
type: research-tracker
status: active
cadence: monthly-manual (recommended, unratified)
tags: [agentic-web, odlyzko, leading-indicators, rails-timing, tracker]
---

# Agentic-rails leading-indicators tracker

Extends the [Odlyzko-check verdict](2026-08-29-agentic-rails-odlyzko-check.md): the
verdict's six indicators whose crossing would reopen the rails-timing question, plus
two ratified additions (7: EDGAR filing-language transition; 8: measurement-series
health — ratified by Sean 2026-08-29), each with an
authoritative series, a re-verified baseline, a threshold, and a $0 checking recipe
runnable in under 10 minutes. **Designed to be re-run and appended to** — add a dated
row to each indicator's log on every check; never overwrite a prior reading.

Evidence discipline: every number tagged [independent]/[vendor]/[derived]. Research
run 2026-08-29 evening by three parallel agents (WebSearch/WebFetch; one deviation —
SEC EDGAR requires `curl` with a declared User-Agent, still $0/read-only). Provenance
ledgers at the bottom of each agent's section notes; fetched-vs-snippet distinctions
carried inline.

> **Standing rule carried over from the council pre-mortem:** this historical/timing
> work is a **filter on what not to build, not a territory warrant**. A crossed
> indicator reopens a question; it doesn't answer it.

## ⚠ Correction to the verdict's x402 baseline (found during re-verification)

The verdict states "the entire x402 economy settles ~$24M/month nominal … organic
≈ $10–15M/month." On-chain re-verification says that was **~20x too high**:

- Dune `thechriscen` x402 dashboard [independent, fetched]: **lifetime cumulative
  settlement $41.37M** (Oct 2025 → Aug 2026), 164.5M tx. Monthly flows implied by the
  cumulative series: Nov-2025 ~$20.5M (peak) → Jan-2026 ~$1.2M → **Feb–Aug 2026
  combined ~$6M (~$0.85M/mo average)** [derived from fetched cumulative].
- Cross-checks agree: agenteconomy.to [independent, fetched 2026-08-29] cumulative
  $41.49M (within 0.3% of Dune); Helios via CryptoPotato [derived]: 7-day avg
  ~$41.8K/day ≈ **$1.25M/mo run-rate**.
- The "$24M in 30 days" figure (CoinDesk, Jul 2026) is inconsistent with the lifetime
  $41M total and is almost certainly a misread of the **$24.77M
  cumulative-through-November-2025** waypoint. Lifetime avg tx ≈ $0.25, not $0.32–0.52.
- **Corrected baseline: nominal ~$0.9–1.3M/month; organic (~50% haircut, Artemis)
  ≈ $0.5–0.7M/month.** The >$100M/mo organic threshold is therefore ~150–200x above
  current reality, not ~10x. The correction *strengthens* the verdict's direction while
  fixing its magnitude. A dated addendum has been added to the verdict doc.

---

## Indicator 1 — ACP / ChatGPT Instant Checkout GMV disclosure

**What fires it:** any party states agent-originated GMV, order counts, or ACP
transaction volume in dollars/units. Relative multipliers ("orders tripled YoY") do
NOT count — they are the pre-signal and are already flowing.

**Series:** none exists — the disclosure event IS the signal. Venues to scan, in order
of likelihood: Stripe newsroom + annual letter (~Jan–Feb, [vendor]); OpenAI
news/DevDay ([vendor]); Shopify quarterly earnings (next: Q3, ~early Nov 2026,
[vendor]); Etsy and PayPal earnings ([vendor]); business press forcing a number
(CNBC, The Information, Modern Retail — [independent]-ish).

**Baseline 2026-08-29 (re-verified): absence holds — 11 months post-launch, zero
disclosure from any party.**
- Stripe newsroom scanned [vendor, fetched]: nothing on ACP volume through Aug 25 2026.
- Stripe's own 2025 annual letter grades agentic commerce at the "edge of levels 1 and
  2" of its five-level maturity ladder [derived, snippet] — a vendor self-grading
  pre-volume.
- Shopify Q2-2026 call [vendor, fetched transcript]: Finkelstein verbatim — "the
  volume from agentic commerce is still small relative to our massive GMV." Relative
  metrics only.
- The deprioritization claim is now **confirmed, well-sourced**: OpenAI scaled back
  Instant Checkout in March 2026 toward discovery + merchant-owned checkout —
  CNBC Mar 24 2026 (URL verified, fetch 403'd, [derived]) + Modern Retail
  [independent, fetched], which also carries the only party-attributed conversion
  number anywhere: Walmart's Daniel Danker, in-chat checkout conversion "three times
  lower" than clickthrough. Notably no primary OpenAI blog post exists — the pivot was
  announced quietly via statements to press [finding].

**Recipe (<10 min):**
1. WebFetch `https://stripe.com/newsroom` — scan for ACP/Instant Checkout + volume language.
2. WebSearch `"Instant Checkout" GMV` and `OpenAI ChatGPT shopping GMV disclosed` (last quarter).
3. WebSearch `Shopify Q<latest> earnings "agentic" transcript` → fetch fool.com
   transcript → has "small relative to GMV" become a dollar figure?
4. WebSearch `Etsy earnings agentic ChatGPT app sales`.
5. Annually: fetch `https://stripe.com/annual-updates/<year>` — did the maturity-level
   self-grade move, and is there a volume number?

**Log:**
| Date | Reading | Notes |
|---|---|---|
| 2026-08-29 | NOT FIRED | Absence re-verified across Stripe/OpenAI/Shopify/Etsy; deprioritization confirmed |

---

## Indicator 2 — Agentic-GMV line item in any GAAP filing

**What fires it:** a quantified agentic revenue/GMV figure in a 10-K/10-Q. Risk-factor
and strategy mentions do not count (they are now widespread and expected).

**Series:** SEC EDGAR full-text search [independent], near-real-time. Working
endpoint (verified): `https://efts.sec.gov/LATEST/search-index?q=%22agentic+commerce%22&forms=10-K,10-Q`
— returns JSON; **requires a User-Agent header** (`curl -A "name email"`); bare
WebFetch gets 403. Human UI: `https://www.sec.gov/edgar/search/#/q=%22agentic%20commerce%22&forms=10-K` (JS).

**Baseline 2026-08-29 (re-verified): zero quantified line items.** [independent, fetched]
- `"agentic commerce"` in 10-K/10-Q: **45 hits** (Visa, Amex, Mastercard, PayPal,
  Shopify, Etsy, Capital One, et al.) — all narrative/risk-factor. All-forms: 265.
- `"agentic commerce revenue"`: **0**. `"agentic GMV"`: **0**. `"agent-initiated transactions"`: 2 (neither commerce-quantified).
- Spot-reads: Visa 10-K FY2025 is the most advanced (named products + "live agentic
  token transactions" pilot + dedicated risk factor — zero quantification); Etsy's own
  10-Q treats agentic purely as competition/fraud risk despite being the day-one
  Instant Checkout merchant [finding].
- Near-misses, neither a GAAP line item: Coinbase Q2'26 8-K deck quantifies agentic
  *market shares* ("99%+ of agentic stablecoin volume on Base", source Artemis —
  [derived] even inside the filing; no dollars); Rezolve AI 6-K claims "~$50M
  India-led TCV" with an explicit not-GAAP-revenue disclaimer.

**Recipe (<10 min):**
```
curl -s -A "sean.winslow28@gmail.com" "https://efts.sec.gov/LATEST/search-index?q=%22agentic+commerce%22&forms=10-K,10-Q"
```
1. Log `hits.total.value` (baseline **45**) — the mention-count trend is a free sub-series.
2. Repeat with `%22agentic+commerce+revenue%22` (baseline 0), `%22agentic+GMV%22` (0),
   `%22agent-initiated+transactions%22` (2). **Any nonzero on the first two → read the filing immediately.**
3. Add `&dateRange=custom&startdt=...&enddt=...` to isolate new filings since last check.
4. Check Coinbase's latest earnings deck (`q=%22agentic%22&forms=8-K`) — most likely
   first mover to a dollar figure.

**Log:**
| Date | Mention count (10-K/10-Q) | Quantified items | Notes |
|---|---|---|---|
| 2026-08-29 | 45 | 0 | Visa most advanced; Coinbase/Rezolve near-misses in 8-K/6-K |

---

## Indicator 3 — x402 organic settlement volume

**Threshold:** sustained **>$100M/month organic**. Corrected baseline: ~$0.5–0.7M/mo
organic — a ~150–200x gap (see correction block above).

**Series:**
- **Dune "x402 Payment Analytics" by `thechriscen`** [independent, community
  on-chain]: https://dune.com/thechriscen/x402-payment-analytics — cumulative USD
  volume, tx, buyers/sellers/facilitators; **renders to WebFetch** (bare
  `dune.com/queries/*` pages do NOT).
- Cross-check: https://agenteconomy.to/stats/x402-transactions [independent
  aggregator, hourly refresh, renders].
- Quality annotations (not series): Chainalysis blog Jun 3 2026 [independent, one-off
  — tx ≥$1 share grew 49%→95%; watch for their "The New Rails" report];
  Artemis ~50% artificial [independent]; `classic.artemis.ai/asset/x402` is JS-only
  and never renders — skip.

**Baseline 2026-08-29:** cumulative $41.37M / 164.5M tx / 711K buyer addresses / 348K
seller addresses / 18 facilitators [independent, fetched]; monthly flow ~$0.9–1.3M
nominal, organic ~$0.5–0.7M [derived]; avg tx ≈ $0.25 lifetime.

**Recipe (<10 min):**
1. WebFetch the Dune dashboard → read cumulative Volume USD → subtract last logged
   cumulative = month's nominal flow.
2. WebFetch agenteconomy.to stats page → confirm cumulative within ~1%.
3. Organic = nominal × 0.5 (Artemis haircut; revisit multiplier if a fresher
   decomposition appears).
4. Fire check: organic monthly flow > $100M sustained ≥2 months.

**Log:**
| Date | Cumulative USD | Implied monthly flow (nominal) | Organic est. | Notes |
|---|---|---|---|---|
| 2026-08-29 | $41.37M | ~$0.9–1.3M | ~$0.5–0.7M | Corrects verdict's $24M/mo (cumulative misread) |

---

## Indicator 4 — HUMAN Security checkout-touch share of live agentic traffic

**Threshold:** **>10%** sustained across ≥2 consecutive monthly editions.

**Series:** HUMAN Security "State of Agentic Traffic," Satori Threat Intelligence,
monthly blog [vendor telemetry, >1 quadrillion interactions/yr]. Editions confirmed:
Apr/May/Jun/Jul 2026; annual anchor: "2026 State of AI Traffic & Cyberthreat
Benchmark Report." **Access caveat: humansecurity.com hard-403s WebFetch site-wide**
(verified on 3 URLs) — all figures are search-snippet tier [derived/vendor]; page-level
verification needs an interactive browser.

**Baseline 2026-08-29:** flat at **2.3–2.6%** — 2025 full year 2.3%; May 2026 2.4%;
Jun 2.34%; **Jul 2.6%** [derived/vendor]. ~75–76% of agentic activity is
discovery/product/search. No August edition yet (series publishes month-N data in
month N+1; missing by mid-September = warning). Sub-shift: July was the first month
media (43.5%) overtook e-commerce (42.0%) in agentic-traffic share.

**Recipe (<10 min):**
1. WebSearch `site:humansecurity.com "state of agentic traffic"` — newest month.
   **Latest edition >6 weeks stale = discontinuation warning (itself a signal — see
   proposed Indicator 8).**
2. WebSearch `humansecurity "state of agentic traffic" checkout payment` — read the
   share % from snippets (don't waste time on WebFetch; 403 confirmed).
3. Fire check: >10% two consecutive editions. Current: 2.6%.

**Log:**
| Date | Latest edition | Checkout share | Notes |
|---|---|---|---|
| 2026-08-29 | Jul 2026 | 2.6% | Flat series Apr–Jul; Aug edition due ~early Sep |

---

## Indicator 5 — AI-referred share of e-commerce sessions

**Threshold:** ~**2–3%** of sessions. **Confirmed: nobody publishes the share
directly — it must stay [derived].** Verified against Adobe (growth % only),
Similarweb (platform market share + citation rates, not retail-referral share),
Cloudflare Radar (crawl-to-refer ratios, explicitly not share-of-traffic), TollBit
(bot visits, not referred human sessions).

**Series (growth proxy):** Adobe Digital Insights AI-traffic reports [vendor, >1T
visit panel], now ~monthly — venue business.adobe.com/blog + PDF assets; Digital
Commerce 360 reliably restates same-day and fetches cleanly.

**Baseline 2026-08-29:** share **<1–2% [derived]**, threshold not crossed. New since
the verdict: **July 2026 AI-referral traffic to US retail +62% YoY** [vendor via
DC360, fetched], cumulative +1,219% since Oct 2024, conversions +60%. The growth
curve is decelerating hard: +393% (Q1) → +269% (Mar) → +138% (May) → **+62% (Jul)** —
at these rates a 2–3% crossing in 2026 looks unlikely absent a step-change. Flag:
Adobe's cumulative index moved DOWN between reports (+1,324% through May → +1,219%
through July) — an unexplained restatement worth logging each check [finding].

**Derivation path:** anchor ~0.1–0.2% share (mid-2025, commercetools synthesis
[derived]) × subsequent Adobe YoY growth. Sanity-cap with Similarweb's global
"AI platforms ≈ 0.15–0.25% of internet traffic" [derived, snippet].

**Recipe (<10 min):**
1. WebSearch `Adobe Analytics AI traffic retail <month> <year>` → WebFetch the newest
   DC360 piece → log YoY %, cumulative %, conversion delta. Watch for Adobe ever
   printing an absolute share — that ends the [derived] era and fires a re-baseline.
2. Roll the derived share forward; log it as [derived] always.
3. Cross-checks: WebFetch `aisearch.similarweb.com/blog/gen-ai-stats/` (free,
   ~monthly); `radar.cloudflare.com/ai-insights` needs a browser (WebFetch 403).

**Log:**
| Date | Latest Adobe YoY | Derived share | Notes |
|---|---|---|---|
| 2026-08-29 | +62% (Jul) | <1–2% [derived] | Deceleration 393→269→138→62; cumulative-index restatement flagged |

---

## Indicator 6 — TollBit / Cloudflare pay-per-use payout disclosure

**What fires it:** a stated/audited **aggregate dollar payout total** from either
company (per-publisher brackets don't count).

**Series:**
- TollBit "State of the Bots" hub: https://tollbit.com/bots/ [vendor] — **cadence has
  slipped quarterly → semiannual** (two consecutive combined editions: "2025 Q3&Q4
  The Leaky Pipes," "2026 Q1&Q2 The Bad Bots"). Report bodies are form-gated; read
  via press coverage. TollBit blog archive fetches cleanly.
- Cloudflare Pay Per Use: blog.cloudflare.com [vendor]; ppc.land tracks it closely
  and fetches cleanly [independent].

**Baseline 2026-08-29: not fired — zero dollars from either.**
- TollBit blog scanned through 2026-08-03 [fetched]: no payout post ever. Closest
  disclosure is qualitative and *against* interest — CEO/team to Press Gazette
  [independent, fetched]: revenue "not going to make their year this year."
  Last two blog posts are about legislation, not monetization wins [finding].
- Cloudflare Pay Per Use: **buyer count still 2** (Ceramic.ai, You.com); "no pricing
  structure was disclosed for either" (ppc.land, fetched); Cloudflare calls it "an
  experiment."
- **New forcing function: Sept 15, 2026** — Cloudflare's deadline to default-block
  "mixed-use" AI crawlers from ad-carrying pages unless the AI company pays [derived,
  snippet]. Post-deadline coverage is the next likely venue for a first real dollar
  number.

**Recipe (<10 min):**
1. WebFetch `https://tollbit.com/blog/` — any payout/revenue disclosure post?
2. WebFetch `https://tollbit.com/bots/` — new edition beyond "2026 Q1&Q2"? Further
   cadence slip? (A skipped H2-2026 edition = going-silent signal.)
3. WebSearch `Cloudflare "Pay Per Use" payout OR partners OR pricing <month> 2026` +
   `site:ppc.land cloudflare pay per use`. Log buyer count (baseline 2).
4. After 2026-09-15: WebSearch `Cloudflare mixed-use crawler blocking results`.

**Log:**
| Date | TollBit payout | CF payout | CF PPU buyers | Notes |
|---|---|---|---|---|
| 2026-08-29 | none ever | none; pricing withheld | 2 | Sept-15 block deadline pending; TollBit cadence halved |

---

## Indicator 7 — EDGAR filing-language transition (risk-factor → quantified)

*Ratified by Sean 2026-08-29 (proposed and ratified same evening).*

**What it measures:** the diffusion of agentic commerce through SEC filings, and each
filer's individual transition from narrative/risk-factor language to numbers — the
early-warning system for Indicator 2. Absorbs the earnings-call language-shift
candidate: Shopify publishes relative multipliers every quarter (orders 3x YoY,
catalog conversion 2x, new-buyer orders 2x); the quarter any multiplier becomes a
dollar figure, Indicator 1 fires.

**What fires it:** (a) any filer moving from risk/strategy language to a quantified
agentic figure in a filing or earnings deck (even a non-GAAP one — Coinbase's
market-share slides and Rezolve's TCV claim are the current frontier); (b) a sharp
inflection in the mention count (baseline-doubling inside two quarters); (c) Shopify
(or any platform) converting its relative-multiplier series to absolute numbers.

**Series:** EDGAR full-text search [independent], same endpoint as Indicator 2 —
zero marginal cost, run in the same curl session. Companion venues: Shopify/Etsy
quarterly transcripts (fool.com fetches cleanly), Coinbase earnings decks
(`q=%22agentic%22&forms=8-K`).

**Baseline 2026-08-29:** 45 "agentic commerce" hits in 10-K/10-Q (265 all forms);
0 quantified. Per-filer frontier: Visa most advanced (named products + live-pilot
claim + dedicated risk factor); Coinbase quantifies third-party market shares in 8-K
decks; Rezolve quantifies non-GAAP TCV with a disclaimer; Etsy — the day-one
Instant-Checkout merchant — mentions agentic only as competition/fraud risk.
Shopify multiplier set (Q2-2026): AI traffic/orders 3x YoY, catalog-conversion 2x,
new-buyer 2x, 75% of AI-attributed orders outside top-100 categories.

**Recipe (<5 min, piggybacks on Indicator 2's curl):**
1. From Indicator 2's queries, log the 10-K/10-Q mention count and the all-forms count.
2. Diff the filer list against the last log row — for each NEW filer, grep ±300 chars
   around "agentic": classify risk-factor / strategy / quantified.
3. `q=%22agentic%22&forms=8-K` — check Coinbase's (and any newcomer's) latest deck
   for dollar figures replacing market-share percentages.
4. Quarterly: log Shopify's multiplier set from the earnings transcript; note any
   multiplier that became a dollar.

**Log:**
| Date | 10-K/10-Q mentions | All forms | Quantified filers | Frontier notes |
|---|---|---|---|---|
| 2026-08-29 | 45 | 265 | 0 | Visa furthest; Coinbase 8-K shares; Rezolve TCV; Shopify multipliers 3x/2x/2x |

---

## Indicator 8 — measurement-series health (meta-indicator)

*Ratified by Sean 2026-08-29 (proposed and ratified same evening).*

**What it measures:** the tracker's own instruments. A vendor that stops publishing a
flattering series usually stopped because it stopped flattering — so the death,
cadence slip, methodology restatement, or silent disappearance of any watched series
is evidence in its own right, in either direction (a series discontinued while
flat-lining reads as capitulation; one discontinued mid-acceleration reads as
strategic withholding).

**Watched series and their health baselines (2026-08-29):**
| Series | Publisher | Expected cadence | Health status | Stale-alarm |
|---|---|---|---|---|
| State of Agentic Traffic | HUMAN Security [vendor] | monthly | OK — latest Jul 2026 (Aug due ~early Sep) | >6 weeks without a new edition |
| State of the Bots | TollBit [vendor] | quarterly → **already slipped to semiannual** | DEGRADED — two consecutive combined editions | a skipped H2-2026 edition = gone-silent signal |
| AI-traffic reports | Adobe [vendor] | ~monthly | DEGRADED — unexplained cumulative restatement (+1,324% → +1,219%) | restatement without methodology note, or >2 months silent |
| x402 dashboards (Dune `thechriscen` + agenteconomy.to) | community [independent] | live | OK — mutually consistent within 0.3% | either dashboard 404s or diverges >5% from the other |

**What fires it:** any row hitting its stale-alarm, a series being formally
discontinued, or a second unexplained restatement in the same series. A firing here
doesn't reopen the rails-timing question by itself — it degrades or upgrades the
confidence of the indicator that depends on the affected series, and the
*circumstances* of the death are the datum to record.

**Recipe (~2 min, runs implicitly with recipes 3–6):** while executing Indicators
3–6, fill in this indicator's log row: latest-edition date per series, any cadence
or methodology change, and the Dune-vs-agenteconomy divergence %. **Always log the
x402 cumulative USD in Indicator 3's row** so a dead dashboard can't orphan the
series history.

**Log:**
| Date | HUMAN latest | TollBit latest | Adobe latest | x402 dashboards | Notes |
|---|---|---|---|---|---|
| 2026-08-29 | Jul 2026 | 2026 Q1&Q2 "The Bad Bots" | Aug 19 (Jul data) | both live, Δ0.3% | TollBit cadence halved; Adobe restatement flagged |

---

## Secondary candidates (log-only unless ratified)

Ratification record: Indicators 7 and 8 were proposed here 2026-08-29 and ratified by
Sean the same evening — promoted to full sections above.

**Still log-only:** a second Etsy-class
integration exit or a contradicting success (Walmart's "3x lower conversion" is the
one to watch); Cloudflare's Sept-15 enforcement outcome (dated binary event); x402
unique-counterparty monthly deltas (harder to farm than volume); Adobe's YoY
deceleration slope itself; robots.txt bypass rate (TollBit: 3.3% → ~13%); publishers'
direct-licensing norm (4–5 LLM partners) substituting for per-crawl tolls.

---

## Cadence recommendation (recommendation only — no automation wired)

**Monthly manual re-check, ~30–40 min, first business day of the month.** The eight
recipes are each <10 min and several are <2 min (EDGAR curl, Dune fetch; 7 piggybacks
on 2's curl session and 8 runs implicitly with 3–6, so the additions cost ~5 extra
minutes); monthly
matches the fastest-moving series (HUMAN, Adobe) and is well ahead of every
threshold's realistic crossing speed — the widest gap is ~2 orders of magnitude
(Indicator 3) and the narrowest ~4x (Indicator 5, decelerating). Two async
date-triggered extras: mid-September (HUMAN August edition present? Cloudflare
Sept-15 outcome?) and early November (Shopify Q3 call).

A fleet-agent design is feasible (the recipes are deliberately mechanical: fixed
URLs, fixed queries, numeric thresholds, append-a-row output) but is **not wired and
not recommended yet** — per the standing agent-downsizing rule, new schedules need
Sean's explicit approval, and one manual cycle should validate the recipes before any
automation conversation.

## Provenance

- Ordered via [docs/prompts/2026-08-29-leading-indicators-and-loose-ends-continuation.md](../../../docs/prompts/2026-08-29-leading-indicators-and-loose-ends-continuation.md).
- Extends: [Odlyzko-check verdict](2026-08-29-agentic-rails-odlyzko-check.md) + its
  evidence pair; standing rule from the
  [council pre-mortem](2026-08-29-tech-revolution-patterns-council-premortem.md).
- Research: three parallel agents, 2026-08-29 evening, $0. Fetched-URL ledgers
  summarized inline per indicator; key fetched primaries: Dune thechriscen dashboard,
  agenteconomy.to, efts.sec.gov (6 query variants), Visa/Shopify/Etsy/PayPal filings,
  Coinbase Q2'26 deck, Rezolve 6-K, stripe.com/newsroom, fool.com Shopify Q2
  transcript, modernretail.co Instant-Checkout post-mortem, chainalysis.com x402 blog,
  cryptopotato.com Helios piece, tollbit.com blog+bots hub, pressgazette.co.uk,
  ppc.land, digitalcommerce360.com (Jun+Aug Adobe pieces),
  aisearch.similarweb.com, blog.cloudflare.com crawl-refer post.
- Known fetch-blocked venues (plan around them): humansecurity.com (403 site-wide),
  openai.com/news (403), cnbc.com (403), radar.cloudflare.com (JS),
  classic.artemis.ai (JS), fastcompany.com (403), business.adobe.com (timeouts) —
  use the named secondary venues in each recipe.
