---
title: Systems Thinking AI PM — Program Strategy
type: spec
status: active
created: 2026-08-16
owner: Sean Winslow
notebook: https://notebook.google.com/notebook/0abf9bb0-6a82-4838-a639-a3f9dd03e963
---

# Systems Thinking AI PM — Program Strategy

An 8-week program to make systems thinking Sean's default operating mode as an AI PM, and to prove it publicly with an evidence-discovered, systems-instrumented AI product build. Learning is audio-first (NotebookLM audio overviews) and practice-first (every module has a hands-on exercise on Sean's real systems; every build decision cites a systems concept).

## Goals

1. **Mindset**: systems-thinking vocabulary and moves (loops, leverage points, archetypes, second-order effects) become second nature — usable in interviews and build decisions without notes.
2. **Portfolio proof**: a shipped AI product with at least one genuinely instrumented feedback loop, a public decision log, and a hiring-manager-readable case study. The artifact demonstrates the skill; it never merely claims it.

## Program shape (Approach A — Foundation then Build)

| Phase | When | What |
|-------|------|------|
| Phase 0 — Research & Strategy | Week 0 (Claude's work) | Curriculum research (Gemini DR + last30days + NotebookLM deep research), product discovery (fusion-discovery-council deep run → 3–5 scored candidates), llm-council critique gate |
| Phase 1 — Curriculum | Weeks 1–3, 2 modules/week | 6+ NotebookLM modules: sources + authored lesson doc → audio overview, quiz, flashcards, mind map, study guide; one real-system exercise each |
| Phase 2 — Build | Weeks 3–8 | Candidate pick → **systems map before PRD** (CLD, leverage-point analysis, pre-mortem + council pre-mortem run) → build sprints with instrumented loop(s) → week 8 polish + public case study + retrospective audio |

## Curriculum modules (draft — research refines; see expansion rule)

| # | Module | Anchor concepts |
|---|--------|----------------|
| M1 | Systems Thinking Foundations | stocks/flows, feedback loops, delays, Meadows' leverage points |
| M2 | AI Product Feedback Loops | data flywheels, drift, degenerate rec-system loops, eval loops, preference/RLHF loops |
| M3 | System Archetypes in AI Failures | fixes-that-backfire, shifting the burden, eroding goals — real public AI failure teardowns |
| M4 | Causal Loop Diagramming & Systems Mapping | CLD notation, stock-flow diagrams, mapping practice |
| M5 | Second-Order Thinking & Pre-mortems | intervention design, Goodhart's law, unintended consequences |
| M6 | AI Architecture as Systems | agents, RAG, eval harnesses, observability |

**Module expansion rule (Sean, 2026-08-16):** the research phase is expected to surface topics this draft misses. Any topic that (a) recurs across independent high-tier sources and (b) is load-bearing for an AI PM's systems practice gets promoted to a new module (M7+). The module list is a starting point, not a wall.

**Per-module exercise principle:** exercises run on Sean's real systems (agent fleet, 16BitFit, portfolio site, the Phase 2 build) or on real public AI failures — never toy problems. Sean submits; Claude reviews with feedback.

## Phase 0 research plan

| Job | Engine | Query shape | Cost |
|-----|--------|-------------|------|
| Curriculum: literature & competencies | Gemini Deep Research | Research-shaped ("what does the literature define as…") to pull academic/primary sources; tier-audited via `audit_dr_citations.py` | ~$1–3 |
| Curriculum: fresh practitioner discourse | last30days | Social + web, last 30 days | $0 |
| Curriculum: per-module source seeding | NotebookLM built-in deep research | Per-module topic queries, imported into the notebook | $0 |
| Product discovery | fusion-discovery-council `--tier deep` | Real user pain points, anti-fabrication-gated → ranked PM opportunities | $4 |
| Critique gate | llm-council premium | Stress-test curriculum map + candidate shortlist | ~$0.30–1 |

**Candidate scoring rubric** (each of 3–5 candidates): evidence strength · systems-thinking surface area (needs real loops/evals/drift handling, not a wrapper) · buildable in 5 weeks at 5–8 hrs/wk · recruiter demo-ability.

## Budget ledger

Approved: **$15–25 total.**

| Date | Item | Est. | Actual |
|------|------|------|--------|
| 2026-08-16 | Gemini DR (curriculum) | $1–3 | $2.80 |
| 2026-08-16 | fusion-discovery-council deep | $4.00 | $0.53 |
| 2026-08-16 | llm-council premium (pre-mortem gate) | $0.30–1 | $0.79 |
| Week 3/4 | falsification pass + optional 2nd council | — | reserved |
| **Spent** | | | **$4.12 of $15–25** |

Note: `council-spend-2026-08-16.json` shows reservation amounts ($7.30/$11.19), not the settled actuals above — ticketed for verification (2026-08-16).

## NotebookLM plan

- Single notebook: `0abf9bb0-6a82-4838-a639-a3f9dd03e963` (AI-PM-System-Thinking-Strategy). CLI auth verified 2026-08-16.
- Source naming: `M1 — <title>`; program-level sources prefixed `P0 —`.
- `notebooklm/source-manifest.md` tracks every source + running count against the plan cap; `notebooklm/artifact-tracker.md` tracks generated artifacts and download paths.
- Known flake: audio/quiz generation rate limits → retry after 5–10 min, `--retry` where supported.

## Vault layout

```
prj-ai-pm-system-thinking-strategy/
├── 00-strategy.md          # this spec: overview, budget ledger, status
├── research/               # DR reports, discovery outputs, citation audits, seed docs
├── curriculum/             # m1+ lesson docs, exercises, Sean's submissions + reviews
├── product/                # candidate scorecard, systems map, PRD, decision-log.md
└── notebooklm/             # source manifest + artifact tracker
```

## Success criteria

- **Mindset:** all modules absorbed (audio listened, quiz passed, exercise submitted and reviewed); by week 8 Sean narrates a product decision in systems vocabulary unprompted.
- **Portfolio:** shipped product with a live instrumented feedback loop + public decision log + 10-minute-readable case study.
- **Honesty guard:** the case study documents real failures and loop corrections as the mechanism's discoveries — never apology, never fabricated metrics.

## Status log

- 2026-08-16 — Spec approved (Approach A; 8 wk; full-depth research budget; module expansion rule added). NotebookLM CLI auth verified. Phase 0 research kicked off.
- 2026-08-16 — Phase 0 complete. Research: last30days ($0), Gemini DR ($2.80, tier mix 17%A/60%C/20%D), fusion-discovery deep ($0.53, 5 verified pains, 12/12 supplement quotes verified), NotebookLM deep research (84 sources imported; notebook at 87). Council pre-mortem ($0.79, 4 models, 1 judge ranking-failed: Gemini). **Curriculum v2 locked** (M3→cost/latency economics; archetypes folded into M2/M4; org systems in M5; HITL in M6; metrics architecture in M7; prediction-before-exercise; fluency@wk3 / judgment@wk6 gates). **Product locked: C2 "Golden Loop"** — eval-first golden-dataset cockpit with playable teaching layer; decision record in product/candidate-scorecard.md. Next: Phase 1 module production (M1 first).
