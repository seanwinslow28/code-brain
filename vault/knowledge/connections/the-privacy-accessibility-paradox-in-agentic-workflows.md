---
title: "The Privacy-Accessibility Paradox in Agentic Workflows"
type: connection
connects:
  - Privacy-Aware Data Routing
  - Vault as Agent Infrastructure
  - Do-Not-Promote Framing
created: 2026-07-03
updated: 2026-07-03
---

## Synthesis

Sean's workflow is defined by a fundamental tension between the need for rich, personal data to fuel creative insights and the requirement to isolate that same data to protect privacy. This paradox forces him to maintain a 'sanitized proxy' layer that acts as a bottleneck; while it enables agent accessibility, it also strips away the nuance necessary for deep agentic assistance. The consequence is a dependency on automated verification scripts to ensure the proxy remains clean, creating a fragile system where any scrubbing failure could lead to privacy leakage or loss of context.

## Threads

### [[Privacy-Aware Data Routing]]

> This mechanism describes a deliberate architectural split where sensitive, high-risk personal data is isolated in gitignored private directories while a sanitized, public-facing copy serves as the sole input for agentic processing.

### [[Vault as Agent Infrastructure]]

> Consolidated the 'Raising Claude' Substack work into this tracked (public) folder inside code-brain, so it backs up to GitHub and syncs across machines.

### [[Do-Not-Promote Framing]]

> "Do-Not-Promote framing" is the umbrella term for the suppressed personal topic (per the series' own voice rule and code-brain Rule #10).

## Implications

- Sean must implement automated verification scripts to continuously check that no private entities have leaked into the public copy, as manual review is not scalable.
- The reliance on a 'sanitized proxy' means that any agent operating on the public data lacks access to the full nuance of the original stories, potentially limiting the depth of agentic assistance in sensitive areas.
