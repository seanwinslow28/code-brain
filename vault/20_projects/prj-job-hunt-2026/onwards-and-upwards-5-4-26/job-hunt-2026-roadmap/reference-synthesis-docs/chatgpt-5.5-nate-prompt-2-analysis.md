# Sean’s 2026 AI PM Signal Strategy

## 1. Executive Summary (Nate's Thesis in 3 Bullets + Your Verdict)

- Nate’s durable insight is real: in an AI-saturated market, raw output has decayed as a proxy for competence, so the scarce signal is whether someone can explain what they built, why they chose that path, what would fail, and what changed in their thinking. His own language is strong here: “the building is easy now,” while what’s scarce is whether you “actually understood what you built.” [Nate article] fileciteturn2file0L19-L33

- The four-question format is the useful part, not the branded wrapper. “Explanation as artifact” is the piece that travels: a short companion record answering “What is this?”, “Why this approach?”, “What would break?”, and “What did I learn?” Nate explicitly says the principles matter more than where they live and even says to “put it on your personal site” if you want nothing to do with his platform. [Nate article] fileciteturn2file0L83-L95 fileciteturn2file0L141-L157

- “Transactions over credentials” is the tactical career move for Sean right now. Sean is eight weeks into a post-entity["company","The Block","crypto media"] job hunt, targeting AI PM first, then Tech PM, then Creative PM, with Track C already defined as MCP-server / portfolio differentiation. That means the answer is not another course, another badge, or another generalized “AI PM” bio line. The answer is a tight public transaction log of real systems and the judgment behind them. [Sean context] fileciteturn2file1L20-L29 [Nate article] fileciteturn2file0L107-L113

**Verdict:** Nate is right about the labor-market shift and mostly right about the remedy; the thing to bet on is the practice of explanation artifacts, not Nate’s TalentBoard as the canonical home for Sean’s identity. [Nate article] fileciteturn2file0L35-L47 fileciteturn2file0L141-L157 [March/May product references] citeturn19view0turn19view1

## 2. Dissection — The 4-Question Explanation Template Applied to Sean's Existing Work

The key difference between a normal portfolio bullet and a recruiter-grade explanation artifact is that the artifact exposes judgment. Below are five of Sean’s existing assets rewritten in that format, using his real inventory rather than invented projects. These are the pieces that already exist in substance and mostly need packaging. [Sean context] fileciteturn2file1L66-L81 fileciteturn2file1L217-L235 fileciteturn2file1L264-L280 [Nate template] fileciteturn2file0L83-L95

**Superuser Pack v3.20.0**

**What is this?**  
A modular personal operating system for agent-assisted work: 117 skills, 13 subagents, 13 hooks, 14 SDK agents, and three primary domain folders. It exists to turn ad hoc prompting into reusable operating leverage across job search, finance, and creative work.

**Why this approach?**  
I did not want one giant “assistant” prompt that becomes impossible to reason about. I chose a modular pack because the real job was not producing one impressive response; it was making repeated interactions stable, legible, and reusable across domains. The pack lets me separate stable behaviors from changing project context, which makes the system easier to debug and easier to extend.

**What would break?**  
The failure modes are prompt drift, stale hooks, duplicated skills, and over-coupling to a single model vendor. There is also a human failure mode: if the pack grows faster than its naming conventions and decision boundaries, it becomes performance theater instead of leverage.

**What did I learn?**  
Agent leverage compounds only when the human operating model is explicit. The real bottleneck is not “what can the model do?” but “what logic belongs in reusable infrastructure versus session-local judgment?” That distinction is what turns prompting into product thinking. [Sean context] fileciteturn2file1L99-L105 fileciteturn2file1L217-L235

**The Block PM templates**

**What is this?**  
A retained library of PM templates, frameworks, and operating patterns from Sean’s time at entity["company","The Block","crypto media"], preserved specifically for portfolio and future-reference use after the layoff.

