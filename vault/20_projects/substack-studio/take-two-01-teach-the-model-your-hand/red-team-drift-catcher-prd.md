---
type: red-team
product: "DriftCatch (working name)"
post: take-two-01-teach-the-model-your-hand
created: 2026-06-28
related:
  - "PRD-drift-catcher.md"
  - "matrix-results-scored.md"
---

# Red-Team: DriftCatch, the controllable identity-survival dial that catches drift and proposes the fix

A fair adversary's read of the PRD. The goal is a sharper bet, not a longer risk list. I ran the cheapest test for the top assumption live (see the spike box) so this is partly evidence, not just theory.

---

## Live spike (ran it instead of just recommending it)

**Assumption tested:** a vision read can judge "still him, on the named markers" across hard style changes (PRD A1).
**Method (proxy):** fresh identity-marker read of the 4 hardest-abstraction images (woodblock, mid-century flat, stained glass, topographic), scoring brow weight, eye spacing, jaw angle, hair/cowlick, against the headshot.
**Result:** 3 of 4 hold cleanly (woodblock, stained glass, topographic). The read independently flagged **#06 mid-century flat** as softened: brow lighter, eyes enlarged, jaw rounded toward generic-handsome. That matches Sean's "too generic" instinct and the earlier hand-grade.
**Reads as:** positive but narrow. Detection is *feasible* and discriminated the one true drift case. It does NOT prove repeatability, calibration to Sean's threshold, performance on faces that aren't Sean, or that the fix works. Those are the surviving risks below.

---

## Top kill-assumptions (ranked by impact × likelihood-wrong × cheapness-to-test)

### 1. The fix-proposer actually reduces drift. Detecting is not fixing.
- **Claim (steelmanned):** the PRD's wedge is "catch the drift AND hand you the fix." anima's tier-2 critic already proposes prompt diffs, so the pattern exists.
- **Fails if:** the proposed prompt diff does not measurably reduce drift, or barely beats a naive "make it look more like the reference photo" re-roll. anima's own fix-rate data is the warning: Em's normalized fix-rate was ~0.67 overall and **0.00 on view-correctness** even after the detection was solid. Detection landed; the fix lagged. On gpt-image-2 it is worse, because there is no seed, so applying a fix is a fresh re-roll that can introduce NEW drift elsewhere (whack-a-mole).
- **Why it is #1:** the spike just made detection look cheap, which means the fix is the unproven half, and the PRD misranks it by calling detection the "make-or-break."
- **Evidence to get this week:** take 3 drifted outputs, apply DriftCatch's proposed diff, regenerate, re-score. Compare against a naive-baseline re-roll.
- **Kill criterion:** if fixes do not beat the naive baseline, or do not clear the threshold within 2 re-rolls on a majority of cases, the "hand you the fix" promise is hollow.
- **Cheapest test:** 3 cases, one fix each, eyeball the before/after. Half a session.
- **If killed:** downgrade honestly to detection-only ("it tells you the moment you stopped being you"). Weaker, but still a real, shippable product, and still the wedge nobody owns.

### 2. The detector is repeatable and calibrated to Sean's eye on faces that are NOT Sean.
- **Claim (steelmanned):** anima already calibrated a vision critic to ~90% agreement with Sean (the Gate-2 result), and the PRD borrows that bar (KR2).
- **Fails if:** that 90% does not transfer. anima's critic was calibrated on **Sean's face with hand-authored IR rules**. DriftCatch must work on an arbitrary user's face with **auto-derived** markers. That is a strictly harder problem, and the borrowed number may not hold. Also unproven: repeatability (does the same image get the same verdict on 5 runs?) and the false-positive rate (flagging faithful images as drift trains users to distrust it, which is fatal for a trust tool).
- **Evidence to get this week:** the Gate-2 method on a small labeled set that includes 2 to 3 other people, N=5 majority vote, measure agreement + false-positive rate.
- **Kill criterion:** <90% agreement, OR a false-positive rate high enough that faithful images get flagged (the spike was 1/12 flagged and it was the *right* one; a noisy detector that flags 3 to 4 faithful ones is unusable).
- **Cheapest test:** the spike, extended: blind-ish N=5 read on the 12 plus a few non-Sean faces. (The proxy above is N=1, not blind, Sean-only. Treat it as a smoke test that passed, not the calibration.)

