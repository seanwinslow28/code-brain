---
name: writing-critique
description: >
  Adversarially red-team a draft and return triaged, directable findings plus an
  explicit verdict and the single highest-leverage fix. Critiques execution across
  structure, value, voice, prose/line, and credibility signal; never rewrites. Runs
  standalone and as the chain gate between your voice skill and writing-humanity-pass.
  Ships a stdlib analyzer (sentence-length burstiness, MATTR, opener variety) that
  baselines against YOUR own voice samples. Use when asked to "red-team this draft",
  "what's weak here", "critique this", "is this ready to ship", or "review my draft".
version: 0.1.0
---

# Writing Critique

## Purpose

Adversarial reading. Find what fails, not confirm what works. A critique that says
"well done" without digging creates false confidence and is worse than none. This
skill produces triaged, directable findings, an explicit verdict, and the one
highest-leverage fix. **It critiques; it never rewrites.** Fixes route back to the
voice layer / `writing-humanity-pass` or to the author.

## The anti-sycophancy mitigation (why it's built this way)

Sycophancy is a measured consequence of RLHF, worst when the same model that produced
the draft also critiques it — exactly the chain-gate path here. The mitigation is
**hard persona separation**: the critic explicitly did NOT write this draft and is a
hostile expert reviewer. `references/finding-rubric.md` encodes this plus per-finding
grounding (quote + concrete reader cost) and a severity-ranked floor (fewer issues on
a strong draft; never invent issues to hit a count). Load that rubric before
critiquing.

## Two modes

### Standalone (interactive)
1. Read the draft. Adopt the reviewer persona (you did not write this).
2. Detect the stage (early → structure + value; late → line + flatness).
3. Apply `references/finding-rubric.md` across the five dimensions.
4. Optionally run the analyzer for line-level evidence.
5. Return: overall assessment → findings by severity → verdict + the one fix. **No
   rewrite.**

### Chain gate (headless)
Detect non-interactive context. Then run the analyzer with `--json`, apply the rubric,
and if any reader-cost (blocking/major) finding exists, emit **one** structured revise
request routed back to the voice layer, then re-critique once. Else pass through to
`writing-humanity-pass`. Always non-destructive; emit the machine-readable verdict
block as a trailing HTML comment.

**One revise pass, grounded.** Anchored to a specific finding + the writer's voice
baseline, never "make it better." Un-anchored self-judged iteration degrades prose
toward bland.

## The five dimensions

Each critiques execution and defers to the owning skill; never re-litigates the premise.

1. **Structure** → `storytelling-architecture` (hook, but/therefore seams, loop
   closure, slippery-slide ends).
2. **Value** → `substack-value-engine` (Itch/Solution/Transfer delivered, seam is
   payoff not appendix, Rule-of-One, one usable thing in 10 minutes).
3. **Voice** → the writer's own voice skill (their signature moves present vs generic
   narrator; register drift). Treat the writer's documented signature moves as
   defensible choices, NOT defects — flagging a signature move as a flaw is the
   failure mode that destroys trust.
4. **Prose / line** → rhythm, sentence variety, repetition, clarity, AI-flatness.
   **The analyzer plugs in here.**
5. **Credibility signal** → `substack-value-engine` (judgment shown not claimed,
   artifact + blameless self-post-mortem, any ask stays sideways).

## The analyzer (optional, advisory)

`references/analyze.py` is pure stdlib. It measures sentence-length burstiness
(coefficient of variation), lexical diversity (MATTR@50), opener variety, and
repetition, and diffs them against a baseline.

```bash
# Build the writer's baseline from their own voice samples (run once / after refine):
python3 references/analyze.py --emit-baseline <your voice-samples.md> --out my-baseline.json
# Then critique a draft against it:
python3 references/analyze.py <draft.md> --baseline my-baseline.json
python3 references/analyze.py <draft.md> --baseline my-baseline.json --json   # chain gate
```

- **Advisory only.** It informs the revise decision and supplies evidence; it never
  blocks and is never a finding on its own.
- **Burstiness (sentence-length CV) is the headline signal**: the best-supported,
  computable AI-flatness tell. Low CV vs the writer's baseline → "monotonous vs your
  voice."
- **Pronoun rate and MATTR are flagged ONLY against the baseline, never as absolute AI
  signals.** A writer's voice may be pronoun-heavy and varied by design; an absolute
  threshold would flag their most characteristic prose.

**The baseline is the writer's own.** VoicePrint generates it from the reader's
`voice-samples.md`; there is no shipped one-size baseline (that would measure someone
else). Regenerate it whenever the voice samples gain a refine round. (`/voiceprint-proof`
also uses this analyzer to compare the writer's fingerprint against a shipped
generic-AI baseline — the "more you, less generic-AI" proof.)

## Verdict

Always explicit, exactly one of: `ship` / `revise` / `structural-rework`, plus the
single highest-leverage fix in one sentence.

## References

- `references/finding-rubric.md`: the adversarial mindset, persona separation, the
  four-quality finding rubric, the five dimensions, stage calibration, report +
  headless-verdict format. Load before critiquing.
- `references/analyze.py`: the stdlib mechanical analyzer (advisory).

## Attribution

The critique rubric and analyzer mechanics are adapted from the `prose-critique` skill
in [`haowjy/creative-writing-skills`](https://github.com/haowjy/creative-writing-skills)
(Apache 2.0). MATTR, the thresholds, and the baseline pipeline are additions.

## Success Criteria

- [ ] Findings are specific (quoted span), reasoned (named reader cost), directable,
      non-obvious.
- [ ] The critic persona is separated ("you did not write this").
- [ ] Severity-ranked floor honored: a strong draft yields fewer findings, never
      invented ones; praise capped to one line.
- [ ] Verdict explicit (`ship` / `revise` / `structural-rework`) + the one fix.
- [ ] Never rewrites; fixes route to the voice layer / humanity-pass / author.
- [ ] The analyzer stays advisory; burstiness/MATTR/pronoun flags are baseline-relative.
