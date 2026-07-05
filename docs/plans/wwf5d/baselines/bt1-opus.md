# BT1 — Opus baseline
- Task: skill-audit on intent-engineering (chain of custody: docs/plans/wwf5d/task-battery.md § BT1)
- Model: Claude Opus 4.8 (fresh subagent, no prior session context)
- Date: 2026-07-04
- Inputs used: .claude/skills/skill-audit/SKILL.md @ 93e5725; .claude/skills/intent-engineering/SKILL.md @ 93e5725; grounding answers pinned in task-battery.md § BT1 (restated below)
- Contamination guard honored: tier1-specs/ not read

---

## Step 1 — Ground First (restated; pinned answers, headless run)

Skill-audit's Step 1 is a hard gate that normally blocks all scanning until the four grounding questions are answered and confirmed. For this run the answers are pre-pinned in task-battery.md § BT1. Per the skill's own instruction ("If the user's request already answers some of these in passing, restate your understanding of each back to them and get explicit confirmation"), I restate my understanding of each below. There is no interactive user to confirm with; the pinned run prompt authorizes proceeding directly to Step 2 once restated, so I treat the pinned answers as the confirmed grounding and do not re-derive or infer beyond them.

**(a) For — what the skill is for and who relies on it.**
Intent-engineering is the fleet's *intent backbone*: it designs, reviews, and retrofits the intent specs that every agent and skill is built on. Its job is to make the *why* — objective, desired outcomes, constraints — explicit so an agent still acts correctly when its literal instructions run out. It is not a one-off convenience skill; it is load-bearing infrastructure that other skills and every agent build depend on. My read: correctness here propagates fleet-wide, so a defect in this skill is a defect multiplier.

**(b) Feeds — what consumes its output.**
Four named downstream consumers: (1) skill-audit's own Step-5 improvement-spec artifact, which borrows intent-engineering's scaffolding "by name"; (2) zoom-out-and-think's spec output, same by-name borrow; (3) *every agent build* in the fleet (the specs become the agents-sdk config, allowed/disallowed tools, hooks); and (4) the local intent-engineering MCP tools. My read: these consumers expect specific, stable shapes — a named 9-section scaffold, a runnable validation checklist, and enforcement claims that map onto real architecture — so any shape drift or unenforced claim breaks a real downstream contract.

**(c) Disappoints — where it's technically-correct-but-owner-fixes-by-hand today.**
Three named pains: (1) the 9-section template is *heavyweight for small retrofits*; (2) the *retrofit levels are fuzzy* — no crisp answer to "when is Level 1 enough?"; (3) the *validation checklist exists but nothing forces it to run*. My read: all three are right-sizing / enforcement gaps, not content gaps — the material is good, but the skill doesn't govern *how much* of itself to apply or *whether* its own quality gate fired.

**(d) Wow — the screenshot-worthy version.**
Specs that (1) survive three handoffs (Fable → Opus → subagent) with *zero intent drift*, (2) are *right-sized per retrofit level*, and (3) have *validation actually gating* the output. My read: the wow bar is durability-under-handoff + right-sizing + a real gate — precisely the inverse of the three disappointments, plus the handoff-durability clause that (c) doesn't mention.

Proceeding to Step 2.

---

## Step 2 — Seam Scan

A seam is where the skill *decides* something early and a later phase can run to completion having silently forgotten it. Intent-engineering isn't a single linear pipeline, but its "How to Use This Skill" section defines three genuine multi-step workflows (write / review / retrofit), each shaped exactly like the ground→draft→refine→output pattern skill-audit flags as most seam-prone. I scan those workflows plus the cross-references between the template sections.

### 2.1 Decided inputs the skill builds or receives early

| # | Decided input | Where it's decided |
|---|---|---|
| D1 | Clarifying answers about domain, users, and **failure modes** | Write flow, step 1 ("Ask clarifying questions about the domain, users, and failure modes") |
| D2 | **Autonomy level** / "is this an unattended, launchd agent?" | Section 7 + Autonomy Levels table (Full-Autonomous = "Runs on schedule via launchd") |
| D3 | Recommended **retrofit level** (1/2/3) | Retrofit flow, step 2 ("Recommend conversion level based on blast radius and complexity") |
| D4 | Named **enforcement mechanism** per hard constraint (hook / disallowedTools / config.toml) | Section 6 ("Never [FORBIDDEN ACTION] — enforced via [MECHANISM]") |
| D5 | **Desired outcomes** (2-4 observable states) | Section 3 |
| D6 | Current-state assessment (prompt vs partial spec) | Retrofit flow, step 1 |

