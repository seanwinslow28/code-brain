# Partner session sidecar contract — `partner-sessions/<date>-<slug>.md`

The running memory and sole deliverable of a `creative-partner` session. One
file, a stamp header, two blocks, hard ownership. Generalized from anima's
front-door sidecar contract; the two-block discipline is identical, the emit
is gone, and the stamp header is new.

## Location and naming

- One file per session:
  `$CREATIVE_HARNESS_HOME/partner-sessions/<YYYY-MM-DD>-<slug>.md`
- `$CREATIVE_HARNESS_HOME` defaults to `~/.creative-harness/`. The skill
  reads the environment variable so the harness home can move (or be a
  satellite machine's local home) without a skill edit.
- **Never inside a repository working tree.** Sidecars carry verbatim
  personal reasons; the harness home is local-only and backed up as a
  protected class. The project a session serves is recorded *inside* the
  file, not by where the file sits.
- If the file can't be written, keep the identical discipline inline in the
  conversation and say so at wrap.

## Shape

```markdown
# Partner session — <slug> — <date>

<!-- identity stamps -->
skill: creative-partner @ <sha256-short of SKILL.md>
pack: <partner-pack @ <hash> | none>
model: <the launched model id>
project: <what this session serves>
modes: <none | diverge:<axis> ...>

## LOCKED DECISIONS   <!-- orchestrator-owned; APPEND-ONLY -->

- [L1] ASK (verbatim): "<Sean's opening words, unedited>"
- [L2] <axis>: <the locked decision, a named specific>
  - why (verbatim): "<Sean's one-line reason, quoted exactly; omit the whole
    sub-line if he skipped the question>"
- ...
<!-- honesty checkpoint @L5 — rules re-read -->
- late why for [Lk] (verbatim): "<a reason Sean volunteered after the lock;
  appended as a new entry — the lock itself is never edited>"
- [Ln] SUPERSEDES [Lk]: <new decision + the orchestrator's account of what changed>
  - why (verbatim): "<Sean's reason for the change>"

## PROPOSALS LOG   <!-- stage-appended; four content kinds only -->

### <axis-slug>            <!-- ONE axis per block wherever possible -->
- observations: <the live tension, in a line>
- options: <distinct named specifics, each WITH its tradeoff>
- recommendation: <the stated lean and its reason, phrased so Sean can
  accept or veto in a line>
- open_questions: <what the room can't resolve alone>

### diverge:<axis-slug> — frames: [<4 ids>], calls: 5   <!-- mode runs only -->
- observations: <why divergence was invoked/offered; the reframed problem>
- options: <the critic's shortlist — each option carries its originating
  frame id; traps flagged as machine_fate_hypothesis with one-line reasons>
- recommendation: <the critic's lean, marked as machine-proposed>
- open_questions: ...
```

## Rules

- **Only the orchestrator writes LOCKED DECISIONS**, and only after Sean
  decides. Locks are append-only: a change is a new `SUPERSEDES` entry,
  never an edit — the sidecar is the session's audit trail, and the harvest
  layer treats any rewrite of already-written history as a tamper signal.
- **Every lock carries Sean's own one-line reason, marked verbatim** — the
  full five rules live in SKILL.md (verbatim-or-nothing; a volunteered
  reason satisfies the ask; one guess only; only his words land; silence
  records nothing). The `(verbatim)` tag is load-bearing: an unmarked reason
  reads downstream as orchestrator paraphrase and is graded accordingly.
- **One axis per proposals block wherever possible.** A block that bundles
  several axes forces the harvest layer to split it by guesswork; when a
  question genuinely spans axes, name each axis on its own `###` block even
  if they were discussed together.
- **Four content kinds only** in proposals blocks: `observations`,
  `options`, `recommendation`, `open_questions`. A stage or sub-agent that
  wants to decide something global raises an `open_question` instead.
- **Locks are named specifics.** "The grandmother's faded headband, too big
  until the return" locks; "a meaningful object" is a proposal that hasn't
  finished cooking.
- **Checkpoint traces are part of the record.** The `<!-- honesty checkpoint
  @Ln -->` comments prove the reassertion mechanism fired; never backfill
  one that didn't.
- **Harvest is opt-in and out of scope here.** Sidecars become harness
  evidence only when Sean registers them under the harvest registry
  contract (private lane, referenced by name only). This file's only job on
  that front: stay append-only, stamped, and axis-clean so registration is
  cheap.
