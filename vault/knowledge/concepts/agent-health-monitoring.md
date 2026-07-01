---
title: "Agent Health Monitoring"
type: concept
sources:
  - knowledge/connections/the-decoupling-of-operational-health-from-functional-value.md
tags: [auto-generated, phase-6]
created: 2026-07-01
updated: 2026-07-01
---

## Definition

The practice of evaluating agent status through operational metrics like uptime and exit codes rather than semantic output verification. This approach assumes that process completion equates to value delivery, ignoring the possibility of empty or corrupted data payloads. It creates a blind spot where agents can be technically 'alive' but functionally inert.

## Context

Sean's current monitoring setup reports 'healthy' statuses even when the synthesizer produces no concepts, leading him to believe his knowledge base is being updated when it is actually stagnant.

## Evidence

> status=error · 5.5h ago · notes='concepts=0 connections=0 rejected=0 edges=0'

> Sean cannot trust the dashboard as a proxy for his knowledge base's vitality

## Examples

- forcing him to manually verify the content quality rather than relying on system metrics

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Silent Failure Propagation in Agent Fleets]]
