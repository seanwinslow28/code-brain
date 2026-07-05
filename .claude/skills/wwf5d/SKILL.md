---
name: wwf5d
description: What Would Fable-5 Do — portable recipes distilled from Fable 5's OBSERVED cognition (grounding, seam-catching, root-cause, intent-preserving triage and spec-writing) so Opus/Sonnet behave more Fable-like. Load as standing context for planning, auditing, and spec work.
---

> BUILD RULE (F2): each section holds an ABSTRACTED RECIPE (procedure/checklist/rubric/template), never a Fable transcript.
> BUILD RULE (F1): a move appears here only if a battery behavioral delta corroborated it.
> Evidence base: three blind Fable-vs-Opus runs on identical pinned tasks (`docs/plans/wwf5d/fable-runs/bt{1,2,3}-diff.md`). Where Opus already matched, the section says so — don't spend effort re-teaching what's already present.

## 1. Grounding protocol

Before analyzing anything, run these five moves on the inputs you were given:

1. **Consume every grounding answer, don't just restate it.** After restating given/pinned context in your own words, each fact must reappear in the analysis *doing work*. Before finishing, ask: which grounding fact did I never use? That's either a missed thread or a scope error — the on-theme miss is dropping a decided input in a task about dropped inputs. (BT2: a pinned prose-drift detail dropped by the baseline became root-cause evidence when consumed and amplified.)
2. **Hold epistemic framings exactly as given.** "Open risk" stays open risk; "hypothesis" stays hypothesis. Never upgrade to "confirmed failure" or downgrade to "non-issue" without new evidence from *this* run. (BT2: the baseline asserted an unobserved failure mode as implemented fact — in the very table whose job is separating intent from verified behavior.)
3. **Expand the evidence base to first-degree references.** Read what the pinned inputs *claim relationships with* before asserting anything about those relationships: `references/` files, named consumers' contracts, mirrored implementations, live tool surfaces. Text-only reasoning about a relationship you could verify is a finding-quality downgrade — and the highest-severity finding may live only in the un-pinned mirror. (BT1: the 1:1 skill-text↔shipped-code mirror was findable only by reading the live server; missing it made the baseline's own spec dangerous.)
4. **Mark every load-bearing property observed / documented / assumed.** Unobserved code gets no behavioral claims: either verify it now or convert the claim into a test obligation in your output ("must be made true by test, not asserted in prose").
5. **Detect the headless case.** If any procedure you're auditing or writing assumes an interactive user ("ask clarifying questions"), define the pre-answered path explicitly — restate supplied answers and proceed. Chains end in subagents that cannot ask anyone anything; an unconditional ask-first step there either hangs or gets silently skipped.

## 2. Seam / handoff checklist

For any multi-phase pipeline (skills chain, agent pipeline, build system), audit every decided input end to end:

1. **Inventory first.** One table: each decided input × where decided × who must consume it × transport-as-written. Include the inputs the grounding *didn't* name — user overrides/authorizations ("unless the owner explicitly asks"), coordinate/format systems, publish surfaces, tool mirrors, negative constraints. The pointed-at seams are where everyone looks; the tail findings live past them. (BT3: override-carrier, publish-surface, headless-format, and coordinate-space findings all came from unpointed seams.)
2. **Map every store of each decided value** with freshness and who-thinks-they-own-it. Two components behaving as owner = seam. Prose records that disagree with *each other* about the same fact are not noise — they're the signature of hand-copied state, and belong in the diagnosis. The designated system of record being the stalest store is the classic shape.
3. **Trace to point-of-effect, not point-of-arrival.** The hard seams aren't where the value fails to arrive; they're where it arrives and doesn't act: arrives-but-ignored (a checklist blind to a level decided two steps earlier), arrives-but-unreadable (coordinates in beat-space, draft in prose-space), arrives-but-empty (a fix list that's empty precisely after a fix was applied), emitted-but-unparseable (a prose verdict in a headless chain). End every trace at the line where the value changes behavior.
4. **Existence-check every enforcement claim.** "Enforced via X" is a claim about the world; verify X exists (the hook file, the deny-list entry, the config limit) before believing it — a named-but-unwired guard is a false sense of safety, which is worse than an admitted gap. Check *content*, not just presence: a checklist item that passes on the words "mandate present" accepts a paraphrase that lost the load-bearing half. (This item is here because the battery showed it does NOT emerge reliably — it was the baseline's best find and the blind run's clearest miss.)
5. **Interrogate the degraded paths.** Every "when X is present, check X" intake is a fail-open gate: ask what distinguishes legitimately-absent from lost-in-transit, and make loss loud (name the missing artifact; cap the verdict; never stamp trusted-pass un-anchored). Check escalation and format-upgrade paths for dropped protections — the "what NOT to change" list that vanishes when a floor template escalates to the full template is protection lost exactly when stakes rose.
6. **Read locked/unchangeable components adversarially.** For any file you may not edit: what could a literal-minded executor legally do with its text (an exception clause, a reshape license)? The disambiguation must ride in with the handoff, from outside.
7. **Treat mirrored text as a cross-boundary edit.** If text is mirrored elsewhere (published package, generated copy, paired doc), any edit to it is a *paired change* — say so where the edit is proposed, with a tripwire ("if you can't make the paired change, file a ticket instead of editing").

## 3. Root-cause ("zoom out") procedure

Honest scope note (F1/F3): the *basic* zoom-out — map state/control-flow/orchestration, produce a one-sentence system-level root cause, refuse the obvious patch — was matched by Opus at near-parity. Don't spend premium effort there. The delta-backed moves are the edges:

1. **Run the convergence check both ways.** The root cause must explain every recurring *instance* AND why every *failed patch* didn't hold. A root cause that doesn't explain the patch history is a candidate, not a conclusion.
2. **Refuse band-aids in both directions.** Name the under-fix (patching the call site where the class last surfaced; "record it in a comment/doc") — and the over-fix (a new service/abstraction/indirection when making the existing seam expressive suffices). Bounding the fix from above is what stops a weaker implementer from gold-plating.
3. **Promote record-vs-record inconsistency to evidence.** When two documents — or a doc and the code, or two sections of one file — disagree about the same fact on the same day, that inconsistency IS the root-cause signature of state without a single home. Cite it as such.
4. **Keep unobserved code out of the causal chain as fact.** A root-cause narrative may *hypothesize* about unread components, but the output must carry those as test obligations, never as observed behavior (§1.4).
5. **Build the intended-vs-implemented table with confirmed-correct rows.** One row per gap (documented intent vs as-built), plus explicit rows for what matches intent — those rows become the "What NOT to change" list, which is how the diagnosis protects working design from the fix.

## 4. Triage rubric (dangerously-wrong / structural / minor)

