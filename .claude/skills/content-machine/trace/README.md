# trace — the content machine's trace kit

The machine's copy of the trace kit: what a run records, where, and the two commands that close a run. Designed on [#261](https://github.com/seanwinslow28/code-brain/issues/261) (the machine has no trace) jointly with Productcraft's [#272](https://github.com/seanwinslow28/code-brain/issues/272), after a primary-source read of Husain's method ([#289](https://github.com/seanwinslow28/code-brain/issues/289)); built on [#291](https://github.com/seanwinslow28/code-brain/issues/291) (2026-09-22). Husain's order, local by law: log full traces → one expert reads them in a purpose-built viewer → binary pass/fail with a written critique → taxonomy → code checks → judges only for persistent failure modes. Nothing here ships a payload anywhere.

**Shared, not forked.** The code is the Productcraft kit at [`productcraft/trace/`](../../../../productcraft/trace/README.md) — the first copy, kit 0.7.0 — imported through a **studio profile**. This folder holds only what the machine writes for itself:

| Piece | File | Who uses it |
|---|---|---|
| The profile | [machine.py](machine.py) — stages 0–6, the ten kinds, the seats, the rep-id shape, and rung-0 line 8 | imported by both commands and the tests |
| Record template | [record-template.md](record-template.md) | the orchestrating session, one file per stage invocation |
| Labels-file template | [labels-template.md](labels-template.md) | Sean, one file per run |
| Rung-0 checker | [check.py](check.py) | deck close / ship, and any time between |
| Viewer renderer | [render.py](render.py) → `trace/eval.html` | Sean, reading and labeling |
| Failure-code taxonomy | [taxonomy.md](taxonomy.md) — empty until ~30 labels | Sean, when a label carries a code |
| Synthetic run | [tests/deck_synth.py](tests/deck_synth.py) — an invented three-card X deck | the tests; never the real brain |

Everything runs on the system `python3` with nothing installed: no model, no network, no third-party import. Templates hold no private content; the scripts read a run folder only at run time and write only `eval.html`.

## Where things live

Inside each run folder under the git-ignored `pieces/` (a deck is `<date>-x-deck/`, a piece `<date>-<slug>/`), the kit owns one subfolder:

```
creative-studio/content-machine/pieces/<run>/
├── run.md                          # the header the kit reads: id, name, type (deck | piece), lane, medium, opened, closed
├── 1-<slug>.md … 8-<slug>.md        # the deck's draft cards (draft, ORIGIN LEDGER, ## Moves) — or the piece's handoff draft
├── picks.md  gates/  …              # the pick record and each gate's own report
└── trace/
    ├── pass-NN-<seat>-<kind>.md    # one immutable record per stage invocation
    ├── labels.md                   # Sean's verdicts, apart from the facts
    ├── notes.md                    # process notes; the viewer's third slot
    ├── logs/                       # raw transcripts the records index (subagent JSONL)
    └── eval.html                   # the rendered viewer — local file, never hosted
```

The stimulus blocks stay where [#250](https://github.com/seanwinslow28/code-brain/issues/250) put them (`creative-studio/content-machine/stimulus/<deck>/`), transcripts under `transcripts/`, corpus and samples in their homes: a record names them by **repo-prefixed path** (`creative-studio/…`, `.claude/…`, `vault/…`) and the kit resolves those against the repo root. `run.md` is the machine's `brief.md`: `id`, `name`, `type`, `lane`, `medium`, `opened`, `closed` (null until close) and `synthetic: true` only on invented runs.

## The close ritual — two lines, then the sweep

```bash
python3 .claude/skills/content-machine/trace/check.py creative-studio/content-machine/pieces/<run>
```

```bash
python3 .claude/skills/content-machine/trace/render.py creative-studio/content-machine/pieces/<run>
```

Then Sean confirms every pass has a row with a verdict in `trace/labels.md` (the page's *Copy label rows* hands him the block). The checker exits 0 when every line passes, 1 when any fails (each finding names the pass and the thing), 2 when the path is not a run. `--json` emits the checks as data. The renderer never refuses to render on a failing check: the page is how the failure gets seen.

## The stages, kinds and seats

`stage` is the machine's own numbering from `SKILL.md § Stages`; there is no coordinator column, because the machine's stage 0 is a real stage (the Oracle).

| stage | name | kinds that fire there | seats |
|---|---|---|---|
| 0 | Oracle | `sweep` (the Oracle run, or X route 1's sweep) · `pick` (a card from an Oracle deck) | `oracle`, `x-sweep`, `sean` |
| 1 | Topic | `topic` (the TOPIC CARD and the value gate) | `orchestrator`, `value-gate` |
| 2 | Interview | `interview` · `stimulus` (X's stage 2 is a block, not an interview) | `interviewer`, `stimulus` |
| 3 | Shape | `shape` — the one kind that hands an artifact forward and owns `## Moves` | `shaper` |
| 4 | Gates | `gate`, one record per gate that ran | `origin-gate`, `coined-lines-gate`, `humanity-gate`, `critique-gate`, `analyzer` |
| 5 | Ship | `pick` (the split of a draft deck) · `rewrite` (his hand-rewrite) · `proofread` | `sean`, `proofread` |
| 6 | Lessons | `lesson` (the deck entry or routed lesson) | `orchestrator` |

Filenames are `pass-NN-<seat>-<kind>.md`. The full field list, the meter rule and the hash rule are in [record-template.md](record-template.md).

## Rung 0 — what the checker asserts

Ten deterministic lines. Nine are the kit's, unchanged; line 8 is the machine's own.

1. **Records parse and carry every required field** — `kind` is one of the ten, `stage` is 0–6, a `shape` lists `the drafting conversation` under `withheld`.
2. **Every pass has a record** — no gap in the numbering; every id a `checks` block or the labels file names exists.
3. **Every pass has a label row.**
4. **Input hashes match disk or a recorded prior revision** — the block and the card are strict (the run wrote them); corpus files, `voice-samples.md` and the reference universe are repo machinery the run did not write, so one that has moved since the shape is counted *unverifiable* and named, never failed and never rewritten.
5. **Cited corpus files** — the machine's drafts cite no corpus file by path, so this line reports 0 of 0 with a note; what a draft leaned on is line 6's job.
6. **Every move names an existing upstream item** — each `kept` / `split` / `merged` / `dropped` rep is found, as a whole token, in an input readable at its recorded hash. `Rep 7` does not satisfy a line that named `Rep 7e`. A card with no `## Moves` section is a finding. `added` lines are new by definition.
7. **Meter present or UNMEASURED** — the shaper's Agent-tool total; every script, gate and pass of Sean's is UNMEASURED and listed.
8. **Each shape ran in the clean context, was gated, and reached the pick** — per `shape`: no input starts with a path banned from the shaping context (`SKILL.md`, the voice-modes skill, `contracts/`, `gates/`, `lessons/`, `interview/`, the ledger, the cheese bank); a transcript or a stimulus block is among the inputs (a shape with no story writes from nothing — the constitution's own failure); every input appears in `## Corpus read` (handed but never opened is a finding); at least one `gate` record fired on the card at the hash the shaper returned, and each such gate is transcribed onto the shape's `checks`; a stage-5 `pick` or `rewrite` took the card as an input — while `run.md` says `closed: null`, a missing pick is a note. A story input no stage-2 pass in the run wrote (re-used material) is a note.
9. **Trials blind-labeled before their runtime is shown** — a spread-run arm recorded with `shadow_of` keeps its runtime out of the page until both rows carry a verdict.
10. **Every `failure_code` is in [taxonomy.md](taxonomy.md)** — empty today, so any code is a finding.

**What rung 0 cannot see.** It reads the record, not the transcript: `## Corpus read` is written by the orchestrating session from the transcript's file reads, and the checker trusts it. Whether the shaper's `## Moves` is *true* — that the draft really carries `Rep 7e`'s shape — is a claim until a replay over the raw transcript exists, which is a later rung. And it cannot tell a corpus file Sean edited between two decks from one edited a month later; that belongs in `trace/notes.md`.

## The viewer

The Productcraft viewer ([DESIGN.md](../../../../productcraft/trace/DESIGN.md)) rendered with this machine's names: masthead → prose reading line → labeling counter → the last-good × first-failing matrix on stages 0–6 beside the fails with their critiques and the rung-0 list → the train (gate seats drawn as gates) → one folded row per invocation with inputs, moves, meter and critique → the taxonomy, judge and notes slots → footer. Fonts embedded; every string escaped; no `<link>`, no `<script src>`, no URLs. Labels drafted on the page live in the browser and leave through **Copy label rows**; the file is the record.

## Tests and the synthetic run

Everything is tested on an invented run, never on the brain. [tests/deck_synth.py](tests/deck_synth.py) builds `2026-10-06-x-deck`: three posts by handles that do not exist, a three-file toy corpus labelled the way the real one labels its reps, three cards with `## Moves`, six gates (one advisory finding), a pick and a deck entry — fifteen passes, hashes computed in launch order so the chain is real. It refuses to write under `creative-studio/content-machine/`, any `ledger/` or any `transcripts/` path.

```bash
cd /Users/seanwinslow/Code-Brain/code-brain && agents-sdk/.venv/bin/python3 -m pytest .claude/skills/content-machine/trace/tests -q
```

```bash
cd .claude/skills/content-machine/trace && python3 tests/deck_synth.py /tmp/cm-synth && python3 check.py /tmp/cm-synth && python3 render.py /tmp/cm-synth
```

No sample is committed here — the render embeds two fonts and would weigh on a skill folder the installer exports; the second command regenerates it anywhere in a second.

## Privacy

The run folder is under `pieces/`, git-ignored by the rule [#232](https://github.com/seanwinslow28/code-brain/issues/232) wrote; `git check-ignore` on a record path is one of the tests. Records index his transcripts and drafts by path and hash, never by content. The one field to be careful with is the labels file's `critique`, which is the field most likely to be pasted into a ticket — write it about the draft, never in his words. The viewer is a local file and carries his drafts, so it is never published as an Artifact or anywhere else.
