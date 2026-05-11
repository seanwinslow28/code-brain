---
type: build-plan
project: prj-job-hunt-2026
artifact: vault-synthesizer-evals
created: 2026-05-10
status: ready-for-execution
target_ship_date: 2026-05-22  # Friday Week 2 of the 8-week sprint
target_loom_date: 2026-05-21
target_substack_date: 2026-05-22  # paired with the Sedaris draft
target_followup_substack_date: 2026-05-29  # after synthesizer fix lands
companion_artifacts:
  - 2026-05-10-evals-error-analysis-real-logs.md   # the data foundation
  - 2026-05-10-the-night-my-vault-said-nothing.md   # Sedaris draft
  - 2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md   # Kerouac variant
execution_consumer: claude-code-with-superpowers
superpowers_repo: https://github.com/obra/superpowers.git
ai-context: "Self-contained build plan for the vault-synthesizer eval suite + the new Substack-Drafter agent. Designed to be loaded into Claude Code as the planning input for an obra/superpowers Plan Mode session, then executed phase-by-phase. References every file Claude Code must read before starting. Phase 0 reads, scope locks, verification gates included."
---

# Build Plan — Vault Synthesizer Eval Suite + Substack-Drafter Agent

> **Read this before doing anything else.** This plan has two coupled artifacts: (A) the eval suite that ships as a 6th flagship portfolio piece, and (B) the new Substack-Drafter agent that closes the publishing-cadence loop. (A) ships first (Week 2 Friday). (B) is post-employment-priority, but specced here so it lives inside one coherent build document.

---

## Why this document exists

I did the error analysis Hamel and Anthropic both insist on before writing any eval cases. That analysis is at [`2026-05-10-evals-error-analysis-real-logs.md`](2026-05-10-evals-error-analysis-real-logs.md). It surfaced something more interesting than I expected — a 9-day silent regression in the vault synthesizer that my own monitoring chain was reporting as healthy. That finding reshaped the eval suite scope: the pre-drafted YAML hallucination cases mostly get deferred, and six new cases grounded in real observed failures take their place.

