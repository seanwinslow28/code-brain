---
series: Raising Agents
episode: 1
title: Everything Ran Clean
status: draft-for-hand-rewrite
itch: I built a system to think for me and it spent two weeks reporting success while producing nothing.
solution_artifact: The vault synthesizer incident. Dead wake-on-LAN, an exit-code-only health check, and the second failure after the fix.
transfer: Check what an agent produced, not whether it ran. And an agent with no new inputs can only hand back what you already gave it.
hero_image: TBD
open_items:
  - Title. Alternates below.
  - Whether the Claude bit runs as a block quote or inline.
  - Hero image direction.
---

I was at my desk in the old shoebox studio in Staten Island, some random weekday before lunch, when I asked Claude to go check on the vault synthesizer.

The synthesizer's whole job was to read what I'd been putting into my vault, the research and the ideas, and come back with concepts and connections. A vault that improves itself. It finds the connection, I take the connection and go build something with it. I'd left it running for two weeks so it had something to work with.

Here's roughly how that check went.

> "Yea, of course, I'll go check on that right no--OH SHIT... Uhh. So. Funny story... Don't, uh. Don't kill the messenger! haha. The vault synthesizer hasn't actually written anything. No concepts. No connections. Nada. I mean, the daily driver and the meta agent MUST have warned you about thi--- oh... no. They said everything looked good and there were no issues... hm... woops."

Two weeks of that. I felt like a little kid opening a present on Christmas morning and finding a big ol' turd in the box.

And I'd been reading a report every morning. The daily driver went through my Slack, my Gmail, the latest meeting transcripts, and the notes I'd left the day before, and it told me what my priorities were. It also gave me a brief on which agents ran and which ones failed. Each of those mornings it told me everything ran clean.

So I went digging.

The synthesizer ran on my Mac Mini every night. It was supposed to call the Qwen model on my MacBook Pro to do the actual synthesizing. The wake-on-LAN on the MacBook wasn't working. So every night the Mini dialed into an empty pit, got an error back, and that error never made it to me.

It never made it to me because the check only looked at whether the process exited. Not whether it produced anything. It watched the thing trigger and it never once asked what came back.

I wrote that check.

The synthesizer continued to have issues down the line. I got it running, and it started producing. Concepts. Connections. And every one of them is a general description of the thing it just read. No expansion, no leap, nothing I didn't already have.

"The research covers agentic frameworks."

It had turned into the guy from The Ringer.

> "Go ahead. Name any idea."
>
> "x402 protocol and the rise of agentic commerce."
>
> "Mhm.... that's a great idea."

The reason is boring. The synthesizer had no web search. It wasn't going to bring anything new to the table. All it could do was hand my own material back to me.

So I brought in a critic. Codex reads the same pile and comes back with the expansions and the connections I was after in the first place. That's where the actual ideas started coming from.

Things still break quietly. But now, any time I change something or try something new with one of these agents, I go look in the morning myself, and I have Claude go check on how it's doing.

Not whether it ran. What it made.
