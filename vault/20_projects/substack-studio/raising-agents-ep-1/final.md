---
series: Raising Agents
episode: 1
title: An Agent's Gift
status: sean-rewrite-final
itch: I built a system to think for me and it spent two weeks reporting success while producing nothing.
solution_artifact: The vault synthesizer incident. Dead wake-on-LAN, an exit-code-only health check, and the second failure after the fix.
transfer: Check what an agent produced, not whether it ran. And an agent with no new inputs can only hand back what you already gave it.
hero_image: TBD
open_items:
  - Hero image direction.
  - Title carries a possessive apostrophe now. Revert if you meant it plural.
---

I was hunched over my desk in a Staten Island shoebox studio apartment when I asked Claude to go check on the vault synthesizer.

The synthesizer's whole job was to read what I'd been putting into my vault, the research and the ideas, and come back with concepts and connections. A vault that improves itself. It finds the connection, I take the connection and go build something with it. I'd left it running for two weeks so it had something to work with.

Here's roughly how that check went:

 "Yea, of course, I'll go check on that right no--OH SHIT... Uhh. So. Funny story... Don't, uh. Don't kill the messenger! haha. The vault synthesizer hasn't actually written anything. No concepts. No connections. Nada. I mean, the daily driver and the meta agent MUST have warned you about thi--- oh... no. They said everything looked good and there were no issues... hm... woops."

Two weeks of nothing. I felt like a little kid opening a present on Christmas morning and unwrapped a big ol' turd.

And I'd been reading a report every morning. The daily driver went through my Slack, my Gmail, the latest meeting transcripts, and the notes I'd left the day before, and it told me what my priorities were. It also gave me a brief on which agents ran and which ones failed. Each of those mornings it told me everything ran clean.

So I went digging.

The synthesizer ran on my Mac Mini every night. It was supposed to call a Qwen model on my MacBook Pro to do the actual synthesizing. The wake-on-LAN on the MacBook wasn't working. So every night the Mini dialed into an empty pit, got an error back, and I was never informed.

It turns out the check only looked at whether the process exited. Not whether it produced anything. It watched the thing trigger and it never once asked what came back.

Welp. Lesson learned.

I had Claude make the fix immediately, but the synthesizer continued to give me headaches that went beyond a trigger error. It was finally producing the concepts and connections, but they each contained a one sentence summarization of the thing it just read. No expansion, no leap, nothing I didn't already have. Taking pages of information and coming out with "The research covers agentic frameworks".

Gee, thanks, bud. You really dove into that one. It basically turned into the guy from *The Ringer*.

 "Go ahead. Name any idea." - Synthesizer

 "x402 protocol and the rise of agentic commerce." - Sean

 *nods its head in approval* "Mhm.... that's a great idea." - Synthesizer

The reason behind the problem is just as boring as the synthesizer's output. It had no web search. It wasn't going to bring anything new to the table. All it could do was hand my own material back to me.

So I brought in a critic. Codex reads the same pile and comes back with the expansions and the connections I was after in the first place. That's where the actual ideas started coming from.

Whenever I change something or try something new with one of these agents, I evaluate, trace, and have watchdogs in every corner.

Things still break quietly. It's inevitable. Now it's just caught, fixed, and shined before I unwrap it.
