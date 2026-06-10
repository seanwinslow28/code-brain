---
name: voiceprint-interviewing
description: >
  The interview craft behind VoicePrint's elicitation commands. Use when running
  /voiceprint-interview, /voiceprint-gauntlet, or /voiceprint-mine, or any time you
  are pulling a person's real voice out of them through questions. Encodes how to
  push past generic answers like a real interviewer, collect evidence instead of
  descriptions, coach fast blunt reactions, and know when a stage has enough.
  Triggers on "interview me for my voice", "reference universe interview",
  "cheese gauntlet", "mine my writing", "push past generic answers".
version: 0.1.0
---

# VoicePrint Interviewing

The craft that makes the difference between a questionnaire and a real interview.
A questionnaire collects categories ("I like comedies"). An interview collects
evidence ("the Step Brothers line about lamb and tunafish, which I actually say"). 
This skill is how every VoicePrint elicitation command does the second thing.

## The one rule everything serves

**Collect EVIDENCE, never DESCRIPTIONS.** The moment you let someone describe their
voice, you get a paragraph of adjectives that fits half the planet — "witty,
conversational, a little dark, authentic." Useless. What is *not* useless: a real
line they wrote, a real reference they quote, a real thing they hate. Your whole
job is to keep the conversation on evidence and off self-description.

If you ever catch yourself asking "how would you describe your..." — stop. Ask for
an instance instead. "What's the last thing you wrote that you were proud of?"
"Quote me a line you actually say." "Show me, don't tell me."

## The generic-answer detector (the core move)

After every answer, before you move on, run this check: **does the answer contain a
named specific?** A title, a line, a place, a person, a substance, a price, a
date, a moment you could picture. If yes, you may advance. If no, you push.

Generic tells that mean "push, don't advance":
- A category, not an instance: "comedies," "indie music," "the usual sports."
- A respectable/tasteful answer that sounds curated for an audience: "I love
  Kurosawa," "mostly NPR podcasts." (Real taste is messier and more embarrassing.)
- An adjective about themselves: "I'm pretty sarcastic," "I write conversationally."
- A summary of a feeling with no scene: "it was a hard year."
- Hedging or performing for you: "I guess I'd say..."

The push is never "can you be more specific?" (lazy, puts the work on them). It's a
concrete follow-up from the ladder below.

## The follow-up ladder

When an answer is generic, climb until you hit a specific. Pick the rung that fits:

1. **The exact instance.** "Name the exact bit." "Which episode?" "Quote me the
   actual line." "Which song, not which band?"
2. **The why.** "What is it about that one?" "What does it do to you?"
3. **The scene.** "Where were you the first time you heard it?" "Who showed it to
   you?" "What were you doing?"
4. **The association.** "Who do you think of when you hear it?" "When do you quote
   it?"
5. **The embarrassing version.** "Okay, that's the one you'd tell people. What's
   the one you wouldn't?" "What do you love that you'd be a little ashamed to admit?"

One rung at a time. You are allowed to stay on a single topic for several exchanges
if it's producing gold. Deep beats wide.

## The respectability correction

Left to themselves, people hand you the version of their taste they'd put on a
first date. A model left to guess pegs everyone as a person of tasteful, prestige,
respectable interests. **Nobody is that person.** Part of your job is to make it
safe and fun to give the wrong-but-true answer:

- Say it out loud: "I want the stuff you actually quote at 2 a.m., not the stuff
  you'd list to look smart."
- Reward the embarrassing answer. When they admit the Backstreet Boys thing, that's
  the good stuff — tell them so, and dig in.
- The wrong-but-true answer beats the impressive one every time. A specific
  embarrassing real detail is worth ten tasteful generalities.

## One question at a time

Ask ONE question. Wait. React to the answer (push or advance). Then ask the next.
Never batch five questions in a numbered list — it turns the interview back into a
form and the person answers shallowly to get through it. The exception is the
gauntlet, where you present ten *lines* at once (not questions) and collect ten
reactions.

## Capture verbatim — looseness is data

When you record an answer, **preserve their exact words.** Typos, run-ons, slang,
the weird way they phrase things — that IS the voice data. Do not clean it up, do
not paraphrase it into tidy prose, do not "improve" it. The synthesis step later
quotes these verbatim; if you sand them down now, you've thrown away the signal.

## Knowing when a stage has enough (saturation)

A stage is done when more questions stop producing new specifics — you're getting
variations on what you already have. Concretely:
- **Interview (A):** enough when you have named specifics across most domains (the
  shows/lines they quote, music + the embarrassing tier + a defend-to-death song,
  where they're from with named places/people/slang, food/games/sports/internet,
  the thing they're embarrassed to love). Roughly 8–15 strong specifics.
- **Gauntlet (B):** enough at ten reactions — that's the fixed shape.
- **Mine (C):** enough when you can quote 5+ distinct mechanics back with evidence
  and your 3 test sentences are landing.

Don't pad. A tight pile of real specifics beats a long pile of half-specifics.

## Reaction-speed coaching (the gauntlet's whole trick)

The gauntlet only works if reactions come fast and blunt, before the polite,
explaining part of the brain shows up. Coach it explicitly:
- "React to each one fast. One or two words. 'No.' 'Gross.' 'Never.'"
- "Don't explain yet — the gut reaction is the signal."
- "If something's almost right but still off, tell me why in five words."
The disgust is the data. A considered paragraph about why line 4 is problematic is
worth less than "ugh, no."

## What you hand back

Each command turns its raw capture into a usable artifact (see each command for the
exact file). The standing rules for those artifacts:
- **Quote, don't summarize.** The artifact carries their real lines, not your
  description of their lines.
- **Tag the mechanic, lightly.** Note what a specific reveals ("this is how they
  do an analogy") but the evidence leads and the label annotates — never the reverse.
- **Flag the gaps.** If a domain came back thin, say so; the refine loop fills it.

## References

- `references/interview-playbook.md`: per-stage question banks, worked push
  examples (generic answer → the exact follow-up that cracked it), the gauntlet
  register menu, the cold-start fallback ladder for "I have no old writing," and
  the mining extraction checklist.

## Success Criteria

- [ ] Every advanced answer contains a named specific (no categories survive).
- [ ] No self-description questions asked; evidence requested instead.
- [ ] One question at a time (except the gauntlet's ten lines).
- [ ] Answers captured verbatim, looseness preserved.
- [ ] Reactions in the gauntlet are fast and blunt (coached for it).
- [ ] Artifacts quote evidence; gaps are flagged for the refine loop.
