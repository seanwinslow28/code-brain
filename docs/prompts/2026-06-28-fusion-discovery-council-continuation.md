# Continuation — fusion-discovery-council + Pencil & Prompt discovery (2026-06-28)

Paste everything **below the divider** into a fresh **Claude Code session opened in `code-brain`** to pick up where we left off. Everything above the divider is context for you (Sean).

This session's headline decision: **backfill moves to the agent layer** (Claude Code's own web tools, on your Anthropic subscription, $0) instead of the in-CLI Exa/Brave version. Task 1 implements that. **Task 2 carries the full remaining roadmap** (Phases 1–3, audit-ordered, with the cheap test/decision `GATE →` points marked) — plan it end-to-end, execute one step at a time.

---

## Who you're working with + how to work

You're partnering with **Sean Winslow** in `code-brain` on two linked things: (1) the **fusion-discovery-council** skill/CLI (an evidence→idea discovery tool: gather real-URL user pain → multi-vendor OpenRouter panel → anti-fabrication gate → ranked idea ledger), and (2) **Pencil & Prompt**, his Substack, which consumes that tool's output for post topics. Sean is a PM/creative technologist who wants the *why* and the *how*, values momentum, and wants a real thinking partner: brainstorm one question at a time, pressure-test ideas, be concise and direct. Use **TDD** + **subagent-driven development** for code, and the superpowers skills. Surface cost before spending.

## Read first (source of truth)

