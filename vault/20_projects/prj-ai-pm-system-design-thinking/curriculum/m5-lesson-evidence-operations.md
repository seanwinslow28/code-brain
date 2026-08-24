---
title: "M5 — Evidence & Operations"
type: lesson
module: M5
status: ready
created: 2026-08-24
anchor: Rechat's Lucy — the whack-a-mole plateau (Hamel Husain)
backup_anchor: ICONIQ's 2026 AI gross-margin survey
mirror_eligibility: "partial — he has telemetry, cost caps and one real ship gate; he has never run an experiment or computed a unit economic"
---

# M5 — Evidence & Operations

*Module 5 of 5 · AI PM System Design Thinking · Weeks 7–8*

---

## 0. What you have, and the two things you've never done

Partial mirror. Some of this you built; a specific and important part you have never touched, and I want the line between them drawn sharply.

**What exists in your fleet, named:**

| What you built | What it is called |
|---|---|
| Health ledgers, nightly manifests, `critic-manifest-{date}.json` | **Instrumentation** — the system writing down what it did, separately from what it said |
| `evaluate_article_depth()` emitting `rejected_reasons` | **A quality gate with rejection telemetry.** Most gates only record the pass |
| The nightly critic running over the synthesizer's output | **An automated quality check on a schedule** — the shape of an eval loop, without a scored dataset behind it |
| `$7/task, $20/day, $50/month` and `check_caps` | **Cost control.** Read the next paragraph before you get comfortable |
| Your portfolio's merge gates — three engines green, 7/7 route sweep, p95 ≤ 16.7 ms, settle seam ≤ 1 px, bytes inside a pinned budget, *"nothing merges without Sean wheeling through all seven bands"* | **A launch gate with written, numeric thresholds and a named human sign-off.** This is the real thing. You built it for a website, by instinct, and it is exactly the artifact this module asks for |

**The distinction that matters most in this module:**

> **Cost control is not unit economics.** A cap stops a bill. Unit economics asks whether the thing makes money when it works. You are genuinely good at the first and have never once done the second — there is no revenue side to your fleet, no cost per successful outcome, no margin.

**What you have never done, taught here from zero:** run an experiment · put a model behind a rollout gate rather than merging code behind one · sample traces for structured human review · measure whether a judge agrees with a human · price anything · negotiate with another person about who owns a model, a threshold, or the data it learns from · run an incident where the thing that broke was probabilistic.

---

## 1. Instrumentation, and the unit you count

**A trace** is the log of one complete interaction — for an LLM product, usually the whole exchange, including what was retrieved, which tools fired, and what came back. Not a metric. The raw thing.

Hamel Husain — an ML engineer who consults on production LLM products and whose writing is the spine of this module — puts the operative rule in one sentence:

> **"You must remove all friction from the process of looking at data."**

His recommendation is blunter than most teams expect: build your own trace viewer rather than adopting a generic one, rendering traces in domain-specific ways, because the generic tool shows you JSON and the domain-specific one shows you the conversation the way the user experienced it. He reports teams with custom viewers **iterate roughly 10× faster**.

**Then the choice everyone skips: the unit of analysis.** The thing you count. Per turn? Per conversation? Per task? Per user per week?

It sounds like bookkeeping and it decides everything downstream. M4's Intercom Fin counts *conversations* — which is why one customer giving up quietly and one customer being helped land in the same bucket. Count turns instead and you'd get a different, equally defensible, completely incompatible number. **Pick the unit that matches the promise you made**, state it beside every metric, and treat a metric with no stated unit as a metric with no meaning.

**Sampling for human review**, and there are two jobs, not one:

- **A random sample** tells you the *rate*. It is the only thing that can. Small, boring, and the number you quote.
- **An error-weighted sample** — deliberately over-sampling failures and low-confidence cases — tells you *what's wrong*. It is where the learning is, and it is a biased estimate of the rate by construction.

