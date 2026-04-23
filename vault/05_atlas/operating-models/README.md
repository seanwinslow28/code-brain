---
type: moc
domain: [the-block, creative-studio, life-systems]
status: index
created: 2026-04-18
ai-context: "Index for the operating-model artifact bundles. One subfolder per domain, five artifacts per bundle. Populated by the work-operating-model skill."
---

# Operating Models

This folder holds five-artifact bundles per domain that capture how Sean actually works — operating rhythms, decision patterns, dependencies, institutional knowledge, and friction. Downstream agents (`meeting-defender`, `daily-driver`, `sprint-health`, `process-inbox`, `pr-digest`) load these to act with real context.

The five artifact types per domain:

| File | Captures | Layer |
|---|---|---|
| `HEARTBEAT.md` | Operating rhythms (daily / weekly / monthly) | 1 |
| `USER.md` | Recurring decisions and prioritization criteria | 2 |
| `SOUL.md` | Dependencies (Part A) + institutional knowledge (Part B) | 3+4 |
| `operating-model.md` | Synthesized one-file profile | (synthesis) |
| `schedule-recommendations.md` | Friction-derived calendar/automation rules | 5 |

## Domain bundles

- [[the-block/HEARTBEAT|The Block — day job (PM at crypto/ETF company)]]
- [[creative-studio/HEARTBEAT|Creative Studio — 16BitFit, Remotion, art, writing]]
- [[life-systems/HEARTBEAT|Life Systems — finance, health, learning, time, career]]

## How to populate

Run the skill: `Run the work-operating-model interview for the-block` (or `creative-studio`, `life-systems`).

The skill walks the [5-layer interview](../../../.claude/skills/work-operating-model/interview-questions.md) and writes outputs to the matching subfolder. Each artifact starts with `status: awaiting-interview` → `draft` → `confirmed`.

## Tier-0 identity

Sits above all three domain bundles: [[../Sean-Winslow-Full-Personal-Context-v1.1|Full Personal Context v1.1]]. To be updated to v2.0 once all three operating-model bundles are confirmed.
