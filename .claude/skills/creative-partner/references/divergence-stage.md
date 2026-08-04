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
**Paraphrase bearing locks into the minimum operational constraints the
axis needs.** Never copy an ASK, a `why` or `late why` quote, identity
metadata, a personal or employer identifier, a filesystem path, a
credential, or a secret into a generator or critic payload — the generators
have no need to know, and verbatim personal material never leaves the
sidecar. If safe abstraction would change a necessary constraint, keep the
axis in-room and skip the run. Record the reframed statement in the
`### diverge:` block's `observations`.

### 2. Frame selection (orchestrator, logged)

Pick 4 frames from `frame-deck.md`: 2 native to the axis's domain, 1
foreign, 1 wild. The orchestrator assigns the axis's domain (an axis that
plausibly belongs to two domains gets the call surfaced, not buried). **For
an axis outside the four home domains** (music, legal, relationships,
anything else), assign the closest home domain by the kind of thinking
required, state that mapping alongside the proposed cards, and treat it as
the meaning of "native"; if no mapping is defensible, do not dispatch until
Sean accepts one. Offer the selection to Sean and **wait for his
confirm-or-swap reply before dispatching anything** — cards printed and
dispatched in the same turn is a violation, not an offer. The final
selection goes in the block header:
`### diverge:<axis-slug> — round: <n> — frames: [id, id, id, id], calls: 5`.

### 3. Generate — 4 isolated calls

Launch four **distinct, fresh** sub-agents in one parallel dispatch — never
reuse or resume an agent. At invocation, deny every tool via the runtime's
deny-list (`disallowedTools`), including agent spawning — tools are
convergence pressure, and a generator that can read files is not isolated.
**The isolation invariant:** each generator receives exactly (a) the
reframed problem statement with its named constraints and (b) its own frame
card — never the sidecar, never the conversation, never a sibling's output.
Do not rely on a prompt instruction to "ignore" inherited context; if the
runtime cannot enforce fresh context and tool denial, do not run divergence.
Each generator's instruction:

- Produce 3–5 mutually distinct options, each a named specific with its
  tradeoff, one short paragraph per option.
- Ban the first three obvious ideas — assume an unimaginative competitor
  already proposed them.
- Generate only. Do not evaluate, rank, or recommend.
- Stamp every option with the frame id.

**Failure accounting:** each attempted generator is one of the four and is
never replaced. A failed, empty, or schema-invalid return occupies its slot
as an explicit failure marker; all four slots pass to the critic, and
failures are recorded in the diverge block's `observations`. `calls: 5`
means five *attempted* calls, not five successful outputs. Any further
generator or critic attempt is a new run requiring Sean's explicit approval
with the cost stated.

### 4. Critique — 1 separate call

The critic is a fifth **fresh, tool-denied** sub-agent call (same invocation
rules as the generators) receiving only the four returned payloads —
including any failure markers — never the sidecar or the conversation. It
may return no shortlist if the surviving material is poor. It returns,
mechanically:

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