### 2.2 Walking later phases against each decided input

**D1 (failure modes) → the draft. SEAM.** The write flow is `ask questions (incl. failure modes) → draft using the 9-section template → validate → flag gaps`. Step 2 points the drafter at the *template*, not at the answers. Section 8 (Edge Cases) and Section 4 (Health Metrics) — the two sections the elicited failure modes should populate — show only generic `[UNUSUAL CONDITION]` / `[METRIC]` placeholders and never say "use the failure modes the user just gave you." A weaker model can ask the questions, receive "the vendor API times out and the agent retries forever," then draft an Edge Cases section full of invented-generic conditions that never mention the timeout the user flagged. This is the canonical ground→draft seam. **Concrete failure:** the user hands over their real failure modes in step 1 and the shipped spec's Edge Cases / Health Metrics are generic template filler that ignores them.

**D2 (autonomy / unattended) → Stop Rules. SEAM.** The determination "this agent runs unattended via launchd" is made in Section 7 / the Autonomy table. The instruction to act on it — "If the agent runs autonomously via launchd, you MUST inject the Zero-Interaction Mandate into the Stop Rules" — lives *only* inside the MVR **Level 1 retrofit** subsection. Section 9's Stop Rules template does not carry the mandate as a conditional, and the *write-from-scratch* flow never mentions it. So a spec **written fresh** for a launchd agent (not retrofitted) reaches Section 9 with the autonomy fact already decided but never converted into a stop rule. The only backstop is one Validation-checklist line ("(For scheduled agents) Zero-Interaction Mandate is present"), which is non-gating (see W3). **Concrete failure:** a from-scratch autonomous-agent spec ships with no Zero-Interaction Mandate; at 3 AM the agent hits an ambiguous case, tries to ask the human, and hangs / burns its budget with no one to unblock it — the exact failure the mandate exists to prevent.

**D4 (named enforcement mechanism) → Verification. SEAM.** Section 6 has the drafter *name* an enforcement mechanism ("enforced via PreToolUse hook"). Section 9's Verification block is generic (`[AUTOMATED CHECK]: [WHAT IT VALIDATES]`) and never says "confirm the mechanism you named actually exists." The Constraint-Quality checklist item "Every harm-causing constraint is enforced architecturally" is satisfiable on paper by *writing the word* "enforced." So the decision "this is enforced in architecture" never carries into any step that verifies the architecture is real. **Concrete failure:** a spec asserts "Never wipe the DB — enforced via PreToolUse hook"; no such hook was ever wired; the owner reads the spec, trusts the guard, ships the agent, and the catastrophic action is in fact unprotected.

**D3 (retrofit level) → conversion. Partially carries; under-determined.** Retrofit step 3 does say "Perform the conversion *at recommended level*," so the level carries. But the *selection* of the level is under-determined: the "Prioritization for 107 Skills" list gives signals that can conflict (Autonomy: "interactive-only → Level 1"; Complexity: "Multi-step workflows → Level 2 or 3") with no tie-breaker for a skill that is both interactive-only *and* multi-step. This is the fuzziness (c) names; treated as structural under Step 4 (W2).

**D5 (desired outcomes) → Health Metrics. CARRIES CORRECTLY — not a seam.** Section 4's quality test ("For each desired outcome, ask 'How could the agent achieve this outcome in a way I'd hate?'") and the Health-Metric-Quality checklist item ("At least one health metric per desired outcome") both force outcomes to carry into health metrics. This seam is already closed and belongs in "What NOT to Change."

**D6 (current-state assessment) → conversion. Carries.** Retrofit step 2 consumes step 1's assessment to pick a level. No seam.

### 2.3 Also confirmed closed (strengths to protect)

Section 1 Objective → trade-off guidance (Objective quality test), Section 6 hard constraints → architecture (Autonomy→architecture mapping bullets), and Section 7 autonomy → config mechanism are all explicitly wired. The template's *internal* seams are well-handled; the live seams are in the **workflow layer** (write/retrofit) and the **cross-references** (validation gating, mandate injection, enforcement verification, MCP-tool handoff), not in the template's section-to-section wiring.