Hamel does both, and shifts the mix over time: *"after the first two iterations, I tend to focus more on errors rather than sampling randomly."* Run only the error-weighted sample and you will confidently report a failure rate that is wildly too high. Run only the random one and you'll never see enough of any single failure mode to fix it.

---

## 2. Error analysis: the highest-leverage thing a non-engineer can do

This is the part of the module I'd have put first if the sequencing allowed, because it is the one activity in this entire curriculum that requires **no engineering at all** and produces more improvement than anything else on the list.

Hamel's framing, and it's addressed to you specifically:

> **"The people best positioned to improve your AI system are often the ones who know the least about AI."**

And the warning that goes with it: **"Generic metrics are worse than useless — they actively impede progress."** Teams adopt a dashboard of hallucination-rate, toxicity, helpfulness, watch the numbers move, and never learn that their users can't get a date parsed correctly.

**The method is borrowed wholesale from qualitative social science, and naming its provenance is worth doing** — it's the coding process from grounded theory, the technique researchers use to build a taxonomy out of interview transcripts. Applied to traces:

1. **Open coding.** Read traces one at a time and write a free-form note about what went wrong. No categories yet, no rubric, no dropdown. Just prose. This step *requires* product and domain knowledge and is actively damaged by delegating it to someone without it.
2. **Axial coding.** Once you have 30–50 hand-coded notes, group them into a taxonomy of **5–10 failure modes**. An LLM helps here — after you've done the hand-coding, not instead of it. The order matters: let the categories emerge from the data rather than imposing them, or you'll find exactly the failures you already believed in.
3. **Count.** Label every trace against the taxonomy and count frequencies. A spreadsheet pivot table is the correct tool.
4. **Prioritise by frequency × cost.** M1's error economics, finally applied to real data — the most common failure and the most expensive failure are rarely the same one.

**What it produces, in his reported cases:** at one company, three issues accounted for **over 60% of all problems**; fixing one failure mode moved date handling from **33% to 95%**. Those numbers come from a practitioner's own consulting write-ups rather than a controlled study, so treat them as illustrative of the shape, not as effect sizes.

**And the two outputs that matter structurally:** the taxonomy becomes your eval categories, and the traces you labelled become the seed of your golden dataset. **You cannot buy either.** This is also the honest answer to M4's background-error problem — errors nobody reports are found by a person reading traces, and by nothing else.

---

## 3. Invariants → golden datasets → holdout hygiene

The progression matters, and most teams try to start at the end.

**Day-one invariants.** M3 planted these: a handful of assertions that must always hold. Destructive tools require approval. Structured output validates against schema. Budget exhaustion stops gracefully. Cheap, immediate, and they run on every change.

Hamel's cost ladder, which is the scheduling rule:

| Level | What | Cadence |
|---|---|---|
| **L1 — Unit tests / assertions** | Fast, cheap, deterministic checks | Every code change |
| **L2 — Human & model eval** | Traces reviewed by a person or scored by a judge | A set cadence |
| **L3 — A/B test** | Real users, real outcomes | Only after major changes |

> **"The cost of Level 3 > Level 2 > Level 1. This dictates the cadence and manner you execute them."**

At Rechat (§5) there are **hundreds** of L1 tests, continuously updated as new failures appear. The test inputs don't have to wait for production traffic — he synthesises them, literally prompting *"write 50 different instructions that a real estate agent can give to his assistant to create contacts on his CRM."*

**And the line to carry into a room:**

> **"You don't necessarily need a 100% pass rate. Your pass rate is a product decision."**

That is M1's threshold lesson wearing engineering clothes. The pass bar is yours, it's a trade-off against cost and time, and a team that treats every red test as blocking will stop writing tests.

**Golden dataset.** A curated set of examples with known-correct outputs, built out of error analysis, versioned like code. Its value is entirely in the curation — a big dataset of easy cases measures nothing.

**Holdout hygiene**, which is the part that quietly rots:

