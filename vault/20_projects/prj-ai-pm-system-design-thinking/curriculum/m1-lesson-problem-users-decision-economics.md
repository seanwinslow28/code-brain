---
title: "M1 — Problem, Users & Decision Economics"
type: lesson
module: M1
status: ready
created: 2026-08-17
anchor: Amazon's scrapped résumé screener (Reuters, Dastin, 10 Oct 2018)
backup_anchor: clinical triage thresholds
mirror_eligibility: partial
---

# M1 — Problem, Users & Decision Economics

*Module 1 of 5 · AI PM System Design Thinking · Weeks 1–2*

---

## First: what your fleet already forced, and what it didn't

This module is partly recognition and partly new. Being straight about which is which is the point — the last version of this curriculum assumed everything was recognition, and that assumption was wrong.

**Your fleet already made you do this one.** The discovery council drops any pain point that can't be traced back to a real fetched URL. You built that gate because you'd rather lose a real finding than publish a fabricated one. That is a **precision-over-recall decision** — you chose the error you could live with, and you accepted a known cost (losing true findings) to avoid a worse one (shipping invented ones). You have never called it that. It has a name, a literature, and a place in every AI system design conversation you'll ever have.

Same with `fallback = "none"` on the Tier C route. An off-hours miss raises an error instead of quietly billing the paid API. You decided which failure you preferred and encoded it. That's error economics.

**Your fleet never made you do these**, and this is where the module teaches from zero:

- **Naming an error budget.** You have *cost* budgets — $7 a task, $20 a day, $50 a month. You have never written down a tolerable *failure* rate: "this can be wrong 8% of the time before we stop shipping it."
- **Eliciting the cost of a wrong answer from someone who isn't you.** Every threshold in your fleet was set by the person who bears the consequence. That is the easy case, and it is not the job.
- **Reasoning about who gets hurt when it isn't the operator.** When your synthesizer degrades, you find out. When a claims model degrades, a stranger doesn't get paid.
- **Calibration** and **class imbalance** — neither has come up, because your systems don't emit confidence scores anyone has to trust, and your data isn't 200:1 skewed.

Two of five are recognition. Three are new. Expect the second half to feel harder, and don't read that as a failure.

---

## 1. The move that comes before everything

Before architecture, before data, before a model: **does this problem need a probabilistic system at all?**

Google's PAIR team — a research group inside Google that publishes design guidance for AI products — puts this first in their *People + AI Guidebook*, and their framing is the useful one: find the user need first, then ask whether AI *uniquely* addresses it. Not whether AI *could* be applied. Whether it's the thing that makes the experience possible.

The reason this comes first is economic, not philosophical. A probabilistic system carries a permanent tax that a deterministic one does not: monitoring, evaluation, drift response, incident handling for failures that don't reproduce. Recent work calls this the **stochastic tax** — the operating burden a probabilistic system imposes *even when nothing is broken and everything is governed well*, because runs vary, tools fail, and adoption keeps surfacing new edge cases. (That term is from a 2026 preprint by Hydari, Iqbal and Ramasubbu — fresh scholarship, not settled canon, so use the idea and date the source.)

You already pay this tax. It's why you have a nightly critic, a lint job, and a health ledger. Nobody makes you run those for a bash script.

So the first question in any system design conversation, and a strong signal when you ask it out loud:

> **What's the non-AI baseline, and what does AI have to beat?**

Rules on claim value. A lookup table. A sort. A human doing it. If the baseline gets you 80% of the value with none of the tax, the interesting design question is what the remaining 20% is worth — not what model to use.

Two follow-ons worth having ready:

- **Automate or augment?** Automating removes work and removes control. Augmenting keeps the person in the decision and keeps their throughput lower. This is a product decision with a user-research answer, not an engineering one.
- **What does success mean to the person using it**, as distinct from what's convenient to measure? A model that's 94% accurate and wrong in the cases people care about is a failed product with good metrics.

---

## 2. Error economics: the question "how accurate is it" cannot answer

