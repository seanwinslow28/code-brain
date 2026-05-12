---
type: research-synthesis
project: prj-job-hunt-2026
phase: interview-prep-phase-1
created: 2026-05-10
sources:
  - 2026-05-09-perplexity-ai-vibe-coding-interview-canon.md
  - 2026-05-09-gemini-ai-vibe-coding-interview-canon.md
provenance_legend:
  - "[P] = Perplexity Pro only"
  - "[G] = Gemini Deep Research only"
  - "[P+G] = both sources, mutually corroborating"
  - "[Coach] = playbook author judgment, not in either source"
ai-context: "Synthesis layer for vibe-coding interview prep. Phase 1 of 4. Output gates Phase 2 playbook."
---

# Vibe-Coding Research Synthesis — Sean × 2026-05

> **Why you're reading this:** You ran the same canon prompt on Perplexity Pro and Gemini Deep Research. Both produced playbook-shaped outputs with overlapping bones and meaningful disagreements. This file reconciles them into one defensible canon, picks sides where they diverge, and labels every claim with provenance. Phase 2 (the executable playbook) builds on top of this synthesis.

> **Note on context resolution.** Initial pass: the surrounding plan documents did not resolve on first search. Sean provided exact paths; on second pass I read the unified roadmap, master plan, and all 5 operating-model files (HEARTBEAT, USER, SOUL, operating-model, schedule-recommendations). The roadmap, in particular, materially composes with this synthesis — see "Roadmap-anchored additions" below. Nothing in the operating model contradicts the synthesis as originally written; several pieces sharpen it.

### Roadmap-anchored additions (read after the rest of the doc)

The unified roadmap and operating-model artifacts add five specific anchors that should sit inside the prep canon:

1. **Tier-A relocation exception clauses** [SOUL]. Walk-away is $100k base; remote-preferred is overridden by (a) Anthropic specifically, or (b) any role with $250k+ base. Implication for the playbook: when an FDE Boston onsite is offered, "would you relocate?" has a yes-with-condition answer pre-decided. Don't fumble that question.

2. **The Karpathy single-top-rec is the operating-model's named thesis** [operating-model + roadmap Part 1 Claim B]. Sean has formally locked "one shipped MCP server" as the canonical career artifact for 2026. This is the artifact-walkthrough opener for FDE and Agent-PM loops — "you're looking at the Karpathy thesis, in code." Phase 2 §5 will lead with this framing.

3. **The Agent Ops / FDP backup track is now official policy** [roadmap Decision 3]. Anthropic FDE Boston is a Week-2 wildcard application; Glean (Agent Security & Governance, AI Quality, FDP), Scale AI (GenAI Platform PM, Public Sector T&E PM), and Sierra/Decagon agent PMs are the named Tier-2/3 set. Phase 2 portfolio walkthroughs will tier-map to this exact target list rather than the abstract "Tier-1 / Tier-2 / Tier-3" framing.

4. **"The Extra Hour" north star — Agentic workflows + Agent Evals + Enterprise build patterns** [schedule-recommendations]. This is the gap Sean himself has flagged. Phase 4 daily warm-keep and Phase 2 question-asking sections will both anchor against these three vectors so the interview surfaces what Sean is actively learning, not what he isn't.

5. **The 4Q `EXPLANATION.md` discipline is the comprehension-artifact backbone** [roadmap Tasks 1-5]. Every portfolio artifact already has (or will have by Week 4) a co-located 4-question explanation file. Phase 2's portfolio walkthrough scripts can lean on the 4Q answers directly — Sean has already done the writing; the walkthrough is reading from the 4Q out loud in his voice. This is a load-reducing realization for the prep plan.

**One sharpening, not contradiction:** the roadmap calls out that Sean self-codes as beginner-to-intermediate and the MCP server v0 scope must be **small** (3 tools, stdio transport, Claude Desktop demo). Phase 2 portfolio scripts will respect that scope discipline — when an interviewer asks "why didn't you build it bigger?" the answer is the same scope discipline Sean already applied: "shipping a defensible small thing beats demoing an over-engineered thing."

---

## The 3 most important findings (read these first)

