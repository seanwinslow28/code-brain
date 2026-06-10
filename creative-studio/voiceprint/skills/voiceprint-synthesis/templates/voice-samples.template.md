# {{reader_name_or_label}}'s Voice Samples

> The authority file. Real writing from this person, tagged by move. When these
> samples and the rules in SKILL.md conflict, **these win.** Real samples beat
> technique descriptions every time.
>
> **Format note (load-bearing):** each `##` heading below holds ONE self-contained
> sample passage. `/voiceprint-proof` and the writing-critique analyzer read passages
> by heading to compute this writer's quantitative fingerprint (sentence-length
> burstiness, lexical diversity) for the "more you, less generic-AI" proof. Keep the
> passages verbatim and reasonably long — the fingerprint is only honest if the prose
> is really theirs. Add a new `##` passage every time a better sample appears.

<!-- Use the reader's longest, most-them real passages from /voiceprint-mine. Verbatim,
     typos and all. One passage per heading. Tag the moves underneath, with the
     specific lines that prove them. -->

## Sample — {{short_label_eg_origin_story}}

> {{verbatim_passage_from_their_pre_ai_writing}}

**Moves visible:** {{move}} ("{{the_line_that_proves_it}}"), {{move}} ("{{line}}").

## Sample — {{short_label}}

> {{verbatim_passage}}

**Moves visible:** {{move}} ("{{line}}").

---

## Refine-loop diffs

<!-- /voiceprint-refine appends here. Each entry: what the skill wrote, what the
     reader changed, and the lesson the edit teaches. These edit-diffs are
     calibration data — the highest-signal samples of all, because they show exactly
     where the generated voice missed and how the writer corrected it. -->

### Round {{n}} — {{date}}

**Skill wrote:** {{generated_line}}
**Reader changed it to:** {{their_edit}}
**Lesson:** {{what_the_diff_teaches_about_their_voice}}
