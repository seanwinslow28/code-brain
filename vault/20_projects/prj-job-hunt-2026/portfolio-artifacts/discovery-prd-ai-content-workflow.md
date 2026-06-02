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
sources_cited: ["Klarna (AI support walk-back)", "Bank of America — Erica", "JPMorgan Chase — LLM Suite"]
---

# Discovery PRD: AI-Assisted Article Drafting & Editorial Review

*A discovery-phase product requirements document for a ~50-person content organization at a Fortune-500 company. Written from the seat of the PM who has to get five people who do not speak the same language to agree on the same product.*

---

## 0. Why this document exists

Every AI product pitch I have watched die in a room died the same way: an engineer explained retrieval-augmented generation to a lawyer, the lawyer heard "the machine writes things and we hope they're true," and the meeting was over before the coffee got cold. They were speaking five languages at one table and calling it a kickoff.

This PRD is built backward from that failure. The product underneath it is unremarkable on purpose: an assistant that drafts articles and routes them through editorial review. The hard part was never the model. It's that the editor wants her voice protected, the strategist wants throughput, the SEO lead wants to not get delisted by Google, the lawyer wants to not get sued, and the executive wants a number she can say to a board. The same sentence about hallucination rates has to land as five different promises. That translation is the whole job, and it's what this document exists to show.

The body below is sober. The discovery section is where the work lives.

---

## 1. Product context & the workflow

**The surface.** A drafting assistant in the existing CMS. A writer or the strategist hands it a brief from the editorial calendar; it returns a first draft grounded in the organization's own published archive and style guide; the draft enters the review queue with every factual claim traced to a source. The editor reviews, edits, approves. Nothing publishes without a human. **What it is not:** an autonomous publisher, a replacement for writers, or anything trained on the open internet. The scope is "first-draft acceleration for a defined content tier," not "content automation."

**Why this org, why now.** The team produces ~120 pieces a month and first-draft cycle time is the bottleneck: an explainer takes three to four working days to reach a reviewable draft, most of it spent re-assembling context already published elsewhere. The org has the raw material (a deep archive, a documented style guide) and the pain (a backlogged calendar) that make this the right first AI surface: high-volume, low-liability work where a bad draft costs an editor's hour, not a lawsuit.

---

## 2. Problem statement

> First-draft cycle time for Tier-1 content runs three to four working days per piece, the bulk of it spent re-assembling context the organization has already published. The calendar is structurally backlogged and the team cannot hire its way out at acceptable cost. **Target outcome: reduce Tier-1 first-draft cycle time from ~4 days to under 8 hours, with no measurable degradation in brand-voice fidelity or factual accuracy, and without the editorial team absorbing the drafting cost as rework.**

Note what this is not: not "adopt AI," not "increase output by N%." It pairs a cycle-time target with two guardrails (voice fidelity, factual accuracy) and one anti-goal: do not move the bottleneck from drafting onto the editor's desk. The guardrails sit in the statement on purpose, because the failure mode for this class of product is buying speed by quietly transferring the cost to the reviewer.

---

## 3. Discovery: five stakeholders, five languages

This is the load-bearing section. Five people, each with a different fear, a different definition of success, and a different vocabulary. For each: what they said, what they were actually asking, and the specific translation move that turned an AI concept into their language. The translations are the deliverable.

### 3.1 The Editor — owns brand voice and quality

> "I have spent six years getting our voice to sound like a person and not a press release. I am not going to spend the next six rewriting a robot's homework. If this thing turns me into a cleanup crew, I will quietly strangle it."

**What she was actually asking:** Will this protect the thing I'm proud of, or will it make my job worse while looking like progress?

**The concept to translate — eval metrics & brand-voice scoring.** I did not say "we'll measure cosine similarity against a reference embedding of your house style." I said: "Before any writer sees a draft, it gets scored against a voice rubric we build from your own best published pieces — the same rubric you'd use in your head, written down. Drafts that don't clear the bar don't reach you. You're not the filter; you're the final read." Eval became a rubric she already owns, applied earlier in the pipeline so she sees fewer bad drafts, not more.

**The concept to translate — hallucination rate.** I did not say "the base model hallucinates at roughly X% on open-domain factual claims." I said: "It will sometimes state things confidently that aren't true. We handle that by making it show its work: every factual sentence links to where it came from in our own archive. If it can't cite it, the sentence gets flagged before it reaches you." Hallucination became a visible, reviewable thing with a guardrail attached, not an abstract risk percentage.

### 3.2 The Content Strategist — owns the pipeline and calendar

> "I don't care how it works. I care that a topic I planned on Monday is a reviewable draft by Tuesday instead of next week. And I do not want a sixth tool. If I have to leave the calendar to use it, nobody will use it."

