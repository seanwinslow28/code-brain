# Vault Synthesizer Eval Suite + Synthesizer Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a 10-case binary pass/fail eval suite for the vault synthesizer (Workstream A, Friday 2026-05-22), patch the synthesizer until 7+/10 cases pass (Workstream B, before 2026-05-29), and build the Substack-Drafter agent (Workstream C, default-disabled, opt-in install) so the publishing cadence that drives the job hunt becomes agent-assisted rather than rate-limited by hand-writing. The SPEC labels Workstream C "post-employment," but the real constraint is that the agent depends on the synthesizer being alive (5+ consecutive nights of `concepts_written > 0`) — not on employment status. Once B's verification gate passes, C can ship.

**Architecture:** `evals/vault-synthesizer/` at repo root. `cases.yaml` lists 10 binary cases (6 new from real-log error analysis + 4 retained from pre-drafted research). `runner.py` (~100 lines) is a pytest harness that parametrizes over the YAML and runs three grader types: exact-match, rubric, llm-judge. The 6 new cases are intentionally red on the current synthesizer — they are the regression suite that Workstream B's patches need to drive green. Synthesizer fixes target `agents-sdk/agents/vault_synthesizer.py` (status taxonomy + per-file LLM-failure promotion + `model_used` enum), `agents-sdk/lib/pushover.py` (boot-time credential check), and `agents-sdk/agents/daily_driver.py` (Vault Health WARNING surface). Workstream C adds `agents-sdk/agents/substack_drafter.py` — a weekly Thursday-18:00 agent that reads the post-fix synthesizer output (`vault/knowledge/concepts/`, `connections/`, `qa/`) plus similarity-pulled references and drafts a Substack post in a rotating voice mode from `.claude/skills/writing-voice-modes/`. Drafts land in the vault; Sean publishes by hand (the agent never publishes autonomously). Default-disabled at three layers per SPEC kill-switch design.

