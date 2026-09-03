# Completion Index — Build Kickoff (founded 2026-09-01)

Kickoff prompt for the build phase of the agentic-web company founded in the
2026-08-29 partner session (`~/.creative-harness/partner-sessions/2026-08-29-agentic-web-startup.md`,
locks [L10]–[L13]). Run in a fresh session; expect to use `/wayfinder` for the
ticket map and `/systemcraft` for the artifact chain (PRD → ADR → eval plan →
ops model). Research-before-build discipline carries from 8/07.

## What the company is

**The completion index — the measurement authority for the agent web.**
Sean's multi-model agent fleet (frontier closed + mid + local open-source)
runs real AI agents against real websites' money journeys on a monthly
cadence, measures whether they can COMPLETE them, and publishes the
longitudinal public index. Nobody publishes completion measurement (verified
void, survived falsification 2026-08-30: Agent Checker sells one-off audits,
Vercel gives away checks, Stiplo is hotels-only — no funded horizontal
bundler, no longitudinal publisher). Being early is the moat: 2026 baselines
cannot be back-filled. Monetization is gated by the leading-indicators
tracker (`vault/20_projects/research/2026-08-29-agentic-rails-leading-indicators-tracker.md`),
never by the success criterion.

Named future expansions the index itself will scope: agent-facing data
distribution (the fitment void) and agent-first reference storefront/template.
Parked cash-flow option: the correction workflow + "Monday Problem" exemplar.

## Success criterion ([L12], mark 2027-03-01, miss two of three → pivot review)

- **(a) Index leg:** public index live, ≥25 real sites × ≥3 consecutive
  monthly cycles, plus outside pull (≥1 unsolicited citation OR ≥100
  subscribers OR ≥1 serious inbound — buyer, partner, or employer).
- **(b) Autonomy leg (PRIMARY):** fleet runs a full monthly cycle end-to-end
  (probe → judge → draft report) with evals governing quality, Sean ≤10
  hrs/week ops, ≥30 consecutive days.
- **(c) Public leg:** build-log weekly.

## v0.1 shape ([L13] — do not widen)

Consent-tier hybrid: ONE category × ~10 real sites × 3 agent stacks × ~5
read-safe canonical journeys (find product, price, availability/hours,
shipping/return policy, add-to-cart) PLUS 2-3 consenting/demo/owned
properties probed to actual checkout completion. Public report separates the
tiers explicitly.

**Ethics constraint is constitutive ([L13] verbatim intent: "We don't want
any situation where we can be flagged or considered harmful"):** on
non-consenting real sites probes are read-safe only — no form submissions
that create fake leads, no real purchases, no load burden (rate-limit,
respect robots where applicable, identify the probe agent honestly where
feasible). Full depth only with consent. The transparent methodology page is
both the ethical floor and the moat.

## What the build kickoff must produce

1. **Wayfinder map** (GitHub issues, `seanwinslow28/code-brain` or a new
   repo — decide repo home first; company code does NOT live in code-brain
   per the driftgate precedent of a separate repo).
2. **Systemcraft chain for the harness:** PRD, ADR set (incl. groundwork
   adoption question — consume-as-is like driftgate did, or lighter), eval
   plan (Arize/Phoenix tracing from probe one; LLM-as-judge grading of
   journey outcomes with human-in-the-loop calibration), ops model
   (monthly-cycle runbook).
3. **Category + site panel** — picked WITH Sean (compatibility-heavy retail
   is the standing lean, tying to the fitment expansion); consent-tier
   properties identified (WebMCP demo-shop lineage, an owned test store).
4. **Journey task definitions + grading rubric** — what counts as completed
   / partial / failed / hallucinated; this rubric IS the product's core IP.
5. **Publishing surface decision** + naming ticket (name lock follows the
   8/08 precedent: availability sweep before lock).
6. **Reuse audit:** the claim-accuracy pilot harness
   (`vault/20_projects/research/2026-09-01-claim-accuracy-presale-pilot.md`)
   generalizes — claims probes become one probe type beside journey probes.

## Standing constraints

- ≤$250/month opex, ~25 hrs/week co-primary with the job hunt ([L2] carry).
- Complement Cloudflare/Stripe, never compete head-on.
- Build-in-public wrapper is the attention engine; weekly build-log from
  week one.
- No build before the systemcraft chain exists (research-before-build).
