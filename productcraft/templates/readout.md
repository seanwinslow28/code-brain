# Readout template — the human version of a final artifact

A **readout** is the version of a seat artifact written for Sean to read, not for a seat to consume. It is derivative, lives beside the artifacts in the private ledger at `ledger/engagements/<eng-id>/readout/`, and is never handed to a seat, hashed as a pass input, or allowed to trigger a repair. Written only from artifacts that are **final and past their gate**, so it is never written twice for one revision. Ruled by Sean on 2026-09-14 (pc-eng-001, at Gate 1) from his eval learning plan's § 4, "Tell the story in language a person would use"; the editorial limits below are that plan's, provisional until his first reading.

The seat artifacts stay exactly as they are. Their ids, tables and Moves grammar are what the hash chain, the co-signs and the handoff contract run on.

## When

| Moment | Readouts written |
|---|---|
| Gate 1 passed | one per final artifact of stages 1–3, plus the gate |
| Gate 2 / close gate passed | one per final artifact of stages 4–7, plus the gate, plus one whole-train readout |
| an audit engagement closes | one per audit record, plus the close gate |

One fresh-context Sonnet 5 pass per moment writes all of that moment's readouts (a mechanical transform of existing substance — the master skill's downshift case). It is a coordinator-commissioned document, logged in `trace/notes.md` with its transcript under `trace/logs/readout-NN.jsonl`, outside the train's pass budget.

## Shape of one readout

```markdown
# <Meaningful title, 8–12 words — what this document settles, not its artifact name>

*Readout of `<artifact id>` revision N (final, <gate verdict>). Proposed explanation until Sean has read it against the original once. Written <date>.*

## What this document decides
80–120 words. What it settles, what it leaves open, and what it is not (a planning document is not a result). In the order a person would want it.

## What you decide
A short list of the rulings that are Sean's on this document — each one sentence, plain, with a recommendation where one exists. Nothing else in the readout asks him for anything.

## <Story 1 title>  … ## <Story N title>
One section per part of the artifact that a reader must understand, each a case story of 120–180 words: what someone wanted, what got in the way, why it matters, what the seat proposed, what is still open. Then one line: **Source:** <artifact section · check-record finding ids · ledger ids>.

## Terms used here
The five to eight studio or product terms this readout needed, each defined in one plain sentence, in the order they first appear. Copied from the glossary; never invented.
```

## Rules

- **Name the actor and the action.** "The Discovery reviewer noticed the count could not be read" beats "L5 was ruled MATERIAL."
- **Ordinary connectives.** Because, but, so, that means. The evidence for each connection is named in the source line.
- **Idea before the term.** Say the thing in plain words first; give the formal term afterwards only if the reader will meet it again, and then define it in the terms section.
- **Ids leave the prose.** Every id, pass number and finding code lives in the Source line at the end of its story, never inside a sentence. A story must read whole with its Source line deleted.
- **Concrete consequence over severity label.** Say what could be miscounted, misunderstood or impossible to carry out; "material" alone tells the reader nothing.
- **One table only where a comparison is genuinely needed** (three bets side by side; two routes weighed). Sentences everywhere else.
- **Keep the story faithful.** Mark an imagined tester situation as an illustration. Never invent participants, observations, dialogue, motives or an outcome. Attribute each conclusion to the seat that made it; keep disagreements, missing evidence and pending owner decisions visible. A planning document distinguishes what could happen from what happened.
- **Provenance labels.** A quoted line is marked *Source excerpt*; everything else is *Explanation*. Excerpts are short and exact.
- **No book text.** The canon line becomes "the seat leaned on <title>'s idea that …" in the writer's words.
- **Voice.** Written to Sean, by name where natural. Short sentences, one idea each. No em dashes, no parentheticals, no bullet-wall summaries of a section that is itself a list. No hedging padding, no significance inflation, no "it's worth noting". Read it aloud; a sentence that sounds like a schema or a policy clause is rewritten.
- **Length.** A stage artifact's readout runs 900–1,400 words; a gate readout 600–900; the whole-train readout 1,200–1,800. Over that, cut stories, not sentences.

## The gate readout opens with "what you are judging"

Four statements, kept apart, from the learning plan's § 2: the record checks (automated, not a quality score) · the reviewers' findings (a seat's assessment, evidence to weigh) · Sean's labels (his verdict on a run's work) · the owner decisions (his rulings on remaining tradeoffs, which a gate recommendation never fills in for him). Then the acceptances, each as a story with a recommendation.

## Optional

- **One small diagram** per readout at most, mermaid, only where a mechanism is easier to see than to read; paired with its text equivalent.
- **Audio.** The readouts are the shape `agents-sdk/scripts/doc_to_audio.py` narrates; an MP3 per readout is one command, $0, on request.
