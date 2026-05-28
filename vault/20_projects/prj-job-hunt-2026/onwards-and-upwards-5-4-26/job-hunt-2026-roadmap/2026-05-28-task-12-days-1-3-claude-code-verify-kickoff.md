---
type: kickoff-prompt
project: prj-job-hunt-2026
parent_task: task-12-judge-layer
target: claude-code-cli
created: 2026-05-28
ai-context: "Kickoff prompt for Claude Code to verify the Judge Layer Days 1-3 artifacts authored in Cowork, fix small issues, commit + tag when green. Sean copy-pastes this verbatim into Claude Code from ~/Code-Brain/code-brain."
---

# Claude Code kickoff prompt — Task 12 Days 1-3 verification

> Copy everything between the `===` lines below into Claude Code (run from `~/Code-Brain/code-brain`).

---

```
===

You're picking up a verification task on Task 12 (Judge Layer Retrofit) of my
job-hunt-2026 roadmap. In a Cowork session earlier today (2026-05-28), an
agent authored the entire infrastructure layer of the judge module in one
sitting — Days 1-3 of a 9-day plan. The agent could not execute Python from
the sandbox (broken venv symlink), so all static checks passed but live
pytest + ruff are pending. You are the first agent to actually execute the
code on real hardware.

The full session handoff is at
vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-28-task-12-days-1-3-handoff.md
— READ THIS FIRST. It has the verification commands, the commit message, the
file map, and the "interview answers this artifact unlocks" section.

I want you to:

  1. Read the handoff doc end-to-end before touching anything.
  2. Run the 6-command verification block from the handoff doc, in order.
  3. Fix small issues if they surface (typos, missing imports, lint nits,
     pytest fixture naming collisions, off-by-one constants). DO NOT refactor
     the design — the architecture is council-locked per the roadmap.
     If you're about to change anything bigger than a 5-line edit or you
     have to delete or rename a top-level symbol, STOP and ask me.
  4. If everything passes (judge tests green, full suite green, ruff clean,
     repo validator green), commit using the pre-written commit message in
     the handoff doc § "Commit message", then tag judge-layer-v0.0.1-infra.
     Do NOT push — I'll push manually after I've eyeballed the commit.
  5. Report back with a structured pass/fail summary (template below).

CONTEXT YOU NEED TO KNOW

  Repo:               ~/Code-Brain/code-brain
  Working dir:        ~/Code-Brain/code-brain/agents-sdk
  Venv:               .venv (activate via `source .venv/bin/activate`)
  Python:             3.13 (from the venv)
  Pydantic:           2.12.5 (installed via google-genai, now promoted to
                      explicit dep in pyproject.toml)
  PyYAML:             6.0.3
  Test framework:     pytest, conftest patterns at tests/conftest.py
  Test count baseline: ~550 existing tests across the existing suite. After
                      this PR: ~624 (550 + 74 new). Zero regressions expected.
  Convention:         Run pytest with `PYTHONPATH=. pytest tests/` from
                      agents-sdk/ (NOT from repo root). This matches every
                      other agent's test invocation in CLAUDE.md.

  Important: the validator at scripts/validate.py from the REPO ROOT
  (not agents-sdk) is the v3.30.1-baseline gate — ≤60 warnings / 0 errors.
  The judge module is pure Python with no new vault paths, so it shouldn't
  add warnings.

WHAT YOU'RE LOOKING AT

  New files (8 production, 3 test):
    agents-sdk/lib/judge/__init__.py        (46 lines)
    agents-sdk/lib/judge/schema.py          (244 lines, Pydantic v2)
    agents-sdk/lib/judge/policy.py          (251 lines, dataclass + YAML)
    agents-sdk/lib/judge/judge.py           (505 lines, evaluate() + HTTP)
    agents-sdk/policies/substack_drafter.yaml  (104 lines, 4 rules)
    agents-sdk/tests/test_judge_schema.py   (300 lines, 24 tests, 5 classes)
    agents-sdk/tests/test_judge_policy.py   (356 lines, 26 tests, 5 classes)
    agents-sdk/tests/test_judge_evaluate.py (533 lines, 24 tests, 7 classes)

  Modified files (2 config nits):
    agents-sdk/pyproject.toml               (+1 dep: pydantic>=2.0,<3)
    agents-sdk/config.toml                  (+1 task_map row: judge_layer)

  Roadmap checkboxes flipped:
    vault/.../2026-05-06-unified-roadmap.md  Task 12 Steps 1, 2, 3 → [x]
    + new Status banner at top of Task 12

  Existing tests/test_judge_runner.py at tests/test_judge_runner.py is
  pre-existing — it tests the skill-optimizer's judge_runner, NOT my new
  lib.judge module. Different concept entirely. No collision.

DESIGN INVARIANTS YOU MUST PRESERVE (council-locked, do not touch)

  1. The 8 fields on ActionProposal are exactly: intended_action,
     target_surface, evidence_used (Optional), authorization_basis,
     expected_consequence, rollback_path (Optional), exposure_level,
     human_review_required. Removing or renaming a field is architectural.
  2. The 5 Outcome values are exactly: ALLOW, BLOCK, REVISE, ESCALATE,
     JUDGE_UNAVAILABLE. The 5th is load-bearing — it makes judge
     unavailability a named observable state.
  3. evaluate() NEVER raises. All exception paths return JudgeDecision
     with outcome=JUDGE_UNAVAILABLE. This is the fail-open contract.
  4. The model is allowed to emit only 4 outcomes (the 5th is set by
     evaluate() itself). _validate_parsed_outcome enforces this.
  5. substack_drafter.yaml has exactly 4 rules with the 4 canonical ids
     (rule_a_unverifiable_claim_named_person,
     rule_b_block_attribution_requires_citation,
     rule_c_voice_mode_drift,
     rule_d_publish_verb_at_top_level). The integration test
     TestRealSubstackDrafterPolicy will fail if you "improve" by adding a
     5th rule — and that's by design; any 5th rule needs a dashboard
     panel update at the same PR.
  6. config.toml's judge_layer = { model = "gemma4:e4b", machine =
     "mac_mini" } reuses the same model as inbox_triage to avoid a cold
     load. Don't switch the model unless gemma4:e4b is somehow unavailable
     on Mac Mini — and even then, ask me first.

LIKELY FAILURE MODES TO WATCH FOR

  - Pydantic v2 enum-equality: with use_enum_values=True, comparing
    decision.outcome to Outcome.ALLOW directly might not work — the tests
    compare to the string "ALLOW" instead. If a test fails on this kind
    of comparison, fix the assertion (compare to the string), NOT the
    schema config.
  - Path resolution in lib/judge/judge.py _call_router(): config_path is
    Path(__file__).parent.parent.parent / "config.toml". If that resolves
    wrong (somehow), the function falls through to JudgeTransportError
    which the test stubs cover — but a real run would fail. Smoke-import
    test from the handoff doc catches this.
  - The _JSON_OBJECT_RE regex in lib/judge/judge.py only handles one level
    of nested {}. If a model emits deeply nested JSON in production,
    parsing fails and we hit the retry loop. Tests don't cover this case
    on purpose — it's documented as a known limitation for v0.1.0.
  - Test isolation: tests should NOT touch the real
    agents-sdk/policies/substack_drafter.yaml (except the
    TestRealSubstackDrafterPolicy class which is integration-by-design).
    All other policy tests use tmp_path. If a test writes to the real
    policies dir, that's a bug — fix the test, not the loader.
  - asyncio interaction: judge.py's _call_router uses asyncio.run() like
    substack_drafter.py. If tests run under pytest-asyncio (which is set
    to asyncio_mode="auto" in pyproject.toml), make sure no test
    accidentally tries to async-call evaluate() — it's a sync function.

REPORT-BACK TEMPLATE (use this verbatim at the end)

  ## Verification — Task 12 Days 1-3

  **Verdict:** PASS | PARTIAL | FAIL

  **Verification commands run:**
    [list each command + exit code + key output line]

  **Test counts:**
    - Judge tests:     <N> passed, <N> failed, <N> skipped
    - Full suite:      <N> passed, <N> failed (regressions vs baseline: <N>)
    - Ruff:            clean / <N> warnings
    - validate.py:     <N> warnings, <N> errors

  **Fixes applied (if any):**
    [enumerate each fix as: file:line — what changed, why]

  **Anything I should know:**
    [surface anything you noticed that isn't a bug but is worth mentioning —
    e.g., a test that's slow, a comment that's misleading, a stale TODO]

  **Commit + tag status:**
    [committed as <sha> with tag judge-layer-v0.0.1-infra | NOT COMMITTED
    because: <reason>]

  **Next step recommendation:**
    [open the next Cowork session for Day 5 ledger writer | fix <X> first |
    surface for human review]

START NOW. Don't ask me clarifying questions until you've at least read the
handoff doc end-to-end — the answer to most questions is in there.

===
```