---

## Step 3 — Adapter Scan

Walking each of the four named (b) consumers and the precise shape each expects.

**Consumer 1 & 2 — skill-audit and zoom-out-and-think borrow the scaffold "by name."** Expected shape: a stably-named 9-section scaffold plus a runnable validation checklist they can point at or invoke. Intent-engineering **provides both** — the adapter mostly holds. *Gap (minor):* both consumers need to *right-size* the borrowed scaffold (skill-audit invents its own "four-element floor" for small fixes vs "full 9-section template" for large ones), but intent-engineering offers no size-ladder framed for *sizing a fresh improvement spec* — its levels are framed around retrofitting *existing* skills. Consumers therefore invent their own floor rather than referencing one. → A2, minor.

**Consumer 3 — every agent build.** Expected shape: Objective / Outcomes / Constraints / Stop-Rules that map onto real agents-sdk artifacts (config.toml limits, allowed_tools/disallowedTools, hooks). The Autonomy-Levels → architecture mapping handles the *translation* well. The adapter defect is verification, not translation: the spec *names* a config.toml/hook/disallowedTools mechanism (D4) but nothing confirms the agent build actually contains it. This is the spec→agent-build face of the D4 seam. → carried as a dangerously-wrong finding.

**Consumer 4 — the local intent-engineering MCP tools. MISSING ADAPTER.** Three MCP tools exist whose names mirror this skill's three core operations one-to-one: `assess_retrofit_level`, `audit_intent_spec`, `generate_intent_spec_scaffold`. The SKILL.md **never references them at all** — it describes doing retrofit-level assessment, spec review/audit, and scaffold generation entirely by hand, in prose, with no acknowledgement that dedicated tools for exactly those three jobs exist. This is two parallel implementations of the same operations with no cross-reference and therefore no shape contract between them. (Per the run's constraint I did **not** invoke these tools — this finding is from the SKILL.md text plus the (b) grounding answer that names the MCP tools as a consumer; the audit is of whether the *skill text* hands off correctly, and it doesn't reference the handoff target at all.) **Concrete failure:** the skill hand-rolls a retrofit level or a scaffold whose shape or level-definitions drift from what the MCP tools produce/expect, so a spec assessed as "Level 1" by the prose heuristics is treated differently by `assess_retrofit_level`, and downstream anything keyed to the tool's structured output silently disagrees with the skill's. → A1, structural.

---

## Step 4 — Wow-Gap Scan

Target bar = (d): survive three handoffs with zero intent drift, right-sized per level, validation actually gating. Each clause maps to a concrete missing move.

**W3 — Validation actually gating (missing move: a stop rule that blocks emission).** Every workflow says "Run the Validation Checklist," but no step says "do not emit the spec until it passes," and no behavior is defined for a *failed* check. So the model can run the checklist, note three unchecked boxes, and emit anyway. The irony is total: this skill's Section 9 is *Stop Rules & Verification* and its 5th Fatal Anti-Pattern is *"Infinite Loops (Missing Stop Rules)"* — yet the skill's own output pipeline has **no stop rule gating its own output**. Missing move: a gate — "do not emit until every harm-relevant check passes; for any failing check, fix the section or explicitly label it `[UNRESOLVED]` and escalate — never emit silently." This single move closes (c)'s "nothing forces it to run" *and* (d)'s "validation actually gating."

**W1 — Zero intent drift across three handoffs (missing move: a handoff-durability pass).** The wow bar is a spec whose *why* survives Fable→Opus→subagent. The skill has the *ingredients* (Objective quality test: "If you remove all other sections, can the agent still make reasonable decisions?") but applies that durability test to the Objective *alone*. Nothing stress-tests the whole spec against the question "if a weaker model read ONLY this and hit an edge case not enumerated, does the written why give it enough to choose as the owner would?" Missing move: a final handoff-durability pass over the intent-bearing sections (Objective, Health Metrics, Hard Constraints, Stop Rules) that strengthens the *why* where a downstream model could drift — not more instructions, more surviving intent.