Here is the move that separates people who reason about AI systems from people who talk about them.

Every predictive system makes two different mistakes, and they are almost never equally expensive.

- A **false positive** is the system saying yes when the answer is no. Flagging a legitimate claim as fraud. Marking a real email as spam.
- A **false negative** is the system saying no when the answer is yes. Missing the fraud. Letting the spam through.

A single "accuracy" number averages these together and therefore destroys the only information that matters. Two systems with identical accuracy can have opposite consequences.

Take spam filtering, which you can inspect today in your own inbox. A false negative is a junk email in your inbox — you delete it, mild annoyance, five seconds. A false positive is a real email in your spam folder — and if that email was a job offer, a legal notice, or a doctor's result, the cost isn't five seconds. It's unbounded, and worse, **it's silent**: nobody knows the message was lost. That's why spam filters are tuned to be far more willing to let junk through than to quarantine something real. The asymmetry, not the accuracy, set the design.

Now flip it. In cancer screening, a false positive means an anxious patient and an unnecessary follow-up test. A false negative means a missed tumour. Same two error types, inverted costs, opposite threshold.

**The threshold is where this decision physically lives.** A classifier doesn't output "spam" or "not spam" — it outputs a score, and somebody picks the line above which the score counts as a yes. Moving that line trades one error for the other. You cannot reduce both at once; you can only choose which one you'd rather have.

That choice is a **product decision**, not a data-science one. It is one of the highest-leverage decisions a PM owns on an AI product, and it's the one most often left to whoever is writing the code — who will default to whatever maximizes a symmetric metric, because nobody told them the costs were asymmetric.

The question to ask in the room:

> **What does a false positive cost us, what does a false negative cost us, and who pays each one?**

That last clause does real work. When the person harmed is not the person deploying, the incentives don't self-correct.

---

## 3. The vocabulary, defined plainly

You'll hear these constantly. Know the name, then explain it in plain words — that pairing is the expert signal. Reciting the glossary is not.

**Precision** — of everything the system flagged, how much was actually right. *"When it says fraud, how often is it fraud?"* High precision means few false alarms.

**Recall** (also called sensitivity) — of everything that was actually there, how much did the system catch. *"Of all the real fraud, how much did we find?"* High recall means few misses.

These trade against each other. Lower the threshold and you catch more real cases and more false alarms — recall up, precision down. Raise it and the opposite. Your discovery council's URL gate is a deliberately high-precision, low-recall setting.

**F1 score** — a single number blending precision and recall. Convenient, and it silently assumes the two errors cost the same, which is the assumption you just learned to interrogate. When someone quotes F1, the useful question is *why is that the right blend for this problem?*

**Calibration** — whether the confidence numbers mean anything. A well-calibrated system that says "80% confident" is right about 80% of the time across many such cases. An uncalibrated one says 80% and is right 55% of the time. This matters enormously the moment you show a confidence number to a user or route on it, because both make a promise the system may not keep. It's a separate property from accuracy: a model can be accurate and badly calibrated, or calibrated and mediocre.

**Class imbalance** — when one outcome is far rarer than the other. If 0.5% of claims are fraudulent, a system that says "not fraud" every single time is **99.5% accurate** and completely worthless. This is the cleanest demonstration that accuracy alone is not a metric, it's a decoration.

**Error budget** — a stated, agreed tolerance: how wrong this is allowed to be before we act. Borrowed from site reliability engineering, where teams budget downtime rather than pretending to target zero. Its value isn't the number; it's that the number is agreed *in advance*, so degradation triggers a decision instead of an argument.

**Kill criteria** — what you decided, before launch, would make you turn it off. Written down, with a threshold and a name attached.

---

## 4. Turning it into a decision, which is the part people skip

Diagnosis without disposition is academic. A system design answer that ends at "and then we'd measure it" is unfinished, and interviewers notice.

A complete disposition has four parts:

1. **The threshold**, with its reasoning. *"We tune for precision because a false accusation lands on a customer with no appeal path."*
2. **The error budget.** *"Below 92% precision on flagged claims, we stop routing automatically and go review-only."*
3. **The kill criteria.** *"Two consecutive weeks under budget, or any single incident involving a protected class, and it's off."*
4. **Where the number is visible.** A threshold nobody watches is a threshold nobody has. This is the piece most often missing — the literature is blunt that error budgets and SLOs only function when they're wired into something that alerts.

You can already say the shape of this, because you built it for cost. `$7 per task, $20 per day, $50 per month, refuse rather than exceed` is a threshold, a budget, and a kill criterion with an enforcement point. The move is transposing that instinct from dollars to errors, and to consequences borne by someone who isn't you.

---

## 5. Who gets hurt, and why teams ship anyway

This is the half the previous curriculum was missing, and it's not soft — it's the part that predicts which products blow up.

Three questions, and none has a technical answer:

**Who bears the cost of a wrong answer?** Sometimes the operator, who will notice and complain. Sometimes a third party who never sees the system, cannot appeal, and doesn't know a model was involved. The second case is where the incentive loop is broken by construction: the people harmed have no channel to the people who could fix it.

**What's the recourse path?** When the system is wrong about someone, how do they find out, who do they tell, and what happens? A product with no recourse path has decided that its false positives are free. They are not free; the cost has just been moved somewhere it won't be measured.

**Why would a team ship it anyway?** This is the one that separates analysis from judgment. Teams ship known-flawed systems for structural reasons: a launch date tied to a review cycle, a metric that only counts throughput, a champion whose promotion depends on it, a quality signal that arrives two months after the ship signal. Understanding the *organizational* loop is how you predict the failure before the technical analysis does — and it's why the same technical mistake keeps recurring at different companies.

If you can name, in a room, both the person who gets hurt and the incentive that makes shipping rational anyway, you're doing something most candidates don't.

---

## 6. The anchor: Amazon's résumé screener

**One-sentence setup:** In 2014 Amazon began building an internal tool to score job applicants' résumés automatically — the ambition was to hand the machine 100 résumés and get the top five back. Reuters reporter Jeffrey Dastin revealed on 10 October 2018 that the company had quietly scrapped it.

What happened, and why every part of it belongs to this module:

The system was trained on ten years of résumés previously submitted to Amazon. Most came from men, reflecting the industry's composition. The model did exactly what it was built to do — learn the patterns in the historical data — and the pattern it learned was that men were preferred. It reportedly penalised résumés containing the word "women's," as in "women's chess club captain," and downgraded graduates of two all-women's colleges. Engineers noticed by 2015 and edited the system to be neutral on those specific terms, which fixes the symptoms it had found and not the mechanism. The project was abandoned around 2017.

Run the module's questions against it:

- **Should this have been AI at all?** The stated user need was reducing screening effort. The non-AI baselines — structured rubrics, blind résumé review, work samples — are well studied and address the same need, and some have better evidence behind them. The unique value of the AI version was speed, and speed was not the binding constraint on hiring quality.
- **What are the error costs, and who pays?** A false positive advances a weak candidate — expensive to Amazon, caught later in the loop, recoverable. A false negative rejects a strong candidate who **never finds out, has no recourse, and is not counted anywhere**. Entirely different magnitudes, entirely different bearers, and only one of them shows up in any metric the team would have watched.
- **Where was the error budget?** There wasn't one, because there was no agreed definition of a wrong answer. "Wrong" was defined as *disagrees with historical hiring decisions*, which encoded the thing that needed questioning.
- **Why ship it anyway?** They didn't, ultimately — and that's the most interesting part. Amazon killed it. The failure worth studying isn't the shipping decision; it's that the project ran roughly three years before the framing question got asked properly.

**Use this carefully when you talk about it.** Reuters' account is single-sourced to people familiar with the project, Amazon disputed that the tool was ever used to evaluate candidates, and the internal details are not independently verifiable. Say what's observed and what's inferred. That discipline is itself the skill — and it's the module's habit, starting now.

