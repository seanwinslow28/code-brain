---
type: outline
project: prj-job-hunt-2026
task: Task 13 Step 1 — Access-vs-Meaning Manifesto outline
created: 2026-05-20
last_updated: 2026-05-21
status: decisions-locked-ready-for-step-2
draft_lock_target: 2026-05-23
publish_target: 2026-06-19
ai-context: |
  Step 1 deliverable for Task 13 (Council Gap-Fill 2). Section-by-section outline with target
  word counts, plotted artifact list for the spectrum chart, role-map JD targets, and pre-drafted
  opening + closing hooks for the personal-voice bookends. Sean's decisions locked 2026-05-21
  (see §7 "DECISIONS LOCKED"); JD URLs populated from vault/20_projects/prj-job-hunt-2026/target-companies.md.
  Ready for Step 2 (full draft pass on docs/MEANING_OVER_ACCESS.md, ~6 hours).
related:
  - "[[2026-05-06-unified-roadmap]]"
  - "[[ref-nate-ai-access-vs-meaning-platform]]"
  - "[[2026-05-16-council-nate-jones-digest]]"
  - "[[target-companies]]"
sources:
  - Nate's "AI Work Primitives: Access vs Meaning" (2026-05-05)
  - Council brief Gap-Fill 2 (2026-05-16)
  - target-companies.md (JD URLs validated 2026-05-13)
---

# Task 13 — Manifesto Outline (Step 1)

> **STATUS 2026-05-21:** All 6 open decisions locked (see §7). JD URLs populated from target-companies.md. **Ready for Step 2** — Hook A (silent regression) is the opener, all 7 artifacts plotted as drafted, voice mode is strategic-sober with planned writing-voice-modes review after full draft.

> Section-by-section structure with word-count targets, plotted artifact list, role-map JD candidates (now with real URLs), and pre-drafted opening/closing hooks. Step 2 expands this into the full ~1,500-word draft of `docs/MEANING_OVER_ACCESS.md`.

## 0. The thesis in one sentence (carry into interviews)

> **The bet:** Access is reach; meaning is judgment. The durable enterprise value in agents is the semantic layer — typed work objects, scoped authority, memory provenance, reviewable decisions — not agents clicking around UIs. I've shipped seven artifacts that back it.

If you can say this sentence cold, the manifesto is doing its job. Every section below is in service of you being able to say it.

---

## 1. Section 1 — "The bet" (Opener, ~150 words, personal voice)

**Job of this section:** earn the right to be read. One concrete moment from your actual recent work, then the thesis.

**Two opener hooks — pick one before Step 2 starts:**

### Hook A — The silent-regression story (Recommended)
> On May 10th I caught a 9-day-old silent regression in my vault synthesizer. The agent had been running clean every night — `status: ok`, zero errors, manifest healthy — and producing nothing. It had complete access to my vault, full write permission, the right model on the right hardware. What it didn't have was a way to recognize that "I wrote zero concept articles tonight" was a failure rather than a quiet success. The button worked. The decision did not.

*Why this hook:* it's a real Sean moment (vault synthesizer, Phase 6, the Tier 1.5 fix). It dramatizes Nate's "the button worked, the decision did not" line without naming it. It earns the thesis turn at the end — "this is what access without meaning costs."

### Hook B — The dogfood result
> When my intent-engineering MCP server audited its own SKILL.md, it scored 23/25 with zero anti-patterns. That's a stupid sentence on its face. But it's the sentence I keep returning to, because it's the only meaningful credibility test I know of for a meaning-layer tool: did you build something that survives looking at itself with the rubric it gives everyone else?

*Why this hook:* shorter, sharper, more cocky. Risk: less narrative arc; reads more like a flex than a story.

**Then the thesis turn (~50 words, same in both hooks):**
> Computer use gives agents reach. Semantic control gives them judgment.* The long-term moat isn't the ability to click the button. It's ownership of the layer that tells the agent what the button means. My bet for the next four years of AI PM work is on meaning — and here's the map.

*\*Cite Nate verbatim with footnote / link to his 2026-05-05 essay.*

---

## 2. Section 2 — "Artifact map" (~400 words + spectrum chart)

**Job of this section:** convert seven scattered shipped things into a single coherent bet.

**The 2D plot (Mermaid `quadrantChart`):**
- **Horizontal axis:** `access ↔ meaning`
- **Vertical axis:** `infrastructure ↔ workflow`
- **All seven plotted artifacts live on the MEANING half.** That's the load-bearing visual claim.

