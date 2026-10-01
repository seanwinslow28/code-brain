# craftwork — the shared home every -craft team inherits from

**This folder is shared law.** It holds the law and machinery that every -craft team inherits: Systemcraft, Productcraft, and every team built after them. Each piece lives here **once**. A team's `CLAUDE.md`, master skill and templates link to it and may add a studio binding. They never keep a copy, and they never restate it.

A -craft team is a specialist bench of at least three seats that plans, executes and audits one kind of work. Each team explains every material choice and names what it leaned on from the canon, and keeps its machinery public and its brain private. The two built so far are [systemcraft/](../systemcraft/README.md) (AI PM system design) and [productcraft/](../productcraft/README.md) (product leadership). The shape was decided on the Productcraft build map's [Method extraction: craftwork](https://github.com/seanwinslow28/code-brain/issues/282) ticket (2026-10-01). Everything here is public machinery. Nothing private lives in this folder, and no team's ledger or corpus is read from it. Both teams run on all of it, and the trace kit checks a closed engagement of either one against the same law.

## What lives here

| Path | What it is |
|---|---|
| [law.md](law.md) | The shared law, one section each: name the canon · the audit shape and the three-seat floor · the standing success measure (D+14) · the availability ladder · the self-targeted modifier · model delegation · the alias probe at Route · checks converge (the repair cap and stopping rule) |
| [handoff-contract.md](handoff-contract.md) | The law every crossing between two teams shares: the typed brief, frozen copies stripped of their process parts and hashed, the five crossing states, `crossing.md` in both ledgers, the mirror return, ids as the only thing that crosses. Each sending team keeps one short binding per pair |
| [templates/red-team-protocol.md](templates/red-team-protocol.md) | The adversarial gate: posture, what a gate may demand, typed verdicts, IMPLEMENTATION HOLD, the never-silently-skips fallback. Each team keeps its own gate schedule |
| [templates/close-digest.md](templates/close-digest.md) | The shape of every Close digest to Sean, and the question protocol for every studio↔Sean question |
| [templates/status-vocabulary.md](templates/status-vocabulary.md) | Reader-facing law: which record is authoritative, how proofs and statuses render, cost wording |
| [templates/ledger-entry.md](templates/ledger-entry.md) | The decision-ledger entry schema, with `## From the canon` and the cross-studio id fields |
| [templates/runtime-registry.md](templates/runtime-registry.md) | Every runtime a pass may run on (one row per harness × provider route), its standing, and the trial protocol by which a new one earns its way in |
| [trace/](trace/README.md) | The trace kit: the pass-record, labels and cases templates, the rung-0 checker, the HTML viewer and its DESIGN.md, the registry numbers, the next-id helper, `freeze.py` (the handoff's strip-then-hash), and the shared process-waste failure codes. It holds no studio: each team keeps a `trace/studio.py` profile and its own failure modes, and the kit finds the profile by walking up from the engagement |
| [`/craftwork`](../.claude/skills/craftwork/SKILL.md) | The recipe for building the next team on this home, from partner session to "built": what every team inherits, what each decides for itself, the three-seat floor, the voice-bearing declaration, the naming rule. User-invoked only; it lives in `.claude/skills/` by the house rule and is excluded from export groups |

## How a team is built

The recipe is a user-invoked skill, [`/craftwork`](../.claude/skills/craftwork/SKILL.md), and it builds nothing by itself: each step is owned by the skill or map ticket that does the work. Partner session, then research passes at no cost, then a Wayfinder map whose destination is the team live with its first engagement complete, then the scaffold (public machinery beside a private brain, the ignore rules canary-tested before the first commit, the ledger as its own repo on a private remote, the validator's blessing), then the machinery the map's tickets build, then the first full-train engagement, traced from its first pass. A team is **built** when that engagement has closed, its fourteen-day outcome record is written, and the team has tested its own law against the engagement's trace under a red team on another vendor. Both existing teams' most valuable law changes came from that last step.

Two questions come before any of it. Below three seats a closed audit cycle cannot exist, so a craft that cannot name three distinct seats gets a skill, not a studio. And a team declares at scaffold whether its output carries Sean's voice: if it does, its corpus gains a layer of his own work, a suggestion that improves the craft but flattens the voice is a failure rather than a trade-off, and every engagement opens as either a critique of his draft or a draft from his seed, finished only when he calls it finished.


## What craftwork deliberately does not encode

A team decides these for itself: seat count above the floor of three, corpus shape, lane slugs, artifact templates, engagement types (the self-targeted and handoff modifiers are inherited), the gate schedule, the audit-cycle layout, and its own rules (e.g. Productcraft's "Insights measures, never decides").

**Naming.** Folder `<x>craft/`, master skill `<x>craft`, ledger ids `<two letters>-eng-NNN` (Systemcraft's bare `eng-` ids grandfathered), private ledger remote `seanwinslow28/<x>craft-ledger`.

## Moved here

Every file that moved into this folder, with the path it left. Old links to these paths are re-pointed in the same change. Past pass records keep the old path as the input their seat read. The trace kit follows this table to find the file, so a closed engagement's record stays checkable. If the file's content is unchanged, its hash still matches. If the file has changed since, the record counts that input as unverifiable machinery, the same as any template that improved after its train closed. **Keep the two path columns in backticks**: the kit reads them.

| From | To | Moved |
|---|---|---|
| `systemcraft/templates/red-team-protocol.md` | `craftwork/templates/red-team-protocol.md` | 2026-10-01, #324 (Systemcraft's gate schedule and attack checklists split out to `systemcraft/templates/gate-schedule.md`) |
| `systemcraft/templates/close-digest.md` | `craftwork/templates/close-digest.md` | 2026-10-01, #324 |
| `systemcraft/templates/status-vocabulary.md` | `craftwork/templates/status-vocabulary.md` | 2026-10-01, #324 |
| `productcraft/templates/ledger-entry.md` | `craftwork/templates/ledger-entry.md` | 2026-10-01, #324 |
| `productcraft/templates/runtime-registry.md` | `craftwork/templates/runtime-registry.md` | 2026-10-01, #324 |
| `productcraft/trace/record-template.md` | `craftwork/trace/record-template.md` | 2026-10-01, #325 |
| `productcraft/trace/labels-template.md` | `craftwork/trace/labels-template.md` | 2026-10-01, #325 |
| `productcraft/trace/cases-template.md` | `craftwork/trace/cases-template.md` | 2026-10-01, #325 |
| `productcraft/trace/DESIGN.md` | `craftwork/trace/DESIGN.md` | 2026-10-01, #325 |
| `productcraft/trace/PRODUCT.md` | `craftwork/trace/PRODUCT.md` | 2026-10-01, #325 |
| `productcraft/trace/check.py` | `craftwork/trace/check.py` | 2026-10-01, #325 (with `render.py`, `registry.py`, `nextid.py`, `tracekit/`, `fonts/` and `tests/` beside it) |
| `productcraft/trace/render.py` | `craftwork/trace/render.py` | 2026-10-01, #325 |
| `productcraft/trace/registry.py` | `craftwork/trace/registry.py` | 2026-10-01, #325 |
| `productcraft/trace/nextid.py` | `craftwork/trace/nextid.py` | 2026-10-01, #325 |
| `productcraft/templates/handoff-contract.md` | `craftwork/handoff-contract.md` | 2026-10-01, #326 (rewritten as the generic law; the Productcraft → Systemcraft specifics went to `productcraft/templates/handoff-binding-systemcraft.md`) |

Two kit files stayed at their old paths with new content, so neither has a row. `productcraft/trace/taxonomy.md` kept Productcraft's seat failure modes, and its process-waste family moved into [trace/taxonomy.md](trace/taxonomy.md). `productcraft/trace/README.md` now describes only what Productcraft keeps. A closed record that names either one reads it as machinery that changed since its pass, which is unverifiable, never a failure.

One file was retired rather than moved, so it has no row either: `systemcraft/templates/ledger-entry.md`, Systemcraft's older entry schema, deleted when Systemcraft adopted [templates/ledger-entry.md](templates/ledger-entry.md) on 2026-10-01 ([#327](https://github.com/seanwinslow28/code-brain/issues/327)). No traced engagement ever read it: Systemcraft traces from eng-005 on.

Text that moved out of a master skill or `CLAUDE.md` into [law.md](law.md) is named there, section by section. Those files stay where they are, so nothing in this table follows them.
