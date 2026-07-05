# Spec — Step C Validation Gate: Panel-vs-Single-Model (fusion-discovery-council)

**Date:** 2026-06-30
**Roadmap item:** Step C `GATE →` panel-vs-single-model (red-team #4). Decides whether **E2** (panel self-preference fix) is worth building.
**Cost class:** paid (OpenRouter, ~$1.8–2.4 real). Surface preflight + get explicit go before any paid call.

## 1. The question this gate answers

Does the 4-model Fusion panel (`opus-4.7 + gpt-5.5 + gemini-pro + grok-4.3`) produce **materially better pain points** than one strong model alone (`opus-4.7`)? If a single model ties the panel on blind rating, the panel's extra cost and the self-preference complexity (E2) aren't earning their keep — E2 becomes no-go and `quick`/single-model tiers look more attractive. If the panel wins clearly, E2 is justified.

## 2. Experimental control

Hold everything constant except **panel breadth**:

- **Same evidence bundle** — gather once, freeze to disk, fuse both arms over the identical bundle.
- **Same judge** — `anthropic/claude-opus-4.7` clusters in both arms (varies only what it clusters *over*).
- **Same tier knobs** — `standard` config, `max_tool_calls=5`, same `max_cost_per_run`.
- **Vary only** `fusion.analysis_models`:
  - **Arm A (panel):** `("anthropic/claude-opus-4.7", "openai/gpt-5.5", "~google/gemini-pro-latest", "x-ai/grok-4.3")`
  - **Arm B (single):** `("anthropic/claude-opus-4.7",)`

This isolates *panel breadth* as the only independent variable. FUSE is pre-lens, so lens (pm/substack) is irrelevant — the comparison is at the pain-point-clustering layer, before framing.

**Topic:** reuse the richest recent real topic — *"artists, writers, and designers who say AI is a slot machine … and who have stopped chasing prompts in favor of building a repeatable system they can trust"* (prior standard run: 46 evidence records, 5 verified, $1.55). Representative, on-brand, known to yield signal. **n=1** by design (cheap gate); writeup flags that a second topic would harden a close verdict.

## 3. Components

### 3.1 `EvidenceBundle` serialization — `council/discovery/evidence.py`
Add `to_dict()`/`from_dict()` to `EvidenceBundle` (and `EvidenceRecord`). Round-trips records losslessly. This is the reusable primitive: freezing the gathered bundle to disk makes the dual-fuse reproducible and re-runnable for **$0** later, and is the snapshot groundwork the PM3 longitudinal gate will need. TDD'd, $0, hermetic. **Not** wired into the production pipeline session-write (no forced persistence on every run — out of scope; that's a PM3 decision).

