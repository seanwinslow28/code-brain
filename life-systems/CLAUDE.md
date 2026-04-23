# CLAUDE.md — Life Systems (Domain: Personal Systems)

Domain context for Sean's personal systems — finance, health, learning, tasks, time, career transition, and the Boston move. For ecosystem-wide rules, see root [CLAUDE.md](../CLAUDE.md).

## Scope of This Domain

**In:** Personal finance (Bilt + Chase categorization, monthly reports, debt paydown, subscription audits, budgets), health and habit tracking (workouts, streaks, XP/level-up gamification, fitness vault entries), learning (study plans, Socratic drills, Anki flashcards), personal task management (GTD, Socratic prioritization matrix, weekly reviews), time management (4:45 AM routine, 45/35/20 work split, calendar audits), career transition (PM → Animation Production), Boston move logistics, life admin (medical providers, address changes, renewals).

**Out:** The Block day-job work, creative projects. Those route to [the-block/CLAUDE.md](../the-block/CLAUDE.md) or [creative-studio/CLAUDE.md](../creative-studio/CLAUDE.md).

## Operating Model

The five-artifact bundle for this domain (populated by the [`work-operating-model`](../.claude/skills/work-operating-model/SKILL.md) skill):

- Heartbeat (rhythms): [vault/05_atlas/operating-models/life-systems/HEARTBEAT.md](../vault/05_atlas/operating-models/life-systems/HEARTBEAT.md)
- User profile (decisions): [vault/05_atlas/operating-models/life-systems/USER.md](../vault/05_atlas/operating-models/life-systems/USER.md)
- Soul (people / tools / tribal): [vault/05_atlas/operating-models/life-systems/SOUL.md](../vault/05_atlas/operating-models/life-systems/SOUL.md)
- Synthesized model: [vault/05_atlas/operating-models/life-systems/operating-model.md](../vault/05_atlas/operating-models/life-systems/operating-model.md)
- Schedule rules: [vault/05_atlas/operating-models/life-systems/schedule-recommendations.md](../vault/05_atlas/operating-models/life-systems/schedule-recommendations.md)

If those files still show `status: awaiting-interview`, run: `Run the work-operating-model interview for life-systems`.

## Workspace Layout

- `reference/` — life-systems reference materials and cheatsheets

## Primary Skills for This Domain

| Skill | Purpose |
|---|---|
| `personal-finance` | Import Chase + Bilt CSV, regex categorization, monthly reports, credit-card paydown tracking, budget targets |
| `subscription-audit` | Find recurring charges in bank exports, decision matrix (keep / replace / cancel) |
| `health-habits` | Log workouts, calculate streaks from CSV, XP / level-up gamification, fitness viz in vault |
| `learning-accelerator` | Study plans, Socratic concept drills, markdown → Anki flashcard CSVs |
| `personal-task-management` | GTD assistant, Socratic prioritization matrix, weekly reviews |
| `time-management` | Calendar around 4:45 AM routine + 45/35/20 work split, energy mapping, conflict resolution |
| `life-admin` | Boston move checklist, medical provider transitions, address changes, renewals, travel planning |
| `career-transition` | PM → Animation Production career arc, portfolio strategy, festival networking |
| `daily-driver` | Morning planning, EOD review, 1-3-5 priorities, integrated with vault daily notes |
| `personal-app-patterns` | Starter patterns when scaffolding small personal apps (React + Vite + Tailwind + Supabase) |

## Primary Agents for This Domain

No domain-specific agents. Uses general-purpose agents (`general-purpose`, `Plan`, `Explore`) and the `data-analyst` agent for finance / health analytics.

## Active MCPs Used Here

- **Gmail** + **Google Calendar** — primarily personal `sean.winslow28@gmail.com` (calendar rule from root CLAUDE.md still applies — query both accounts)
- **Obsidian Vault** — daily notes, finance reports, health logs, task lists
- **Zapier** — Bilt / Chase via Sheets bridge when needed (no native MCP)

## Non-Negotiable Rules Specific to This Domain

1. **Personal data stays local.** Finance and health data lives in vault and on local machines — don't ship to external APIs without explicit Sean approval. Local models (gemma4 / phi4-mini on Mac Mini) handle financial categorization where possible.
2. **No cross-contamination with The Block domain.** Personal Gmail content does not get summarized into Block stakeholder updates, and vice versa. The two email accounts stay segmented.
3. **Sleep window and gym blocks are sacred.** Daily-driver and meeting-defender treat them as protected. Don't propose tasks that violate them.
4. **Health-habits XP is gamified — don't backfill.** Streaks must be earned in real time. Logging a missed workout retroactively breaks the gamification contract.
5. **Boston move context is time-bounded.** Sean is moving from NYC to Boston. Several life-admin items are tied to that arc — once complete, prune them rather than letting them linger as stale checklist items.

## Related Vault Paths

- MOC: [vault/05_atlas/moc-life-systems.md](../vault/05_atlas/moc-life-systems.md)
- Active project: [vault/20_projects/prj-boston-move](../vault/20_projects/prj-boston-move)
- Standalone health data: [vault/health/](../vault/health/)

## When Modifying This Domain

- Update [CHANGELOG.md](../CHANGELOG.md) for any new life-systems-specific skill, agent, hook, or workflow
- Update [vault/05_atlas/operating-models/life-systems/](../vault/05_atlas/operating-models/life-systems/) artifacts when personal cadence / dependencies / friction shifts
- For finance changes: keep regex categorization rules in version control (in the skill, not as one-off scripts) so they're reproducible
