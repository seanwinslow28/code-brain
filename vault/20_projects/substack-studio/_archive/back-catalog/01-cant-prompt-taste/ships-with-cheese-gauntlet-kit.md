---
type: substack-companion
series: raising-claude
post_number: 1
project: substack-studio
artifact: cheese-gauntlet-prompt-kit
created: 2026-06-05
parent_post: 2026-06-05-raising-claude-post1.md
status: draft
ai-context: "Reader-facing companion tool for Raising Claude post 1 (Nate-style over-deliver-on-a-narrow-promise artifact). Three copy-paste prompts the reader runs to start calibrating their own voice: (1) reference-universe interview, (2) the Cheese Gauntlet, (3) mine-your-pre-AI-writing. The post links here; the post itself never dumps the kit inline. Voice dialed ~60-70% (practical tool, light Sean seasoning in framing, clean prompts)."
---

# The Cheese Gauntlet Prompt Kit

Companion to [You Can't Prompt Taste Into a Machine](2026-06-05-raising-claude-post1.md).

The post's whole point is that you can't describe your way into a machine sounding like you. So here's the part you actually do instead. Three prompts. Run them this weekend, in order, into whatever model you use. Paste your answers back in as you go.

One expectation up front, because it's the thing I got wrong: this is not a one-shot. You're not pasting these in and walking away with your voice on tap. You're starting a pile of evidence the model gets to learn you from. The first session gets you a sharper outline. The tenth gets you something that sounds like you wrote it. Treat it like reps, not a magic prompt.

Do them in this order. The gauntlet alone tells the model what you're *not*. The other two tell it what you actually are. You want all three.

---

## Prompt 1: The Reference-Universe Interview

**What it's for:** Left to guess, a model pegs you as a person of tasteful, prestige, respectable interests. You are not that person. Nobody is. This drags out the real stuff: the shows you quote at 2 a.m., the music you'd actually defend, the embarrassing tier. Your references are half your voice, and the model will invent generic ones unless you hand it the real ones.

**How to run it:** Paste the prompt. Answer out loud, fast, no editing. Don't make yourself sound cool. The wrong-but-true answer beats the impressive one every time. When it's done, save the whole transcript.

```
You're interviewing me to build a map of my actual cultural taste, so you can
later write in my voice without inventing generic references. Ask me ONE question
at a time. Go deep, not wide: when I name something, follow up on WHY, the
specific line or moment I love, where I was when I found it, who I associate it
with. Cover, over the course of the interview:

- The TV shows and movies I quote in real life (not the ones I'd list to look
  smart, the ones I actually quote)
- Music: what I grew up on, my embarrassing tier, the song I'd defend to the death
- Where I'm from, and the specific places, slang, and people that come with it
- Food, games, sports, internet stuff, whatever I actually spend time on
- The thing I love that I'd be a little embarrassed to admit

Push me when an answer is generic. If I say "I like comedies," make me name the
exact bit. Keep going until you have specifics, not categories. At the end, give
me back a tight inventory of my reference universe with the specific lines and
details I gave you, and a short note on how I tend to deploy them.
```

---

## Prompt 2: The Cheese Gauntlet

**What it's for:** You can't describe your voice. Trust me, you'll try, and you'll produce a paragraph of adjectives that fits half the planet. But you can spot what *isn't* you instantly. This weaponizes that. The model generates ten lines of the exact stuff you hate, in your name, and you react. Your disgust is the signal. The "no" draws the outline that the adjectives couldn't.

**How to run it:** Paste the prompt. When the ten lines come back, react to each one FAST, before the polite part of your brain shows up. One or two words is fine. "No." "Gross." "Never." When something's almost right but still off, say why in five words. Save the reactions.

```
I want to find my writing voice by reacting to what it ISN'T.

Generate 10 short lines "in my voice" on [PICK A TOPIC YOU'D ACTUALLY WRITE ABOUT
-- your work, a life update, a thing you learned]. But write them in the register
I most hate: LinkedIn-inspirational, motivational-poster, hustle-culture, fake-
profound, the stuff that makes me physically cringe. Make them fluent and
confident and grammatically perfect. Number them 1 to 10.

Do not explain them. Just give me the 10 lines and wait.

After I react to each one (I'll be fast and blunt), collect my reactions and tell
me what they reveal about my actual voice: the registers I reject, the moves I
won't make, the words that are instant tells. Turn my disgust into a list of
things to never write.
```

---

## Prompt 3: Mine Your Pre-AI Writing

**What it's for:** This is the strongest one, and the one most people skip because they think they don't have anything. You do. The texts you sent your friends in 2014. An old blog. A zine. Emails. A notebook. A half-finished screenplay. Anything you wrote before a model could write it for you is evidence of a voice that's provably yours, with no machine in the loop. Feed it in whole. Don't summarize it. The model learns more from one rambling real paragraph than from any description you could write about yourself.

**How to run it:** Go find something. Old enough that AI had nothing to do with it. Paste a real chunk of it, the more unguarded the better, then paste the prompt under it.

```
Above is a piece of my own writing from before I used AI to write anything. It's
raw, real, and provably mine. Don't fix it. Don't judge it. Mine it.

Tell me how I actually build a sentence: my rhythm, where my jokes land, how long
I run before I cut, the words and constructions I reach for, how I open and how I
close, what I do when I'm being sincere vs. when I'm deflecting. Quote my own
lines back to me as evidence for each pattern you find. Then write me 3 NEW
sentences on a totally different topic that use those exact mechanics, so I can
check whether you've actually got me or you're faking it. I'll tell you which
ones land.
```

---

## What to do with the three outputs

You now have three artifacts: a reference inventory, a list of registers you reject, and a breakdown of how you actually build a sentence. That's the start of your pile.

Paste all three back into one place and tell the model: *this is who I am, draft in this voice, and I'll react.* Then keep reacting. Keep feeding it the next old thing you find, the next line that made you wince, the next reference it guessed wrong. The voice doesn't arrive in one session. It accretes.

That's the whole secret, and it's a little anticlimactic: there isn't a prompt that does it for you. There's just the pile, and the hours, and you in the loop saying *no, not that, this.* Same as raising anything.