**W2 — Right-sized per retrofit level (missing move: a tie-breaker + a post-conversion right-size check).** (c)'s "when is Level 1 enough?" has no deterministic answer when signals conflict, and there is no check after conversion asking "does this spec have exactly the sections its blast radius demands — no missing safety sections, no ceremonial ones?" Missing move: a precedence rule (safety/blast-radius signals beat convenience/complexity signals) plus a post-conversion right-size checkpoint. Compounded by S3 below (the headline "MUST include all 9 sections" fights the MVR's 3-section Level 1).

**Prioritization (required by Step 4.3).** The two highest-leverage gaps are **W3 (validation gating)** and **W1 (handoff-durability pass)**. W3 is #1: it's a single concrete mechanism (a stop rule) that resolves one full (c) pain and one full (d) clause at once, and it removes the skill's most embarrassing self-contradiction. W1 is #2: it directly buys the "zero intent drift across three handoffs" clause that is the heart of the wow bar and is the skill's entire reason to exist ("intent is what determines how an agent acts when instructions run out"). **W2 / right-sizing is real but second-tier** — it's judgment-tuning (a precedence rule) rather than a missing mechanism, and it improves an already-usable output rather than closing a trust gap.

---

## Artifact 1 — Seam Report

Flat list, most-severe first. Each finding: severity — where — what — what the owner concretely observes when it bites.

- `dangerously-wrong` — **Write flow + Section 9 (Stop Rules), vs MVR Level 1.** The Zero-Interaction Mandate is required only inside the MVR-Level-1 retrofit subsection; the write-from-scratch flow and Section 9's template never inject it, even though the "unattended launchd agent" fact is already decided in Section 7 / the Autonomy table. A fresh spec for an autonomous agent ships with no mandate. **Owner observes:** a scheduled agent hits an ambiguous case at 3 AM, tries to ask a human, and hangs or burns its full budget with no one present — the precise failure the mandate exists to prevent, in a spec the owner trusted as complete.
- `dangerously-wrong` — **Section 6 → Section 9 (Verification).** Hard constraints are written as "enforced via [MECHANISM]," but no step verifies the named hook / disallowedTools / config.toml limit actually exists; the Constraint-Quality checklist ("enforced architecturally") is satisfiable by merely writing the word "enforced." **Owner observes:** a spec that reads "Never wipe the DB — enforced via PreToolUse hook" where no hook was ever wired; the owner ships believing the catastrophic action is guarded, and it isn't. This directly undercuts the skill's own central thesis ("don't trust the prompt to enforce it") and its Anti-Pattern #2.
- `structural` — **All three workflows (validation step).** The Validation Checklist is run but never *gates*: no stop rule blocks emission on a failed check and no on-failure behavior is defined, so specs ship with silent validation failures. **Owner observes:** exactly (c) — "the validation checklist exists but nothing forces it to run"; the owner re-checks specs by hand. (Self-contradiction: the skill preaches Stop Rules in Section 9 and Anti-Pattern #5 yet has no stop rule on its own output. Highest-leverage gap toward the (d) wow bar.)
- `structural` — **Write flow, step 1 → step 2.** The clarifying answers — especially the elicited **failure modes** — are not carried into the draft; Step 2 points at the template, and Sections 4/8 show only generic placeholders. **Owner observes:** the failure modes they described in the interview are absent from the shipped spec's Edge Cases and Health Metrics, replaced by generic template filler — the canonical ground→draft seam.
- `structural` — **Headline mandate vs MVR guide.** "Every intent spec you write or review MUST include all 9 sections" contradicts "Level 1 = 3 sections (Objective, Desired Outcomes, Stop Rules)"; the skill never scopes which rule applies when. A model reading top-down hits the absolute MUST first. **Owner observes:** exactly (c)'s "9-section template is heavyweight for small retrofits" — a tiny interactive skill gets a full 9-section spec because the headline said MUST.
- `structural` — **MVR "Prioritization for 107 Skills."** Retrofit-level selection has conflicting signals (interactive-only → Level 1 vs multi-step → Level 2/3) with no tie-breaker, and no post-conversion right-size check. **Owner observes:** exactly (c)'s "retrofit levels are fuzzy — when is Level 1 enough?"; two runs pick different levels for the same skill.
- `structural` — **Whole skill vs the intent-engineering MCP tools.** The SKILL.md never references `assess_retrofit_level`, `audit_intent_spec`, or `generate_intent_spec_scaffold`, which mirror its three core operations; the skill hand-rolls all three with no shape contract to the tools. **Owner observes:** a scaffold or retrofit-level produced by the skill drifts from what the MCP tools produce/expect, so structured consumers of the tools' output silently disagree with the skill's freehand output.
- `structural` — **All workflows (final output).** No handoff-durability pass: nothing stress-tests whether the spec's *why* survives a weaker model reading only the spec and hitting an un-enumerated edge case. **Owner observes:** the (d) wow bar ("three handoffs, zero intent drift") is missed — the subagent at the end of Fable→Opus→subagent improvises off-intent because the surviving text under-specified the why.
- `minor` — **Consumer handoff (skill-audit / zoom-out-and-think).** The by-name scaffold + checklist borrow works, but there's no size-ladder for a *borrowed* scaffold, so consumers invent their own floor (skill-audit's "four elements"). **Owner observes:** mild inconsistency in how borrowing skills size their intent scaffolds; nothing breaks.

