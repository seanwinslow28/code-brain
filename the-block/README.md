# the-block/

> **ARCHIVED 2026-05.** This domain is the prior role at The Block. Templates and patterns retained for portfolio + future reference. Calendar / Atlassian / Slack rules below are no longer enforced.

Domain workspace for Sean's prior day job at **The Block** — a crypto/ETF data company where Sean was a Product Manager (Nov 2025 – May 2026).

## What lives here

- [`CLAUDE.md`](CLAUDE.md) — domain router (load when working on Block-related tasks)
- `product-management/` — generic PM workspace (PRD templates, sprint frameworks, stakeholder comms templates, analysis templates). Moved here from repo root in v3.15.0 because Sean's only PM work right now IS Block.

## What does NOT live here

- The autonomous Block-context skills (`jira-automation`, `etf-page-creator`, `stakeholder-update`, etc.) — those live at canonical `.claude/skills/` and auto-load regardless of workspace
- Granola-synced meeting transcripts — those live at `vault/30_domains/product-management/the-block-meetings-granola-notes/` (vault is independent of workspace structure)
- Operating model artifacts — those live at `vault/05_atlas/operating-models/the-block/`

## How to use

When starting Block-domain work in Claude Code, `cd` into this directory or open a session here. Claude Code will auto-load this folder's `CLAUDE.md` as the nearest-ancestor context.

For the broader ecosystem architecture, refer back to the root [CLAUDE.md](../CLAUDE.md).
