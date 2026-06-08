# Build-vs-Buy Memo — AP Invoice-Approval Agent

**Decision:** what platform do we build the AP agent on? Four options across the buy↔build spectrum, scored on five dimensions, with a defended recommendation. Capability and certification claims are sourced from the [research reference brief §3](../2026-06-08-task-26-research-reference-brief.md) (re-pull vendor trust pages at build time — ⏱ certs drift).

## The four options (on the buy ↔ build spectrum)

| | Option | What you buy | What you build |
|---|---|---|---|
| Most **buy** | **Workday-native AP** | Pre-built finance agents (configure, don't code) | Configuration only |
| | **Anthropic platform** | Agent SDK + models + enterprise compliance substrate (audit logs, SSO) | The AP escalation tree + domain logic |
| | **OpenAI platform** | Agents SDK + models + enterprise substrate | The AP escalation tree + domain logic |
| Most **build** | **Self-build on Anthropic SDK** | Raw model API only | Everything: orchestration, audit, SSO, observability, AP logic |

The escalation tree and trust boundary we designed in Session A are *custom either way* on the middle two — the question is how much of the surrounding enterprise scaffolding you rent vs. own.

## Scoring (1–5; higher is better for the buyer on every dimension)

> Lock-in and exit-cost are scored so that **5 = least lock-in / lowest exit cost**.

| Dimension | Workday-native | Anthropic platform | OpenAI platform | Self-build (Anthropic SDK) |
|---|:--:|:--:|:--:|:--:|
| **Cost @ 5K/mo** | 2 | 5 | 4 | 3 |
| **Latency** | 5 | 4 | 4 | 4 |
| **Lock-in (5 = low)** | 1 | 4 | 3 | 5 |
| **Certifications** | 5 | 4 | 5 | 2 |
| **Exit cost (5 = low)** | 1 | 4 | 3 | 5 |
| **Total / 25** | **14** | **21** | **19** | **19** |

### Cell rationale

**Cost @ 5K/mo**
- Workday-native (2): ERP-grade licensing, not token-metered; economical only if you're already a Workday shop — overkill for a 200-person SaaS on a lighter ERP.
- Anthropic platform (5): cheapest in the cost model — hybrid routing across Haiku/Sonnet/Opus within one vendor lands at **~$27/mo**. ([cost-model.md](./cost-model.md))
- OpenAI platform (4): comparable token economics, but cross-tier hybrid routing is cleaner when the cheap and deep models are one lineup.
- Self-build (3): same low token cost, but the **build + maintenance + your-own-SOC 2-scope** burden dominates — the cost the GPU/ops line hides.

**Latency**
- Workday-native (5): in-platform, no external model hop. Others (4): API round-trips of a few seconds — well inside the <30s escalation SLA, and Haiku-first keeps the common path fast.

**Lock-in (5 = low)**
- Workday-native (1): the agent becomes part of the ERP system of record — deepest coupling.
- Anthropic platform (4): **lowest model lock-in of the API options** — Claude runs on the direct API *and* AWS Bedrock, Google Vertex, Azure Foundry, so the model layer is portable. (privacy.claude.com / trust.anthropic.com)
- OpenAI platform (3): higher model lock-in; Azure OpenAI provides some portability. (trust.openai.com)
- Self-build (5): you own the stack; nothing proprietary to be locked into — at the cost of owning all of it.

**Certifications**
- Workday-native (5): broadest — SOC 1/2/3 Type II, ISO 27001/27017/27018/27701, ISO 42001, HIPAA attestation, FedRAMP Moderate, NIST AI RMF. (workday.com/trust)
- OpenAI platform (5): SOC 2 Type 2, ISO 27001/27017/27018/27701, ISO 42001, SOC 3, CSA STAR, PCI DSS v4, FedRAMP 20x, and a **HIPAA BAA** — available for the API and ChatGPT Enterprise via baa@openai.com (verified 2026-06-08). (trust.openai.com / help.openai.com)
- Anthropic platform (4): SOC 2 Type I & II, ISO 27001:2022, ISO 42001:2023, HIPAA-ready/BAA — strong, slightly shorter published list. (privacy.claude.com)
- Self-build (2): inherits the *model's* certs only; **your AP application carries its own SOC 2 scope** — a real audit lift you now own.

**Exit cost (5 = low)**
- Workday-native (1): ERP-grade migration. OpenAI (3): re-implement orchestration + prompts, model lock-in higher. Anthropic platform (4): portable models lower the exit; re-wire orchestration. Self-build (5): nothing to exit — but you've already paid in build/maintenance.

## What the scores say (decision criteria for THIS scenario)

The buyer is a **200-person SaaS company, 5,000 invoices/mo**, that needs SOC 2 / SR 11-7 governance and wants to keep the differentiated logic it designed. Filtering the options:
- **Self-build** is the wrong call on governance and cost — the cost model showed the hidden ops burden, and you'd take on your own SOC 2 scope for an undifferentiated runtime. (Best lock-in/exit, but those aren't the binding constraints here.)
- **Workday-native** only makes sense if they're already a Workday shop; even then, you'd inherit Workday's agent logic instead of the escalation tree we designed, and accept ERP-grade lock-in. For this buyer it's likely N/A.
- That leaves the two managed platforms — and the differentiator is **portability + cost**: Anthropic's tri-cloud model availability gives the lowest exit cost of the API options, and its single-vendor Haiku→Sonnet→Opus lineup is what makes the cost-model's hybrid routing clean.

## Recommendation (ratified 2026-06-08)

> **Build the differentiated AP logic on the Anthropic platform; buy the runtime, models, and compliance substrate.** Reject self-build (governance + hidden ops cost), reject Workday-native (lock-in; inherits their logic), with OpenAI a close second (broader cert list and a now-verified HIPAA BAA, but higher lock-in). This is the classic enterprise split: **build the thing that's yours (the escalation tree, the trust boundary, the controls), buy the undifferentiated heavy lifting (model serving, SSO, SOC 2 substrate).**
>
> *Most-defensible counter-position to be ready for: if the company is already standardized on OpenAI or Azure, the switching cost erases Anthropic's portability edge and OpenAI's broader cert list wins — the recommendation is buyer-context-dependent, not absolute.*

## Failure modes this decision must respect

- **Vendor lock-in cascade** — if you wire the agent to one vendor's proprietary orchestration primitives, you can't migrate when prices or terms change. Mitigation: keep the AP logic (tree, controls, schema) vendor-neutral; treat the model/runtime as a swappable dependency. This is *why* portability (exit cost) is scored as a first-class dimension.
- **Silent capability degradation** — a vendor can change model behavior behind the same API without notice, which for a money-moving agent is a model-risk event. Mitigation: pin model versions, gate version bumps through the SOC 2 CC8.1 change process, and run the eval suite against any new version before it touches production. (This is where Sessions B and D connect.)

## Sources
Research reference brief §3 (vendor comparison, with primary trust-page citations): trust.anthropic.com / privacy.claude.com, trust.openai.com, workday.com/en-us/why-workday/trust/compliance.html, code.claude.com. Cost figures: [cost-model.md](./cost-model.md). ⏱ Re-pull all trust pages at publish — certifications are point-in-time. Re-verified 2026-06-08: OpenAI offers a HIPAA BAA for the API + ChatGPT Enterprise (request via baa@openai.com) and provides SAML SSO + SCIM for enterprise — both previously unverified, now confirmed.
