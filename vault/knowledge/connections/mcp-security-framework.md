---
title: "MCP Security Framework"
type: connection
connects:
  - Intent Engineering
  - MCP Server Hardening
  - Vault Knowledge - MCP Research
created: 2026-05-19
updated: 2026-05-19
---

## Synthesis

A cross-domain pattern where intent engineering, MCP hardening practices, and vault knowledge about vulnerabilities inform a unified security framework for public npm-distributed servers.

## Threads

### [[Intent Engineering]]

> input validation at JSON-RPC boundary, tool description sanitization, output filtering, audit logging, threat model.

### [[MCP Server Hardening]]

> input validation at JSON-RPC boundary, tool description sanitization, output filtering, audit logging, threat model.

### [[Vault Knowledge - MCP Research]]

> The specific publicly-disclosed MCP-related prompt-injection vulnerabilities of 2025-2026 (GitHub MCP private-repo exfiltration case especially — what was the attack path, what was the fix).

## Implications

- Sean can build a secure @swins/intent-engineering-mcp@0.1.0 server by combining intent engineering with hardening practices and referencing documented vulnerabilities in Vault Knowledge.
