# Field Report — PM3 t1 Trend-vs-Noise Verdict (the Phase-2 gate)

**Date:** 2026-07-22
**Task:** Run PM3 t1, compare vs the frozen t0 bundle with the 4a-validated matcher, deliver the GO/KILL/RESCOPE verdict, branch on it.
**Outcome:** **KILL the trend premise** (RESCOPE contingent on Sean's re-run behavior). Phase 2 closes without building the persistence spec. One fleet-blocking bug found + fixed along the way.

## What happened

1. **Pre-flight.** main at #138 (ahead of expected #123), tests 745 pass / 1 skip (suite grew), validate PASSED, 22-day t0→t1 gap (good signal window). Cost check surfaced a scare: raw July council-spend summed to $240 vs a "$50/month" cap — but $237 was **the-oracle F8b soak** (`oracle-*` tools, a separate bucket), and the F8b enforcement flip (policy v3, 2026-07-19) had **raised discovery caps to $30/day / $100/month** and made budgets per-tool. Real discovery July spend: **$2.98**. Ample headroom. Got Sean's go-ahead.

2. **t1 blocked 3× by an OpenRouter outage.** Every real run failed at FUSE with `OpenRouter 500 on Fusion call (judge=anthropic/claude-opus-4.7)`. Rather than blind-retry, I isolated it: plain model calls 200'd; small-payload fusion calls 200'd; a faithful 118-record replay 200'd — but the **exact `_build_body`** payload 500'd reproducibly. Controlled A/B pinned it: **`max_price` on the `openrouter:fusion` tool → 500; popped → 200.** A provider-side change (t0 ran fine with it on 6/30). This blocked *all* paid discovery, not just t1.

3. **Fix (approved by Sean).** Scoped drop of `max_price` in `fusion._build_body` only (not `provider_price_policy`, which the regular council still uses). Cost safety preserved by model-pinning + `max_tool_calls` + the enforced F8b ledger caps. Two tests updated; suite green (745/1). Committed on `fix/discovery-fusion-max-price-500` (unpushed).

4. **t1 ran.** 6 verified, 0 dropped, session `20260722-122152-4b67cc`. **Cost $6.81** — a 3.7× overshoot vs t0's $1.85 (logged as an incident; likely fusion web-tool spend, which `max_price` never bounded anyway).

5. **Comparison (4a two-stage matcher, reused exactly, $0 local Ollama).** 2 SAME · 3 RELATED · 3 ABSENT · 2 emerged. The matcher correctly rejected all 3 cheap-signal false candidates (3-for-3), consistent with 4a's complementarity result.

6. **Verdict: movement ≤ noise.** Mean score 38→65 is a **recency artifact** (t0 6/8 aging → t1 6/6 fresh; the recency multiplier does the work, not the world). Count/granularity churn is the 4a same-day-noise signature across time. Vanished/emerged pains sit inside the sampling envelope. The *matcher* works (identity/dedup is sound); the *trend claim* isn't validated. Red-team #5 lands. Full note: `vault/20_projects/research/2026-07-22-pm3-t1-trend-noise-verdict.md`.

## What worked
- **The $0 gate did exactly its job.** 4a ($0) + one paid run ($6.81) killed an unvalidated feature before its full build. Cheap failure beats expensive momentum.
- **Diagnose-before-retry.** Three identical failures could have been "retry and hope"; isolating the payload difference found a real fleet bug and the fix that unblocked the authorized run.
- **The 4a matcher held up** on a genuinely different (cross-time) dataset.

## What to watch (tickets filed)
- `max_price` fusion fix — **push + PR pending Sean's OK.**
- Discovery cost overshoot $6.81 vs $1.85 — investigate `max_tool_calls` / fusion cost bound.
- F8b ledger reconcile question — spend-file `total` ($17.25 reservations) vs actuals (~$6.84); confirm stale reservations are released and the cap check reads settled/reconciled, not gross.

## Next
Phase 2 complete. **Phase 3** (paid, was gated behind Phase 2): E5 (decouple from one machine) · D5 (interactive triage) · PM1+PM5 (gate scorecard as brand + packaging) · Step F buyer conversations (the paid wedge, red-team #2/#3) — scope in a fresh session with its own continuation prompt.
