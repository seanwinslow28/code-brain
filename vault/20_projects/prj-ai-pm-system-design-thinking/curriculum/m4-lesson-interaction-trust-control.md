---
title: "M4 — Interaction, Trust & Control"
type: lesson
module: M4
status: ready
created: 2026-08-22
anchor: Intercom Fin — the published outcome taxonomy
backup_anchor: GitHub Copilot accept/reject
mirror_eligibility: "no — teach from zero; a single-operator fleet never forced a trust surface"
---

# M4 — Interaction, Trust & Control

*Module 4 of 5 · AI PM System Design Thinking · Weeks 6–7*

---

## 0. This is the module your fleet never made you build

M3 was mostly recognition. This one is mostly new, and I'd rather say that plainly than hunt for things to flatter you about.

The structural reason: your twelve agents run in a world with **exactly one human in it, and that human is you.** You wrote the code, you know what `wol-deferred` means, you know which manifest to read when something looks off, and you can tell in a second whether an output is garbage. **You are not a user. You are the operator with ground truth.** Every hard problem in this module — how does a stranger know whether to believe this, what happens to them when it's wrong, how do they get out — was pre-solved for you by the fact that you already knew the answer.

**Three things transfer, and they're worth naming precisely because they're narrow:**

1. **You designed one real uncertainty surface for strangers.** Your portfolio's daily-dated layer falls back to evergreen copy when the fleet data is stale or the render fails, rather than showing a fabricated number. That is *honesty-preserving degradation* — a decision about what a stranger is told when the system doesn't know.
2. **You built abstention — for machines.** The discovery council drops any pain point not traceable to a real fetched URL. Refusing to answer rather than answering badly is the most underused uncertainty primitive in AI products, and you built it into a pipeline and never into an interface.
3. **You have been the victim of an uncalibrated system.** The local research run that produced fabricated entities and fabricated Microsoft URLs — the one you kept as a specimen rather than deleting. You know from the inside what a confidently-wrong system costs, and how little the confidence had to do with correctness.

**What you have never done, and what this teaches from zero:** designed for a person who cannot check the answer · decided what a system says when it doesn't know, to someone who isn't you · designed a handoff to another human, including what context travels with it · put a reviewer in a loop and then thought about that reviewer in month four · tested an interaction *before* building the system behind it · asked who is affected by a system and never touches it.

**One trap to disarm first.** The instinct is "make users trust it more." That's the wrong goal, and saying it that way in a room is a tell. The goal is **calibration** — trust that tracks actual reliability, case by case. A user who trusts a 60%-reliable feature 60% of the time is a success. One who trusts it 100% of the time is an incident waiting to happen; one who trusts it 0% is a feature nobody uses that you still pay inference on.

---

## 1. Five relationships, not one interface

"The interface" is no longer one thing. An April 2025 essay by Ryan Wilson, a design leader, published as a guest post on Nate B Jones' newsletter (Jones is a product writer you already read), makes one structural move worth stealing: design **five distinct relationships**, each with its own mode, levers, failure modes and metrics.

