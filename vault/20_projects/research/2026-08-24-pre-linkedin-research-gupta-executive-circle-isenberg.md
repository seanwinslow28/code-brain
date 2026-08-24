---
title: "Pre-LinkedIn research — Gupta/Kubicka, Executive Circle, Isenberg"
date: 2026-08-24
project: content-machine
ticket: "https://github.com/seanwinslow28/code-brain/issues/170"
map: "https://github.com/seanwinslow28/code-brain/issues/158"
status: findings
tags: [research, content-machine, linkedin, professional-lane, syndication]
cost: $0 (local watch/Whisper-free captions + web + Executive Circle MCP; no paid research invoked)
---

# Pre-LinkedIn research — findings brief

Feeds the **LinkedIn contract only** (map [#158](https://github.com/seanwinslow28/code-brain/issues/158), lock L4: LinkedIn is a **syndication target**, never a native composition surface). Findings, not decisions — the contract ticket decides.

## Correction to the ticket's framing

The ticket names the video "Akash Gupta's video on AI-PM LinkedIn optimization." Two fixes:

- The name is **Aakash Gupta** (Product Growth podcast) and he is the **host**, not the source of the method.
- The method belongs to **Basia Kubicka**, the guest. Every framework below is hers; Gupta's contribution is interrogation and the takeaway summary in the video description.

Video: [She Gets 5 Job Offers a Week on LinkedIn with Claude Code](https://www.youtube.com/watch?v=TO3KhNfxvnA), published 2026-08-21, 92 minutes. A written companion exists at [aakashg.com](https://www.aakashg.com/how-to-get-inbound-job-offers-on-linkedin-as-a-pm/). Captions pulled natively (no Whisper spend); full deduped transcript reviewed, not just the summary page.

**Standing caveat on the whole primary source:** it is a founder-of-a-paid-cohort demonstrating her own system on a podcast that sells a bundle. The system's *artifacts* (LinkedIn's indexed fields, post anatomy, the three arrival paths) are checkable and several were independently verified below. The *results* (0→50k followers in six months, five inbound offers a week, cohort students seeing similar results by week five) are self-reported, single-subject, uncontrolled, and commercially motivated. Treat the mechanism as usable and the outcome numbers as unverified.

---

## Q1 — Which keywords does a recruiter search actually hit for an AI PM role?

### The finding: the question has no fixed answer, and that is the answer

The strongest result of this pass is a **negative** one. There is no stable, citable keyword list for "AI PM" worth encoding in a contract, and any contract that hardcodes one will be wrong within a quarter and wrong for any specific role today.

I ran the obvious search (`"AI product manager" job description most common keywords 2026`). Every result on page one was vendor SEO: interviewkickstart, futurense, secondtalent, interviewguy, kore1, nextinhr, rework. These are interview-prep sellers and job-description-template mills writing for search traffic, not employers describing what they screen on. **Flagged as vendor-marketing-shaped; not repeated as fact.** This is the exact failure mode CLAUDE.md documents for market-shaped queries — fresh marketing that recency filters cannot remove.

Kubicka's method sidesteps this entirely, and the sidestep is the transferable part:

**Derive the keyword set per-search from five real job descriptions with ≥75% keyword overlap.** Not five interesting roles — five *tightly clustered* roles. Her worked example used five API-platform PM postings (OpenAI API agents, API agentic, API developer platform, API/ML platform, APIs-and-applications) and hit ~80% coverage. The overlap threshold is a **diagnostic gate, not a target**: her skill halts and tells the operator to rethink what they are applying for if the five postings do not converge. Scattered postings produce a scattered profile because no unifying keyword set exists to write toward.

The stated purpose is not ATS gaming. It is that any hiring manager drawn from that cluster of five should read the profile and feel it was written for them.

### Where LinkedIn actually indexes keywords (verified against LinkedIn's own docs)

This is the one claim in the whole video I could check against a primary source, and it holds. Per [LinkedIn's Recruiter help center on Boolean search](https://www.linkedin.com/help/recruiter/answer/a415295):

- Keyword matches are highlighted on the **profile card**, the **Summary** (About) section, the **Experience** section — header, description, *and* location — and the **Skills** section.
- Supported Boolean operators: **AND**, **OR**, **NOT**. The `+` and `-` operators are **not** officially supported.
- Job titles, Location, Companies, Skills, Schools, Industries and Spoken languages also work as structured Boolean filters with must-have / can-have / doesn't-have.

LinkedIn's own talent-attraction material additionally weights the headline and About section most heavily ([How to Attract Recruiters Using Keywords](https://www.linkedin.com/top-content/recruitment-hr/talent-attraction-techniques/how-to-attract-recruiters-using-keywords/)) — first-party but marketing-adjacent, so weight it below the help-center page.

### The asymmetry that matters for a contract

The indexed fields do **not** all have the same tolerance for keyword density, and this is the single most contract-relevant thing in the research:

| Surface | Indexed? | Human-read? | Keyword-loading tolerance |
|---|---|---|---|
| Endorsable **Skills** section | Yes | Effectively no — nobody scrolls that far | **Unbounded.** Load every relevant keyword; volume is free here |
| Skills pinned **under an Experience entry** | Yes | Yes | **Low.** ~40 stacked under one job reads as gaming and actively damages the page |
| **Headline** / tagline | Yes | Yes — it is the highest-traffic element on the profile | **Capped by readability.** Kubicka rejected her own generated headline as too long on the first pass |
| **About** section | Yes, heavily weighted | Yes — but only the first three lines before "see more" | **Capped by the hook.** Keyword load must survive being skimmable |
| **Experience** descriptions | Yes | Yes | Medium — but the real constraint is results-over-responsibilities, below |
| **Banner** | **No** | Yes — first thing seen | Zero keyword value; pure persuasion surface |

The second contract-relevant rule is orthogonal to keywords: **experience entries should state what was delivered, with numbers, not what was owned.** Her profile-writer skill blocks on this — if the current profile lacks the quantities, it asks clarifying questions before writing anything rather than inventing them. That behaviour is the same shape as the Content Machine's L2 constitution, arrived at independently.

### Implication for the LinkedIn contract (not a decision)

The contract should probably own a *procedure* — mine five clustered JDs, gate on overlap, map keywords to verifiable claims, place them per the tolerance table — and should probably **not** own a keyword list. A hardcoded list is a maintenance liability and, worse, invites the machine to write toward keywords Sean cannot substantiate, which is the origin-fidelity gate's exact failure mode.

---

## Q2 — How much flare can a syndicated cut carry before it stops reading as professional?

### The finding: "flare" is not one dial, because LinkedIn is not one surface

The research does not support a single global flare percentage. It supports a **split by surface**, because the three ways a hiring manager arrives at you impose different constraints. Kubicka's three arrival paths:

1. **Passive** — they see a post in the feed, then the face and tagline, then the profile.
2. **Active** — they post or comment, you comment on them, they see the face and tagline in their notifications, then the profile.
3. **Recruiter search** — Boolean keyword search, then they scroll a results list of hundreds seeing only face and tagline, then the profile.

All three funnel through the same two elements — photo and tagline — and all three terminate on the profile. So:

- **Feed surfaces (posts) require flare.** The hook is the first two or three lines that show above the fold, and it has to stop a scroll while working *with* the image. A post with no flare does not fail politely; it fails invisibly. Her control-group example — a flat, self-pitying opener — drew 12 likes.
- **Profile surfaces (headline, About, experience) have a flare budget near zero**, but for a reason that is not "professionalism." They are read under a keyword-and-skim constraint: three lines before the fold in About, a results list in recruiter search. Flare that costs skimmability costs the read.

So the honest answer to "how much flare before it stops reading as professional" is: **the ceiling is set by skimmability and by employer-safety, not by decorum.** Two concrete governors emerged, both empirical rather than stylistic:

**Governor 1 — the spammy-DM signal.** Six months in, a former colleague DM'd Kubicka to say her AI marketing posts were coming off as spammy. She nearly quit that day. She names this as the real failure mode: not that the writing was too colourful, but that the *topic set* was undisciplined. The fix was brand pillars, not tone reduction.

**Governor 2 — the two-audience test.** Gupta puts it directly: brand pillars have to look good to a *future* employer without alarming a *current* one. Three to five pillars, chosen narrowly enough to be legible as a specialism, wide enough that the person is not a single-topic obsessive. Kubicka's stated reason for the upper bound on narrowness is social, not strategic: nobody wants to spend time with someone who can only talk about one thing.

**On the decorative layer specifically:** she uses emoji and arrows in the About section and defends them as skimmability devices — visual breaks that let a reader scan rather than read — while conceding on camera that they can turn people off, and that plain numbers or blank lines do the same job. She holds no position that emoji are professional or unprofessional. They are a formatting choice serving skim, and interchangeable with other choices that serve skim.

**On the mix:** while actively job-searching, three posts a week — **two authority, one reach**. The reasoning is that the activity feed is the *third thing* a hiring manager sees after landing on a profile, and generic viral content there proves nothing about how the person thinks.

### Implication for the LinkedIn contract (not a decision)

"Flare" may be the wrong axis for the contract to control. The evidence suggests two axes instead: a **skim-cost budget** (does this survive being read in three lines / in a results list?) and a **pillar-membership check** (does this sit inside the declared pillars, and does it clear the current-employer test?). Neither is a percentage. Both are checkable.

---

## Q3 — What should a cut of an existing artifact look like structurally?

### The five-part post anatomy

Verified from the transcript, not from the summary page. Every high-performing post she analysed has the same skeleton:

1. **Hook** — the first two to three lines visible above the fold. Works as a pair with the image; either alone fails.
2. **Bridge** — usually a story or a lived sequence, carrying the reader from the hook's promise toward the payload.
3. **Meat** — the educational payload. Her stated reason this section is non-optional: people are on a professional platform to learn, so the promise made in the hook has to be paid off with something usable.
4. **Mic drop** — a two-to-four-line summary built on a contrast (what we over-invest in / what we neglect). This is the line that gets remembered.
5. **Engagement question or CTA.**

### The reach/authority fork is a structural fork, not a topic fork

The same subject becomes either post type depending on framing:

- **Reach (ToFU) = "how to X."** Shareable *because* it is detached from a person — generic guidance carries no endorsement cost, so people repost it. That is the mechanism by which it reaches new audiences.
- **Authority (MoFU) = "how I did X."** Not shareable, by construction — and that is fine, because its job is to convince someone already looking at your activity feed that you can think.

Bottom-of-funnel exists (leads, founders, sales) and is out of scope for a job search.

### The templatize move — and where it collides with L2

Her drafting loop: scrape posts that beat a virality bar (she uses 750+ likes, and separately an "X factor" ratio of a post against that creator's own 30-day moving average, to separate a good post from a big following), paste a winner into a **fresh** session, ask the model to extract the reusable skeleton — which phrases are static, which slots are variable — then fill the slots from her own material.

**This is the sharpest finding for the Content Machine, and it cuts both ways.**

The move is genuinely strong as *structural* research: it is competitor/user research applied to format, and it means nobody has to derive copywriting structure from first principles. She is explicit that the template is a container and the contents must be yours; she draws a hard line at word-for-word reuse (permitted only in a pre-agreed content swap between creators who tag each other), credits or asks permission for other people's graphics, and treats written templates as fair game on the grounds that the original author almost certainly used one too.

But the move as demonstrated **imports someone else's sentence rhythms** into the draft. Reusable static phrases lifted from a viral post are, by definition, words that did not come out of Sean's mouth in an interview. That is a direct collision with L2 (the interview transcript is the only permitted source of draft words) and precisely what the origin-fidelity gate exists to catch.

The reconciliation available to the contract — and it is a decision for the contract ticket, not this brief — is to let the machine borrow **structure** (the slot skeleton: hook / six-beat story / turn / payload / contrast mic-drop) while forbidding it to borrow **strings**. Structure is a container; strings are voice. Kubicka's own practice already gestures at this line without naming it.

### Two more structural components

- **The image is part of the hook, not decoration.** The image is what stops the scroll before a single word is read. Her method for choosing one is to describe the *feeling* rather than the content — her worked example rendered a fast train on a collapsing bridge against a slower train on a solid one to carry a speed-versus-durability contrast. This matters for a syndication contract: a cut of an existing artifact needs an image decision, and that decision is downstream of the mic drop, not of the topic.
- **Post length is real but unstated.** Nobody in the video gives a character count, and I found no trustworthy primary source for one. The functional constraints are the ones named above — three lines before "see more" in About, two to three lines above the fold in a post. Treat any specific character-count advice found elsewhere with suspicion; every source I found offering one was vendor SEO.

### The story bank ≈ the corpus (convergent design, independently arrived at)

Her system keeps a **story bank** — her career narratives with specifics, metrics, decisions and outcomes — in a file the agent can read, so authority posts pull real details rather than re-eliciting them every session. She seeded it by having the model **interview her**, then grew it situationally: after a session where she told a new story, she asks for it to be appended.

Gupta's read of this on camera is that the harness is why it works — Claude Code with CLAUDE.md pointing at ICP, positioning and the story bank, which you cannot assemble in a chat window.

This is the Content Machine's corpus + interview-first architecture, built independently by someone who did not have the map. That is meaningful convergent evidence for the design ratified on 2026-08-24, and worth noting that she reached it from the *content* direction while the map reached it from the *voice-fidelity* direction.

---

## Source 2 — Executive Circle (Nate B Jones library)

### The negative finding first

The Executive Circle library **has essentially nothing on content repurposing, syndication mechanics, or LinkedIn post craft.** I searched posts, guides and prompt kits across LinkedIn, content-machine, audience-building, personal brand, voice, distribution and repurposing. It is an AI-strategy, prompting and career library, not a content-marketing library. Do not plan on it as a source for the LinkedIn contract's structural rules.

What it does carry that bears on this ticket:

### Convergent evidence on origin-fidelity (the strongest hit in the library)

[AI Slop Isn't Free. It Hands the Bill to the Next Person.](https://natesnewsletter.substack.com/p/ai-slop-cost) (2026-08-05) ships a "pro-authorship skill" whose stated design is: most voice skills hand you someone else's taste and call it your style, so this one starts from **your own rejected work** — give it a paragraph you threw out and the version you actually sent, infer which choice you were protecting, write that down as an instruction, and test whether the model holds it on unseen material.

That is the Content Machine's origin rule reached from a third direction, and it suggests a cheap addition worth considering: the corpus currently holds what Sean *sent*; the reject/send **pair** is a higher-information signal than either alone. Filed as an observation, not a proposal.

The same post supplies the economic argument the origin gate is defending against — that polished AI output makes unfinished thinking look complete enough to travel, so the cost lands on the reader. It cites curl maintainer Daniel Stenberg's four-word version, and the [BetterUp Labs / Stanford Social Media Lab "workslop" work](https://hbr.org/2025/09/ai-generated-workslop-is-destroying-productivity) (2025) for the shifted-burden framing — that HBR-published lab collaboration is the highest-tier citation in this brief for the claim that slop imposes downstream cost.

### Career and networking assets (adjacent, not core)

- [Cold applications have a <2% response rate now](https://natesnewsletter.substack.com/p/cold-applications-have-a-2-response) (2026-01-29) plus five companion prompt kits: export your own LinkedIn data (Connections.csv, messages.csv, Positions.csv, endorsements) and run relationship-decay, reciprocity, vouch-score and warm-path analyses locally. **The "<2%" figure is a newsletter assertion with no cited study — flagged as unverified.** The *technique* is sound and independently checkable.
- **FDE Skill Builder** (Executive-Circle-gated, published 2026-08-23) — a 30-day worksheet for building one real deployed AI artifact and packaging it as an interview portfolio: classify 10–20 recent instances of a real workflow, sit with the person doing the work, build the smallest intervention, run evals against the old cases, then watch two or three real users use it. Relevant because it is a concrete spec for what belongs in a **Featured section**, which is the one profile surface that carries proof rather than claims. Paywalled — linked, not reproduced.
- [The AI Resume Survival Guide](https://natesnewsletter.substack.com/p/the-ai-resume-survival-guide-for-72f) — adjacent to the resume contract, not this one.

---

## Source 3 — Greg Isenberg

Usable, but with a large caveat: **Isenberg's frame is founder/creator monetization, not job search, and his platform bias is X and short-form video, not LinkedIn.** His central funnel terminates in a product and revenue, which L4 puts out of scope. Take the input side, discard the output side.

His primary X post on building an audience from zero returned HTTP 402 to a direct fetch; the material below comes from his Substack and from secondary write-ups, so it is weaker sourcing than the rest of this brief.

- **ACP / ATM.** Audience → Community → Product, earning Attention → Trust → Money. His test for which one you actually have: if you stop broadcasting, do the conversations continue? An audience goes quiet; a community does not. ([Audiences versus communities](https://latecheckout.substack.com/p/audiences-versus-communities))
- **Format testing.** Test one format per business day until something resonates; evaluate over 90 days; assume formats have life cycles and expire. ([contentgrip write-up](https://www.contentgrip.com/greg-isenberg-audience-building-framework/) — secondary, a content-marketing trade site, so **tier C**.)
- **Creative faucet + capture system.** A routine that reliably produces ideas, a place to catch them, and a scheduled slot to convert them into posts.
- **Swipe files of winning formats.** Independently the same move as Kubicka's viral-post scraping — two unconnected practitioners converging on "study what already worked, keep the skeleton."
- **One painful problem, one platform.** The narrow-promise discipline, matching the map's Rule-of-One heritage in `substack-value-engine`.

**What is not usable:** the community layer. A job search does not need a community, and building one is a multi-quarter commitment that L4's syndication framing explicitly declines. His audience-vs-community distinction is still worth knowing so the contract does not accidentally chase community metrics.

---

## Source tier audit

| Source | Tier | Note |
|---|---|---|
| LinkedIn Recruiter help centre — Boolean search & indexed fields | **B — primary** | Platform's own operator documentation; the only fully verifiable mechanism claim in this brief |
| BetterUp Labs / Stanford SML "workslop" (via HBR, 2025) | **A/B** | Lab collaboration, published research; cited second-hand through Nate's post |
| Kubicka/Gupta video + companion article | **C — practitioner, commercially motivated** | Method checkable and partly verified; outcome numbers self-reported and uncontrolled |
| Nate B Jones / Executive Circle posts & guides | **C — trade/practitioner** | Strong on framing, thin on primary citation; the `<2%` figure uncited |
| Isenberg Substack | **C — trade/practitioner** | First-party but frame-mismatched to job search |
| contentgrip write-up of Isenberg | **C/D — secondary trade** | Second-hand summary of a first-party source |
| "AI PM keyword list" search results (interviewkickstart, futurense, secondtalent, interviewguy, kore1, nextinhr, rework) | **D — vendor SEO** | **Rejected. Not used for any claim.** Interview-prep sellers and JD-template mills writing for search traffic |
| "LinkedIn repurposing 2026" search results (postiv.ai, viralbrain.ai, postory.io, meet-lea.com, itsourcecode) | **D — vendor SEO** | **Rejected.** Scheduling-tool vendors; cadence and character-count numbers uncorroborated |

Two of the three questions in this ticket produced a page-one sweep of vendor marketing on the obvious query. That is a reusable lesson, not an accident: **"what should a LinkedIn post look like" is a market-shaped question**, and per CLAUDE.md market-shaped questions return fresh marketing that recency filters cannot remove. The queries that produced real evidence were the mechanism-shaped ones — what does the platform index, what does the operator do.

---

## What this pass could not answer

- **No corroborated character-count or length guidance** for a LinkedIn post exists in any source I would cite. The functional above-the-fold constraints are the only defensible ones.
- **No independent verification of the outcome claims** (0→50k in six months, five inbound offers weekly, cohort results by week five). Single subject, self-reported, selling a cohort.
- **Nothing on LinkedIn's feed ranking**, as distinct from recruiter search. Everything above concerns *discovery via search and profile*, not distribution. Whether a syndicated cut is throttled for external links, and how, is unaddressed and would need its own pass.
- **The Apify/scraping layer is out of scope and probably should stay there.** Kubicka connects Claude to LinkedIn through third-party Apify actors using proxy servers specifically so LinkedIn cannot attribute the scraping to her account. That is a deliberate ToS-evasion posture. Recorded because it is load-bearing in her system; **recommended against adopting**, and out of scope for L4 regardless, since a syndication contract does not need to scrape anything.

## Open questions this hands forward

These are for the LinkedIn contract ticket to decide, not for this brief:

1. Does the contract own a keyword **procedure** (mine → gate at 75% → map to verifiable claims → place per the tolerance table) rather than a keyword list?
2. Does the "borrow structure, never strings" line get written into the contract as the reconciliation between the templatize move and L2 — and does the origin-fidelity gate get taught to detect borrowed strings specifically?
3. Do "skim-cost budget" and "pillar-membership check" replace a flare percentage as the Professional-lane governors?
4. Does the reach/authority split belong in the LinkedIn contract at all, given L4 says LinkedIn is a syndication target? A cut of an existing Pencil & Prompt post is structurally an *authority* post already — which may mean the contract only ever needs the authority shape, and reach posts are simply not a thing this machine makes.