**Why this approach?**  
I kept the templates instead of just describing my role because templates are closer to the real unit of PM work. A résumé bullet says I “led” or “coordinated.” A working template shows how I structured ambiguity, how I framed tradeoffs, and what “good” looked like in a live organization.

**What would break?**  
Without context, templates can look generic. The weak version is a downloadable pack with no explanation. The strong version pairs each template with where it was used, what decision it helped unlock, and how I’d adapt it for AI-native teams. Another break point is confidentiality; anything published has to stay on the safe side of company-sensitive detail.

**What did I learn?**  
A surprisingly large portion of PM signal already exists in reusable operating artifacts, but most PMs never publish them because they were trained to narrate outcomes, not expose process design. In 2026, that hidden layer is exactly the differentiator. [Sean context] fileciteturn2file1L66-L68 [Nate article] fileciteturn2file0L51-L57

**Agentic financial-research fleet**

**What is this?**  
A multi-agent research system spanning Perplexity API, Gemini Deep Research MCP, NotebookLM MCP, The Block’s crypto API, and web sources to produce research briefs with summary, recommended action, and path to execution.

**Why this approach?**  
I built this as a fleet instead of a single assistant because the target output is not “a nice answer”; it is a decision-ready brief with clear source roles. Different agents are better at retrieval, synthesis, context accumulation, and execution planning. The architecture mirrors the actual shape of the problem: financial decisions were piling up because source collection, reasoning, and action planning were all bottlenecks.

**What would break?**  
Weak source quality, stale retrieval, conflicting outputs between agents, and invisible assumptions in the synthesis layer. The system can also fail socially: a polished brief can create false certainty if the confidence level and blast radius are not made explicit.

**What did I learn?**  
The real value in “deep research” is not longer text. It is auditability: knowing which agent retrieved which evidence, where disagreement exists, and what would change the recommendation. That is closer to product/evals thinking than to content generation. [Sean context] fileciteturn2file1L217-L220 fileciteturn2file1L247-L252

**2D animation pipeline plan**

**What is this?**  
Sean’s long-term career-R&D pipeline: an agentic-AI-plus-human workflow designed to produce 2D shorts at a real quality bar, with a portfolio short due June 11, 2026 as the first proof piece.

**Why this approach?**  
I did not frame this as a hobby project. I framed it as a production pipeline because the actual long game is a PM role in the animation industry. The point is not merely “make a short.” The point is to design and test a repeatable system that combines tooling, quality gates, and human taste.

**What would break?**  
Three things: quality drift, tool-chain instability, and deadline collapse. A pipeline that can generate frames but not preserve style or editorial intent is not a pipeline. It is a demo. There is also a sequencing risk: if job-search differentiation starts cannibalizing the June 11 proof piece, the project loses its strategic function.

**What did I learn?**  
Creative work is one of the best places to prove comprehension because taste has nowhere to hide. If the artifact is any good, I have to explain not just what the system produced, but what I rejected and why. That is the same skill frontier AI teams now want from PMs. [Sean context] fileciteturn2file1L71-L81 fileciteturn2file1L217-L219 fileciteturn2file1L241-L245

**Phase 6 knowledge loop**

**What is this?**  
An operational knowledge loop inside Sean’s vault: SessionEnd flush, nightly synthesizer, and weekly lint, turning daily work into a maintained second-brain layer that future agents can actually use.

**Why this approach?**  
I chose a loop instead of passive note accumulation because retrieval only works if context keeps getting normalized. The goal was not “have more notes.” The goal was to make future reasoning cheaper and more trustworthy for both me and my agents.

**What would break?**  
If capture becomes inconsistent, if synthesis is too lossy, or if lint does not happen, the vault turns into clutter. The other failure mode is abstraction drift: notes become polished summaries divorced from the real operational decisions they were supposed to preserve.

**What did I learn?**  
Knowledge systems become valuable when they shorten time-to-judgment, not time-to-storage. The loop taught me that agent quality is downstream of context hygiene. That is a strong PM signal because it shows systems thinking, operational design, and respect for failure modes. [Sean context] fileciteturn2file1L264-L270 fileciteturn2file1L278-L280

