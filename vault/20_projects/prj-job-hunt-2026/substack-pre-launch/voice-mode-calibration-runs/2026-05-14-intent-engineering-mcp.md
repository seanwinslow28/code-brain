# Council Session — voice-mode-calibration

- **Session ID:** `20260514-215427-fc35a4`
- **Profile:** `variance`
- **Duration:** 354.3s
- **Tokens:** 10525 in, 8601 out
- **Cost:** $0.1816

## Original prompt

```
You are critiquing a writing voice spec by trying to write IN it. The spec below is "Sean Mode" — a calibrated hybrid voice from a personal `writing-voice-modes` SKILL.md file. The author wants to know whether the spec is unambiguous enough that four different frontier models would read it the same way. Divergence between your draft and the other three models' drafts is the calibration signal.

=== SEAN MODE SPEC (verbatim from .claude/skills/writing-voice-modes/SKILL.md) ===

## 5. Sean Mode (Calibrated Hybrid) — DEFAULT

The natural voice. Load this when no specific mode is requested.

- **Base layer:** Sedaris-Thompson — humor, specificity, self-deprecation, self-implication
- **Sentence engine:** Kerouac — flowing connective rhythm, sensory anchoring, dash breath marks
- **Credibility layer:** Thompson — factual precision (exact numbers, timestamps) dropped AFTER sensory/analogical buildup
- **Punctuation:** Vonnegut — refrains as closers, flat one-liners for impact, deployed in bursts

## Sean's Signature Moves (cross-mode — apply instinctively)

| Move | Mechanic | Example |
|---|---|---|
| **Hard Cut / Deflation** | Build epic register, land mundane/absurd in final clause | "Here's the deal — we'll architect the perfect system, ship it, scale it, and then we'll burn it all, throw our hands in the air, and question everything." |
| **Rule of Three + Emotional Pivot** | Two concrete/funny items, third pivots to genuine feeling | "Fuelled by new found skills, fresh brewed coffee, and for once in my life, a glimmer of hope." |
| **Sensory Before Numbers** | Smells, sounds, images FIRST. Numbers confirm and anchor. | Nostrils flare, pupils dilate, sweat drips. Then: "847 errors in ninety seconds." |
| **Pop Culture Anchoring** | Movie/TV/meme/music ref slotted into a tech context, never the other way around | Dashboard alarms screeching "like the soprano in Pink Floyd's *Great Gig In The Sky*." |
| **Hyper-Specific Anecdote** | One concrete personal moment so specific the reader pictures it without sharing it | "I haven't squinted this hard since I got drunk on a bucket of vodka redbulls in Phuket and stumbled into a local bathhouse." |
| **Screenwriting Cut-To** | Hard juxtaposition between stated intent and actual reality | "I'll be taking it easy tonight" *cut to* "SHOVE THE BEER BONG UP MY ASS." |
| **Humor as Trojan Horse** | Serious points arrive inside jokes; never end on the serious beat alone | The werewolf/turning-30 bit: epic mythology setup → mundane truth ("tired by 6 pm and you think about taxes"). |
| **Self-Deprecation as Structure** | Be the biggest fool first, then earn the right to observe everyone else | "I am a person who deploys to production at 11:47 PM" earns the right to critique every engineer who does the same. |
| **The Domestic Defamiliarizer** | Strip the brand name; keep the concrete function. Blunt, NOT precious. "Agents" beats "small computer programs." | LLM = "a server farm somewhere in Oregon that mathematically hallucinates reassurance." Slack = "a chat room that bills your employer." |
| **Reader-Dismissal** | Preempt the objection the reader is about to raise. Three syntactic shapes: parenthetical / coda / mid-paragraph self-correction. | (a) "...I went through the 6 stages of grief in a week (Yes, 6. There are no rules, nerd)." (b) "Officially becoming a Mass-hole. Patriots still suck though." (c) "There's a moment when every parent notices their kid... I'm not a parent and I would crush ANY youth playing me in SSB." |
| **Equation / Formula Defamiliarizer** | Render an abstract claim as a math/categorical equivalence; the formula does the argument | "In 2026, PM = You and Claude = Entire P&E department." / "You would think AI Companies were Culinary Schools with the amount they 'COOK'." |
| **Inverted Refrain** | Take a canonical refrain and flip its vector — same cadence, opposite meaning. Inversion counts as invention. | "And so it begins." (inverting Vonnegut's "And so it goes" — resignation → anticipation) |

## Anti-Patterns (do NOT do these)

- **Bad Sean** — over-referencing the same sensory detail (coffee three times). Too many metaphors stacked without breathing room. One strong reference earns it; three is falling in love with your own material.
- **Bad Vonnegut** — *copying* "So it goes" verbatim instead of inventing your own refrain (inversion counts as invention; verbatim does not).
- **Desperation Posing as Self-Deprecation** — Self-deprecation EARNS the right to make a point (writer becomes biggest fool first). Desperation NAMES the ask directly: "I need a job," "you can hire me," "give me a chance." Naming the ask collapses the move from earned-funny to needy-transactional. Job-hunt context belongs sideways (a fact about what an agent *does*) — never as a closer ask.

=== TOPIC ===

The author shipped his first Model Context Protocol (MCP) server — `@swins/intent-engineering-mcp v0.1.0` — to the npm registry and the official MCP registry on 2026-05-12. He gave himself 19 days to build it; he shipped on day 6. The server exposes three tools (audit / scaffold / retrofit) wrapped around the concept of "intent engineering" — the discipline of writing structured intent specifications for AI agents and skills (boundaries, success criteria, decision rules — not just prompts). He built it because he's mid-career-pivot from a 2-year PM role at a crypto media company toward an AI PM / Forward-Deployed-Engineer role, and the consensus signal across his research is that MCP servers are the portable career artifact of 2026 — Karpathy's exact words were "stop building skills and start building MCP servers." The server dogfooded itself in the audit (its own SKILL.md scored 23/25, zero anti-patterns). It's the centerpiece of a portfolio sprint targeting July 4 employment.

=== YOUR TASK ===

Write a **150-word paragraph in Sean Mode** about why this MCP server got built and what it cost / felt like / proved. Apply the signature moves instinctively — don't over-deploy them; pick the two or three the topic actually wants. Avoid the anti-patterns, especially Desperation Posing as Self-Deprecation: this is a story about shipping, not a closer ask for a job.

Do NOT reference any existing draft from the author. Write blind from the spec only. Aim for **150 words** (±10 is fine; 200+ is too long, 100 is too short).

Return ONLY the 150-word paragraph. No preamble, no meta-commentary, no headers. Just the paragraph.
```

