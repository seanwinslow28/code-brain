# Field report — fusion-discovery-council Step D session: gather follow-ups + PM3 t0 seed + E1 spec/plan

- **Date:** 2026-06-30
- **Branches:** `feat/discovery-followups` (PR #110), `feat/discovery-e1-entailment-gate` (spec + plan)
- **Outcome:** the continuation prompt's full single-session target met — two follow-ups shipped, PM3 t0 seeded, E1 researched → decided → spec'd → planned (build handed to next session).

## What shipped

### Task A — gather follow-ups (PR #110, `feat/discovery-followups`)
1. **Sonar cost-integrity leak.** Sonar bills ~$0.02/run via OpenRouter `usage.cost` on every run, but the gather stage discarded it — the "every collector is FREE" invariant never covered Sonar, so the $10/day cap under-counted. Collectors now follow an explicit `list` (free) / `(records, cost)` (paid) contract; cost accumulates onto a new `EvidenceBundle.gather_cost_usd` and the pipeline folds it into recorded spend on every path. Review found (and I hardened) a latent serialization drop: `to_dict`/`from_dict` now persists the field — exactly the failure class PM3's bundle-freeze would have hit.
2. **Review-site fan-out.** Brave collapses an OR'd multi-`site:` query, so most review domains were never searched. Now fans out one single-`site:` query per domain (concurrent, per-domain-failure tolerant), round-robin-merges for diversity, dedups by URL, caps total fetches.
- TDD throughout; **278 passed, 1 skipped**; validator PASS; adversarial Code Reviewer **8/10** (both fixes verified correct, no deformed tests).

### Task B — PM3 t0 longitudinal seed
- Paid standard run on **"AI coding assistants"**: 93 evidence records, 8 verified / 2 dropped, **$1.85** (spend $2.59 → $4.43 of $10/day cap).
- t0 bundle frozen via `EvidenceBundle.to_dict` at `vault/20_projects/research/.discovery-sessions/pm3-t0-ai-coding-assistants-2026-06-30.json`. A one-off harness mirrored the CLI's budget-preflight + `record_spend` exactly (the live CLI doesn't persist the bundle yet — that's the deferred production-persistence follow-up).
- **Live validation bonus:** the t0 bundle captured `gather_cost_usd=$0.0298` — proof that Task A's Sonar threading AND the serialization hardening both work end-to-end in production.
- t1 re-run ticketed for ~2026-07-21.

### Task C — E1 entailment gate (research → decision → spec → plan)
- **$0 deep-research** (5 angles, ~30 sources) → synthesis at `vault/20_projects/research/2026-06-30-citation-entailment-nli-verification-research.md`.
- **Decisions with Sean:** local NLI **in-process** (`nli-deberta-v3-small` int8 ONNX, 173 MB, no server → no asleep-host failure mode); optional dependency + graceful substring-only fallback; hermetic tests via injected scorer.
- Spec + 6-task TDD plan committed on `feat/discovery-e1-entailment-gate`. Build handed to a fresh session via `docs/prompts/2026-06-30-fusion-discovery-council-e1-build-continuation.md`.

## What worked
- **Parallelizing the $0 deep-research in the background** while doing Task A's TDD — the E1 evidence (and a clean design direction) was ready the moment we turned to the cost-model decision. No idle wait.
- **The review caught a real latent gap** (serialization-drops-cost) that was *exactly* the failure mode the next task (PM3 bundle-freeze) would have triggered. Fixing it before PM3 ran de-risked the seed.
- **In-process ONNX** as the answer to the fleet's recurring "asleep local host" pain — the single most consequential research finding; it makes E1 both $0 and robust.

## Gotchas / notes for next time
- `load_dotenv()` from `tools/llm-council` does NOT walk up to the repo-root `.env` reliably — the harness had to load `ROOT / ".env"` explicitly. The key lives in the **repo-root** `.env` (len 73), not under `tools/llm-council`.
- The deep-research skill's parent agent returned before its angle children finished and **did not persist the synthesis note** — I wrote it from the angle agents' verified findings (which surfaced as background-task notifications in-session). If using `deep-research` for a persisted artifact, verify the file actually got written.
- E1's `_ENTAILMENT_IDX` (3-logit label order) is the one silent-failure risk — must be confirmed against the model card and exercised by the skip-marked real-model test once the model is installed.

## Open / deferred (all ticketed or in the continuation)
- E1 TDD build (next session, continuation prompt written).
- PM3 t1 re-run ~2026-07-21; then PM3 persistence + production evidence-persistence wiring.
- Sonar cost-integrity + review-fan-out tickets marked ✅ DONE (PR #110) in `tickets.md`.
