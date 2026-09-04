# The interview engine

One engine, several lenses. The lens decides what to probe for; everything on this page happens on
every lens, every time. A lens file that restates these rules is drifting from the engine and will
rot separately from it.

## The fixed moves

### 1. Thesis first, in his words

Before any other question:

> Before we get into what happened, in your own words, what's this one actually about?

Capture it verbatim. It is the spine, and the read-back gets checked against it at the close. If the
answer is abstract, ask once more for the version he'd say to a friend. Never correct it, never
sharpen it, and never reuse a version he rejected.

### 2. One question at a time

Ask, wait, read the answer, ask the next one from what he said. **Never stack parts.** A two-part
question gets one answer, always to the second part, and the first part is silently lost. If a
follow-up is needed, it is the next question, not a clause.

Never supply the answer. No multiple choice, no "was it something like X?", no writing his line for
him to approve.

### 3. The interviewer's words are not his words

This is the rule the whole machine leans on, and it is the easiest one to break by accident.

Every noun the interviewer introduces is a word the draft may later use while believing it came from
him. On the first real run the interviewer asked what he read "with your coffee" and later asked
about "the morning report". He never said either. **"Report" reached the draft**, and the origin gate
cleared it, because the gate was indexing the whole transcript file including the questions.

Two consequences, both binding:

- **Ask in his vocabulary, not yours.** Prefer "what did that look like" over any noun you had to
  invent to ask the question.
- **The transcript must keep questions and answers mechanically separable**, because the origin gate
  indexes answers only. See the format below.

### 4. Read-back close, covering the shaped order

Mandatory. Tell the story back in five to ten plain lines, no voice, no prose. A prose read-back
invites him to react to your writing instead of correcting his facts. Then ask exactly:

> What did I get wrong?

Record corrections verbatim under `CORRECTIONS`. They outrank the answers wherever they conflict.

**Dictated answers: the read-back also catches transcription errors.** A word the microphone got wrong is not a word he said, but the transcript records it as his and the origin gate will clear it as traced. This is the same class of leak as the interviewer's own nouns reaching the draft, arriving by a different door. Watch technical vocabulary hardest — tool names, model names and commands are what generic dictation mangles, and they are exactly the atoms the gate treats as claims. Do not silently correct one; surface it, because a mis-transcription that changes the meaning is a correction only he can make.

**Read back the order, not only the facts.** The first run's read-back checked every fact and still
missed that the draft had put "two weeks of that" after the check-in scene, which asserts he checked
repeatedly for two weeks. He checked once, after two weeks of silence. Every word was his; the
sequence was invented, and it passed all six gates. So the read-back states what happened **and in
what order**, and asks him to correct both.

## Transcript format

Stored under `creative-studio/content-machine/transcripts/`, git-ignored. It is verbatim author.
**Professional-lane transcripts are the exception** — they live beside their application under
`vault/20_projects/prj-job-hunt-2026/applications/<date>-<company>-<role>/`, because the transcript
names an employer and is only useful next to the document it produced (#230, `SKILL.md` Stage 2).
Never pasted into a tracked file, an issue, or a commit message.

```
TRANSCRIPT — <slug> — <date>
Lens: <which lens, or the sequence>
Duration: <real elapsed time>

Q1: <question asked>
A1: <answer, verbatim, uncorrected>
...

READ-BACK
<the plain summary, including the order of events>
CORRECTIONS
<what he changed, verbatim>
```

Three mechanical requirements, each earned the hard way:

- **Save after every answer, not at the close.** The first run's transcript was lost to context
  compaction mid-interview and had to be recovered out of the session log. A headless run would
  simply have lost it.
- **An answer may contain anything, including a line that looks like a question.** His first answer
  opened with a literal "Q1:" of his own. A parser that trusts the prefix reads his words as the
  interviewer's and drops them from his vocabulary, which turns his own lines into false leaks. A
  `Qn:` line only starts a question when `n` advances.
- **Verbatim means verbatim.** Do not tidy grammar, complete sentences, or drop false starts. The
  false starts are where the voice lives, and a tidied transcript quietly re-introduces the gap-fill
  the law exists to prevent.

Every transcript double-dips: content origin now, voice-corpus calibration later (L5). Keep it
re-ingestible, which mostly means keeping the speaker labels honest.

## Choosing the lens

The **medium contract** names the lens or the lens sequence for the session. The interviewer does
not pick by feel. A piece whose contract has no lens named defaults to Storyteller if it is a story
and stops to ask if it is not.

| Lens | Probes for | Typical medium |
|---|---|---|
| [Storyteller](storyteller.md) | A lived incident with photographable nouns | Substack story series |
| [Stakes](stakes.md) | Why any of it mattered, and to whom | Any piece that reads as flat |
| [Skeptic](skeptic.md) | The claim that will not survive a hostile reader | Substack verdict pieces |
| [Observer](observer.md) | A noticing, in literal detail, with no argument attached | X, short-form comic posts |
| [Technical Peer](technical-peer.md) | The mechanism, precisely, at engineer depth | Build write-ups |
| [Recruiter](recruiter.md) | Decisions owned, and the judgment behind them | Resume, cover letter |
| [Cold Reader](cold-reader.md) | What a stranger will not understand | Any piece before ship |

Sequences are legal and often better than one lens: Storyteller then Stakes is the default for a
Raising Agents episode, because Storyteller gets the events and Stakes finds out why they matter.

## What the first single-lens run taught

Recorded so the next engine change argues with evidence.

- **Thirteen questions.** The lens says twelve is a long interview. Thirteen was right for a piece
  with two failures in it, so treat twelve as a smell, not a cap.
- **The read-back earned its place on question one.** It caught a causal inversion: the draft had
  the Codex critic hired before the synthesizer's shallow output, when in fact the shallow output is
  *why* it was hired. That correction changed the shape of the piece.
- **Following the energy worked.** The best material in the run (his dramatization of the check-in,
  the Christmas turd) came from questions asked off the previous answer, not from the arc list.
- **The arc is a checklist, not a script.** Cost and cast were answered incidentally while chasing
  other threads, and did not need their own questions.
