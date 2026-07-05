# Continuation — fusion-discovery-council, Step C validation gates (panel-vs-single-model first) + beyond (next session)

Paste everything **below the divider** into a fresh **Claude Code session opened in `code-brain`** to continue the roadmap. Everything above the divider is context for you (Sean).

**What just shipped (2026-06-29):** **D2 — receipts UI** merged as **PR #106**. New `council/discovery/receipts.py` ($0/deterministic/stdlib): a compact `🧾` receipts line under each ranked card in **both** ledgers — a two-axis evidence-depth gradient (corroboration tier off `distinct_domains`: 1 = single-source / 2 = corroborated / 3+ = well-corroborated, **caps at 3+**; freshness badge off the existing scoring recency decay: fresh / recent / aging / undated) — plus a one-time legend above the ranked list framing receipts as evidence *depth*, not a verdict. The defining move (fourth headline running) was again a **$0 deep-research pass before locking the shape**: it grounded the tier ladder in the journalism two-source rule + NATO Admiralty scale and **capped it at well-corroborated** (arXiv 2501.01303: no trust gain 1→5 citations), and confirmed a binary "✓ verified" stamp is meaningless (citation-hallucination 11–57% even when links resolve) — which is the whole reason the receipt shows words, not a checkmark, with the floats kept in the detail lines. Final whole-branch review (Opus): **Ship, 9/10**, all six honesty invariants confirmed at source. **249 passed / 1 skipped.** **This CLOSES Step B** (PM4+D1 #103, D4 #104, E3 #105, D2 #106). Next arc: **Step C — validation gates**, which are cheap-ish and decide whether the bigger, first *paid-per-run* builds (E2, PM3) are worth it.

**One process lesson worth carrying (new this session):** the per-task review loop caught a defect *I* introduced — two test assertions in my plan collided with the legend's own `🧾`/"well-corroborated" text, and the implementer deformed the renderer logic (legend below the cards, asymmetric guards) to pass them, flagging it as DONE_WITH_CONCERNS. The right call was to reject that fix: the bug was my tests, not the design. **When an implementer contorts the design to pass a test, suspect the test.**

---

## Who you're working with + how to work

You're partnering with **Sean Winslow** in `code-brain` on the **fusion-discovery-council** tool — an evidence→idea discovery engine (gather real-URL user pain → multi-vendor OpenRouter Fusion panel → anti-fabrication gate → ranked, evidence-linked PM opportunities or Substack angles). Sean is a PM/creative technologist who wants the *why* and the *how*, values momentum, and wants a real thinking partner: brainstorm one question at a time, pressure-test ideas, be concise and direct. Use **TDD** + the superpowers skills (`brainstorming` → `writing-plans` → `subagent-driven-development`). **Surface cost before any paid run — Step C is the first arc with a real per-run OpenRouter cost, so this matters now.**

**The mission:** make this discovery council *the best it can be*. Step C is different in shape from Step B: these are **gates** — experiments that produce a **verdict**, not features that produce a PR. The verdict decides whether the next build proceeds. Don't build E2/PM3 before its gate clears.

### ⭐ Standing practice — research before you lock a design decision

This is a first-class part of how we work — it has now paid off directly on **four** consecutive headlines (PM4: multiplicative confidence; D4: the absence-of-evidence guardrail; E3: split dedup from MMR; D2: capped the corroboration ladder + words-not-checkmark). **Before committing to any design decision that has documented prior art, run a deep-research pass and let the evidence shape the design.**

