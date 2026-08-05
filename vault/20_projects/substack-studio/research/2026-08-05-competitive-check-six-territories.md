---
title: "Competitive Check — Six Territories: Does a Free Equivalent Already Exist?"
type: research-verification
status: complete
domain: [substack-studio]
tags: [pencil-and-prompt, refocus-2026-08, competitive-check, commodity-trap, executive-circle, divergence, territories]
created: 2026-08-05
last-updated: 2026-08-05
cost_usd: 0.00
method: "Per territory: (1) Executive Circle MCP pass over Nate Jones's archive, reading the closest posts in full, not previews; (2) web search for the closest free equivalents, with a direct fetch of the primary artifact (repo README, wiki page, article) rather than coverage of it. Every verdict carries a resolvable URL. No paid calls."
verdict: "No territory is a clean COMMODITY kill, and none is clean CLEAR either except Sourdough. The free equivalents cover the MECHANISM in five of six territories and publish an evaluation of it in ZERO. The commodity trap is real but it is one layer up from where the sidecar assumed: the mechanism is the commodity, the verdict is the product."
related: [2026-08-05-move-b-candidate-falsification, 2026-08-05-move-a-verification-two-named-examples, 2026-08-05-citation-tier-audit, 2026-08-05-prior-art-synthesis]
ai-context: "Kickoff C, all five steps. Runs the commodity-trap check on the six loose-locked territories from the 2026-08-04 partner session (sidecar ~/.creative-harness/partner-sessions/2026-08-04-pencil-and-prompt-refocus.md, lock L6). Step 3 (the library-model question) was partially discharged by Move B; this pass EXTENDS it into the agent-skill-marketplace class Move B never checked, and that class is the one Sean's library would actually ship into. This document decides nothing. The reconvene makes the keep/kill calls."
---

# Competitive Check — Six Territories

The question, asked the way the old publication should have asked it before shipping prompt pack #1: **for each territory, what is the closest thing a reader can already get for free, and what would they still be missing?**

Cost: $0. Sources: Nate Jones's archive via the Executive Circle MCP, plus open web. Every claim below has a URL.

---

## The finding that outranks the six verdicts

Across every territory except Sourdough, a free equivalent of the **mechanism** exists, often better-engineered than anything a solo writer will ship. Across every territory, including the ones with mature open-source tooling, the number of free equivalents that publish **an evaluation of whether the mechanism works** is zero.