- Keep a portion you **never** tune against. Look at it to decide, not to iterate.
- Every time you fix a prompt to pass a specific eval case, that case has partly stopped measuring. Over months of that, your suite measures your history of fixes rather than your product.
- **The LLM-specific leak:** eval examples get pasted into prompts as few-shot examples. Now the model has seen the test. This happens constantly and almost nobody notices.
- Rotate. Add new cases from live failures. Retire cases everything passes.

---

## 4. LLM-as-judge: the method, then the ways it lies

**What it is:** instead of a human scoring outputs, another model scores them. Cheap, fast, and it scales — which is precisely why it gets adopted before anyone checks whether it's measuring anything.

**Hamel's method, which is the good version:**

**Find *The* Principal Domain Expert — one person.** His words: *"In most organizations there is usually one (maybe two) key individuals whose judgment is crucial."* And the failure he names explicitly: *"Many developers attempt to act as the domain expert themselves… This is a recipe for disaster."* One authoritative voice, because a committee produces contradictory labels and you cannot align a judge to a contradiction.

**Collect their critiques, in prose.** Not scores — written critiques explaining *why*, **"detailed enough that a new employee could understand it. Being too terse is a common mistake."** Those critiques become few-shot examples in the judge prompt.

**Start with ~30 examples** and keep going *"until I do not see any new failure modes."*

**Then measure agreement — and here is the sentence that separates competent from not:**

> **"Using raw agreement is generally not recommended and can be misleading when classes are imbalanced. Instead, you should typically measure precision and recall separately."**

If 95% of your outputs are fine, a judge that says "fine" every time scores 95% agreement and is worthless. Straight out of M1's confusion matrix. In his Honeycomb case, three iterations reached **>90% agreement** with the expert — and he is explicit that alignment is not a one-time event: it needs re-checking periodically and whenever anything material changes.

**Now the failure modes.** A 2024–26 academic survey of LLM-as-a-judge (continuously revised, so date it when you cite it) catalogues them; the ones with the most evidence behind them:

- **Position bias** — the judge favours whichever answer it sees first. The most-studied by a distance. *Mitigation: randomise order, or score both orders and require agreement.*
- **Length / verbosity bias** — longer answers score higher, independent of quality. *Mitigation: length-normalise, or state a length expectation in the rubric.*
- **Self-enhancement / self-preference** — a judge prefers text from its own model family. *Mitigation: judge with a different family than the generator.*
- **Concreteness bias** — answers full of specific numbers and citations score higher whether or not the specifics are correct. Worth sitting with: this one rewards exactly the surface features of a confident hallucination.
- Plus style, knowledge, instruction and cultural biases, all named in the literature with thinner evidence.

**And the one the map singles out — weak-judge Goodharting.** Goodhart's law: *when a measure becomes a target, it ceases to be a good measure.* Applied here: if you iterate your product against a judge that is weaker than your system on the dimension being judged, you optimise toward **the judge's biases** rather than toward quality. Your eval score climbs, your users notice nothing, and the improvement is entirely inside the measuring instrument.

> **The governing idea: a judge is a measuring instrument, and an uncalibrated instrument is not a cheap instrument — it is a decorative one.** Validate it against human labels, re-validate on a schedule, and quote its numbers with the agreement figure attached.

---

## 5. The anchor: Rechat's Lucy, and the plateau that has a name

**Setup.** Rechat is a software company for real-estate agents; **Lucy** is its conversational AI assistant, built to replace clicking and navigating the CRM with a conversation. Hamel Husain worked on it and wrote the story up.

The early phase went the way it always goes: fast progress from prompt engineering. Then it stopped. Three symptoms, and they are the diagnostic set worth memorising because they show up in this exact combination:

1. **"Addressing one failure mode led to the emergence of others, resembling a game of whack-a-mole."**
2. No visibility into how the assistant performed across tasks beyond subjective impressions.
3. Prompts grew into *"long and unwieldy forms, attempting to cover numerous edge cases."*

**What those three symptoms mean, together, is one thing: the team had no measurement.** Every fix was a bet placed blind, and because nothing measured the whole surface, a fix that broke something else was indistinguishable from a fix that worked. The prompt grew because the prompt was the only place to put a fix.

