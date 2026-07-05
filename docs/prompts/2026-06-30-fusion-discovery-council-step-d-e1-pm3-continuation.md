# Continuation — fusion-discovery-council, Step D: E1 entailment gate + PM3 t0 seed + two follow-ups (next session)

Paste everything **below the divider** into a fresh **Claude Code session opened in `code-brain`** to continue the roadmap. Everything above the divider is context for you (Sean).

**What just shipped (2026-06-30):** **E2 — panel self-preference fix** is done as **PR #109** (open, awaiting your squash-merge). One enforceable invariant — *judge model family ∉ panel families, every tier* — in `tiers.py`: `quick` judge swapped Gemini→GPT-5.5 (panel unchanged); `standard`/`deep` drop the Opus panelist (Opus stays the judge → anthropic-free 3-/5-vendor panels). New `_family()` helper + a regression test that permanently blocks reintroducing the confound. **268 passed / 1 skipped, validator PASS.** Final review (Opus): **Ship, 9/10** (sole deduction = a stale doc comment, fixed). Driven by a $0 deep-research pass (sixth headline running): family separation is the highest-leverage debias lever and the only one robust to both mechanism accounts; the full order-randomized pipeline was rejected (wrong task shape for a *synthesis* judge — order-swap can backfire 4–11pp). Decision record: `vault/20_projects/research/2026-06-30-llm-judge-self-preference-debias-research.md`.

**⚠️ Honest scope for this session (read before promising a clean sweep):** the remaining roadmap is **not** all knock-out-able in one sitting.
- **Two small follow-ups** (Sonar cost leak, review-sites under-yield) — quick, $0, real wins. Do these first.
- **PM3 longitudinal gate** — *wall-clock gated*, **cannot finish today**: it needs a 2–4 week gap between two runs to tell signal from sampling noise. You can only **seed the t0 baseline** now (one **paid** discovery run, persist the bundle via `EvidenceBundle.to_dict`); the verdict comes weeks later. Surface the cost first.
- **E1 — entailment gate v2** — the big one and the real point of Step D. Research → decide local-NLI **with Sean** → wire NLI entailment into the documented `verify.py` chokepoint. A real build (local-model integration), likely to fill most of the session and possibly spill to a second. **Don't rush it to "finish the list."**

A sane single-session target: **the two follow-ups + the PM3 t0 seed + E1 research→decision→(start the) build.** If E1's build lands clean too, great — but treat E1 as the headline, not item #4 on a checklist.

---

## Who you're working with + how to work

You're partnering with **Sean Winslow** in `code-brain` on **fusion-discovery-council** — an evidence→idea discovery engine (gather real-URL user pain → multi-vendor OpenRouter Fusion panel → anti-fabrication gate → ranked, evidence-linked PM opportunities / Substack angles). Sean is a PM/creative technologist who wants the *why* and the *how*, values momentum, and wants a real thinking partner: brainstorm one question at a time, pressure-test ideas, be concise and direct. Use **TDD** + the superpowers skills (`brainstorming` → `writing-plans` → `subagent-driven-development` *or* `executing-plans`). **Surface cost before any paid run.**