**Finding 1 — Sierra's actual format is a 2-hour solo build, not a 45-minute rep [P, contradicts G].** Gemini's company-format table puts Sierra at "45 minutes, open choice tooling." Perplexity reads Sierra's own engineering blog post (sierra.ai/blog/the-ai-native-interview, published 2026-04-23) and cites the actual three-phase structure: a 30-45 min Plan phase (candidate ideates, interviewers probe), a **2-hour solo Build phase with the interviewer leaving the room**, and a 45-60 min Review phase (demo + code-level interrogation). Perplexity also flags that Sierra's documented format is for engineers, not PMs — so the Sierra PM loop is "not publicly verifiable." This matters concretely: if you're prepping for Sierra-style loops you're prepping stamina + architectural depth + how-you-used-AI narration, **not** the panic-cadence of a 45-min build. Verdict: Perplexity wins. The Gemini table is overconfident; the Sierra row should be treated as wrong on duration and rep shape.

**Finding 2 — Anthropic does NOT do vibe-coding for PMs [P+G, with Perplexity more honest about the evidence].** Both sources agree that Anthropic's PM loop is portfolio walkthrough + system design + behavioral + safety/values, not a live AI-assisted build. Anthropic's published candidate AI guidance permits Claude in the take-home only when explicitly stated. For your Tier-3 wildcards (Anthropic FDE Boston/NYC/Chicago, Glean FDP), the prep load is asymmetric to the rest of your target list — you're building portfolio-walkthrough fluency and architectural defensibility, not Bolt/v0 muscle memory. Plan accordingly.

**Finding 3 — The F1-score failure mode is the single highest-leverage thing to inoculate against [P+G, same Aakash Gupta primary source].** Both sources cite the same coaching anecdote: a Google PM candidate, asked the F1 score of an AI feature they "owned," said "I'd have to check," and the loop ended in the interviewer's mind. Both sources agree this is the canonical signal of "claiming AI ownership without being able to defend the technical specifics." For you specifically — given a 14-agent fleet, an in-flight MCP server, Phase D typed reasoning edges, and a sanitized financial-research fleet, all of which an interviewer can ask metric-defining questions about — this is your biggest avoidable landmine. **You don't have an experience problem. You have a metrics-vocabulary problem.** Inoculation is concrete and finite: memorize precision, recall, F1, latency budgets, token cost per call, and at least one named eval metric per portfolio artifact. This shows up in Phase 2 as the #1 weak-spot drill.

---

## Consensus canon (claims both sources support)

The following are the load-bearing pieces of the canon that both Perplexity and Gemini converge on independently. Treat these as the trunk of the playbook:

**Format diversity is real.** [P+G] No single vibe-coding format dominates. The three recognized shapes are (a) the 45-min live build, (b) the product-design case with a prototyping component (30-60 min), and (c) the take-home with deployed-prototype deliverable. Both sources emphasize you can't prep a single mode. Perplexity is the more disciplined one about flagging "not publicly verifiable" per company.

**Verification depth is the senior signal.** [P+G] Generation is now cheap; verification is what evaluators score. The HIGH signal is vocalized hesitation after AI-generated code lands ("let me check the error path on this," "the loop will degrade past 10k records"). The LOW signal is paste-and-run with no audit. The blow-up is shipping hallucinated/unsecured code to the deploy target.

**Decision narration is the load-bearing communication skill.** [P+G] Evaluators cannot score what they cannot hear. Both sources name silence as a top failure mode and over-narration as the equally-fatal opposite. Gemini frames it as "auditory breadcrumbs"; Perplexity as "concurrent narration." Same idea.

**Working-state freeze near the end of the rep is mandatory.** [P+G] Gemini puts the freeze at minute 40 of a 45-min rep; Perplexity puts the hard stop at minute 35. Both agree the most preventable unforced error is the "one more feature" deploy crash in the final 5 minutes. Verdict on the cutoff: Perplexity's minute-35 stop is more defensible because it leaves a 10-minute polish + demo + trade-off-narration buffer. [Coach] For you specifically, lock minute 35 and never let it move.

**Spec interpretation in the first 5 minutes is non-optional.** [P+G] Restate the brief, ask 2-3 clarifying questions (Perplexity caps at 3 explicitly; Gemini implies similar), state a "will-build / won't-build" list, prime the tool. Skipping any of these reads as junior. Perplexity's framing — "treat the will/won't list as a contract" — is more usable than Gemini's "ruthless scope negotiation" framing.

