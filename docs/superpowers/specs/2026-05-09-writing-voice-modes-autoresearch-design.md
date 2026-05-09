---
title: AutoResearch Optimization for `writing-voice-modes` Skill
date: 2026-05-09
status: design — approved, awaiting user spec review
owner: Sean Winslow
domain: claude-code-superuser-pack / agents-sdk
related:
  - autoresearch-skill-optimizer-prompt.md (root prompt that triggered this work)
  - .claude/skills/writing-voice-modes/SKILL.md (artifact being optimized)
  - .claude/skills/writing-voice-modes/references/voice-samples.md (calibration anchors)
  - agents-sdk/agents/daily_driver.py (architectural pattern reference)
---

# AutoResearch Optimization for `writing-voice-modes`

## 1. Context

Karpathy's autoresearch pattern (March 2026) gives an AI agent a mutable artifact, a measurable metric, and English-language instructions, then runs an autonomous optimize→measure→keep-or-revert loop. We are adapting that pattern to optimize the body of `.claude/skills/writing-voice-modes/SKILL.md` against a hybrid eval suite (deterministic structural checks + LLM-judge binary evaluations) so that the skill produces output that more reliably sounds like Sean Winslow's voice for Substack blog posts.

This spec is for **a one-skill prototype** — validate the loop end-to-end against `writing-voice-modes` before generalizing. The goal is not just "improve this one skill" but "produce a working harness we can reuse for other skills in `.claude/skills/`."

## 2. Scope

**In scope:**
- A new agent `agents-sdk/agents/skill_optimizer.py` that runs the autoresearch loop for one skill
- An eval suite YAML schema co-located with the target skill (`evals.yaml` + `evals.sealed.yaml`)
- Three new shared modules in `agents-sdk/lib/skill_optimizer/`: judge runner, structural-check runner, stylometric distance computer, mutation guard, trip-wire monitor
- A judge prompt template + results.tsv schema
- `config.toml` additions for `[agents.skill_optimizer]`
- A pre-flight requirement: Sean writes 2 short 60%-dial samples to add to `voice-samples.md` before iteration 1