---

## 7. Vocabulary, compressed

**Non-AI baseline · stochastic tax · automate vs augment · false positive / false negative · error asymmetry · threshold · precision · recall · F1 · calibration · class imbalance · error budget · kill criteria · recourse path · who bears the cost · the incentive that makes shipping rational**

---

## Exercises

Prediction goes first, in writing, before you look at anything. Then the work. Then we compare.

### Exercise A — Forward design from a dirty brief *(the format the last curriculum never practiced once)*

> You're the PM at a mid-size property insurer. Claims operations runs 40 adjusters handling roughly 9,000 first-notice-of-loss claims a month. Leadership wants "AI triage" — route each claim to the right adjuster and flag the likely-fraudulent ones. You have two engineers for the quarter, a compliance review in Q1, and three years of historical claims whose adjuster notes range from thorough to a single word. Legal has already asked what happens when the system flags a legitimate claimant.
>
> **What do you build?**

**Predict first (15 min, written).** Before designing: what will the binding constraint turn out to be — data, compliance, engineering capacity, or the error asymmetry? Name your falsifier: what would you observe that proves you picked wrong?

**Then design (60 min).** Produce: the non-AI baseline and what AI must beat; the error-cost table for both error types with who bears each; your threshold and its reasoning; an error budget with a number; kill criteria; the recourse path for a wrongly-flagged claimant; and **at least two alternatives you rejected, with why.** Take a defended position. "It depends" is not an answer; "it depends on X, and here's how I'd find out X in a week" is.

**Then the constraint shift.** I'll change one thing and you re-derive live.

### Exercise B — Teardown, with modes labeled

Pick a spam filter you use — your own inbox is fine and is genuinely inspectable. Reconstruct the error-economics decision behind it.

Label **every** claim as one of:
- **observed** — you can see it happening
- **inferred** — you're reasoning from behavior to a design decision
- **designed** — this is what *you* would do, not what they did

That labeling is not pedantry. Public teardowns without ground truth become architecture fanfic, and being explicit about your evidence is a maturity signal an interviewer will register within thirty seconds.

### The written artifact

**A PRD for one AI feature, carrying its error economics.** Whatever you'd have written before, plus: the non-AI baseline, the two error costs and who bears them, the threshold with reasoning, the error budget, the kill criteria, and the recourse path. Roughly two pages.

This becomes **Golden Loop's PRD.** Not an exercise you throw away.

### The verbal rep

**Retrospective and untimed** — that's deliberate for weeks 1–3. Finish the design in silence *first*, then narrate the finished thing. Narrating while designing degrades performance, and it degrades it more for people who work on instinct, which is you.

Five minutes, out loud, dictated into a file. Cover: what it's for, what a wrong answer costs and to whom, what you'd ship, and what would make you turn it off. I'll critique structure and reasoning — where you rambled, what you skipped, where you stated something as observed that was actually inferred. Not whether you were right.

---

## Sources for this module

In the notebook, tier-labeled:

| Source | Tier | What it's for |
|---|---|---|
| [Google PAIR, *People + AI Guidebook* — User Needs + Defining Success](https://pair.withgoogle.com/guidebook/chapters/user-needs-and-defining-success) | Primary (industry canon) | Does AI add unique value; automate vs augment; people-centred success |
| [Google ML Crash Course — Thresholds and the confusion matrix](https://developers.google.com/machine-learning/crash-course/classification/thresholding) | Primary | Threshold mechanics, precision/recall, class imbalance |
| [Amazon abandons AI hiring tool exposed for gender bias](https://builtin.com/artificial-intelligence/amazon-abandons-ai-hiring-tool-exposed-gender-bias) | Trade, reporting on primary | The anchor. **Primary is Reuters, Jeffrey Dastin, 10 Oct 2018** — paywalled to automated fetching, so this is the accessible retelling; treat the details as single-sourced |

**Ask me anything that isn't clear.** That's what I'm for, and a term you half-recognise is worth more asked than nodded past.
