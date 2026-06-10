---
description: Sharpen your voice skill — it drafts, you edit, the diff teaches it
argument-hint: (optional) a topic to write a short sample about
allowed-tools: Read, Write, Edit, Bash
---

You are running **Stage E — the Refine Loop** of VoicePrint. This is how the voice
gets good: the skill writes a sample, the reader edits it, and the **diff between
what it wrote and what they changed is the highest-value calibration data there is.**
Run it repeatedly; the edits should shrink over rounds.

## Before you start

1. Read `voiceprint/_work/pile-state.json`. If absent, send them to `/voiceprint-start`.
2. The skill must exist (`voiceprint/my-voice/SKILL.md`). If `stages.synthesize` is
   not `complete`, tell them to run `/voiceprint-synthesize` first and stop.
3. Determine the round number: `stages.refine.rounds + 1`.

## Run one round

1. **Load their voice.** Read `voiceprint/my-voice/SKILL.md` and its three reference
   files. Treat the **voice samples as the authority** (when the rules and samples
   conflict, samples win).
2. **Write a short sample in their voice.** Pick a topic from `$ARGUMENTS`, or ask for
   one, or reuse a topic from their pile. Keep it short (a paragraph or two — enough
   to edit meaningfully, not a whole essay). Save it to
   `voiceprint/_work/refine/round-<N>-draft.md`.
3. **Hand it over for editing.** Show the draft. Coach: "Edit it like it's yours —
   change whatever's off, cut what's not you, fix the lines that feel faked. Paste it
   back, or just tell me what's wrong and I'll apply it." Capture their edited version
   to `voiceprint/_work/refine/round-<N>-edited.md`.
4. **Measure the diff:**
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/diff_metrics.py \
     --before voiceprint/_work/refine/round-<N>-draft.md \
     --after  voiceprint/_work/refine/round-<N>-edited.md \
     --round <N> --log voiceprint/_work/refine-log.jsonl
   ```
   Read the `pct_changed` it prints.
5. **Feed the diff back into the voice.** Append a `### Round <N>` entry to the
   "Refine-loop diffs" section of `voiceprint/my-voice/references/voice-samples.md`:
   what the skill wrote, what the reader changed it to, and the **one-line lesson** the
   edit teaches about their voice. This is the calibration — the sample file is the
   authority, so a new diff sharpens the voice without re-authoring the whole skill.
   Do NOT rewrite the SKILL.md wholesale; let the evidence accrete.

## Update state + dashboard

In `pile-state.json`: set `stages.refine.status` to `in_progress` (or `complete` if
they say they're done), bump `stages.refine.rounds` to `<N>`, set
`stages.refine.last_diff_pct` to the measured `pct_changed`, update `updated`, and
recompute `next_best_action`. Then re-render:
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_dashboard.py --root voiceprint/`

## Close the round

Tell them the convergence read in one line — compare this round's `pct_changed` to the
trend in `refine-log.jsonl` ("you changed 9% this round, down from 26% — it's
converging"). Invite another round, or suggest `/voiceprint-proof` once a few rounds
are in. If the diff went UP, that's fine and worth saying — it usually means a new
topic stretched the voice into territory the samples hadn't covered; the round you
just logged now covers it.
