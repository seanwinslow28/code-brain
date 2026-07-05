# WWF5D Step 4 — Council Validation Results

- **Date:** 2026-07-05
- **Run spec:** [`council-run-prompt.md`](council-run-prompt.md) / [`validation-run.md`](validation-run.md)
- **Profile:** `variance` (chairman + member `~anthropic/claude-sonnet-latest`, `openai/gpt-5.4-mini`, `deepseek/deepseek-v4-pro`, `mistralai/mistral-medium-3-5`)
- **Transcripts:** `council-rt{1,2,3}-{AB,BA}.md` in this directory
- **Prompt files fed to the council:** `/tmp/llm-council/wwf5d-val-rt{1,2,3}-{AB,BA}.md` (blind, order-swapped, header-and-self-citation redacted — see §4)

## 1. Cost

| Run | Duration | Tokens (in/out) | Cost |
|---|---|---|---|
| rt1-AB | 271.1s | 115,108 / 14,510 | $0.7932 |
| rt1-BA | 143.8s | 115,013 / 10,253 | $0.7289 |
| rt2-AB | 150.8s | 86,694 / 8,512 | $0.5612 |
| rt2-BA | 82.4s | 86,766 / 5,321 | $0.5136 |
| rt3-AB | 254.8s | 124,970 / 15,903 | $0.8634 |
| rt3-BA | 101.1s | 124,751 / 7,711 | $0.7394 |
| **Total** | | | **$4.1997** |

**Cost note:** the doc's estimate was $0.10–0.40/query (~$0.6–2.4 total). Actual cost landed at **$4.20**, roughly 2x the top of the estimate, because the RT1–RT3 artifact bodies (up to ~1,000 lines for RT3) are far larger than the calibration-style prompts the estimate was based on. Flagged to Sean mid-run at $0.79/query (after rt1-AB); he approved continuing. Still well within the $7/day, $40/month council caps — no other spend recorded 2026-07-05 before this run.

No dropped models, no ranking failures across all 6 runs — full 4-model panel + chairman completed every time.

## 2. Per-task tally (non-Claude panel majority, both orders)

Per the F4 fix: the verdict is the majority of **GPT-5.4-mini, DeepSeek-v4-pro, Mistral-medium-3-5 only**. The Sonnet chairman/member is same-family as the Opus authors and is excluded from the vote (read for color in §3).

| Task | AB-order majority | BA-order majority | Both-orders result |
|---|---|---|---|
| RT1 (preserve-session fix-spec) | 2/3 → WWF5D (gpt, deepseek) | 2/3 → WWF5D (deepseek, mistral) | **WWF5D win** |
| RT2 (hooks-configuration audit) | 2/3 → baseline (deepseek, mistral) | 3/3 → WWF5D | **flips → TIE** |
| RT3 (portfolio explainer spec) | 2/3 → WWF5D (gpt, deepseek) | 2/3 → WWF5D (deepseek, mistral) | **WWF5D win** |

**Result: 2 of 3 tasks WWF5D win, 1 tie** under the panel's own both-orders rule.

## 3. Position-bias audit (beyond what the run-prompt asked for, done because the RT2 flip looked suspicious)

Checked whether each non-Claude member's vote tracked **content** (the actual arm) or just **position** (slot A vs slot B), by comparing each model's vote across the AB/BA order-swap of the same task.

- **Mistral-medium-3-5 voted `VERDICT: A` in all 6 of 6 runs**, regardless of which arm occupied slot A. Zero content signal — pure primacy bias. Its vote is non-diagnostic across the entire battery, not just RT2.
- **GPT-5.4-mini voted `VERDICT: B` in 5 of 6 runs** (only break: rt2-BA, where it tracked content). Strong recency/position-B bias.
- **DeepSeek-v4-pro is the only member that tracked content across the order-swap** on RT1 and RT3 (same real-arm answer in both orders, both times favoring WWF5D). It flipped on RT2 (baseline in AB, WWF5D in BA) — the one member showing a genuine, non-positional disagreement on that task.
- **Sonnet (chairman/member, excluded from the vote) was perfectly content-consistent across all three tasks — favoring WWF5D every single time**, both orders. This is exactly the self-preference risk the F4 exclusion exists to guard against, and it corroborates that excluding it from the vote was the right call, not a formality.

