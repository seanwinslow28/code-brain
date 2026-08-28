---
title: "M2 — Data, Feedback & the Model Path"
type: lesson
module: M2
status: ready
created: 2026-08-17
anchor: Zillow Offers (JISE 2024 case study)
backup_anchor: content-moderation labeling pipelines
mirror_eligibility: "mechanics yes, human/economic layer no — see §0"
---

# M2 — Data, Feedback & the Model Path

*Module 2 of 5 · AI PM System Design Thinking · Weeks 2–3*

---

## 0. What you've touched, and what you haven't

The curriculum map called this module "teach from zero." That's very slightly wrong, and being precise about it matters more than being tidy.

**You have touched the mechanics.** Your vault indexer runs an embedding pipeline — it takes documents, splits them into pieces, and turns each piece into a vector so it can be searched by meaning rather than keyword. You chunk. You store `chunk_id` provenance. You have quality gates: `evaluate_article_depth()` rejects thin articles and writes `rejected_reasons` into the manifest, which is a labeled rejection log whether or not you called it one. `audit_dr_citations.py` scores sources into tiers. Your discovery council refuses any claim not traceable to a fetched URL.

That is more data-plane experience than most PMs have, and none of it was accidental.

**You have not touched the human and economic layer, and that's the whole rest of this module:**

- **Labeling by other people.** Every quality judgment in your fleet is made by you or by a model you configured. You have never written instructions for a stranger, discovered they interpreted the task differently than you meant, or measured how often two people looking at the same item disagree.
- **Selection effects created by your own product.** Your agents don't have users whose choices decide which data comes back. That mechanism destroyed Zillow, and it is invisible until you know to look.
- **Feedback that changes the distribution.** Your agents don't learn from being used. Products that do have a loop that can quietly poison itself.
- **Data contracts.** Nobody upstream of you has ever promised you a schema and then broken it in a sprint you weren't in.

So: mechanics, recognition. Everything downstream of "another human is involved," new.

---

## 1. Where the data actually comes from

Three sources, and the distinction drives almost every downstream decision.

**Data you already have.** Logs, transactions, documents, support tickets. Cheapest and most dangerous, because it was collected for a different purpose and carries the shape of that purpose. Amazon's résumé screener (M1) failed on exactly this: ten years of résumés were *real* data, and their reality was the problem.

**Data you go get.** Purchased, licensed, scraped, or collected on purpose. More expensive, more controllable, and it raises consent and licensing questions the first two rarely do.

**Data your product generates by running.** Every interaction produces a record. This is the flywheel everyone wants — and §3 is about how it eats you.

Google's PAIR team — a research group inside Google that publishes design guidance for AI products — makes a point in their data chapter that's worth memorising because it inverts the usual instinct: **more time and resources go into model development than into data quality, and that allocation is backwards.** The model is the part that looks like engineering. The data is the part that decides whether it works.

The PM question:

> **What does this system need to know, where does that live today, and who would have to agree to give it to us?**

That last clause is the one that turns a two-week estimate into a two-quarter one.

---

## 2. Labeling: the part nobody warns product managers about

For a system that learns from examples, someone has to say what the right answer *was*. Those are **labels**, and they are the ground the whole thing stands on.

The naïve view is that labeling is data entry — cheap, outsourceable, done. Here is what actually happens.

**Instructions are a product, and yours are ambiguous.** You write "label this ticket as urgent if it needs attention today." One labeler reads that as *the customer is angry*, another as *there is money at risk*, a third as *the SLA expires*. You now have three datasets braided together, and the model will learn the average of three incompatible definitions — which is a definition nobody holds. PAIR's guidance on this is concrete: give at least three positive, three negative, and **three deliberately ambiguous** examples, explain the goal rather than just the rule, state what gets an item rejected, and give labelers a channel to flag cases the instructions don't cover. That last one is the highest-value and the most often skipped, because the ambiguous cases are the ones your instructions were silently wrong about.

**Agreement is measurable, and you should measure it.** Have two people label the same items and see how often they match. That's **inter-rater agreement**, and it sets a ceiling: if two careful humans agree only 70% of the time, no model trained on those labels is going to be meaningfully better than 70%, because the task itself isn't defined well enough to do better. **Low agreement is a specification bug, not a labeler problem** — and the fix is rewriting the instructions, not hiring better people.

**Labelers drift and fatigue.** By item 200 the same person is applying a looser standard than at item 20. Counter-design: rotate, cap volume, and salt the queue with items whose answer you already know so you can measure catch rate over time.

