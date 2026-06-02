# Council Session — spec-stress-discovery-prd

- **Session ID:** `20260602-123710-d1c851`
- **Profile:** `premium`
- **Duration:** 237.4s
- **Tokens:** 55022 in, 22527 out
- **Cost:** $0.6130

## Original prompt

```
Stress-test the following Discovery PRD. It is a portfolio artifact whose explicit purpose is to prove ONE skill: cross-functional translation (the most-cited competency across Tier-1 AI Product Manager job descriptions). The load-bearing section is §3, where five stakeholders are voiced and AI concepts are translated into each one's language.

Each council member should independently surface:

1. **Persona distinctness (the make-or-break test).** Read §3's five personas (editor, content strategist, SEO lead, legal counsel, executive sponsor) WITHOUT their headers. Could you reliably tell them apart blind from voice and concerns alone? Name any two that blur together, and quote the lines that fail to differentiate them.

2. **Translation integrity.** For each AI-concept translation in §3 (embeddings, RAG, hallucination rate, eval metrics, token economics), judge whether it is (a) accurate, or (b) oversimplified to the point a competent ML engineer would wince or a domain expert (e.g. an SEO lead, a lawyer) would catch an error. Quote the specific translation and say what's wrong if anything.

3. **Standard PRD holes.** Acceptance criteria that are ambiguous or unmeasurable; missing edge cases; hidden dependencies (X requires Y, Y unmentioned); vocabulary used inconsistently. Quote specific lines/sections.

4. **The metrics + rollout.** Are the adoption-funnel metrics (adoption rate, fallback-to-human rate, Time-to-Trust) actually the right leading indicators, or is there a vanity-metric or gaming risk hidden in them? Is the Klarna/BofA/JPMorgan rollout reasoning sound, or is a case study misapplied?

5. **The credibility risk.** This is a job-hunt artifact for a PM with short formal PM tenure and a long informal AI-evangelism track. Does anything here read as over-claiming, template-generic, or as a tell that the author hasn't actually shipped this class of product? Be specific.

Be ruthless. The author wants the strongest critique, not validation. Quote lines. Where you disagree with the other council members, say so.

=== PRD ===


# Discovery PRD: AI-Assisted Article Drafting & Editorial Review

*A discovery-phase product requirements document for a ~50-person content organization at a Fortune-500 company. Written from the seat of the PM who has to get five people who do not speak the same language to agree on the same product.*


## 0. Why this document exists

Every AI product pitch I have watched die in a room died the same way: an engineer explained retrieval-augmented generation to a lawyer, the lawyer heard "the machine writes things and we hope they're true," and the meeting was over before the coffee got cold. They were speaking five languages at one table and calling it a kickoff.

This PRD is built backward from that failure. The product underneath it is unremarkable on purpose: an assistant that drafts articles and routes them through editorial review. The hard part was never the model. It's that the editor wants her voice protected, the strategist wants throughput, the SEO lead wants to not get delisted by Google, the lawyer wants to not get sued, and the executive wants a number she can say to a board. The same sentence about hallucination rates has to land as five different promises. That translation is the whole job, and it's what this document exists to show.

The body below is sober. The discovery section is where the work lives.


## 1. Product context & the workflow

**The surface.** A drafting assistant in the existing CMS. A writer or the strategist hands it a brief from the editorial calendar; it returns a first draft grounded in the organization's own published archive and style guide; the draft enters the review queue with every factual claim traced to a source. The editor reviews, edits, approves. Nothing publishes without a human. **What it is not:** an autonomous publisher, a replacement for writers, or anything trained on the open internet. The scope is "first-draft acceleration for a defined content tier," not "content automation."

**Why this org, why now.** The team produces ~120 pieces a month and first-draft cycle time is the bottleneck: an explainer takes three to four working days to reach a reviewable draft, most of it spent re-assembling context already published elsewhere. The org has the raw material (a deep archive, a documented style guide) and the pain (a backlogged calendar) that make this the right first AI surface: high-volume, low-liability work where a bad draft costs an editor's hour, not a lawsuit.


## 2. Problem statement

> First-draft cycle time for Tier-1 content runs three to four working days per piece, the bulk of it spent re-assembling context the organization has already published. The calendar is structurally backlogged and the team cannot hire its way out at acceptable cost. **Target outcome: reduce Tier-1 first-draft cycle time from ~4 days to under 8 hours, with no measurable degradation in brand-voice fidelity or factual accuracy, and without the editorial team absorbing the drafting cost as rework.**

Note what this is not: not "adopt AI," not "increase output by N%." It pairs a cycle-time target with two guardrails (voice fidelity, factual accuracy) and one anti-goal: do not move the bottleneck from drafting onto the editor's desk. The guardrails sit in the statement on purpose, because the failure mode for this class of product is buying speed by quietly transferring the cost to the reviewer.


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


## 5. Success metrics

The metrics are an adoption funnel, not a content-output scoreboard. The distinction matters: output metrics (articles shipped, words generated) reward exactly the behavior that gets organizations into trouble. These reward trust earned.

**Primary.**
- **Adoption rate** — % of eligible writers using the assistant at least once per week. *Target: 70% of the Tier-1 pool by Day 90.* Measures whether the tool earned its place, not whether it was mandated into it.
- **Fallback-to-human rate** — % of AI drafts the editor discards and rewrites from scratch (vs. edits). *Target: declining, below 20% by Day 90.* The quality signal and the expansion tripwire: a rising rate means the tool is moving the bottleneck onto the editor (the §2 anti-goal).
- **Time-to-Trust** — median days from a writer's first use to their first unsupervised publish (editor approves with light edits, not a rewrite). *Target: under 21 days.* The DR-Max research flags this as the metric that replaced DAU/MAU for agentic products: it measures the human relationship with the tool, not raw usage.

**Guardrail.** Factuality-gate catch rate (should trend down as drafts improve); brand-voice rubric score (must hold steady or rise; a productivity win that degrades voice is a loss); cost-per-published-article vs. a writer-hour baseline.

**Explicitly not tracked as success:** click-through rate, total AI-generated articles, total words — either downstream of factors the tool doesn't control (CTR) or dangerous as targets (volume).


## 6. Rollout plan — 90 days, phased, champion-led

The rollout is designed around one lesson the research surfaced repeatedly: **the organizations that got burned expanded scope before they earned trust; the ones that succeeded expanded internally and iteratively, and let metrics, not the calendar, open each gate.**

**Phase 0 — Baseline & champions (Weeks -2 to 0).** Instrument the current state: measure today's cycle time and a baseline editor-satisfaction score so the "no degradation" guardrail is provable later. Lock the Tier-1 definition (high-volume, low-liability: evergreen explainers, product education, listicles). Recruit a champion cohort: the editor plus five to six respected writers who will shape the tool and advocate for it. *(Prosci ADKAR "Awareness + Desire": trust is built internally, deliberately, before anything scales.)*

**Phase 1 — Champion cohort only (Days 1-30).** Live only for the champions, only on Tier-1 content. Daily feedback; weekly tuning of the voice rubric and factuality gate. **This is where the Klarna lesson is load-bearing: Klarna deployed AI support at scale, handled 2.3M chats and cut resolution time from 11 minutes to 2, then walked it back when complex cases degraded CSAT because generic answers failed on nuance. The encoded takeaway: do not open the tool to complex or high-liability content at launch. Tier-1 only, humans on every output, until the metrics earn the next phase.**

**Phase 2 — Full Tier-1 rollout (Days 31-60).** Gate to enter: fallback rate below threshold and Time-to-Trust trending down. The champions become the training layer, onboarding the rest of the Tier-1 pool. **This mirrors JPMorgan Chase's LLM Suite rollout to 250,000 employees, where adoption came from deliberate enablement (training in prompting and tool use, the ADKAR "Knowledge + Ability" stages) rather than a mandate. Champions teaching peers is the adoption engine, not an executive memo.**

**Phase 3 — Conditional Tier-2 expansion (Days 61-90).** Only after editor satisfaction is validated against the Phase-0 baseline and the factuality gate has a track record does scope expand toward nuanced (Tier-2) content. **This is the Bank of America Erica pattern in miniature: Erica scaled to 2.5 billion interactions at a 98% containment rate not through a big-bang launch but through relentless iteration (tens of thousands of model updates) and an internal-first trust curve. Expansion is earned by performance, not scheduled by date.** Regulated or advice content stays gated behind explicit legal sign-off (Story 5c).

**The standing rule across all phases:** the expansion gate is a metric (fallback rate + editor CSAT), never the calendar. If metrics regress, the rollout holds or rolls back. That single rule is the difference between this plan and the cautionary tales it cites.


## 7. Open questions & risks

- **Voice rubric subjectivity.** Only as good as its examples; if editor and rubric disagree, trust erodes. Mitigation: the editor owns and revises the rubric in Phase 1.
- **Archive quality.** RAG grounding faithfully reproduces an outdated or off-brand corpus. Mitigation: a curated, approved subset for Phase 1, expanded deliberately.
- **The gate as bottleneck.** Too aggressive a gate becomes the new bottleneck. Mitigation: tune thresholds against the fallback metric; keep five-plus champions so the program survives a departure.


## 8. Where the AI-evangelism arc applies

I have run this discovery before, just without the title or the mandate to make it stick. For the better part of a decade, first inside a financial-services org and then a media company, I was the person quietly translating between the people who could build with AI and the people who were afraid of it, and I did it with no budget, no roadmap, and a headcount of one. I learned the five languages in this document the hard way: by watching the pitch die in the room, by being the engineer the lawyer didn't believe and the evangelist the executive tuned out. I got a handful of coworkers to fold AI into their workflow and I lost a lot more meetings than I won, because being early and being persuasive are different skills and I only had the first one. This PRD is the version I would have shipped if either of those orgs had handed me named accountability instead of letting me freelance the future on the side. The translation table in §3 is not a framework I read about. It is the scar tissue.


*Rollout case studies (Klarna's AI-support walk-back, Bank of America's Erica, JPMorgan Chase's LLM Suite) surfaced via the 2026-05-18 Enterprise AI PM skill-gap research: `vault/20_projects/research/2026-05-18-enterprise-ai-pm-skill-gaps.md` (Q1 cross-functional translation; Q6 change management).*
```

