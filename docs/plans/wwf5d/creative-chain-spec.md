# Creative-chain improvement spec (Substack writing chain)

> Provenance: extracted verbatim from the BT3 blind Fable run
> (`fable-runs/bt3-fable.md`, Artifact 2 + wow move), 2026-07-05. Chain files audited
> @ `93e5725`. Companion evidence: `fable-runs/bt3-diff.md` (note the OPUS+ items
> worth folding in at implementation: cut-vs-reorder clarification; section-level
> spine-adherence check at critique). Implementer: Opus, Phase C. Hard rule: 
> `writing-voice-modes/SKILL.md` is Tier-1 — zero edits.

## Artifact 2 — Intent-Carrying Improvement Spec (chain-level)

Implementer note: you may be a smaller model than the one that audited. Every fix below carries its reasoning — when you hit an edge case this spec didn't anticipate, decide in favor of the reasoning, not the letter. One rule dominates everything: **`writing-voice-modes/SKILL.md` is Tier-1 and receives zero edits.** Every fix routes around it.

### Objective

The chain exists to move Sean's early taste decisions — beat map, value verdict, locked takeaway, voice choices — intact into a published Substack post that feeds his portfolio and a recruiter audience (grounding (a), (b)). The 2026-07-04 first pass named the right artifacts; what still leaks is their *transport and binding*: artifacts cross the locked voice stage on assertion rather than mechanism, every downstream intake silently tolerates their absence, the strictest verdicts bind nobody, and several real decisions (voice dial, per-piece overrides, applied fixes) have no carrier at all (grounding (c)). Left as-is, the chain's worst outputs are the ones Sean trusts most: a `ship` stamped by an un-anchored critique, and a polished post its own gate ruled unshippable.

### Desired outcome

Observable differences, before → after:

1. A mid-chain compaction or fresh-session resume can no longer silently un-anchor critique: it either has the ledger/verdict or it names the loss and refuses to stamp `ship`.
2. A recruiter-dialed piece survives critique without a gritting-up revise request; the one revise pass is spent only on real findings.
3. A draft that fails the structure/value gate can never arrive at Substack polished; the chain stops loudly with the draft and its manifest parked for Sean.
4. A blunt sentence the gate demanded survives humanity-pass on every run, because the applied fix is enumerated, not inferred.
5. Sean's explicit per-piece calls (a pinned dial, an authorized topic) are honored downstream instead of reverted by his own pipeline.
6. Every completed run ends with a one-screen "intent thread intact" block — the wow bar (grounding (d)) as a visible artifact rather than an aspiration.

### The backbone fix — the Chain Manifest (closes F3, F4, F9, F11, F12; enables the thread check)

**Change.** Promote stage 1's Handoff Block into a single accreting **Chain Manifest**: one fenced block, created by `storytelling-architecture`, appended to (never rewritten) by each subsequent editable stage, and **re-emitted verbatim at the end of every stage's output**. Fields:

- *Stage 1 writes:* working title; scaffold (F12); the beat map itself (numbered, one line per beat); open-loop ledger — with the loop **question text required** per entry (F6); central loop; crest beat; seam beat; section-end pull beats (F13); any per-piece overrides already known (F11).
- *Stage 2 appends:* Value Gate verdict + the three slots; the locked takeaway (the exact sentence); the Rule-of-One promise; pivot-line job (where + what it must assert); ask placement.
- *Voice boundary — owned by the orchestrator, not the locked stage:* whoever invokes the chain (the interactive session or the drafter agent) prepends the manifest to the voice invocation and re-attaches it to the voiced draft, adding a one-line **voice header**: mode, dial, borrowed techniques (F5). This is recorded *about* the voice stage from outside it; the Tier-1 file is not touched.
- *Stage 4 appends:* verdict; findings; and on any revise, the **applied-fix record** — finding → the quoted prose span that changed (F7).
- *Stage 5 appends:* the Intent Thread Check results (below).

**Persistence rule.** In-context re-emission is the default — this *respects* the existing "handoff is in-context, not a saved file" philosophy while fixing its physics: a block re-emitted at every stage boundary always sits near the context tail, which is what survives compaction. Headless runs (Substack-Drafter) persist manifest + draft together as the inter-process artifact, because there is no shared context to ride in.

**Intake rule (edit stages 2, 4, 5).** In chain mode the manifest is REQUIRED. When a needed field is absent: proceed with the degraded check, but *name the missing artifact in the output*, and — critique specifically — **cap the verdict at `revise`** while the ledger or Value Gate verdict is missing. Never `ship` un-anchored.

