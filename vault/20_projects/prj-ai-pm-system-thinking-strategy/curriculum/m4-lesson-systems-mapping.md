# M4 — Causal Loop Diagramming & Systems Mapping + Archetype Pattern Library II (Lesson)

*Module 4 of 7 · Systems Thinking AI PM program · Week 2*
*Prerequisites: M1–M3. This is the practice-heavy module — the concepts are few, the reps matter.*

## Why this module exists

M1–M3 taught you to *recognize* loops someone else has drawn. This module makes you the one who draws them — because the diagram is not documentation, it's the diagnostic act itself. Teams that map a problem *discover loops they didn't know existed*; teams that skip to solutions intervene on the loop they happened to notice first. You'll also complete the archetype library and practice on two famous corpses.

## 1. CLD notation that actually matters

A causal loop diagram is variables connected by arrows with **polarity**:
- **Same-direction link (+ / "s")**: more A → more B (and less A → less B). More bad answers → more churn.
- **Opposite link (− / "o")**: more A → less B. More eval coverage → fewer shipped regressions.
- **Loop label:** count the opposite links in the loop. **Odd → balancing (B). Even (or zero) → reinforcing (R).** This is arithmetic, not judgment — label every loop.
- **Delay marks (∥)**: annotate every link where cause and visible effect are separated by meaningful time. In AI products the big delays are: retraining lag, user-habit lag, reputation lag, and *billing-cycle lag* (M3's routing trap lived in exactly that delay).

Naming discipline: variables must be *quantities that can rise or fall* ("user trust," "eval coverage," "support ticket rate") — never actions or judgments ("fix the model," "bad UX"). If you can't say "more of it" and "less of it," it's not a variable.

## 2. Stock-and-flow, when CLDs aren't enough

CLDs show structure; stock-and-flow models show *magnitude and timing*. Promote a CLD to stock-and-flow when the question is "how fast / how much / when": budget burn (M3), labeled-data accumulation, trust depletion. Rule of thumb: stocks are what you'd report at a board meeting (cash, users, dataset size, trust); flows are what your team actually changes day to day. Simulating even crudely — a spreadsheet stepping weeks — reveals overshoot and oscillation that a static diagram hides.

## 3. Boundary setting: the map's most political line

Every map has a boundary: what's inside (you model it) and outside (you treat it as given). Two failure modes:
- **Too narrow** — Unity's boundary excluded its own developer ecosystem's feedback loops (see §5): the pricing model was modeled in a vacuum, the retaliation was not.
- **Too wide** — a map of everything persuades no one and predicts nothing.

The craft: draw the boundary where *your decisions* stop having dominant influence, then explicitly list the exogenous forces just outside it (regulation, model-provider pricing, competitor moves) with the question "what if this shifts?" attached. Boundary-setting is also stakeholder work: whoever's incentives you leave off the map will surprise you from off the map.

## 4. The stakeholder-incentive CLD

Technical maps stop at the technical system; half the leverage points are organizational. A stakeholder-incentive CLD puts *people and their rewards* in the loops: whose KPI improves when the metric moves, who bears the cost of the fix, who can veto it. The OpenAI board crisis (M1) was exactly this — a structure where two groups' incentives formed opposing loops. When your drift fix keeps not getting resourced, draw the org: the blocking loop is usually somebody's bonus.

## 5. Archetype pattern library, part II — with corpses

**Success to the successful.** Winner-take-more reinforcing loop: initial advantage → more resources → bigger advantage. AI version: the data flywheel at market scale — dominant platforms get the data, the talent, and the defaults, and their models' encoded values become everyone's defaults. Recognize it inside companies too: the team with last quarter's wins gets this quarter's headcount.

**Limits to growth.** A reinforcing engine hits a balancing constraint — growth stalls, and pushing the engine harder makes the stall worse. AI's 2024–26 version: model scaling hitting the ceilings of high-quality human data and energy; the "fix" (synthetic training data) triggered its own fixes-that-fail loop via model collapse (M2). When growth flattens, the question is never "how do we push harder" but "which constraint did we hit, and does the constraint move?"

**Case anchor — Knight Capital (2012, still the canonical warning).** A reactivated piece of legacy code flooded the market with errant trades: $440M gone in 45 minutes. The systemic reading: a fully automated reinforcing loop with **no runtime awareness** — the system had no mechanism to recognize its own catastrophic behavior, and the humans had no kill switch that worked. Map it: where's the balancing loop that should have existed? (There isn't one. That's the lesson.) Every autonomous AI deployment inherits this architecture question: *what closes the loop between "the system is acting" and "the system is acting wrong"?*

**Case anchor — Unity (2023).** Unprofitable despite dominance, Unity imposed a fee-per-install model — a parameter-level fix (M1: shallow leverage) modeled inside too narrow a boundary. The developer ecosystem's response loops — trust collapse, mass migration to Godot, public revolt — forced full retreat. Map it: the missing variables were *accumulated trust* (a stock, drained in days after years of filling) and *switching momentum* (reinforcing: each studio that left made leaving safer). A pricing model is never just a number; it's an intervention in an ecosystem of loops.

## 6. Vocabulary, compressed

**Link polarity (same/opposite) · odd-negative rule · delay mark · variable naming discipline · stock-and-flow promotion · boundary setting · exogenous variable · stakeholder-incentive CLD · success to the successful · limits to growth · runtime awareness · kill switch.**

## Exercise (prediction-first, three drills, decreasing scaffolding)

**Drill 1 (scaffolded) — Unity re-map.** Predict first: write the three loops you expect drove the disaster. Then map it with the case in front of you: pricing decision, developer trust (stock), migration loop, retreat. Compare.

**Drill 2 (half-scaffolded) — the portfolio-grade artifact.** Full systems map of the Code-Brain fleet: agents as flows acting on vault stocks, cost caps as B-loops, the knowledge loop (flush → synthesizer → critic → lint) as an R-loop, **plus the stakeholder-incentive layer** (you, recruiters reading the public repo, the job hunt's calendar pressure). Predict first: which single loop, if it broke, would degrade the whole system fastest? This map becomes a portfolio artifact — draw it clean.

**Drill 3 (cold) — this week's news.** Pick any AI product story from the last 30 days. No scaffold: 30 minutes, map it, name the archetype if one fits, state the leverage point the actors are missing. This is the week-6 judgment gate's dress rehearsal.

Submit all three with predictions attached.
