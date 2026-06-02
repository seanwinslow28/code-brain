---
type: portfolio-artifact
artifact: discovery-prd
title: "Discovery PRD — AI-Assisted Article Drafting & Editorial Review"
subtitle: "A product requirements document for deploying a drafting agent into a skeptical 50-person content organization."
author: Sean Winslow
date: 2026-06-02
status: draft
framing: >
  All names, teams, and company specifics are generic. The workflow is modeled on a
  Fortune-500 content organization, not any single employer. The load-bearing section
  is the stakeholder discovery: five personas, five different languages, one technical
  product. Translation across those five is the skill this artifact exists to prove.
maps_to: "DR-Max Enterprise AI PM skill-gap research (2026-05-18), Q1 — Cross-Functional Translation, the single most-cited skill across Tier-1 AI PM JDs (90%)."
sources_cited: ["Klarna (AI support walk-back)", "JPMorgan Chase — LLM Suite"]
---

# Discovery PRD: AI-Assisted Article Drafting & Editorial Review

*A discovery-phase product requirements document for a ~50-person content organization at a Fortune-500 company. Written from the seat of the PM who has to get five people who do not speak the same language to agree on the same product.*

---

## 0. Why this document exists

Every AI product pitch I've watched die in a room died the same way: an engineer explained RAG to a lawyer, the lawyer heard "the machine writes things and we hope they're true," and the meeting was over before the coffee got cold. Five languages at one table, and we called it a kickoff.

This PRD is built backward from that failure. The product underneath it is unremarkable on purpose: an assistant that drafts articles and routes them through editorial review. The hard part was never the model. It's that the editor wants her voice protected, the strategist wants throughput, the SEO lead wants to not get delisted by Google, the lawyer wants to not get sued, and the executive wants a number she can say to a board. The same sentence about hallucination rates has to land as five different promises. That translation is the whole job.

The body below is sober. The discovery section is where the work lives.

---

## 1. Product context & the workflow

**The surface.** A drafting assistant in the existing CMS. A writer or the strategist hands it a brief from the editorial calendar; it returns a first draft grounded in the organization's own published archive and style guide; the draft enters the review queue with every factual claim traced to a source. The editor reviews, edits, approves. Nothing publishes without a human. **What it is not:** an autonomous publisher, a replacement for writers, or a system that drafts from the open web. (The base model still carries general pretrained knowledge; the engineering constraint is that *publishable factual claims* are grounded in an approved internal corpus, and vendor terms must prohibit training on our prompts, outputs, or retrieved content.) The scope is "first-draft acceleration for a defined content tier," not "content automation."

**Why this org, why now.** The team produces ~120 pieces a month and first-draft cycle time is the bottleneck: an explainer takes three to four working days to reach a reviewable draft, most of it spent re-assembling context already published elsewhere. The org has the raw material (a deep archive, a documented style guide) and the pain (a backlogged calendar) that make this the right first AI surface: high-volume, low-liability work where a bad draft costs an editor's hour, not a lawsuit.

---

## 2. Problem statement

> First-draft cycle time for Tier-1 content runs three to four working days per piece, the bulk of it spent re-assembling context the organization has already published. The calendar is structurally backlogged and the team cannot hire its way out at acceptable cost. **Target outcome: reduce Tier-1 first-draft cycle time from ~4 days to under 8 hours, with no measurable degradation in brand-voice fidelity or factual accuracy, and without the editorial team absorbing the drafting cost as rework.**

Note what this is not: not "adopt AI," not "increase output by N%." It pairs a cycle-time target with two guardrails (voice fidelity, factual accuracy) and one anti-goal: do not move the bottleneck from drafting onto the editor's desk. The guardrails sit in the statement on purpose — the failure mode for this class of product is buying speed by quietly transferring the cost to the reviewer.

---

## 3. Discovery: five stakeholders, five languages

This is the load-bearing section. Five people, five fears, five vocabularies. For each: what they said, what they were actually asking, and the translation move that turned an AI concept into their language. The translations are the deliverable.

### 3.1 The Editor — owns brand voice and quality

> "I have spent six years getting our voice to sound like a person and not a press release. I am not going to spend the next six rewriting a robot's homework. If this thing turns me into a cleanup crew, I will quietly strangle it."

