---
title: "Groundwork v1→v2 fit check — agentic-web company shape (light)"
date: 2026-08-29
project: agentic-web-startup
type: audit-delta
status: final
tags: [agentic-web, groundwork, fleet-os, research-sprint]
---

# Groundwork fit check — what carries, what the new company shape would strain

Sprint item 2 per the [kickoff](../../../docs/prompts/2026-08-29-agentic-web-research-sprint-kickoff.md):
the 2026-08-08 groundwork audit was done for driftgate; this is the light product-agnostic
re-read. **Scope discipline: notes only, no fixes, no verdict on groundwork-vs-alternatives —
that comparison belongs to a partner session, informed by the
[literature synthesis](2026-08-29-software-factory-literature-synthesis.md).**

## First: the audit's snapshot is stale in details, not in shape

Groundwork has **131 commits since the 8/08 audit** (last: 2026-08-29). Material changes,
verified in-repo today:

- **SCHEMA_VERSION 1 → 2** — "roles as the accountable unit": a `governance/roles.md`
  roster with typed holders, held-to-activate resolution of constitution-rule owner
  fields, review-record rules. (The audit reviewed v1.)
- **Per-check `since:` demotion is now code**, not "documented intent" as the audit
  recorded — v2 checks demote to WARN on v1-pinned content (`MIGRATIONS.md`).
- **The evidence floor (mechanic 5)** landed in the interview: practice claims carry
  their basis, typed divergence evidence, observables-only generation, halt rules.
- **Standing rules 8 and 9** ("pre-made text is not pre-verified"; rejection categories
  + consent-gate exception) — the honesty machinery got teeth it lacked in v1.
- Dozens of Codex adversarial review rounds on each slice — the build process itself now
  resembles the doer/grader separation the factory literature prescribes.

None of this changes the audit's verdict shape: **groundwork is the constitution and org
chart; it is, by design, none of the nervous system.** That division of labor is fully
product-agnostic and carries to any company the fleet builds.

## What carries product-agnostically (no strain)

From the [8/08 audit](2026-08-08-groundwork-v1-audit.md), unchanged by the pivot:

1. **The adopt-as-governance-layer posture.** "Do NOT grow an engine inside groundwork"
   — the Never list (no runtime, no memory engine, no hosted anything) matches the
   factory literature's own doctrine (durable inspectable state; humans hold the commit
   bit; hard steers over soft). Nothing about that was driftgate-specific.
2. **Owner's Cards, describability gate, blast-radius routing, governed memory,
   two-repo model.** All product-independent accountability plumbing. The v2 roles
   roster strengthens this half (owner fields now resolve to typed, held roles).
3. **The three-way build split** (extend groundwork with *content*; build the runtime
   *beside* it; build both eval layers) — still the right frame. Sean's agents-sdk
   primitives (hybrid_router, cap_policy, manifests, circuit breakers) still cover much
   of the runtime column.
4. **The dogfooding story**: whichever product wins Sept 1, the company would still be
   groundwork's first real adopter — the interview remains untested instrumentation
   (still no real-company run; the simulated run's planted-fact extraction scored in
   the lowest diagnostic band).

## What the new company shape would strain (noted, not fixed)

1. **Fleet-role ontology is still the #1 content gap, and the pivot raises its price.**
   v2 "roles" are accountability holders for rule owner fields — *not* fleet topology
   (who orchestrates, who validates, who judges, who may overrule whom). The 8/08 audit
   flagged this as the one L1 need with no representable form; 131 commits later that
   is still true. A factory-builds-product company hits this gap on day one.
2. **The interview presumes an existing operating reality to interview.** Its ontologies
   map human company functions (sales, HR, customer success) and its questions mine
   "the work each function actually does." A pre-product solo company whose "team" is
   the fleet has almost no such reality yet — driftgate's generated OS (2026-08-10)
   worked because the 8/07–8/08 campaign had already produced decisions to transcribe.
   The new company would either re-run generation *after* the Sept-1 pick lands enough
   decisions, or start from a thinner OS than the protocol assumes.
3. **Enforcement parity got MORE acute, not less.** Hooks remain Claude-Code-only;
   Sean's ask explicitly wants a mixed closed+open fleet (Codex, Gemini, local Qwen).
   Every forbidden action binds only as instruction outside Claude Code unless the
   runtime mediates all side effects. The literature's convergent answer (Stripe's
   deterministic blueprint nodes; OpenAI's linters-as-gates) is runtime-side — which is
   consistent with the audit's split, but it means the *runtime* budget line, not the
   groundwork one, carries the governance load for non-Claude agents.
4. **Review-queue mechanics remain absent, and the new territory makes that ironic.**
   The primary product territory is observability (journey evals + agent analytics);
   the founder's own fleet OS still surfaces pending work only as files and PRs. At 25
   hrs/week the consolidated review inbox is the choke point the audit named — and the
   company would be selling the cure for a disease its own OS still has.
5. **Migration friction is real but small:** driftgate's generated OS is pinned at
   schema v1; a fresh company OS would generate at v2. Reusing driftgate's generated
   artifacts wholesale would cross the v1→v2 migration gate — fine if intended, worth
   knowing before anyone copies files.

## For the groundwork-vs-alternatives comparison (not prejudged here)

The literature adds one genuinely new datapoint since the 8/08 audit: OpenAI's harness
team runs a working factory on a **repo-as-system-of-record shape with no separate
governance layer at all** — ~100-line AGENTS.md as a map, versioned docs/ tree, plans as
first-class artifacts, invariants enforced by generated linters rather than a validator
("anything [the agent] can't access in-context while running effectively doesn't
exist"). That is the strongest published non-groundwork path. What it conspicuously
lacks — and what groundwork uniquely has — is human accountability structure: named
owners, death conditions, blast-radius consent, an interview that refuses to invent
answers. Which half matters more for a one-founder company is a partner-session
question; both halves are now evidenced.

## Provenance

- Prior audit: [2026-08-08-groundwork-v1-audit.md](2026-08-08-groundwork-v1-audit.md)
- Repo re-checked 2026-08-29: `/Users/seanwinslow/Code-Brain/groundwork/` (`git log
  --since=2026-08-08` = 131 commits; `SCHEMA_VERSION = 2` in `scripts/validate.py`;
  `governance/roles.md`; `MIGRATIONS.md` per-check `since:` section)
- Literature: [2026-08-29-software-factory-literature-synthesis.md](2026-08-29-software-factory-literature-synthesis.md)
  and evidence in [2026-08-29-software-factory-lit-delta/](2026-08-29-software-factory-lit-delta/)
