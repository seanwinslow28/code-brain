# The Tool-Shipping Playbook

> The repeatable engine behind VoicePrint, written down so the next build is faster and
> the Substack series has a spine. The one-line version: **find a real pain point →
> ship a friction-killing tool → write the story → repeat.** Each turn of the loop
> feeds three things at once: the marketplace (a shipped plugin/MCP), the portfolio (an
> artifact), and the Substack (a post). That triple-payout is the whole point.

This is domain-agnostic, but it's aimed at the space Sean is betting on: creative tools,
SaaS, UX/UI, and marketing teams shifting into AI, and the people inside them who need a
helping hand making that shift.

## The flywheel

```
  pain point  ──►  shipped tool  ──►  the story (Substack)
      ▲                  │                    │
      │                  ▼                    ▼
   research          portfolio            audience
   (next idea)        artifact          (next pain point)
```

Every loop should leave behind an installable thing, a portfolio entry, and a post.
If a build only produces one of the three, you under-monetized the work.

## The seven steps (what we actually did)

### 1. Research first — find and *validate* a real pain point
- Run the trio: **`last30days`** (the sharpest — real Reddit/X/YouTube complaints, run it on the machine with the keys), **web search** (landscape + listicles), and a **deep pass** (verified, cited) for competitive depth.
- Hunt for three things specifically: **pain points** people repeat, **underappreciated skills** (high value, low adoption), and **what people are screaming for** (verbatim "I wish X existed").
- Mine the gaps with one blunt prompt: *"From the research — not from what I'm telling you — what are the loudest unmet needs and the gaps nobody's filling? Quote the exact words. Be blunt about what's hard."* The "tell me what works against me" framing is what gets you contrary signal instead of a cheerleader.
- **The discipline that matters most:** do NOT research your *moat*. If you already have a validated method or asset, external research will only surface weaker generic advice and dilute it. Research the *market*, not the *method*. (We deliberately did not research "how to capture a voice" — that was already earned.)

### 2. Separate table stakes from the wedge
- The marketplace is crowded and growing. Whatever the obvious framing is ("write like me," "build a skill," "another MCP"), assume it's **table stakes** — someone already owns it (Skill Creator owns "build a skill"; Grill Me owns "interview me").
- Your defensibility is the thing nobody else does. For VoicePrint it was *learn-from-what-you-reject* + *works-with-no-corpus* + *honest-loop* + *local/free*. Name the wedge explicitly and lead every artifact with it.
- Friction-killer test (from the MCP doctrine): *every tool exists because it killed a specific friction.* If you can't name the one friction in a sentence, it's a feature dump.

### 3. Scope with the human before building
- Lock the decisions that change the build (where it lives, scope, the one or two opinionated calls) via a few sharp multiple-choice questions. Don't build on assumptions.
- Write the plan down (a BUILD-PLAN that lives with the code). Get a yes on the *shape* before spending a single build session.

### 4. Build in checkpointed chunks
- Decompose into chunks with a visible task list; check in at each boundary, pause at the high-taste ones (the part where the human's judgment matters most — for VoicePrint, the interview craft).
- Validate continuously (`claude plugin validate`, a repo validator, unit tests, `py_compile`). Green between chunks, not just at the end.
- Keep the moat's principle load-bearing in the build, not just the pitch. (VoicePrint's "samples win over rules" is the drift defense AND the marketing.)

### 5. Ship a proof — answer "how do you know it works?"
- The technical crowd dismisses tools that can't show a measurable before/after ("naive testing doesn't provide any confidence"). Build the proof *in*, locally, no API key: a deterministic signal the user can watch (VoicePrint's burstiness fingerprint + shrinking edit-diffs).
- A proof is also counter-positioning: while competitors promise "80% on the first pass," you *show* convergence and set honest expectations.

### 6. Dogfood a stranger — the two gates
- Before "it works," prove it works for someone who is **not you**. Run a deliberately opposite persona end-to-end.
- **Gate 1 — zero leakage:** a deterministic grep for your own fingerprints over the generated output. If your tool personalizes, none of *you* may end up in *their* result.
- **Gate 2 — distinctness:** an **independent subagent** audits whether the output reads as one specific person vs. a template (a fresh agent has no stake in it being good). The dogfood's job is to *find the over-reach* — ours caught two template bugs we then fixed for every future user. A dogfood that finds nothing wasn't skeptical enough.

### 7. Package, capture, and tell the story
- Ship the installable cleanly (exclude dev docs + dogfood artifacts from the package; keep them in the source repo as provenance).
- Capture every deferred follow-up as a ticket before you wrap (real-human dogfood, marketplace repo, the launch post).
- Write the post *from the build*, not after it. The honest build narrative — including what the dogfood caught — is the most credible content you can publish, and it doubles as a hiring signal (judgment shown, not claimed).

## Distribution notes (how the tool actually gets found)
- Install happens from the **official** + **community** marketplaces; **discovery** is social-first (a YouTube/Reddit listicle or a thread → a named tool → a copy-paste install). Ship as a **GitHub marketplace repo** (`marketplace.json`), not only a `.plugin`.
- **Install-count + maintainer reputation are the trust currency.** A new solo tool has neither — so trust has to come from elsewhere: a clean "will install" manifest (VoicePrint ships *no* MCP/hooks/connectors — pure local), a transparent build story, and a one-screen before/after demo.
- The market is security-anxious about plugins that touch accounts/cloud. **Local-only / no-API-key is a feature, not a footnote.**

## The Substack throughline
Every loop is a post, and the posts compound into a position: *the person helping creatives, SaaS, UX/UI, and marketing teams actually make the shift into AI — by shipping the small tools that kill their specific frictions and showing the work.* Lead with the pain (their words), show the build (honest, including failures), hand them the tool. The ask lands sideways; the work is the pitch.

## Anti-patterns (how this engine fails)
- **Researching the moat** → dilutes the one thing that's yours.
- **Leading with the table-stake** → you become tool N+1 in a 9,000-tool list.
- **No proof** → dismissed on sight by the people whose opinion travels.
- **Skipping the stranger dogfood** → you ship something that only works for you and find out in public.
- **Building three tools and writing zero posts** → you did the hard part and skipped the payout.