### 3.2 Experiment harness — `tools/llm-council/experiments/panel_vs_single.py`
New `experiments/` directory (sibling to `council/`, `tests/`). A `click` CLI:
- Options: `--topic` (default = the slot-machine topic), `--tier standard`, `--single-model anthropic/claude-opus-4.7`, `--out <dir>` (default a timestamped dir under `experiments/runs/`), `--yes`, `--skip-budget-check` (hidden, test-only).
- **Preflight budget check** against the discovery cap (`DISCOVERY_DAILY_CAP=10`, `DISCOVERY_MONTHLY_CAP=50`) *before* any paid call; abort on `BudgetExceeded`.
- **Gather once** (real; Sonar ~$0.02) → save `bundle.json` via 3.1.
- **Fuse A** with the standard `TierConfig`; **Fuse B** with a derived `TierConfig` whose `panel=(single_model,)`, everything else identical (judge stays opus). Both over the frozen bundle.
- `record_spend(amount=fr.cost, tool="discovery", tag="discovery-experiment")` after **each** fuse so the cap stays honest even if arm B fails after arm A billed.
- Emit:
  - `arm-A.json`, `arm-B.json` — raw `FusionResult` pain points per arm (with model identity, for the writeup).
  - `blind-rating.md` — both pain-point sets relabeled **"Set 1" / "Set 2"**, order **deterministically shuffled** (seeded by a fixed constant so it's reproducible, not `random` which the workflow/runtime forbids — derive the swap from a hash of the topic string), model identities and arm labels stripped.
  - `key.json` — maps Set 1/Set 2 → arm A/B, kept separate so the rater stays blind.

Failure handling mirrors the pipeline: a `FusionError` carries `.cost`; record it before re-raising so no paid call goes unrecorded.

### 3.3 Council blind-rating
Generate a rating prompt file from `blind-rating.md` + fixed criteria:
- **Signal density** — fraction of pain points that name a specific, real, recent user frustration (not generic).
- **Evidence grounding** — quotes/URLs that concretely support each point.
- **Distinctness / dup-rate** — are the points non-overlapping, or near-duplicates padding the count?
- **Actionability** — could a PM/creator act on this as an opportunity?

Run `python -m council --profile variance --prompt-file <rating.md> --output <verdict.md> --tag panel-vs-single`. The chairman synthesis (4 mixed-lineage models cross-ranking) is the blind verdict: which set wins, on which criteria, and by how much. ~$0.15. Then **unblind** via `key.json` and record which arm the council preferred.

### 3.4 Writeup
- **Vault (Sean commits):** `vault/20_projects/research/2026-06-30-panel-vs-single-model-gate.md` — methodology, raw A/B, council verdict, Sean's spot-check, and the **decision: panel justified? → E2 go/no-go.** Mirror the research-note exemplar shape (per-finding confidence + sources + "how this changed the build/roadmap").
- **Vault ticket (Sean commits):** mark the gate done in the fusion-discovery roadmap ticket; record the verdict + E2 decision.
- **Tracked (Claude commits):** field report in `docs/field-reports/2026-06-30-fusion-discovery-council-stepc-panel-vs-single-gate-field-report.md`.

## 4. Cost (surfaced before any paid run)

| Item | Estimate |
|---|---|
| Gather (Sonar — billed but currently unrecorded; see §6) | ~$0.02 |
| Fuse A — full panel | ~$1.2–1.6 |
| Fuse B — opus alone | ~$0.4–0.6 |
| Council rating (variance) | ~$0.15 |
| **Total (recorded vs cap)** | **~$1.8–2.4** |

Against $10/day cap, **$0 spent today**. The harness prints the live preflight estimate; Claude stops for Sean's explicit go before the first paid call.

## 5. Testing

- `evidence.py` round-trip: `from_dict(to_dict(bundle)) == bundle` (records, order, all fields). Hermetic, $0.
- Harness unit tests with **injected fake `gather_fn`/`fuse_fn`** (the pipeline already supports DI) — assert: budget preflight runs first; both arms fuse over the *same* bundle object; `record_spend` called once per arm; blind-rating.md strips identity and key.json maps correctly; deterministic shuffle is stable for a given topic. No network, no spend.
- `cd tools/llm-council && uv run pytest tests/ -q` stays green (currently 249 passed, 1 skipped) + `python3 scripts/validate.py` at repo root.

## 6. Out of scope / follow-ups (capture as tickets for Sean)

- **Sonar cost-integrity leak:** `gather/sonar.py` calls OpenRouter (perplexity) and bills ~$0.02/run, but the cost is never read from the response and the gather module's docstring asserts "every collector is FREE." Real (tiny) unrecorded spend contradicting an in-code invariant. Separate fix.
- **Production evidence persistence** (every-run bundle snapshot) — deferred to the PM3 decision; this gate only persists its own experiment bundle.
- **Second topic** to harden a close verdict — run only if §3.3 result is ambiguous.

## 7. Conventions

TDD; verification-before-completion; final whole-branch adversarial review (`Code Reviewer` on the most capable model). Branch `feat/discovery-stepc-panel-vs-single-gate` → PR into `main` → Sean squash-merges. **Zero vault changes staged on this branch** — research note + ticket updates are written and left for Sean. Commit trailer `Co-Authored-By: Claude Opus 4.8 (1M context)`.
