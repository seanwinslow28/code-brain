# M1 — Systems Thinking Foundations (Lesson)

*Module 1 of 7 · Systems Thinking AI PM program · Sean Winslow · Week 1*
*This lesson is the module's spine. The audio overview, quiz, and flashcards are generated from it plus the curated M1 sources.*

## Why this module exists

Every AI product failure you will study in this program — Zillow's $881M write-down, Air Canada's chatbot liability, Knight Capital's 45-minute collapse — was diagnosed *after the fact* using the concepts in this module. The PMs involved weren't stupid; they were looking at events when the cause lived three layers down. This module gives you the x-ray: four core ideas (stocks and flows, feedback loops, delays, leverage points) and one diagnostic tool (the iceberg model). Everything in M2–M7 is these ideas wearing AI-specific clothing.

## 1. Systems, stocks, and flows

A **system** is a set of parts that interact to produce behavior none of the parts has alone. A thermostat plus furnace plus room is a system; so is a recommendation model plus its users plus the content pool.

A **stock** is anything that accumulates and can be measured at a moment in time: money in an account, labeled examples in a training set, user trust, your own energy. A **flow** is the rate that fills or drains a stock: revenue per month, new labels per week, trust gained per good answer, trust lost per hallucination.

The PM move: when a metric moves, ask *which stock changed, and which flow changed it?* "Engagement dropped" is an event. "The stock of user trust has been draining for six weeks because the flow of bad answers exceeded the flow of good ones" is a diagnosis.

Two things about stocks that trip everyone up:
- **Stocks change slowly.** You can cut the bad-answer flow to zero today and trust will still be low tomorrow. Stocks are why fixes feel like they "aren't working."
- **Stocks buffer and hide.** A big stock of trust absorbs a lot of bad answers before anything visible happens — which is why problems seem to appear "suddenly." They didn't. The stock finally ran out.

## 2. Feedback loops: the engine of system behavior

A **feedback loop** exists when a stock's level influences its own flows. Two kinds, and only two:

**Reinforcing loops (R)** amplify. More begets more; less begets less. The AI data flywheel is the canonical one: more users → more data → better model → more users. Reinforcing loops produce exponential growth — and exponential collapse. The same flywheel that grew the product spins backward when quality dips: fewer users → less data → staler model → fewer users.

**Balancing loops (B)** stabilize. They push a stock toward some target and resist change in either direction. A cost cap is a balancing loop. So is user fatigue: the more aggressively you optimize recommendations, the faster users burn out, which caps engagement no matter how good the model gets.

Every system's behavior is the arithmetic of its loops. Growth that flattens = a reinforcing loop hitting a balancing one. Oscillation = a balancing loop with a delay. Collapse = a reinforcing loop running in reverse. When you see a behavior pattern, your first question is: *which loops produce this shape?*

## 3. Delays: where intuition goes to die

A **delay** is the lag between a flow changing and its effect appearing. Retraining lag, user-habit lag, quarterly-review lag, reputation lag.

Delays are the single biggest reason smart people mismanage systems. With a delay in the loop, the feedback you're reacting to is *old news*. You push harder because nothing seems to be happening, then the accumulated effect arrives all at once and you overshoot — so you slam the other direction and oscillate. (This is Knight Capital's 45 minutes and every "we shipped the fix, why is churn still rising?" meeting you've ever sat in.)

The PM move: for every loop you draw, annotate the delay. *How long between cause and visible effect?* If the delay is longer than your decision cadence, you cannot steer by the metric — you need a leading indicator (a flow measure) instead of the lagging stock.

## 4. Leverage points: where to push

Donella Meadows ranked the places you can intervene in a system, from shallow to deep:

- **Parameters** (shallowest): tweak numbers — thresholds, weights, prices, prompt wording. Easy, visible, and usually washed out by the loops around them.
- **Buffers and stocks**: change the size of accumulations — bigger eval set, larger cash reserve.
- **Feedback loops**: change loop strength or delay — faster retraining, real-time monitoring instead of weekly reports, adding a missing balancing loop (a cost cap, a quality gate).
- **Information flows**: change *who sees what, when* — a dashboard that surfaces drift to the people who can act on it is a deeper intervention than the model tweak it prompts.
- **Rules and incentives**: change what's rewarded — the reward function, the team's KPI, the pricing model.
- **Goals**: change what the system is *for* — optimizing long-term retention vs. short-term clicks rewires every loop below it.
- **Paradigm** (deepest): change the shared belief the system runs on — "shipping fast beats infrastructure" vs. "the eval system is the product."

The uncomfortable rule of thumb: **effort and leverage are inversely correlated with popularity.** Teams love parameter tweaks (low conflict, fast, measurable) and avoid goal/paradigm interventions (high conflict, slow, transformative). When your fix keeps not sticking, you are almost always intervening too shallow.

## 5. The iceberg: your diagnostic ladder

Four layers, descending:

1. **Events** — what just happened. "The chatbot told a customer a fake policy."
2. **Patterns** — what keeps happening. "Hallucinations spike on policy questions every time content ships faster than retrieval reindexing."
3. **Structures** — what produces the pattern. "Content and ML teams ship on independent schedules; nothing couples them; no eval gates policy answers."
4. **Mental models** — what beliefs built those structures. "Legal reviews human answers; the bot is 'just software,' so it doesn't need that."

React at the event layer and the problem returns, because you left the structure that generates it intact. The working diagnostic sequence: *name the event → find the pattern it belongs to → find the structure producing the pattern → name the belief that built the structure.* Interventions aimed at layers 3–4 are the ones that stick — and they are exactly the leverage points from section 4.

**Worked case — the OpenAI board crisis (Nov 2023).** Event: CEO fired Friday, rehired the next week. Pattern: months of accelerating commercialization diverging from the nonprofit research mission. Structure: a capped-profit company governed by a nonprofit board — two legal architectures with incompatible objectives welded together. Mental models: "safe AI requires slow, non-commercial development" versus "beneficial AI requires massive capital and market speed." No board reshuffle (an event-layer fix) could resolve a mental-model conflict; the structure had to change, and did.

## 6. The M1 vocabulary, compressed

**System · stock · flow · reinforcing loop · balancing loop · delay · leverage point (parameters → buffers → loops → information → rules → goals → paradigm) · iceberg (events → patterns → structures → mental models).**

If you can use these fourteen terms accurately about *your own* products, unprompted, M1 has done its job. Fluency test at week 3; judgment test at week 6.

## Exercise (prediction-first — do not skip the prediction)

**Subject: the April 2026 Code-Brain fleet downsizing** — 8 of 10 autonomous agents were disabled after an audit found only 2 producing value.

1. **Predict first, in writing (15 min, before any digging):** What structure produced a fleet where 80% of agents ran without producing value? Name the mechanism (which loops existed, which were missing), your falsifier (what evidence would prove you wrong), and one expected side-effect of the fix that was chosen.
2. **Then diagnose (45–60 min):** Read the audit (`agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`). Build the full iceberg: event → pattern → structure → mental model. Identify which balancing loop was missing before the audit, and which leverage-point level the audit itself operated at.
3. **Calibrate:** Compare your prediction to your diagnosis. Where were you wrong, and which concept would have caught it?

Submit all three parts. Claude reviews the *calibration*, not just the diagnosis.