### The seven plotted artifacts (with quadrant + one-line "why meaning here")

| # | Artifact | Quadrant | One-line "why meaning here" | Status |
|---|---|---|---|---|
| 1 | **intent-engineering MCP** | meaning + infrastructure | Turns vague PM intent into a typed spec the agent can act on without guessing | ✅ shipped 5/12 |
| 2 | **vault-knowledge MCP** | meaning + infrastructure | Turns 17 days of personal knowledge into queryable concepts with typed reasoning edges | 🟡 ships ~6/4 (Task 10) |
| 3 | **concept_edges (Phase D)** | meaning + infrastructure | Six-relation typed schema (`supports`, `contradicts`, `evolved_into`, ...) that makes agent memory queryable, not just retrievable | ✅ shipped |
| 4 | **eval suite** | meaning + workflow | A 10-case binary rubric that converts "did the agent run?" into "did it produce a publishable concept article?" | ✅ shipped 5/12 |
| 5 | **cost caps (HybridRouter + budget governors)** | meaning + workflow | Per-task / per-day / per-month budgets aren't a cost control; they're an authority primitive — the agent is *allowed* to spend $X here, not $Y | ✅ shipped |
| 6 | **judge layer (substack-drafter retrofit)** | meaning + workflow | Promotes draft output from "the agent wrote a thing" to "the agent wrote a thing AND another agent judged it against a rubric before any human sees it" | 🟡 ships ~6/4 (Task 12) |
| 7 | **agent fleet observability** | meaning + workflow | Turns 17 SDK agents from "trust me they run" into "look at the screen for 30 seconds and verify" — observability as audit primitive | ✅ shipped 5/18 |

### Two negative-space callouts (named, not endorsed)
- **Browser-use / computer-use agents** (access + workflow): Manus, Adept, browser-use, OpenAI Operator. Powerful, brittle, and what most candidates lead with. Named here to make the contrast visible.
- **MCP HTTP transports / generic SaaS connectors** (access + infrastructure): the connector layer that gets the agent near the work but doesn't tell it what the work means. Named to make explicit that *MCP itself isn't the meaning layer* — the rubric inside a meaning-layer MCP server is.

### Mermaid source (for `docs/diagrams/access-meaning-spectrum.mmd`)

```mermaid
quadrantChart
  title Access vs Meaning × Infrastructure vs Workflow
  x-axis Access --> Meaning
  y-axis Workflow --> Infrastructure
  quadrant-1 Meaning + Infrastructure
  quadrant-2 Access + Infrastructure
  quadrant-3 Access + Workflow
  quadrant-4 Meaning + Workflow
  intent-engineering MCP: [0.80, 0.85]
  vault-knowledge MCP: [0.82, 0.80]
  concept_edges (Phase D): [0.75, 0.90]
  eval suite: [0.78, 0.30]
  cost caps (authority primitive): [0.70, 0.25]
  judge layer: [0.85, 0.20]
  fleet observability: [0.72, 0.35]
  browser-use agents: [0.15, 0.20]
  MCP HTTP transports: [0.25, 0.75]
```

> **Sean — confirm or adjust the plotted coordinates.** I positioned all seven on the meaning side with mild spread; you may have a sharper read on whether (e.g.) the judge layer is more "meaning" than the eval suite or vice versa. The visual punch is "seven dots on one side, two faint dots on the other."

### Closing line of Section 2
> Seven artifacts. One side of the chart. That's not a coincidence; it's the bet.

---

## 3. Section 3 — "Role map" (~400 words, table format)

**Job of this section:** prove the bet is hireable. Show that real companies pay for meaning-layer thinking, with cited JDs as evidence.

### The role map table

> **JD URLs populated 2026-05-21** from [`vault/20_projects/prj-job-hunt-2026/target-companies.md`](../../target-companies.md). Validated dates per target-companies frontmatter (last_updated 2026-05-13). Step 6 of Task 13 re-validates URLs on publish day (~6/19).