## 3. The Agentic AI Landscape — Why "Comprehension" Is a Real Hiring Signal Now

Nate’s framing lands because the market has moved from “can you use AI?” to “can you define, constrain, evaluate, and improve AI systems?” The first version is performative AI hiring. The second is real AI hiring. Sean’s profile fits the second path better than the first: beginner-to-intermediate coder, strong systems PM instincts, Claude Code power user, and already operating across MCP, multi-agent workflows, and creative-production pipelines. That combination is unusually good for explanation artifacts because it is grounded in real tradeoffs rather than empty “AI native” branding. [Sean context] fileciteturn2file1L47-L53 fileciteturn2file1L99-L105

The right way to read the “GitHub as résumé is dead” claim is not literal collapse. Here’s an alternative to consider: entity["company","GitHub","software platform"] has not collapsed; its exclusivity has. GitHub’s own 2025 Octoverse says “a new developer joins GitHub every second,” with AI and agents driving major shifts in software development. At the same time, the market now offers industrialized scaffolding everywhere: entity["company","Vercel","cloud platform"]’s template marketplace, public sharing for Anthropic artifacts, live publishing in Lovable, and prompt-to-app flows across Bolt/Replit/Lovable. That means a working repo or app URL is now table stakes, especially for non-engineers and PMs. The differentiator is the comprehension layer attached to it. [GitHub Octoverse] citeturn23view15turn23view16 [Vercel] citeturn23view9turn23view10 [Anthropic artifacts] citeturn19view14turn10search2 [Lovable publish] citeturn19view15

That same pattern shows up in the “portfolio platform” graveyard. entity["company","Read.cv","career profile app"] was acquired by Perplexity and began winding down in January 2025. entity["organization","buildspace","builder community"]’s main site is now a memorial page, while an unofficial-looking discovery layer continues at buildspaceprojects.com. entity["company","Polywork","professional network"] also appears to have shut down around January 31, 2025, but in this session I could only verify that through secondary sources, not a surviving official archival announcement. The takeaway is not “never use platforms.” It is “never let a platform be your only canonical home.” [Read.cv / Perplexity] citeturn23view14 [buildspace] citeturn23view12turn23view13 [Polywork secondary reports] citeturn25search1turn25search7turn25search11

The market is also visibly shifting toward evaluation-driven work. entity["company","Google","technology company"]’s agent stack is blunt about it: the Gemini Enterprise Agent Platform supports both final-response evaluation and trajectory evaluation, and Google’s ADK literally says “Go beyond vibes. Evaluate everything.” entity["company","Cohere","ai company"] says public benchmarks are “necessary but far from sufficient” and argues for evaluation systems tuned to business reality. entity["company","OpenAI","ai company"] now has public Model Spec documents and Model Spec Evals; entity["company","Anthropic","ai company"] publishes system cards; Google DeepMind publishes model cards that explicitly include limitations, mitigations, safety performance, and updated evaluations. This is the exact institutional version of what Nate is describing. Frontier labs are already normalizing explanation artifacts; they just call them model cards, specs, system cards, evals, and ADRs. [Google evals / ADK] citeturn19view10turn19view11 [Cohere evals] citeturn23view8 [OpenAI Model Spec] citeturn23view4turn23view5 [Anthropic system cards] citeturn23view6 [Google model cards] citeturn23view3turn28view0

