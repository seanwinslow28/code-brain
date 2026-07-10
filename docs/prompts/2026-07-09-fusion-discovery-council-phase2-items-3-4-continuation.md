# Continuation — fusion-discovery-council, Phase 2 Items 3–4 (fresh session)

Paste everything **below the divider** into a fresh **Claude Code session in `code-brain`**. Above the divider is context for you (Sean).

**Where we are:** Item 1 (E1 loose-ends) merged as PR #112. Item 2 (PM2/E4 velocity scoring channel) merged as **PR #122 (2026-07-09)** — baseline on `origin/main` is now **326 passed, 1 skipped** in `tools/llm-council`. Remaining in the Phase-2 "everything buildable now" campaign: **Item 3 (D3 dashboard)** and **Item 4 (PM3 groundwork — de-risk + spec only)**. Everything blocked on the 7/21 PM3 t1 verdict stays out of scope.

**Verified insights carried from Items 1–2:**
- The empty-bundle early-return in `pipeline.py` (`if not bundle.records:`) writes **nothing** to `sessions_dir`, and `sessions_dir` isn't passed on every path — so many real runs persist nowhere. This is Item 3's highest-leverage decision (Slice A), now confirmed twice.
- E4 (Item 2) added the fields D3 renders: each session JSON now carries run-level **`velocity_mode`** ("off"/"pytrends") and **`why_now_coverage`** (% cards with a velocity signal), plus per-card `ScoreBreakdown.velocity*`. The §9 "why-now coverage" metric is measurable now.
- Follow-up ticket already logged (do NOT action in this campaign): expose `velocity_weight` via config/env.

**Local-main note (2026-07-09):** at the end of the Item-2 session, local `main` had diverged from `origin/main` — a local-only tickets commit (`e3ced2e`) whose one-line change is **already on `origin/main`** via the #122 squash. Fix is `git reset --hard origin/main`, but that discards an **unstaged** `velocity_weight` follow-up ticket in `vault/00_inbox/tickets.md` — commit the vault first (Obsidian-Git) or re-add that ticket after. The fresh session should work from a synced `origin/main`.

---

You're partnering with **Sean Winslow** in `code-brain` on **fusion-discovery-council**. Sean is a PM/creative technologist who wants the *why* and the *how*, values momentum, and wants a real thinking partner — not a yes-man. Use **TDD** and the superpowers skills. **Surface cost before any paid run** (this campaign is $0 except optional live-validation runs — flag and check the $10/day cap first).