**Reasoning to carry.** The named artifacts already exist; the failure is that their transport across the locked stage is an assertion ("these travel in-context through the voice stage") that no one executes, and every consumer treats absence as normal. Assigning transport to the orchestrator makes the assertion an executable duty without touching the Tier-1 file. Re-emission (not a file) is the compaction defense for interactive runs. The verdict cap is the crux: a silent degrade converts transport loss into a trusted-but-wrong `ship` (F4, the audit's worst finding); a loud cap converts the same loss into a one-line fix — re-supply the manifest and re-run the gate. If you must choose between re-emitting the manifest "too often" and risking a silent drop, re-emit too often.

### Fix per finding

**F1 (structural) — one owner for the seam definition.** Edit `storytelling-architecture`: define the seam beat as *the beat where the central loop closes AND the Transfer lands — one beat*, and repair the example map so PAYOFF and SO-CAN-YOU are a single beat carrying both labels. Edit `substack-value-engine`: when an arriving map's seam beat ≠ the central-loop close, **return the map to storytelling by name** (a wired micro-back-edge) — never silently re-weld. *Reasoning:* value-engine owns the seam craft (its same-beat rule is the correct craft: the Transfer must feel like the story finishing), so storytelling's coordinates must conform at map-time, where a fix costs one beat edit — not at draft-time, where it costs a re-voice. The forbidden move is value-engine quietly relocating the seam: that is exactly the re-derivation the chain bans, even when the relocation is "right."

**F2 (structural) — pre-empt the reorder license from upstream.** Add one clause to the chain-contract sections of `storytelling-architecture` and `substack-value-engine`: "The beat map is not a 'skeleton' the voice stage may reshape; the personal-essay exception in `writing-voice-modes` refers to `creative-writing`'s format skeleton only. Beat order binds at every dial." *Reasoning:* the ambiguous sentence lives in a file that cannot be edited, so the disambiguation must arrive WITH the map. Upstream files already state constraints on the voice stage ("must never reorder beats") — this sharpens an existing constraint at the seam into the locked stage, which the Tier-1 rule explicitly permits.

**F3 (structural)** — closed by the backbone fix: the takeaway and verdict ride the manifest in and out of the voice stage via orchestrator re-attachment, and critique's value check keys on the manifest's promise + takeaway rather than trusting arrival. *Reasoning:* no acknowledgment can be demanded from inside the locked stage, so the boundary event has to be owned from outside it.

**F4 (dangerously-wrong)** — closed by the backbone fix (manifest + loud degrade + verdict cap). *Reasoning restated because it is the one to protect in every edge case:* critique's authority comes from being anchored; an un-anchored critique that still stamps `ship` is worse than no critique, because it converts a transport bug into trusted slop. When in doubt, downgrade the verdict and say why.

**F5 (structural) — carry the register decision; interpret the analyzer through it.** Voice header in the manifest (backbone fix). Edit `writing-critique`: an interpretation rule — analyzer deltas are read *relative to the declared dial*; at dial ≤ 60%, lower burstiness/grit vs the 100% baseline is expected and is not a finding; only deltas unexplained by the declared register escalate. Do NOT modify `baseline.json`, the MATTR window (locked at 50 by critique's own text), or the locked stage's dial table. *Reasoning:* the baseline is Sean-at-full-intensity; using it as an absolute target re-derives a register decision the chain already made, and the cost is concrete — the single revise pass is the scarcest resource in the chain, and a false flatness finding spends it making a recruiter-facing piece worse. The dial is an input to *interpretation*, never a knob to tune the analyzer with.

**F6 (structural) — re-key loop closure to prose-space.** Edit `storytelling-architecture`: ledger entries require the loop question text (the format already shows it parenthesized; make it mandatory). Edit `writing-critique`: closure is checked as "does the draft answer this ledger question?" — beat numbers demote to hints. *Reasoning:* the draft only exists in prose-space; questions are checkable there, beat numbers are not. This also makes legitimate beat compression (which the voice stage's own conflict table endorses) stop producing phantom blocking findings that burn the revise pass.

**F7 (structural) — the revise request carries the manifest; the fix list enumerates applied fixes.** Edit `writing-critique`: the structured revise request includes the manifest (map, Handoff Block, takeaway) alongside the finding; after the revise + re-critique, the fix list must contain the applied-fix record (finding → quoted changed span), not just surviving findings. Edit `writing-humanity-pass`: its protection clause keys on applied-fix records. *Reasoning:* "protect prose changes made to satisfy a finding" is only executable if those changes are enumerated; today the protection set is empty precisely when a fix was applied and resolved — the only time protection matters. And a revision written against a bare finding, without the spine in context, is a fresh chance to drift; the one revise pass must be the *most* anchored write in the chain, not the least.

**F8 (dangerously-wrong) — make the verdict a router, not a label.** Edit `writing-critique` (headless branch): split the routing — line-level blocking finding → one revise to voice-modes (unchanged); **structure/value-gate failure → verdict `structural-rework` and STOP the chain**: park the draft + manifest for Sean (or return to stages 1–2 in an interactive run); never pass through, including after a failed re-critique. Edit `writing-humanity-pass`: intake precondition — in chain mode, run only when the manifest verdict is `ship`, or `revise` with the applied-fix record present; on `structural-rework`, refuse and say why. *Reasoning:* critique's own semantics already say a broken spine is not a line fix; the headless algorithm just never got that branch, so it routes spine breaks to the one stage that cannot fix them without violating the no-reorder contract. The stop IS the success path for a bad draft — value-engine's contract is explicit that the worst outcome is a well-voiced piece that solves nothing. An implementer tempted to "be helpful" by letting the draft continue is recreating the bug.

**F9 (structural)** — closed by the backbone intake rule applied at `writing-humanity-pass` (fix list required in chain mode; absence named, scrub proceeds in maximum-preservation mode rather than silently unprotected).

**F10 (structural) — give the hardest gate the same machine voice as the others.** Edit `substack-value-engine`: emit the same trailing-HTML machine-readable verdict block the other two gate stages already define, on both PASS (verdict, slots, takeaway, promise) and BLOCK (missing slot, disposition). BLOCK and Rule-of-One "split" verdicts name their return target (backlog / back to storytelling for a re-map of the surviving itch). *Reasoning:* a uniform verdict-block vocabulary lets even a simple orchestrator branch on one format; today the only stage whose verdict can stop the chain is the only one a drafter can miss by parsing prose.

**F11 (structural) — a carrier for per-piece overrides.** The manifest's `per-piece overrides` field (backbone fix), written at grounding time: pinned dial + audience; any authorized suppressed-topic use, quoted in Sean's own words. Edit `writing-critique` (hiring-signal dimension) and `writing-humanity-pass` (scrub): consult overrides before flagging or stripping. *Reasoning:* every exception clause in the chain says "unless Sean explicitly asks" — but an authorization with no carrier is unimplementable three stages later, so the chain currently *reverts Sean's explicit calls by design*. Overrides are decided intent of exactly the same class as the takeaway; they ride the same vehicle. Edge rule for a weaker implementer: an override must be quoted, not paraphrased — a paraphrased override is how scope creeps back in.

**Minor findings, listed:**
- **F12** — add a `scaffold:` line to the manifest (stage 1). One line; lets critique defer to the committed shape by name.
- **F13** — stage 1 lists section-end pull beats in the manifest; `writing-humanity-pass` checks its dash replacements on those lines preserved forward pull (function, not punctuation).
- **F14** — `writing-humanity-pass` delivery: the publishable text contains zero HTML comments; the change summary and verdict block attach to the manifest instead. One sentence in its Step 3.

### The wow move (carry from the wow-gap scan)

Extend `writing-humanity-pass`'s existing fix-list check into the full **Intent Thread Check**, appended to the manifest as the chain's final act: locked takeaway present and welded to its named artifact · every ledger question answered in prose · ask sideways / overrides honored · declared dial consistent with the delivered register · verdict `ship` · applied fixes intact · zero dashes · zero HTML comments in the publishable text. One screen. *Reasoning:* this is grounding (d) made observable — the difference between a chain that claims a single thread of intent and one that can show it on every run. It costs one section in one editable file, because every input it needs already rides the manifest.

### What NOT to change

1. **`writing-voice-modes/SKILL.md` — zero edits, full stop.** Not Sean Mode, not House Style, not the signature moves, not the dial table, not its Related Skills paragraph. Every fix above routes through the four editable stages and the orchestrator. If an edge case seems to require touching it, the answer is: move the duty to the orchestrator or the adjacent stage.
2. **The named artifacts from the 2026-07-04 first pass** — Handoff Block, open-loop ledger, locked takeaway, Value Gate verdict, critique fix list. The concepts and names are right and are referenced by name across files; this spec changes their *transport and binding*, never their names or existence. Renaming breaks every cross-reference.
3. **Critique's one-revise-pass cap and its anchored-external-target rationale.** Do not add loops "for safety" — the cap exists because un-anchored self-judged iteration degrades prose toward generic. The fixes make the one pass better-anchored; they must not multiply it.
4. **The analyzer's advisory status, `baseline.json`, the MATTR window locked at 50, and the baseline regeneration pipeline.** F5 is an interpretation rule, not an analyzer change.
5. **Humanity-pass's identity:** the em-dash hard rule, the VOICE-SAFE/FULL split, per-section classification, and its runs-LAST position.
6. **The Value Gate's three slots and BLOCK-stops-the-chain semantics, Rule of One, and the seam-as-finishing-the-story craft rule.** F1 conforms storytelling's coordinates to value-engine's craft rule — the rule itself is correct and untouched.
7. **Stage order** and the in-context-first handoff philosophy for interactive runs — re-emission is the mechanism; files are for headless runs only. Do not invent a file bureaucracy for a five-message interactive chain.
