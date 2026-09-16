---
title: "Adversarial Mandate vs. Convergence in Agentic Evaluation"
type: connection
connects:
  - Manufactured Finding
  - Convergence Rule for Agentic Audits
  - Supervision Fatigue as the Hard Cap on Fleet Scaling
created: 2026-09-16
updated: 2026-09-16
---

## Synthesis

The tension arises between an agent's adversarial mandate to find flaws and the system's need for convergence to declare a clean verdict. When the mandate is asymmetric—requiring the auditor to always find something—the system manufactures findings, creating a false sense of rigor while actually degrading quality through noise. This pattern manifests in both creative studio audits and job-hunt application reviews, where automated checks can become self-defeating if not constrained by explicit stopping rules.

## Threads

### [[Manufactured Finding]]

> if the red-team is going in being told it HAS to point out the flaws, then it will find them, even if it has to make them up

### [[Convergence Rule for Agentic Audits]]

> propose a convergence rule for the master skill (a per-artifact repair cap, a severity floor tied to the P0 rule, or a 'holds / residual' verification pass instead of a fresh audit)

### [[Supervision Fatigue as the Hard Cap on Fleet Scaling]]

> without his stop it would have looped audit → repair indefinitely, because the ladder escalates on every material finding and has no stopping rule

## Implications

- Sean must implement explicit convergence rules in his master skill to prevent infinite loops in creative studio audits.
- Job-hunt application reviews should use severity floors rather than pass counts to determine when an application is ready for submission.
