---
title: "Agent Health"
type: concept
sources:
  - knowledge/expansions/agent-health.md
tags: [auto-generated, phase-6]
created: 2026-05-28
updated: 2026-05-28
---

## Definition

Agent Health is a reliability contract that shifts the failure state from simple liveness (did the process run?) to functional utility (did the output serve the consumer?). It requires defining specific Service Level Objectives (SLOs) such as freshness windows, successful completion rates, and downstream consumer impact, rather than relying on binary status checks. This transforms the concept from a monitoring dashboard into a portfolio-grade reliability system where agents have error budgets and alert policies tied to their actual value delivery.

## Context

Sean is currently building a job-hunt infrastructure that relies on automated agents. By redefining health as an SLO contract, he can demonstrate to hiring managers that he understands distributed systems reliability, moving beyond simple cron-job automation to complex fleet management.

## Evidence

> Right now the concept treats “stale” as the main failure state; that is closer to a liveness probe than health.

> Define agent health as a small SLO contract: freshness, successful completion, output usefulness, dependency readiness, and downstream consumer impact.

> This lets Sean sound like he operates a reliability system, not just a cron dashboard.

## Examples

- Defining an agent's health by its 'downstream consumer impact' rather than its exit code.
- Creating an 'Agent Fleet SLO one-pager' that specifies error budgets for each agent.

## Related Concepts

[[Agent Health Monitoring]] [[Agent Ops / FDP Backup Track]] [[Infrastructure Status]]
