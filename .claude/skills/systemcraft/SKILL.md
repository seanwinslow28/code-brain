---
name: systemcraft
description: Run the Systemcraft studio — the five-seat AI PM system design bench at systemcraft/. Use on explicit summons ("systemcraft", "engage the studio", "/systemcraft") or unambiguous studio-shaped work — designing or auditing an AI product's system, anything wanting the artifact chain (PRD → ADR → failure-UX/model card → eval plan → ops model) or a named seat's lane. On an ambiguous match, ask one clarifying line before launching anything. NOT for generic PM artifacts (pm-* plugin skills own those), Sean's NotebookLM curriculum, or quick factual questions — answer those directly.
---

# Systemcraft — master skill

The studio's orchestrator. **The skill knows the process, the seats know the craft, CLAUDE.md knows the law**: craft lives in [systemcraft/bench/](../../../systemcraft/bench/README.md) (contracts, templates, audit stakes, baselines, corpus discipline), law in [systemcraft/CLAUDE.md](../../../systemcraft/CLAUDE.md) (boundaries, explain-why, fresh-context audits). This file owns only what happens when, and never restates the other two. Excluded from export groups — useless without this repo's corpus and bench.

## Engagement types and routing

Type the engagement first; the type fixes the roster.

| Type | Routing |
|---|---|
| **Design a new project** | All five seats, pipeline order (Strategist → Architecture → Trust → Evals → Ops), no skipping. Milestone: gates fire. |
| **Audit / improve an existing system** | Every seat whose lane the target actually has; each audits its own lane, fresh-context. One gate at close. |
| **Support landing a role** | Derivative artifacts cut from **real ledger entries, never hypotheticals**; owning seat(s) only. No gate. |
| **Serve employer work** | Same machinery on employer problems; route by the ask's shape (full train for a new design, subset otherwise). Honor the law's privacy boundary absolutely. |

A one-off question routes to the owning seat alone, which must name any adjacent lane it noticed but didn't cover — skipped lanes are visible, never silent.

## The five phases

**1 — Open.** Type the engagement (table above). Write a one-paragraph brief. Pull relevant past ledger entries via `systemcraft/ledger/index.md` (two hops: index line → entry). Assign the engagement id (`eng-NNN-slug`).

**2 — Route.** State the roster and each seat's model **from its own seat file** — never inherit the session model silently. State any deviations now or as they arise, each with a one-line why (triggers below).

**3 — Run.** Seats draft in pipeline order; hand **full artifacts forward, never summaries**. Every seat invocation is fresh-context: a subagent given its seat file, its lane manifest, and the upstream artifacts — never this conversation. Audits per the bench's closed cycle, also fresh-context, on the auditor's own baseline. Material defects loop back to the drafting seat. The PRD is not done until the Evals co-sign lands. **Ledger writes happen here**: the deciding seat writes an entry at the moment of a material decision (schema: [ledger-entry template](../../../systemcraft/templates/ledger-entry.md)).

**4 — Gate.** Milestone engagements only, per [the red-team protocol](../../../systemcraft/templates/red-team-protocol.md): design engagements gate at PRD sign-off and pre-launch; audits gate once at close. FAIL → redraft one tier up and re-gate. A gate never silently skips; every gate writes its ledger entry.

**5 — Close.** Checklist, in order:
- [ ] Ledger entries complete; one line per entry appended to `ledger/index.md`.
- [ ] Corpus inbox sweep (`systemcraft/corpus/inbox.md`): file each entry or consciously defer — never silently skip.
- [ ] Live deferred work → one rule-8 ticket per item in `vault/00_inbox/tickets.md` (CLAUDE.md rule 8); everything else stays in the ledger for pull.
- [ ] Verify `git status` shows nothing under `systemcraft/{corpus,ledger,books}/` — the private layer never reaches git.
- [ ] Explain-why digest to Sean: the material choices, one breath each, why-A-over-B.

## Model deviations (named triggers, per-task, never per-engagement)

**Escalate one tier** (Sonnet→Opus; Opus→Fable at milestones — Fable is the ceiling) on any of:
1. Milestone artifact — the output feeds a red-team gate.
2. Thin corpus — the lane manifest has no pointer for the topic.
3. Redraft after an audit bounced substance (same brain, same blind spots).
4. Hard-to-reverse commitment (build-vs-buy, vendor lock-in, data-model choices).
5. Novel engagement shape with no ledger precedent.

**Downshift** (to Sonnet; Haiku floor, mechanical work only) on any of:
1. Mechanical transform of existing substance.
2. Single-source corpus lookup.
3. Objective checklist application.
4. Inbox-filing clerical work (the file-or-defer *decision* stays at baseline).

Guardrails: audits never run below the auditor seat's baseline; every deviation logs its one-line why. No silent deviations, ever.

## Degradation

On a machine without the private layers, seats already carry the ladder (partial → none); the skill's own duty is to say so once at Open and proceed — never fabricate ledger precedent or corpus grounding that can't be read.
