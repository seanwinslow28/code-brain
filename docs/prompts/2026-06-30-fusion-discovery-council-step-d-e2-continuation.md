# Continuation — fusion-discovery-council, Step D: E2 panel self-preference fix (next session)

Paste everything **below the divider** into a fresh **Claude Code session opened in `code-brain`** to continue the roadmap. Everything above the divider is context for you (Sean).

**What just shipped (2026-06-30):** **Step C — panel-vs-single-model gate (red-team #4)** is DONE. A controlled dual-fuse experiment (same 46-record evidence bundle, same judge, only `analysis_models` varied) blind-rated by the variance council returned a clear verdict: **the 4-model Fusion panel beats a single strong model on all four criteria at only an ~8% cost premium → E2 is GO.** It also shipped reusable infra: `EvidenceBundle.to_dict/from_dict` (freeze a bundle to disk; PM3's groundwork) + an `experiments/` harness (gather-once → dual-fuse → blind-rate). Spend $2.77. **263 passed / 1 skipped, validator PASS.** Final review: Ship-with-fixes 8/10, all invariants confirmed. This sits on branch **`feat/discovery-stepc-panel-vs-single-gate`** — **unmerged, no PR yet** (see FIRST ACTION). Decision record: `vault/20_projects/research/2026-06-30-panel-vs-single-model-gate.md`. Field report: `docs/field-reports/2026-06-30-fusion-discovery-council-stepc-panel-vs-single-gate-field-report.md`. **Step B is fully on main** (PM4+D1 #103, D4 #104, E3 #105, D2 #106).

**Two process lessons worth carrying (recent):**
1. **When an implementer contorts the design to pass a test, suspect the test** (D2: my plan's assertions collided with the legend's own text; the fix was the tests, not the design).
2. **Verify subagent claims against git + test ground truth, especially on slow async runs** (Step C: a fix-wave subagent emitted a misleading "completed/deferred" message while still running 181s; the commit was actually correct, but only confirmed by checking git/tests, not the summary).

---

## Who you're working with + how to work

You're partnering with **Sean Winslow** in `code-brain` on the **fusion-discovery-council** tool — an evidence→idea discovery engine (gather real-URL user pain → multi-vendor OpenRouter Fusion panel → anti-fabrication gate → ranked, evidence-linked PM opportunities or Substack angles). Sean is a PM/creative technologist who wants the *why* and the *how*, values momentum, and wants a real thinking partner: brainstorm one question at a time, pressure-test ideas, be concise and direct. Use **TDD** + the superpowers skills (`brainstorming` → `writing-plans` → `subagent-driven-development`). **Surface cost before any paid run.**

**The mission:** make this discovery council *the best it can be*. The panel gate just proved the panel is worth its cost; **E2 makes the panel's *judging* trustworthy** by removing the self-preference confound the gate flagged (the judge + one rater were Anthropic-family). E2 is now de-risked and greenlit — it's a build, not a gate.

### ⭐ Standing practice — research before you lock a design decision

Five consecutive headlines have each turned on a **$0 deep-research pass before locking the shape** (PM4 multiplicative confidence · D4 absence-of-evidence guard · E3 dedup≠MMR split · D2 capped corroboration ladder · and at the meta level the Step-C spec, which caught that old bundles don't persist evidence). **Before committing to any design decision with documented prior art, run a deep-research pass and let the evidence shape the design.**

- **E2 has deep prior art** — LLM-as-judge **self-preference / self-enhancement bias**, **position/order bias**, and the standard debiasing toolkit (separate judge family, blind authorship, swap/randomize order, multi-judge panels). Research it before locking the mechanism.
- **How:** the **`deep-research` skill** (`/deep-research` or the Skill tool) — **$0 on the Anthropic subscription**. Scope tightly.
- **Then:** fold findings into the spec **with citations**, persist the synthesis to `vault/20_projects/research/YYYY-MM-DD-<topic>.md`. **Five exemplars to copy** (per-finding confidence + sources + a "How this changed the build" section): `2026-06-29-opportunity-scoring-frameworks-research.md` (PM4) · `…-whitespace-gap-map-presentation-research.md` (D4) · `…-mmr-dedup-similarity-research.md` (E3) · `…-receipts-provenance-ui-research.md` (D2) · `2026-06-30-panel-vs-single-model-gate.md` (the Step-C decision record).
- **⚠️ Salvage lesson (still live):** the deep-research harness's verify stage fans out ~40+ agents and **can self-trip transient Anthropic-side rate-limiting**, aborting final synthesis (hit D4 and D2; E3 clean). If it aborts, **don't blindly re-run** (~2.5M tokens wasted) — salvage the completed transcripts / `result.confirmed[]` (3-0 & 2-0 votes are solid; 0-0 "kills" were rate-limit *abstentions*, not refutations) and hand-write the note.

## Read first (source of truth)

- **The master plan:** [`vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md`](../../vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md) — ranked ideas (§4), phased roadmap (§5), OST (§8), North Star/metrics (§9), red-team (§10). E2 is the panel-self-preference fix; the buyer test is red-team #2/#3.
- **The Step-C verdict that greenlit E2:** the decision record above + the field report `docs/field-reports/2026-06-30-fusion-discovery-council-stepc-panel-vs-single-gate-field-report.md` (read the "Confound checked" + "Honest limits" sections — they define exactly what E2 must neutralize).
- **The pattern to mirror (research → spec → plan → TDD → final review → field report):** any recent pair, e.g. D2 spec [`docs/superpowers/specs/2026-06-29-discovery-d2-receipts-ui-design.md`](../superpowers/specs/2026-06-29-discovery-d2-receipts-ui-design.md) + plan, or the Step-C spec/plan (`docs/superpowers/specs/2026-06-30-discovery-stepc-panel-vs-single-gate-design.md`).
- **The engine — E2 touches the FUSE judge:**
  - `tools/llm-council/council/discovery/tiers.py` — **the lever you control directly:** `TierConfig.judge` (currently `anthropic/claude-opus-4.7` at standard/deep) and `.panel` (which *includes* `anthropic/claude-opus-4.7` at standard). **That judge-shares-family-with-a-panelist is the exact self-preference risk the gate flagged.**
  - `tools/llm-council/council/discovery/fusion.py` — `_build_body` sends `model = tier.judge` + `fusion.analysis_models = tier.panel` to the **opaque `openrouter:fusion` tool** (`tool_choice: required`). **Load-bearing unknown:** the fusion tool runs the panel and feeds their outputs to the judge *internally* — we do **not** obviously control whether the judge sees model attribution or in what order. So "blind authorship / swap order" may NOT be reachable through the fusion tool. Verify what `openrouter:fusion` exposes before designing.
  - `FUSION_SCHEMA.md` (same dir) — the confirmed request/response shape.
- **The skill:** `.claude/skills/fusion-discovery-council/SKILL.md` (§2 stages, §6 gate). **Spend:** `vault/health/council-spend-*.json` (discovery caps $10/day / $50/month, shared file).

## FIRST ACTION (state reconciliation — do this before anything)

The Step-C panel-gate work is **complete but unmerged** on `feat/discovery-stepc-panel-vs-single-gate`, with **no open PR**. Decide with Sean:
1. `git checkout feat/discovery-stepc-panel-vs-single-gate && git log --oneline -8` to confirm (verdict commit `c86a6fd` on top; vault notes committed at `407e96a`).
2. **Open a PR for it into `main`** (`gh pr create`), let Sean squash-merge, then `git checkout main && git pull --ff-only`. **E2 must branch off a `main` that contains Step C** — it builds on the same FUSE path and you want the experiment harness + `EvidenceBundle` serializer in your base.
3. `gh pr list --state open` (expect none otherwise). Branch off the merged `main`, e.g. `feat/discovery-e2-judge-debias`.
4. **Do NOT touch** Sean's uncommitted vault WIP (`take-two-01-…`, substack-studio edits). Keep the E2 branch free of vault changes (research note → `vault/`, left **unstaged** for Sean).

## TASK (this session) — E2: fix panel self-preference

**Why now:** the Step-C gate proved the panel is worth its cost *but* flagged a plausible Anthropic-affinity confound (judge = `claude-opus-4.7`, panel includes `claude-opus-4.7`, and an Anthropic rater). E2 removes that confound so the panel's pain-point clustering is demonstrably authorship-blind, not self-preferring.

**`RESEARCH →` before locking the mechanism (tight):** LLM-as-judge **self-preference/self-enhancement bias** + **position/order bias** + the debiasing toolkit — *concretely*: does separating the judge's model family from the panel measurably reduce self-preference? what's the evidence on position-swap / authorship-blinding / multi-judge aggregation? Fold into the spec with citations + a vault note (mirror the five exemplars).

**The load-bearing design fork to brainstorm with Sean (think before you build):**
- **(a) Minimal, in-arch:** set `tier.judge` to a **non-panelist family** (e.g. a Gemini or GPT judge over the multi-vendor panel), so no model grades its own family. Cheap, ships today, directly kills the flagged confound. But the fusion tool may still hide authorship/order, so this only addresses *self-preference*, not *position bias*.
- **(b) Fuller, more control:** if `openrouter:fusion` won't expose authorship/order, replace it with a **panel-then-blind-judge** pipeline we control — run panel models, strip model attribution, randomize finding order, then judge — so blinding + order-swap become real. More work, bigger surface, needs its own gate. **Don't default to this without evidence it's worth it** (the gate showed cross-lineage agreement already mitigates the confound somewhat).
- Likely right answer: **(a) now** (judge-family separation, a `tiers.py` change + a re-run sanity check), and only escalate to **(b)** if research says position bias is large *and* the fusion tool truly can't be blinded. Decide with Sean; surface the cost of any paid re-run (a verification FUSE is ~$1–2 — check the day's spend vs the $10/day cap first).

**Build discipline:** TDD; hermetic tests (no paid calls in the suite — assert on config/prompt construction, not live FUSE). If E2 is the (a) judge-family change, add a test that the standard/deep `TierConfig.judge` family ∉ `TierConfig.panel` families, and document the rationale. Run `cd tools/llm-council && uv run pytest tests/ -q` (currently **263 passed, 1 skipped**) + `python3 scripts/validate.py`. Update SKILL.md + CHANGELOG. Final whole-branch adversarial review (Opus) before PR. If you do a paid verification re-run, record spend and capture the before/after in the field report.

## THEN (subsequent sessions — one step at a time, in order)

`GATE →` = a cheap test/decision that must clear before the build it gates. `RESEARCH →` = a deep-research pass should precede the design.

### Step C — the remaining gate (parallel; needs a time gap)
- `GATE →` **PM3 longitudinal-signal:** re-run one past topic 2–4 weeks apart; does verified-pain frequency/intensity move beyond sampling noise? If not, PM3 is a memory/dedup feature, not a trend signal. **Set up the t0 baseline run now** (persist the bundle via the new `EvidenceBundle.to_dict`), compare later. Gates PM3.

### Step D — Defensibility (E1)
- `GATE →` `RESEARCH →` **E1 cost model — DECIDE WITH SEAN (left open on purpose):** entailment verification as (a) **local NLI** (DeBERTa/Luna — $0, fits the fleet's local-model infra), (b) **OpenRouter LLM-judge per claim** (recurring API $ — the cost trap), or (c) **subscription agent** (interactive-only). Research local-NLI options + citation precision/recall benchmarks. **Do NOT default to a paid per-claim approach.** (Lean: local NLI.)
- **E1 — entailment gate v2** for the **core VERIFY stage:** atomic-claim decomposition + NLI entailment (does the source *entail* the claim, not just contain a substring); keep substring as a cheap pre-filter; report citation precision + recall. `verify.py::quote_supported_at_url` is the documented single chokepoint to upgrade in place.

### Step E — Phase 2 (evidence breadth + the longitudinal moat)
- **PM3 — pain-taxonomy persistence** (only if its gate validated the signal): SQLite next to `vault/.vault-index.db`; stable pain key via **E3's dedup/similarity**; track frequency/intensity over time. Needs **production evidence persistence** first (deferred follow-up below).
- **PM2/E4 — velocity + demand-intent channel:** `RESEARCH →` Google Trends (pytrends) slope + autocomplete/PAA as a **scoring** signal — never gate-evidence (watch source cost; prefer free/local).
- **D3 — discovery dashboard artifact:** run history, spend vs caps, pain-trend movement — a self-contained HTML view (model on `agent-fleet-observability/`).

### Step F — Phase 3 (map to paid; gated behind the engine being best-in-class)
- `GATE →` **buyer-conversation test (red-team #2/#3):** ~5 buyer conversations — does "verified, not hallucinated" rank above quantity/novelty as a purchase driver? Settle buyer identity (PM vs founder vs creator) before building the paid surface.
- **E5** decouple from one machine · **D5** interactive card triage · **PM1** fabrication-gate scorecard · **PM5** packaging (ledger §6 price points).

### Loose follow-ups (small; surfaced 2026-06-30, in `tickets.md`)
- **Sonar cost-integrity leak:** `gather/sonar.py` bills ~$0.02/run unrecorded, contradicting the "every collector is FREE" docstring — thread the billed cost into recorded spend, or document it as a known fixed line item.
- **Production evidence persistence:** wire `EvidenceBundle.to_dict/from_dict` into the live pipeline (persist each run's raw evidence). Groundwork for PM3 + cheap re-FUSE; deferred until PM3 is greenlit.
- **Review-sites under-yield** (existing LOW): Brave collapses the OR'd multi-`site:` query in `gather/reviews.py`; fan out to N single-`site:` queries.

## Conventions (do not violate)

- **TDD** + verification-before-completion + a **final whole-branch adversarial review** (dispatch the `Code Reviewer` agent on the most capable model against the feature diff). Verify with `cd tools/llm-council && uv run pytest tests/ -q` (currently **263 passed, 1 skipped**) and `python3 scripts/validate.py` (repo root). Watch each test fail before implementing.
- **Execution:** `brainstorming` → `writing-plans` → `subagent-driven-development` (fresh implementer per task, spec+quality review after each, broad final review at the end). Cheapest model for transcription, standard for logic/integration, most capable for the final review. **Suspect the test when an implementer deforms the design to pass it; verify subagent claims against git + tests, not their summary.**
- **Cost:** council/FUSE = OpenRouter, **real $** (discovery cap **$10/day / $50/month**; council caps separate but share the spend file). **Deep-research = subscription, $0.** Surface the estimate + check the day's spend vs the cap before any paid call (E2 may need one verification FUSE).
- **Vault git (read carefully):** Per CLAUDE.md rule 8 the **Obsidian-Git plugin owns vault commits** — normally never `git add`/`commit` under `vault/`. **Sean is on the MacBook Pro this cycle (Obsidian-Git NOT running) and is mid-audit on vault files**, so keep discovery branches free of vault changes — write notes to `vault/20_projects/research/` but **leave them unstaged** unless Sean explicitly says to commit them; tell him what to commit. **Never weaken the privacy layer (rule 10):** never stage `prj-job-hunt-2026/`, `operating-models/`, `the-block/`, `_private/`, or `10_timeline/`; verify the staged set before every commit.
- **Branch/PR workflow:** feature branch → PR into `main` → Sean squash-merges. Keep PRs small, focused, reviewable. End commit messages with the `Co-Authored-By: Claude Opus 4.8 (1M context)` trailer and PR bodies with the Claude Code footer. Write a **field report** to `docs/field-reports/` at the end of a meaty session.
- **Capture deferred work** as one-line `- ` bullets under `## Todo` in `vault/00_inbox/tickets.md` — but per the vault rule, flag it for Sean rather than committing it unless he says otherwise.

## Already handled this session (no action needed)
- D2 + Step-C research/decision notes committed to the Step-C branch (`407e96a`); `tickets.md` updated: Step B ✅ complete, Step C panel gate ✅ done (E2 = GO), + the two follow-ups above.
- **Open question for Sean:** open the PR for the Step-C branch so E2 branches off a Step-C-inclusive `main`? (Recommended — see FIRST ACTION.)