## Council responses

### ~anthropic/claude-sonnet-latest

Andrei Karpathy said stop building skills and start building MCP servers — which is either the clearest career signal of 2026 or the kind of sentence that sounds profound at 11 PM when you've been staring at a terminal for six hours straight. I gave myself nineteen days. I shipped on day six. `@swins/intent-engineering-mcp v0.1.0` hit the npm registry on May 12th — three tools, one discipline, zero apologies. The discipline is intent engineering: boundaries, success criteria, decision rules — the difference between an AI agent that *does the thing* and an AI agent that does *a thing* adjacent to the thing while confidently explaining why that's fine. The server audited its own SKILL.md and scored 23 out of 25 with zero anti-patterns flagged, which is either rigorous self-validation or the most elaborate way a person has ever argued with themselves and won. And so it begins.

### openai/gpt-5.4-mini

I shipped `@swins/intent-engineering-mcp v0.1.0` because the job market stopped rewarding vibes and started rewarding artifacts — portable ones, inspectable ones, the kind you can hand to a stranger and say, here, this is how I think. So I built three tools — audit, scaffold, retrofit — around intent engineering, which is just a fancy way of admitting prompts are toddler shoes and real systems need boundaries, success criteria, and decision rules. I gave myself 19 days and finished in 6, which felt less like triumph than a caffeine-soaked hostage negotiation with my own calendar: 2 years of PM muscle memory, 1 crypto-media-shaped résumé, and a future that kept asking for evidence. The server audited itself at 23/25, zero anti-patterns, which was deeply annoying in the best way. Proof, apparently, is a thing you can ship to npm. And the MCP registry. And then go stare at the ceiling like you’ve just discovered gravity still works.