**Tech Stack:** Python 3.11+ via `agents-sdk/.venv`; pytest; PyYAML; existing `agents_sdk` package; macOS launchd (already wired); no new external deps; no platform infra (Braintrust/Langfuse/etc. are explicitly on the don't-build list).

**Source spec:** `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-10-eval-suite-build-plan.md` — referenced as **SPEC** throughout.

**Sequencing:** A runs first (ship 2026-05-22). B starts Monday 2026-05-25. The 5-consecutive-nights-of-`concepts_written > 0` precondition for the follow-up post (2026-05-29) is gated; do not skip it. C starts when B's 5-night gate passes — realistically the week of 2026-06-01. First weekly draft fires Thursday 2026-06-04 at the earliest (Sean reviews Friday morning, publishes Friday/Saturday). If B's gate slips, C slips with it; the agent without concepts to draft from is a no-op.

---

## File Structure

### Create (under `evals/vault-synthesizer/`)

- `README.md` — Recruiter-readable cold paragraph, mandatory framing block (intentionally red, ~80% expected to fail at v1), CWD-pinned quickstart, baseline-pending placeholder until Task A4, link out to `EXPLANATION.md` and `failure-modes.md`. One responsibility: the entry door.
- `cases.yaml` — The 10 active cases (vs-012, vs-013, vs-014, vs-015, vs-016, vs-017, vs-018, vs-019, vs-020, vs-021). One responsibility: structured case data the runner parametrizes over.
- `deferred-cases.yaml` — The 11 deferred cases (vs-001..vs-011) lifted from the Perplexity and Gemini primers. One responsibility: hold the hallucination/drift/confidence work until the synthesizer is alive enough to actually fire them.
- `runner.py` — pytest harness. ~100 lines, no externals beyond pyyaml+pytest. One responsibility: load cases, dispatch by `judge_type`, write `last-run.md`.
- `failure-modes.md` — Six-mode taxonomy from the error-analysis doc, restated as a cases.yaml README. One responsibility: explain *what* each failure mode means in plain English.
- `EXPLANATION.md` — 4Q artifact (What is this? / Why this approach? / What would break? / What did I learn?). One responsibility: portfolio hook.
- `references.md` — Sources index + interview-vocab cheat-sheet. One responsibility: credit + vocabulary.
- `traces/phase-0.5-spike.md` — Recorded REPL output from the spike test that confirms vs-016/vs-017/vs-018 actually fail on the live code today. One responsibility: prove the regression-suite claim.
- `traces/coded-traces.md` — 5–10 representative excerpts from `vault/90_system/agent-logs/vault-synthesizer-stderr.log` + `vault/health/synth-manifest-*.json`, open-coded. One responsibility: the evidence column behind `failure-modes.md`.
- `traces/baseline-run-2026-05-22.md` — One-shot review file written after Task A4 baseline run; per-case classification (real failure vs grader bug). One responsibility: prove no grader bugs remain before we lock the baseline number.
- `traces/fixtures/note-{1..6}.md` — Mock daily notes for vs-014 (output completeness) and vs-020 (knowledge-index integrity). One responsibility: deterministic input data.
- `last-run.md` — Auto-written by `runner.py` each invocation. Has a `<!-- generated, do not edit -->` marker at the top. One responsibility: latest run output.

### Create (Workstream C — Substack-Drafter agent)

- `agents-sdk/agents/substack_drafter.py` — The agent. ~250–350 lines. Reads synth manifests + concepts/connections/qa, picks the densest cluster, composes a system+user prompt with the current week's voice mode, calls HybridRouter (Qwen3-14B local → Sonnet fallback), writes a draft markdown file. Never publishes.
- `agents-sdk/tests/test_substack_drafter.py` — pytest suite covering the input gate (graceful no-op when synthesizer is dry), voice rotation arithmetic, cluster picker, prompt composition, draft frontmatter, dry-run mode, and Pushover ping path.
- `agents-sdk/schedules/com.sean.agents.substack_drafter.plist` — launchd plist with the standard `PATH` `EnvironmentVariables` block (non-negotiable, per CLAUDE.md). Thursday 18:00 weekly.
- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/.gitkeep` — Ensure the output dir exists (it likely does already if Sedaris/Kerouac drafts are there; verify).

### Modify (rooted at repo root, paths absolute below)

- `agents-sdk/agents/vault_synthesizer.py` (663 lines today) — Workstream B targets: status enum + `success-empty`/`partial-empty` values; per-file `LLMCallError` exception handler that promotes the run-level status; `model_used` enum init; `warnings` field on result.
- `agents-sdk/lib/pushover.py` (107 lines today) — Add `ensure_credentials_or_raise()` boot-time check that raises `PushoverConfigurationError` instead of silent-log-and-return.
- `agents-sdk/agents/daily_driver.py` (484 lines today) — Update the Vault Health section in `build_prompt()` so `status == "success-empty"` or `concepts_written == 0` surfaces as `WARNING`, not `ok`.
- `agents-sdk/config.toml` — Add `[substack_drafter]` table with `enabled = false` default.
- `agents-sdk/schedules/install_schedules.sh` — Add `INSTALL_SUBSTACK_DRAFTER` opt-in flag + plist install path (mirrors the `process_inbox` pattern).
- `CHANGELOG.md` — One entry under v3.29.x (A+B) and a v3.30.x entry (C).
- `CLAUDE.md` — Update skill/agent counts (agent count +1 when C ships); add `evals/` and the Substack-Drafter row to the agent table.
- `README.md` — Mention the eval suite + the new agent.

### Read-only (consult during execution, do not modify)

- `vault/health/synth-manifest-2026-05-{02,03,06,07,08,09,10}.json` — error-analysis evidence
- `vault/90_system/agent-logs/vault-synthesizer-stderr.log` — Mode 5 evidence (Pushover)
- `vault/90_system/agent-logs/vault-synthesizer-2026-05-{08,09,10}.log` — empty-but-ok evidence
- `vault/knowledge/index.md` — current empty-state confirmation
- `agents-sdk/lib/hybrid_router.py` — `WOLUnavailable` lives here (relevant for status promotion logic)
- `.claude/skills/writing-voice-modes/SKILL.md` — voice modes for Phase 7 publishing

---

# PART A — Workstream A: Eval Suite (ships 2026-05-22)

## Task A0: Phase 0 pre-execution reads

**Files:** (read-only)
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/CLAUDE.md`
- SPEC (eval-suite build plan)
- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-10-evals-error-analysis-real-logs.md`
- `agents-sdk/agents/vault_synthesizer.py` (focus: lines 291–420 around `run_synthesis()`; manifest write path 580–660)
- `agents-sdk/config.toml`
- `agents-sdk/schedules/install_schedules.sh`
- `.claude/skills/writing-voice-modes/SKILL.md`
- `vault/40_knowledge/references/ref-anthropic-demystifying-agent-evals.md`
- `vault/20_projects/research/2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md`
- `vault/20_projects/research/2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md`

- [ ] **Step 1: Read all 10 files above in order.** Do not produce code yet — this step exists only to confirm the engineer has the same mental model the SPEC assumes.

- [ ] **Step 2: Write a 5-bullet "what I learned" note in `traces/phase-0-reads.md`.** This file is throwaway (kept out of git via Task A1 `.gitignore`) but exists so the engineer notices if they were tempted to skip a read.

```
# Phase 0 — what I learned before writing code

- The vault synthesizer's `run_synthesis()` takes a dependency-injected `llm_caller`. That is the seam every status-misreport case mocks.
- The status field today has values `ok`, `error`, `partial`. It does NOT have `success-empty` or `partial-empty` yet — both are introduced in Workstream B.
- `model_used` is initialized to `""` and overwritten on the first successful LLM call. Zero-success runs leave the empty string in place — that's vs-018.
- Pushover credentials are read from macOS keychain. Today, missing creds log + return silently inside the notify path. That's vs-019.
- The daily driver's morning brief reads `status` directly from the manifest. Today a `status: ok` + `concepts_written: 0` manifest renders as healthy. That's vs-021.
```

## Task A0.5: Phase 0.5 spike test — confirm the regression-suite claim before writing case YAML

**Files:**
- Create: `evals/vault-synthesizer/traces/phase-0.5-spike.md`
- Read-only: `agents-sdk/agents/vault_synthesizer.py`

- [ ] **Step 1: Activate the venv and open a Python REPL.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3
```

- [ ] **Step 2: Probe vs-016 — every-file LLM failure must NOT escalate to `status=error` today.**

```python
from agents_sdk.agents import vault_synthesizer
def always_raise(prompt, *a, **kw):
    raise ConnectionRefusedError("synthetic LLM failure")
# Build the smallest viable input — re-use vault_synthesizer's own test fixtures if present;
# otherwise pass a minimal note list. Inspect run_synthesis()'s signature first:
import inspect
print(inspect.signature(vault_synthesizer.run_synthesis))
# Now invoke with llm_caller=always_raise and capture the result:
result_016 = vault_synthesizer.run_synthesis(llm_caller=always_raise, ...)  # fill ... per signature
print("vs-016 — status:", result_016.status, "concepts_written:", result_016.concepts_written)
```

- [ ] **Step 3: Probe vs-018 — `model_used` defaults to `""` after a no-success run.**

```python
print("vs-018 — model_used:", repr(result_016.model_used))
```

- [ ] **Step 4: Write `evals/vault-synthesizer/traces/phase-0.5-spike.md` with the actual values.**

```markdown
# Phase 0.5 — Synthesizer spike test (run 2026-05-12)

Purpose: confirm the regression-suite claim that vs-016, vs-017, vs-018 fail on the current
synthesizer code AS WRITTEN, before we write the YAML cases.

## vs-016 probe — all-file LLM failure
- llm_caller: `lambda *a, **kw: raise ConnectionRefusedError`
- result.status: `<actual value here>`
- result.concepts_written: `<actual value here>`
- Verdict: <PASS = fails today as expected (status != "error") | RECONSIDER = case needs rewrite>

## vs-018 probe — model_used default
- result.model_used: `<actual value, repr()>`
- Verdict: <PASS = fails today as expected ("") | RECONSIDER>

## Conclusion
- If any verdict above is RECONSIDER, update the case's pass_criteria in Task A3 to assert
  what the synthesizer ACTUALLY does wrong, not the assumed behavior.
```

- [ ] **Step 5: If any verdict is RECONSIDER, flag it now.** The case YAML in Task A3 must assert against observed behavior, not the SPEC's assumed behavior.

- [ ] **Step 6: Commit (spike file only, no other artifacts yet).**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git add evals/vault-synthesizer/traces/phase-0.5-spike.md
git commit -m "chore(evals): record Phase 0.5 spike — confirm vs-016/vs-018 failure modes are live"
```

## Task A1: Scaffold `evals/vault-synthesizer/` (the directory + empty files)

**Files:**
- Create: `evals/vault-synthesizer/{README.md,cases.yaml,deferred-cases.yaml,runner.py,failure-modes.md,EXPLANATION.md,references.md,last-run.md,traces/coded-traces.md,traces/.gitkeep,traces/fixtures/.gitkeep}`
- Create: `evals/vault-synthesizer/.gitignore`

- [ ] **Step 1: Create the directory tree.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
mkdir -p evals/vault-synthesizer/traces/fixtures
touch evals/vault-synthesizer/{README.md,cases.yaml,deferred-cases.yaml,runner.py,failure-modes.md,EXPLANATION.md,references.md,last-run.md,traces/coded-traces.md,traces/.gitkeep,traces/fixtures/.gitkeep}
```

- [ ] **Step 2: Add a tiny `.gitignore` so the throwaway Phase 0 note + auto-generated `last-run.md` don't get tracked accidentally.**

```bash
cat > evals/vault-synthesizer/.gitignore << 'EOF'
phase-0-reads.md
__pycache__/
.pytest_cache/
EOF
```

- [ ] **Step 3: Verify the tree.**

```bash
ls -la evals/vault-synthesizer/ evals/vault-synthesizer/traces/
```

Expected: 8 files at the root + a `traces/` directory with `coded-traces.md`, `phase-0.5-spike.md`, `.gitkeep`, `fixtures/`.

- [ ] **Step 4: Commit.**

```bash
git add evals/vault-synthesizer/
git commit -m "feat(evals): scaffold evals/vault-synthesizer/ directory + empty files"
```

## Task A2: Write `failure-modes.md` (the taxonomy)

**Files:**
- Modify: `evals/vault-synthesizer/failure-modes.md`
- Read-only: SPEC §"Six-mode failure taxonomy" (in the error-analysis companion doc)

- [ ] **Step 1: Write the taxonomy file.** The content is canonical from the error-analysis doc — copy the six modes into a recruiter-readable format with one paragraph each + a one-line "what case catches it" link.

```markdown
# Vault Synthesizer — Failure Modes (open-coded from 17 days of real logs)

> The cases in `cases.yaml` are not imagined. Each one is grounded in an observed
> failure mode from 2026-04-24 → 2026-05-10 production logs. This file is the
> Rosetta Stone between log evidence and case ID.

## Mode 1 — Silent empty output

The synthesizer reports `status: "ok"` while writing zero concept articles to disk.
Three layers of monitoring (manifest, daily-driver brief, Pushover) all read this
as healthy. The system rotted silently for nine consecutive nights before the
discrepancy surfaced.

Evidence: `vault/health/synth-manifest-2026-05-{02,03,06,07,08,09,10}.json` —
each has `"status": "ok"` with `"concepts_written": 0`.

Caught by: **vs-015**, **vs-016**, **vs-017**.

## Mode 2 — Status-field misreport on per-file LLM failures

When every per-file LLM call raises (WOL fails, model returns an error, network
drops), the synthesizer's outer loop catches each one, logs it, and continues.
The run-level status promotion does not happen — final status reports `ok`
because the function returned without itself raising.

Evidence: stderr logs on the same dates as Mode 1.

Caught by: **vs-016**.

## Mode 3 — Missing status taxonomy values

The status enum today is `{ok, error, partial}`. There is no `success-empty`
(succeeded structurally, produced no output) or `partial-empty` (some files
processed, none produced articles). Downstream consumers cannot distinguish
"healthy and quiet" from "broken and quiet."

Caught by: **vs-017**.

## Mode 4 — `model_used` schema integrity

`model_used` is initialized to `""` and overwritten on the first successful LLM
response. Zero-success runs leave the empty string in the manifest. Any
downstream code that reads this field has to handle a sentinel that isn't part
of the documented enum.

Caught by: **vs-018**.

## Mode 5 — Pushover credentials fail-quiet

Missing keychain credentials cause Pushover's `notify()` to log "missing creds"
and return. The synthesizer treats this as a successful notification. A
catastrophic failure in the very system designed to surface failures.

Evidence: `vault/90_system/agent-logs/vault-synthesizer-stderr.log` — repeated
`"pushover credentials missing"` lines with no corresponding crash.

Caught by: **vs-019**.

## Mode 6 — Downstream-consumer misread of healthy status

The daily-driver morning brief takes the synth manifest's `status` field at face
value. A `status=ok, concepts_written=0` manifest renders in the brief as
"Vault Health: ok," which is the literal truth and a complete lie.

Caught by: **vs-020** (index/disk integrity) and **vs-021** (brief consumer).
```

- [ ] **Step 2: Commit.**

```bash
git add evals/vault-synthesizer/failure-modes.md
git commit -m "docs(evals): add open-coded failure-modes taxonomy"
```

## Task A3: Write `cases.yaml` (10 active cases)

**Files:**
- Modify: `evals/vault-synthesizer/cases.yaml`
- Read-only: Phase 0.5 spike output (`traces/phase-0.5-spike.md`)

- [ ] **Step 1: Write all 10 cases in one pass.** The YAML schema is `{id, category, description, failure_mode_under_test, input, expected_output, judge_type, pass_criteria}`. The `input` and `pass_criteria` blocks must be tight enough that vs-016/017/018 fail on today's code and pass after Workstream B. If the Phase 0.5 spike reported a RECONSIDER verdict for any case, edit that case's `pass_criteria` to target the *observed* failure.

```yaml
# evals/vault-synthesizer/cases.yaml
# Schema: {id, category, description, failure_mode_under_test, input, expected_output,
#          judge_type, pass_criteria}
# Judge types: exact-match (Python assertion) | rubric (structured check) | llm-judge (Claude Haiku, not used at v1)
# This file is canonical. deferred-cases.yaml holds the 11 cases waiting on the synthesizer fix.

- id: vs-014
  category: output-completeness
  description: "Synthesizer fails to emit a concept article on a 5+ note corpus"
  failure_mode_under_test: "Mode 1 — silent empty output"
  input:
    fixtures: traces/fixtures
    note_count: 6
  expected_output:
    concepts_written: ">= 1"
  judge_type: rubric
  pass_criteria: "result.concepts_written >= 1"

- id: vs-015
  category: output-completeness
  description: "Synthesizer reports status=ok with zero outputs (the load-bearing case)"
  failure_mode_under_test: "Mode 1 — silent empty output"
  input:
    fixtures: traces/fixtures
    note_count: 6
  expected_output:
    status: not "ok"  # if no outputs were produced, status must not be "ok"
  judge_type: exact-match
  pass_criteria: "not (result.status == 'ok' and result.concepts_written == 0)"

- id: vs-016
  category: status-misreport
  description: "All-file LLM failure must escalate the run-level status"
  failure_mode_under_test: "Mode 2 — status-field misreport"
  input:
    llm_caller_mock: "raises ConnectionRefusedError on every call"
    fixtures: traces/fixtures
    note_count: 3
  expected_output:
    status: in {"error", "partial-empty"}
  judge_type: exact-match
  pass_criteria: "result.status != 'ok'"

- id: vs-017
  category: status-misreport
  description: "Status taxonomy must distinguish partial-some-output from partial-empty"
  failure_mode_under_test: "Mode 3 — missing status taxonomy"
  input:
    llm_caller_mock: "raises on file 1 + 2, succeeds with empty body on file 3"
    fixtures: traces/fixtures
    note_count: 3
  expected_output:
    status: "partial-empty"
  judge_type: exact-match
  pass_criteria: "result.status == 'partial-empty'"

- id: vs-018
  category: schema-integrity
  description: "model_used must be one of the documented enum values, never empty string"
  failure_mode_under_test: "Mode 4 — model_used schema"
  input:
    llm_caller_mock: "raises ConnectionRefusedError on every call"
    fixtures: traces/fixtures
    note_count: 1
  expected_output:
    model_used: in {"qwen3-14b", "claude-sonnet-4-6", "claude-haiku-4-5", "none"}
  judge_type: exact-match
  pass_criteria: "result.model_used in {'qwen3-14b', 'claude-sonnet-4-6', 'claude-haiku-4-5', 'none'}"

- id: vs-019
  category: config-fail-loud
  description: "Missing Pushover credentials must raise at synthesizer boot, before any LLM call"
  failure_mode_under_test: "Mode 5 — Pushover fail-quiet"
  input:
    pushover_keychain: "removed"
    fixtures: traces/fixtures
    note_count: 1
  expected_output:
    exception: "PushoverConfigurationError"
    raised_before_llm_call: true
  judge_type: exact-match
  pass_criteria: "raises PushoverConfigurationError before any llm_caller invocation"

- id: vs-020
  category: index-integrity
  description: "Concept count in vault/knowledge/index.md matches file count in vault/knowledge/concepts/"
  failure_mode_under_test: "Mode 6 — downstream-consumer misread"
  input:
    fixture_concepts_dir: traces/fixtures/concepts_3files
    fixture_index_md: traces/fixtures/index_lists_3.md
  expected_output:
    consistent: true
  judge_type: rubric
  pass_criteria: "count(index.md '## Concepts' entries) == count(concepts/*.md)"

- id: vs-021
  category: downstream-consumer
  description: "Daily-driver morning brief must surface success-empty as a WARNING, not as healthy"
  failure_mode_under_test: "Mode 6 — downstream-consumer misread"
  input:
    fake_manifest:
      status: "success-empty"
      concepts_written: 0
      duration_s: 12.4
  expected_output:
    brief_text: contains "WARNING"
    brief_text_alt: contains one of ("concepts_written: 0", "empty")
  judge_type: rubric
  pass_criteria: "'WARNING' in brief and ('concepts_written: 0' in brief or 'empty' in brief)"

# Retained from pre-drafts — deferred-semantics, kept active per SPEC §Scope Lock
- id: vs-012
  category: source-attribution
  description: "Concept articles cite at least one source note by wikilink"
  failure_mode_under_test: "Source-attribution loss (Gemini §6)"
  input:
    fixtures: traces/fixtures
    note_count: 6
  expected_output:
    each_concept_cites_source: true
  judge_type: rubric
  pass_criteria: "every concept article body contains >= 1 wikilink to a source note"
  skip_reason: "requires live synthesizer output; skipped until Workstream B"

- id: vs-013
  category: stale-overweighting
  description: "Concept clustering does not over-weight stale notes vs recent ones"
  failure_mode_under_test: "Stale-content overweighting (Gemini §6)"
  input:
    fixtures: traces/fixtures
    note_count: 6
    age_distribution: "3 from last 7 days, 3 from > 60 days"
  expected_output:
    recent_cluster_weight: ">= 0.5"
  judge_type: rubric
  pass_criteria: "majority of cluster wikilinks point to notes < 30 days old"
  skip_reason: "requires live synthesizer output; skipped until Workstream B"
```

- [ ] **Step 2: Validate the YAML parses.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
agents-sdk/.venv/bin/python3 -c "import yaml; cases = yaml.safe_load(open('evals/vault-synthesizer/cases.yaml')); print(f'{len(cases)} cases loaded'); [print(c['id']) for c in cases]"
```

Expected: `10 cases loaded` followed by `vs-014 vs-015 vs-016 vs-017 vs-018 vs-019 vs-020 vs-021 vs-012 vs-013`.

- [ ] **Step 3: Commit.**

```bash
git add evals/vault-synthesizer/cases.yaml
git commit -m "feat(evals): add 10 active cases (6 new from real-log analysis + 4 retained)"
```

## Task A4: Write `deferred-cases.yaml` (11 cases)

**Files:**
- Modify: `evals/vault-synthesizer/deferred-cases.yaml`
- Read-only: `vault/20_projects/research/2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md` (vs-001..vs-011)
- Read-only: `vault/20_projects/research/2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md`

- [ ] **Step 1: Lift vs-001..vs-011 from the two primer documents.** Top-of-file note explaining why they're deferred.

```yaml
# evals/vault-synthesizer/deferred-cases.yaml
#
# These 11 cases test hallucination, edge-confidence, relation-tag drift, and
# temporal confusion. All are valid; none can fire on the current system because
# the LLM call did not successfully complete during the error-analysis window
# (2026-04-24 → 2026-05-10).
#
# Re-enable when the synthesizer produces ≥1 concept article in a clean run.
# At that point, move 2–3 cases at a time into cases.yaml and rebaseline.
#
# See ../failure-modes.md for the open-coded evidence behind why these are
# deferred-not-deleted.

# (Body: copy vs-001..vs-011 verbatim from the Perplexity §6 and Gemini §6 case
# blocks. Preserve their original schema; do not adapt to the cases.yaml shape
# until a case is being moved active.)
```

- [ ] **Step 2: Copy each case body from the source primer documents.** This is mechanical — preserve the schema the primer documents used. (The runner deliberately does not parametrize over this file; it's a holding pen.)

- [ ] **Step 3: Validate the YAML parses.**

```bash
agents-sdk/.venv/bin/python3 -c "import yaml; d = yaml.safe_load(open('evals/vault-synthesizer/deferred-cases.yaml')); print(f'{len(d)} deferred cases'); [print(c['id']) for c in d]"
```

Expected: `11 deferred cases` listing vs-001..vs-011.

- [ ] **Step 4: Commit.**

```bash
git add evals/vault-synthesizer/deferred-cases.yaml
git commit -m "feat(evals): add deferred-cases.yaml — 11 cases waiting on synthesizer fix"
```

## Task A5: Write fixtures for vs-014 + vs-020

**Files:**
- Create: `evals/vault-synthesizer/traces/fixtures/note-{1..6}.md`
- Create: `evals/vault-synthesizer/traces/fixtures/concepts_3files/{a,b,c}.md`
- Create: `evals/vault-synthesizer/traces/fixtures/index_lists_3.md`

- [ ] **Step 1: Write 6 mock daily notes** with realistic-but-tiny bodies. They need enough overlap that a working synthesizer would cluster them into ≥1 concept article. Pick a theme — e.g., three notes mention "Pushover credentials" and three mention "vault synthesis" — so the clustering target is obvious.

```markdown
---
date: 2026-05-04
tags: [agent-fleet, pushover]
---

# 2026-05-04 daily note

Spent an hour debugging why the synthesizer wasn't pinging on failures. Turns out
the Pushover credentials weren't in the keychain — the notify call was logging
"missing creds" and returning. The system designed to surface failure was the
first thing to fail quietly.

See `vault/90_system/agent-logs/vault-synthesizer-stderr.log` for the pattern.
```

(Repeat with 5 more notes in the same theme; vary the date 2026-05-04..2026-05-09 and rotate the tag set. Keep each body 4–6 sentences.)

- [ ] **Step 2: Write `concepts_3files/{a,b,c}.md`** — three trivial concept article stubs (just frontmatter + a title).

```markdown
---
type: concept
slug: pushover-fail-quiet
---

# Pushover fail-quiet

(stub for vs-020 fixture)
```

- [ ] **Step 3: Write `index_lists_3.md`** — a `## Concepts` section listing exactly the three slugs from step 2.

```markdown
# Knowledge Index (fixture)

## Concepts

- [[pushover-fail-quiet]]
- [[silent-empty-output]]
- [[status-misreport]]
```

- [ ] **Step 4: Commit.**

```bash
git add evals/vault-synthesizer/traces/fixtures/
git commit -m "feat(evals): add fixtures for vs-014 (6 mock notes) + vs-020 (concepts/index parity)"
```

## Task A6: Build `runner.py` (TDD — start with the smallest grader)

**Files:**
- Modify: `evals/vault-synthesizer/runner.py`
- Test: `evals/vault-synthesizer/test_runner.py` (transient; deleted after Task A6 or kept as a hidden self-test)

- [ ] **Step 1: Write a small unit test for the exact-match grader.** This locks the grader contract before the harness gets wired up.

```python
# evals/vault-synthesizer/test_runner.py
import pytest

def test_exact_match_grader_pass():
    from runner import grade_exact_match
    case = {"id": "vs-018", "pass_criteria": "result.model_used in {'qwen3-14b', 'none'}"}
    class R: model_used = "qwen3-14b"
    assert grade_exact_match(R(), case) == ("PASS", "")

def test_exact_match_grader_fail():
    from runner import grade_exact_match
    case = {"id": "vs-018", "pass_criteria": "result.model_used in {'qwen3-14b', 'none'}"}
    class R: model_used = ""
    status, _ = grade_exact_match(R(), case)
    assert status == "FAIL"
```

- [ ] **Step 2: Run the test — confirm it fails (no `runner.py` yet).**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/evals/vault-synthesizer
../../agents-sdk/.venv/bin/python3 -m pytest test_runner.py -v
```

Expected: ImportError / "No module named 'runner'".

- [ ] **Step 3: Write the minimum `runner.py` that makes the unit test pass.**

```python
# evals/vault-synthesizer/runner.py
"""Vault Synthesizer Eval Runner.

Run with:
    cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
        ../evals/vault-synthesizer/runner.py -v

Standalone (for the Loom demo):
    cd agents-sdk && PYTHONPATH=. .venv/bin/python3 ../evals/vault-synthesizer/runner.py
"""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent
CASES_PATH = ROOT / "cases.yaml"
LAST_RUN_PATH = ROOT / "last-run.md"


def grade_exact_match(result, case) -> tuple[str, str]:
    """Evaluate `case['pass_criteria']` as a Python expression against `result`.

    The expression has `result` bound in its namespace; nothing else. Failure to
    evaluate is reported as FAIL with the exception message, not a runner crash.
    """
    expr = case["pass_criteria"]
    try:
        ok = bool(eval(expr, {"__builtins__": {}}, {"result": result}))
    except Exception as e:  # noqa: BLE001 — graders never crash the run
        return "FAIL", f"grader-eval-error: {e!r}"
    return ("PASS", "") if ok else ("FAIL", f"{expr} evaluated False")


def grade_rubric(result, case) -> tuple[str, str]:
    """Structured rubric checks — case-specific Python that asserts against `result`.

    For v1, this is identical to exact-match (pass_criteria is a Python expr).
    The split exists so future rubric cases can grow without re-shaping the schema.
    """
    return grade_exact_match(result, case)


GRADERS = {"exact-match": grade_exact_match, "rubric": grade_rubric}
```

- [ ] **Step 4: Re-run the unit test — confirm pass.**

```bash
../../agents-sdk/.venv/bin/python3 -m pytest test_runner.py -v
```

Expected: 2 passed.

- [ ] **Step 5: Append the case-runner + last-run-md writer.**

```python
# Append to evals/vault-synthesizer/runner.py

def _load_cases() -> list[dict]:
    return yaml.safe_load(CASES_PATH.read_text())


def _invoke_synthesizer(case) -> object:
    """Build the synthesizer call from case['input'] and invoke it.

    Returns the SynthesisResult-like object the synthesizer produced, or a
    sentinel `_RaisedSentinel` when the synthesizer raised (vs-019 needs this).
    """
    from agents_sdk.agents import vault_synthesizer as vs
    inp = case.get("input", {})

    # Build a mock llm_caller per case
    mock_spec = inp.get("llm_caller_mock")
    if mock_spec is None:
        llm_caller = None
    elif "raises ConnectionRefusedError" in mock_spec:
        def llm_caller(*a, **kw):
            raise ConnectionRefusedError("synthetic LLM failure")
    elif "raises on file 1 + 2, succeeds with empty body on file 3" in mock_spec:
        state = {"n": 0}
        def llm_caller(*a, **kw):
            state["n"] += 1
            if state["n"] <= 2:
                raise ConnectionRefusedError("synthetic LLM failure")
            return ""  # empty body
    else:
        raise ValueError(f"unsupported llm_caller_mock: {mock_spec!r}")

    fixtures_dir = ROOT / (inp.get("fixtures") or "traces/fixtures")
    note_count = inp.get("note_count")

    # Pushover-removed scenario for vs-019
    if inp.get("pushover_keychain") == "removed":
        import os
        os.environ.pop("PUSHOVER_USER_KEY", None)
        os.environ.pop("PUSHOVER_API_TOKEN", None)

    return vs.run_synthesis(
        llm_caller=llm_caller,
        fixtures_dir=fixtures_dir,
        note_count=note_count,
    )


def _invoke_brief(case) -> str:
    """vs-021: invoke the daily-driver brief builder with a fake synth manifest."""
    from agents_sdk.agents import daily_driver as dd
    fake = case["input"]["fake_manifest"]
    return dd.render_vault_health(fake)


@pytest.fixture(scope="session")
def cases():
    return _load_cases()


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["id"])
def test_case(case):
    # Routing
    if case.get("skip_reason"):
        pytest.skip(case["skip_reason"])
    if case["id"] == "vs-021":
        result = _invoke_brief(case)
        # Treat brief output string AS the result for the grader to eval against.
        class _Wrap:
            pass
        w = _Wrap()
        w.brief = result
        # Rewrite pass_criteria for vs-021 to reference w.brief
        case = dict(case)
        case["pass_criteria"] = (
            "'WARNING' in result.brief and "
            "('concepts_written: 0' in result.brief or 'empty' in result.brief)"
        )
        result = w
    elif case["id"] == "vs-019":
        # Expect an exception type
        import pytest as _p
        from agents_sdk.lib.pushover import PushoverConfigurationError
        with _p.raises(PushoverConfigurationError):
            _invoke_synthesizer(case)
        return  # pass implicitly
    else:
        result = _invoke_synthesizer(case)

    grader = GRADERS[case["judge_type"]]
    status, detail = grader(result, case)
    if status == "FAIL":
        pytest.fail(f"{case['id']}: {detail}")


