---
title: "Agent Health and Automation Routines Tension"
type: connection
connects:
  - Agent Fleet Observability Dashboard
  - Automation Routines
  - Infrastructure Status and Agent Failure
created: 2026-05-22
updated: 2026-05-22
---

## Synthesis

The Agent Fleet Observability Dashboard exposes a tension between the Automation Routines' clockwork predictability and the reality of agent health variability. When agents like `deep_researcher` complete tasks successfully (as evidenced by the 11 KB report), it reinforces trust in automation routines. However, if an agent fails silently (like `gemini-researcher` being disabled by default), the dashboard must surface this to prevent knowledge workflow disruptions.

## Threads

### [[Agent Fleet Observability Dashboard]]

> The `deep_researcher` smoke-test [...] wrote a real 11 KB report at [...] in 280 s wall-clock at $0.00 cost.

### [[Automation Routines]]

> What to expect at 02:45 on 2026-05-06 [...] `deep-researcher` fires → reads `vault/00_inbox/r

### [[Infrastructure Status and Agent Failure]]

> The `gemini-researcher` correctly skipped (default disabled, opt-in via `INSTALL_GEMINI=1`).

## Implications

- Sean must balance the need for clockwork automation with active monitoring of agent health status, as failures in routines can reduce knowledge quality without visible feedback.
- The existence of opt-in agents like `gemini-researcher` introduces complexity in the observability dashboard, requiring clear status indicators for optional components.
