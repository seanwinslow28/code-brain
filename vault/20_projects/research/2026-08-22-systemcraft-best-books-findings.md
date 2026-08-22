---
title: "Systemcraft corpus — best-books research findings (L6 seed)"
date: 2026-08-22
project: systemcraft
status: ratified-2026-08-22
tags: [research, systemcraft, corpus, books]
cost: $0 (web research; no paid research invoked)
---

# Systemcraft best-books — findings brief

**Gate:** L6 — two-layer private corpus; this pass ranks which books earn purchase (private book-to-skill layer) and confirms the free canon (free layer). Book *content* never lands in tracked files; this brief holds only findings and citations.

## Headline recommendation

**Buy six books (~$250), in this order: Huyen *AI Engineering* → Shankar/Husain *Evals for AI Engineers* (early release) → Berryman/Ziegler *Prompt Engineering for LLMs* → Alammar/Grootendorst *Hands-On Large Language Models* → Huyen *Designing Machine Learning Systems* → Nika *Building AI-Powered Products*. Drop Aminian & Xu. Treat the Interaction & Trust lane as a free-canon lane.**

## Ranked purchase list

1. **Chip Huyen — *AI Engineering* (O'Reilly, 2025). Buy first.** The consensus LLM-era system-design reference: evaluation methodology, RAG vs fine-tune vs prompt decisions, inference cost, failure modes. Written around timeless concepts, not perishable APIs — ideal for an ingested corpus. Caveat: survey-style, qualitative; pair with hands-on material.
2. **Shreya Shankar & Hamel Husain — *Evals for AI Engineers* (O'Reilly, early release; final ~Oct 2026). Buy in early release.** Book form of the field's leading evals course (2,000+ PMs/engineers, incl. OpenAI/Anthropic teams): error analysis, LLM-as-judge, synthetic data, production monitoring. Converts the evals lane from book-poor to book-rich. Caveat: incomplete until final edition — bridge with the authors' free essays.
3. **John Berryman & Albert Ziegler — *Prompt Engineering for LLMs* (O'Reilly, 2024).** Two GitHub Copilot architects on how prompts actually meet the model — context assembly, tool loops. Caveat: API specifics dating; some Python assumed.
4. **Jay Alammar & Maarten Grootendorst — *Hands-On Large Language Models* (O'Reilly, 2024).** The mechanism/vocabulary layer under Huyen (transformers, embeddings, RAG internals); Andrew Ng-endorsed. Caveat: its famous diagrams degrade in text-only ingestion.
5. **Chip Huyen — *Designing Machine Learning Systems* (O'Reilly, 2022). Not superseded — complementary.** Covers what *AI Engineering* deliberately skips: data pipelines, feature engineering, **drift and monitoring** — the Ops lane's weakest book coverage otherwise. Caveat: pre-ChatGPT; tooling examples aging.
6. **Marily Nika — *Building AI-Powered Products* (O'Reilly, 2025). Buy, ranked low.** The only credible LLM-era book written *as* an AI-PM playbook (AI-first PRDs, feasibility checklists) — serves the framing lane no engineering book covers. Caveat: slim (~195pp), checklist-grade rather than reference-grade; reviewers say experienced PMs skip the basics.
7. **(Contingent) Nudelman & Kempka — *UX for AI* (Wiley, 2025).** Only current book-length AI interaction/trust treatment (35 real projects). Hold: little independent critical reception yet — buy only if the free HAX/PAIR canon proves insufficient after first engagements.

## Evaluated and rejected

- **Aminian & Xu, *ML System Design Interview*** (original candidate) — 8/10 chapters are pre-LLM recommender-system variants in interview-prep framing; reviews call it much weaker than Xu's system-design series. DMLS covers the ground better for reference use.
- **Bratsis, *AI Product Manager's Handbook*** — reviews: repetitive, vague, thin.
- **Bouchard & Peters, *Building LLMs for Production*** — LangChain-bound code already outdated.
- **Iusztin & Labonne, *LLM Engineer's Handbook*** — good but an engineer's build-along project, not PM reference.
- **Lipenkova, *Art of AI Product Development*** — near-miss; overlaps Nika, and Nika is more GenAI-native.
- **Mollick / *AI Snake Oil*** — literacy narratives, not system-design reference.
- **Cagan *Inspired* / Torres *Continuous Discovery Habits*** — excellent but AI-agnostic; the pm-* plugin skills already encode this layer.

## Lane-by-lane coverage

| Lane | Verdict | Coverage |
|---|---|---|
| Framing / PRDs | Book-thin but covered | Nika + Huyen AIE ch.1–2; Lenny's/Aakash Gupta AI-PRD posts for templates |
| Architecture | **Book-rich** | Huyen AIE (primary), Alammar, Berryman |
| Interaction / Trust | **Book-poor — confirmed** | Free canon carries it: HAX/Amershi, PAIR, Shape of AI; Nudelman contingent |
| Evals & Evidence | Was book-poor; closing | Shankar/Husain (primary) + Huyen AIE eval chapters; hamel.dev bridges |
| Ops & Economics | Split | Huyen AIE (inference cost) + DMLS (drift/monitoring); LLMOps specifics stay free-web |

## Free-canon shortlist (validated current)

- **applied-llms.org** — "What We Learned from a Year of Building with LLMs"; still the best single free doc on LLM product operations.
- **hamel.dev** + free AI Evals email course — the Analyze-Measure-Improve evals lifecycle.
- **eugeneyan.com** — LLM patterns and eval design essays; book-grade rigor.
- **Microsoft HAX Toolkit / Amershi et al. 18 Guidelines** — most-cited human-AI interaction framework, still actively referenced.
- **Google PAIR People + AI Guidebook** — v2 with generative-AI guidance; trust/expectation-setting patterns hold.
- **sh-reya.com** — Shankar's evals/data-quality research writing.
- **Lenny's Newsletter AI posts + Aakash Gupta's Product Growth** — freshest AI-PM framing material.
- **OpenAI Cookbook / Anthropic docs & courses** — canonical, continuously updated; more current than any book.
- **chiphuyen/aie-book repo** — free maintained companion to purchase #1.

## Decision requested (Sean)

1. Ratify the six-book purchase list and order (~$250 total), with Nudelman as a contingent seventh.
2. Ratify dropping Aminian & Xu from the candidate list.
3. Ratify the free-canon shortlist as the free layer's seed, with Interaction & Trust designated a free-canon-carried lane.
