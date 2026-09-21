# Pass record template — one immutable file per invocation

The first piece of the trace kit (designed on [#272](https://github.com/seanwinslow28/code-brain/issues/272), decision 2; built on [#290](https://github.com/seanwinslow28/code-brain/issues/290)). One file per seat invocation at `ledger/engagements/<eng-id>/trace/pass-NN-<seat>-<kind>.md`, private, never edited after the pass completes. Frontmatter for machine fields, three short sections for human ones. The record **indexes** the transcript; it never replaces it. Ruled out: dollar figures; prose about what the seat "thought".

**Who writes which field.** The **coordinator** writes the launch fields before firing the seat (`pass` through `inputs`, `withheld`, `raw_log`, `triggered_by`, `shadow_of`) and the completion fields after it returns (`completed`, `wall_clock_s`, `meter`, `meter_source`, `outputs` with their hashes, `## Corpus read` from the transcript's file reads, `## Notes`). The **seat** writes its `## Moves` in the artifact, never here. The coordinator appends to `checks` as audits, co-signs and gates land. **Sean** writes labels in [labels-template.md](labels-template.md), never in a record.

The frontmatter is a YAML subset the checker parses with the stdlib: scalars, lists, one level of nesting, `- key:` blocks. Nothing else. A record the checker cannot parse fails the first rung-0 line, loudly.

```markdown
---
pass: pass-01                          # pass-NN, two digits, launch order; the filename repeats it
seat: product-strategist               # seat slug per templates/artifact-header.md; coordinator | red-team-gate
kind: draft                            # draft | audit | co-sign | gate | repair | trial | open | readout | close
stage: 1                               # fixed train numbering 1–7; 0 for open, readout, close, the breakdown, a one-off
runtime: claude-opus-5                 # the model that actually ran — a trial's real runtime too (the viewer hides it, the record never does)
launch: "Agent tool, fresh context"    # verbatim launch form: the Agent-tool call, or the codex exec line
effort: high
launched: 2026-10-06T08:12:00-04:00    # exact instant, written before the seat fires
completed: 2026-10-06T08:46:00-04:00   # exact instant, written after it returns
wall_clock_s: 2040
meter:                                 # tokens as the runtime reported them; `meter: null` when UNMEASURED
  input: 182400                        # the split pair when the coordinator has both numbers…
  output: 21300
  cached: 96000
# meter:                               # …or the single `total`, which is what both sources actually report
#   total: 203700
meter_source: Agent-tool usage         # Agent-tool usage | codex footer | UNMEASURED — never an estimate
inputs:                                # every file handed over, path + content hash, relative to the engagement folder
  - path: brief.md                     # (studio-prefixed paths — productcraft/…, systemcraft/… — resolve against the repo)
    sha256: <64 hex>
  - path: productcraft/corpus/canon/strategy-good-strategy-bad-strategy.md
    sha256: <64 hex>
withheld:                              # always includes the drafting conversation
  - the drafting conversation
  - ledger entries of other engagements
outputs:                               # what came back: every file with the hash the coordinator took on return
  - path: artifacts/strategy-pov.md
    sha256: <64 hex>
  - path: d01-the-binding-constraint.md    # a ledger entry the pass wrote is a file: path + hash, like any other
    sha256: <64 hex>
  - id: pc-eng-001.d01                     # and its id beside it, so cross-references resolve
raw_log: trace/logs/pass-01.jsonl      # the subagent JSONL or the codex log — the record indexes it, never replaces it
checks: []                             # appended afterwards, one block per audit / co-sign / gate that touched this pass:
                                       #   - pass: pass-02
                                       #     kind: gate
                                       #     verdict: STRATEGY FAIL — QUALITY VERDICT ONLY
triggered_by: null                     # the pass id whose verdict caused this repair or re-gate
shadow_of: null                        # trials only: the baseline pass this trial shadows, fired on identical inputs (same hashes)
---

## Corpus read

<!-- recovered from the transcript's file reads — a fact, not the seat's claim; one path per line, or `none` -->

- productcraft/corpus/canon/strategy-good-strategy-bad-strategy.md

## Moves

<!-- pointer only; the lines live in the artifact's own `## Moves` section, where the next seat and the auditors read them -->

artifacts/strategy-pov.md § Moves

## Notes

<!-- deviations, substitutions, anything the next reader must know; never prose about what the seat "thought" -->
```

## The kinds

| kind | Who | Hands an artifact forward | `stage` |
|---|---|---|---|
| `draft` | the stage's seat, first pass on its artifact | yes — `## Moves` against the upstream artifacts | 1–7 |
| `repair` | the same seat, after a loopback, bounce or gate FAIL | yes — `## Moves` against its previous revision and the finding that triggered it; `triggered_by` set | the artifact's stage |
| `co-sign` | the co-signing seat, on one named section | no — writes a check record | the checked artifact's stage |
| `audit` | the fixed auditor, on the whole artifact | no — writes a check record | the checked artifact's stage |
| `gate` | the red-team gate on its vendor | no — writes gate findings | the anchor's stage (Gate 1: 1; Gate 2: 6; close gate: 7) |
| `trial` | a different runtime on identical inputs (#272 decision 9) | yes — its own artifact beside the train, `## Moves` included; `shadow_of` set | the baseline's stage |
| `open` | the coordinator's own session, one record at Open | the brief, the frozen evidence and any entries the chain anchors on | 0 |
| `readout` | the coordinator's post-gate human readout, outside the pass budget | no — writes the readout and its glossary | 0 |
| `close` | the coordinator's own session, one record at Close | no | 0 |

A redraft after the stale cascade is a `repair` with `triggered_by` naming the loopback pass. The coordinator's own records carry the deviations and the meter of its own session (usually `UNMEASURED`).

**The three coordinator kinds** — `open`, `readout`, `close` — are the sessions where no seat fires. They are the one exception to the `withheld` rule: there is no drafting conversation to withhold, so the checker does not demand the line. `open` matters to the chain rather than to the reading: the brief, the frozen evidence and any anchoring entries enter the hash history as its outputs, so a later pass that reads them has something to match against. Without it, the first engagement recorded Open as a second `close`. `readout` is the human-facing pass after the close gate — it hands nothing to a seat and is not counted against the pass budget, but it is a real invocation and gets a real record.

## Meters — the split pair, or one total

The Agent tool's usage field and the Codex footer each report **one number** for a pass. The record's split `input` / `output` form is what the coordinator writes when it has both; when it has one, it writes `total:` and that is a complete, honest meter — the checker accepts it and the viewer prints it as a total, marked *as the runtime reported it, not split*. Splitting a total means summing the raw transcript's per-turn usage by hand, which the coordinator may do and is never obliged to do. The one thing neither form permits is a guess: a pass whose tokens were not reported is `meter: null` with `meter_source: UNMEASURED`, never a round number.

## Hashes and the overwrite rule

Artifacts are redrafted **in place** with `revision:` bumped (#274); the pass records keep the history through their hashes. So a later pass's `inputs` hash for a redrafted artifact will not match the file on disk — the checker accepts it when an earlier pass recorded that hash as its `outputs` hash for the same path, and the disk holds the *latest* recorded revision. A file edited outside any pass fails the hash line for every record that names it. Record the hash the seat actually saw; never "fix" a record to match a later edit.

**Machinery inputs are provenance.** A seat's inputs include repo files the engagement does not own — its seat contract, a lane manifest, an artifact template. Those keep improving after the train closes. Their recorded hash says what the seat saw and is never rewritten to match a later version; when the file has moved, the checker counts it unverifiable and names it rather than calling it tampering. Anything the engagement itself wrote stays strict.

**Ledger entries are files too.** An entry the pass wrote is listed as a `- path:` block with its hash, exactly like an artifact, and its `- id:` beside it. The hash is what puts the entry in the chain: without it a later pass that reads the entry has nothing to match, and an edit to the entry is invisible. When the coordinator marks an older entry `status: superseded`, that edit is an **output of the superseding pass** — it happened in that pass, so it is recorded there with the new hash. An entry edited outside any pass fails the hash line, which is the point.

## Corpus reads along a revision chain

A repair that fixes one paragraph hands back a file still carrying every citation its earlier revisions made. The checker does not charge the repairing pass with reading all of them: a citation is accounted for by this pass's `## Corpus read` **or** by that of any earlier pass which recorded the same artifact path as an output. Reads travel along one artifact's own revision chain and never sideways to another artifact. So write `## Corpus read` as what this pass actually opened — never pad it to cover inherited lines.
