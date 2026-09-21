---
name: productcraft
description: Run the Productcraft studio — the seven-seat product leadership bench at productcraft/. Use on explicit summons ("productcraft", "engage the product studio", "/productcraft") or unambiguous studio-shaped work — a product's strategy, discovery, metrics and evidence, growth, business case, roadmap, or org design, anything wanting the seven-artifact train or a named seat's lane. Productcraft is upstream by default — on a request that spans product and AI-system questions, open here and let the AI layer reach Systemcraft through the handoff; open Systemcraft directly only when the product decision is already made or given as a constraint. On an ambiguous match, ask one clarifying line before launching anything. NOT for generic PM artifacts (pm-* plugin skills own those), AI-layer design when the product is already decided (systemcraft), job-hunt writing (the voice skills), or quick factual questions — answer those directly.
---

# Productcraft — master skill

The studio's coordinator. **The skill knows the process, the seats know the craft, CLAUDE.md knows the law**: craft lives in [productcraft/bench/](../../../productcraft/bench/README.md) (contracts, stakes, co-sign duties, baselines, toolbelts), law in [productcraft/CLAUDE.md](../../../productcraft/CLAUDE.md) (public/private split, explain-why and the canon line, Insights never decides, full artifacts forward, the two audit cycles, one invocation one seat, Systemcraft owns the AI layer). This file owns only what happens when, and never restates the other two. Excluded from export groups — useless without this repo's corpus and bench. Design ratified on the build map's [Master skill design](https://github.com/seanwinslow28/code-brain/issues/273) ticket (2026-09-13).

**Upstream by default.** Systemcraft owns the AI system, platform and technical architecture *inside* a product; Productcraft owns whether it should exist, for whom, how it earns, and how it ships. A request carrying both opens here, and the AI layer crosses at stage 6 under [the handoff contract](../../../productcraft/templates/handoff-contract.md). Systemcraft opens directly only when the product decision is already made.

## Engagement types and routing

