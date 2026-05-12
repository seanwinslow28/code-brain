# Kickoff prompt — analyze the writing-voice-modes autoresearch run, propose improvements

> Paste everything below the `---` line into a fresh Claude Code session at the repo root.
> Engineered against Anthropic's prompt-engineering checklist (role + clarity + XML structure + CoT + validation).

---

<role>
You are a senior prompt engineer reviewing the results of the first live autoresearch optimization run on the `writing-voice-modes` Claude Code skill. You are not the author of the skill or the harness — you are coming in fresh, like a code reviewer, to read the artifacts, diagnose where the optimization fell short, and propose concrete improvements. Your audience is Sean Winslow, the user of the skill. Your goal is to make the skill produce output that scores higher on the existing eval suite — not to soften the eval suite.
</role>

<context>
On 2026-05-09 we shipped a Karpathy-style autoresearch optimization harness for Claude Code skills. Branch `autoresearch/writing-voice-modes-2026-05-09` (PR #32) merged into main contains:

- A new SDK agent `agents-sdk/agents/skill_optimizer.py` that runs an autonomous mutate→score→keep-or-revert loop on a single SKILL.md.
- A hybrid eval suite: 3 deterministic structural checks (`substack_format_intro`, `anti_pattern_overreference`, `stylometric_distance`) + 3 LLM-judge criteria (`signature_move_present`, `sounds_like_sean`, `no_anti_pattern_violation`) defined in `.claude/skills/writing-voice-modes/evals.yaml`.
- Generation runs on Opus 4.7. Judges run on Qwen3-14B (local Ollama on Mac Mini at `192.168.68.200:11434`) with Sonnet 4.6 sample-checks every 5 iterations.
- A pre-flight stylometric baseline in `agents-sdk/data/skill-optimizer/stylometry_baseline.json` and a 28-row hand-labeled calibration set at `agents-sdk/data/skill-optimizer/calibration_set.jsonl` (13 real-Sean chunks + 15 generic-AI Opus generations). Threshold tuned via TPR-FPR maximization to **7.57**.

The first live run (2026-05-10, `max_iterations=10`, `runs_per_prompt=15`) halted at the iteration cap. **One iteration completed and was kept** (commit `173e1c6` — a mutation tightening the `## Sean's Signature Moves` table). Iterations 2-10 each failed at the `propose_mutation` JSON parse step (Opus returned un-escaped multi-line markdown inside a JSON string field). That parser bug was fixed post-run in commit `190c686` by switching to a delimited-block format, but **no re-run has happened yet**.

Two of the six criteria scored below the 0.60 floor in iter 1 — that is the signal you are here to interpret.
</context>

<artifacts_to_read>
Read these in order. Quote relevant content when grounding your diagnosis.

1. **The run results** — `agents-sdk/data/skill-optimizer/writing-voice-modes-results.tsv` (one data row, 20 columns).
2. **The kept mutation diff** — `git show 173e1c6 -- .claude/skills/writing-voice-modes/SKILL.md` to see exactly what was changed in iter 1.
3. **The current artifact (post-mutation)** — `.claude/skills/writing-voice-modes/SKILL.md` in its current state on `main`.
4. **The eval definitions** — `.claude/skills/writing-voice-modes/evals.yaml` (criteria + thresholds).
5. **The structural-check source** — `agents-sdk/lib/skill_optimizer/structural_checks.py` (this is what `substack_format_intro` and `stylometric_distance` actually compute — read the code, not just the docs).
6. **Sean's voice corpus** — `.claude/skills/writing-voice-modes/references/voice-samples.md` (the calibration anchor).
7. **The stylometric baseline** — `agents-sdk/data/skill-optimizer/stylometry_baseline.json` (5 features: sentence_length_mean ≈ 14.9, sentence_length_stdev ≈ 17.9, comma_density_per_100w ≈ 3.24, em_dash_density_per_100w ≈ 1.41, first_person_freq_per_100w ≈ 3.85; 30 distinctive n-grams; threshold 7.57).
8. **The calibration set** — `agents-sdk/data/skill-optimizer/calibration_set.jsonl` (28 lines; each has `label`, `distance`, `text`). Sample 5-10 rows spanning the distance distribution to ground your intuition about what triggers a high vs. low score.
9. **The mutation guard** — `agents-sdk/lib/skill_optimizer/mutation_guard.py` (so you know what kinds of edits the orchestrator will reject).
10. **The optimizer's instructions to Opus** — `agents-sdk/lib/skill_optimizer/program.md` (the mutation subagent's system prompt — useful context for understanding why iter 1 made the choice it did).
</artifacts_to_read>

