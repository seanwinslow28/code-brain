# Code-Brain System Card

> A model-risk and AI-governance accounting of the autonomous agent fleet I run on my own hardware. Code-Brain is not a regulated product, and almost none of these obligations legally apply to it — so this card leads by saying which regimes are *out* of scope, then models the full discipline against them voluntarily. The gaps are named on purpose. They're the credibility.

I built Code-Brain to run my life, not to pass an audit. It's a personal command center — an Obsidian vault plus a fleet of agents on the Claude Agent SDK that index, synthesize, critique, and research while I sleep. The first thing a model-risk officer does with a system isn't tier it; it's decide which rules even apply. So that's where this starts. The point isn't to claim conformance with frameworks that don't bind me — it's to prove I can scope a regulation correctly, tier by materiality, and tell you exactly where the controls stop.

---

## 1. Applicability — what's in scope, and what isn't

This is the section that makes the rest honest. Both frameworks below are applied *voluntarily*; by their own terms, neither binds Code-Brain.

**SR-11-7** (the U.S. Federal Reserve's [*Supervisory Guidance on Model Risk Management*](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm)) governs models used by supervised financial institutions. Code-Brain is a personal system, not a bank's model, so SR-11-7 has no jurisdiction here. I apply it anyway because its core discipline — maintain a model inventory, risk-rate by **materiality**, and size validation effort to that rating — transfers directly to any agent fleet. SR-11-7 doesn't prescribe tiers; the Low/Medium/High rating below is the convention firms use to operationalize it.

**EU AI Act** (Regulation (EU) 2024/1689) is risk-tiered. Code-Brain is **not** a prohibited system (Title II) and **not** a high-risk system under [Article 6](https://artificialintelligenceact.eu/article/6/) / Annex III (no biometrics, credit scoring, critical infrastructure, employment decisions, etc.). It is a minimal-risk system. That single classification rules out most of the Act:

- [**Annex IV**](https://artificialintelligenceact.eu/annex/4/) (technical documentation), [**Article 13**](https://artificialintelligenceact.eu/article/13/) (instructions for deployers), and [**Article 72**](https://artificialintelligenceact.eu/article/72/) (post-market monitoring) are **high-risk-only obligations. They do not apply.** I map against them anyway, voluntarily, to show what the work looks like.
- [**Article 50**](https://artificialintelligenceact.eu/article/50/) (transparency) is the one provision that *would* bite — not today, but the moment any surface faces another person. It is **activation-gated**, not absent (see §4).

> **A numbering note.** Post-market monitoring is **Article 72** in the adopted Regulation; the widely-cited "Article 61" was the 2021 Commission *proposal* numbering, renumbered in the final text. I flag it only because the renumbering is a common tell that someone is working from the draft.

**On training data.** No component is trained or fine-tuned here — every model is a Claude API call or a local-inference call against published open weights. That removes my *first-party* training-data obligation, but it does **not** erase the category: under SR-11-7's external-resources provision, a vendor model must be validated *as if* it were internal. The obligation is **inherited from the provider**, and the drift risk simply moves — from "we retrained" to "the vendor shipped a silent point release" — which is arguably harder to monitor, not easier. I name this as a real, unclosed gap rather than architecting it away.

**The floor rule.** A component's **inherent** materiality is set by its highest-risk action surface, not its average one — an agent that writes to my private vault 99% of the time and drafts a public post under my byline 1% of the time is tiered on the 1%, because blast radius is a worst-case property. Controls then produce a **residual** rating below the inherent one. (Inherent ≠ residual is the distinction that makes a materiality table defensible; the floor rule governs the inherent column, controls govern the residual.)

---

## 2. SR-11-7 materiality tiering (the model inventory)

Materiality here is **model risk** specifically — the risk that a model's output is wrong and propagates before I catch it. Where a component's dominant risk is something else (privacy, supply-chain, cost), I say so rather than smuggling it into the model-risk tier.

| Component | Status | Inherent (model risk) | Residual (after controls) | Dominant risk axis | Validation evidence | Override path |
|---|---|---|---|---|---|---|
| **substack_drafter** | Built, **disabled** | **High** | **Medium** | External / reputational | None yet — its failure surface is the explicit reason the Judge Layer exists | Agents draft / I send; never auto-publishes; Judge gate when armed |
| **skill_optimizer** | Live, manual-only | **High** | **Medium** | Model-interconnection (edits *other agents'* skills) + cost | Local judge + Sonnet sample-check every 5 iters; plateau-halt | Branch only, never self-merges; `$200` hard cap |
| **deep_researcher** | Live, local | **Medium** | **Low–Med** | Model (documented fabrication of entities + URLs) | **Published post-mortem** (LDR grounding-collapse); routing rule diverts heavy topics to Gemini DR | Vault-internal; 900s timeout; I cite nothing unread |
| **vault_synthesizer** | Live, local | **Medium** | **Low–Med** | Model + detection latency (silent-empty rot ran 9 nights) | **10/14 eval suite**, 6 failure modes from 17 days of logs ([evals/vault-synthesizer](https://github.com/seanwinslow28/code-brain/tree/main/evals/vault-synthesizer)) | Vault-internal; eval gate + manifest monitoring |
| **gemini_researcher** | Built, **disabled** | **Medium** *(when armed)* | — | Model + cost | Inherits Gemini DR caps | Opt-in only; `$7`/task, `$20`/day, `$50`/mo |
| **daily_driver** | Live, cloud/Opus | **Low** | **Low** | **Data/privacy + vendor** (egresses personal context to a cloud API) — *not* primarily model risk | Cost-instrumented | Writes only the daily-note skeleton; `$0.90` cap |
| **vault_critic** | Live, local + ext CLIs | **Low** | **Low** | **Data/privacy** (sends vault excerpts to Codex / Anti-Gravity) | Graceful degradation to `status: partial` | Vault-internal; manual promotion |
| **LLM Council** | Tool, manual | **Low** | **Low** | **Data/vendor** (multi-vendor egress of whatever I submit) | Pre-flight cost caps | Advisory only; acts on nothing |
| **job_feed** | Live, local | **Low** | **Low** | Model (job scoring), low stakes | Idempotency guard; `$0` via `fallback_disabled` | Informational only |
| **flush / meta_agent / knowledge_lint / vault_indexer** | Live, local | **Low** *(indexer & lint are deterministic — arguably not "models" at all)* | **Low** | Operational | Deterministic checks self-validate; no generative output | Vault-internal / report-only |
| **intent-engineering MCP** | Shipped (npm + registry) | **N/A — not a model** | — | **Software supply-chain** (governed by AppSec, not MRM) | Pure-function, no `exec`/egress; hardening pass scheduled (Task 23) | Stateless, side-effect-free by design |

**The honest limit of this inventory:** SR-11-7's central control is *effective challenge by parties independent of development.* A one-person fleet has **no independent validation function** — the LLM Council is the closest substitute (multi-vendor adversarial review; this very card was stress-tested through it), but a council I convene is not independent validation, and I won't call it that.

**Inventory reconciliation.** The roadmap's planning list named 11 components; the live fleet differs. `gemini_researcher` and `substack_drafter` are built but **default-disabled**; `vault_critic` and `job_feed` are live but weren't on that list; `skill_optimizer` is live but manual-only. Honest live count: ~12 running components plus 2 dormant-but-built.

---

## 3. The control plane: Judge Layer (designed and tested, not yet operating)

The most interesting governance component isn't an agent — it's the thing meant to sit *between* an agent's intent and its action. The **Judge Layer** ([agents-sdk/lib/judge](https://github.com/seanwinslow28/code-brain/tree/main/agents-sdk/lib/judge), built 2026-05-31) intercepts a typed `ActionProposal`, evaluates it against a declarative YAML policy a non-engineer can read, and returns one of five verdicts — `ALLOW`, `REVISE`, `BLOCK`, `ESCALATE`, `JUDGE_UNAVAILABLE` — writing each to an append-only JSONL log at `vault/health/judge_log/`.

Three honest qualifiers, because the language here is easy to inflate. It is **fail-open** by design (judge unreachable → fall back to my manual review, not block). Its module-level switch is **off by default**, and its first wrapped agent (`substack_drafter`) is itself disabled. So today the Judge Layer provides **zero runtime mitigation** — it is a designed-and-tested control, not an operating one, and a deactivated control guarding a deactivated agent is not defense-in-depth. And the JSONL is a *log*, not an audit-grade ledger: no hash-chaining, WORM storage, or signing, so I won't call it tamper-evident. What it is: the right architecture, wired and unit-tested, waiting to be armed.

---

## 4. EU AI Act — voluntary mapping

Per §1, the high-risk obligations below **do not apply**; I model them to show the discipline. Article 50 is the exception that becomes real on activation.

| Obligation | Applies? | What it would require | Code-Brain, modeled voluntarily |
|---|---|---|---|
| **Art. 50 — Transparency** | **On activation** | 50(1) interactive systems disclose they're AI; 50(2) generative output marked machine-readable; 50(4) deployers of AI-generated text *published to inform the public* disclose it — **unless** it had human review and a person holds editorial responsibility. | The in-scope surface is `substack_drafter`, currently disabled. Notably, my **"agents draft / I send" gate is exactly the 50(4) human-editorial-responsibility carve-out** — but 50(2) machine-readable output marking is unbuilt. Enabling the drafter without a disclosure mechanism is the act that puts this in scope; the control gating that is the module switch, not a design feature. |
| **Art. 72 — Post-market monitoring** | **No** (high-risk only) | A documented monitoring *system and plan* — thresholds, incident classification, root-cause and corrective-action loops — proportionate to risk. | I have **telemetry, not a monitoring system**: `vault/health/*` manifests, the judge log, cost ledgers, a fleet dashboard. Logs without a review cadence and corrective-action workflow are an *input* to Art. 72, not Art. 72 itself. |
| **Annex IV — Technical documentation** | **No** (high-risk only) | Twelve elements (1(a)–(l)): general description, intended purpose, architecture, dependencies, data specs, validation, risk-management, human oversight, monitoring, changes, conformity. | Partially present as *engineering* documentation (see §5), covering perhaps three of the twelve. Not Annex IV-conformant, and the gap is substantive, not cosmetic. |

**The three transparency/monitoring/override questions, answered:** *Self-identify as AI?* No agent faces an external human, so none must today; the MCP package is documented as software (product docs, not an Art. 50 control). *What's logged?* Per-run manifests, the judge log, stderr, the cost ledgers, the fleet dashboard. *Override path?* The system-wide **"agents draft / I send" gate** — nothing publishes, sends, or commits an irreversible external action without me.

---

## 5. Annex IV-style documentation actually present

- **Training data:** no first-party training or fine-tuning (so that sub-section is N/A) — but, per §1, third-party model provenance, version pinning, input/retrieval-corpus specs, and known-limitations documentation would still be required and are **not** assembled in one place.
- **Testing:** the `vault_synthesizer` eval suite (10/14, six failure modes from 17 days of real logs) is the one **graded behavioral eval** in the fleet. There are also ~800 pytest cases across the SDK — but those are software unit tests, not model evaluations, and I won't list them as eval coverage. Honest scope: **one of twelve components has a real eval suite.**
- **Evaluation processes:** documented in [CLAUDE.md](https://github.com/seanwinslow28/code-brain/blob/main/CLAUDE.md) — architecture-decision tables, the research-routing rule born from the grounding-collapse, the cost-cap and kill-switch design. It is real system documentation; it just isn't shaped like an Annex IV file.

---

## 6. Honest gaps

A scorecard you win every cell of is a sales sheet.

- **Vendor-model risk is inherited and unmanaged.** No third-party model inventory, no version pinning, no monitoring for silent vendor point-releases. This is the SR-11-7 obligation the "no training here" framing is most tempted to wave away.
- **No independent validation function.** Inherent to a solo operator; named, not hidden. The Council is adversarial review, not independent validation.
- **The Judge Layer is built but not armed**, guarding a disabled agent — so the fleet's highest-blast-radius surface (`substack_drafter`) currently rests entirely on the manual-review gate, with zero programmatic mitigation in force.
- **Eval coverage is one-of-twelve.** The High-inherent components (`substack_drafter`, `skill_optimizer`) have no graded evals.
- **Telemetry without a monitoring plan.** Rich logs, no written review cadence or corrective-action workflow — the most fixable gap, since the data already exists.
- **Art. 50(2) output-marking is unbuilt** — the precondition to ever enabling `substack_drafter` for anything public.
- **No Annex IV file and no Art. 13 instruction set** — voluntary gaps, not legal ones, but real if Code-Brain ever became a product.

---

## 7. Reference templates

A portfolio piece modeled on public governance documents, not a regulated filing. The templates it draws from:

- **Google — Model Cards for Model Reporting** (Mitchell et al., 2019): https://arxiv.org/abs/1810.03993 — the origin of structured model documentation.
- **Anthropic — Claude system cards:** index at https://www.anthropic.com/system-cards; Claude Opus 4 & Sonnet 4 card at https://www.anthropic.com/claude-4-system-card — the safety-evaluation-plus-deployment-decision shape, organized around Responsible Scaling Policy domains.
- **OpenAI — GPT-4 System Card:** https://cdn.openai.com/papers/gpt-4-system-card.pdf; GPT-4o System Card: https://openai.com/index/gpt-4o-system-card/ — the risk-enumeration-plus-mitigation pattern.
- **EU — Declaration of Conformity:** [Article 47](https://artificialintelligenceact.eu/article/47/) + [Annex V](https://artificialintelligenceact.eu/annex/5/) — the conformance statement I am explicitly *not* filing, because Code-Brain is not a high-risk AI product placed on the EU market.

---

I run a fleet that writes to my second brain every night, and until I tiered it I'd never asked the question a model-risk officer asks first: *if this one were wrong, how far would it get before I noticed?* For most of Code-Brain the answer is "into my private vault, where I'd catch it." For two surfaces — a draft under my name, a package in someone else's agent — the answer is "out the door," and one of those isn't even a model. That's the whole value of the exercise: not the conformance I can claim, but the materiality I can name and the regimes I can correctly rule out. The gaps in §6 are the build order.

*Portfolio artifact. Code-Brain is not a regulated production system; this card applies regulated-industry frameworks to it voluntarily, as a demonstration of accountability fluency, not as a claim of conformance.*