## Council responses

### anthropic/claude-opus-4.7

# Council Review: Stress-Test of Discovery PRD

## 1. Persona distinctness (blind test)

I tried the blind read. Four of the five hold up cleanly — the editor's "I will quietly strangle it" voice, the strategist's "I do not want a sixth tool" operator register, the lawyer's "I need real answers, not 'probably'" cadence, and the executive's "ninety seconds with the board" framing are all sharply differentiated.

**The SEO Lead and Legal Counsel blur.** Both speak in defensive, risk-averse, consequence-citing prose. Compare:

- SEO Lead: *"Flood the index with thin, fabricated, near-duplicate junk and we don't get a productivity win, we get a manual action and six months of recovery."*
- Legal: *"Air Canada's chatbot invented a refund policy and the airline was held liable. I'm not signing off on a sentence-generator with no chain of custody."*

Both invoke a named external catastrophe, both demand provenance/defensibility, both frame the AI as an existential threat to a specific accountability surface. Strip the headers and the SEO line about "manual action and six months of recovery" could plausibly be a compliance officer; the legal "chain of custody" line could be an SEO lead worried about audit trails. The author distinguishes them via *content* (E-E-A-T vs. liability) but not via *voice*. They have the same emotional temperature and the same rhetorical move (cite a horror story, demand a guarantee).

The editor is also doing a lot of work to feel distinct — "quietly strangle it" is vivid but borders on too-writerly, the kind of line a PM writes *for* an editor rather than what an editor says. More on this in §5.

## 2. Translation integrity

**Embeddings — "finds related work the way a good editor would."** Accurate enough as a metaphor, but the "401k rollovers" / "retirement planning" example is the *easy* case (clear lexical neighbors). A competent ML engineer wouldn't wince; they'd note this undersells the failure mode (semantic retrieval also surfaces topically-adjacent-but-wrong matches, e.g. a piece on Roth conversions when the draft needed traditional IRA rules). The translation doesn't prepare the strategist for retrieval misses.

**RAG — "reads from our approved archive at the moment it drafts, the way a researcher pulls a book off our own shelf."** This is the strongest translation in the document. Accurate, defensible to an engineer, intelligible to a lawyer. Keep.

**Hallucination — "every factual sentence links to where it came from in our own archive. If it can't cite it, the sentence gets flagged."** ⚠️ **This is the translation an ML engineer would wince at.** Citation ≠ factuality. The model can confidently cite a real source that does not actually support the claim (citation hallucination / misattribution is one of the most-studied RAG failure modes). The PRD treats "has a citation" as equivalent to "is true," which is exactly the gap a lawyer would catch on a second pass: *"Counsel, the sentence cites a source. Does the source say what the sentence says?"* — and the PRD has no answer. Story 1c ("mark a citation 'wrong source'") tacitly admits this exists but treats it as an edge case rather than the central failure mode.

**Eval metrics — "your rubric, applied earlier... a pre-publish linter."** The rubric framing for the editor is good. The "pre-publish linter" framing for the SEO lead is where I'd push back: linters are deterministic; LLM-as-judge evals are stochastic and notoriously poorly calibrated on originality detection. The PRD promises the SEO lead an *automated* near-duplicate gate with a similarity score (Story 4b) — fine — but bundles factuality detection into the same gate, and *automated factuality eval is an open research problem*. An SEO lead might not catch this; an ML engineer on the panel definitely would.

**Token economics — "cost-per-published-article, fully loaded, against a writer-hour."** Accurate and well-framed. No notes.

**The biggest translation hole isn't listed:** there is no translation of **model choice / model drift / versioning**. Story 5a mentions "model version" in passing as part of the provenance record, but no persona is ever told that the model behind the assistant will change, that behavior will drift, and that the voice rubric and factuality gate will need re-baselining each time. For a PRD whose entire thesis is "translate the hard parts," omitting this is conspicuous.

## 3. Standard PRD holes

- **"Tier-1" is load-bearing and underdefined.** §1 says "high-volume, low-liability work." §6 Phase 0 says "evergreen explainers, product education, listicles." These are examples, not a definition. Who adjudicates whether a given brief is Tier-1? The strategist? The lawyer? This is the kind of ambiguity that produces the exact scope creep the rollout claims to prevent.
- **"Voice rubric threshold" is referenced four times and never specified.** Story 2a: "Drafts meet the agreed house-voice rubric threshold." Agreed by whom, scored how, on what scale? §7 acknowledges the rubric is subjective but doesn't acknowledge that *the threshold* is a separate, also-unspecified artifact.
- **"Unsourced claims" threshold (Story 1b) is undefined.** "Exceeding a set threshold" — set by whom, at what number? Zero unsourced claims is unachievable (transition sentences, framing); ten is too many. This is the central guardrail and it has no number.
- **Hidden dependency: the "approved corpus" curation work is unscoped.** §7 mentions "a curated, approved subset for Phase 1" as a mitigation, but curating an archive of presumably thousands of articles into an approved RAG corpus is a multi-week project with its own owner, criteria, and review cycle. It is mentioned in a risk bullet, not in the rollout plan. Phase 0 is two weeks and includes baselining, Tier-1 definition, and champion recruitment — corpus curation cannot also fit there.
- **Hidden dependency: "near-duplicate content against the index" (Story 4b)** requires either an external index crawl or a licensed dataset. Against *whose* index? The org's own published archive (easy), or the broader web (hard, expensive, and itself a vendor decision)? Unaddressed.
- **"Fallback-to-human rate" vocabulary is inconsistent.** §5 defines it as "% of AI drafts the editor discards and rewrites from scratch (vs. edits)." Story 6b calls it "the expansion tripwire." §6 Phase 2 says "fallback rate below threshold." Three names, one metric, no defined threshold.
- **Edge case missing: what happens when the archive contradicts itself?** Real content archives at Fortune-500 scale have outdated pieces, retracted claims, and editorial pivots. RAG grounded on a self-contradictory corpus produces confidently wrong drafts with valid citations. §7's "outdated or off-brand corpus" risk gestures at this but the mitigation ("curated subset") doesn't solve it.
- **Edge case missing: the writer who games the tool.** Adoption rate measures "at least once per week." A writer who runs one throwaway brief weekly to stay on the dashboard is indistinguishable from a real user. See §4.

## 4. Metrics + rollout

**Adoption rate (70% weekly active) is the vanity-metric risk.** "At least once per week" is a textbook gameable threshold, and worse, the executive sponsor is *explicitly told* this is a leading indicator she can report to the board. Pair this with a rollout where champions are evangelizing peers, and you have soft social pressure to click the button once a week. The metric should be something like *% of eligible Tier-1 briefs that went through the assistant*, which measures workflow penetration rather than user compliance.

**Fallback-to-human rate is the right metric but the definition is fragile.** "Discards and rewrites from scratch (vs. edits)" requires the editor to classify her own behavior honestly, in real time, on every draft. Editors under deadline pressure will not reliably distinguish "heavy edit" from "rewrite from scratch." Without instrumentation (diff-based measurement against the original draft), this metric is self-reported and therefore soft. The PRD doesn't say how it's measured.

**Time-to-Trust** — the PRD attributes this to "DR-Max research" which I cannot verify and reads as a name-drop. The *concept* (median days to first unsupervised publish) is reasonable, but it's a lagging indicator dressed as a leading one: by the time Time-to-Trust stabilizes, you're 21+ days in and the cohort is small. For a 90-day rollout with a champion cohort of 5-6, the denominator is too small to be statistically meaningful until Phase 2 at earliest.

**Case study application:**

- **Klarna** — applied correctly. The "deployed at scale, walked back on complex cases" framing matches the public reporting, and the lesson drawn (Tier-1 only at launch) is genuinely the right takeaway. ✓
- **JPMorgan LLM Suite** — applied loosely. The "250,000 employees, champions not mandate" framing is directionally true but JPM's rollout is a horizontal productivity tool (general-purpose assistant), not a workflow-embedded content pipeline. The adoption dynamics are different: JPM employees can use LLM Suite for any task; this PRD's tool only fires on a specific workflow step. Borrowing JPM's "champions teach peers" lesson is fine, but the analogy is thinner than the PRD claims.
- **Bank of America Erica** — **misapplied.** Erica is a customer-facing conversational banking assistant with a 98% *containment* rate (i.e., resolved without escalation). Citing it as the model for "expansion is earned by performance" in an internal editorial tool is a category error: Erica's iteration loop was driven by user intent classification on millions of customer queries; an editorial assistant for 50 people has neither the volume nor the structure for that kind of iteration. The Erica reference reads as a case study reached for because it's impressive, not because it's analogous. I'd cut it.

## 5. Credibility risk

This is where I'll be most direct, because §8 invites it.