**The 7-dimension evaluation rubric.** [P+G] Both sources arrive at 7 evaluation dimensions independently with substantial overlap. Spec interpretation, prompting/steerage, decision narration, failure recovery, speed-to-working-state, and artifact quality appear in both. The seventh slot diverges (see disagreements below) — Gemini puts "economic awareness" there, Perplexity puts "user-centered decision making." [Coach] Hold both. Phase 2 will land with 7 dimensions where the seventh is a fused "user-centered + economic" dimension because both are evaluator-real and they touch in practice (rejecting an expensive vector DB for a string-match problem is both economic and user-centered).

**Sample-rep difficulty calibration.** [P+G] Both sources land on the same four core rep types: sentiment-triaging feedback collector, PII-redacting CSV uploader, mini-RAG over local Markdown, agentic dashboard. The briefs are nearly interchangeable. Gemini adds a fifth — local-file analysis via Claude Desktop with an MCP configuration, which directly leverages your existing skill stack. [Coach] Add Gemini's Rep 5 to the rotation; it's the rep that maps closest to your differentiation hook.

**Cap of 2 reps/week, 15:00-17:15 comms block, weeks 3-6.** [P+G] Both sources independently arrive at the same 4-week cadence with the same Track-C protection logic. This is consensus. The cadence is the right cadence.

**Working evaluator partner is required by Week 5.** [P+G] Both sources flag self-evaluation as insufficient past Week 4. The mock-partner sourcing channels diverge (see source-quality notes). [Coach] The named collaborators in your brief — Mary, Matt, Larry — are the right first ring before reaching outside it. Phase 4 will detail the ask.

---

## Cross-source disagreements (with verdicts)

**Disagreement 1 — Sierra format.** [G] says 45 min, 4-5 rounds, vibe-coding present, open tooling. [P] says 2-hour solo Build phase inside a Plan-Build-Review structure, and PM-format is not publicly verifiable. **Verdict: Perplexity, decisively.** Gemini cites Tolan's Relay (a related but distinct write-up about hiring engineers when AI writes code) and conflates it with the Sierra interview shape. Perplexity reads Sierra's own blog post. The Sierra row in Gemini's table is wrong; replace it.

**Disagreement 2 — Glean format.** [G] says 4 onsite rounds, vibe-coding present "in Outcome roles," 2-hour assessment. [P] says "multiple technical rounds, no confirmed vibe-coding live build — not publicly verifiable." **Verdict: Perplexity is more honest about evidence.** Gemini may be right that Glean Outcome / FDP roles include something resembling a live build, but the citation chain doesn't actually establish the rep shape or duration. Treat Glean's vibe-coding round as **partially confirmed** (consistent with the role family) but **format unverified**. If you progress with Glean, do warm-network outreach for the actual format.

**Disagreement 3 — The seventh rubric dimension.** [G] = Economic Awareness + Capital Constraint (compute, latency, token costs). [P] = User-Centered Decision Making (design choices justified in user-goal language, named success metrics). **Verdict: don't pick — keep both.** They're both real. They show up in the same evaluator moment: when you reject a $0.04/call vector DB for a $0/call regex on a 50-row CSV, you're being economically aware *and* user-centered (because the user's spec didn't justify the cost). Phase 2 fuses these into one dimension labeled "User & System Economics."

**Disagreement 4 — Number of failure modes.** [G] = 10. [P] = 9. Substantial overlap. **Verdict: union both.** Gemini contributes "context window exhaustion" and "hallucinated dependency acceptance" as load-bearing additions. Perplexity contributes "fighting the tool instead of pivoting" (with the specific 3-prompt-rule inoculation) and "no success metric at debrief" (the debrief-layer test). Phase 2 will carry the union (11 modes), filtered to Sean-relevant ones.

**Disagreement 5 — Working-state freeze cutoff.** [G] = minute 40. [P] = minute 35. **Verdict: Perplexity's minute-35.** [Coach] You over-narrate when nervous; you'll need the buffer. Minute 35 cutoff = 10 min for self-test, demo, and trade-off narration. This is the right cutoff for your weak-spot profile.

**Disagreement 6 — Mock-evaluator sourcing.** [G] = "The Product Group Boston" Slack. [P] = Sundai Club, AI Tinkerers Boston, Boston Python Meetup, Aakash Gupta's community, warm-network LinkedIn outreach to recent hires. **Verdict: Perplexity's options are richer and more specific.** Use Perplexity's list. [Coach] But the first ring is named in your context: Mary, Matt, Larry. Phase 4 sequences these — domestic ring first, Boston communities second, warm-network LinkedIn third.

