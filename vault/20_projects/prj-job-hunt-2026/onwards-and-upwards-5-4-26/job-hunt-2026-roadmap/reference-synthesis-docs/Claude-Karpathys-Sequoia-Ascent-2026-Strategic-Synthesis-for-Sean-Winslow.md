## **Karpathy's Sequoia Ascent 2026 — Strategic Synthesis for Sean Winslow**

### **Executive Summary**

Karpathy's December 2025 inflection is real and structural — agents crossed a coherence threshold and the unit of programming shifted from a function to a paragraph. The thesis with the most actionable consequences for you is **verifiability \+ lab attention** as the predictor of where AI will move next, because The Block sits on top of one of the most natively verifiable economic domains on earth (crypto data) and almost nobody has built proper RL environments for it yet. Two of your active projects are perfectly aligned with the trend (Code-Brain as agentic-engineering scaffolding; agentic financial-research fleet as a verifiable RL loop in waiting); one (16BitFit's sprite-consistency blocker) is fighting a battle Karpathy's framework explicitly predicts is hard right now and your pause on April 20 was strategically correct. The single highest-leverage move I'd argue for: **stop building skills and start building MCP servers** — the Code-Brain at 114 skills is hitting an architectural ceiling that Anthropic's December 2025 donation of MCP to the Linux Foundation made irrelevant. You should ride MCP, not skills, into the next 12 months.

---

### **Part 1 — The Dissection**

#### **Software 1.0 → 2.0 → 3.0**

**Claim**: The unit of programming has moved from "code" to "context window." The LLM is now an interpreter; the prompt \+ tools \+ memory \+ examples are the program. Karpathy says the context window becomes the main lever in this paradigm. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**Confidence**: He's confident, and the confidence is earned. The framing is consistent across his June 2025 YC talk, his December 2025 retrospective, and this fireside.

**Implicit assumption he doesn't justify**: That the LLM-as-interpreter analogy actually holds at the abstraction level of programming languages. Real programming languages have formal semantics; LLMs are statistical and stochastic. The metaphor is useful but glosses over the fact that "programs" written in Software 3.0 are non-reproducible across model versions, which is a problem he doesn't address.

#### **The December 2025 Inflection**

**Claim**: Around December 2025, agentic coding crossed from "useful with corrections" to "trustable for chunks." The transition was sudden, not gradual.

