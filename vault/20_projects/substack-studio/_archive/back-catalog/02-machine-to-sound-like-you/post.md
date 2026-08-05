---
series: raising-claude
post_number: 2
title: "I Built a Machine to Sound Like You. Then I Made It Sound Like a Woman Who Names Her Tomato Plants."
subtitle: "Raising Claude · Post 2"
status: published
publish_date: 2026-06-15
live_url: https://seanpwins.substack.com/p/i-built-a-machine-to-sound-like-you
hero_image: images/hero.png
ships_with: VoicePrint
ships_with_status: shipped
pain_point: "it's obvious, we know / I'm becoming a fraud"
voice_chain_run: y
voice_chain_notes: |
  Full chain run 2026-06-10 (storytelling-architecture → substack-value-engine →
  writing-voice-modes → writing-critique → writing-humanity-pass). Critique verdict: ship.
  Analyzer (pre-rewrite): CV 0.81 (in band) / MATTR 0.789. Zero body em dashes.
  AUTHOR REWRITE 2026-06-15 (post-publish): Sean renamed the persona Priya→Mildred throughout,
  swapped the diegetic reference (Mister Rogers → Fran Drescher / "The Nanny"), reworked the
  gauntlet reactions, and tightened the dogfood line (dropped "hand in the cookie jar").
  Grammar pass caught + fixed one leftover "Priya" (the 0.69 line) and two periods-outside-quotes
  ("Hurumph", "The Nanny"). Preserved: the dogfood self-post-mortem (the seniority beat), the
  three numbers (0.39 / 0.69 / 0.57), the VoicePrint install link, "start your pile this weekend",
  em-dash-clean body, references ≤2.
event: voiceprint-build
created: 2026-06-08
voice_target: Sean Mode ~70% (creative/hiring audience; grit dialed down by SUBSTITUTION, not sterilized)
pre_publish_checklist:
  - Run writing-voice-modes → writing-critique → writing-humanity-pass on the body
  - Run the analyzer/proof to confirm burstiness sits in your baseline band
  - Confirm zero em dashes (humanity-pass hard rule)
  - Confirm Do-Not-Promote framing stays suppressed (it is not in this draft — keep it that way)
  - Reference count: ≤2 (now Fran Drescher / "The Nanny", diegetic via Mildred)
  - Swap the install link / VoicePrint repo URL in before publish
notes: |
  Build-narrative for the VoicePrint ship. Doubles as the Post-2 launch (ends on
  "start your pile this weekend"). The dogfood-caught over-claim is a deliberate
  blameless-self-post-mortem beat (the seniority signal). Numbers are real (dogfood
  2026-06-08): generic-AI burstiness 0.39, the made-up persona's samples 0.69, the
  generated draft 0.57 → closer to her. Persona renamed Priya→Mildred by Sean 2026-06-15.
---

# I Built a Machine to Sound Like You. Then I Made It Sound Like a Woman Who Names Her Tomato Plants.

The strangest part of building a tool that clones your voice is the day you have to prove it can sound like someone who is nothing like you, and that it kept none of you in the process.

Her name is Mildred. I made her up. She writes a community garden newsletter, she names her tomato plants after her favorite presidents, and she quotes Fran Drescher because… why not? My favorite quote of hers is “I put ketchup on my tomato salad.” She is very much my opposite. And the only way to know my tool actually worked was to feed it Mildred and confirm that what came back out sounded like her, and not one bit like me.

Let me back up.

The marketplace is already drowning in tools that promise to make AI write like you. I tried a pile of them. They all do one of two things. They ask you to describe your voice, or they ask you to feed them ten old blog posts so they can hand you back a tidy description of your voice, which you then paste back into the same machine that wrote the description. It’s qualitative all the way down. And everyone selling it swears you’ll be eighty percent of the way there on the first try.

You won’t. You can’t describe your own voice. Go ahead, try it right now. You’ll produce a paragraph of adjectives, “witty, conversational, a little dark,” that fits half the planet and teaches a machine nothing. And you can’t analyze a voice you haven’t bothered to write down yet.

So VoicePrint starts at the other end. Before it reads a single thing you’ve written, it writes ten lines you’ll hate. On purpose. In your name. In the exact register that makes you wince, the dig-deep-dream-big, your-garden-is-your-brand, unlock-your-abundance stuff. And you react. Fast, before the polite part of your brain shows up. “No.” “NAH.” “Hurumph.” Whatever you’re feeling. Go wild.

That disgust is the whole trick. You can’t tell me what your voice is, but you can spot what it isn’t from across the room. The “no” draws the outline the adjectives never could. Then it mines what you actually wrote, and it quotes you back to yourself instead of mashing you into a paragraph of mush.

Which brings me back to Mildred. I ran her through the whole thing, start to finish. Then I did the part I was a little afraid of. I handed the draft to a second machine, a cold one with no stake in it being good, and told it to take the result apart.

It did. I had written, in Mildred’s profile, that “her voice barely changes by context.” Confident. Tidy. Completely unearned, because she had only ever shown me one register. I had invented a fact about her to make the profile look finished. That is the precise sin the entire tool exists to prevent, and I had done it myself, in the prose, on the first real test. So I fixed it. Then I fixed the template so it can’t do that to anyone else either.

The part I’m proudest of doesn’t look like much. It’s three numbers. Burstiness, which is basically how much your sentence lengths jump around, the short-then-long rhythm every human has and every machine sands flat. Generic AI prose scored a 0.39. Mildred’s real writing scored a 0.69. The draft my tool wrote in her voice came in at 0.57. Closer to her than to the machine. Not magic. Measured, on her laptop, no account, nothing uploaded anywhere.

That’s the pitch, and it’s a little anticlimactic on purpose: there is no prompt that hands you your voice on a plate. There is a pile of evidence, and the hours, and you in the loop saying no, not that, this. Same as raising anything.

You can start your pile this weekend. I packaged the whole method into a free, local Claude plugin called [VoicePrint](https://github.com/seanwinslow28/voiceprint), so you don’t have to run the prompts by hand. Nothing you write leaves your machine. Install it, point it at a folder, and run /voiceprint-start. The first session gets you a sharp outline, not a finished you. The tenth gets you something that sounds like you wrote it.

I spent a month teaching a machine to sound like me. The day it finally clicked was the day it sounded like Mildred, instead. Rambling about compost, thinly sliced tomatoes, and her 103rd rewatch of “The Nanny.” My ramblings are nowhere to be found.