The sharpest specimen is [`wan-huiyan/agent-review-panel`](https://github.com/wan-huiyan/agent-review-panel), an MIT-licensed Claude Code skill that runs a 16-phase adversarial review panel with blind final scoring, sycophancy detection, correlated-bias warnings, skepticism calibration, and a control-validation gate that drops personas which cannot discriminate quality. It is more mechanically sophisticated than most of what this publication would build in a year. Its README says:

> "The cited papers validate multi-agent debate on reasoning benchmarks; this project has not independently benchmarked review quality."

That sentence is the white space, written by a competitor, in their own repo. The engineering is free and excellent. The verdict is absent, and the author is honest that it is absent.

This converges, from a completely independent evidence base, on what [Move B](deep-dives/2026-08-05-move-b-candidate-falsification.md) found by a different route: the differentiator is not the mechanism and not the testing posture, it is the **cumulative, published verdict against a stated protocol**.

**Second cross-cutting finding, and it cuts the other way:** Nate's tactical artifacts are **paid**. Both posts checked directly are truncated at the paywall — the eight adversarial prompts ("The full episode is only available to paid subscribers of Nate's Substack") and the 20-prompt anti-slop set ("Subscribers get all these newsletters!") are gated. So on the literal question the commodity check asks, Nate is an encroachment risk on **angle**, not a free equivalent on **artifact**. The genuinely free equivalents are GitHub repos, Wikipedia, and SEO blog content.

---

## Verdict table

| # | Territory | Verdict | The one-line gap |
|---|---|---|---|
| d1 | Cartography of the Default | **COMMODITY** as a beat / CLEAR as an instrument | A reader can get a better attractor field guide free from Wikipedia; what they cannot get is the twenty-run census of *their own* brief. |
| d2 | Stolen Methods | **CROWDED-BUT-DIFFERENTIATED** | Everyone ports offline methods; nobody states the original practice faithfully, runs it against a real job, and reports what broke in translation. |
| d3 | Import Duty | **CROWDED-BUT-DIFFERENTIATED**, weakest of the three | "Add constraints" is saturated SEO advice; the *social and physical* imports and the customs-violation report are not covered anywhere. |
| d4 | The Input Axis | **COMMODITY** on the corpus half / **CLEAR** on the data-hole half | Teaching someone to feed the model their corpus is the single most saturated query in the category; probing what it invents when there is no corpus is not covered outside engineer-facing eval tooling. |
| d5 | Manufactured Opposition | **CROWDED-BUT-DIFFERENTIATED**, sharpest delta | Four free adversarial tools exist and not one installs a *stake* or tests whether the disagreement changed the output. |
| d6 | Sourdough | **CLEAR** (and the absence may be a cost signal, not an opening) | Nobody has published a blind aged-collaborator-vs-fresh-instance comparison on a creative job; the memory field measures recall accuracy instead. |

---

## d1 — Cartography of the Default

**Closest Nate coverage:** ["I Got Tired of AI Slop so I Built 20 Prompts to Fix It"](https://natesnewsletter.substack.com/p/i-built-a-20-prompt-set-to-kill-ai) (2025-10-10, 5,051 words). Read in full. It is not a census of the median. It is a **quality gate**: 20 function-specific rubrics scoring artifacts on dimensions like specificity, proof density, differentiation. He names anti-patterns ("best-in-class" without proof, "trusted by 1000+ companies" without naming any) but as review criteria, not as a map of where the model lands by default.

**Where his angle stops:** he is filtering output, we are characterizing the attractor. He never runs one brief twenty times, never clusters, never names a basin. He also ships zero measurements: the 20 prompts arrive with statistics about the slop *problem* (Ahrefs, MIT, FTC) and none about the prompts' *effect*.

**Closest free equivalents:**

1. **[Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)** — the real competitor, and it is a monster. Fetched directly: roughly 50+ distinct indicators across seven categories (content, language, style, communication, markup including model-specific signatures, citations, edit summaries), built from thousands of real diffs dated 2023 through 2026, maintained by WikiProject AI Cleanup, free, and updated faster than one person can write. It is the named-attractor field guide, already shipped, at a scale a solo publication cannot match. It is also honest about its own limits: *"The patterns listed here are also only potential signs of a problem, not the problem itself."*
2. **[The Temperature Variance experiment](https://medium.com/@elizabetakuzevska/temperature-variance-experiment-55a049aa9ae7)** (2026-03) + its free [Temperature Variance Lab](https://onlinemarketingacademy.ai) — 20 runs of one prompt across four temperature settings, word count / lexical diversity / variance reported, plus a live tool where a reader can run their own prompt. This is the closest existing thing to the "default probe."
3. Listicle tier: [Forbes, 15 new giveaway signs of AI writing](https://www.forbes.com/sites/jodiecook/2026/05/21/15-new-giveaway-signs-of-ai-writing-may-2026-update/), [Alex Banks, "You Sound Like ChatGPT"](https://thesignal.substack.com/p/you-sound-like-chatgpt), [vrid.ai's 27 red flags](https://vrid.ai/blog/signs-of-ai-writing). Free, endless, and collectively they have this beat covered as commentary.

**Verdict: COMMODITY as a standalone beat. CLEAR as the instrument.** The field-guide product is already free and better. What nobody publishes is the census run against *a specific creative brief* with the outputs clustered and the basin named — the temperature lab is one prompt, one model, lexical metrics only, and per [Finding 8](2026-08-05-prior-art-synthesis.md) lexical metrics are the ones the literature considers insufficient.

**What someone with the same tools would lack:** the twenty-run render of their own job with the attractor named, rather than a general list of tells they still have to map onto their work themselves.

**Note for the reconvene:** this independently ratifies the critic's structural call in the sidecar — d1 was already demoted from beat to instrument on structural grounds. The competitive evidence says the same thing for a different reason. Two independent paths to the same demotion is the strongest signal in this document.

---

## d2 — Stolen Methods

**Closest Nate coverage:** two.
- ["Surfing the Guardrails: 7 Production-Grade Prompting Patterns I Stole from Claude's (Alleged) System Prompt"](https://natesnewsletter.substack.com/p/surfing-the-guardrails-7-production) (2025-05-29). Same verb, different larceny: he steals from a leaked *system prompt*, not from an offline craft.
- ["Too Helpful to Think"](https://natesnewsletter.substack.com/p/too-helpful-to-think-the-hidden-cost) (2025-06-19), read in full, is the real overlap: six of its eight prompts **are** ports of offline protocols — the harsh journal referee, devil's advocacy, the pre-mortem, the VC grilling, the security audit, the red team.

**Where his angle stops:** he states the port in a sentence and never runs it. No before/after, no baseline, no failure. The closest he comes to reporting a breakdown is an unmeasured aside: *"if you start to get upset with it then you will see that it just tends to back down."* That is the translation failure this territory exists to document, mentioned in passing and never tested. Plus: the prompts are paywalled.

**Closest free equivalents:**

1. **[Zoe Scaman, "A New Creative Intelligence"](https://zoescaman.substack.com/p/a-new-creative-intelligence)** (2025-10) — the nearest miss in the whole check. She does exactly the move: *"I feed the AI frameworks from jazz improvisation, ecosystem design, evolutionary biology, network theory, game theory."* Fetched and checked: zero empirical data, no A/B, no before/after, no failure cases, nothing shipped as installable code or documented protocol. Anecdote at newsletter scale ("I killed three major pieces this year") with no supporting evidence.
2. **[Greg Petroff, "The Art of Juxtaposition"](https://gregpetroff.substack.com/p/the-art-of-juxtaposition-how-designers)** (2025-08) — designers colliding unrelated domains ("What if traffic lights worked like jazz improvisation?"). Same shape, same absence of measurement.
3. **The academic tier**, which is where the actual rigor lives: [IDEAFix](https://arxiv.org/pdf/2606.00875) evaluates creative defixation prompting; [cognitive prompting](https://arxiv.org/abs/2410.02953) ports structured cognitive operations. Both tested, neither shipped as anything a reader can install. This is the same enterprise-vs-consumer split [Finding 2](2026-08-05-prior-art-synthesis.md) found for the library model, reappearing at the technique level.

**Verdict: CROWDED-BUT-DIFFERENTIATED.** The port move is common. Faithful statement of the source practice, a run against a real job, a report of what broke in translation, and an installable artifact with a verdict: not found anywhere, free or paid.

**What someone with the same tools would lack:** they would know that jazz and murder boards are interesting lenses; they would not know which ports survive contact with a real job, which are metaphors wearing a method's name, or what happened the half of the time it failed.

---

## d3 — Import Duty

**Closest Nate coverage:** ["10x Your Prompt Power With a 100 Word Prompt"](https://natesnewsletter.substack.com/p/goldilocks-prompting-10x-your-prompt) (2025-11-13) is a *length* constraint (Goldilocks prompts), the nearest neighbour by mechanism but not by intent. Nothing in the archive smuggles a real-world constraint (a budget that runs out, a person who will be hurt, a car everything must fit inside).

**Closest free equivalents:** "constraint-based prompting" is an established, named, SEO-saturated technique:

1. [What Is Constraint Based Prompting](https://www.c-sharpcorner.com/article/what-is-constraint-based-prompting/) — "adding limits like time, budget, and resources."
2. [Prompt With Constraints: Why Limitations Make AI Better](https://whitebeardstrategies.com/blog/prompt-with-constraints-why-limitations-make-ai-better/) — fetched and checked: no measured comparison, no captured runs, no documented failures, no reusable artifact. Airbnb/IKEA/Dropbox as illustrative anecdote. Pure advice.
3. [PromptQuorum's constrained prompting page](https://www.promptquorum.com/prompt-engineering/constrained-prompting) and [Constraint-Aware Prompting](https://prompton.wordpress.com/2025/07/08/%F0%9F%9A%80-constraint-aware-prompting-mastering-ai-with-real-world-limits-in-2025-%F0%9F%98%B1/) — same shape, same absence.

**Verdict: CROWDED-BUT-DIFFERENTIATED, and this is the weakest of the three such verdicts.** The generic version ("give it a budget and a deadline") is genuinely commodity, and it is exactly the shape of takeaway that got prompt pack #1 blocked. The differentiation is narrow and lives entirely in the *kind* of import: social stakes (a named person who will read this and be hurt), physical stakes (it has to fit in the Civic), and the customs-violation report when the borrowed mind ignores the constraint. Nobody covers those.

**What someone with the same tools would lack:** they would know constraints sharpen output; they would not have a bindable constraint pack for their own life, or any report of what the model does when the constraint is a person rather than a number.

**Risk flag for the reconvene:** if a post in this territory lands on "add constraints," the value gate should block it. The territory only survives on the imports the SEO tier cannot reach.

---

## d4 — The Input Axis

**Closest Nate coverage:** ["Beyond the Perfect Prompt: The Definitive Guide to Context Engineering"](https://natesnewsletter.substack.com/p/beyond-the-perfect-prompt-the-definitive) (2025-06-20) and ["Stop Waiting for New AI Models: Here's How to Use Data to Make AI at Work, WORK"](https://natesnewsletter.substack.com/p/stop-waiting-for-new-ai-models-heres) (2025-05-14). The second is this territory's thesis in his voice: the value comes from getting the data right, not from the model. He owns this angle at scale.

**Where his angle stops:** enterprise/work data, not a hand-built personal creative corpus, and no diet comparison — he never runs the same brief on two diets and shows the difference line by line.

**Closest free equivalents (corpus half): saturated.** This is the most crowded shelf in the entire check.

1. [thecentral.ai's humanize guide](https://thecentral.ai/p/how-to-humanize-your-ai-writing) — fetched: three-technique method (corpus analysis, voice profile, tell-banning), and it gives away a **650+ word master prompt** free plus a pointer to the Wikipedia taxonomy. No measured before/after, but the artifact is free and immediately usable.
2. [eesel: How to train AI on your writing style](https://www.eesel.ai/blog/how-to-train-ai-on-your-writing-style), [thestacc's 2026 guide](https://thestacc.com/blog/train-ai-writing-style/), [The Brand Algorithm](https://www.the-brand-algorithm.com/guide-to-training-ai-for-brand-voice/), [digitalapplied](https://www.digitalapplied.com/blog/extract-brand-voice-guide-ai-content-2026), [TextPolish](https://www.text-polish.com/blog/beyond-surface-edits-how-to-infuse-personal-voice-into-ai-drafts-2026).

One of these even reaches for the measurement move ("stop describing your voice with adjectives and start measuring it"), though none actually computes anything.

**Closest free equivalents (data-hole half): thin, and engineer-facing only.** Probing what the model invents where no corpus exists exists as eval tooling, not as creative practice: [Braintrust's hallucination-detection roundup](https://www.braintrust.dev/articles/best-hallucination-detection-tools-2026), consistency sampling, and the [SHINE method](https://arxiv.org/html/2411.09689v4) (classifies output as aligned / misaligned / fabricated with no external knowledge required). All of it is aimed at developers shipping RAG apps. None of it is aimed at a writer asking what the model made up about *their* subject.

**Verdict: COMMODITY as framed, CLEAR on the data-hole probe.** The corpus half must not lead. It is the most-covered query in the category and it is also the closest surviving relative of the premise that died by Sean's own GPT Image 2 test.

**What someone with the same tools would lack:** on the corpus half, nothing — they can get it free in ten places. On the probe half, everything: a practitioner-facing procedure for catching the model confidently inventing where the data runs out.

---

## d5 — Manufactured Opposition

**Closest Nate coverage:** ["Too Helpful to Think"](https://natesnewsletter.substack.com/p/too-helpful-to-think-the-hidden-cost) (2025-06-19) is a direct hit and the strongest encroachment in this document. Read in full: he diagnoses the RLHF sycophancy mechanism, cites Anthropic's 2023 sycophancy research, gives seven decision rules ("Do not believe the first yes from an LLM. Ever."), and ships eight named adversarial personas — Harsh Academic Reviewer, Devil's Advocate, Pre-Mortem Analyst, Skeptical Investor, Security Auditor, Contrarian Colleague, Future Retrospective, Red Team Commander.

**Where his angle stops, precisely:**
- **No stakes.** Every one of the eight is a *persona instruction*. None gives the collaborator something to lose: no scoreboard, no secret to protect, no budget it defends against you, no rival instance, no instance paid to kill the idea. That is the entire content of this territory.
- **No measurement.** Zero runs, zero comparison against the agreeable default, no evidence any of the eight changes an outcome.
- **The theater failure is acknowledged and left untested.** His own note that the model "tends to back down" if you push back is the performed-disagreement failure mode named in the sidecar's machine-fate hypothesis, reported anecdotally and never instrumented.
- **Paywalled.**

**Closest free equivalents — and this shelf is genuinely crowded:**

1. **[`wan-huiyan/agent-review-panel`](https://github.com/wan-huiyan/agent-review-panel)** — MIT, 4-6 reviewers, 16 phases, parallel independent review before cross-examination, blind final scoring, sycophancy detection, correlated-bias warnings, skepticism calibration 20-60%, verification gates. $3-20/run in Opus tokens. And: *"this project has not independently benchmarked review quality."*
2. **[`dungnotnull/devils-advocate-agent`](https://github.com/dungnotnull/devils-advocate-agent)** — multi-provider routing, 14+ fallacy types via NLI models, RAG-grounded counterarguments crawled from arXiv and Semantic Scholar, four intensity levels from Skeptic to Demolisher. Fetched: **no evaluation results, no benchmarks, no documented failures**, no claim that the output changes any decision. Motivational epigraphs instead of evidence.
3. **[`movito/adversarial-workflow`](https://github.com/movito/adversarial-workflow)** and the [OpenClaw Devil's Advocate Suite](https://llmbase.ai/openclaw/devils-advocate-suite/) (pre-mortem, PR/FAQ review, dialectical inquiry, TRIZ contradiction resolution).

**Verdict: CROWDED-BUT-DIFFERENTIATED, with the sharpest and best-evidenced delta of the six.**

Three separate gaps, each defensible:
- **Stakes.** Four free tools, all persona-based. Not one installs an incentive.
- **Theater detection.** Nobody publishes a test of whether the opposition changed the artifact. The one competitor sophisticated enough to have anti-groupthink machinery says in writing that it has not benchmarked itself.
- **Heterogeneity.** [Finding 4](2026-08-05-prior-art-synthesis.md) from the DR round: homogeneous multi-agent debate hits consensus collapse and rarely beats single-agent self-consistency; heterogeneous debate across genuinely different architectures is the active ingredient. `agent-review-panel` forces *one model* through divergent stances. The entire free shelf ships the variant the evidence says is weaker, and Sean already runs the stronger one (`llm-council`, `fusion-discovery-council`).

**What someone with the same tools would lack:** they would have a very sophisticated agreeable machine wearing a critic costume, with no way to tell whether it ever cost them anything — and they would be running the homogeneous variant the literature says underperforms.

---

## d6 — Sourdough

**Closest Nate coverage:** ["I Wrote the AI Memory Fix Every Existing Solution Missed"](https://natesnewsletter.substack.com/p/i-wrote-the-ai-memory-fix-every-existing) (2025-10-16), read in full, plus the [Memory Gap executive briefing](https://natesnewsletter.substack.com/p/executive-briefing-the-memory-gap) (2025-12-07). The first is substantial: five root causes, eight principles (separate by lifecycle, match storage to query pattern, mode-aware retrieval, build portable, compression is curation, verify fuzzy retrieval against ground truth, structure compounds), and five prompts free via Notion.

**Where his angle stops:** it is architecture advice, delivered as principles, and it is entirely about **recall fidelity**. There is no longitudinal run, no aged instance, no blind comparison, and nothing about whether a long-lived collaborator gets *better or worse as a creative partner* over months. His own framing is that forgetting is a technology AI lacks, which is adjacent to the engineered-amnesia sub-genre but is a design observation, not an experiment.

**Closest free equivalents:** the memory field measures the wrong axis for this territory. [mem0's 2026 memory benchmark report](https://mem0.ai/blog/state-of-ai-agent-memory-2026) and LoCoMo test multi-session recall (single-hop, multi-hop, open-domain, temporal). [supermemory](https://supermemory.ai/blog/long-term-memory-ai-study-assistants/) and the vendor tier sell retention. A [Towards Data Science piece](https://towardsdatascience.com/context-windows-forget-what-matters-i-used-a-140-year-old-psychology-paper-to-fix-ai-memory/) builds an Ebbinghaus-curve decay engine — the closest thing to engineered amnesia, and it is an engineering artifact with no creative comparison. Searches for a published aged-vs-fresh blind creative comparison returned academic work on ChatGPT and creativity (RCTs, INFORMS collaboration-modality studies) but nothing longitudinal on a single standing collaborator.

**Verdict: CLEAR.** No free equivalent found. The honest caveat, and it should be read as part of the verdict: this is CLEAR partly *because* it is expensive. Months of feeding before the first comparison post exists, a serialized arc new readers arrive in the middle of, and a real chance the answer is boring. The absence may be a rational market response rather than an unclaimed opening.

**What someone with the same tools would lack:** any evidence at all about whether the collaborator they have been feeding for six months is sharper than a fresh one, or just more agreeable — the question every serious daily user eventually asks and nobody has answered in public.

---

## Step 3 — The library model, extended past Move B

[Move B](deep-dives/2026-08-05-move-b-candidate-falsification.md) checked twelve named candidates (Anthropic's prompt library, DAIR.AI, promptingguide.ai, LangSmith Hub, PromptHub, PromptLayer, Braintrust, DSPy, OpenAI Cookbook, awesome-chatgpt-prompts, HF finephrase, Nate Jones) and found eleven clean NOs plus one partial. That work stands and is not repeated here.

**What this pass adds is a category Move B never checked, and it is the one that matters most:** agent-skill marketplaces. This is the actual shelf a Pencil & Prompt mechanism library would ship onto, since the packaging plan's both-tiers rule puts a symlinkable `.claude` skill next to every copy-paste kit.

Checked live: [claudemarketplaces.com/skills](https://claudemarketplaces.com/skills), which indexes 23,600+ Claude Code skills. Per-entry metadata is **developer avatar, skill name, org identifier, one-line description, install count**. Fetched verdict: *"The directory contains no test results, evaluation scores, pass/fail verdicts, or documented failure cases attached to individual skills — only installation volume is tracked as a quantitative measure."*

Install count is a popularity signal standing in for an evidence signal. That is precisely the trust substitution [Finding 2](2026-08-05-prior-art-synthesis.md) identified in the consumer prompt marketplaces, reproduced one abstraction layer up in the skill ecosystem.

Skill-quality **tooling** does exist (a skill-quality benchmarker on mcpmarket, `claude-skills-benchmark`, aiskill.market's Skill Evaluator, and [self-testing guidance for agent skills](https://zenvanriel.com/ai-engineer-blog/claude-agent-skills-software-testing-rigor/)), which is the same private-tooling-versus-public-artifact split as Braintrust and PromptLayer. You can benchmark your own skill. Nobody publishes the result next to the entry.

**Net:** Move B's restated claim survives this extension and gets stronger, because the extension covers the category the product would actually compete in. The absence is now verified in four distinct categories: prompt libraries, enterprise eval tooling, practitioner newsletters, and agent-skill marketplaces.

*(One skill-quality URL returned HTTP 429 and could not be fetched; the marketplace-directory verdict rests on the live claudemarketplaces fetch, which did render.)*

---

## Two findings outside the six territories

**1. The folklore rung has partial encroachment.** [Finding 3](2026-08-05-prior-art-synthesis.md) called temperature-tuning-as-folklore "the highest-value publishable finding of the round." A free Medium post already published a version of it in March 2026: 20 runs, four temperature settings, and the conclusion that *"19 of 20 outputs recommended identical core strategies regardless of temperature setting"* and *"if your outputs feel generic, temperature is almost certainly not where the problem lives."* It also ships a free live tool.

This does not kill the rung. That experiment is n=20 on one prompt against one model with lexical metrics; the academic result behind Finding 3 is a factorial across 7 foundation models and 100 open-ended questions. But the contrarian *finding* is no longer novel, so the post cannot be sold on the surprise. It has to be sold on the protocol and the scale, which is a different, more honest, and more on-masthead pitch.

**2. The commodity trap was mis-located.** The sidecar's worry, inherited from prompt pack #1, is that a territory might have a free equivalent. The evidence says nearly all of them do, and that this is survivable, because the free equivalents are uniformly unevaluated. The trap is not "someone else covers this topic." The trap is "the reader's takeaway is a technique, and techniques are free everywhere." A post whose deliverable is a mechanism competes with GitHub. A post whose deliverable is a *verdict on a mechanism* competes with nobody.

---

## What this changes for the reconvene

- **d1 should be demoted from beat to instrument.** Two independent arguments now agree (the critic's structural one and this competitive one). Wikipedia has the field-guide product and cannot be out-catalogued by one person.
- **d4 should be reshaped or dropped as framed.** The corpus half is the most saturated shelf checked, and it is a relative of the dead premise. The data-hole probe is the part with air around it.
- **d5 is the strongest keep.** Crowded shelf, three defensible gaps, and it is the territory where Sean's existing infrastructure maps onto the best-evidenced mechanism in the DR round. It is also the rung-#1 candidate the synthesis already named, and this check strengthens rather than complicates that.
- **d2 keeps its spine role**, on the condition that every port ships with a translation-failure report. Without that, it collapses into Scaman's shape, and she has more distribution.
- **d3 survives on the imports only.** If a draft's takeaway is "add constraints," kill the draft.
- **d6 is genuinely open** and genuinely expensive. Treat the emptiness as an unanswered question, not a free lunch.
- **The measurement protocol moves up again.** Three independent passes now (Finding 8, Move B, this one) land on the same build-order inversion. It is no longer a prudent first step; it is the only thing on this list that a competitor is not already giving away.

---

## Method limitations, stated

- **Coverage is not proof.** Absence of a free equivalent in these searches is not proof one does not exist. This pass reduces commodity risk; it does not eliminate it. Searches were English-language, US-weighted, and run on 2026-08-05.
- **Executive Circle covers Nate Jones's archive only.** Other practitioner newsletters running comparable work would not surface here. Same limitation Move B stated.
- **Paywall status was checked on two Nate posts, not all of them.** Both were gated. It is likely but not verified that his other tactical artifacts are too.
- **Verdicts describe the artifacts as published today.** A territory that is CLEAR in August can be claimed in September, and the free tooling in d5 is being actively developed.
- **One fetch failed** (HTTP 429, mcpmarket skill benchmarker). Its absence does not change the marketplace verdict, which rests on a fetch that succeeded.