**What she was actually asking:** Will this protect the thing I'm proud of, or will it make my job worse while looking like progress?

**The concept to translate — eval metrics & brand-voice scoring.** I did not say "we'll measure cosine similarity against a reference embedding of your house style." I said: "Before any writer sees a draft, it gets scored against a voice rubric we build from your own best published pieces — the same rubric you'd use in your head, written down. Drafts that don't clear the bar don't reach you. You're not the filter; you're the final read." Eval became a rubric she already owns, applied earlier in the pipeline so she sees fewer bad drafts, not more.

**The concept to translate — hallucination rate.** I did not say "the base model hallucinates at roughly X% on open-domain factual claims." I said: "It will sometimes state things confidently that aren't true — and it can even attach a real-looking source to a claim the source doesn't support, so we don't treat a citation as proof. Each factual sentence gets a proposed source, a check scores whether that source actually backs the claim, and low-confidence ones surface to you instead of hiding. You review flagged claims; you don't hunt for them." Hallucination became a sampled, scored, human-validated control — explicitly not a promise that a citation equals a fact.

### 3.2 The Content Strategist — owns the pipeline and calendar

> "I don't care how it works. I care that a topic I planned on Monday is a reviewable draft by Tuesday instead of next week. And I do not want a sixth tool. If I have to leave the calendar to use it, nobody will use it."

**What he was actually asking:** Does this unblock my throughput without adding workflow friction?

**The concept to translate — RAG.** I did not say "we ground generations on a vector store of your corpus." I said: "It drafts from our own published work and style guide, not the open web — so on a topic we've covered before, it builds on what we already said instead of starting over or contradicting us." RAG became "it remembers what we've published," the throughput unlock he wanted.

**The concept to translate — embeddings.** I did not say "embeddings let us do similarity search by meaning." I said: "It finds related coverage by what pieces are *about*, not just matching keywords — so a draft on 'retirement planning' surfaces our '401k rollovers' piece even when the words don't overlap." Embeddings became "it finds related work the way a good editor would."

### 3.3 The SEO Lead — owns organic traffic

> "Google has been at war with low-effort AI content since the helpful-content update. Flood the index with thin, fabricated, near-duplicate junk and we don't get a productivity win, we get a manual action and six months of recovery. Prove to me this doesn't tank our E-E-A-T."

**What she was actually asking:** Does this protect the ranking signals I'm accountable for, or does it put them at risk?

**The concept to translate — factual grounding, in her frame.** I did not claim Google "punishes hallucinations" — it doesn't; the helpful-content system rewards genuinely helpful, original content regardless of how it was made. I said: "Thin, fabricated, or near-duplicate pages are the E-E-A-T risk, not the fact that AI touched the draft. So grounding and a duplication check are ranking safeguards: claims are drafted against our own sources, and a pre-publish check scores factual support and near-duplicate similarity against our index before anything can be queued." I mapped the risk onto the ranking signals she owns, without promising a deterministic truth-detector.

**The concept to translate — what the gate actually checks, in SEO terms.** I did not say "we'll run an LLM-as-judge eval." I said: "Before a draft can enter the publish queue it runs an *SEO* check, not just a quality check — search-intent match, keyword cannibalization and canonical conflict against pages we already rank for, near-duplicate similarity, freshness, and schema and internal-link completeness. Factual support is scored in the same pass, but sampled and human-confirmed, not guaranteed." The eval became a gate in her currency — the specific ranking risks she owns — instead of a vague "factual + original" promise.

### 3.4 Legal Counsel — owns liability and IP

> "My questions are simple, and I need real answers, not 'probably.' Where did this sentence come from? Can we defend it if challenged? Are we training on anything we don't have rights to? And when, not if, it publishes something false, what's our exposure? Air Canada's chatbot invented a refund policy and the airline was held liable. I'm not signing off on a sentence-generator with no chain of custody."

**What she was actually asking:** Can I establish provenance and bound the liability, in writing?

