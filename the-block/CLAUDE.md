# CLAUDE.md — The Block (Domain: PM Day Job)

> **ARCHIVED 2026-05.** This domain is the prior role at The Block. Templates and patterns retained for portfolio + future reference. Calendar / Atlassian / Slack rules below are no longer enforced.

Domain context for Sean's prior day job at **The Block**, a crypto/ETF data company where Sean was a Product Manager from Nov 2025 – May 2026. For ecosystem-wide rules (non-negotiables, hook exit codes, agents-sdk, MCPs), see root [CLAUDE.md](../CLAUDE.md). For the active job-hunt workspace, see `vault/20_projects/prj-job-hunt-2026/`.

## Scope of This Domain

**In:** PRDs for data and crypto products, sprint ceremonies, stakeholder communications (bi-weekly P&E status update is the marquee one), ETF page creation on WordPress, Jira/Confluence work, daily standup, design syncs, SEO check-ins, ad operations, Campus education product work, internal Simon AI feature work.

**Out:** Side projects, creative work, personal finance, 16BitFit, animation pipeline. Those route to [creative-studio/CLAUDE.md](../creative-studio/CLAUDE.md) or [life-systems/CLAUDE.md](../life-systems/CLAUDE.md).

## Operating Model

The five-artifact bundle for this domain (populated by the [`work-operating-model`](../.claude/skills/work-operating-model/SKILL.md) skill):

- Heartbeat (rhythms): [vault/05_atlas/operating-models/the-block/HEARTBEAT.md](../vault/05_atlas/operating-models/the-block/HEARTBEAT.md)
- User profile (decisions): [vault/05_atlas/operating-models/the-block/USER.md](../vault/05_atlas/operating-models/the-block/USER.md)
- Soul (people / tools / tribal): [vault/05_atlas/operating-models/the-block/SOUL.md](../vault/05_atlas/operating-models/the-block/SOUL.md)
- Synthesized model: [vault/05_atlas/operating-models/the-block/operating-model.md](../vault/05_atlas/operating-models/the-block/operating-model.md)
- Schedule rules: [vault/05_atlas/operating-models/the-block/schedule-recommendations.md](../vault/05_atlas/operating-models/the-block/schedule-recommendations.md)

If those files still show `status: awaiting-interview`, run: `Run the work-operating-model interview for the-block`.

## Workspace Layout

- `product-management/` — PRD templates, sprint frameworks, stakeholder comms templates, analysis reference (moved here from repo root in v3.15.0)

## Primary Skills for This Domain

| Skill | Purpose |
|---|---|
| `jira-automation` | Create Epics, Design Stories (`[Design]` prefix), Implementation Stories (`[Implementation]` prefix), bulk JQL operations |
| `etf-page-creator` | WordPress ETF page creation with Track Insight schema |
| `stakeholder-update` | Bi-weekly P&E status update (Jira → Confluence → Slack), executive summaries |
| `meeting-prep` | Standup prep, agenda generation, post-meeting action items, knows the recurring meeting schedule |
| `prd-generator` | Interview-driven PRD writing with acceptance criteria |
| `tech-spec` | Bridge from PM requirements to engineering spec |
| `sprint-roadmap` | Backlog prioritization (RICE / MoSCoW / Impact-Effort), capacity planning |
| `ticket-batch` | Batch-create Jira tickets from PRDs or brain dumps |
| `analytics-workarounds` | GA4 / Looker access via Zapier MCP bridge into Sheets |
| `data-analysis` | GA4 analytics, article CTR, ad revenue, sprint dashboards |
| `crypto-web3-context` | Blockchain terminology (DeFi, L1/L2, TVL, MEV), market data concepts, crypto-specific PRD vocabulary |
| `api-product-management` | API doc generation, endpoint specs, DX optimization for The Block Data API |
| `campus-education` | Course structure / lesson outline / curriculum patterns for the Campus product |
| `revops-adops-automation` | Pipeline reports, revenue forecasts, campaign audits, yield analysis |
| `ai-native-products` | LLM integration patterns for The Block's Simon and similar AI features |
| `research-synthesis` | Interview transcripts → themes → personas |
| `org-definition-of-done` | DoD validator for features and releases |

## Primary Agents for This Domain

- `checklist-validator` — validate work against acceptance criteria before marking tickets done
- `doc-reviewer` — review PRDs and tech specs for completeness, clarity, actionability
- `compliance-summarizer` — review work for regulatory/policy compliance (relevant for ETF + crypto product changes)
- `data-analyst` — visualize data and surface insights from analytics outputs

## Active MCPs Used Here

- **Atlassian** (Jira + Confluence) — primary work-tracking surface
- **Slack** — workspace pending Block admin OAuth approval; until then use Zapier `slack_*` fallback
- **Gmail + Google Calendar** — query BOTH `swinslow@theblock.co` AND `sean.winslow28@gmail.com` in parallel (calendar rule from root CLAUDE.md)
- **Google Sheets / Docs / Drive** — for analytics-workarounds and roadmap docs
- **Zapier** — Salesforce, GA4 (no native MCP for these)

## Non-Negotiable Rules Specific to This Domain

1. **Never auto-post Jira tickets.** Always show drafts and wait for confirmation. Same for Slack messages and Confluence pages.
2. **ETF pages follow the Track Insight schema.** Use `etf-page-creator` skill — don't freelance the data structure.
3. **Story title prefixes:** `[Design]` for design stories, `[Implementation]` for implementation stories. The `jira-automation` skill enforces this; if working manually, follow the same convention.
4. **Granola meeting transcripts at [vault/30_domains/product-management/the-block-meetings-granola-notes/](../vault/30_domains/product-management/the-block-meetings-granola-notes/) are the source of truth for internal quotes and decisions.** Don't paraphrase from memory.
5. **Bi-weekly P&E update cadence is sacred.** That's the highest-leverage stakeholder artifact in this domain. Any agent that touches it should use the `stakeholder-update` skill, not freelance.
6. **Calendar queries always hit BOTH email accounts** (work + personal). The Block schedules cross both.

## Related Vault Paths

- Granola-synced meetings: [vault/30_domains/product-management/the-block-meetings-granola-notes/](../vault/30_domains/product-management/the-block-meetings-granola-notes/)
- MOC: [vault/05_atlas/moc-product-management.md](../vault/05_atlas/moc-product-management.md) (still uses the historical `product-management` domain tag for vault dataview queries — these tags are intentionally separate from workspace folders)

## When Modifying This Domain

- Update [CHANGELOG.md](../CHANGELOG.md) for any new Block-specific skill, agent, hook, or workflow
- If you add a new skill that's exclusively Block-specific, consider whether it belongs in `.claude/skills/` (canonical, auto-loaded) and whether to surface it in the Primary Skills table above
- Update [vault/05_atlas/operating-models/the-block/](../vault/05_atlas/operating-models/the-block/) artifacts when Sean's role / cadence / dependencies shift
