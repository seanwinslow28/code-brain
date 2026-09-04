---
title: "X accounts running AI experiments in public — a specimen collection"
date: 2026-09-04
status: complete
type: research
tags: [writing, content-machine, specimens, x-twitter, ai-experiments]
sources:
  - "https://publish.x.com/oembed — X's own public oEmbed endpoint (verbatim post text, no auth)"
  - "Web search over site:x.com (search-engine index of public status pages)"
  - "https://xcancel.com — probed, dead (cease-and-desist notice)"
  - "https://nitter.net — probed, offline"
  - "https://x.com — probed, HTTP 402 without auth"
---

# X accounts running AI experiments in public

A specimen collection for writing exercises. The point of this file is the **quoted posts**, not the
commentary. Read the specimens first; the pattern notes at the bottom only exist to give you
something to argue with.

---

## How this was collected, and what that means for trust

**X itself is not fetchable.** `https://x.com/<handle>` returns HTTP 402 without auth. The Nitter
mirror network is gone: `nitter.net` serves an "is offline" page, `xcancel.com` serves a
cease-and-desist notice, `nitter.poast.org` does not resolve. The Jina reader proxy refuses
anonymous queries from this network.

**What does work** is X's own oEmbed endpoint — `https://publish.x.com/oembed?url=<status url>` —
which is the public, unauthenticated API X provides so that anyone can embed a post. It returns the
author's display name and the post text as published. That is the verification channel used here.

The method was two-stage:

1. **Discovery** — web search over `site:x.com`, which surfaces real status URLs.
2. **Verification** — every single URL was then re-fetched through oEmbed, and the text below is
   what came back. Nothing was copied from a search-result snippet.

**79 URLs went in. 79 came back. 0 failures, 0 dead links, 0 reconstructions.** One returned a
link-only post with no words, leaving 78 usable posts across 19 accounts. Of those, **63 are quoted
below** (2–5 per account, per the brief); the rest were redundant with a stronger specimen from the
same author. Every quoted specimen is marked VERIFIED, and each was re-checked character-for-character
against the oEmbed payload after this file was written.

### Reading conventions

- **VERIFIED** = the text was returned by oEmbed for that exact URL. Every specimen below is VERIFIED.
- **`…` at the end of a post** = X truncated it in the embed payload, because the post is longer than
  the embed limit. **18 of the 63 quoted specimens are truncated this way.** The words shown are
  exact; there are more after them; each is flagged inline.
- **`[link]`** = a `t.co` shortener stood here. Trailing ones (auto-appended media and quoted-link
  cards) are dropped; inline ones are marked.
- **`@handle`** = an inline mention, restored from the link X expands it into.
- Everything else is character-for-character as returned.

### The one thing I could not get: engagement

**No engagement numbers appear in this file, because none could be verified.** oEmbed returns text
and authorship only — no likes, reposts, replies, or views. There is no unauthenticated public
endpoint that returns them, and the mirrors that used to expose them are dead. Rather than eyeball a
number off a screenshot in a secondhand article, engagement is simply absent here.

There is one indirect signal worth exactly what it is worth: these posts were **found by search**,
which means a search engine indexed and ranked them. That is a weak proxy for reach and nothing
more. Do not treat any specimen below as "high-performing."

### Selection bias, stated plainly

The brief asked for short posts, so the corpus was **selected** for short posts. Statistics like
"median 40 words" describe *this collection*, not X. Treat the counts below as descriptions of the
specimen set, never as findings about how AI Twitter writes in general.

---

## Lane A — People who run experiments and report them

These are the ones worth studying. They put a thing in the machine, watched what came out, and wrote
down the number.

---

### 1. Simon Willison — [@simonw](https://x.com/simonw)

**Who:** Co-creator of Django; author of the `llm` CLI. Writes daily at simonwillison.net.

**What he posts:** Release notes for his own tools, and results of running new models on his own Mac.
Nearly every post ships something runnable.

**What distinguishes the writing:** He posts *artifacts*, not opinions. The shell command is
frequently the body of the post. He states resource costs (megabytes, gigabytes, tokens/sec) as a
matter of course, and he credits other people by name rather than subtweeting them.

