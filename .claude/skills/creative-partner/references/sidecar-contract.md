# Partner session sidecar contract — `partner-sessions/<date>-<slug>.md`

The running memory and sole deliverable of a `creative-partner` session. One
file, a stamp header, two blocks, hard ownership. Generalized from anima's
front-door sidecar contract; the two-block discipline is identical, the emit
is gone, and the stamp header is new.

## Location, naming, and the preflight

- One file per session:
  `$CREATIVE_HARNESS_HOME/partner-sessions/<YYYY-MM-DD>-<slug>.md`
- **Preflight before any create, read, or append:** resolve the harness home
  and the target to canonical absolute paths, following symlinks. If
  `CREATIVE_HARNESS_HOME` is unset or empty, use `~/.creative-harness/`;
  treat the environment value as a quoted literal path. Refuse to start
  unless the resolved target is under `<harness-home>/partner-sessions/` and
  outside every git working tree. If either property cannot be proved,
  report the resolved path immediately and write nothing. A missing
  `partner-sessions/` directory under a preflight-clean home is created,
  not an error.
- **Never inside a repository working tree.** Sidecars carry verbatim
  personal reasons; the harness home is local-only and backed up as a
  protected class. The project a session serves is recorded *inside* the
  file, not by where the file sits.
- **New sessions create exclusively.** Never overwrite or append to an
  existing path as a new session; on collision, choose an unused slug
  suffix (`-2`, `-3`…). Hold exclusive writer ownership for the session and
  refuse a write if another session owns the file.
- **Resume only when Sean explicitly names an existing sidecar.** First
  re-read it top to bottom; validate its identity and project stamps;
  derive the next lock ID, checkpoint state, `modes:` history, and
  divergence-run count; then continue without changing any existing entry.
- **Write failures fail stop.** If creation, any append or header update,
  or any required read-back fails, tell Sean immediately and pause before
  the next proposal, question, lock, or divergence call. Retry only the
  failed operation; resume only after a disk re-read proves the last
  durable entry and the failed mutation landed. Conversation text is not a
  substitute sidecar and never counts as the deliverable.

## Header grammar (exact — every field required)

```
skill: creative-partner @ sha256:<full 64-hex hash of SKILL.md>
sidecar_contract: sha256:<full hash of sidecar-contract.md>
frame_deck: sha256:<full hash of frame-deck.md>
divergence_stage: sha256:<full hash of divergence-stage.md>
pack: <partner-pack @ sha256:<full hash> | none>
model: <the launched model id>
project: <what this session serves>
date: <YYYY-MM-DD>
modes: []
```

Hashes are exactly 64 lowercase hex characters (`shasum -a 256`). All four
skill files are stamped because any of them changes session behavior; two
behaviorally different sessions must never carry identical stamps. `modes:`
is a bracketed list of run tags (e.g. `[diverge:color-system]`), starting
empty; it is the header's only mutable line.

## Shape

```markdown
# Partner session — <slug> — <date>

<header stamps per the grammar above>

## LOCKED DECISIONS   <!-- orchestrator-owned; APPEND-ONLY -->

- [L1] ASK (verbatim): "<Sean's opening words, unedited>"
- [L2] <axis>: <the locked decision, a named specific>
  - why (verbatim): "<Sean's reason, quoted exactly; omit the whole sub-line
    if he skipped the question>"
- ...
<!-- honesty checkpoint @L5 — rules re-read -->
- late why for [Lk] (verbatim): "<a reason Sean volunteered after the lock,
  OR his correction of a mis-taken reason line; appended as a new entry
  that supersedes the sub-line for harvest purposes — the lock itself is
  never edited>"
- [Ln] SUPERSEDES [Lk]: <axis> — <the new decision only>
  - change_note (orchestrator): <the orchestrator's account of what changed>
  - why (verbatim): "<Sean's reason for the change>"

## PROPOSALS LOG   <!-- stage-appended; four content kinds only -->

### <axis-slug> — round: 1      <!-- ONE axis per block; a new pass on the
                                     same axis is a NEW block, round: 2 -->
- observations: <the live tension, in a line>
- options:
  - id: <axis-slug>.1
    text: <a named specific>
    tradeoff: <its cost, in a line>
    frame: orchestrator
    machine_fate_hypothesis: null
  - id: <axis-slug>.2
    ...
- recommendation: <the stated lean and its reason, phrased so Sean can
  accept or veto in a line>
- open_questions: <what the room can't resolve alone>

### diverge:<axis-slug> — round: 1 — frames: [<4 ids>], calls: 5
- observations: <why divergence was invoked/offered; the reframed problem;
  any generator failure slots>
- options:
  - id: <axis-slug>.d1
    text: ...
    tradeoff: ...
    frame: <originating frame id>
    machine_fate_hypothesis: <null | "one-line trap reason">
- recommendation: <the critic's lean, marked machine-proposed>
- open_questions: ...
```

## Parsing rules (what makes the format deterministic)

- **A verbatim quote runs to the end of its entry.** An entry ends at the
  next line opening a new record at the same or shallower indent (`- `,
  `### `, `## `, or a checkpoint comment) — never at an inner quote mark.
  Inner quotes, typos, and line breaks inside an entry belong to the quote.
- **Option records carry fixed fields** — `id`, `text`, `tradeoff`,
  `frame` (`orchestrator` when not from a divergence run),
  `machine_fate_hypothesis` (`null` when absent). IDs are block-local and
  stable; rulings and fates reference them.
- **Round headers disambiguate repeated axes.** Same axis revisited = new
  block with the next round number; blocks are immutable once written.
- **SUPERSEDES entries carry the new decision only**; the orchestrator's
  account lives in the `change_note (orchestrator)` sub-line; Sean's reason
  in the `why (verbatim)` sub-line. Three lines, three authors, no merging.

## Rules

- **Only the orchestrator writes LOCKED DECISIONS**, and only after Sean
  decides — with one exception: `[L1] ASK` is the session-origin lock, not
  a Sean decision; it takes no reason ask, but counts in lock numbering and
  the checkpoint cadence. Reason capture completes BEFORE the lock is
  written; decision + why land in one durable mutation.
- Locks are append-only: a change is a new `SUPERSEDES` entry, never an
  edit — the sidecar is the session's audit trail, and the harvest layer
  treats any rewrite of already-written history as a tamper signal.
- **Every lock carries Sean's own one-line reason, marked verbatim** — the
  full rules live in SKILL.md (verbatim-or-nothing; a volunteered reason
  satisfies the ask; one guess only; only his words land; silence records
  nothing; a late-volunteered reason appends, never edits).
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
