# Adversarial review — `creative-partner` skill

**Verdict: revise.** The happy-path creative loop is strong, and the ratified reason rules survived the generalization well, but the skill is not yet safe to treat as an auditable, harvest-ready session system. The two highest-risk failures can put verbatim personal material in a repository or leave the session with no sole deliverable; several other contracts are asserted without enough mechanics to survive collision, resumption, compaction, malformed divergence output, or deterministic parsing.

Sound as written: divergence is genuinely default-OFF at the policy level (exact stall gate, Sean's yes for this run, prior approval does not roll over, and a second run requires a new explicit ask); the critic vocabulary consistently keeps `machine_fate_hypothesis` and the lean machine-authored; harvest remains opt-in with no registration, promotion, or auto-memory; the public files contain no taste corpus and the private reference slot is gitignored; the volunteered-reason, one-guess, bare-agreement, silence, late-why, and `SUPERSEDES` intentions match the proven anima spine. The named exclusions for `brainstorm-front-door`, `grilling`, and `writing-voice-modes` are also clear. The findings below concern places where the mechanics do not yet make those intentions dependable.

## f1 — dangerously-wrong

**(a) Severity:** dangerously-wrong.

**(b) Exact text at issue:** `.claude/skills/creative-partner/SKILL.md` § “Step 0 — open the session sidecar”: “`$CREATIVE_HARNESS_HOME` defaults to `~/.creative-harness/`. Never place a sidecar inside a repository working tree.” `.claude/skills/creative-partner/references/sidecar-contract.md` § “Location and naming”: “The skill reads the environment variable so the harness home can move” and “Never inside a repository working tree.”

**(c) Concrete failure scenario:** the location rule is declarative, not a preflight. If `CREATIVE_HARNESS_HOME=.` or names a symlink that resolves into a repository, the orchestrator can write to exactly `$CREATIVE_HARNESS_HOME/partner-sessions/...` and claim compliance while committing Sean's verbatim reasons to a tracked tree. An empty value also has no defined relationship to the stated unset-variable default. The default-unset case is handled; an unsafe or ambiguous configured value is not.

**(d) Minimal proposed amendment:** replace the location setup prose in both files with:

> Before any create, read, or append, resolve the harness home and target to canonical absolute paths, following symlinks. If `CREATIVE_HARNESS_HOME` is unset or empty, use `~/.creative-harness/`. Refuse to start unless the target is under the resolved `<harness-home>/partner-sessions/` and outside every Git working tree. Treat the environment value as a quoted literal path. If either property cannot be proved, report the resolved path immediately and write nothing.

## f2 — dangerously-wrong

**(a) Severity:** dangerously-wrong.

**(b) Exact text at issue:** `SKILL.md` opening: “There is no other deliverable. **The sidecar IS the deliverable**”; § Step 0: “If the file can't be written, keep the identical discipline inline in the conversation and say so.” `references/sidecar-contract.md` § “Location and naming”: “If the file can't be written, keep the identical discipline inline in the conversation and say so at wrap.” The checkpoint later requires “Re-read the sidecar file from disk” and “Leave an audit trace in the sidecar.”

**(c) Concrete failure scenario:** a disk-full, permission, or interrupted-write failure after L8 permits the orchestrator to continue taking reasons through L15, disclose the failure only at wrap, skip the required disk rereads and traces, and finish with chat text instead of the sole deliverable. The most important failure path therefore invalidates the audit contract while the orchestrator can still say it followed the inline fallback.

**(d) Minimal proposed amendment:** replace both fallback sentences with:

> If initial creation, any append or header update, or any required read-back fails, tell Sean immediately and pause before the next proposal, question, lock, or divergence call. Retry only the failed operation. Resume only after rereading the file from disk proves the exact last durable entry and the failed mutation has landed. Conversation text is not a substitute sidecar and never counts as the deliverable.

## f3 — structural

**(a) Severity:** structural.

**(b) Exact text at issue:** `references/sidecar-contract.md` § “Location and naming”: “One file per session: `$CREATIVE_HARNESS_HOME/partner-sessions/<YYYY-MM-DD>-<slug>.md`.” `SKILL.md` § “Honesty checkpoint”: “the sidecar makes resumption trivial.” No reviewed file defines existing-path behavior, writer ownership, or a resume procedure.

**(c) Concrete failure scenario:** two sessions on the same date choose the same slug. One can truncate the other, or both can append duplicate L1/L2 entries and race on the `modes:` header. Separately, a resumed orchestrator has no rule for validating the project and identity stamps, deriving the next lock ID, recognizing whether L10's checkpoint is due, or preserving the already-spent divergence budget. “Append-only” does not prevent concurrent interleaving.

**(d) Minimal proposed amendment:** add under “Location and naming”:

> Create a new-session path exclusively; never overwrite or append to an existing path as a new session. On collision, choose an unused slug suffix. Hold exclusive writer ownership for the session and refuse a write if another session owns the file. Resume only when Sean explicitly names the existing sidecar; first reread it top to bottom, validate its identity and project stamps, derive the next lock ID, checkpoint state, `modes:` history and divergence-run count, and then continue without changing existing entries.

## f4 — structural

**(a) Severity:** structural.

**(b) Exact text at issue:** `references/divergence-stage.md` § “Generate”: “Dispatch 4 sub-agents in parallel. **The isolation invariant:** each generator sees ONLY (a) the reframed problem statement with its named constraints and (b) its own frame card — never the sidecar, never the conversation, never a sibling's output, and no tools.” The reframe step also says: “Locked decisions from the sidecar that bear on this axis are constraints.”

**(c) Concrete failure scenario:** the text states an invariant but gives no invocation requirements. An eager orchestrator can reuse/resume an agent, allow its default tools, or rely on “ignore the conversation” inside a prompt and still call the result isolated. It can also copy a bearing lock, its `why`, Sean's opening ask, or an employer identifier into the permitted reframe and truthfully say the generator never saw the sidecar itself. That defeats both anti-anchoring and need-to-know privacy. The critic's nominal separation is sound, but has the same missing fresh-context/tool-denial mechanics.

**(d) Minimal proposed amendment:** replace the first paragraph of “Generate” and tighten “Reframe” with:

> Launch four distinct fresh sub-agents in one parallel dispatch; never reuse or resume an agent. At invocation, use the runtime's deny-list (`disallowedTools`) to deny every available tool, including agent spawning. Give each agent exactly the minimal reframed axis plus one complete frame card; do not rely on a prompt instruction to ignore inherited context. Launch the critic as a fifth fresh, tool-denied call with only the four returned payloads. If the runtime cannot enforce fresh context and tool denial, do not run divergence.
>
> Paraphrase bearing locks into the minimum operational constraints the axis needs. Never copy an ASK, `why`, `late why`, identity metadata, personal/employer identifier, filesystem path, credential, or secret into a generator or critic payload. If safe abstraction would change a necessary constraint, keep the axis in-room.

## f5 — structural

**(a) Severity:** structural.

**(b) Exact text at issue:** `references/sidecar-contract.md` § “Shape” specifies `- why (verbatim): "<Sean's one-line reason, quoted exactly>"`, `- options: <distinct named specifics, each WITH its tradeoff>`, `- [Ln] SUPERSEDES [Lk]: <new decision + the orchestrator's account of what changed>`, and `modes: <none | diverge:<axis> ...>`. `SKILL.md` § “The loop” anticipates “two option rounds” on one axis, while the contract says “one block per axis wherever possible.”

**(c) Concrete failure scenario:** this is a human-readable example, not a deterministic harvest grammar. For `Because he called it "finished"`, one parser can terminate the reason at the inner quote and another at the last quote; a raw newline can look like a new Markdown record. Options may be commas, semicolons, nested bullets, or paragraphs, so parsers will disagree about option boundaries, tradeoffs, frame IDs, and which option owns a `machine_fate_hypothesis`. A `SUPERSEDES` parser cannot separate the new decision from the orchestrator's change account. Repeated same-axis rounds can be merged, overwritten, or treated as duplicate keys. Multiple `modes:` entries have no separator grammar.

**(d) Minimal proposed amendment:** replace the placeholders with a canonical encoding while retaining the two sections and four proposal kinds:

> Every ASK, decision, why, late-why, change-note, observation, recommendation, and open-question payload is a JSON string on one physical line; JSON decoding must reproduce the original text exactly. Every proposal round is a new immutable block headed `### <axis-slug> — round: <positive integer>`. Under `options`, use nested records with stable block-local IDs and fixed fields: `id`, `text`, `tradeoff`, `frame` (`orchestrator` when not divergent), and `machine_fate_hypothesis` (`null` when absent). A `SUPERSEDES` line contains only the target ID, axis, and new decision; put the orchestrator account in a separate `change_note (orchestrator)` sub-line. Encode `modes:` as a JSON array of run tags, initially `[]`.

## f6 — structural

**(a) Severity:** structural.

**(b) Exact text at issue:** `SKILL.md` § “Honesty checkpoint”: “if context auto-compacts mid-session, say so plainly and recommend wrapping or splitting into a fresh session … Recommendation only; Sean decides.”

**(c) Concrete failure scenario:** Sean chooses to continue after compaction. The orchestrator may have lost the current lock number, current axis, selected frames, whether a one-guess allowance was already spent, or whether a reason was pending, but the skill requires only a recommendation to wrap. It can then duplicate IDs, guess twice, dispatch after stale approval, or miss a checkpoint while claiming Sean chose continuation.

**(d) Minimal proposed amendment:** replace the compaction clause with:

> After any context compaction, do not continue the loop until you reread the loop and reason rules and reread the sidecar from disk top to bottom. Reconstruct the next lock ID, checkpoint and mode state, current axis, pending decision/reason, and frame confirmation. If the record cannot prove whether the current axis's one guess was spent, take the stricter path and do not guess again. Then say compaction occurred and recommend wrapping or splitting; Sean still decides. Do not add the regular five-lock audit comment unless that checkpoint is actually due.

## f7 — structural

**(a) Severity:** structural.

**(b) Exact text at issue:** `references/divergence-stage.md` § “Generate” requires four generator results; § “Critique” says the critic “sees all generated options”; § “Land” hardcodes `calls: 5`; § “What this stage never does” covers only a “weak” output: “Never retries a ‘weak’ run silently. If the output is poor, say so.”

**(c) Concrete failure scenario:** generator three errors or returns prose without frame stamps/tradeoffs. The orchestrator can silently replace it and spend six calls, send only three frames to the critic while logging a complete-looking five-call run, abort after four calls with no durable trace, or let garbage silently contaminate the shortlist. The happy-path five-call budget is clear; failure accounting is not.

**(d) Minimal proposed amendment:** add after the generator instructions:

> Each attempted generator is one of the four and is never replaced. Represent a failed, empty, or schema-invalid return as an explicit failure marker in that generator's slot; pass all four slots to the critic and record failures in the diverge block's `observations`. The critic remains the fifth and final call and may return no shortlist. `calls: 5` means five attempted calls, not five successful outputs. Any further generator or critic attempt is a new run requiring Sean's explicit approval and the cost statement.

## f8 — structural

**(a) Severity:** structural.

**(b) Exact text at issue:** `SKILL.md` § “Identity contract”: “The stamps are load-bearing: they are what lets the harness say exactly which skill version and which pack version shaped a session.” Step 0 then specifies only “skill name + SKILL.md content hash … short form” and “pack name + hash or `pack: none`.” `references/sidecar-contract.md` § “Shape” uses `skill: creative-partner @ <sha256-short of SKILL.md>` and `pack: <partner-pack @ <hash> | none>`; it has no explicit `date:` field despite Step 0 calling date a header stamp.

**(c) Concrete failure scenario:** `frame-deck.md` or `divergence-stage.md` changes without changing `SKILL.md`; two behaviorally different sessions then carry the same purported version. Two writers can choose different “short” lengths. Before the pack exists, `pack: none` does not stamp the `partner-pack` identity at all. A parser can take the title date as the stamp while another requires a header key. The header therefore cannot support its stated exact-provenance job.

**(d) Minimal proposed amendment:** make the header grammar explicit:

> `skill: creative-partner @ sha256:<full SKILL.md hash>`
>
> `sidecar_contract: sha256:<full sidecar-contract.md hash>`
>
> `frame_deck: sha256:<full frame-deck.md hash>`
>
> `divergence_stage: sha256:<full divergence-stage.md hash>`
>
> `pack: partner-pack @ <full hash | none>`
>
> `date: <YYYY-MM-DD>`
>
> Hashes are exactly 64 lowercase hexadecimal characters. Keep `model`, `project`, and the canonical `modes:` line as required header fields.

## f9 — structural

**(a) Severity:** structural.

**(b) Exact text at issue:** `SKILL.md` § “The loop” says: “Sean decides; you lock. Write the lock as a named specific, then capture the reason.” The next section says: “Before writing a LOCKED DECISION … ask one short question, then write the lock.” Step 0 says: “Record Sean's opening ask verbatim as the first locked entry,” while the reason section says “Every lock carries Sean's reason” and `references/sidecar-contract.md` says locks are written “only after Sean decides.” The template nevertheless shows `[L1] ASK` with no reason.

**(c) Concrete failure scenario:** one orchestrator writes the decision first and asks why later; another waits to write it. A failure or compaction between those operations produces different durable history. A third asks “Why that one?” about the opening ask, while a fourth excludes L1 from the L5 cadence because it was not a decision. All can quote some part of the contract as authority.

**(d) Minimal proposed amendment:** replace loop step 4 and add an L1 exception:

> **Sean decides; you complete reason capture, then lock.** Apply the reason rules first, including the volunteered-reason and silence paths; then append the decision and its optional why sub-line in one durable mutation.
>
> `[L1] ASK` is the session-origin lock, not a Sean decision. It is the sole exception to the reason ask and “only after Sean decides” rules, but it does count in lock numbering and the L5/L10 checkpoint cadence.

## f10 — structural

**(a) Severity:** structural.

**(b) Exact text at issue:** `SKILL.md` frontmatter: “Use when Sean brings a problem, idea, or decision to think through with a partner — any domain … or anything else.” Trigger phrases include “I'm stuck on” and “cast a wide net”; only the three named neighbor exclusions follow. The same description says `USER-INVOKED` without defining whether the listed generic phrases constitute that invocation.

**(c) Concrete failure scenario:** “I'm stuck on this frontend build error” or “cast a wide net for primary sources” matches literally. The model can start a persistent, write-producing, one-question-at-a-time partner session instead of diagnosing or researching. The named neighbor boundaries are good, but the catch-all still captures unrelated execution, review, factual-answer, and artifact-production work.

**(d) Minimal proposed amendment:** replace the first two description sentences with:

> Use only when Sean explicitly asks for an interactive partner session or collaborative option-and-decision deliberation, such as “partner session,” “help me think through these options,” “let's ideate on,” or “challenge this idea.” Do not trigger merely because a request mentions a problem, decision, being stuck, or casting a wide net; requests to execute, diagnose, review, research, answer a factual question, or produce an artifact stay with their owning workflow. USER-INVOKED.

Keep the three existing named exclusions unchanged.

## f11 — structural

**(a) Severity:** structural.

**(b) Exact text at issue:** `SKILL.md` and `references/frame-deck.md` require “2 native to the axis's domain, 1 foreign, 1 wild.” The deck defines only four home-domain groups: story/writing, art direction/visual, product/work execution, and frontend/build, while the skill promises “any domain … or anything else.” `references/divergence-stage.md` says the orchestrator “assigns the axis's domain” and should “Offer the selection to Sean in one line before dispatch — he may swap any card.”

**(c) Concrete failure scenario:** a relationship, music, medical, or legal-adjacent axis has no native group. The orchestrator can silently declare arbitrary cards native and produce a compliant-looking 2/1/1 header. It can also print the four cards and dispatch in the same turn: technically the offer appeared “before dispatch,” but Sean never had a chance to swap. This is a rationalization path around both selection quality and user control.

**(d) Minimal proposed amendment:** add to frame selection:

> For an axis outside the four home domains, assign the closest home domain by the kind of thinking required, state that mapping with the proposed cards, and treat that assignment as the meaning of `native`. If no mapping is defensible, do not dispatch until Sean accepts one. Ask Sean to confirm or swap the four cards and wait for his reply before dispatch.

## f12 — minor

**(a) Severity:** minor.

**(b) Exact text at issue:** `references/frame-deck.md` card `pre-mortem`: “assume the current lean shipped and failed; name the causes of death, then derive each option from a cause.” Card `inversion`: “first specify how to make the thing fail with certainty, then invert each failure cause into an option.” Card `silhouette-first` bans “anything that needs a paragraph to visualize,” while `references/divergence-stage.md` requires “one short paragraph per option.”

**(c) Concrete failure scenario:** if `pre-mortem` and `inversion` are selected together, both generators enumerate failure causes and reverse them into options, so the advertised structural spread collapses. The silhouette ban is also subjective and superficially conflicts with the required paragraph output; a lazy generator can either reject every option or claim any paragraph-length description “reads in silhouette.” The other ten forcing moves are meaningfully distinct and mostly mechanically followable.

**(d) Minimal proposed amendment:** replace the two overlapping moves and the silhouette ban with:

> **pre-mortem:** Backcast a dated causal sequence from launch to failure. Each option must be an early intervention, gate, or cheapest test tied to one link in that sequence. Ban an option without an explicit cause-to-intervention link.
>
> **inversion:** Design deliberate anti-goal behaviors, then reverse one hidden operating assumption per option into a design principle. Ban mitigations, gates, tests, and contingency plans; those belong to `pre-mortem`.
>
> **silhouette-first ban:** Ban any option whose defining distinction depends on color, texture, dialogue, labels, or explanatory context rather than shape, pose, and staging.