**What he was actually asking:** Does this unblock my throughput without adding workflow friction?

**The concept to translate — RAG (retrieval-augmented generation).** I did not say "we ground generations on a vector store of your corpus." I said: "It drafts from our own published work and our style guide, not from the open web. So when it covers a topic we've written about before, it builds on what we already said instead of starting from scratch or contradicting ourselves." RAG became "it remembers what we've already published," which is exactly the throughput unlock he wanted.

**The concept to translate — embeddings / semantic retrieval.** I did not say "embeddings let us do similarity search by meaning." I said: "When it pulls related coverage, it finds pieces by what they're *about*, not just matching keywords. So a draft on 'retirement planning' surfaces our piece on '401k rollovers' even if the words don't overlap." Embeddings became "it finds related work the way a good editor would," tied to a calendar workflow he already runs.

### 3.3 The SEO Lead — owns organic traffic

> "Google has been at war with low-effort AI content since the helpful-content update. Flood the index with thin, fabricated, near-duplicate junk and we don't get a productivity win, we get a manual action and six months of recovery. Prove to me this doesn't tank our E-E-A-T."

**What she was actually asking:** Does this protect the ranking signals I'm accountable for, or does it put them at risk?

**The concept to translate — hallucination & factual grounding, in her frame.** I did not lead with model behavior. I said: "Fabricated claims are an E-E-A-T problem, not just a quality problem — they're exactly what the helpful-content system punishes. So factual grounding isn't a nice-to-have here; it's a ranking safeguard. Every claim ties back to a source, and unsourced claims get gated out before publish." I mapped hallucination directly onto the algorithmic risk she already loses sleep over.

**The concept to translate — eval metrics, as a publish gate.** I did not say "we'll run an LLM-as-judge eval." I said: "There's an automated check before anything enters the publish queue: it scores factuality and originality, and near-duplicate or unsupported drafts are blocked. Think of it as a pre-publish linter for the two things that get us penalized." The eval became a gate expressed in the currency she cares about: originality and factual defensibility as ranking protection.

### 3.4 Legal Counsel — owns liability and IP

> "My questions are simple, and I need real answers, not 'probably.' Where did this sentence come from? Can we defend it if challenged? Are we training on anything we don't have rights to? And when, not if, it publishes something false, what's our exposure? Air Canada's chatbot invented a refund policy and the airline was held liable. I'm not signing off on a sentence-generator with no chain of custody."

**What she was actually asking:** Can I establish provenance and bound the liability, in writing?

**The concept to translate — training data & RAG provenance.** I did not say "we use a frozen base model with no fine-tuning on your data, retrieval-augmented at inference." I said: "It is not trained on our content — it reads from our approved archive at the moment it drafts, the way a researcher pulls a book off our own shelf. We can show, per article, exactly which internal sources every claim drew from. Nothing comes from material we don't own or license." Provenance became a chain of custody she can audit, which is the artifact she actually needs.

**The concept to translate — hallucination, as bounded liability.** I did not give her a rate. I said: "The risk is real, so we bound it three ways: a human approves every published piece, every factual claim carries a traceable source, and we start only with low-liability content where the worst case is a correction, not a court. We don't put this near regulated or advice content until the controls are proven." Hallucination became a risk-management posture with named controls and a blast radius, which is the only language a 'probably' allergy responds to.

### 3.5 The Executive Sponsor — owns budget and the board narrative

> "I have ninety seconds with the board. I need one number that says this is working and one sentence that says it won't blow up in our face. I don't want to hear about embeddings. I read about Klarna walking back their AI support. Don't make me the next case study."



**What she was actually asking:** What's the ROI, what's the leading indicator that it's safe, and what's the story?

**The concept to translate — the adoption funnel & eval metrics, as leading indicators.** I did not say "we'll track eval pass rates and adoption cohorts." I said: "The number for the board is cycle time: four days to under eight hours on our highest-volume work. The safety story is three leading indicators we watch weekly: how many writers actually use it, how often the editor throws a draft out, and how long a writer takes to earn unsupervised trust. If the throwaway rate climbs, we stop expanding before it becomes a Klarna headline." The metrics became one ROI number plus a tripwire she can say in a sentence.

**The concept to translate — token economics / cost.** Not "input plus output tokens at the blended rate," but "cost-per-published-article, fully loaded, against a writer-hour: a rounding error versus the cycle-time gain, and the dashboard shows it the moment that stops being true." Cost became a unit she can defend in a budget conversation.

**The translation matrix, at a glance:**

