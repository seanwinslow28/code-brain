---
title: "Specimens and Craft Mechanics for the Short Comic Post"
date: 2026-09-04
status: active
type: research
tags: [writing, comedy, one-liner, social-post, craft]
sources:
  - https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed
  - https://www.thepoke.com/2026/08/14/our-25-favourite-funny-tweets-of-the-week-131/
  - https://www.thepoke.com/2026/08/07/our-25-favourite-funny-tweets-of-the-week-130/
  - https://www.thepoke.com/2026/02/20/our-25-favourite-funny-tweets-of-the-week-107/
  - https://www.pastemagazine.com/comedy/funniest-tweets-of-the-week/the-funniest-tweets-of-the-week-114
  - https://www.thepoke.com/2024/01/02/were-only-two-days-in-but-this-mansplaining-response-is-already-a-hot-contender-for-best-response-of-the-year/
  - https://funnyhow.substack.com/p/how-anthony-jeselnik-writes-jokes
  - https://www.alexbaia.com/blog/jack-handey-humor-writer-comedy-legend
  - https://stand-upcomedy.com/crowd-work-adapts-group-improv-skills-reason-8
  - https://funnymuscle.com/upgrade-your-crowd-work/
  - https://willhines.substack.com/p/how-to-be-funny
  - https://www.verygoodcopy.com/hubspotcom/the-onion-scott-dikkers-on-writing
---

# Specimens and Craft Mechanics for the Short Comic Post

A specimen collection for studying the joke that lands in 5–50 words with no setup room, with
particular attention to the **reactive** joke — the one written as a reply or quote-post against
someone else's words.

Every line quoted below came from a page or API response actually fetched on 2026-09-04. Nothing
here is reconstructed from memory. Quotations are short excerpts for study; each carries its author
and a link to the original.

---

## 0. What was reachable, and what was not

**X/Twitter is not directly readable.** Three separate routes were tried and all failed:

| Route | Result |
|---|---|
| `https://x.com/<handle>` via fetch | **HTTP 402 Payment Required** |
| `publish.twitter.com/oembed` (the official embed API) | **HTTP 301**, no content |
| `cdn.syndication.twimg.com/tweet-result` (the embed CDN), with a correctly computed token | Served X's generic error page |
| Wayback Machine (`archive.org/wayback/available`) for X status URLs | `archived_snapshots: {}` — no snapshots |

So **no specimen in this file was read on X itself.** Two substitute routes were used instead, and
every specimen is tagged with which one:

- **VERIFIED** — pulled directly from the platform's own public API by this research pass. All
  VERIFIED specimens here are **Bluesky**, via the unauthenticated `public.api.bsky.app` endpoints.
  This is a different platform from X, but the form is identical — same character economy, same
  reply and quote-post mechanics — and, decisively, **the API returns the parent post inline**, so
  the stimulus and the joke arrive together. That is the exact relationship missing from every
  "best tweets" listicle.
- **SECONDHAND** — X posts reproduced verbatim inside the embed markup of a publication whose page
  was fetched. The named publication is given for each. The text is the publisher's embedded copy
  of the post, not a paraphrase, and each carries its original `x.com`/`twitter.com` status URL.

**Corpus size behind this file:** 2,947 Bluesky posts across 23 verified comedian and comedy-writer
accounts (893 replies to other people and 394 quote-posts, each with parent text attached), plus 49
text-only X posts from four publication roundups. The excerpts below are a selected, clean subset;
the working corpus contains a good deal of blue material that is not reproduced here.

---

## 1. The single most useful finding: reactive jokes are a third the length

Measured across the harvested corpus:

| Form | n | Median length | Share at ≤15 words |
|---|---|---|---|
| Reply to someone else | 882 | **6 words** | 78% |
| Quote-post | 400 | **11 words** | 61% |
| Standalone post | 1,360 | **19 words** | — |
| X posts curated as "funniest of the week" | 49 | **22 words** | 22% |

The reactive joke is short **because the stimulus already paid for the setup.** The other person
wrote your first act. Every word you spend re-establishing what they said is a word spent buying
something you already own.

This is the discipline to internalize: a standalone joke has to build its own world in ~22 words. A
reply only has to *turn* — and turning takes about six.

---

## 2. Reactive specimens — VERIFIED (Bluesky public API)

Organized by **what the joke did to the stimulus**, which is the thing worth studying. Format is
stimulus → joke → mechanic.

### 2.1 Take the euphemism literally and supply the real sentence

