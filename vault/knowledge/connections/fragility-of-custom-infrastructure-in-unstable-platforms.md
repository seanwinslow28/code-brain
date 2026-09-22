---
title: "Fragility of Custom Infrastructure in Unstable Platforms"
type: connection
connects:
  - Graceful Extensibility
  - The Abstraction Tax on Creative Authority
  - Structural Integrity vs. Automation Velocity
created: 2026-09-22
updated: 2026-09-22
---

## Synthesis

There is a fundamental tension between the desire for a highly customized, owner-controlled AI harness and the reality of building on a platform that explicitly rejects stability guarantees. When a platform like Pi offers 'graceful extensibility' but no versioning or deprecation policy, any custom infrastructure Sean builds becomes a liability rather than an asset. The consequence is that his creative authority is held hostage by the platform's development velocity, forcing him to choose between rapid feature adoption and long-term system reliability.

## Threads

### [[Graceful Extensibility]]

> The interface is pre-1.0 and says nothing about stability. No stability, semver or deprecation policy appears in extensions.md, sdk.md, development.md or either README.

### [[The Abstraction Tax on Creative Authority]]

> One TypeScript factory receives ExtensionAPI and can register tools, slash commands, CLI flags, keyboard shortcuts, providers, renderers and Markdown transformers; subscribe to ~39 lifecycle events (four of them can block or rewrite: tool_call, tool_result, context, before_agent_start).

### [[Structural Integrity vs. Automation Velocity]]

> The repo has moved: badlogic/pi-mono now redirects to earendil-works/pi (108,110 stars, 13,682 forks, created 2025-08-09) and the npm scope is @earendil-works/*

## Implications

- Sean should treat Pi extensions as ephemeral prototypes rather than permanent infrastructure components.
- He must prioritize local, file-based configuration (like SYSTEM.md) over extension-dependent features to maintain control.