*(#266, ratified 2026-09-09.)* Type by the question being answered and the output owed.

| Type | Selection test | Roster |
|---|---|---|
| **Full train** | A new organizing premise or a full artifact chain, including a replacement for something that exists | All seven seats in pipeline order, no skipping; all three co-sign touches; both audit cycles; three red-team gates |
| **Audit** | Tests an existing product, strategy or org before keep / repair / reframe / replace | Every seat whose lane the target actually has, each auditing its own lane fresh-context; the roster states absent lanes; one audit-close gate |
| **Execution breakdown** | A design has returned from the Systemcraft handoff and needs turning into buildable work | Delivery seat only, receiving the complete design plus Systemcraft's frozen return; epics → stories (design set + implementation set) → first sprint plan, filed as issues in the target's tracker; one ledger entry; no audit cycle; no gate — it creates the implementation candidate Systemcraft's Gate 3 waits for |
| **One-off** | One reversible framing or judgment question, no governed state changed | Owning seat only; adjacent lanes named, never drafted; if the answer creates dependent decisions or a hard-to-reverse commitment, stop and retype. Mid-build stories, release notes and retros are Delivery one-offs. A one-off that surfaces a Systemcraft question stops and retypes; it never hands off |
| **Support landing a role** | The output is a derivative used in a real job pursuit | Owning seat(s) only; real ledger entries, never hypotheticals; no gate |

"Serve employer work" is deliberately absent until Sean has an employer — one row to add then.

## Inherited law (one line each; Systemcraft's text is the authority until `craftwork` extracts it)

- **Standing success measure** — outside use at Close + 14 days, P0-equivalent findings each carrying a dated disposition, Close always `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`, never success: [systemcraft SKILL.md § Standing success measure](../systemcraft/SKILL.md). A handoff crossing is not outside use for the sender; the execution breakdown filing issues in the target's tracker is dependent work begun.
- **Availability ladder** — an unavailable planned runtime gets a dated Sean-approved substitution preserving seat identity, else a dated deferral of that branch; never a merged lane, never a silent switch: [systemcraft SKILL.md § Availability ladder](../systemcraft/SKILL.md).
- **Self-targeted modifier** — when the studio or its law is the target, Open pre-registers the questions and the finding classes the studio cannot produce, records a context manifest per pass, uses a fresh gate of a different lineage, and reserves ratification to Sean: [systemcraft SKILL.md § Engagement types](../systemcraft/SKILL.md).
- **Red-team protocol** — posture, attack checklists per artifact (each Productcraft template carries its own), typed verdicts, `IMPLEMENTATION HOLD`, and the never-silently-skips fallback: [systemcraft/templates/red-team-protocol.md](../../../systemcraft/templates/red-team-protocol.md). Productcraft's gate schedule and vendor rule are below.

## The five phases

**1 — Open.** First, look in the ledger's `handoff/inbound/` for a return with no crossing state in `crossing.md`; if one is waiting, propose the execution breakdown before anything else. Then type the engagement (table above) and write a one-paragraph brief to `brief.md`, opening with the header the trace kit reads (`id`, `name`, `type`, `opened`, `pass_budget` — [productcraft/trace/README.md](../../../productcraft/trace/README.md)). Pull relevant past entries via `productcraft/ledger/index.md` (two hops: index line → entry). Assign the id (`pc-eng-NNN-slug`). Run the **thin-lane check**: each rostered seat's lane manifest against the engagement's topics; a lane with no pointer for its topic drafts one tier up, declared in the pass budget before anything runs. Declare the **pass budget** (below). Pre-register the P0-equivalent rule. The coordinator writes the **Open entry** (type, brief, budget, thin-lane result, P0 rule).

**2 — Route.** State the roster and each seat's runtime **from its own seat file's `model:` line** — never inherit the session model silently. State every deviation now or as it arises, each with a one-line why against a named trigger (below). The coordinator writes the **Route entry** (roster, runtimes, declared deviations).

**3 — Run.** Seats draft in pipeline order and hand **full artifacts forward, never summaries**. Every invocation is fresh-context and carries exactly one seat: the seat file, its lane manifest, [the seat preamble](../../../productcraft/templates/seat-preamble.md) verbatim, the declared target, and the upstream artifacts — never this conversation. Before firing a seat the coordinator writes the pass record's launch fields; after it returns, the completion fields ([record-template.md](../../../productcraft/trace/record-template.md) — one file per invocation at `trace/pass-NN-<seat>-<kind>.md` in the engagement folder, hashes of every input and output, `## Corpus read` from the transcript; #290). Material defects **loop back** to the drafting seat, never a rewrite in place. **Ledger writes happen here**: the deciding seat writes its entry at the moment of a material decision ([ledger-entry template](../../../productcraft/templates/ledger-entry.md)).

The full train, stage by stage — what drafts, which co-sign it waits on, which **trailing audit** fires the moment the artifact is final, and what else fires:

| Stage | Drafts | Co-sign before it is done | Trailing audit fires | Gate / crossing |
|---|---|---|---|---|
| 1 | Product Strategist — Strategy & POV doc | — | *(Discovery's audit of it waits for stage 2 — there is no evidence yet)* | — |
| 2 | Discovery Lead — Discovery packet | Insights, touch one: grades every evidence claim against raw-evidence pointers, passes or bounces | Discovery Lead → Strategy & POV doc; Leadership → Discovery packet | — |
| 3 | Insights & Analytics — Metrics & evidence plan (touch two; any Strategist outcome it cannot give a metric bounces to the Strategist) | — | Delivery → Metrics & evidence plan | **Gate 1 — strategy sign-off** (anchor: Strategy & POV doc). Fires once stage 3 is final and Discovery's audit of the Strategy doc has landed with no open material defect; nothing at stage 4 starts before it passes |
| 4 | Growth & Distribution Architect — Growth model & GTM plan | — | Insights → Growth model & GTM plan | — |
| 5 | Business & Economics Modeler — Business case | — | Growth → Business case | — |
| 6 | Delivery & Execution Lead — Outcome roadmap | Strategist co-signs the OKR translation, key result by key result | Business → Outcome roadmap | Delivery writes the **handoff verdict** (a brief, or a recorded no-handoff). If a brief: **Gate 2 — pre-handoff** (anchor: the brief), then the crossing per the contract |
| 7 | Product Leadership & Org Designer — Leadership packet (Systemcraft on the stakeholder map with the return date as its ask, or stated absent) | — | Strategist → Leadership packet | **Close gate** on the whole train, after every trailing audit has landed and every loopback closed |

**Trailing audits and the stale cascade** (#273, ratified 2026-09-13). An audit fires as soon as its artifact is final (after any co-sign) and runs in parallel with the next seat's draft, fresh-context, on the auditor's own baseline. A loopback that changes an artifact **stales every artifact below it**: the coordinator reports the cascade size before firing it, then the stale artifacts are redrafted in pipeline order, each redraft counted from the pass budget, and their own trailing audits re-fire. Audits in Cycle A (Strategist → Leadership → Discovery → Strategist) and Cycle B (Insights → Growth → Business → Delivery → Insights) never run below the auditor's baseline.

**Dispatch forms** (#267). Claude seats: an Agent-tool subagent with the seat's `model:` set explicitly, fresh context, the five inputs above; the meter is the usage field. Codex passes: `codex exec --model gpt-5.6-sol -c model_reasoning_effort="high" --sandbox workspace-write --skip-git-repo-check -C <repo>` with stdin from `/dev/null`; the footer token count is the meter. Never through the plugin's unset default model; `ultra` effort is forbidden.

**4 — Gate.** Per the inherited protocol, with Productcraft's schedule: a full train gates three times — strategy sign-off after stage 3, pre-handoff on the brief at stage 6 (only when a brief exists), and at close on the whole train; an audit gates once at close; the execution breakdown, one-offs and role support never gate. **Anchor-vendor rule:** a gate runs on the vendor that did not last write its anchor artifact — Codex GPT-5.6 Sol High by default, a fresh-context Opus 5 subagent when the anchor was last written on Codex; the close gate uses a majority rule across the train, ties to Codex; Fable only on Sean's say-so. FAIL → the owning seat redrafts one tier up and re-gates. A gate never silently skips: an unavailable vendor runs the gate on the other, labeled `fallback: same-vendor`, with a re-run ticket. Every gate writes its ledger entry naming its vendor and why. **A passed gate also earns its readouts** — Gate 1 takes one per final artifact of stages 1–3 plus the gate itself, written to `readout/` per [readout.md](../../../productcraft/templates/readout.md); the rest wait for Close. A close-gate defect in an artifact that already crossed frozen is repaired as a **new crossing**, never a silent edit.

**5 — Close.** Checklist, in order:
- [ ] Ledger entries complete, the coordinator's **Close entry** among them; one line per entry appended to `ledger/index.md`.
- [ ] Corpus inbox sweep (`productcraft/corpus/inbox.md`): file each entry or consciously defer — never silently skip. Mid-pass thin-lane flags from artifact headers land here.
- [ ] **Trace 1 — check** (#272, built #290): `python3 productcraft/trace/check.py productcraft/ledger/engagements/<eng-id>` — every rung-0 line PASS, or each FAIL fixed in the record it names, never by editing an artifact after its pass.
- [ ] **Trace 2 — render**: `python3 productcraft/trace/render.py productcraft/ledger/engagements/<eng-id>` — writes `trace/eval.html` into the engagement; opened from disk, never hosted.
- [ ] **Trace 3 — labels**: every pass has a row with a verdict in `trace/labels.md` (Sean labels as he reads, on the page, and pastes *Copy label rows*; this sweep catches the rest) — the check's "Every pass has a label row" line clears with no "still wait for a verdict" note. Kit and layout: [productcraft/trace/README.md](../../../productcraft/trace/README.md).
- [ ] **Readouts** (ruled 2026-09-14 at pc-eng-001's Gate 1): one per final, past-gate artifact of stages 4–7 plus the close gate plus one whole-train readout, written to `ledger/engagements/<eng-id>/readout/` per [readout.md](../../../productcraft/templates/readout.md), with the terms they use copied from [readout-glossary.md](../../../productcraft/templates/readout-glossary.md). The readout pass is a real invocation with its own trace record (`kind: readout`, stage 0) and sits **outside the pass budget**; a readout is never handed to a seat, hashed as a pass input, or allowed to trigger a repair.
- [ ] **Handoff engagements:** the crossing state is in `crossing.md` on both sides; the return date is filed as one rule-8 line in `vault/00_inbox/tickets.md` (`return due <date>`); a date that cannot be met is a variance question to Sean before the date, never a silent overrun.
- [ ] Live deferred work → one rule-8 ticket per item in `vault/00_inbox/tickets.md`; everything else stays in the ledger for pull.
- [ ] Verify `git status` shows nothing under `productcraft/{corpus,ledger,books}/` — the private layer never reaches this repo.
- [ ] Commit and push the ledger's own repo: `git -C productcraft/ledger add -A && git -C productcraft/ledger commit -m "<eng-id>: <close gist>" && git -C productcraft/ledger push` — private remote `seanwinslow28/productcraft-ledger`. Sessions are one per ticket, so **every session that touched the ledger pushes before it ends**, not just Close.
- [ ] Freeze the P0-equivalent denominator (Sean ratifies) and name the D+14 outcome-record date; declare `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`, never success.
- [ ] Explain-why digest to Sean — recommendation first, one question, statuses per Systemcraft's [close-digest](../../../systemcraft/templates/close-digest.md) and [status-vocabulary](../../../systemcraft/templates/status-vocabulary.md) (inherited until `craftwork` extracts them).

## The wait between a full train and its execution breakdown

*(#273, ratified 2026-09-13: close and track.)* The full train does not wait for Systemcraft. It closes administratively after stage 7 and the close gate, with the crossing state and return date recorded; the wait lives as the rule-8 line above. When the return lands in `handoff/inbound/`, the next Open finds it (step 1 of Open) and proposes the execution breakdown, whose Delivery seat runs the intake check, writes `informed_by`, and flips overturned entries per the contract. An overturn that demands a new *product* decision is a loopback to the owning seat as a one-off.

## Model deviations (named triggers, per-pass, never per-engagement)

*(#267, ratified 2026-09-09.)* A normal pass **is** the baseline; only a real change is a deviation, and every deviation carries a one-line why.

**Escalate one tier** — Sonnet 5 → Opus 5 → Codex GPT-5.6 Sol High → Codex Sol xhigh → stop and ask Sean — only on:
1. **Gate FAIL** — the owning seat redrafts one tier up.
2. **Audit bounced substance** — a MATERIAL that loops back is redrafted one tier up.
3. **Thin lane, decided at Route** — from the Open-time check; a seat that only discovers thinness mid-pass finishes at baseline and flags it in the artifact header. No mid-pass switching.
4. **Owner-directed** — Sean names a pass at Open or at a gate checkpoint. A hard-to-reverse commitment is a reason for the coordinator to *propose* this, never to fire alone.

"Feeds a gate", "novel shape" and "hard-to-reverse" are not triggers — they were true of every draft and caused the 2026-08-26 Fable cap event.

**Downshift** (Opus → Sonnet; Sonnet → Haiku 4.5, mechanical work only) on: a mechanical transform of existing substance; a single-source corpus lookup; objective checklist application; clerical filing (the file-or-defer *decision* stays at baseline).

**Aggregate pass budget.** Every Open declares an integer budget: the base manifest plus two pre-authorized rounds per scheduled gate (one owning-seat repair + one re-gate); the coordinator's own session counts inside it. Full train: ≈20 base passes (7 drafts, the handoff brief, 2 co-sign passes, 7 audits, 3 gates) + 6 rounds = **cap 26 funded invocations**, the coordinator session the 27th by the counting rule. An escalation needs both its trigger and remaining allowance; exhaustion is a stop — actual-versus-cap plus one variance question to Sean, never a silent overrun. Every invocation records a meter line (runtime-reported tokens and wall-clock, else `UNMEASURED`); a partial total is `known subtotal + N unmeasured passes`, never a precise figure. Cost line, canonical form: `Claude usage: OAuth subscription, $0 marginal cash; Codex billing: subscription-absorbed, marginal cash UNMEASURED; Sean attention: <measured>; elapsed: <measured>`.

## Degradation

On a machine without the private layers, seats already carry the ladder (`grounding: full | manifest-only | none`); the skill's own duty is to say so once at Open and proceed — never fabricate ledger precedent or corpus grounding that can't be read.