This matters for AI PM hiring because the interview loop is changing around the same premise. entity["company","Sierra","customer agents"] publicly describes an “AI-native onsite” where candidates plan, build, and review with AI tools, then face system-design and debugging interviews because simple vibe-coding is no longer the meaningful screen. Public job pages at OpenAI emphasize developer APIs, ambiguous technical spaces, “tool use, evals, telemetry, safety constraints,” and deployed product roles at the intersection of product, deployment, and customer strategy. Anthropic’s current public roles include Product Manager, Claude Code; Product Manager, API Growth; and multiple Agent Prompts & Evals / Model Evaluations roles. entity["company","Decagon","ai company"] describes its Agent PMs as “part product manager and part AI consultant,” while Pair Team highlights safety-critical AI, voice and LLM systems in production, and orchestration problems. That is real AI hiring. The signal is not “I use AI daily.” The signal is “I can scope, deploy, evaluate, debug, and explain AI systems in context.” [Sierra interview] citeturn20view2turn20view4 [OpenAI roles] citeturn19view2turn19view3turn19view4turn19view6turn19view13 [Anthropic careers] citeturn13search6turn13search7turn19view12 [Decagon] citeturn19view8turn19view9 [Pair Team] citeturn27view5

So where is the puck going that Nate does not fully see yet? From explanation artifact to explanation-plus-evidence artifact. His four questions are a strong base layer. The next layer is an eval layer: success criteria, failure taxonomy, known breakpoints, logging, and the threshold at which you would not ship. Martin Fowler’s refreshed ADR guidance lands here too: keep decision records short, put the decision, context, alternatives, tradeoffs, and consequences up front, and keep them near the work. For Sean, that means the strongest artifact is not just “what I learned.” It is “here are the evals, here is where this system fails, and here is why I still chose it.” [ADR guidance] citeturn28view1turn28view2 [Product School evals signal] citeturn27view2

## 4. Career Strategy — 8-Week Tactical Plan Anchored to Sean's Situation

Sean’s calendar matters here. The deep-work block is 9:00–14:00, the portfolio short has a hard date of June 11, evenings belong to Mary and recovery, and the job hunt is already organized into Track A / B / C. So the best trade is not “be everywhere.” It is one owned canonical home plus a small number of high-signal transactions shipped on a steady cadence. [Sean context] fileciteturn2file1L24-L29 fileciteturn2file1L153-L170 fileciteturn2file1L241-L245

The actionable target for the full eight-week window is **six public explanation artifacts** and **two private interview packets**. Six is enough to create pattern-recognition for recruiters without consuming the whole runway. Two private packets exist for role customization: one AI PM / developer-tools packet and one creative/consumer PM packet. The artifacts live in four layers, but only one is canonical:

**Canonical:** personal site on Sean’s own domain.  
**Source-of-truth technical layer:** GitHub repos / READMEs / ADR folder.  
**Distribution layer:** LinkedIn featured section plus short posts; one longer essay every other week on Hashnode or Substack, not both every time.  
**Mirror layer:** TalentBoard only if it becomes stable and publicly browseable. [Nate article] fileciteturn2file0L141-L157 [Hashnode] citeturn26search1turn26search2 [Anthropic shareable artifacts] citeturn19view14

This week’s spend wants to stay tiny and owned: **$15–$20** for a domain if Sean does not already have one, **$0–$20/month** for hosting, **$0** for TalentBoard until the product is visibly live, and **$0** for communities or portfolio builders. That fits “build don’t buy” and avoids the trap of spending runway to construct profile theater. The hard cap through June 11 looks like **$100 total** unless Track C needs API credits for a demo that directly improves interview signal. [Sean context] fileciteturn2file1L97-L104

The cadence is straightforward:

**By May 10:** launch the skeleton site with one page called “Transactions” and one page called “How I work with AI.” Do not wait for polish. Anchor the first two artifacts there: Block PM templates and Superuser Pack. These are already real, and both are high confidence. [Sean context] fileciteturn2file1L66-L68 fileciteturn2file1L221-L235

**By May 17:** publish the agentic financial-research fleet artifact and a short “What would break?” companion ADR. This becomes the flagship AI PM proof because it shows orchestration, multi-source reasoning, and decision support rather than mere prototype generation. [Sean context] fileciteturn2file1L217-L220

**By May 24:** publish the Phase 6 knowledge loop artifact. This is the most underrated one for AI-native employers because it shows context hygiene, memory architecture, and second-order thinking about agent quality. [Sean context] fileciteturn2file1L264-L270