| AI concept | Editor | Strategist | SEO Lead | Legal | Executive |
|---|---|---|---|---|---|
| Hallucination | "shows its work; cite or flag" | (deferred to editor) | "E-E-A-T / ranking risk, gated" | "bounded liability + chain of custody" | "the throwaway-rate tripwire" |
| RAG / retrieval | "drafts in our voice from our work" | "it remembers what we published" | "originality, not duplication" | "reads our shelf, isn't trained on it" | (deferred to ROI) |
| Eval metrics | "your rubric, applied earlier" | (deferred) | "a pre-publish linter" | (deferred to controls) | "weekly leading indicators" |
| Embeddings | (deferred) | "finds related work by meaning" | "semantic dedup check" | (deferred) | (deferred) |
| Cost / tokens | (deferred) | (deferred) | (deferred) | (deferred) | "cost-per-article vs. writer-hour" |

The deferrals are deliberate: translation is also knowing which concept each persona does *not* need to hear. Boring the editor with token economics fails as surely as telling the lawyer nothing about provenance.

---

## 4. User stories

Six stories, each in standard form, each with acceptance criteria a non-technical PM can verify without reading code.

**Story 1 — Sourced drafts (Editor).**
*As an editor, I want every AI draft to arrive with each factual claim linked to its source, so that I can verify accuracy without re-reporting the whole piece.*
**Acceptance criteria:** (a) Every draft renders inline citations; clicking a factual sentence reveals its internal source. (b) Drafts exceeding a set threshold of unsourced claims are held from the editor's queue and returned for regeneration. (c) The editor can mark a citation "wrong source" in one click, flagging the draft for review.

**Story 2 — House voice from the archive (Writer).**
*As a writer, I want the assistant to draft in our house style using only our approved corpus, so that my first draft already sounds like us and I'm editing voice, not inventing it.*
**Acceptance criteria:** (a) Drafts meet the agreed house-voice rubric threshold before reaching the writer. (b) The writer can regenerate any section with a one-line instruction without leaving the editor. (c) No phrasing comes from outside the approved corpus, verifiable via the Story 1 citation trail.

**Story 3 — Calendar-to-draft handoff (Content Strategist).**
*As a content strategist, I want to turn a planned calendar item into a reviewable draft in one action, so that planning and drafting don't live in two disconnected tools.*
**Acceptance criteria:** (a) A calendar brief has a "generate draft" action that produces a draft in the review queue. (b) The strategist never leaves the CMS/calendar to trigger or track it. (c) Draft status (generating / in review / approved) shows on the calendar item.

**Story 4 — Pre-publish factuality & originality gate (SEO Lead).**
*As an SEO lead, I want an automated factuality-and-originality check before any draft can enter the publish queue, so that we never ship fabricated claims or near-duplicate content that risks ranking penalties.*
**Acceptance criteria:** (a) No AI-assisted draft reaches the publish queue until it passes the gate. (b) The gate flags unsupported claims (per Story 1) and near-duplicate content against the index, with a similarity score the SEO lead can review. (c) Gate pass/fail and reason are logged per article.

**Story 5 — Provenance trail (Legal Counsel).**
*As legal counsel, I want a per-article provenance record on every published AI-assisted piece, so that if a claim is challenged I can show where it came from and who approved it.*
**Acceptance criteria:** (a) Every published AI-assisted article has a retrievable record of the internal sources each claim drew from, the model version, and the approving editor. (b) The record is exportable for a legal hold. (c) Categories flagged "restricted" (regulated, advice, legally sensitive) are blocked from the workflow until explicitly cleared.

**Story 6 — Adoption & trust dashboard (Executive Sponsor).**
*As the executive sponsor, I want a weekly adoption-and-trust dashboard, so that I can tell the board whether this is working and catch trouble before we expand.*
**Acceptance criteria:** (a) The dashboard shows adoption rate, fallback-to-human rate, and Time-to-Trust, weekly. (b) It flags when fallback-to-human rate exceeds the agreed threshold (the expansion tripwire). (c) It reports cost-per-published-article against a writer-hour baseline.

---

## 5. Success metrics

The metrics are an adoption funnel, not a content-output scoreboard. The distinction matters: output metrics (articles shipped, words generated) reward exactly the behavior that gets organizations into trouble. These reward trust earned.

**Primary.**
- **Adoption rate** — % of eligible writers using the assistant at least once per week. *Target: 70% of the Tier-1 pool by Day 90.* Measures whether the tool earned its place, not whether it was mandated into it.
- **Fallback-to-human rate** — % of AI drafts the editor discards and rewrites from scratch (vs. edits). *Target: declining, below 20% by Day 90.* The quality signal and the expansion tripwire: a rising rate means the tool is moving the bottleneck onto the editor (the §2 anti-goal).
- **Time-to-Trust** — median days from a writer's first use to their first unsupervised publish (editor approves with light edits, not a rewrite). *Target: under 21 days.* The DR-Max research flags this as the metric that replaced DAU/MAU for agentic products: it measures the human relationship with the tool, not raw usage.

