---
name: systemcraft
description: Run the Systemcraft studio — the five-seat AI PM system design bench at systemcraft/. Use on explicit summons ("systemcraft", "engage the studio", "/systemcraft") or unambiguous studio-shaped work — designing or auditing an AI product's system, anything wanting the artifact chain (PRD → ADR → failure-UX/model card → eval plan → ops model) or a named seat's lane. On an ambiguous match, ask one clarifying line before launching anything. NOT for generic PM artifacts (pm-* plugin skills own those), Sean's NotebookLM curriculum, or quick factual questions — answer those directly.
---

# Systemcraft — master skill

The studio's orchestrator. **The skill knows the process, the seats know the craft, CLAUDE.md knows the law**: craft lives in [systemcraft/bench/](../../../systemcraft/bench/README.md) (contracts, templates, audit stakes, baselines, corpus discipline), law in [systemcraft/CLAUDE.md](../../../systemcraft/CLAUDE.md) (boundaries, explain-why, fresh-context audits). This file owns only what happens when, and never restates the other two. Excluded from export groups — useless without this repo's corpus and bench.

## Engagement types and routing

*(Amended 2026-08-29 — eng-003.d41, ratified.)* Type by the question being answered and the output owed, not by whether a target already exists.

| Type | Selection test | Routing |
|---|---|---|
| **Design a new project or operating model** | The engagement must choose a new organizing premise or produce a new full artifact chain, including a replacement for an existing system. | All five seats in pipeline order (Strategist → Architecture → Trust → Evals → Ops), no skipping; typed design gates fire. |
| **Audit / improve an existing system** | The engagement tests the behavior, evidence, or fitness of an existing organizing premise before deciding whether to preserve, repair, reframe, or replace it. | Every seat whose lane the target actually has, fresh-context; one audit-close gate. |
| **Support landing a role** | The output is a derivative used in a real role pursuit. | Owning seat(s) only; **real ledger entries, never hypotheticals**; no gate. |
| **Serve employer work** | The target and authority belong to employer work. | Route by the ask's shape; preserve the privacy law absolutely. |
| **Bounded one-off question** | One reversible framing or judgment question can be answered by one owning seat without changing governed state. | One seat, one decision entry, no PRD, roster, build, state mutation, or gate. Adjacent lanes are named only. If the answer creates dependent decisions, implementation, a hard-to-reverse commitment, or a P0-equivalent candidate, stop and retype before further work. A one-off cannot waive an existing phase gate. |

**Self-targeted modifier (eng-003.d41).** When the studio, coordinator, or studio law is the target, Open must additionally: (1) pre-register the questions and the classes of finding the studio cannot produce; (2) record an exact context manifest for every pass; (3) bind live claims to the standing provenance contract; (4) use a fresh independent gate with a different model lineage when available, naming any fallback; and (5) reserve judgment and ratification to Sean while using at least one outcome signal the studio cannot self-issue. No self-targeted engagement may implement or ratify its own expansion; it may only draft it for Sean.

## Standing success measure

*(eng-003.d40/d11/d42/d43, ratified 2026-08-29.)* An engagement succeeds only on **outside use**, judged at **Close + 14 days**: (1) at least one dated use event beyond the ledger names it — shipped, scheduled-with-owner-and-date, stopped/declined, or dependent work actually begun; ratification alone never counts; (2) 100% of the Close-frozen **P0-equivalent** findings carry a dated Sean disposition (`shipped` / `scheduled-with-date` / `explicitly-deferred-with-reason`), delivered one rule-8 ticket per finding at Close; (3) the engagement stayed inside its Open-ratified attention budget. **Close is administrative** — a clean Close records `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`, never success; an unresolved coordinator breach or required-output deferral cannot Close as delivery-complete (`OPEN — DEFERRED`). A month with no due date is NO OBSERVATION, never PASS. *P0-equivalent* (must-handle before dependent work proceeds) = the finding would expose a person/private data/money/hard-to-reverse asset to material harm, make the success claim or its load-bearing evidence materially false, or let a gate/launch/consequential decision cross a known blocking contradiction; the rule is pre-registered at Open, candidates are nominated during Run, and the denominator freezes at Close under Sean's ratification — superseded later, never erased.