**The voice in §3 is too polished.** The personas don't talk like stakeholders; they talk like a PM's idealized rendering of stakeholders. Real editors don't say "I will quietly strangle it" in a kickoff — they say "I'm worried about voice" and the PM has to *extract* the strangle-it energy through three follow-ups. Each quote is suspiciously well-formed: every stakeholder leads with their fear in the first sentence, names the consequence in the second, and issues a demand in the third. Real stakeholder discovery is messier — people contradict themselves, hedge, get distracted, anchor on the wrong concern for ten minutes before surfacing the real one. The dialogue here is too clean, and a hiring manager who has actually run discovery will register that.

**§8 is the strongest tell and also the most honest paragraph.** "I have run this discovery before, just without the title or the mandate to make it stick" is good — it's the right framing for the gap. But "the translation table in §3 is not a framework I read about. It is the scar tissue" undercuts itself: scar tissue produces *uneven* documents, with one persona observed in extreme depth and the others sketched. This PRD has five equally polished personas, which reads as constructed (read: workshopped from a framework) rather than excavated (lived through). The shape of real scar tissue would be: the editor and the executive rendered with painful specificity, the SEO lead and lawyer rendered competently from secondary observation, the strategist a bit thin. Symmetry is the tell.

**Specific over-claims:**

- "I learned the five languages in this document the hard way" — but the document has only five languages because the PM decided on five stakeholders. A real history would have produced six, or four, or a weird seventh persona that doesn't fit a 2x5 matrix.
- The translation matrix table is too clean. Every cell is either filled with a punchy phrase or marked "(deferred)" — no half-translations, no failed translations, no "this one I'm still working on." Real cross-functional translation is lossy and the lossiness shows.
- "Six stories, each with acceptance criteria a non-technical PM can verify without reading code" — this is a tell. Real PRDs don't announce their own readability; the framing reveals the PRD is being read by someone evaluating PM-ness, not by an engineer about to build.
- The metric attributions ("DR-Max research," the dated vault path footnote) are doing credibility work that's slightly *too* visible. The footnote especially — citing an internal research file with a specific date in a portfolio artifact is theater. Either the research is in the portfolio (then link it) or it isn't (then don't reference the file path).

**What's actually strong and would survive a skeptical hiring manager:** §2's anti-goal ("do not move the bottleneck from drafting onto the editor's desk"), the deferrals in the translation matrix (acknowledging which concepts each persona doesn't need is genuinely sophisticated), and the Klarna-driven phasing logic in §6. These three things read as earned. Almost everything else reads as well-studied.

---

## Where I'd disagree with other council members (anticipated)

I'd expect some council members to praise §3's persona quotes as the document's standout strength. I think they're the *riskiest* part: they're vivid enough to be memorable but stylized enough to read as written rather than gathered. I'd also expect defense of the Bank of America Erica citation as a fine analogy for "iterate to earn trust." I think it's a category error and would cut it specifically — JPMorgan alone carries the rollout argument.

The single most important fix: **the hallucination translation conflates citation with factuality**, and that's the one error a senior AI PM hiring manager will spot in 30 seconds. Fix that one thing and the document's load-bearing claim — "I can translate AI concepts accurately into five languages" — holds. Leave it, and §3's central proof collapses on inspection.

### openai/gpt-5.5

## Bottom line

§3 is directionally strong as a translation artifact, but the PRD overreaches in ways that would make a real ML lead, SEO lead, lawyer, or implementation PM push back. The biggest issue is not persona voice; the personas are mostly distinguishable. The bigger issue is **translation by overpromise**: “cite every factual sentence,” “unsourced claims get gated out,” “no phrasing comes from outside the approved corpus,” “nothing comes from material we don’t own,” “worst case is a correction.” Those are not just simplifications. Several are false or operationally unproven.

If this artifact is meant to prove cross-functional translation, the author should show they can translate **without making impossible guarantees**.

---

# 1. Persona distinctness: mostly good, but two pairs blur

If I read the five §3 personas without headers, I could identify most of them reliably. The opening quotes are doing useful work:

- Editor: voice, quality, resentment at cleanup work.
- Strategist: calendar, throughput, tool friction.
- SEO: Google, E-E-A-T, penalties, duplicates.
- Legal: provenance, rights, liability, chain of custody.
- Executive: board narrative, ROI, reputational risk.

The personas are distinct at the level of their **initial quotes**. The blur happens in the translation sections, where several stakeholders start receiving the same generic “source/cite/gate” promise.

## Blur pair 1: Editor vs. SEO Lead

The editor’s hallucination translation:

> “Every factual sentence links to where it came from in our own archive. If it can't cite it, the sentence gets flagged before it reaches you.”

The SEO hallucination translation:

> “Every claim ties back to a source, and unsourced claims get gated out before publish.”

These are nearly the same promise with different labels. The SEO version adds E-E-A-T framing, but operationally both are: cited claims good, uncited claims blocked. Blind, the second could easily belong to an editor, managing editor, fact-checker, or legal reviewer.

The SEO voice is strongest in the opening quote:

> “Google has been at war with low-effort AI content since the helpful-content update.”

But the actual translation is less SEO-specific than it could be. A real SEO lead would also care about search intent, cannibalization, internal linking, topical authority, freshness, structured data, author/entity signals, index bloat, crawl budget, and whether the AI drafts create pages that compete with existing pages. The PRD collapses SEO into “factual + original,” which is too narrow.

## Blur pair 2: Legal Counsel vs. SEO Lead

Legal:

> “Every factual claim carries a traceable source…”

SEO:

> “Every claim ties back to a source…”

Legal:

> “We can show, per article, exactly which internal sources every claim drew from.”

SEO:

> “Unsupported drafts are blocked.”

Again, both stakeholders are being sold provenance and claim support. That is relevant to both, but the distinction should be sharper.

Legal should sound more like: audit logs, retention, privilege, indemnity, vendor data use, copyright status, approval authority, regulated-content taxonomy, litigation hold, risk acceptance.

SEO should sound more like: helpfulness, search intent, cannibalization, duplicate clusters, page quality, SERP differentiation, author credibility, freshness, schema, manual action risk.

Right now, both are too often getting the same “source-backed claims” story.

---

# 2. Translation integrity: several simplifications cross into overclaim

## A. Embeddings / semantic retrieval

Quoted translation:

> “When it pulls related coverage, it finds pieces by what they're about, not just matching keywords. So a draft on ‘retirement planning’ surfaces our piece on ‘401k rollovers’ even if the words don't overlap.”

Judgment: **Mostly accurate, but too clean.**

This is an acceptable nontechnical explanation of embeddings. “Finds by what they’re about, not just matching keywords” is fair.

But it hides important caveats:

- Embedding retrieval is not magic “aboutness.”
- It often needs hybrid search: embeddings + keyword search + metadata filters + recency + content type + permissions.
- The example is plausible, but “retirement planning” and “401k rollovers” probably do have overlapping semantic and lexical signals. Better would be a less obvious example.
- Embeddings can retrieve conceptually adjacent but editorially wrong pieces.

The line in the matrix is more problematic:

> “Embeddings” → SEO Lead: “semantic dedup check”

Semantic similarity can help deduplication, but embeddings alone do not solve near-duplicate SEO risk. A competent SEO lead would ask whether you are checking:

- Same search intent.
- Keyword cannibalization.
- Canonical conflicts.
- Substantially similar pages.
- Existing rankings and traffic.
- Content decay or consolidation opportunities.

Calling embeddings a “semantic dedup check” is too glib.

## B. RAG / retrieval-augmented generation

Quoted translation:

> “It drafts from our own published work and our style guide, not from the open web.”

Judgment: **Potentially misleading.**

If the system uses a frontier base model, the model absolutely has parametric knowledge from pretraining, often including open-web data. RAG can ground the output in internal sources, but it does not mean the model “drafts from” only those sources unless the system is designed with strict source constraints, citation enforcement, retrieval-only answering patterns, and rejection behavior.

This line is also risky:

> “What it is not: … anything trained on the open internet.”

That is likely false unless this organization is using a model trained exclusively on licensed/internal data. Most commercial LLMs were trained at least partly on open-web-scale corpora. If the author means “not trained or fine-tuned on our open web crawl” or “not generating from live web search,” say that. As written, a technical reviewer would flag it immediately.

Legal translation:

> “It is not trained on our content — it reads from our approved archive at the moment it drafts, the way a researcher pulls a book off our own shelf.”

This is a good translation if true. But it requires vendor guarantees about:

- Whether prompts and retrieved context are logged.
- Whether logs are used for training.
- Data retention.
- tenant isolation.
- SOC2/security posture.
- whether internal content can leak into future outputs.

Then this line overclaims:

> “Nothing comes from material we don't own or license.”

Not defensible. The base model’s language ability and world knowledge come from pretraining. You can say “we only retrieve from approved internal sources and require citations to those sources.” You cannot safely say “nothing comes from material we don’t own or license” unless the model stack is contractually and technically constrained to that.

## C. Hallucination rate / factual grounding

Editor translation:

> “Every factual sentence links to where it came from in our own archive. If it can't cite it, the sentence gets flagged before it reaches you.”

SEO translation:

> “Every claim ties back to a source, and unsourced claims get gated out before publish.”

Legal translation:

> “Every factual claim carries a traceable source…”

Judgment: **This is the biggest integrity problem in the PRD.**

These lines overpromise claim-level provenance. In real systems:

- Detecting “every factual claim” is hard.
- Sentence-level citation is not equivalent to claim-level support.
- A sentence may contain multiple claims.
- A cited source may be topically related but not actually support the generated claim.
- The model can produce citation laundering: plausible citations attached to unsupported statements.
- Internal archives may themselves be outdated, wrong, noncompliant, or superseded.
- “If it can’t cite it” assumes the model or gate can reliably know when support is absent.

The better translation would be:

> “The draft will include source-linked claims, and the gate will sample or score whether citations actually support the claims. Unsupported or low-confidence claims are flagged for review.”

That is less sexy but more credible.

SEO translation:

> “Fabricated claims are an E-E-A-T problem, not just a quality problem — they're exactly what the helpful-content system punishes.”

This is oversimplified. Google’s helpful content systems are not simply hallucination detectors. Low-quality AI content can be a problem, but Google has repeatedly said AI-generated content is not inherently against guidelines if it is helpful and original. “Exactly what the helpful-content system punishes” is too certain.

Legal translation:

> “We start only with low-liability content where the worst case is a correction, not a court.”

A lawyer would not let this slide. Even “low-liability” evergreen content can create legal exposure: defamation, financial advice implications, product claims, employment claims, health/safety claims, copyright, regulatory misstatements, or deceptive marketing. The worst case may be unlikely to be court, but you cannot promise “not a court.”

## D. Eval metrics / brand-voice scoring

Editor translation:

> “Before any writer sees a draft, it gets scored against a voice rubric we build from your own best published pieces — the same rubric you'd use in your head, written down. Drafts that don't clear the bar don't reach you.”

Judgment: **Good translation, weak implementation credibility.**

This is a strong stakeholder translation. But technically, “brand-voice scoring” is hard to make reliable. The PRD does not say:

- Who labels examples.
- How many gold-standard samples exist.
- Whether scoring is done by humans, LLM-as-judge, classifiers, or hybrid.
- How inter-rater reliability is measured.
- What the threshold is.
- How false positives/false negatives affect workflow.
- How the system avoids optimizing for superficial tone markers.

SEO eval translation:

> “There's an automated check before anything enters the publish queue: it scores factuality and originality, and near-duplicate or unsupported drafts are blocked. Think of it as a pre-publish linter for the two things that get us penalized.”

Judgment: **Too strong.**

“Factuality” and “originality” are not like lint checks. A linter detects deterministic patterns. Factuality requires source support, temporal freshness, contradiction handling, and sometimes external verification. Originality for SEO requires more than similarity score. A “pre-publish linter” is a useful metaphor, but the acceptance criteria need to avoid implying deterministic correctness.

Executive translation:

> “The safety story is three leading indicators we watch weekly: how many writers actually use it, how often the editor throws a draft out, and how long a writer takes to earn unsupervised trust.”

Judgment: **Conceptually useful, but “unsupervised trust” conflicts with the product scope.**

Earlier:

> “Nothing publishes without a human.”

Later:

> “Time-to-Trust — median days from a writer's first use to their first unsupervised publish…”

If “unsupervised publish” means “writer can publish without editor review,” that contradicts the core safety posture. If it means “editor approves with light edits,” then “unsupervised” is the wrong word.

## E. Token economics / cost

Quoted translation:

> “Not ‘input plus output tokens at the blended rate,’ but ‘cost-per-published-article, fully loaded, against a writer-hour: a rounding error versus the cycle-time gain, and the dashboard shows it the moment that stops being true.’”

Judgment: **Good framing, unjustified claim.**

“Cost-per-published-article, fully loaded” is exactly the right executive translation. But “a rounding error” is an unsupported assertion.

Fully loaded cost includes:

- Model inference.
- Retrieval infrastructure.
- Embedding/indexing.
- Storage.
- Evaluation runs.
- Citation verification.
- CMS integration.
- Security review.
- Legal/procurement.
- Vendor minimums.
- Observability.
- Human review/rework.
- Prompt/eval maintenance.
- Support and training.

Token cost may be a rounding error. Productized AI workflow cost may not be.

---

# 3. Standard PRD holes

## A. Acceptance criteria are full of undefined thresholds

Story 1:

> “Drafts exceeding a set threshold of unsourced claims are held from the editor's queue…”

What threshold? Per sentence? Per claim? Weighted by severity? Does one unsupported legal/financial claim block the draft even if the percentage is low?

Story 2:

> “Drafts meet the agreed house-voice rubric threshold before reaching the writer.”

What rubric? What threshold? Who agrees? How is it validated? What happens when the editor disagrees with the automated score?

Story 6:

> “It flags when fallback-to-human rate exceeds the agreed threshold…”

Again, no threshold. The metric section says:

> “Target: declining, below 20% by Day 90.”

But rollout gates say “below threshold” without saying whether 20% is the gate or just Day-90 target.

## B. “Factual claim” is undefined

Story 1:

> “Every AI draft to arrive with each factual claim linked to its source…”

Acceptance criteria:

> “Every draft renders inline citations; clicking a factual sentence reveals its internal source.”

The PRD shifts from “claim” to “sentence.” This matters. One sentence can contain five claims. Some claims are implied. Some are interpretive. Some are forward-looking. Some are about the company itself. Some are common knowledge. Some need external sources.

This needs a claim taxonomy:

- Common knowledge.
- Internal-source factual claims.
- External factual claims.
- Product/legal claims.
- Numeric claims.
- Time-sensitive claims.
- Advice/recommendation claims.
- Quotes/attribution.

Without that, “every factual claim” is not testable.

## C. “No phrasing comes from outside the approved corpus” is impossible or undesirable

Story 2:

> “No phrasing comes from outside the approved corpus, verifiable via the Story 1 citation trail.”

This is a serious problem. If taken literally, it implies the model can only use phrases that appear in the approved corpus. That is not how generation works, and it may increase plagiarism/self-plagiarism/duplicate content risk.

If the intended meaning is “no factual claims are sourced from outside the approved corpus,” say that. “No phrasing” is the wrong unit.

Also, citation trails verify factual support, not whether phrasing came from somewhere else.

## D. “Reviewable draft” is undefined

Problem statement:

> “reduce Tier-1 first-draft cycle time from ~4 days to under 8 hours”

Story 3:

> “produces a draft in the review queue.”

But what counts as a reviewable draft?

- Minimum completeness?
- Word count?
- Citation coverage?
- Voice score?
- SEO brief coverage?
- Structure adherence?
- Editor acceptability?
- Reading level?
- Internal links?
- Metadata?

Without a definition, the team can hit “under 8 hours” by producing bad drafts faster.

## E. Hidden dependency: approved corpus curation

§7 acknowledges:

> “RAG grounding faithfully reproduces an outdated or off-brand corpus. Mitigation: a curated, approved subset for Phase 1…”

But corpus curation is not treated as a real dependency in the rollout. This is a large workstream:

- Which articles are approved?
- Who owns inclusion/exclusion?
- How are outdated articles removed?
- How are corrections propagated?
- How are regulated/restricted topics tagged?
- How are permissions enforced?
- How are canonical sources selected when archive articles disagree?

This is not a side risk. It is foundational.

## F. Hidden dependency: claim-source alignment system

The PRD assumes:

> “every factual claim traced to a source.”

That requires much more than RAG. You need:

- Claim extraction.
- Source retrieval.
- Evidence matching.
- Citation placement.
- Support scoring.
- Contradiction detection.
- UI for citation review.
- Human correction feedback.
- Audit logging.

None of that is specified as a capability. It appears as a promise.

## G. Hidden dependency: CMS/calendar integration

Story 3:

> “The strategist never leaves the CMS/calendar to trigger or track it.”

This implies a real integration with the CMS and editorial calendar. Missing:

- Which CMS?
- Authentication/permissions.
- Draft states.
- Version history.
- Review queue semantics.
- Failure states.
- Latency expectations.
- API availability.
- Ownership between product/engineering/editorial ops.

For a discovery PRD, you do not need implementation detail, but you do need to name the dependency.

## H. Vocabulary inconsistency: writer vs. editor queue

§1:

> “The editor reviews, edits, approves.”

Story 1:

> “so that I can verify accuracy…”

Story 2:

> “Drafts meet the agreed house-voice rubric threshold before reaching the writer.”

Story 3:

> “produces a draft in the review queue.”

Which happens first?

- Strategist generates draft.
- Writer edits draft.
- Editor reviews draft.
- Publish gate runs.
- Legal provenance record created.

The workflow is not crisp. Sometimes the draft is held before the editor. Sometimes before the writer. Sometimes before the publish queue. The PRD needs a state diagram.

## I. Vocabulary inconsistency: Tier-1 / Tier-2

§1:

> “high-volume, low-liability work”

Phase 0:

> “evergreen explainers, product education, listicles”

“Product education” may not be low-liability in a Fortune-500 context. It can involve product claims, regulated disclosures, pricing, availability, suitability, financial/health implications, or competitive claims.

Legal would not accept “product education” as automatically Tier-1.

## J. Missing edge cases

Important missing edge cases:

1. **Archive conflicts:** two internal articles disagree.
2. **Outdated source:** cited article was correct in 2021, wrong now.
3. **No coverage:** brief asks for something the archive does not cover.
4. **Restricted content leakage:** a restricted source is retrieved into a low-liability draft.
5. **Prompt injection:** malicious or accidental instructions embedded in archived content.
6. **Embargoed/confidential material:** internal draft sources should not be used for public content.
7. **Licensed third-party content:** the company can read it but may not be able to reuse it.
8. **Author attribution:** whose byline goes on AI-assisted content?
9. **Corrections:** how post-publication corrections update the provenance record and corpus.
10. **Model/vendor change:** model upgrade changes voice/factuality behavior.
11. **Failure mode:** retrieval service down, model timeout, incomplete citations.
12. **Security:** role-based access, SSO, logs, PII, retention.
13. **Regulatory review:** what if content is low-liability editorial but mentions regulated topics?
14. **SEO cannibalization:** new draft competes with existing page.
15. **Internal linking:** generated article omits required links or links to deprecated pages.
16. **Human overtrust:** editors skim because citations create false confidence.

---

# 4. Metrics + rollout critique

## A. Adoption rate is useful but gameable

Metric:

> “Adoption rate — % of eligible writers using the assistant at least once per week. Target: 70% of the Tier-1 pool by Day 90.”

This can become a vanity metric. Writers can open the tool once a week and abandon the draft. Managers can pressure usage. It does not prove quality, time savings, or trust.

Better leading indicators:

- % of eligible briefs attempted with AI.
- % of AI drafts accepted into writer editing.
- % reaching editor review without full rewrite.
- Median writer edit time per AI draft.
- Median editor review time per AI draft.
- Draft acceptance rate by content type.
- Repeat usage after first bad experience.
- Citation-support precision.
- Voice pass rate calibrated against editor judgment.

## B. Fallback-to-human rate is important but too coarse

Metric:

> “% of AI drafts the editor discards and rewrites from scratch.”

Good instinct. But it misses the common failure mode: the editor does not fully discard the draft but spends two hours fixing every paragraph.

A writer/editor can game or distort this by not marking something “discarded.” Better companion metrics:

- Edit distance between AI draft and submitted draft.
- Editor time-in-document.
- Number of unsupported/wrong citations.
- Number of factual corrections.
- Number of voice corrections.
- Section regeneration count.
- “Would you use this again?” post-task rating.
- Draft helpfulness score.

## C. Time-to-Trust is vague and contradictory

Metric:

> “median days from a writer's first use to their first unsupervised publish”

This conflicts with:

> “Nothing publishes without a human.”

The parenthetical tries to clarify:

> “editor approves with light edits, not a rewrite”

Then call it “time to first light-edit approval,” not “unsupervised publish.” The current wording creates a safety red flag.

Also, this metric can be gamed by choosing one easy article for each writer. It should be paired with a sustained trust metric, e.g.:

- two consecutive light-edit approvals,
- light-edit approval rate over last N drafts,
- median review time over last N drafts.

## D. Factuality-gate catch rate is ambiguous

Guardrail:

> “Factuality-gate catch rate (should trend down as drafts improve)”

This is dangerous. A declining catch rate could mean:

- drafts are improving,
- the gate is missing more errors,
- thresholds were loosened,
- writers are avoiding hard topics,
- source coverage changed.

You need independent sampling by humans to know whether the gate’s precision/recall is improving.

## E. The primary business metric is underweighted

The target outcome is:

> “reduce Tier-1 first-draft cycle time from ~4 days to under 8 hours”

But success metrics say:

> “The metrics are an adoption funnel, not a content-output scoreboard.”

That is a good philosophical distinction, but cycle time should still be a primary metric. The whole product exists to reduce cycle time without quality loss.

A better metric stack:

Primary outcome:
- Median first-draft cycle time for Tier-1 content.
- Median total time from brief to editor-approved draft.

Quality guardrails:
- Editor review time.
- Full-rewrite rate.
- Citation-support accuracy.
- Factual correction rate.
- Voice rubric human score.
- Post-publication correction rate.
- SEO cannibalization/duplicate risk.

Adoption/trust:
- Repeat usage.
- AI draft acceptance rate.
- Time to first light-edit approval.
- Writer/editor satisfaction.

Cost:
- Fully loaded cost per approved article.
- Cost per hour saved.

## F. Rollout: case studies feel partially misapplied

### Klarna

Quoted:

> “Klarna deployed AI support at scale, handled 2.3M chats and cut resolution time from 11 minutes to 2, then walked it back when complex cases degraded CSAT because generic answers failed on nuance.”

The lesson “do not expand to complex cases too early” is sound. But customer-support chatbots and editorial drafting are different enough that this needs care. Klarna’s issue is real-time customer resolution, deflection, and service quality. Editorial drafting has human review before publication. The analogy works only at the level of “don’t over-automate nuanced work.”

Also, Klarna’s AI story is contested and PR-heavy. Using it as a load-bearing rollout proof point may look like blog-post research rather than operator knowledge.

### JPMorgan Chase LLM Suite

Quoted:

> “This mirrors JPMorgan Chase's LLM Suite rollout to 250,000 employees…”

This is too broad. An enterprise-wide LLM assistant rollout is not the same as a CMS-embedded article drafting workflow with legal/SEO review. “Champions teaching peers” is plausible change management, but the JPM reference does not prove this rollout design.

### Bank of America Erica

Quoted:

> “Erica scaled to 2.5 billion interactions at a 98% containment rate not through a big-bang launch but through relentless iteration…”

This is the weakest analogy. Erica is a banking virtual assistant with high-volume customer interactions. “Containment rate” is a call-center metric. It does not map cleanly to editorial drafting, where the goal is not containment but high-quality human-approved output.

Also:

> “internal-first trust curve”

Erica is customer-facing. If there was an internal-first rollout, spell it out. As written, this feels like a case-study name-drop.

## G. The “metrics, not calendar” principle is good but contradicted by calendar phases

The PRD says:

> “the expansion gate is a metric … never the calendar.”

But rollout phases are framed as:

> “Days 1-30”  
> “Days 31-60”  
> “Days 61-90”

That is not fatal, but the gates should be written as: “No earlier than Day 31, and only if…” Otherwise it still reads like a scheduled rollout with metric theater.

---

# 5. Credibility risk: several tells that this has not been shipped

This artifact is strong as a narrative exercise. It is weaker as a real discovery PRD. The credibility risk is that it sounds like someone who understands the meeting dynamics but has not yet lived through implementation, compliance, evals, and operational ownership.

## A. Impossible guarantees

These lines are the biggest credibility hits:

> “every factual claim traced to a source”

> “Every factual sentence links to where it came from”

> “Every claim ties back to a source, and unsourced claims get gated out before publish.”

> “No phrasing comes from outside the approved corpus”

> “Nothing comes from material we don't own or license.”

> “where the worst case is a correction, not a court.”

These are the kinds of statements an experienced PM would soften or scope because they know how hard they are to prove.

Better wording would use confidence, sampling, source-support checks, and escalation:

- “source-linked factual claims”
- “unsupported or low-confidence claims flagged”
- “claim-support score”
- “human-verifiable provenance”
- “approved retrieval corpus”
- “restricted categories blocked pending legal review”

## B. Too many unnamed thresholds

Repeated lines like:

> “set threshold”

> “agreed threshold”

> “scores factuality and originality”

> “brand-voice rubric score”

make the PRD feel template-generic. Discovery PRDs can have open questions, but the PRD should at least define how thresholds will be established: baseline sample, editor calibration, human labels, false-positive tolerance, severity weighting, and pilot exit criteria.

## C. The eval plan is hand-wavy

The PRD talks confidently about evals but does not specify:

- gold dataset,
- labeling process,
- inter-rater reliability,
- eval dimensions,
- model-as-judge validation,
- citation-support accuracy,
- failure taxonomy,
- regression testing,
- model/version change management,
- minimum viable eval before launch.

For an AI PM artifact, this is a major omission.

## D. Legal/security/procurement are underdeveloped

Legal is voiced well, but the PRD does not cover enough of what legal and enterprise procurement would actually require:

- vendor terms,
- indemnity,
- data retention,
- training opt-out,
- audit rights,
- SOC2/security,
- access controls,
- PII handling,
- confidential information,
- copyright posture,
- byline/disclosure policy,
- retention schedule,
- legal hold process,
- regulated-content approval workflow.

Story 5 gestures at provenance, but provenance is only one slice of legal readiness.

## E. The artifact over-indexes on fashionable references

These lines create a “research deck” smell:

> “Prosci ADKAR ‘Awareness + Desire’”

> “DR-Max research flags this as the metric that replaced DAU/MAU for agentic products”

> “Klarna…”

> “JPMorgan Chase…”

> “Bank of America Erica…”

The case studies are not useless, but they are doing too much reputational work. A hiring manager may read this as “smart person who reads enterprise AI articles,” not “PM who has shipped an AI workflow.”

The private/future-looking citation also hurts portability:

> “surfaced via the 2026-05-18 Enterprise AI PM skill-gap research: `vault/20_projects/research/...`”

As a portfolio artifact, citing a local vault path is odd. It makes the evidence non-verifiable to the reader.

## F. The “scar tissue” paragraph is emotionally effective but also risky

§8:

> “This PRD is the version I would have shipped if either of those orgs had handed me named accountability instead of letting me freelance the future on the side.”

This is candid, but it also says: I have not actually shipped this. That may be acceptable if the artifact is explicitly a discovery artifact, but then the rest of the PRD should be extra careful not to sound overconfident.

The strongest version would say:

- “This is a discovery artifact, not a shipped case study.”
- “The riskiest assumptions are X, Y, Z.”
- “Here is how I would validate them in two weeks.”
- “Here is what I would not promise until proven.”

Right now, §8 is compelling but slightly defensive.

---

# Recommended fixes

If the author wants this to survive serious scrutiny, I would revise in five ways.

## 1. Replace absolute guarantees with testable controls

Change:

> “Every factual sentence links to where it came from.”

To:

> “The system identifies factual claims, attaches proposed supporting sources from the approved corpus, and flags low-confidence or unsupported claims for human review. During pilot, we measure citation-support accuracy against human judgment.”

## 2. Clarify model/data boundaries

Change:

> “not from the open web”  
> “not trained on the open internet”  
> “Nothing comes from material we don't own or license.”

To:

> “The generation step is constrained to retrieve from an approved internal corpus. We do not use live web retrieval. Vendor terms must prohibit training on our prompts, outputs, or retrieved content. Because the base model has pretrained knowledge, publishable factual claims still require support from approved sources.”

## 3. Make SEO actually SEO-specific

Add SEO acceptance criteria around:

- search intent match,
- cannibalization check,
- existing ranking URL conflicts,
- internal-link recommendations,
- freshness requirements,
- metadata/schema completeness,
- duplicate cluster detection.

Do not reduce SEO to “originality + factuality.”

## 4. Add an eval plan

Include a small table:

| Eval dimension | Method | Human owner | Launch threshold |
|---|---|---|---|
| Citation support | Human-labeled sample of claims | Editor/legal | ≥ X% supported |
| Voice | Editor-scored rubric | Editor | No worse than baseline |
| Factual error severity | Human review | Editor/legal | Zero high-severity errors in pilot |
| Duplicate/cannibalization | SEO review + similarity tools | SEO | No blocked duplicates |
| Editor rework | Time/edit distance | Editorial ops | Below baseline |

## 5. Fix metric definitions

Rename:

> “Time-to-Trust”

To:

> “Time to first light-edit approval”

Define:

- adoption as repeat use on eligible briefs, not once-weekly logins,
- fallback as full rewrite plus heavy-edit rate,
- cycle time as primary outcome,
- citation-support precision as a safety metric,
- editor review time as the anti-bottleneck metric.

---

# Final assessment

The artifact succeeds at showing that the author understands the politics of AI adoption. The stakeholder quotes are vivid, and the core insight — translation is the PM job — is strong.

But the PRD currently proves a second, unintended thing: the author may translate AI concepts into stakeholder language by making the controls sound more deterministic than they are. That is the credibility risk.

The revision goal should be: **keep the human translation, remove the magic.**

### ~google/gemini-pro-latest

Here is a ruthless stress-test of your Discovery PRD. You asked for the strongest critique, so I will not cushion the blow: while this document reads like a brilliant piece of PM theater, it fundamentally fails the reality test of shipping generative AI. 

As a PM artifact, it reveals a candidate who understands product *marketing* and stakeholder management deeply, but who lacks the technical scars of actually wrangling probabilistic models in production. 

Here is the breakdown across your five criteria.

### 1. Persona Distinctness (The Make-or-Break Test)
While the *titles* are distinct, the personas blur heavily because the author feeds them the exact same mechanical solutions dressed up in slightly different syntax. 

**The Editor and the SEO Lead fail the blind-read test.** They are functionally indistinguishable in their handling of hallucination/factuality.
*   **The Editor (3.1):** *"Every factual sentence links to where it came from in our own archive. If it can't cite it, the sentence gets flagged before it reaches you."*
*   **The SEO Lead (3.3):** *"Every claim ties back to a source, and unsourced claims get gated out before publish... flagged unsupported claims and near-duplicate content."*

If you removed the headers and the SEO buzzwords ("E-E-A-T"), both personas are just requesting a deterministic citation-checker. The PM didn't translate the concept differently; they just handed the same exact feature to two different people and called it a successful translation.

### 2. Translation Integrity
This is where the PRD's credibility unravels. The translations overclaim the deterministic capabilities of LLMs to a degree that an ML engineer would immediately flag as a liability.

*   **Hallucination rate ("citations/flagging"):** *"If it can't cite it, the sentence gets flagged..."* and *"every factual sentence links to where it came from."* This is deeply flawed. LLMs do not inherently know when they are lying, and they are notoriously proficient at hallucinating citations or misattributing real text to the wrong internal document. Promising a lawyer or an editor a deterministic "flag" when an LLM hallucination occurs implies you have a perfect, unsolved fact-checking architecture. 
*   **Eval metrics ("brand voice scoring"):** *"scored against a voice rubric... The same rubric you'd use in your head, written down."* An ML engineer would wince here. LLM-as-a-judge for subjective "brand voice" is highly brittle, expensive, and prone to extreme variance. Framing this to an editor as a solved, reliable pre-read filter oversells the technology.
*   **RAG:** *"It drafts from our own published work... so when it covers a topic we've written about before, it builds on what we already said instead of starting from scratch."* This ignores the primary danger of RAG on a legacy corpus: contradictions. If the archive has an article from 2021 and 2024 with opposing views, how does it resolve them? The translation glosses over retrieval accuracy.
*   **Token economics:** Accurate and well-translated for an executive ("cost-per-published-article vs writer-hour").

### 3. Standard PRD Holes
*   **Ambiguous/Unmeasurable Acceptance Criteria:** Story 2 mentions: *"Drafts meet the agreed house-voice rubric threshold before reaching the writer."* This is entirely unmeasurable for engineering. What is the threshold? Is it an LLM-as-a-judge score of 4/5? Who writes the evaluation prompt? 
*   **Hidden Dependencies:** Story 3 states: *"The strategist never leaves the CMS/calendar to trigger or track it,"* and *"A calendar brief has a 'generate draft' action..."* This casually mandates a deep bi-directional UI/backend integration with a 3rd-party CMS/Calendar. That is a massive, months-long engineering dependency hand-waved as a simple AC.
*   **Missing Edge Cases (Closed-loop limitation):** If the tool *only* drafts using the approved archive (Story 2c: *"No phrasing comes from outside the approved corpus"*), how does the organization write about *new* developments, external news, or new products? The PRD mandates strict grounding but completely ignores the edge case of net-new information.

### 4. The Metrics + Rollout
*   **The Gaming Risk in "Time-to-Trust":** Defining Time-to-Trust as the median days to *"first unsupervised publish (editor approves with light edits, not a rewrite)"* is a massive vanity metric risk. You are not measuring the AI's quality; you are measuring the *Editor's fatigue*. A busy editor overwhelmed by the volume of AI drafts will eventually stop rewriting and just hit "approve" to clear their queue. The metric goes down, looking like "trust," while brand voice is quietly degrading.
*   **Misapplied Rollout Case Studies:** The Klarna and BofA Erica citations are wholly inappropriate. Klarna and Erica are **autonomous, B2C customer-facing chatbots** dealing with unpredictable user inputs. This PRD is for an **internal, human-in-the-loop, asynchronous drafting tool**. Applying Klarna's B2C public relations failure to justify an internal phased rollout makes zero sense. The JPM LLM Suite is the only relevant comp.

### 5. The Credibility Risk
As someone reviewing a PM portfolio, my takeaway is exactly what you feared: **this reads like a PM who has read a lot about AI but never actually shipped a generative text product.** 

The tell is in Section 3.4 (Legal): *"We can show... exactly which internal sources every claim drew from."* 

A PM who has built RAG systems knows that tracing the exact provenance of a synthesized, abstract generated sentence back to a single source document is messy, probabilistic, and often inaccurate. Promising a lawyer "exact provenance" in writing is a rookie execution mistake that opens the company to the exact legal liability the PM is trying to prevent. 

**Summary Verdict:** The artifact brilliantly demonstrates stakeholder empathy and narrative framing. But technically, it writes checks that the underlying ML architecture cannot cash. To fix this, the PM must introduce *probability and friction*—admitting to the lawyer that citations can be hallucinated and defining the human-in-the-loop mitigations for when the "factuality gate" inevitably fails.

### x-ai/grok-4.20

**1. Persona distinctness**

I can reliably distinguish four, but **Editor and SEO Lead blur together** when read blind.

- Editor quote: "I am not going to spend the next six rewriting a robot's homework. If this thing turns me into a cleanup crew..."
- SEO Lead: "Flood the index with thin, fabricated, near-duplicate junk... Prove to me this doesn't tank our E-E-A-T."

Both center on *not wanting to deal with low-quality AI output that creates downstream cleanup work*. The Editor fears editorial rework; the SEO Lead fears algorithmic punishment for the same root cause (fabricated/thin content). The voices are too similar in tone ("prove to me this doesn't make my life worse"). The Editor's "cleanup crew" and SEO's "near-duplicate junk" read as the same fear translated into adjacent dialects rather than distinct personas. Legal, Strategist, and Executive are sharply distinct.

**2. Translation integrity**

All five translations have accuracy issues that a competent ML engineer or domain expert would flag.

- **Hallucination (Editor):** "It will sometimes state things confidently that aren't true. We handle that by making it show its work: every factual sentence links to where it came from in our own archive. If it can't cite it, the sentence gets flagged."  
  This is *partially* accurate for RAG but misleading. RAG reduces but does not eliminate hallucinations on synthesis or inference steps. A competent engineer winces at treating citation as a complete solution. The lawyer section compounds it by calling it "bounded liability."

- **Eval metrics (SEO):** "There's an automated check before anything enters the publish queue: it scores factuality and originality... Think of it as a pre-publish linter."  
  LLM-as-judge for factuality and "originality" is notoriously noisy. An SEO lead who understands Helpful Content Update and core web vitals would catch that "originality score" is not how Google detects AI spam; semantic similarity != duplicate content penalty. This oversimplifies to the point of error.

- **RAG (Strategist):** "It drafts from our own published work... it remembers what we've already published."  
  Mostly fair, but the translation erases the distinction between retrieval and generation. The model does *not* "remember"; it retrieves chunks at inference. Minor, but an ML engineer would note the anthropomorphism.

- **Embeddings (Strategist):** "When it pulls related coverage, it finds pieces by what they're *about*, not just matching keywords... the way a good editor would."  
  Accurate at a high level. The analogy holds.

- **Token economics (Executive):** "cost-per-published-article, fully loaded, against a writer-hour."  
  This is directionally correct but hides that token cost is only one component. A sophisticated executive (or their finance partner) would ask about prompt caching, vector DB costs, latency, and whether "fully loaded" includes the human review cost—the actual dominant variable. It's oversimplified.

- **Training data & provenance (Legal):** "It is not trained on our content — it reads from our approved archive at the moment it drafts... We can show, per article, exactly which internal sources every claim drew from."  
  This is the strongest translation. Correctly distinguishes RAG from fine-tuning and emphasizes provenance. A lawyer familiar with the Air Canada case would still push on whether retrieval can be gamed and on model memorization, but the core mapping is sound.

**3. Standard PRD holes**

- **Ambiguous/unmeasurable acceptance criteria.** Story 1(b): "Drafts exceeding a *set threshold* of unsourced claims..." — what is the threshold? Who sets it? How is it measured? Story 2(a): "Drafts meet the agreed house-voice rubric threshold" — undefined, subjective, and the primary success guardrail. Story 4(b): "near-duplicate content against the index, with a similarity score" — which index (published articles? web?), which similarity function (cosine on embeddings? BM25?), what threshold? All unverifiable by a "non-technical PM."

- **Hidden dependencies.** The entire voice rubric and factuality gate depend on high-quality embeddings and chunking of the archive, plus robust LLM-as-judge prompts. None of this is mentioned anywhere. The "curated, approved subset" in §7 is acknowledged too late and too weakly.

- **Inconsistent vocabulary.** "Fallback-to-human rate" is defined in §5 as "% of AI drafts the editor discards and rewrites from scratch." In Story 6 and the rollout it morphs into the primary expansion gate, but the acceptance criteria in Story 1(c) and Story 4 allow "mark wrong source" and regeneration, which is neither full fallback nor light edit. The metric becomes fuzzy exactly where it is load-bearing.

- **Missing edge cases.** No mention of prompt injection by writers, model version drift, archive staleness beyond §7, multi-modal sources, or what happens when the "one-click wrong source" feedback loop trains the system to be overly conservative.

**4. The metrics + rollout**

The metrics are mostly correct *in theory* but contain clear vanity/gaming risk. **Fallback-to-human rate** is the strongest signal, but "Time-to-Trust" (median days to first unsupervised publish) is easily gamed: editors can simply approve mediocre drafts faster to hit the number, or champions can be given easier briefs. Adoption rate is the weakest; 70% weekly usage can be achieved by making the "generate draft" button the only obvious path in the CMS.

The rollout reasoning is **misapplied case studies**. Klarna walked back because the *use case* (customer support on complex financial queries) was high-liability and the model wasn't ready. Mapping that directly to "therefore only do low-liability Tier-1 explainers" is reasonable, but claiming it as proof that champion-led internal rollout prevents failure is loose. JPMorgan's LLM Suite and BofA Erica were *broad capability platforms* with heavy training/enablement, not a narrow drafting assistant. The author is pattern-matching famous names to sound enterprise-savvy while the actual analogy (Perplexity-style internal RAG at The Atlantic or similar) would be more honest. This is the tell.

**5. Credibility risk**

This artifact overclaims in subtle but detectable ways for someone with "short formal PM tenure."

- The opening framing ("Every AI product pitch I have watched die... This PRD is built backward from that failure") and the final §8 ("I have run this discovery before, just without the title... This PRD is the version I would have shipped... The translation table in §3 is not a framework I read about. It is the scar tissue.") read as defensive autobiography. It screams "I was the AI guy, not the PM."

- The citation "2026-05-18 Enterprise AI PM skill-gap research" in a document that is otherwise timeless is a bizarre artifact. (Future-dated vault reference?)

- The product itself is presented as "unremarkable on purpose" while the discovery is framed as heroic. This is a classic tell of someone who evangelized but never owned the shipping spec, engineering tradeoffs, or post-launch metrics in a real org. Real enterprise drafting products (e.g., at Bloomberg, Thomson Reuters, or The New York Times) have far more complex grounding, human-in-the-loop, and A/B testing layers than are hinted here. The PRD never once mentions latency, prompt engineering discipline, evaluation harness design, or the actual difficulty of maintaining a high-quality voice rubric at scale. Those omissions, combined with the polished translation matrix, suggest the author has done the *translation* work extensively but has not shipped the *product* at the claimed level of accountability.

**Overall verdict:** The cross-functional translation skill is genuinely demonstrated and is strong. That is the only unqualified success. Everything else—technical accuracy, PRD rigor, metric integrity, and authenticity—has cracks that a sharp hiring panel or engineering counterpart would see immediately. The document proves the author can bridge languages. It does not yet prove they can ship.

I disagree with any council member who thinks the personas are fully distinct or that the technical translations are clean. They are not. The blurring of Editor/SEO voice and the optimistic treatment of hallucination-as-solved-by-citation are objective flaws.

## Cross-rankings

### Judge: anthropic/claude-opus-4.7

- **Order:** A > C > B
- **Reasoning:** Response A is the most comprehensive and rigorous: it catches the most translation overclaims (e.g., 'not trained on the open internet' being likely false, 'no phrasing from outside the corpus' being technically incoherent, the 'unsupervised publish' contradiction with 'nothing publishes without a human'), identifies more PRD holes with specific quoted evidence, provides a deeper edge-case list, and offers constructive revisions. Response C is tight, well-organized, and surfaces several sharp points (the future-dated vault citation, gaming of Time-to-Trust, anthropomorphism in RAG translation, the §8 defensive tell) but is less exhaustive than A. Response B is solid and identifies the core issues (Editor/SEO blur, hallucinated citations, Klarna/Erica misapplication, closed-corpus edge case) but is the shortest, misses several technical inaccuracies the others catch, and engages less with the specifics of PRD rigor.

### Judge: openai/gpt-5.5

- **Order:** A > C > B
- **Reasoning:** Response A is the strongest: it is the most specific, quotes extensively, distinguishes technical overclaim from acceptable translation, and gives especially sharp critiques on citation≠factuality, undefined thresholds, corpus curation, metric gaming, and misapplied case studies. Response C is also solid and covers all requested areas with good specificity, but it is less nuanced and occasionally overstates or contradicts itself, e.g. saying all translations have issues while calling some accurate/strong. Response B identifies several real flaws, especially provenance and hallucination overclaiming, but it is more rhetorically sweeping, less comprehensive, and sometimes too categorical in dismissing case-study relevance.

### Judge: ~google/gemini-pro-latest

- **Order:** B > A > C
- **Reasoning:** Response B provides the most technically rigorous critique, correctly identifying impossible product guarantees (like strictly constraining LLM phrasing) and the vital missing taxonomy of factual claims. Response A offers a brilliant meta-analysis of the artifact's credibility, astutely pointing out that the symmetric polish of the personas and perfectly parsed dialogue betray a lack of actual 'scar tissue.' Response C is solid and accurate but lacks the exceptional depth of technical and behavioral insight found in the top two.

### Judge: x-ai/grok-4.20

- **Order:** A > B > C
- **Reasoning:** Response A ranks first for its superior overall quality: it delivers ruthless, specific critiques with precise quotes across all five required dimensions, demonstrates deep technical insight (e.g., citation hallucination as a core RAG failure mode), identifies subtle PRD holes like undefined thresholds and hidden dependencies, and offers balanced disagreement notes while maintaining clarity and structure. Response B ranks second as it is similarly comprehensive and technically accurate (highlighting oversimplifications like conflating citations with factuality, SEO reductionism, and impossible guarantees), but is slightly less focused and more repetitive in listing edge cases. Response C ranks last: while it correctly flags key technical flaws (e.g., provenance overclaims and gaming risks), it is less thorough on persona blurring and PRD holes, relies on broader assertions without as many targeted quotes, and occasionally overstates (e.g., dismissing all case studies rather than differentiating). All three agree on core issues like hallucination translations and credibility tells, but A and B provide more insightful, evidence-based depth.

## Chairman synthesis

_Chairman model: `anthropic/claude-opus-4.7`_

# Final Council Synthesis: Stress-Test of Discovery PRD

Four council members independently reviewed your PRD. The convergence is striking on the load-bearing failures, and the divergence is informative on what's actually salvageable. Here's the consolidated verdict, with lineage.

---

## Where all four council members converge (high confidence — fix these first)

### 1. The Editor and SEO Lead blur in §3

**Unanimous across Opus, GPT-5.5, Gemini, and Grok.** This is the most important finding because §3 is the load-bearing section.

The blur is not at the level of opening quotes — those are distinct. It's that **both personas receive the same mechanical translation dressed in different vocabulary**:

- Editor (3.1): *"every factual sentence links to where it came from in our own archive. If it can't cite it, the sentence gets flagged before it reaches you."*
- SEO Lead (3.3): *"Every claim ties back to a source, and unsourced claims get gated out before publish."*

Gemini put it most sharply: *"The PM didn't translate the concept differently; they just handed the same exact feature to two different people and called it a successful translation."* Grok identified the deeper structural problem: both personas are organized around the same emotional posture (*"prove to me this doesn't make my life worse"*). Opus noted the rhetorical move is identical: both invoke a named catastrophe, both demand provenance, both treat AI as existential threat.

**The fix (synthesizing GPT-5.5's strongest recommendation):** Make the SEO translation actually SEO-specific. Currently it collapses to "factual + original." A real SEO lead would also need acceptance criteria around search intent match, keyword cannibalization, canonical conflicts, freshness, schema/metadata, internal linking, and topical authority — none of which appear.

### 2. The hallucination translation conflates citation with factuality — the single biggest technical error

**Unanimous, and flagged by every member as the error a senior AI PM hiring manager would catch in 30 seconds.**

Opus stated it most precisely: *"Citation ≠ factuality. The model can confidently cite a real source that does not actually support the claim (citation hallucination / misattribution is one of the most-studied RAG failure modes)."* Gemini called this *"a rookie execution mistake that opens the company to the exact legal liability the PM is trying to prevent."* Grok noted RAG reduces but does not eliminate hallucinations on synthesis or inference steps. GPT-5.5 offered the cleanest rewrite:

> "The system identifies factual claims, attaches proposed supporting sources from the approved corpus, and flags low-confidence or unsupported claims for human review. During pilot, we measure citation-support accuracy against human judgment."

Story 1(c) ("mark a citation 'wrong source' in one click") tacitly admits this failure mode exists but treats it as an edge case rather than the central one. **This is the load-bearing fix.** If only one technical change is made to the PRD, it is this.

### 3. Bank of America Erica is misapplied; Klarna is the only solid case study

**Three of four (Opus, GPT-5.5, Grok) explicitly call Erica a category error.** Opus was sharpest: *"Erica is a customer-facing conversational banking assistant with a 98% containment rate. Citing it as the model for 'expansion is earned by performance' in an internal editorial tool is a category error."*

Gemini went further and called both Klarna and Erica inappropriate (customer-facing autonomous chatbots vs. internal human-in-the-loop drafting). The majority view — which I adopt — is more nuanced: Klarna's "don't expand to complex/high-liability content too early" lesson translates legitimately; Erica should be cut; JPMorgan's relevance is real but thinner than the PRD claims (JPM's tool is a horizontal assistant, not a workflow-embedded pipeline).

### 4. "Time-to-Trust" is contradictory and gameable

**Unanimous.** Two distinct problems were surfaced:

- **GPT-5.5's contradiction catch:** "Time-to-Trust" is defined as "median days to first *unsupervised* publish," which contradicts §1's "Nothing publishes without a human." Rename to *"Time to first light-edit approval."*
- **Gemini's gaming catch (echoed by Grok):** *"A busy editor overwhelmed by the volume of AI drafts will eventually stop rewriting and just hit 'approve' to clear their queue. The metric goes down, looking like 'trust,' while brand voice is quietly degrading."*

Pair with sustained-trust requirements (two consecutive light-edit approvals, rolling-window approval rate) and editor-time-in-document instrumentation.

### 5. Undefined thresholds make the acceptance criteria untestable

**Unanimous.** Quoted across all four reviews:

- Story 1b: *"exceeding a set threshold of unsourced claims"* — undefined
- Story 2a: *"the agreed house-voice rubric threshold"* — undefined
- Story 4b: *"a similarity score the SEO lead can review"* — which index? which function? which cutoff?
- §6 phase gates: *"fallback rate below threshold"* — which threshold?

Discovery PRDs are allowed open questions, but they should at minimum define *how* thresholds will be established (baseline sample, editor calibration, false-positive tolerance).

### 6. Adoption rate (70% weekly) is a vanity metric

**Unanimous.** "Used once per week" is gameable by social pressure and by writers running a throwaway brief to stay on the dashboard. Opus's replacement is the strongest: *"% of eligible Tier-1 briefs that went through the assistant"* — workflow penetration rather than user compliance.

---

## Where the council diverges (lower confidence — judgment calls)

### Divergence 1: How "unshippable" is the PRD's claim about training data?

GPT-5.5 alone flagged this as a major technical overclaim:

> *"What it is not: ... anything trained on the open internet"* and *"Nothing comes from material we don't own or license"* — these are likely false unless the org uses a model trained exclusively on licensed/internal data.

Opus, Gemini, and Grok did not catch this. **I side with GPT-5.5.** Any frontier base model has parametric knowledge from open-web pretraining. The defensible version is: *"The generation step is constrained to retrieve from an approved internal corpus; vendor terms prohibit training on our prompts and outputs."* As written, an ML engineer would flag this immediately, and worse, a lawyer who later learned the truth would feel misled. This is the second-biggest credibility risk after the citation/factuality conflation.

### Divergence 2: Are the persona quotes too polished?

**Opus alone** made this argument and it's the sharpest single observation in the entire council review:

> *"Real editors don't say 'I will quietly strangle it' in a kickoff — they say 'I'm worried about voice' and the PM has to extract the strangle-it energy through three follow-ups... The shape of real scar tissue would be: the editor and the executive rendered with painful specificity, the SEO lead and lawyer rendered competently from secondary observation, the strategist a bit thin. Symmetry is the tell."*

The other three members focused on content blurring rather than voice symmetry. I find Opus's framing the most damaging because it attacks the artifact's central credibility claim (§8's "scar tissue") on stylistic evidence. **This is the most defensible single revision target if you want §3 to feel earned rather than workshopped:** make the personas asymmetric. Have one persona where you nailed the translation, one where you partially failed, one where the deferral is visible. The current translation matrix's clean "(deferred)" cells are too tidy.

### Divergence 3: Should "factuality gate catch rate trending down" be a guardrail at all?

**GPT-5.5 alone** caught this:

> *"A declining catch rate could mean: drafts are improving, the gate is missing more errors, thresholds were loosened, writers are avoiding hard topics... You need independent sampling by humans to know whether the gate's precision/recall is improving."*

This is correct and important. The other three reviewers missed it. Add an independent human-labeled sample as a check on the gate's precision.

### Divergence 4: Is "Tier-1 = product education" actually low-liability?

**GPT-5.5 alone** flagged that "product education" in a Fortune-500 context can involve product claims, regulated disclosures, pricing, suitability, or financial/health implications. Legal would not accept "product education" as automatically Tier-1. The other reviewers accepted the Tier-1 framing.

---

## Convergent additions I would prioritize beyond what's above

Drawing from the strongest individual contributions:

- **Opus's edge case — archive self-contradiction:** *"Real content archives at Fortune-500 scale have outdated pieces, retracted claims, and editorial pivots. RAG grounded on a self-contradictory corpus produces confidently wrong drafts with valid citations."* §7 gestures at this; the mitigation doesn't solve it.

- **GPT-5.5's missing edge cases worth adopting:** prompt injection from archived content, model/vendor change behavior drift, byline/disclosure policy, restricted-source leakage into low-liability drafts.

- **Gemini's net-new content problem:** *"If the tool only drafts using the approved archive, how does the organization write about new developments, external news, or new products?"* Story 2c's "No phrasing comes from outside the approved corpus" is either incoherent (that's not how generation works) or destructively restrictive.

- **Opus's & Grok's tell on the dated vault citation:** the `2026-05-18-enterprise-ai-pm-skill-gaps.md` footnote is theater in a portfolio artifact. Either link the research or remove the citation.

- **GPT-5.5's eval plan table** is the single most concrete operational fix and should be added wholesale. The PRD currently talks confidently about evals without specifying gold dataset, labeling process, inter-rater reliability, or model-as-judge validation — a major omission for an AI PM artifact.

---

## The credibility verdict (where the council agrees most)

All four reviewers concluded that the PRD **proves cross-functional translation skill but reveals a candidate who has not shipped this class of product.** The pattern of tells is consistent:

- **Opus:** persona symmetry, self-announcing readability ("acceptance criteria a non-technical PM can verify without reading code"), and clean matrix cells.
- **GPT-5.5:** impossible guarantees ("worst case is a correction, not a court"), absent eval plan, name-dropped frameworks (ADKAR, DR-Max) doing reputational work.
- **Gemini:** "writes checks that the underlying ML architecture cannot cash."
- **Grok:** "The document proves the author can bridge languages. It does not yet prove they can ship."

This is convergent enough to treat as the final diagnosis.

---

## The minimum viable revision

If you change only five things, change these — in priority order:

1. **Fix the citation/factuality conflation** in §3.1, §3.3, §3.4. Replace deterministic guarantees with sampled, scored, human-validated controls. (All four members)

2. **Cut or rewrite the training-data claims.** "Not trained on the open internet" and "Nothing comes from material we don't own or license" are technically false for any frontier base model. (GPT-5.5)

3. **Differentiate the SEO Lead from the Editor.** Give SEO acceptance criteria about cannibalization, search intent, freshness, and schema — not just factuality + originality. (All four)

4. **Rename Time-to-Trust to "Time to first light-edit approval"** and pair it with a sustained-trust companion metric to prevent editor-fatigue gaming. (GPT-5.5 contradiction; Gemini gaming risk)

5. **Cut the Bank of America Erica reference.** Klarna's lesson translates; Erica's containment-rate framing is a category error. JPM stays but trim the analogy. (Opus, GPT-5.5, Grok)

If you change one more thing for credibility rather than correctness: **make the personas asymmetric.** Show one translation you nailed, one you half-failed, one where the deferral hurt. Symmetry reads as workshop; asymmetry reads as scar tissue.

The core thesis of the PRD — that translation is the PM job — is correct and defensibly demonstrated. The artifact currently undermines that thesis by translating AI concepts into stakeholder language that makes the controls sound more deterministic than they are. **The revision goal, in GPT-5.5's phrase that the council largely endorses: "keep the human translation, remove the magic."**
