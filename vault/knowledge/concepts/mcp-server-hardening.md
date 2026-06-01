---
title: "MCP Server Hardening"
type: concept
sources:
  - 20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-31-task-23-step-0-prebuild-prep.md
tags: [auto-generated, phase-6]
created: 2026-06-01
updated: 2026-06-01
---

## Definition

The practice of tightening existing input validation schemas to enforce strict path confinement and size limits, rather than adding new validation layers. This approach relies on the principle that the primary vulnerability in agentic tools is often the misuse of existing permissions (like file access) rather than a lack of input parsing. By hardening the boundaries of unconstrained absolute paths, the system prevents indirect prompt injection from escalating into arbitrary local file exfiltration. This requires identifying the specific code paths that handle file operations and applying guards that reject symlinks or out-of-bounds reads before the file system is accessed.

## Context

Sean is auditing his `sw-mcp-intent-engineering` server to ensure it is defensible against prompt injection attacks that exploit file read capabilities. The audit reveals that generic checklists are insufficient; the real risk lies in the specific implementation of `fs.readFile` without path confinement. This hardening is critical for maintaining the integrity of the server as a portfolio project and a potential job-hunt artifact.

## Evidence

> The honest work is tightening existing schemas (.strict() + path guard), not adding Zod. Claiming I added input validation would be false — say I hardened the existing validation.

> The concrete, server-specific hole is file_path → arbitrary local file read. audit.ts:80-83 and retrofit.ts:59-62 do fs.stat(file_path) + isFile() + fs.readFile(file_path) — no size cap, no extension allowlist, no root confinement, and fs.stat follows symlinks so a symlink to /etc/passwd passes isFile().

## Examples

- Replacing generic 'add Zod schema validation' with 'tighten existing schemas to enforce path confinement and size limits'
- Identifying that fs.stat follows symlinks, allowing a symlink to /etc/passwd to pass isFile() checks

## Related Concepts

[[Intent Engineering]] [[Vibe-Coding Interview Canon]]