**The concept to translate — training data & RAG provenance.** I did not say "we use a frozen base model with no fine-tuning on your data, retrieval-augmented at inference." I said: "It is not trained on our content — it retrieves from our approved archive at draft time, the way a researcher pulls a book off our own shelf, and the vendor is contractually barred from training on what we send it. Per article, we keep a record of which approved sources each claim was drafted against and who approved it. The base model carries general language ability from its own training, so the honest control isn't 'nothing else exists in there' — it's that every *publishable* claim is tied to a source we can produce on demand." Provenance became an auditable chain of custody, scoped honestly rather than promised absolutely.

**The concept to translate — hallucination, as bounded liability.** I did not give her a rate. I said: "The risk is real, so we bound it: a human approves every published piece, every factual claim carries a source we can produce, and we start only with the lowest-liability content — where the likely failure is a correction, and where regulated or advice topics are blocked from the workflow until the controls are proven." I did not promise her we'd never see a courtroom; I gave her named controls and a deliberately small blast radius, which is the only thing a 'probably' allergy trusts.

### 3.5 The Executive Sponsor — owns budget and the board narrative

> "I have ninety seconds with the board. I need one number that says this is working and one sentence that says it won't blow up in our face. I don't want to hear about embeddings. I read about Klarna walking back their AI support. Don't make me the next case study."



**What she was actually asking:** What's the ROI, what's the leading indicator that it's safe, and what's the story?

**The concept to translate — the adoption funnel & eval metrics, as leading indicators.** I did not say "we'll track eval pass rates and adoption cohorts." I said: "The number for the board is cycle time: four days to under eight hours on our highest-volume work. The safety story is three indicators we watch weekly: how many eligible briefs actually run through it, how often the editor throws a draft out and rewrites from scratch, and how long a writer takes to reach steady light-edit approvals. If the throwaway rate climbs, we stop expanding before it becomes a Klarna headline." The metrics became one ROI number plus a tripwire she can say in a sentence.

**The concept to translate — token economics / cost.** Not "input plus output tokens at the blended rate," but "cost-per-published-article, fully loaded, against a writer-hour: a rounding error versus the cycle-time gain, and the dashboard shows it the moment that stops being true." Cost became a unit she can defend in a budget conversation.

**The translation matrix, at a glance:**

| AI concept | Editor | Strategist | SEO Lead | Legal | Executive |
|---|---|---|---|---|---|
| Hallucination | "claims scored + flagged; cite ≠ fact" | (deferred to editor) | "thin/fabricated = E-E-A-T risk" | "named controls + small blast radius" | "the throwaway-rate tripwire" |
| RAG / retrieval | "drafts in our voice from our work" | "it remembers what we published" | "drafts from our pages, not the web" | "retrieves our shelf, isn't trained on it" | (deferred to ROI) |
| Eval metrics | "your rubric, applied earlier" | (deferred) | "intent + cannibalization + duplicate gate" | (deferred to controls) | "weekly leading indicators" |
| Embeddings | (deferred) | "finds related work by meaning" | "near-duplicate similarity check" | (deferred) | (deferred) |
| Cost / tokens | (deferred) | (deferred) | (deferred) | (deferred) | "cost-per-article vs. writer-hour" |

The deferrals are deliberate: knowing which concept each persona does *not* need to hear is half the skill.

---

## 4. User stories

Six stories, each in standard form with verifiable acceptance criteria.

**Story 1 — Sourced drafts (Editor).**
*As an editor, I want every AI draft to arrive with each factual claim linked to its source, so that I can verify accuracy without re-reporting the whole piece.*
**Acceptance criteria:** (a) Every draft renders inline citations; clicking a factual sentence reveals its proposed source *and* a support score for whether that source actually backs the claim. (b) Drafts whose unsupported-claim rate exceeds a Phase-1-calibrated threshold are held from the editor's queue and returned. (c) The editor can mark a citation "doesn't support this" in one click, and those corrections feed the support scorer.

**Story 2 — House voice from the archive (Writer).**
*As a writer, I want the assistant to draft in our house style using only our approved corpus, so that my first draft already sounds like us and I'm editing voice, not inventing it.*
**Acceptance criteria:** (a) Drafts meet the agreed house-voice rubric threshold (rubric and threshold owned and calibrated by the editor in Phase 1) before reaching the writer. (b) The writer can regenerate any section with a one-line instruction without leaving the editor. (c) Every *factual claim* is drawn from the approved corpus and traceable via the Story 1 trail; the model still supplies ordinary connective language, which the voice rubric governs.

