---
description: Prove your voice skill is more you and less generic-AI
argument-hint: (optional) a topic to generate a fresh test sample about
allowed-tools: Read, Write, Edit, Bash
---

You are running **the proof** — VoicePrint's answer to "how do you know it sounds
like me and not like every other AI?" It combines a qualitative self-check, a
quantitative fingerprint, and the convergence trend into one honest verdict. This is
the thing skeptics ask for; do not inflate it. If the result is weak, say so.

## Before you start

1. Read `voiceprint/_work/pile-state.json`. The bundle must exist
   (`voiceprint/my-voice/SKILL.md`) and there should be at least a gauntlet and some
   voice samples. If not, name what's missing and stop.

## Part 1 — Gauntlet self-check (qualitative)

Read `voiceprint/my-voice/references/cheese-bank.md` (the registers the reader
rejected). Then generate a short fresh sample in their voice on a real topic (use
`$ARGUMENTS` or ask), or use the latest `voiceprint/_work/refine/round-*-draft.md`.

For each rejected register in the cheese bank, check: does the generated sample (and
the SKILL.md's own guidance) avoid it? Report it straight — "avoids all 6 rejected
registers," or "leaks #3 (motivational-poster) in the closer." A leak is a finding,
not a failure to hide; it tells the reader exactly what to fix in the next refine
round.

## Part 2 — Fingerprint (quantitative)

Run the fingerprint wrapper, which builds the reader's baseline from their samples,
analyzes a draft, and compares both against the shipped generic-AI baseline:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/fingerprint.py \
  --samples voiceprint/my-voice/references/voice-samples.md \
  --draft  <the fresh sample file you just generated> \
  --out    voiceprint/_work/fingerprint.json
```

Read the JSON. The headline signal is **sentence-length burstiness** (variety):
generic AI is flat and low; real human prose is bursty. The claim you can make is
comparative and honest: *is the draft's fingerprint closer to the reader's own
samples than to the generic-AI baseline?* Report the three numbers (you / your draft
/ generic-AI) for burstiness and lexical diversity. If the draft sits closer to
generic-AI than to the reader, that is the truth — say it, and point to more refine
rounds.

## Part 3 — Convergence

Read `voiceprint/_work/refine-log.jsonl`. Report the `pct_changed` trend across
rounds (lower over time = converging). If there are fewer than two rounds, say the
convergence signal needs a couple of refine rounds first.

## Assemble + show

Write `voiceprint/_work/proof.json` combining the three parts:

```json
{
  "date": "<today>",
  "gauntlet_self_check": "<one-line result, e.g. 'avoids all 6 rejected registers'>",
  "fingerprint": {
    "reader_burstiness": <n>, "draft_burstiness": <n>, "generic_ai_burstiness": <n>,
    "reader_mattr": <n>, "draft_mattr": <n>, "generic_ai_mattr": <n>
  },
  "convergence_trend": [<pct_changed per round>],
  "verdict": "<one honest sentence: is this more them than generic-AI yet, or not?>"
}
```

Re-render the dashboard so the proof panel shows:
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_dashboard.py --root voiceprint/`

Then give the reader the verdict in plain language — the one-screen "more you, less
generic-AI" read — with the actual numbers, and the single most useful next move
(usually a specific refine round aimed at whatever was weakest). Never claim a pass
the numbers don't support.