The escape wasn't a better model or a cleverer prompt. It was **hundreds of unit tests plus a systematic eval loop** — the thing this module is about. Note what that implies for you: the plateau is not a capability ceiling, and reaching for a bigger model when you hit it is the most expensive available way to avoid writing an eval.

**The backup anchor** covers the other half of the module — money. ICONIQ Growth, a firm that invests in software companies and publishes an annual survey of them, surveyed roughly **300 executives building AI products** (fieldwork in April and December 2025, published as its 2026 snapshot — mind that gap when you quote it). Headline: companies expect AI-product gross margins of **~52% on average in 2026**. Pricing is unsettled — **58%** keep a subscription or platform component, **35%** charge on consumption, **18%** have moved to outcome-based pricing, and **37%** plan to change pricing within twelve months.

*(Tier note: a VC surveying a population that includes its own portfolio, self-reported and projected rather than audited. Directionally useful; not a benchmark to state as fact.)*

---

## 6. The ML Test Score — steal this rubric

**Setup.** In 2017, Eric Breck, Shanqing Cai, Eric Nielsen, Michael Salib and D. Sculley at Google published *The ML Test Score* at the IEEE Big Data conference. Same Sculley as M3's technical-debt paper. It is a **28-test rubric for production readiness**, in four sections of seven: **Data, Model, Infrastructure, Monitoring.**

**The scoring design is the part to steal:**

- **Half a point** for running a test manually, with results documented and distributed.
- **A full point** if it runs **automatically, on a repeated basis.**
- Sum each of the four sections — then **the final score is the *minimum* of the four**, not the total.

That minimum rule is the whole philosophy in one arithmetic choice: **a system is exactly as production-ready as its weakest area**, and you cannot buy your way out of no monitoring with excellent data tests. Their scale bottoms out at *"more of a research project than a productionized system."* They interviewed **36 teams across Google** with it — and one team, asked a routine question, discovered a thousand-line completely untested file generating their input features.

**The rows that carry the most for an LLM product:**

- **Model 2 — offline proxy metrics correlate with actual online impact.** The most important and most skipped test in the whole rubric. Your eval score is a *proxy*. Has anyone ever checked that moving it moves anything a user or the business feels? If not, you are optimising a number you have never validated.
- **Model 6 — quality is sufficient on all important data slices.** Averages hide the segment you're failing. This is M4's model card asking for disaggregated results, from the engineering side.
- **Model 4 / Monitor 4 — staleness.** How much worse does the system get per day without an update, and how old is the thing in production right now?
- **Infra 6 and 7 — canary before production, and fast safe rollback.** They call rollback *"a key part of incident response."*
- **Monitor 1, 2, 7 — dependency changes notify you; data invariants hold in both training and serving; prediction quality has not regressed on served data.**

**Honesty note:** it's 2017 and pre-LLM. Some rows don't map — nobody's tuning hyperparameters on a hosted model. The **structure, the manual-vs-automated distinction, and the minimum rule transfer completely**, and saying "this is a 2017 rubric and here's the third of it that doesn't apply" is exactly the calibrated reading that reads as senior.

---

## 7. Rollout, and the five things between "it works" and "everyone has it"

| Stage | What it is | What it buys |
|---|---|---|
| **Shadow mode** | The new version runs on real traffic; output is logged, never shown | Real-distribution measurement at zero user risk. Absurdly underused |
| **Canary** | A small slice of real traffic gets it | Catches what offline testing structurally cannot |
| **Champion / challenger** | Incumbent keeps serving; challenger runs alongside and is promoted on evidence | Makes "should we switch" a measurement instead of an argument |
| **A/B test** | Randomised, measuring the actual outcome | The only thing that establishes the change *caused* the result |
| **Kill switch** | A config flag that disables the feature without a deploy | The difference between a 4-minute incident and a 4-hour one |

**Three things people get wrong, in order of frequency:**

