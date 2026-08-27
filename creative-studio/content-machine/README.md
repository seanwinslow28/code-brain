# Content Machine

An interview-first writing system. The machine does not write from a topic — it interviews the
author, then drafts **only** from the transcript of that interview. Words that were never said do
not enter the draft.

Build map: [GitHub #158](https://github.com/seanwinslow28/code-brain/issues/158).

## Why it works this way

A model asked to "write a post about X" fills the gaps with the average of its training data. The
result passes every style rule and still isn't the author's — it is plausible text wearing their
voice. The fix is not a better style guide. It is to remove the gap-filling step: interview first,
then shape what was actually said.

That constraint is the whole design. Everything else — the medium contracts, the gates, the lessons
loop — exists to keep it enforced.

## Shape

```
Oracle  →  interview  →  transcript-only drafting  →  gates  →  lessons loop
```

Two output lanes: **Expressive** (Substack, X, video, portfolio) and **Professional** (resume,
cover letter, questionnaire, email, LinkedIn). LinkedIn is a syndication target — cuts of pieces
that already exist — never a place the machine composes natively.

## Public machinery, private brain

The machine is tracked here and in `.claude/skills/content-machine/`. Its brain is not:

| Directory | Tracked? | What it holds |
|---|:--:|---|
| `README.md`, contracts, skill | yes | The machinery. Portable, no personal data. |
| `corpus/` | **no** | Verbatim writing by the author — the evidence every voice decision is checked against. |
| `ledger/` | **no** | The consent-gated lessons loop. |
| `cheese-bank/` | **no** | Labeled negative specimens: registers to never emit. |
| `reference-universe.md` | **no** | The author's personal-history and pop-culture library — the only place a reference may be sourced from. |
| `do-not-promote.md` | **no** | Subjects ruled off-limits. |
| `ideas-bank.md` | **no** | Spike cards the Oracle decked and the author did not pick. Quotes his commits, dailies and session sidecars. |

The private directories are git-ignored (`.gitignore`, "Content Machine private brain"). The corpus
is the irreplaceable input: raw interview answers, hand-edits, and pre-AI prose, consolidated and
provenance-audited so that a claim about how the author writes can be traced to something he
actually wrote. It is personal material and it stays on local disk.

This split is deliberate and it mirrors `systemcraft/`: the method is worth sharing, the material
it was tuned on is not.