**Story 3 — Calendar-to-draft handoff (Content Strategist).**
*As a content strategist, I want to turn a planned calendar item into a reviewable draft in one action, so that planning and drafting don't live in two disconnected tools.*
**Acceptance criteria:** (a) A calendar brief has a "generate draft" action that produces a draft in the review queue. (b) The strategist never leaves the CMS/calendar to trigger or track it. (c) Draft status (generating / in review / approved) shows on the calendar item.

**Story 4 — Pre-publish factuality & originality gate (SEO Lead).**
*As an SEO lead, I want an automated factuality-and-originality check before any draft can enter the publish queue, so that we never ship fabricated claims or near-duplicate content that risks ranking penalties.*
**Acceptance criteria:** (a) No AI-assisted draft reaches the publish queue until it passes the gate. (b) The gate checks, with a reviewable score for each: search-intent match, keyword cannibalization / canonical conflict against pages we already rank for, near-duplicate similarity against our own index, and schema / internal-link completeness — plus the Story 1 claim-support score. (c) Gate pass/fail and per-check reason are logged per article.

**Story 5 — Provenance trail (Legal Counsel).**
*As legal counsel, I want a per-article provenance record on every published AI-assisted piece, so that if a claim is challenged I can show where it came from and who approved it.*
**Acceptance criteria:** (a) Every published AI-assisted article has a retrievable record of the internal sources each claim drew from, the model version, and the approving editor. (b) The record is exportable for a legal hold. (c) Categories flagged "restricted" (regulated, advice, legally sensitive) are blocked from the workflow until explicitly cleared.

**Story 6 — Adoption & trust dashboard (Executive Sponsor).**
*As the executive sponsor, I want a weekly adoption-and-trust dashboard, so that I can tell the board whether this is working and catch trouble before we expand.*
**Acceptance criteria:** (a) The dashboard shows brief-penetration rate, fallback-to-human rate, and time-to-first-light-edit-approval, weekly. (b) It flags when fallback-to-human rate exceeds the agreed threshold (the expansion tripwire). (c) It reports cost-per-published-article against a writer-hour baseline.

---

## 5. Success metrics

The metrics are an adoption funnel, not a content-output scoreboard. The distinction matters: output metrics (articles shipped, words generated) reward exactly the behavior that gets organizations into trouble. These reward trust earned.

**Primary.**
- **Brief-penetration rate** — % of *eligible Tier-1 briefs* that ran through the assistant. *Target: 70% by Day 90.* Deliberately not "writers who logged in once a week," which a single throwaway brief games — this measures workflow penetration, not compliance.
- **Fallback-to-human rate** — % of AI drafts the editor rewrites from scratch rather than edits, measured by edit-distance against the original so it isn't self-reported under deadline. *Target: declining, below 20% by Day 90.* The quality signal and the expansion tripwire: a rising rate means the bottleneck moved onto the editor (the §2 anti-goal).
- **Time to first light-edit approval** — median days to a writer's first draft the editor approves with light edits, not a rewrite. (Nothing publishes without a human; this measures *trust earned*, not autonomy granted.) *Target: under 21 days*, paired with a sustained-trust companion — two consecutive light-edit approvals, so one rubber-stamped draft can't fake it. It's the adoption-funnel metric that replaces DAU/MAU for agentic products.

*Thresholds (rubric bar, unsupported-claim ceiling, fallback gate) are set from a human-labeled baseline in Phase 1 with an explicit false-positive tolerance, not named in advance — picking the numbers before the pilot would be the fake-precision tell.*

**Guardrail.** Factuality-gate catch rate, read against an independent human-labeled sample so a falling rate isn't mistaken for "drafts improving" when it might be "gate missing more"; brand-voice rubric score (must hold or rise); cost-per-published-article vs. a writer-hour baseline.

**Explicitly not tracked as success:** click-through rate, total AI-generated articles, total words — either downstream of factors the tool doesn't control (CTR) or dangerous as targets (volume).

---

## 6. Rollout plan — 90 days, phased, champion-led