**Randomise the right unit.** If the same person can hit both variants, or if one user's behaviour affects another's experience, per-request randomisation gives you a clean-looking number that means nothing. Randomise the *user*, usually.

**Decide what would make you stop, before you start.** Written, numeric, agreed. You already do this — your portfolio build has "three engines green," "7/7," "p95 ≤ 16.7 ms," and a human wheeling through every band. That's launch criteria. The only difference here is that one of the thresholds is a *quality* number that will never be 100%, so it has to be argued for rather than assumed.

**Rollback is a time budget, not a capability.** "Can we roll back?" is the wrong question; every team says yes. **"How long does it take, who can do it, and have we ever actually done it?"** is the question — and it's M4's "who can turn it off at 2 a.m." with a stopwatch attached.

---

## 8. Drift: four ways yesterday's evidence expires

Your evals passed. Nothing changed. The product got worse anyway.

- **Covariate shift** — the inputs change; the underlying relationship doesn't. A new customer segment arrives asking differently-shaped questions. *Detect:* monitor the input distribution.
- **Label shift** — the base rate changes. Fraud attempts double. Your threshold was tuned to the old rate and is now in the wrong place. *Detect:* monitor the output/prediction distribution.
- **Concept drift** — the relationship itself changes. Same input, different correct answer, because the world moved: what counts as spam, what a policy allows, what "our refund window" means after Legal changed it. **The nastiest of the three**, because nothing about the data looks different.
- **The LLM-native fourth: the model changes underneath you.** A provider deprecates a version, you migrate, and behaviour shifts everywhere at once. M4's guideline 14 said this is a user-trust event. It is also a full re-run of your evals, and it belongs on the roadmap as scheduled work rather than arriving as a surprise.

**The honest difficulty:** the strongest signal — prediction quality on *served* data — is usually the one you can't measure, because served data has no labels. Which is why §1's sampling and §2's error analysis aren't a nice-to-have. They are the only ground truth you will ever have about live behaviour.

---

## 9. Unit economics at the product level

Not cost per call. Cost per **successful outcome**, held next to what that outcome is worth.

**Why the shape is different from software you've priced before:** classic SaaS ran 80–90% gross margins because serving one more user cost almost nothing. AI serving cost scales with usage — every query spends real inference. That single fact is why ICONIQ's surveyed companies project **~52%** and why **18%** of them have already moved to outcome pricing. It changes what you can afford to give away free, whether unlimited plans are survivable, and which customers are worth having.

**The calculation a PM should be able to sketch on a whiteboard:**

1. **Define the unit** — the thing the customer values. A resolved ticket. A drafted contract. Not a token, not a call.
2. **Count everything one unit consumes**, including the failures. Four model calls, two retrievals, a judge pass, and — critically — **the 30% of attempts that don't resolve and still cost money**, plus the human review minutes on the ones that escalate.
3. **Put revenue beside it.** Price per unit, or subscription revenue divided by units consumed.
4. **Then ask the three questions that matter:** what's the margin per unit · which direction does it move as usage grows (retries and long contexts make it *worse*, caching and routing make it better) · and **at what usage level does a customer become unprofitable?** Heavy users are your best reference accounts and your worst margins, simultaneously.

**The levers, cheapest first:** routing hard work to a strong model and routine work to a cheap one — *you built a router; you have never pointed it at a margin* · caching · trimming context · cutting retries by fixing the failure that causes them, which is §2 paying for itself · and last, renegotiating rates.

**The trap, and it links straight back to M4:** the moment you price per outcome, **the definition of "outcome" becomes a revenue decision.** Intercom's "assumed resolution" is what that looks like from the inside. Whoever writes that definition is setting a price, and it should not be a decision that happens by default in an engineering ticket.

---

## 10. Ownership, review, and what an AI incident actually is

M4 ended on four questions. Here they get answered.

**Ownership, written down before launch:** who can disable it, and how fast · who approves a threshold change (product, cost and staffing at once — so name one owner and one approver, not three claimants) · who owns the data it learns from, including feedback captured through your own interface · who signs the public statement when it's wrong in public.

