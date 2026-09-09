---
title: "Torres × Husain — evals inside product discovery (pass 4 findings note)"
date: 2026-09-09
project: productcraft
status: filed-2026-09-09 — feeds the Discovery Lead lane and the studio-evals ticket
tags: [research, productcraft, discovery, evals, tracing]
cost: $0 (native YouTube captions; no Whisper spend; ten frames from four short sections)
models: "watch and first-draft extraction: Opus 5 · findings and routing to the two destinations: Fable 5.1"
source: https://youtu.be/K3cmR_i3dF0 — Hamel Husain's channel, "How to Stop Building Products Nobody Wants," published 2026-09-02, 91:46
---

# Torres × Husain — evals inside discovery

**Why this note exists:** Sean named this talk as the origin of the Productcraft idea (L12). It feeds two places: the **Discovery Lead's lane** (how a discovery practice uses evals) and the **studio-evals ticket** shared with the content-machine trace ticket #261 (how to see what a team does under the hood). Timestamps are from the caption track; the captions render "evals" as "emails" throughout, corrected here.

## Headline

**Torres treats evals as "a missing discovery habit": one more fast, disconfirming feedback loop, in the same family as interviews and assumption tests.** She is not advising on someone else's AI; she builds and ships four AI services (classify transcript, extract key moments and opportunities, generate a tree from three interviews, update a tree) and an interview coach, and evals are how she keeps them honest. Her practice started by reading every output by hand at a scale of fifty students per cohort, then learning error analysis from Husain's course when that stopped scaling.

## What transfers to the Discovery Lead's lane

1. **Every discovery artifact gets a disconfirming loop.** "Good discovery is just building in fast feedback loops" [04:59]; "design our feedback loops to be disconfirming from the beginning" [18:42]. For the seat: an opportunity tree or discovery plan is not done until it names the loop that could prove it wrong.
2. **The interview rubric is four observable behaviors:** ask a story-based question, set the scene, build the timeline, redirect generalizations [46:39]. Her coach grades those four, pulls excerpts, and gives one tip. This is a ready-made rubric for the seat's interview-quality check and for the Insights seat's evidence grading.
3. **Strength of evidence is graded on the input, not just the output.** An opportunity from a story-based interview outranks one from a general interview; she ran experiments on general transcripts to decide what could be extracted at all [66:04]. Her beta made the point brutally: of 500 teams uploading three interviews each, about eight had story-based interviews, and eight different interview types showed up, including sales calls and team meetings [65:17, 66:49]. For the seat: classify the evidence before synthesizing it, and carry an evidence-strength label on every opportunity.
4. **Framing is the hard judgment.** "I get too many Slack notifications" is what people say; "I don't want to be interrupted during focused work" is the need, and a model will capture the first unless told about the humans [53:31–55:03]. The seat's opportunity statements must be about the customer's experience, never about the product.
5. **Start from an outcome.** The two most common questions she gets are "I don't have an outcome" and "I haven't done any interviews" [55:46]. A tree without an outcome at the root or without interview evidence under it is a made-up tree, which Husain equates with "generic metrics off the shelf" [56:54].
6. **The anti-pattern is dumping transcripts into a model.** Without stated research goals the synthesis "may or may not be grounded… may or may not be what you needed to learn" [50:02]. The seat states the decision the research serves before any synthesis runs.
7. **Assumption tests should close in a day or two** when the assumption is specific enough [23:40]; story-map the customer's steps, then generate assumptions per step across desirability, willingness, usability, feasibility, viability, ethics.
8. **Show the work as the teaching surface.** She learned AWS by watching Claude do it, and builds her synthesis to show process, not answers [59:58, 61:29]. This is L11's ledger-as-textbook argued from the other side: a seat that shows its moves teaches Sean by default.

## What transfers to the studio-evals ticket (shared with #261)

1. **Read every output by hand first.** Her evals came *after* a season of QA-ing every coach response and emailing students when she disagreed [44:24, 44:46]. Husain's parallel: interviewing is to discovery what error analysis is to evals, "same relationship" [48:32]. The studio's first eval is a hand-read of its own artifacts and ledger entries, with a written error taxonomy; judges come second.
2. **Change sets: the agent narrates its own moves, with provenance, and an audit tool replays them.** She defined a vocabulary of allowed moves (add, split, merge); a split must also split its sources [69:34, 69:58]. Deriving the change set from a diff after the fact failed because "the diff is ambiguous" [72:14]; making the model emit its moves as a scratchpad fixed it and, as a side effect, **improved output quality** [73:01]. An audit tool applies the change set to the input and checks it produces the output, feeding mismatches back [73:23]. For the studios: each seat's artifact could carry a moves section (what it kept, split, merged, or dropped from the upstream artifact, with sources), and a trace is then replayable rather than reconstructed. This is the mechanism #258 had to rebuild by hand.
3. **Attack the upstream error.** Her hardest judge (missed groupings on a tree) would not calibrate for three weeks and four experiment variants because of confounding upstream errors "no customer had ever complained about" [86:44–87:54]. Husain: "you need to focus on the upstream error, and everyone resists that" [89:01]. A trace that cannot point at the stage is not a trace; this is #261's question one, answered.
4. **Auto-eval cannot read your mind.** An LLM judge passes a leasing assistant that answers an objection with "have a nice day" [51:47]. Judges need Sean's rubric, not generic metrics; the studio's judge criteria are written from the hand-read error taxonomy, never imported.
5. **Evals as guardrails in a loop, not magic prompts.** She could not get one agent to avoid both errors, so she ran her evals as guardrails and kicked failures back for a second pass, which "has no problem correcting on the second loop" [89:24]. Systemcraft's audit-bounce (material defects loop back to the drafting seat) is already this shape; the studio evals ticket should make the bounce measurable.
6. **Cost posture favors pipelines with agentic steps.** A skills-per-step agent cost about $25 a run; her pipeline with agentic steps runs at 50 to 60 cents [74:33]. Supports #261's instinct toward a flat per-run manifest on disk over hosted tracing, with the privacy law as the second reason.
7. **Provenance is a feature, not plumbing.** Every opportunity links to the interviews it came from, down to playable clips [71:06]. The ledger's Evidence section is the studio's equivalent; the trace should make it navigable, not just present.
8. **Watch the user read the output.** The "missed groupings" failure mode came from watching a customer pause on a branch and say she would have to clean it up [85:13]. For the studios: Sean reading an artifact is an observation, and his pauses are the failure-mode catalogue.

## Named resources worth a lane pointer
- Product Talk: "Product Discovery: Everything You Need to Know" (2021) and the change-sets post shown on screen; the forthcoming post on the three-week judge calibration.
- Torres, *Continuous Discovery Habits* (self-narrated); Ericsson, *Peak* (mental representations, the origin of the tree).
- Husain and Shankar's AI Evals course and its axial-coding framing of error analysis; Husain's model-cascade lesson.
- Vistaly, the tree product that licenses her services; the interview coach.

## Not in this note
No recommendation on tooling for the studio evals ticket. That ticket decides Arize versus a flat manifest with #261; this note supplies the mechanisms (hand-read first, change sets with provenance, upstream-first tracing, guardrail loops) that any tooling must support.

## Filing note (2026-09-09)

No ratification required. Carried onto the Wayfinder map as an input to two tickets: the Discovery Lead's lane manifest (items 1–8 under the lane section) and the studio evals-and-trace design shared with #261 (items 1–8 under the evals section).