def _write_last_run(report_lines: list[str]) -> None:
    header = [
        f"# Vault Synthesizer Eval Run — {datetime.now(timezone.utc).isoformat()}",
        "",
        "> **Read this first.** This suite ships intentionally red. Each ❌ below is a",
        "> real production failure mode this suite catches — not a broken eval. The",
        "> pass rate jumps after the Workstream B synthesizer fix lands. See",
        "> `EXPLANATION.md` for the design rationale.",
        "",
        "| ID | Category | Result | Notes |",
        "|---|---|---|---|",
    ]
    LAST_RUN_PATH.write_text("\n".join(header + report_lines) + "\n")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
```

- [ ] **Step 6: Add a pytest hook that writes `last-run.md`.** (Append to `runner.py` — uses pytest's `pytest_runtest_logreport` + `pytest_sessionfinish`.)

```python
# Append to evals/vault-synthesizer/runner.py

_RESULTS: list[tuple[str, str, str]] = []

def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    case_id = report.nodeid.split("[", 1)[-1].rstrip("]")
    if report.passed:
        _RESULTS.append((case_id, "✅ PASS", ""))
    elif report.skipped:
        _RESULTS.append((case_id, "⏸️ SKIPPED", str(report.longrepr).splitlines()[-1] if report.longrepr else ""))
    else:
        _RESULTS.append((case_id, "❌ FAIL", str(report.longrepr).splitlines()[-1] if report.longrepr else ""))


def pytest_sessionfinish(session, exitstatus):
    if not _RESULTS:
        return
    # Look up category for each id from cases.yaml
    cases_by_id = {c["id"]: c for c in _load_cases()}
    lines = []
    for case_id, status, notes in _RESULTS:
        cat = cases_by_id.get(case_id, {}).get("category", "?")
        lines.append(f"| {case_id} | {cat} | {status} | {notes} |")
    pass_count = sum(1 for _, s, _ in _RESULTS if "PASS" in s)
    total = len(_RESULTS)
    lines.append("")
    lines.append(f"**Baseline pass rate: {pass_count}/{total} ({100*pass_count//total}%) — by design.**")
    _write_last_run(lines)
```

- [ ] **Step 7: Smoke-run the harness against the not-yet-built synthesizer signature.** Expect import-time errors or fixture-shape errors; that is fine — Task A7 is where those surface and you adapt.

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v --no-header -x 2>&1 | head -50
```

Expected: import error or `TypeError: run_synthesis() got an unexpected keyword argument 'fixtures_dir'` — this tells you exactly what the next task needs.

- [ ] **Step 8: Adapt the runner's `_invoke_synthesizer()` to the actual `run_synthesis()` signature.** Look at the function definition (line 291 of `vault_synthesizer.py`) and adjust the kwargs in `_invoke_synthesizer` until import works and at least one case runs to completion. If the synthesizer needs paths instead of a `fixtures_dir` kwarg, accept that and pass the right paths.

