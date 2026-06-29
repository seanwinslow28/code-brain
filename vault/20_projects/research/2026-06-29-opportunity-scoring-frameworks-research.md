---
title: Opportunity-scoring frameworks — how mature systems score pain from evidence
date: 2026-06-29
status: complete
tags: [research, discovery, fusion-discovery-council, scoring, product-discovery]
method: deep-research harness (5 angles → 20 sources → 86 claims → 25 verified, 3-vote adversarial)
informs: PM4+D1 (tools/llm-council/council/discovery/scoring.py)
---

# Opportunity-scoring frameworks — research synthesis

**Question:** How do mature product-discovery, opportunity-scoring, and Voice-of-Customer / review-mining systems compute a defensible composite priority score for a user pain point from evidence — and does that validate or correct a 4-component composite (importance · reach · recency · corroboration, weights 0.35/0.30/0.15/0.20)?

**Bottom line:** The component *choice* is validated by the canonical frameworks. The two corrections worth making: (1) reach must be non-linearly damped (we already did this), and (2) confidence/corroboration should **multiply** the value rather than add as a 4th term — and model-consensus must be kept separate from independent-source breadth to avoid the single-source illusion. Result: we moved to a RICE-style `value × confidence` architecture.

## Findings (verified, 3-0 unless noted)

1. **Component choice validated** [high]. ODI (Ulwick/Strategyn): `Opportunity = Importance + max(Importance − Satisfaction, 0)` — double-weights importance, floors the gap at 0 so over-served outcomes don't penalize; Importance/Satisfaction are **top-box proportions** (% high responses), not raw means. RICE (Intercom/Sean McBride): `(Reach × Impact × Confidence) / Effort` = "total impact per time worked." Both use importance/intensity, reach/frequency, confidence.

2. **RICE normalizes asymmetrically — by design** [high]. Impact = fixed discrete ordinal (3/2/1/0.5/0.25), Reach = raw count over a timeframe, Confidence = probability-style multiplier (100/80/50%) that **discounts** the numerator for uncertainty ("curb enthusiasm for exciting but ill-defined ideas"). Template: bounded intensity vs unbounded reach (needs damping) vs confidence-as-discount each normalize differently.

3. **Reach MUST be non-linearly compressed** [high, verified against Reddit source]. Engagement is extremely heavy-tailed (top 1% of accounts ≈ 97% of upvotes). Reddit "hot" (`_sorts.pyx`): `order = log10(max(abs(ups-downs), 1))` → first 10 upvotes ≈ next 100 ≈ next 1000. ARWU (bibliometrics): sqrt compression for skewed citation/award distributions. **A raw upvote count in the reach component is the documented failure mode.**

4. **Naive reach sorting fails two ways → Wilson lower bound** [high, Evan Miller]. (a) net = pos−neg lets high-volume outrank quality (1000-net/55% beats 200-net/60% — WRONG); (b) raw average lets tiny samples win (2/2 beats 100/101 — WRONG). Fix: lower bound of the Wilson score interval — "the real positive fraction, at least, given the evidence." Directly motivates separating model-consensus from independent-source count and discounting thin evidence.

5. **Recency = exp decay, smallest weight + floor** [medium]. `W = e^(−λt)` confirmed; the named failure mode is over-emphasizing recent data and discarding still-valuable older signal ("recency bias / whack-a-mole" — corroborated by Amplitude, Productboard, Culture Amp). Justifies recency as the smallest weight and a floor.

6. **Composite indicators: false precision + non-neutral weights** [high, peer-reviewed]. Frontiers RMA 2026 + OECD/JRC Handbook: compressing heterogeneous components into one scalar over-interprets small differences and loses construct validity; the normalization method AND weight allocation **materially change rankings**. → weights/damping must be **explicitly justified and sensitivity-tested, not asserted**; show the breakdown.

7. **Goodhart: pair quality+quantity, don't make the composite the target** [medium]. Pairing an importance (quality) component with a reach (quantity) component is the standard anti-gaming defense — necessary but not sufficient; damping is a separate required mechanism. The composite must stay one input, not the sole optimization target.

## Refuted (excluded)
- ❌ "Importance/Satisfaction are raw 1–10 scales" — they are top-box proportions.
- ❌ "ODI uses thresholds >12 strong / <8 low" — no canonical basis.

## Open questions (deferred to E3/PM3)
- Which exact damping transform for reach (log10 / sqrt / percentile / Wilson) per signal type?
- Should corroboration use a Wilson/Bayesian lower bound on independent source count, with a minimum-source floor? (We used a saturating ratio for now.)
- Decay λ per pain type (durable structural vs transient incident)?
- Full weight sensitivity-testing.

## How this changed the build (PM4/D1)
- Architecture → **`composite = 100 × value × confidence`** (RICE pattern), value = weighted(importance, reach, recency); confidence = independent-source corroboration + model-consensus (separate, lightly weighted), floored at 0.5 so a single-source pain is halved not zeroed.
- Reach keeps `log1p/log1p(CEIL)` damping (finding 3/4).
- Recency stays smallest weight (0.15) + floor 0.3 (finding 5).
- Weights are tunable constants, flagged for sensitivity-testing (finding 6); the card renders the full breakdown, not a black-box number (findings 6/7).

## Sources (20 fetched)
- ODI: https://en.wikipedia.org/wiki/Outcome-Driven_Innovation · https://strategyn.com/outcome-driven-innovation/market-opportunity/ · https://marketingjournal.org/the-path-to-growth-the-opportunity-algorithm-anthony-ulwick/ · https://medium.com/@AlexJupiter/outcome-driven-innovation-3377252aec15 · https://roadmap.one/blog/posts/blog8-8-opportunity-scoring/ · https://medium.com/uxr-microsoft/what-is-the-opportunity-score-and-how-to-obtain-it-bb81fcbf79b7
- RICE: https://www.productplan.com/glossary/rice-scoring-model · https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
- Reach damping / ranking: https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9 · https://www.evanmiller.org/how-not-to-sort-by-average-rating.html · http://www.righto.com/2013/11/how-hacker-news-ranking-really-works.html · https://redaccs.com/reddits-ranking-algorithm/ · https://upvote.net/blog/reddit-algorithm · https://www.frontiersin.org/journals/research-metrics-and-analytics/articles/10.3389/frma.2026.1828850/full
- Recency: https://customers.ai/recency-weighted-scoring · https://fastercapital.com/content/Recency-Bias--Recency-Bias-in-Data-Mining--The-New-Overpowers-the-Old.html
- VoC / review-mining / triangulation: https://www.revenuecat.com/blog/growth/review-mining-for-subscription-apps/ · https://qualz.ai/blog/research-triangulation-product-decisions/ · https://www.saber.app/glossary/multi-signal-scoring
- Critiques: https://kpitree.co/guides/frameworks/goodharts-law · https://www.nature.com/articles/s41562-025-02385-1