<task>
Two criteria scored below the 0.60 floor in iter 1:

| Criterion | Score | Floor |
|---|---:|---:|
| `substack_format_intro` | **0.36** | 0.60 |
| `stylometric_distance` | **0.40** | 0.60 |

The other four scored well (`anti_pattern_overreference` 0.79; `signature_move_present` 0.81; `sounds_like_sean` 1.00; `no_anti_pattern_violation` 1.00). The 1.00s are likely Qwen3-14B leniency that the Sonnet sample-check (every 5 iters) didn't get a chance to validate — note that, but don't focus on it; the real signal is the two below-floor structural checks.

**Diagnose** why each below-floor criterion fell short, then **propose 3-5 specific, concrete improvements** to SKILL.md (or, if clearly more appropriate, to the eval/calibration setup) that would push the failing scores up on the next run.
</task>

<thinking_steps>
Work through these in order, in `<thinking>` tags, before writing the final answer:

1. Read `structural_checks.py` and quote the exact logic for `substack_format_intro` and `stylometric_distance` (including the helper `_split_paragraphs`, `_word_count`, `extract_features`, `compute_distance`). What inputs make them pass? What inputs make them fail?
2. Read the iter-1 results.tsv row. Per-criterion scores are pass-rates over `runs_per_prompt=15` outputs × the criterion. So `substack_format_intro` 0.36 means roughly 5-6 of 15 outputs passed; `stylometric_distance` 0.40 means roughly 6 of 15 passed.
3. Read `git show 173e1c6` — what did the mutation actually change? Did it target shape/format or stylometric features at all, or did it sharpen the Signature Moves table (which is more relevant to `signature_move_present` / `sounds_like_sean`)? If the mutation didn't touch the failing-criterion territory, that's a clue that iter 1 went after the wrong target.
4. Read the current SKILL.md. Specifically:
   - Does it tell Claude to write a 60-180 word first paragraph? Where? In which words? Is the rule explicit and quotable, or buried in narrative?
   - Does it give Claude explicit numbers for sentence-length variance (Sean's mean ≈ 14.9, stdev ≈ 17.9) or em-dash density (≈ 1.41 per 100 words) or first-person frequency (≈ 3.85 per 100 words)?
   - Are the example outputs (locked at lines 23-69) actually demonstrating Substack-intro shape, or are they showing other content types?
5. For each below-floor criterion, hypothesize the gap between what SKILL.md teaches and what the eval measures. Be concrete: "the skill describes mood and signature moves but never names a target word count, so Opus optimizes prose at the wrong length" beats "the skill is too vague".
6. Sample the calibration_set.jsonl. Look at 3-5 label=1 examples with the LOWEST distance (closest to baseline) and 3-5 label=0 examples with the HIGHEST distance (most distant). What do the low-distance Sean samples have that the AI samples don't? That gap is what SKILL.md should be pulling Opus toward.
7. Now draft 3-5 proposals. Each one should be a SINGLE non-protected section edit, paste-ready, with a stated mutation-guard check. Reject any proposal that targets lines 1-4, lines 23-69, or the `## References` / `## Related Skills` / `## Copy/Paste Ready` sections.
</thinking_steps>

<constraints>
- **Protected ranges in SKILL.md** (the mutation guard will reject edits here, so your proposals must avoid them):
  - Lines 1-4 (YAML frontmatter — `name`/`description` are stable contracts)
  - Lines 23-69 (the 3 calibration anchor outputs — these are real Sean voice)
  - Sections named `## References`, `## Related Skills`, `## Copy/Paste Ready`
- **No anti-gaming**: don't propose introducing a heading whose text matches a criterion ID verbatim (`substack_format_intro`, `stylometric_distance`, etc.).
- **No softening the eval**: do NOT propose lowering the 0.60 floor, raising the stylometric threshold past 7.57, or relaxing the `substack_format_intro` rules. The point is to teach the skill to write better prose, not to weaken the test.
- **One section per proposal**: each proposal should be small enough that one mutation-subagent iteration could apply it cleanly. Don't bundle "rewrite half the skill" into a single proposal.
- **Each proposal must change ≥ 5 lines OR introduce a structural change** (heading add/remove, table edit, bullet add/remove) — that's the per-iteration mutation policy in `program.md`.
- **Quote the data**: every diagnosis claim should be grounded in a quoted line from results.tsv, structural_checks.py, SKILL.md, or the calibration set. No vibes-based claims.
</constraints>

<output_format>
Use this exact structure. Markdown. No JSON.

## Diagnosis

For each below-floor criterion (`substack_format_intro` and `stylometric_distance`), in 100-200 words each:

- **What the check actually measures**: quote 2-4 lines from `structural_checks.py`.
- **The score and what it implies**: the exact pass-rate from results.tsv, translated into "X of 15 outputs passed".
- **Likely cause**: 1-2 specific gaps between what the current SKILL.md teaches and what this check measures. Reference SKILL.md sections by name.
- **What the output would need to do differently** to pass.

## Proposals

3-5 numbered proposals. For each:

### Proposal N — <one-sentence summary>

- **Target section** (exact heading from current SKILL.md, e.g. `## Sean's Signature Moves` or `### 1. Domestic Observer`):
- **Change** (paste-ready markdown — show the new lines, or a before/after block for an existing line):
  ```markdown
  <new or replacement content>
  ```
- **Hypothesis** (2-3 sentences): why this change should move the targeted criterion up. Be specific about the mechanism.
- **Mutation-guard check**: confirm not a protected range, not a protected section, not whitespace-only, not a criterion-ID heading, ≥5 lines changed OR a structural change.
- **Targets criterion**: `substack_format_intro` | `stylometric_distance` | both. Direction: ↑.

## Self-check (run before finalizing)

Answer YES/NO to each — if any is NO, revise:

- [ ] Did I read structural_checks.py and quote the actual logic, not paraphrase it?
- [ ] Did I read SKILL.md post-mutation (commit 173e1c6 applied), not the pre-mutation baseline?
- [ ] Did I sample calibration_set.jsonl and let actual examples ground at least one proposal?
- [ ] Are all proposals targeting non-protected sections?
- [ ] Does each proposal change ≥5 lines or include a structural change?
- [ ] Am I proposing changes that teach the skill better, not changes that weaken the eval?
- [ ] If a proposal touches Sean's stylometric features (sentence length, comma density, em-dash density, first-person frequency), did I cite the actual baseline numbers from `stylometry_baseline.json`?

## Optional bonus

If, after writing the proposals, you notice a deeper issue — e.g., a structural check that doesn't match its YAML description, a calibration-set chunk that's mislabeled, or a baseline feature that looks miscomputed — flag it under a final `## Notes for Sean` section. Keep it short (≤ 150 words). This is optional and only if you actually find something.
</output_format>

---

**End of kickoff prompt.**

When this analysis returns, the natural follow-up is: pick the 1-2 strongest proposals, hand-apply them as a single commit on a fresh `autoresearch/writing-voice-modes-2026-05-XX` branch, then re-launch `skill_optimizer.py` with `max_iterations=10, runs_per_prompt=15` (now using the fixed delimited-block parser from `190c686`) to confirm the criteria actually move.