---

## Artifact 2 — Intent-Carrying Improvement Spec

Structured on intent-engineering's own scaffolding (per skill-audit Step 5). Scoped, in the skill's own terms, as a **Level-2-equivalent** change to the skill's *workflow and cross-reference layer* — it adds stop rules, edge-case handling, and verification to how the skill operates, and deliberately does **not** rewrite the (strong) 9-section template. Right-sizing the fix this way is itself an instance of the (d) "right-sized per level" bar.

### Objective
Intent-engineering is the fleet's intent backbone (a): a defect here multiplies across every agent build and every consuming skill. Today it is technically complete but disappoints in three governed-by-the-skill-itself ways (c): it over-applies itself to small retrofits, it can't crisply size a retrofit, and it never enforces its own quality gate. Two unnamed-but-present defects are worse than disappointing — they let a spec ship that the owner *trusts but shouldn't* (a missing Zero-Interaction Mandate on an autonomous agent; a hard constraint "enforced via" a mechanism that was never wired). When trade-offs arise, prioritize **trustworthy-and-right-sized output over feature completeness of the template** — the template is already rich; the missing thing is *governance of how much of it fires and whether the result is safe to trust*.

### Desired Outcome
From the owner's perspective (answers (c) and (d)): a spec this skill emits is (1) **right-sized** — a small interactive retrofit gets a 3-section Level 1, not a ceremonial 9-section wall; (2) **self-gated** — it does not emit until validation passes or the failures are explicitly surfaced and escalated; (3) **safe to trust** — an autonomous-agent spec always carries the Zero-Interaction Mandate, and every "enforced via X" claim has been existence-checked, never asserted on faith; and (4) **handoff-durable** — the *why* survives Fable→Opus→subagent with zero intent drift. Observable difference: the owner stops hand-fixing specs for size and for missing gates, and stops discovering after the fact that a "guarded" agent was never actually guarded.

### The fix, per finding

**`dangerously-wrong` — Zero-Interaction Mandate not injected in the write flow.**
*Fix:* Move the Zero-Interaction Mandate from an MVR-Level-1-only instruction to (i) a conditional inside Section 9's Stop Rules template and (ii) an explicit step in the write-from-scratch flow, keyed on autonomy level: "If Section 7 autonomy = Full-Autonomous or Guarded-Autonomous, you MUST inject the Zero-Interaction Mandate into Stop Rules — this fires for specs written from scratch, not only retrofits."
*Reasoning a weaker model needs:* the trigger is the *autonomy determination*, not the retrofit-vs-write path — the current text accidentally couples the mandate to the retrofit path only. The *why*: an unattended agent that pauses for input has no human to unblock it, so it hangs or burns budget; the mandate is the architectural expression of "no human is coming." On any edge case where you're unsure whether an agent is unattended, treat "runs on a schedule / launchd / cron / no interactive session" as unattended and inject the mandate — false-positive cost is near zero, false-negative cost is a hung production agent.

