---
name: writing-critique
description: Adversarially red-team a draft and return triaged, directable findings plus an explicit verdict and the single highest-leverage fix. Critiques execution across structure, value, voice, prose/line, hiring signal, and operator credibility; never rewrites. Runs standalone (on-demand red-team) and as the chain gate between writing-voice-modes and writing-humanity-pass, with the same interactive-vs-headless detection as writing-humanity-pass. Ships a stdlib analyzer (sentence-length burstiness, MATTR, opener variety) with a baseline captured from Sean's voice corpus. Use when asked to "red-team this draft", "what's weak here", "critique this", "find what doesn't work", "is this ready to ship", "what would a skeptical reader catch", or "review my draft".
---

# Writing Critique

## Purpose

Adversarial reading. Find what fails, not confirm what works. A critique that says
"well done" without digging creates false confidence and is worse than none. This
skill produces triaged, directable findings, an explicit verdict, and the one
highest-leverage fix. **It critiques; it never rewrites.** Fixes route back to
`writing-voice-modes` / `writing-humanity-pass` or to Sean.

It is the only *evaluative* stage in an otherwise generative chain: every other
writing skill produces; this one red-teams.

## When to Use

- "Red-team this draft", "what's weak here", "critique this", "find what doesn't
  work", "is this ready to ship", "what would a skeptical reader catch", "review
  my draft".
- As the chain gate between `writing-voice-modes` (compose) and
  `writing-humanity-pass` (scrub), on the voiced draft.
- Gating an agent-drafted post (e.g. Substack-Drafter) before it ships.

## The anti-sycophancy mitigation (why this skill is built the way it is)

Sycophancy is a measured consequence of RLHF, and self-enhancement bias is at its
worst when the same model that produced the draft also critiques it, which is
exactly the chain-gate path here (the model just ran `writing-voice-modes`). The
named mitigation is **hard persona separation**: the critic explicitly did NOT
write this draft and is a hostile expert reviewer. `references/finding-rubric.md`
encodes this plus per-finding grounding (quote + concrete reader cost) and a
severity-ranked floor (report fewer issues on a strong draft; never invent issues
to hit a count). Load that rubric before critiquing.

## Two modes (same interactive-vs-headless detection as writing-humanity-pass)

### Standalone (interactive)

1. Read the draft. Adopt the reviewer persona (you did not write this).
2. Detect or take the stage (early → structure + value; late → line + flatness).
3. Apply `references/finding-rubric.md` across the six dimensions.
4. Optionally run the analyzer for line-level evidence (see below).
5. Return: overall assessment → findings by severity → verdict + the one fix.
   **No rewrite.**

### Chain gate (headless, e.g. Substack-Drafter)

Detect non-interactive context the same way `writing-humanity-pass` does (no human
can answer a prompt in a launchd run). Then:

1. Run the analyzer with `--baseline references/baseline.json --json` and apply the
   rubric.