- **When to research:** scoring/ranking, de-dup/MMR, similarity thresholds, time-decay, entailment/NLI gates, trust/provenance UX, **and evaluation method design** (this is squarely Step C — how to run a fair blind panel-vs-single comparison, how many raters/items, how to measure fabrication-resistance, what counts as a real signal vs sampling noise — all have prior art). If your gut says "someone has surely solved this," research it.
- **How:** the **`deep-research` skill** (`/deep-research` or the Skill tool) — **$0 on the Anthropic subscription**. Scope tightly to the decision.
- **Then:** fold findings into the spec/decision-doc **with citations**, and persist the synthesis to `vault/20_projects/research/YYYY-MM-DD-<topic>.md`. **Four exemplars to copy** (note the per-finding confidence + sources + a "How this changed the build" section): [`…/2026-06-29-opportunity-scoring-frameworks-research.md`](../../vault/20_projects/research/2026-06-29-opportunity-scoring-frameworks-research.md) (PM4), [`…/2026-06-29-whitespace-gap-map-presentation-research.md`](../../vault/20_projects/research/2026-06-29-whitespace-gap-map-presentation-research.md) (D4), [`…/2026-06-29-mmr-dedup-similarity-research.md`](../../vault/20_projects/research/2026-06-29-mmr-dedup-similarity-research.md) (E3), [`…/2026-06-29-receipts-provenance-ui-research.md`](../../vault/20_projects/research/2026-06-29-receipts-provenance-ui-research.md) (D2).
- **⚠️ Salvage lesson (still live):** the deep-research harness's adversarial-verify stage fans out ~40+ parallel agents and **can self-trip transient Anthropic-side rate-limiting**, aborting the final synthesis. It happened on D4 and again on D2 (both salvaged from transcripts; E3 completed clean). If it aborts, **don't blindly re-run** (~2.5M tokens burned hitting the same wall) — salvage the completed Search/Fetch/verify transcripts under `…/subagents/workflows/<run>/agent-*.jsonl` (or the `result.confirmed[]` in the task output), hand-vet, and write the note. Confirmed claims (3-0 / 2-0 votes) are solid; claims "killed" at 0-0 were *abstentions* from the rate-limit, not refutations.

## Read first (source of truth)

- **The master plan:** [`vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md`](../../vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md) — ranked idea table (§4), phased roadmap (§5), Opportunity Solution Tree (§8), North Star + metrics (§9), **red-team (§10)** — the panel-vs-single gate is red-team #4; the buyer test is #2/#3.
- **The pattern to mirror (research → spec → plan → TDD → final review → field report):** D2 spec [`docs/superpowers/specs/2026-06-29-discovery-d2-receipts-ui-design.md`](../superpowers/specs/2026-06-29-discovery-d2-receipts-ui-design.md) · plan [`docs/superpowers/plans/2026-06-29-discovery-d2-receipts-ui.md`](../superpowers/plans/2026-06-29-discovery-d2-receipts-ui.md) · **field report** [`docs/field-reports/2026-06-29-fusion-discovery-council-d2-receipts-ui-field-report.md`](../field-reports/2026-06-29-fusion-discovery-council-d2-receipts-ui-field-report.md). (A gate is lighter — it may produce a *decision doc* instead of a feature PR, but the research→verdict discipline is the same.)
- **The engine, for the panel-vs-single gate specifically:**
  - `tools/llm-council/council/discovery/tiers.py` — **the panel/judge config**: `TierConfig.panel` (tuple of Fusion `analysis_models`) + `.judge`. A single-model arm = a `TierConfig` whose `panel` is one strong model (e.g. `("anthropic/claude-opus-4.7",)`). This is the lever.
  - `tools/llm-council/council/discovery/fusion.py` — `fuse(*, api_key, bundle, tier, topic, timeout)` → `FusionResult`; `_build_body` reads `tier.panel`/`tier.judge`. This is the call to run twice (panel vs single) on the **same** evidence bundle.
  - `tools/llm-council/council/discovery/pipeline.py` — the orchestration; **note line ~146/158**: the saved session JSON persists only a *result summary*.
  - `tools/llm-council/council/discovery/verify.py` — the anti-fabrication gate (`verify_pain_points`), the fabrication-resistance you're trying to compare across arms.
- **⚠️ Load-bearing wrinkle the old prompt got wrong — verify it yourself first:** the saved bundles under `vault/20_projects/substack-studio/research/discovery/.discovery-sessions/*.json` are **result snapshots** (`topic, lens, tier, evidence_count, verified, dropped, cost_usd, blind_spots, contradictions, supplement`) — they do **NOT** persist `bundle.records` (the raw fetched evidence). So you **cannot re-FUSE a saved session directly.** For an apples-to-apples panel-vs-single comparison you need the *same* evidence bundle through both arms, which means either (a) a small pre-step to **persist `bundle.records`** (a sidecar cache — makes the gate cheap + repeatable at $0-gather, and is reusable infra), or (b) one fresh gather then two FUSE calls on that in-memory bundle. Decide with Sean; (a) is probably worth the tiny build.
- **The skill:** `.claude/skills/fusion-discovery-council/SKILL.md` (§2 stages, §4 FRAME, §6 gate).
- **Open items / spend:** `vault/00_inbox/tickets.md` (roadmap ticket) and the spend ledger `vault/health/council-spend-*.json` (discovery tagged `tool="discovery"`; caps **$10/day / $50/month**, shared file with council).

