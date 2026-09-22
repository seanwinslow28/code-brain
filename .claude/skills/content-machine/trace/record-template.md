# Record template — one immutable file per stage invocation

The content machine's copy of the trace kit's first piece (designed on [#261](https://github.com/seanwinslow28/code-brain/issues/261) with [#272](https://github.com/seanwinslow28/code-brain/issues/272); built on [#291](https://github.com/seanwinslow28/code-brain/issues/291), importing the Productcraft kit's grammar unchanged). One file per invocation at `creative-studio/content-machine/pieces/<run>/trace/pass-NN-<seat>-<kind>.md`, private by construction (the run folder is git-ignored), never edited after the invocation completes. Frontmatter for machine fields, three short sections for human ones. The record **indexes** the transcript; it never replaces it. Ruled out: dollar figures; prose about what the shaper "thought"; any of his words.

**Who writes which field.** The **orchestrating session** writes the launch fields before firing a stage (`pass` through `inputs`, `withheld`, `raw_log`) and the completion fields after it returns (`completed`, `wall_clock_s`, `meter`, `meter_source`, `outputs` with their hashes, `## Corpus read` from the transcript's file reads, `## Notes`); it appends to `checks` as gates and the pick land. The **shaper** writes its `## Moves` at the end of its draft card, never here. **Sean** writes labels in [labels-template.md](labels-template.md), never in a record.

The frontmatter is a YAML subset the checker parses with the stdlib: scalars, lists, one level of nesting, `- key:` blocks. Nothing else.

```markdown
---
pass: pass-05                          # pass-NN, two digits, launch order; the filename repeats it
seat: shaper                           # who ran — see The seats below
kind: shape                            # sweep | pick | topic | stimulus | interview | shape | gate | rewrite | proofread | lesson
stage: 3                               # the machine's own numbering, SKILL.md § Stages: 0 Oracle · 1 Topic · 2 Interview · 3 Shape · 4 Gates · 5 Ship · 6 Lessons
runtime: claude-sonnet-5               # the model that actually ran; a script is named as itself ("x/stimulus.py (no model)"); Sean is "Sean"
launch: "Agent tool, fresh context"    # verbatim launch form — the Agent call, the exact command line, or "chat"
effort: high                           # or — for a script or a person
launched: 2026-10-06T08:10:00-04:00    # exact instant, written before the stage fires
completed: 2026-10-06T08:14:00-04:00   # exact instant, written after it returns
wall_clock_s: 240
meter:                                 # tokens as the runtime reported them; `meter: null` when UNMEASURED
  total: 41500                         # the Agent tool reports one total; a split `input` / `output` pair is also legal
meter_source: Agent-tool usage         # the kit's registry vocabulary: Agent-tool usage | claude -p result.usage | codex turn.completed.usage | codex footer | … | UNMEASURED — never an estimate; a script, a gate and Sean are UNMEASURED
inputs:                                # every file handed over, path + content hash — for a shape, this IS the clean context, every slot of it
  - path: creative-studio/content-machine/stimulus/2026-10-06-x-deck/1-the-slug.md   # slot 1: the block (or the transcript)
    sha256: <64 hex>
  - path: creative-studio/content-machine/corpus/01-raw-interviews.md              # slots 2–5: corpus 01–06, voice-samples.md,
    sha256: <64 hex>                                                                #           reference-universe.md, do-not-promote.md
  - path: .claude/skills/writing-voice-modes/references/voice-samples.md
    sha256: <64 hex>
withheld:                              # a shape always lists the drafting conversation, then the files banned from the context
  - the drafting conversation
  - .claude/skills/content-machine/SKILL.md
  - .claude/skills/content-machine/contracts/
  - creative-studio/content-machine/ledger/
outputs:                               # what came back, with the hash taken on return
  - path: 1-the-slug.md                # the draft card: draft, ORIGIN LEDGER, `## Moves`
    sha256: <64 hex>
raw_log: trace/logs/pass-05.jsonl      # the subagent transcript — the record indexes it, never replaces it
checks: []                             # appended afterwards, one block per gate and the pick that touched this draft:
                                       #   - pass: pass-08
                                       #     kind: gate
                                       #     verdict: origin-gate: clean
                                       #   - pass: pass-14
                                       #     kind: pick
                                       #     verdict: picked
triggered_by: null                     # the pass id whose finding caused a re-run (rare: L8 forbids revision loops; a routed revise is one)
shadow_of: null                        # a second runtime on identical inputs (a spread-run arm), fired on the same hashes
---

## Corpus read

<!-- recovered from the transcript's file reads — a fact, not the shaper's claim. For a shape, every input should appear here; a slot handed but never opened is a finding -->

- creative-studio/content-machine/stimulus/2026-10-06-x-deck/1-the-slug.md
- creative-studio/content-machine/corpus/01-raw-interviews.md
- .claude/skills/writing-voice-modes/references/voice-samples.md

## Moves

<!-- pointer only; the lines live at the end of the draft card, where the gates and Sean read them -->

1-the-slug.md § Moves

## Notes

<!-- deviations, substitutions, anything the next reader must know; never prose about what the shaper "thought", never his words -->
```

## The kinds

| kind | stage | who | hands an artifact forward | what the record indexes |
|---|---|---|---|---|
| `sweep` | 0 | `oracle` or `x-sweep` | no | the Oracle run or route 1's sweep: the pool and the ranked deck as outputs |
| `pick` | 0 or 5 | `sean` | no | his choice — a card from an Oracle deck (0), or the split of a draft deck (5); the picks file is the output |
| `topic` | 1 | `orchestrator` (`value-gate` when the gate is the story) | no | the TOPIC CARD and the value gate's ruling |
| `stimulus` | 2 | `stimulus` | no | `x/stimulus.py block`: the block file is the output, and it is the *only* thing that writes one |
| `interview` | 2 | `interviewer` | no | one lens; the transcript is the output (its path is private and repo-prefixed) |
| `shape` | 3 | `shaper` | **yes — `## Moves`** | the clean-context draft: inputs are the whole context, hashed; the card is the output |
| `gate` | 4 | `origin-gate` · `coined-lines-gate` · `humanity-gate` · `critique-gate` · `analyzer` | no | one record per gate that ran, on the draft at the hash the shaper returned; its output is the gate's own report; its verdict is transcribed onto the shape's `checks` |
| `rewrite` | 5 | `sean` | no | his hand-rewrite; the final is the output (and later corpus) |
| `proofread` | 5 | `proofread` | no | the mechanical proofread on his final |
| `lesson` | 6 | `orchestrator` | no | the deck entry or routed lesson; the ledger file is the output |

Only the shaper has a drafting conversation to withhold. Every other kind is a script, a person, or a conversation that *is* its output (the interview), so the checker does not demand the `withheld` line of them.

## The seats

`seat` is who ran: `oracle`, `x-sweep`, `orchestrator`, `stimulus`, `interviewer`, `shaper`, `value-gate`, `origin-gate`, `coined-lines-gate`, `humanity-gate`, `critique-gate`, `analyzer`, `proofread`, `sean`. The gate seats are drawn as gates in the viewer's train.

## `## Moves` — the shaper's closing section

The shaper's draft card ends with a `## Moves` section: **what the draft took from the clean context and what it made**, one line per move in the kit's five-word vocabulary, each naming its source. This is the mechanism [#258](https://github.com/seanwinslow28/code-brain/issues/258) had to rebuild by hand for an hour — which of his samples a draft was imitating — written down at the moment it is cheapest to know. It is a **report about the draft**, in the same class as the ORIGIN LEDGER: metadata that rides with the card and is never part of the published text. *Not the voice-move roster* — the word is the kit's, and the collision is noted here so nobody reads `kept` as a licensed move.

```markdown
## Moves

- kept — Rep 7e from creative-studio/content-machine/corpus/06-short-form-and-exercises.md
- added — the two-minute-app turn from the block (stimulus/2026-10-06-x-deck/3-the-slug.md)
- merged — Rep 1 + Sample 2 → the closing line from corpus/06; voice-samples.md
- split — Rep 3 → the open, the tag from corpus/06
- dropped — Rep 4 from corpus/06; dunks on the poster
```

- **`kept`** — a rep whose shape the draft carries. Name it exactly as the file labels it (`Rep 7e`, `Sample 2`); the checker matches whole tokens, so `Rep 7` never covers `Rep 7e`.
- **`added`** — a beat with no rep behind it. Its source is the block or the transcript line; new by definition, a claim rung 0 does not replay.
- **`split` / `merged`** — the kit's grammar (`→` for children and results, `+` between merged items).
- **`dropped`** — a rep considered and set aside, `; <why>` after the source. The why is the lessons loop's cheapest input.

The origin form (`origin draft, no upstream`) is **not legal for a shape**: a shape always has upstream — the samples are the upstream. A card with no `## Moves` section fails the moves line.

## Hashes

Inputs match the file on disk, or a revision an earlier pass in the run recorded as its output. Repo-prefixed inputs the run did not write — the corpus files, `voice-samples.md`, the reference universe — are **provenance, not chain links**: when one has moved since the shape (Sean edits the corpus between runs), the checker counts it *unverifiable* and names it, never fails it and never rewrites the record. The block and the draft card are strict: the run wrote them.

## Meters

The shaper runs through the Agent tool and reports one `total`; write it as the runtime reported it. Every script, every gate and every pass of Sean's is `meter: null` with `meter_source: UNMEASURED` — honest and listed, never a round number.
