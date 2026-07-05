---
title: "Receipts / provenance UI patterns for evidence-backed claims (D2)"
date: 2026-06-29
topic: fusion-discovery-council / D2 receipts UI
status: salvaged
method: deep-research skill ($0, Anthropic subscription); verify stage rate-limited mid-run, salvaged from completed transcripts + 8 cleanly-confirmed claims
tags: [discovery-council, provenance-ui, trust-ux, evidence-grading, research]
---

# Receipts / Provenance UI — what the field already knows

**Decision this informs:** D2 adds a compact "receipts" line to each ranked card in the
fusion-discovery-council ledgers (PM + substack). Every card already passed the
anti-fabrication gate, so a binary "✓ verified" stamp says nothing. The receipt must
communicate the **gradient** — how *deeply* evidenced, how *fresh* — without manufacturing
false precision. This note grounds the tier vocabulary and thresholds in prior art.

**Run note (salvage):** the deep-research harness's adversarial-verify stage fanned out
~50 verifier agents and tripped transient Anthropic-side rate-limiting, which aborted the
final synthesis (the documented D4 failure mode — see the master continuation prompt).
Per the salvage lesson I did **not** re-run (same wall, ~2.5M tokens). 8 claims confirmed
cleanly (3-0 / 2-0 votes) before the storm; the rest were killed by *abstention*
(rate-limit), not refutation. The threshold specifics below are hand-vetted from the
completed Search/Fetch transcripts. 23 sources fetched, 90 claims extracted, 25 verified.

---

## Finding 1 — Corroboration tiers have established prior art; the line is "two sources"

**Confidence: HIGH** (multiple independent confirmations: journalism two-source rule +
NATO Admiralty credibility scale, both 3-0 confirmed or directly quoted in fetch transcripts).

- **Journalism's two-source rule:** "a fact isn't entirely credible unless it can be
  verified by two sources" — i.e. **one source = below the corroboration threshold, two =
  corroborated.** (communicationclamor.wordpress.com/2014/01/09/the-two-source-rule/)
