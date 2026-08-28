---
title: "How to make `job_feed` better"
type: expansion
parent: "[[job_feed]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-15
updated: 2026-08-15
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[job_feed]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Add a bitemporal listing model

**What:** Replace the single notion of “freshness” with two clocks: `observed_at`—when `job_feed` saw the record—and `valid_during`—when the employer appeared to accept applications. Preserve `first_seen`, `last_seen`, disappearance, reopening, and source-specific revisions.

**Anchor:** Richard T. Snodgrass, *Developing Time-Oriented Database Applications in SQL*, especially transaction-time and bitemporal tables; Martin Fowler’s [“Effectivity” pattern](https://martinfowler.com/eaaDev/Effectivity.html). Snodgrass distinguishes when a fact was true in the world from when the database learned it—exactly the ambiguity hidden by “new posting.” [Full book](https://www.cs.arizona.edu/~rts/tdbbook.pdf)

**Unlock:** An executable “listing archaeology” demo and reliability runbook: detect stale jobs, silent removals, recycled requisition IDs, and postings that disappear between morning runs. It also yields a stronger portfolio claim than “deduped freshness”: *the agent reconstructs job-market state from contradictory temporal evidence.*

---

### 2. Add capture–recapture coverage estimation

**What:** Treat each feed and ATS crawler as a partial observer, then calculate source overlap, unique yield, and estimated unseen inventory. The missing metric is not “jobs fetched”; it is **how much of the relevant market remains unobserved**.

**Anchor:** Krishna Bharat and Andrei Broder, [“A Technique for Measuring the Relative Size and Overlap of Public Web Search Engines”](https://research.google/pubs/a-technique-for-measuring-the-relative-size-and-overlap-of-public-web-search-engines/) (1998). They estimate coverage from overlaps among independently incomplete indexes without privileged database access.

**Unlock:** A weekly source-ablation report: overlap matrix, marginal discoveries per source, watchlist blind spots, and “expected additional qualified jobs per engineering hour.” That becomes both a decision artifact—whether to add another ATS integration—and a compelling portfolio one-pager about measuring an ingestion system whose ground truth is unknowable. It also challenges the concept’s unsupported equation of “four feeds + 40 companies” with adequate coverage.

---

### 3. Add counterfactual preference learning—not a naïve fit score

**What:** Record every job shown, its rank, Sean’s actions, and the probability that it received that exposure. Learn from pairwise choices—“A deserved attention before B”—while retaining deliberate exploration. Rejections of unseen or low-ranked jobs must not become negative labels.

**Anchor:** Thorsten Joachims, Adith Swaminathan, and Tobias Schnabel, [“Unbiased Learning-to-Rank with Biased Feedback”](https://www.microsoft.com/en-us/research/publication/unbiased-learning-rank-biased-feedback/) (WSDM 2017). Their counterfactual framework corrects the presentation bias that makes naïve behavioral learning reinforce its own rankings.

**Unlock:** A personal job-search decision engine with an honest offline evaluation harness: compare ranking policies using logged interactions before deploying them. The artifact could be an agent spec plus interactive demo showing exploration, propensity logging, and preference updates. This moves `job_feed` from inventory plumbing to a defensible agentic-engineering case study—without pretending an LLM can infer career fit from job-description prose alone.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