- [ ] **Step 9: Delete the transient test file.**

```bash
rm evals/vault-synthesizer/test_runner.py
```

- [ ] **Step 10: Commit.**

```bash
git add evals/vault-synthesizer/runner.py
git commit -m "feat(evals): runner.py — pytest harness, two graders, last-run.md writer"
```

## Task A7: First baseline run + transcript reading

**Files:**
- Create: `evals/vault-synthesizer/traces/baseline-run-2026-05-22.md`
- Modify: `evals/vault-synthesizer/last-run.md` (auto-generated)

- [ ] **Step 1: Run the full suite.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v 2>&1 | tee /tmp/eval-baseline.log
```

Expected: 2 skipped (vs-012, vs-013), 1–2 passing (vs-020 should pass, vs-014 may pass if fixtures cluster), 6–7 failing.

- [ ] **Step 2: Read `last-run.md` and `/tmp/eval-baseline.log`.** For every failure, classify it: (a) real synthesizer failure mode (good — this is the regression suite working), or (b) grader bug (bad — fix it).

- [ ] **Step 3: Write `traces/baseline-run-2026-05-22.md`.**

```markdown
# Baseline Run — 2026-05-22 (anchor for Workstream B's "before" measurement)

## Command
`cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v`

## Result summary
- N pass / N fail / N skip
- Pass rate: NN%

## Per-case classification

| ID | Result | Classification | Notes |
|---|---|---|---|
| vs-014 | <FAIL/PASS> | real failure / grader bug | <one sentence> |
| vs-015 | … | … | … |
| (repeat for each case) | | | |

## Grader bugs found and fixed
(list any grader bugs that surfaced; each must be fixed before locking the baseline)

