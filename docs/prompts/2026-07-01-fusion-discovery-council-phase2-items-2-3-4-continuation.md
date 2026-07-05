# Continuation — fusion-discovery-council, Phase 2 Items 2–4 (fresh session)

Paste everything **below the divider** into a fresh **Claude Code session in `code-brain`**. Above the divider is context for you (Sean).

**Where we are:** Item 1 (the E1 loose-ends cleanup) shipped as **PR #112, merged to `main` 2026-07-01** — option (c) phantom-URL precision semantics + abbreviation-aware claim split + hygiene; all three E1 tickets closed; baseline is now **303 passed, 1 skipped**. This continuation is the **rest of the Phase-2 "everything buildable now" campaign**: Item 2 (PM2/E4 velocity+demand-intent, the flagship build), Item 3 (D3 dashboard), Item 4 (PM3 groundwork — de-risk + spec only). Everything blocked on the 7/21 PM3 t1 verdict stays out of scope.

**Verified insight to carry into Item 3 (found during Item 1):** the empty-bundle early-return path in `pipeline.py` (`if not bundle.records:`) never writes to `sessions_dir` at all — so low-signal runs leak from history entirely, on top of the known "`sessions_dir` not passed on every path" gap. This makes the Item-3 decision to wire `sessions_dir` on by default the highest-leverage part of D3, and it's now confirmed, not hypothetical.

---

You're partnering with **Sean Winslow** in `code-brain` on **fusion-discovery-council**. Sean is a PM/creative technologist who wants the *why* and the *how*, values momentum, and wants a real thinking partner — not a yes-man. Use **TDD** and the superpowers skills. **Surface cost before any paid run** (most of this is $0; the only paid touchpoints are optional live-discovery validation runs and possibly a demand-intent API — flag and check the $10/day cap first).

## YOUR MISSION: complete Phase-2 Items 2, 3, and 4 (Item 1 already merged), so the 7/21 PM3 t1 verdict is the only thing left gating Phase 2.

Three work items below, in recommended order. Items 2 and 3 each ship as their own branch → PR → Sean squash-merges. Item 4 is de-risk + spec only (no gated build). **These are NEW features, not pre-planned** — so for Items 2 and 3 you MUST start with **superpowers:brainstorming**, then a spec, then **superpowers:writing-plans**, then **superpowers:subagent-driven-development** (fresh subagent per task, two-stage review, final whole-branch adversarial review on the most capable model before the PR). Do NOT skip brainstorming — the design decisions in 2 and 3 are real.

