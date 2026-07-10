# Continuation — fusion-discovery-council, PM3 t1 verdict + conditional 4b build (fresh session)

Paste everything **below the divider** into a fresh **Claude Code session in `code-brain`** — run it **on or after ~2026-07-21** (the t1 re-run is time-gated; see "Timing" below). Recommended model: **Opus 4.8** (a signal-vs-noise judgment plus, on GO, a substantial multi-file TDD build). Above the divider is context for you (Sean).

**Where we are:** The **Phase-2 "everything buildable now" campaign is COMPLETE** — Item 1 (E1) #112, Item 2 (E4 velocity) #122, Item 3 (D3 dashboard + persist-by-default) #123, Item 4 (PM3 groundwork: 4a clustering validation + 4b persistence spec) on `main` via `189f71a`. Baseline on `main`: **366 passed, 1 skipped** (`cd tools/llm-council && uv run pytest tests/ -q`).

**The ONLY thing left gating Phase 2 is the PM3 t1 re-run + verdict.** This prompt is that task. It is paid (~$1.50–1.85) and time-gated to ~7/21. Its outcome forks the future:
- **GO** (movement > sampling noise) → build PM3 from the execute-ready 4b spec.
- **KILL/rescope** (movement ≤ noise → PM3 is memory/dedup, not a trend signal — red-team #5's objection) → close PM3; Phase 2 is done; **Phase 3 opens** (E5 · D5 · PM1+PM5 · Step F — a new, paid campaign, out of scope here).

**Trailer note:** Fable did Items 3–4 with a `Co-Authored-By: Claude Fable 5` trailer. This session runs on Opus 4.8, so use `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

---

You're partnering with **Sean Winslow** in `code-brain` on **fusion-discovery-council**. Sean is a PM/creative technologist who wants the *why* and the *how*, values momentum, and wants a real thinking partner — not a yes-man. Use the superpowers skills. This task has a **paid touchpoint** — surface the cost estimate and check the cap BEFORE running it.

## FIRST: sync, baseline, timing
1. `git fetch origin && git status` — confirm you're on an up-to-date `main` (should be at least `560b663` = D3 #123). Fast-forward if behind.
2. Baseline: `cd tools/llm-council && uv run pytest tests/ -q` → **366 passed, 1 skipped**; `python3 scripts/validate.py` (repo root) PASSED.
3. **Timing check:** t0 was seeded **2026-06-30**. The t1 comparison is a *trend-over-time* read, so it needs a real gap — **~7/21 or later**. If today is materially earlier than ~7/21, tell Sean the shorter gap weakens the signal-vs-noise verdict and confirm he still wants to run it now.

## THE TASK: run PM3 t1, deliver the verdict, then branch

### Step 1 — Surface cost, check the cap, get the go-ahead (BEFORE spending)
The t1 re-run is a **standard-tier** discovery run on topic **"AI coding assistants"** (the exact t0 config). Estimated **$1.50–1.85**. Check `vault/health/council-spend-*.json` against the **$10/day / $50/month** caps for the current month FIRST, state the estimate + remaining headroom, and get Sean's explicit go-ahead before running. Do NOT spend without it.

### Step 2 — Run t1 (same topic + tier as t0)
Re-run the SAME topic + tier via the `fusion-discovery-council` skill (or `uv run python -m council.discovery ...` at standard tier, topic "AI coding assistants"). D3's Slice A now **persists sessions by default**, so t1's session JSON lands in the store automatically. Record the run's session id and cost.

### Step 3 — Compare t1 vs the frozen t0 bundle (use the 4a-validated matcher)
- **t0 bundle:** `vault/20_projects/research/.discovery-sessions/pm3-t0-ai-coding-assistants-2026-06-30.json` (93 evidence records, **8 verified**, 2 dropped, $1.85). Do not mutate it — it's the frozen baseline.
- **Pain-key matching:** use the two-stage matcher 4a proved (8-for-8), NOT naive lexical similarity (which scored cross-run duplicates at 0.06–0.17, far under E3's 0.5 threshold — it will under-match and lie). The matcher: **candidate generation = exact-shared-evidence-URL ∪ lexical top-1** (E3's `dedup.py::pain_similarity`, reused as-is), then **confirm each candidate with a temperature-0 local LLM judge** (`qwen3.6_35b-a3b-32k` on MBP Ollama, `localhost:11434`) returning strict `SAME | RELATED | DIFFERENT`. **Never a similarity band** for candidate gen (measured B1↔B7 hazard). Full recipe + the failure analysis: `vault/20_projects/research/2026-07-09-pm3-4a-pain-key-clustering-validation.md`. (If Ollama/MBP is unreachable, defer honestly and tell Sean — no cloud fallback.)
- For each t0 verified pain, establish its identity in t1 (SAME/RELATED/DIFFERENT), then compute **per-pain frequency + intensity movement** t0→t1: which pains persisted, which cooled/vanished, which newly emerged, and whether intensity rose/fell.

### Step 4 — THE VERDICT (the gate)
Judge: **is the t0→t1 movement > sampling/panel noise, or ≤ noise?** This is red-team #5's exact objection. Be adversarial with yourself — a couple of pains shuffling rank on a 3-week gap is noise, not a trend signal. State the verdict explicitly (GO / KILL / RESCOPE) with the evidence. Write the t1 result + comparison + verdict to `vault/` (a research note beside the 4a note) and update the PM3 t1 ticket in `vault/00_inbox/tickets.md`.

### Step 5 — Branch on the verdict
- **GO** → build PM3 from the execute-ready spec `docs/superpowers/specs/2026-07-09-pm3-persistence-design.md`. It's a NEW feature build: **superpowers:writing-plans** over that spec → **superpowers:subagent-driven-development** (fresh subagent per task, two-stage review, final whole-branch adversarial review on the most capable model before the PR). The spec already fixes the architecture (SQLite at `vault/.discovery-pains.db`, opaque pain id + per-ingest two-stage matcher, `pain_links` for RELATED/`broader_than`, `match_audit` replayability, opt-in `DISCOVERY_PAIN_STORE=1`, honest Ollama-down deferral + catch-up, trend labels into the ledger + the D3 dashboard's PM3 slot). Ships as its own branch → PR → Sean squash-merges. Then Phase 2 is fully closed.
- **KILL / RESCOPE** → do NOT build. Record the rationale in the ticket + the vault note, close PM3, and report that **Phase 2 is complete**. The $0 groundwork gate did its job — we spent only the clustering test + this one paid run. Then tee up **Phase 3** for a future session (E5 decouple-from-one-machine · D5 interactive triage · PM1+PM5 gate-scorecard-as-brand + packaging · Step F buyer conversations — the paid wedge, red-team #2/#3).

## Conventions (do not violate)
- **Cost:** the t1 run is the only paid touchpoint — surface the estimate + check `vault/health/council-spend-*.json` against the $10/day / $50/month caps FIRST; get explicit go-ahead. The 4a matcher comparison is $0 (local Ollama).
- **Method:** on GO, the 4b build follows superpowers:writing-plans → subagent-driven-development (fresh subagent per task, two-stage review, final whole-branch review on the most capable model before the PR). TDD + verification-before-completion throughout; hermetic tests (tmp SQLite; judge behind an injectable seam like E4's `_pytrends_fetch`) — nothing may touch the real vault or make a live LLM call in tests.
- **Baseline:** `cd tools/llm-council && uv run pytest tests/ -q` (366 passed, 1 skipped) and `python3 scripts/validate.py` (repo root). Suspect the test when an implementer deforms the design to pass it.
- **Vault git:** keep branches free of vault changes (research/verdict notes land in `vault/` and stay unstaged for vault paths; Sean commits the vault); never weaken the privacy layer. Commit trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`; PR footer the Claude Code line. Field report to `docs/field-reports/` at the end.
- **Capture deferred work** as one-line `- ` bullets under `## Todo` in `vault/00_inbox/tickets.md`.

## Read first (source of truth)
- **4b spec (the build target on GO):** `docs/superpowers/specs/2026-07-09-pm3-persistence-design.md`.
- **4a validation note (the matcher recipe + why naive matching fails):** `vault/20_projects/research/2026-07-09-pm3-4a-pain-key-clustering-validation.md`.
- **PM3 groundwork field report:** `docs/field-reports/2026-07-09-fusion-discovery-council-pm3-groundwork-field-report.md`.
- **Master plan:** `vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md` (§5 roadmap, §7 caveats, §8 OST, §9 metrics, §10 red-team #5, §11 conversion audit).
- **Skill:** `.claude/skills/fusion-discovery-council/SKILL.md` (§6 the gate). **Engine:** `tools/llm-council/council/discovery/` — `dedup.py` (E3 `pain_similarity`, the 4a candidate-gen signal), `pipeline.py` (persist-by-default session store from D3; the PM3 ingest hook point on the success path), `scoring.py`/`frame.py` (E4 `velocity_raw` per observation), `dashboard.py`/`__main__.py` (D3 render + the reserved PM3 slot).
- **D3 dashboard (renders run history + the PM3 slot):** `uv run python -m council.discovery.dashboard --output <path>` — the honest health surface over the now-persisted store.
- **Prior continuations (lineage):** `docs/prompts/2026-07-09-fusion-discovery-council-phase2-items-3-4-continuation.md`, `docs/prompts/2026-07-01-fusion-discovery-council-phase2-items-2-3-4-continuation.md`.

## THEN (after this task)
- **On GO + 4b merged, or on KILL:** Phase 2 is closed. **Phase 3** (paid, gated behind Phase 2) is next: E5 (decouple from one machine) · D5 (interactive triage) · PM1+PM5 (gate scorecard as brand + packaging) · Step F buyer conversations (the paid wedge). Scope it in a fresh session with its own continuation prompt.
- **Optional interim polish (non-gating, $0):** the D3 hardening bundle ticket in `vault/00_inbox/tickets.md` (charset/doctype, intra-day discrepancy granularity, kind-aware empty-gather label, `DISCOVERY_SESSIONS_DIR=""` disable semantics) — all triaged-LEAVE at the D3 final review, safe to pick up anytime.
