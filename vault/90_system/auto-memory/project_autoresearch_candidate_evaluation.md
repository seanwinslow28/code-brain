---
name: Evaluate autoresearch candidates before next run
description: Sean asked for a reminder to survey the 117 skills + 16 SDK agents and identify which would actually benefit from autoresearch before spending another $20-145 cycle. writing-voice-modes hit a corpus/taste ceiling; not every skill will.
type: project
originSessionId: f17ffb8f-8a62-445b-9540-7646aa2cec13
---
Before running `agents-sdk/agents/skill_optimizer.py` again, do a survey pass on which skills/agents have the right shape for autoresearch ROI. Sean explicitly asked for this as a reminder on 2026-05-11 after the writing-voice-modes run ($0 actual via Qwen judges, but 6300s of compute).

**Why:** autoresearch shines on (a) skills with clean numeric/structural ground truth, (b) skills where failure modes are structural not taste-based, (c) skills Sean uses often enough that gains compound. writing-voice-modes failed (a) and (c) at this stage — corpus is too thin (voice-samples.md only, no Substack archive yet), and the failing criteria turned out to be diagnosable in 30 minutes of manual review (output shape + stylometric targets weren't even in SKILL.md). Spending compute on hill-climbing a skill whose real bottleneck is corpus size is wasted budget.

**How to apply:** Whenever Sean asks "what should I run autoresearch on next" or returns to skill_optimizer work — surface this memory and propose:

1. Scan all 117 skills under `.claude/skills/` and 16 SDK agents under `agents-sdk/agents/`.
2. Score each on three axes: (a) does a clean structural/numeric eval exist or is it cheap to write? (b) are failure modes structural (template adherence, format compliance, schema correctness) vs taste-based (voice, judgment, creativity)? (c) does Sean use it weekly+?
3. Rank top 3-5 candidates with one-line rationale.
4. Sean picks 1-2 for the next autoresearch cycle.

**Likely strong candidates to investigate first** (cheap structural eval + frequent use + structural failure modes):
- `commit-checklist` — diff parsing + conventional-commit format is fully structural
- `prd-generator` — template section adherence + acceptance-criteria shape is structural
- `intent-engineering` — frontmatter compliance + section order is structural
- `tech-spec` — structural section requirements + interface specs
- SDK agents emitting structured JSON (`flush.py`, `vault_synthesizer.py` connection JSON) — schema validation is the eval

**Likely weak candidates** (taste-bound, corpus-thin, or low-frequency):
- `writing-voice-modes` (revisit only after Substack corpus is built)
- `creative-director`, `script-writing`, `creative-writing` — judgment-bound
- Any skill where "good output" requires Sean-specific context the eval can't supply

Do not auto-run another cycle without this survey. The point of the harness is leverage, not exercising the loop.