**`dangerously-wrong` — Named-but-unverified enforcement mechanism.**
*Fix:* Add to Section 9 Verification (and tighten the Constraint-Quality checklist) a required existence check: "For every Hard Constraint that names an enforcement mechanism, confirm the mechanism actually exists in the codebase (the hook file, the `disallowedTools` entry, the `config.toml` limit) before declaring the spec done. If it does not exist, the constraint is NOT yet enforced — mark it `[ENFORCEMENT NOT WIRED]`; for a catastrophic constraint, shipping is blocked until it is wired."
*Reasoning a weaker model needs:* the skill's entire thesis is "don't trust the prompt; enforce in architecture" — but *naming* a mechanism is not *enforcing* it. The dangerous failure is a false sense of safety, which is worse than an admitted gap because the owner stops watching. Edge case: if you lack filesystem access to verify, you must **downgrade the claim** to "PROPOSED enforcement — unverified," never assert enforcement you did not confirm. The rule is: the word "enforced" is a claim about the world, and you may only make it after checking the world.

**`structural` — Validation checklist doesn't gate emission (highest-leverage).**
*Fix:* Add a Stop Rule to the skill's own workflow (all three modes): "Do not emit a spec until the Validation Checklist has run and every harm-relevant box passes. For any unchecked box, either fix the section or explicitly label it `[UNRESOLVED: <check>]` and escalate to the human — never emit silently past a failed check." Wire this to the existing write-flow step 4 ("Flag sections where you lack information") so a genuinely-missing input becomes an explicit surfaced gap, not a papered-over pass.
*Reasoning a weaker model needs:* the gate's purpose is **trust** — a spec that ships with silent validation failures is exactly the "works but disappoints" outcome (c), and it is the failure this skill's own Section 9 and Anti-Pattern #5 exist to prevent. The skill must model on its own output the discipline it demands of the agents it specs. On the edge case where a check can't pass because information is missing (not because the spec is wrong), surface it explicitly and escalate — the sin is silent emission, not an honest `[UNRESOLVED]`.

**`structural` — Ground→draft seam (failure modes dropped).**
*Fix:* Make write-flow step 2 explicitly consume step 1. Before drafting, map each clarifying answer to its home section: failure modes → Edge Cases (Section 8) **and** Health Metrics (Section 4); user friction → User Goal (Section 2) + Objective; domain constraints → Constraints (Section 6). Require that the draft's Edge Cases and Health Metrics *name the specific failure modes the user gave*, not generic placeholders.
*Reasoning a weaker model needs:* the elicited failure modes are the single highest-value input and the easiest to drop, because Section 8's template shows generic `[UNUSUAL CONDITION]` slots that *look* complete when filled with invented conditions. The *why*: every unhandled real edge case is (per the skill's own words) "a potential hallucination point" — and the ones the user just handed you are the real ones. On any edge case where an elicited failure mode doesn't obviously belong to a section, default it into Edge Cases (Section 8) rather than dropping it.

**`structural` — "MUST include all 9 sections" contradicts Level 1 = 3 sections.**
*Fix:* Scope the headline. Change "Every intent spec you write or review MUST include all 9 sections" to: "Every **full (Level-3 / from-scratch production)** intent spec MUST include all 9 sections. Retrofits are right-sized via the MVR guide — Level 1 is 3 sections and is *complete* for interactive, low-blast-radius skills." Add a forward-link from the headline to the MVR guide.
*Reasoning a weaker model needs:* the contradiction is what produces (c)'s "heavyweight for small retrofits" — a model reading top-down obeys the most prominent, most absolute rule (the headline MUST) and over-applies it. The *why*: "complete" is relative to blast radius, not to the template's maximum. The scope boundary must be explicit, because a weaker model will otherwise resolve the contradiction toward the loudest rule.

**`structural` — Retrofit-level selection has no tie-breaker.**
*Fix:* Add a precedence rule and a post-conversion check to the MVR guide: "When signals conflict, **autonomy / blast-radius wins over complexity** — an unattended or production-touching skill gets at least Level 2 regardless of simplicity; a purely interactive, reversible skill caps at Level 1 even if multi-step, *unless* it produces specs other skills chain off (then Level 2). After converting, run a right-size check: does the spec have exactly the sections its blast radius demands — no missing safety sections, no ceremonial ones?"
*Reasoning a weaker model needs:* the fix is *determinism* — two models must pick the same level for the same skill, which requires a precedence order, not more prose. The *why* behind "safety signals beat convenience signals": under-sizing a risky skill is a safety failure, over-sizing a safe skill is only an annoyance, so the tie must break toward safety. On a genuinely novel conflict the spec didn't enumerate, apply that same asymmetry: when unsure, size up if any safety/autonomy signal is present, size down only when all signals are convenience.

