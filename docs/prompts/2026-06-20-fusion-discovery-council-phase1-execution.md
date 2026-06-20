# Kickoff Prompt — Execute fusion-discovery-council Phase 1 (subagent-driven)

Paste everything inside the fenced block below into a fresh Claude Code session opened at the repo root (`/Users/seanwinslow/Code-Brain/code-brain`).

---

```
We're building a new skill called `fusion-discovery-council`: a multi-model, fresh-evidence
discovery research tool that mines real user pain points and frames them as ranked,
evidence-linked PM opportunities. The design and a complete 16-task TDD implementation plan
already exist. Your job this session is to EXECUTE Phase 1 of that plan, task by task, using
subagent-driven development.

START HERE — read these two files in full before doing anything else:
- Spec:  docs/superpowers/specs/2026-06-20-fusion-discovery-council-design.md
- Plan:  docs/superpowers/plans/2026-06-20-fusion-discovery-council.md   ← the source of truth for execution

EXECUTION METHOD:
- Invoke the `superpowers:subagent-driven-development` skill and follow it exactly.
- Dispatch ONE fresh subagent per task (Tasks 1–16, in order). Each subagent implements only
  its task using strict TDD (write failing test → run it red → minimal code → run it green →
  commit), then returns. Do a two-stage review between tasks before moving on.
- Every task in the plan already contains the exact files, complete code, exact test code, exact
  run commands, and expected output. Do NOT redesign — implement what's written. If a task's code
  genuinely doesn't work, fix minimally and note why.

WHERE THE WORK LIVES:
- You should already be on branch `feat/fusion-discovery-council` (the spec + plan are committed
  there). Confirm with `git branch --show-current`; if not, `git checkout feat/fusion-discovery-council`.
- All skill code lives in a NEW subpackage `tools/llm-council/council/discovery/` that REUSES the
  existing council `client.py` + `budget.py` spine. Run all Python/test commands from
  `tools/llm-council/`. Test command: `uv run pytest tests/discovery/ -v`.

NON-NEGOTIABLE CONSTRAINTS (from the plan's Global Constraints — enforce in every task):
- Python floor stays `>=3.10`. Do not add a second HTTP client or a second spend file.
- Shared spend file `vault/health/council-spend-*.json`; discovery runs are tagged `tool="discovery"`
  with INDEPENDENT caps: $10/day, $50/month, plus per-run caps quick $0.50 / standard $1.50 /
  deep $4.00. `deep` confirms cost before running.
- FABRICATION GATE IS SACRED: every pain point in the final ledger must trace to a quote whose URL
  exists in the gathered evidence bundle. Untraceable → dropped or marked `unverified`. Never soften.
- The skill must NEVER run `git add` against the `vault/` directory (CLAUDE.md rule 8 — Obsidian-Git
  owns vault commits). This applies to the skill's runtime behavior, not your task commits.
- Verified OpenRouter model IDs are listed in the plan; Sonar models are `tools=False` and belong in
  Stage 1 gather only, never in the Fusion panel.

TASK 4 IS SPECIAL (a live spike): it makes one real OpenRouter Fusion API call to capture the exact
request/response JSON shape, then writes `council/discovery/FUSION_SCHEMA.md`. It needs
`OPENROUTER_API_KEY` in `tools/llm-council/.env` and network access. Run it for real if the key is
present. If the live call 4xx's, correct the request shape per the error and document the working
shape — then make sure Task 5's `_build_body` matches what you captured. If no key/network is
available in this environment, STOP and tell me rather than fabricating the schema.

DEFINITION OF DONE for Phase 1:
- All 16 tasks complete; `cd tools/llm-council && uv run pytest -v` is fully green (new discovery
  suite + all pre-existing council tests, no regressions).
- `python3 scripts/validate.py` passes at repo root (new SKILL.md loads).
- The skill is invocable end-to-end: `cd tools/llm-council && uv run python -m council.discovery
  "obsidian sync" --lens pm --tier quick --output /tmp/test-ledger.md` produces an idea ledger whose
  every pain point has a traceable evidence URL. (Doing one real run is optional and will spend a few
  cents — ask me before spending; the test suite already proves the logic with mocks.)
- CHANGELOG.md + CLAUDE.md (and README.md if it has a skill table) updated per Task 16.

DO NOT:
- Do not build Phase 2 (extended review/GitHub/intent/Q&A/trend collectors) or Phase 3 (the
  `substack` lens) — they are deferred to follow-on plans.
- Do not merge to `main` or open a PR unless I explicitly ask. Stay on the feature branch.
- Do not weaken the budget caps, the fabrication gate, or the vault-commit rule.

When you finish all 16 tasks, give me a short summary: tasks completed, full test count + pass status,
the validate.py result, anything you had to deviate from in the plan (and why), and the exact command
to try a live run.
```

---

## Notes for Sean (not part of the paste)

- The fresh session must be opened on branch `feat/fusion-discovery-council`. If you open it on `main`, just tell that session to `git checkout feat/fusion-discovery-council` first (it's also in the prompt).
- Make sure `tools/llm-council/.env` has `OPENROUTER_API_KEY` (the same one llm-council uses) so Task 4's spike and any live run work. `EXA_API_KEY` (optional) enables the web collector at runtime; without it that collector returns empty and the suite still passes (it's mocked).
- Phase 1 is mostly pure-logic + mocked I/O, so it should run nearly free. The only real spend is Task 4's one tiny Fusion call (~cents) and any optional end-to-end live run.
- After Phase 1 lands and you've tried a real run, come back and I'll write the Phase 2 (extended sources) and Phase 3 (substack lens) plans against the now-real interfaces.
