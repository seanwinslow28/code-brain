---
title: "MCP Server Hardening"
type: concept
sources:
  - 20_projects/research/2026-05-18-mcp-prompt-injection-hardening.md
tags: [auto-generated, phase-6]
created: 2026-05-19
updated: 2026-05-19
---

## Definition

A checklist of security practices to defend public npm-distributed MCP servers against prompt-injection attacks, including input validation and audit logging.

## Context

Sean's @swins/intent-engineering-mcp@0.1.0 server must follow MCP hardening guidelines to prevent exploitation.

## Evidence

> input validation at JSON-RPC boundary, tool description sanitization, output filtering, audit logging, threat model.

> The GitHub MCP private-repo exfiltration case involved tool poisoning and cross-tool prompt injection (CPI / line-jumping).

## Examples

- input validation at JSON-RPC boundary
- audit logging

## Related Concepts

[[Vault Knowledge - MCP Research]] [[Intent Engineering]]