---

## Why this prompt is shaped the way it is (for Sean — not for Claude Code)

**It briefs like a colleague who just walked in.** Claude Code starts fresh with no memory of the Cowork session. The first paragraph names the context (Days 1-3 verification of an artifact authored elsewhere), the constraints (the original author couldn't execute Python), and the deliverable (PASS/FAIL + commit-when-green).

**It points at the handoff doc as canonical.** Rather than duplicating the verification commands inline (which would invite Claude Code to skip reading the handoff), it tells Claude Code to read the doc first. The commit message in the handoff doc is the one Claude Code should use verbatim — keeps a single source of truth for the artifact provenance.

**It names design invariants explicitly.** Claude Code sometimes "improves" code by refactoring. The 6 numbered invariants make every council-locked decision a tripwire — if Claude Code violates one, it has to consciously override a named constraint, which it won't do without surfacing.

**It names likely failure modes.** Pydantic v2 enum equality, path resolution, regex coverage, test isolation, asyncio interaction — these are the five places a verification run could legitimately reveal a real bug. If something breaks at one of these surfaces, Claude Code has the context to fix it cleanly. If something breaks elsewhere, that's surprising and Claude Code should surface before patching.

**It gates the commit on green tests.** "Commit when green, do not push, report back" — that gives you the final eyeball before anything lands publicly. Tagging without pushing is harmless and preserves the artifact's lineage if you do push later.

**It gives a structured report-back template.** Free-text reports are hard to scan. The template forces Claude Code to surface the four pieces of information you actually need (verdict, fixes, surprises, next step) in a predictable shape.

## What to do if the prompt comes back FAIL

If Claude Code reports back with PARTIAL or FAIL:

1. **Read the "Fixes applied" section first.** Anything Claude Code patched is now live in the working tree, uncommitted. You'll want to eyeball those diffs before deciding whether the fix is right.
2. **If the fix is wrong** (e.g., Claude Code tried to "improve" by simplifying a fail-open path), revert with `git checkout -- <file>` and open a new Cowork session pointing at the specific failure.
3. **If the fix is right** but more issues surfaced, you can either: (a) re-run this same prompt to keep iterating, or (b) open a Cowork session if the issue is architectural rather than a typo.
4. **If Claude Code surfaced something non-blocking** ("there's a stale TODO comment in policy.py"), that's a follow-up not a stop-ship.

## When this prompt SHOULD come back PASS

Realistic expectations: ~85% chance of clean pass first try. The static checks I ran in Cowork caught every AST + YAML + import-resolution issue I could see from there. The 15% risk is Pydantic v2 runtime-only behavior (enum equality, model_validate edge cases) that doesn't surface until pytest actually runs. If you hit a Pydantic-syntax issue, the fix is usually a 2-line test assertion change — Claude Code can handle that without escalation.
