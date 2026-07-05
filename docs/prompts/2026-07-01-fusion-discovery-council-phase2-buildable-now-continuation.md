# Continuation — fusion-discovery-council, Phase 2 "everything buildable now" (fresh session)

Paste everything **below the divider** into a fresh **Claude Code session in `code-brain`**. Above the divider is context for you (Sean).

**Why this campaign:** E1 (entailment gate v2) merged 2026-07-01 (PR #111) and closed out **Phase 1**. The next phase (Phase 2 — evidence breadth + the longitudinal moat) has one item, **PM3**, that is **time-gated on the PM3 t1 re-run (~2026-07-21)** — red-team #5 says don't build the taxonomy persistence until that re-run proves pain-movement exceeds sampling noise. This campaign builds **everything in Phase 2 that is NOT blocked on that verdict**, plus de-risks and pre-plans PM3 itself, so that when 7/21 arrives the only open question is the data verdict — the build is ready to execute either way.

**What's already done (context):** Phase 0 (E2 #109, H/gather #110) and Phase 1 (PM4+D1 #103, D4 #104, E3 #105, D2 #106, E1 #111) are all shipped to `main`. E6/BACKFILL shipped (#97, agent-layer). Week-0 conversion audit REFUTED the "discovery doesn't convert" kill-assumption (~88%). PM3 t0 baseline seeded (`vault/20_projects/research/.discovery-sessions/pm3-t0-ai-coding-assistants-2026-06-30.json`).

**Master plan (source of truth for the whole roadmap):** `vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md` — read §5 (phased roadmap), §8 (OST), §9 (metrics), §10 (red-team). This campaign = Phase 2's buildable half + the E1 loose ends.

---

You're partnering with **Sean Winslow** in `code-brain` on **fusion-discovery-council**. Sean is a PM/creative technologist who wants the *why* and the *how*, values momentum, and wants a real thinking partner — not a yes-man. Use **TDD** and the superpowers skills. **Surface cost before any paid run** (most of this campaign is $0; the only paid touchpoints are optional live-discovery validation runs and possibly a demand-intent API — flag and check the $10/day cap first).

## YOUR MISSION: complete all Phase-2 work that isn't blocked on the 7/21 PM3 t1 verdict, so 7/21 is execute-ready.

Four work items below, in recommended order. Items 1–3 each ship as their own branch → PR → Sean squash-merges (match the established rhythm). Item 4 is de-risk + spec only (no gated build). **These are mostly NEW features, not pre-planned like E1 was** — so for items 2 and 3 you MUST start with **superpowers:brainstorming**, then a spec, then **superpowers:writing-plans**, then **superpowers:subagent-driven-development**. Item 1 is already-scoped cleanup (go closer to direct TDD). Do NOT skip brainstorming on 2 and 3 — the design decisions there are real.

---

### Item 1 — Close the E1 loose ends (quick, already-scoped; ~1 short session)
These are the three open E1 tickets (`vault/00_inbox/tickets.md`). Small, clear, mostly TDD-direct. One branch, one PR.

1a. **Settle the ALCE citation-precision semantics for unfetched/phantom cited URLs** — this is a real DECISION, make it with Sean before coding. `verify.py::citation_metrics` uses `v.point.urls` (all model-cited urls, incl. ones never fetched into the bundle) as the precision denominator. Options: **(a)** keep phantoms in the denominator (current — a phantom lowers precision in the common case); **(b)** exclude non-bundle urls `[u for u in v.point.urls if bundle.has_url(u)]`; **(c)** count each unfetched citation as a hard precision miss (most aligned with "verified, not hallucinated"). Background: the final E1 review claimed phantom urls "inflate precision toward 1.0," but that only holds in a narrow multi-quote edge case; the common case lowers precision (controller-traced 2026-07-01). Pick one WITH Sean, then **add a phantom-URL test** asserting the chosen value **and a τ=0.5 boundary fixture** (today only 0.92/0.10 are tested, so `>=` vs `>` is unpinned).
1b. **Fix the E1 plan-doc bug** so a future re-run can't reintroduce it: `docs/superpowers/plans/2026-06-30-discovery-e1-entailment-gate.md` Task 3 Step 3 example code writes `urls = v.supporting_urls` (yields precision 1.0, contradicting its own asserted 0.5 test). Correct it to `v.point.urls` (or whatever 1a decides). This is a docs edit, not code.
1c. **Code hygiene** (non-blocking, do while you're in there): `verify.py::_CLAIM_SENT` splits on every `.` ("Mr. Smith" / "v3.0" → spurious fragments — consider an abbreviation-aware split or a min-length guard, TDD it); `tools/llm-council/scripts/install_nli_model.sh` download step's `|| true` swallows the `hf` error message (drop it, let failures surface — the existence check still guards); `tests/discovery/test_nli.py` unused `import importlib` + duplicated mid-file imports; empty-bundle session JSON omits `verify_mode`/`citation_*` keys (add for schema uniformity — the pipeline already passes `verify_mode="substring-only"` to that render call, so mirror it into the returned session dict).

### Item 2 — PM2/E4: velocity + demand-intent scoring channel (the flagship Phase-2 build)
The "why now" layer competitors sell separately (Exploding Topics velocity, AnswerThePublic demand-intent) — fused into the gated card. **Brainstorm → spec → plan → build.**

- **What exists:** `scoring.py::score_opportunity` → `ScoreBreakdown(value, confidence, importance, reach, recency, source_corroboration)`; `VALUE_WEIGHTS = {importance .45, reach .40, recency .15}`; exponential **recency** decay (halflife 30d). `frame.py::_why_now(score)` is a **static freshness note** off the single evidence date — NOT a real velocity signal. E4 adds a real **velocity** (demand slope over time) + **demand-intent** (autocomplete / People-Also-Ask) term and rewrites `_why_now` to use it.
- **THE LOAD-BEARING INVARIANT (this is the moat — do not violate):** velocity/demand-intent are **SCORE signals ONLY, NEVER gate-evidence.** Autocomplete/PAA produce *queries, not URL-anchored quotes* — they must never enter `verify.py`, the `EvidenceBundle`, or be paraphrased into a sourced claim. Enforce structurally (a separate channel that feeds `scoring.py`, blind to the gate), exactly as the skill already excludes non-URL sources. A reviewer must be able to confirm no demand-intent string can reach the fabrication gate.
- **Design decisions for brainstorming:** which free/cheap source (pytrends for Google-Trends slope is free but alpha; SerpApi autocomplete/PAA has a metered tier — surface cost); how the velocity term folds into `VALUE_WEIGHTS` **without over-correcting** (research §7 caveat: recency/velocity weighting can over-correct — keep the weight tunable, guard it, and report the raw term so a regression is visible); graceful degradation (no signal → card still renders, `_why_now` falls back to today's recency note — mirror E1's optional-dependency + `get_scorer()→None` seam).
- **Success:** a run produces cards whose `why_now` carries a real velocity/demand signal with a tunable weight; the fabrication gate is provably untouched; no-signal degrades cleanly; metrics §9 "why-now coverage" becomes measurable.
- **Cost:** pytrends = $0; any demand-intent API = surface + check the $10/day cap first; validation can re-score an EXISTING session JSON ($0) before any live run.

### Item 3 — D3: discovery dashboard artifact (observability surface, $0)
A self-contained HTML view over run history. **Brainstorm/design → build** (consider the frontend-design / impeccable skills for the artifact itself).

- **What it shows:** spend vs the $10/day + $50/mo caps; verified/dropped trend; **citation precision/recall** (now in session JSON from E1); FUSE success / per-collector yield; cost/run vs tier cap; (pain-taxonomy movement once PM3 lands — leave a slot). Add "re-open / re-run this topic" affordances. This makes the §9 health metrics — which are *measurable now* from the session JSON + spend files — actually visible, and answers the research-flagged bill-shock anxiety.
- **Data sources:** session JSONs in `vault/20_projects/research/.discovery-sessions/*.json` + spend ledgers `vault/health/council-spend-*.json`. Follow the **agent-fleet-observability** HTML pattern Sean already ships.
- **FLAG (design constraint):** the session store is currently **sparse** — only ~5 JSONs — because `run_discovery`'s `sessions_dir` isn't passed on every path (many real runs wrote nowhere). D3 should (a) render honestly what exists, and (b) this motivates PM3's persistent store as the real run-history home. Decide with Sean whether D3 also wires `sessions_dir` on by default so history stops leaking (small pipeline change) — that's arguably the highest-leverage part.
- **Success:** one command produces an HTML artifact that shows the health metrics over whatever run history exists, honestly labeled when data is thin.

### Item 4 — PM3 groundwork: de-risk + pre-plan (NOT the gated build)
Make 7/21 execute-ready without building the part red-team #5 gates. Two deliverables, both $0, no PR needed (research notes → `vault/`, a spec → `docs/superpowers/specs/`).

4a. **Run the cheap pain-key clustering validation NOW** (§8 O3 / §7 assumption #2): cluster the verified pains from two existing **same-topic** runs and eyeball whether the "same pain" matches are real. Candidates on disk: the two 2D-animation **pm** runs (2026-06-21, standard+deep, same topic) in `.discovery-sessions/`, and/or the pm3-t0 bundle. **Threshold: ≥80% correct same-pain matches before persistence is worth building.** Reuse **E3's** dedup/similarity (`dedup.py`) for the pain-key match — it already exists. Write findings to `vault/`. This validates PM3's *stable-key* assumption independently of the *trend-signal* question the t1 re-run tests.
4b. **Spec the persistence design** (`docs/superpowers/specs/`): SQLite next to `vault/.vault-index.db`; stable pain-key via embedding-cluster or canonical-title (whichever 4a validates); reuse the existing `EvidenceBundle.to_dict/from_dict` serializer (built in Step C/D) as the seed; schema for pain frequency/intensity/recency-over-time; how a re-run emits "accelerating / cooling / newly emerged." **Do NOT build it** — the go/no-go is the 7/21 t1 verdict. Result: if t1 says GO, item 4b is a ready plan to execute; if it says KILL/rescope, we spent only the $0 clustering test.

**PM3 t1 re-run itself (~2026-07-21, ticketed, NOT this campaign):** re-run the SAME topic+tier ("AI coding assistants", standard) and compare verified-pain frequency/intensity vs the frozen t0 bundle. Paid (~$1.50–1.85) — surface cost + check the cap. If movement ≤ sampling noise → PM3 is a memory/dedup feature, not a trend signal → kill or rescope per red-team #5.

---

## Recommended order & rationale
1 (E1 cleanups — quick, closes loops, warms up the discovery code) → 2 (PM2/E4 — biggest differentiation, the meaty build) → 3 (D3 — lighter, and benefits from E4's new fields) → 4 (PM3 de-risk — unblocks 7/21). Items are independent; reorder if you prefer D3 before E4. Each of 1/2/3 is its own PR.

## Conventions (do not violate)
- **Method:** new features (items 2, 3) → superpowers:brainstorming → spec → superpowers:writing-plans → superpowers:subagent-driven-development (fresh subagent per task, two-stage review, final whole-branch adversarial review on the most capable model before the PR). Item 1 → TDD-direct is fine (scoped). Item 4 → research + spec, no build.
- **TDD** + verification-before-completion. `cd tools/llm-council && uv run pytest tests/ -q` (current baseline after E1: **297 passed, 1 skipped** on `main`) and `python3 scripts/validate.py` (from repo root). Suspect the test when an implementer deforms the design to pass it.
- **Cost:** most of this is $0. Any paid discovery/demand-intent call — surface the estimate and check `vault/health/council-spend-*.json` against the $10/day / $50/month caps FIRST.
- **Vault git:** keep branches free of vault changes (Obsidian-Git owns the vault) — research/specs/notes land in `vault/`/`docs/` and stay unstaged for vault paths; never weaken the privacy layer. Commit trailer `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`; PR footer the Claude Code line. Field report to `docs/field-reports/` at the end of each item.
- **Capture deferred work** as one-line `- ` bullets under `## Todo` in `vault/00_inbox/tickets.md`.

## Read first (source of truth)
- Master plan: `vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md` (§5 roadmap, §8 OST, §9 metrics, §10 red-team, §11 conversion audit).
- Skill: `.claude/skills/fusion-discovery-council/SKILL.md` (§6 the gate).
- Engine: `tools/llm-council/council/discovery/` — chiefly `scoring.py` (the score E4 extends), `frame.py` (`_why_now`, the card), `pipeline.py` (session JSON + `sessions_dir`), `dedup.py` (E3 similarity, reused by PM3 4a), `verify.py` (the gate — must stay untouched by E4's demand channel).
- E1 field report (just shipped): `docs/field-reports/2026-07-01-fusion-discovery-council-e1-entailment-gate-build-field-report.md`.

## THEN (after this campaign, subsequent sessions)
- **PM3 t1 re-run + verdict (~2026-07-21)** → then execute the item-4b PM3 persistence plan (if GO).
- **Phase 3 (map to paid, gated behind Phase 2):** E5 (decouple from one machine) · D5 (interactive triage) · PM1+PM5 (gate scorecard as brand + packaging) · Step F buyer conversations (red-team #2/#3 — the paid wedge).
