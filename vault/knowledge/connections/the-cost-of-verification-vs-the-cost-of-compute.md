---
title: "The Cost of Verification vs. The Cost of Compute"
type: connection
connects:
  - The Efficiency-Quality Inversion in Automated Synthesis
  - Hardware Fragility Masks Semantic Decay in Agent Fleets
  - Supervision Fatigue as the Hard Cap on Fleet Scaling
created: 2026-09-22
updated: 2026-09-22
---

## Synthesis

There is a direct trade-off between the monetary cost of high-capability models and the cognitive cost of verifying their outputs. When Sean uses cheaper or local models, he saves money but incurs higher supervision costs due to potential hallucinations or lower reasoning depth. Conversely, using top-tier models like Kimi K3 reduces verification time but increases financial expenditure. This tension defines the economic boundary of his automated synthesis capabilities.

## Threads

### [[The Efficiency-Quality Inversion in Automated Synthesis]]

> On AA-Omniscience, the hallucination rate (wrong answers as a share of non-correct responses) is GLM-5.3 30%, Kimi K3 51%, DeepSeek V4 Pro 0813 95%.

### [[Hardware Fragility Masks Semantic Decay in Agent Fleets]]

> The three names Sean hears are the top three open models on every independent board that has scored them — and none of them can run on his hardware.

### [[Supervision Fatigue as the Hard Cap on Fleet Scaling]]

> A seat whose job is to say 'the evidence does not support this' cannot be the model that answers 95% of what it does not know.

## Implications

- Sean must budget for API costs for high-stakes strategic seats (a, e) where verification time is too expensive relative to model cost.
- Local models should be restricted to low-risk, high-volume tasks where hallucination can be tolerated or easily detected.