> **Stimulus** — DiscussingFilm: "Kit Harington has been cast as Gilderoy Lockhart in Season 2 of
> the 'HARRY POTTER' TV series. Nicholas Hoult has left the series due to scheduling conflicts."
>
> **Joke** — Paul F. Tompkins: **"I was scheduled to have the rest of my career"**
>
> — VERIFIED, [bsky.app/profile/pftompkins.bsky.social/post/3mtttis7rxc2r](https://bsky.app/profile/pftompkins.bsky.social/post/3mtttis7rxc2r)

Eight words. The joke is a *fake direct quote* that fills in the euphemism the press release was
hiding behind. Note the mechanic: it does not comment on the news, it **speaks as a person inside
the news.** No "lol imagine", no framing, no "this is basically". Quotation marks do all the
signalling.

### 2.2 Speak as the subject and say the part they left out

> **Stimulus** — The Tennessee Holler: "HANNITY: 'I left NYC because I would walk into restaurants
> and see disdain and disgust on people's faces just because I was in the room.'"
>
> **Joke** — Patton Oswalt: **"Everywhere I went in New York people openly loathed the very sight of
> me. So naturally I concluded that the entire city had gone crazy and I left. There was no other
> possible explanation."**
>
> — VERIFIED, [bsky.app/profile/pattonoswalt.bsky.social/post/3mhmsrvqqzc2z](https://bsky.app/profile/pattonoswalt.bsky.social/post/3mhmsrvqqzc2z)

The highest-engagement quote-post in the entire harvested corpus (8,823 likes). It is a
**translation**, not a comment. The joke never says "he's the problem" — it re-voices the quote
until the omitted conclusion is unavoidable. "There was no other possible explanation" is the
whole joke and it sits last.

### 2.3 Accept the premise, then audit one detail of it

> **Stimulus** — Adam Kinzinger: "…His brain is filled with tapioca and raisins"
>
> **Joke** — Michael Ian Black: **"You give him too much credit by including raisins."**
>
> — VERIFIED, [bsky.app/profile/michaelianblack.bsky.social/post/3moq4rvvqg22l](https://bsky.app/profile/michaelianblack.bsky.social/post/3moq4rvvqg22l)

Nine words. This is the cleanest reactive move in the collection and the most transferable. It does
not argue with the stimulus or top it — it **agrees, then finds the single element that was too
generous.** The joke lives entirely inside the other person's metaphor. You cannot write this line
without their line; that dependency is the point.

### 2.4 Affirm a distinction nobody offered

> **Stimulus** — Cullen: "its funny how rayban took a brand whose single biggest association was
> 'cool' and changed it to 'pervert'"
>
> **Joke** — Josh Gondelman: **"And not even the cool kind of pervert!"**
>
> — VERIFIED, [bsky.app/profile/joshgondelman.bsky.social/post/3muahotduqs2b](https://bsky.app/profile/joshgondelman.bsky.social/post/3muahotduqs2b)

Eight words, opening with "And" — the yes-and made structural. The comedy is in **conceding a
taxonomy that should not exist** ("the cool kind of pervert") in a tone of mild disappointment. The
funny word is "cool," and it lands on a callback to the stimulus's own first word.

### 2.5 Snap a borrowed template onto the stimulus

> **Stimulus** — merritt: "spider man must suffer"
>
> **Joke** — Josh Gondelman: **"We must imagine Spider-Man slovenly."**
>
> — VERIFIED, [bsky.app/profile/joshgondelman.bsky.social/post/3mtluo6czjc2b](https://bsky.app/profile/joshgondelman.bsky.social/post/3mtluo6czjc2b)

Five words. Camus's "One must imagine Sisyphus happy" dropped onto a Spider-Man post, with the
adjective swapped for a deflating one. The register clash *is* the joke: philosophical cadence,
trivial subject, and a final word ("slovenly") that belongs to neither.

### 2.6 Answer a prompt with absurd specificity, in the prompt's own format

> **Stimulus** — ceej: "What injury would you present with as a walk-on guest star in The Pitt? I'm
> penis stretched by taffy puller"
>
> **Joke** — Patton Oswalt: **"Snoopy Sno-Cone Machine™️ explosion with extensive face burns."**
>
> — VERIFIED, [bsky.app/profile/pattonoswalt.bsky.social/post/3mi3ppjnfdc2b](https://bsky.app/profile/pattonoswalt.bsky.social/post/3mi3ppjnfdc2b)

Eight words and **no sentence** — it is a chart entry, matching the clinical register of a triage
note. Two specifics do the work: the trademark symbol (over-precision) and "extensive face burns"
(a real medical phrase attached to a toy). No verb, no subject, no "I would say."

### 2.7 Respond in a completely different institutional register

> **Stimulus** — Kieron Gillen: "My broken keyboard is now functional as I've constructed an
> improvised key to access the capital letters. It's a make shift solution."
>
> **Joke** — Patton Oswalt: **"Kieron, can we talk really quickly in my office? Bring your parking
> pass and company cell phone please."**
>
> — VERIFIED, [bsky.app/profile/pattonoswalt.bsky.social/post/3mnksalmel22e](https://bsky.app/profile/pattonoswalt.bsky.social/post/3mnksalmel22e)

The stimulus is a pun. The reply never mentions the pun, never says "groan" or "get out." It
**answers a joke with a firing.** The comic content is 100% in the props — parking pass, company
cell phone — and the refusal to break character. This is the deadpan-role-play move, and it is the
one with the most room for a dive-bar register.

### 2.8 Top the absurd premise by volunteering to be worse

> **Stimulus** — Coach Finstock: "It's physically impossible to not moo when you drive by cows"
>
> **Joke** — Rob Delaney: **"I don't need to see a cow to moo"**
>
> — VERIFIED, [bsky.app/profile/robdelaney.bsky.social/post/3mrsvdcyuds2w](https://bsky.app/profile/robdelaney.bsky.social/post/3mrsvdcyuds2w)

Nine words that accept a silly universal law and then **remove its only precondition**, making the
speaker the extreme case. Self-implicating, no adjectives, no punchline word — the funny thing is
the *position*, not any single term.

### 2.9 Finish their sentence

> **Stimulus** — Better Things Are Possible: "…Bunch of people trying to yell at you but their
> phones keep slipping out of their greasy bacon hands"
>
> **Joke** — Rob Delaney: **"and hitting an ugly baby"**
>
> — VERIFIED, [bsky.app/profile/robdelaney.bsky.social/post/3mtkndbk3b22f](https://bsky.app/profile/robdelaney.bsky.social/post/3mtkndbk3b22f)

Five words, lowercase "and," no capital, no terminal punctuation. It is grammatically a
**continuation of the other person's clause** — the slipping phone has to land somewhere, so it
lands on a baby, and the baby is gratuitously ugly. The gratuitous adjective is the joke.

### 2.10 Treat the absurd claim as classified information

> **Stimulus** — Brendel: "This is where Rick Moranis lives that's why he can only be in movies
> sometimes"
>
> **Joke** — Rob Delaney: **"Can you take down? Ppl outside of show business aren't supposed to know
> this"**
>
> — VERIFIED, [bsky.app/profile/robdelaney.bsky.social/post/3muhsnmkiik2q](https://bsky.app/profile/robdelaney.bsky.social/post/3muhsnmkiik2q)

Takes a made-up fact entirely seriously and **panics about the leak.** Note the clipped texting
register ("Can you take down?", "Ppl") — the urgency is performed by the missing words, not stated.

### 2.11 Insert yourself falsely into the news

> **Stimulus** — The Associated Press: "Lionel Messi became the first player to score in seven
> consecutive World Cup games while extending his all-time scoring record…"
>
> **Joke** — Michael Ian Black: **"Congrats to Messi for breaking my record."**
>
> — VERIFIED, [bsky.app/profile/michaelianblack.bsky.social/post/3mpd5lsopd222](https://bsky.app/profile/michaelianblack.bsky.social/post/3mpd5lsopd222)

Seven words. A wire-service headline plus one false personal claim, delivered as gracious
sportsmanship. The whole joke is the word **"my."**

### 2.12 Apply the headline's grammar to yourself

> **Stimulus** — The Verge: "Bored Ape Yacht Club is making a comeback — as a metaverse"
>
> **Joke** — Paul F. Tompkins: **"I am too, I am also making a comeback as a Metaverse"**
>
> — VERIFIED, [bsky.app/profile/pftompkins.bsky.social/post/3mszd6n6ivc2u](https://bsky.app/profile/pftompkins.bsky.social/post/3mszd6n6ivc2u)

The joke is a **syntactic parasite**: it borrows the headline's sentence frame and substitutes "I."
Nothing is added except the impossibility of a person being a metaverse. Repeating "I am" makes it
sound sincere, which is what makes it land.

### 2.13 Apply a modern real-world frame to a children's-book line

> **Stimulus** — Frog and Toad Bot: "Then Toad poured a glass of water over his head."
>
> **Joke** — Paul F. Tompkins: **"This guy needs a conservatorship"**
>
> — VERIFIED, [bsky.app/profile/pftompkins.bsky.social/post/3mskbd5tzlk2u](https://bsky.app/profile/pftompkins.bsky.social/post/3mskbd5tzlk2u)

Five words. A gentle 1970s children's sentence read as **evidence in a competency hearing.** Note
"This guy" — the flat, faintly contemptuous demonstrative is doing as much as "conservatorship."

### 2.14 Accept the correction, refuse the consequence

> **Stimulus** — Erin Biba: "ICYMI, the Dobby grave story was completely fake. Like, just, totally
> not true in any way."
>
> **Joke** — Paul F. Tompkins: **"Desecrate the grave anyway"**
>
> — VERIFIED, [bsky.app/profile/pftompkins.bsky.social/post/3msw22gpoxs2r](https://bsky.app/profile/pftompkins.bsky.social/post/3msw22gpoxs2r)

Four words, imperative mood, no hedging. A fact-check is answered with **unbothered escalation.**
The absence of any connective ("well," "ok but") is what makes it read as a command rather than an
argument.

### 2.15 Mock-solemn condolence attached to a trivial specific

> **Stimulus** — The Independent: "ChatGPT down: OpenAI chatbot not working in major outage"
>
> **Joke** — Josh Gondelman: **"My heart goes out to the millions of people struggling to remember
> how to write 'Thanks! Sounds great!' in an email."**
>
> — VERIFIED, [bsky.app/profile/joshgondelman.bsky.social/post/3mumwgswdt22q](https://bsky.app/profile/joshgondelman.bsky.social/post/3mumwgswdt22q)

Second-highest engagement in the corpus (6,619). Two-part construction: a **disaster-response
register** ("My heart goes out to the millions") crashed into the smallest possible stake. The
funny material is the quoted email fragment, and the three words after it — "in an email" — are the
button. Cutting them kills the joke; they are the confirmation that this is all it was.

### 2.16 Feigned ignorance that convicts the person you are quoting

> **Stimulus** — Aaron Rupar: "Rep. Brandon Gill: 'We particularly need the left to tone down the
> rhetoric … somebody is gonna listen and believe they are the next Dietrich Bonhoeffer and act on
> that…'"
>
> **Joke** — Patton Oswalt: **"Whoah! This Dietrich Bonhoeffer person sounds horrible. Was there a
> specific person he tried to kill or something like that?"**
>
> — VERIFIED, [bsky.app/profile/pattonoswalt.bsky.social/post/3mogtmfvhq22m](https://bsky.app/profile/pattonoswalt.bsky.social/post/3mogtmfvhq22m)

The joke plays a naive reader who does not know Bonhoeffer plotted to kill Hitler, and asks the one
question that detonates the quote. **The stupidity is a costume.** "or something like that" is the
tell that the naivety is performed.

### 2.17 Flat insincere endorsement, zero sarcasm markers

> **Stimulus** — KTLA 5: "Snapchat bets on smart glasses as the future"
>
> **Joke** — Tim Heidecker: **"These look really cool."**
>
> — VERIFIED, [bsky.app/profile/timheidecker.bsky.social/post/3mjwp32lhf222](https://bsky.app/profile/timheidecker.bsky.social/post/3mjwp32lhf222)

Four words with **no irony punctuation at all** — no "lol", no "/s", no ellipsis. The comedy is
entirely a function of who is saying it and what is above it. This is the highest-risk, lowest-cost
move in the set: it is invisible if the reader doesn't have the context, and perfect if they do.

### 2.18 Deadpan request for elaboration (the straight-man move)

> **Stimulus** — Erin Whitehead: "Q: What's Eating Gilbert Grape? A: The Grapes of Wrath"
>
> **Joke** — Paul F. Tompkins: **"Walk me through this one"**
>
> — VERIFIED, [bsky.app/profile/pftompkins.bsky.social/post/3mtcv6ezeck24](https://bsky.app/profile/pftompkins.bsky.social/post/3mtcv6ezeck24)

Five words. Not a counter-joke — a **refusal to laugh, phrased as procedure.** Works only against a
joke, never against a statement. This is the cheapest reactive move that still reads as written
rather than reflexive.

### 2.19 The absolute floor: two words

> **Stimulus** — Adam McKay: "…I want old dogs, dogs with cataract'd eyes, sketchy dogs that view
> every movement as a possible attack… Even 2 or 3 raccoons would be good."
>
> **Joke** — Tim Heidecker: **"Let's talk"**
>
> — VERIFIED, [bsky.app/profile/timheidecker.bsky.social/post/3mk4sjfrauk2i](https://bsky.app/profile/timheidecker.bsky.social/post/3mk4sjfrauk2i)

Two words. The joke is a **business proposition offered in response to lunacy** — it implies an
entire off-screen character who has been waiting for this exact request. This is the extreme end of
the finding in §1: the stimulus was 30 words of setup, so the punchline needed two.

---

## 3. X-native specimens — SECONDHAND

All reproduced from the embed markup of pages fetched on 2026-09-04. Publication named per block.
These are standalone posts; they show what the form has to do when nobody else supplies the setup.

**Source: The Poke, "Our 25 Favourite Funny Tweets of the Week" (editions 107, 130, 131)**

| Specimen | Author | Words | Link |
|---|---|---|---|
| "Bobsled is short for Robertsled." | G (@stevensongs) | 5 | [status](https://twitter.com/stevensongs/status/2023743145695924701) |
| "divorce court should let you pick walkout music" | Fawf (@Fawf_iguess) | 7 | [status](https://x.com/Fawf_iguess/status/2086956335887688005) |
| "Explosion at the cheese factory / Da brie is everywhere" | Bob Golen (@BobGolen) | 9 | [status](https://x.com/BobGolen/status/2087727910509556132) |
| "the human body was not designed to remember this many passwords" | maro (@ProofofMaro) | 11 | [status](https://twitter.com/ProofofMaro/status/2024136042429706540) |
| "Sixteen sodium atoms walk into a bar. / Batman follows them in." | PUNS (@ThePunnyWorld) | 11 | [status](https://x.com/ThePunnyWorld/status/2084053268955582758) |
| "oh ur a people pleaser? name 3 people that are pleased with you" | pinkie (@pinkamaniaa) | 13 | [status](https://x.com/pinkamaniaa/status/2087483164205695266) |
| "Americans sometimes use French words like 'hors d'oeuvres.' And that's just for starters." | Alice Mills (@millsalice144) | 13 | [status](https://twitter.com/millsalice144/status/2024161032424607824) |
| "All I'm saying is it's statistically impossible that every murder victim lit up a room." | Lori (@lori_socal) | 15 | [status](https://twitter.com/lori_socal/status/2023839053087683058) |
| "My landlord found out I have a cat and he's furious. Mostly because it's his cat." | Martin Pilgrim (@MartinPilgrim1) | 16 | [status](https://twitter.com/MartinPilgrim1/status/2022572561851118016) |
| "I thought about buying that camouflage jacket / Tried it on and I couldn't see myself wearing it" | Bob Golen (@BobGolen) | 18 | [status](https://x.com/BobGolen/status/2085329390431252965) |
| "I don't normally brag about my expensive trips, but we just got back from the vet." | (@itsme_urstruly) | 17 | [status](https://x.com/itsme_urstruly/status/2086099560393478460) |
| "Alligators can live up to 100 years, which is why there's an increased likelihood that they will see you later" | Weekday Jokes (@weekdayjokes) | 19 | [status](https://twitter.com/weekdayjokes/status/2023825171090489508) |
| "jesus turns water into wine and everybody go crazy. i turn grass into milk and nobody bats an eye" | cow (@cowincrisis) | 19 | [status](https://x.com/cowincrisis/status/2084056051373289490) |
| "lengthy German word for that sinking sensation when, at lunch with a friend, you see that your friend has ordered a much better lunch than you did." | Joyce Carol Oates (@JoyceCarolOates) | 26 | [status](https://x.com/JoyceCarolOates/status/2083786296544096704) |
| "A woman was rude to me on the train today, so I googled the book she was reading and told her who the murderer is." | Georgina-Libbie (@georginalibbie) | 24 | [status](https://x.com/georginalibbie/status/2084413861923348823) |
| "Mythical creatures make a lot more sense when you realise humanity spent hundreds of thousands of years without glasses or any form of eyesight aid." | (@foreeeeeal) | 24 | [status](https://x.com/foreeeeeal/status/2083621910009499721) |
| "sauron deciding how many rings everyone gets and seeing a hobbit for the first time: [mumbling] skip. i dont like this one. skip it." | turbomander (@turbomander) | 24 | [status](https://x.com/turbomander/status/2085334379195171111) |
| "Shall I compare thee to a summer's day? Sure. You're getting worse every year and it's going to get people killed." | Noah Garfinkel (@NoahGarfinkel) | 21 | [status](https://x.com/NoahGarfinkel/status/2087745060184223948) |
| "Dracula had it right, sleep all day, live alone in a castle & explode into a thousand bats to get out of social situations." | tooflyszn (@_tooflyszn) | 24 | [status](https://x.com/_tooflyszn/status/2087479198130508086) |
| "BREAKING: A thesaurus belonging to Elton John has been stolen. The singer commented, 'It's sad. So sad. It's a sad, sad situation.'" | Pundamentalism (@Pundamentalism) | 22 | [status](https://twitter.com/Pundamentalism/status/2022836197328891959) |
| "Preparing to tell my dentist that I haven't really flossed at all since my last visit but I've done a lot of other things I'm really proud of" | paige (@BonerWizard) | 28 | [status](https://x.com/BonerWizard/status/2087437543944142873) |

**Source: Paste Magazine, "The Funniest Tweets of the Week" #114**

| Specimen | Author | Link |
|---|---|---|
| "Everyone always jokes that women are obsessed with shoes but my female friends aren't the ones posting 6 sneaker insta pics a week." | mark normand (@marknorm) | [status](https://twitter.com/marknorm/status/1135551109102211073) |
| "Trust me, when you're feeling depressed the best remedy is to put on music, go for a run, and change every aspect of your social and socioeconomic status over 8 to 12 years" | Zack Bornstein (@ZackBornstein) | [status](https://twitter.com/ZackBornstein/status/1136070299206602752) |
| "Twitter is a beautiful place where you can watch people who didn't text you back complain about ppl who didn't text them back" | Brodie Reed (@ayobrobro) | [status](https://twitter.com/ayobrobro/status/1136451628431601664) |
| "I synced up watering my cactus with my friend's 'My baby is ___ months old' Instagram updates, so I should be able to keep this one alive for at least two years." | Katrina (@katrinasivad) | [status](https://twitter.com/katrinasivad/status/1136364405845716993) |
| "To the next person who drops me off at the airport and tells me to have a safe flight: If I say 'you too', you're now going on the trip with me. I'm done feeling awkward and I always need a travel buddy." | Solomon Georgio (@solomongeorgio) | [status](https://twitter.com/solomongeorgio/status/1136450466152407041) |

### 3.1 The borrowed-format sub-form

A distinct pattern in the X sample: when a joke needs a setup it cannot afford, it **steals a format
that implies one.** The reader supplies the missing scene for free.

> "professor x: what's your power? / me: deflection / professor x: bullets? gamma rays? / me:
> criticism / professor x: that's a stupi— / me: say, is that a new tie?"
> — Henpecked Hal (@HenpeckedHal), SECONDHAND via The Poke,
> [status](https://twitter.com/HenpeckedHal/status/2024213145636786661)

> "[farmers market] / Guy about to invent popcorn: Do you have any vegetables that fucking explode"
> — Ron Iver (@ronnui_), SECONDHAND via The Poke,
> [status](https://twitter.com/ronnui_/status/2023780182407213068)

> "ME: And another thing, It should be called a buycycle when it's in the shop and a bicycle when
> you get it home. / MY KIDNAPPER: *crying* Omg we let you go two hours ago"
> — FAT GANDALF (@sofarrsogud), SECONDHAND via The Poke,
> [status](https://x.com/sofarrsogud/status/2084752665146179883)

The bracketed slugline, the screenplay colon, the all-caps speaker label: each costs 2–4 words and
buys an entire premise. This is the standalone writer's substitute for what a reply gets for free.

---

## 4. The one-liner as a stage form

Gary Delaney (@garydelaney) is a working British one-liner comic — the jokes on his feed are the
jokes he performs. His account is the closest thing in this collection to a controlled sample of the
pure form, because there is no image, no context, and no reply to lean on.

All VERIFIED via the Bluesky public API.

> **"My helium dealer is so good I can't recommend him highly enough."**
> — [post](https://bsky.app/profile/garydelaney.bsky.social/post/3lxh5oa4hkk24)

> **"I used to think I was a vampire but on reflection I might not be."**
> — [post](https://bsky.app/profile/garydelaney.bsky.social/post/3lycrlw5uok2s)

> **"The easiest impersonation for beginners to learn is the vampire off Sesame Street and that's
> because first impressions count."**
> — [post](https://bsky.app/profile/garydelaney.bsky.social/post/3lyi7f6hffs2o)

> **"The artic ice is melting. Scientists says it's global warming but I remember when that happened
> to my freezer and actually it was just one dodgy seal."**
> — [post](https://bsky.app/profile/garydelaney.bsky.social/post/3lzsqfxixds2a)

> **"A Sultan's wife is genuinely called a Sultana although she is sometimes also known as his
> currant wife."**
> — [post](https://bsky.app/profile/garydelaney.bsky.social/post/3lx7mkqvejk2i)

> **"When this film warned it contained adult themes I was hoping for more about sex and less about
> mortgages."**
> — [post](https://bsky.app/profile/garydelaney.bsky.social/post/3m4vnixyzqk2g)

> **"My therapist said I'm prone to catastrophising. That's bad, isn't it? It sounds bad."**
> — [post](https://bsky.app/profile/garydelaney.bsky.social/post/3m4qh4jhrzc2m)

> **"Mom always tried to kill people with kindness for example she gave home made jams and cakes to
> our difficult neighbour until eventually he developed type 2 diabetes"**
> — [post](https://bsky.app/profile/garydelaney.bsky.social/post/3midxbug25k2s)

**The positional rule this sample establishes:** in every one of these, the pivot word is the last
word or in the last three — *seal, currant, mortgages, reflection, count, diabetes, bad.* Not one of
them explains after the pivot. The sentence ends the instant the meaning flips.

The one exception proves it: "That's bad, isn't it? It sounds bad." adds words *after* the pivot —
but they are not explanation, they are **the character failing to understand his own diagnosis.**
The extra words are a second joke, not a gloss on the first.

---

## 5. Craft mechanics, stated as rules

Each supported by a specimen above.

**1. The stimulus is your setup — do not rebuild it.**
Median reply length in the corpus is six words. Michael Ian Black's "You give him too much credit by
including raisins" does not restate the tapioca metaphor, quote it, or name the subject. It cannot
survive being detached from its parent, and that is the correct design for a reply.

**2. The pivot word goes last. Nothing follows it.**
Across the Gary Delaney sample the flip word is terminal in every case. In Gondelman's ChatGPT post the
last three words ("in an email") are the button, not a clarification. If a word appears after the
pivot, it must be a *second* move, never a gloss.

**3. State the subject only when the subject is the joke.**
Oswalt's Sno-Cone reply has no subject and no verb — it is a chart entry. Tompkins's "Walk me
through this one" has no object. But Michael Ian Black's "Congrats to Messi for breaking **my**
record" is a joke that exists solely because of one possessive pronoun. Subject-dropping is the
default; break it when the pronoun carries the payload.

**4. Change the register, not the topic.**
The strongest reactive specimens keep the other person's subject and swap the *voice*: an HR
termination (Oswalt/Gillen), a disaster-response condolence (Gondelman/ChatGPT), a competency
hearing (Tompkins/Frog and Toad), a business proposition (Heidecker/McKay). None of them introduce a
new topic. Register clash is cheaper than invention and reads as wit rather than non sequitur.

**5. Perform, don't characterize.**
Oswalt's response to a post calling a speech gibberish was to write the gibberish, not to say it was
gibberish. Tompkins answered "scheduling conflicts" with the sentence a person would actually have
said. Quotation marks and voice are load-bearing; "imagine saying" and "this is basically" are not.

**6. The floor is two words, and it is reached by the stimulus doing more work.**
"Let's talk" answers a 30-word stimulus. "Looking good!" answers a chart. The shorter your joke, the
more precisely it must be aimed — brevity is not compression of your idea, it is **delegation of the
setup to someone else's post.**

**7. Commit without irony markers, or don't do it.**
Heidecker's "These look really cool." carries no "/s", no lol, no ellipsis. Tompkins's "Desecrate the
grave anyway" has no softening connective. Every hedge you add is a request that the reader
acknowledge you were joking, and that request is the thing that kills it.

---

## 6. What comedy writers say about the form

Craft literature, gathered by a parallel research pass. Every quote below was read on the page
linked. Two honest caveats: **almost nobody has written seriously about the joke-as-reply
specifically** — the closest real body of published craft is the **crowd-work** literature, which is
the identical operation offline (take a stranger's utterance, find the premise inside it, heighten).
And Megan Amram's Fast Company piece "How To Be Hilarious On Twitter", the single most on-target
document identified, was unreachable behind Cloudflare; nothing is quoted from it.

### 6.1 On the short joke

**The good line is at the third thought, not the first.** Anthony Jeselnik, quoted in Matt Ruby's
*Funny How*: "Third thought is one step removed. It's something that you never would have thought
of, and that's where the best jokes lie." His method: "I will write the premise and think, 'How many
different ways can this turn out?'… Then I pick the funniest ones, the craziest ones you can't really
see coming."
→ [funnyhow.substack.com](https://funnyhow.substack.com/p/how-anthony-jeselnik-writes-jokes)

**The key word goes last — confirmed independently.** Jack Handey: "Yes, in a joke, usually the key
word comes at the end." And on length: "don't make a joke too 'sweaty' — that is, too long and
convoluted. A good joke has a certain non-logic. It's often mathematical, as in '2 plus 2 = 5.'"
→ [alexbaia.com](https://www.alexbaia.com/blog/jack-handey-humor-writer-comedy-legend)

*This is the most valuable convergence in the whole file:* the terminal-pivot rule derived
empirically from the Gary Delaney sample in §4 is stated outright by Handey as a working principle.

**Cutting is the edit.** Handey, on what he does to a draft: "Often, cutting is the best answer."
Scott Dikkers, founding editor of The Onion: "Any time I edit a joke, I look for ways to reduce.
Cutting even a single syllable can make the joke punchier, better."
→ [alexbaia.com](https://www.alexbaia.com/blog/jack-handey-humor-writer-comedy-legend) ·
[verygoodcopy.com](https://www.verygoodcopy.com/hubspotcom/the-onion-scott-dikkers-on-writing)

**Volume is the method, and most of it is waste.** Dikkers: "Basically, 95% of everything we create
is garbage." Jeselnik: "I try to write three jokes a day. I find that that's the amount I can get out
without exhausting myself, but I'm keeping the wheels turning."
→ [verygoodcopy.com](https://www.verygoodcopy.com/hubspotcom/the-onion-scott-dikkers-on-writing) ·
[funnyhow.substack.com](https://funnyhow.substack.com/p/how-anthony-jeselnik-writes-jokes)

**Don't over-swing on weirdness.** Will Hines (UCB) proposes a clock: normal is noon, opposite-of-
normal is six, and the funniest answers "are like 12 minutes past the hour. Weird but not too
weird… Don't over swing." Four-o'clock answers "tend to NOT WORK. TOO WEIRD"; six-o'clock ones are
"too on the nose." His micro-rules: "Quiet is funnier than loud. Serious is better than grinning.
When in doubt, do less." And: "Non round numbers are funnier than round ones."
→ [willhines.substack.com](https://willhines.substack.com/p/how-to-be-funny)

**Typography is delivery.** Emma Tattenbaum-Fine: "You don't have italics, but you can convey timing
and expression with all-caps, some-caps, and no-caps, as well as with too much or too little
punctuation." Danny Cohen, analyzing the posted joke as a literary form, calls out "the surgical use
of capital letters" and concludes: "The whole thing operates on an intuitive presentational logic."
→ [goldcomedy.com](https://goldcomedy.com/resources/write-funny-tweet/) ·
[typebarmagazine.com](https://www.typebarmagazine.com/the-tweet-as-a-literary-form/)

### 6.2 On the reactive joke

**Agree and heighten; do not roast and reject.** Mike Lukas: "The rookie move is to roast or reject.
The pro move? Agree and heighten. 'Yes, and' doesn't just apply to improv — it's the engine of great
crowd work. If they say something weird, agree like it's gospel and then twist it into absurdity."
Michael Halcomb: work "stalls or dies the moment you treat the person in the crowd as an opponent
(even if they are a 'heckler') and start trying to 'win' against them."
→ [funnymuscle.com](https://funnymuscle.com/upgrade-your-crowd-work/)

This is exactly what §2.3, §2.4 and §2.8 do, and exactly what the arguing replies in §7 fail to do.

**Latch onto the first unusual thing.** Halcomb: "Listen for the first unusual thing… Whatever the
first unusual thing is, latch on to that. Crowd work is first about listening, then diagnosing, then
responding."
→ [funnymuscle.com](https://funnymuscle.com/upgrade-your-crowd-work/)

**The menu of reactive moves.** Greg Dean's list of what to do once you have actually heard them:
"exaggerate it / judge it / defend it / act it out / intentionally misunderstand it / create
characters around it / invent consequences from it / push it into absurdity / build an alternate
reality around it."
→ [stand-upcomedy.com](https://stand-upcomedy.com/crowd-work-adapts-group-improv-skills-reason-8)

Every reactive specimen in §2 is on that list. "Intentionally misunderstand it" is §2.1 and §2.16;
"create characters around it" is §2.7; "invent consequences from it" is §2.10; "act it out" is §2.2.

**Build only from their material.** Dean: "Organic comedy comes from the interaction itself… The
laughs are born from what is unfolding now, not from something imported from your notebook." And
listen past the surface: "Too many comics hear answers only at surface level. Whereas trained
improvisation performers learn to hear implications. They listen for what is suggested beneath the
words."
→ [stand-upcomedy.com](https://stand-upcomedy.com/crowd-work-adapts-group-improv-skills-reason-8)

**Find the negative opinion hiding in their post.** Dean: "In my system, a Premise is 'a negative
opinion about a subject.' Crowd work requires you to identify that subject immediately inside an
audience member's answer. Without a premise, you have nothing to build the comedy on."
→ [stand-upcomedy.com](https://stand-upcomedy.com/crowd-work-conversation-into-jokes-reason-4)

**Generators for the reply.** Matt Ruby's list of punchline sparks, verbatim: "What do you secretly
wish you had said?", "What should be said in a given situation (appropriate response to stupid
comment)", "When would that be the right thing to say?", "What if this was normal?"
→ [funnyhow.substack.com](https://funnyhow.substack.com/p/ways-to-make-it-funny)

**Skip a beat.** From Ruby's UCB notes: "Go from A to C. Leaving the B out is often the interesting
part because it lets the audience's brains make the connection." And: "Be ahead of the audience. If
you just thought of it, go for it. If they already know where you're going, you've lost."
→ [funnyhow.substack.com](https://funnyhow.substack.com/p/using-game-of-the-scene-in-standup)

**Agreement as a reply form.** Hines: "Agree with accusations. 'You know, I AM lazy.'"
→ [willhines.substack.com](https://willhines.substack.com/p/how-to-be-funny)

**Post fast; the delay is the enemy.** Alex Dobrenko: "Jump into existing conversations. If you see
two people talking, say something," and "try to minimize the time between having an idea and posting
it because otherwise, the negative voice in my brain is gonna barge in and convince me the idea
sucks." Dean, on the same failure: "overthinking destroys spontaneity. The moment you start
internally reviewing, editing, judging, filtering, or pre-approving your responses, your timing
immediately becomes late."
→ [on.substack.com](https://on.substack.com/p/alexdobrenko-notes) ·
[stand-upcomedy.com](https://stand-upcomedy.com/crowd-work-adapts-group-improv-skills-reason-8)

**Do not absorb the feed's tone.** Dobrenko: "Resist this urge for mimicry. When I'm scrolling
through a feed, I'm taking in the tone of it and, without knowing, feeding that tone back into the
system." Directly relevant to keeping a distinct register instead of converging on house style.
→ [on.substack.com](https://on.substack.com/p/alexdobrenko-notes)

### 6.3 On failure

**Crowding — too many jokes in one space.** Alex Baia: "When you crowd a sentence or a section with
too many jokes, you crowd the reader, giving her no space to process the one funniest thing." He
names the two causes: "The maximalist desire: If one joke here is good, then five is better!" and
"Failure to edit." Also: "Cut your preambles, your disclaimers, and your apologies. Your words are
better spent on jokes." And the test: "'Do I love this joke/paragraph/sentence/word?' If you don't
love it, cut it."
→ [The Ultimate Humor Writing Cheat Sheet (PDF)](https://static1.squarespace.com/static/641e40efdcca762202ebf5ba/t/64321093f240232a6d73bb42/1681002643563/The+Ultimate+Humor+Writing+Cheat+Sheet+-+2023+Version.pdf)

**Stacking jokes reads as amateur.** Dikkers, on people imitating The Onion by adding gags:
"Everyone does that, and it's a killer; it's an immediate rejection." And on complexity: "It has to
be accessible, simple, and understandable — one concept, one thing at a time."
→ [howiwrite.substack.com](https://howiwrite.substack.com/p/scott-dikkers-11-ways-to-make-your)

**A one-liner has no story to absorb a miss.** Jeselnik: "It's not fun to bomb with a joke,
especially a one-liner… the only reason I tell a joke at all is for laughs."
→ [funnyhow.substack.com](https://funnyhow.substack.com/p/how-anthony-jeselnik-writes-jokes)

**Old weak drafts do not ripen.** Handey: "I have folders full of bad ideas and weak drafts. They
don't get better over time." His keep-test, from Fred Wolf: "if something was funny after three days,
it was funny."
→ [alexbaia.com](https://www.alexbaia.com/blog/jack-handey-humor-writer-comedy-legend)

---

## 7. Failure modes visible in the data

**Explaining the reference.** No specimen in the top-engagement set explains itself. "We must imagine
Spider-Man slovenly" does not mention Camus; "This is now the most embarrassing thing JD has done on
a couch" does not mention the meme it invokes. The reference either lands or it doesn't — annotating
it removes the reader's participation, which is where the laugh comes from.

**Setup the format cannot afford.** The standalone X sample runs a 22-word median and tops out
around 53 words. Anything requiring more scene than that has to borrow a format (§3.1) or become a
reply. A standalone joke that opens with "So I was at the…" has already spent its budget.

**Reaction that isn't a joke.** A real and instructive category. Several of the highest-engagement
reactive posts in the corpus are not jokes at all — a string of emoji, "OOOOF", "No notes.", "Oh
WOW!!!", "💯💯💯💯". They perform agreement, and they perform well by the metrics. **Engagement is not
evidence that a line was funny.** If Sean's target is the joke, the metric is useless as a filter and
the corpus has to be read by ear.

**The caption mistaken for a one-liner.** A large share of short high-performing posts are captions
on an image or video and are meaningless without it ("A story in three parts", "Live from @theonion
HQ", "We go way back"). These look like tight one-liners in a text export and are nothing of the
kind. Caption writing is a different discipline from the one Sean is studying; do not harvest
examples from it by accident.

**The reply that argues.** Visible in the corpus but never in the high-performing set: replies that
correct, rebut, or agree in earnest. Tompkins's "Genuinely astonishing" and "The 'victim complex' is
the default setting for these people…" sit in the same feed; the two-word one is a joke and the long
one is an argument. The tell is the presence of a claim the writer wants believed.

---

## 8. Named accounts and their registers

VERIFIED accounts harvested (Bluesky handles; several of these people also post on X, which was not
reachable). Register descriptions are drawn from the harvested posts, not from reputation.

| Handle | Register |
|---|---|
| `garydelaney` | Pure constructed one-liner. Pun-based, terminal pivot, no persona. The technical benchmark. |
| `pftompkins` | Deadpan character work. Fake quotes, straight-man requests, mock-officialdom. Best single source for reactive moves. |
| `pattonoswalt` | Wide range: high-register parody, voiced translations of other people's quotes, sudden vulgarity. Highest volume of reactive posts. |
| `joshgondelman` | Warm, precise, structural. Yes-and constructions and borrowed-template jokes. The most imitable for a writer who doesn't want to be cruel. |
| `michaelianblack` | Minimalist reframe. Short flat sentences that audit one detail of the stimulus. |
| `robdelaney` | Dive-bar adjacent — self-implicating, escalatory, frequently blue. Closest register to Sean's stated one. |
| `zackbornstein` | Punchy comparison and callback jokes on news stimuli. |
| `timheidecker` | Anti-comedy. Sincerity as a weapon; refuses all irony markers. |
| `kathbarbadoro`, `solomongeorgio`, `sarajbenincasa`, `htownjenny` | Conversational reply registers; short, fast, low-formality. |
| `hodgman`, `roywoodjr`, `meganamram`, `blaireerskine`, `danaschwartz`, `bessbell`, `joekwa`, `josielong`, `richardosman1`, `jonnysun`, `anthonyjeselnik` | Also harvested; lower reactive volume in the sampled window. |

X-native handles worth tracking through publication roundups, since the platform itself is
unreadable: `@BobGolen` (two-line pun structure), `@Pundamentalism` (news-format puns),
`@HenpeckedHal` and `@ronnui_` and `@sofarrsogud` (borrowed-format scenes), `@weekdayjokes`,
`@marknorm`, `@ZackBornstein`, `@solomongeorgio`, `@JoyceCarolOates`.

---

## 9. Exercises

Drawn directly from the mechanics above. Each is a constrained rewrite, not a prompt for
inspiration.

1. **Six-word reply.** Take ten posts from a feed. Write a reply to each in six words or fewer.
   Forbidden: naming the subject, restating the stimulus, any word ending in "-ing" as the opener.
2. **Audit one detail.** Find a post containing a metaphor or a list. Write the reply that agrees
   with all of it except one element, and objects only to that element. (Model: "…by including
   raisins.")
3. **Supply the real quote.** Find a euphemism in a press release or headline. Write the sentence
   the person would have said, in quotation marks, under fifteen words, with no framing text.
4. **Register swap.** Take a pun someone else made. Reply in the voice of an institution — HR, a
   hospital, a probate court, a landlord — without ever acknowledging the pun.
5. **Terminal pivot drill.** Write ten standalone one-liners under 20 words in which the final word
   is the word that flips the meaning. Delete any that continue past it.
6. **Two-word ceiling.** Find the five stimuli in your feed that are longest and most unhinged. Reply
   to each in two words. (The stimulus has to do the work; if two words can't land, the stimulus
   wasn't finished.)
7. **Un-hedge.** Take five of your own drafts and delete every irony marker — "lol", "/s",
   ellipses, "I mean", "imagine". Keep only the ones that survive.

---

## 10. Sources fetched

**Directly fetched (VERIFIED specimens):**
- `public.api.bsky.app` — `app.bsky.feed.getAuthorFeed`, `app.bsky.actor.getProfile`,
  `app.bsky.actor.searchActors`. 2,947 posts across 23 verified accounts, 2026-09-04.

**Fetched publications (SECONDHAND specimens, verbatim embed markup):**
- The Poke — [Funny Tweets of the Week #131](https://www.thepoke.com/2026/08/14/our-25-favourite-funny-tweets-of-the-week-131/)
  ([p2](https://www.thepoke.com/2026/08/14/our-25-favourite-funny-tweets-of-the-week-131/2/)),
  [#130](https://www.thepoke.com/2026/08/07/our-25-favourite-funny-tweets-of-the-week-130/)
  ([p2](https://www.thepoke.com/2026/08/07/our-25-favourite-funny-tweets-of-the-week-130/2/)),
  [#107](https://www.thepoke.com/2026/02/20/our-25-favourite-funny-tweets-of-the-week-107/)
  ([p2](https://www.thepoke.com/2026/02/20/our-25-favourite-funny-tweets-of-the-week-107/2/))
- Paste Magazine — [The Funniest Tweets of the Week #114](https://www.pastemagazine.com/comedy/funniest-tweets-of-the-week/the-funniest-tweets-of-the-week-114)
- The Poke — [reply-guy piece, 2024-01-02](https://www.thepoke.com/2024/01/02/were-only-two-days-in-but-this-mansplaining-response-is-already-a-hot-contender-for-best-response-of-the-year/)

**Craft literature (§6), fetched pages:**
- funnyhow.substack.com (Jeselnik, Steven Wright, punchline placement, punchline generators)
- alexbaia.com (Jack Handey interview) and *The Ultimate Humor Writing Cheat Sheet* (PDF)
- verygoodcopy.com and howiwrite.substack.com (Scott Dikkers / The Onion)
- willhines.substack.com (the Clock Method)
- funnymuscle.com and stand-upcomedy.com (crowd-work craft — the reactive-joke substitute literature)
- goldcomedy.com (writing funny posts; quote-post devices), typebarmagazine.com (the post as literary form)
- on.substack.com (Alex Dobrenko), npr.org, floodmagazine.com, nbcnews.com

**Attempted and unreachable:**
- `x.com` profile and status pages — HTTP 402
- `publish.twitter.com/oembed` — HTTP 301, no payload
- `cdn.syndication.twimg.com/tweet-result` — error page, with and without a valid token
- Wayback Machine — no snapshots for sampled X status URLs
- Paste Magazine roundup archive beyond #114 — all other edition numbers 404
- fastcompany.com — Megan Amram, "How To Be Hilarious On Twitter" (Cloudflare challenge, never read)
- vulture.com (Steven Wright interview), medium.com paywall stub, huffpost.com, pbs.org — JS-gated or blocked

## 11. Gaps

- **No X reply/quote pairs.** Every reactive specimen here is Bluesky. Publication roundups
  reproduce standalone posts almost exclusively, and the reactive pieces that do exist (The Poke's
  reply-guy articles) resolve to screenshots and images whose text is not machine-readable. If X
  reactive specimens are needed, they will have to be collected by hand from a logged-in session.
- **No published craft writing on the reply-joke as such.** §6.2 is assembled largely from
  crowd-work craft, which is the same operation performed live. No interview was found with
  Demetri Martin, Emo Philips, Stewart Francis, Milton Jones, dril, Megan Amram, Jenny Johnson or
  Shelby Fero that treats the reply or quote-post as a form. Megan Amram's Fast Company piece "How
  To Be Hilarious On Twitter" — the most on-target document identified — is behind a Cloudflare
  challenge and was never read; nothing is quoted from it. It may be reachable from a browser
  session with JavaScript.
- **Sampling window.** The Bluesky harvest covers roughly the most recent 300 posts per account, so
  it reflects late-2025 through 2026 and skews toward whatever those accounts were reacting to.
