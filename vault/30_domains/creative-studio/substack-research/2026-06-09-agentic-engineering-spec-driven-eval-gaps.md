---
title: "Agentic Engineering — Spec-Driven Development & Evals: Intent / Eval / Governance Gaps (companion pass)"
type: research
status: complete
domain: [creative-studio]
tags: [agentic-engineering, spec-driven-development, evals, eval-driven-development, intent-engineering, governance, human-in-the-loop, mcp-servers, market-gaps, voiceprint, last30days, research, opportunity]
created: 2026-06-09
last-updated: 2026-06-09
date-range: 2026-05-10 to 2026-06-09
sources: [reddit, x, youtube, tiktok, instagram, hackernews, github, web]
coverage: "123 items across 8 sources — Reddit (15 threads, signal-noisy), X (24 posts), YouTube (1 video), TikTok (19 videos, 113K views), Instagram (9 reels), Hacker News (23 stories, 1,636 pts / 955 cmt), GitHub (22 PRs/issues), Web (10 pages + 10 WebSearch supplements). One planned pass + 3 WebSearch supplements."
tool: "/last30days v3.3.0 (model-authored --plan, 8 targeted subreddits, x-related=HamelHusain,sh_reya)"
ai-context: "Companion to [[2026-06-09-agentic-engineering-intent-eval-governance-gaps]] (which mined the 'frustrations building AI agents' pass). This one mines the DISCOURSE pass — 'spec-driven development and evals for AI agents' — and reads it along the same three axes: INTENT (make agents do what the human meant), EVAL (prove they did), GOVERNANCE (keep a human in control). Where the frustrations pass surfaced failure modes (statefulness, ghost-debugging), this pass surfaces the methodology the field is converging on (Spec Kit, eval-driven development, 'grade outcomes not paths', pass^k, judge calibration) AND the live backlash against it ('Waterfall in Markdown'). Part 2 ranks gaps by frequency x unservedness, tagging Sean-niche vs NOT-Sean. Part 3 maps to two SHIPPED MCPs — intent-engineering (@swins/intent-engineering-mcp; thesis: the audit IS the eval) and vault-knowledge (typed reasoning edges) — plus the writing chain, VoicePrint, design-team agents. Part 4 = clean-sheet builds biased to gates and lenses, deliberately NON-overlapping with the frustrations-pass build list. The corpus is engineer/builder-skewed; the creative slice is re-aimed from engineer-voiced gaps. Confidence: medium. Feeds the combined opportunity report + Substack series."
related: [2026-06-09-agentic-engineering-intent-eval-governance-gaps, 2026-06-09-claude-code-skills-mcp-gaps-and-opportunities, 2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days, 2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days, tool-shipping-playbook, voiceprint-plugin-build-spec]
---

# Agentic Engineering — Spec-Driven Development & Evals (companion pass)

> Research across **123 items / 8 sources** (Reddit 15, X 24, YouTube 1, TikTok 19, Instagram 9, Hacker News 23, GitHub 22, Web 10 + 10 supplements), 2026-05-10 → 2026-06-09. Query: *"spec-driven development and evals for AI agents."* Model-authored query plan; 8 targeted subreddits; `x-related=HamelHusain,sh_reya`. Raw corpus: `~/Documents/Last30Days/spec-driven-development-and-evals-for-ai-agents-raw-v3.md`.
>
> This is the **discourse companion** to [[2026-06-09-agentic-engineering-intent-eval-governance-gaps]]. That report mined *what makes agents fail* (the frustrations pass); this one mines *the method the field is adopting to fix it* — spec-driven development and evals — and the **backlash** against that method. Same three axes (intent → eval → governance), different corpus. Read them together: the frustrations pass is the symptom, this pass is the prescription-and-its-side-effects. Both deepen the creative-AI niche covered by [[2026-06-09-claude-code-skills-mcp-gaps-and-opportunities]], [[2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days]], and [[2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days]].

## Quick verdict