**By June 7:** publish the Track C MCP server artifact if it is built, or publish the design brief plus ADR pack if the code is still in flight. In real AI hiring, a clean architecture decision pack often beats a half-working app. [MCP] citeturn23view0turn23view1turn23view2

**By June 11:** publish the animation pipeline artifact next to the short itself, even if the short is still “portfolio-short alpha.” In this market, the explanation layer around a high-taste pipeline can matter as much as the artifact. [Sean context] fileciteturn2file1L71-L81

**By July 4:** six artifacts live, two role packets cut, and the résumé/LinkedIn/e-mail signature all point to one owned “Transactions” page rather than a generic home page. [Sean context] fileciteturn2file1L20-L29

The recruiter-funnel mechanic is simple and practical. A generic portfolio link rarely converts because it asks for too much interpretation. A role-specific artifact link converts because it removes interpretation. Resume bullet -> LinkedIn featured item -> owned artifact page -> 90-second demo -> four-question explanation -> “what I’d improve next” -> contact CTA. That works for outbound and inbound. The move in outreach is not “here is my portfolio.” It is “I built and documented a decision-ready MCP research system / AI-native PM template pack / animation production pipeline that maps directly to your role; here’s the artifact page.” In other words: transaction first, credentials second. [Nate article] fileciteturn2file0L107-L113

## 5. Portfolio Products to Build (Job-Search Signal)

These are not hypothetical side quests. They are the publishable wrappers around Sean’s actual material. Each one is hard to fake because the strongest part is the explanation, not the demo.

**AI PM artifact: “MCP Research Analyst for Financial Decisions”**  
**What it is:** a public writeup plus repo/demo of the multi-agent financial-research fleet, with one sample brief and an ADR on source routing.  
**4Q explanation:** This is a decision-support system that turns scattered financial sources into auditable briefs; I chose a multi-agent design because retrieval, synthesis, and action planning are distinct jobs; it breaks when source freshness or agent-role boundaries degrade; I learned that evaluation and confidence labeling matter more than longer summaries.  
**Where it gets published:** personal site + GitHub README + one Hashnode/Substack essay.  
**Who finds it:** AI infra recruiters, developer-tools PMs, startup founders hiring technical PMs.  
**Recruiter-eye headline:** “Built an MCP-based research analyst that turns noisy sources into auditable action briefs.” [Sean context] fileciteturn2file1L217-L220 [MCP / GitHub] citeturn23view0turn23view1

**AI-native PM artifact: “The Block Templates, Rewritten for Agent Teams”**  
**What it is:** a sanitized pack of PM templates from Sean’s Block work with attached explanation artifacts showing what each template is for, when it fails, and how it changes for AI-native teams.  
**4Q explanation:** This is a set of operating templates I used and retained from a live product org; I’m publishing them because templates are closer to the real unit of PM work than résumé bullets; the pack breaks if it is generic or detached from decision context; I learned that PM process itself is publishable proof when paired with tradeoff rationale.  
**Where it gets published:** personal site, downloadable PDF, selected GitHub markdown templates.  
**Who finds it:** PM hiring managers, recruiter screens, other PMs who share it.  
**Recruiter-eye headline:** “I don’t just talk about PM process — here are the decision frameworks I actually use.” [Sean context] fileciteturn2file1L66-L68

**Systems-thinking artifact: “My Phase 6 Knowledge Loop”**  
**What it is:** a visual explainer of SessionEnd flush -> nightly synth -> weekly lint -> retrieval, with one concrete example of how an agent gets smarter because the loop exists.  
**4Q explanation:** This is the memory and context hygiene layer behind my agent stack; I chose a loop because passive note piles do not improve future judgment; it breaks when capture, synthesis, or lint becomes inconsistent; I learned that better memory architecture improves agent quality more reliably than swapping models.  
**Where it gets published:** personal site + GitHub ADR folder + short LinkedIn carousel.  
**Who finds it:** Anthropic/OpenAI-style teams, productivity infra teams, anyone hiring for agent ops / PM systems thinking.  
**Recruiter-eye headline:** “I designed the memory loop that keeps my agents from becoming context goldfish.” [Sean context] fileciteturn2file1L264-L270 fileciteturn2file1L278-L280

