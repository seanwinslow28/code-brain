# Agent-company founding — research campaign kickoff (sitting 3+)

**Decision record:** `~/.creative-harness/partner-sessions/2026-08-07-agent-company-founding.md` — 12 locks, 1 SUPERSEDES, sidecar closed 2026-08-08. Read it before starting; the locks govern.

## What was decided (the short version)

- **[L2]** The agent fleet builds and operates a real product; the factory is internal infrastructure, wrapped in build-in-public.
- **[L11]** Territory: **creator quality-governance** — serial creators whose verified pain is reproducing their own quality bar and keeping a series consistent.
- **[L12]** Shape: **multimodal series-consistency keeper** — a tool-agnostic pre-publish gate that checks visual character/style drift across installments alongside voice/canon checks for the text, in one drift report with receipts. Text-canon is one modality, not the product (that lane is contested: Novarrium, Novelium, Bunsho — see sidecar product-shape round 3). Personal quality gate ("CI for your voice") is the earned second act.
- **[L12 gate, Sean verbatim]** "if research and testing shows it's a fools errand, than we should go back to the drawing board before I spend months of my time on an impossible task."
- **Standing constraints:** compound 6-month criterion, autonomy-proof primary [L6]; co-primary with job hunt, ~25 hrs/wk, ≤$250/mo opex, quality over speed [L7]; **no company code before the architecture is ratified** [L10].

## Campaign sequence (research front-load per L10, gate first per L12)

### 1. Feasibility spike — vision-model drift detection (GO/NO-GO, runs FIRST)
The L12 gate. Build a small eval harness that answers: can current vision models judge character/style consistency across installments reliably enough to productize?
- **Testbed:** the anima corpus (`/Users/seanwinslow/Code-Brain/anima/` — `characters/`, `runs/`, `evals/`, existing consistency checks with "plenty of hits, but plenty of misses").
- Measure hit/miss/false-alarm rates on known-good and known-drifted pairs; test across at least 2 vision models.
- **Named design question — the haircut problem:** canon-sanctioned change vs drift ("A character could decide to get a haircut and then the whole thing is fucked"). A viable design must distinguish declared canon updates from unintended drift.
- Feasibility cautions already on record: FlawedFictions (arxiv 2504.11900) — SOTA LLMs struggle at long-story plot-hole detection; visual identity scoring exists only as research metrics (ArcFace ISM/FSS).
- Output: a go/no-go evidence memo. **No-go → SUPERSEDES [L12] in a new partner sitting, back to the drawing board.**

### 2. Software-factory literature review
Stripe / OpenAI / Ramp / Anthropic engineering blogs + the NotebookLM corpus (`https://notebook.google.com/notebook/d0c5e65f-8469-4219-aab7-a43b55bc540c`); Codex synthesizes. Adopt what works, flag what doesn't.

### 3. Groundwork v1 audit
`/Users/seanwinslow/Code-Brain/groundwork/` as the fleet OS — what it satisfies today, what the company needs it to satisfy, gap list.

### 4. Architecture + orchestration ratification
Fleet topology (orchestrator / validator / LLM-as-judge / HITL, mixed closed + open-source models), roles and ontologies. Ratify via LLM council (premium profile) before any code — this is the L10 gate.

### 5. Arize eval-stack design
Two-layer eval design: fleet-evals (run the company) and product-evals (ARE the product). Traces from day one.

### 6. Wayfinder plan-of-action / ticket map
Only after 1–5. Then build.

## Open questions carried forward

1. L6 placeholder numbers (20 WAU / 1 paying / 30 autonomous days / ≤10 hrs oversight / weekly posts) stand until Sean resets them.
2. L11 carries no verbatim reason yet — Sean can add a late-why any time.
3. Wedge segment (which serial creators first) and business model — future partner axes after the spike.
4. Pre-mortem item: text-lane incumbents expanding into multimodal; "feature, not a company" risk.