Do **one item per session** if context runs long; each is independent. Recommended: 2 → 3 → 4 (D3 benefits from E4's new fields), but 3-before-2 is fine if you prefer.

---

### Item 2 — PM2/E4: velocity + demand-intent scoring channel (the flagship Phase-2 build)
The "why now" layer competitors sell separately (Exploding Topics velocity, AnswerThePublic demand-intent) — fused into the gated card. **Brainstorm → spec → plan → build.**

- **What exists:** `scoring.py::score_opportunity` → `ScoreBreakdown(value, confidence, importance, reach, recency, source_corroboration)`; `VALUE_WEIGHTS = {importance .45, reach .40, recency .15}`; exponential **recency** decay (halflife 30d). `frame.py::_why_now(score)` is a **static freshness note** off the single evidence date — NOT a real velocity signal. E4 adds a real **velocity** (demand slope over time) + **demand-intent** (autocomplete / People-Also-Ask) term and rewrites `_why_now` to use it.
- **THE LOAD-BEARING INVARIANT (this is the moat — do not violate):** velocity/demand-intent are **SCORE signals ONLY, NEVER gate-evidence.** Autocomplete/PAA produce *queries, not URL-anchored quotes* — they must never enter `verify.py`, the `EvidenceBundle`, or be paraphrased into a sourced claim. Enforce structurally (a separate channel that feeds `scoring.py`, blind to the gate), exactly as the skill already excludes non-URL sources. A reviewer must be able to confirm no demand-intent string can reach the fabrication gate.
- **Design decisions for brainstorming:** which free/cheap source (pytrends for Google-Trends slope is free but alpha; SerpApi autocomplete/PAA has a metered tier — surface cost); how the velocity term folds into `VALUE_WEIGHTS` **without over-correcting** (research §7 caveat: recency/velocity weighting can over-correct — keep the weight tunable, guard it, and report the raw term so a regression is visible); graceful degradation (no signal → card still renders, `_why_now` falls back to today's recency note — mirror E1's optional-dependency + `get_scorer()→None` seam).
- **Success:** a run produces cards whose `why_now` carries a real velocity/demand signal with a tunable weight; the fabrication gate is provably untouched; no-signal degrades cleanly; metrics §9 "why-now coverage" becomes measurable.
- **Cost:** pytrends = $0; any demand-intent API = surface + check the $10/day cap first; validation can re-score an EXISTING session JSON ($0) before any live run.

### Item 3 — D3: discovery dashboard artifact (observability surface, $0)
A self-contained HTML view over run history. **Brainstorm/design → build** (consider the frontend-design / impeccable skills for the artifact itself).

- **What it shows:** spend vs the $10/day + $50/mo caps; verified/dropped trend; **citation precision/recall** (now in session JSON from E1); FUSE success / per-collector yield; cost/run vs tier cap; (pain-taxonomy movement once PM3 lands — leave a slot). Add "re-open / re-run this topic" affordances. This makes the §9 health metrics — measurable now from the session JSON + spend files — actually visible, and answers the research-flagged bill-shock anxiety.
- **Data sources:** session JSONs in `vault/20_projects/research/.discovery-sessions/*.json` + spend ledgers `vault/health/council-spend-*.json`. Follow the **agent-fleet-observability** HTML pattern Sean already ships.
- **FLAG (design constraint, confirmed in Item 1):** the session store is **sparse** — the empty-bundle early return writes nothing, and `sessions_dir` isn't passed on every path, so many real runs wrote nowhere. D3 should (a) render honestly what exists (labeled thin when thin), and (b) **decide with Sean whether to also wire `sessions_dir` on by default** so history stops leaking (small pipeline change — include the empty-bundle path). That's arguably the highest-leverage part and it motivates PM3's persistent store as the real run-history home.
- **Success:** one command produces an HTML artifact showing the health metrics over whatever run history exists, honestly labeled when data is thin.

### Item 4 — PM3 groundwork: de-risk + pre-plan (NOT the gated build)
Make 7/21 execute-ready without building the part red-team #5 gates. Two deliverables, both $0, no PR needed (research notes → `vault/`, a spec → `docs/superpowers/specs/`).

- **4a. Run the cheap pain-key clustering validation NOW** (§8 O3 / §7 assumption #2): cluster the verified pains from two existing **same-topic** runs and eyeball whether the "same pain" matches are real. Candidates on disk: the two 2D-animation **pm** runs (2026-06-21, standard+deep, same topic) in `.discovery-sessions/`, and/or the pm3-t0 bundle (`vault/20_projects/research/.discovery-sessions/pm3-t0-ai-coding-assistants-2026-06-30.json`). **Threshold: ≥80% correct same-pain matches before persistence is worth building.** Reuse **E3's** dedup/similarity (`dedup.py`) for the pain-key match. Write findings to `vault/`. This validates PM3's *stable-key* assumption independently of the *trend-signal* question the t1 re-run tests.
- **4b. Spec the persistence design** (`docs/superpowers/specs/`): SQLite next to `vault/.vault-index.db`; stable pain-key via embedding-cluster or canonical-title (whichever 4a validates); reuse the existing `EvidenceBundle.to_dict/from_dict` serializer as the seed; schema for pain frequency/intensity/recency-over-time; how a re-run emits "accelerating / cooling / newly emerged." **Do NOT build it** — the go/no-go is the 7/21 t1 verdict. Result: if t1 says GO, 4b is ready to execute; if KILL/rescope, we spent only the $0 clustering test.

**PM3 t1 re-run itself (~2026-07-21, ticketed, NOT this campaign):** re-run the SAME topic+tier ("AI coding assistants", standard) and compare verified-pain frequency/intensity vs the frozen t0 bundle. Paid (~$1.50–1.85) — surface cost + check the cap. If movement ≤ sampling noise → PM3 is a memory/dedup feature, not a trend signal → kill or rescope per red-team #5.

---

## Conventions (do not violate)
- **Method:** new features (2, 3) → superpowers:brainstorming → spec → superpowers:writing-plans → superpowers:subagent-driven-development (fresh subagent per task, two-stage review, final whole-branch adversarial review on the most capable model before the PR). Item 4 → research + spec, no build.
- **TDD** + verification-before-completion. `cd tools/llm-council && uv run pytest tests/ -q` (**baseline on `main` after PR #112: 303 passed, 1 skipped**) and `python3 scripts/validate.py` (from repo root). Suspect the test when an implementer deforms the design to pass it.
- **Cost:** most of this is $0. Any paid discovery/demand-intent call — surface the estimate and check `vault/health/council-spend-*.json` against the $10/day / $50/month caps FIRST.
- **Vault git:** keep branches free of vault changes (Obsidian-Git owns the vault) — research/specs/notes land in `vault/`/`docs/` and stay unstaged for vault paths; never weaken the privacy layer. Commit trailer `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`; PR footer the Claude Code line. Field report to `docs/field-reports/` at the end of each item.
- **Capture deferred work** as one-line `- ` bullets under `## Todo` in `vault/00_inbox/tickets.md`.

## Read first (source of truth)
- Master plan: `vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md` (§5 roadmap, §7 caveats, §8 OST, §9 metrics, §10 red-team, §11 conversion audit).
- Skill: `.claude/skills/fusion-discovery-council/SKILL.md` (§6 the gate).
- Engine: `tools/llm-council/council/discovery/` — chiefly `scoring.py` (the score E4 extends), `frame.py` (`_why_now`, the card), `pipeline.py` (session JSON + `sessions_dir` — note the empty-bundle path writes nothing), `dedup.py` (E3 similarity, reused by PM3 4a), `verify.py` (the gate — must stay untouched by E4's demand channel).
- Item 1 field report (just merged): `docs/field-reports/2026-07-01-fusion-discovery-council-e1-loose-ends-field-report.md`.

## THEN (after this campaign, subsequent sessions)
- **PM3 t1 re-run + verdict (~2026-07-21)** → then execute the Item-4b PM3 persistence plan (if GO).
- **Phase 3 (map to paid, gated behind Phase 2):** E5 (decouple from one machine) · D5 (interactive triage) · PM1+PM5 (gate scorecard as brand + packaging) · Step F buyer conversations (red-team #2/#3 — the paid wedge).