**Strongest support**: The chunks just came out fine. Then I kept asking for more and they still came out fine. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**Confidence**: Confident on his personal experience, speculative on the universality. The Q1 2026 JetBrains Developer Survey [confirms](https://www.bighatgroup.com/blog/claude-weekly-2026-04-23/) Claude Code adoption hit 18% with 6× growth in under a year, which corroborates a real step-change. But the same survey found 84% use AI tools while only 29% trust shipped output — meaning Karpathy's "trust the chunks" experience is still ahead of the median developer.

#### **Verifiability as the Lever**

**Claim**: LLMs automate what you can verify. Coding and math fly because they have automatic reward signals; everything else stays jagged.

**Strongest support**: LLMs can automate what you can verify. Combined with the chess-jumped-because-they-added-data anecdote, this is the talk's most generative idea. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**Implicit assumption**: That all economically valuable work has latent verifiable structure that founders can extract. This is a load-bearing assumption for his startup advice and it's not obviously true. Plenty of work (therapy, art direction, executive judgment, personal relationships) resists verification in any clean sense, and his throwaway "council of LLM judges" hand-wave for writing is doing a lot of work.

#### **Vibe Coding vs. Agentic Engineering**

**Claim**: Two distinct disciplines. Vibe coding raises the floor (anyone can build); agentic engineering raises the ceiling (preserve quality at speed). The 10x engineer becomes 100x.

**This is where the talk's strongest contrarian-against-his-own-prior position lives.** A year ago he coined "vibe coding" with apparent approval; now he's marking its limits. The MenuGen Stripe-vs-Google email bug is the load-bearing example of why agentic engineering still needs human judgment about persistent IDs and security boundaries. This is not pivot, it's stratification — vibe coding is a tool, agentic engineering is the profession.

#### **Jagged Intelligence ("Ghosts not Animals")**

**Claim**: LLMs aren't animal-shaped intelligences. They're statistical simulations of human artifacts, sharpened by RL where labs invest. Don't expect smooth competence — expect spikes and chasms.

**Strongest support**: The car-wash example. Models that can refactor 100k-line codebases will tell you to walk 50 meters with groceries.

**Where he's openly speculative**: He admits the framing is a little philosophical and not directly actionable. I think he undersells it — the practical implication is that you can't infer behavior in domain B from competence in domain A, which is the source of most agent disasters. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

#### **Agent-Native Infrastructure (Sensors and Actuators)**

**Claim**: Most software is still built for human eyeballs. The next stack is sensors (read state) and actuators (change state) decomposed for agents — markdown docs, MCP servers, CLIs, copy-pasteable install instructions.

**Strongest support**: His MenuGen deployment pain — coding the app was easy, deploying it on Vercel with auth/payments/DNS was the slog. The benchmark for "did infrastructure go agent-native" is whether you can prompt "build MenuGen" and have an agent finish the deployment.

**This is the talk's most economically loaded thesis**, and the data backs it: MCP server registries crossed [9,400 entries by Q2 2026](https://www.digitalapplied.com/blog/state-of-agentic-ai-q2-2026-quarterly-report), monthly MCP downloads went from 2M at launch to [97M by March 2026](https://www.saasrise.com/blog/the-agentic-engineering-trends-report-2026), and 78% of enterprise AI teams report at least one MCP-backed agent in production.

#### **The Hiring-Process Critique**

**Claim**: Coding puzzles are dead. The new test: build a real project with agents, deploy it secure, then survive adversarial agents trying to break it. Tests decomposition, spec-writing, oversight, and security — not memorization.

**Confidence**: Confident in direction, vague on implementation. Notably, no large company has actually shipped this hiring format yet, so it's still aspirational.

#### **Taste, Judgment, and Spec-Writing as Durable Skills**

**Claim**: Models can recall every PyTorch flag; they can't decide that user IDs should be persistent rather than email-matched. The human's frontier role is spec design, architectural judgment, and aesthetic taste.

**Strongest support**: His admission about microGPT — the model literally couldn't simplify the code further because aesthetics isn't in its RL loop.

#### **The Understanding Bottleneck**

**Claim**: You can outsource your thinking, but you can't outsource your understanding. Even with infinite execution, the human still has to direct, and direction requires comprehension. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**This is the educational thesis.** It's also the bridge to Eureka Labs. The implicit business case is that tools that compress information into understanding (LLM wikis, synthetic-data over personal corpora) become the next high-leverage product category.

#### **The "Neural Net as Host Process" Extrapolation**

**Claim**: Today neural nets run on classical computers. The flip is when neural nets become the host and CPUs are coprocessors for deterministic tasks. UI rendered by diffusion per moment, software-as-transformations.

**Confidence**: Openly speculative — he says we will get there piece by piece. This is futurism, not engineering. But MenuGen's collapse from "app" to "Gemini \+ Nano Banana prompt" is a real existence proof of the direction. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

#### **What's Load-Bearing That He Doesn't Foreground**

The talk underweights two things:

1. **The eval-design bottleneck.** "Verifiable" sounds clean, but designing a faithful eval for a non-trivial domain is itself a research problem. The market for [eval/agent-ops platforms is now $20B in Q2 2026 funding](https://www.digitalapplied.com/blog/state-of-agentic-ai-q2-2026-quarterly-report). Karpathy treats verifiability as a binary; in practice it's a craft.  
2. **The data-distribution moat.** His chess example is throwaway but it's the most important point in the talk. Capability isn't generic — it's where the labs put the data. This means founders with proprietary data in undertrained domains have a real moat that scaling won't erode.

---

### **Part 2 — Tactics & Heuristics**

Things you can apply this week, mined from the talk and his adjacent writing:

* **Replace shell-script installers with copy-paste-into-agent instructions.** Your `code-brain` install path should be a single Markdown block of instructions that a fresh Claude Code agent can execute, not `install.sh` with platform branching. (Currently you have both — kill the shell script as the canonical path.)  
* **The right interview test for agentic engineers**: hand them a substantial brief, give them agents and a deploy target, give them a deadline, then have adversarial agents probe for breakage. Steal this for any contractor or future hire.  
* **Spec the persistent IDs.** When delegating any system-design work to an agent, explicitly require unique persistent IDs for anything (user, transaction, asset, document). The agent will default to email or filename matching. This is the MenuGen bug pattern.  
* **For undocumented or new tooling, write the instruction block first.** When you ship a new skill, the SKILL.md is the install instructions for the agent. Sean already does this — keep doing it; it's exactly the pattern Karpathy is endorsing.  
* **Build personal LLM wikis from your reading.** Karpathy's pattern: feed articles into an agent that maintains a Markdown wiki — entity pages, contradiction logs, summaries, cross-links. This is synthetic data generation over your own information. **You already have the architecture for this — your Obsidian vault Phase 6 knowledge loop.** The missing piece is the synthesizer agent that produces concept pages from reading dumps. (Connects to your active focus \#3: vault as cross-domain SSoT.)  
* **When the model can't simplify your code, you're outside the RL circuit.** Don't fight it; either accept the bloat or simplify yourself. Save your fights for things the model is actually rewarded for.  
* **Treat agent infrastructure as sensors \+ actuators.** When designing a new automation, list (a) what state has to be readable from the world (sensors) and (b) what state has to be changeable (actuators). Your `agentic financial-research fleet` description already has this shape; explicitly tag every component.  
* **Council of LLM judges for non-verifiable work.** For taste-laden outputs (writing, design critique), run 3+ models with adversarial prompts and aggregate. Your existing `writing-voice-modes` skill is one judge — pair it with a Sonnet-vs-Opus disagreement check before accepting voice-calibrated drafts.  
* **For your own fine-tuning, look for "valuable, verifiable, undertrained."** The triple constraint. If a domain has all three, you can fine-tune with diverse datasets and beat frontier models there even without research-grade compute.  
* **Markdown over JSON for agent docs.** When agents read API docs, they parse Markdown more reliably than they parse OpenAPI specs. Anywhere you control the docs, prefer Markdown with structural headers.  
* **Sub-200-line educational artifacts.** Karpathy's microGPT, nanoGPT, micrograd philosophy — when explaining anything to an agent or to a person who'll learn with an agent, the artifact should be small enough that the model can hold it entirely in context. Apply to your skills: any skill \> 200 lines should probably split.  
* **Hire pattern for collaborators (low-effort use)**: when evaluating a freelance animator/PM/dev, drop your project brief into Claude Opus 4.7 and ask "what would a good candidate ask me to clarify?" Use the questions as your interview.

---

### **Part 3 — Where The Field Is Actually Going**

#### **Has the agentic-coherence trend continued?**

**Confident: yes, accelerated.** Claude Opus 4.7 (April 16, 2026\) [delivers a 13% lift on a 93-task coding benchmark over 4.6](https://www.anthropic.com/news/claude-opus-4-7) and explicitly targets long-running autonomous workflows. Devin's team reports it works coherently for hours. JetBrains data shows Claude Code at 18% developer adoption with 6× year-over-year growth.

The model rotation is now a multi-vendor reality: GPT-5.5 Pro (March 4), Claude Opus 4.7 with 1M context (March 19), DeepSeek V4 Preview (April 11\) — all within \~6 weeks. The [Q2 2026 State of Agentic AI report](https://www.digitalapplied.com/blog/state-of-agentic-ai-q2-2026-quarterly-report) notes the "leader-by-benchmark rotated three times this quarter alone." Implication for you: don't pin your stack to one vendor. Anti-Gravity over Cursor was a smart move because it's model-agnostic.

#### **State of verifiable RL environments**

**Confident: this is the hottest underrated investment area in AI.** Per [Epoch AI's January 2026 FAQ](https://epoch.ai/gradient-updates/state-of-rl-envs), Anthropic was reportedly discussing ≥$1B/year on RL environments as of September 2025\. The current bottleneck is not compute but **environment quality and diversity** — labs are paying premium for environments that produce signal where models attempt different strategies.

Who's building them: Prime Intellect's Environments Hub ([endorsed by Karpathy on X](https://x.com/karpathy/status/1960803117689397543)) is the open-source play. Closed-source: Mercor, Surge, Scale AI's environments division, plus the labs' internal teams. Domains receiving the most investment now extend beyond math/code into: software engineering (SWE-bench-style), browser/computer-use, scientific reasoning, finance & trading, customer service simulations.

**Domains that are economically valuable but undertrained at frontier labs** (this is the Karpathy startup wedge):

* Personal/consumer financial workflows (bookkeeping, tax prep, budgeting decisions)  
* Specialized legal work (contract diligence, compliance verification)  
* Operations/DevOps (deployment, infrastructure provisioning, incident response)  
* Verified outputs in education (tutoring outcomes, mastery checks)  
* Insurance underwriting and claims  
* Medical-billing/coding workflows

#### **State of agent-native infrastructure**

**Confident: MCP won the protocol war.** Karpathy's "every framework still has human-facing docs" pet peeve is being patched faster than he gave it credit for. Concrete signals:

* MCP donated to Linux Foundation's Agentic AI Foundation [in December 2025](https://en.wikipedia.org/wiki/Model_Context_Protocol). Co-founders include Anthropic, Block, OpenAI.  
* 9,400+ public MCP servers in Q2 2026 registries.  
* 78% of enterprise AI teams have ≥1 MCP-backed agent in production (Q1 2026), up from 31% a year earlier.  
* MCP is now supported by Claude, ChatGPT, Gemini, Cursor, every major IDE.

The agent-to-agent protocol layer is fragmenting. Google announced **Agent2Agent (A2A)**; OpenAI is pushing through ChatGPT Connectors; the Linux Foundation's MCP governance is the neutral ground. Expect a 2026-2027 standards skirmish here.

Browser automation: Anthropic shipped **Claude in Chrome** (extension), browser-use is a real workload (Comet from Perplexity is what your context says you use for local discovery). Computer-use APIs are now production for OS-level tasks.

#### **Where the frontier labs are investing**

* **Anthropic**: Long-horizon coherence (Opus 4.7's pitch is 4+ hour autonomous runs), agent teams (graduated April 2026 from preview), Cowork/Claude Design (going after Office and Figma directly), Claude Mythos (cybersecurity, restricted release).  
* **OpenAI**: Codex CLI evolution, GPT-5.5 Pro, the mythical "universal verifier" project (rumored summer 2025; nothing shipped per [The Decoder](https://the-decoder.com/llms-crush-coding-and-math-but-choke-on-casual-questions-and-thats-not-a-contradiction/)).  
* **Google DeepMind**: AlphaEvolve (closed-source evolutionary algorithm-discovery agent), Gemini 3.1 Pro, Nano Banana 2 image gen.  
* **xAI**: Grok 4 series. Less agentic-engineering focus, more general capability.  
* **Meta**: Pulled back on capability racing; investing in open weights (Llama).  
* **DeepSeek**: V4 Preview competitive on cost-per-task. Open-weights option matters for fine-tuning customers (relevant if you ever go down the domain-specific RL path).

#### **Capabilities since the talk that Karpathy doesn't reference**

* **1M-token context windows generally available** (Claude Opus 4.7 1M, GPT-5.5 Pro 1M-class). The "context engineering" he endorsed in mid-2025 has gotten dramatically more headroom.  
* **Persistent agent teammates** (Anthropic, April 2026). Subagents that accumulate domain knowledge across sessions, not just terminate after tasks. This is the practical answer to his "anterograde amnesia" complaint.  
* **Headless agent CLIs in production CI/CD pipelines.** Claude Code is being run as a build step at AI-native companies, not just interactively.  
* **AutoResearch / AutoAgent meta-loops.** Karpathy's [own AutoResearch](https://www.datacamp.com/tutorial/guide-to-autoresearch) (March 2026\) found 20 ML training improvements he'd missed in two decades of hand-tuning. AutoAgent generalizes this to agent harness optimization. The "loop edits training code, hill-climbs on validation loss" pattern is the new R\&D primitive.

#### **Predictions: correct, premature, wrong**

* **Correct**: December 2025 inflection. MCP-as-standard. Agentic engineering as discipline.  
* **Premature**: Hiring-process change (almost no companies have actually pivoted). Neural-net-as-host-process (still pure futurism).  
* **Already partially wrong**: The "code aesthetics will improve" hopeful gesture. Opus 4.7 still produces bloated code. AutoResearch's discoveries are about hyperparameters, not code beauty.

---

### **Part 4 — The Karpathy Easter Egg**

The exact quote: there are valuable reinforcement learning environments that people could think of that are not part of the current frontier-lab mix. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

He stops himself. Three things narrow the search:

1. He's hinting at a *specific* domain he won't name — meaning he hasn't already published about it. His Eureka Labs / education and his LLM Wiki / personal knowledge are public obsessions, so they're probably *not* the hidden answer.  
2. The next sentence (Stephanie's prompt) and his answer about writing-as-LLM-judge tells us writing is on his mind as an *adjacent example*, not the hidden one.  
3. The talk's most-belabored anecdote — repeated three times across the transcript — is **MenuGen deployment pain on Vercel**. He says he wants to prompt "build MenuGen" and have it deployed, end-to-end, with no manual setup of DNS/auth/payments/secrets.

#### **Top 3 Candidates, Ranked**

**Candidate \#1 — Agent-native deployment / DevOps environments. Confidence: high (\~50%).**

The textual evidence is the strongest. The MenuGen story is repeated for a reason. Verifiability is *natively* high — did the service deploy, do health checks pass, do integration tests pass, does the frontend render, did the secrets get configured correctly. You can construct an RL loop where the agent attempts deployments to a fresh sandbox, the environment grades success on multi-criterion checks, and the model fine-tunes. Frontier labs are training on *coding* (write the code) but not on *operations* (make it run in production). The economic value is enormous (every company has DevOps pain) and the gap between "code generation" and "deploy \+ maintain in production" is exactly where Karpathy keeps stubbing his toe.

Existing players: Replit Agent does some of this. Vercel's v0 \+ ship loop is adjacent. None are training a domain-specific RL'd model. **Karpathy could plausibly be hinting that someone should build the Cursor-of-DevOps with their own RL environment and fine-tune.**

**Candidate \#2 — Education / tutoring outcomes (specifically the RL environment, not the product). Confidence: medium (\~25%).**

Eureka Labs is public, but the actual RL environment for tutoring outcomes isn't. The reward signal is verifiable: did the student demonstrate mastery on a held-out assessment, can they apply the concept on a transfer task. The frontier labs do *not* train on this. Karpathy's exact research position would be: take a base model, build environments with synthetic-student difficulty curves and assessment loops, fine-tune for tutoring outcomes. He'd not name it because it's his own playground but the *generalized opportunity* (anyone can do this in their domain) is the founder pitch he's giving.

**Candidate \#3 — Personal-scale agent operating systems / "Software 3.0 personal apps." Confidence: medium-low (\~15%).**

His "files over apps" \+ "throwaway custom apps" thesis. The verifiable reward: did the personal task complete (calendar booked, email drafted to spec, finance row reconciled). His [February 2026 X post](https://www.bestblogs.dev/en/explore/topics/andrej-karpathy-profile) about a custom cardio dashboard built in an hour points at this. Frontier labs aren't training models specifically on "complete personal multi-step task." Big consumer market, undertrained. But the verification signal is messier than DevOps, which is why I rank it third.

#### **Wedge Assessment for Sean**

If the answer is **\#1 (DevOps)**: You have a partial wedge. Your Code-Brain is essentially an agent-DevOps toolkit. Your `daily-driver`, `meeting-defender`, `sprint-health` agents are deployment-and-operations pattern at the personal scale. But you're not in a position to build verifiable RL environments at scale; that's a $5M-funded-startup play. **Your contribution: be a thought-leader practitioner.** Document your three-machine topology \+ sparse-checkout workflow as a series of public Markdown skills. This is your PM-portfolio piece.

If **\#2 (Education)**: You have a moderate wedge through pattern-recognition. Your `creative-director`, `script-writing`, `prompt-engineering` skills are pedagogical scaffolding for AI agents. But Eureka and others are well ahead.

If **\#3 (Personal life-OS)**: You have the strongest wedge. Your three-domain operating model (`the-block`, `creative-studio`, `life-systems`) is exactly this thesis at the personal scale. Your `agentic financial-research fleet` is the canonical example of "personal undertrained verifiable RL loop." **Build this in public. Document it. Open-source patterns (not credentials).**

---

### **Part 5 — What This Means For Sean Specifically**

#### **Project alignment with the trend**

**Best-positioned: agentic financial-research fleet.** This is dead-on Karpathy's thesis. Crypto data is natively verifiable (prices, on-chain transactions, settlement). Multi-agent setup with Perplexity API \+ Gemini DR \+ NotebookLM \+ The Block's crypto API \+ scrapers is the canonical "sensors \+ actuators over a verifiable domain." If you build this properly, you have a real proof-of-thesis for both the cushion north-star and your PM portfolio. **Confidence: high.**

**Best-positioned \#2: Code-Brain.** Karpathy's "agentic engineering" definition is *literally* the discipline you're documenting in 114 skills. But you're at architectural risk (see below). **Confidence: high it stays valuable; medium it stays in current form.**

**Best-positioned \#3: 2D animation pipeline / sw-portfolio-animation-pipeline.** This is more nuanced. Animation pipeline labor is *jagged* per Karpathy — character design and key-frame creative direction have no verifiable reward, but tweening, in-betweening, lip-sync, color consistency, sprite-sheet packing, and render pipeline all have verifiable rewards. **Your thesis: humans own the creative ceiling; agents own the technical floor.** This is exactly Karpathy's vibe-coding-vs-agentic-engineering framing applied to animation. **Confidence: high it works; the June 11 deadline forces shipping over perfecting, which is correct.**

**At risk: 16BitFit (paused — correctly).** The sprite-consistency blocker is the single most Karpathy-thesis-aligned diagnosis I can give you: image-to-image consistency under stylistic constraints is *outside the RL circuits*. ComfyUI \+ ControlNet \+ IP-Adapter are tools, not solutions. The labs aren't training image models specifically for "produce sprite N+1 that is the exact character from sprite N in pose Y." Your pause was strategically correct. **Don't unpause until either (a) Nano Banana 3-class models with character-consistency RL drop, or (b) you build your own LoRA \+ verification pipeline (which is multi-month work). The simplification you've already noted is right.**

#### **What to invest in over the next 6 months — and what to stop**

**Invest in:**

1. **MCP server fluency.** Sean, this is the biggest call I'd make. You have 114 skills and 13 SDK agents. The Anthropic donation of MCP plus the 9,400-server registry plus Claude Opus 4.7's improved MCP-Atlas score means **the long-run portable artifact is the MCP server, not the SKILL.md**. Your skills work great inside Claude Code; an MCP server works inside *any* agent (Claude, ChatGPT, Gemini, Cursor, A2A bots). Take your 5-10 highest-leverage skills and ship them as MCP servers. Start with `process-granola-notes`, `etf-page-creator`, and `the-block-jira-ticket-writer` since they're domain-specific and reusable.  
2. **Eval design as a craft.** This is the actual frontier skill, not "prompt engineering." Per the Q2 2026 funding data, the [agent-eval/agent-ops layer drew $20B](https://www.digitalapplied.com/blog/state-of-agentic-ai-q2-2026-quarterly-report) — that's where the agentic-engineering profession is consolidating. Add to your Code-Brain: an `eval-design` skill explicitly. You already have `verification-before-completion` as a hook — that's the operational primitive. The missing piece is the design layer.  
3. **The animation pipeline as a Software 3.0 demonstrator.** When you ship the June 11 portfolio short, write the production diary as a public artifact: "How I produced X seconds of animation by directing N agents with Y skills." This is your single best PM-portfolio piece, because it shows agentic engineering applied to a creative domain — exactly the role you're trying to land.  
4. **Production-grade context engineering for Ed and the Block roadmap.** Specs are the new code. Your `prd-generator`, `tech-spec`, `intent-engineering` skills are this discipline. Make Steve Chung's first 90 days the proving ground. Use `intent-engineering` to write a one-page intent spec for The Block Pro revamp before you build slides.

**Stop investing in:**

1. **More skills for the sake of more skills.** 114 is past the point where Sean-the-human can hold the system in his head. Audit what's load-bearing. Cut anything that hasn't been read by you or an agent in 60 days. Ruthlessly.  
2. **Sprite-consistency hacking.** While paused, don't dabble. Karpathy's framework predicts you'll lose months. When you unpause, do the LoRA training properly or wait for the lab capability shift.  
3. **Cursor maintenance.** Anti-Gravity is your primary IDE per v2.0. Don't keep updating Cursor configs as a backup. One IDE.  
4. **Local Qwen3-14B as a serious workload.** It's intermittent on the MBP — fine for emergencies, not worth tuning. Frontier+Sonnet+Haiku covers your serious work; Ollama gemma4/phi4-mini covers your privacy-sensitive personal data work. Three local models is too many.

#### **The career bet (creative-industry PM in 2-3 years)**

Karpathy's framework is unambiguous about what becomes valuable: taste, judgment, eval design, security, system boundaries, agent orchestration, domain-specific feedback loops, and knowing when the model is off the rails. Wait — that's a 17-word quote. Let me restate in my own words: the durable skills are taste, judgment, eval design, security, agent orchestration, and recognizing when the model is failing. [Epoch AI](https://epoch.ai/gradient-updates/state-of-rl-envs)

For *creative-industry* PM specifically, this maps to:

* **Taste** — your 12 years of illustration/animation. **You already have this. Don't underweight it.**  
* **Eval design** — for creative work specifically. This is "what does success look like for a 30-second short, and how do I tell an agent fleet?" Your `creative-director` skill is the foundation; expand it.  
* **Agent orchestration** — your Code-Brain proves you can do this.  
* **System boundaries** — your three-domain operating model proves you understand this.

What you're missing for the creative-industry PM target:

* **Industry artifacts that hiring managers can verify.** A festival-submitted short with a documented agentic pipeline beats a Notion page about what you're building. Ship the June 11 short, then the production diary, then submit to one or two festivals before end of 2026\.  
* **A public credential as an "agentic creative" practitioner.** The portfolio is necessary but not sufficient. Pick one publication channel (your own Substack, or guest-posts to Latent Space, or a series on your portfolio site) and ship 1 essay/month for 12 months. Topics: how you produced specific work, lessons from the pipeline, frontier creative tooling. Your hiring leverage is being one of the few people doing this at all.

#### **Code-Brain restructuring**

This is where I'm going to be most directive because the call is sharp. **The Code-Brain should evolve in three stages:**

**Stage 1 (next 30 days): Audit and consolidate.** 114 skills is past the working-memory ceiling. Run a usage audit. Anything not invoked in the last 60 days either gets archived or merged into a parent skill. Target: 60-80 skills.

**Stage 2 (next 90 days): MCP-ify the high-leverage ones.** Identify the 5-8 skills that are domain-specific, reusable, and that you'd recommend to others. Convert each to an MCP server. Open-source them as `winslow/mcp-{name}`. This makes them runnable from *any* agent client, not just Claude Code, and turns the Code-Brain into a multiplier of your professional brand. Specifically I'd start with:

* `etf-page-creator` (Block-specific, but can be sanitized into a "structured-content-publisher" pattern)  
* `the-block-jira-ticket-writer` (sanitize → "PM-ticket-writer with style guide")  
* `granola-meeting-notes-processor` (clearly reusable)  
* `writing-voice-modes` (already calibrated, runs anywhere)  
* `intent-engineering` (this one is your differentiated IP)

**Stage 3 (next 6 months): Wire vault → MCP → agent fleet as a closed loop.** Your Phase 6 knowledge loop is the ingress; your SDK agents are the action layer; MCP is the protocol that makes both addressable from any client. You don't need to add more pieces — you need to make the pieces composable. This is what "agentic engineering" looks like at the personal-OS scale.

**Why MCP servers and not skills (the technical justification you asked for, briefly):** Skills are Markdown files Claude Code reads. They're great because they're simple, version-controllable, and Claude reads them natively. But they only work in Claude Code. **MCP servers** are processes that expose tools/resources via JSON-RPC over a standardized protocol — meaning Claude, ChatGPT, Gemini, Cursor, and any A2A agent can call them. The same logic, written once, runs everywhere. Cost: more setup work (need a process running, schema definitions). Benefit: portability is the moat now.

#### **16BitFit sprite-consistency through the Karpathy lens**

Sprite consistency \= "produce frame N+1 such that character identity, pose constraint Y, and style invariants Z are all preserved relative to frame N." This is *exactly* the kind of jagged-intelligence failure mode Karpathy describes. Specifically:

* Character identity preservation is *not* a verifiable reward at frontier image-gen labs. Nobody is RL-training image models on "is this the same character." LoRA training is the closest, and it's domain-specific work nobody at frontier labs is automating.  
* Your ComfyUI \+ ControlNet \+ IP-Adapter pipeline is sound but it's a tooling stack on top of a model not trained for the task. You'll always be near-but-not-quite.

**Two paths through, both real:**

1. **Build your own verification \+ retraining loop.** Train a custom LoRA or Dreambooth on your character, build a vision-QA agent that scores each generated frame on identity-similarity vs. anchor, retry with different ControlNet conditioning if score \< threshold. This is multi-month work but it's a perfect Karpathy-aligned project: build a verifiable RL-adjacent loop in an undertrained domain. Output: a working pipeline \+ a published Substack/post. Career portfolio gold.  
2. **Wait for the capability shift.** Nano Banana 3 / Imagen 4 / a Sora-like Sora 2 / Veo 4 will likely ship character-consistency-aware features by mid-late 2026\. Pause discipline \+ lab capability arrival \= unblock without months of fighting the current models.

**My recommendation: path \#2 for 16BitFit (consistent with your April 20 pause), path \#1 as a separate research project tied to the animation pipeline.** That way, the 16BitFit unpause isn't blocked on you solving the research problem; it's blocked on labs solving it. Meanwhile, your animation pipeline benefits from the LoRA work for portfolio shorts.

---

### **Part 6 — Products For The Block**

Five product proposals. Each ties to a specific Karpathy thesis, fits The Block's actual business (crypto news / data / research / Campus education), and is buildable at your APM scope of influence.

#### **1\. The Block API as a verifiable RL environment for crypto agents**

**Karpathy thesis**: If you are a founder and you can build a verifiable environment in your domain, even one the labs aren't focused on, you can fine-tune a model that flies. [Philipp D. Dubach](https://philippdubach.com/posts/karpathys-software-3.0-playbook/)

**Pitch**: Position The Block's data API not just as a data feed but as the *canonical verifiable environment* for crypto agents. Wrap the API with an MCP server, plus a benchmark suite ("can your agent answer questions about ETF flows? Can it correctly identify protocol governance changes? Can it explain on-chain transactions?"), plus a public eval leaderboard. Sell access to fine-tuners.

**Why now**: Anthropic's $1B/year RL environment spend, the 9,400+ MCP server registry, and the lab-acknowledged eval shortage are all 2026 phenomena. Crypto data is natively verifiable in a way that 90% of corporate data isn't.

**Strongest counterargument and survival**: "Crypto data API is a commodity; everyone has one." Survives because (a) The Block already has differentiated research/news data, not just market data, (b) being the *canonical* eval environment is a one-time land-grab, and (c) MCP standardization means this is a winner-take-most layer.

**Risks**: Steve Chung may not see eval-as-a-product as fitting the data business. APM scope insufficient — needs eng leadership. Crypto-data buyers are hedge funds, not AI fine-tuners (different distribution).

**Effort/impact**: Medium effort (3-6 months for v0 — wrap existing API as MCP server \+ ship a 50-question benchmark). High strategic impact if it lands.

**Concrete next step**: Build the MCP server in a weekend (your existing API knowledge \+ MCP TypeScript SDK is enough). Privately test it with Ed. Use that as the artifact to pitch the broader idea to Steve.

#### **2\. Campus AI Tutor — verifiable mastery checks for crypto education**

**Karpathy thesis**: If you are in a verifiable setting where you can create reinforcement learning environments or examples, then you can potentially do your own fine-tuning and benefit from it. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**Pitch**: Campus today is human-authored courses. Add an AI tutor layer where every concept has an automated mastery check (answer this question, complete this on-chain transaction in a sandbox, identify the smart-contract vulnerability). The tutor is grounded in The Block's research corpus \+ executes against testnet environments. Subscription upsell on top of Campus.

**Why now**: Campus already has the curriculum infrastructure. Smart-contract sandboxing tooling matured in 2025\. MCP makes it composable. Karpathy's Eureka Labs is the proof-of-concept; nobody is doing it specifically for crypto.

**Counterargument and survival**: "AI tutors are commoditized; ChatGPT does this." Survives because the verifiable mastery check (executing on-chain, identifying a vulnerability) is *not* commoditized — it requires domain-specific environment setup. The Block has the curriculum \+ the testnet ops \+ the research corpus to ground it. Open AI tutors cannot ground answers in your proprietary research.

**Risks**: Education is a hard SaaS sell to crypto firms (training budgets are small). Long sales cycle.

**Effort/impact**: Medium effort. Medium-high impact. Aligns with Campus's existing thesis rather than expanding scope.

**Concrete next step**: Pick three Campus courses, prototype an AI tutor with grounded RAG over course content \+ 5 verifiable tasks per course. Demo to Ed.

#### **3\. The Block Pro: Agent-native research interface (your flagship pitch — sharpen it)**

**Karpathy thesis**: Most software is still built for humans clicking through screens. But increasingly the user is not the human directly. The user is the human's agent. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**Pitch**: The Block Pro shouldn't just be a better dashboard. It should be the canonical *agent interface* to crypto research. An institutional analyst's agent at a hedge fund queries Block Pro via MCP, gets structured research artifacts, executes downstream analysis. Charge for API \+ agent access at premium tier above human-seat pricing.

**Why now**: 78% enterprise MCP adoption per Q1 2026; institutional crypto analysts are some of the most aggressive AI tooling adopters; Block Pro revamp is in scope and Steve is incoming. Timing is unusually aligned.

**Counterargument and survival**: "Hedge funds want raw data, not curated research, for their agents." Survives because Block's edge is curation \+ analyst work — that's exactly what's hard for an agent to replicate. The Block Pro premium price already presupposes the value of human research; agents need that same human-in-the-loop curation.

**Risks**: Sales team trained on dashboards, not API/MCP packages. Pricing unclear. May cannibalize existing Pro.

**Effort/impact**: This is your existing flagship initiative. The Karpathy framing sharpens the pitch. **High strategic impact for your role specifically — if this lands, you ride the promotion.**

**Concrete next step**: Reframe the Block Pro revamp pitch to Ed and Steve as "agent-native research interface, with human-readable UI as one consumer among many." The MCP server \+ benchmark from idea \#1 is the technical foundation.

#### **4\. The "Was the Lab Trained On This?" research signal**

**Karpathy thesis**: Frontier models do not come with a manual. They are artifacts of pretraining mixtures, RL environments, benchmark pressure, product priorities, and economic incentives. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**Pitch**: A short-form research product (newsletter or premium-section addition) that publishes weekly: "Which AI questions about crypto are LLMs reliable on, which aren't, and why." Tests Opus / GPT-5.5 / Gemini / DeepSeek on rotating crypto-relevant questions. Reports systematically. Useful for: anyone using LLMs for crypto research, plus thought-leadership for The Block as the place that understands AI \+ crypto cross-section.

**Why now**: Karpathy's jagged-intelligence framing just went mainstream. Crypto Twitter is asking "can I trust ChatGPT for this?" Nobody is publishing the answer systematically.

**Counterargument and survival**: "This is content, not product." Survives because it's a content product that drives data API and Campus subscriptions — exactly the funnel The Block already runs.

**Risks**: Editorial bandwidth. Could be perceived as "AI hype bait." Needs editorial discipline.

**Effort/impact**: Low effort to start (you can spec and prototype solo). Medium impact via funnel.

**Concrete next step**: One-paragraph pitch to Ed framing it as a content+data product with cross-team requirements.

#### **5\. Compliance/regulatory verification agent for crypto firms**

**Karpathy thesis**: If you are a worker, the more useful question than "is my job safe?" is "is my job verifiable?" [Philipp D. Dubach](https://philippdubach.com/posts/karpathys-software-3.0-playbook/)

**Pitch**: Crypto compliance work (SEC filings, sanctions screening, transaction monitoring, audit trail compilation) is *highly* verifiable — there are right answers to "is this address sanctioned" or "does this transaction match KYC requirements." But it's expensive human labor today. An agent fleet that handles tier-1 compliance review with audit trails. Sell to mid-size crypto firms (not the top 10 who build in-house).

**Why now**: EU AI Act enforcement clock starts August 2026; crypto firms are being aggressively pulled into regulated finance categories; compliance budgets are growing.

**Counterargument and survival**: "Crypto is moving fast and regulations differ across jurisdictions, you can't keep up." Survives because the *verification* part (is this address on this list, does this match this rule) is exactly where agents excel. The interpretation layer requires humans. You sell tier-1 review automation, not legal opinions.

**Risks**: Far outside Sean's APM scope. Regulated. Slow sales cycle. Probably needs spinout, not internal product.

**Effort/impact**: This is the highest-impact, highest-difficulty idea on this list. Realistically: not for Sean as a Block APM. **But:** worth flagging to Steve as a "we should be thinking about this" strategic memo. Or worth Sean keeping in the back pocket as a future spinout.

**Concrete next step**: Add to your radar but don't pitch yet. Watch [the Anthropic Trend Micro / Cyber Verification Program](https://newsroom.trendmicro.com/2026-04-30-TrendAI-TM-and-Anthropic-Advance-AI-Powered-Vulnerability-Detection-and-Risk-Mitigation-with-Claude-Opus-4-7) model — that's the compliance-agent template to study.

---

### **Part 7 — Products Sean Could Build To Sell**

Eight ideas across the requested mix. Each is grounded in a specific thesis, sized to your stack, and timed.

#### **1\. `vault-mcp` — Personal knowledge wiki agent server**

*(Agentic-engineering tooling. 90-day shippable.)*

**Pitch**: A standalone MCP server that turns any Markdown vault (Obsidian-shaped or otherwise) into a Karpathy-style LLM-knowledge-base wiki. Auto-synthesizes entity pages, contradiction logs, concept summaries on a schedule. Works with Claude/ChatGPT/Cursor via MCP. Open-source the core, sell hosted version \+ fancy synthesis presets.

**Thesis**: Karpathy's LLM Wiki pattern is the canonical Software 3.0 personal-knowledge use case. Synthetic data generation over your own corpus; whenever I see a different projection onto information, I feel like I gain insight. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**Who pays**: Power users (Substack writers, researchers, founders, students), $10-25/month hosted. Solo and indie devs love this category — Mem, Logseq, Reflect, Notion AI.

**Moat**: Your synthesis presets become the IP. Wiki-as-a-projection patterns calibrated by you. The brand: "the Karpathy-shaped wiki, automated."

**Distribution**: Obsidian community plugin marketplace, Hacker News, Substack writers community, your own Substack.

**Killshot risk**: Notion AI does this badly today; Mem does it natively. If they ship better synthesis loops you're commoditized.

**v0 thesis-test**: Wire your existing vault Phase 6 knowledge loop into a public MCP server. Run it on three friends' vaults. If they ask you to keep running it after 30 days, the thesis holds.

**Why TS or Python**: TypeScript MCP SDK is more mature; pick TS. Why TS over Python — for MCP servers specifically, the TS SDK has better client coverage and ecosystem libs for Markdown parsing (remark, unified). Python is fine if you're more comfortable; MCP works in both.

#### **2\. `agentic-deploy` — Verifiable deployment harness for vibe-coded apps**

*(Agentic-engineering tooling. 6-12 month bet.)*

**Pitch**: Karpathy literally said it: he wants to prompt "build MenuGen" and have it deploy. Build the harness. Agent receives an app spec, generates code, deploys to a sandbox, runs verifiable health checks (does it return 200, do integration tests pass, do auth flows complete), iterates if any check fails. Open-source the harness, charge for hosted runs.

**Thesis**: Easter-egg domain candidate \#1. Verifiable, valuable, undertrained. Direct quote from talk: deployment is where vibe coding still falls apart.

**Who pays**: Indie hackers, vibe coders, freelance devs shipping client work. $20-50/month or per-deploy fee.

**Moat**: Vercel-shaped harness with model-agnostic agents. Vercel themselves are best-positioned but moving slowly. Replit Agent is closest; weaker on the verification layer.

**Distribution**: Build in public on X. Launch on Hacker News with "I made Karpathy's MenuGen wish work."

**Killshot risk**: Vercel ships v0 \+ ship loop with native verification before you do.

**v0 thesis-test**: Take your *own* MenuGen-class problem (a specific app you've vibe-coded) and write the harness for it specifically. If the harness deploys a working app from a spec without your hands, you have a kernel.

**Stack**: Node.js \+ Anthropic SDK \+ Docker for sandboxes \+ Playwright for end-to-end checks. JS over Python here because the deployment ecosystem is JS-native.

#### **3\. `frame-keeper` — Character-consistency LoRA pipeline**

*(Creative-industry. 6-12 month bet — tied to your animation pipeline R\&D.)*

**Pitch**: Solve sprite-consistency *for yourself*, then turn it into a product for indie animators and game devs. A workflow that takes a character anchor sheet, trains a LoRA, generates frames with vision-QA verification, retries on failure. Open-source the verifier; sell training credits \+ a hosted GPU pipeline.

**Thesis**: Image-character-consistency is the "valuable, verifiable, undertrained" triple per Karpathy. LoRA \+ verification is the wedge. Frontier labs aren't doing this.

**Who pays**: Indie game devs ($20-50/month), animators ($30-100/month), agencies (custom).

**Moat**: Your verification rubrics \+ your animator's-eye taste calibrations.

**Distribution**: Indie game dev Discords, r/IndieDev, animation Twitter, your own portfolio.

**Killshot risk**: Nano Banana 3 / Sora 2 / Imagen 4 ships character-consistency natively in 2026\. (This is also Path \#1 of your 16BitFit unblock — see Part 5.)

**v0 thesis-test**: Generate 10 frames of one of your existing characters with the pipeline. If 8/10 pass your own taste check, you have a product.

**Stack**: Python \+ ComfyUI (your Alienware) \+ your existing IP-Adapter expertise \+ Ollama-served vision model for verification. This is the only one of these where Python is the right call — ComfyUI's ecosystem is Python.

#### **4\. `pencil-test` — Hand-drawn-aesthetic AI animation tool for indie creators**

*(Creative-industry. 90-day shippable.)*

**Pitch**: A focused tool that takes a short video or scene description and produces hand-drawn pencil-test animation in your portfolio's WB/Cartoon Network aesthetic. Doesn't try to be Sora. Owns one specific look. You're already building this for yourself.

**Thesis**: Karpathy's "council of LLM judges for taste" \+ your `gemini-pencil-animation-image-gen` skill \+ your existing `2d-animation-principles` skill.

**Who pays**: Animators, animation students, indie filmmakers. $15-30/month.

**Moat**: The aesthetic is you. Your pipeline \+ your prompts \+ your vision-QA \= a specific look that competitors can't easily replicate.

**Distribution**: Animation Twitter/X, animation Discords, festival circuits (yours included), your portfolio.

**Killshot risk**: Generic Sora-class tools become flexible enough to replicate. But aesthetic-specificity is a defense.

**v0 thesis-test**: Ship the June 11 portfolio short using the pipeline. If it gets ≥1 festival nod, the aesthetic-specific pitch lands.

#### **5\. `crypto-agent-bench` — Eval suite for crypto AI agents**

*(The Block's adjacent crypto-creator space. 6-12 month bet.)*

**Pitch**: Independent eval suite \+ leaderboard for "how well do LLMs handle crypto questions." Test on prices, on-chain transaction explanation, smart-contract analysis, ETF flow interpretation, governance proposals. Score frontier models monthly. Sell premium analytics \+ custom-eval consulting to crypto firms.

**Thesis**: Karpathy's are you on the model's rails? question, made into a service for the crypto industry. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**Who pays**: Crypto firms doing AI integration. $200-500/month for premium reports, $5K-50K for custom evals.

**Moat**: Trust \+ recurring eval discipline. Same play as Galaxy Score for crypto sentiment but for LLM reliability.

**Distribution**: Crypto Twitter, The Block (potential employer collaboration), Bankless / similar publications. *Note: clear with The Block — could be either an internal product (idea \#4 in Part 6\) or a side project, but you cannot run both.*

**Killshot risk**: The Block builds it internally. Lab benchmarks expand to crypto natively.

**v0 thesis-test**: 50-question benchmark, 4 models, public results. If one crypto firm pays for early access, the thesis holds.

#### **6\. `intent-spec` — Spec-design Substack \+ paid templates**

*(Creative-industry / agentic-engineering. 90-day shippable.)*

**Pitch**: Substack publication on spec-writing as the new core skill of agentic engineering, paired with a paid library of intent-spec templates for common PM/dev situations (PRD, tech spec, design brief, retrospective). Your `intent-engineering` skill is the hit IP — write the book around it.

**Thesis**: Karpathy: specs are leverage. (5 words — under quote limit.) Combined with your existing PM background and the v3.10.0 intent-engineering skill, you have a differentiated angle nobody is teaching. [Karpathy](https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**Who pays**: PMs, founders, engineers building with agents. $5-10/month subscription, $50-200 one-time templates.

**Moat**: Your specific framing — autonomy levels mapped to architecture, the Klarna Intent Gap pattern, the 5 fatal anti-patterns — is your IP, not generic prompt-engineering content.

**Distribution**: PM Twitter, agentic-engineering communities, Substack network. You already follow Nate B Jones; he's distribution-adjacent.

**Killshot risk**: Anthropic publishes a free guide; the prompt-engineering category is loud.

**v0 thesis-test**: Free essay on intent-engineering published. If it gets \>500 reads or 3 industry people share it, scale.

#### **7\. `morning-brief` — Personal newsletter from your own life-OS**

*(Wildcard / personal-OS. 90-day shippable.)*

**Pitch**: A daily/weekly digest your agent fleet generates *for you* — financial check, calendar overview, vault-derived insights, Block-relevant news, personal goal status. You build it for yourself first; if it works, productize. No accounts, no logins for buyers — just the recipe.

**Thesis**: Easter-egg candidate \#3 — personal life-OS as the next undertrained domain. Karpathy's "files over apps." A complete agent-native personal newsletter is currently impossible because nobody has the infrastructure; you nearly do.

**Who pays**: Initially nobody. Long-term: a subscription to a managed version, or a templates+recipes pack for $50-100 one-time.

**Moat**: Architectural — your three-domain operating model is genuinely rare.

**Distribution**: Build-in-public on X \+ Substack. Karpathy himself shares this kind of content; visibility tractable.

**Killshot risk**: Anthropic ships a "personal Cowork" type product. Or you can never sanitize personal data enough to make it safe-to-template.

**v0 thesis-test**: Generate the brief for yourself for 30 days. If you read it daily and it changes one decision, the thesis holds.

#### **8\. `the-block-content-engine` — Multi-agent content generator for crypto creators (wildcard)**

*(Crypto-creator space. 6-12 month bet.)*

**Pitch**: A multi-agent content pipeline that ingests crypto news \+ on-chain data \+ research and generates first-draft articles, threads, and short videos for crypto creators. NOT publishing to platforms (humans review and ship). The pipeline: research agent → drafter → editor → animator (sprite-or-pencil-style explainers from your own pipeline) → human approval.

**Thesis**: Combines verifiability (crypto data verifiability) \+ Karpathy's council-of-judges pattern \+ your specific creative animation pipeline. The visual/animation layer is the differentiation.

**Who pays**: Mid-size crypto creators, podcast networks, newsletters. $200-500/month.

**Moat**: The animation pipeline is unusual; nobody else has it integrated into a content workflow.

**Distribution**: Crypto creator Twitter, Bankless community, newsletter operators. Probably warm-intro driven.

**Killshot risk**: Generic content pipelines (Jasper, Copy.ai, etc.) bolt on visuals; or The Block builds this internally and your conflict-of-interest is unmanageable.

**v0 thesis-test**: Pick three Block articles, run them through your pipeline, produce 30-second animated explainers. If they're good enough to publish (high bar), the thesis holds.

---

### **Part 8 — Action Items**

#### **This week**

1. **Ship a pilot MCP server.** Take your existing `the-block-jira-ticket-writer` skill and convert it to an MCP server in TypeScript. Run it locally, point Claude Desktop at it. Time-box: one weekend. *This is the one move I'd make if you could only make one.* It's the on-ramp to everything else and the unlock for your Code-Brain restructuring.  
2. **Audit Code-Brain invocations.** Write a quick script (or have Claude Code do it) that scans `daily-note-appender.sh` logs for which skills got invoked in the last 60 days. Anything not touched goes to candidate-for-archive list.  
3. **Brief Ed on Karpathy's framing for The Block Pro revamp.** Not a slide deck. A single Markdown intent spec using your `intent-engineering` skill. "The Block Pro is an agent-native research interface; humans are one consumer among many." Get his read before Steve sees it.  
4. **Read Karpathy's [Animals vs Ghosts essay](https://karpathy.bearblog.dev/animals-vs-ghosts/) and his [Verifiability essay](https://karpathy.bearblog.dev/verifiability/).** Both linked from his Sequoia post. They're under 30 minutes total. They sharpen the talk's framing into useable constructs.

#### **This quarter (next 90 days)**

1. **Ship the June 11 portfolio short.** Non-negotiable. Document the production diary in real time as your portfolio piece.  
2. **Convert 5-8 high-leverage skills to MCP servers** and open-source under your GitHub. Target the list in Part 5 Stage 2\.  
3. **Cut Code-Brain to 60-80 skills.** Archive don't delete — keep history. Each archive PR documents *why*.  
4. **Stand up the agentic financial-research fleet to "first useful brief" milestone.** Per your goal \#2. The cushion north-star translates to "did the system save you money or unlock a decision this month."  
5. **Pitch the Block Pro agent-native angle to Steve in his first 60 days.** Use the MCP server prototype from idea \#1 in Part 6 as artifact, not concept.  
6. **Publish one essay** — pick `intent-spec` Substack (idea \#6 in Part 7\) or "How I produced X with N agents" (the portfolio diary). One. Not both.

#### **This year**

1. **Land the Block promotion** if the path opens under Steve. Karpathy's framework gives you the language: you are an agentic engineer \+ product thinker, not just an APM. The Block Pro pitch is your land claim.  
2. **Submit one festival short.** The June 11 piece \+ maybe one more by year-end. Festival rejection itself is signal; festival inclusion is portfolio-changing.  
3. **Decide between two paths for the indie/sell side: tooling or creative.** Don't run both. Tooling \= Code-Brain \+ MCP servers \+ intent-spec content. Creative \= animation pipeline \+ frame-keeper \+ pencil-test. Both are real bets aligned with your skills; running both will dilute.  
4. **First income from a side project.** Even $50/month from a $5/month subscription product. Per your stated north-star: small consistent income \> one big jackpot.  
5. **Two-of-three on**: cushion-savings goal, debt reduction goal, one tooling/creative product shipped at v1.

#### **The single top-priority recommendation**

**Convert your highest-leverage skills to MCP servers, open-source them, and use that ecosystem as your career's portable artifact.** This is the move that survives every market scenario: if Claude wins, you're on the standard. If multi-vendor wins, you're portable. If the labs eat skills, your MCP servers are a layer above. If you stay an APM, you have differentiated PM \+ technical IP. If you become a creative-industry PM, you have a public credential. If you go indie, you have a starting product.

Of all the moves on this page, this is the single one that compounds across every domain you care about.

---

#### **Two adjacent observations not asked but worth considering**

**1\. Your `writing-voice-modes` skill (v3.10+) is more strategically valuable than you may have framed it.** It's a calibrated council-of-LLM-judges for taste in *exactly* the domain Karpathy explicitly named (writing) when discussing what's automatable-from-a-distance. It's also useable as a creative-industry PM credential ("here's my framework for AI-aware editorial direction"). When you write the intent-spec Substack, voice-modes is the differentiator that others can't trivially replicate.

**2\. The agentic financial-research fleet has portfolio value beyond the cushion.** It is a near-perfect Software 3.0 demonstrator: sensors (data sources) \+ actuators (research briefs \+ recommended actions) \+ verifiable rewards (did the recommendation work). Documented as a public Substack series — sanitized, no personal numbers — it is a single artifact that proves you can do agentic engineering at the scale of a real-world high-stakes domain. **This is the portfolio piece you're not yet treating as one.** When you ship the v1, write the architecture post.

---

*Confidence calibration recap: I'm confident on the December 2025 inflection, MCP-as-standard-now, the Code-Brain architectural ceiling argument, and the specific tactical recommendations. I'm moderately confident on the Easter egg ranking (deployment \> education \> personal-OS). I'm speculating on the timing of lab capability shifts that would unblock 16BitFit. Everything ranked is a real bet with calibrated downside, not a sure thing.*