**Creative-tech artifact: “2D Animation Pipeline with Human Taste Gates”**  
**What it is:** the June 11 short plus the production-system writeup behind it.  
**4Q explanation:** This is a human-plus-agent pipeline for producing 2D animation at a real quality bar; I chose a pipeline framing because the long game is repeatable production, not one-off novelty; it breaks when style consistency, editorial intent, or deadline discipline slips; I learned that creative quality gates are the cleanest proof that I understand both system design and taste.  
**Where it gets published:** personal site first, then a shareable artifact/demo link.  
**Who finds it:** creative-tech companies, consumer product teams, animation-adjacent PM searches.  
**Recruiter-eye headline:** “Designed a repeatable AI-assisted animation pipeline instead of shipping a one-off demo.” [Sean context] fileciteturn2file1L71-L81

**Meta-signal artifact: “Superuser Pack as a PM Operating System”**  
**What it is:** a cleaned-up public case study of the Superuser Pack showing system boundaries, guardrails, and why the architecture is modular.  
**4Q explanation:** This is my reusable agent operating system for work across domains; I chose modular skills, subagents, and hooks over a monolith because maintainability matters more than wow-factor; it breaks when naming, governance, and dependency boundaries drift; I learned that agent design is product design when the user is your future self.  
**Where it gets published:** personal site + GitHub docs.  
**Who finds it:** AI-native startups, developer-tools teams, hiring managers who want evidence of real operator behavior.  
**Recruiter-eye headline:** “Built a reusable agent operating system, not a pile of clever prompts.” [Sean context] fileciteturn2file1L221-L235

## 6. Sellable Products (Cushion-Building Income Streams Aligned to the Comprehension Thesis)

Sean’s north star is a cushion and multiple income streams, with a bias toward “every win counts.” That makes low-overhead, explanation-centered products a much better fit than a grand SaaS moonshot right out of the layoff window. [Sean context] fileciteturn2file1L89-L105 fileciteturn2file1L247-L252

**Comprehension Review service**  
**Who buys it:** founders, PMs, and nontraditional builders who have AI-built apps or workflows and know they cannot explain them cleanly in hiring, selling, or deployment settings.  
**Why:** they need a structured “What is this / Why this / What breaks / What I learned” review, plus a short blast-radius memo.  
**Build cost:** roughly **$0–$150** this month for a landing page + intake form + sample deliverable.  
**Run cost:** mostly Sean’s time; maybe **$10–$40/month** in model/API spend.  
**Low-effort distribution:** LinkedIn and one case-study post showing before/after explanation quality.  
**Why it resists six-month commoditization:** the defensible piece is not text generation; it is pressure-testing judgment with PM framing, eval instincts, and human challenge. The product is discernment, not formatting. [Nate template prompt] citeturn23view11

**Explanation Artifact Kit**  
**Who buys it:** AI PMs, indie hackers, job seekers, and founders who want an owned portfolio system.  
**Why:** they need templates for project cards, ADRs, failure logs, recruiter packets, and personal-site transaction pages.  
**Build cost:** **$0–$200** depending on whether Sean includes sample site components.  
**Run cost:** near zero.  
**Lowest-effort distribution:** Gumroad/website sell page, plus a free lite version on GitHub.  
**Price point:** **$29 basic / $79 pro** is realistic.  
**Why it resists commoditization:** generic templates are free; credible templates pre-loaded with agent/evals/MCP patterns and PM-grade examples are rarer. The differentiation is example quality. [ADR guidance] citeturn28view1turn28view2

