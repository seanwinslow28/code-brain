# M6 — AI Architecture as Systems: the Harness & Human-in-the-Loop Design (Lesson)

*Module 6 of 7 · Systems Thinking AI PM program · Week 3*
*Prerequisites: M1–M5. The architecture module — where the loops get bolted into software.*

## Why this module exists

In 2026 you don't ship a model; you ship a **harness** — the system wrapped around the model that plans, builds context, evaluates, and loops. Anthropic's revenue isn't the model API; it's the harness (Claude Code). Harvey isn't a legal model; it's a legal harness. The PM implication is total: your product's quality ceiling is set by harness design, not model choice, and harness design is loop design — which you now know how to do. This module also finally answers the question every case so far has raised: *where exactly do the humans go?*

## 1. The model → harness shift

A **model** knows things and can plan. A **harness** turns that into work: it (1) makes a plan for the task, (2) **builds context** — retrieving the right knowledge, memory, and constraints, (3) acts through tools, (4) **evaluates** whether the goal was met, and (5) loops until done or stopped. Harness quality = planning quality × context quality × eval quality — a *product* of factors, so a zero anywhere is a zero everywhere.

Judge any AI product by its harness, not its demo: What does it retrieve, and how does it know what's relevant? What does it check before declaring success? What makes it stop? Where does it put the human? Those four questions are a complete architecture review, and you can run them in any meeting.

## 2. Why learning loops break outside code — "there is no compiler for PRDs"

Coding harnesses work because code has *cheap, objective verification*: compile, test, run. The loop closes itself thousands of times a day. Now ask the harness to write a PRD: your manager calls it great, your skip-level calls it the worst they've seen. **No compiler.** Verification is expensive, subjective, and org-specific — so the learning loop that makes coding agents compound doesn't close, and out-of-the-box harnesses fake it.

This is the deepest strategic insight in the module: **wherever verification is cheap, AI compounds; wherever verification is expensive, AI plateaus** — and the PM's highest-leverage architectural act is *making verification cheaper* in their domain (rubrics, golden examples, structured formats, binary checks). That is what M7 industrializes.

Two more open wounds in current harnesses:
- **Long-horizon context decay.** Over long tasks, context accumulates irrelevance, contradictions, and poison; plan quality degrades with horizon length. Scope harness tasks to what context can hold honestly — long-horizon autonomy claims deserve your M1 skepticism about stocks (context is a stock; its quality drains).
- **RAG as a system, not a feature.** Retrieval-augmented generation bolts a retrieval loop onto generation. Its failure modes are systemic: incomplete or contradictory context in → confident falsehood out (Air Canada's exact mechanism, M5). RAG quality is retrieval quality, and retrieval quality is measurable — which makes it governable, if anyone measures it.

## 3. Multi-agent dynamics and the commons

Multi-agent systems reproduce classical economic failures at machine speed. The **tragedy of the commons** is live: generative agents extract from the shared data commons (the public internet) faster than humans replenish it, while flooding it with synthetic content that poisons future training (model collapse, M2) — a commons being over-grazed and polluted simultaneously. Simulations show LLM agents managing shared resources default to short-term exploitation unless explicitly framed toward collective outcomes — AI decision-makers fall into the same coordination traps as humans, without the embarrassment.

Inside your own fleet the same math applies at small scale: agents sharing a budget, a vault, a rate limit are agents sharing a commons. The governance moves are the classical ones — quotas (caps), reputation, and rules that make the individual agent's cheap move expensive for it rather than for the collective.

## 4. Human-in-the-loop as a designed loop (not a vibe)

"Add human oversight" is where rigor usually goes to die. Design it like the loop it is:

- **Insertion point:** humans go where consequence is high, reversal is hard, or model confidence is low — not everywhere (that's the verification tax unbounded, M3) and not nowhere (that's Zillow). For each action class, decide: autonomous / autonomous-with-audit / propose-then-approve / human-only.
- **Confidence thresholds:** the system routes *by uncertainty* — high-confidence flows through, low-confidence escalates. This requires the system to *have* calibrated confidence (epistemic honesty, M5), which is a buildable feature, not a hope.
- **Escalation UX is a product surface.** An escalation must arrive with context (what was attempted, what's uncertain, what happens on approve/reject), at the right person, at a sustainable rate. An escalation channel that cries wolf gets muted — and then you have Zillow with extra steps.
- **Reviewer drift and fatigue:** attention is a draining stock. By item 40, your reviewer is rubber-stamping — which converts "human oversight" into "human liability sponge." Counter-design: sampling instead of everything, injected known-bad items to measure reviewer catch-rate, rotation, and rate caps. **Measure the reviewers** (catch rate, reversal rate, time-per-item drift) or the HITL loop is decorative.
- **Escalation as success:** a loop that raises its hand at the right moment is *working*. Zillow's failure wasn't the model — it was executives deleting the raised hand from the architecture because velocity KPIs pointed the other way (M5's org loops, closing the circle).

## 5. Vocabulary, compressed

**Harness · planning × context × evals · context building · "no compiler for PRDs" · cheap vs expensive verification · long-horizon context decay · RAG as system · tragedy of the commons · agent governance (quotas/reputation/rules) · HITL insertion point · autonomy ladder · confidence-routed escalation · escalation UX · reviewer drift · liability sponge.**

## Exercise (prediction-first)

**Subject: your own agents-sdk fleet as a harness.**

1. **Predict (15 min, written):** Before diagramming — which of the four harness functions (planning / context / evals / stop-and-escalate) is weakest across your fleet? Which agent is most exposed to the "no compiler" problem (its output has no cheap verification)? State a falsifier.
2. **Diagram + design (60 min):** Draw the fleet as a harness: where each of the four functions lives (or doesn't) for 3 representative agents (e.g., vault_synthesizer, job_feed, daily_driver). Find the weakest loop. Then **design its HITL insertion**: the action class ladder, the confidence threshold, the escalation UX (what Sean sees, where, with what context), and the reviewer-drift counter-measure (even for a reviewer team of one).
3. **Calibrate:** Compare. Did the diagram contradict your prediction about the weakest function?

Submit all three parts.