### deepseek/deepseek-v4-pro

I was a crypto media PM who once deployed a content calendar two weeks late. Now Karpathy was telling me to stop building skills and start building MCP servers, so I gave myself 19 days to learn a new protocol and ship something that wasn't a prompt. On day 6, with the port still steaming from a last-minute scramble, I pushed @swins/intent-engineering-mcp v0.1.0 to npm — audit, scaffold, retrofit, three tools wrapped around a discipline I'm calling intent engineering. The terminal scrolled green as the server audited its own SKILL.md: 23 out of 25, zero anti-patterns. I hadn't seen numbers that reassuring since my credit score briefly touched “excellent” for two weeks in 2019. The cost was the sensation that my career pivot had just stopped being a conversation and started being a protocol. And so it begins.

### qwen/qwen3.5-plus-20260420

The terminal blinked. I hadn’t slept since Tuesday. Cold coffee rings bloomed like territorial tattoos on a yellow legal pad while I wrestled a node script that refused to behave — convinced I was pacing a nineteen-day sprint, a graceful sidestep past crypto-media slide decks into actual engineering, when really I was just guessing in TypeScript. The cursor pulsed anyway. Day six, I cut the wire. `@swins/intent-engineering-mcp` went live on 2026-05-12: audit, scaffold, retrofit, three blunt instruments that force chaos into boundaries and decision rules. I built it because the consensus was loud — a server is the portable career artifact of 2026, a headless clerk that translates vague ambition into machine-readable contracts. I dogfooded the audit against my own spec. It scored 23 out of 25. Zero anti-patterns. You don’t ship to prove you’re qualified. You ship because the alternative is just another empty tab.

## Cross-rankings

### Judge: ~anthropic/claude-sonnet-latest

- **Order:** A > C > B
- **Reasoning:** Response A most faithfully executes the Sean Mode spec: it deploys 'Sensory Before Numbers' subtly (the caffeine-soaked hostage negotiation before the numbers land), nails the 'Hard Cut / Deflation' with the ceiling-staring closer, uses 'Domestic Defamiliarizer' ('prompts are toddler shoes'), and hits the Sedaris-Thompson specificity without over-stacking metaphors. The word count and rhythm are tight. Response C has strong sensory opening and good closer ('empty tab'), but the 'I hadn't slept since Tuesday / cold coffee rings' opener risks Bad Sean territory (over-stacking atmosphere without the humor anchor), and 'territorial tattoos' is a strained metaphor. Response B opens with a clever self-deprecating setup and the credit score anecdote is a good Hyper-Specific Anecdote, but 'And so it begins' as a closer is the spec's own example of Inverted Refrain used verbatim — the spec explicitly warns against copying existing refrains rather than inventing new ones, which is a direct anti-pattern violation.

### Judge: openai/gpt-5.4-mini

- **Order:** B > C > A
- **Reasoning:** B best matches Sean Mode’s blend of self-implication, specific career context, and a clean hard-cut ending without overdoing the jokes or slipping into a job-ask. C has strong sensory setup and good rhythm, but it leans a bit more solemn and explanatory than the spec’s calibrated hybrid wants. A is clear and accurate, but it’s the least embodied and most generic in voice, with the Karpathy line and closing refrain doing more work than the paragraph’s own personality.

### Judge: deepseek/deepseek-v4-pro

- **Order:** A > B > C
- **Reasoning:** Response A most consistently nails the signature moves — especially the Inverted Refrain ('And so it begins.') as a closer, a hard-cut deflation in the AI agent contrast, and self-deprecating humor that earns the insight without desperation. Response B is very strong with Domestic Defamiliarizer ('toddler shoes') and a Rule of Three emotional pivot, but the inversion is absent and the cadence is slightly less punchy. Response C provides vivid sensory anchoring, but misses an inverted refrain and leans more on narrative than the calibrated, Vonnegut-punctuated burst structure; the inverted refrain sets A apart as the most voice-accurate draft.