**Repo-to-Artifact CLI**  
**Who buys it:** developers, PMs, and hiring candidates with repos but weak documentation.  
**Why:** it turns repo structure, ADRs, commit history, and issue context into a first-draft explanation artifact.  
**Build cost:** roughly **$0 cash / 20–40 focused hours** if Sean uses existing tooling and keeps v1 narrow; **$200–$500** if API-heavy.  
**Run cost:** negligible for a local CLI; small for hosted SaaS.  
**Lowest-effort distribution:** open-source on GitHub with a paid hosted version later.  
**Why it resists commoditization:** the wedge is not “generate README.” It is “infer rationale, alternatives, breakpoints, and missing-eval gaps.” That nudges it from commodity writing tool into comprehension diagnostics. [GitHub / MCP context] citeturn23view0turn23view15

**MCP Comprehension Linter**  
**Who buys it:** teams and solo builders shipping MCP servers or agent tools.  
**Why:** MCP adoption is growing fast, but server quality, safety boundaries, and documentation quality are uneven. A linter that asks “what would break?” for tools, permissions, schemas, and eval coverage is directly useful.  
**Build cost:** **$300–$1,000** in opportunity cost and infra depending on how much static analysis vs LLM review it includes.  
**Run cost:** **$10–$50/month** at small scale.  
**Lowest-effort distribution:** MCP community channels, GitHub repo, and one public teardown of Sean’s own Track C server.  
**Why it resists commoditization:** MCP is a growing but still specialized niche, and the value is operational nuance, not generic syntax linting. [MCP spec / roadmap] citeturn23view1turn23view2

**AI PM teardown newsletter**  
**Who buys it:** PMs and builders trying to separate real agent products from demo theater.  
**Why:** weekly “explanation artifact case studies” are useful if the voice is sharp, practical, and grounded in real examples.  
**Build cost:** essentially **$0**.  
**Run cost:** time only.  
**Lowest-effort distribution:** Substack.  
**Why it resists commoditization:** only if Sean keeps the bar high and writes from actual build experience. Otherwise this is the easiest one to get flattened by the market, which makes it better as a lead-gen layer than the main income bet. [Hashnode/Substack-style reputation layer] citeturn26search1

The sequencing trade is clear: **service first, kit second, tool third**. Service creates cash fastest. Kit productizes patterns. Tool only earns the build time once Sean sees repeated demand.

## 7. Where Nate Is Probably Wrong / What He's Underselling

Steel-man first: Nate is describing a real market break. He is also right that the apprenticeship ladder has weakened, that public proof matters more now, and that a short explanation layer can expose real understanding faster than a polished demo can. His prompt kit is also well aimed: pressure-testing the artifact with AI before publishing it is useful, and it aligns with what frontier teams increasingly care about. [Nate article] fileciteturn2file0L21-L33 fileciteturn2file0L83-L95 [Prompt Kit] citeturn23view11

Where he overreaches is infrastructure. The line that there is “literally nowhere to put” AI work with context is too strong. There are already many places to publish work with varying levels of context: owned sites, GitHub READMEs, ADR folders, public Anthropic artifacts, Lovable publish URLs, Hashnode blogs, Vercel templates as distribution scaffolds, and even Show HN as a launch stage. The problem is fragmentation and weak defaults, not absolute absence. [Nate article] fileciteturn2file0L145-L157 [Anthropic artifacts / Lovable / Vercel / Hashnode] citeturn19view14turn19view15turn23view9turn26search1 [Show HN example] citeturn8search3

TalentBoard itself looks much more like early creator monetization and audience capture than durable hiring infrastructure so far. As of May 6, 2026, the things I could verify were: the Substack article, the prompt kit, intake/queue language, a later Substack reference still pointing readers toward TalentBoard signup, and a March post announcing “Nate’s Network” beta as a vetted AI talent network. I could not verify a public, searchable, independently discoverable artifact directory with export guarantees, hiring-manager adoption, or long-term platform stability. That does not mean it will fail. It does mean Sean’s canonical identity does not belong there. [Nate article] fileciteturn2file0L35-L47 [March/May references] citeturn19view0turn19view1