The build plan below sequences that work. It is also designed to seed a Plan Mode session in Claude Code using the [obra/superpowers](https://github.com/obra/superpowers.git) skill pack — every phase has explicit files-to-create, files-to-modify, commands-to-run, and verification gates so the planning skills can render the work as a clean execution graph.

---

## Phase 0 — Pre-execution Reads (do not skip)

Claude Code must read these files (in this order) before producing a Phase-Mode plan. They establish the scope, the constraints, the source data, and the don't-build list.

| Order | File | Why |
|---|---|---|
| 1 | [`CLAUDE.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/CLAUDE.md) | Non-negotiable rules, agent-fleet topology, Phase D + Phase 6 history, launchd PATH requirement |
| 2 | [`2026-05-06-unified-roadmap.md`](2026-05-06-unified-roadmap.md) | Tier-A truths, 8-week sprint, Task 6 §I scope (eval fluency Week 5, publication Week 7 → now upgraded to Week 2 ship) |
| 3 | [`2026-05-10-evals-error-analysis-real-logs.md`](2026-05-10-evals-error-analysis-real-logs.md) | The data foundation — six-mode failure taxonomy grounded in 17 days of real logs |
| 4 | [`agents-sdk/agents/vault_synthesizer.py`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/vault_synthesizer.py) | Lines 320–420 (per-file loop, status promotion) and lines 580–660 (manifest write path). The synthesizer fix must touch both. |
| 5 | [`agents-sdk/config.toml`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/config.toml) | Cost caps, paths, safety limits — any new agent must inherit these |
| 6 | [`agents-sdk/schedules/install_schedules.sh`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/schedules/install_schedules.sh) | launchd plist installer pattern (the `PATH` env var fix is non-optional) |
| 7 | [`.claude/skills/writing-voice-modes/SKILL.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/writing-voice-modes/SKILL.md) | The 5 voice modes + signature moves the Substack-Drafter agent depends on |
| 8 | [`vault/40_knowledge/references/ref-anthropic-demystifying-agent-evals.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/40_knowledge/references/ref-anthropic-demystifying-agent-evals.md) | Anthropic's 8-step playbook + 3 grader-type framework — vocabulary alignment |
| 9 | [`vault/20_projects/research/2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/research/2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md) | Pre-drafted YAML cases (vs-001 → vs-015); vs-014 and vs-015 are the keeps |
| 10 | [`vault/20_projects/research/2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/research/2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md) | Pre-drafted YAML cases (vs-001 → vs-013); vs-012 and vs-013 are the keeps |

After reading these, Claude Code should produce a phase-by-phase execution plan against the structure below. **Do not start work without producing the plan first.**

---

## Scope Lock — what ships, what doesn't

### Ships in Phase 1 (Eval Suite — Friday Week 2, 2026-05-22)

1. New directory: `.claude/skills/agents-sdk/evals/vault-synthesizer/` (or `evals/vault-synthesizer/` at repo root — Claude Code decides on the conventional location; see Phase 1 below)
2. `README.md` — what this is, how to run, current baseline pass rate
3. `cases.yaml` — 10 binary pass/fail cases (6 new + 4 retained from pre-drafts)
4. `deferred-cases.yaml` — 11 hallucination/drift cases set aside until the synthesizer is alive again
5. `runner.py` — ~100-line pytest harness, local-only, no platform deps
6. `failure-modes.md` — the taxonomy from the error-analysis doc, restated as the README of the cases.yaml
7. `EXPLANATION.md` — 4Q comprehension artifact (the portfolio hook)
8. `traces/coded-traces.md` — the open-coded log evidence (5–10 representative excerpts from the actual stderr + manifests)
9. `references.md` — sources index + interview-vocabulary cheat-sheet
10. Updates to: [`CHANGELOG.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/CHANGELOG.md), [`CLAUDE.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/CLAUDE.md), [`README.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/README.md) — per non-negotiable rule "Mandatory doc updates"

### Ships in Phase 2 (Synthesizer Fix — between Friday Week 2 and Friday Week 3)

1. Patch `agents-sdk/agents/vault_synthesizer.py` — status taxonomy adds `success-empty` and `partial-empty`; per-file LLM-failure exceptions promote the run-level status; `model_used` becomes a proper enum; warnings surface in the result
2. Patch the Pushover notify path — boot-time credential check; missing creds = `ConfigurationError`, not silent-log-and-continue
3. Patch the Daily Driver morning brief — when synth manifest has `status == "success-empty"` or `concepts_written == 0`, surface as a WARNING, not "ok"
4. Run the eval suite once against the patched synthesizer — confirm pass rate jumps from the Phase-1 baseline (which is intentionally low) to a real number

### Ships in Phase 3 (Substack-Drafter Agent — POST-EMPLOYMENT priority, specced here for completeness)

See full spec in §B below.

### Does NOT ship — the don't-build list

These are all real temptations. Each is post-employment Q3 work per both research docs.

- ❌ GitHub Actions CI/CD wiring with pass-rate gates (Anthropic Step 8 territory — comes after a stable baseline)
- ❌ A generic abstracted eval framework Python package
- ❌ Braintrust / Langfuse / LangSmith / Phoenix integration
- ❌ Cross-model comparison tooling (Qwen3-14B vs Sonnet 4.6, etc.)
- ❌ Coverage metrics dashboards (Metabase/Grafana)
- ❌ Inter-annotator agreement studies
- ❌ The Substack-Drafter agent being installed on a launchd schedule (it ships disabled-by-default; only enable post-employment)

---

# PART A — EVAL SUITE BUILD PHASES

## Phase 1 — Directory + Scaffolding (estimated 60 min)

### Files to create

```
evals/vault-synthesizer/
├── README.md
├── cases.yaml
├── deferred-cases.yaml
├── runner.py
├── failure-modes.md
├── EXPLANATION.md
├── traces/
│   └── coded-traces.md
└── references.md
```

### Decision: where does `evals/` live?

Two reasonable options. Claude Code should pick one in Plan Mode and stick with it:

- **Option A:** `evals/vault-synthesizer/` at repo root. Cleaner discoverability for recruiters browsing the repo. Matches Anthropic-canonical convention.
- **Option B:** `.claude/skills/agents-sdk-evals/vault-synthesizer/` nested under skills. Keeps the eval suite co-located with the agent stack it tests.

**Recommendation:** Option A (repo root). It's the first thing a recruiter sees when they open the GitHub page. Update `CLAUDE.md` architecture diagram accordingly.

### README.md content checklist

- [ ] Opening paragraph in Sean Mode at 60% (per `writing-voice-modes`): what this is, why it exists, who it's for
- [ ] Quickstart: `python evals/vault-synthesizer/runner.py`
- [ ] Current baseline pass rate (filled in after Phase 4)
- [ ] Brief note on the failure taxonomy → link to `failure-modes.md`
- [ ] Link to `EXPLANATION.md` for the 4Q
- [ ] Sources block

### Verification gate

`ls evals/vault-synthesizer/` returns the 7 expected files + 1 directory. README opens with a recruiter-readable cold paragraph.

---

## Phase 2 — Write `cases.yaml` and `deferred-cases.yaml` (estimated 90 min)

### `cases.yaml` — the 10 active cases

Each case is binary pass/fail. Each has: `id`, `category`, `description`, `failure_mode_under_test`, `input` (mocked synthesizer inputs or real manifest fixtures), `expected_output` (pass condition), `judge_type` (exact-match | rubric | llm-judge), `pass_criteria`.

#### Retained from pre-drafts (4 cases)

| ID | Source | Failure mode |
|---|---|---|
| vs-014 | Perplexity §6 | Silent omission — synthesizer fails to emit concept article for 5+ note corpus |
| vs-015 | Perplexity §6 | Silent empty output — `status="ok"` with zero outputs (LIVE failure mode, promoted to load-bearing) |
| vs-012 | Gemini §6 | Source-attribution loss (deferred semantics until synthesizer runs) |
| vs-013 | Gemini §6 | Stale-content overweighting (deferred semantics until synthesizer runs) |

#### New cases grounded in real-log evidence (6 cases)

| ID | Failure mode (from `failure-modes.md`) | Judge type |
|---|---|---|
| vs-016 | Status-field misreport — mocked LLM caller raises `ConnectionRefusedError` on every file; assert `result.status != "ok"` | exact-match |
| vs-017 | Status-field collapse — run to budget timeout with zero LLM successes; assert `result.status` distinguishes `partial-some-output` from `partial-empty` | exact-match |
| vs-018 | Empty-string `model_used` rejection — assert `model_used` is one of the valid enum values, never `""` | exact-match |
| vs-019 | Pushover credentials health check — on synthesizer boot with missing creds, assert `ConfigurationError` raised before any LLM call attempt | exact-match |
| vs-020 | Knowledge-index integrity — assert `vault/knowledge/index.md` count of concept entries matches the count of files in `vault/knowledge/concepts/` | rubric |
| vs-021 | Daily-driver brief consumer check — mocked synth-manifest with `status="success-empty"`; assert morning brief surfaces it as WARNING | llm-judge |

### `deferred-cases.yaml` — the 11 cases set aside

Lift vs-001 → vs-011 verbatim from the Perplexity primer §6 and Gemini primer §6. Top-of-file note:

```yaml
# Deferred cases — re-enable when synthesizer produces ≥1 concept article in a clean run.
# These test hallucination, edge-confidence, relation-tag drift, and temporal confusion.
# All are valid; none can fire on the current system because the LLM call has not
# successfully completed in at least 9 nights (see ../failure-modes.md).
```

### Verification gate

- All 10 active cases parse as valid YAML.
- Each case has every required field.
- The mocked inputs for vs-016, vs-017, vs-018 are tight enough to fail the current synthesizer code AS WRITTEN (this is the point — they're a regression suite for the fix that's coming in Phase 2 of the broader build).

---

## Phase 3 — `runner.py` (estimated 90 min)

### Architecture

~100 lines of Python. Pytest-compatible. No external dependencies beyond `pyyaml`, `pytest`, and whatever is already in `agents-sdk/.venv`.

```python
# runner.py — pseudocode
import yaml
import pytest
from pathlib import Path
from agents_sdk.agents import vault_synthesizer
from agents_sdk.lib.hybrid_router import HybridRouter

CASES = yaml.safe_load(Path("cases.yaml").read_text())

@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_case(case):
    # 1. Build mocked synthesizer inputs from case["input"]
    # 2. Invoke vault_synthesizer.run_synthesis() with mocks
    # 3. Apply grader per case["judge_type"]
    #    - exact-match: direct assertion
    #    - rubric: structured check against expected_output
    #    - llm-judge: call Claude Haiku with critique-shadowing prompt
    # 4. assert pass per case["pass_criteria"]
```

### Three grader implementations (per Anthropic's framework, ordered by preference)

1. **Code-based (exact-match)** — direct Python assertion. ~70% of cases. Fast, deterministic, free.
2. **Rubric** — structured Python check over the synthesizer output (e.g. "every concept article body contains at least one filename reference"). ~20% of cases.
3. **LLM-as-judge (Claude Haiku with critique-shadowing)** — for the one or two cases that genuinely need semantic judgment (vs-021's "is this WARNING text clear?"). ~10% of cases.

### Mocking strategy

The cases that test failure modes (vs-016, vs-017, vs-018) mock the `llm_caller` parameter that `run_synthesis()` already accepts. The synthesizer was designed test-friendly — the mock is a one-line lambda that raises the desired exception.

The cases that test output content (vs-014, vs-020) use a real fixture set: 5–10 mock daily notes loaded from `evals/vault-synthesizer/traces/fixtures/`.

### Output

A markdown results table written to `evals/vault-synthesizer/last-run.md` after every invocation:

```markdown
# Vault Synthesizer Eval Run — 2026-05-22T14:31:02

| ID | Category | Result | Notes |
|---|---|---|---|
| vs-014 | output-completeness | ❌ FAIL | (expected — synthesizer can't emit; will pass after Phase 2 fix) |
| vs-015 | output-completeness | ❌ FAIL | (expected — load-bearing case) |
| vs-016 | status-misreport | ❌ FAIL | status field promoted to "ok" despite all-file LLM failures |
| vs-017 | status-misreport | ❌ FAIL | status taxonomy missing `partial-empty` value |
| vs-018 | schema-integrity | ❌ FAIL | model_used="" returned, not enum |
| vs-019 | config-fail-loud | ❌ FAIL | Pushover missing creds logged-and-ignored, no ConfigurationError raised |
| vs-020 | index-integrity | ✅ PASS | index.md and disk both empty — consistent |
| vs-021 | downstream-consumer | ❌ FAIL | morning brief reads status="ok", surfaces as healthy |
| vs-012 | source-attribution | ⏸️ SKIPPED | requires live synthesizer output; deferred until Phase 2 fix |
| vs-013 | stale-overweighting | ⏸️ SKIPPED | requires live synthesizer output; deferred until Phase 2 fix |

**Baseline pass rate: 1/10 (10%) — by design.** The 8 failures are the failure modes the fix needs to address.
```

### Verification gate

- `python evals/vault-synthesizer/runner.py` runs to completion without infrastructure errors.
- The result table renders cleanly.
- The baseline pass rate is genuinely low (somewhere in the 10–20% range). Anthropic Step 5: *if you're passing 100% of your evals, you're not challenging the system enough.*

---

## Phase 4 — First Baseline Run + Transcript Reading (estimated 45 min)

Per Anthropic Step 6: *Read the transcripts.* This phase is non-negotiable. Run the suite. For every failure, read the actual synthesizer output (or the synthesizer's stderr lines, or the mocked-grader output). Ask: was this a real synthesizer failure, or did my grader misfire?

### Outcome

A `traces/baseline-run-2026-05-22.md` file documenting which failures are real vs. grader-side. Fix any grader bugs. Re-run. Lock the baseline.

### Verification gate

The baseline number in `README.md` is filled in. Every failure in `last-run.md` has been reviewed and classified (real failure vs. grader bug). No grader bugs remain.

---

## Phase 5 — `EXPLANATION.md` 4Q Artifact (estimated 60 min)

The portfolio hook. Per the unified roadmap's Task 1, this follows the standard 4Q template.

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
as the vault evolves — quarterly refresh. (3) The LLM-as-judge case (vs-021)
requires Claude Haiku availability; on offline runs, this case is skipped
not failed.

## What did I learn?
That evals aren't really about hallucinations. The failure modes I imagined —
hallucinated phase numbers, relation-tag drift, temporal confusion — were the
easy cases. The hard case was the one nobody drafts on purpose: the
status field that says "ok" while the output is empty. Three layers of
monitoring agreed everything was fine while the system underneath them rotted
silently for nine days. Error analysis surfaces the failures imagination does
not.
```

### Verification gate

`EXPLANATION.md` is recruiter-readable cold in under 90 seconds (test this — open in a private browser).

---

## Phase 6 — Loom Recording (Sean owns this — 30 min)

5-minute unedited screen recording. Shot list:

1. **0:00 – 0:30** — Open `evals/vault-synthesizer/README.md` in browser preview. Read the opening paragraph aloud.
2. **0:30 – 1:30** — Show `failure-modes.md`. Walk Mode 1 (silent empty output) with a sentence each. Land on the real evidence: open one of the manifest JSON files, show `concepts_written: 0` with `status: "ok"`.
3. **1:30 – 3:00** — Run the suite live. `python evals/vault-synthesizer/runner.py`. Let the output scroll. Narrate one PASS and one FAIL.
4. **3:00 – 4:00** — Open one transcript from `traces/baseline-run-2026-05-22.md`. Read 3–4 lines aloud. Explain what the grader saw.
5. **4:00 – 5:00** — Close on the EXPLANATION.md "What did I learn?" paragraph. Read aloud. Stop recording.

Don't polish. Re-shoot only if Claude Code's CLI errors out mid-recording. The transparency IS the credential.

---

## Phase 7 — Substack + LinkedIn Publish (Friday Week 2 — 60 min)

### Friday 2026-05-22 — primary publication

Publish the [Sedaris draft](../substack-drafts/2026-05-10-the-night-my-vault-said-nothing.md) on Substack. Title: "The Night My Vault Said Nothing." Embed the Loom. Link the GitHub directory. Sign off with the eval-suite link.

Decide before publishing: Sedaris primary OR Kerouac variant. The Kerouac variant lives at [`2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md`](../substack-drafts/2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md). Recommendation: ship Sedaris first; hold Kerouac for the follow-up post if voice rotation feels right.

### Following Wednesday 2026-05-27 — LinkedIn syndication

Adapt the same post to LinkedIn format (~600 words, scannable). Drop the section breaks. Keep the JSON snippet.

### Friday 2026-05-29 — follow-up post

After Phase 2 (synthesizer fix) lands, publish the resolution post. Voice: try Kerouac if Sean is comfortable. Title candidates: "The Night My Vault Started Talking Again" / "Three Layers, Patched."

---

# PART B — SUBSTACK-DRAFTER AGENT SPEC (post-employment build)

## Why this agent exists

The hardest part of writing-in-public is consistency. Sean has built fourteen agents that maintain a vault, run research, lint knowledge, and flush sessions. None of those agents turn the resulting synthesis into Substack-ready drafts. The Substack post that publishes Friday Week 2 is hand-written. The post that publishes Friday Week 6 will be hand-written. By Week 8, the cadence is at risk of falling off because the writing block is the rate-limiting step.

The Substack-Drafter agent closes that loop. It watches the post-fix vault synthesizer's output, picks a synthesis cluster worth writing about, pulls in connected research from `vault/40_knowledge/`, and drafts a Substack post in a rotating voice mode from `writing-voice-modes`. Sean reviews and publishes; the agent never publishes anything autonomously.

## Agent design

### Name

`substack_drafter.py` — lives at `agents-sdk/agents/substack_drafter.py`

### Schedule

**Default: disabled.** Install plist ships disabled (per `agents-sdk/schedules/install_schedules.sh` precedent for `process_inbox`). Enable opt-in via `INSTALL_SUBSTACK_DRAFTER=1`.

When enabled: **Thursday 18:00 weekly.** This gives Sean Friday morning to review, edit, and publish.

### Inputs

1. **`vault/health/synth-manifest-*.json`** — last 7 nights. Skip if last 3 runs had `concepts_written == 0` (graceful degradation — don't draft if there's no fresh synthesis to draft about).
2. **`vault/knowledge/concepts/*.md`** — last 14 days. Picks the cluster of 3–5 concepts with the densest interconnection.
3. **`vault/knowledge/connections/*.md`** — same window. Provides the angle/argument.
4. **`vault/knowledge/qa/*.md`** (Phase C, v3.19.0) — any Q&A artifacts in the same date window. These contain Sean's actual questions, which often make good Substack hooks.
5. **`vault/40_knowledge/references/`** — pulled by similarity (using the existing nomic-embed-text index at `vault/.vault-index.db`) to ground the post in real source material.
6. **`vault/20_projects/research/*.md`** — same similarity pull. Last 30 days only.
7. **`.claude/skills/writing-voice-modes/SKILL.md`** — the voice modes spec. Loaded as system prompt context.

### Voice rotation

The agent rotates through the 5 voice modes on a 5-week cycle to keep the Substack from feeling monotone:

| Week of year mod 5 | Voice mode | Use case |
|---|---|---|
| 0 | Sedaris (Domestic Observer) | Default — comedic, narrative-driven |
| 1 | Kerouac (Beat Flow) | Discovery-heavy posts, sensory-rich |
| 2 | Thompson (Gonzo Technical) | Post-mortems, product reviews |
| 3 | Vonnegut (Minimalist Absurdist) | Short-form, refrain-driven |
| 4 | Sean Mode (Hybrid default) | Anything else |

Override: a `voice:` field in the run config can pin a specific mode.

### Process

```
1. Read synth-manifest for last 7 days
   - if last 3 manifests have concepts_written == 0 → exit 0 with note
     "synthesizer dry, no draft generated"
2. Read concepts/, connections/, qa/ for last 14 days
   - cluster by wikilink density (≥3 shared wikilinks = same cluster)
   - pick the densest cluster
3. Pull similarity-matched references from vault/40_knowledge/ and
   vault/20_projects/research/
4. Compose system prompt:
   - load writing-voice-modes SKILL.md
   - select current week's voice mode
   - inject 4Q template structure
5. Compose user prompt:
   - "Draft a 1200-1500 word Substack post in {voice_mode} voice
      about the connections between {concept_a}, {concept_b}, {concept_c}.
      Ground in these sources: {references}. Hook in the first 2 sentences.
      Use {voice_mode}'s signature moves from the skill spec."
6. Call HybridRouter route to MBP Qwen3-14B (fallback Sonnet 4.6)
7. Write draft to vault/20_projects/prj-job-hunt-2026/.../substack-drafts/
   - filename: YYYY-MM-DD-agent-draft-{slug}.md
   - frontmatter includes voice, source_concepts, source_connections,
     source_references, generated_at, cost_usd
8. Append run to vault/90_system/agent-logs/agent-run-history.csv
9. Send Pushover ping (after Phase 2 fix lands the cred check):
   "Substack draft ready for review: {filename}"
```

### Outputs

- One markdown draft per week at `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/YYYY-MM-DD-agent-draft-{slug}.md`
- Run line in `agent-run-history.csv`
- Pushover notification (informational only, never decision-forcing)

### Cost cap

`max_cost_usd = 0.10` per run. Qwen3-14B local is free; Sonnet fallback for a 1500-word draft is ~$0.05. Hard cap is a safety net.

### Kill switch

Three layers:
1. `enabled = false` in `agents-sdk/config.toml` `[substack_drafter]` table (default-off)
2. launchd plist not installed unless `INSTALL_SUBSTACK_DRAFTER=1` flag passed to `install_schedules.sh`
3. `--dry-run` flag prints the prompt but does not call the LLM

### Verification gates (when implementing post-employment)

- [ ] Agent runs end-to-end in `--dry-run` mode, prints a complete prompt, exits 0
- [ ] Real run produces a draft file with valid frontmatter
- [ ] Draft is recognizably in the targeted voice mode (Sean sanity-checks 2–3 generated drafts before going to weekly cadence)
- [ ] Cost stays under $0.10 across 5 real runs
- [ ] The agent gracefully no-ops when the synthesizer has been dry for 3 nights
- [ ] Sean can disable in one command: `./agents-sdk/schedules/install_schedules.sh --remove-substack-drafter`

### What this agent does NOT do

- It does not publish to Substack. Drafts land in the vault; Sean publishes by hand.
- It does not edit existing drafts. New drafts only.
- It does not write follow-up posts or threaded series autonomously.
- It does not select voice mode based on content (only based on calendar rotation) — this is a deliberate constraint to avoid creating a system that optimizes for engagement instead of authenticity.

### Tier-A check

- Walk-away $100k: N/A
- AI > Tech > Creative PM track: ✅ this agent demonstrates the same exact pattern Anthropic FDE / Sierra would want a candidate to have built
- Agents draft / Sean sends: ✅ this is the canonical implementation of that Tier-A truth
- Track-C protected: ✅ post-employment build, doesn't touch the May 25 MCP ship
- 5:30 PM hard stop: ✅ agent runs on its own schedule, no work time consumed

### Roadmap fit

Goes into the unified roadmap as **Task 9 — Substack-Drafter Agent (post-employment Q3 build, specced now)**. Becomes the 7th flagship portfolio artifact when it ships. Pairs naturally with the Substack series as the demonstration of the "build agents that close your own loops" thesis.

---

# Appendix — Files Referenced In This Plan

## Source data (read-only)

- [`vault/health/synth-manifest-2026-05-{02,03,06,07,08,09,10}.json`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/health/) — primary error-analysis evidence
- [`vault/90_system/agent-logs/vault-synthesizer-stderr.log`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/vault-synthesizer-stderr.log) — Mode 5 evidence (Pushover credential failure)
- [`vault/90_system/agent-logs/vault-synthesizer-2026-05-{08,09,10}.log`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/) — successful-status-but-empty evidence
- [`vault/knowledge/index.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/knowledge/index.md) — empty-state confirmation

## Code to read (and patch in Phase 2)

- [`agents-sdk/agents/vault_synthesizer.py`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/vault_synthesizer.py) — run_synthesis() lines 320–420; manifest write path 580–660
- [`agents-sdk/lib/hybrid_router.py`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/lib/hybrid_router.py) — `WOLUnavailable` exception class, route decisions
- [`agents-sdk/agents/daily_driver.py`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/daily_driver.py) — morning brief consumer of synth-manifest (search "Vault Health" section)
- [`agents-sdk/config.toml`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/config.toml) — agent config inheritance

## Reference / canon (read-only)

- [`vault/40_knowledge/references/ref-anthropic-demystifying-agent-evals.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/40_knowledge/references/ref-anthropic-demystifying-agent-evals.md)
- [`vault/20_projects/research/2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/research/2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md)
- [`vault/20_projects/research/2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/research/2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md)

## This artifact set

- [`2026-05-10-evals-error-analysis-real-logs.md`](2026-05-10-evals-error-analysis-real-logs.md) — the data foundation
- [`../substack-drafts/2026-05-10-the-night-my-vault-said-nothing.md`](../substack-drafts/2026-05-10-the-night-my-vault-said-nothing.md) — Sedaris primary draft
- [`../substack-drafts/2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md`](../substack-drafts/2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md) — Kerouac variant
- [`2026-05-06-unified-roadmap.md`](2026-05-06-unified-roadmap.md) — canonical 8-week roadmap (this artifact updates it)

## Skills to load

- [`.claude/skills/writing-voice-modes/SKILL.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/writing-voice-modes/SKILL.md) — required for both Phase 7 publishing and Part B agent
- [`.claude/skills/intent-engineering/SKILL.md`](/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/intent-engineering/SKILL.md) — for cross-checking this plan's intent spec quality (dogfood opportunity)

## Superpowers integration

`obra/superpowers` skill pack provides Plan Mode templates, structured task graphs, and verification patterns. To use:

1. Clone or symlink the superpowers repo into the appropriate skills location
2. In Claude Code, open Plan Mode (`Shift+Tab` twice)
3. Load this build plan: *"Read `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-10-eval-suite-build-plan.md` and produce a Plan-Mode execution graph against Phase 0 reads + Phase 1–7 phases. Stop at verification gates between phases."*
4. Review the graph, approve or adjust
5. Execute phase-by-phase, with Claude Code marking verification gates as it goes

---

## Self-review

**Spec coverage:** Phase 0 (10 reads), Phase 1 (scaffolding), Phase 2 (cases), Phase 3 (runner), Phase 4 (baseline), Phase 5 (4Q), Phase 6 (Loom shotlist), Phase 7 (publishing). Part B specs the Substack-Drafter agent with schedule, voice rotation, kill switches, and verification gates. All files referenced have absolute paths. Don't-build list is explicit.

**Tier-A check:**
- ✅ Track-C (2026-05-25 MCP ship) protected — eval suite is parallel work, not on the critical path
- ✅ Walk-away $100k floor: N/A
- ✅ Agents draft / Sean sends: Part B explicitly preserves this
- ✅ Friday 4:30 retro: untouched
- ✅ 5:30 PM hard stop: Part A sized for one deep-work day; Part B is post-employment
- ✅ Block IP scrub: no Block references in any of the deliverables

**Honest flags:**
- Phase 3's runner.py assumes the synthesizer's `run_synthesis()` test surface is clean. It is (the `llm_caller` parameter is dependency-injected). If `agents-sdk` evolves before Phase 3 lands, refactor before writing the runner.
- The Substack-Drafter agent (Part B) depends on the synthesizer being alive again. Don't try to ship it before Phase 2 (synthesizer fix) lands and `vault/knowledge/concepts/` starts populating.
- The Kerouac variant is a voice test, not a publish decision. Sean reviews both drafts and decides which Substack rhythm he wants. The Sedaris draft is the safer first publication; Kerouac is the higher-risk-higher-reward second.

**The single most important decision in this plan:** Where `evals/` lives. Repo root vs. nested under `.claude/skills/agents-sdk-evals/`. Decide in Plan Mode, then commit. Don't drift.

---

*Plan ends here. Claude Code: produce the Plan-Mode execution graph against this document and stop.*
