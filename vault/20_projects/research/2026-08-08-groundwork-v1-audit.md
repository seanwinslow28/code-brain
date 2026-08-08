---
title: "Groundwork v1 audit — campaign step 3 (fleet OS gap list)"
date: 2026-08-08
project: agent-company-founding
type: audit
status: final
tags: [agent-company, groundwork, fleet-os, L10-campaign]
---

# Groundwork v1 audit — what the fleet OS satisfies today, what the company needs

Campaign step 3 per the [L10] research front-load. Question from the kickoff:
groundwork as the fleet OS — what it satisfies today, what the company needs it
to satisfy, gap list. Feeds step 4 (architecture ratification): specifically
TOP-TEN items #2 (deterministic pipeline boundary), #7 (autonomy/permission
matrix), #8 (orchestration topology) from the
[literature review](2026-08-08-software-factory-literature-review.md).

## State of the repo (verified 2026-08-08)

Ahead of the code-brain ticket's snapshot: all 20 wayfinder decision tickets
(#2–#21) are CLOSED; only the map issue (#1) stays open. v1 exists with its
decisions resolved and recorded in `CONTEXT.md` as a ubiquitous language
(ontology tiers, Owner's Card spine, describability gate, three-bucket
proposal routing, version-skew policy, consent gate/ladder, synthetic-demo
verification, positioning/attribution doctrine). `python3 scripts/validate.py .`
runs clean on the repo itself (0 errors, 7 benign high-entropy warnings).
`docs/known-limitations.md` is load-bearing and honest — the enforcement teeth
are the human commit bit plus a Claude-Code-only hook layer; every other
harness gets instruction-strength governance.

## Verdict summary

**Groundwork is the constitution and org chart of the company — genuinely
built, validator-enforced where a field backs a running agent, and honest
about its limits. It is, by explicit design ("files, not an engine"; the
roadmap's "Never" list), none of the nervous system.** The company must build
a runtime layer that treats groundwork's cards, rules, and memory records as
declarative config — plus both eval layers, of which the product-eval layer
literally IS the product.

## Gap analysis (12 company needs vs what exists — audit agent, verbatim)

# Groundwork Gap Analysis — fleet OS for a multimodal series-consistency-checker company

Audited read-only at `/Users/seanwinslow/Code-Brain/groundwork/`. Verdicts are against what is in the files, not the README's ambitions — though notably the two rarely diverge; this repo under-claims more than it over-claims.

| # | Need | Verdict | Evidence (paths) | What's missing / where the fix belongs |
|---|---|---|---|---|
| 1 | Agent roles/ontologies, non-overlapping | **PARTIAL** | Two-tier function ontologies (`/Users/seanwinslow/Code-Brain/groundwork/ontologies/README.md`) + per-skill non-overlap doctrine: `description` is "the selection surface... **non-overlapping** with other skills (agents mis-select at 30+ overlapping tools)" (`skills/work-package-spec.md`). | The convention answers the L1 ask for *skills*, but ontologies map **human company functions** (sales, HR), not fleet topology — orchestrator→validator→judge relationships (who calls whom, who may overrule whom) have no representable form. A fleet-role ontology is new *content* plus a small schema extension; fits "files, not an engine" cleanly. |
| 2 | Accountability: owners, forbidden actions, kill/pause | **SATISFIED** | Owner's Card spine requires `owner`, `backup_owner`, `forbidden_actions`, `pause_condition`, `retirement_condition` on every card, human-authored only — generator refuses to invent them (`skills/work-package-spec.md`; worked example `skills/feature-request-triage/owner-card.md`; validator-enforced per `docs/rule-map.md`). | This is groundwork's core lane and it is genuinely built. Caveat: pause/retirement conditions are prose a human reads, not runtime kill switches. |
| 3 | Orchestration runtime: pipelines, queues, retries, handoffs | **MISSING** (by explicit design) | `docs/roadmap.md` "Never": "**No agent runtime.** The harness is the runtime." Closest artifacts are prose exception paths (`gate_exception_path` in `ontologies/product/feature-request-triage.md`) and `pause_condition`s. | State machines, task queues, retry/escalation logic are runtime by nature. Conflicts with the philosophy on purpose — build it as a separate layer (your agents-sdk shape) that *reads* groundwork's cards and rules as its config. |
| 4 | Verification stack: gates, judge, no self-approval | **PARTIAL** | Deterministic gate: `scripts/validate.py` (3,694 lines, stdlib-only) + high-risk hook `governance/hooks/action_class_gate.py`. Worker-never-self-approves exists structurally: agents propose, only the human commit bit lands (`proposals/README.md`), plus per-skill `gate_review_gate`/`review_sample`. | No LLM-as-judge anywhere. Hooks are Claude-Code-only; Codex/Cursor/Gemini degrade to instruction-strength (`docs/known-limitations.md`), and "the gate is not installed in this repo" itself. Judge wiring is runtime; a judge *charter* (what it may rule on, owner, appeal) fits as files. |
| 5 | Eval infrastructure: eval sets, runners, regression | **MISSING** | Roadmap V3: "An evaluations and traces recipe for skills that actually run" — explicitly not built. Seed exists: captured pre-provisioning baselines as governed memory (`memory/feature-request-triage-baseline.md`) and `success_standard` measured against baseline. `validate.py` is a structural linter, not an eval runner. | Both eval layers (fleet-evals and product-evals) must be built. Eval-set *conventions* (cases as files, owners, provenance) fit groundwork's philosophy; runners and regression dashboards do not — separate layer. |
| 6 | Tracing/observability: trace schema, Arize | **MISSING** | Zero hits for Arize/telemetry/trace-schema anywhere in product content; traces named only as the V3 recipe (`docs/roadmap.md`). | Entirely runtime-layer. Groundwork could at most hold the *policy* file (what must be traced, retention, owner). |
| 7 | Model routing: closed/open mix, per-task assignment | **MISSING** | `substrate:` field means systems of record ("The issue tracker + CRM..."), not models (`ontologies/product/feature-request-triage.md`; `interview/questions.md` line 71). Harness-agnostic by design — deliberately silent on model choice. | A model-assignment field per skill/card would fit as files; the router itself (like your `hybrid_router.py`) is runtime. |
| 8 | Agent memory: continuity, provenance, poisoning defense | **PARTIAL** | Strong *governance* of memory: provenance labels, append-and-supersede immutability enforced by `validate.py --diff` (edits to frozen fields ERROR), forward-only promotion, per-skill Memory row (reads/writes/run-only) — `memory/README.md`, `skills/feature-request-triage/SKILL.md`. These are real poisoning defenses at the record layer. | Session-to-session recall/retrieval explicitly delegated: "session recall and retrieval belong to the harness"; "No memory or retrieval engine" (roadmap Never). Continuity mechanics = runtime layer, reading groundwork-governed records. |
| 9 | Change management: proposal, review, blast radius | **SATISFIED** | The whole consent-gate apparatus: proposal schema (diff, reason, evidence, blast-radius declaration), three-bucket routing (track1-body auto-apply + append-only `governance/changelog.md`; escalating → human sign-off), and the `--diff` declared-vs-actual tripwire that catches a rule edit smuggled under a track-1 label (`proposals/README.md`, `governance/README.md`, `CONTEXT.md` #17/#18). | Best-in-class for a files-based system. Caveats: routes **skills and rules only**, and the tripwire fires only under a `groundwork.pin` root; it cannot prove a human actually reviewed (commit bit is the teeth — `docs/known-limitations.md`). |
| 10 | Cost governance: budget caps, spend tracking | **MISSING** | Every "budget" in the repo is the *context/token* budget (#13, `docs/known-limitations.md`); the finance ontology is about the fictional company's own spend approvals, not fleet opex. No caps, no spend ledger. | Cap *policy* as a file (per-agent $/run, monthly ceiling, owner, breach = pause_condition) fits the philosophy; metering and enforcement are runtime. Sean's code-brain `cap_policy.json` pattern is the missing piece, not groundwork. |
| 11 | Human-in-the-loop: review queues, approval gates | **PARTIAL** | Approval gates are pervasive as convention: `proposed_only_actions`, per-activity `gate_review_gate`, track-2 `review_sample`, the `human-decision` rung ("there is no rung six" — `governance/README.md`, `governance/constitution/access-grants-need-human-signoff.md`), draft-PR consent ladder. Hook hard-blocks high-risk actions pending "a named human sign-off." | No review *queue* mechanics — pending work surfaces only as unassigned items, pending proposals, and PRs. For 25 founder-hrs/week you need a consolidated review inbox; that's runtime/UI, not files. |
| 12 | Product-pipeline hosting | **MISSING** (by design, correctly) | "No hosted anything. No server... No agent runtime" (`docs/roadmap.md` Never). Nothing in the repo executes work; even the interview generator "is documents, not a program" (`README.md`). | The product — the multimodal drift checker with receipts — is application software groundwork was never meant to host. It belongs in its own repo/runtime; groundwork can only govern the *company* that builds and operates it. |

## SHAPE OF THE GAP

Groundwork is the accountability and change-control half of a fleet OS and roughly none of the execution half: it fully delivers needs 2 and 9 (owners, forbidden actions, death conditions, blast-radius-routed change consent) and gives real partial credit on 1, 4, 8, and 11 — but orchestration, evals, tracing, model routing, cost metering, and the product pipeline itself (3, 5, 6, 7, 10, 12) are all absent, and mostly absent *on purpose*, per the roadmap's "Never" list. The honest framing: groundwork is the constitution and org chart; the company must still build the entire nervous system — a runtime layer (state machines, queues, retries, router, Arize instrumentation, budget meters, review inbox) that treats groundwork's cards, rules, and memory records as its declarative config, plus both eval layers, of which the product-eval layer literally *is* the product. The philosophy conflicts with production-fleet needs in exactly one place worth naming: "files, not an engine" means enforcement is instruction-strength everywhere except Claude Code hooks, and the repo says so itself — pause conditions, forbidden actions, and refusals bind only as long as the runtime you build chooses to read and enforce them. That's not a reason to reject groundwork; it's the spec for what to build next to it — and the repo's unusual honesty about its own limits (`docs/known-limitations.md`) makes it a trustworthy foundation for exactly that division of labor.

## Capability inventory (audit agent, verbatim)

# Groundwork v1 — Capability Inventory

## 1. WHAT IT IS

Groundwork is a repo of markdown conventions plus one 3,694-line zero-dependency Python validator (`scripts/validate.py`) — there is no runtime, server, generator script, or database; agents follow protocol documents and the validator gates the output. The validator mechanically enforces structure (frontmatter fields, one canonical table grammar, referential link integrity, secrets floor, append-only memory/changelog under `--diff`, blast-radius-vs-proposal matching on pinned content), while everything behavioral — the interview, generation, the demo's governance refusal, cross-harness enforcement — is instruction-strength prose an agent may or may not follow. The real enforcement backstop is explicitly named as the human commit bit ("agents propose; humans land"), not the validator, and the repo itself says no real company has ever run the interview (`README.md:167-174`, `AGENTS.md:13-21`).

## 2. CAPABILITY TABLE

| Subsystem | What it provides | Enforcement level | File evidence |
|---|---|---|---|
| **Governance / Owner's Cards** | Per-skill `owner-card.md` with 14-field human-accountability spine (owner, backup, allowed/proposed-only/forbidden actions, pause + retirement "death conditions", review dates, success standard) + track-2 trio (`evidence_required`, `sources_must_not_use`, `review_sample`) for external-side-effect/high-risk skills. Three worked exemplars. | Validator-errors on owner drift vs ontology, malformed values, and missing spine fields once `provisioned: yes`; validator-warns below provisioning and on freshness. Card *content truth* is convention-only. | `skills/work-package-spec.md`, `skills/renewal-prep/owner-card.md`, `docs/rule-map.md` (check_owner_cards row) |
| **Describability Gate** | 8 required `gate_*` frontmatter fields (inputs, output, standard, source of truth, exception path, error cost, owner, review gate) on any deep record whose Motion is automate/build; "none" answers pass, "N/A"/"TBD" do not; no waiver mechanism. | Validator-errors on the automation path (machinery-follows doctrine: strict only when a field backs a running agent; warns on acted-on-but-incomplete; silent on untouched work). | `CONTEXT.md` (§Ontology), `ontologies/customer-success/renewal-prep.md` (worked example), `validate.py:check_deep_record` |
| **Blast-radius change routing** | Three-bucket routing: `track1-body` auto-applies with changelog line; `escalating` (rules, track-2 skills, descriptions, governance frontmatter, cards) needs sign-off; incomplete demotes to memory note. `--diff` tripwire: escalating change with no pending proposal, or declared-vs-actual radius mismatch → ERROR. Only fires on `groundwork.pin`-carrying roots (demo + generated repos), not the engine's own exemplars. | Validator-errors under `--diff` only (tripwire); the actual gate is the human commit bit — a permissions convention, stated as such. Missing changelog line and governed deletions are WARNs by design. | `proposals/README.md`, `validate.py:blast_radius_diff_findings`, `docs/known-limitations.md:47-74` |
| **Constitution "compiler"** | A five-question worksheet protocol (prose) + typed rule files: 4 owned objects (value/rule/runtime-check/appeal, each with owner), 5-rung ladder, no-rung-six invariant (high-risk never terminates in automation), mandatory sunset, orphan-prohibition on repeals. One compiled rule exists in the engine (`access-grants-need-human-signoff.md`); three in demo. "Compiler" is a metaphor — no code compiles anything. | Validator-errors on safety spine (high-risk rule w/o appeal, missing owned objects, unreassigned surviving job); warns on drafts/sunset. Rule *execution* is convention-only except one Claude-Code hook. | `governance/README.md`, `governance/constitution/access-grants-need-human-signoff.md`, `validate.py:check_constitution` |
| **Action-class hook (runnable floor)** | `action_class_gate.py` (159 lines, stdlib): PreToolUse hook denying curated high-risk command shapes (rm -rf, force push, destructive SQL, terraform apply, payments, outbound writes). Deliberately over-blocks quoted text; fails toward deny. Claude-Code-only; other harnesses get `review-gate.md` as instruction. **Not installed in groundwork's own repo.** | Runtime-enforced *if* a company installs the settings snippet in Claude Code; instruction-strength on Codex/Cursor/Gemini. Validator-errors only on a registered-but-unfireable guard (`check_hooks`, root-only). | `governance/hooks/action_class_gate.py`, `governance/hooks/settings.snippet.json`, `docs/known-limitations.md:24-45` |
| **Org memory** | One record per file, 6-field schema (provenance observed/inferred/confirmed/superseded, owner, valid_at, review_by, superseded_by, source); never-edit-always-supersede; live-only index; bi-temporal (Zep pattern). 3 baselines in engine, richer set in demo. No retrieval/recall engine — explicitly the harness's job. | Validator-errors on spine, broken supersession chains, confirmed-without-source; under `--diff`, errors on any edit/deletion of frozen body, provenance downgrade, non-append source. Warns on staleness/unindexed. | `memory/README.md`, `memory/_index.md`, `validate.py:check_memory`, `check_memory_diff` |
| **Ontologies** | 8 function directories, each `_executive-view.md` (activity + Direction up/down in exactly one canonical table grammar — anything else ERRORs) + deep records for acted-on activities (Motion verdict, 5 scores, work type, owner). 4 worked deep records incl. one deliberate non-automation (`engineering/technical-hiring-loops.md`, Motion: hire). Engine copies are declared "exemplars/templates". | Validator-errors on table grammar and deep-record path fields; warns on unlisted deep record. Direction/Motion *judgments* are convention-only. | `ontologies/README.md`, `ontologies/customer-success/renewal-prep.md`, `validate.py:parse_exec_table`, `check_ontology` |
| **Skills format + portability** | "Work package" convention: `skills/<name>/SKILL.md` (frontmatter: name, description, action_class, provisioned, ontology, baseline) + `owner-card.md` + harness requirements + compatibility notes + memory row. Portability = documented symlink layer (`.claude/skills/` + `.agents/skills/`), head-to-head tested 2026-07-18 in one shape (printed shape is one hop away from the tested one, stated). | Validator-errors on frontmatter/referential/drift; portability is convention + manual steps (`check_company_root` merely WARNs when a pinned repo's skills are harness-invisible). | `skills/work-package-spec.md`, `skills/renewal-prep/SKILL.md`, `delivery/README.md:22-67`, `docs/known-limitations.md:314-345` |
| **Interview flow** | Four documents, no program: consultant protocol (`protocol.md`), 9-section question skeleton with every question naming its destination field (`questions.md`), resumable state format (manifest + frozen numbered layers + `_working.md`; "confirmed" is git structure, not a label), generation protocol (`generate.md`). Halt-instead-of-guess on the 5 human-only fields. | State *shape* validator-errored (`check_interview_state`: half-committed turns, working-file-claims-confirmed, manifest/directory drift; `--diff` freezes committed layers). Interview *conduct* and answer truth are instruction-strength — "Nothing checks interview prose." | `interview/README.md`, `interview/questions.md`, `interview/protocol.md`, `docs/known-limitations.md:236-253` |
| **OS generation into private repo** | `generate.md` protocol: agent transcribes confirmed layers into a separate private company repo (two-repo model; engine is pull-only, content never re-copied); generator refuses to invent owner, backup owner, forbidden actions, 2 death conditions; carve-out of adopter content from Apache-2.0 written into generated root file. Executed twice ever: one scoped dry run + one full simulated-company run (2026-07-31/08-01, blind-graded, 1 of 9 planted facts fully surfaced — lowest diagnostic band, diagnosed as protocol stopping-condition flaw). One known unresolved instruction composition. | Instruction-strength end to end; the only mechanical guarantee is that the *output shape* passes the validator (a test materializes a company repo and validates it: `TestGeneratedCompanyRepo`). Faithfulness to answers is unverifiable — stated. | `interview/generate.md`, `README.md:90-113`, `docs/known-limitations.md:255-312`, `tests/test_validate.py:6324` |
| **Validator** | Single stdlib-only script, 3,694 lines, ~28 named checks (all enumerated with severities in `docs/rule-map.md`). Stateless pass: secrets floor + entropy, links, context budget (Codex 32KiB chain, always-loaded aggregate), root-pointer drift, ontology/cards/memory/constitution/proposals/changelog/interview shape, synthetic-identifier allowlist (demo-scoped, checked against `demo/canon.md`), version pin. `--diff <base>` adds memory/interview immutability + blast-radius tripwire. Instance model: any dir carrying `ontologies|skills|governance|proposals|memory` validates as its own root. Exit 0 = no ERRORs; currently 0 errors / 7 entropy WARNs on the repo itself. | This *is* the enforcement layer; its own limits are cataloged (skips `tests/` and dot-dirs, inline links only, high-signal secrets, TOCTOU on `--diff`, cannot read prose for truth). | `scripts/validate.py`, `docs/rule-map.md`, `docs/known-limitations.md:5-22` |
| **Migrations / versioning** | Single integer `SCHEMA_VERSION = 1`, bumped only on breaking changes; `groundwork.pin` in company repos (schema_version + provenance sha); pull promise (same-version pull always safe; skew ≥1 → single migration-gate ERROR pointing at MIGRATIONS.md; max skew 1; reverse skew WARNs). Per-check `since:` demotion is **documented intent, not code** (explicitly unwired at v1). One on-record exception: exec-table grammar tightened without a bump before any pin existed; window declared closed 2026-07-29. | Validator-errors on malformed pin / skew ≥1 (`check_version_pin`); migration notes themselves are convention (none exist yet — no migrations). | `MIGRATIONS.md`, `demo/groundwork.pin`, `validate.py:30`, `check_version_pin` |
| **Tests** | 709 tests in one 6,814-line file across 57 classes; **all pass** (`Ran 709 tests … OK (skipped=1)`, ~9s, stdlib unittest — pytest not required). Cover: every check incl. nested instances, symlink attacks, diff CLI wiring, exec-table hardening, code-fence stripping edge cases, the hook's classify(), zero-dep import guard (`TestZeroDep`), demo liftability pin (`TestDemoIsLiftable`), question-skeleton field coverage, a materialized-and-validated company repo, and `TestRuleMap` binding rule-map ↔ code bidirectionally. | Test-enforced (CI-grade); severity *correctness* verified by hand once, per known-limitations. | `tests/test_validate.py`, `docs/rule-map.md:8-14` |
| **Demo** | `demo/` = complete fictional 20-person company (Umbercress): canon allowlist, 8 exec views, 7 deep records, 4 work packages, 3 constitution rules, memory with a supersession chain, one pending proposal, one runnable rung-3 reminder, own `groundwork.pin` (so it is itself a governed root), 15-minute 3-query walkthrough ending in a governance refusal. | Synthetic-identifier check validator-errors (demo-scoped); the walkthrough refusal is explicitly instruction-strength, "not a runtime block", and the demo says so in-line. | `demo/README.md`, `demo/canon.md`, `demo/walkthrough.md`, `demo/proposals/refusal-names-next-step.md` |

## 3. EXPLICIT NON-CLAIMS (the repo's own words)

- **No real-company run, ever**: "no interview has ever been run on a real company, and no company OS has ever been generated from real answers" (`README.md:167-174`, `docs/known-limitations.md:276-299`, `docs/roadmap.md:16`). Simulated-company personas are "cooperative by construction" and don't prove human-gap extraction.
- **No check reads prose for truth** — validator confirms fields are answered, not that answers are true (`README.md:39-42,138-141`).
- **Demo refusal is instruction-strength, not a runtime block** (`README.md:82-88`).
- **The validator is a tripwire, not the teeth** — cannot prove a human reviewed anything; commit bit is the real enforcement, a "permissions convention, not a cryptographic proof" (`docs/known-limitations.md:49-56`, `CONTEXT.md` "Commit-bit teeth").
- **Secrets floor and hook pattern set are high-signal, not exhaustive**; Gitleaks is the documented real guarantee; the hook is a floor, not a sandbox (`docs/known-limitations.md:7-9,26-31`).
- **Hooks are Claude-Code-only**; other harnesses get an instruction, and "an instruction is not enforcement"; the gate is not installed in groundwork's own repo (`docs/known-limitations.md:39-45`).
- **Nothing checks that a generation was faithful**; a wrong-owner transcription passes cleanly (`docs/known-limitations.md:257-264`).
- **A company repo is not standalone-validatable** (needs the engine clone) (`docs/known-limitations.md:272-275`).
- **Provisioning is manual; nothing zips, uploads, or syncs**; a generated repo's skills are invisible until symlinks are made (WARN only); packaging the repo root leaks the interview transcript and "no check can enforce" against it (`delivery/README.md`, `docs/known-limitations.md:314-338`).
- **`since:` demotion is documented intent, not code** (`MIGRATIONS.md:40-47`).
- **Never list** (commitments, not deferrals): no hosted anything, no agent runtime, no memory/retrieval engine, no third-party dependencies (`docs/roadmap.md:91-99`).
- Plus enumerated validator limits: link check inline-only, minimal `.gitignore` semantics, token counts are bytes/4 estimates, `--diff` TOCTOU, dot-directories unscanned, one schema gap (no "what must not degrade" field — named first v2 candidate) (`docs/known-limitations.md` throughout).

## 4. MATURITY SIGNALS

**Real:**
- Validator + test suite is the hardest part: 3,694-line validator, 709 passing tests (verified this audit: `OK (skipped=1)` in 9s), 0 errors on `validate.py .`. Test depth is unusual — symlink escape, TOCTOU-adjacent diff wiring, Markdown-tokenizer edge cases in code-fence stripping, and a `TestRuleMap` that makes documentation drift a test failure in both directions.
- Zero TODO/FIXME markers in `validate.py` (all "placeholder" hits are about *rejecting* placeholder field values, not stubs).
- Worked content is fully specified, not lorem: deep records carry all 8 gate fields with substantive prose (`ontologies/customer-success/renewal-prep.md`); Owner's Cards carry the full 17-field spine+trio (`skills/renewal-prep/owner-card.md`); demo memory includes a real supersession chain (`demo/memory/daily-standups.md` → `async-standups.md`).
- The demo is self-governing: carries its own `groundwork.pin`, so its rules/skills run the same consent gate a company repo would.
- Honesty machinery is itself mechanized: `TestDemoIsLiftable` pins the exact 4 engine-pointing links; the rule-map records its own hand-audit corrections (3 rows moved to match code, code never moved).

**Scaffolded / thin:**
- The "constitution compiler" is one worksheet doc + 1 engine rule (3 in demo) — a schema with exemplars, not machinery.
- Runtime enforcement is one 159-line regex hook, one harness, uninstalled locally; everything cross-harness is prose.
- The interview→generation path has been exercised twice total, never on humans; one known instruction-composition conflict is unresolved and parked on the roadmap.
- `since:` version demotion, changelog rotation, and per-rule runnable automation are documented-not-built (V1.5/V2 items, labeled as such).
- 4 of 8 ontology functions have only an executive view; `proposals/` is empty by design.

Overall pattern: the enforcement/verification layer (validator + tests) is production-grade and slightly over-built relative to the content; the generative/behavioral layer is protocol documents whose only mechanical guarantee is that their output shape passes the gate. The repo is unusually rigorous about saying exactly this about itself.

## What this means for the ratification session (step 4)

**Recommended posture: adopt groundwork as the company's governance layer
as-is, and do NOT "improve groundwork to satisfy our needs" for most of the
gaps.** The [L1] ask assumed groundwork would grow toward the fleet's needs;
the audit says the opposite division of labor is correct. Groundwork's "Never"
list (no agent runtime, no memory engine, no hosted anything) is not a
deficiency — it is the same doctrine the literature review's convergent
findings reached independently ("files not an engine" ≈ durable inspectable
state; commit-bit teeth ≈ agents-never-self-approve; hard steers over soft).
Growing an engine inside groundwork would break the thing that makes it
trustworthy.

The build therefore splits three ways:

1. **Extend groundwork with CONTENT (fits its philosophy, small schema
   extensions at most):** a fleet-role ontology (orchestrator/validator/judge
   relationships — who calls whom, who may overrule whom; the one L1 need with
   no representable form today), a judge charter (what the judge may rule on,
   owner, appeal path), a model-assignment field per skill/card, a cost-cap
   policy file (per-agent $/run, monthly ceiling, breach = pause_condition),
   and a trace policy file (what must be traced, retention, owner). Each of
   these is a files-layer artifact the runtime reads as config.
2. **Build the runtime layer separately (the nervous system):** state-machine
   pipeline, queue, retries/escalation, model router, Arize wiring, budget
   metering, review inbox. Sean already owns most of the primitives in
   agents-sdk (hybrid_router, cap_policy.json, launchd scheduling, manifest
   conventions, circuit breakers) — the gap is smaller than the MISSING column
   suggests. The runtime treats groundwork artifacts as declarative config and
   is where pause conditions become actual kill switches.
3. **Build both eval layers (step 5's job, nothing exists):** fleet-evals and
   product-evals. Eval-set conventions (cases as files, owners, provenance)
   can live in the groundwork-governed company repo; runners and regression
   tracking are runtime. The 32-case spike corpus seeds the product side.

**Three cautions the ratification must carry:**

- **Enforcement parity is the one real philosophy conflict.** Hooks are
  Claude-Code-only; on Codex/Cursor/Gemini every forbidden action binds only
  as instruction. A mixed-model fleet [L1] therefore gets mixed-strength
  governance unless the runtime layer enforces uniformly (e.g., all
  side-effectful actions route through runtime-mediated tools, never raw
  harness access for non-Claude agents). This should be an explicit
  ratification decision, not an accident.
- **The company would be groundwork's first real adopter.** The interview →
  generation path has run twice ever, only on simulated companies, with a
  known low diagnostic result on planted-fact extraction. Dogfooding it is a
  strong build-in-public story and genuinely useful to groundwork — but treat
  the interview as untested instrumentation, not proven process.
- **Review-queue mechanics are the founder-time bottleneck.** Groundwork
  surfaces pending work as files and PRs; at 25 hrs/week [L7] the consolidated
  review inbox (the literature's "Needs Review as designed success state")
  must be built early or the human gate silently becomes the fleet's
  choke point.

Mapping to the literature review's TOP-TEN agenda: this audit resolves the
groundwork half of #2 (pipeline boundary: groundwork = declarative config,
runtime = execution), #7 (permission matrix: extend Owner's Cards/action-class
tiers + the enforcement-parity decision above), and #8 (orchestration
topology: fleet-role ontology as new groundwork content + runtime state
machines). Items #3/#6/#9 pass to the Arize eval-stack design (step 5).

## Provenance

- Kickoff: [docs/prompts/2026-08-08-agent-company-research-campaign-kickoff.md](../../../docs/prompts/2026-08-08-agent-company-research-campaign-kickoff.md)
- Prior steps: [feasibility spike (GO)](2026-08-08-vision-drift-feasibility-spike-go-no-go.md) · [literature review](2026-08-08-software-factory-literature-review.md)
- Audited repo: `/Users/seanwinslow/Code-Brain/groundwork/` (github.com/seanwinslow28/groundwork), read-only pass, two independent audit agents + orchestrator reads