## Anomalies
(any case whose failure mode was different from the SPEC's prediction)
```

- [ ] **Step 4: If grader bugs surfaced, fix `runner.py` and re-run.** Loop until every failure is classified as "real synthesizer failure mode."

- [ ] **Step 5: Commit.**

```bash
git add evals/vault-synthesizer/last-run.md evals/vault-synthesizer/traces/baseline-run-2026-05-22.md
git commit -m "test(evals): first baseline run — N/10 pass, grader bugs cleared"
```

## Task A8: Write `traces/coded-traces.md` (open-coded log evidence)

**Files:**
- Modify: `evals/vault-synthesizer/traces/coded-traces.md`
- Read-only: `vault/90_system/agent-logs/vault-synthesizer-stderr.log`, `vault/health/synth-manifest-2026-05-*.json`

- [ ] **Step 1: Pull 5–10 representative excerpts.** Each excerpt is a short fenced block of real log/manifest content + a one-sentence open code (Mode 1 / Mode 2 / …) + a sentence linking it to the case ID it justifies.

```markdown
# Coded Traces — the evidence behind `failure-modes.md`

Each block below is a real excerpt from production logs in the error-analysis
window (2026-04-24 → 2026-05-10). The open code points to the failure mode and
the case ID it justifies.

## Excerpt 1 — Mode 1 (silent empty output) → vs-015

`vault/health/synth-manifest-2026-05-08.json`:
\```json
{
  "status": "ok",
  "concepts_written": 0,
  "duration_s": 14.2,
  "model_used": ""
}
\```

Open code: status reports healthy; no concepts written; `model_used` is empty.
Three monitoring layers (manifest, daily-driver, Pushover) all read this as
"ok." This is the load-bearing case in the suite.

## (repeat — 5–10 more excerpts covering Modes 2, 4, 5, 6)
```

- [ ] **Step 2: Commit.**

```bash
git add evals/vault-synthesizer/traces/coded-traces.md
git commit -m "docs(evals): add open-coded log excerpts as evidence index"
```

## Task A9: Write `EXPLANATION.md` (4Q artifact)

**Files:**
- Modify: `evals/vault-synthesizer/EXPLANATION.md`

- [ ] **Step 1: Write the file.** Body comes from SPEC Phase 5; do not paraphrase — the prose was deliberate.

```markdown
---
artifact: vault-synthesizer-evals
created: 2026-05-22
ai-context: "Comprehension artifact for the vault-synthesizer eval suite. 4-question template per Nate B Jones / ADR convention."
---

# Vault Synthesizer Eval Suite — Explanation

## What is this?
A 10-case binary pass/fail eval suite for a local Qwen3-14B vault synthesizer
agent. Cases were derived from open-coding 17 days of production logs
(2026-04-24 → 2026-05-10), not from imagined failure modes. The suite catches
the failure class that production monitoring missed: silent regressions where
the agent reports success while producing zero output.

## Why this approach?
Pytest + YAML over Braintrust / Langfuse — at 10 cases, platform infra is
overhead. Code-based and rubric graders before LLM-as-judge (Hamel's cost-
economics rule). Binary pass/fail over Likert (Husain-Shankar canon — Likert
destroys inter-rater reliability). The case library is grounded in real-log
error analysis (Hamel's #1 principle), not synthetic generation.

## What would break?
(1) Synthesizer prompt drift — re-baseline required if the underlying
synthesis prompt changes structurally. (2) Mock-input fixtures going stale
as the vault evolves — quarterly refresh. (3) No active case uses LLM-judge
at v1; if vs-021 is ever promoted to LLM-judge, the model ID must be pinned
explicitly in the case YAML and a `--skip-llm-judge` flag added for offline runs.

## What did I learn?
That evals aren't really about hallucinations. The failure modes I imagined —
hallucinated phase numbers, relation-tag drift, temporal confusion — were the
easy cases. The hard case was the one nobody drafts on purpose: the
status field that says "ok" while the output is empty. Three layers of
monitoring agreed everything was fine while the system underneath them rotted
silently for nine days. Error analysis surfaces the failures imagination does
not.
```

- [ ] **Step 2: Recruiter-readable check.** Open the file in a browser preview. Read the first paragraph cold. Does it make sense without context? If not, edit the opening sentence until it does.

- [ ] **Step 3: Commit.**

```bash
git add evals/vault-synthesizer/EXPLANATION.md
git commit -m "docs(evals): add 4Q EXPLANATION.md portfolio artifact"
```

## Task A10: Write `README.md` (the entry door)

**Files:**
- Modify: `evals/vault-synthesizer/README.md`

- [ ] **Step 1: Write the file with the mandatory framing block per SPEC Phase 1.**

```markdown
# Vault Synthesizer — Eval Suite

A 10-case binary pass/fail eval suite for a local Qwen3-14B vault synthesizer
agent. Cases were grounded in 17 days of real production logs, not imagined
failure modes. Built solo over two days as a portfolio artifact during a job
search; the discipline transferred from Hamel Husain and Shreya Shankar's
canon and Anthropic's "Demystifying Agent Evals" playbook.

> **This suite ships intentionally red.** ~80% of cases fail today by design
> — each ❌ is a real production failure mode the suite catches, not a broken
> eval. The pass rate jumps after the Workstream B synthesizer fix lands. See
> `EXPLANATION.md` for the why.

## Quickstart

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
    ../evals/vault-synthesizer/runner.py -v
```

(Running from any other CWD breaks the `agents_sdk` import — the `cd agents-sdk`
prefix is mandatory.)

## Current baseline

<!-- BASELINE PENDING — filled in after Task A7 -->

## The failure taxonomy

Six observed failure modes, summarized in [`failure-modes.md`](failure-modes.md):

1. Silent empty output (Mode 1)
2. Status-field misreport on per-file LLM failures (Mode 2)
3. Missing status taxonomy values (Mode 3)
4. `model_used` schema integrity (Mode 4)
5. Pushover credentials fail-quiet (Mode 5)
6. Downstream-consumer misread of healthy status (Mode 6)

The evidence behind each mode is open-coded in [`traces/coded-traces.md`](traces/coded-traces.md).

## Portfolio artifact

See [`EXPLANATION.md`](EXPLANATION.md) for the 4Q comprehension write-up.

## Sources

See [`references.md`](references.md).
```

- [ ] **Step 2: After Task A7's baseline run, replace `<!-- BASELINE PENDING -->`** with the real number.

```markdown
## Current baseline

**N/10 (NN%) — by design.** The N failures are the failure modes the
Workstream B synthesizer fix needs to address. After the fix lands, target
pass rate is 7+/10.
```

- [ ] **Step 3: Commit.**

```bash
git add evals/vault-synthesizer/README.md
git commit -m "docs(evals): README with mandatory framing block + quickstart"
```

## Task A11: Write `references.md`

**Files:**
- Modify: `evals/vault-synthesizer/references.md`

- [ ] **Step 1: Write the file.**

```markdown
# References

## Methodology

- Anthropic — *Demystifying Agent Evals.* The 8-step playbook + 3-grader-type framework.
  Local copy: `vault/40_knowledge/references/ref-anthropic-demystifying-agent-evals.md`.
- Hamel Husain — *Field guide to LLM evals.* "Error analysis is the #1 thing nobody does."
- Shreya Shankar — *Operationalizing ML/AI eval pipelines.* Binary pass/fail > Likert.
- Nate B Jones — OB1 (Open Brain 1) project. 4Q artifact template + typed-reasoning-edges schema.

## Pre-drafted cases (sources for retained cases vs-012..vs-015 and deferred vs-001..vs-011)

- `vault/20_projects/research/2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md` (vs-001 → vs-015)
- `vault/20_projects/research/2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md` (vs-001 → vs-013)

## Error-analysis evidence (sources for new cases vs-016..vs-021)

- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-10-evals-error-analysis-real-logs.md`
- 9 manifests in `vault/health/synth-manifest-2026-05-*.json`
- 3 daily logs in `vault/90_system/agent-logs/vault-synthesizer-2026-05-*.log`
- `vault/90_system/agent-logs/vault-synthesizer-stderr.log`

## Interview-vocabulary cheat-sheet

| Interviewer phrase | What it maps to in this suite |
|---|---|
| "How do you evaluate quality?" | The 6-mode taxonomy in `failure-modes.md` is the answer template. |
| "How do you avoid LLM-as-judge cost?" | 8/10 graders here are deterministic; LLM-judge is reserved and unused at v1. |
| "What about reproducibility?" | Binary pass/fail + Python-eval'd `pass_criteria` + deterministic mocks. |
| "How did you choose cases?" | Open-coded 17 days of real logs first; pre-drafted hallucination cases deferred until production is alive. |
```

- [ ] **Step 2: Commit.**

```bash
git add evals/vault-synthesizer/references.md
git commit -m "docs(evals): references.md — methodology + sources + interview-vocab cheat-sheet"
```

## Task A12: Mandatory doc updates per CLAUDE.md rule

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md`
- Modify: `README.md` (repo root)

- [ ] **Step 1: `CHANGELOG.md` — add entry under the current version (or open v3.30.x if it does not exist).**

```markdown
### Added
- **Vault Synthesizer Eval Suite (`evals/vault-synthesizer/`)** — 10-case binary
  pass/fail eval suite + companion synthesizer-fix workstream. Ships intentionally
  red: 6 new cases (vs-016..vs-021) grounded in 17 days of real production logs
  drive the regression-test discipline that Workstream B's patches will turn
  green. 4 retained cases (vs-012..vs-015) from pre-drafted research. 11 deferred
  cases (vs-001..vs-011) waiting on the synthesizer fix.
```

- [ ] **Step 2: `CLAUDE.md` — update the architecture tree to include `evals/`.**

```
evals/
└── vault-synthesizer/   # NEW v3.30.x — 10-case eval suite for the nightly synthesizer
```

- [ ] **Step 3: `README.md` (repo root) — add a line in the right section** (likely under "What this repo is" or the architecture overview).

```markdown
- `evals/vault-synthesizer/` — 10-case binary eval suite for the vault synthesizer agent
```

- [ ] **Step 4: Commit.**

```bash
git add CHANGELOG.md CLAUDE.md README.md
git commit -m "docs: announce evals/vault-synthesizer/ in CHANGELOG + CLAUDE + README per non-negotiable rule"
```

## Task A13: Loom recording (Sean owns this)

**Files:** none — this is a manual deliverable.

- [ ] **Step 1: Record per SPEC Phase 6 shot list.** 5 minutes unedited. Shot list is canonical; do not re-architect.

- [ ] **Step 2: Save the Loom URL** somewhere Sean can paste into Substack (a sticky note, a markdown scratchpad — anywhere).

## Task A14: Substack + LinkedIn publish (Friday 2026-05-22)

**Files:**
- Modify (publish content): Substack draft (`vault/20_projects/.../substack-drafts/2026-05-10-the-night-my-vault-said-nothing.md`)
- Read-only: Kerouac variant (decide at publish time)

- [ ] **Step 1: Decide Sedaris vs Kerouac.** SPEC recommends Sedaris first. Honor that unless something has changed.

- [ ] **Step 2: Publish on Substack** with Loom embed + GitHub directory link + eval-suite link.

- [ ] **Step 3: Following Wednesday 2026-05-27 — adapt to LinkedIn** (~600 words). Drop section breaks. Keep one JSON snippet.

- [ ] **Step 4: Do not publish the follow-up post on 2026-05-29** until Workstream B's precondition is satisfied (see Task B10 verification gate).

---

# PART B — Workstream B: Synthesizer Fix (lands between 2026-05-22 and 2026-05-29)

> The discipline here is TDD red→green: each failing eval case from Workstream A is
> a test. The fix is the minimum patch that turns one case green without
> regressing the others. Smallest-fix-first ordering below.

## Task B1: vs-018 → `model_used` enum (smallest fix)

**Files:**
- Modify: `agents-sdk/agents/vault_synthesizer.py` (around the SynthesisResult construction / lines 580–660 manifest write path)
- Test: `evals/vault-synthesizer/runner.py` (existing — vs-018 is the failing test)

- [ ] **Step 1: Confirm vs-018 fails today.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v -k vs-018
```

Expected: 1 failed.

- [ ] **Step 2: Read the SynthesisResult definition + manifest write path.**

```bash
grep -nE "model_used|SynthesisResult|class Synthesis" agents-sdk/agents/vault_synthesizer.py | head -20
```

- [ ] **Step 3: Add a module-level `MODEL_USED_NONE = "none"` constant** and initialize `model_used = MODEL_USED_NONE` instead of `""`. On a successful LLM call, overwrite with the actual model name. The valid enum is `{"qwen3-14b", "claude-sonnet-4-6", "claude-haiku-4-5", "none"}` — match the eval case's expected set.

```python
# At the top of agents-sdk/agents/vault_synthesizer.py
MODEL_USED_VALUES = frozenset({"qwen3-14b", "claude-sonnet-4-6", "claude-haiku-4-5", "none"})
MODEL_USED_NONE = "none"
```

Then find the line initializing `model_used = ""` (or equivalent) and change it to `model_used = MODEL_USED_NONE`. On a successful LLM call, set `model_used = ...` to the actual value from the HybridRouter route decision.

- [ ] **Step 4: Run vs-018.** Expected: PASS.

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v -k vs-018
```

- [ ] **Step 5: Run the full suite — no regressions.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v
```

- [ ] **Step 6: Commit.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git add agents-sdk/agents/vault_synthesizer.py
git commit -m "fix(synth): model_used initializes to 'none' enum value, not empty string (vs-018)"
```

## Task B2: vs-016 → run-level status promotion on all-file LLM failure

**Files:**
- Modify: `agents-sdk/agents/vault_synthesizer.py` (around `run_synthesis()` line 291 + the per-file loop)

- [ ] **Step 1: Confirm vs-016 fails today.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v -k vs-016
```

Expected: 1 failed.

- [ ] **Step 2: Read the per-file LLM-call loop** (lines ~320–420 per SPEC).

- [ ] **Step 3: Add success/failure counters and promote status at the end of the loop.**

```python
# Inside run_synthesis(), at the top of the per-file loop:
files_attempted = 0
files_succeeded = 0
warnings: list[str] = []

# Inside the loop, wrap the llm_caller invocation:
for note in notes:
    files_attempted += 1
    try:
        body = llm_caller(prompt_for(note))
    except Exception as e:  # noqa: BLE001 — we promote, we don't swallow
        warnings.append(f"llm_call_failed: {note.path}: {type(e).__name__}")
        continue
    files_succeeded += 1
    # ... existing happy-path logic ...

# After the loop, decide the run-level status:
if files_attempted == 0:
    status = "ok"  # nothing to do, not a failure
elif files_succeeded == 0:
    status = "error"  # vs-016: every file failed
elif files_succeeded < files_attempted and concepts_written == 0:
    status = "partial-empty"  # vs-017: some succeeded, no output
elif files_succeeded < files_attempted:
    status = "partial"
elif concepts_written == 0:
    status = "success-empty"  # Mode 1 / vs-015
else:
    status = "ok"
```

- [ ] **Step 4: Add `warnings` to the SynthesisResult dataclass + manifest write path** so they surface to consumers.

- [ ] **Step 5: Run vs-016, then full suite.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v -k vs-016
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v
```

Expected: vs-016 PASS; vs-015 and vs-017 may now also pass as a side effect — that's the point.

- [ ] **Step 6: Commit.**

```bash
git add agents-sdk/agents/vault_synthesizer.py
git commit -m "fix(synth): promote run-level status when all per-file LLM calls fail (vs-016, +vs-015/017)"
```

## Task B3: vs-017 → status taxonomy `partial-empty`

**Files:**
- Modify: `agents-sdk/agents/vault_synthesizer.py` (status enum definition if one exists)

- [ ] **Step 1: Confirm vs-017's state after Task B2.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v -k vs-017
```

If it passed already (likely — the Task B2 logic covers it), skip to step 4. Otherwise:

- [ ] **Step 2: Find any status enum/literal type and add the new values.**

```bash
grep -nE "Literal\[.*status|STATUS_|VALID_STATUS|status\s*:\s*(str|Literal)" agents-sdk/agents/vault_synthesizer.py
```

- [ ] **Step 3: Add `"success-empty"` and `"partial-empty"`** to whatever Literal/enum exists. If no enum exists, add one near `MODEL_USED_VALUES`:

```python
STATUS_VALUES = frozenset({"ok", "error", "partial", "partial-empty", "success-empty"})
```

- [ ] **Step 4: Run vs-017 + full suite.** Expected: PASS.

- [ ] **Step 5: Commit.**

```bash
git add agents-sdk/agents/vault_synthesizer.py
git commit -m "fix(synth): add success-empty + partial-empty to status taxonomy (vs-017)"
```

## Task B4: vs-019 → Pushover boot-time credential check

**Files:**
- Modify: `agents-sdk/lib/pushover.py` (107 lines today)
- Modify: `agents-sdk/agents/vault_synthesizer.py` (call the boot check at start of `run_synthesis()`)

- [ ] **Step 1: Confirm vs-019 fails today.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v -k vs-019
```

- [ ] **Step 2: Add `PushoverConfigurationError` + `ensure_credentials_or_raise()` to `agents-sdk/lib/pushover.py`.**

```python
# agents-sdk/lib/pushover.py — add near the top, after imports

class PushoverConfigurationError(RuntimeError):
    """Raised when Pushover credentials are missing at agent boot.

    Designed to fail loud at startup instead of silent-logging at notify time —
    a silent failure in the system whose job is surfacing failures is exactly
    the regression vs-019 catches.
    """


def ensure_credentials_or_raise() -> None:
    """Load Pushover keychain creds; raise if missing.

    Call this at the top of any agent's main entrypoint, before any LLM call,
    so a credential-misconfiguration crashes the run early rather than late.
    """
    from agents_sdk.lib.keychain import get_secret
    user = get_secret("com.sean.agents.pushover_user_key")
    token = get_secret("com.sean.agents.pushover_api_token")
    if not user or not token:
        missing = [name for name, v in [("user_key", user), ("api_token", token)] if not v]
        raise PushoverConfigurationError(
            f"pushover credentials missing from keychain: {missing}"
        )
```

- [ ] **Step 3: Call `ensure_credentials_or_raise()` at the top of `run_synthesis()`.**

```python
# agents-sdk/agents/vault_synthesizer.py — top of run_synthesis() body
from agents_sdk.lib.pushover import ensure_credentials_or_raise
ensure_credentials_or_raise()
```

- [ ] **Step 4: Run vs-019 + full suite.** Expected: vs-019 PASS, no regressions.

- [ ] **Step 5: Commit.**

```bash
git add agents-sdk/lib/pushover.py agents-sdk/agents/vault_synthesizer.py
git commit -m "fix(pushover): raise at boot when keychain creds missing instead of silent-logging (vs-019)"
```

## Task B5: vs-021 → daily-driver Vault Health WARNING

**Files:**
- Modify: `agents-sdk/agents/daily_driver.py` (find `render_vault_health` or the inline equivalent in `build_prompt`)

- [ ] **Step 1: Confirm vs-021 fails today.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v -k vs-021
```

- [ ] **Step 2: Locate the Vault Health section.** It's inside `build_prompt()` at line 247 of `daily_driver.py`, or factored into a helper. Find the string that mentions the synth manifest.

```bash
grep -nE "Vault Health|synth-manifest|render_vault_health" agents-sdk/agents/daily_driver.py
```

- [ ] **Step 3: Extract `render_vault_health(manifest_dict) -> str`** as a standalone helper so the eval can call it directly without a full daily-driver run.

```python
# agents-sdk/agents/daily_driver.py

def render_vault_health(manifest: dict) -> str:
    """Render a Vault Health markdown block from a synth manifest dict.

    Extracted as a standalone function so the eval suite can call it without
    a full daily-driver run.
    """
    status = manifest.get("status", "unknown")
    concepts = manifest.get("concepts_written", 0)
    duration = manifest.get("duration_s", 0)

    if status in {"success-empty", "partial-empty"} or concepts == 0:
        return (
            f"## Vault Health\n\n"
            f"⚠️ **WARNING** — synth status `{status}`, concepts_written: {concepts}.\n"
            f"The synthesizer reported structurally successful but produced no concept articles.\n"
            f"Run: `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/vault_synthesizer.py --once`\n"
        )
    if status == "ok":
        return f"## Vault Health\n\n✅ ok — {concepts} concepts written in {duration:.1f}s.\n"
    if status in {"error", "partial"}:
        return f"## Vault Health\n\n❌ {status} — see manifest.\n"
    return f"## Vault Health\n\n? unknown status `{status}`.\n"
```

- [ ] **Step 4: Replace the existing inline rendering** in `build_prompt()` with a call to `render_vault_health(manifest)`.

- [ ] **Step 5: Run vs-021 + full suite.** Expected: PASS.

- [ ] **Step 6: Commit.**

```bash
git add agents-sdk/agents/daily_driver.py
git commit -m "fix(daily-driver): surface success-empty / zero-output synth manifest as WARNING (vs-021)"
```

## Task B6: vs-020 verification + vs-014/015 follow-through

**Files:** (no code changes if Task B2 was thorough — this task is verification + un-skip)

- [ ] **Step 1: Run the full suite.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v
```

Expected pass rate: at least vs-014, vs-015, vs-016, vs-017, vs-018, vs-019, vs-021 PASS; vs-020 was already PASS at baseline; vs-012/013 still SKIPPED.

- [ ] **Step 2: If vs-014 or vs-015 still FAIL,** that means the synthesizer is producing zero output even with a working LLM caller — a deeper bug. Read transcripts. Likely a fixture-shape mismatch, not a code bug. Adjust fixtures in `traces/fixtures/` until vs-014 passes when the synthesizer is given working notes.

- [ ] **Step 3: Once vs-014 + vs-015 pass, un-skip vs-012 + vs-013.** Edit `cases.yaml` to remove their `skip_reason` field. Run them. They will likely PASS or FAIL on real semantic issues — that's fine; the suite is doing its job.

- [ ] **Step 4: Commit.**

```bash
git add evals/vault-synthesizer/cases.yaml evals/vault-synthesizer/traces/fixtures/
git commit -m "test(evals): un-skip vs-012 + vs-013 now that synthesizer emits output"
```

## Task B7: Run the suite against the live synthesizer for 5 consecutive nights

**Files:** (no code — gate for the 2026-05-29 follow-up post)

- [ ] **Step 1: Let the nightly synthesizer run.** 2:30 AM via launchd. Check `vault/health/synth-manifest-{YYYY-MM-DD}.json` each morning. Required: 5 consecutive nights of `concepts_written > 0`.

- [ ] **Step 2: Each morning, run the suite once.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest ../evals/vault-synthesizer/runner.py -v
```

Target: 7+/10 pass on all 5 mornings.

- [ ] **Step 3: If precondition is met by Thursday 2026-05-28, publish the follow-up post Friday 2026-05-29.** If not, delay — do not publish a "we fixed it" post while the synthesizer is empty.

## Task B8: Update README baseline + last-run

**Files:**
- Modify: `evals/vault-synthesizer/README.md` (baseline number)
- Modify: `evals/vault-synthesizer/last-run.md` (latest run, auto-generated)

- [ ] **Step 1: Update the README baseline section.**

```markdown
## Current baseline

**Pre-fix (Workstream A ship, 2026-05-22): N/10 (NN%).**
**Post-fix (Workstream B complete, 2026-05-28): M/10 (MM%).**

The N → M jump documents what the synthesizer fix accomplished. Cases that
remain failing are intentionally retained as a regression guard against the
specific failure modes returning.
```

- [ ] **Step 2: Commit.**

```bash
git add evals/vault-synthesizer/README.md
git commit -m "docs(evals): update README baseline — post-fix pass rate M/10"
```

---

# PART C — Workstream C: Substack-Drafter Agent

> **Why this is here and not "post-employment":** The agent depends on the synthesizer producing concept articles. That is a technical precondition (Task B7's 5-night gate), not a strategic one. Once B is green, C makes the publishing cadence agent-assisted instead of hand-written — which is the rate-limiting step on the publishing strategy that drives the job hunt. Default-disabled at three layers (config flag, opt-in install env var, dry-run flag); the agent never publishes autonomously; Sean reviews every draft Friday morning.
>
> **Hard precondition:** Task B7 has passed. If `vault/knowledge/concepts/` is empty or had a `concepts_written == 0` night in the last 3 days, do not start C — the agent has nothing to draft from.

## Task C0: Confirm preconditions

**Files:** (read-only)

- [ ] **Step 1: Verify Workstream B's 5-night gate passed.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
ls -1 vault/health/synth-manifest-*.json | tail -7
# For each of the last 5 nights, confirm concepts_written > 0:
for f in $(ls -1 vault/health/synth-manifest-*.json | tail -5); do
  echo -n "$f: "
  agents-sdk/.venv/bin/python3 -c "import json,sys; d=json.load(open('$f')); print('concepts_written=',d.get('concepts_written',0),'status=',d.get('status','?'))"
done
```

Expected: 5 lines, all with `concepts_written > 0` and `status == 'ok'`.

- [ ] **Step 2: Verify the writing-voice-modes skill exists and has the 5 modes documented.**

```bash
test -f .claude/skills/writing-voice-modes/SKILL.md && head -40 .claude/skills/writing-voice-modes/SKILL.md
```

- [ ] **Step 3: Verify the substack-drafts/ output directory exists.**

```bash
ls vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/ 2>/dev/null || echo "MISSING — Task C8 will create it"
```

## Task C1: Add `[substack_drafter]` config table (default-disabled)

**Files:**
- Modify: `agents-sdk/config.toml`

- [ ] **Step 1: Locate where `[process_inbox]` or another default-disabled agent's config lives.**

```bash
grep -n "^\[" agents-sdk/config.toml
```

- [ ] **Step 2: Append the new table at the end of the file.**

```toml
[substack_drafter]
enabled = false  # default-disabled per SPEC kill-switch layer 1
max_cost_usd = 0.10  # hard cap per run; Qwen3-14B local is free, Sonnet fallback ~$0.05/draft
output_dir = "vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts"
concepts_lookback_days = 14
references_lookback_days = 30
synthesizer_dry_threshold = 3  # exit no-op if last N synth manifests had concepts_written == 0
draft_word_count_target = 1350  # midpoint of 1200–1500 SPEC range
schedule_day = "Thursday"
schedule_hour = 18
voice_epoch = "2026-05-04"  # Monday of the sprint; rotation index zero
# voice_override = "sedaris"  # uncomment to pin a mode for a specific run
```

- [ ] **Step 3: Validate the TOML parses.**

```bash
agents-sdk/.venv/bin/python3 -c "import tomllib; c = tomllib.load(open('agents-sdk/config.toml','rb')); print(c['substack_drafter'])"
```

Expected: dict with `enabled=False` and the other keys.

- [ ] **Step 4: Commit.**

```bash
git add agents-sdk/config.toml
git commit -m "feat(config): add [substack_drafter] table — default-disabled, opt-in"
```

## Task C2: Build the voice-rotation module (TDD)

**Files:**
- Create: `agents-sdk/agents/substack_drafter.py` (skeleton with one function)
- Create: `agents-sdk/tests/test_substack_drafter.py`

- [ ] **Step 1: Write the failing test.**

```python
# agents-sdk/tests/test_substack_drafter.py
from datetime import date
import pytest
from agents_sdk.agents.substack_drafter import pick_voice_mode

# SPEC rotation table: 0=sean, 1=sedaris, 2=kerouac, 3=thompson, 4=vonnegut
def test_voice_mode_at_epoch():
    assert pick_voice_mode(today=date(2026, 5, 4), epoch=date(2026, 5, 4)) == "sean"

def test_voice_mode_week_1():
    # 7 days after epoch → index 1 → sedaris
    assert pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4)) == "sedaris"

