# Medium contract: Email (Professional lane)

Wave 2 ([#171](https://github.com/seanwinslow28/code-brain/issues/171)).

**Lens: Stakes → Cold Reader.** This is the one Professional document
[`recruiter.md`](../../interview/recruiter.md) does not name, and the omission is right: most of these
emails are not about a decision he owned. What an unrequested email has to earn is **consequence** —
what was different afterwards, and for whom — which is Stakes. Cold Reader closes because the
recipient is doing something else and has none of his context. When the whole job of the email *is* to
restate a decision he owned, such as an interview follow-up, run Recruiter first. The lane's
facts-only law governs the draft either way; the lens only shapes the interview.

**Status: unproven.** No email has run through it.

## Governing documents, in precedence order

1. [`LANE.md`](LANE.md) — Professional-lane law.
2. [`../move-licensing.md`](../move-licensing.md) — the shared matrix.
3. This contract.

## What this medium is

Job-search and professional correspondence: a reply to a recruiter, a follow-up after an interview,
a thank-you, a referral or intro request, a note to someone whose work he actually used. **Not** the
newsletter (that is Substack), and not internal work mail, which this machine has no stake in.

The property that decides everything below: **the recipient did not ask for it, and reading it is
the whole cost.** A cover letter is read by someone whose job is to read it. An email is read by
someone doing something else.

## Licensed moves: six

Budget heat 1, room 2. The same six as the cover letter and the questionnaire:

**Expectation / Instead** · **Then / Now Narrator** · **Short Declarative Drop** ·
**Anaphoric Stack** · **Blunt-Literal Description** · **Rhetorical Catechism**

All structural, none a joke. Heat 2 and above is banned.

**Practical narrowing: room 2 rarely fits.** A body of five to eight lines gives most two-beat moves
nowhere to turn. Short Declarative Drop and Blunt-Literal Description do the real work here; the
other four are available and usually the wrong tool for the length. That is a fact about the form,
not a further ban — a longer email that has earned its length may use them.

## Length is the message

A long email from someone the recipient does not owe anything is a claim on their time made before
any claim on their interest.

**The bound: what fits on a phone screen without scrolling.** Roughly five to eight lines of body.
Not a rule about brevity as a virtue — a rule about where the reply decision is actually made, which
is before the scroll and usually in a preview pane.

If the material genuinely needs more room, it is an attachment or a link, and the email is the note
that points at it.

## One ask, small enough to say yes to in one reply

This is the medium's real design constraint, and the one most emails fail.

- **One ask.** Two asks is zero asks; the recipient defers the whole message rather than triaging it.
- **Sized to a reply.** "Would you forward this to the hiring manager if it makes sense?" can be
  answered by one person in thirty seconds. "Can I pick your brain for thirty minutes?" is a large
  ask wearing a small ask's clothes, and the cost is entirely on the person being asked.
- **Stated plainly, once, near the end.** Not buried, not repeated, not apologized for.

The cover letter's **exception to the sideways-ask rule extends here**, for the same reason and by
the same ruling: an email whose purpose is an ask has failed if it does not ask.
[`cover-letter.md`](cover-letter.md) holds the reasoning; it is not re-derived. What carries over
with it is the reason behind the original rule — confidence is shown by not needing to grovel. The
ask is direct, unembarrassed, and never reaches for the predicament.

## Enthusiasm is the untraced claim this medium invites

The lane already names generic enthusiasm as an untraced claim wearing a friendly face. Email doubles
the pressure, because warmth is the genre's default register and a cold-sounding email reads as rude.

**A warmth line traces like any other claim.** If the transcript does not say he read the post,
listened to the episode, or used the tool, the email does not say he did. This is the one place where
a fabrication is both trivially easy and trivially checkable by the recipient, who wrote the thing
being complimented.

The clean move is available and it is better anyway: say the specific thing he actually took from it.
That is traceable, and it is the difference between a compliment and evidence.

## The thread is the document

An email is read with its parent, in a client that shows both.

- **Never restate context the recipient wrote.** Summarizing their own message back to them tells
  them you needed a paragraph to get started.
- **A reply answers before it elaborates.** The answer to their question is in the first line.
- **A follow-up names what it is following up on and when**, and then makes its ask. "Just circling
  back" names nothing and asks nothing.

## Format

- **The subject line says what this is.** It is the entire first screen. A curiosity-gap subject from
  a job applicant reads as marketing, and it is the one line the recipient uses to decide whether
  this is a person or a campaign. A format fact about how the message is triaged, not the Expressive
  lane's first-screen test, which does not apply here.
- **Addressed to a person, by the name they use.**
- **Plain text.** No formatting that a client can mangle. No tracking pixels, no read receipts.
- **One link, two at most.** A wall of links is a request to do research on his behalf.
- **A signature is a signature.** Name, one line, done. Not a résumé.

## Negative specimens — what this must never look like

- **The unearned cold open.** "I've been following your work for a while now." Unfalsifiable,
  unverifiable by the gate because he might have said it, and the recipient can usually tell.
- **The resume in prose.** Three paragraphs of history before the ask. The ask is what the email is
  for.
- **The multi-ask.** A meeting, an intro, and feedback on a portfolio, in one message.
- **"Just circling back."** A follow-up that does not say what it is following up on, or what it now
  needs.
- **The hooked subject line.** "A quick question about your team" when it is not quick and not a
  question.
- **The essay with a link at the bottom.** If the link is the point, the email is three lines.
- **Borrowed strings.** "I hope this email finds you well." Template phrasing, banned by the lane,
  and the recipient has read it four hundred times.

## Gates, in order

Post-draft as of 2026-08-31, in the machine's current order: **origin (claims tier) →
do-not-promote + coined-lines sweep → humanity scrub → critique / analyzer**. Professional lane:
**origin blocks delivery** while any claim is untraced (`origin_check.py` exits 1). In this medium a
warmth line is a claim.

`writing-humanity-pass` runs **FULL** scrub. Coined lines run
`gates/coined_lines.py --lane professional`.

## Delivery

A ship packet: the subject line, the body, the ORIGIN LEDGER, and the ASK LIST. **The machine never
sends an email**, never adds a recipient, and never schedules one. Sean sends it himself, from his
own client.

## What this contract does not own

Who to write to (Sean), whether to send (Sean), or the claims (the transcript).