## FIRST: sync + baseline
Confirm you're on an up-to-date `main`: `git fetch origin && git status`. If `main` is behind `origin/main`, fast-forward. If it's **diverged** (a known local-only tickets commit `e3ced2e`, content already on origin via the #122 squash), tell Sean — the fix is `git reset --hard origin/main`, which he must approve because it touches the vault working tree (an unstaged `velocity_weight` ticket). Baseline check: `cd tools/llm-council && uv run pytest tests/ -q` should report **326 passed, 1 skipped**; `python3 scripts/validate.py` (repo root) PASSED.

## YOUR MISSION: complete Phase-2 Items 3 and 4, so the 7/21 PM3 t1 verdict is the only thing left gating Phase 2.

Two items below. **Item 3** ships as its own branch → PR → Sean squash-merges — it is a **NEW feature**, so start with **superpowers:brainstorming**, then a spec, then **superpowers:writing-plans**, then **superpowers:subagent-driven-development** (fresh subagent per task, two-stage review, final whole-branch adversarial review on the most capable model before the PR). Do NOT skip brainstorming — Slice A is a real design decision. **Item 4** is research + spec only (no PR, no gated build). Do **one item per session** if context runs long; each is independent. Recommended order: 3 → 4.

### Item 3 — D3: discovery dashboard artifact ($0)
A self-contained HTML view over run history + the highest-leverage persistence fix. **Brainstorm/design → spec → plan → build.**

- **Slice A — stop the leak (the highest-leverage part; decide WITH Sean during brainstorm).** The session store is **sparse**: the empty-bundle early-return writes nothing and `sessions_dir` isn't passed on every path, so real runs persist nowhere. Decide whether to **wire `sessions_dir` on by default** (including the empty-bundle path) — a small `pipeline.py` change with a test. This is **data-loss-in-progress**; every un-persisted run is history we can't recover. It also motivates PM3's persistent store (Item 4) as the real run-history home.
- **Slice B — the artifact.** One command renders a self-contained HTML view over whatever run history exists: spend vs the **$10/day + $50/mo caps**; **verified/dropped** trend; **citation precision/recall** (in session JSON from E1); FUSE success / per-collector yield; cost/run vs tier cap; run-level **`velocity_mode` + `why_now_coverage`** (new from E4 — the §9 why-now-coverage metric); leave a **slot** for pain-taxonomy movement once PM3 lands. Add **"re-open / re-run this topic"** affordances. Render **honestly** — labeled "thin" when data is thin. Consider the **impeccable** / **frontend-design** skills for the artifact itself.
- **Data sources:** session JSONs in `vault/20_projects/research/.discovery-sessions/*.json` + spend ledgers `vault/health/council-spend-*.json`. Follow the **agent-fleet-observability** HTML pattern Sean already ships.
- **Success:** one command produces the HTML artifact over the real run history, honestly labeled when thin; the `sessions_dir` decision is made and (if chosen) the leak is fixed with a test.
- **Cost:** $0.

### Item 4 — PM3 groundwork: de-risk + pre-plan (NOT the gated build)
Make 7/21 execute-ready without building the part red-team #5 gates. Two deliverables, both **$0**, no PR (research note → `vault/`, a spec → `docs/superpowers/specs/`).

- **4a. Run the cheap pain-key clustering validation NOW** (§8 O3 / §7 assumption #2): cluster the verified pains from two existing **same-topic** runs and eyeball whether the "same pain" matches are real. Candidates on disk: the two 2D-animation **pm** runs (2026-06-21, standard+deep, same topic) in `.discovery-sessions/`, and/or the pm3-t0 bundle (`vault/20_projects/research/.discovery-sessions/pm3-t0-ai-coding-assistants-2026-06-30.json`). **Threshold: ≥80% correct same-pain matches before persistence is worth building.** Reuse **E3's** dedup/similarity (`dedup.py`) for the pain-key match. Write findings to `vault/`. This validates PM3's *stable-key* assumption independently of the *trend-signal* question the t1 re-run tests.
- **4b. Spec the persistence design** (`docs/superpowers/specs/`): SQLite next to `vault/.vault-index.db`; stable pain-key via embedding-cluster or canonical-title (whichever 4a validates); reuse the existing `EvidenceBundle.to_dict/from_dict` serializer as the seed; schema for pain frequency/intensity/recency-over-time; how a re-run emits "accelerating / cooling / newly emerged." **Do NOT build it** — the go/no-go is the 7/21 t1 verdict. Result: if t1 says GO, 4b is ready to execute; if KILL/rescope, we spent only the $0 clustering test.

## Conventions (do not violate)
- **Method:** new features (Item 3) → superpowers:brainstorming → spec → superpowers:writing-plans → superpowers:subagent-driven-development (fresh subagent per task, two-stage review, final whole-branch adversarial review on the most capable model before the PR). Item 4 → research + spec, no build.
- **TDD** + verification-before-completion. `cd tools/llm-council && uv run pytest tests/ -q` (**baseline on `main` after PR #122: 326 passed, 1 skipped**) and `python3 scripts/validate.py` (from repo root). Suspect the test when an implementer deforms the design to pass it.
- **Cost:** this campaign is $0. Any paid discovery/validation call — surface the estimate and check `vault/health/council-spend-*.json` against the $10/day / $50/month caps FIRST.
- **Vault git:** keep branches free of vault changes (Obsidian-Git owns the vault) — research/specs/notes land in `vault/`/`docs/` and stay unstaged for vault paths; never weaken the privacy layer. Commit trailer `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`; PR footer the Claude Code line. Field report to `docs/field-reports/` at the end of each item.
- **Capture deferred work** as one-line `- ` bullets under `## Todo` in `vault/00_inbox/tickets.md`.

## Read first (source of truth)
- Master plan: `vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md` (§5 roadmap, §7 caveats, §8 OST, §9 metrics, §10 red-team, §11 conversion audit).
- Skill: `.claude/skills/fusion-discovery-council/SKILL.md` (§6 the gate).
- Engine: `tools/llm-council/council/discovery/` — chiefly `pipeline.py` (session JSON + `sessions_dir` — note the empty-bundle path writes nothing), `dedup.py` (E3 similarity, reused by 4a), `scoring.py`/`frame.py` (E4's `velocity_mode`/`why_now_coverage` now in session JSON), `verify.py` (the E1 gate; citation precision/recall in session JSON).
- Field reports: Item 2 `docs/field-reports/2026-07-09-fusion-discovery-council-e4-velocity-channel-field-report.md`; Item 1 `docs/field-reports/2026-07-01-fusion-discovery-council-e1-loose-ends-field-report.md`.
- Prior continuation (Items 2–4, for lineage): `docs/prompts/2026-07-01-fusion-discovery-council-phase2-items-2-3-4-continuation.md`.

## THEN (after this campaign, subsequent sessions)
- **PM3 t1 re-run + verdict (~2026-07-21, ticketed, paid ~$1.50–1.85)** → then execute the Item-4b PM3 persistence plan (if GO).
- **Phase 3 (paid, gated behind Phase 2):** E5 (decouple from one machine) · D5 (interactive triage) · PM1+PM5 (gate scorecard as brand + packaging) · Step F buyer conversations (red-team #2/#3 — the paid wedge).