**`structural` — SKILL.md never references the intent-engineering MCP tools.**
*Fix:* Add an explicit handoff note near the "How to Use" section: "Three MCP tools mirror this skill's core operations — `assess_retrofit_level`, `audit_intent_spec`, `generate_intent_spec_scaffold`. When available, treat them as the canonical implementation (their scaffold shape, retrofit-level definitions, and audit structure are the source of truth) and align prose output to their contract. When unavailable, this SKILL.md is the fallback and must produce the same shape. Never let the skill's hand-rolled levels or scaffold silently diverge from the tools'."
*Reasoning a weaker model needs:* (b) names the MCP tools as consumers; two parallel implementations of the same three operations will drift, and the drift is invisible until a structured consumer of the tools' output disagrees with a hand-rolled spec. The *why*: the tools define the shape contract; the skill's job is to stay compatible with it, not to reinvent it. (Do **not** infer the tools' exact schema by calling them during an *audit* of the skill text — the fix is a durable "prefer the tools / match their shape" instruction, which holds regardless of the current schema.)

**`structural` — No handoff-durability pass.**
*Fix:* Add a final pass to the write and retrofit workflows: "Handoff-durability check — for each intent-bearing section (Objective, Health Metrics, Hard Constraints, Stop Rules), ask: if a weaker model read ONLY this spec and hit an edge case not enumerated here, does what's written give it enough to choose as the owner would? Where it doesn't, strengthen the *why* — do not add more instructions."
*Reasoning a weaker model needs:* (d)'s bar is zero intent drift across three handoffs, and the skill already contains the right test for the Objective alone ("if you remove all other sections, can the agent still decide?") — generalize that test to the whole intent-bearing spec. The *why*: this skill's own opening claim is that intent is "what determines how an agent acts when instructions run out," so the durability test *is* the product. Critically, the fix for under-durability is more surviving *intent* (why), never more *instructions* (what) — adding instructions makes the spec heavier (worsening (c)) without making the why survive.

**`minor` — No size-ladder for consumer skills borrowing the scaffold.**
*Fix (terse):* Add a one-line pointer for consumers: "Borrowing skills right-size a borrowed scaffold on the MVR ladder — Level 1 (3 sections) ≈ a small contained fix; the full 9-section template ≈ a large fix." No reasoning writeup required.

### What NOT to Change
The audit confirmed these are working; do not "improve" them:

- **The 9-section template's internal wiring.** Outcomes→Health-Metrics (via the "how could the agent game this?" quality test), Hard-Constraints→architecture (the mapping bullets), and Objective-as-trade-off-guide are already closed seams. Leave them.
- **The Activity-vs-Outcome anti-pattern table and the "how could the agent achieve this in a way I'd hate?" health-metric test.** These are the skill's crown jewels and its most-borrowed content. Leave them verbatim.
- **The four Sean-specific Domain Examples** (education course, 16BitFit sprite, daily driver, spending analysis). They are concrete and load-bearing; do not genericize them.
- **The Autonomy Levels → architecture mapping** and the Five-Lenses risk assessment. Correct as-is.
- **The core thesis** ("intent cannot live entirely in the prompt; hard boundaries must be enforced by architecture"). This is the skill's spine — every fix above *serves* it; none should dilute it.
- **Do NOT add new sections to the 9-section template to address the heavyweight complaint.** The fix for (c) is *scoping and right-sizing what already exists*, not adding more — adding sections makes the heavyweight problem strictly worse.

---

## Success-criteria self-check (skill-audit's own checklist)
- [x] All four grounding answers (a)-(d) restated before scanning (Step 1; pinned-answer headless variant honored).
- [x] Seam scan names specific decided inputs (D1-D6) and the specific phase each fails to survive into.
- [x] Adapter scan names the receiving format for every (b) handoff (all four consumers walked), not just "format it better."
- [x] Wow-gap scan names concrete missing moves (stop-rule gate, handoff-durability pass, tie-breaker) and prioritizes (W3 then W1).
- [x] Seam report is a flat bulleted list; every finding tagged exactly one of `dangerously-wrong` / `structural` / `minor` (2 / 6 / 1).
- [x] Improvement spec carries Objective, Desired Outcome, per-finding fix-with-reasoning (all `dangerously-wrong` + `structural`), and What NOT to Change.
- [x] Both artifacts emitted in the same pass.