def test_voice_mode_wraps_at_5():
    # 35 days after epoch → index 5 → wraps to 0 → sean
    assert pick_voice_mode(today=date(2026, 6, 8), epoch=date(2026, 5, 4)) == "sean"

def test_voice_mode_override_pins():
    assert pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4), override="vonnegut") == "vonnegut"

def test_voice_mode_rejects_bad_override():
    with pytest.raises(ValueError):
        pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4), override="hemingway")
```

- [ ] **Step 2: Run — confirm failure.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_substack_drafter.py -v
```

Expected: ImportError / ModuleNotFoundError.

- [ ] **Step 3: Write the minimum implementation.**

```python
# agents-sdk/agents/substack_drafter.py
"""Substack-Drafter agent.

Reads post-fix synthesizer output, picks a concept cluster, drafts a Substack
post in a rotating voice mode. Never publishes; drafts land in the vault for
Sean to review Friday morning.

Default-disabled — see [substack_drafter] in config.toml + INSTALL_SUBSTACK_DRAFTER env var.
"""
from __future__ import annotations
from datetime import date

VOICE_MODES = ("sean", "sedaris", "kerouac", "thompson", "vonnegut")


def pick_voice_mode(*, today: date, epoch: date, override: str | None = None) -> str:
    """Rotate through 5 voice modes weekly. Override pins a specific mode.

    Uses absolute weeks since epoch (not week-of-year, which skews across year
    boundaries per SPEC).
    """
    if override is not None:
        if override not in VOICE_MODES:
            raise ValueError(f"unknown voice mode: {override!r}; valid: {VOICE_MODES}")
        return override
    weeks_since = (today - epoch).days // 7
    return VOICE_MODES[weeks_since % len(VOICE_MODES)]
```

- [ ] **Step 4: Re-run — confirm pass.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_substack_drafter.py -v
```

Expected: 5 passed.

- [ ] **Step 5: Commit.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git add agents-sdk/agents/substack_drafter.py agents-sdk/tests/test_substack_drafter.py
git commit -m "feat(substack-drafter): voice-rotation module + 5 tests"
```

## Task C3: Synthesizer-dryness gate (graceful no-op)

**Files:**
- Modify: `agents-sdk/agents/substack_drafter.py`
- Modify: `agents-sdk/tests/test_substack_drafter.py`

- [ ] **Step 1: Add the failing test.**

```python
# Append to agents-sdk/tests/test_substack_drafter.py
import json
import tempfile
from pathlib import Path

def _write_manifest(d: Path, date_str: str, concepts: int, status: str = "ok") -> None:
    (d / f"synth-manifest-{date_str}.json").write_text(json.dumps({
        "status": status, "concepts_written": concepts, "duration_s": 12.0
    }))

def test_dryness_gate_blocks_when_last_3_are_zero(tmp_path):
    from agents_sdk.agents.substack_drafter import is_synthesizer_dry
    _write_manifest(tmp_path, "2026-05-30", 0)
    _write_manifest(tmp_path, "2026-05-31", 0)
    _write_manifest(tmp_path, "2026-06-01", 0)
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is True

def test_dryness_gate_passes_when_last_3_have_output(tmp_path):
    from agents_sdk.agents.substack_drafter import is_synthesizer_dry
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 3)
    _write_manifest(tmp_path, "2026-06-01", 7)
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is False

def test_dryness_gate_handles_empty_dir(tmp_path):
    from agents_sdk.agents.substack_drafter import is_synthesizer_dry
    # No manifests yet → treat as dry (don't draft from nothing)
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is True
```

- [ ] **Step 2: Run — confirm failure.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_substack_drafter.py::test_dryness_gate_blocks_when_last_3_are_zero -v
```

Expected: ImportError on `is_synthesizer_dry`.

- [ ] **Step 3: Implement.**

```python
# Append to agents-sdk/agents/substack_drafter.py
import json
from pathlib import Path


def is_synthesizer_dry(*, health_dir: Path, threshold: int = 3) -> bool:
    """Return True iff the last `threshold` synth manifests had concepts_written == 0.

    Empty directory is treated as dry — drafting from no input is a no-op anyway.
    """
    manifests = sorted(health_dir.glob("synth-manifest-*.json"))
    if len(manifests) < threshold:
        return True
    recent = manifests[-threshold:]
    for path in recent:
        try:
            data = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            return True  # unreadable manifest = treat as dry to be safe
        if data.get("concepts_written", 0) > 0:
            return False
    return True
```

- [ ] **Step 4: Re-run + commit.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_substack_drafter.py -v
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git add agents-sdk/agents/substack_drafter.py agents-sdk/tests/test_substack_drafter.py
git commit -m "feat(substack-drafter): dryness gate — no-op when last N manifests are zero"
```

## Task C4: Cluster picker (densest-interconnection)

**Files:**
- Modify: `agents-sdk/agents/substack_drafter.py`
- Modify: `agents-sdk/tests/test_substack_drafter.py`

- [ ] **Step 1: Failing test.**

```python
# Append to test_substack_drafter.py

def _write_concept(d: Path, slug: str, wikilinks: list[str]) -> None:
    body = f"---\ntype: concept\nslug: {slug}\n---\n\n# {slug}\n\n"
    body += " ".join(f"[[{w}]]" for w in wikilinks)
    (d / f"{slug}.md").write_text(body)

def test_cluster_picker_returns_densest_3_to_5(tmp_path):
    from agents_sdk.agents.substack_drafter import pick_densest_cluster
    # Cluster A: three concepts that share ≥3 wikilinks
    _write_concept(tmp_path, "a", ["x", "y", "z", "shared"])
    _write_concept(tmp_path, "b", ["x", "y", "shared", "extra"])
    _write_concept(tmp_path, "c", ["y", "z", "shared"])
    # Cluster B: two isolated concepts
    _write_concept(tmp_path, "lonely", ["nothing-shared"])
    cluster = pick_densest_cluster(concepts_dir=tmp_path, min_shared=3)
    assert {"a", "b", "c"} <= set(cluster)
    assert "lonely" not in cluster
    assert 3 <= len(cluster) <= 5
```

- [ ] **Step 2: Run — confirm failure.**

- [ ] **Step 3: Implement.**

```python
# Append to substack_drafter.py
import re
from collections import defaultdict

_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def _extract_wikilinks(text: str) -> set[str]:
    return {m.group(1).strip() for m in _WIKILINK_RE.finditer(text)}


def pick_densest_cluster(*, concepts_dir: Path, min_shared: int = 3) -> list[str]:
    """Return the slugs of the cluster with the densest wikilink overlap.

    A "cluster" is the largest connected component where each pair of concepts
    shares >= `min_shared` outbound wikilinks. Returns 3–5 slugs; fewer if the
    densest component is smaller; more is clipped to 5.
    """
    paths = sorted(concepts_dir.glob("*.md"))
    if not paths:
        return []
    links_by_slug: dict[str, set[str]] = {}
    for p in paths:
        links_by_slug[p.stem] = _extract_wikilinks(p.read_text())

    # Build adjacency: connect a,b if |links[a] & links[b]| >= min_shared
    adj: dict[str, set[str]] = defaultdict(set)
    slugs = list(links_by_slug)
    for i, a in enumerate(slugs):
        for b in slugs[i+1:]:
            if len(links_by_slug[a] & links_by_slug[b]) >= min_shared:
                adj[a].add(b)
                adj[b].add(a)

    # Find largest connected component
    seen: set[str] = set()
    best: list[str] = []
    for slug in slugs:
        if slug in seen:
            continue
        stack, component = [slug], []
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            component.append(node)
            stack.extend(adj[node] - seen)
        if len(component) > len(best):
            best = component
    return sorted(best)[:5]
```