2. If any reader-cost (blocking/major) finding exists, emit **one** structured
   revise request, *"revise against [this specific finding]"*, routed back
   through `writing-voice-modes` (which carries Sean's calibrated target), then
   re-critique once.
3. Else pass through to `writing-humanity-pass`.
4. Always non-destructive. Emit the machine-readable verdict block as a trailing
   HTML comment (see the rubric's "Headless verdict block").

**One revise pass, grounded.** The cap is a proxy for the real lever: the single
pass must be anchored to an external target (a specific finding + Sean's voice
baseline), never "make it better." Un-anchored self-judged iteration degrades
prose toward bland/generic. Any second pass would require **new external input**
(a human note, a new finding from a different source), never a self-judged re-roll.

## The six dimensions

Each critiques execution and defers to the owning skill; never re-litigates the
premise.

1. **Structure** → defers to `storytelling-architecture` (hook, but/therefore
   seams, open-loop closure, slippery-slide ends). When storytelling's
   **open-loop ledger** is present in context, check closure against it by name:
   a ledger loop with no close in the draft is a blocking structural finding, not
   a matter of taste.
2. **Value** → defers to `substack-value-engine` (Itch/Solution/Transfer
   delivered, seam is payoff not appendix, Rule-of-One, one usable thing in 10
   minutes). When the named **Value Gate verdict** is present, re-check each slot
   actually landed in the voiced draft (especially that the Transfer's artifact is
   really there) — verify, do not re-run the gate.
3. **Voice** → defers to `writing-voice-modes` (signature moves present vs
   generic narrator; register drift).
4. **Prose / line** → rhythm, sentence variety, repetition, clarity, AI-flatness.
   **The analyzer plugs in here.**
5. **Hiring signal** (Sean-specific) → defers to `substack-value-engine`
   (judgment shown not claimed, artifact + blameless self-post-mortem, ask stays
   sideways).
6. **Operator credibility** → does the author read as someone who actually builds
   this, to a reader who already does. **The one dimension this skill owns
   outright** (see below): every other dimension has an upstream owner; operator
   credibility is a property of the author-reader relationship rather than of any
   single stage, so nobody upstream can hold it. Three named tells: **essay-drift**,
   **false authority**, **keyword-stuffing**.

### Operator credibility, in full

The reader this dimension protects against is the one who already has a platform
and already ships — a builder peer. That reader forgives a rough sentence and
does not forgive being lectured by someone who has done less than they have. A
piece can pass all five other dimensions and still lose them.

| Tell | What it is | The question that catches it | Reader cost |
|---|---|---|---|
| **Essay-drift** | The piece slides from what ran to what one *could* do. Commentary about the work replaces the work. | Point at the paragraph and name the artifact it rests on. None? Drift. | The builder-reader stops at the first paragraph with nothing in it. They came for the run, not for the reflection on runs. |
| **False authority** | A claim whose scope outruns the evidence in the piece. One experiment licensing "teams should"; a week of use licensing "the right way to". | Name the evidence *in this draft* that licenses the claim's scope. | The reader with more scars catches the overreach and discounts everything else, including what was earned. This is the expensive one: it costs the relationship, not the paragraph. |
| **Keyword-stuffing** | Term density written for a search index rather than a reader. Inherited from the LinkedIn field-tolerance finding ([#170](https://github.com/seanwinslow28/code-brain/issues/170)): the same term load reads as normal in one field and as gaming in another. | Would this term still be here if nobody searched for it? | The reader concludes the piece was optimized rather than written, and re-reads every other claim as optimization too. |

**Severity.** Operator-credibility findings are reader-cost findings like any
other and rank the same way. **False authority is blocking when the overreaching
claim is load-bearing** — when the piece's spine is a prescription the evidence
does not support, no line fix rescues it and the verdict is `structural-rework`.

**The guard, and it is the load-bearing half.** The failure mode of this
dimension is flagging earned authority as overreach, which is the same class of
error as flagging a signature move as a defect: it destroys the critique. Before
raising one, check all three:

- A first-person claim backed by an artifact **in the draft** is not false
  authority. It is the thing the piece is for.
- Sean's self-deprecation is a signature move, not a credibility defect. He
  undersells on purpose; do not read it as a confession of thin evidence.
- A deliberate reflective beat is not essay-drift. The tell is the *sustained*
  slide, several paragraphs with no artifact under any of them, never one
  paragraph of thinking between two concrete ones.

**Where it defers.** It owns the dimension, but not the specifics others already
hold. Essay-drift's floor is the medium contract's artifact rule (a piece with no
captured artifact is the contract's block, not this skill's finding);
false-authority's overlap with resume-speak defers to `substack-value-engine`'s
hiring signal; keyword tolerance per surface belongs to the medium contract.
Where none of those is in context — a standalone red-team — this skill applies
the dimension on its own.

## The analyzer (optional, advisory)

`references/analyze.py` is pure stdlib. It measures sentence-length burstiness
(coefficient of variation), lexical diversity (MATTR@50, MTLD fallback for short
drafts), opener variety, and repetition, and diffs them against
`references/baseline.json` (Sean's own voice corpus).

```bash
python3 references/analyze.py <draft.md> --baseline references/baseline.json
python3 references/analyze.py <draft.md> --baseline references/baseline.json --json   # chain gate
```

- It is **advisory**: it informs the revise decision and supplies evidence for a
  prose/line finding. It never blocks and is never a finding on its own.
- **Burstiness (sentence-length CV) is the headline signal**: the best-supported,
  analyzer-computable AI-flatness tell. Low CV vs the baseline → "monotonous vs
  your voice."
- Pronoun rate and MATTR are flagged **only** against the baseline, never as
  absolute AI signals (Sean's voice is pronoun-heavy and varied by design).
- **Degraded paths:** no Python in a headless run → critique proceeds
  qualitatively (the rubric still works). Missing/stale baseline → the analyzer
  falls back to its one absolute advisory (low CV) and logs that the baseline was
  absent. Tiny draft (a tweet) → it reports "insufficient length for variance
  signal" and MTLD low-confidence instead of a false flatness flag.

**Baseline regeneration:** when `writing-voice-modes/references/voice-samples.md`
gains a calibration round, re-extract the new Sean prose into
`references/baseline-corpus.md` (one passage per `## ` heading) and re-run
`python3 references/analyze.py --emit-baseline references/baseline-corpus.md --out references/baseline.json`.
The MATTR window is locked at 50; do not tune it.

## Verdict (binding on the findings, never softened)

Always explicit, exactly one of: `ship` / `revise` / `structural-rework`, plus the
single highest-leverage fix in one sentence.

The verdict is a *function of the findings*, not a judgment call. Softening it to
spare the writer is the exact sycophancy this skill is built to resist:

- Any unresolved **blocking or major reader-cost** finding forbids `ship`. A draft
  with a real defect cannot be stamped ship because the rest is strong.
- A failed **structure or value gate** (a ledger loop left open, a Value Gate slot
  that did not land) forces `structural-rework`, not `revise`. `revise` is for
  line-and-execution fixes; a broken spine is not a line fix.
- `ship` requires zero unresolved blocking/major findings. When torn between two
  verdicts, pick the more severe: a false `ship` ships slop, a false `revise`
  costs one more pass.

**Selecting the single highest-leverage fix.** It is the finding with the highest
*reader cost × reach*, never the most visible or the easiest one. Validate it: *if
only this were fixed, would the draft clear the ship bar?* If yes, it is the right
fix. If no, either you picked a lower-leverage one, or the true verdict is
`structural-rework` and no single line-fix rescues the draft. Say which.

## The chain after this change

```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE)               (value GATE)            (every SENTENCE)      (RED-TEAM, advisory)  (scrub + no em dash, LAST)
```

Critique sits between voice and humanity so `writing-humanity-pass` keeps its
"runs LAST" identity. The analyzer runs on the *voiced* draft (pre-scrub) and
informs the revise decision; humanity-pass still does the qualitative scrub
afterward. Critique is advisory, never rewrites, caps at one grounded revise pass,
and hands off in-context.

**The handoff forward is a named artifact — the critique fix list:** the findings
carried forward, the single highest-leverage fix, and the verdict. It travels to
`writing-humanity-pass`, which treats any prose change made to satisfy a critique
finding as protected — the final scrub must not undo the gate's work (a blunt
sentence a fix introduced can read like a tell but was a reader-cost decision).
Emit the fix list so the last stage preserves those fixes instead of regressing
them.

## Related Skills

- `storytelling-architecture`: owns structure; this skill critiques structural
  execution, never the chosen scaffold.
- `substack-value-engine`: owns the value gate + hiring signal; this skill checks
  they actually landed.
- `writing-voice-modes`: owns the sentences and Sean's signature moves; this skill
  routes a grounded revise request back here, and treats signature moves as
  defensible choices, not defects.
- `content-machine`: when a piece runs through the machine, the medium contract in
  `contracts/<lane>/<medium>.md` is in context. Operator credibility defers to it
  on the artifact rule and on per-surface keyword tolerance; the lane file owns
  the first-screen test, which is a shape-stage check, not a critique finding.
- `writing-humanity-pass`: runs after this skill. It consumes this skill's
  **critique fix list** and protects those fixes from the scrub. Its
  `references/ai-tells.md` evidence stratification shares this skill's measurable
  signals (burstiness, MATTR, pronoun rate) and the same analyzer.

## Attribution

The critique rubric and the analyzer mechanics are adapted from the
`prose-critique` skill in
[`haowjy/creative-writing-skills`](https://github.com/haowjy/creative-writing-skills)
(Apache License 2.0). Attribution retained, mirroring how `writing-humanity-pass`
credits `blader/humanizer`. The citations in the evidence tiers were re-grounded
for this repo (a deliberate divergence from upstream); MATTR, the thresholds, and
the baseline pipeline are new additions, not ports.

## References

- `references/finding-rubric.md`: the adversarial mindset, persona separation, the
  four-quality finding rubric, the six dimensions, stage calibration, and the
  report + headless-verdict format. Load before critiquing.
- `references/analyze.py`: the stdlib mechanical analyzer (advisory).
- `references/baseline.json`: Sean's precomputed voice baseline (regenerable).
- `references/baseline-corpus.md`: the Sean-only prose the baseline is built from.

## Success Criteria

- [ ] Findings are specific (quoted span), reasoned (named reader cost),
      directable, and non-obvious, never spellcheck.
- [ ] The critic persona is separated ("you did not write this"), especially in
      the chain gate.
- [ ] Severity-ranked floor honored: a strong draft yields fewer findings, never
      invented ones; praise is capped to one line.
- [ ] Verdict is explicit (`ship` / `revise` / `structural-rework`) + the one fix,
      and binding on the findings: no `ship` with an unresolved blocking/major
      finding; a failed structure/value gate forces `structural-rework`.
- [ ] The single highest-leverage fix is the highest reader-cost × reach finding,
      validated by the "if only this were fixed, would it ship?" test.
- [ ] Operator credibility is read on every Sean-authored draft: essay-drift,
      false authority, keyword-stuffing — with earned first-person authority and
      deliberate self-deprecation explicitly NOT flagged.
- [ ] The critique fix list is emitted for `writing-humanity-pass` to preserve.
- [ ] The skill never rewrites; fixes route to voice-modes / humanity-pass / Sean.
- [ ] Headless runs emit the machine-readable verdict block.
- [ ] The analyzer stays advisory; burstiness/MATTR/pronoun flags are
      baseline-relative (pronoun rate never absolute).

## Copy/Paste Ready

```
"Red-team this draft"
"What's weak here? Be a hostile reviewer"
"Critique this, find what doesn't work"
"Is this ready to ship?"
"What would a skeptical reader catch?"
"Does this read like an operator or like someone writing about operators?"
"Run the analyzer against my voice baseline"
"Critique gate this before humanity-pass"
```