**Review boards** are useful when they have a decision right, a scope, and a written standard to review against. They are theatre when they exist to distribute blame for a decision already made. **The test: has the board ever said no?** If not, it isn't a gate.

**What makes an AI incident different from a software incident** — three things, and they break normal incident practice:

1. **You often can't reproduce it.** Same input, different output. Your first job is capturing the trace, because it may be the only evidence that will ever exist.
2. **The fix usually isn't code.** It's a prompt, a threshold, a retrieved document, a model version. Those move through different review than code and frequently through *no* review, which is its own finding.
3. **"The model got it wrong" is not a root cause.** It's the observation. The root cause is that nothing detected it, or the threshold was set without the cost analysis, or the retrieved document was stale, or nobody owned the update.

**The runbook — and this is a section of your artifact:** how it's detected (which alarm, on what metric, at what threshold) · severity levels, with an example of each so people don't argue during the incident · who is paged · the rollback procedure **and its measured time budget** · what users are told and when · and the postmortem, blameless, ending in the only two questions that matter: **what would have caught this earlier, and which test gets added today?**

That last question closes the loop. Every incident should end by growing the golden dataset, which is the whole loop from §2 to §10 running once around.

---

## 11. Vocabulary, compressed

**Trace · unit of analysis · random vs error-weighted sampling · error analysis · open coding · axial coding · failure taxonomy · frequency × cost prioritisation · invariant test · L1/L2/L3 eval ladder · pass rate as a product decision · golden dataset · holdout hygiene · eval contamination · LLM-as-judge · principal domain expert · judge–human agreement · precision and recall over raw agreement · position bias · length/verbosity bias · self-enhancement bias · concreteness bias · Goodhart's law · weak-judge Goodharting · ML Test Score · manual vs automated scoring · the minimum rule · offline proxy vs online impact · data slices · staleness · shadow mode · canary · champion/challenger · A/B test · unit of randomisation · kill switch · rollback time budget · launch criteria · covariate shift · label shift · concept drift · model version drift · cost per successful outcome · gross margin · outcome-based pricing · blameless postmortem · incident runbook**

---

## Exercises

**How these run:** I work one fully out loud first; then you take one of the same shape with me available throughout. No cold start, no score.

### Exercise A — Error analysis, on real traces

The one mirror exercise in the curriculum that earns its place, for two reasons: error analysis can only be learned on data whose domain you actually understand, and **the output is Golden Loop's demo dataset.** The map left open whether that dataset should be fictional or real; this settles it in favour of real, which is also the stronger honesty story.

Take **20 real traces from `job_feed`** — the scoring decisions, with the posting and the fit verdict.

I'll open-code the first five out loud, writing the note before naming any category, and narrating why I'm resisting the urge to categorise early. **You take the next fifteen.** Then together: axial-code into 5–10 failure modes, count frequencies, and rank by frequency × cost.

Produce: the taxonomy, the counts, the top three by frequency × cost, **the unit of analysis you chose and why**, and the five traces you'd promote into a golden dataset with the correct output written out.

### Exercise B — Forward design from a dirty brief

> A B2B software company wants an AI agent that resolves inbound support tickets. **30,000 tickets a month.** A human-handled ticket currently costs them about **$6** fully loaded. Sales wants to charge customers **per resolution** and has floated **$1**. The CEO has told the board **"70% deflection by Q4."** Support leadership has not been consulted. There is no eval suite and nobody has read a transcript in months.
>
> **Define what "launch" means, and what it costs.**

Produce: how you'd define a resolution, and the three ways that definition could be gamed · your first two weeks of error analysis and what you'd expect it to change · the eval ladder — what's L1, L2, L3 here, and the cadence of each · whether you'd use an LLM judge, how you'd validate it, and what you'd report alongside its numbers · **written launch criteria with numeric thresholds and a named owner per threshold** · the unit economics: cost per successful resolution including failures and escalations, margin at $1, and the usage level where a customer goes underwater · the rollout sequence and the rollback time budget · what you'd monitor for each of the four drift types · and the incident runbook's first page.