**Who labels changes what "correct" means.** Domain experts, crowdworkers, and your own users produce different ground truth for the same task. For anything requiring judgment, cheap labels are frequently worse than no labels, because they look like data.

**The artifact that fixes most of this** is a written record of what a dataset *is*. Timnit Gebru and colleagues proposed exactly that in a 2018 paper — the analogy is the electronics industry, where every component ships with a datasheet stating its operating characteristics. A **datasheet for a dataset** answers: why was this collected, what's in it, how was it gathered, who's represented, what shouldn't it be used for. It's now standard practice at serious shops, and writing one is this module's artifact.

---

## 3. The mechanism that killed Zillow: your product picks its own data

**One-sentence setup:** Zillow, the American real-estate listings company, ran a house-flipping business called Zillow Offers from 2018, using an algorithm to make instant cash offers on homes; it shut the business down in November 2021, wrote down a large loss, and laid off about a quarter of its workforce.

The usual telling is "the model mispredicted prices." That's true and it's the shallow half. Here's the structural half, and it's the most important idea in this module.

Zillow's algorithm made an offer. **The seller then chose whether to accept.** Think about what that choice does to the data.

When the algorithm offered *too much*, the seller was delighted and accepted. When it offered *too little*, the seller declined and sold elsewhere. So the set of homes Zillow actually bought was not a random sample of homes — **it was systematically enriched for the cases where the algorithm was wrong in the expensive direction.** The company's own purchasing behaviour filtered reality into a biased sample, and the errors it could see were disproportionately the ones that cost it money.

That pattern has a name — **adverse selection**, borrowed from insurance, where the people most eager to buy a policy are the ones most likely to claim on it. *(Fair warning: the JISE case study in your sources analyses the closure without using that term. The mechanism is visible in the facts; the framing is mine and standard in economics, so say which is which if you use it in a room.)*

Then the second mechanism compounded it. The model was trained on historical prices during a period when the market moved sharply, so the relationship it had learned no longer held. When the world changes underneath a model and its learned patterns go stale, that's **concept drift**. Renovation crews were also scarce during COVID, so homes sat longer, which meant the price a home would fetch drifted further from the price the model had assumed.

**The generalisable lesson, and the one to carry into every design review:**

> **If your product's own behaviour decides which data comes back, your data is not a sample of the world. It is a sample of your product's mistakes.**

Ask it of any system with a human in the loop: a recommender only learns about items it recommended; a fraud model only learns outcomes for transactions it let through; a résumé screener only learns about candidates someone interviewed. **The unshown, the blocked, and the rejected are invisible to the loop, and their absence is not neutral.**

---

## 4. Feedback loops that improve the system, and the ones that eat it

A **feedback loop** here means user behaviour flowing back in as training signal.

The good version is deliberate: an explicit correction, a thumbs-down with a reason, a human review queue whose verdicts become labels. It works because someone designed what counts as signal.

The degenerate versions:

- **You train on your own output.** A model's suggestions get accepted, the accepted results become training data, and it learns to agree with itself. Confidence goes up, contact with reality goes down.
- **Popularity masquerades as quality.** A recommender surfaces an item, it gets clicked because it was surfaced, the click is read as evidence it was good, so it gets surfaced more. You've measured your own placement.
- **The thumbs-up nobody reads.** The most common failure isn't a poisoned loop, it's a decorative one. Feedback is collected, stored, and never routed anywhere that changes a decision. It looks like a loop in the architecture diagram and is a dead end in the system.

**The test for any feedback mechanism:** *what specific decision does this signal change, who sees it, and how long until it takes effect?* If there's no answer, it's decoration.

---

## 5. Retrieval is data infrastructure, and it fails in documented ways

If a system looks things up before answering — the pattern you'll hear called **RAG**, retrieval-augmented generation — the lookup layer is part of the data plane, and it has its own catalogue of failures.

A peer-reviewed 2026 taxonomy (presented at TrustNLP, a workshop on trustworthy natural-language processing) catalogues **33 distinct failure modes across seven pipeline stages**, each graded by how much evidence supports it. The ones that bite earliest:

- **Stale data.** The store holds documents that were true once. Nothing announces this.
- **Layout parsing errors.** Tables and multi-column PDFs get read into nonsense before anything else happens.
- **Chunking boundary errors.** Documents get split into pieces, and a bad split cuts a fact in half so neither piece can answer the question. **This is a product decision disguised as a technical parameter.**
- **Embedding drift.** You upgrade the model that turns text into vectors, and old vectors are no longer comparable to new ones. Quality degrades with no code change and no alert.
- **Position-of-gold bias.** Systems attend disproportionately to the beginning and end of what they're given and skim the middle — so the right answer can be retrieved and still ignored.

