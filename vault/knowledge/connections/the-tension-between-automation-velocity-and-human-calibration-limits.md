---
title: "The Tension Between Automation Velocity and Human Calibration Limits"
type: connection
connects:
  - The Calibration Bottleneck in Scalable Creative Production
  - Supervision Fatigue as the Hard Cap on Fleet Scaling
  - Criteria Drift as a Systemic Risk
created: 2026-09-16
updated: 2026-09-16
---

## Synthesis

There is a fundamental tension between the exponential cost reduction of automated agent outputs and the linear cost of human calibration required to validate them. As Sean scales his Productcraft pipeline, the velocity of artifact generation outpaces the human's ability to perform open coding and axial coding on traces. This creates a systemic risk where the system produces high volumes of low-fidelity content because the supervision layer cannot keep up with the production layer. The consequence is that automation without prior calibration leads to 'slop' rather than efficiency.

## Threads

### [[The Calibration Bottleneck in Scalable Creative Production]]

> Error analysis helps you decide what evals to write in the first place.

### [[Supervision Fatigue as the Hard Cap on Fleet Scaling]]

> Instead of plowing ahead and building an LLM judge, you want to fix any obvious errors.

### [[Criteria Drift as a Systemic Risk]]

> The EvalGen paper supplies the theory for why criteria cannot be fixed ahead of reading outputs (criteria drift).

## Implications

- Sean must prioritize error analysis and trace review over building automated judges to avoid validating incorrect assumptions about quality.
- Scaling agent fleets requires a corresponding increase in human supervision capacity or the development of hierarchical filtering mechanisms to prevent calibration collapse.
