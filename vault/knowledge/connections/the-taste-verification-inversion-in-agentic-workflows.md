---
title: "The Taste-Verification Inversion in Agentic Workflows"
type: connection
connects:
  - Golden Dataset as Taste Artifact
  - Supervision Fatigue as the Hard Cap on Fleet Scaling
  - Taste as Evaluation Function vs. Activity Proof
created: 2026-08-31
updated: 2026-08-31
---

## Synthesis

There is a fundamental tension between the speed of agentic production and the depth of human taste required to validate it. When evaluation datasets are built *after* model selection, they reflect generic benchmarks rather than specific aesthetic standards, leading to outputs that are technically correct but creatively hollow. Conversely, building the golden dataset first externalizes taste but creates a rigid constraint that can stifle innovation if not treated as a living artifact. This inversion means that the most valuable work in agent development is often pre-computation: defining what 'good' looks like before any code is written.

## Threads

### [[Golden Dataset as Taste Artifact]]

> spent weeks 1 and 2 purely on building the evaluation database (compiling 200 real human agent chats to represent the 'golden data set') and establishing metrics before ever testing a model

### [[Supervision Fatigue as the Hard Cap on Fleet Scaling]]

> Without these gates, product teams become trapped in 'reactive loops,' identifying bugs only after they hit live users, where fixing one failure inadvertently triggers regressions elsewhere

### [[Taste as Evaluation Function vs. Activity Proof]]

> Anthropic separates its test suites into two distinct categories: Capability (Quality) Evals and Regression Evals

## Implications

- Sean should prioritize building a 'golden dataset' of his own past high-quality vault entries before scaling agent output volume, ensuring taste is encoded early.
- The cost of human supervision will likely exceed the value of automated synthesis if the golden dataset is not robust enough to filter out low-taste outputs automatically.