**Disagreement 7 — Stripe and Netflix coverage.** [P] explicitly names Stripe and Netflix as Type-3 (take-home with prototype) per Aakash Gupta. [G] doesn't mention them. **Verdict: Perplexity gap-fills.** Hold this. Several Tier-2 stretch roles (Senior PM at small AI startup) will land in Type-3 format, not 45-min live, and you should not over-prep one shape.

**Disagreement 8 — Spec restatement framing.** [G] = "Spec Restatement and Alignment" using a fixed-phrase scaffold ("To ensure perfect alignment, the core deliverable is X..."). [P] = "Restate the brief in your own words" + a "will-build / won't-build" contract list. **Verdict: Perplexity, with one hold from Gemini.** The will/won't contract is the higher-leverage move. Gemini's fixed-phrase scaffold is brittle (sounds rehearsed). [Coach] Use Perplexity's framing in your own words; do **not** memorize Gemini's exact phrasing.

---

## Source-quality notes

**Perplexity is materially stronger on:**
- **Calibration of evidence.** Perplexity says "not publicly verifiable" repeatedly and means it; Gemini occasionally fills gaps with confident-sounding entries (Sierra row, Glean row) that don't survive citation pressure. For your prep, calibrated uncertainty is more useful than fluent confidence.
- **Granular tactical moves.** Perplexity's §5 has 5 numbered moves per phase (first-five, build cadence, last-ten). Gemini's §5 has 3 moves per phase. Perplexity's are more directly executable.
- **PM-product lens.** Perplexity's rubric leans more on user metrics, scope creep under pressure, no-success-metric failure mode at debrief — the layer that separates "engineer who can ship" from "PM who can ship and explain why."
- **Source citations.** Specific URLs with publish dates and accessed dates. Gemini's footnote chain is occasionally vague ("17 Aakash Gupta..." with no specific URL).

**Gemini is materially stronger on:**
- **Engineering-systems awareness.** Economic awareness as a discrete rubric dimension; context window exhaustion as a discrete failure mode; hallucinated dependency acceptance as a security-conscious flag. These are the dimensions that separate strong AI PMs from generic "PM who heard about AI." For your Anthropic FDE / Glean FDP wildcards specifically, hold these.
- **MCP-stack relevance.** Gemini's Rep 5 (local file analysis via Claude Desktop with an MCP configuration) is the only sample rep that maps to your `intent-engineering` MCP server stack. Perplexity didn't get there.
- **Portfolio-walkthrough role-tier mapping.** Gemini's §6 has explicit per-asset role-tier mapping ("Artifact 1 → AI APM / PM I-II; Artifact 2 → FDE/FDP; Artifact 3 → Senior PM stretch"). Perplexity has the same idea but less explicit. Use Gemini's mapping as the skeleton.

**Both sources are equally weak on:**
- Anything past Week 6. The cadence stops at the live partner-eval phase. Neither sources address pre-loop ritual, post-loop debrief, or energy management. Phase 4 fills this.
- Recovery scripts when the candidate freezes. Both name "panic-delete" as a failure mode but neither gives you the specific verbal moves to execute when you blank.
- The 2-year tenure asymmetry. Neither source addresses how to reframe titled tenure when portfolio signal is the actual differentiator.

---

## Gaps filled by Coach

Six gaps that neither source addresses but your situation requires:

**Gap 1 — Tenure asymmetry [Coach].** You have 2 years titled PM. You have 4-6 years portfolio signal. The reframe in interviews is never "in my X years of PM experience" — it's "in the work I've shipped." Behavioral stories will be framed around demonstrated artifacts (the 14-agent fleet, the financial-research fleet, the MCP server), not tenure milestones. This is a Phase 2 story-bank constraint, not a rubric dimension, but it's load-bearing — most candidates lose offers on this exact frame mismatch.

**Gap 2 — Track-C bandwidth math [Coach].** Both sources name "respect Track-C" but neither computes it. Your Track-C MCP build owns ~80% of deep-work hours through 2026-05-25. Practice reps eat 60-90 minutes of comms-block time twice a week starting Week 3. Total practice load = 120-180 min/wk in non-deep-work time. This fits. **But:** if you start practice reps before the MCP server ships, you're context-switching against 80% deep-work load. Recommendation: Reps don't start until Week 3 (per the canon) AND not before MCP server ships if MCP slips. Hold the line on Track-C.

