---
type: moc
domain: [creative-studio, life-systems, job-hunt-2026]
status: index
created: 2026-04-18
ai-context: "Index for the operating-model artifact bundles. One subfolder per domain, five artifacts per bundle. Populated by the work-operating-model skill. The the-block bundle was archived 2026-05 to vault/60_archive/operating-models-the-block-2026-05/ following Sean's layoff."
---

# Operating Models

This folder holds five-artifact bundles per domain that capture how Sean actually works — operating rhythms, decision patterns, dependencies, institutional knowledge, and friction. Downstream agents (`daily-driver`, `meta_agent`, `flush`, `knowledge_lint`) load these to act with real context.

The five artifact types per domain:

| File | Captures | Layer |
|---|---|---|
| `HEARTBEAT.md` | Operating rhythms (daily / weekly / monthly) | 1 |
| `USER.md` | Recurring decisions and prioritization criteria | 2 |
| `SOUL.md` | Dependencies (Part A) + institutional knowledge (Part B) | 3+4 |
| `operating-model.md` | Synthesized one-file profile | (synthesis) |
| `schedule-recommendations.md` | Friction-derived calendar/automation rules | 5 |

## Domain bundles

- [[creative-studio/HEARTBEAT|Creative Studio — 16BitFit, Remotion, art, writing]]
- [[life-systems/HEARTBEAT|Life Systems — finance, health, learning, time, career]]
- [[job-hunt-2026/HEARTBEAT|Job Hunt 2026 — 8-week post-Block search, AI/Tech/Creative PM]]
- *Archived 2026-05:* The Block bundle moved to `vault/60_archive/operating-models-the-block-2026-05/` after Sean's layoff. Selectable for re-running historical interviews; not loaded by active agents.

## How to populate

Run the skill: `Run the work-operating-model interview for creative-studio` (or `life-systems`, `job-hunt-2026`).

The skill walks the [5-layer interview](../../../.claude/skills/work-operating-model/interview-questions.md) and writes outputs to the matching subfolder. Each artifact starts with `status: awaiting-interview` → `draft` → `confirmed`.

## Tier-0 identity

Sits above all three domain bundles: [[Sean-Winslow-Full-Personal-Context-v2.0|Full Personal Context v2.0]]. Bumped from v1.1 on 2026-05-02 (interview-driven refresh — see [_archive/Sean-Winslow-Profiles-For-Context/](../../../_archive/Sean-Winslow-Profiles-For-Context/) for the v1.1 archive).
