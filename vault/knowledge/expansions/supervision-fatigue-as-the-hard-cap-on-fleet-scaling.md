---
title: "How to make `Supervision Fatigue as the Hard Cap on Fleet Scaling` better"
type: expansion
parent: "[[supervision-fatigue-as-the-hard-cap-on-fleet-scaling]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-18
updated: 2026-08-18
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[supervision-fatigue-as-the-hard-cap-on-fleet-scaling]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add a measurement model, not an inferred diagnosis

**WHAT:** Separate *system throughput*, *review workload*, and *decision quality*. The cited runs measure machine duration and artifact count—not Sean’s attention, fatigue, rejection rate, or trust. “Supervision fatigue” is currently an untested causal story.

**WHO/WHAT:** Anchor the concept on Sandra Hart’s [“NASA-TLX: 20 Years Later”](https://humanfactors.arc.nasa.gov/groups/tlx/downloads/HFES_2006_Paper.pdf), which operationalizes workload across mental demand, temporal demand, effort, frustration, and perceived performance.

**ADD THIS MODE:**  
> “At batch size *n*, review minutes and TLX frustration rose, while accepted-novel-connections per review minute fell from *x* to *y*.”

Instrument three nightly conditions—5, 15, and 30 candidates—and record review time, raw TLX, acceptance rate, and delayed usefulness after seven days.

**UNLOCKS:** An executable fleet-evaluation protocol and portfolio case study demonstrating experimental judgment. Without it, this concept cannot distinguish fatigue from slower inference, weaker source material, duplicate clusters, or a stricter critic.

## 2. Add the “out-of-the-loop” contradiction

**WHAT:** Replace the one-directional claim—more automation creates more supervision—with a U-shaped failure model. Excessive review creates overload; insufficient active participation causes situation-awareness and judgment decay. The optimum is not maximum automation or minimum output, but designed operator engagement.

**WHO/WHAT:** Lisanne Bainbridge’s [“Ironies of Automation”](https://www.sciencedirect.com/science/article/pii/0005109883900468) shows that automation leaves humans supervising precisely the abnormal cases for which passive supervision leaves them least prepared. Endsley and Kiris experimentally sharpen this in [“The Out-of-the-Loop Performance Problem and Level of Control in Automation”](https://doi.org/10.1518/001872095779064555).

**ADD THIS MODE:**  
> “The fleet should preserve Sean’s calibration, not merely conserve his attention.”

Specify periodic blind ranking, manually authored synthesis rounds, and recovery drills where Sean must diagnose a deliberately corrupted connection without agent explanation.

**UNLOCKS:** A “maintaining operator taste” runbook, incident exercise, and agent specification for preserving human capability—not merely reducing notification volume.

## 3. Add selective prediction and an explicit review budget

**WHAT:** Treat human attention as a fixed budget and require the fleet to abstain. Emit only candidates that clear novelty, disagreement, and consequence thresholds; archive or discard the rest automatically. Evaluate the selector with a **risk–coverage curve**, not raw connection count.

**WHO/WHAT:** Yonatan Geifman and Ran El-Yaniv’s [“Selective Classification for Deep Neural Networks”](https://arxiv.org/abs/1705.08500) formalizes the reject option: sacrifice coverage to bound error among accepted outputs.

**ADD THIS MODE:**  
> “Given a review budget of seven items, maximize useful surprise; abstain when estimated value is below the seventh-ranked candidate.”

Build a review-budget controller that ranks candidates using embedding novelty, critic disagreement, source quality, and predicted actionability, then plots accepted-value versus coverage.

**UNLOCKS:** An executable demo, MCP policy primitive, and strong portfolio one-pager: not “I built seven agents,” but “I built a fleet that knows when human attention is worth spending.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