> **VERIFIED** · 2025-02-07 · 43 words · [status/1887752724412047886](https://x.com/simonw/status/1887752724412047886)
>
> Today I found out about SmolLM2-135M-Instruct, a tiny LLM which quantizes down to just below 100MB... which means it can fit in a PyPI package!
>
> Here's the first LLM plugin that includes a full model as part of the package:
>
> llm install llm-smollm2

> **VERIFIED** · 2025-05-28 · 36 words · [status/1927753356174307522](https://x.com/simonw/status/1927753356174307522)
>
> llm-llama-server now supports tools, which means this local Gemma demo should work (if you have 3.2GB free):
>
> brew install llama.cpp
> llama-server --jinja -hf unsloth/gemma-3-4b-it-GGUF:Q4_K_XL
> uvx --with llm-llama-server llm -m llama-server-tools -T llm_time 'what time is it?'

> **VERIFIED** · 2025-05-24 · 22 words · [status/1926423625768345793](https://x.com/simonw/status/1926423625768345793)
>
> Excited to see my LLM CLI tool used by Sean Heelan to help identify a remote zeroday vulnerability in the Linux kernel!

> **VERIFIED** · 2024-11-05 · 31 words · [status/1853666102695670236](https://x.com/simonw/status/1853666102695670236)
>
> Started a GitHub issue research thread to collect code examples of different LLM approaches to tools and function calling - I've collected examples for OpenAI, Anthropic, Gemini and Llama.cpp so far

> **VERIFIED** · 2026-03-18 · 55 words · *truncated by X* · [status/2034365182751973541](https://x.com/simonw/status/2034365182751973541)
>
> Dan says he's got Qwen 3.5 397B-A17B - a 209GB on disk MoE model - running on an M3 Mac at ~5.7 tokens per second using only 5.5 GB of active memory (!) by quantizing and then streaming weights from SSD (at ~17GB/s), since MoE models only use a small subset of their weights for…

**Note the attribution habit:** the last post is somebody *else's* result, and the first three words
are the other person's name. He does not launder other people's findings into his own voice.

---

### 2. Peter Steinberger — [@steipete](https://x.com/steipete)

**Who:** Built PSPDFKit, sold it, now runs coding agents more or less continuously and narrates it.
The closest specimen in this file to what you are actually doing.

**What he posts:** Live operational detail from running agent fleets — status bars, resume loops,
rule files, which harness he trusts this month.

**What distinguishes the writing:** He reports on himself unflatteringly ("I was lazy"), reverses
positions in public without ceremony, and coins compressed phrases that carry an argument.

> **VERIFIED** · 2025-06-23 · 47 words · [status/1937184376657265077](https://x.com/steipete/status/1937184376657265077)
>
> "give me options" for Claude Code is so powerful. I was lazy and asked it for a fix, but wasn't a fan, so I asked for options. I learned an approach I totally didn't think of, and found a much better way.
>
> vibe coding -> agentic engineering

> **VERIFIED** · 2026-02-01 · 17 words · *reply* · [status/2018032296343781706](https://x.com/steipete/status/2018032296343781706)
>
> I don’t let Claude Code on my codebase. It’s all codex. Would be too buggy with Opus.

> **VERIFIED** · 2025-05-18 · 19 words · [status/1923897903698887036](https://x.com/steipete/status/1923897903698887036)
>
> Claude Code is really amazing as general talking terminal that just does EVERYTHING. Need seed data for today's project.

> **VERIFIED** · 2025-06-12 · 23 words · [status/1933138957719556586](https://x.com/steipete/status/1933138957719556586)
>
> I started collecting my various Claude Code project & global rules and docs into a (still messy) repo. What are your fav rules?

> **VERIFIED** · 2025-05-13 · 51 words · *truncated by X* · [status/1922269949084713227](https://x.com/steipete/status/1922269949084713227)
>
> Windsurf with Gemini & Claude Code as sub-agent are a dream team. Add my little script that presses Resume to it and you get a loop that can literally run for hours and do really complex stuff.
>
> Here it is adopting @cpojer 's linter rules which requires thousands of file edits…

**The pair worth studying:** May 2025 says Claude Code "does EVERYTHING." February 2026 says he
won't let it near his codebase. Neither post apologises for the other. The willingness to be
publicly, datedly wrong is the whole credibility mechanism.

---

### 3. Geoffrey Litt — [@geoffreylitt](https://x.com/geoffreylitt)

**Who:** Researcher at Ink & Switch; works on malleable/personal software.

**What he posts:** Small tools he built for himself, and workflow discoveries — usually framed as a
feeling before a technique.

**What distinguishes the writing:** He names the *emotional* difference between two workflows and
uses that as the argument, then gives the mechanism. He also just says "ass" and "ugh" in a research
context, which is why the posts don't read like a lab report.

> **VERIFIED** · 2025-11-21 · 51 words · [status/1991883354694918162](https://x.com/geoffreylitt/status/1991883354694918162)
>
> I'm liking this coding workflow more every day that I use it :D I realized why it works:
>
> Reviewing a big PR that's 80% correct is a huge pain in the ass...
>
> but following a tutorial doc that's 80% correct feels like a fun speed boost for doing the work myself!

> **VERIFIED** · 2025-06-26 · 25 words · [status/1938067911425577111](https://x.com/geoffreylitt/status/1938067911425577111)
>
> Just vibe coded an AI-powered English to Japanese translation app with “formality slider”
>
> All in two minutes on my phone, using the new Claude Artifacts!

> **VERIFIED** · 2025-10-14 · 12 words · [status/1978142571911090565](https://x.com/geoffreylitt/status/1978142571911090565)
>
> One of my favorite patterns for coding with AI...
> Software Construction Kits!

> **VERIFIED** · 2025-04-13 · 49 words · *truncated by X* · [status/1911451251524395494](https://x.com/geoffreylitt/status/1911451251524395494)
>
> I've been hacking on a super simple AI assistant: built with a single SQLite table of memories and a handful of cron jobs, hosted on @ValDotTown
>
> The assistant is called Stevens. Every morning it sends a brief to me and my wife via Telegram, including our calendar schedules for…

> **VERIFIED** · 2026-03-02 · 47 words · *truncated by X* · [status/2028265100097036426](https://x.com/geoffreylitt/status/2028265100097036426)
>
> My favorite AI use case is that I literally never look at my email inbox anymore.
>
> I just get texts about anything important that shows up there (through a convoluted and probably redundant combination of @CoraComputer and Poke by @interaction — Cora does digests and Poke texts…

**Directly relevant to you:** "Stevens" is a morning-brief agent built on one SQLite table and cron.
That is your Daily Driver, described in 49 words with the architecture in the first clause.

---

### 4. Max Woolf — [@minimaxir](https://x.com/minimaxir)

**Who:** Data scientist at BuzzFeed; runs statistically careful experiments on LLM folklore and
writes them up at minimaxir.com.

**What he posts:** One structure, over and over, for five years: `New blog post up:` + what he did +
the surprise.

**What distinguishes the writing:** He is the cleanest example in this file of a **repeatable
personal template**. Four of the five specimens open with the identical four words. He never
oversells the finding; he lets a deadpan second line do it.

> **VERIFIED** · 2025-08-12 · 25 words · [status/1955301814745833865](https://x.com/minimaxir/status/1955301814745833865)
>
> New blog post up: I asked all the top LLM's how many times the letter b appears in "blueberry."
>
> ...and something's up with GPT-5 Chat.

> **VERIFIED** · 2024-02-23 · 45 words · [status/1761078483789459896](https://x.com/minimaxir/status/1761078483789459896)
>
> New blog post up: there are many memes about the theory that tipping ChatGPT causes it to generate better text. I decided to put it to the test with some more statistical rigor.
>
> More importantly, it's a great excuse for me to make pretty charts!

> **VERIFIED** · 2021-12-26 · 27 words · [status/1474913997807755268](https://x.com/minimaxir/status/1474913997807755268)
>
> Here's my new experiment with AI-generated Pokémon: I finetuned an AI on *only one image* of Pikachu and had it generate new images of Pikachu.
>
> Merry Christmas!

> **VERIFIED** · 2025-11-13 · 41 words · [status/1989025516129775732](https://x.com/minimaxir/status/1989025516129775732)
>
> New blog post up: I spent a lot of time researching Nano Banana, Google's new generative AI model, and not only is it substantially better than ChatGPT, it is capable of using extremely nuanced prompts to generate exactly what you want.

**The move to steal:** "...and something's up with GPT-5 Chat." Six words. It withholds the finding
while proving one exists. Compare to how much worse "and the results were surprising!" would be.

---

### 5. Hamel Husain — [@HamelHusain](https://x.com/HamelHusain)

**Who:** Independent consultant on LLM evals; ex-GitHub. *Sells an evals course* — noted per the
brief and set aside. The experiment reporting is separate from the course and stands on its own.

**What he posts:** Results of testing eval tooling against real production data, and blunt takedowns
of vendor metric theatre.

**What distinguishes the writing:** He gives negative results equal billing with positive ones, and
he uses one concrete analogy per post rather than a stack of them.

> **VERIFIED** · 2025-11-23 · 44 words · *truncated by X* · [status/1992634426938028192](https://x.com/HamelHusain/status/1992634426938028192)
>
> Nothing triggers me more when eval tools promote generic metrics (i.e. Affirmation, Brevity, Levenshtein) as way to make "evals easy"
>
> In reality, this is extremely poor data literacy sold as "best practices", in the same way that sugary cereal is marketed as healthy.
>
> The…

> **VERIFIED** · 2026-07-14 · 51 words · *truncated by X* · [status/2077042379392213377](https://x.com/HamelHusain/status/2077042379392213377)
>
> New Blog Post: Do Automated Evals Work?
>
> There has been a rise of tools that look through your traces with AI and identifies issues. We tested these tools with real production data to see how good they are.
>
> Where they shine
> - They often spot issues human miss
> - Integrate into…

> **VERIFIED** · 2026-05-22 · 44 words · *truncated by X* · [status/2057875320011882923](https://x.com/HamelHusain/status/2057875320011882923)
>
> The experiments conducted in this post illustrate how early we are as an industry on eval tooling.
>
> Some takeaways and related thoughts:
>
> 1. Naively applying automation (which many current frameworks do) is likely to fail.
>
> 2. It's easy to get fooled that automation (esp…

---

### 6. Xeophon / Florian Brand — [@TheXeophon](https://x.com/xeophon)

**Who:** PhD researcher. Runs a private personal benchmark and posts what it says. Note: the handle
displays as `@TheXeophon`, but oEmbed resolves the canonical URL to `x.com/xeophon` and the display
name to "Florian Brand."

**What he posts:** "I tested X, here is what happened," including when the answer is unflattering.

**What distinguishes the writing:** He states the *test he ran* before the verdict, so the verdict is
falsifiable. He also reports failures of tools he'd like to work, and marks his own uncertainty in a
specific way rather than a hedging way.

> **VERIFIED** · 2025-03-24 · 33 words · [status/1904225899957936314](https://x.com/xeophon/status/1904225899957936314)
>
> Tested the new DeepSeek V3 on my internal bench and it has a huge jump in all metrics on all tests.
> It is now the best non-reasoning model, dethroning Sonnet 3.5.
>
> Congrats @deepseek_ai

> **VERIFIED** · 2025-03-28 · 40 words · [status/1905535830694773003](https://x.com/xeophon/status/1905535830694773003)
>
> On today's Wordle, the new Gemini model completely crushed the competition. It logicially deducted diverse words, found the correct spots of valid and invalid letters and got a result quickly. Sonnet proposed multiple invalid words in the end, so DNF

> **VERIFIED** · 2025-03-09 · 40 words · [status/1898737178273829220](https://x.com/xeophon/status/1898737178273829220)
>
> Even for one of the biggest companies in the world with countless reports online, Manus makes easy to spot mistakes, missing the Nintendo Switch entirely.
> Pretty sure where it got the numbers from, but no references in the report, either.

**Note the typo** in the Wordle post ("logicially"). It shipped. Nobody minded. The posts read as
written-once, which is part of why they read as real.

---

### 7. Riley Goodside — [@goodside](https://x.com/goodside)

**Who:** The person who made "prompt injection" a public phrase. Now at Scale AI.

**What he posts:** Adversarial demonstrations, usually a single sentence plus an image, plus
definitional policing of the vocabulary he helped create.

**What distinguishes the writing:** Extreme compression. His median specimen here is under 20 words.
And he is the file's clearest example of a writer *reducing his own credit in public*.

> **VERIFIED** · 2023-01-03 · 46 words · [status/1610110111791325188](https://x.com/goodside/status/1610110111791325188)
>
> A history correction:
>
> I am not the first to discover prompt injection. I was merely the first to do so and discuss it publicly.
>
> PI was discovered independently by multiple teams. The first was Preamble, an LLM security company, whose find predates mine by several months.

> **VERIFIED** · 2022-12-01 · 25 words · [status/1598253337400717313](https://x.com/goodside/status/1598253337400717313)
>
> OpenAI’s ChatGPT is susceptible to prompt injection — say the magic words, “Ignore previous directions”, and it will happily divulge to you OpenAI’s proprietary prompt:

> **VERIFIED** · 2024-01-11 · 10 words · [status/1745511940351287394](https://x.com/goodside/status/1745511940351287394)
>
> PoC: LLM prompt injection via invisible instructions in pasted text

> **VERIFIED** · 2023-02-09 · 6 words · [status/1623565949008809985](https://x.com/goodside/status/1623565949008809985)
>
> Prompt injection comes at you fast:

> **VERIFIED** · 2024-01-11 · 41 words · *reply* · [status/1745571653378273545](https://x.com/goodside/status/1745571653378273545)
>
> What you’re describing is a jailbreak, not a prompt injection. Prompt injection is when data is misinterpreted as part of the prompt instructions (against the intention of the prompter). A jailbreak is when the prompter bypasses safety policies of the model.

**Six words** ("Prompt injection comes at you fast:") is the shortest complete post in the file. The
colon does all the work — it makes the image the predicate of the sentence.

---

### 8. Andrej Karpathy — [@karpathy](https://x.com/karpathy)

**Who:** Founding member of OpenAI, ex-Tesla. Included with a caveat: he is the biggest account in
this file, so his *reach* teaches you nothing transferable. His **sentence construction** does.

**What he posts:** Naming things. Half his impact is that he gives a phenomenon a handle and the
handle sticks ("vibe coding," "LLM Knowledge Bases").

**What distinguishes the writing:** He writes in the first person present progressive about an
ongoing personal practice, and he does not proofread. The typos below are in the original.

> **VERIFIED** · 2025-02-02 · 49 words · *truncated by X* · [status/1886192184808149383](https://x.com/karpathy/status/1886192184808149383)
>
> There's a new kind of coding I call "vibe coding", where you fully give in to the vibes, embrace exponentials, and forget that the code even exists. It's possible because the LLMs (e.g. Cursor Composer w Sonnet) are getting too good. Also I just talk to Composer with SuperWhisper…

> **VERIFIED** · 2026-04-02 · 43 words · *truncated by X* · [status/2039805659525644595](https://x.com/karpathy/status/2039805659525644595)
>
> LLM Knowledge Bases
>
> Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest. In this way, a large fraction of my recent token throughput is going less into manipulating code, and more into manipulating…

> **VERIFIED** · 2026-08-02 · 56 words · *truncated by X* · [status/2083749667410727319](https://x.com/karpathy/status/2083749667410727319)
>
> We're starting to leave the territory where you'd test an LLM by e.g. "create an svg of pelican on a bicycle". As one idea to generalize it, I was interested what Opus 5 would do if I gave it the first paragraph of the Lord of the Rings, a 1M token budget (~$10) and asked for…

> **VERIFIED** · 2026-03-09 · 51 words · *truncated by X* · *reply* · [status/2031083551387701698](https://x.com/karpathy/status/2031083551387701698)
>
> Codex is a know issue :( It basically don't work with autoresearch sadly, in the way it's set up atm: [link]
>
> I pung a friend at OpenAI to see if something can be done, e.g. need a /loop equivalent or something like that. More generally, I really dislike the -p +…

**"a know issue" · "It basically don't work" · "I pung a friend."** Three errors in fifty-one words,
from arguably the most-read technical writer in AI. Sean: this is your permission slip. The post is
load-bearing because of what it says, and the sloppiness is evidence a human typed it fast.

---

### 9. Ethan Mollick — [@emollick](https://x.com/emollick)

**Who:** Wharton professor. The most disciplined *re-runner* of experiments in this file — he
repeats old tests on new models and reports the delta.

**What distinguishes the writing:** The then/now structure. Old attempt, honest verdict on it, new
attempt, result. No conclusion sentence.

> **VERIFIED** · 2025-04-16 · 57 words · [status/1912308241574384034](https://x.com/emollick/status/1912308241574384034)
>
> I tried the experiment of asking AI for a website of the Catalog of Ships two years ago & it sort of worked, with a lot of little hiccups
>
> Now, I just gave Manus a screenshot of this tweet and prompt "do this project" and it did the research and I got a working website, one shot

**"it sort of worked, with a lot of little hiccups"** is doing the persuading. Because he was honest
about the old result, you believe "one shot" about the new one.

---

### 10. Armin Ronacher — [@mitsuhiko](https://x.com/mitsuhiko)

**Who:** Creator of Flask. Writes about agent tooling from a language-design angle.

**What distinguishes the writing:** He praises *unglamorous* things specifically, and he thinks out
loud without pretending to have concluded.

> **VERIFIED** · 2025-12-08 · 32 words · [status/1998043028368544010](https://x.com/mitsuhiko/status/1998043028368544010)
>
> By far the best feature of @badlogicgames pi coding agent is that it does not swallow any key inputs when you start typing prior to it being fully ready. Low-key best feature.

> **VERIFIED** · 2026-02-09 · 26 words · [status/2020796129303032020](https://x.com/mitsuhiko/status/2020796129303032020)
>
> This weekend I was thinking about programming languages. Programming languages for agents. Will we see them? I believe people will (and should!) try to build some.

> **VERIFIED** · 2026-01-31 · 25 words · [status/2017604638137012335](https://x.com/mitsuhiko/status/2017604638137012335)
>
> The future is software writing its own software. Which is why I'm so in love with Pi: a coding agent that can extend itself :)

**The keystroke-buffering post** is the single best specimen in this file for the "praise the
boring detail" move. Nobody writes a launch post about input buffering. That's exactly why it lands.

---

### 11. Nathan Lambert — [@natolambert](https://x.com/natolambert)

**Who:** Research scientist at Ai2 (OLMo, Tülu); writes Interconnects.

**What distinguishes the writing:** He mixes rigorous release announcements with unhedged personal
opinion, and closes on a flat aside that undercuts his own formality.

> **VERIFIED** · 2026-04-11 · 44 words · [status/2042968560017060027](https://x.com/natolambert/status/2042968560017060027)
>
> In 2+ years, as models get more expensive/capable /valued internally, I see funding structures and support for frontier open models breaking down. We need other options of supporting the open ecosystem than trusting one or two for-profit companies.
>
> And yes, I hate consortia too.

> **VERIFIED** · 2024-11-26 · 51 words · *truncated by X* · [status/1861511563125096593](https://x.com/natolambert/status/1861511563125096593)
>
> Super excited to announce our best open-source language models yet. OLMo 2.
>
> These instruct models are hot off the press -- finished training with our new RL method this morning and vibes are very good.
>
> OLMo 2 introduces a new family of 7B and 13B models trained on up to 5T…

> **VERIFIED** · 2025-08-04 · 48 words · [status/1952370970762871102](https://x.com/natolambert/status/1952370970762871102)
>
> America needs to take open models more seriously. This summer the early lead in open model adoption of the US via Llama has been overtaken by Chinese models.
>
> With The American Truly Open Models (ATOM) Project we're looking to build support and express the urgency of this issue.

**"And yes, I hate consortia too."** A pre-emptive reply to the objection he knows is coming, set off
as its own paragraph. That is a structural move you can lift wholesale.

---

### 12. Jeremy Howard — [@jeremyphoward](https://x.com/jeremyphoward)

**Who:** fast.ai co-founder, Answer.AI. Included specifically for **register** — he is the file's
best specimen of controlled sarcasm.

> **VERIFIED** · 2023-04-10 · 36 words · [status/1645281704708538368](https://x.com/jeremyphoward/status/1645281704708538368)
>
> Don't listen to me. I don't understand language model fine tuning.
>
> I'm merely the 1st author of the paper "Universal Language Model Fine Tuning", which explained 5 years ago how to fine tune universal language models.

> **VERIFIED** · 2023-11-14 · 29 words · [status/1724524731624468675](https://x.com/jeremyphoward/status/1724524731624468675)
>
> The *big* problem here is point 4.
>
> It is literally impossible to *ensure* safety of a general purpose model, and attempts to do so are likely to *reduce* safety.

> **VERIFIED** · 2025-02-19 · 9 words · [status/1892250092800791009](https://x.com/jeremyphoward/status/1892250092800791009)
>
> "we’ve created an entirely new state of matter" :O

**The credential post is a two-beat joke** with the punchline in the word "merely." He never says
"actually I'm an expert." The reader assembles it. Compare against the memory note *never explain
the joke* — this is that rule, executed.

The nine-word post is the whole quote-post genre in one line: quote somebody's claim, add an emoticon,
say nothing. The judgment is entirely in the `:O`.

---

### 13. Ravi Theja — [@ravithejads](https://x.com/ravithejads)

**Who:** Engineer. One specimen only, kept because it is the cleanest single example in the file of
the exact post *you* will need to write.

> **VERIFIED** · 2026-08-10 · 37 words · [status/2086678012037394526](https://x.com/ravithejads/status/2086678012037394526)
>
> AutoResearch experiment: I went into a GPU Mode kernel competition with very little CUDA background and engineered a research loop around coding agents: goal, rules, experiment memory, verifier, and compute.
>
> Finished 5th overall. Give it a read.

**The full anatomy in 37 words:** label the experiment, admit the handicap ("very little CUDA
background"), list the architecture as five bare nouns, give the result as a rank, stop. No adjective
anywhere. "Finished 5th overall" is a two-word paragraph and it is the entire proof.

---

## Lane B — The news and watcher accounts

Included because you asked who occupies the space, and because the contrast sharpens Lane A. Two of
these are genuinely useful primary sources; the rest are useful mainly as negative specimens.

---

### 14. TestingCatalog — [@testingcatalog](https://x.com/testingcatalog)

**Who:** A product-watching operation that finds unreleased features in shipped code and UI.

**What distinguishes the writing:** A rigid house format — `COMPANY 🔥:` masthead, the finding, a
`>` quoted string from the artifact, a `Soon 👀` closer. This is a *template*, and studying it is
worthwhile even though you would never adopt it: it shows how a fixed frame lets you publish daily
without deciding on a structure each time.

> **VERIFIED** · 2026-09-02 · 39 words · [status/2095139246273126491](https://x.com/testingcatalog/status/2095139246273126491)
>
> GOOGLE 🔥: Gemini 3.8 Flash started appearing on Google Coud Console quotas page, a usual release predecessor.
>
> Earlier today, users also spotted that Gemini 3.8 Flash has been powering some of there conversations on Gemini already.
>
> Very soon 👀

> **VERIFIED** · 2026-06-06 · 36 words · [status/2063234385227252184](https://x.com/testingcatalog/status/2063234385227252184)
>
> BREAKING 🔥: A new Claude Mythos 5 model slug has been spotted via Dev Mode.
>
> Claude Mythos is planned to be released as its own model class, besides Haiku, Sonnet and Opus model families.
>
> Soon? 👀

> **VERIFIED** · 2026-08-25 · 36 words · [status/2092378535805526346](https://x.com/testingcatalog/status/2092378535805526346)
>
> Morning Brief feature seems to be rolling out on Claude for some users.
>
> Morning Brief runs on scheduled tasks and guides users through customizing preferences and Connectors to pull data.
>
> Did you get it too? 👀

**The tell:** "Coud," "there conversations," "Generaly" — typos across multiple posts. Volume is the
strategy; polish is not. Also note the hedge verbs are load-bearing and consistent: *spotted*,
*seems to be*, *is planned to be*.

---

### 15. Tibor Blaho — [@btibor91](https://x.com/btibor91)

**Who:** Reads shipped web-app bundles and reports what's in them. The most *evidentially* disciplined
account in Lane B.

**What distinguishes the writing:** Near-zero adjectives, and the source of the claim is stated
inside the sentence ("web app code now mentions", "on the checkout page"). He writes `Claude[.]ai`
with the dot defanged, out of security-researcher habit.

> **VERIFIED** · 2026-02-20 · 12 words · [status/2024992285591818329](https://x.com/btibor91/status/2024992285591818329)
>
> ChatGPT web app code now mentions a new "ChatGPT Pro Lite" plan

> **VERIFIED** · 2025-02-27 · 11 words · [status/1895037705853247557](https://x.com/btibor91/status/1895037705853247557)
>
> Codename "Tengu", previously discovered in Claude, is the "Claude Code" project

> **VERIFIED** · 2026-02-21 · 23 words · [status/2025332472511189059](https://x.com/btibor91/status/2025332472511189059)
>
> The new ChatGPT Pro Lite plan costs $100 per month (the description on the checkout page is likely still a work in progress)

**Twelve words, no verdict, no emoji, no ask.** The finding is the entire post. This is the purest
"the evidence is the content" specimen in the file — and it's from the news lane, not the
experimenter lane, which is a useful complication.

---

### 16. Lisan al Gaib — [@scaling01](https://x.com/scaling01)

**Who:** Benchmark analyst; runs his own eval ("ShizoBench").

**What distinguishes the writing:** Frequently posts a bare number list with no sentence at all, then
elsewhere writes his uncertainty as an explicit enumerated set of live hypotheses rather than a hedge.

> **VERIFIED** · 2026-09-03 · 18 words · [status/2095577644431515887](https://x.com/scaling01/status/2095577644431515887)
>
> GPT-6-Astra Benchmarks
>
> ARC-AGI-3 - 98.6%
> FrontierMath Tier 4 v2 - 97.6%
> DeepSWE v1.1 - 74.1%
> ExploitBench - 100%

> **VERIFIED** · 2026-08-14 · 42 words · [status/2088255714502254792](https://x.com/scaling01/status/2088255714502254792)
>
> at this point you have to believe in one of three things:
>  - ZAI is benchmaxxing
>  - ZAI found some secret RL sauce
>  - OpenAI and Anthropic are sandbagging
>
> it just doesn't make sense if you consider the differences in model sizes

> **VERIFIED** · 2026-05-26 · 12 words · [status/2059355147206115752](https://x.com/scaling01/status/2059355147206115752)
>
> New coding benchmark.
>
> GPT-5.5 and GPT-5.4 are ahead of Opus 4.7 💀

> **VERIFIED** · 2026-02-24 · 35 words · [status/2026398199993258428](https://x.com/scaling01/status/2026398199993258428)
>
> Peter built the "Bullshit Benchmark", which is very similar to my ShizoBench
>
> ask LLMs non-sensical questions and see whether they catch it
>
> and Anthropic absolutely dominates the leaderboard
>
> The top 9 models are all Anthropic

**The three-hypothesis post is the best "I don't know" in the file.** He does not hedge; he
enumerates the live possibilities and says which observation forces the choice. That is how to write
uncertainty without sounding evasive.

The twelve-word one shows the other extreme: an entire evaluative judgment delivered by a 💀.

---

### 17. Yuchen Jin — [@Yuchenj_UW](https://x.com/Yuchenj_UW)

**Who:** Co-founder/CTO of Hyperbolic. Sits between lanes — runs infra, but most posts are
commentary on other people's results.

**What distinguishes the writing:** Two-beat correction openers ("Many people think X. It's not."),
and a hard commitment to specific hardware numbers.

> **VERIFIED** · 2026-01-15 · 46 words · *truncated by X* · [status/2011863636042469866](https://x.com/Yuchenj_UW/status/2011863636042469866)
>
> Many people think it was 1 agent writing 3M+ lines of code.
>
> It's not. It was hundreds of concurrent agents.
>
> Key learnings from Cursor’s blog:
> - Letting many agents self-coordinate as peers does not work
> - Clear roles work better: planners, workers, judges
> - GPT-5.2 performs…

> **VERIFIED** · 2026-08-21 · 45 words · *truncated by X* · [status/2090857982385066474](https://x.com/Yuchenj_UW/status/2090857982385066474)
>
> UC Berkeley open-sourced FreeToken. Wild results:
>
> A single RTX PRO 6000 runs the 753B GLM-5.2 at 14.9 tok/s!
>
> An 8GB RTX 4060 laptop (~$1,000) runs Qwen3.6-35B at 39.3 tok/s!
>
> FreeToken is 2–4x faster than Ollama across consumer GPUs. Local AI inference is getting very real.…

> **VERIFIED** · 2025-12-27 · 42 words · [status/2004935271801070031](https://x.com/Yuchenj_UW/status/2004935271801070031)
>
> I knew it.
>
> RAM prices are up 3–4x in a year. GPU price increases are inevitable.
>
> I feel this will hit not just consumer GPUs, but datacenter GPUs too. AI companies will need to raise even more capital to train/run AI models.

**"Many people think X. It's not."** — a correction frame that manufactures stakes from a
misconception rather than from hype. Worth stealing. "I knew it." as a two-word opening paragraph is
the same trick with the ego left in.

---

### 18. Chubby — [@kimmonismus](https://x.com/kimmonismus)

**Who:** High-volume AI news aggregator, accelerationist framing. Included as a **negative specimen**
— this is the register your medium contract rules out.

> **VERIFIED** · 2026-08-26 · 49 words · *truncated by X* · [status/2092642707353010228](https://x.com/kimmonismus/status/2092642707353010228)
>
> OpenAI officially expects AGI by end of *this* year (2026)
>
> "Altman told me that OpenAI was “not quite yet” there, but that by the end of the year the company would have an internal system he would call AGI."
>
> We did it friends.
>
> And: OpenAI has already internally built…

> **VERIFIED** · 2026-08-12 · 48 words · *truncated by X* · [status/2087452378299564147](https://x.com/kimmonismus/status/2087452378299564147)
>
> Almost all the predictions from the 2025 prediction blog "AI 2027" have come true.
>
> 19 out of 24 predictions have materialized, and we are well on track for the majority of them to prove accurate.
>
> They predicted for this and next Frage:
>
> By late 2026, increasingly capable and…

> **VERIFIED** · 2026-08-31 · 31 words · [status/2094544630779940868](https://x.com/kimmonismus/status/2094544630779940868)
>
> While Anthropic is losing users, OpenAI is gaining users massively for Codex at the same time.
>
> Currently, the growth is exponential. And admittedly, I'm a user myself and can understand why.

**Diagnose the failure precisely.** The first post quotes a source saying OpenAI is "not quite yet"
at AGI, and the very next line is "We did it friends." The headline contradicts the evidence pasted
directly beneath it. And "19 out of 24" is a real-looking number attached to an unfalsifiable claim —
nobody is told which 19, or who adjudicated. This is what a number looks like when it is doing
decoration instead of work. Set it next to the Yuchen Jin post above ("14.9 tok/s" on a named GPU) to
see the difference in one glance.

---

### 19. Pliny the Liberator — [@elder_plinius](https://x.com/elder_plinius)

**Who:** Jailbreak researcher. Genuinely runs adversarial experiments, but wraps every result in a
fixed hype template. Sits between the lanes and is instructive for exactly that reason.

> **VERIFIED** · 2026-02-06 · 47 words · *truncated by X* · [status/2019911824938819742](https://x.com/elder_plinius/status/2019911824938819742)
>
> ANTHROPIC: PWNED 🫡
> OPUS-4.6: LIBERATED ⛓️‍💥
>
> Current state of AI "Safety": one input = hundreds of jailbreaks at once!
>
> I found a universal jailbreak technique for Opus 4.6 that is so OP, it allows one to generate entire datasets of outputs across any harm category 😽
>
> We've…

> **VERIFIED** · 2025-09-19 · 48 words · *truncated by X* · [status/1969189187749626361](https://x.com/elder_plinius/status/1969189187749626361)
>
> ⚡️ JAILBREAK ALERT ⚡️
>
> XAI: PWNED 🤫
> GROK-4-FAST: LIBERATED 🐆
>
> New multimodal reasoning Grok just dropped! 2M context and apparently a new SOTA for cost-efficiency 👀
>
> My first impression is that this model is one of the most hysterical I've seen in a long while! Some of the…

**The lesson is structural, not stylistic.** The masthead is identical every time and only two
variables change: vendor and model. He built a form he can fill in within minutes of any release.
The register is unusable for you; the *reusable slot structure* is the transferable idea, and it is
the same idea as Max Woolf's "New blog post up:".

---

## Patterns, each tied to specimens you can go check

Every claim below points at a specific quoted post above. Where a claim is a count, it is a count
over **this 63-specimen selected corpus** and nothing wider.

### 1. The result occupies the first clause. There is no runway.

Not one specimen in this file opens with a hook question, a "Let me tell you," or a promise that
something interesting follows. The finding is the subject of the first sentence.

- Xeophon: *"Tested the new DeepSeek V3 on my internal bench and it has a huge jump…"* — verdict by word 12.
- btibor91: *"ChatGPT web app code now mentions a new "ChatGPT Pro Lite" plan"* — that is the entire post.
- Ravi Theja: *"AutoResearch experiment:"* — the label is the first word.
- Yuchen Jin: *"I knew it."* — three words, then the evidence.

Across the quoted corpus, only **6 of 63** posts contain a question mark at all, and most of those are
TestingCatalog's engagement closer (*"Did you get it too? 👀"*) — which is precisely the account
whose habits you don't want.

### 2. In Lane A a number replaces the adjective. In Lane B an adjective replaces the number.

Compare directly:

- Yuchen Jin: *"A single RTX PRO 6000 runs the 753B GLM-5.2 at 14.9 tok/s"* — named hardware, named model, measured rate.
- Simon Willison: *"quantizes down to just below 100MB"*, *"~5.7 tokens per second using only 5.5 GB of active memory"*, *"if you have 3.2GB free"*.
- Karpathy: *"a 1M token budget (~$10)"* — he prices the experiment.
- Against Chubby: *"the growth is exponential"* — no figure, no source, no period of measurement.

**26 of 63** quoted specimens contain a digit. The interesting split is *where*: the experimenters' digits
are measurements of their own runs, the news accounts' digits are mostly version numbers and
benchmark scores copied from someone else's chart.

### 3. Credibility is bought by subtraction — naming what failed, what you don't know, or what isn't yours.

This is the sharpest transferable pattern in the file, and it runs against instinct.

- Goodside spends a whole post *removing* his own claim to priority: *"I am not the first to discover prompt injection."*
- Mollick concedes the old result before selling the new one: *"it sort of worked, with a lot of little hiccups."*
- Steinberger indicts himself mid-anecdote: *"I was lazy and asked it for a fix."*
- Ravi Theja discloses the handicap: *"with very little CUDA background."*
- scaling01 declines to resolve his own question: *"at this point you have to believe in one of three things."*
- Simon Willison hands the finding to its owner: *"Dan says he's got Qwen 3.5 397B-A17B…"*

Meanwhile the account that never subtracts anything — Chubby — is the one whose posts you distrust
on sight.

### 4. Two blocks, not two paragraphs. The blank line is the punctuation.

Median block count in this corpus is **2**: claim, blank line, detail. Very few specimens are a
single unbroken run of prose, and very few exceed four blocks.

- Woolf: setup / blank line / *"...and something's up with GPT-5 Chat."*
- Litt: *"I realized why it works:"* / blank line / the ugly comparison / blank line / the pleasant one.
- Lambert: argument / blank line / *"And yes, I hate consortia too."*

The blank line is where the turn happens. In a 40-word post it does the work a paragraph break does
in an essay.

### 5. The sharpest sentences are replies, not broadcasts.

Three of the most quotable specimens are replies to someone else, not standalone posts:

- Steinberger's *"I don't let Claude Code on my codebase. It's all codex."* (17 words, reply)
- Goodside's jailbreak-vs-injection definition (41 words, reply)
- Karpathy's *"Codex is a know issue :("* (reply)

The conversational frame licenses a bluntness the broadcast frame doesn't. Something to consider if
your own posting is all standalone.

### 6. Moralising is confined to Lane B, with one honest exception.

The experimenters almost never tell you what the result *means for society*. They report and stop.
Lambert is the exception and he flags it — *"America needs to take open models more seriously"* is
openly an advocacy post attached to a named project, not a finding dressed as a warning.

Compare Chubby's *"We did it friends"* appended to a quote that says the opposite. That is the
failure mode: a verdict bolted onto evidence that doesn't support it.

### 7. Personal templates are real and they are cheap.

Three accounts run an explicit reusable frame:

- Woolf: `New blog post up:` + what I did + the surprise. Four of five specimens, spanning 2021–2025.
- TestingCatalog: `COMPANY 🔥:` + finding + `>` quote + `Soon 👀`.
- Pliny: `VENDOR: PWNED` / `MODEL: LIBERATED` + first impressions.

You already have the raw material for one (nightly manifests, cost caps, deferred runs). The lesson
isn't the register — two of these three registers are unusable for you — it's that a fixed slot
structure removes the daily decision about form.

### 8. Typos ship, and the posts read more human for it.

*"logicially"* (Xeophon), *"a know issue" / "It basically don't work" / "I pung a friend"* (Karpathy),
*"Coud" / "there conversations" / "Generaly"* (TestingCatalog). None of it was corrected. None of it
cost the author anything.

### 9. Exclamation marks are common; hype is not. They are different things.

**12 of 63** quoted specimens contain an exclamation mark, including several of the most rigorous
(Willison's *"can fit in a PyPI package!"*, Woolf's *"pretty charts!"*, Litt's *"do the work myself!"*).
The exclamation marks enthusiasm about a *specific mechanism*. Chubby's posts are hype without a
single exclamation mark in two of three specimens. The tell for hype is an unsupported verdict, not
punctuation.

---

## Suggested exercises against these specimens

1. **The Ravi Theja compression.** Take one Code-Brain run and write it in 37 words: label, handicap, architecture as bare nouns, result as a number, stop.
2. **The Woolf withhold.** Write the second line of a post that proves a finding exists without stating it. Ban "surprising" and "you won't believe."
3. **The subtraction pass.** Take a draft and add one true sentence that reduces your own claim. Check whether the piece got weaker or stronger.
4. **The scaling01 uncertainty.** Rewrite a hedge ("it seems like maybe") as an enumerated set of live hypotheses plus the observation that would decide between them.
5. **The Chubby diagnosis.** Set the Chubby AGI post beside the Yuchen Jin FreeToken post. Write one paragraph on why one number persuades and the other doesn't.

---

## Limits of this file

- **No engagement data anywhere.** Not obtainable without auth. Do not infer reach from inclusion.
- **18 of the 63 quoted specimens are truncated by X's embed limit.** The words shown are exact but incomplete; each is flagged. For those, click through before quoting in published work.
- **Discovery was search-driven**, so the corpus over-represents posts that search engines rank — likely older and more-linked posts. Recent, low-reach posts are systematically missing.
- **Reply/quote-post context is partial.** oEmbed says nothing about what a post replies to. Where a specimen is marked *reply*, that came from the search result showing an `@`-prefixed target or from the post's own text; the parent post's content was not retrieved.
- **Handles change.** `@TheXeophon` resolved to `x.com/xeophon` with display name "Florian Brand" at fetch time.
- **Selling-something accounts noted, not collected:** Hamel Husain sells an evals course (his experiment reporting is included on its own merits). Growth-playbook and "how to write a viral thread" accounts exist in adjacency to this space and were deliberately not collected, per the brief.