- **The master plan:** `vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md` — the ranked idea ledger + phased roadmap (harden → sharpen → workflow → map-to-paid), the Opportunity Solution Tree (§8), the North Star + metrics (§9), the red-team (§10), the Week-0 conversion audit (§11, ~88% — red-team #1 refuted), and the E1–E6 items.
- **The skill + engine:** `.claude/skills/fusion-discovery-council/SKILL.md` and `tools/llm-council/council/discovery/` (pipeline.py, fusion.py, verify.py, backfill.py, gather/, tiers.py, __main__.py). Tests: `tools/llm-council/tests/discovery/`.
- **The substack synthesis:** `vault/20_projects/substack-studio/research/discovery/2026-06-28-discovery-synthesis-T2-T3-backlog.md`.
- **The editorial home:** `vault/20_projects/substack-studio/SERIES-COMMAND-CENTER.md` + `vault/20_projects/substack-studio/CLAUDE.md` (the §8 writing workflow + voice/privacy rules).
- **Open items:** `vault/00_inbox/tickets.md`.

## Where things stand (2026-06-28)

- **E6 BACKFILL shipped** (`b127aed`) and **crash-fixed + committed** (`ce6ffcc` — clamp + per-gap try/except; 155 tests pass).
- **6 discovery runs done** (4 first sweep + 2 `v2` rescues). **All four Pencil & Prompt topics are mine-able:** T1 iteration-tax, T2 accused-of-AI, T3 re-entry, T4 reproducibility. The synthesis + command center are updated (Take Two backlog rows #6/#7/#8 + the discovery-angle map).
- **Today's discovery spend ≈ $9.17 / $10** (note: the local ledger under-counts by ~$1.9 from the cost-recording hole below — so real spend is higher than recorded; the $10/day cap is less protective until that's fixed).

## TASK 1 (priority) — Rework BACKFILL to the agent layer

**Why:** the backfill should run on Sean's Anthropic **subscription** via the agent's own `WebSearch`/`WebFetch` (Claude Code), $0 marginal — NOT inside the Python CLI (which uses Exa/Brave + deterministic keyword extraction, off-subscription and lower-quality; "relevance: mixed"). The Cowork agent-driven backfill "worked really well." An agent doing intelligent search + read + synthesis is both cheaper and better, and it vets relevance natively.

Do:
1. **Flip the CLI `--supplement` default to OFF** so interactive runs don't trigger the deterministic Exa/Brave backfill. Keep `--supplement` working as opt-in (for a future headless/autonomous mode with no agent). **[Sean to confirm at session start: keep the CLI backfill as opt-in, or remove it entirely? Recommend keep — it's tested and serves the headless case; removal is fine if you'd rather simplify.]** TDD the default change; keep the existing tests green.
2. **Document the agent-driven backfill as the standard flow** in `SKILL.md` (revise the §2 stages + §3 flag note + §6 gate): after the council run(s) finish, the orchestrating agent reads each ledger's `## Blind-spot / Whitespace Map`, runs `WebSearch`/`WebFetch` on the *solution/evidence side* of each gap, and appends a `## Web Supplement (gap-fill)` section — keeping the SAME anti-fabrication discipline: every item is a **verbatim quote from a real fetched URL**, or it's rendered `still open — not filled`. Subscription-covered, $0 API.
3. **Update the run-prompt template** so a single Claude Code session does it all in one go: run the council CLI → agent reads blind-spot maps → agent backfills with its web tools → append the supplement section. (Model it on the manual Cowork pass that worked.)
4. **Cascade cleanup:** because the agent vets relevance natively, **close the E1-coupled-backfill cleanup ticket** (no deterministic gate to upgrade for backfill), and **downgrade the post-fuse cost-recording hole to LOW** (backfill was the only post-fuse network call, so the crash trigger is gone) — but still do the cheap structural fix (Task 2).
5. Update `CHANGELOG.md` + `tickets.md`. Do NOT touch the vault with git.

## TASK 2 — The full remaining roadmap (plan end-to-end; execute in this order)

The master plan is the idea ledger (§4 scored table, §5 phases). The 2026-06-28 conversion audit **re-ordered priorities: felt-value order is E6 (done) → PM4 → D4; E1 is the defensibility track.** Below is the complete remaining arc in execution order. Each step is its own session(s) — do **not** attempt it all at once. `GATE →` marks a cheap test/decision that must clear before the build it gates. The research is done (5 cited briefs + OST + metrics + red-team are in the ledger); what remains are builds, plus the named gates.

### Step A — Close the harden backlog (cheap; folds into the Task-1 session where natural)
- **H hygiene:** the `reviews` + `github` collectors clamp their query length (the 2026-06-28 long-topic 422s); stabilize HN under `--no-native-web`; `--segment` operator-char strip; OpenRouter request-shape live re-verify; surface the typed Fusion `failure_reason`.
- **Cost-recording fix:** thread post-fuse billed cost into a typed failure (mirror `FusionError.cost` → `DiscoveryFailed.cost_usd`) so a post-fuse crash records real spend, not $0 (~$1.9 under-counted 2026-06-28; verify on the OpenRouter dashboard + reconcile). Low after Task 1, but it's an invariant.

### Step B — Sharpen the output (the audit's #1 felt-value; Phase 1 minus E1)
- **PM4 + D1 — opportunity score + card redesign.** Replace the toy `intensity × (1+domains)` score with an ODI/RICE-style score (importance/underserved · reach from upvotes/authors · recency decay · corroboration), and redesign the card to **who · pain (their words) · evidence · size · why-now · proposed bet (riskiest assumption + cheapest test)**. Basis: ledger §9 + the output-frameworks research. No new API spend.
- **E3 — MMR dedup + recency/reach decay.** Near-duplicate collapse (MMR) + exponential time decay; feeds PM4's score. Tunable α; guard against recency over-correction.
- **D4 — whitespace map as hero output.** Lead the ledger with the blind-spot/whitespace map + "sharpen the next run" actions (it's the most-acted-on section AND the agent-backfill's input).
- **D2 — receipts UI.** Verification status inline per claim (✓ verified · corroborated-K-domains · recency badge).

### Step C — Validation gates (cheap; run before the builds they gate)
- **GATE → panel-vs-single-model test (red-team #4):** re-FUSE an existing session bundle with the full panel vs a single strong model; blind-rate. Decides E2/panel-config — keep the 4-model panel + fix self-preference, or collapse to single-model + a cheap cross-check and bank the cost. Run before E2.
- **GATE → PM3 longitudinal-signal test:** re-run one past topic 2–4 weeks apart; does verified-pain frequency/intensity move beyond sampling noise? If not, PM3 is a memory/dedup feature, not a trend signal — don't price a subscription on it. Run before PM3.

### Step D — Defensibility / moat track (E1) + the panel fix (E2)
- **GATE → E1 cost model (DECIDE WITH SEAN before implementing — left open on purpose):** entailment verification can run as (a) a **local NLI model** (DeBERTa/Luna — $0, fits the fleet's existing local-model infra), (b) an **OpenRouter LLM-judge per claim** (recurring API $ — the cost trap we escaped on backfill), or (c) the **subscription agent** (interactive-only). Evaluate the three, recommend with cost/quality/latency trade-offs, and get Sean's sign-off. **Do NOT default to a paid per-claim approach.**
- **E1 — entailment gate v2** for the **core VERIFY stage**: atomic-claim decomposition + NLI entailment (does the source *entail* the claim, not just contain a substring); keep substring as a cheap pre-filter; report citation precision + recall. Note: the agent-driven backfill (Task 1) vets relevance natively, so E1 is now for the core gate only.
- **E2 — fix panel self-preference** (per the Step-C test result): judge ≠ any panelist family; blind to authorship; swap evidence order.

### Step E — Phase 2 (evidence breadth + the longitudinal moat)
- **PM3 — pain-taxonomy persistence** (if Step-C validated the signal): SQLite next to `.vault-index.db`; stable pain key via embedding-cluster / canonical-title; track frequency/intensity over time (the recurring-value moat).
- **PM2/E4 — velocity + demand-intent channel:** Google Trends (pytrends) slope + autocomplete/PAA, as a **scoring** signal — never gate-evidence (watch the cost of the source; prefer free/local).
- **D3 — discovery dashboard artifact:** run history, spend vs caps, pain-trend movement, re-open — a self-contained HTML view (model on the agent-fleet-observability pattern).

### Step F — Phase 3 (map to paid; gated behind the engine being best-in-class)
- **GATE → buyer-conversation test (red-team #2/#3):** ~5 buyer conversations — does "verified, not hallucinated" rank above quantity/novelty as a purchase driver? Settle buyer identity (PM vs founder vs creator) before building the paid surface.
- **E5 — decouple from one machine** (config-driven paths, per-user spend, kill the "for Sean" hardcode); **D5 — interactive card triage** (accept/reject/promote → shortlist); **PM1 — fabrication-gate scorecard** (the brand); **PM5 — packaging** (ledger §6 has the price points). Autonomous/queued mode if daily use materializes.

## TASK 3 — Substack pipeline (separate workflow, when Sean wants)

All four topics are mine-able (see the synthesis doc). Write posts via the project's voice chain (`substack-value-engine` → `storytelling-architecture` → `writing-voice-modes` Sean Mode → `writing-critique` → `writing-humanity-pass`), per `substack-studio/CLAUDE.md` §8. Strongest-ready: **T2** (defend-the-human essay + a "standard of evidence / disclosure" Tool Drop), **T3** (Start Here sharpening + Take Two "keep the intern in a bounded role"). The flagship Take Two #1 ("teach the model your hand") is still capture-pending on Sean's Mac (image gen is firewalled in Cowork).

## Conventions (do not violate)

- **Cost:** council = OpenRouter (real $, ~$1–2/run, $10/day cap); **backfill = subscription ($0)** after Task 1. Never add a paid collector without threading its cost into spend recording.
- **TDD** + subagent-driven dev + verification-before-completion (run the suite; `python -m pytest tools/llm-council/tests/discovery/ -q`).
- **NEVER `git add`/`commit` the vault** — Obsidian-Git owns vault commits (CLAUDE.md rule 8). Commit code (`tools/`) normally via PR.
- **Capture deferred work** as one-line bullets under `## Todo` in `vault/00_inbox/tickets.md`.