The field has named its own fix out loud: **"vibe coding is out, spec-driven development is in"** — write a spec the agent must obey, then prove it obeyed with evals. The spec side has a gravitational center ([GitHub Spec Kit](https://github.com/github/spec-kit)) and the eval side has a canonical rule (Anthropic: **"Don't grade the path the agent took, grade what it produced"**). But three things are wide open. (1) **Nobody helps a human author a good spec** — the cost of getting intent across is itself the unsolved problem (*"it takes too much effort to help AI comprehend what exactly you want"*). (2) **Every eval in the corpus is a code test** — there is no spec-bound eval for subjective output (voice, brand, taste). (3) **Human review can't keep pace with agent output**, and the loudest governance signal in the pull is a developer quitting: *"I won't be reviewing AI generated PRs."* The infrastructure (Spec Kit, eval harnesses, CI plumbing) is taken or commoditizing; the **human-interface layer — define intent, prove it for non-code output, gate it fast enough that nobody disables the gate — is empty for anyone who isn't a backend engineer.** Sean's shipped **[[intent-engineering]] MCP** ("the audit *is* the eval") sits on gaps 1–2; the **writing chain + design-team agents** already *are* the spec-bound creative eval the market lacks.

---

# Part 1 — What people are converging on (and fighting about)

The corpus splits into a dominant **adoption narrative** (spec + eval is the answer), a **methodology consensus** (how to actually do evals), and a **backlash** (it's just waterfall). Organized by the three axes.

## Backdrop — the frame shift everyone is repeating

"Vibe coding → spec-driven development" is the meme carrying the whole topic. The sharpest articulation, [@itsallykrinsky](https://www.tiktok.com/@itsallykrinsky/video/7643950991301283086) (173 likes, 4.4K views): a PRD is "written for humans, full of rationale and business framing," but *"a spec is how the agent should think about building this — it is the context your AI needs to stay consistent across every single session."* [GitHub Spec Kit](https://github.com/github/spec-kit) is the lightning rod — a launch reaction video framed it as *"GITHUB JUST FIXED VIBE CODING… forces AI agents to create a structured spec before writing any code"* ([@whitewhoadie](https://www.tiktok.com/@whitewhoadie/video/7641607143535152398), 736 likes). The deeper "why" (per [Towards Data Science](https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/)): *"AI agents are stateless… effectively starting our communication from scratch."* The spec is the durable intent artifact that survives that.

## Axis A — INTENT: define what "right" means before the agent runs

- The root-cause quote of the whole topic, [Medium / "Definitive Guide"](https://medium.com/predict/spec-driven-development-with-ai-coding-agents-the-definitive-guide-453fba1baf39): *"The root cause is not the AI. It is the absence of a disciplined framework for communicating intent to the agent."*
- The cost of doing that is named as the live pain — [@wangxian0](https://x.com/wangxian0/status/2063466407694913920): *"do you feel it takes too much effort to help AI comprehend what exactly you want?… I think it's more of a collaborative work problem, not a software development problem or product management problem."* That is the elicitation gap, said in the wild.
- The failure when intent is vague — [@aidevquicktips](https://www.tiktok.com/@aidevquicktips/video/7644095035369295112) (733 likes): *"when project scale inconsistency appears, the logic is duplicated, abstraction is broken, and no AI knows."*
- The emerging definition, [Augment Code](https://www.augmentcode.com/guides/what-is-spec-driven-development): SDD *"converts AI agent ambiguity into executable contracts"* via a six-element spec (outcomes, scope, constraints, prior decisions, task breakdown, verification criteria).
- The open question developers are literally asking — [Ask HN: "Do you give AI agent the specs and have it start building unattended?"](https://news.ycombinator.com/item?id=48364162) Nobody has a settled answer.

## Axis B — EVAL: prove the agent did the thing

- The canonical, highest-authority rule, [Anthropic Engineering, "Demystifying evals for AI agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): **"Don't grade the path the agent took, grade what it produced."** Avoid forcing tool-call order; grade the outcome against the spec.
- The field knows evals are now the center of gravity — and one voice calls it a dodge: [@zhitong45](https://x.com/zhitong45/status/2063830029973483668): *"The AI Industry Has Pivoted to Evals — and Is Dodging the Real Question."*
- The demo-to-production chasm, [sarang.tech](https://www.instagram.com/reel/DYOpGyzx5um/): *"your demos are beautiful, but in production, your agent crashes."* The eval-pipeline definition that answers it, [digitalapplied](https://www.digitalapplied.com/blog/ai-agent-evaluation-pipeline-2026-testing-methodology): the system that decides *"whether your agent actually works — not in a demo, but across the full distribution of real inputs it will meet in production."*
- The methodology consensus is remarkably tight across the long-form sources: golden dataset built from real production failures; calibrate the LLM-judge to **"75–90% agreement with human labels before you scale it"** ([getmaxim](https://www.getmaxim.ai/articles/building-a-golden-dataset-for-ai-evaluation-a-step-by-step-guide/) / [Arize](https://arize.com/llm-as-a-judge/)); deploy as *"three triggers, three jobs — the PR gate is the merge decision, the nightly batch is the drift detector, the canary is the live-traffic guardrail"* ([Latitude](https://latitude.so/blog/ultimate-ci-cd-llm-evaluation-guide)); measure **pass^k** (all k attempts succeed) over pass@k (best case).
- Even imperfect judges help — [TensorZero, HN](https://www.tensorzero.com/blog/even-very-noisy-llm-evaluators-are-useful-for-improving-ai-agents/): *"Even (very) noisy LLM evaluators are useful for improving AI agents."*
- The origin story everyone cites, [Cameron Wolfe](https://cameronrwolfe.substack.com/p/agent-evals) quoting Claude Code: evals came *"first for narrow areas like concision and file edits, and then for more complex behaviors like over-engineering"* — i.e., evals lag shipping, and you bootstrap them.
- The literacy gap underneath it all: non-engineers are still being taught what an eval *is* — [kaicalls](https://www.tiktok.com/@kaicalls/video/7645365305497193742): *"'Evals' are like practice tests that help AI agents perform well before they are used for real tasks."*

**Every eval artifact in this corpus is a code test or an engineer's harness.** None evaluate "did it do what I *meant*" for prose, design, or a campaign.

## Axis C — GOVERNANCE: keep a human in control

- The loudest governance signal is a capitulation — [r/ExperiencedDevs, "Today I announced that I won't be reviewing AI generated PRs at company meeting"](https://www.reddit.com/r/ExperiencedDevs/comments/1towli9/today_i_announced_that_i_wont_be_reviewing_ai/) (1,839 upvotes / 444 comments). Review volume broke the human.
- The control-via-coverage reflex, [@garrytan](https://x.com/garrytan/status/2054064931515855118) (792 likes): *"The AI Agent Complexity Ratchet: Why 90% Test Coverage Is Required."*
- The accountability stance, [enunomaduro](https://www.instagram.com/reel/DZKWkAzqn2C/): *"Agentic coding is not vibe coding… every single line generated by your prompts to AI will be generated by you."*
- The management-tooling gap, [@mickyarun](https://x.com/mickyarun/status/2062170009284288595): *"Sprints. Scrum. Standups. Planning poker. Jira boards no one updates. None of it was built for a team where AI writes the first draft, estimates the work, and tests the code… They kept snapping back to 2010."*
- The enterprise reality check, Gartner (via [HN](https://www.gartner.com/en/newsroom/press-releases/2026-05-26-gartner-says-applying-uniform-governance-across-ai-agents-will-lead-to-enterprise-ai-agent-failure)): *"40% of Enterprises Will Demote or Decommission Autonomous AI Agents,"* and uniform governance *"will lead to enterprise AI agent failure"* — i.e., governance has to be **fitted**, not uniform.
- The security edge, [HN: "Open source project contains hidden instruction for 'AI' agents: delete my code"](https://www.osnews.com/story/145130/) and the provenance reflex appearing in PR templates — [SENTINEL-CLI](https://github.com/KunjShah95/SENTINEL-CLI/pull/23): a checkbox, *"I wrote this code myself (not generated by an AI agent without human review)."*
- The sober production verdict, [r/AI_Agents](https://www.reddit.com/r/AI_Agents/comments/1tlgz6o/after_6_months_of_running_ai_agents_in_production/): after six months in production *"the framework you pick barely matters — the thing that kills them is something else"* (context, data, verification discipline).

## The backlash (weigh before building on it)

The spec narrative has a loud counter-movement: ["Spec-Driven Development Is Waterfall in Markdown"](https://medium.com/@iamalvisng/spec-driven-development-is-waterfall-in-markdown-e2921554a600), ["It isn't broken — it will collapse"](https://cafeai.home.blog/2026/05/19/spec-driven-development-isnt-broken-it-will-collapse/). The substance, [Antony Marcano](https://ideas.riverglide.com/what-almost-everyone-gets-wrong-about-spec-driven-development-with-ai-70ab457d15ec): people write exhaustive specs *"because that's what 'thorough' looks like in training data — this accidentally recreates waterfall's big upfront design problem."* The strongest defense, [Marc Brooker](https://brooker.co.za/blog/2026/04/09/waterfall-vs-spec.html): when regenerating from an updated spec costs ~nothing, *"the feedback loop collapsed from six months to twenty minutes,"* which is what waterfall never had. **Implication for builds:** the win is not "generate a giant spec," it's "keep a *small, living* spec honest" — a lens, not a generator.

---

# Part 2 — The gaps nobody is filling

> Ranked by **frequency in the corpus × how unserved it is.** Quotes verbatim. Tagged **Sean-niche** (intent/eval/governance judgment, creative-team-facing — per the [[tool-shipping-playbook]] guardrail) or **NOT-Sean** (orchestration/observability/CI infra = capital + eng play). Confidence **medium**: single planned pass + supplements; engineer/builder-skewed; creative slice re-aimed from engineer-voiced gaps.

### Gap 1 — Nobody helps a human *author* a good spec (highest frequency × emptiest) — **Sean-niche**
The whole field agrees the spec is the answer, and simultaneously admits writing one is the unsolved part: *"the absence of a disciplined framework for communicating intent to the agent"* and *"it takes too much effort to help AI comprehend what exactly you want."* Spec Kit gives you a *template*; nothing helps a non-engineer get their actual intent into it.
**Hard to build because:** the hardness is *human* — eliciting intent (and taste) from someone who can't write a spec, and turning "make it pop" into a checkable artifact. That's interview-design + UX, which is exactly why no infra vendor touches it and why it's solo-buildable. The trap: a thin reformatter that just prettifies vague input is worthless; the value is the elicitation and the audit.

### Gap 2 — There is no spec-bound eval for *subjective* output — **Sean-niche**
High frequency, near-zero service for non-code. The eval methodology is mature for code (golden datasets, judge calibration, pass^k), and Anthropic's *"grade what it produced"* is the right rule — but every artifact in the pull grades code or tool-calls. For voice, brand, and design there is no pass/fail. The market is still *defining* evals for laypeople (*"evals are like practice tests"*), let alone scoring taste.
**Hard to build because:** the eval *is* the product — for subjective output you need a measurable rubric or it collapses to vibes, and judges must be calibrated (*"75–90% agreement with human labels"*) before anyone trusts the score. This is the single highest-skill item, and the one Sean has the most proof on (the writing-critique analyzer + Cheese-Gauntlet).

### Gap 3 — Human review can't scale with agent output (reviewable-by-design) — **Sean-niche (team slice) / NOT-Sean (enterprise compliance)**
The loudest governance pain in the pull is review volume breaking the human: *"I won't be reviewing AI generated PRs"* (1,839↑), and the control reflex of demanding *"90% Test Coverage."* The enterprise/regulatory version (Gartner, EU AI Act, fitted governance) is a consultancy + big-co build → **NOT-Sean.** The **fast, clear approval gate sized for a 5-person studio** — so the human checkpoint survives instead of getting disabled — is unbuilt → **Sean-niche.**
**Hard to build because:** generation parallelizes; review does not. A gate only survives if review is *fast enough* that people don't switch it off to get their automation back. The product is the speed/clarity of the checkpoint, not the checkpoint.

### Gap 4 — On-brand / on-voice judges that are *calibrated*, not vibes — **Sean-niche**
A specialization of Gap 2, called out separately because the methodology exists and nobody has applied it to creative domains. *"Even (very) noisy LLM evaluators are useful"* and the calibration bar (*"75–90% agreement"*) are documented — but only for code/factual tasks. A calibrated "does this sound like the client / fit the brand system" judge is the unclaimed square.
**Hard to build because:** you need a labeled gold set of the target voice/brand to calibrate against, and *"ghost debugging"* (non-determinism) means single-run scores need confidence bands. Without calibration it's another humanize-skill that dies at "less-robotic-average."

### Gap 5 — Keeping the spec *small and living* (anti-drift) — **Sean-niche, but genuinely hard**
The backlash names the real failure: exhaustive specs recreate waterfall, and *"spec drift"* lets the spec and reality diverge. Nobody ships the discipline tool that keeps a minimal spec honest as the work changes.
**Hard to build because:** it's an incentive/discipline problem, not a code problem — a tool can surface drift but can't supply the judgment to resolve it. Risk of building a nag nobody runs.

### Gap 6 — AI-native project/process tooling — **NOT-Sean (big build)**
Real and loud (*"None of it was built for a team where AI writes the first draft… they kept snapping back to 2010"*) but this is a Jira-replacement — a capital + team build, not a solo gate/lens. Note it; don't build it.

### Gap 7 — Eval harnesses, judges-as-a-service, CI plumbing, observability — **NOT-Sean**
Spec Kit, MLflow, Confident AI/DeepEval, W&B Weave, Arize, LangSmith, Vercel AI Gateway (*"3.5% of AI requests fail"*), the *"three triggers, three jobs"* CI pattern — all funded and commoditizing. High frequency, low unservedness. Skip. (If the buyer is a platform engineer or the deliverable is a dashboard, walk away.)

### Overlap flag (don't repeat the sibling reports)
- **vs [[2026-06-09-agentic-engineering-intent-eval-governance-gaps]] (frustrations pass):** same three axes, same Sean-niche verdict — that report reached it from *failure modes* (statefulness, ghost-debugging, "correct behavior was never defined"); this one reaches it from *the adopted method and its backlash* (Spec Kit, eval-driven development, "Waterfall in Markdown"). The convergence from two independent corpora **raises confidence** that Gaps 1–3 are real. New material this pass adds: the **calibrated-subjective-judge** gap (#4), the **anti-drift / small-living-spec** gap (#5), and the **pass^k / judge-calibration methodology** Sean can borrow wholesale. Do not re-rank the frustrations report against this one; merge them in Step 4.
- **vs [[2026-06-09-claude-code-skills-mcp-gaps-and-opportunities]]:** Gaps 2–4 are the agentic root cause of that report's "write like me," "brand-lock," and "Approval-Gate Publisher" items. This pass supplies the *eval methodology* (calibration, pass^k, grade-the-outcome) that report didn't cover.

---

# Part 3 — How Sean is positioned

> Mapped to **shipped** assets, leading with the two MCPs. No capabilities beyond what's listed.

## Priority 1 — Point [[intent-engineering]] MCP at Gap 1 + Gap 2 (the flagship fit)
The corpus's #1 and #2 gaps — *"the absence of a disciplined framework for communicating intent"* and the missing spec-bound eval — are exactly what the intent-engineering MCP addresses. Its three tools (`audit_intent_spec`, `generate_intent_spec_scaffold`, `assess_retrofit_level`) operationalize **"evals are the new PRDs,"** and its thesis — **the audit *is* the eval**: it scores a spec against the framework *before* that spec ships to a coding agent — is the direct answer to Anthropic's *"grade what it produced"* moved one step earlier (grade the *spec* before you spend a token).
- **Action:** position it as the **define-correct-before-you-build** layer, not a dev tool. Landing-page quote, verbatim from the market: *"it takes too much effort to help AI comprehend what exactly you want."* `generate_intent_spec_scaffold` answers Gap 1 (capture intent); `audit_intent_spec` answers Gap 2 (prove the spec is checkable). `assess_retrofit_level` is the **anti-drift** hook for Gap 5 — it's how you keep a *small living* spec instead of a waterfall doc.
- **Honest risk:** today it's packaged for engineers (npm `@swins/intent-engineering-mcp`, MCP registry). The creative-team front-end — an interview that emits a spec a non-coder can read — is *not yet built*, and that front-end is the hard, defensible part (Gap 1's elicitation problem). Without it, this stays a dev tool.

## Priority 2 — The writing chain + design-team agents already *are* the spec-bound creative eval (Gap 2 + Gap 4)
This is the asset the market is most starved of and Sean most uniquely has. The corpus keeps reinventing "submit to a reviewer sub-agent, human approves." Sean shipped that as judgment gates years before the meme: [[writing-critique]] → [[writing-humanity-pass]] is a **spec-bound eval for prose** (it scores against a voice spec — precisely the "did it do what I meant" eval the market lacks for non-code), and the design-team agents (UI Reviewer, Design System Enforcer, Visual Polish Auditor, Accessibility Checker) are **calibrated brand/quality gates for UI** — the creative answer to Gap 4.
- **Action:** market these as the creative-native answer to the "glorified validator" anxiety — *the review step is the product.* Borrow the engineer methodology wholesale: present the Cheese-Gauntlet as the **calibration set** (the "75–90% agreement with human labels" proof) and report scores with confidence bands to neutralize the "ghost debugging" / vibes objection.
- **Honest risk:** subjective evals are the hardest item in the whole dataset; if the score reads as vibes it dies like the 16-install humanize skills the sibling report flagged. Lead with calibration evidence, not adjectives.

## Priority 3 — [[vault-knowledge]] MCP for the provenance/anti-drift edge — **only the defensible slice**
The memory/observability frustration is infra (NOT-Sean), but vault-knowledge owns the one non-commodity part: **typed reasoning edges** (`concept_edges`: supports / contradicts / evolved_into / supersedes / depends_on / related_to). That is the layer that answers Gap 5's drift and the governance need to trace *why* — a vector store says "what's similar"; typed edges say "what contradicts what, and what superseded it."
- **Action:** frame it as **decision/provenance memory** for creative work — "why did the agent write/design it this way, and which brand rule does that trace to" — not "another memory server."
- **Honest risk:** sits adjacent to the funded memory-infra race (Gap 7). Stay on typed-edges + provenance; never drift into building a general memory store.

## The throughline
Sean owns the **judgment / intent / ownership** half of all three axes and is badly positioned for the **harness / CI / orchestration** half — and *two independent corpora now agree* the valuable half is the human-interface one. The asset he already shipped (intent-engineering: *the audit is the eval*) sits on the loudest, emptiest gap. The work is **translation, then calibration**: re-skin the engineer-framed intent→eval→gate loop for writers/designers/marketers, and prove the subjective judge is calibrated rather than vibes.

---

# Part 4 — What to build (clean-sheet ideas)

> Grounded only in the gaps above. Bias: **gates and lenses, not generators.** Deliberately **non-overlapping** with the frustrations-pass build list — these lean on what *this* pass uniquely surfaced (calibration, pass^k, grade-the-outcome, small-living-spec). Each names its gap and the genuinely hard part. All creative/SaaS/UX/marketing-facing.

### 1. Spec Audit for non-coders — "is this brief checkable before you run the agent?"
**Gap 1 + Gap 2.** A front-end on [[intent-engineering]]'s `audit_intent_spec` that takes a marketer's/PM's brief and returns *"these 4 clauses are unmeasurable — an agent will exploit them"* before any generation. The creative version of grading the spec, not the output. Directly productizes "the audit *is* the eval."
**Hardest part:** the elicitation (Gap 1's unsolved 80%) — turning "make it pop" into clauses an audit can score. Reformatting is the easy 20%.

### 2. Calibrated Voice/Brand Judge Kit — borrow the engineer methodology, aim it at taste
**Gap 4.** Ship the on-brand/on-voice eval *with its calibration harness*: a small labeled gold set (the Cheese-Gauntlet pattern), a documented "% agreement with human labels," and pass^k-style confidence bands so a single run isn't trusted blindly. The thing MLflow/Confident AI will never build because their rubric is code, not voice.
**Hardest part:** assembling and maintaining the labeled gold set of the target voice; the judge is only as trustworthy as its calibration.

### 3. Reliability Card for creative output — pass^k for words/designs
**Gap 2 + Gap 4.** Run the agent k times against the spec and report *"3 of 5 drafts held the voice"* instead of a single green check — the creative translation of pass^k (*"whether all k attempts succeed"*). Turns non-determinism from a hidden risk into a visible reliability number a creator can act on.
**Hardest part:** defining the per-attempt pass criterion measurably for subjective output (depends on #2's calibrated judge).

### 4. Small-Living-Spec Lens — kill the "Waterfall in Markdown" failure mode
**Gap 5.** A lens (not a generator) that flags when a spec has drifted from the work, or bloated past the point of usefulness — operationalizing `assess_retrofit_level` for creators. Answers the strongest backlash critique head-on: keeps the spec *small and current* so the twenty-minute feedback loop survives.
**Hardest part:** measuring "drift" and "bloat" without a labeled corpus, and resisting becoming a nag people disable.

### 5. Fast Editor-in-the-Loop Gate for small studios
**Gap 3 (team slice).** Generated content can't publish until it clears the calibrated voice/brand/fact gates **plus** a one-click human approval — sized for a 5-person studio, not a bank. The honest, non-enterprise answer to "the human stays in control."
**Hardest part:** review has to be *fast* or it gets switched off; the product is the speed of the checkpoint. (Pairs with the sibling report's "Approval-Gate Publisher" — converge, don't duplicate.)

**Pattern across all five:** every buildable win is a **gate or a lens** on the intent→eval→control chain, and each leans on the one thing this pass uniquely contributes — the engineer eval *methodology* (calibration, pass^k, grade-the-outcome) re-aimed at subjective creative output. The two MCPs already cover the spine (intent-engineering = define + audit + retrofit; vault-knowledge = provenance/typed-edges); the rest is the creative-facing, *calibrated* front-end the engineer ecosystem structurally won't build.

---

## Methodology & sources

- **Tool:** `/last30days v3.3.0`, concept query, model-authored `--plan` (4 subqueries), `--subreddits=LocalLLaMA,MachineLearning,AI_Agents,ClaudeAI,ChatGPTCoding,PromptEngineering,ExperiencedDevs,OpenAI`, `--x-related=HamelHusain,sh_reya`. 123 items, 2026-05-10 → 2026-06-09. Pass: *"spec-driven development and evals for AI agents."* Plus 3 post-engine WebSearch supplements (SDD backlash, eval-driven-development methodology, how Anthropic/OpenAI eval agents). Raw dump: `~/Documents/Last30Days/spec-driven-development-and-evals-for-ai-agents-raw-v3.md` (WebSearch supplements appended).
- **Sources:** Reddit (15 threads — **signal-noisy**; several high-upvote items, e.g. Forza Horizon / "dehydrating for our AI overlords," were keyword-collision noise dropped from synthesis), X (24 posts, 1,646 likes), YouTube (1 video, 26K views), TikTok (19 videos, 113K views), Instagram (9 reels, 123K views), Hacker News (23 stories, 1,636 pts / 955 cmt — the strongest signal layer for this topic), GitHub (22 PRs/issues), Web (10 pages + 10 supplements: Anthropic, MLflow, Confident AI, W&B, Cameron Wolfe, Augment, Towards Data Science, digitalapplied, Latitude, getmaxim, Arize, Kiro, Tessl, Brooker, RiverGlide, sudoish). Polymarket + Threads returned nothing.
- **Top voices:** [@itsallykrinsky](https://www.tiktok.com/@itsallykrinsky/video/7643950991301283086) (TikTok, "spec is the agent's context"), [@wangxian0](https://x.com/wangxian0/status/2063466407694913920) (X, intent-cost), [@garrytan](https://x.com/garrytan/status/2054064931515855118) (X, 90%-coverage), [r/ExperiencedDevs](https://www.reddit.com/r/ExperiencedDevs/comments/1towli9/) (won't-review-AI-PRs), [Anthropic Engineering](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (grade-the-outcome), Hacker News (Spec Kit / eval-driven-dev Show HNs).
- **Confidence: medium.** (1) One planned pass + supplements, not the kit's full three — but it **converges with** the independently-run frustrations pass ([[2026-06-09-agentic-engineering-intent-eval-governance-gaps]]) on the same Sean-niche verdict, which raises confidence on Gaps 1–3. (2) Corpus is engineer/builder-skewed; the creative/SaaS/UX/marketing slice is **re-aimed from engineer-voiced gaps, not directly observed** — the team-adoption pass (*"how creative and marketing teams are adopting AI agents"*) would harden it. (3) Web/supplement findings are search-synthesized and attributed by publication; Reddit/X/TikTok/HN quotes are verbatim. (4) Reddit retrieval was noisy on this concept query (keyword collisions); HN, GitHub, X, and the long-form web were the load-bearing sources.
- **Companion + related:** [[2026-06-09-agentic-engineering-intent-eval-governance-gaps]] (frustrations pass — merge in Step 4), [[2026-06-09-claude-code-skills-mcp-gaps-and-opportunities]], [[2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days]], [[2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days]], [[tool-shipping-playbook]], [[voiceprint-plugin-build-spec]], [[intent-engineering]], [[vault-knowledge]].
