# Shared law — what every -craft team inherits

The law below holds for every -craft team (Systemcraft, Productcraft, and every team built after them). It lives here once. A team's `CLAUDE.md` and master skill link to a section and may **add** to it (a stricter rule, a studio binding), never restate or contradict it. Moved here on the Productcraft build map's [craftwork build 1](https://github.com/seanwinslow28/code-brain/issues/324) ticket (2026-10-01), per the [Method extraction: craftwork](https://github.com/seanwinslow28/code-brain/issues/282) ruling. Each section names where its text came from and when it was ratified.

**Adoption.** Productcraft runs on all of it. Systemcraft adopts it in full at [craftwork build 4](https://github.com/seanwinslow28/code-brain/issues/327), before eng-005's first seat runs. Until that ticket closes, the one place Systemcraft's own master skill still differs is its § Model deviations (Fable at the top of its ladder, five draft-time triggers), and there Systemcraft's skill governs Systemcraft's passes. Every other section already holds for both studios, because its text came from Systemcraft.

Shared machinery sits beside this file in [templates/](templates/): the red-team protocol, the close digest, the status vocabulary, the ledger-entry schema and the runtime registry. See [README.md](README.md).

---

## Name the canon

*(Productcraft L11, 2026-09-09; shared on #282 decision 7, 2026-10-01.)*

Every material choice ships with a one-breath why-A-over-B **and names what it leaned on from the canon**: a title and the idea, in the seat's own words. Never the book's text, and never a paraphrase of a source's substance. Every ledger entry carries a `## From the canon` section ([ledger-entry.md](templates/ledger-entry.md)): one title normally and two at most, never omitted. When nothing applies the entry says so, and on `manifest-only` grounding the line is marked "(manifest only, not read this pass)".

Why: the canon line is the studio's teaching surface, and it is what keeps a published entry safe. It names an idea and never carries a book's text.

## The audit shape, and the three-seat floor

*(Systemcraft bench ratification 2026-08-22, Productcraft rule 6; shared on #282 decision 8.)*

- **Closed cycles.** Every seat audits exactly one artifact and is audited by exactly one peer. Each team draws its own cycle layout (Systemcraft runs one five-seat cycle, Productcraft runs two).
- **Fresh context.** An audit is a fresh-context invocation that never sees the drafting conversation, and it never runs below the auditor seat's baseline.
- **The red-team gate is a protocol, not a seat** ([red-team-protocol.md](templates/red-team-protocol.md)).
- **The floor is three seats.** Below three seats a closed cycle cannot carry the audit shape. **Do not build a studio** below the floor. Use a skill, or a skill plus the red-team gate.

## Standing success measure

*(Systemcraft eng-003.d40/d11/d42/d43, ratified 2026-08-29; moved from Systemcraft's master skill. The handoff sentence is Productcraft #268.)*

An engagement succeeds only on **outside use**, judged at **Close + 14 days**:

1. At least one dated use event beyond the ledger names it: shipped, scheduled-with-owner-and-date, stopped/declined, or dependent work actually begun. Ratification alone never counts.
2. 100% of the Close-frozen **P0-equivalent** findings carry a dated Sean disposition (`shipped` / `scheduled-with-date` / `explicitly-deferred-with-reason`), delivered one rule-8 ticket per finding at Close.
3. The engagement stayed inside its Open-ratified attention budget.

**Close is administrative.** A clean Close records `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`, never success. An unresolved coordinator breach or a deferred required output cannot Close as delivery-complete (`OPEN — DEFERRED`). A month with no due date is NO OBSERVATION, never PASS.

*P0-equivalent* (must-handle before dependent work proceeds) = the finding would expose a person/private data/money/hard-to-reverse asset to material harm, make the success claim or its load-bearing evidence materially false, or let a gate/launch/consequential decision cross a known blocking contradiction. The rule is pre-registered at Open, candidates are nominated during Run, and the denominator freezes at Close under Sean's ratification. It can be superseded later, never erased.

**A handoff crossing is not outside use** for the sender, because it stays inside the org. Work the receiving side's return makes possible can be.

## Availability ladder

*(Systemcraft eng-003.d30, ratified as words; moved from Systemcraft's master skill. The registry clause is Productcraft #286.)*

When a planned provider is unavailable, there are two legal moves. The first is a **dated Sean-approved vendor substitution that preserves seat identity**: same seat contract, lane, target, and audit duty, run as a fresh invocation, never on inherited context. Otherwise, a **dated deferral** that stops the dependent branch. Never legal: crossing lanes in one run, drafting seat substance in coordinator context, silent provider/tier switches, merging deferred lanes. Live deferrals become rule-8 tickets at Close.

The substitute is a row of [the runtime registry](templates/runtime-registry.md), named with its standing in the Route entry. An **unmeasured** row serves only on Sean's dated word for a named pass. The coordinator may *propose* a row only once it is **substitution-eligible**.

## Self-targeted modifier

*(Systemcraft eng-003.d41, ratified 2026-08-29; moved from Systemcraft's master skill.)*

When the studio, its coordinator, or its law is the target, Open must additionally:

1. pre-register the questions and the classes of finding the studio cannot produce;
2. record an exact context manifest for every pass;
3. bind live claims to the standing provenance contract;
4. use a fresh independent gate with a different model lineage when available, naming any fallback;
5. reserve judgment and ratification to Sean while using at least one outcome signal the studio cannot self-issue.

No self-targeted engagement may implement or ratify its own expansion; it may only draft it for Sean.

## Model delegation

*(Productcraft #267, ratified 2026-09-09; #296 clauses 3–5, 2026-09-21; re-ruled to the 5.5 generation on #321, 2026-09-29; shared on #282 decision 2.)*

**A seat's `model:` line names the runtime that actually runs**, as a row of [the runtime registry](templates/runtime-registry.md). A baseline comes only from a row whose standing is **ruled** or **baseline-eligible**. The Route entry states each seat's runtime from its own seat file and never inherits the session model silently. **A normal pass is the baseline**; only a real change is a deviation, and every deviation carries a one-line why against a named trigger. Deviations are per pass, never per engagement. No silent deviations, ever.

**Escalate one tier**: Sonnet 5.5 → Opus 5.5 → Codex GPT-5.6 Sol High → Codex Sol xhigh → stop and ask Sean. It fires only on:

1. **Gate FAIL.** The owning seat redrafts one tier up.
2. **Audit bounced substance, at severity.** A MATERIAL finding that loops back is redrafted one tier up **only** when it meets the engagement's P0-equivalent bar, or when it is the second material round on the same artifact. Count is not severity.
3. **Thin lane, decided at Route.** The thin-lane check at Open decides it. A seat that only discovers thinness mid-pass finishes at baseline and flags it in the artifact header. No mid-pass switching.
4. **Owner-directed.** Sean names a pass at Open or at a gate checkpoint. A hard-to-reverse commitment is a reason for the coordinator to *propose* this, never to fire it alone.

"Feeds a gate", "novel shape" and "hard-to-reverse" are not triggers. They were true of every draft and caused the 2026-08-26 Fable cap event. A **self-raised** finding (a defect a seat raised while drafting) is ruled on its grounds and may never be the sole trigger for a tier.

**One tier up is what the registry row says.** The ladder is defined on ruled rows only: Claude's model steps and Codex's `high` → `xhigh`. A trial runtime has no tier. A failed trial is a labeled fail beside the train, and a runtime reaches a tier only by a new ruling, never by a trial.

**Downshift** (Opus → Sonnet; Sonnet → Haiku 4.5, mechanical work only) on a mechanical transform of existing substance, a single-source corpus lookup, objective checklist application, or clerical filing (the file-or-defer *decision* stays at baseline). Audits never run below the auditor seat's baseline.

**A gate runs on the vendor that did not last write its anchor artifact.** That is Codex GPT-5.6 Sol High by default, or a fresh-context Opus 5.5 subagent when the anchor was last written on Codex. **A verification pass follows the same rule**: it runs on the vendor that did not write the repair. The checker changes vendor, not the repairer.

**Pinned, always.** Codex passes always pass `--model gpt-5.6-sol`, never the plugin's or the config's unset default. Codex `ultra` effort is forbidden: it auto-delegates and breaks one invocation, one seat. Fable runs the interactive coordinator's session only, and a seat pass only on Sean's word for a named pass.

## The alias probe at Route

*(Productcraft #321, ruled 2026-09-29.)*

**An alias is not a pin.** Before the first Claude pass, the coordinator probes what each Agent-tool alias it will launch (`opus`, `sonnet`, `haiku`) resolves to. The probe is a one-line subagent asked for its own model id, run outside the budget, and the answers go into the Route entry. An alias that no longer resolves to a seat file's `model:` is an availability-ladder event for Sean before any seat runs, never a silent switch. A pass record's `runtime:` is copied from the transcript's model stamp, never from the alias. The trace kit's rung-0 line 11 fails a record whose runtime disagrees with its transcript.

Why: the first Productcraft train's aliases moved to the 5.5 generation after it closed, and nothing noticed.

## Checks converge, and the ladder has brakes

*(Productcraft rule 9, ratified 2026-09-21 on [#296](https://github.com/seanwinslow28/code-brain/issues/296) from pc-eng-001's d51; shared on #282 decision 2.)*

The adversarial posture is unchanged. It was tested and found innocent: on pc-eng-001, 20 of 20 seat-audit materials were repaired-and-verified or owner-accepted, none withdrawn. The brakes are on the ladder.

1. **The repair cap is standing law.** One repair round per artifact per check. A residual that survives that round routes to the next scheduled gate as a candidate acceptance, or to Sean. It never gets a second loopback.
2. **Round two is a verification pass, not a fresh audit.** The check that raised the findings re-runs in `verify` stance with exactly three duties: rule each repair `holds` or `residual`, attack the text the repair changed, and stop. A defect found outside the changed text is a **gate residual, never a loopback**.
3. **Escalation fires on severity, never on count** (Model delegation, trigger 2).
4. **The checker changes vendor**, not the repairer (Model delegation, the gate rule).
5. **Self-raised findings are routed, not banned.** A seat may rule material on a defect it raised itself. It declares the conflict and gives grounds that do not depend on who raised it, and the finding never buys a tier on its own.
6. **The stopping rule.** A check series on one artifact ends when the verification pass returns holds-with-no-new-material, **or** when the cap is spent, whichever comes first. The coordinator reports every open series at each gate as *round / findings / repair size*, so shrinkage is visible. A series that does not shrink is a variance question to Sean, never another round.
7. **Residuals are re-read before Close.** Every residual carried to a gate as a candidate acceptance is re-read against the artifact as it now stands. One that a later round already repaired closes as stale. A finding raised by more than one check routes to one owner **once**. Duplicates route; they never recount.
8. **Process waste is a finding against the studio**, coded from the trace kit's process-waste family ([trace/taxonomy.md](trace/taxonomy.md)), never a bare `manufactured` code.

Why: on pc-eng-001's one re-audit, all four new findings were residuals of that revision's own repairs, although it re-attacked the whole document. The unbounded thing was repair-induced surface, not unexamined text.