**Guardrail.** Factuality-gate catch rate (should trend down as drafts improve); brand-voice rubric score (must hold steady or rise; a productivity win that degrades voice is a loss); cost-per-published-article vs. a writer-hour baseline.

**Explicitly not tracked as success:** click-through rate, total AI-generated articles, total words — either downstream of factors the tool doesn't control (CTR) or dangerous as targets (volume).

---

## 6. Rollout plan — 90 days, phased, champion-led

The rollout is designed around one lesson the research surfaced repeatedly: **the organizations that got burned expanded scope before they earned trust; the ones that succeeded expanded internally and iteratively, and let metrics, not the calendar, open each gate.**

**Phase 0 — Baseline & champions (Weeks -2 to 0).** Instrument the current state: measure today's cycle time and a baseline editor-satisfaction score so the "no degradation" guardrail is provable later. Lock the Tier-1 definition (high-volume, low-liability: evergreen explainers, product education, listicles). Recruit a champion cohort: the editor plus five to six respected writers who will shape the tool and advocate for it. *(Prosci ADKAR "Awareness + Desire": trust is built internally, deliberately, before anything scales.)*

**Phase 1 — Champion cohort only (Days 1-30).** Live only for the champions, only on Tier-1 content. Daily feedback; weekly tuning of the voice rubric and factuality gate. **This is where the Klarna lesson is load-bearing: Klarna deployed AI support at scale, handled 2.3M chats and cut resolution time from 11 minutes to 2, then walked it back when complex cases degraded CSAT because generic answers failed on nuance. The encoded takeaway: do not open the tool to complex or high-liability content at launch. Tier-1 only, humans on every output, until the metrics earn the next phase.**

**Phase 2 — Full Tier-1 rollout (Days 31-60).** Gate to enter: fallback rate below threshold and Time-to-Trust trending down. The champions become the training layer, onboarding the rest of the Tier-1 pool. **This mirrors JPMorgan Chase's LLM Suite rollout to 250,000 employees, where adoption came from deliberate enablement (training in prompting and tool use, the ADKAR "Knowledge + Ability" stages) rather than a mandate. Champions teaching peers is the adoption engine, not an executive memo.**

**Phase 3 — Conditional Tier-2 expansion (Days 61-90).** Only after editor satisfaction is validated against the Phase-0 baseline and the factuality gate has a track record does scope expand toward nuanced (Tier-2) content. **This is the Bank of America Erica pattern in miniature: Erica scaled to 2.5 billion interactions at a 98% containment rate not through a big-bang launch but through relentless iteration (tens of thousands of model updates) and an internal-first trust curve. Expansion is earned by performance, not scheduled by date.** Regulated or advice content stays gated behind explicit legal sign-off (Story 5c).

**The standing rule across all phases:** the expansion gate is a metric (fallback rate + editor CSAT), never the calendar. If metrics regress, the rollout holds or rolls back. That single rule is the difference between this plan and the cautionary tales it cites.

---

## 7. Open questions & risks

- **Voice rubric subjectivity.** Only as good as its examples; if editor and rubric disagree, trust erodes. Mitigation: the editor owns and revises the rubric in Phase 1.
- **Archive quality.** RAG grounding faithfully reproduces an outdated or off-brand corpus. Mitigation: a curated, approved subset for Phase 1, expanded deliberately.
- **The gate as bottleneck.** Too aggressive a gate becomes the new bottleneck. Mitigation: tune thresholds against the fallback metric; keep five-plus champions so the program survives a departure.

---

## 8. Where the AI-evangelism arc applies

I have run this discovery before, just without the title or the mandate to make it stick. For the better part of a decade, first inside a financial-services org and then a media company, I was the person quietly translating between the people who could build with AI and the people who were afraid of it, and I did it with no budget, no roadmap, and a headcount of one. I learned the five languages in this document the hard way: by watching the pitch die in the room, by being the engineer the lawyer didn't believe and the evangelist the executive tuned out. I got a handful of coworkers to fold AI into their workflow and I lost a lot more meetings than I won, because being early and being persuasive are different skills and I only had the first one. This PRD is the version I would have shipped if either of those orgs had handed me named accountability instead of letting me freelance the future on the side. The translation table in §3 is not a framework I read about. It is the scar tissue.

---

*Rollout case studies (Klarna's AI-support walk-back, Bank of America's Erica, JPMorgan Chase's LLM Suite) surfaced via the 2026-05-18 Enterprise AI PM skill-gap research: `vault/20_projects/research/2026-05-18-enterprise-ai-pm-skill-gaps.md` (Q1 cross-functional translation; Q6 change management).*