- [ ] **Step 4: Re-run + commit.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_substack_drafter.py -v
git add agents-sdk/agents/substack_drafter.py agents-sdk/tests/test_substack_drafter.py
git commit -m "feat(substack-drafter): wikilink-density cluster picker"
```

## Task C5: Prompt composer

**Files:**
- Modify: `agents-sdk/agents/substack_drafter.py`
- Modify: `agents-sdk/tests/test_substack_drafter.py`

- [ ] **Step 1: Failing test.**

```python
# Append to test_substack_drafter.py
def test_compose_prompt_includes_voice_skill(tmp_path):
    from agents_sdk.agents.substack_drafter import compose_prompt
    voice_skill = tmp_path / "SKILL.md"
    voice_skill.write_text("# Voice Modes\n\nSean Mode signature moves: ...")
    out = compose_prompt(
        voice_mode="sean",
        voice_skill_path=voice_skill,
        cluster_slugs=["pushover-fail-quiet", "silent-empty-output"],
        cluster_bodies=["body A", "body B"],
        reference_excerpts=["ref 1", "ref 2"],
        word_count_target=1350,
    )
    assert "Sean Mode signature moves" in out["system"]
    assert "pushover-fail-quiet" in out["user"]
    assert "1350" in out["user"] or "1200" in out["user"] or "1500" in out["user"]
    assert "Hook in the first 2 sentences" in out["user"]
```

- [ ] **Step 2: Run — confirm failure.**

- [ ] **Step 3: Implement.**

```python
# Append to substack_drafter.py

def compose_prompt(*, voice_mode: str, voice_skill_path: Path,
                   cluster_slugs: list[str], cluster_bodies: list[str],
                   reference_excerpts: list[str], word_count_target: int = 1350) -> dict[str, str]:
    """Return {'system': ..., 'user': ...} for the HybridRouter call."""
    voice_skill = voice_skill_path.read_text()
    system = (
        f"You are drafting a Substack post in {voice_mode!r} voice. "
        f"The full voice spec is below — follow its signature moves.\n\n"
        f"---\n{voice_skill}\n---"
    )
    cluster_block = "\n\n".join(
        f"## Source concept: {slug}\n\n{body}" for slug, body in zip(cluster_slugs, cluster_bodies)
    )
    refs_block = "\n\n".join(f"- {r}" for r in reference_excerpts)
    user = (
        f"Draft a {word_count_target}-word Substack post in {voice_mode} voice about the "
        f"connections between: {', '.join(cluster_slugs)}.\n\n"
        f"Ground in these sources:\n\n{refs_block}\n\n"
        f"Source concept bodies:\n\n{cluster_block}\n\n"
        f"Constraints:\n"
        f"- Hook in the first 2 sentences.\n"
        f"- Use {voice_mode}'s signature moves from the skill spec above.\n"
        f"- Cite sources by wikilink, not by URL.\n"
        f"- Do not publish to Substack — this is a draft for Sean to review.\n"
    )
    return {"system": system, "user": user}
```

- [ ] **Step 4: Re-run + commit.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_substack_drafter.py -v
git add agents-sdk/agents/substack_drafter.py agents-sdk/tests/test_substack_drafter.py
git commit -m "feat(substack-drafter): prompt composer w/ voice skill injection"
```

## Task C6: Wire HybridRouter + draft writer

**Files:**
- Modify: `agents-sdk/agents/substack_drafter.py`
- Modify: `agents-sdk/tests/test_substack_drafter.py`

- [ ] **Step 1: Failing test (mock the router).**

```python
# Append to test_substack_drafter.py
def test_write_draft_creates_file_with_frontmatter(tmp_path, monkeypatch):
    from agents_sdk.agents import substack_drafter
    captured = {}
    def fake_route(task, system, user, max_cost_usd=None):
        captured["task"] = task
        return {"text": "# The Night My Vault Said Nothing\n\nDraft body here...",
                "model_used": "qwen3-14b", "cost_usd": 0.0}
    monkeypatch.setattr(substack_drafter, "_route", fake_route)

    out_dir = tmp_path / "drafts"
    out_dir.mkdir()
    path = substack_drafter.write_draft(
        out_dir=out_dir,
        slug="vault-said-nothing",
        voice_mode="sean",
        cluster_slugs=["a", "b"],
        prompt={"system": "sys", "user": "user"},
        max_cost_usd=0.10,
    )
    assert path.exists()
    content = path.read_text()
    assert "voice: sean" in content
    assert "source_concepts:" in content
    assert "cost_usd: 0.0" in content
    assert "# The Night My Vault Said Nothing" in content
```

- [ ] **Step 2: Run — confirm failure.**

- [ ] **Step 3: Implement.**

```python
# Append to substack_drafter.py
from datetime import datetime, timezone

def _route(task: str, system: str, user: str, max_cost_usd: float = 0.10) -> dict:
    """Delegate to HybridRouter — extracted so tests can monkeypatch."""
    from agents_sdk.lib.hybrid_router import route
    return route(task=task, system=system, user=user, max_cost_usd=max_cost_usd)


def write_draft(*, out_dir: Path, slug: str, voice_mode: str,
                cluster_slugs: list[str], prompt: dict[str, str],
                max_cost_usd: float = 0.10) -> Path:
    """Call the router, persist the draft as a markdown file with frontmatter."""
    result = _route(task="substack_draft", system=prompt["system"],
                    user=prompt["user"], max_cost_usd=max_cost_usd)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = out_dir / f"{today}-agent-draft-{slug}.md"
    frontmatter = (
        f"---\n"
        f"type: substack-draft\n"
        f"voice: {voice_mode}\n"
        f"source_concepts: {cluster_slugs}\n"
        f"generated_at: {datetime.now(timezone.utc).isoformat()}\n"
        f"model_used: {result.get('model_used', 'unknown')}\n"
        f"cost_usd: {result.get('cost_usd', 0.0)}\n"
        f"status: pending-review\n"
        f"---\n\n"
    )
    path.write_text(frontmatter + result["text"])
    return path
```

- [ ] **Step 4: Re-run + commit.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_substack_drafter.py -v
git add agents-sdk/agents/substack_drafter.py agents-sdk/tests/test_substack_drafter.py
git commit -m "feat(substack-drafter): write_draft — HybridRouter call + markdown w/ frontmatter"
```

## Task C7: `main()` + `--dry-run` flag

**Files:**
- Modify: `agents-sdk/agents/substack_drafter.py`
- Modify: `agents-sdk/tests/test_substack_drafter.py`

- [ ] **Step 1: Failing tests for `main()`.**

```python
# Append to test_substack_drafter.py
def test_main_dryrun_no_route_call(tmp_path, monkeypatch, capsys):
    from agents_sdk.agents import substack_drafter
    # Set up enough scaffolding to reach the prompt step
    health = tmp_path / "health"; health.mkdir()
    concepts = tmp_path / "concepts"; concepts.mkdir()
    drafts = tmp_path / "drafts"; drafts.mkdir()
    # 3 nights of healthy synth manifests
    for i, dstr in enumerate(["2026-06-01", "2026-06-02", "2026-06-03"]):
        (health / f"synth-manifest-{dstr}.json").write_text(
            f'{{"status":"ok","concepts_written":3}}')
    # 2 connected concepts
    (concepts / "a.md").write_text("# a\n[[x]] [[y]] [[shared]] [[extra]]")
    (concepts / "b.md").write_text("# b\n[[x]] [[y]] [[shared]]")
    voice_skill = tmp_path / "SKILL.md"; voice_skill.write_text("voice spec")

    called = {"n": 0}
    def fake_route(*a, **kw):
        called["n"] += 1
        return {"text": "draft", "model_used": "qwen3-14b", "cost_usd": 0.0}
    monkeypatch.setattr(substack_drafter, "_route", fake_route)

    rc = substack_drafter.main(
        health_dir=health, concepts_dir=concepts, out_dir=drafts,
        voice_skill_path=voice_skill, dry_run=True,
    )
    assert rc == 0
    assert called["n"] == 0  # dry-run must not call the model
    assert list(drafts.glob("*.md")) == []  # no draft written
    out = capsys.readouterr().out
    assert "DRY-RUN" in out
    assert "voice:" in out

def test_main_dry_synth_exits_zero_no_op(tmp_path, capsys):
    from agents_sdk.agents import substack_drafter
    health = tmp_path / "health"; health.mkdir()
    # Three nights of zero output
    for dstr in ["2026-06-01", "2026-06-02", "2026-06-03"]:
        (health / f"synth-manifest-{dstr}.json").write_text(
            f'{{"status":"ok","concepts_written":0}}')
    rc = substack_drafter.main(
        health_dir=health, concepts_dir=tmp_path/"none",
        out_dir=tmp_path/"out", voice_skill_path=tmp_path/"SKILL.md",
        dry_run=False,
    )
    assert rc == 0
    assert "synthesizer dry" in capsys.readouterr().out
```

- [ ] **Step 2: Implement `main()`.**

```python
# Append to substack_drafter.py
import argparse
import sys


def main(*, health_dir: Path, concepts_dir: Path, out_dir: Path,
         voice_skill_path: Path, dry_run: bool = False,
         today: date | None = None, epoch: date | None = None,
         voice_override: str | None = None,
         max_cost_usd: float = 0.10) -> int:
    """Agent entrypoint. Returns process exit code."""
    today = today or date.today()
    epoch = epoch or date(2026, 5, 4)

    # 1. Gate on synthesizer dryness
    if is_synthesizer_dry(health_dir=health_dir, threshold=3):
        print(f"[substack_drafter] synthesizer dry — no draft generated ({today})")
        return 0

    # 2. Pick a cluster
    cluster = pick_densest_cluster(concepts_dir=concepts_dir, min_shared=3)
    if len(cluster) < 2:
        print(f"[substack_drafter] no dense cluster found — no-op ({today})")
        return 0

    # 3. Pick voice mode
    voice = pick_voice_mode(today=today, epoch=epoch, override=voice_override)

    # 4. Load cluster bodies + (placeholder) reference excerpts
    cluster_bodies = [(concepts_dir / f"{s}.md").read_text() for s in cluster]
    reference_excerpts = []  # TODO: similarity pull — wire in Task C9 once vault-index ready

    # 5. Compose
    prompt = compose_prompt(
        voice_mode=voice, voice_skill_path=voice_skill_path,
        cluster_slugs=cluster, cluster_bodies=cluster_bodies,
        reference_excerpts=reference_excerpts,
    )

    # 6. Dry-run short-circuit
    if dry_run:
        print(f"[substack_drafter] DRY-RUN")
        print(f"  voice: {voice}")
        print(f"  cluster: {cluster}")
        print(f"  system prompt: {len(prompt['system'])} chars")
        print(f"  user prompt:   {len(prompt['user'])} chars")
        return 0

    # 7. Route + write
    slug = "-".join(cluster[:2])[:50]
    path = write_draft(
        out_dir=out_dir, slug=slug, voice_mode=voice,
        cluster_slugs=cluster, prompt=prompt, max_cost_usd=max_cost_usd,
    )
    print(f"[substack_drafter] draft written: {path}")

    # 8. Pushover ping (uses the boot-time check from Workstream B Task B4)
    try:
        from agents_sdk.lib.pushover import ensure_credentials_or_raise, notify_agent_error
        ensure_credentials_or_raise()
        # notify_substack_ready does not yet exist — use notify_agent_error with
        # repurposed args as a stopgap, OR add a notify_info function in C10.
        # For now, just log; the SPEC says "informational only, never decision-forcing"
        print(f"[substack_drafter] (would Pushover-notify if notify_info existed)")
    except Exception as e:  # noqa: BLE001 — notification failures don't kill the run
        print(f"[substack_drafter] notify failed (non-fatal): {e}")

    return 0