- **`dangerously-wrong`** — evaluate first, always: can this silently harm? The compound test is **silent × trusted × propagating**: produces output that will be *believed* (wrong number, false `ship`, fabricated citation, "enforced" that isn't), and/or spends real money or loses data, and/or fails only where nobody is watching (a scheduled run that quietly writes garbage outranks a crash). Quiet correctness failures outrank loud ones — a crash self-reports; a plausible wrong answer propagates.
- **`structural`** — correct today, taxes everything after: duplicated source of truth, a seam in the wrong place, a missing invariant, protection that drops at a boundary, a design that makes the next change expensive or the next contributor wrong by default. It doesn't fail; it compounds.
- **`minor`** — locally contained, loud when wrong, cheap to fix any time.

Calibration rules the battery corroborated:
1. **Altitude rule:** when a class-level enforcement surface and its instance failures both appear, tag the *gate* by the harm class it fails to catch (a validation gate that cannot fail anything is `dangerously-wrong` even though "nothing is broken yet"), and tag instances a class-level fix would catch as `structural`. The gate is the multiplier.
2. Don't demote structural to minor just because you can't construct the failing input on demand — "compounds silently" is the definition, not an excuse.
3. Instance-level triage matched Opus (cheap) — the rubric's value-add is the altitude rule and the DW-first ordering, not the category definitions.

## 5. Handoff / tool-adapter pattern

When output crosses to another skill, stage, agent, or human:

1. **Name WHO and the exact SHAPE.** A consumer named without its expected shape (schema, format, section/tag vocabulary) ships strong-content-wrong-shape — prose where the pipeline wanted `{stage, status, details}`. If the shape is unknown, write `shape: TBD — blocked on <consumer>`; an explicit unknown is a to-do, an omitted field is a seam.
2. **Operationalize available tools; don't acknowledge them.** Route the concrete procedure step through the concrete tool with its exact name and argument vocabulary ("run `audit_intent_spec`, paste its score+findings as the verdict block"), and make hand-run mode adopt the tool's output shape so the two paths stay comparable. "Prefer the tools when available" is a principle; a weaker executor needs the wiring.
3. **Uniform, machine-readable verdicts at every gate that can stop a pipeline.** If one gate emits structured verdicts and another emits prose, the prose gate is the one a headless consumer sails past — and the stop-authority gate is the worst place for that.
4. **State lives on the artifact, not in promised behavior.** Append the validation/verdict block to the emitted artifact itself (per-item pass/fail/waived-with-reason; `SKIPPED (user request)` is marked, never silent) so an unvalidated artifact is *visibly different* downstream. A behavioral rule dies at the first handoff to a model that didn't read it; an artifact convention is checkable by anyone holding the artifact.
5. **Strip internals at the publish boundary.** Pipeline metadata (verdict comments, change summaries) attaches to the manifest/handoff record, never to the published text; some real reader sees the publish surface.
6. **Protections travel through format changes.** Every escalation target (floor → full template, draft → final) needs a home for preservation constraints ("What NOT to change"), or escalation silently sheds the guardrails.
7. **Transport across an unowned or uneditable boundary belongs to the orchestrator.** When an artifact must cross a stage that can't carry it (locked file, pure-prose emitter, process boundary), assign the crossing to whoever invokes the stages — re-emit the bundle at every boundary (re-emission keeps it near the context tail, which is what survives compaction; files are for headless runs).

## 6. Intent-preserving spec template

Skeleton (all seven parts; the four-element floor is Objective / Root-cause-or-Reasoning / Change / What-NOT-to-change — scale up, never drop the negative space):

```
Objective            — why this exists + the trade-off priority for unspecified cases
Desired outcome      — observable before→after, from the owner's chair (not "section X now says Y")
The change           — per-finding fix, each with reasoning-to-carry + edge guidance
What NOT to change   — each entry: the thing + WHY it's protected
Done looks like      — checkable statements (greps, tests, exact error behaviors)
Band-aid tripwires   — "what would still count as a band-aid; reject these in review"
Deferrals            — what is explicitly NOT in this build, and what gates it
```

Rules the battery corroborated:

1. **Pre-make every decision.** Field names, state vocabularies, file locations, error shapes — decided in the spec, not offered as "e.g. X, or Y". Every decision left open delegates the exact judgment the diagnosis said keeps being made ad hoc, to the participant with the worst tiebreakers.
2. **Reasoning-to-carry per fix, plus edge guidance.** One paragraph the implementer can *decide from* when they hit a case the spec didn't enumerate, and the anticipated hard case with its resolution rule ("scope by content present, floor by declared level"; "when two rows disagree, blast radius wins").
3. **Anticipate the likeliest implementer breakage in THIS repo and defuse it explicitly.** Byte-pinned oracles, frozen dataclasses, load-bearing orderings, characterization tests: name the landmine, give the defusal ("add the field with a default; if the oracle asserts whole-spec equality, extend it deliberately in its own commit — never weaken it"). The spec that omits the repo's tripwires ships a breakage with extra steps.
4. **Negative space is load-bearing.** The do-NOT list carries reasons ("checklist ids — mirrored in shipped code"), authorizations and canonical texts are *quoted, never paraphrased* (a paraphrased override is how scope creeps back; a paraphrased mandate loses its halt-and-fallback half), and hedged language is banned — "consider maybe X" reads as optional and gets cut.
5. **Mirrored-text edits carry the paired-change protocol** (§2.7) inside the spec itself — the implementer must learn the cross-repo rule from the document instructing the edit.
6. **Done-criteria are executable.** "Grep finds no transport verdict that exists only in prose"; "generating X today raises, proven by test"; "suite passes with the oracle untouched." A criterion the implementer can't run is a wish.
7. **Self-application check:** if any fix in the spec edits text governed by a rule the spec itself establishes, say so and follow the rule ("this rewording is itself a paired cross-repo change per F5"). Specs that exempt themselves teach exemption.

## 7. Known ceiling — what did NOT transfer (from validation)

_Filled in Phase B from validation results: what did NOT transfer (F3)._

---

### Evidence index (F1 audit trail — section item → corroborating delta)

- §1.1 ← BT2-diff "consumed and amplified the prose-drift evidence". §1.2 ← BT2-diff "unobserved code stays unasserted". §1.3 ← BT1-diff "verified-world evidence-gathering" + "silently forks canonical text". §1.4 ← BT2-diff (same). §1.5 ← BT1-diff "headless / pre-answered grounding path".
- §2.1 ← BT3-diff coverage note + override/publish/format findings. §2.2 ← BT2-diff prose-drift + state-stores table. §2.3 ← BT1-diff level-blind checklist; BT3-diff coordinate-space, post-revise emptiness, headless verdict. §2.4 ← BT1-diff **OPUS+** existence-check + mandate-content findings (ceiling made explicit — adopted *because* the blind run missed it). §2.5 ← BT1-diff escalation-drop; BT3-diff fail-open intake + verdict cap. §2.6 ← BT3-diff reorder-license. §2.7 ← BT1-diff cross-repo fork.
- §3 scope note ← BT2-diff headline (near-parity). §3.1 ← BT2 both-runs convergence checks (matched; kept as floor). §3.2 ← BT2-diff both-direction band-aids. §3.3 ← BT2-diff prose-drift. §3.4 ← BT2-diff unobserved-code. §3.5 ← BT2 intended-vs-implemented + confirmed-correct rows (both runs; Fable's confirmed-correct list fed What-NOT directly).
- §4 altitude rule ← BT1-diff calibration note; §4 matched-parity note ← BT3-diff (identical DW tags).
- §5.1 ← BT1-diff shape-slot. §5.2 ← BT1-diff tools-operationalized. §5.3 ← BT3-diff value-engine machine voice. §5.4 ← BT1-diff verdict-block-as-artifact. §5.5 ← BT3-diff HTML-comments. §5.6 ← BT1-diff escalation-drop. §5.7 ← BT3-diff backbone (convergent with Opus — kept because the *mechanics*: re-emission physics, verdict cap, field-by-field accretion were the Fable side).
- §6.1 ← BT2-diff decided-not-optioned. §6.2 ← BT1/BT2/BT3 specs (edge guidance; matched in kind on BT1, Fable-systematic). §6.3 ← BT2-diff oracle-collision. §6.4 ← BT3-diff quoted-overrides; BT1 mandate copy-don't-paraphrase. §6.5 ← BT1-diff self-referential paired-change catch. §6.6 ← BT2-diff done-criteria. §6.7 ← BT1-diff (Fable's own F3 flagged as paired change).
- Dropped as uncorroborated (F1): introspection's deliverable-shape-first claim, research triggers "internal disagreement" and "repeated failure" (untested by this battery), compaction self-observations (the *design rule* §5.7 is corroborated; the self-claim isn't), grep-the-token as stated (the corroborated form is the store-inventory, §2.2).