### 3. The wedge is genuinely unowned.
- **Claim (steelmanned):** the discovery pass found wrappers commoditize "lock one face" but none productize anchor → drift-report → fix.
- **Fails if:** a tool already ships the loop (the space moves monthly, and a "consistency + auto-QA" wrapper is an obvious next step for an incumbent). If it is owned, DriftCatch is tool N+1.
- **Evidence to get this week:** a 1-hour search of the official + community marketplaces, Product Hunt, and the consistency-wrapper listicles for any tool that returns a per-image drift verdict + a fix.
- **Kill criterion:** a credible tool already does detect+fix on user-supplied identity. Then re-aim to the deepest whitespace from the discovery (expressive/animated or multi-character long-series drift, where the leaders are weakest and anima is strongest).
- **Cheapest test:** the search above. One hour.

### 4. The tool can ship inside the post's launch window without holding the post hostage.
- **Claim (steelmanned):** "a post that ships a tool" is the playbook's triple-payout, and the post narrates the tool.
- **Fails if:** building a calibrated detector + the fix loop + packaging + the stranger-dogfood gates is more than the post window allows, so the flagship post (the actual near-term deliverable) gets stuck waiting on the tool. The PRD's KR4 ("within the post's launch window") is an estimate, not a plan.
- **Evidence to get this week:** a 1-day timeboxed build spike of just the detection loop.
- **Kill criterion:** if the detection loop is not roughly working in a day, decouple: ship the post on the hand-run matrix (which is already a complete, honest artifact), ship the tool as a fast-follow.
- **Cheapest test:** the 1-day spike. This is the highest-leverage *de-risking-the-post* move, because the post does not actually depend on the tool existing.

### 5. Non-coders tolerate the companion-mode handoff.
- **Claim (steelmanned):** local-first / no-key is the trust-safe v1 surface per the playbook.
- **Fails if:** the "generate in ChatGPT, then bring the outputs back to DriftCatch" round-trip is too clunky and users bounce at the handoff (A2), or they will not do the one-time anchor setup (A3).
- **Evidence to get this week:** watch one non-coder run it end to end (the planned stranger dogfood).
- **Kill criterion:** the stranger stalls at the handoff or skips the anchor setup. Then power-mode (their own key, automated) becomes v1 and the trust story has to be rebuilt around it.
- **Cheapest test:** one stranger, one session. (Already in the plan; just pull it earlier.)

---

## What's well-reasoned (not manufacturing doubt)

- **Wedge vs table-stakes is correctly separated.** "Lock one face" is correctly called commodity; the detect+fix+dial loop is a real, evidence-backed gap. The positioning is sound.
- **The model-agnostic critic-layer hedge is genuinely good.** Vendors racing toward the dial is a real threat, and "own the workflow that survives model upgrades" is the right structural answer, not hand-waving.
- **The honesty about no-seed / dial-as-workflow is a strength, not a weakness.** Naming it pre-empts the obvious technical objection and is on-brand.
- **The anima reuse is a real asset, not vapor.** The pattern is shipped and calibrated; the spike confirms the detection half is feasible today.
- **Local-first packaging** correctly reads the security-anxious market.

## What I couldn't assess

- **Real calibration / repeatability** on arbitrary faces. Needs the keyed machine, an N=5 run, and a multi-person labeled set. The live spike was N=1, Sean-only, not blind.
- **Whether the fix beats baseline.** Needs a generation run (firewalled off this environment).
- **Actual market saturation.** Needs the live marketplace search.
- **Non-coder tolerance.** Needs a real stranger.

---

## The one thing to do first

Run the **#4 one-day detection-loop spike**, because it does double duty: it tests timing (kill-assumption #4) AND produces the labeled outputs you need to test the detector (#2) and the fix (#1) in the same sitting. And it protects the flagship post: the post is already shippable on the hand-run matrix, so the tool must never be allowed to hold it hostage. Decouple them in the plan now, before the build starts.
