# Divergence stage — mechanics

The adapted wide-net loop: isolated parallel takes wearing different frames,
then a separate critic pass. Architecture adapted from the MIT-licensed adhd
repo (Udit Akhouri) — the isolation invariant, the mechanical
generator/critic split, and trap-flagging with reasons — with Sean-domain
frames replacing the stock engineering-biased set. The honest claim, per the
teardown: this does not escape the model's training distribution; it samples
it more widely while protecting each take from anchoring on the others. That
is worth 5–10x a single answer *sometimes*, which is why it is a mode and
never a default.

## Preconditions (all three, every run)

1. **Sean said yes.** Either he invoked it by name, or the orchestrator
   offered it at a stall (two option rounds on one axis without a pick, or
   Sean calling the options samey) and he accepted. The offer always states
   the cost: "~5 extra calls."
2. **One axis.** The run targets exactly one contested axis, stated in a
   line. A run on "the whole project" is a smell — narrow it first.
3. **Budget clear.** One run per session by default; a second run in the
   same session requires Sean asking again explicitly. No chaining.

## The run

### 1. Reframe (orchestrator, in-room, no call)

Rewrite the axis's problem statement stripped of incidental anchors —
current tool names, the option leaning that stalled, "how we've been doing
it" — keeping every real constraint (budget, format, locked decisions).
Locked decisions from the sidecar that bear on this axis are constraints;
everything else from the session is anchor. Record the reframed statement in
the `### diverge:` block's `observations`.

### 2. Frame selection (orchestrator, logged)

Pick 4 frames from `frame-deck.md`: 2 native to the axis's domain, 1
foreign, 1 wild. The orchestrator assigns the axis's domain (an axis that
plausibly belongs to two domains gets the call surfaced, not buried). Offer
the selection to Sean in one line before dispatch — he may swap any card. The final selection goes in the block header:
`### diverge:<axis-slug> — frames: [id, id, id, id], calls: 5`.

### 3. Generate — 4 isolated calls

Dispatch 4 sub-agents in parallel. **The isolation invariant:** each
generator sees ONLY (a) the reframed problem statement with its named
constraints and (b) its own frame card — never the sidecar, never the
conversation, never a sibling's output, and no tools (tools are convergence
pressure). Each generator's instruction:

- Produce 3–5 mutually distinct options, each a named specific with its
  tradeoff, one short paragraph per option.
- Ban the first three obvious ideas — assume an unimaginative competitor
  already proposed them.
- Generate only. Do not evaluate, rank, or recommend.
- Stamp every option with the frame id.

### 4. Critique — 1 separate call

A single critic sub-agent sees all generated options (still not the sidecar
or the conversation) and returns, mechanically:

- **Clusters** — options that are the same idea wearing different hats,
  named as such.
- **One concrete strength per surviving option.**
- **Traps flagged with one-line reasons** — each labeled
  `machine_fate_hypothesis`. These are hypotheses for Sean to confirm or
  overrule, never verdicts; a real fate (`dud` / `usable-elsewhere`) exists
  only when Sean supplies or confirms it.
- **A shortlist and a stated lean**, marked machine-proposed.

### 5. Land, rule, lock

The orchestrator appends the whole run as ONE `### diverge:` proposals block
(four content kinds only; every option carrying its frame id), presents the
shortlist to Sean exactly like any other proposals round — one question,
recommendation first — and Sean rules. His picks, wave-offs, and reasons are
locked under the standard reason rules. Add the run to the header's `modes:`
line. Done — the mode leaves nothing behind except sidecar content.

## What this stage never does

- Never runs without Sean's yes for *this* run. Prior approval doesn't roll
  over.
- Never invokes other skills or tools inside generators or critic.
- Never writes a fate, a lock, or a reason — machines write candidates only.
- Never retries a "weak" run silently. If the output is poor, say so; a
  re-run is a new ask with the same cost stated.
