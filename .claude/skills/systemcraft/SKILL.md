---
name: systemcraft
description: Run the Systemcraft studio — the five-seat AI PM system design bench at systemcraft/. Use on explicit summons ("systemcraft", "engage the studio", "/systemcraft") or unambiguous studio-shaped work — designing or auditing an AI product's system, anything wanting the artifact chain (PRD → ADR → failure-UX/model card → eval plan → ops model) or a named seat's lane. On an ambiguous match, ask one clarifying line before launching anything. NOT for generic PM artifacts (pm-* plugin skills own those), Sean's NotebookLM curriculum, or quick factual questions — answer those directly.
---

# Systemcraft — master skill

The studio's orchestrator. **The skill knows the process, the seats know the craft, CLAUDE.md knows the law**: craft lives in [systemcraft/bench/](../../../systemcraft/bench/README.md) (contracts, templates, audit stakes, baselines, corpus discipline), law in [systemcraft/CLAUDE.md](../../../systemcraft/CLAUDE.md) (boundaries, explain-why, fresh-context audits) and, for what every -craft team shares, [craftwork/law.md](../../../craftwork/law.md). This file owns only what happens when, and never restates the other two. Excluded from export groups — useless without this repo's corpus and bench.

## Engagement types and routing

*(Amended 2026-08-29 — eng-003.d41, ratified.)* Type by the question being answered and the output owed, not by whether a target already exists.

| Type | Selection test | Routing |
|---|---|---|
| **Design a new project or operating model** | The engagement must choose a new organizing premise or produce a new full artifact chain, including a replacement for an existing system. | All five seats in pipeline order (Strategist → Architecture → Trust → Evals → Ops), no skipping; typed design gates fire. |
| **Audit / improve an existing system** | The engagement tests the behavior, evidence, or fitness of an existing organizing premise before deciding whether to preserve, repair, reframe, or replace it. | Every seat whose lane the target actually has, fresh-context; one audit-close gate. |
| **Support landing a role** | The output is a derivative used in a real role pursuit. | Owning seat(s) only; **real ledger entries, never hypotheticals**; no gate. |
| **Serve employer work** | The target and authority belong to employer work. | Route by the ask's shape; preserve the privacy law absolutely. |
| **Bounded one-off question** | One reversible framing or judgment question can be answered by one owning seat without changing governed state. | One seat, one decision entry, no PRD, roster, build, state mutation, or gate. Adjacent lanes are named only. If the answer creates dependent decisions, implementation, a hard-to-reverse commitment, or a P0-equivalent candidate, stop and retype before further work. A one-off cannot waive an existing phase gate. |

