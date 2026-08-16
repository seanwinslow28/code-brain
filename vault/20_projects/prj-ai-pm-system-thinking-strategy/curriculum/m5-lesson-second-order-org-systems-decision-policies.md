# M5 — Second-Order Effects, Organizational Systems & Decision Policies (Lesson)

*Module 5 of 7 · Systems Thinking AI PM program · Week 3*
*Prerequisites: M1–M4. This is the judgment module: diagnosis becomes disposition.*

## Why this module exists

The first four modules made you a diagnostician. This one makes you dangerous in a meeting. Three upgrades: thinking past the first-order effect (where AI product disasters live), reading the *organization* as a system (where fixes go to die), and converting analysis into **decision policies** — because diagnosis without disposition is academic, and shipping PMs dispose.

## 1. Second- and third-order effects

First-order: what the change does. Second-order: what the system does in response. Third-order: what the *ecosystem* does in response to that. The discipline is mechanical — for any proposed change, write the chain before shipping:

*We retrain to maximize clicks* → model surfaces sensationalist content (2nd) → advertisers pull spend, trust collapses (3rd). *We route easy queries to a cheap model* → bill drops (1st) → quality drains silently (2nd) → churn shows up in a different quarter's dashboard (3rd). Every 2nd-order effect in these chains is a loop you could have drawn in M4 — the orders are just the loop unrolled in time.

**Goodhart's law is the recurring 2nd-order engine:** any measure that becomes a target stops measuring. You met it at gradient speed (reward hacking, M2) and at judge level (weak evals, M7). Here it's organizational: teams optimize the KPI, the KPI decouples from the goal, leadership doubles down on the KPI. When you set a metric, simultaneously ask *"how will this be gamed, and what guardrail metric detects that?"* — that pairing habit is the entire defense.

**Epistemic vs aleatoric uncertainty — the liability frontier.** Aleatoric: the world is noisy (the model is *wrong* sometimes, measurably). Epistemic: the model *doesn't know what it doesn't know* — and generates confident, plausible falsehood instead of admitting ignorance. Standard testing catches the first; only deliberate design (grounding, refusal behavior, confidence surfacing) addresses the second. **Case anchor — Air Canada:** its chatbot invented a bereavement-fare policy; a tribunal ruled the airline fully liable, rejecting the argument that the chatbot was "a separate legal entity." NYC's MyCity bot confidently advised small businesses to break labor law. No error codes fired in either. The 2nd-order chain PMs must pre-write: hallucination → user acts on it → *the company is legally bound by it*. Terms-of-service disclaimers do not survive contact with a judge.

**Two slow-burn 2nd-order risks worth naming:**
- **Model monoculture.** When your product, your competitors, and your vendors all sit on the same two foundation models, any bias, outage, or repricing hits everyone *simultaneously* — correlated failure at industry scale. Diversification has a cost; correlated collapse has a bigger one. Know which bet you're making.
- **Cognitive offloading.** Teams that use AI purely for speed lose the ability to reason without it — junior output rises while the review/rework loop degrades and deep understanding atrophies. You are personally running this risk in this program: it's why every exercise demands *your* prediction before AI critique.

## 2. The organization as a system

Meadows' deepest leverage points — goals, paradigms — are *organizational* objects. The org chart is a loop diagram wearing a suit: budgets are flows, headcount is a stock, incentives are link polarities, and the resourcing meeting is where loops collide.

Why good fixes die: the diagnostician maps the technical system, finds the structural fix, and loses — because the fix's *cost* lands in one team's budget while its *benefit* lands in another's KPI. Nobody in the room is against it; the structure is. The counter-move is the stakeholder-incentive CLD from M4: before proposing, map who pays, who gains, who decides, and *what loop each of them is inside*. Then re-shape the proposal so at least one powerful loop points the same direction as the fix — that's what "winning the meeting" means structurally, and it's the difference between "a brilliant diagnostician" and an effective agent of change.

The mental-model layer is real leverage: "shipping fast beats infrastructure" is a paradigm, and while paradigms are the hardest thing to shift, a *named* paradigm loses much of its silent power. Naming the belief in the room — "we're acting like the eval system is overhead rather than the product" — is itself an intervention.

## 3. Pre-mortems, done systemically

A pre-mortem assumes the project *has already failed* and asks why. The systems upgrade: don't brainstorm failure *events* — locate failure *loops*. For each: which reinforcing loop ran away, which balancing loop was missing, which delay hid the signal, which stakeholder's incentive fed it. Then check the classic archetype shelf (M2, M4) — most failures you can imagine are one of five patterns with your product's name pasted in. A pre-mortem that produces "risks" is a list; one that produces *structures* tells you which single intervention removes three risks at once.

## 4. Decision policies: kill criteria, thresholds, and the written record

Analysis becomes a decision policy when it's written down *before* the emotion arrives:

- **Ship/no-ship thresholds:** the eval bar, the latency budget, the cost ceiling — numeric, agreed, and set *before* the demo dazzles everyone.
- **Kill criteria:** the conditions under which this feature/product dies, written at kickoff when nobody's identity is invested yet. "We kill it if verified-good-output cost stays above $X after two improvement cycles." A bet without a kill criterion is not a bet; it's a future sunk-cost argument.
- **Rollback triggers:** launch-time automation — *if guardrail metric Y regresses past Z for W minutes, revert without a meeting.* The meeting is where rollbacks go to die while the incident compounds.
- **The written decision record:** for every significant call — the decision, the alternatives considered, the expected mechanism, the falsifier, the review date. Ten minutes of writing buys three things: calibration (you can check your prediction later), institutional memory (the next PM inherits reasoning, not folklore), and honesty (a record you'd be embarrassed to re-read is a decision you shouldn't be making). Your Phase 2 build's decision log is exactly this practice in public.

## 5. Vocabulary, compressed

**Second-/third-order effects · Goodhart's law · guardrail metric pairing · epistemic vs aleatoric uncertainty · liability chain · model monoculture · cognitive offloading · stakeholder-incentive mapping · paradigm naming · failure loops (vs failure events) · ship/no-ship threshold · kill criterion · rollback trigger · decision record.**

## Exercise (prediction-first)

**Subject: a real upcoming change** — recommended: "Phase 2 begins — the Golden Loop build replaces curriculum-first time allocation in week 4," or pick any live fleet/portfolio change with real stakes.

1. **Predict (15 min, written):** Name the single most likely failure *loop* (not event), the stakeholder whose incentive structure most threatens the change, and your falsifier.
2. **Pre-mortem (60 min):** It's week 8 and the change failed. Write the systemic post-mortem: the runaway or missing loop, the delay that hid it, the archetype if one fits, the org loop that fed it. Then produce the *disposition package*: ship/no-ship threshold for proceeding, one kill criterion, one rollback trigger, and a decision record for the choice you'd make today.
3. **Calibrate:** Compare prediction to pre-mortem. File the decision record in `product/decision-log.md` — it's the log's first real entry.

Submit all three parts.