**Constraint shift, walked the first time:** partway through I'll change something — shadow mode measures 41% resolution against the 70% in the board deck, or the provider deprecates your model version three weeks post-launch, or a competitor prices at $0.60 — and we re-derive together before you take one alone.

### The written artifact

**Launch criteria, a cost model, and an incident runbook** — for Golden Loop.

- **Launch criteria:** each threshold numeric, each with a named owner, and each with the sentence "we do not ship if…" written out. Your portfolio gates are the template; you already know how to do this.
- **Cost model:** per trace, per eval round, and at 10,000 traces/month for a team — the three levels the Phase C prompt asks for.
- **Incident runbook:** detection, severity with examples, rollback and its time budget, comms, postmortem template.

These **close the remaining two of Grok's three Golden Loop gaps.** With M4's failure-UX spec and model card, all three are closed and the five module artifacts are the product's complete planning spine — which was the point of running the modules in this order.

---

## Sources for this module

| Source | Tier | What it's for |
|---|---|---|
| [Hamel Husain — *Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/) | **B** primary (practitioner) | The Rechat anchor, the L1/L2/L3 ladder, unit tests, traces |
| [Hamel Husain — *Using LLM-as-a-Judge For Evaluation*](https://hamel.dev/blog/posts/llm-judge/) | **B** primary (practitioner) | The judge method: principal domain expert, critiques, agreement measurement |
| [Breck et al., *The ML Test Score*](https://research.google.com/pubs/archive/aad9f93b86b7addfea4c419b9100c6cdd26cacea.pdf) (IEEE Big Data 2017) | **A** peer-reviewed | The 28-test rubric, the minimum rule, monitoring and rollout tests |
| [*A Survey on LLM-as-a-Judge*](https://arxiv.org/pdf/2411.15594) (arXiv, revised through 2026) | **A** survey | Judge failure modes — position, length, self-enhancement, concreteness |
| [ICONIQ — *2026 State of AI: Bi-Annual Snapshot*](https://www.iconiq.com/growth/reports/2026-state-of-ai-bi-annual-snapshot) | **C** industry survey | Unit economics: gross margins and pricing-model adoption |
| Sculley et al., *Hidden Technical Debt in ML Systems* — already in the notebook (`ce870d74`), carried from M3 | **A** peer-reviewed | Why the ops burden exists at all |

**Not in the notebook, cited here as reference reading:** NIST *AI Risk Management Framework* (AI 100-1, 2023) — the citable structure for governance and incident response, if anyone asks where the ownership questions come from · Hydari, Iqbal & Ramasubbu, *The Stochastic Tax* (arXiv 2605.27320) — taught in M3; the ongoing operating burden a probabilistic system imposes even when nothing is broken · Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (NeurIPS 2023) — the paper that first documented position, verbosity and self-enhancement bias · Google's SRE practice on blameless postmortems.

**Honesty notes.** Hamel Husain's writing is **practitioner primary, not research** — the method is battle-tested and widely adopted, and the numbers in it (33%→95%, three issues = 60% of problems, >90% agreement in three iterations) are consulting write-ups, not controlled studies. Cite them as shape, not as effect sizes. The ML Test Score is **2017 and pre-LLM**; roughly a third of its rows don't map to a hosted-model product, and saying which third is the calibrated read. The judge survey is a **continuously-revised arXiv survey** rather than a fixed peer-reviewed artifact — date it when you cite it, and note that its bias catalogue has much stronger evidence for position and length bias than for the rest. ICONIQ is **tier C**: a VC surveying a population that includes its own portfolio, self-reported and projected, with fieldwork in 2025 published under a 2026 title. Directionally useful, and I would not put the 52% in a slide without that sentence attached.

**Ask me anything.** §2 especially — error analysis is the one thing here you could start doing this afternoon with no code, and it is the single highest-leverage skill in the module.
