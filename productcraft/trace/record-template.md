# Pass record template — one immutable file per invocation

The first piece of the trace kit (designed on [#272](https://github.com/seanwinslow28/code-brain/issues/272), decision 2; built on [#290](https://github.com/seanwinslow28/code-brain/issues/290)). One file per seat invocation at `ledger/engagements/<eng-id>/trace/pass-NN-<seat>-<kind>.md`, private, never edited after the pass completes. Frontmatter for machine fields, three short sections for human ones. The record **indexes** the transcript; it never replaces it. Ruled out: dollar figures; prose about what the seat "thought".

**Who writes which field.** The **coordinator** writes the launch fields before firing the seat (`pass` through `inputs`, `withheld`, `raw_log`, `triggered_by`, `shadow_of`) and the completion fields after it returns (`completed`, `wall_clock_s`, `meter`, `meter_source`, `outputs` with their hashes, `## Corpus read` from the transcript's file reads, `## Notes`). The **seat** writes its `## Moves` in the artifact, never here. The coordinator appends to `checks` as audits, co-signs and gates land. **Sean** writes labels in [labels-template.md](labels-template.md), never in a record.

The frontmatter is a YAML subset the checker parses with the stdlib: scalars, lists, one level of nesting, `- key:` blocks. Nothing else. A record the checker cannot parse fails the first rung-0 line, loudly.

```markdown
---
pass: pass-01                          # pass-NN, two digits, launch order; the filename repeats it
seat: product-strategist               # seat slug per templates/artifact-header.md; coordinator | red-team-gate
kind: draft                            # draft | audit | co-sign | gate | repair | trial | close
stage: 1                               # fixed train numbering 1–7; 0 for close, the breakdown, a one-off
runtime: claude-opus-5                 # the model that actually ran — a trial's real runtime too (the viewer hides it, the record never does)
launch: "Agent tool, fresh context"    # verbatim launch form: the Agent-tool call, or the codex exec line
effort: high
launched: 2026-10-06T08:12:00-04:00    # exact instant, written before the seat fires
completed: 2026-10-06T08:46:00-04:00   # exact instant, written after it returns
wall_clock_s: 2040
meter:                                 # tokens as the runtime reported them; `meter: null` when UNMEASURED
  input: 182400
  output: 21300
  cached: 96000
meter_source: Agent-tool usage         # Agent-tool usage | codex footer | UNMEASURED — never an estimate
inputs:                                # every file handed over, path + content hash, relative to the engagement folder
  - path: brief.md                     # (studio-prefixed paths — productcraft/…, systemcraft/… — resolve against the repo)
    sha256: <64 hex>
  - path: productcraft/corpus/canon/strategy-good-strategy-bad-strategy.md
    sha256: <64 hex>
withheld:                              # always includes the drafting conversation
  - the drafting conversation
  - ledger entries of other engagements
outputs:                               # what came back: artifact paths with the hash the coordinator took on return, and ledger ids
  - path: artifacts/strategy-pov.md
    sha256: <64 hex>
  - id: pc-eng-001.d01
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
| `close` | the coordinator's own session, one record at Close | no | 0 |

A redraft after the stale cascade is a `repair` with `triggered_by` naming the loopback pass. The coordinator's one record carries the deviations and the meter of its own session (usually `UNMEASURED`).

## Hashes and the overwrite rule

Artifacts are redrafted **in place** with `revision:` bumped (#274); the pass records keep the history through their hashes. So a later pass's `inputs` hash for a redrafted artifact will not match the file on disk — the checker accepts it when an earlier pass recorded that hash as its `outputs` hash for the same path, and the disk holds the *latest* recorded revision. A file edited outside any pass fails the hash line for every record that names it. Record the hash the seat actually saw; never "fix" a record to match a later edit.