**Self-targeted modifier (eng-003.d41).** When the studio, coordinator, or studio law is the target, Open adds the five duties of [craftwork law § Self-targeted modifier](../../../craftwork/law.md#self-targeted-modifier) (shared law since 2026-10-01, text unchanged).

**Handoff modifier (Productcraft build map #271, ratified 2026-09-11).** When the engagement opens from another studio's handoff brief — Productcraft's Delivery seat crossing a *design* ask (typed *Design a new project*) or an audit finding (typed *Audit / improve*) — the authority is [the handoff contract](../../../productcraft/templates/handoff-contract.md) and Open must additionally: (1) have the **Design Strategist run a fresh-context intake check** on the brief and issue its typed state — `accepted`, `input-required` (named gaps, no engagement opened), or `rejected` (reason, no engagement opened) — into `crossing.md` on both sides and this engagement's Open entry; the check asks only *can I do my job from this packet*, never whether the product decision was right; (2) set `originates_from: <brief id>` on the brief and every ledger entry; (3) treat the six **frozen, hashed copies** in `handoff/inbound/artifacts/` as the seats' upstream artifacts — the PRD's problem, users and assumptions inherit the sender's graded evidence; the studio never re-runs discovery or re-litigates the product decision, and a Productcraft artifact edited after the crossing does not move the target. Close then packages the return per [handoff-return.md](../../../systemcraft/templates/handoff-return.md) (see the Close checklist). Reasoning never crosses in either direction; ids do.

## Standing success measure

*(eng-003.d40/d11/d42/d43, ratified 2026-08-29.)* An engagement succeeds only on outside use at Close + 14 days, every Close-frozen P0-equivalent finding carries a dated Sean disposition, and Close is declared `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`, never success. The authority, including the P0-equivalent definition, is [craftwork law § Standing success measure](../../../craftwork/law.md#standing-success-measure) (shared law since 2026-10-01, text unchanged).

## The five phases

**1 — Open.** Type the engagement (table above). Write a one-paragraph brief. Pull relevant past ledger entries via `systemcraft/ledger/index.md` (two hops: index line → entry). Assign the engagement id (`eng-NNN-slug`).

**2 — Route.** State the roster and each seat's model **from its own seat file** — never inherit the session model silently. State any deviations now or as they arise, each with a one-line why (triggers below).

**3 — Run.** Seats draft in pipeline order; hand **full artifacts forward, never summaries**. Every seat invocation is fresh-context: a subagent given its seat file, its lane manifest, and the upstream artifacts — never this conversation. Audits per the bench's closed cycle, also fresh-context, on the auditor's own baseline. Material defects loop back to the drafting seat. The PRD is not done until the Evals co-sign lands. **Ledger writes happen here**: the deciding seat writes an entry at the moment of a material decision (schema: [ledger-entry template](../../../systemcraft/templates/ledger-entry.md) until Systemcraft adopts [the shared schema](../../../craftwork/templates/ledger-entry.md) at [craftwork build 4](https://github.com/seanwinslow28/code-brain/issues/327)).

**4 — Gate.** Milestone engagements only, per [the red-team protocol](../../../craftwork/templates/red-team-protocol.md) (shared law) and [Systemcraft's gate schedule](../../../systemcraft/templates/gate-schedule.md): design engagements gate at PRD sign-off, design-complete, and pre-launch (the third fires only when an implementation candidate exists); audits gate once at close. Verdicts are typed per the protocol. FAIL → redraft one tier up and re-gate. A gate never silently skips; every gate writes its ledger entry.

**5 — Close.** Checklist, in order:
- [ ] Ledger entries complete; one line per entry appended to `ledger/index.md`.
- [ ] Corpus inbox sweep (`systemcraft/corpus/inbox.md`): file each entry or consciously defer — never silently skip.
- [ ] Live deferred work → one rule-8 ticket per item in `vault/00_inbox/tickets.md` (CLAUDE.md rule 8); everything else stays in the ledger for pull.
- [ ] Verify `git status` shows nothing under `systemcraft/{corpus,ledger,books}/` — the private layer never reaches git.
- [ ] Commit and push the ledger's own repo: `git -C systemcraft/ledger add -A && git -C systemcraft/ledger commit -m "<eng-id>: <close gist>" && git -C systemcraft/ledger push` — the ledger is its own git repo with a **private** remote (`seanwinslow28/systemcraft-ledger`, 2026-09-10); an unpushed ledger exists on one laptop only. Sessions are one per ticket, so every session that touched the ledger pushes before it ends, not just Close.
- [ ] Freeze the P0-equivalent denominator (Sean ratifies) and name the D+14 outcome-record date; Close is declared as `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`, never success.
- [ ] **Handoff engagements only:** after Gate 2, the Design Strategist writes the return note per [templates/handoff-return.md](../../../systemcraft/templates/handoff-return.md), freezes the five artifacts with hashes into `handoff/outbound/`, copies the packet into the sender's `handoff/inbound/`, appends `returned` (or `returned-partial`, with the deferred lane's rule-8 ticket) to `crossing.md` on both sides, and confirms `supersedes_external` is set on every entry that overturned a product assumption. Gate 3 is recorded `NOT FIRED — IMPLEMENTATION ABSENT` until the sender's `candidate-note.md` arrives.
- [ ] Explain-why digest to Sean per [the close digest](../../../craftwork/templates/close-digest.md) — recommendation first, one question, statuses rendered per [the status vocabulary](../../../craftwork/templates/status-vocabulary.md) (both shared law).

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

**Availability ladder (eng-003.d30, ratified as words).** An unavailable planned provider gets a dated Sean-approved substitution that preserves seat identity, else a dated deferral of the dependent branch; never a merged lane or a silent switch. The authority is [craftwork law § Availability ladder](../../../craftwork/law.md#availability-ladder) (shared law since 2026-10-01).

## Degradation

On a machine without the private layers, seats already carry the ladder (partial → none); the skill's own duty is to say so once at Open and proceed — never fabricate ledger precedent or corpus grounding that can't be read.