**Gap 3 — Mary as domestic mock-evaluator [Coach].** Mary is a critical-path collaborator. The right ask is not "interview me" — that loads a partner-relationship dynamic that introduces signal noise. The right ask is "watch me build for 30 minutes and tell me three things you couldn't follow." This is a low-stakes way to get an external ear without the partner-evaluator dynamic. Phase 4 details the script.

**Gap 4 — MCP-stack live rep [Coach + G].** Gemini's Rep 5 is the seed. Your specific MCP server (`intent-engineering`, ships 2026-05-25) is a unique surface to demo against in a portfolio walkthrough variant of the live rep. For Anthropic FDE / Glean FDP loops specifically, you may be asked to extend or modify your own MCP server live. Practice: extend the MCP server with one new tool inside a 45-min window. Phase 2 details.

**Gap 5 — Recovery script for freeze [Coach].** When you blank under pressure, the move is not "try to think harder." The move is the verbal lifeline: "Let me restate where I am — I have X working, Y is in progress, the next prompt I want to try is Z. Does that match how you're seeing it?" This converts the freeze from a silence-blow-up into a decision-narration moment. Phase 2 lists this as one of the 5 recovery moves.

**Gap 6 — AI eval vocabulary anchor [Coach + P+G implied].** Both sources name F1 score as the canonical landmine. Neither gives you the actual list. The minimum vocab to pass the F1-score test for your portfolio: precision, recall, F1, accuracy, ROC-AUC, mean reciprocal rank (for retrieval), groundedness/faithfulness (for RAG), latency p50/p95/p99, token cost per call, context window, attention degradation, eval datasets, golden sets, regression tests. Memorize, with one concrete example each, mapped to a portfolio artifact. Phase 4 makes this a 10-min/day warm-keep drill.

---

## Provenance distribution at a glance

Approximate breakdown of what's in this synthesis:
- **[P+G]** consensus canon: ~55% of the load-bearing claims (verification depth, narration discipline, working-state freeze, spec restatement, 7-dim rubric trunk, sample-rep types, weekly-rep cap, F1-score landmine).
- **[P]** uniquely defensible: Sierra format, Stripe/Netflix Type-3, will/won't contract framing, evaluator-sourcing channels, no-success-metric failure mode.
- **[G]** uniquely defensible: economic-awareness dimension, context-window-exhaustion failure, hallucinated-dependency failure, MCP-aware Rep 5, role-tier × portfolio mapping skeleton.
- **[Coach]** gap-fills: tenure reframe, Track-C bandwidth math, Mary-as-domestic-mock framing, MCP-stack live rep adaptation, freeze recovery script, AI-eval vocabulary list.

---

## What changes the verdict

If any of these surface between now and Week 5, revisit the synthesis:
- A first-person candidate post-mortem from a PM who actually went through the Sierra PM loop (not the engineering loop).
- A primary source for Glean Outcome / FDP vibe-coding rep duration and shape.
- A first-person Anthropic FDE post-mortem (Boston/NYC/Chicago).
- A published Stripe or Netflix vibe-coding rubric.
- A primary source for Decagon's PM-vs-engineer interview format split.

Until those land, Perplexity-on-evidence-calibration + Gemini-on-engineering-systems-vocabulary + Coach-on-Sean-specific-gaps is the defensible canon.

---

## Phase 2 hand-off

Phase 2 (the executable playbook) inherits from this synthesis with four specific commitments:
1. The 7-dimension rubric uses 6 consensus dimensions + 1 fused "User & System Economics" dimension.
2. The 11 failure modes carry forward (10 from Gemini + 1 unique from Perplexity), filtered to the 5-7 that match Sean's named weak spots.
3. The first-five / last-five tactical playbook uses Perplexity's 5-move-per-phase granularity, with Gemini's preemptive defense narration as a Last-Five addition.
4. The portfolio-walkthrough §5 uses Gemini's role-tier × asset mapping skeleton, extended to all 7 of Sean's named artifacts, with the F1-score-vocabulary inoculation drilled into every artifact's expected-questions block.

Pause point: review this synthesis before Phase 2 begins.