**Out of scope:**
- launchd scheduling (this is a manually-triggered prototype, not a daily agent)
- Automatic generalization to other skills (that's Phase 5 work, after the prototype validates)
- Vision-based eval (writing-voice-modes is text-only)
- Optimizing prompts other than the body of `SKILL.md` (frontmatter, examples, references are explicitly locked)
- The `prompt-engineering` and `skill-system-mastery` meta-skills (per autoresearch hard constraint #10)

## 3. Architecture (3-file mapping)

| Karpathy original | Our adaptation | Path |
|---|---|---|
| `prepare.py` (FIXED) | `skill_optimizer.py` orchestrator + `evals.yaml` + judge prompt template + structural-check Python | `agents-sdk/agents/skill_optimizer.py`, `.claude/skills/writing-voice-modes/evals.yaml`, `agents-sdk/lib/skill_optimizer/judge_prompt.txt`, `agents-sdk/lib/skill_optimizer/structural_checks.py` |
| `train.py` (MUTABLE) | The body of `SKILL.md` (frontmatter + locked sections protected by pre-write diff guard) | `.claude/skills/writing-voice-modes/SKILL.md` |
| `program.md` (instructions) | Master optimizer instructions consumed by the mutation subagent | `agents-sdk/lib/skill_optimizer/program.md` |
| `val_bpb` (single metric) | Composite training-set pass rate: `total_yes / (5 prompts × 15 runs × 6 criteria)` = `passes / 450` | computed in-memory; logged to results.tsv |
| `results.tsv` (log) | Per-iteration TSV with mutation summary, scores, deltas, trip-wire flags | `agents-sdk/data/skill-optimizer/writing-voice-modes-results.tsv` |

## 4. Eval Suite Design

### 4.1 Test prompts — three tiers

All 10 prompts are 250-word Substack blog post intros. Topic diversity is intentional: training prompts and surprise prompts share modes but cover different content so we can detect overfitting to specific phrasing.

**Training set (5 prompts — optimizer sees scores)**
| ID | Mode | Prompt |
|---|---|---|
| `sean_quitting_job` | Sean Mode | Write a 250-word Substack blog post intro about quitting your day job to bet on AI. Sean Mode, full intensity. |
| `sedaris_coffee_ritual` | Domestic Observer | Write a 250-word Substack intro in Domestic Observer mode about how your morning coffee ritual changed when you started talking to Claude every day. |
| `gonzo_broken_deploy` | Gonzo Technical | Write a 250-word Substack intro in Gonzo mode about deploying a broken migration to production at 11:47 PM on a Wednesday. |
| `kerouac_agent_moment` | Beat Flow | Write a 250-word Substack intro in Beat Flow mode about the moment you understood Claude Code agents — the sensory rush of watching code rewrite itself. |
| `vonnegut_leaving_loved_job` | Minimalist Absurdist | Write a 250-word Substack intro in Vonnegut mode about leaving a job you loved for a job that scared you. |

**Holdout trip-wire (2 prompts — scored every iteration, never fed back to optimizer)**
| ID | Scenario | Prompt |
|---|---|---|
| `dial_60_slipped_launch` | Dial-shift to 60% professional | Write a 250-word Substack intro about a launch that slipped two weeks. Sean Mode, dialed to 60% — appropriate for cross-posting on LinkedIn where former colleagues will read it. |
| `combo_gonzo_to_vonnegut` | Mode combination | Write a 250-word Substack intro that opens Gonzo (cold open, mid-action) and lands Vonnegut (flat collision closer). Topic: the day you realized your side project was actually your job. |

**Sealed surprise (3 prompts — scored every 5 iterations, optimizer cannot read this file)**
Stored in `evals.sealed.yaml`. The mutation subagent's read scope explicitly excludes this file.
| ID | Mode | Prompt |
|---|---|---|
| `surprise_sean_obsidian` | Sean Mode | Write a 250-word Substack intro about throwing away your second-brain Notion vault and starting from zero in Obsidian. |
| `surprise_sedaris_treadmill` | Domestic Observer + Gonzo escalation | Write a 250-word Substack intro in Domestic Observer mode, with one Gonzo escalation passage in the middle. Topic: the absurdity of buying a treadmill desk. |
| `surprise_kerouac_drive` | Beat Flow | Write a 250-word Substack intro in Beat Flow mode about driving from New York to Boston the day you accepted your move. |

### 4.2 Criteria — 3 structural + 3 LLM-judge

**Structural (Python, deterministic, free)**

| ID | Type | Check |
|---|---|---|
| `substack_format_intro` | regex + length | First paragraph 60-180 words. ≥ 2 paragraph breaks. Closing sentence ≤ 12 words (Sean's closer pattern). |
| `anti_pattern_overreference` | python | No single sensory noun (configurable list: coffee, bathroom, ferry, cursor, terminal, screen, mug, keyboard) appears more than 2 times. Exception: closing callback that intentionally re-uses an opening image (detected by position-based heuristic). |
| `stylometric_distance` | python (NEW per research B.3) | Compute z-score distance from Sean's corpus on 4 features: (a) sentence length mean+stdev, (b) comma density per 100 words, (c) em-dash density per 100 words, (d) Sean-specific n-gram match rate against ~30 distinctive n-grams extracted from `voice-samples.md`. Pass if total distance < threshold tuned at calibration time. |

**LLM-judge (Qwen3-14B local, with Sonnet 4.6 sample-check every 5 iterations)**

| ID | Question | Judge ensemble |
|---|---|---|
| `signature_move_present` | Does this output contain at least one signature move from the prescribed mode (e.g., for Sedaris: sentence-end punchline OR mundane→pivot OR cold-description defamiliarization)? | single-judge (more concrete) |
| `sounds_like_sean` | Does this output read like a Sean-Winslow-authored Substack intro rather than a generic AI imitation? | **3-judge majority vote** with shuffled anchor order + randomized seed |
| `no_anti_pattern_violation` | Is this output free of the prescribed mode's documented anti-patterns (e.g., for Kerouac: NOT 'rambling without a jewel center', NOT 'dashes everywhere with no rhythmic variation')? | **3-judge majority vote** with shuffled anchor order + randomized seed |

### 4.3 Scoring

```yaml
training_set:
  prompts: 5
  runs_per_prompt: 15  # bumped from 10 per research C.b
  criteria_count: 6  # 3 structural + 3 LLM-judge
  max_score: 450
  per_criterion_ceiling: 75  # 5 prompts × 15 runs

success:
  per_criterion_floor: 0.60  # every criterion ≥ 60% of its ceiling
  aggregate_target: 0.75     # aggregate ≥ 75% (was flat 80%; relaxed because per-criterion floors do most of the work)

decision_rule:
  use_moving_average: true
  window: 3  # 3-iteration moving average for keep/revert decisions
  bootstrap_ci: true
  bootstrap_resamples: 1000

iteration_cap: 25
plateau_halt: 3  # 3 consecutive iterations with no improvement → stop
starting_score_floor: true  # 3 iterations below starting score → halt + flag
```

## 5. Mutation Policy

Encoded in `agents-sdk/lib/skill_optimizer/program.md` and enforced by the mutation guard.

**Allowed:**
- Edit ONE section of the SKILL.md body per iteration
- Section = a Markdown subtree under a `##`, `###`, or `####` heading
- Mutation summary ≤ 200 chars, logged before applying

**Forbidden (enforced by pre-write diff guard, not trust):**
- Touch lines 1-4 (YAML frontmatter — name + description must stay stable per autoresearch constraint #3)
- Touch lines 23-69 (the 3 example outputs — these are real Sean-voice calibration anchors)
- Touch sections matching `## References`, `## Related Skills`, `## Copy/Paste Ready`
- Multi-section rewrites (must be exactly one section per iteration)
- Changes that introduce a heading whose text matches any criterion ID verbatim (anti-gaming guard)
- Whitespace-only diffs (rejected as gaming the iteration counter)
- Diffs with fewer than 5 changed lines AND no structural change (heading add/remove, table edit, bullet add/remove) — too small to constitute a "meaningful mutation"

**Diff guard implementation:** `agents-sdk/lib/skill_optimizer/mutation_guard.py` parses the proposed unified diff, rejects any hunk overlapping protected line ranges, rejects multi-section hunks. Rejection costs nothing (no generation calls, no judge calls) — counts as "wasted mutation, retry."

## 6. Judge Prompt Template

`agents-sdk/lib/skill_optimizer/judge_prompt.txt`. Per research B.5: 2 anchors (not 3), placed AFTER the output being judged to reduce anchoring bias.

```
You are evaluating a Substack blog post intro against ONE binary criterion.

OUTPUT TO EVALUATE:
[generation]

ANCHOR SAMPLES (real Sean Winslow voice in {mode} mode — for reference AFTER you've read the output):

Sample 1:
[~80 token excerpt from voice-samples.md, mode-matched]

Sample 2:
[~80 token before/after correction from voice-samples.md, mode-matched]

CRITERION:
{question}

Think step-by-step about whether the output above matches the criterion. Then on the LAST LINE answer with EXACTLY one word: YES or NO.
```

For 3-judge ensemble criteria (`sounds_like_sean`, `no_anti_pattern_violation`): run 3 calls, each with a shuffled anchor order (Sample 1 vs Sample 2 swapped, or different anchor pairs from the mode's pool), and a different randomized temperature seed. Majority wins.

## 7. Stylometric Distance Spec

`agents-sdk/lib/skill_optimizer/stylometry.py`.

**Corpus:** all "Full Exercise Passages" + "Raw Voice" snippets in `voice-samples.md` (4 full passages, 5 raw snippets ≈ 1,800 words). After Sean's pre-flight 60%-dial additions, corpus ≈ 2,000 words.

**Features computed once (cached):**
1. Sean's mean sentence length + stdev (compute from corpus, store in `stylometry_baseline.json`)
2. Sean's comma density per 100 words
3. Sean's em-dash density per 100 words
4. Sean-specific n-grams: extract all 2-4-grams from corpus, compute relative frequency vs. a baseline corpus (use NLTK Brown corpus or Project Gutenberg sample), keep top ~30 with highest relative-frequency ratio

**Per-output computation:**
1. Compute the same 4 features for the generation
2. z-score distance for each feature against baseline
3. Total distance = sum of absolute z-scores
4. Binary pass: `total_distance < threshold` where threshold is calibrated at pre-flight time against 30 hand-labeled examples (15 real Sean, 15 generic AI) to maximize separation

**Calibration pass:** one-time, before iteration 1. Uses Sonnet 4.6 to label 30 hand-labeled examples, tunes threshold to maximize ROC AUC. Locked once chosen.

## 8. Decision Rules + Trip-Wires

Implemented in `agents-sdk/lib/skill_optimizer/decision.py` and `tripwire.py`.

### 8.1 Keep / revert rule

**Only the training-set score drives keep/revert decisions.** Holdout score is for trip-wires only (Section 8.2, Signal 1). Surprise score is reported in results.tsv every 5 iterations but never used in keep/revert.

After each iteration:
1. Compute current iteration training score `S_i` and 3-iteration moving average `MA_i = mean(S_i, S_{i-1}, S_{i-2})` (for i < 3, use available — i.e., MA_1 = S_1, MA_2 = mean(S_1, S_2))
2. Compare `MA_i` vs. best-so-far `MA_best`
3. Bootstrap 1000 resamples on the per-criterion-pass binary array. If 95% CI of `MA_i - MA_best` is fully > 0 → **keep** (git commit). If CI overlaps 0 or is negative → **revert** (`git checkout -- SKILL.md`).

### 8.2 Six trip-wires (run after every iteration; halt + flag if any fire)

```python
TRIPWIRES = {
    "train_holdout_divergence":  # Signal 1
        lambda: holdout_score_drop_3iter > 5,
    "criterion_uneven_drift":    # Signal 2
        lambda: any(criterion_ratio / median_ratio > 1.5 for c in criteria),
    "stylometric_drift":         # Signal 3
        lambda: stylometric_drop > 0.15 and llm_judge_score_rising,
    "diversity_collapse":        # Signal 4
        lambda: avg_inter_run_similarity_rise > 0.20,
    "judge_disagreement":        # Signal 5
        lambda: sonnet_qwen_agreement < 0.70,
    "complexity_ratchet":        # Signal 6
        lambda: skill_token_growth > 0.50 and score_gain < 0.05,
}
```

**Calibration phase:** for iterations 1-3, trip-wires LOG ONLY (we need real data to calibrate thresholds). From iteration 4 onward, any tripped signal triggers HALT + flag in results.tsv. Sean reviews on next session.

**Note on interaction with primary halt conditions:** The primary halt conditions in Section 9 step 14 (success threshold reached, plateau, iteration cap, starting-score floor) operate from iteration 1 onward. Trip-wires are an independent safety layer that activates from iteration 4 onward. Either path can halt the loop.

## 9. Per-Iteration Data Flow

```
1.  Read current SKILL.md
2.  Read recent results.tsv (last 5 iterations) for context
3.  Spawn mutation subagent with program.md + recent failed-criterion stats
4.  Subagent proposes ONE mutation (target section, unified diff, summary)
5.  Mutation guard validates diff against protected ranges + sections
    └─ If invalid: log "rejected mutation: <reason>", increment retry counter, GOTO 3
6.  Apply mutation to SKILL.md (in-memory only until step 11)
7.  For each of 5 training prompts: spawn 15 generations (Opus 4.7) → 75 outputs
    For each of 2 holdout prompts: spawn 15 generations → 30 outputs
    If iteration % 5 == 0: also score 3 surprise prompts × 15 = 45 outputs
8.  For each output:
    - Run 3 structural checks (Python, deterministic, free)
    - Run 3 LLM-judge calls (single-judge for signature_move; 3-judge majority for sounds_like_sean + no_anti_pattern_violation = 5 calls total)
9.  Every 5th iteration: re-judge a 10% sample with Sonnet 4.6, log Sonnet↔Qwen agreement
10. Compute training score, holdout score, surprise score (if applicable)
11. Apply decision rule (Section 8.1) → keep or revert
    - If keep: write SKILL.md to disk, git commit with conventional-commit message
    - If revert: discard in-memory changes, log "reverted: score did not improve"
12. Run trip-wire check (Section 8.2)
    - If any trip: halt loop, write HALT row to results.tsv, exit
13. Append row to results.tsv:
    iteration | timestamp | mutation_section | mutation_summary | train_score | holdout_score | surprise_score | per_criterion_scores_json | delta | kept_or_reverted | tripwires_triggered | sonnet_qwen_agreement | duration_sec | cost_usd
14. Halt conditions check:
    - Aggregate ≥ 75% AND all per-criterion floors ≥ 60%
    - Plateau (3 iterations with no improvement)
    - 25 iterations reached
    - Tripwire halt
    - Starting-score floor breached (3 consecutive iterations below S_0)
    If any: exit. Else: GOTO 1.
```

## 10. Branch + Git Strategy

- **Branch:** `autoresearch/writing-voice-modes-2026-05-09`
- **Pre-flight check:** `skill_optimizer.py` aborts on startup if `git rev-parse --abbrev-ref HEAD` ≠ the expected branch
- **Kept mutation commit:** conventional-commit format
  ```
  optimize(writing-voice-modes): <mutation_summary>

  Score: 0.XXX → 0.YYY (+0.ZZZ)
  Per-criterion: signature_move 0.X→0.Y, sounds_like_sean 0.X→0.Y, ...
  Iteration: NN/25
  Section mutated: <section_name>

  🤖 Generated by skill_optimizer.py
  ```
- **Reverted mutation:** `git checkout -- SKILL.md` (no commit, no history pollution)
- **End of run:** PR from autoresearch branch → main, with results.tsv summary as PR body. Mandatory CHANGELOG/CLAUDE/README updates per repo rules (constraint #9).

## 11. Pre-Flight Requirements (block iteration 1)

1. **60% dial samples added to `voice-samples.md`** — Sean writes 2 short real samples (one ~80-word professional Slack message, one ~150-word stakeholder-update intro) at 60% professional dial. Add under a new "## Professional Dial — 60%" section in `voice-samples.md`.
2. **N-gram extraction from voice-samples.md** — one-time prep step. Run `python -m agents_sdk.lib.skill_optimizer.stylometry --extract-ngrams` to populate `stylometry_baseline.json` with the top ~30 Sean-distinctive n-grams + baseline feature distributions.
3. **Hand-labeled calibration set** — Sean labels 30 examples (15 real Sean writing pulled from voice-samples.md and prior Substack drafts; 15 generic AI outputs from a quick generation run with the current skill). Used to calibrate stylometric threshold + verify Qwen3-14B judge agreement on the criteria. ~30 minutes of Sean's time, one-shot.
4. **Branch created** — `git checkout -b autoresearch/writing-voice-modes-2026-05-09`
5. **Cost watchdog configured** — `[agents.skill_optimizer]` block in `config.toml` with hard cap `$200`, soft cap `$50` (alert).

## 12. File-by-File Change Manifest

For writing-plans to convert into ordered implementation tasks.

### 12.1 New files
| Path | Purpose |
|---|---|
| `agents-sdk/agents/skill_optimizer.py` | Main orchestrator |
| `agents-sdk/lib/skill_optimizer/__init__.py` | Module init |
| `agents-sdk/lib/skill_optimizer/program.md` | Optimizer subagent instructions |
| `agents-sdk/lib/skill_optimizer/judge_prompt.txt` | Judge prompt template |
| `agents-sdk/lib/skill_optimizer/structural_checks.py` | 3 deterministic checks |
| `agents-sdk/lib/skill_optimizer/stylometry.py` | Stylometric distance + n-gram extractor |
| `agents-sdk/lib/skill_optimizer/judge_runner.py` | Qwen3-14B judge runner with ensemble support |
| `agents-sdk/lib/skill_optimizer/mutation_guard.py` | Pre-write diff validator |
| `agents-sdk/lib/skill_optimizer/decision.py` | Keep/revert with bootstrap CI |
| `agents-sdk/lib/skill_optimizer/tripwire.py` | 6 trip-wire checks |
| `.claude/skills/writing-voice-modes/evals.yaml` | Training + holdout eval suite |
| `.claude/skills/writing-voice-modes/evals.sealed.yaml` | Sealed surprise prompts |
| `agents-sdk/data/skill-optimizer/.gitkeep` | Data dir for results.tsv |
| `agents-sdk/data/skill-optimizer/stylometry_baseline.json` | Baseline features + n-grams (generated at pre-flight) |
| `agents-sdk/tests/test_skill_optimizer.py` | Pytest suite for the new modules |

### 12.2 Modified files
| Path | Change |
|---|---|
| `agents-sdk/config.toml` | Add `[agents.skill_optimizer]` block (model, cost caps, paths) |
| `.claude/skills/writing-voice-modes/references/voice-samples.md` | Sean adds "## Professional Dial — 60%" section with 2 samples (pre-flight) |
| `CHANGELOG.md` | Entry under current version (post-run) |
| `CLAUDE.md` | Update agent count + add brief mention of skill_optimizer (post-run) |
| `README.md` | Update counts (post-run) |

### 12.3 Read-only / locked
| Path | Reason |
|---|---|
| `.claude/skills/writing-voice-modes/SKILL.md` lines 1-4 | Frontmatter (autoresearch constraint #3) |
| `.claude/skills/writing-voice-modes/SKILL.md` lines 23-69 | Example outputs (calibration anchors) |
| `## References`, `## Related Skills`, `## Copy/Paste Ready` sections | Meta-navigation, no quality leverage |

## 13. config.toml Additions

```toml
[agents.skill_optimizer]
enabled = true
schedule = "manual"  # not on launchd; run by hand
target_skill = ".claude/skills/writing-voice-modes"
branch = "autoresearch/writing-voice-modes-2026-05-09"
generator_model = "claude-opus-4-7"
judge_model_local = "qwen3-14b-research:latest"  # via Ollama on Mac Mini
judge_model_sonnet_check = "claude-sonnet-4-6"
sonnet_check_every_n_iterations = 5
max_iterations = 25
plateau_halt_iterations = 3
runs_per_prompt = 15
training_prompts_count = 5
holdout_prompts_count = 2
surprise_prompts_count = 3
surprise_score_every_n_iterations = 5
cost_cap_usd_hard = 200.00
cost_cap_usd_soft = 50.00
results_path = "data/skill-optimizer/writing-voice-modes-results.tsv"
stylometry_baseline_path = "data/skill-optimizer/stylometry_baseline.json"
```

## 14. results.tsv Schema

Tab-separated, one row per iteration. Header committed once at file creation.

```
iteration	timestamp	mutation_section	mutation_summary	train_score	holdout_score	surprise_score	criterion_substack_format	criterion_anti_pattern_overreference	criterion_stylometric_distance	criterion_signature_move	criterion_sounds_like_sean	criterion_no_anti_pattern_violation	moving_avg	delta_vs_best	kept_or_reverted	tripwires_triggered	sonnet_qwen_agreement	duration_sec	cost_usd
```

`tripwires_triggered` = comma-separated trip-wire names, or empty string. `surprise_score` = empty string for non-multiple-of-5 iterations.

## 15. Open Questions / Risks

| Topic | Question | Mitigation if it goes wrong |
|---|---|---|
| Qwen3-14B judge stability | Will Qwen3-14B reliably do binary yes/no on voice criteria? | Sonnet sample-check every 5 iters catches drift; if disagreement > 30%, halt. Worst case: fall back to Sonnet for all judge calls (~+$50 to total cost). |
| Stylometric corpus size | Is ~2,000 words enough corpus for stable baseline? | If feature variance is too high, add more Sean writing to voice-samples.md before run. Calibration pass against 30 hand-labeled examples will surface this. |
| Mutation subagent gaming | What if the optimizer learns to make trivial whitespace mutations to "score" iterations? | Mutation guard requires diff hunks > 5 lines OR substantive structural change (heading add/remove, table edit). Whitespace-only diffs rejected. |
| Branch enforcement | What if Sean accidentally runs on `main`? | Pre-flight check aborts. Hard error, no recovery — refuses to run. |
| 60% dial sample quality | What if Sean's pre-flight samples don't generalize? | The dial-shift prompt is a holdout, not training. If it scores poorly throughout, that's diagnostic info, not a loop failure. |

## 16. Success Criteria

- [ ] Loop runs to completion (success or principled halt) without manual intervention
- [ ] At least one kept mutation improves the moving-average composite score by ≥ 5%
- [ ] Final training score ≥ 75% aggregate AND all per-criterion floors ≥ 60% — OR clear diagnostic from halt conditions
- [ ] Holdout score does not diverge > 5 points below training score (no overfitting)
- [ ] Surprise score on iteration 25 ≥ surprise score on iteration 1 (held-out generalization)
- [ ] results.tsv is human-readable and tells the story of what was tried
- [ ] No locked sections were modified (mutation guard never bypassed)
- [ ] Sonnet-Qwen agreement ≥ 70% throughout
- [ ] Anti-pattern criterion never gamed (manual review of kept commits passes)
- [ ] All 7 changes from research v2 are present in the implementation
- [ ] The harness is generalizable: pattern works for other skills with minimal eval-suite changes (validated by sketching what eval.yaml would look like for `prd-generator` or `jira-automation` as a proof of generalization)

## 17. References

- Original autoresearch prompt: `autoresearch-skill-optimizer-prompt.md` (root of repo)
- Karpathy autoresearch repo: https://github.com/karpathy/autoresearch
- Daily-driver pattern: `agents-sdk/agents/daily_driver.py`
- Voice samples corpus: `.claude/skills/writing-voice-modes/references/voice-samples.md`
- Calibration notes: `.claude/skills/writing-voice-modes/references/calibration-notes.md`
- Research backing v2 changes (full citations in conversation log 2026-05-09): Anthropic reward-hacking 2026, GPT-4o stylometric imitation (Oxford DSH 2025), LLM-as-Judge survey (arXiv 2411.15594), Statistics for LLM Evals (Cameron Wolfe 2025), IJCNLP 2025 position bias, ScienceDirect stylometry 2025, MIPROv2 docs, Lilian Weng reward hacking 2024.