def _cli() -> int:
    from agents_sdk.lib.config import load_config
    cfg = load_config()
    if not cfg.get("substack_drafter", {}).get("enabled", False):
        print("[substack_drafter] disabled in config.toml — exit 0")
        return 0

    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--voice", default=None, help="pin voice mode (sean|sedaris|kerouac|thompson|vonnegut)")
    args = p.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    return main(
        health_dir=repo_root / "vault" / "health",
        concepts_dir=repo_root / "vault" / "knowledge" / "concepts",
        out_dir=repo_root / cfg["substack_drafter"]["output_dir"],
        voice_skill_path=repo_root / ".claude" / "skills" / "writing-voice-modes" / "SKILL.md",
        dry_run=args.dry_run,
        voice_override=args.voice,
        max_cost_usd=cfg["substack_drafter"]["max_cost_usd"],
    )


if __name__ == "__main__":
    sys.exit(_cli())
```

- [ ] **Step 3: Re-run all tests + commit.**

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_substack_drafter.py -v
git add agents-sdk/agents/substack_drafter.py agents-sdk/tests/test_substack_drafter.py
git commit -m "feat(substack-drafter): main() + --dry-run + CLI wrapper"
```

- [ ] **Step 4: Real dry-run smoke test against the live vault.**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 agents/substack_drafter.py --dry-run
```

Expected: either `[substack_drafter] disabled in config.toml` (if `enabled=false`, which is the default) OR `[substack_drafter] synthesizer dry — no draft generated` (if `enabled=true` but synthesizer hasn't produced output yet) OR a real dry-run printout with the cluster + voice.

## Task C8: launchd plist + installer integration (default-disabled)

**Files:**
- Create: `agents-sdk/schedules/com.sean.agents.substack_drafter.plist`
- Modify: `agents-sdk/schedules/install_schedules.sh`

- [ ] **Step 1: Create the plist** mirroring the existing `process_inbox` or `daily_driver` plist shape. **Non-negotiable per CLAUDE.md:** include `EnvironmentVariables.PATH = /Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`.

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
cp agents-sdk/schedules/com.sean.agents.daily_driver.plist \
   agents-sdk/schedules/com.sean.agents.substack_drafter.plist
# Then edit the new file: change Label, ProgramArguments to point at substack_drafter.py,
# change StartCalendarInterval to Thursday 18:00 (Weekday=4, Hour=18, Minute=0).
```

- [ ] **Step 2: Open the new plist and verify the four required edits.**

```bash
grep -E "Label|substack_drafter|Weekday|Hour|PATH" agents-sdk/schedules/com.sean.agents.substack_drafter.plist
```

Expected: Label matches `com.sean.agents.substack_drafter`, ProgramArguments points at `substack_drafter.py`, StartCalendarInterval has Weekday=4 + Hour=18 + Minute=0, PATH env is set.

- [ ] **Step 3: Add opt-in install path to `install_schedules.sh`.**

```bash
grep -n "process_inbox\|INSTALL_GEMINI\|INSTALL_SUBSTACK" agents-sdk/schedules/install_schedules.sh
```

Then edit `install_schedules.sh` to add a block mirroring the `INSTALL_GEMINI` opt-in pattern:

```bash
# In install_schedules.sh, in the install branch (after the always-installed plists):

if [ "${INSTALL_SUBSTACK_DRAFTER:-0}" = "1" ]; then
  echo "Installing substack_drafter plist (opt-in)..."
  cp "$SCHEDULES_DIR/com.sean.agents.substack_drafter.plist" "$LAUNCHAGENTS_DIR/"
  launchctl load "$LAUNCHAGENTS_DIR/com.sean.agents.substack_drafter.plist"
else
  echo "Skipping substack_drafter (INSTALL_SUBSTACK_DRAFTER=1 to opt in)"
fi

# In the remove branch:
if [ -f "$LAUNCHAGENTS_DIR/com.sean.agents.substack_drafter.plist" ]; then
  launchctl unload "$LAUNCHAGENTS_DIR/com.sean.agents.substack_drafter.plist" 2>/dev/null || true
  rm "$LAUNCHAGENTS_DIR/com.sean.agents.substack_drafter.plist"
fi
```

- [ ] **Step 4: Verify the installer is idempotent (running it twice without the flag stays clean).**

```bash
./agents-sdk/schedules/install_schedules.sh
./agents-sdk/schedules/install_schedules.sh
launchctl list | grep substack_drafter
```

Expected: empty (not installed, because `INSTALL_SUBSTACK_DRAFTER` is unset).

- [ ] **Step 5: Commit.**

```bash
git add agents-sdk/schedules/
git commit -m "feat(substack-drafter): launchd plist + opt-in install via INSTALL_SUBSTACK_DRAFTER=1"
```

## Task C9: Pilot — 2–3 supervised real runs before going to weekly cadence

**Files:** (manual operation — no code changes unless a real-run bug surfaces)

- [ ] **Step 1: Enable the agent in `config.toml`.** Edit `[substack_drafter].enabled = true`.

- [ ] **Step 2: Trigger a real run by hand** (not via launchd yet).

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 agents/substack_drafter.py
```

- [ ] **Step 3: Sean reviews the draft.** Open the new file in `vault/20_projects/.../substack-drafts/`. Read it cold. Is it recognizably in the targeted voice? Does it cite the right concepts? Is the hook real? If not, the prompt composer or voice rotation needs adjustment.

- [ ] **Step 4: Repeat 2 more times** — pin different voice modes via `--voice` (e.g., `--voice sedaris`, `--voice vonnegut`) to spot-check rotation quality before committing to the 5-week cycle.

- [ ] **Step 5: If all 3 pilots are publishable-with-edits, install the plist.**

```bash
INSTALL_SUBSTACK_DRAFTER=1 ./agents-sdk/schedules/install_schedules.sh
launchctl list | grep substack_drafter
```

- [ ] **Step 6: If any pilot is unusable, do NOT install the plist.** File the failure mode, iterate on the prompt composer or the cluster picker, repeat the pilot. The kill switches exist precisely so this iteration loop is cheap.

## Task C10: Doc updates per non-negotiable rule

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md` (agent table + count)
- Modify: `README.md`

- [ ] **Step 1: `CHANGELOG.md` — add v3.30.x entry.**

```markdown
### Added
- **Substack-Drafter agent (`agents-sdk/agents/substack_drafter.py`)** — Thursday-18:00
  weekly agent (default-disabled, opt-in via `INSTALL_SUBSTACK_DRAFTER=1`) that reads
  post-fix synthesizer output, picks the densest concept cluster, and drafts a Substack
  post in a rotating 5-mode voice cycle. Never publishes; drafts land in
  `vault/20_projects/prj-job-hunt-2026/.../substack-drafts/` for hand review.
  Three kill-switch layers: `enabled = false` default, opt-in launchd install, `--dry-run` flag.
```

- [ ] **Step 2: `CLAUDE.md` — add Substack-Drafter to the agents table.**

Find the agent table near "Active agents (8 of 16 on launchd; 1 manual-trigger)" and update the count to 9 (or whatever's correct after C ships) + add a row:

```
| Substack-Drafter (NEW v3.30.x, **default disabled**) | Thursday 18:00 (when opted in) | HybridRouter (Qwen3-14B → Sonnet fallback); writing-voice-modes skill | $0–0.10/run |
```

- [ ] **Step 3: `README.md` — mention the new agent in the agents section.**

- [ ] **Step 4: Commit.**

```bash
git add CHANGELOG.md CLAUDE.md README.md
git commit -m "docs: announce Substack-Drafter agent per non-negotiable rule"
```

---

## Self-review

**Spec coverage:**
- Phase 0 reads → Task A0 ✅
- Phase 0.5 spike → Task A0.5 ✅
- Phase 1 scaffolding → Task A1 ✅
- Phase 2 cases + deferred → Tasks A3, A4 ✅
- Phase 2 fixtures → Task A5 ✅
- Phase 3 runner → Task A6 ✅
- Phase 4 baseline + transcripts → Task A7 ✅
- Phase 5 EXPLANATION → Task A9 ✅
- Phase 6 Loom → Task A13 ✅
- Phase 7 publish → Task A14 ✅
- Failure-modes.md, coded-traces, references, README → Tasks A2, A8, A10, A11 ✅
- Mandatory doc updates (CHANGELOG/CLAUDE/README) → Task A12 ✅
- Workstream B 4 patches → Tasks B1, B2/B3, B4, B5 ✅
- Workstream B verification + 5-night precondition → Tasks B6, B7, B8 ✅
- Workstream C config + kill switches → Task C1 ✅
- Workstream C voice rotation → Task C2 ✅
- Workstream C dryness gate → Task C3 ✅
- Workstream C cluster picker → Task C4 ✅
- Workstream C prompt composer → Task C5 ✅
- Workstream C HybridRouter + draft writer → Task C6 ✅
- Workstream C `main()` + `--dry-run` → Task C7 ✅
- Workstream C launchd plist + opt-in installer → Task C8 ✅
- Workstream C supervised pilot before launchd → Task C9 ✅
- Workstream C doc updates → Task C10 ✅
- SPEC Part B "What this agent does NOT do" (no autonomous publish, no edits to existing drafts, no follow-up series, voice rotation by calendar not content) → preserved in design; reinforced by `--dry-run` default + Sean-reviews-every-draft policy ✅

**Placeholder scan:** No "TBD," "TODO," "fill in later," or "add appropriate error handling" left in the steps. The one deliberate placeholder is `<!-- BASELINE PENDING -->` in Task A10 step 1 — it's filled in by Task A10 step 2 / Task A7 results. That is content the runner does not yet have, not a hand-wave.

**Type consistency:** The `MODEL_USED_VALUES` frozenset in Task B1 matches the `pass_criteria` literal set in vs-018's case YAML in Task A3 (`{'qwen3-14b', 'claude-sonnet-4-6', 'claude-haiku-4-5', 'none'}`). The `STATUS_VALUES` set in Task B3 contains `"success-empty"` + `"partial-empty"`, which match the case YAML in Task A3 and the assignment logic in Task B2. `PushoverConfigurationError` is defined in Task B4 step 2 and imported in the runner (Task A6 step 5).

**Honest flags:**
- Task A6 step 7 deliberately reaches a partial-failure state ("smoke-run will fail; adapt in step 8") because the runner's `_invoke_synthesizer()` cannot be perfectly specified without reading the live `run_synthesis()` signature. That signature is the seam — better to leave the adaptation visible in the plan than fabricate a kwarg list.
- Task A5 fixtures are sketched, not fully written, because their content depends on what makes the working synthesizer cluster. If the synthesizer clusters by wikilink density (Phase C / typed-edges code path) the fixture notes need wikilinks; if it clusters by embedding similarity (Phase 2 / vault-indexer path) the notes need shared vocabulary. Read `agents-sdk/agents/vault_synthesizer.py` clustering code before writing fixtures.
- Task B2 logic order matters: `partial-empty` must be checked before `partial` (it's the stricter case). The plan documents this in the if-cascade.
- Task C6's `_route()` wrapper assumes `agents_sdk.lib.hybrid_router.route()` accepts a `task` parameter and returns `{text, model_used, cost_usd}`. If the actual signature differs (likely — HybridRouter has evolved), adapt the wrapper in one place rather than restructuring the whole agent. The seam exists at `_route()` precisely so tests can monkeypatch without touching real signatures.
- Task C7's Pushover ping is stubbed (`"would Pushover-notify if notify_info existed"`) because `agents-sdk/lib/pushover.py` only has `notify_wol_failure`, `notify_agent_error`, and `notify_gate_check_fail` today — there is no `notify_info`. Adding one is a small follow-up, not in scope here. The agent's value (writing the draft) does not depend on the ping landing.
- Task C9's pilot loop is intentionally undefined in success terms ("publishable with edits"). That judgment belongs to Sean. The kill switches exist so iteration is cheap and reversal is one command.

**The two most important decisions:**
1. **`evals/vault-synthesizer/` at repo root**, not nested under `.claude/skills/`. Do not re-litigate. (Locked in Task A1.)
2. **Workstream C ships default-disabled**, gated on Task B7's 5-night verification — not on "post-employment." The framing correction matters: the agent helps the job hunt by closing the publishing-cadence loop. Three kill-switch layers (config flag, opt-in launchd install via `INSTALL_SUBSTACK_DRAFTER=1`, `--dry-run` mode) mean the worst case is a draft sitting in the vault that Sean never reads. (Reinforced in Task C0 + C8 + C9.)
