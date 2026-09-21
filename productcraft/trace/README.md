# trace — the Productcraft trace kit

The public pieces the studio's evals-and-trace design needs before its first engagement opens, designed on [#272](https://github.com/seanwinslow28/code-brain/issues/272) (record, labels, ladder, blind trials) and [#292](https://github.com/seanwinslow28/code-brain/issues/292) (the viewer's [DESIGN.md](DESIGN.md)), built on [#290](https://github.com/seanwinslow28/code-brain/issues/290) (2026-09-13). Husain's order, local by law: log full traces → one expert reads them in a purpose-built viewer → binary pass/fail with a written critique → taxonomy → code checks → judges only for persistent failure modes. Nothing here ships a payload anywhere.

| Piece | File | Who uses it |
|---|---|---|
| Record template | [record-template.md](record-template.md) | the coordinator, one file per invocation |
| Labels-file template | [labels-template.md](labels-template.md) | Sean, one file per engagement |
| Rung-0 checker | [check.py](check.py) | Close, and any time between |
| Viewer renderer | [render.py](render.py) → `trace/eval.html`, to [DESIGN.md](DESIGN.md) | Sean, reading and labeling |
| Cases template | [cases-template.md](cases-template.md) → an engagement's `trace/cases.md` | the writer pass, once a train has run |
| Entry-id helper | [nextid.py](nextid.py) | the coordinator, before writing a ledger entry |

Everything runs on the system `python3` with nothing installed: no model, no network, no third-party import. Templates hold no private content; the scripts read the private ledger only at run time and write only `eval.html`.

## Where things live

Inside each engagement folder of the private ledger (`productcraft/ledger/engagements/<eng-id>/`, layout per #268), the kit owns one subfolder:

```
<eng-id>/
├── brief.md                        # Open: the header below, then the one-paragraph brief
├── artifacts/  audits/  dNN-*.md   # what the seats wrote — record paths are relative to this folder
├── readout/                        # the human versions of final, past-gate artifacts — never a pass input
└── trace/
    ├── pass-NN-<seat>-<kind>.md    # one immutable record per invocation
    ├── labels.md                   # Sean's verdicts, apart from the facts
    ├── cases.md                     # the guided-reading content, apart from the records
    ├── notes.md                    # process notes; the viewer's third growth slot
    ├── logs/                       # raw transcripts the records index (subagent JSONL, codex logs)
    ├── trials/                     # a trial's artifact, beside the train, never in artifacts/
    └── eval.html                   # the rendered viewer — local file, never hosted
```

The `trace/` subfolder is a #290 call: #272 said "in the engagement folder", and twenty-six pass files at the ledger root would bury the decision entries the ledger exists for. Both commands accept the engagement folder or its `trace/` subfolder.

**The brief header the kit reads.** `brief.md` opens with frontmatter the coordinator writes at Open: `id` (`pc-eng-NNN`), `name`, `type` (`full-train` | `audit` | `execution-breakdown` | `one-off` | `role-support`), `opened`, `closed` (null until Close), `pass_budget`, and `synthetic: true` only on invented engagements (the viewer shows a badge; a real engagement shows nothing, never "REAL"). The stage-structure check asserts the full train's shape only when `type` says full train.

## The Close ritual — three lines, adopted verbatim by the master skill

```bash
python3 productcraft/trace/check.py productcraft/ledger/engagements/<eng-id>
```

```bash
python3 productcraft/trace/render.py productcraft/ledger/engagements/<eng-id>
```

Then confirm every pass has a row with a verdict in `trace/labels.md`. The checker exits 0 when every line passes, 1 when any fails (each finding names the pass and the thing), 2 when the path is not an engagement. `--json` emits the same checks as data. The renderer never refuses to render on a failing check: the page is how the failure gets seen.

## Rung 0 — what the checker asserts, and what it cannot see

Nine deterministic lines, in this order:

1. **Records parse and carry every required field** — the YAML subset parses; every field in the template is present; `kind` and `stage` are in range; `withheld` names the drafting conversation.
2. **Every pass has a record** — the numbering has no gap; every id referenced by `checks`, `triggered_by`, `shadow_of` or the labels file has a record; each filename matches its record.
3. **Every pass has a label row** — and every row names a real pass. Rows still waiting for a verdict are counted in a note.
4. **Input hashes match disk or a recorded prior revision** — each input's sha256 matches the file now, or matches a hash an earlier pass recorded as its output for that path *and* the disk holds the latest recorded revision. Outputs are checked the same way. A file edited outside a pass fails here — with one carve-out, below.
5. **Cited corpus files appear in the transcript's file reads** — every `corpus/…` path an output artifact or ledger entry cites is in the record's `## Corpus read`, **or in that of an earlier pass which wrote the same artifact**: a repair inherits the citations of the revision it overwrote, and charging it with those reads would be a false finding. Reads travel along one artifact's revision chain, never sideways. `grounding: full` with no corpus read, or `grounding: none` with one of this pass's own, is a finding.
6. **Every move names an existing upstream item; splits are subsets** — each `kept` / `split` / `merged` / `dropped` item is found in an input readable at its recorded hash (ids like `O2`, `OC-1a`, `KR-2`; ranges like `E1–E5` expand; prose items are phrase-matched); a split's children are new and appear in the artifact. Malformed lines and unknown ops are findings. `added` lines are new by definition.
7. **Meter present or UNMEASURED** — `meter_source` is in the vocabulary; a measured meter carries whole token counts in one of two forms, the split `input` + `output` pair or a single `total` (which is what the Agent tool's usage field and the Codex footer each actually report); `UNMEASURED` is honest and listed, and so is a total that was never split.
8. **Each drafting stage has one draft, an audit, and its required co-signs** — per stage reached: exactly one `draft` by the stage's seat, at least one `audit` by the fixed auditor, a `co-sign` by the co-signing seat at stages 2 and 6. Full trains only.
9. **Trials blind-labeled before their runtime is shown** — a trial's inputs are hash-identical to its baseline's; while either lacks a verdict, the rendered page's rows for both hide runtime, launch form and log path (the check reads the pair's own rows in `eval.html`, since gates may share a runtime).

**Shared machinery is provenance, not a chain link.** A seat's inputs include the studio's own files — its seat contract, a lane manifest, an artifact template — which live in the repo, outside the engagement, and keep improving after a train closes. The ticket that fixes a template is doing its job, not tampering with a record, so a repo-path input (`productcraft/…`, `systemcraft/…`, `.claude/…`) that **no pass in this engagement wrote** is counted *unverifiable* and named in a note when its hash has moved, exactly as an overwritten revision's Moves are. The recorded hash is never rewritten to match. Everything the engagement itself wrote — including a repo path some pass recorded as an output — stays strict, which is where the guarantee matters. The limit, stated plainly: this cannot tell a template edited *between* two passes of a live train from one edited a month after Close; mid-train, that belongs in the engagement's `## Notes`.

**Ledger entries ride the chain.** A drafting pass lists each entry it wrote as a `- path:` block with its hash, with the `- id:` beside it — an entry with no hash is outside the chain, so an edit to it is invisible. When the coordinator marks an older entry `status: superseded`, that edit is an **output of the superseding pass**, recorded there with the new hash; otherwise the entry reads as edited outside any pass and fails line 4, correctly.

**What rung 0 cannot see.** Artifacts are redrafted in place (#274), so a superseded revision is no longer on disk. The checker names this honestly rather than passing or failing it: a pass whose artifact was later overwritten has its Moves reported as no longer on disk; a move whose only possible home is an unreadable revision is counted *unverifiable*, never verified. A replay over the raw transcript is a later rung (#272 decision 4), not day one. The checker also does not read transcripts: `## Corpus read` is written by the coordinator from the transcript's file reads, and the checker trusts the record.

## The next entry id

Ids are permanent and bare (#268), so a gap in the `dNN` numbering is harmless — but reserving a block ahead of writing it is how two passes end up claiming one id, which is what the first engagement did. The helper hands out the next free one and shows its working:

```bash
python3 productcraft/trace/nextid.py productcraft/ledger/engagements/<eng-id>
```

An id is **claimed** by a file on disk *or* by a pass record naming it among its outputs, so a reserved-but-unwritten id is never handed out twice. The report names the gaps (left alone, never reused) and separately the ids a record reserved but no file fills — at Close, each of those is either a gap or an entry someone forgot to write. `--bare` prints the id alone, for a shell variable. Read-only: it writes nothing.

## The viewer

One self-contained HTML per engagement, to [DESIGN.md](DESIGN.md) (APPROVED 2026-09-11, the renderer's authority — if the two disagree, DESIGN.md is the intent and the renderer is the bug). Masthead → prose reading line → labeling counter → the first-failing-stage matrix beside the fails with their critiques and the rung-0 checks → the train → one folded row per pass → three growth slots → footer. Fonts embedded from [fonts/](fonts/); every string from a record, label or artifact is escaped; no `<link>`, no `<script src>`, no URLs. Labels drafted on the page live in the browser and leave through **Copy label rows**; the file is the record. **The blind rule:** a shadow pair's runtime, launch form, meter source and log path are not in the HTML at all until both rows carry a verdict in the labels file — the reveal happens on the next render, never on the page.

## Guided reading

The page teaches as it is read, to phase 3 of the eval learning plan (adopted 2026-09-20, recorded in [DESIGN.md §14](DESIGN.md)). Above the counts it states the four things a reader is judging, kept apart — record checks, the seats' findings, your own labels, the owner decisions that are yours alone — with the versioned review prompt for each kind of run. Below them sits **guided reading**: one chapter per case, with decreasing help, each leading with a plain `Run NN · <Seat> <kind>` line, quoting its source with the line it sits on, and offering a question, a note and a bookmark.

That teaching content is **not** in the renderer. It lives in `trace/cases.md` beside the records, written by hand in a **writer pass** after a train has run, to [cases-template.md](cases-template.md): one case per pass and finding, each source pinned to the sha256 it carried at writing time. The renderer reads, checks and qualifies it, and composes nothing. No file renders an honest empty section; a source whose hash has moved renders "the source changed since this story was written" instead of a stale quote; an excerpt that is not in its file is printed as an error. Practice answers live in the browser under a key of their own and never touch `labels.md` — the page records which help was opened before each answer, so an assisted answer is never mistaken for a blind one.

## Tests and the synthetic sample

Everything is tested on an invented engagement, never on ledger content. `pc-eng-000` "Callboard" (a fictional casting tool for community theatre, the same invention #292's sample used) is built by [tests/synth.py](tests/synth.py), which *simulates* the train — it hashes each pass's inputs from the folder as it stands and lets repairs overwrite artifacts in place — so the records' hash chain is real and the checker is exercised on superseded revisions, bounce loops and a blind pair. It refuses to write under any `ledger/` path.

```bash
cd /Users/seanwinslow/Code-Brain/code-brain && agents-sdk/.venv/bin/python3 -m pytest productcraft/trace/tests -q
```

```bash
cd productcraft/trace && python3 tests/synth.py samples/synthetic-engagement && python3 check.py samples/synthetic-engagement && python3 render.py samples/synthetic-engagement
```

[samples/synthetic-engagement/](samples/synthetic-engagement/) is that folder, committed with its rendered `trace/eval.html` so the page can be opened from a fresh clone. The #292 prototype render Sean ratified stays untouched at [samples/pc-eng-000-callboard/](samples/pc-eng-000-callboard/).

## Shared home

This is the **first copy** (#272 decision 8). The content machine's kit ([#291](https://github.com/seanwinslow28/code-brain/issues/291)) shares the code rather than forking it: import `tracekit` from this folder (`frontmatter`, `labels`, `moves` and `checker` are studio-agnostic; `engagement.py` carries the seat, stage and auditor tables that are Productcraft's). `craftwork` extracts the shared home later. Rung 1 (the taxonomy, a tracked file per studio holding shapes of failure only) and rung 2 (a judge per failure mode, validated on TPR/TNR) land beside this README when they are earned.