The realistic adoption curve for explanation artifacts is also slower than the article implies. Hiring managers at AI-native companies will appreciate them now. Recruiters and mainstream PM companies will not suddenly browse a new platform and rewire their funnels around it. So the bet is not “the market will adopt TalentBoard.” The bet is “the discipline of producing explanation artifacts makes Sean better at screening calls, recruiter follow-ups, hiring-manager reviews, and live interviews regardless of where the artifact lives.” That is a much safer bet. [OpenAI interview guide] citeturn19view13 [Sierra / Decagon / Anthropic public signals] citeturn20view2turn19view8turn19view12

What Nate undersells is the eval layer. In the real 2026 agent market, explanation without evaluation is already starting to feel incomplete. The highest-signal artifact is not just “what I built and what I learned.” It is also “how I know it works, where it fails, and what threshold would make me stop shipping it.” That is where Sean has a chance to beat most portfolio builders, because he is already closer to agent harness / decision-system thinking than to vibe-coded demo culture. [Google / Cohere / OpenAI evals] citeturn19view10turn19view11turn23view8turn23view5

## 8. The 5 Decisions Sean Needs to Make This Week

1. **Decision: where the canonical “TalentBoard” lives.**  
   **Default:** Sean’s own site is canonical; GitHub is source-adjacent; TalentBoard is a mirror if it becomes real.  
   **Switch only if:** TalentBoard launches with stable public pages, exportability, and visible recruiter discovery that Sean can verify firsthand. [Platform fragility / TalentBoard ambiguity] citeturn23view14turn23view12turn25search1turn19view0turn19view1

2. **Decision: what the flagship AI PM proof is.**  
   **Default:** lead with the MCP/financial-research artifact, because it is the cleanest intersection of AI PM, orchestration, system design, and real-world decisions.  
   **Switch only if:** a target role is explicitly consumer/creative-first, in which case the animation pipeline becomes the front door. [Sean context] fileciteturn2file1L71-L81 fileciteturn2file1L217-L220

3. **Decision: how many artifacts to publish before June 11.**  
   **Default:** four by June 11, six by July 4.  
   **Switch only if:** live interview volume spikes enough that role-specific interview prep is clearly higher ROI than another public transaction. [Sean timeline] fileciteturn2file1L24-L29 fileciteturn2file1L241-L245

4. **Decision: whether to spend money on portfolio tooling.**  
   **Default:** keep spend under **$100 through June 11** — domain, hosting, maybe a tiny amount of API spend tied to one demo.  
   **Switch only if:** a paid tool directly improves a flagship artifact that Sean will use in applications within the next 14 days. [Sean values] fileciteturn2file1L97-L104

5. **Decision: which income-stream bet to place first.**  
   **Default:** offer the Comprehension Review service first at a starter rate in the **$150–$300** range for the first 3–5 pilots, then turn repeated patterns into a template kit.  
   **Switch only if:** Sean gets repeated inbound demand for a productized template/tool faster than he can comfortably fulfill service work. [Sean north star] fileciteturn2file1L89-L105

## 9. Open Research Questions

- I could not verify a public standalone TalentBoard product beyond the article, prompt kit, and sign-up references. The relationship between “TalentBoard” and “Nate’s Network” still looks ambiguous from public materials. [Public references] citeturn19view0turn19view1turn23view11

- Public detail on PM interview loops at Anthropic and OpenAI remains thinner than the public detail Sierra provides for engineering interviews. The hiring signal is inferable from jobs and company writing, but not fully observable end to end. [OpenAI / Anthropic / Sierra] citeturn19view13turn19view12turn20view2

- Polywork’s shutdown appears real, but in this session I did not find a surviving official archival statement — only consistent secondary references and remnants. [Secondary references] citeturn25search1turn25search7turn25search11

- If Sean wants to publish the deepest technical internals of Phase D typed reasoning edges, a follow-up pass should check whether anything in that material is better framed as a private interview packet rather than a public artifact.