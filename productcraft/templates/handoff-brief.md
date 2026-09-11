# Handoff brief template

The outbound packet of [the Systemcraft handoff contract](handoff-contract.md). Owned by the **Delivery & Execution Lead**, written right after its OKR section is co-signed at stage 6 and before Leadership runs (or by the closing seat of an audit engagement). A typed packet of references: the six frozen artifact copies travel *beside* it in `handoff/outbound/artifacts/`, never inside it. The Codex red-team gate fires on this file before it crosses; Systemcraft's Design Strategist issues the crossing state on arrival.

Filled briefs are **private** (`ledger/engagements/<eng-id>/handoff/outbound/brief.md`); this template is public machinery. Brevity law applies: every section reads in a breath. The brief carries no reasoning — the why lives in the ledger entry that files it.

```markdown
---
id: pc-eng-001.handoff
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-20
seat: delivery-execution
ledger_entry: pc-eng-001.d31          # the entry that decided to hand off (hands_off_to set there)
trigger: first-slice-systemcraft-layer   # first-slice-systemcraft-layer | audit-finding-in-systemcraft-lane
receive_as: design                    # design | audit — which Systemcraft engagement type this asks for
return_by: 2026-10-04                 # the return date; a miss is a variance question before the date
gate: pending                         # pending | PASS <date> | PASS WITH ACCEPTANCES <date> — blocks crossing
state: null                           # written by the receiving seat: accepted | input-required | rejected
---

## The ask

Decisions Systemcraft owns, stated as questions, one per line, each with an id the return answers by.

| Id | Question | Why it is Systemcraft's |
|---|---|---|
| Q1 | | |

## Referenced artifacts

The six frozen copies in `artifacts/`, by permanent id. The manifest holds the hashes; this table says what each one is for.

| Source id | Artifact | What Systemcraft should take from it |
|---|---|---|
| pc-eng-001.strategy | Strategy & POV doc | |
| pc-eng-001.discovery | Discovery packet (co-signed) | |
| pc-eng-001.insights | Metrics & evidence plan | |
| pc-eng-001.growth | Growth model & GTM plan | |
| pc-eng-001.business | Business case | |
| pc-eng-001.roadmap | Outcome roadmap (OKR section co-signed) | |

## Constraints

- **First shipping slice** — what ships first and by when (from the roadmap).
- **Metrics the eval plan must serve** — the input metrics by name (from the Insights plan).
- **Cash and pricing envelope** — what the design may cost to run and what it may charge (from the business case).
- **Non-goals inherited** — the strategy's non-goals Systemcraft must not design around.
- **Privacy and data** — what may not leave the org, what may not be logged.
- **Budget envelope** — optional; a pass-budget or spend cap Sean ratifies at Systemcraft's Open.

## Stays behind

Raw evidence pointers Systemcraft may follow on this disk but does not receive: one line per pointer, with the claim it supports.
```

## Filing

1. Freeze the six copies: write each into `handoff/outbound/artifacts/<source-id>--<slug>.md` with `frozen_from`, `sha256`, `frozen_at` in its frontmatter; one line each in `manifest.md`.
2. Write the ledger entry that decides the handoff (`hands_off_to: eng-NNN` once Systemcraft assigns the id; `none` on a no-handoff verdict, which still gets its entry).
3. Run the Codex gate on this file; record the verdict in `gate:` and in the entry's `## Checks`.
4. Copy `brief.md`, `manifest.md` and `artifacts/` into Systemcraft's engagement `handoff/inbound/`; open `crossing.md` on both sides with `crossed · <date> · delivery-execution · <one line>`.
5. Wait for the state. `input-required` → repair and re-cross (re-gate only if the ask changed). `rejected` → record it, retype or drop.