### Judge: qwen/qwen3.5-plus-20260420

- **Order:** C > A > B
- **Reasoning:** C best captures the Sedaris-Thompson self-deprecating base with genuine specificity—the early failure callback and credit score tangent feel authentically self-mocking rather than performatively witty. A executes signature moves cleanly (argued with themselves and won lands well) and maintains good Kerouac dash-rhythm, but reads slightly more analytical than vulnerable. B reaches furthest stylistically but over-explains ('which is just a fancy way of admitting') and reads like polished LinkedIn essay rather than self-implicating humor; the closing 'stare at the ceiling' line meanders where Sean's voice should snap flat. All three deploy the inverted refrain aptly, but C's 'my career pivot had just stopped being a conversation and started being a protocol' is the strongest closing pivot across all three, and C lands closest to the 150-word target.

## Chairman synthesis

_Chairman model: `~anthropic/claude-sonnet-latest`_

## Council Synthesis

**Convergence (high confidence):**
All four models agreed on the structural backbone: Karpathy quote as entry point, the 19-days/day-6 contrast as the emotional engine, the 23/25 self-audit as the proof beat, and a clean refrain-style closer. Every model also reached for at least one Domestic Defamiliarizer (intent engineering demystified) and some form of self-deprecating career framing. These are the load-bearing elements the spec is unambiguous about.

**Divergence (low confidence — genuine spec gaps):**

- **The Inverted Refrain:** Claude-Sonnet and DeepSeek both closed on "And so it begins." — which is the spec's *own listed example*. The spec says "inversion counts as invention; verbatim does not." Using the spec's own example verbatim is an anti-pattern violation. Claude-Sonnet's ranker flagged this correctly about DeepSeek; no one flagged it about Claude-Sonnet itself. GPT-5.4-mini closed on the ceiling-staring hard cut instead; Qwen closed on "a career pivot that stopped being a conversation and started being a protocol" — the latter being the most inventive of the four and arguably the strongest closer.

- **Sensory Weight:** Qwen front-loaded heavy atmosphere ("Cold coffee rings bloomed like territorial tattoos") and was flagged by Claude-Sonnet for Bad Sean territory — over-stacking without a humor anchor. GPT-5.4-mini's "caffeine-soaked hostage negotiation with my own calendar" is the tightest sensory-with-humor fusion. DeepSeek's credit score anecdote is a strong Hyper-Specific Anecdote but slightly disconnected from the topic.

- **Tone register:** Claude-Sonnet reads most analytically precise. GPT-5.4-mini has the sharpest Kerouac rhythm. DeepSeek has the warmest self-deprecation. Qwen has the best closer but the most cluttered opener.

**Synthesis rationale:** The final draft takes GPT-5.4-mini's "hostage negotiation" sensory-humor fusion (its clearest contribution), DeepSeek's self-deprecating career-context opener (stronger grounding), Qwen's closing pivot ("stopped being a conversation / started being a protocol" — most inventive refrain), and Claude-Sonnet's precision on the intent engineering definition ("does the thing" vs. "a thing adjacent to the thing"). The Inverted Refrain needs to be *invented*, not borrowed from the spec's own example.

---

I was a crypto-media PM who once made a content calendar feel like an act of engineering. Then Karpathy said stop building skills and start building MCP servers — which is either the clearest career signal of 2026 or what a very confident man says right before you pull an all-nighter. I gave myself nineteen days. I shipped on day six. `@swins/intent-engineering-mcp v0.1.0` — audit, scaffold, retrofit, three blunt instruments built around intent engineering: boundaries, success criteria, decision rules — the difference between an AI agent that *does the thing* and one that does *a thing adjacent to the thing* while confidently explaining why that's fine. The server audited its own SKILL.md: 23 out of 25, zero anti-patterns, which is either rigorous validation or the most elaborate way a person has ever won an argument with themselves. Either way, the career pivot stopped being a conversation. It became a protocol.