**Read:** RT2's "TIE" is mostly an artifact of 2 of 3 panel members being order-biased rather than the panel genuinely splitting on RT2's merits. Once you weight by which members actually engage with content, the panel's real signal on RT2 is thin — closer to "no reliable signal" than "the panel disagrees with WWF5D."

## 4. Blindness redaction (a real gap in the original prep, fixed before spend)

Before assembling the prompt files, the WWF5D-authored bodies (`rt{1,2,3}-opus-wwf5d.md`) were checked for leakage beyond the one-line provenance header the run-prompt anticipated. Found and fixed, on the `/tmp` copies only (source files in this directory untouched):

- **58 inline self-citations** of the form `WWF5D §X.Y` across the three WWF5D bodies (the artifacts cite their own framework by name throughout the prose) — redacted to bare `§X.Y` (kept the section-number cross-reference, dropped the name that would have instantly deblinded every panelist).
- **One explicit self-reference** in `rt2-opus-wwf5d.md` ("from the *baseline's* known catches on this substrate, folded in") that named the compared arm directly — reworded to remove the comparison language while preserving the underlying factual claim.
- Verified clean of "Fable", "Opus", and comparison language ("versus", "the other artifact", etc.) after redaction; the only remaining "Baseline" hits in RT3 are unrelated (web-platform Baseline/caniuse references).

This means the artifacts fed to the council are **not byte-identical** to `rt{1,2,3}-opus-wwf5d.md` as committed — they're a redacted copy for blindness only. Content/argument substance is untouched.

## 5. κ-gate

Per Sean's direction, reused his existing reference-blind verdict (recorded in WWF5D §7 before this run: **3/3 favoring WWF5D** — RT1, RT2, RT3 all called for WWF5D) as the n=3 label set, rather than a fresh relabel.

| Task | Sean's label | Panel's both-orders label |
|---|---|---|
| RT1 | WWF5D | WWF5D |
| RT2 | WWF5D | TIE |
| RT3 | WWF5D | WWF5D |

Raw agreement: 2/3 (66.7%). **Cohen's κ = 0.0** (Po = 0.667, Pe = 0.667).

**Honest read:** κ = 0 here is a known degeneracy, not evidence the panel is random relative to Sean. Sean's labels have zero variance (WWF5D all three times), so the chance-agreement term Pe collapses to equal the observed agreement Po by construction — with a rater showing no variability, Cohen's κ cannot register above-chance agreement no matter how good the raw agreement is. At n=3 this statistic is not informative in either direction; it is reported because the design doc commits to reporting it, not because it should be read as "the panel doesn't track Sean's judgment" in the usual sense.

**Gate result:** κ = 0.0 < 0.6 → **gate fails on paper**. Per the pre-committed decision rule ("if κ < 0.6, report the panel result but treat Sean's eye as authoritative and say so"): **Sean's eye is the authoritative call.**

## 6. Final decision

**Sean's eye (Engine Truth, per the pre-committed rule): WITH-WWF5D wins 3/3.** The κ-gate technically failed, but the failure is a small-sample/zero-variance artifact (§5), not a substantive panel objection.

**The panel corroborates on 2 of 3 tasks (RT1, RT3) and ties on the third (RT2)** — and the RT2 tie is better explained by 2 of 3 panelists showing pure position bias (§3) than by genuine disagreement on RT2's content. Net: this run is a **partial, imperfect robustness check that leans toward confirming Sean's 3/3 rather than complicating it**, with the honest caveats that (a) the panel itself is noisy (only DeepSeek tracked content reliably), (b) n=3 makes the κ-gate uninformative as computed, and (c) the same-family Sonnet chairman's clean 3/3 agreement with Sean is consistent with either "WWF5D really does transfer" or "Claude-family models share a preference here" — which is exactly why it was excluded from the vote rather than used to break the RT2 tie.