| Buyer | Spectrum position | Vocabulary tell (verbatim from JD) | Example JD |
|---|---|---|---|
| **Anthropic FDE (Boston / NYC / Chicago)** | meaning + workflow | "MCP servers, sub-agents, and agent skills"; "control architectures around production agent deployments" | [Greenhouse — Forward Deployed Engineer](https://job-boards.greenhouse.io/anthropic/jobs/4985877008) |
| **Glean** (Forward Deployed PM) | meaning + infrastructure | "0-to-1 product creation"; "shipped AI in production" | [Greenhouse — FDP](https://job-boards.greenhouse.io/gleanwork/jobs/4651950005) |
| **Sierra / Decagon** | meaning + workflow | "PM, Agent Development" (Sierra); "Senior Agent Product Manager" (Decagon); "review and escalation paths" | [Sierra — PM, Agent Development](https://jobs.ashbyhq.com/Sierra/effd7cd2-8a28-4bae-a3b8-40720ba09717) · [Decagon — Sr. Agent PM](https://jobs.ashbyhq.com/decagon/dcf9b561-f2fb-422b-88a9-33ce76e96608) |
| **Cohere** (Agent Harness & Modelling) | mixed (meaning + workflow, leaning infrastructure) | "agent runtime"; "tool orchestration, parallel execution, failure recovery" | [Ashby — PM, Agent Harness & Modelling](https://jobs.ashbyhq.com/cohere/1d1b300d-254b-48c4-958f-99c6b907f295) |
| **Manus / Adept / browser-use / OpenAI Operator** | access + workflow | "computer-use"; "browser automation"; "general computer-using agent" | Negative-space callout — not on Sean's target list; cited as the category the manifesto argues *against* |

### Body prose (~300 words after the table)

Two paragraphs of analysis after the table:

**Paragraph A (~150 words):** Why the four meaning-side rows cluster on specific vocabulary. The tell is verbs — `govern`, `scope`, `review`, `validate`, `escalate` — vs. access-side verbs (`click`, `automate`, `operate`). Note that Anthropic's own FDE listing literally requests "MCP servers, sub-agents, and agent skills" by name; that's not a coincidence, that's the layer the company that ships the model thinks they're hiring for.

**Paragraph B (~150 words):** Why the access-side row exists. Acknowledge browser-use / computer-use as real, important work. Then the move: name the structural reason candidates with stronger CS backgrounds will win that side, and the structural reason a PM-with-context like Sean will win the meaning side. The honest read: meaning-layer roles select for judgment about what should be made legible, not pure engineering ability. That's a PM superpower being valued correctly.

### Closing line of Section 3
> Five buyers. Five vocabularies. One spectrum. If you're hiring for "agents that operate," you can find a thousand candidates; if you're hiring for "agents that understand what they're operating on," the market is thin. I want to be in the thin market.

---

## 4. Section 4 — "Why not browser-first" (~250 words)

**Job of this section:** make the case structurally, not just preferentially. Why is the meaning-layer bet *correct* and not just "what Sean happens to like"?

### The three structural arguments (4-5 sentences each)

**Argument 1 — Access agents fight the interface they operate on.**
A browser-use agent depends on button labels, page structure, DOM semantics — all of which are hostile to it because they change under it. Notion ships a UI refresh; the agent's selectors break overnight. The agent has to relearn the same workflow it learned last week. Meaning-layer agents operate on typed work primitives the human controls; the schema is a contract, not a guess.

*Concrete example to embed:* Lindy clicking through a Notion page whose section header changed (verifiable failure mode from Nate's essay).

**Argument 2 — The richest interface wins, not the broadest.**
A connector that tells the agent "this is a calendar event with recurrence, attendees, and notification policy" beats a screenshot of a calendar 100% of the time on tasks that matter. The broad interface (screen + mouse) is the bridge technology for the messy middle; the rich interface (typed objects + scoped actions) is the destination. Building toward the destination today is the strategic call.

**Argument 3 — Trust is an architecture, not a switch.**
"Trusted write access" is too small as a thesis. Trust is *scoped* — read but not write, draft but not send, recommend but not approve, spend under threshold but not above. Those distinctions require semantics. An agent that can only see a button doesn't know whether pressing it costs $5 or $5,000; an agent that operates on typed payment objects does. Authority follows meaning. You can't have one without the other.

### Closing line of Section 4
> The browser will exist. So will the agents that drive it. Both will keep getting better. But the durable platform value is going to accrue to the layer that tells the agent what the button means — not the agent that pushes it.

---

## 5. Section 5 — "The bet, restated" (Close, ~150 words, personal voice)

**Job of this section:** echo the opener, deliver the quotable kicker, point at the artifact map as evidence.

### The closing arc (3 beats)

**Beat 1 (~50 words) — Echo the opener.**
If Hook A was used: bring the silent-regression story back. "The fix shipped May 20th — a depth gate that asks the agent before it writes 'does this output meet the bar?' That's the move. That's the bet, in one fix."
If Hook B was used: bring the dogfood result back. "I keep returning to the 23/25 because it's the only signal I trust on a meaning-layer tool. Builders should be willing to be measured by their own rubrics."

**Beat 2 (~70 words) — The quotable kicker (chairman synthesis line, lightly Sean-voiced).**
> I don't think the durable enterprise value is agents clicking around UIs. I think it's the semantic layer: typed work objects, scoped authority, memory provenance, reviewable decisions. I've shipped seven artifacts that back the bet. Five of them are live as of today. Two more ship before mid-June. The map is at seanwinslow.com/essays/meaning-over-access.

**Beat 3 (~30 words) — The signature line.**
> Access is the bridge. Meaning is the destination. That's where I'm spending the next four years. If that's the layer you're building, let's talk.

---

## 6. Supporting artifacts the manifesto generates

Per Task 13's spec, this manifesto's draft-lock ships with companion files:

- [ ] `docs/MEANING_OVER_ACCESS.md` — the canonical 1,500-word Markdown source
- [ ] `docs/diagrams/access-meaning-spectrum.mmd` — Mermaid source (above)
- [ ] `docs/diagrams/access-meaning-spectrum.svg` — pre-rendered SVG via `mmdc` for Substack image embed
- [ ] `docs/MEANING_OVER_ACCESS_EXPLANATION.md` — 4Q artifact (feeds Gap-Fill 3 ledger row)
- [ ] `~/Code-Brain/sw-ai-pm-portfolio/src/content/essays/meaning-over-access.mdx` — Astro syndicated copy
- [ ] `~/Code-Brain/sw-ai-pm-portfolio/src/pages/essays/index.astro` — new `/essays/` landing page
- [ ] `~/Code-Brain/sw-ai-pm-portfolio/src/pages/essays/[slug].astro` — dynamic essay route
- [ ] `~/Code-Brain/sw-ai-pm-portfolio/src/content/config.ts` — `essays` collection schema
- [ ] `vault/.../substack-drafts/2026-06-19-meaning-over-access-substack-cross.md` — Substack-formatted cross-post

---

## 7. DECISIONS LOCKED (2026-05-21)

Sean's answers captured from `open-question-answers-5-21.md`. All defaults except the JD-URL source decision, which Sean explicitly redirected to target-companies.md.

| # | Decision | Locked answer |
|---|---|---|
| 1 | Opener: Hook A (silent regression) or Hook B (dogfood)? | ✅ **Hook A.** Silent-regression story. Stronger narrative arc, earns the thesis turn. |
| 2 | All 7 plotted artifacts the right 7? | ✅ **Yes** — keep all 7 as drafted (intent-MCP, vault-knowledge MCP, concept_edges, cost caps, judge layer, eval suite, fleet observability). |
| 3 | Spectrum chart coordinates? | ✅ **Default** — Mermaid coordinates as drafted in §2. |
| 4 | Personal voice for sections 1 + 5? | ✅ **Default (strategic-sober with one dry beat per bookend)** for the initial pass. **NOTE — Sean's planned voice review:** after the full ~1,500-word draft lands in Step 2, Sean will pass it through the `writing-voice-modes` skill himself to tune tone before the draft-lock commit. The Step 2 draft is a strategic-sober first pass, not the final voice. |
| 5 | Role-map JD URLs source? | ✅ **Use target-companies.md** — Sean explicitly redirected here. URLs now populated in the §3 role-map table (Anthropic FDE / Glean FDP / Sierra + Decagon / Cohere; Manus/Adept named as negative-space). |
| 6 | Closing kicker — verbatim chairman synthesis or Sean-rewritten? | ✅ **Default** — lightly Sean-voiced. |

### Outstanding Step-2-time considerations (not blocking, but worth flagging when I draft)

- **Voice-review checkpoint:** the full draft Step 2 produces is *strategic-sober first*, not the final voice. After it lands, Sean runs the `writing-voice-modes` skill against it to tune cadence — particularly the bookend hooks (Sections 1 + 5). Step 6's "draft-lock review" gate is where the voice-tuned version is committed.
- **JD URL re-validation:** target-companies.md URLs were last validated 2026-05-13. Step 6 of Task 13 (publish-day verification) re-checks all 5 URLs for 200 OK. If any decay between draft-lock (5/23) and publish (~6/19), Step 6's fallback is to swap to that company's careers landing page + a 2026-05-13 snapshot saved at `vault/40_knowledge/references/role-map-2026-05-13-snapshots/` (snapshot dir to be created during Step 6).
- **The "essays" IA on the portfolio:** Task 13 Step 4 creates `~/Code-Brain/sw-ai-pm-portfolio/src/pages/essays/{index,[slug]}.astro` + the `essays` collection. Sean is simultaneously running the portfolio redesign per `sw-ai-pm-portfolio/CLAUDE.md`. Coordinate so the `/essays/` IA lands in his Phase 3 build (or as a parallel route in the V3 bridge). My Step 4 work assumes V3-bridge integration unless Sean signals Phase 3 has shipped.

---

## 8. Timeline + sequencing

| Day | Task | Hours | Output |
|---|---|---|---|
| **Today (5/20)** | Step 1 — this outline | 3 (done) | This document |
| **5/20-5/21 evening** | Sean reviews + answers the 6 open decisions | 0.5 | Decisions captured |
| **5/21** | Step 2 — full ~1,500-word draft pass | 6 | `docs/MEANING_OVER_ACCESS.md` |
| **5/21 evening** | Step 3 — Mermaid spectrum chart + SVG render | 2 | `docs/diagrams/access-meaning-spectrum.{mmd,svg}` |
| **5/22 morning** | Step 4 — `/essays/` IA + syndicated MDX | 4 | 4 portfolio files |
| **5/22 afternoon** | Step 5 — Substack cross-post + LinkedIn TL;DR | 3 | 2 files |
| **5/22 evening** | Step 6 — Draft-lock review + 4Q EXPLANATION.md | 3 | EXPLANATION.md + ledger row |
| **5/22 night** | Step 7 — Validate + commit + tag `gap-fill-2-draft-locked` | 1 | Commit |
| **5/23 EOD** | **Draft-lock gate passes** | | Task 13 draft-locked |
| **~6/19 Fri** | Step 8 — Publish Substack Post 3 + LinkedIn pin | 0.75 (Sean) | Manifesto live |

**Critical-path reality check:** Step 1 (this) is done. Steps 2-7 collapse into a single 3-day window (5/20 evening → 5/22 EOD). Step 8 is calendar-time, gated on Substack Posts 1 + 2 shipping first per the publishing cadence.

---

## 9. Interview talking points (the why behind the why — carry these forward)

These are the meta-arguments you should be able to deliver in 60 seconds each:

**"Why publish a manifesto when you have working artifacts?"**
> Theses get callbacks; tools get bookmarked. A hiring manager who reads my GitHub sees seven tools. A hiring manager who reads the manifesto sees a thesis with seven pieces of evidence. The manifesto turns the work I've already done into an argument they can have an opinion about.

**"Why this manifesto instead of (e.g.) 'How I built my agent fleet'?"**
> Process posts are interchangeable. Most AI PMs can write "how I built." A bet-and-defend post is harder to fake because it requires the work to exist as evidence. This one cites seven shipped artifacts; it would be brittle to write without them.

**"Why now and not six months ago?"**
> Six months ago the artifacts didn't exist. The manifesto is downstream of the work, not upstream of it. The chairman of my LLM council called this out explicitly — the thesis was always in the artifacts; the missing piece was framing them as a single bet.

**"Why call it 'meaning over access' instead of inventing new language?"**
> Citation discipline. Nate Jones published the access/meaning framing on May 5th. My value-add is showing what a meaning-layer stack actually looks like, not coining the term. Building on someone else's frame and crediting them is a higher-trust signal than inventing my own and isolating myself from a conversation that's already happening.

**"What's the risk if the bet is wrong?"**
> Concrete and bounded. If meaning-layer agents lose to access-layer agents, the seven artifacts still work — they just won't be the differentiating thing. The downside is being early; the upside is being correctly early. I'd rather be wrong on a specific bet I can defend than vague enough to be unfalsifiable.

---

*End of outline. Sean: answer the six open decisions in §7 (or just say "all defaults") and I expand into the full 1,500-word draft as Step 2.*