## The five phases

**1 — Open.** Type the engagement (table above). Write a one-paragraph brief. Pull relevant past ledger entries via `systemcraft/ledger/index.md` (two hops: index line → entry). Assign the engagement id (`eng-NNN-slug`).

**2 — Route.** State the roster and each seat's model **from its own seat file** — never inherit the session model silently. State any deviations now or as they arise, each with a one-line why (triggers below).

**3 — Run.** Seats draft in pipeline order; hand **full artifacts forward, never summaries**. Every seat invocation is fresh-context: a subagent given its seat file, its lane manifest, and the upstream artifacts — never this conversation. Audits per the bench's closed cycle, also fresh-context, on the auditor's own baseline. Material defects loop back to the drafting seat. The PRD is not done until the Evals co-sign lands. **Ledger writes happen here**: the deciding seat writes an entry at the moment of a material decision (schema: [ledger-entry template](../../../systemcraft/templates/ledger-entry.md)).

**4 — Gate.** Milestone engagements only, per [the red-team protocol](../../../systemcraft/templates/red-team-protocol.md): design engagements gate at PRD sign-off, design-complete, and pre-launch (the third fires only when an implementation candidate exists); audits gate once at close. Verdicts are typed per the protocol. FAIL → redraft one tier up and re-gate. A gate never silently skips; every gate writes its ledger entry.

**5 — Close.** Checklist, in order:
- [ ] Ledger entries complete; one line per entry appended to `ledger/index.md`.
- [ ] Corpus inbox sweep (`systemcraft/corpus/inbox.md`): file each entry or consciously defer — never silently skip.
- [ ] Live deferred work → one rule-8 ticket per item in `vault/00_inbox/tickets.md` (CLAUDE.md rule 8); everything else stays in the ledger for pull.
- [ ] Verify `git status` shows nothing under `systemcraft/{corpus,ledger,books}/` — the private layer never reaches git.
- [ ] Freeze the P0-equivalent denominator (Sean ratifies) and name the D+14 outcome-record date; Close is declared as `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`, never success.
- [ ] Explain-why digest to Sean per [templates/close-digest.md](../../../systemcraft/templates/close-digest.md) — recommendation first, one question, statuses rendered per [templates/status-vocabulary.md](../../../systemcraft/templates/status-vocabulary.md).

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

**Aggregate budget (eng-003.d13/d04, ratified 2026-08-29 — words; tool enforcement gated).** Every Open declares an integer pass budget: the base pass manifest plus **two pre-authorized rounds per scheduled gate** (one owning-seat repair + one re-gate); Ops sets the caps, Sean ratifies them at Open, and **the coordinator's own session counts inside the budget**. An escalation needs both its per-invocation trigger and remaining aggregate allowance; exhaustion is a stop — actual-versus-cap plus one variance question to Sean, never a silent overrun and never a lane-crossing. Every invocation records a meter line (runtime-reported tokens/wall-clock, else `UNMEASURED`); a partial meter reports `known subtotal + N unmeasured passes`, never a precise total.

**Availability ladder (eng-003.d30, ratified as words).** Planned provider unavailable → a **dated Sean-approved vendor substitution that preserves seat identity** (same seat contract, lane, target, and audit duty; a fresh invocation, never inherited context), else a **dated deferral** that stops the dependent branch. Never legal: crossing lanes in one run, drafting seat substance in coordinator context, silent provider/tier switches, merging deferred lanes. Live deferrals become rule-8 tickets at Close.

## Degradation

On a machine without the private layers, seats already carry the ladder (partial → none); the skill's own duty is to say so once at Open and proceed — never fabricate ledger precedent or corpus grounding that can't be read.
