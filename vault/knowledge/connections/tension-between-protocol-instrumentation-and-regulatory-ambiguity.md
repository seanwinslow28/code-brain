---
title: "Tension Between Protocol Instrumentation and Regulatory Ambiguity"
type: connection
connects:
  - Vault as Agent Infrastructure
  - Mock Interview rig
  - Judge Layer Retrofit
created: 2026-06-08
updated: 2026-06-08
---

## Synthesis

The core tension lies in the conflict between Sean's need for rigorous, automated feedback loops (instrumentation) and the inherent ambiguity of human-centric evaluation criteria (regulatory/subjective judgment). As Sean builds more sophisticated agent tools like the Mock Interview rig, he encounters a boundary where quantitative metrics (test passes, scorecard medians) cannot fully capture qualitative success (interview performance). The consequence is that Sean must design 'hybrid' systems where agents handle the data processing and aggregation, but humans remain in the loop for final interpretation, creating a dependency on human judgment to validate the agent's output.

## Threads

### [[Vault as Agent Infrastructure]]

> Council Gap-Fill 5 expanded into Task 15 (Vault as Agent Infrastructure 5-Test Scorecard)

### [[Mock Interview rig]]

> Task 19 Mock Interview rig BUILD SHIPPED + TESTED — interview_grader Council profile + 8-dim rubric + mock_interview_loop.py (record→Whisper→grade, median-aggregates 4 panelist scorecards) + README; 13/13 new tests + profile test green

### [[Judge Layer Retrofit]]

> Council Gap-Fill 1 expanded into Task 12 (Judge Layer Retrofit on Substack-Drafter)

## Implications

- Sean must define clear 'human-in-the-loop' checkpoints where agent-generated scores are reviewed, preventing over-reliance on automated metrics for subjective outcomes.
- The evaluation rubric itself becomes a critical artifact that requires continuous refinement as Sean gains more data from mock interviews, shifting the burden of proof from the candidate to the evaluator.
