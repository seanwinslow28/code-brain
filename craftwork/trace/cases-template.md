# cases.md — the template

Copy this into an engagement's `trace/cases.md` and write over it. It is the guided-reading content
the viewer reads: the teaching sits here, apart from the immutable records, keyed to a pass and a
finding, with each source's sha256 **as that file stood when the case was written**.

Three rules the renderer enforces, so the page can never bluff:

1. **No file, no stories.** A missing `cases.md` renders an honest empty section, never an invented one.
2. **A changed source is qualified, not quoted.** If a source's hash no longer matches, the page says
   "the source changed since this story was written" in place of the excerpt and marks the case qualified.
3. **A quotation that is not in its file is reported.** The excerpt must occur verbatim (whitespace may
   differ). If it does not, the page prints the error instead of the quote.

Unknown `assist` values and a missing `### Story` are parse errors, printed on the page with the case
dropped. Everything else degrades: a case with no reveal says so rather than disappearing.

Write the hash with `shasum -a 256 <path>` from the engagement folder, or `sha256sum` on Linux.

---

```markdown
---
engagement: pc-eng-001-16bitfit-revisit
written: 2026-09-20
status: proposed            # proposed | reviewed — "reviewed" only after Sean has read
                            # every case against its sources
---

# What happened in this review

80–120 words, plain language, no ids in the prose. What the review was for, what it found,
what is still open. The page prints this above the counts sentence.

## Case: eight to twelve words, and it must not reveal the answer

pass: pass-10
finding: M8                 # or "none"
assist: worked              # worked | hint | independent — decreasing assistance
question: One sentence the reader answers.
options:
  - key: a
    label: A short choice
  - key: b
    label: Another short choice
  - key: c
    label: A third short choice
sources:
  - path: audits/audit-strategy-r3.md     # relative to the engagement folder;
                                          # studio-prefixed paths resolve against the repo
    sha256: 0000000000000000000000000000000000000000000000000000000000000000
    excerpt: "A short exact quote, forty words at most, verbatim from that file."
    label: M8 · Audit of Strategy revision 3

### Story

120–180 words across two or three paragraphs: what someone wanted, what got in the way, why it
matters, what the reviewer proposed, what is still open. Name the actor and the action. Use
ordinary causal words — because, but, so, that means. Keep ids out of the prose; they live in
the source labels. Mark anything imagined as an illustration, and never invent a participant,
an observation or an outcome.

The first paragraph is the **goal**. In an `independent` case it is the only paragraph shown
before the reader answers; the rest stays folded with the reveal.

### Hint

One sentence. Optional for a worked case, expected for a `hint` case.

### Reveal

60–120 words: the reviewer's reasoning and the recorded outcome, attributed. While `status:
proposed`, the page labels this a proposed explanation rather than an answer key.

### Your turn

One question the reader answers in their own words.

### Terms

- term: one plain sentence, beside its first relevant use.

### Diagram

Optional. A small text flow, rendered as an inline SVG and repeated as a list underneath. Four
line shapes, and nothing else:

- A step in the flow
- ? A decision, written as a question
- no: what happens on that branch
- yes: what happens on the other branch
```

---

## Which assistance level

| `assist` | The page shows | Use it for |
|---|---|---|
| `worked` | Story, evidence, reasoning and the practice question, all open. The first worked case opens by default. | The first case of a kind. Teach the idea before asking for it. |
| `hint` | Story and evidence open; the hint and the reasoning behind disclosures that record they were opened. | The second case of that kind. |
| `independent` | The goal, the evidence and the question with its options. The rest of the story and the reasoning stay folded until the reader picks an option or asks for help. Needs at least two options. | The check on whether it landed. Keep the title neutral. |

## What the reader's answers are, and are not

Practice answers, notes and bookmarks live in the browser under a key of their own and never
touch `labels.md`, the verdict buttons or the label export. An answer saved here is learning
metadata: the page records which help was opened before it, so an assisted answer is never
mistaken for a blind one. **Copy practice notes** puts the lot on the clipboard as markdown,
with each case's sources and their hashes; **Download backup** writes the same as JSON.