*(Provenance: tier C — a practitioner blog post, ChatGPT-assisted by the authors' own disclosure, coining two terms nobody else uses. **Take the grid, leave the coinage.** Never say "Reflexive Intelligence" in an interview.)*

| Pairing | Primary mode | Design levers | Failure modes | Metrics |
|---|---|---|---|---|
| **Human ↔ Software** | Command → execute | Clarity, hierarchy, feedback, affordances | Friction, error cascades, abandonment | Efficiency, usability, completion rate |
| **Human ↔ LLM** | Prompt → generative response; iterative, dialogic | Prompt scaffolding, grounding, memory calibration (session vs. persistent) | Hallucination, false agreement, "yes-man" behaviour, drift from intent | Relevance, alignment, trust, successful co-creation |
| **Human ↔ Agent** | Ongoing negotiation of goals and roles; the agent adapts over time | Memory, consent protocols ("should I do this for you next time?"), autonomy tuning — boundaries, pause, override | Overstepping, dependency, goal drift, **erosion of trust through invisible behaviour** | Longitudinal — see below |
| **Agent ↔ Agent** | Negotiation and delegation between systems | Protocols (who speaks first, how consensus is reached), role definitions, trust graphs, permission models, conflict resolution | Infinite loops, conflicting goals, over-coordination, unintended escalation | Task success, cycle count, deadlocks avoided |
| **Agent ↔ Software** | Execution — invoking APIs, filling forms, triggering workflows | Observability (logs, status codes, progress), permission scoping, delegation affordances | **Silent failures**, tool misuse, cascading errors, conflicting state between agent and software | Execution fidelity, speed, observability coverage |

**Look at where your fleet lives.** Rows four and five — which have *no human in them at all.* That is the whole explanation for why eighteen months of production experience left this module untouched.

**The one genuinely new idea in the essay:** Human↔Agent success can't be measured like the first two rows. Task completion is a single-episode metric; a relationship with an agent is measured over its lifespan. Three metrics, all longitudinal:

- **Relational trust** — does it follow through, respect stated boundaries, recover well when wrong?
- **Behavioural alignment** — is it getting better at helping *this* person specifically, over time?
- **Friction recovery** — when it goes wrong, how fast does the pair get back on track?

Say this in a room and you separate yourself from everyone reporting accuracy: *"task completion tells me about the episode; friction recovery tells me about the relationship."*

---

## 2. Trust is a dial you calibrate, not a number you maximise

Google's PAIR team — People + AI Research, which publishes Google's practitioner guidance on human-AI design — defines it usefully:

> **Trust is the willingness to take a risk based on the expectation of a benefit.**

Three ingredients, and they fail differently. **Ability** — can it do the job? **Reliability** — does it do it *consistently*, at the level you led the user to expect? **Benevolence** — does the user believe you're on their side? Teams skip the third, and it's exactly where "assumed resolution" (§5) will bite.

Both directions of miscalibration cost real money:

- **Overtrust** (*automation bias*, *complacency*): the user accepts output they should have checked. The reviewer rubber-stamps. Nobody notices until it's external.
- **Undertrust** (*algorithm aversion*): people are suspicious, redo the work by hand, or route around the system. You pay inference for output nobody uses, and adoption metrics tell you nothing about quality.

**The connection back to M1, and it's the sentence to remember:**

> Model calibration is a property of the number. Trust calibration is a property of the person. **You can ship a perfectly calibrated model and still produce badly calibrated users**, because the interface rendered every answer in the same confident prose.

That is the failure mode of every chat interface built since 2023 — including the one that fabricated `PureMCPClient` for you in the same tone it used for real libraries.

---

## 3. Communicating uncertainty — and what the evidence actually says

The obvious move is to show a confidence score. The evidence is more interesting than either camp claims.

**The study.** In 2020 three IBM researchers — Yunfeng Zhang, Q. Vera Liao and Rachel Bellamy — ran a controlled experiment published at FAT\*, the ACM conference on Fairness, Accountability and Transparency. People predicted income levels alongside an AI that was right about 75% of the time; unaided humans scored 63–65%. The experiment varied whether per-case confidence was shown, and separately whether a local explanation — which features drove *this* prediction — was shown.

1. **Showing confidence did calibrate trust.** Below 60% confidence people trusted the AI less; above 80%, significantly more. Statistically significant interaction. The number moved trust in the right direction.
2. **Better-calibrated trust did not produce better decisions.** Joint accuracy didn't improve — their explanation being that there wasn't enough *complementary knowledge*. The humans didn't know things the model didn't, so knowing when to distrust it bought nothing.
3. **Local explanations did nothing measurable**, for calibration or accuracy, in this task.

**The PM lesson is not "show confidence" or "hide confidence":**

> Displaying uncertainty pays off only when the person **can do something with it that the model can't do for itself.** With no complementary knowledge and no alternative action, a confidence score is decoration that makes the screen look rigorous.

So the design question is: **what different action does this person take at 55% versus 85%?** If the answer is "nothing," don't show it. If it's "at 55% they open the source document," design *that* — the number is only the trigger.

**PAIR's four representations:**

| Form | What it is | When it works |
|---|---|---|
| **Categorical** | High / Medium / Low buckets | When each bucket maps to a *stated user action*. Best default |
| **N-best** | Show top alternatives instead of a score | Strong in low-confidence cases — hands judgment back and teaches your system's mental model |
| **Numeric** | "87% confident" | Risky. Presumes probability literacy, and invites "what do I do differently at 85.8% versus 87%?" |
| **Data-viz** | Error bars, shaded ranges | Forecasts and continuous quantities |

PAIR's two reasons **not** to show it: when the level changes no decision, and when a misleadingly high number will produce blind acceptance from less-savvy users.

**Four alternatives to a number, all underused:** **abstention** (say you don't know — you built this for machines) · **show the evidence, not the score** (per-claim citations that resolve; the user calibrates on something they can actually judge) · **hedged language, deliberately specified** — PAIR cites a music recommender whose entire uncertainty surface is *"we think you'll like"* · **uncertainty as behaviour** — ask a clarifying question instead of guessing, which is Amershi's G10 and the most PM-specifiable uncertainty move there is.

---

## 4. Failure UX: a product surface, not an exception path

AI fails. That is a permanent property, not a defect to be minimised out of existence, and what happens after the failure has the same standing as the happy path. PAIR's framing: **the trick isn't to avoid failure, it's to find it and make it as user-centred as the rest of the product.**

**The taxonomy, organised by *who notices* — which is the insight.**

**Errors the user perceives:**

- **Context errors.** The system works exactly as intended and the user still experiences a failure, because the behaviour broke their mental model, wasn't explained, or rested on a wrong assumption about what they wanted. Often **true positives**. A friend's flight confirmation arrives and the calendar helpfully creates the event. Nothing is broken. It's still wrong.
- **Failstates.** The system can't produce an answer and correctly says so — often a **true negative**. The plant identifier is shown an animal that wasn't in its training data. The system is right; the user is stuck.

**Errors the user does not perceive:**

- **Happy accidents.** The system flags its own output as poor; the user finds it useful anyway.
- **Background errors** — *the dangerous one.* The system is wrong and **neither the user nor the system registers it.** A search engine returns a wrong result the user can't identify as wrong. No error fires, no thumbs-down arrives, no ticket is filed, and your dashboards look excellent.

> **Background errors generate no feedback signal, so you cannot find them through feedback channels. They require a dedicated QA process.** That is the bridge into M5: sampling for human review exists because the errors that matter most are invisible to every metric you'd naturally build.

**The risk gauge.** The same error carries different risk by moment. *Higher risk:* the user is a novice at the task · reduced attention or time pressure · low system confidence · a narrow definition of success. *Higher stakes:* health, safety, financial decisions · sensitive social contexts. Risk and stakes are independent axes — a low-stakes system used by a distracted novice still fails badly.

**Three paths forward:**

1. **Create opportunities for feedback** — including alongside *correct* output, or you only ever sample your failures. Repeated rejections are themselves a signal to ask.
2. **Return control to the user** — usually cheapest, with a requirement most teams miss: they must arrive holding everything needed to take over. What the system already did, what it was about to do, what it knows. A handoff into a blank state is a failure with extra steps.
3. **Assume subversive use.** Make failure **safe, boring, unremarkable** — never interesting. And don't over-explain it: PAIR's example is a spam filter that explains why a message *wasn't* caught, which is a tutorial for spammers. M3's security section wearing a UX hat.

**The structural link back to M3:** a mature system names every way a run can end — your `RouteUnavailable`, `partial`, `wol-deferred`, `rejected_reasons`. **Every internal stop reason needs a user-facing counterpart:** what the person is told, what they can do next, what the system does on their behalf, what gets logged. Building that mapping table *is* the failure-UX spec, and it's this module's artifact.

---

## 5. The anchor: Intercom Fin, and a taxonomy with a price attached

**Setup, assuming no familiarity.** Intercom is a customer-support software company; its product is the messenger and inbox companies use to answer customer questions. **Fin** is Intercom's AI support agent: it answers incoming questions automatically and hands off to a human when it shouldn't. Fin is one of very few AI products whose full outcome taxonomy is public — and it's public because Intercom **bills on it.**

| Outcome | Billable | Definition (Intercom's own wording) |
|---|---|---|
| **Resolution** | $0.99 | "No further help is requested after the last AI answer" — *confirmed* ("ok thanks") or **assumed** (the customer leaves without asking again) |
| **Procedure Handoff** | $0.99 | Fin executes a procedure *you configured* that ends in handoff to a human or workflow |
| **Disqualification** | $0.99 | Fin decides a sales prospect doesn't match your criteria |
| **Qualification** | $9.99 | Fin matches a prospect to your criteria and routes them |
| **Escalation** | not billed | Handoff from *default behaviour or workspace rules* — the customer asks for a human, or shows frustration |
| **Abandoned** | not billed | The customer leaves without Fin answering, or the conversation times out |
| **Spam** | not billed | Routed to the spam view |
| **Pending** | not billed | Fin sent an outbound message, the customer opened it, no reply |

**Four takeaways, each labelled, because you're being trained to label.**

**One — observed.** This is a **stop-reason taxonomy pointed at customers instead of at logs**: eight named endings, each with a defined trigger. Most AI products in the market distinguish "answered" from "errored" and nothing else.

**Two — observed, and the most instructive line in the module.** *Resolution* includes **assumed resolution**: the customer stops replying, it counts as resolved, and it bills. The vendor defines the success metric, and silence scores as success.

**Three — inferred, and say "inferred" out loud when you say it.** A customer who gives up in frustration and closes the tab is indistinguishable in that taxonomy from one whose problem was solved. Opposite experiences, identical telemetry. That is a **measurement decision with revenue attached**, and it's the cleanest example in this curriculum of *why teams ship things that hurt people*: nobody had to act in bad faith. Someone chose the cheaper definition of "resolved" and the incentive gradient did the rest. Note too that a *configured* handoff bills while a *default* escalation doesn't — the pricing encodes a preference for designed handoffs over fallback ones. Reasonable. Also a thumb on the scale.

**Four — the caveat.** Competing vendors publish tests claiming real resolution rates well below Intercom's headline figures. Those are tier-D sources with obvious commercial interest and I'm not asking you to believe them. The transferable point needs no number: **when the seller defines the metric, read the definition before the figure.** In M5 you do this to your own product.

**The backup anchor.** GitHub Copilot — GitHub's AI coding assistant, which suggests code inline as you type — instruments a simpler surface: accept or don't. In 2024 a GitHub team led by Albert Ziegler published a study in *Communications of the ACM* finding that **acceptance rate predicted developers' perceived productivity better than other measures**, good enough for coarse-grained monitoring. Read that precisely, because the precision is the lesson: *perceived* productivity. Accepted code can still be wrong; a rejected suggestion may still have helped someone think. **Acceptance is the industry's most available interaction metric, and it is a proxy.** Knowing what a metric is a proxy *for* is most of the job.

---

## 6. Human-in-the-loop: where the human actually sits

"Human in the loop" is used as one thing. It's four, they cost differently, and choosing between them is a PM decision.

| Insertion point | What it is | Cost |
|---|---|---|
| **Pre-action approval** | Nothing happens until a human approves. Your PreToolUse hooks, aimed at a person | Highest latency; the only one that *prevents* harm rather than detecting it |
| **Post-hoc sampled review** | The system acts; humans review a sample afterwards | Cheap, scales, catches nothing in real time |
| **Exception routing** | Only low-confidence or policy-flagged cases reach a person | The workhorse. Volume is set by the threshold |
| **User-invoked escalation** | The end user asks for a human | Costs nothing until used, and is what users judge you on |

**Exception routing is where M1 comes back and bites.** The confidence threshold that decides what gets escalated *is* the size of the review queue. Move it two points to be safer and you may double daily volume; with forty reviewers, you have just designed a backlog. **The threshold is simultaneously a quality decision, a cost decision and a staffing decision — and in most orgs three different people own those and never meet.** Being the PM who says that out loud is the job.

**What happens to the reviewer, which nobody plans for:**

- **Automation bias in reviewers.** Show someone the model's answer and ask them to check it, and they agree more than they should. If you need independent judgment, don't show the model's answer first. Same anchoring problem as M2's labeling instructions, aimed at a different person.
- **Throughput pressure produces rubber-stamping.** Review time falls, agreement with the model rises, quality metrics look *better*. The corruption mode with the friendliest dashboard.
- **Reviewer drift.** Standards shift over months; nobody re-reads the guidelines.
- **It contaminates M2.** Your reviewers are usually also your label source, so a degraded review loop doesn't just miss errors — it *teaches the model its errors were fine.*

**Countermeasures — this list is the reviewer-integrity plan in your artifact:** plant known-answer gold cases and track accuracy on them · monitor override rate and review-time distributions, not just throughput · run periodic inter-rater agreement checks (M2's measure, aimed at your own staff) · rotate reviewers off the queue · re-anchor with scheduled calibration sessions · and treat a *rising* agreement rate as something to investigate, not celebrate.

**The ethnographic point underneath:** the reviewer is a user of your product for whom nobody has designed anything. They stare at your queue six hours a day. Bad tooling means bad data means a degrading model. **Design the review interface as a first-class surface.**

---

## 7. Wizard of Oz: test the relationship before you build the system

**Definition:** you build the interface and a human secretly performs the AI's job behind it. The user believes they're using a system; a person is typing. Decades old in HCI, named for the man behind the curtain.

Everything above — the confidence representation, the escalation copy, the failure paths, what transfers on handoff, whether the user even has complementary knowledge — is testable *before the model exists*, because you are testing an interaction, not a capability.

**Three payoffs, in order of how badly they're undervalued:** you learn whether the interaction works before spending a quarter on the system underneath · **the transcripts are training and evaluation data**, captured with a human doing the task correctly, which is M2's problem partly solved as a side effect · and writing instructions for the person behind the curtain forces you to specify behaviour precisely — **if you can't write instructions a person can follow, your spec was never a spec.**

The PM-sized version costs a morning: take twenty real requests, answer them by hand through the intended interface, and log where you hesitated, what you needed and didn't have, and what you'd have wanted to tell the user when you weren't sure.

---

## 8. Amershi's 18 guidelines — the review checklist with evidence behind it

**Setup.** In 2019 a Microsoft Research team led by Saleema Amershi, with Eric Horvitz and thirteen others, published *Guidelines for Human-AI Interaction* at CHI, the field's main human-computer interaction conference. They consolidated **more than 150 scattered recommendations** into 20 candidates, cut to 18, then had **49 design practitioners** evaluate them against **20 popular AI products**, then ran an expert review of the revisions. Eight of the 18 trace back to principles Horvitz proposed for mixed-initiative systems in 1999.

That process is why this is **brick** rather than opinion, and it's the most citable thing in the module.

**Initially** — **G1** Make clear what the system can do · **G2** Make clear *how well* it can do it (how often it may be wrong).

**During interaction** — **G3** Time services based on context · **G4** Show contextually relevant information · **G5** Match relevant social norms · **G6** Mitigate social biases.

**When wrong** — **G7** Support efficient invocation · **G8** Support efficient dismissal · **G9** Support efficient correction (easy to edit, refine, recover) · **G10** Scope services when in doubt (disambiguate or gracefully degrade when uncertain about the user's goal) · **G11** Make clear why the system did what it did.

**Over time** — **G12** Remember recent interactions · **G13** Learn from user behaviour · **G14** Update and adapt cautiously · **G15** Encourage granular feedback · **G16** Convey the consequences of user actions · **G17** Provide global controls · **G18** Notify users about changes.

**How to use it:** as a **silent review checklist**, the way you'll use Intent·Ground·Contact·Consequence. Walk a design against 18 rows and you'll find three violations in ten minutes. Recite the list in an interview and you sound like someone who read a paper.

**The three hardest in a generative product** — a genuinely good thing to have an opinion about:

- **G2** assumes a single accuracy figure exists. For open-ended generation it usually doesn't, so hedged framing and visible sources carry the load a number can't.
- **G11** is dangerous with language models, because a model can produce a *fluent explanation that is not the actual cause.* Post-hoc rationalisation presented as explanation is worse than no explanation — it manufactures unearned trust.
- **G14** collides head-on with model version swaps. A provider deprecates a version, you migrate, and every behaviour users habituated to shifts at once. Most teams treat that as an infrastructure ticket. **It is a user-trust event**, and it belongs in your M5 rollout plan.

---

## 9. Who gets hurt, why teams ship anyway, and who owns the model

The design-thinking half. M1 asked who bears the cost of each error type; this is the harder version.

**Map three populations, and notice only one is "the user."**

1. **The operator** — the person using the system to do their job. Usually the only one in the PRD.
2. **The subject** — the person the system makes a decision *about*, who often never touches the interface. The claimant, the applicant, the flagged account. **They cannot see it, cannot correct it, and bear the largest share of a bad output.**
3. **The absorber** — whoever inherits the mess. The support agent taking the escalation, the reviewer clearing the queue, the ops person reconciling what the agent did overnight.

A spec with interaction design for population 1 only is a third of a product.

**Why teams ship anyway — and the honest answer isn't "bad people," it's four structural forces:**

- **The metric is authored by the party that benefits from it.** Assumed resolution, every time.
- **The counterfactual is never measured.** You know the system's error rate; nobody computes what the humans it replaced got wrong, so "better than nothing" goes unchallenged in both directions.
- **Costs land outside the org booking the benefit.** Automation saves your support budget; the cost is thirty extra minutes for each of ten thousand customers, and no line item collects it.
- **Launch pressure converts unknowns into assumptions.** "We'll monitor it" is where a missing decision goes to be forgotten.

**The politics of ownership**, which is where M4 hands off to M5. Four questions asked *before* launch, because afterwards they're a blame exercise: **who can turn it off**, and can they at 2 a.m. without a deploy? · **who owns a threshold change**, given it's a product, cost and staffing decision at once? · **who owns the data the system learns from**, including feedback captured through your interface? · **when it's wrong in public, whose name is on the statement?** Teams that answer these in advance behave differently from teams that don't.

---

## 10. Vocabulary, compressed

**Trust calibration (vs. maximisation) · appropriate reliance · overtrust / automation bias / complacency · undertrust / algorithm aversion · ability, reliability, benevolence · complementary knowledge · abstention · n-best · categorical vs. numeric confidence · hedged framing · uncertainty as behaviour · context error · failstate · background error · happy accident · risk gauge vs. stakes · return control · escalation contract · assume subversive use · stop-reason → user-facing message mapping · HITL insertion points: pre-action approval / sampled review / exception routing / user-invoked escalation · reviewer drift · rubber-stamping · gold cases · override rate · inter-rater agreement · anchoring in review · Wizard of Oz · the 18 guidelines (G1–G18) · post-hoc rationalisation · operator / subject / absorber · relational trust, behavioural alignment, friction recovery · model card**

---

## Exercises

**How these run:** I work one fully out loud first, saying why at each step; then you take one of the same shape with me available throughout. No cold start, no prediction, no score.

### Exercise A — Teardown of a trust surface *(not your fleet)*

I'll do **Intercom Fin** out loud: its pairings, where uncertainty surfaces, what happens at each of the eight outcomes, what transfers on handoff, and who the subject and absorber are — every claim labelled as I go.

**Then you take GitHub Copilot**, a product you can actually open and use. Produce:

- Which pairing(s) it operates in, and what changes when it moves from inline suggestion to agent mode.
- Its complete uncertainty surface. What does it *ever* tell you about how sure it is, and what does it use instead of a number?
- Its errors in PAIR's terms — context errors, failstates, and above all **background errors**. (Accepting a plausible wrong suggestion is the background error of your professional life. Say how you'd detect it.)
- Amershi's 18: three clearly applied, three clearly violated, with evidence.
- Two changes you'd make, each tied to a metric you'd expect to move.

Label every claim **observed** (you saw it), **inferred** (you're reasoning from behaviour) or **designed** (your proposal, not theirs). Public teardowns without this are architecture fanfic, and the labeling is itself the seniority signal.

### Exercise B — Forward design from a dirty brief

> A mid-sized health insurer wants to speed up **prior authorization** — the process where a doctor must get approval before a treatment is covered. Roughly 12,000 requests a week. 40 nurse reviewers. Median turnaround 6 days, and members complain constantly. Legal has one hard rule: **a denial may never be issued by the model alone.** The COO wants "80% automated by Q3." A nurse manager has said quietly that her team is already at capacity.
>
> **Design the interaction.**

Produce: which pairings exist and who occupies each · where the human sits, and why that insertion point over the other three · the confidence threshold *and its queue-volume and staffing consequence* · what the nurse reviewer sees, in what order, and what you deliberately withhold to avoid anchoring · the confidence representation, and the specific different action taken at each level · failure UX per PAIR error class — including how you'd ever detect a **background error**, since a wrongly-*approved* request generates no complaint · the escalation contract: what travels with the case, what the receiving human sees first · your reviewer-integrity plan · the three populations with what each is owed · and the one metric you'd refuse to report alone, with what you'd report beside it.

**Constraint shift, walked the first time:** partway through I'll change something — headcount drops from 40 to 25, or a regulator requires a member-readable written reason for every denial, or the vendor silently ships a new model version — and we re-derive together before you take one alone.

### The written artifact

**A failure-UX spec plus a model card**, for Golden Loop.

**The failure-UX spec** is one table, the deliverable form of §4: every stop reason → what the user is told → what they can do next → what the system does on their behalf → what gets logged → how you'd detect this failing silently. Plus a short subversive-use note (what you deliberately *don't* explain) and the escalation contract.

**The model card** format comes from *Model Cards for Model Reporting* (Mitchell, Gebru et al., 2019) — the sibling of M2's *Datasheets for Datasets*: where a datasheet documents a dataset, a model card documents a model. Sections: **intended use** and **out-of-scope use** · **factors** (populations and conditions performance varies across) · **metrics**, with decision thresholds stated · **evaluation data** and **training data** · **quantitative results, disaggregated** rather than averaged · **ethical considerations** · **caveats and recommendations**.

Together these **close the first of Grok's three gaps** on Golden Loop — the objection that an eval cockpit is an ML-engineer artifact rather than an AI-PM one. A failure-UX spec and a model card are the two documents an engineer will not write for you.

---

## Sources for this module

| Source | Tier | What it's for |
|---|---|---|
| [Amershi et al., *Guidelines for Human-AI Interaction*](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf) (CHI 2019) | **A** peer-reviewed | The 18 guidelines and their validation |
| [Google PAIR — *Errors + Graceful Failure*](https://pair.withgoogle.com/guidebook-v2/chapter/errors-failing/) | **B** primary | The error taxonomy, the risk gauge, paths forward |
| [Google PAIR — *Explainability + Trust*](https://pair.withgoogle.com/guidebook-v2/chapter/explainability-trust/) | **B** primary | Trust definition and calibration; the four confidence displays |
| [Zhang, Liao & Bellamy, *Effect of Confidence and Explanation on Accuracy and Trust Calibration*](https://arxiv.org/pdf/2001.02114) (FAT\* 2020) | **A** peer-reviewed | The empirical spine of §3, and the debate |
| [Intercom — *Fin AI Agent outcomes*](https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes) | **B** primary (vendor) | The anchor: a published, priced outcome taxonomy |

**Not in the notebook, cited here as reference reading:** Ziegler et al., *Measuring GitHub Copilot's Impact on Productivity*, CACM 67(3), 2024 (the backup anchor) · Mitchell et al., *Model Cards for Model Reporting*, FAT\* 2019 (the artifact format) · Lee & See, *Trust in Automation: Designing for Appropriate Reliance*, Human Factors 2004 (the origin of "calibrated trust") · Horvitz, *Principles of Mixed-Initiative User Interfaces*, CHI 1999 (eight of Amershi's 18 trace to it) · Wilson & Jones, *Stop Designing AI Chatbots, Start Designing AI Relationships*, April 2025 (the §1 grid).

**Honesty notes.** The pairings grid is **tier C** — a practitioner blog post, ChatGPT-assisted by disclosure, coining terms nobody else uses; the grid is useful, the vocabulary isn't portable. The Intercom material is **vendor documentation**: the outcome definitions and prices are observed fact, the incentive reading in §5 is explicitly my inference, and the competing resolution-rate claims are tier-D commercial sources I've deliberately not leaned on. Zhang et al. is a **single controlled study on one income-prediction task** — the trust-calibration finding is solid; the null result on explanations should be reported as "did not replicate in this setup," not "explanations don't work." Amershi is the brick; if you cite one thing from this module, cite that.

**Ask me anything.** §6 especially — reviewer integrity is what most PMs discover eight months after launch, and it's the one you can pre-empt for free.
