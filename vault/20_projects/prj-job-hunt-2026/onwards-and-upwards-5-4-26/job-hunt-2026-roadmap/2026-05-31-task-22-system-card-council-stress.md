# Council Session — spec-stress-code-brain-system-card

- **Session ID:** `20260531-142103-811b6e`
- **Profile:** `premium`
- **Duration:** 210.6s
- **Tokens:** 45943 in, 21983 out
- **Cost:** $0.5595

## Original prompt

```
Stress-test the following AI "system card." It maps a personal AI agent fleet to
SR-11-7 model-risk tiers and EU AI Act technical-documentation requirements. The
author is an AI Product Manager using it as a portfolio piece to prove regulatory-
accountability fluency to enterprise hiring managers (fintech, regulated SaaS).

Each council member should independently surface:
1. SR-11-7 mappings that are wrong, hand-wavy, or that a model-risk officer would
   reject — name the specific component and the corrected tier + reasoning.
2. EU AI Act claims that misstate the regulation (Annex IV / Article 50 / Article 61/72)
   — quote the line and correct it.
3. The single weakest "honest gap" framing — where the card either over-confesses
   (undersells the work) or under-confesses (claims more compliance than it shows).
4. Anything that reads as a candidate performing rigor rather than demonstrating it.
5. The one change that would most increase a hiring manager's trust.

Quote specific lines/sections. Be ruthless — the author wants the strongest critique,
not validation. This is a portfolio artifact, not a regulated filing; critique it as
the strongest version of that.

=== SYSTEM CARD DRAFT ===

# Code-Brain System Card

> A model-risk and AI-governance accounting of the autonomous agent fleet I run on my own hardware — tiered to SR-11-7 materiality and mapped to the EU AI Act's technical-documentation, transparency, and post-market-monitoring obligations. The gaps are named on purpose. They're the credibility.

I built Code-Brain to run my life, not to pass an audit. It's a personal command center — an Obsidian vault plus a fleet of agents on the Claude Agent SDK that index, synthesize, critique, and research while I sleep. So this is not a regulated filing, and I'm not going to pretend it is. It's the document a model-risk officer would ask me to produce if Code-Brain *were* a production system at a bank — written against the system I actually operate, with the lines where it wouldn't pass marked in plain sight. The point isn't to claim conformance. It's to prove I can run the accounting, name the materiality, and tell you exactly where the controls stop.

---

## 1. Scope and framing

**System:** Code-Brain — ~12 live SDK agents (most on macOS `launchd` schedules, one hook-triggered), one published MCP server, a multi-vendor critique tool, and a control-plane "Judge Layer." Models are either the Claude API (cloud) or local inference on Ollama (Mac Mini / MacBook Pro). **No model is trained or fine-tuned here** — every component is an API call or a local-inference call against open weights, which collapses an entire category of model-risk obligation (training-data governance, drift-from-retraining) to "not applicable, by architecture."

**Frameworks applied:**
- **SR-11-7** — the U.S. Federal Reserve's *Supervisory Guidance on Model Risk Management* ([SR 11-7](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm)). SR-11-7 does *not* prescribe risk tiers; it requires a firm to maintain a **model inventory** and **risk-rate each model by materiality**, with validation effort commensurate with that rating. I apply a three-level Low/Medium/High rating, which is how most institutions operationalize the guidance.
- **EU AI Act** — Regulation (EU) 2024/1689. I map three obligations that would bite a system like this: [Article 50](https://artificialintelligenceact.eu/article/50/) (transparency / AI self-identification), [Article 72](https://artificialintelligenceact.eu/article/72/) (post-market monitoring by providers), and [Annex IV](https://artificialintelligenceact.eu/annex/4/) (technical documentation).

> **A precision note, because it's the kind of thing this card is supposed to get right.** Post-market monitoring is **Article 72** in the *adopted* Regulation. The widely-circulated "Article 61" is the 2021 Commission *proposal* numbering, which the final text renumbered. If you've seen this artifact cite Article 61, that was the draft; the live version is 72.

**The floor rule.** A component's materiality is set by its **highest-risk action surface, not its average one.** An agent that writes to my private vault 99% of the time and drafts a public post under my byline 1% of the time is tiered on the 1%. Materiality is blast radius, and blast radius is a worst-case property — you don't get to average it away. This is the same move the [Enterprise Data Readiness Matrix](https://github.com/seanwinslow28/enterprise-data-readiness-matrix) makes with its floor rule; a system fails at its weakest seam regardless of how clean the rest is.

---

## 2. SR-11-7 materiality tiering (the model inventory)

Materiality = blast radius of a *wrong* action: how far a bad output propagates before a human catches it, and whether it can be undone.

| Component | Materiality | Rationale (blast radius) | Validation evidence | Human-override path |
|---|---|---|---|---|
| **substack_drafter** *(built, default-disabled)* | **High** | Writes long-form drafts **under my public byline**. A fabricated quote or uncited employer claim is reputational and external. | No standalone eval suite. Failure surface is the **explicit reason the Judge Layer was built** (its first wrapped agent). | "Agents draft / I send" — never auto-publishes; output lands in a drafts dir for manual review. Judge Layer adds a programmatic gate when armed. |
| **intent-engineering MCP** *(shipped: npm + MCP registry)* | **High** | The only component **other people execute** — a published package installed into others' agents. Public-software blast radius. | Pure-function analysis tools; no `exec`, no network egress. Hardening pass scheduled (Task 23). | Out of my hands once installed — which is exactly why it's tiered High. Mitigated by stateless, side-effect-free tool design. |
| **daily_driver** *(live, cloud/Opus)* | **Medium** | The one cloud agent that loads personal operating-model context and touches calendar/email data in interactive backfill. Egresses private context to a third party; costs real money. | No dedicated eval suite. Cost behavior is instrumented and capped. | Writes only the daily-note skeleton; I review and act. Hard `$0.90` budget cap per run. |
| **deep_researcher** *(live, local)* | **Medium** | Writes research digests into the vault that I later cite. Documented to **fabricate** entities and URLs under compound prompts. | **Published post-mortem** (LDR grounding-collapse). Bad-output specimen retained as a fixture; routing rule now diverts heavy topics to Gemini DR. | Output is vault-internal; nothing acts on it without me. 900s timeout; compound topics routed off this engine. |
| **vault_synthesizer** *(live, local)* | **Medium** | Writes durable concept articles into my knowledge base that propagate into downstream reads. "Silent empty output" rot ran nine nights undetected. | **10/14 eval suite** ([evals/vault-synthesizer](https://github.com/seanwinslow28/code-brain/tree/main/evals/vault-synthesizer)), 6 failure modes open-coded from 17 days of production logs, intentionally-red baseline. | Vault-internal; I consume, nothing external acts. Eval gate + manifest monitoring. |
| **vault_critic** *(live, local + external CLIs)* | **Medium** | Sends vault excerpts to external CLIs (Codex / Anti-Gravity) and writes critique expansions back. Egress + durable write. | No formal eval suite. Both-CLI-rate-capped degrades to `status: partial` and exits clean — a documented graceful-degradation path. | Vault-internal output; manual promotion of suggestions. 600s wall budget, 120s per-CLI. |
| **skill_optimizer** *(live, manual-trigger only)* | **Medium** *(cost: High)* | Rewrites one of my own `SKILL.md` files via an Opus-generation loop. Edits agent behavior — but on a branch I merge by hand. | Local judge + periodic Sonnet sample-check every 5 iterations; plateau-halt. | Writes to a feature branch; never merges itself. `$200` hard cost cap, `$50` soft. |
| **job_feed** *(live, local)* | **Low** | Fetches public job feeds and writes roll-ups. Read-external / write-vault; no action taken on my behalf. | No eval suite. Idempotency guard; `fallback_disabled=true` preserves $0 cost. | Informational only. Per-host rate limit; MBP-asleep defers scoring rather than paying for cloud. |
| **flush** *(live, hook-triggered, local)* | **Low** | SessionEnd summarizer; writes to the daily log. Local model, vault-internal. | No eval suite. Routes by message count. | Vault-internal; reviewed in normal note flow. |
| **meta_agent** *(live, local)* | **Low** | Reads fleet health and writes a digest into the daily note. Reports on the fleet; takes no action. | No eval suite. Local model. | Read-and-report only. |
| **knowledge_lint** *(live, local)* | **Low** | Weekly vault health scan; writes a lint report. | Tier-1 structural Python checks are deterministic and self-validating. | Report-only; I act on findings. |
| **vault_indexer** *(live, local)* | **Low** | Generates embeddings into a local index DB. Read-and-embed; no generative output. | Deterministic pipeline; no LLM generation to hallucinate. | No human-facing output to override. |
| **gemini_researcher** *(built, default-disabled)* | **Medium** *(when armed)* | Paid external deep research. Dormant; would write digests like deep_researcher. | Inherits Gemini DR caps. | Opt-in install only (`INSTALL_GEMINI=1`); `$7`/task, `$20`/day, `$50`/month caps. |
| **LLM Council** *(tool, manual)* | **Low** | Multi-vendor critique I invoke by hand. Advisory output to me only. | Cost caps enforced pre-flight. | I read the synthesis; it acts on nothing. `$1`/query, `$7`/day, `$40`/month. |

**Inventory reconciliation (requested in the brief).** The roadmap's Step-1 list named 11 components, but it predates the live fleet. Two it names — `gemini_researcher` and `substack_drafter` — are **built but default-disabled**, so I mapped them and marked their state. Two that are genuinely live — `vault_critic` and `job_feed` — were **not** on the Step-1 list; I added them. `skill_optimizer` is live but manual-trigger-only. Net: the honest live count is ~12 running components plus 2 dormant-but-built, not 11.

---

## 3. The control plane: Judge Layer

The strongest governance component isn't an agent — it's the thing that sits *between* an agent's intent and its action. The **Judge Layer** ([agents-sdk/lib/judge](https://github.com/seanwinslow28/code-brain/tree/main/agents-sdk/lib/judge), shipped 2026-05-31) intercepts a typed `ActionProposal`, evaluates it against a declarative YAML policy a non-engineer can read, and returns one of five verdicts — `ALLOW`, `REVISE`, `BLOCK`, `ESCALATE`, or `JUDGE_UNAVAILABLE`. It runs on a local model at $0/decision and writes **every verdict to an append-only JSONL ledger** at `vault/health/judge_log/`. That ledger is, in EU AI Act terms, a post-market monitoring stream: a timestamped, per-decision record of what each agent tried to do and why it was allowed, revised, or stopped.

Two honest facts about it. It is **fail-open** by deliberate design: if the judge model is unreachable, the wrapped agent falls back to my manual review rather than blocking — because "agents draft / I send" is the canonical control and the judge is defense-in-depth, not the load-bearing gate. And the module-level master switch is **off by default** today; the layer is shipped and tested, but not yet armed in continuous production. A control that exists and is tested is not the same as a control that is running, and I won't blur the two.

---

## 4. EU AI Act mapping

| Obligation | What it requires | Code-Brain status |
|---|---|---|
| **Art. 50 — Transparency** | Systems that interact with people must disclose they are AI. | **N/A in practice, honestly: there is no external user to disclose to.** Code-Brain's only human is me, and I know. The one public-facing surface — the `substack_drafter` byline — is the *opposite* problem: its risk is that output reads as *human* (mine), which is why it's tiered High and routed through manual review. The MCP server self-describes as software in its registry listing. |
| **Art. 72 — Post-market monitoring** | Providers must systematically collect and analyze performance data over the system's life, per a monitoring plan. | **Partial.** The telemetry exists — `vault/health/*` JSONL ledgers, the Judge Layer's `judge_log`, nightly manifests, a fleet dashboard. What's missing is a *plan*: a written cadence that reviews this data on a schedule against thresholds. I have the stream, not the standing report. |
| **Annex IV — Technical documentation** | Training data, testing, evaluation processes, and architecture must be documented. | **Substantially present, see §5.** |

**Per-component transparency / monitoring / override**, the three Article-50/72 questions answered for the components that matter:
- *Does it self-identify as AI?* No agent does, because none faces an external human. The MCP package identifies as software to the developers who install it.
- *What's logged for monitoring?* Per-run manifests (`vault/health/`), the Judge Layer JSONL ledger, agent stderr logs, the cost ledgers (`gemini-spend-*.json`, `council-spend-*.json`), and the fleet dashboard.
- *What's the override path?* The **Tier-A "agents draft / I send" gate** — the canonical, system-wide control. Every component that could have external effect produces a draft I approve; nothing publishes, sends, or commits an irreversible external action autonomously.

---

## 5. Annex IV-style technical documentation already in place

- **Training data: none.** No component trains or fine-tunes. Every model is a Claude API call or a local-inference call against published open weights. The Annex IV training-data section is satisfied by architecture, not by paperwork.
- **Testing:** the `vault-synthesizer` eval suite (10/14, six failure modes grounded in 17 days of real logs) plus ~800-test pytest suites across the SDK layer, plus the production telemetry above. The honest scope: **one agent has a real eval suite.** The rest are validated by tests and logs, not by graded behavioral evals.
- **Evaluation processes:** documented in [CLAUDE.md](https://github.com/seanwinslow28/code-brain/blob/main/CLAUDE.md) — the architecture-decisions tables, the research-routing rule (born from the LDR grounding-collapse), the cost-cap and kill-switch design, and the per-agent state. CLAUDE.md is the de-facto system documentation; it just isn't shaped like an Annex IV file.

---

## 6. Honest gaps — where Code-Brain is not compliant

This is the load-bearing section. A scorecard you win every cell of is a sales sheet.

- **No post-market-monitoring report cadence.** Article 72 wants a *plan*, not just a *stream*. I have rich telemetry and no standing review against thresholds. The judge_log and manifests are read ad hoc, not on a written schedule. This is the single largest gap, and it's the most fixable: the data already exists.
- **No Annex IV-conformant template.** CLAUDE.md documents the system thoroughly but in its own shape. There is no document organized to Annex IV's sections, so a conformity assessor couldn't tick boxes against it.
- **No Article 13 instructions for use.** Article 13 requires providers to give deployers instructions. The published MCP server ships a README, not an Article-13-structured instruction set with the prescribed fields.
- **The Judge Layer is shipped but not armed.** Module-level switch off; first wrapped agent (`substack_drafter`) is itself disabled. The control plane is real and tested; it is not yet running in production.
- **Eval coverage is one-of-twelve.** Only `vault_synthesizer` has a graded eval suite. The high-materiality `substack_drafter` has none yet — its safety currently rests entirely on the manual-review gate and the not-yet-armed judge.
- **Article 50 self-identification is unimplemented** — defensible today (no external users), but the moment any surface faces another person, this becomes a real obligation rather than a non-applicable one.

---

## 7. Reference templates

This card is a portfolio piece modeled on public governance documents, not a regulated filing. The templates it draws from:

- **Google — Model Cards for Model Reporting** (Mitchell et al., 2019): https://arxiv.org/abs/1810.03993 — the origin of structured model documentation.
- **Anthropic — Claude system cards:** index at https://www.anthropic.com/system-cards; Claude Opus 4 & Sonnet 4 card at https://www.anthropic.com/claude-4-system-card — the safety-evaluation-plus-deployment-decision shape, organized around Responsible Scaling Policy domains.
- **OpenAI — GPT-4 System Card:** https://cdn.openai.com/papers/gpt-4-system-card.pdf; GPT-4o System Card: https://openai.com/index/gpt-4o-system-card/ — the risk-enumeration-plus-mitigation pattern.
- **EU — Declaration of Conformity:** [Article 47](https://artificialintelligenceact.eu/article/47/) + [Annex V](https://artificialintelligenceact.eu/annex/5/) — the conformance-statement template I am explicitly *not* filing, because Code-Brain is a personal system, not a high-risk AI product placed on the EU market.

---

I run a fleet that writes to my second brain every night, and until I sat down to tier it I'd never asked the question a model-risk officer asks first: *if this one were wrong, how far would it get before I noticed?* For most of Code-Brain the answer is "into my private vault, where I'd catch it." For two components — a draft under my name, a package in someone else's agent — the answer is "out the door." That's the whole value of the exercise: not the conformance I can claim, but the materiality I can name. The gaps in §6 aren't apologies. They're the build order.

*Portfolio artifact. Code-Brain is not a regulated production system; this card applies regulated-industry frameworks to it as a demonstration of accountability fluency, not as a claim of conformance.*
```

## Council responses

### anthropic/claude-opus-4.7

# Stress-test of the Code-Brain System Card

Reading this as the strongest version of itself: it's a genuinely sophisticated piece, well above the median portfolio artifact. The "blast radius = worst-case, not average" framing is correct and the kind of sentence that earns a second-round interview. Below is where it would still get hit by a real MRM officer or an AI Act-literate GC.

---

## 1. SR-11-7 mappings that wouldn't survive a model-risk officer

**(a) "No model is trained or fine-tuned here … collapses an entire category of model-risk obligation … to 'not applicable, by architecture.'"**

This is the single most consequential error in the card, and an MRM officer would flag it in the first ten minutes. SR-11-7 defines a "model" by *function*, not provenance:

> "the term model refers to a quantitative method, system, or approach that applies statistical, economic, financial, or mathematical theories, techniques, and assumptions to process input data into quantitative estimates."

A *vendored* or *third-party* model is explicitly in scope — SR-11-7 has a dedicated section on "External Resources" requiring the firm to validate vendor models *as if* they were internal, including conceptual soundness and ongoing monitoring, even when the firm has no access to training data. Claiming "not applicable, by architecture" because you didn't train it is exactly the framing the guidance was written to reject. The correct statement is: *training-data governance obligations are inherited from the provider and must be validated as a third-party model risk; drift risk shifts from retraining to silent vendor model updates (e.g., Anthropic point releases), which is arguably harder to monitor, not easier.*

This one line will cost the card credibility with anyone who has actually run an MRM function.

**(b) `intent-engineering MCP` rated High on "public-software blast radius."**

An MRM officer would push back: SR-11-7 materiality is about *model* risk — the risk that a quantitative output is wrong and causes a bad decision. A pure-function, side-effect-free analysis tool with no `exec` and no network egress is closer to a *library* than a *model*. The High rating conflates **software supply-chain risk** (real, but governed by SDLC/AppSec, not MRM) with **model risk**. Corrected tier: **Low-to-Medium for model risk**, with a separate, explicit callout that supply-chain risk is the dominant axis and is governed elsewhere. The current framing reads as if the author wants a High in the inventory for narrative symmetry.

**(c) `skill_optimizer` — "Medium *(cost: High)*"**

Splitting materiality into two axes inside a single cell is exactly the hand-wave a validator catches. SR-11-7 wants *one* materiality rating that drives validation effort. Worse, `skill_optimizer` **edits the behavior of other agents in the fleet** — that's a model-on-model meta-risk, the kind of feedback loop SR-11-7's "model interconnection" concerns target. The fact that the merge is manual is a *control*, not a *materiality reduction*. Correct rating: **High, mitigated to Medium residual by the manual-merge gate.** Distinguishing inherent vs. residual materiality is table stakes in MRM and its absence here is conspicuous.

**(d) `vault_synthesizer` at Medium while `deep_researcher` is also Medium.**

`vault_synthesizer` writes *durable* concept articles that "propagate into downstream reads" — i.e., they're cited and built upon. `deep_researcher` writes digests the author then re-reads. The propagation depth is meaningfully different and the synthesizer arguably deserves a higher rating than the researcher under the card's own blast-radius logic. The "silent empty output ran nine nights undetected" anecdote is itself evidence that detection latency on this component is poor — which under SR-11-7 *raises* materiality, not lowers it.

**(e) Missing: no statement of validation independence.**

SR-11-7's central control is **effective challenge by parties independent of development**. The card never addresses this — understandably, because the author is a one-person shop. But the honest move is to *name* that constraint ("no independent validation function exists; the LLM Council partially substitutes by providing multi-vendor adversarial review") rather than leave it unspoken. A validator would notice the omission immediately.

---

## 2. EU AI Act claims that misstate the regulation

**(a) Article 50 framed as "Transparency / AI self-identification."**

Article 50 is broader than the card implies. It covers four distinct obligations:

- 50(1): providers of systems intended to interact with natural persons must design them so users are *informed* they're interacting with AI.
- 50(2): providers of generative systems must mark outputs as artificially generated in a machine-readable format.
- 50(3): deployers of emotion-recognition / biometric categorization must inform exposed persons.
- 50(4): deployers of deepfake / synthetic content must disclose.

The `substack_drafter` is the live wire here. The card says: *"its risk is that output reads as human (mine), which is why it's tiered High."* Under **Art. 50(4)**, content that is "artificial or manipulated … which would falsely appear to a person to be authentic" triggers a disclosure obligation, with a carve-out for "evidently artistic, creative … work." A Substack post drafted by AI and published under a human byline is plausibly in scope of 50(4), and the obligation is *not* satisfied by an internal review gate — it requires disclosure to readers. The card's framing ("N/A in practice, honestly: there is no external user") is wrong on its own facts the moment `substack_drafter` ships. The correct statement: *"Art. 50(4) would apply to substack_drafter outputs; current mitigation is non-deployment. Disclosure design is a precondition to enabling."*

Also: **Art. 50(2)** obligations on generative-output marking (machine-readable watermarking/provenance) is the more interesting gap and isn't mentioned at all.

**(b) Article 72 — "Providers must systematically collect and analyze performance data…"**

The actual text:

> "Providers shall establish and document a post-market monitoring system in a manner that is proportionate to the nature of the AI technologies and the risks of the high-risk AI system."

The card's paraphrase drops the critical qualifier: **Article 72 applies to *high-risk* AI systems** as defined by Article 6 and Annex III. Code-Brain is not a high-risk system under any Annex III category. So Article 72 doesn't bite *at all* — not "partial," not "missing a plan." The honest mapping is: *"Art. 72 inapplicable; I am modeling the discipline voluntarily as a portfolio demonstration."* Claiming "Partial" compliance to a regime that doesn't apply to you is the kind of category error that reads to a regulated-SaaS hiring manager as *not actually understanding which regime applies* — which is the opposite of the impression intended.

The same critique lands harder on **Annex IV**: Annex IV is the technical-documentation requirement for **high-risk systems under Article 11**. Saying it is "substantially present" presumes the system is in scope. It isn't.

**(c) Article 13 reference in §6.**

> "Article 13 requires providers to give deployers instructions."

Article 13 is titled "Transparency and provision of information to deployers" and applies to **high-risk** systems. Same scope problem as Art. 72. Also, the published MCP server's "deployers" are open-source developers, not deployers in the AI Act sense (which means a natural/legal person using a high-risk system in a professional capacity). Inserting Art. 13 here is genuine over-reach.

**(d) The Art. 61 / Art. 72 "precision note."**

This is well-intentioned and correctly identifies the renumbering. But the framing — "A precision note, because it's the kind of thing this card is supposed to get right" — combined with the *actual* misapplication of Art. 72's scope, produces the worst possible impression: pedantic about a citation number while wrong about the substance. Either get the substance right or drop the flex.

---

## 3. The single weakest "honest gap" framing

**Under-confession, in §4:** *"Art. 50 — N/A in practice, honestly: there is no external user to disclose to."*

This is the line that, on a careful second read, undermines the card. `substack_drafter` is **literally a public-byline generator** — the author has already identified it as the highest external-blast-radius component in the fleet. Saying Art. 50 is N/A while simultaneously documenting a built-but-disabled deepfake-adjacent component contradicts itself within the same artifact. The card *almost* notices this — "its risk is that output reads as *human* (mine)" — and then steers away from the obvious conclusion that this *is* the Art. 50(4) trigger.

The corrected framing: *"Art. 50 is currently dormant because the one in-scope surface (`substack_drafter`) is disabled. Enabling it without an AI-disclosure mechanism would be the act that puts this system in scope. The control gating that decision is the module-level switch, not a design feature."* That version is honest, technically correct, and demonstrates exactly the regulatory thinking the card claims.

---

## 4. Performing rigor vs. demonstrating it

A few tells that read as performance:

- **"The gaps are named on purpose. They're the credibility."** Followed by **"This is the load-bearing section. A scorecard you win every cell of is a sales sheet."** Followed by **"The gaps in §6 aren't apologies. They're the build order."** Three variants of the same meta-move in one document. Once is sharp; three times is a candidate underlining their own self-awareness. Cut two of them.

- **The Article 61/72 precision note.** Performs pedantry to inoculate against a charge of imprecision — while the actual scoping of Art. 72 is wrong. This is the highest-cost performance moment in the card.

- **"This is the same move the Enterprise Data Readiness Matrix makes with its floor rule."** Self-citation to another of the author's portfolio pieces inside a system card reads as resume-stuffing, not as a load-bearing reference. Either the floor rule is self-justifying (it is) or it needs an external citation (Reason's Swiss-cheese model, for instance). Citing your own GitHub repo as authority is a tell.

- **`skill_optimizer` "Medium (cost: High)"** — the dual-rating is a *visible* refusal to commit to one number, which a validator reads as the author not wanting to put a High in the inventory.

- **Footnote-style precision on Article numbers** alongside the "no model is trained here, so training-data governance is N/A" claim. The big thing is wrong; the small things are precise. That pattern is what "performing rigor" *means*.

- **"~800-test pytest suites across the SDK layer"** as Annex-IV evaluation evidence. Unit tests are not model evaluations and an MRM officer or AI Act assessor would say so. The card elsewhere distinguishes these correctly ("validated by tests and logs, not by graded behavioral evals") — but listing the 800 tests in the *Annex-IV testing* bullet undercuts that distinction.

---

## 5. The single change that would most increase a hiring manager's trust

**Reframe the entire card as a voluntary application of frameworks that do not, by their own terms, apply — and be explicit about why each was chosen anyway.**

Specifically: open §4 with a one-paragraph **scope determination** that states (i) Code-Brain is not a financial institution's model under SR-11-7 jurisdiction; (ii) Code-Brain is not a high-risk AI system under AI Act Article 6 / Annex III, so Articles 11, 13, and 72 and Annex IV do not apply by their own terms; (iii) Article 50 *would* apply at the moment `substack_drafter` or any external surface activates; (iv) the author is nonetheless modeling the full regulated-system discipline as a demonstration of *what the work looks like* — and naming the gaps that would exist *if* the system were in scope.

This single change does three things simultaneously:

1. It removes every "Partial / N/A" claim that currently misstates the regulation's scope, replacing them with a clean "inapplicable, modeled voluntarily" — which is *more* impressive, not less, because correctly scoping a regulation is the first thing a regulated-SaaS GC tests for.
2. It dissolves the Article 50 contradiction by making explicit that the disclosure obligation is *activation-gated*, not absent.
3. It converts the card from "here is what I comply with" (which invites the question "but does any of this apply to you?") to "here is what I would owe, and what I would have ready, the day this system became a regulated product" — which is exactly the deliverable a fintech or regulated-SaaS PM role needs to produce in week one.

The author already has the instinct — the closing line, "*Code-Brain is not a regulated production system; this card applies regulated-industry frameworks to it as a demonstration*," is the thesis. It belongs at the top, structuring the document, not in italics at the bottom apologizing for it.

### openai/gpt-5.5

## Bottom line

This is a strong portfolio artifact rhetorically, but it overclaims regulatory mapping in exactly the places a model-risk officer or AI Act reviewer would challenge: it mixes **model risk, privacy risk, cyber/supply-chain risk, cost risk, and product-liability risk** into one “materiality” tier; it treats EU AI Act obligations as if they apply generically to “AI systems like this” rather than mostly to **high-risk AI systems, GPAI providers, or specific transparency-triggering use cases**; and it repeatedly converts “I have logs / tests / README / manual review” into quasi-compliance language.

The strongest version would separate: **model risk tier**, **data/privacy risk**, **operational/cyber risk**, **external-impact risk**, and **current vs inherent risk**.

---

# 1. SR-11-7 mappings a model-risk officer would reject

## Cross-cutting problem: you are tiering “components,” not “models,” and mixing risk types

> “## 2. SR-11-7 materiality tiering (the model inventory)”

A model-risk officer would push back immediately: this is not a clean **model inventory**. It is an **application/component inventory**. Some entries are models or model-enabled workflows; others are deterministic tools, schedulers, dashboards, MCP packages, or control-plane infrastructure.

SR 11-7 model inventories usually require at least:

- model name/version;
- owner;
- business use / intended use;
- model type;
- input data;
- output;
- downstream decision/use;
- limitations;
- materiality/inherent risk;
- residual risk after controls;
- validation status;
- implementation status;
- change-control status;
- retirement/monitoring plan.

Your table has some of that, but not enough to pass as an SR 11-7-style inventory.

Also, this line is only half right:

> “Materiality = blast radius of a *wrong* action: how far a bad output propagates before a human catches it, and whether it can be undone.”

That is a good intuition, but SR 11-7 materiality is not only blast radius. It also turns on **business use, financial exposure, regulatory/legal impact, customer impact, complexity, reliance, frequency, substitutability, and control environment**. You are collapsing all of that into one “wrong action” dimension.

---

## `intent-engineering MCP` — wrongly classified as High model risk

> “**intent-engineering MCP** *(shipped: npm + MCP registry)* | **High** | The only component **other people execute** — a published package installed into others' agents. Public-software blast radius.”

This is probably not a **High SR-11-7 model-risk** item. It may be **Medium/High cyber, product, supply-chain, or open-source liability risk**, but that is not the same as model risk.

You say:

> “Pure-function analysis tools; no `exec`, no network egress.”

If it is mostly deterministic tooling, it may not be a “model” under SR 11-7 at all. If it shapes prompts or downstream agent behavior, it could be a **model-enabled control/tool**, but the materiality depends on how deployers use it, not merely that it is public.

**Corrected classification:**

- **SR-11-7 model risk:** Low or out-of-scope unless it uses predictive/generative logic that affects decisions.
- **Operational/cyber/product risk:** Medium to High because others install it.
- **Required correction:** Do not call it High model risk solely because it is distributed software. Label it “non-model component / third-party-use operational risk.”

A model-risk officer would say: public execution is not SR-11-7 materiality by itself.

---

## `substack_drafter` — High may be right as inherent risk, but wrong as current/residual risk

> “**substack_drafter** *(built, default-disabled)* | **High** | Writes long-form drafts **under my public byline**.”

This is overstated. It does **not** write under your public byline if it only creates local drafts.

You also say:

> “never auto-publishes; output lands in a drafts dir for manual review.”

So the current action surface is not “public byline”; it is “private draft later reviewed by human.”

**Corrected classification:**

- **Current active risk:** Not active / dormant.
- **Inherent risk if enabled and allowed to draft publishable public content:** Medium to High.
- **Residual risk with mandatory human editorial approval and no auto-publication:** Medium.
- **High only if:** it can publish, email, submit, or otherwise externally disseminate without meaningful human review.

The right structure is: **Inherent: High; Residual: Medium; Current status: disabled.** Right now the table makes dormant/private-draft behavior sound like autonomous public publication.

---

## `daily_driver` — Medium model risk is weakly justified; you are mostly describing privacy/vendor risk

> “The one cloud agent that loads personal operating-model context and touches calendar/email data in interactive backfill. Egresses private context to a third party; costs real money.”

This rationale is mostly **privacy, data governance, vendor, and cost risk**, not SR-11-7 model risk. SR 11-7 cares about the consequences of model output being wrong or misused. You need to describe what decision it supports or what action it takes.

You say:

> “Writes only the daily-note skeleton; I review and act.”

That sounds Low model risk.

**Corrected classification:**

- **Model risk:** Low, unless it makes material scheduling, financial, employment, or communication decisions.
- **Data/privacy/vendor risk:** Medium.
- **Operational cost risk:** Low; a `$0.90` cap is not material in enterprise model-risk terms.

If you want Medium, justify it as: “contains sensitive personal data and may influence daily prioritization,” not as “egresses context and costs money.”

---

## `vault_critic` — Medium is again mostly egress risk, not model risk

> “Sends vault excerpts to external CLIs ... Egress + durable write.”

This is not a clean model-risk rationale. Egress is data/privacy/vendor risk. Durable write to a private vault is not by itself Medium model risk unless downstream use is material.

**Corrected classification:**

- **Model risk:** Low to Medium depending on whether its critiques influence external/public/employment/financial decisions.
- **Data/privacy risk:** Medium.
- **Third-party tool/vendor risk:** Medium.

A bank MRO would ask you to split the risk dimensions.

---

## `vault_synthesizer` — Medium may be defensible, but the rationale is incomplete

> “Writes durable concept articles into my knowledge base that propagate into downstream reads. ‘Silent empty output’ rot ran nine nights undetected.”

This is one of the better entries because you have actual evaluation evidence. But “durable concept articles” is still vague. What decisions do they support? If this only affects your private notes, Low may be more appropriate. If those notes feed public claims, job materials, code, product decisions, or research artifacts, Medium is defensible.

**Corrected classification:**

- **Low** if it only writes private knowledge artifacts with manual consumption.
- **Medium** if the KB is used as a source for public writing, portfolio claims, code generation, or professional decisions.
- Add explicit downstream-use examples.

Right now you are relying on “persistence” as a proxy for materiality. Persistence is not enough.

---

## `deep_researcher` — Medium is plausible, but should be tied to downstream external use

> “Writes research digests into the vault that I later cite. Documented to fabricate entities and URLs under compound prompts.”

This is probably the strongest Medium case because it can create false citations that later leave the vault. But your human-override path says:

> “Output is vault-internal; nothing acts on it without me.”

That control reduces residual risk.

**Corrected classification:**

- **Inherent risk:** Medium.
- **Residual risk:** Low/Medium depending on citation-review controls.
- Add whether generated URLs/citations are programmatically checked.

A model-risk officer would want validation around citation accuracy, source grounding, URL existence, and quote fidelity.

---

## `skill_optimizer` — “Medium (cost: High)” is not a valid SR-11-7 tiering move

> “**Medium** *(cost: High)*”

This is a category error. Cost risk should not be jammed into the model-risk tier. Also:

> “Rewrites one of my own `SKILL.md` files via an Opus-generation loop. Edits agent behavior — but on a branch I merge by hand.”

Because it modifies agent behavior, it may be more important than you are giving it credit for, especially if those skills are reused by multiple agents.

**Corrected classification:**

- **Inherent model/operational risk:** Medium, possibly High if it can alter controls, prompts, routing, or safety policies used by higher-risk agents.
- **Residual risk:** Medium/Low if branch review is real and documented.
- **Cost risk:** separate field, not a parenthetical tier.

Required fix: define whether it can modify governance files, judge policies, prompt templates, secrets handling, routing, or tool permissions.

---

## `LLM Council` — Low ignores third-party data egress and governance influence

> “Multi-vendor critique I invoke by hand. Advisory output to me only.”

Low is plausible if you submit only non-sensitive content. But if this sends internal governance artifacts, proprietary code, personal notes, or confidential business context to multiple vendors, then the primary risk is not model output; it is data leakage and third-party handling.

**Corrected classification:**

- **Model risk:** Low.
- **Data/vendor risk:** Medium unless redaction controls are documented.
- Add: allowed content classes, redaction rules, vendor retention settings, logging, and opt-out status.

---

## `vault_indexer` — “no generative output” does not mean no model risk

> “Generates embeddings into a local index DB. Read-and-embed; no generative output.”

This is Low, but the rationale is too glib. Embedding systems can create retrieval errors, privacy issues, stale-index problems, or semantic misrouting. No hallucination does not mean no risk.

**Corrected classification:**

- **Model risk:** Low.
- **Data/security risk:** Low/Medium depending on what is embedded and whether the index is protected.
- Better rationale: “local-only, no external action, no autonomous decisioning.”

---

## `knowledge_lint` and deterministic tools — should not all be in the model inventory

> “Tier-1 structural Python checks are deterministic and self-validating.”

If deterministic, this may be a control or utility, not a model. Include it in a **system/component inventory**, but not necessarily the **SR-11-7 model inventory**.

**Corrected classification:**

- **Model inventory:** out of scope if no model/statistical/AI method.
- **Control inventory:** Low operational risk.

---

## Judge Layer — not a model-risk control if it is off and fail-open

> “The strongest governance component isn't an agent — it's the thing that sits *between* an agent's intent and its action.”

Then:

> “It is **fail-open** by deliberate design...”

And:

> “the module-level master switch is **off by default** today”

This means it is not currently a load-bearing control. It is design evidence, not operating control evidence.

A model-risk officer would not give you much residual-risk credit for a control that is:

- off by default;
- not continuously operating;
- fail-open;
- dependent on local model availability;
- not independently validated;
- not backed by alerting, exception review, or control-effectiveness metrics.

**Corrected treatment:**

- Count it as a **planned / tested control**, not an active production control.
- Do not use it to justify residual tiering until armed and monitored.
- Add “control status: designed / implemented / operating / tested / monitored.”

---

# 2. EU AI Act claims that misstate or overstate the regulation

## Claim: “I map three obligations that would bite a system like this”

> “I map three obligations that would bite a system like this: Article 50 ... Article 72 ... and Annex IV.”

This is too broad and partially wrong.

Article 72 and Annex IV do **not** generally “bite a system like this.” They primarily apply to **providers of high-risk AI systems**. Article 50 applies only in specified transparency scenarios, not to every AI system.

**Correction:**

Say:

> “I use Article 50, Article 72, and Annex IV as reference controls. Strictly speaking, Article 72 and Annex IV apply to high-risk AI systems, and Code-Brain is not being placed on the EU market as a high-risk AI system.”

---

## Article 50 line is oversimplified

> “**Art. 50 — Transparency** | Systems that interact with people must disclose they are AI.”

This is materially incomplete. Article 50 has several distinct obligations:

- providers must design systems intended to interact directly with natural persons so people are informed they are interacting with AI, unless obvious;
- providers of AI systems generating synthetic audio/image/video/text content must ensure outputs are machine-readable marked, subject to limits;
- deployers of emotion recognition or biometric categorization systems have disclosure obligations;
- deployers of systems generating or manipulating deepfakes must disclose;
- deployers generating/manipulating text published to inform the public on matters of public interest must disclose AI generation unless there was human review/editorial control and responsibility.

**Correction:**

Replace with:

> “Article 50 imposes specific transparency duties for AI systems that directly interact with natural persons and for certain AI-generated or manipulated content, including deepfakes and public-interest text, subject to exceptions such as human review and editorial responsibility.”

---

## Article 50 “N/A” is too confident

> “**N/A in practice, honestly: there is no external user to disclose to.** Code-Brain's only human is me, and I know.”

This is mostly fine for purely private use, but you underplay the public-content branch. The relevant issue is not only whether the AI “interacts” with an external user. If `substack_drafter` helps generate text that is published to inform the public on matters of public interest, Article 50 may be relevant to the **deployer disclosure** obligation, unless the human-review/editorial-responsibility exception applies.

You partly notice this:

> “The one public-facing surface — the `substack_drafter` byline — is the *opposite* problem: its risk is that output reads as *human* (mine)”

But you frame it as reputation/model risk, not as the specific Article 50 text-publication issue.

**Correction:**

Say:

> “Article 50 is not triggered for private vault agents. For public writing, the relevant Article 50 question is whether AI-generated or AI-manipulated text is published to inform the public on matters of public interest, and whether human review/editorial responsibility removes or modifies the disclosure obligation.”

---

## MCP registry self-description is not an Article 50 control

> “The MCP server self-describes as software in its registry listing.”

This does not meaningfully satisfy Article 50. Article 50 is about informing natural persons when they interact with an AI system or when certain synthetic content is generated/manipulated. A registry listing saying “software” is not the relevant disclosure mechanism.

**Correction:**

Either remove this or recast it as product documentation, not Article 50 transparency.

---

## Article 72 line omits “high-risk”

> “**Art. 72 — Post-market monitoring** | Providers must systematically collect and analyze performance data over the system's life, per a monitoring plan.”

Incomplete. Article 72 is for **providers of high-risk AI systems**.

**Correction:**

> “Article 72 requires providers of high-risk AI systems to establish and document a post-market monitoring system, proportionate to the nature of the AI technology and risks, to collect, document, and analyze relevant performance data throughout the system’s lifetime.”

Also: a private personal system not placed on the EU market is not a “provider” obligation in the ordinary sense.

---

## Judge Layer log is not “in EU AI Act terms” a post-market monitoring stream

> “That ledger is, in EU AI Act terms, a post-market monitoring stream: a timestamped, per-decision record of what each agent tried to do and why it was allowed, revised, or stopped.”

This overclaims. A log can be evidence used in a post-market monitoring system, but it is not itself “post-market monitoring” under Article 72.

Article 72 expects a **system and plan** for collecting, documenting, and analyzing performance data, including feedback loops into risk management, corrective action, and compliance duties. Logs without review cadence, thresholds, incident classification, root-cause workflow, and corrective-action process are telemetry, not PMS.

**Correction:**

> “The judge ledger would be one input to an Article 72-style post-market monitoring system. By itself it is telemetry, not a monitoring plan or post-market monitoring system.”

---

## Annex IV summary is too narrow

> “**Annex IV — Technical documentation** | Training data, testing, evaluation processes, and architecture must be documented.”

Annex IV is broader. It includes general description, intended purpose, provider details, system versions, interaction with other systems, design specs, development process, data requirements, monitoring/human oversight, risk-management system, changes, conformity assessment information, standards used, and more.

**Correction:**

> “Annex IV requires high-risk AI technical documentation covering the system’s general description, intended purpose, versions, architecture, development process, data requirements, validation/testing, risk management, human oversight, monitoring, cybersecurity where relevant, changes, and conformity-assessment information.”

---

## “Training data: none” does not satisfy Annex IV by architecture

> “**Training data: none.** No component trains or fine-tunes... The Annex IV training-data section is satisfied by architecture, not by paperwork.”

This is one of the weakest legal claims. If you are a provider of a high-risk system built on third-party models, you do not get to erase data documentation by saying “I did not train.” You still need to document:

- third-party model dependencies;
- model versions;
- known limitations;
- data inputs used by your system;
- retrieval/indexing data;
- evaluation datasets;
- data governance for operational inputs;
- if applicable, training/validation/test data used for components you developed.

You can say “no fine-tuning performed,” but not “training-data section satisfied.”

**Correction:**

> “No component is trained or fine-tuned by me, so first-party training-data documentation is not applicable. An Annex IV-style file would still need third-party model provenance, model/version documentation, input-data specifications, evaluation datasets, retrieval/index data descriptions, and known limitations.”

---

## “Substantially present” is not supportable

> “**Annex IV — Technical documentation** ... **Substantially present, see §5.**”

Then §5 says:

> “The honest scope: **one agent has a real eval suite.** The rest are validated by tests and logs, not by graded behavioral evals.”

And:

> “CLAUDE.md is the de-facto system documentation; it just isn't shaped like an Annex IV file.”

This is not “substantially present.” It is partially present as engineering documentation. Annex IV-style documentation is not substantially present if:

- no Annex IV template exists;
- only one agent has behavioral evals;
- no high-risk classification analysis exists;
- no risk-management file exists;
- no instructions for use;
- no conformity-assessment mapping;
- no data governance section;
- no versioned dependency/model inventory;
- no human-oversight specification by component;
- no cybersecurity/resilience documentation;
- no change-control evidence.

**Correction:**

Use:

> “Partially present as engineering documentation; not Annex IV-conformant.”

---

## Article 13 gap is misplaced

> “**No Article 13 instructions for use.** Article 13 requires providers to give deployers instructions. The published MCP server ships a README, not an Article-13-structured instruction set with the prescribed fields.”

This is technically true only for **high-risk AI systems**. Article 13 is a high-risk-system transparency/instructions obligation. Your MCP server is not shown to be high-risk.

**Correction:**

> “If the MCP server were part of a high-risk AI system, Article 13-style instructions for use would be required. Today, this is better treated as a voluntary documentation gap, not an applicable legal obligation.”

---

## Article 61/72 precision note is mostly correct, but could be more careful

> “Post-market monitoring is **Article 72** in the *adopted* Regulation. The widely-circulated ‘Article 61’ is the 2021 Commission *proposal* numbering, which the final text renumbered.”

This is directionally right. The issue is not the numbering; it is that you later imply Article 72 broadly applies. The bigger correction is: **Article 72 final applies to high-risk AI providers.**

---

# 3. Single weakest “honest gap” framing

The weakest gap framing is this:

> “**Annex IV — Technical documentation** | Training data, testing, evaluation processes, and architecture must be documented. | **Substantially present, see §5.**”

And then:

> “**No Annex IV-conformant template.** CLAUDE.md documents the system thoroughly but in its own shape. There is no document organized to Annex IV's sections, so a conformity assessor couldn't tick boxes against it.”

This under-confesses. The problem is not merely that the material is not in the right template. The problem is that large parts of Annex IV-style documentation are missing or only loosely implied.

Missing or weak:

- high-risk classification rationale;
- intended purpose by component;
- foreseeable misuse;
- system boundaries;
- model/version/dependency list;
- data input specifications;
- third-party model provenance;
- risk-management file;
- human oversight design;
- monitoring plan;
- incident thresholds;
- corrective-action process;
- cybersecurity/resilience controls;
- change-management records;
- validation protocols for most agents;
- performance metrics by intended use;
- user/deployer instructions where relevant.

So the honest gap should not be “no Annex IV-conformant template.” It should be:

> “I have engineering documentation and some eval evidence, but I do not yet have an Annex IV-style technical file. The gap is substantive, not just formatting.”

That one change would make the card much more credible.

---

# 4. Things that read as performing rigor rather than demonstrating it

## “The gaps are named on purpose. They're the credibility.”

This is polished, but too self-certifying. Naming gaps is good. It is not itself credibility. Credibility comes from evidence, repeatable controls, and clear scoping.

## “the document a model-risk officer would ask me to produce”

> “It's the document a model-risk officer would ask me to produce if Code-Brain *were* a production system at a bank”

Not quite. A model-risk officer would ask for a model inventory, model development documentation, validation reports, implementation testing, monitoring reports, change logs, issue inventory, and governance approvals. This card is a narrative governance memo, not the document they would ask for.

Better:

> “It is a portfolio-style approximation of the questions a model-risk officer would ask.”

## “Training data... collapses an entire category of model-risk obligation”

> “No model is trained or fine-tuned here... which collapses an entire category of model-risk obligation... to ‘not applicable, by architecture.’”

This sounds sophisticated but is overbroad. You still have data obligations: input data, retrieval corpus, eval fixtures, embeddings, prompt logs, vendor model provenance, model limitations, and third-party data rights/security.

## “The floor rule”

> “Materiality is blast radius, and blast radius is a worst-case property — you don't get to average it away.”

This is rhetorically good, but it creates bad tiering because you do not distinguish **inherent vs residual** or **current vs dormant**. Worst-case tiering is useful, but without status/control separation it overstates disabled components and understates active data-risk components.

## “append-only JSONL ledger”

> “append-only JSONL ledger”

Unless you have file permissions, hash chaining, WORM storage, signing, or tamper-evidence, this reads like inflated audit language. A local JSONL file is a log, not necessarily an audit-grade ledger.

## “Pure-function analysis tools; no `exec`, no network egress.”

Good security facts, but irrelevant to the claimed High SR-11-7 model-risk tier. It shows hardening, not model-risk validation.

## “~800-test pytest suites”

> “plus ~800-test pytest suites across the SDK layer”

This is impressive engineering, but it is not model validation unless you classify which tests validate model behavior, controls, routing, policies, failure modes, and monitored metrics. Otherwise it reads like test-count theater.

## “The strongest governance component”

> “The strongest governance component isn't an agent — it's the thing that sits between an agent's intent and its action.”

Then you disclose it is off by default and fail-open. The language outruns the control evidence.

## “Substantially present”

As above, this is the worst phrase in the EU mapping. It makes the gap section feel less honest.

---

# 5. One change that would most increase hiring-manager trust

Add a **one-page control matrix that separates inherent risk, residual risk, risk type, control status, and evidence**.

Right now the card is persuasive but muddy. The best change would be a table like this:

| Component | Current status | Inherent model risk | Residual model risk | Data/privacy risk | Op/cyber risk | External-impact risk | Key controls | Control status | Evidence | Open gap |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---|

Example:

| `substack_drafter` | Disabled | High | Medium if enabled | Medium | Low | High | manual editorial review; no auto-publish; planned Judge Layer | manual control active only when used; Judge off | draft directory; policy YAML tests | no eval suite; judge not armed |
| `intent-engineering MCP` | Shipped | Low / non-model | Low | Low | Medium/High | Medium | no exec; no network; stateless | implemented | code review/tests | needs security review, SBOM, release signing |
| `daily_driver` | Live | Low | Low | Medium | Low | Low | local write only; budget cap | operating | logs/cost ledger | no data classification/redaction policy |
| `vault_synthesizer` | Live | Medium | Medium/Low | Low | Low | Low/Medium | eval suite; manifest monitoring | operating | 10/14 evals; logs | expand eval coverage |

That would show you understand the difference between:

- model risk vs privacy/cyber/operational risk;
- inherent risk vs residual risk;
- active controls vs designed controls;
- legal applicability vs voluntary benchmark mapping.

If you make only one substantive revision, make that one. It would convert the artifact from “smart PM performing governance literacy” into “operator who can structure a defensible risk inventory.”

### ~google/gemini-pro-latest

Here is a direct, ruthless stress-test of the system card, evaluated from the perspective of an enterprise risk and governance hiring manager. 

### 1. SR-11-7 mapping: Rejected component
**Quote:** `intent-engineering MCP` ... `High` ... *"Pure-function analysis tools; no exec, no network egress."*
**Corrected Tier:** **Not a Model (Remove from Inventory) / N/A.**
**Reasoning:** You fundamentally misunderstand what SR-11-7 regulates. SR-11-7 (Section II) defines a "model" as a quantitative method applying statistical, economic, or mathematical theories, explicitly clarifying that deterministic logic, pure functions, and simple IT tools *are not models*. If your MCP server is a "pure-function analysis tool" without probabilistic generation (non-LLM), it belongs in standard IT Asset Management, not the Model Inventory. Categorizing a deterministic npm package as a "High-Risk Model" tells a Model Risk Officer you only know the buzzwords, not the regulatory definitions.

*(Secondary mapping failure: `skill_optimizer` is listed as **Medium**, but it alters the behavior of other agents. In MRM, a model that governs, tunes, or outputs code for a High-Risk model automatically inherits the downstream model's High-Risk rating. You cannot rate a meta-model Medium if it controls the output parameters of a High-risk system).*

### 2. EU AI Act misstatement: Article 72 / High-Risk scoping
**Quote:** *"EU AI Act... I map three obligations that would bite a system like this: ... Article 72 (post-market monitoring by providers)"* and *"Art. 72 — Post-market monitoring | Providers must systematically collect and analyze performance data... | Partial."*
**Correction:** This is a fatal misunderstanding of the AI Act’s structural applicability. Article 72 (Title III, Chapter 8) applies **exclusively to High-Risk AI systems** (as defined in Article 6 and Annex III, such as biometrics, critical infrastructure, credit scoring, or HR). Your personal note-taking and coding agent fleet is Minimal Risk. Article 72 does not "bite a system like this"—it is entirely legally inapplicable. Claiming "Partial" compliance with Article 72 (and Article 13 later) shows you skimmed the regulation for the word "monitoring" without understanding the risk-based tiering that serves as the foundation of the law. 

### 3. The weakest "honest gap" framing
**Quote:** *"The Judge Layer is shipped but not armed. Module-level switch off; first wrapped agent (substack_drafter) is itself disabled... the control plane is real and tested; it is not yet running in production."*
**Critique:** This drastically under-confesses the vulnerability and invalidates your entire MRM posture. Your only generative *High-Risk* model (`substack_drafter`) relies completely on this Judge Layer to mitigate its risk. A risk control that is turned off, protecting an agent that is also turned off, is not a "gap"—it is vaporware. You are counting disabled code as your primary defense-in-depth on your highest-blast-radius surface. To an auditor, a deactivated control equals zero control. Framing this as "shipped but not armed" is spinning a fundamental system failure as a roadmap item.

### 4. Performing rigor rather than demonstrating it
**Quote:** *"The floor rule. A component's materiality is set by its highest-risk action surface, not its average one... blast radius is a worst-case property — you don't get to average it away. This is the same move the Enterprise Data Readiness Matrix makes..."*
**Critique:** This is performative security theater. In enterprise risk management, you actually *do* factor in probability and frequency when calculating expected exposure (Risk = Impact × Likelihood). If a model does low-risk work 99% of the time and high-risk work 1% of the time, an institution doesn’t just blindly label the whole monolith "High" and eat the massive regulatory overhead. They segment the system: they build a separate pipeline/model ID for the 1% use case to contain the compliance cost. Proclaiming "you don't get to average it away" sounds tough to a layman, but to a risk professional, it sounds like an inability to properly architect workload isolation.

### 5. The single change to most increase a hiring manager's trust
**Stop assuming all regulations apply, and add an "Applicability Scope" section.**
Before mapping obligations, you must demonstrate the skill of *ruling regulations out*. A fintech Hiring Manager doesn't want a PM who wastes $500k in engineering resources building compliance tools for laws that don't apply. 

Add a section at the top of the EU AI Act mapping stating: 
> *"Applicability Analysis: Code-Brain does not meet the criteria for Prohibited AI (Title II) or High-Risk AI (Title III / Annex III). Therefore, technical documentation (Annex IV), instructions for use (Article 13), and post-market monitoring (Article 72) are legally N/A. However, to demonstrate enterprise readiness, I am mapping against these High-Risk requirements voluntarily to show how I would govern a regulated system."* 

This single adjustment proves you know how to read the actual law, contextualize product risk, and separate mandatory legal obligations from voluntary best practices.

### x-ai/grok-4.20

**1. SR-11-7 mappings that are wrong, hand-wavy, or that a model-risk officer would reject**

* **substack_drafter — rated High.** A model-risk officer would reject this as both inflated and misapplied. SR 11-7 (and every bank's implementation) ties materiality to *financial, regulatory, or customer-impact* exposure, not "reputational" personal byline risk. This is personal reputational risk, not bank-level model risk. Correct tier inside a bank context: **Low** (or at most Medium-Low if it touched customer communications at scale). The blast-radius language is copied from enterprise risk but applied to a solo author's Substack. A CRO would call this category error.

* **intent-engineering MCP — rated High because "other people execute".** This is the most hand-wavy entry. SR 11-7 materiality is driven by the *deploying institution's* exposure, not whether code is open-source. Publishing an npm package does not magically make your local agents "high materiality" under a bank's model inventory. The rationale confuses developer risk with model risk. Correct tier: **Low**. The "public-software blast radius" claim is marketing, not supervisory language. Model-risk officers would mark this as misunderstanding SR 11-7's scope.

* **skill_optimizer — rated Medium (cost: High).** Conflates dollar cost with model materiality. SR 11-7 is not a cost-control framework. If the only output is a branch you manually review and merge, this is **Low**. The parenthetical cost note reveals the real concern is spend, not model risk.

* **All "Medium" local agents (deep_researcher, vault_synthesizer, vault_critic).** These are over-tiered. They write to a private Obsidian vault that only you read. There is no third-party reliance, no customer impact, no financial exposure. Under real SR 11-7 inventory logic these are **Low**. The "floor rule" rhetoric sounds rigorous but is misapplied — the floor is still zero external blast radius.

The entire table performs the *form* of a model inventory while ignoring that SR 11-7 is about *governance of models that materially affect a regulated entity's risk profile*. Almost nothing here meets that bar.

**2. EU AI Act claims that misstate the regulation**

* "**Art. 72 — Post-market monitoring** — Providers must systematically collect and analyze performance data over the system's life, per a monitoring plan."  
  This is a serious misstatement. Article 72 imposes obligations on *providers* of high-risk AI systems placed on the market. You are not a provider placing anything on the EU market. The paragraph also mischaracterizes the content: Article 72(1) requires providers to "implement a post-market monitoring system" proportionate to the risk. Claiming your JSONL logs are "in EU AI Act terms, a post-market monitoring stream" is regulatory cosplay.

* "**Annex IV — Technical documentation** — Training data, testing, evaluation processes, and architecture must be documented. **Substantially present, see §5.**"  
  Annex IV lists *twelve* detailed elements that must be included in technical documentation for high-risk systems (Annex IV 1(a)–(l)). Your §5 addresses roughly three in the most superficial way and declares "substantially present." This is false. A notified body or market surveillance authority would reject it instantly. The correct statement is "intentionally non-conformant; documentation exists in developer-native artifacts, not in Annex IV format."

* "**Article 13 instructions for use.** Article 13 requires providers to give deployers instructions."  
  Again, you are not acting as a provider under the Act. The obligation in Article 13 is specific to high-risk systems and has defined content requirements. Treating your MCP README gap as an "Article 13" gap is incorrect application of scope.

The precision note correctly identifies the Article 61→72 renumbering but then proceeds to misuse the live articles anyway. This is exactly what a skeptical hiring manager would notice.

**3. The single weakest "honest gap" framing**

The weakest section is the entire **Honest gaps** list combined with the opening framing: "The gaps are named on purpose. They're the credibility."

This is over-confession that undersells the actual work while simultaneously inflating the rigor. By labeling obvious absences (no real evals on the highest-rated component, control plane not armed, no Annex IV document, no monitoring plan, no Article 13 instructions) as "honest gaps," the card tries to convert non-compliance into a virtue. It is the classic "I'm not saying I'm compliant, I'm saying I'm the kind of person who can *talk* about compliance" move. A model-risk officer would see this as sophisticated hand-waving rather than demonstrated accountability. The single most dishonest honest gap is claiming the Judge Layer is "the strongest governance component" while admitting it is switched off in production.

**4. Anything that reads as a candidate performing rigor rather than demonstrating it**

- The repeated insistence that "this is not a regulated filing" while spending 2,500 words mapping to specific articles, annexes, and supervisory letters.
- The "precision note" about Article numbering — correct but placed as a humblebrag.
- The "floor rule" reference to your own GitHub project as if it were authoritative precedent.
- "Inventory reconciliation (requested in the brief)" — there was no brief; this is theatrical.
- Naming the Judge Layer with a GitHub link and exact ship date ("shipped 2026-05-31" — a future date?) while admitting the master switch is off.
- The entire table formatting and "per-component transparency / monitoring / override" section that looks like a real compliance matrix but rests on "N/A in practice, honestly" and "agents draft / I send."

This document performs the *aesthetic* of a senior governance artifact extremely well. It does not demonstrate operating at the standard a fintech or regulated SaaS hiring manager actually needs.

**5. The one change that would most increase a hiring manager's trust**

**Delete the entire EU AI Act mapping section and the Annex IV claims.** Replace it with a short, accurate paragraph:

"I deliberately mapped this personal system against SR 11-7-style materiality logic because that framework is directly transferable to enterprise agent fleets. I did not attempt to map it to the EU AI Act because Code-Brain is not a product placed on the market, I am not a provider, and the Act's obligations therefore do not apply. Pretending otherwise would demonstrate regulatory fluency poorly."

This single edit would remove the most obvious regulatory overreach, eliminate the misstatements, and make the remaining SR 11-7 exercise look like genuine taste and judgment rather than portfolio decoration. A strong model-risk or AI governance hiring manager cares far more about not mis-citing the law than about seeing a fake Annex IV mapping.

**Overall verdict:** This is an ambitious, well-written portfolio piece that tries too hard to look like a regulated artifact. It is strongest when it stays in the realm of "I built governance instincts and controls for my own 12-agent fleet" and weakest when it borrows the language and structure of formal regulatory filings it has no obligation (or ability) to satisfy. The author clearly has taste and has done real work. The card currently signals "I can perform regulatory theater at a high level." The strongest version would signal "I understand what real accountability looks like and where the theater stops."

## Cross-rankings

### Judge: anthropic/claude-opus-4.7

- **Order:** A > C > B
- **Reasoning:** Response A is the most comprehensive and technically rigorous: it correctly identifies that the card conflates model risk with privacy/cyber/operational/cost risk, distinguishes inherent vs. residual vs. current risk, provides component-by-component corrections with nuanced reasoning, accurately characterizes Article 50's multiple branches (including the deepfake/public-interest-text deployer obligation that B and C miss), and proposes a concrete, actionable control matrix as the single biggest improvement. Response C is sharp, well-written, and lands several strong hits (the 'regulatory cosplay' Article 72 critique, the Annex IV twelve-elements point, the future-dated ship date catch, the recommendation to delete the EU mapping entirely), but is less thorough than A and somewhat overstates that all local agents must be Low. Response B is punchy and makes valid points about SR-11-7's definition of 'model' and the high-risk scoping of Article 72/13, but it's the shortest, misses Article 50's deployer obligations for public-interest text (where substack_drafter could actually trigger), and its skill_optimizer 'inherits High' claim is itself somewhat hand-wavy.

### Judge: openai/gpt-5.5

- **Order:** A > B > C
- **Reasoning:** Response A is the strongest: it gives specific line-level critiques, correctly distinguishes EU AI Act scope from voluntary benchmarking, catches the SR-11-7 third-party/vendor-model issue, and offers a constructive restructuring that would improve the artifact. Response B is accurate on the biggest issue—high-risk AI Act obligations do not legally apply—and gives a clear fix, but it is narrower and misses some important Article 50 and Annex IV nuance. Response C has useful observations about regulatory theater and EU scope, but it overcorrects on SR-11-7 by downgrading nearly everything to Low, makes some questionable claims, and is less balanced or actionable than A and B.

### Judge: ~google/gemini-pro-latest

- **Order:** A > B > C
- **Reasoning:** Response A delivers the most incisive, expert critique, catching highly specific nuances like SR-11-7 vendor model obligations and the Art 50(4) text generation trigger, while providing a narrative 'one change' that fixes the artifact's core legal flaw. Response B is also exceptionally strong, particularly in separating risk types (cyber vs. model vs. privacy), but places second. Response C fails to engage with the artifact's hypothetical premise, dismissing risks as 'Low' simply because it is a personal system, missing the point of the portfolio exercise.

### Judge: x-ai/grok-4.20

- **Order:** A > B > C
- **Reasoning:** Response A ranks highest for its precision, depth, and insight: it correctly identifies the core scoping error (SR-11-7 and AI Act applicability to non-high-risk/personal systems), quotes exact lines, supplies accurate regulatory corrections (e.g., SR 11-7's vendor-model section, Art. 50(2)/(4) details), and offers the strongest hiring-manager recommendation (reframing the entire card around voluntary modeling). Response B is second: it covers overlapping ground with thorough risk-dimension separation and table suggestions but is longer, more repetitive, and slightly less ruthless on the biggest scoping misstatements. Response C is weakest: while it nails the same applicability gap and some SR-11-7 definitional errors, its reasoning is occasionally overstated (e.g., blanket rejection of 'worst-case' materiality ignores regulatory practice) and less comprehensive on EU Act specifics or nuanced component critiques.

## Chairman synthesis

_Chairman model: `anthropic/claude-opus-4.7`_

# Council Synthesis: Stress-Test of the Code-Brain System Card

All four council members converged on a single verdict: **the card is rhetorically excellent and substantively miscalibrated in the same places.** The disagreements are mostly about emphasis and which fix matters most. I'll resolve them below.

---

## 1. SR-11-7 mappings that would not survive a model-risk officer

### Strong convergence (all four models agree)

**`intent-engineering MCP` is wrongly tiered High.**
- **Claude** and **GPT-5.5**: this conflates *software supply-chain / AppSec risk* with *model risk*. SR-11-7 is about quantitative outputs driving bad decisions, not about distribution surface.
- **Gemini** goes further and is correct: if it's truly a "pure-function analysis tool" with no probabilistic generation, SR-11-7 §II's definition of "model" likely excludes it entirely. It belongs in IT asset management, not the model inventory.
- **Grok** reinforces: materiality is driven by the *deploying institution's* exposure, not by whether the package is public.
- **Corrected treatment**: remove from model inventory, or rate Low for model risk with a separate, explicit callout for supply-chain/product risk governed elsewhere.

**`skill_optimizer`'s "Medium *(cost: High)*" is a category error all four flagged.**
- SR-11-7 wants *one* materiality rating. Cost is not materiality.
- **Claude** and **Gemini** add the sharper point the card misses: this agent *modifies the behavior of other agents in the fleet* — a model-on-model meta-risk that SR-11-7's "model interconnection" concerns target directly. Manual merge is a **control** (reducing residual risk), not a **materiality reduction** (changing inherent risk).
- **Corrected treatment**: Inherent **High**, residual **Medium** under the manual-merge gate. Distinguishing inherent from residual is table stakes the card never does.

### Divergence the user should be aware of

**`substack_drafter` at High** — the council split:
- **Claude** accepts High for the active case but notes the missing inherent-vs-residual distinction.
- **GPT-5.5** wants inherent High / residual Medium / current status Disabled.
- **Grok** argues this is *personal* reputational risk, not bank-grade model risk, and would tier Low inside a real bank context.
- **My read**: Grok is technically right about a literal bank inventory, but the card is a portfolio piece demonstrating *how* the author would tier. The strongest fix is GPT-5.5's three-axis labeling (inherent / residual / status), which makes Grok's objection moot.

**The "Medium" local agents** (`vault_synthesizer`, `deep_researcher`, `vault_critic`, `daily_driver`):
- **Grok**: should all be Low — no external blast radius, private vault only.
- **GPT-5.5**: most of the "Medium" rationale is actually privacy/vendor risk masquerading as model risk.
- **Claude**: makes the inverse point on `vault_synthesizer` — durable propagation into downstream reads, combined with a *nine-day undetected failure*, arguably *raises* materiality.
- **Synthesis**: the disagreement reveals the deeper problem GPT-5.5 names most clearly — **the card mixes five risk types into one tier column** (model, data/privacy, cyber/supply-chain, cost, external-impact). Until those are separated, neither "Low" nor "Medium" is defensible.

### The miss that all four agree is the most consequential

**Claude alone catches the single most damaging SR-11-7 error**, and it's the one a real MRM officer would flag in the first ten minutes:

> "No model is trained or fine-tuned here … collapses an entire category of model-risk obligation … to 'not applicable, by architecture.'"

SR-11-7's "External Resources" section explicitly requires vendor models to be validated *as if* they were internal. Training-data governance is **inherited from the provider**, not erased. Drift risk shifts from retraining to **silent vendor model updates** (Anthropic point releases), which is arguably *harder* to monitor, not easier. **GPT-5.5** independently reaches the same conclusion from the Annex IV angle: "you do not get to erase data documentation by saying 'I did not train.'"

This single line is the highest-cost error in the card.

**Also missing, per Claude**: SR-11-7's central control is **effective challenge by parties independent of development**. A solo-operator system has no independent validation function. The honest move is to *name* that constraint (and perhaps cite the LLM Council as a partial adversarial substitute), not leave it unspoken.

---

## 2. EU AI Act claims that misstate the regulation

### Total convergence — this is the card's load-bearing weakness

**All four models independently identified the same structural error**: Articles 72, 13, and Annex IV apply to **high-risk AI systems** as defined by Article 6 / Annex III. Code-Brain is not high-risk under any Annex III category. So:

- **Claiming "Partial" compliance with Art. 72** is not a gap, it's a category error. The honest mapping is "inapplicable; modeled voluntarily."
- **"Substantially present, see §5"** on Annex IV is not supportable. **Grok** correctly notes Annex IV has *twelve detailed elements* (1(a)–(l)); §5 addresses roughly three superficially.
- **Article 13** isn't triggered either — MCP package consumers aren't "deployers" in the AI Act sense.
- **Grok**'s framing is the sharpest: *"regulatory cosplay."* **Claude**'s is the most damaging to the artifact's credibility: *"pedantic about a citation number while wrong about the substance"* (referring to the Art. 61/72 precision note that performs precision while the Art. 72 scope is wrong).

### The Article 50 contradiction — Claude and GPT-5.5 catch what Gemini and Grok miss

The card says Art. 50 is "N/A in practice, honestly: there is no external user to disclose to" — while simultaneously documenting `substack_drafter` as a public-byline generator tiered High specifically *because* output reads as human.

**Claude** and **GPT-5.5** both identify the specific sub-articles the card omits:
- **Art. 50(2)**: providers of generative systems must mark outputs as artificially generated in machine-readable format.
- **Art. 50(4)**: deployers generating/manipulating text **published to inform the public on matters of public interest** must disclose AI generation, *unless human review with editorial responsibility applies*.

`substack_drafter` is plausibly the live wire for **50(4)**, and the human-review carve-out is exactly the kind of nuance that would impress a regulated-SaaS GC if handled correctly. The current framing — Art. 50 N/A because no external user — is wrong on the card's own facts the moment `substack_drafter` activates.

**Claude's correction is the cleanest**: *"Art. 50 is currently dormant because the one in-scope surface (`substack_drafter`) is disabled. Enabling it without an AI-disclosure mechanism would be the act that puts this system in scope."*

### One overreach to flag from the council itself

**Gemini** claims "Article 72 does not 'bite a system like this'—it is entirely legally inapplicable." This is correct as a strict legal matter but slightly misses the portfolio framing. The right answer (per **Claude** and **GPT-5.5**) is: "Art. 72 is inapplicable; I am modeling it voluntarily as a discipline demonstration" — which is *more* impressive than claiming partial compliance.

---

## 3. The single weakest "honest gap" framing

The council split, but the splits illuminate each other:

- **Claude**: the Art. 50 "N/A in practice" line — **under-confesses** by contradicting itself within the same document.
- **GPT-5.5**: the "Annex IV substantially present" claim — **over-claims** what's there; the gap is substantive, not just formatting.
- **Gemini**: the Judge Layer "shipped but not armed" framing — **under-confesses** a fundamental control failure (a deactivated control protecting a deactivated agent = zero defense-in-depth on the highest-blast-radius surface).
- **Grok**: the entire §6 "honest gaps as credibility" move — **over-confession that undersells the work while inflating the rigor**, converting non-compliance into a virtue.

**My synthesis**: Gemini's catch is the most concrete operational dishonesty (a non-running control cannot be the "strongest governance component"). Claude's catch is the most legally consequential (self-contradiction inside the artifact). If forced to one: **Gemini's, because it's the one that converts the card's strongest claim into vaporware on inspection.**

---

## 4. Performing rigor rather than demonstrating it

Convergent tells across all four reviews:

| Tell | Identified by |
|---|---|
| Three variants of "the gaps are the credibility" meta-move | Claude (cut two of three) |
| The Art. 61/72 precision note that performs precision while the Art. 72 substance is wrong | Claude, Grok |
| Self-citation to the author's own Enterprise Data Readiness Matrix as authority | Claude, Grok |
| "~800-test pytest suites" listed as Annex IV evaluation evidence (unit tests ≠ model evals) | Claude, GPT-5.5 |
| "append-only JSONL ledger" inflated to audit-grade language without hash chaining, WORM, or signing | GPT-5.5 |
| "Inventory reconciliation (requested in the brief)" — there was no brief | Grok |
| `skill_optimizer`'s dual-rating as visible refusal to commit to one number | Claude |
| Future-dated ship date ("2026-05-31") | Grok |
| The "floor rule" rhetoric — Gemini and Grok argue real enterprise risk *does* factor in probability/likelihood, and segments workloads rather than over-tiering monoliths | Gemini, Grok |

The pattern **Claude** names most precisely: *"The big thing is wrong; the small things are precise. That pattern is what 'performing rigor' means."*

---

## 5. The one change that would most increase a hiring manager's trust

The council converged on **the same structural fix from two angles**:

**Claude, Gemini, and Grok** all recommend the same thing: **lead with an Applicability/Scope Determination.** State explicitly that:
1. Code-Brain is not a financial institution's model under SR-11-7 jurisdiction.
2. Code-Brain is not a high-risk AI system under Art. 6 / Annex III, so Articles 11, 13, 72 and Annex IV do not apply by their own terms.
3. Art. 50 *would* apply at the moment `substack_drafter` activates.
4. The author is nonetheless modeling the full regulated-system discipline as a demonstration of *what the work looks like* — naming the gaps that would exist *if* the system were in scope.

The author's existing italicized closing line — *"this card applies regulated-industry frameworks to it as a demonstration of accountability fluency, not as a claim of conformance"* — is the thesis. It belongs **at the top, structuring the document**, not at the bottom apologizing.

**GPT-5.5** proposes a complementary fix at the operational level: replace the single-tier table with a **multi-axis control matrix**:

| Component | Status | Inherent model risk | Residual model risk | Data/privacy risk | Op/cyber risk | External-impact risk | Controls | Control status | Evidence | Open gap |

This separates the five risk types the card currently conflates and distinguishes inherent from residual, designed from operating.

**My recommendation**: do **both**. The scope determination at the top fixes the legal credibility problem. The multi-axis matrix fixes the SR-11-7 craft problem. Together they convert the artifact from *"smart PM performing governance literacy"* (Grok / GPT-5.5) into *"operator who can structure a defensible risk inventory and correctly scope a regulation"* — which is the actual deliverable a fintech or regulated-SaaS PM role needs in week one.

---

## Highest-confidence takeaways (all four agree)

1. The card misapplies Articles 13, 72, and Annex IV by treating high-risk-system obligations as if they apply to a personal system.
2. `intent-engineering MCP` is mis-tiered; it likely isn't a "model" under SR-11-7 at all.
3. `skill_optimizer`'s dual rating is a category error.
4. The "Substantially present" claim for Annex IV is unsupportable.
5. The card needs an explicit Applicability/Scope section at the top.
6. The Judge Layer's "shipped but not armed + fail-open" status cannot bear the weight of being called the "strongest governance component."

## Lower-confidence (council divergence)

- Whether the "Medium" local agents should be Low (Grok) or stay Medium with better rationale (Claude, GPT-5.5) — resolved by separating risk axes.
- Whether `substack_drafter` is High inherent or only contingent on activation — resolved by inherent/residual/status labeling.
- Whether the EU AI Act mapping should be **deleted entirely** (Grok's most ruthless cut) or **reframed as voluntary** (Claude, Gemini, GPT-5.5). The majority view is reframing; Grok's cut is the safer move if the author can't commit to handling Art. 50(2)/(4) carefully.

## The single most damaging individual catch

**Claude's** identification that SR-11-7 explicitly governs vendor/third-party models and that the "no training = not applicable, by architecture" line erases an obligation rather than satisfying it. This is the line that costs the most credibility with anyone who has actually run an MRM function — and the one the author should fix first.