- **NATO/Admiralty information-credibility scale (1-6):** the **top** tier (1 = "Credible
  and verified") is reserved for *"Multiple independent and trusted sources confirm"*;
  tier 3 ("Possibly True") explicitly *"lacks corroborating evidence."* So "multiple
  independent sources" is the documented bar for the top corroboration tier.
  (sans.org/blog/enhance-your-cyber-threat-intelligence-with-the-admiralty-system — 3-0)
- **Intelligence-community analytic confidence (High/Moderate/Low):** the lever separating
  the tiers is *corroboration depth* — High = "multiple sources" with "minimal conflict";
  Low = "scant, questionable, fragmented, or **poorly corroborated**." Single-source maps
  to a lower tier by definition. (cisecurity.org WEP/analytic-confidence — 3-0)

**How this changed the build:** the corroboration ladder reads off our gate-truth
`distinct_domains` count (domains = independent-publisher proxy; already weighted 0.7 vs
0.3 over sources in `scoring.py`):
- **1 domain → `single-source`** (below the two-source bar)
- **2 domains → `corroborated`** (meets the rule)
- **3+ domains → `well-corroborated`** (Admiralty "multiple independent")

## Finding 2 — Do NOT add tiers above "well-corroborated" (anti-false-precision)

**Confidence: HIGH** (primary empirical source; killed only by rate-limit abstention, not refuted).

A Cornell/AAAI study on citations and trust found **no significant trust difference between
one citation and five** (one-way effect F(2,3037)=10.23, p<.001 for ≥1 vs 0, but the
1-vs-5 contrast was non-significant) — attributed to diminishing returns. Worse, the *mere
presence* of citations raised trust even when the citations were **random/irrelevant**
(β≈0.39, p<0.01) — a "trust-washing" effect. (arxiv.org/pdf/2501.01303)

**How this changed the build:** the ladder **caps at 3+ ("well-corroborated")** — no
"very-well-corroborated" tier for 5/8 domains, because the evidence says higher counts
don't buy real trust and risk false precision. This is *consistent with* but distinct from
`scoring.DOMAIN_CEIL=4` (the continuous-score saturation point) — the label threshold is
the two-source rule, the score ceiling is saturation. Documented so they don't drift.

## Finding 3 — Binary "verified" is meaningless; raw confidence floats are an anti-pattern

**Confidence: HIGH** (two primary empirical sources).

- **Citation hallucination runs 11–57%** across deployed models, and factual support of a
  cited claim is only **39–77%** even when **link validity is 94–100%** and topical
  relevance 80–95%. A "cited"/"verified" stamp passes for nearly everything while many
  items fail substantive verification. (arxiv.org/html/2605.06635v1)
- A **raw numeric confidence** (e.g. "0.73") is an anti-pattern: users misread it as
  percent-correct, producing false precision; miscalibrated confidence *actively* degrades
  appropriate reliance (users can't detect miscalibration — 64–67% rate over/under-confident
  AI as "well-calibrated"). (authoritytech blog; arxiv.org/pdf/2402.07632)
- Every credible grading system uses an **ordinal gradient with named tiers**, never a
  binary: GRADE (High/Moderate/Low/Very-low — 3-0), analytic confidence (High/Mod/Low),
  Admiralty (A-F × 1-6), WEP verbal-probability bands.

**How this changed the build:** the receipt uses **qualitative words, not a checkmark and
not a float.** The existing `Confidence:`/`Size:` detail lines keep the floats as the
auditable trail; the receipt is the human-readable headline judgment above them.

## Finding 4 — Recency is a freshness signal, not a truth signal

**Confidence: MODERATE** (design-system practice + one blog threshold; the "old ≠ wrong"
principle is well-attested across PatternFly/Cloudscape relative-timestamp guidance).

- Design systems (PatternFly, Cloudscape) render **relative time as the surface, exact
  timestamp on hover/drill-down**, and a stale timestamp should still read as the real
  time — staleness is shown, never hidden, and never implies the content is *wrong*.
- A content-freshness scoring example applied a staleness **penalty** past a threshold
  (`if freshness_days > 365: score -= 0.15`) — staleness lowers a *freshness* score, not a
  *truth* score. (authoritytech.io/blog/content-freshness-seo-ai-2026)

**How this changed the build:** badges reuse our existing decay (`recency = 0.5^(age/30)`,
floored at `RECENCY_FLOOR=0.3`) — no parallel constants:
- **`recency ≥ 0.5` AND date present → `fresh`** (≤ ~1 half-life; this is *already*
  `frame._why_now`'s "Fresh signal" cutoff — the discoverable existing threshold)
- **`0.3 < recency < 0.5` → `recent`**
- **`recency ≤ 0.3` (floor) → `aging`** (+ one-time "old ≠ wrong" caveat)
- **`evidence_date == "" → `undated`** — the honesty trap: unparseable dates get
  `recency = RECENCY_NEUTRAL = 0.5`, so a naive `≥0.5` test would falsely badge them
  "fresh." The badge gates on **date-present first**. (Explicit test case.)

---

## Net design rules folded into the D2 spec

1. Receipt = **two evidence-grounded axes**: corroboration tier (off `distinct_domains`) +
   freshness badge (off `recency`/`evidence_date`). Model consensus stays in the detail line
   (it's model-agreement, a different axis — and adding a third number risks false precision).
2. **Words, never a checkmark, never a float** in the receipt.
3. Corroboration ladder caps at 3+ (`well-corroborated`); no higher tier.
4. **`undated` ≠ `fresh`** — gate on date-present before the recency test.
5. One-time legend (D4-style), not per-card noise: gate-survival is assumed; corroboration =
   evidence breadth (two-source rule); freshness = recency, not proof; old ≠ wrong.

## Sources (salvaged; quality per harness)
- sans.org Admiralty system — *primary*, 5 claims (corroboration tiers, two-axis separation)
- cisecurity.org WEP / analytic confidence — *primary*, 5 claims (confidence-as-gradient)
- cdc.gov ACIP-GRADE handbook ch.7 — *primary*, 4 claims (4-tier certainty gradient)
- arxiv 2501.01303 (Cornell/AAAI, citations & trust) — *primary*, 5 claims (1-vs-5, trust-washing)
- arxiv 2402.07632 (confidence miscalibration) — *primary*, 5 claims (false-precision harm)
- arxiv 2605.06635 (deep-research citation support) — *primary*, 4 claims ("verified" is meaningless)
- arxiv 2303.12118 (provenance & accuracy judgments) — *primary*, 4 claims
- communicationclamor — *blog*, two-source rule
- patternfly.org / cloudscape.design timestamp guidelines — *primary*, relative-time + staleness honesty
- authoritytech.io content-freshness 2026 — *blog*, staleness-penalty threshold
- kravensecurity.com / blockint.nl Admiralty critique — *secondary* (corroboration-count ambiguity caveat)
