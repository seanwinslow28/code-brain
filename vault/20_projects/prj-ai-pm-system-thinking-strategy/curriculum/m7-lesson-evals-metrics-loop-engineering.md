# M7 — Evals, Metrics Architecture & Loop Engineering (Lesson · Capstone)

*Module 7 of 7 · Systems Thinking AI PM program · Week 3, final module*
*Prerequisites: everything. The capstone exercise is the first artifact of your Golden Loop build.*

## Why this module exists

Everything converges here. M6 ended on the deepest strategic point — AI compounds where verification is cheap — and this module is the discipline of *making* verification cheap: evals. The practitioner consensus of 2026 is blunt: unsuccessful AI products share one root cause, the failure to build evaluation systems, and once an AI feature is probabilistic, **the roadmap itself becomes an eval problem**. This is also where the curriculum stops being preparation: the exercise you'll do here is the opening move of your portfolio build.

## 1. Evals are the PM's job now

An **eval** is a repeatable measurement of whether your AI's output is *good, by your product's definition of good*. That definition — what dimensions matter, what failure costs, what "good enough to ship" means — is product judgment, not engineering. Delegate the plumbing, never the definition.

Without evals, quality control is outsourced to users — "and they don't file bug reports, they just leave" (silent failure, the discovery run's top pain). With evals, you get the compiler that PRD-land lacks: a cheap, repeatable verification signal that lets improvement loops actually close.

**Case anchor — Rechat's whack-a-mole.** A real-estate AI assistant whose every fixed failure mode spawned new ones; performance plateaued as surface area grew. The escape was not a better model — it was a systematic eval pipeline: log real failures, categorize them, convert them to test cases, measure every change against the set. "If you streamline your evaluation process, all other activities become easy." The plateau was a *missing balancing loop*, and evals were the loop.

## 2. The golden dataset: your quality ground truth

A **golden dataset** is a curated set of real inputs with reviewed definitions of correct output — trusted by someone with domain knowledge, built from *production failures* more than imagination, small first (50–100 cases beats a fantasy thousand), covering edge cases deliberately.

Treat it as a *versioned product*: every item has provenance, every schema and label change is tracked, flagged production traces flow in while failures are fresh. And split it — improvement set the loop can see, **holdout set it never sees**. The moment you optimize against your own grading set, scores rise while quality doesn't (Goodhart, once more). The holdout is the only honest referee you have.

## 3. Weak judges get gamed

"Rate this reply 1–10" is a weak eval — models learn to please it fast, and LLM self-evaluation fails exactly where it matters. Strong evals are **binary checks on specific facts**: *Does it restate the customer's request? Is the stated status true? Does it avoid promising anything off-roadmap? Under 120 words?* Score 0–5 by summing checks. Binary checks resist gaming because each one is falsifiable; a vague judge is a vibe with a number attached.

LLM-as-judge is legitimate *plumbing* for scale — but the judge needs its own eval (agreement with human labels on a sample), and epistemic humility about what it can't judge. Spot-check with your own eyes on every improvement cycle: trust the number, then verify three examples manually. Always.

## 4. Loop engineering: the anatomy

A prompt run ten times is a slot machine. A **loop** is an engineered system with nine parts — goal, context, actions, tools, **evals, memory, guardrails, escalation, stop condition** — and the last five are where amateurs and professionals separate. The stop condition is a trio: **target** (holdout average ≥ X), **budget** (max rounds / max dollars), **stall** (N rounds without improvement = done learning). Without evals, a loop is automated guessing; without a stop, it's a billing machine (M3).

**The champion/challenger pattern** — the loop you'll actually run:
1. Baseline the current prompt (champion) on the holdout set. Write the number down.
2. Each round, propose **exactly one change** (the challenger). One — so when the score moves, you know what moved it.
3. Test the challenger on the improvement set. If better, run the title fight on the *holdout*. Promote only if it beats the champion there. Ties go to the champion.
4. Log every round: change, both scores, decision, reason.
5. Stop on target, budget, or stall.

The round to internalize: a challenger adds three examples, improvement-set score jumps — and the holdout *drops*. The examples taught mimicry of the practice cases. Without the split you'd have shipped it, felt great, and degraded production. Most challengers lose; if every challenger wins, suspect the judge before praising the agent.

## 5. Metrics architecture: the full stack

Evals are one layer of a stack, and confusing layers is how teams lie to themselves:

- **Offline eval metrics** — golden-set scores, rubric passes. Cheap, fast, *simulations of reality*.
- **Online product metrics** — task completion, retention, edit rate, escalation rate. Reality, slow and noisy.
- **Guardrail metrics** — the Goodhart-pair (M5): latency, cost, complaint rate, refusal rate — the things that must *not* regress while you optimize the target.
- **Business metrics** — revenue, churn, support load. The reason anyone funds any of this.
- **Trust & safety metrics** — unsafe-output rate, hallucination-on-policy rate, reviewer catch rate (M6).

The **offline–online gap** is structural, not a bug: a 10% offline gain can produce zero online movement, and 95% on a curated set can be 70% in production, because real users leave the distribution the benchmark froze. Design for the gap: pick offline proxies *validated against* online outcomes, watch for **proxy decay** (drift applies to metrics too — a proxy that correlated last quarter may not now), and when labels are delayed or absent, monitor input distributions as your early-warning flow (M2). Then set **thresholds and stop-the-line criteria** (M5's rollback triggers, wired to this stack) so the metrics *do* something.

## 6. Diagnosis over delivery

The master-tutor stance that ties the whole curriculum: when quality disappoints, the amateur move is *deliver more* (new prompt, new model, new feature); the professional move is *diagnose exactly* — which failure mode, which loop, which layer of the stack, which structural cause (iceberg, M1). Bottom-up error analysis — read the actual failures, cluster them, attack the biggest cluster — beats top-down metric-chasing every time. Every module of this program has been teaching the same reflex at different altitudes: **find the structure before touching the system.**

## 7. Vocabulary, compressed

**Eval · golden dataset · provenance · improvement/holdout split · binary checks · weak judge · LLM-as-judge (with its own eval) · loop anatomy (goal/context/actions/tools/evals/memory/guardrails/escalation/stop) · target-budget-stall · champion/challenger · one-change rule · metrics stack (offline/online/guardrail/business/trust) · offline-online gap · proxy decay · stop-the-line · bottom-up error analysis · diagnosis over delivery.**

## Exercise (prediction-first) — THE C2 SEED

**Subject: your job-feed agent's relevance judgments.** This artifact carries directly into week 4 as the Golden Loop build's first dataset. Do it for real.

1. **Predict (15 min, written):** Before touching data — what's the job feed's dominant failure mode (irrelevant-included vs relevant-missed vs mis-tiered)? What holdout baseline score do you expect the current prompt to get (0–5 rubric)? State your falsifier.
2. **Build (90 min, spread over days if needed):**
   a. Pull 40 real job-feed items with your own verdicts — 25 improvement, **15 holdout**.
   b. Write a 5-check binary rubric for "good relevance judgment" (specific, falsifiable checks — no "rate 1–10").
   c. Baseline the current prompt on the holdout. Write the number down.
   d. Run **one** champion/challenger round: one change, improvement-set test, holdout title fight, log the round (change, scores, decision, reason).
3. **Calibrate + file:** Compare prediction to baseline and outcome. Write the decision record (M5 format) and file it in `product/decision-log.md`. This is Golden Loop's first entry — the build has begun.