And the finding I'd want you to carry into a room, because it's the kind of thing that marks someone who reads sources rather than summaries: **12 of the 33 modes have no dedicated peer-reviewed evidence — and all 8 agentic modes are among them.** The paper calls it an evidence desert. The fastest-growing way to build these systems is the part we know least about. Saying *"I'd instrument that rather than assume it, because the evidence there is thin"* is a more senior move than confidently reciting a mitigation.

---

## 6. Contracts, provenance, freshness

Three properties that turn data from a resource into an engineered dependency:

**Data contract** — a written agreement about what an upstream system will send: fields, types, meanings, and what happens when it changes. Without one, someone renames a column in a sprint you weren't in and your quality drops for a month before anyone connects the two.

**Provenance** — where each item came from and when. You already do this: `chunk_id` provenance in your vault index, the URL traceability gate in your discovery council. Its value is that when something goes wrong you can ask *which source did this come from* and get an answer instead of a shrug.

**Freshness** — how old is too old, stated as a number. Your fleet has staleness checks. Most products don't, and discover the threshold by having a customer find it.

---

## 7. Vocabulary, compressed

**Ground truth · labels · labeling instructions · inter-rater agreement · labeler drift · datasheet for a dataset · selection effect · adverse selection · concept drift · distribution shift · feedback loop · degenerate loop · training on your own output · data contract · provenance · freshness · chunking · embedding · embedding drift · stale index · position-of-gold bias**

---

## Exercises

**How these run:** I work one fully out loud first, saying why at each step, then you take one of the same shape with me available throughout. No cold start, no prediction, no score.

### Exercise A — Teardown, modes labeled

Pick any product that recommends things to you — a streaming service, a shopping site, a music app. Reconstruct its data plane: where its training signal comes from, what its product behaviour prevents it from ever learning, and where a degenerate loop could form.

Label every claim **observed** (you can see it), **inferred** (you're reasoning from behaviour), or **designed** (what you'd do, not what they did). I'll do the first one; you take the second.

### Exercise B — Forward design from a dirty brief

> A mid-size company wants to auto-triage inbound support email into five categories and route each to the right team. There are three years of past tickets. They were categorised by whoever closed them, the category list changed twice in that period, and roughly 30% are tagged "Other." Two people can be pulled onto labeling for two weeks.
>
> **What's your data plan?**

Produce: what you'd use as ground truth and why; your labeling instructions for one genuinely ambiguous category; how you'd measure agreement and what number would make you stop and rewrite rather than continue; what you'd do about "Other"; the freshness rule; and what you'd put in the datasheet.

**Constraint shift, walked the first time:** partway through I'll change something — the two labelers become one, or legal says the ticket bodies can't leave the building — and we'll re-derive it together before you do one yourself.

### The written artifact

**A data contract plus a labeling plan**, roughly two pages, structured as a datasheet: what the dataset is for, what's in it, how it was collected, who's represented, freshness rule, known limitations, and what it must not be used for.

This becomes **Golden Loop's golden-dataset spec** — the document that defines what goes into the sealed holdout and why. Not a throwaway.

---

## Sources for this module

| Source | Tier | What it's for |
|---|---|---|
| [Google PAIR — Data Collection + Evaluation](https://pair.withgoogle.com/guidebook-v2/chapters/data-collection/) | Primary (industry canon) | Sourcing, labeling instructions, designing for labelers. **Note:** this is the pre-generative edition of the chapter; the current guidebook reorganised it, and this version's labeling guidance is more concrete |
| [Gebru et al., *Datasheets for Datasets*](https://arxiv.org/pdf/1803.09010) | **A** peer-reviewed | The artifact you'll produce, and the question list to produce it from |
| [*A Systematic Taxonomy of Failure Modes in RAG Systems*](https://aclanthology.org/2026.trustnlp-main.27.pdf) (ACL TrustNLP 2026) | **A** peer-reviewed | 33 modes / 7 stages, evidence-graded — including the honest admission of where evidence runs out |
| [*Exploring the Role of AI in the Closure of Zillow Offers*](https://jise.org/Volume35/n1/JISE2024v35n1pp67-72.pdf) (JISE 2024) | **A** academic | The anchor. **Does not use the term "adverse selection"** — that framing is mine and standard in economics; keep the distinction when you speak |

**Two honesty notes.** Loss figures for Zillow Offers vary by what's counted (inventory write-down alone, versus the full wind-down), so quote the mechanism rather than a number unless you've checked which figure you mean. And ask me anything here — this module is the one where you have the least prior footing, and a term half-recognised is worth more asked than nodded past.