### ⭐ Standing practice — research before you lock a design decision
Six consecutive headlines have each turned on a **$0 deep-research pass before locking the shape** (PM4 · D4 · E3 · D2 · Step-C gate · E2). **Before committing to any design decision with documented prior art, run a deep-research pass and let the evidence shape the design.**
- **E1 has deep prior art** — natural-language inference (NLI / entailment) for citation verification, atomic-claim decomposition, local NLI models (DeBERTa-MNLI, Luna, MiniCheck, AlignScore, Bespoke-MiniCheck), and citation precision/recall benchmarks. Research it before locking the mechanism.
- **How:** the **`deep-research` skill** (`/deep-research`) — **$0 on the Anthropic subscription**. Scope tightly. It ran clean on E2 (101 agents, no rate-limit abort); the salvage lesson still stands if it ever aborts mid-synthesis (don't blindly re-run — salvage the completed transcripts).
- **Then:** fold findings into the spec **with citations**; persist the synthesis to `vault/20_projects/research/YYYY-MM-DD-<topic>.md` (mirror the six exemplars — per-finding confidence + sources + a "How this changed the build" section). The newest exemplar is E2's: `2026-06-30-llm-judge-self-preference-debias-research.md`.

## FIRST ACTION (state reconciliation)
1. `git checkout main && git pull --ff-only`. Confirm **PR #109 (E2) is merged** (`git log --oneline -5` should show the E2 squash commit). If it's *not* merged yet, ask Sean — E1 builds on the same VERIFY path and you want a clean base.
2. `gh pr list --state open` (expect none from discovery). Branch off `main`, e.g. `feat/discovery-followups` for the quick wins, then a separate `feat/discovery-e1-entailment-gate` for E1 (keep PRs small + focused — one roadmap item per PR).
3. **Vault discipline (unchanged):** per CLAUDE.md rule 8 the Obsidian-Git plugin owns vault commits — **keep discovery branches free of vault changes**; write research notes to `vault/20_projects/research/` and **leave them unstaged** for Sean. Never weaken the privacy layer (rule 10). **Still in Sean's court from E2:** commit the E2 research note + mark **E2 ✅ DONE** in the `tickets.md` roadmap ticket.

## TASK A (warm-up, $0, quick) — the two logged follow-ups
Small, real, and they de-risk E1 by leaving the gather/verify path tidy. One PR (or two tiny ones).

1. **Sonar cost-integrity leak.** `gather/sonar.py::collect_sonar` calls OpenRouter (`OPENROUTER_URL`, line ~41–51) and the response carries a `usage.cost` (same shape as Fusion's), but that ~$0.02/run is **never threaded into `record_spend`** — contradicting the "every collector is FREE" framing in `gather/__init__.py`. **Fix:** capture `usage.cost` from the Sonar response and thread it into the recorded discovery spend (mirror how `FusionError.cost` / `fr.cost` flow to `record_spend(..., tool="discovery")` in `__main__.py`), **or** explicitly document it as a known fixed line item if threading is disproportionate. TDD: assert the billed cost is recorded (mock the response `usage.cost`).
2. **Review-sites under-yield.** `gather/reviews.py::_review_query` (line ~26–28) builds one `" OR ".join(f"site:{d}" ...)` query; **Brave collapses the OR'd multi-`site:` query**, so most review domains never get searched. **Fix:** fan out to **N single-`site:` queries** (one per domain), merge + dedup results, keep the existing query-length clamp per query. Watch the result cap (`max_results`) so fan-out doesn't explode cost/latency — it's all on the free Brave/Exa path, but cap total fetches. TDD: assert N queries issued, results merged/deduped.

Run `cd tools/llm-council && uv run pytest tests/ -q` (baseline **268 passed, 1 skipped**) + `python3 scripts/validate.py`.

## TASK B (seed only — cannot complete) — PM3 longitudinal t0 baseline
**This is a GATE that needs a time gap; today you only start the clock.**
- Pick **one stable topic** to track (ideally one already run before, so you can compare to history). Run it once at a fixed tier, and **persist the raw evidence bundle to disk** via the new `EvidenceBundle.to_dict` (the serializer shipped in Step C for exactly this). Stamp it `t0` with the date.
- **COST: this is a real paid discovery run** (~$1.50 standard / up to $4 deep). **Surface the estimate and check today's discovery spend vs the $10/day cap** (`vault/health/council-spend-*.json`, tagged `tool="discovery"`) before running. Get Sean's go.
- Log a `tickets.md` bullet (flag for Sean, don't commit): "PM3 t1 re-run due ~`<t0+3wk>` — compare verified-pain frequency/intensity vs the persisted t0 bundle; if movement ≤ sampling noise, PM3 is a memory/dedup feature, not a trend signal." E3's dedup/similarity is the stable pain-key groundwork for the comparison.
- **Related deferred follow-up:** wiring `EvidenceBundle.to_dict/from_dict` into the *live* pipeline (persist every run's raw evidence) is PM3's production groundwork — only needed once PM3 is greenlit by this gate.

## TASK C (the headline) — E1: entailment gate v2 for the core VERIFY stage
**Why now:** E1 is the **defensibility / brand** core — "verified, not hallucinated." Today the gate is substring containment.

- **The single documented chokepoint to upgrade in place:** `verify.py::quote_supported_at_url(*, cited_quote: str, fetched_text: str) -> bool` (line ~18; its docstring already says "E1 will upgrade it in place from substring containment to atomic-claim + NLI entailment"). Keep substring as a cheap **pre-filter**; add atomic-claim decomposition + NLI entailment (does the source *entail* the claim, not just contain a substring?). Report **citation precision + recall**. (Agent BACKFILL already vets relevance natively, so E1 is a **core-VERIFY** concern only.)
- `GATE → RESEARCH →` **E1 cost model — DECIDE WITH SEAN (left open on purpose):** entailment verification as **(a) local NLI** (DeBERTa/Luna/MiniCheck — $0, fits the fleet's local-model infra), **(b) OpenRouter LLM-judge per claim** (recurring API $ — the cost trap), or **(c) subscription agent** (interactive-only). Research local-NLI options + citation precision/recall benchmarks (MiniCheck, AlignScore, RAGTruth, etc.). **Do NOT default to a paid per-claim approach.** **Lean: local NLI** (consistent with the fleet's $0 local-model spine — Ollama on the Mac Mini / MBP). Surface the integration cost (model download, latency, where it runs) before locking.
- **Build discipline:** `brainstorming` → research → `writing-plans` → TDD. Hermetic tests (mock the NLI scorer; no live model in the unit suite — or a tiny fixture). Watch each test fail first. Update SKILL.md §6 (the gate) + CHANGELOG. **Final whole-branch adversarial review** (Code Reviewer, most capable model) before the PR.

## THEN (subsequent sessions — one step at a time)
- **PM3 t1 re-run + verdict** (when the time gap elapses) → only then **PM3 — pain-taxonomy persistence** (SQLite next to `vault/.vault-index.db`; stable pain key via E3's dedup).
- **PM2/E4** velocity + demand-intent (`RESEARCH →` Google Trends slope / autocomplete as a *scoring* signal, never gate-evidence; prefer free/local).
- **D3** discovery dashboard artifact (run history, spend vs caps, pain-trend movement — self-contained HTML, model on `agent-fleet-observability/`).
- **Step F (Phase 3, gated):** buyer-conversation test (red-team #2/#3) before any paid surface; then E5 (decouple from one machine) · D5 (interactive card triage) · PM1 (fabrication-gate scorecard) · PM5 (packaging).

## Conventions (do not violate)
- **TDD** + verification-before-completion + a **final whole-branch adversarial review**. Verify with `cd tools/llm-council && uv run pytest tests/ -q` (baseline **268 passed, 1 skipped**) and `python3 scripts/validate.py`. **Suspect the test when an implementer deforms the design to pass it; verify subagent claims against git + tests, not their summary.**
- **Cost:** council/FUSE/Sonar = OpenRouter, **real $** (discovery cap **$10/day / $50/month**; shared spend file). **Deep-research + local-NLI = $0.** Surface the estimate + check the day's spend before any paid call (PM3 t0 seed is the paid item here; E1 should be $0 if it lands on local NLI).
- **Vault git:** keep discovery branches free of vault changes; research notes → `vault/`, left **unstaged**; never weaken the privacy layer. **Branch → PR → Sean squash-merges**, small/focused. Commit trailer `Co-Authored-By: Claude Opus 4.8 (1M context)`; PR footer the Claude Code line. Write a **field report** to `docs/field-reports/` at the end of a meaty session.
- **Capture deferred work** as one-line `- ` bullets under `## Todo` in `vault/00_inbox/tickets.md` — flag for Sean rather than committing it.

## Read first (source of truth)
- Master plan: `vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md` (ranked ideas §4, roadmap §5, OST §8, North Star §9, red-team §10).
- E2 (newest pattern to mirror): spec `docs/superpowers/specs/2026-06-30-discovery-e2-judge-debias-design.md` · plan `docs/superpowers/plans/2026-06-30-discovery-e2-judge-debias.md` · research note `vault/20_projects/research/2026-06-30-llm-judge-self-preference-debias-research.md`.
- The engine: `tools/llm-council/council/discovery/` — E1 touches `verify.py` (the chokepoint); follow-ups touch `gather/sonar.py` + `gather/reviews.py`; PM3 seed uses `evidence.py::EvidenceBundle.to_dict`. Tests in `tools/llm-council/tests/discovery/`.
- Skill: `.claude/skills/fusion-discovery-council/SKILL.md` (§2 stages, §6 gate). Spend: `vault/health/council-spend-*.json`.