The rollout is designed around one lesson the research surfaced repeatedly: **the organizations that got burned expanded scope before they earned trust; the ones that succeeded expanded internally and iteratively, and let metrics, not the calendar, open each gate.**

**Phase 0 — Baseline & champions (Weeks -2 to 0).** Instrument the current state: measure today's cycle time and a baseline editor-satisfaction score so the "no degradation" guardrail is provable later. Lock the Tier-1 definition — high-volume, genuinely low-liability work (evergreen explainers, how-tos, listicles; *not* product, financial, or health claims, which legal must adjudicate). Recruit a champion cohort: the editor plus five to six respected writers who shape the tool and advocate for it. *(Prosci ADKAR "Awareness + Desire" — trust is built internally before it scales.)*

**Phase 1 — Champion cohort only (Days 1-30).** Live only for the champions, only on Tier-1 content. Daily feedback; weekly tuning of the voice rubric and claim-support gate. **This is where the Klarna lesson is load-bearing: Klarna deployed AI support at scale, cut resolution time from 11 minutes to 2, then walked it back when complex cases degraded CSAT because generic answers failed on nuance. The takeaway: do not open the tool to complex or high-liability content at launch. Tier-1 only, humans on every output, until the metrics earn the next phase.**

**Phase 2 — Full Tier-1 rollout (Days 31-60).** Gate to enter: fallback rate below threshold and time-to-first-light-edit-approval trending down. The champions become the training layer, onboarding the rest of the Tier-1 pool. **The enablement model comes from JPMorgan Chase's LLM Suite rollout — adoption there was driven by training and peer enablement (the ADKAR "Knowledge + Ability" stages), not a mandate. Their tool was a broad horizontal assistant rather than a workflow-embedded pipeline like this one, so I'm borrowing the change-management lesson, not the architecture: champions teaching peers is the adoption engine, not an executive memo.**

**Phase 3 — Conditional Tier-2 expansion (no earlier than Day 61, and only if Phase-2 metrics held).** Scope expands toward nuanced (Tier-2) content only after editor satisfaction is validated against the Phase-0 baseline and the claim-support gate has a track record. Expansion is earned by sustained performance, not scheduled by date — the gate is a metric, not the calendar. Regulated or advice content stays gated behind explicit legal sign-off (Story 5c).

**The standing rule across all phases:** the expansion gate is a metric (fallback rate + editor CSAT), never the calendar. If metrics regress, the rollout holds or rolls back. That single rule is the difference between this plan and the cautionary tales it cites.

---

## 7. Open questions & risks

- **Voice rubric subjectivity.** Only as good as its examples; if editor and rubric disagree, trust erodes. Mitigation: the editor owns and revises the rubric in Phase 1.
- **Archive quality + self-contradiction.** RAG faithfully reproduces an outdated, off-brand, or self-contradicting corpus (two pieces that disagree produce a confidently-wrong draft with a valid citation). Mitigation: a curated, approved subset for Phase 1, with canonical-source rules.
- **Net-new topics.** Strict grounding can't draft what the archive doesn't cover; those briefs route to a human, not a fabricated draft.
- **The gate as bottleneck.** Too aggressive a gate becomes the new bottleneck. Mitigation: tune thresholds against the fallback metric; keep five-plus champions so the program survives a departure.

---

## 8. Where the AI-evangelism arc applies

I have run this discovery before, just without the title or the mandate to make it stick. For the better part of a decade, first in financial services and then in media, I was the person quietly translating between the people who could build with AI and the people who were afraid of it, with no budget, no roadmap, a headcount of one. I learned these five languages the hard way: by watching the pitch die in the room, by being the engineer the lawyer didn't believe and the evangelist the executive tuned out. I got a handful of coworkers to fold AI into their work and lost far more meetings than I won, because being early and being persuasive are different skills and I only had the first. This PRD is the version I'd have shipped with named accountability instead of freelancing the future on the side. The translation table in §3 isn't a framework I read about. It's the scar tissue.

---

*Rollout draws on two documented enterprise-AI-adoption cases: Klarna's AI-support walk-back (the Tier-1-only lesson) and JPMorgan Chase's LLM Suite (training-led adoption).*
