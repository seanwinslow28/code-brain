# Continuation — fusion-discovery-council, E1 entailment-gate BUILD (next session)

Paste everything **below the divider** into a fresh **Claude Code session in `code-brain`**. Above the divider is context for you (Sean).

**What's already done (2026-06-30):** E1 is fully designed and planned — only the TDD build remains.
- **Spec** (approved): `docs/superpowers/specs/2026-06-30-discovery-e1-entailment-gate-design.md`
- **Plan** (6 TDD tasks, ready to execute): `docs/superpowers/plans/2026-06-30-discovery-e1-entailment-gate.md`
- **Research** (5-angle deep-research synthesis): `vault/20_projects/research/2026-06-30-citation-entailment-nli-verification-research.md`
- **Branch already exists:** `feat/discovery-e1-entailment-gate` (off `main`), holding the spec + plan commits.
- **Decisions locked with Sean:** local NLI in-process (`cross-encoder/nli-deberta-v3-small` int8 ONNX, no server → no asleep-host failure mode); optional dependency with graceful substring-only fallback; hermetic tests via an injected scorer.

**Also shipped this session (context):** Task A (Sonar cost integrity + review-site fan-out) = **PR #110**, awaiting Sean's squash-merge; PM3 t0 baseline seeded (paid $1.85, bundle frozen at `vault/20_projects/research/.discovery-sessions/pm3-t0-ai-coding-assistants-2026-06-30.json`, t1 re-run ticketed ~2026-07-21). Field report: `docs/field-reports/2026-06-30-fusion-discovery-council-followups-pm3-e1-field-report.md`.

---

You're partnering with **Sean Winslow** in `code-brain` on **fusion-discovery-council**. Sean is a PM/creative technologist who wants the *why* and the *how*, values momentum, and wants a real thinking partner. Use **TDD** and the superpowers skills. **Surface cost before any paid run** (E1 itself is $0 — local NLI).

## YOUR TASK: execute the E1 build plan
**The design and plan are done and approved — do NOT re-brainstorm.** Go straight to execution.

1. **FIRST:** `git checkout feat/discovery-e1-entailment-gate` (it already has the spec + plan). Confirm with `git log --oneline -3` (you should see the E1 plan + spec commits on top of `main`'s E2 commit `0b0366e`). If PR #110 (Task A) has merged to `main` since, `git rebase main` — E1 touches `verify.py`/new `nli.py`/`pipeline.py` session-JSON, disjoint from Task A's gather files, so expect a clean rebase.
2. Capture the test baseline: `cd tools/llm-council && uv run pytest tests/ -q` (note the count; E1 only ADDS tests + an optional `scorer` param, so the baseline must stay green throughout).
3. **Execute** `docs/superpowers/plans/2026-06-30-discovery-e1-entailment-gate.md` task-by-task via **superpowers:subagent-driven-development** (fresh subagent per task, two-stage review) or **executing-plans**. The plan has complete code for all 6 tasks.
4. **The two load-bearing risks the plan calls out — keep them front of mind:**
   - **Recall-safety invariant:** the substring pre-filter may only ever ADD an accept, NEVER reject. Every substring-miss must fall through to NLI. A reviewer should be able to confirm this by reading the cascade.
   - **`_ENTAILMENT_IDX` correctness:** the 3-logit label order for `nli-deberta-v3-small` must be confirmed against the model card `id2label` (Task 4 note + Task 6 step 7). A wrong index silently inverts the gate. The skip-marked real-model test catches it ONLY once the model is installed — so run `scripts/install_nli_model.sh` and the integration test before the PR if at all possible.
5. **Build discipline:** TDD (watch each test fail first); hermetic suite (no model download in CI — Tasks 1-3,5 use the injected `FakeScorer`); update SKILL.md §6 + CHANGELOG (Task 6); **final whole-branch adversarial review** (Code Reviewer, most capable model) before the PR. Branch → PR → Sean squash-merges.

## Conventions (do not violate)
- **TDD** + verification-before-completion + final adversarial review. `cd tools/llm-council && uv run pytest tests/ -q` and `python3 scripts/validate.py`. Suspect the test when an implementer deforms the design to pass it.
- **Cost:** E1 is **$0** (local NLI). Council/FUSE/Sonar = real $ if you run discovery (cap $10/day / $50/month, shared `vault/health/council-spend-*.json`) — surface + check before any paid call.
- **Vault git:** keep the branch free of vault changes; research/notes → `vault/`, left unstaged; never weaken the privacy layer. Commit trailer `Co-Authored-By: Claude Opus 4.8 (1M context)`; PR footer the Claude Code line. Field report to `docs/field-reports/` at the end.
- **Capture deferred work** as one-line `- ` bullets under `## Todo` in `vault/00_inbox/tickets.md`.

## Read first (source of truth)
- Plan: `docs/superpowers/plans/2026-06-30-discovery-e1-entailment-gate.md` (the build).
- Spec: `docs/superpowers/specs/2026-06-30-discovery-e1-entailment-gate-design.md` (the why + decisions).
- Research: `vault/20_projects/research/2026-06-30-citation-entailment-nli-verification-research.md`.
- The chokepoint: `tools/llm-council/council/discovery/verify.py::quote_supported_at_url`. Tests in `tools/llm-council/tests/discovery/`.

## THEN (subsequent sessions)
- PM3 t1 re-run + verdict (~2026-07-21, ticketed) → then PM3 pain-taxonomy persistence.
- PM2/E4 demand-intent scoring; D3 discovery dashboard; Step F (Phase 3, gated) buyer-conversation test.
- Master plan: `vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md`.
