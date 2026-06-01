---
title: "The Tension Between Generic Security Checklists and Server-Specific Threat Models"
type: connection
connects:
  - MCP Server Hardening
  - Vibe-Coding Interview Canon
  - Intent Engineering
created: 2026-06-01
updated: 2026-06-01
---

## Synthesis

Generic security checklists often fail because they prescribe actions (like 'add validation') that may already exist or are irrelevant to the specific attack surface. The tension arises when a pre-written roadmap assumes a generic threat model, while the actual code exposes a unique, low-level vulnerability (like unconstrained file paths). This disconnect forces a choice between following the checklist blindly or deviating to address the real, server-specific risk. The consequence is that credibility in security audits depends on identifying and naming the precise, non-obvious vulnerability rather than performing generic hardening tasks.

## Threads

### [[MCP Server Hardening]]

> The concrete, server-specific hole is file_path → arbitrary local file read. audit.ts:80-83 and retrofit.ts:59-62 do fs.stat(file_path) + isFile() + fs.readFile(file_path) — no size cap, no extension allowlist, no root confinement, and fs.stat follows symlinks so a symlink to /etc/passwd passes isFile().

### [[Vibe-Coding Interview Canon]]

> The roadmap's Task 23 checklist was written before anyone read the current code. I read it. Five corrections turn a generic checklist into a defensible, server-specific audit — and the corrections themselves are the credibility move.

### [[Intent Engineering]]

> The one-sentence thesis for the whole artifact: the real vulnerability in this server isn't abstract prompt injection — it's that two of the three tools accept an unconstrained absolute file_path and fs.readFile it, so an indirect prompt injection can turn a 'spec analysis' tool into a local-file-exfiltration primitive.

## Implications

- Sean should prioritize reading live code before executing security tasks to avoid performing redundant or irrelevant work.
- Security audits of agentic systems must focus on the specific permissions granted to tools (like file access) rather than just input validation.