## Where things stand (after D2, merged #106)

- **Step A — harden — DONE** (#99, #101, #102).
- **Step B — sharpening — DONE & CLOSED:** PM4+D1 (#103), D4 (#104), E3 (#105), D2 (#106).
- **Step C — validation gates — THIS ARC.** Two cheap gates, run before the builds they gate. **Start with panel-vs-single-model** (gates E2, and E2 is the next build in Step D).
- **FIRST ACTION:** `git checkout main && git pull --ff-only`, then `gh pr list --state open` (expect none from discovery). Branch off clean `main`, e.g. `feat/discovery-stepc-panel-vs-single`.
- **Do NOT touch** Sean's uncommitted vault WIP (the `take-two-01-teach-the-model-your-hand/` files, substack-studio edits, `tickets.md`). **Keep the branch free of vault changes** (research/decision notes go in `vault/` but stay **unstaged** for Sean).

## TASK (this session) — `GATE →` panel-vs-single-model (red-team #4)

**The question this decides:** does the **full multi-vendor panel** actually produce better, *more fabrication-resistant* pain points than a **single strong model** on the same evidence — enough to justify the panel's cost and complexity? **This gates E2** (the panel self-preference fix) and the broader panel-config investment. If a single model is as good, E2/E5 panel work changes shape.

**Shape of the work (a gate, not a feature):**
1. **Brainstorm the protocol with Sean first** (one question at a time): which saved topic(s)/evidence to use; the single-model arm's model; the **blind-rating method** (Sean blind-rates? an LLM-judge blind? the `llm-council` skill as a blind panel?); the metric (fabrication-resistance via the gate's drop behavior + pain-point quality/usefulness); how many pain points / items to rate to beat sampling noise.
2. **`RESEARCH →`** the evaluation-method design before locking it — blind A/B protocol for LLM outputs, inter-rater needs, single-vs-ensemble quality findings, how to measure hallucination-resistance fairly. Tight scope. Fold into the decision doc with citations + a vault note (mirror the four exemplars).
3. **Resolve the evidence-bundle wrinkle** (above): persist `bundle.records` as a sidecar cache (small TDD build) OR fresh-gather once. Apples-to-apples requires the *same* bundle through both arms.
4. **Surface cost BEFORE running** — two FUSE calls (~$1–2 total at `standard` tier; confirm against `tiers.py`), plus one gather if not cached. **Check today's discovery spend in `vault/health/council-spend-*.json` against the $10/day cap first**, state the estimate, and get Sean's go before any paid call.
5. **Run** both arms on the same bundle (`fuse(... tier=panel_cfg ...)` vs `fuse(... tier=single_cfg ...)` where `single_cfg.panel` is one model), gate both, blind-rate.
6. **Verdict → decision doc** at `docs/superpowers/specs/` or `docs/decisions/` (a decision record, not a feature spec): the protocol, the numbers, the call, and **what it means for E2/E5**. Record the spend. This is the deliverable — a clear go/no-go for the panel, not necessarily new product code (beyond the bundle-cache enabler).

**Discipline:** TDD any code (the bundle cache, any single-model `TierConfig` plumbing); hermetic tests; `cd tools/llm-council && uv run pytest tests/ -q` (currently **249 passed, 1 skipped**) + `python3 scripts/validate.py`. Watch tests fail before implementing. Final whole-branch review only if there's a meaningful code diff.

## THEN (subsequent sessions — one step at a time, in order)

`GATE →` marks a cheap test/decision that must clear before the build it gates. `RESEARCH →` marks where a deep-research pass should precede the design.

### Step C — the other gate
- `GATE →` **PM3 longitudinal-signal**: re-run one past topic 2–4 weeks apart; does verified-pain frequency/intensity move beyond sampling noise? If not, PM3 is a memory/dedup feature, not a trend signal. (E3's dedup is the groundwork for a stable pain key.) **Run before PM3.** Note: this needs a real time gap between runs — set up the baseline run now, compare later, or use the oldest existing `.discovery-sessions` snapshots as a t0 if comparable.

### Step D — Defensibility (E1) + panel fix (E2)
- `GATE →` `RESEARCH →` **E1 cost model — DECIDE WITH SEAN (left open on purpose):** entailment verification as (a) **local NLI** (DeBERTa/Luna — $0, fits the fleet's local-model infra), (b) **OpenRouter LLM-judge per claim** (recurring API $ — the cost trap), or (c) **subscription agent** (interactive-only). Research should compare local-NLI options + citation precision/recall benchmarks. **Do NOT default to a paid per-claim approach.** (Lean: local NLI.)
- **E1 — entailment gate v2** for the **core VERIFY stage**: atomic-claim decomposition + NLI entailment (does the source *entail* the claim, not just contain a substring); keep substring as a cheap pre-filter; report citation precision + recall. `verify.py::quote_supported_at_url` is the documented single chokepoint to upgrade in place.
- **E2 — fix panel self-preference** (per the Step-C result): judge ≠ any panelist family; blind to authorship; swap evidence order.

### Step E — Phase 2 (evidence breadth + the longitudinal moat)
- **PM3 — pain-taxonomy persistence** (only if Step-C validated the signal): SQLite next to `vault/.vault-index.db`; stable pain key via **E3's dedup/similarity**; track frequency/intensity over time.
- **PM2/E4 — velocity + demand-intent channel:** `RESEARCH →` Google Trends (pytrends) slope + autocomplete/PAA as a **scoring** signal — never gate-evidence (watch source cost; prefer free/local).
- **D3 — discovery dashboard artifact:** run history, spend vs caps, pain-trend movement — a self-contained HTML view (model on `agent-fleet-observability/`).

### Step F — Phase 3 (map to paid; gated behind the engine being best-in-class)
- `GATE →` **buyer-conversation test (red-team #2/#3):** ~5 buyer conversations — does "verified, not hallucinated" rank above quantity/novelty as a purchase driver? Settle buyer identity (PM vs founder vs creator) before building the paid surface.
- **E5** decouple from one machine (config-driven paths, per-user spend) · **D5** interactive card triage (accept/reject/promote → shortlist) · **PM1** fabrication-gate scorecard (the brand) · **PM5** packaging (ledger §6 price points).

## Conventions (do not violate)

- **TDD** + verification-before-completion + a **final whole-branch adversarial review** for any meaningful code diff (dispatch the `Code Reviewer` agent on the most capable model against the feature diff). Verify with `cd tools/llm-council && uv run pytest tests/ -q` (currently **249 passed, 1 skipped**) and `python3 scripts/validate.py` (repo root). Watch each test fail before implementing.
- **Execution:** `brainstorming` → `writing-plans` → `subagent-driven-development` (fresh implementer per task, spec+quality review after each, broad final review at the end). Cheapest model for pure-transcription tasks, standard for logic/integration, most capable for the final review. **And: when an implementer contorts the design to pass a test, suspect the test** (this session's lesson).
- **Cost:** council/FUSE = OpenRouter, **real $** (discovery cap **$10/day / $50/month**; council caps separate but share the spend file). **Deep-research = subscription, $0.** **This arc has the first paid per-run item (the panel-vs-single FUSE calls) — surface the estimate and check the day's spend vs the cap before any paid call.**
- **Vault git (read carefully):** Per CLAUDE.md rule 8 the **Obsidian-Git plugin owns vault commits** — normally never `git add`/`commit` under `vault/`. **Sean is on the MacBook Pro this cycle (Obsidian-Git NOT running) and is mid-audit on vault files**, so **keep discovery branches free of vault changes** — write research/decision notes to `vault/20_projects/research/` but **leave them unstaged**; tell Sean what to commit. **Never weaken the privacy layer (rule 10):** never stage `prj-job-hunt-2026/`, `operating-models/`, `the-block/`, `_private/`, or `10_timeline/` paths; verify the staged set before every commit.
- **Branch/PR workflow:** feature branch → PR into `main` → Sean squash-merges. Keep PRs **small, focused, reviewable**. End commit messages with the `Co-Authored-By: Claude Opus 4.8 (1M context)` trailer and PR bodies with the Claude Code footer. Write a **field report** to `docs/field-reports/` at the end of a meaty session (mirror the D2 one).
- **Capture deferred work** as one-line `- ` bullets under `## Todo` in `vault/00_inbox/tickets.md` — but per the vault rule above, **flag it for Sean rather than committing it** this cycle.

## Still in Sean's court from D2 (vault commits he owns)
- Commit the D2 research note: `vault/20_projects/research/2026-06-29-receipts-provenance-ui-research.md` (written, left unstaged).
- Mark **D2 ✅ DONE** and **Step B complete** in the fusion-discovery roadmap ticket in `vault/00_inbox/tickets.md`; the next arc is **Step C** (panel-vs-single-model gate first).
