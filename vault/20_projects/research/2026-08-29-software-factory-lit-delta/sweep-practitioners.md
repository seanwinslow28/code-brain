# Sweep — independent practitioner write-ups (2026-08-29)

Research-agent sweep, 12 pages fetched and read. Quotes verbatim as extracted; access
caveats flagged inline. Feeds the 2026-08 delta synthesis. The corpus-level pattern:
**credible practitioners converge on simpler orchestration than the hype layer claims**,
and the two best pieces are explicitly negative results.

---

## 1. Geoffrey Huntley — "Ralph Wiggum as a 'software engineer'"

- **URL:** https://ghuntley.com/ralph/ — July 14, 2025
- **CLASSIFICATION:** Practitioner-testimony (runs it, documents failure modes)
- The entire orchestrator is a bash one-liner: `while :; do cat PROMPT.md | claude-code; done` — one task per loop iteration.
- Economics: a $50k contract delivered as MVP for **$297** in tokens; "6 Repos Overnight" at a YC hackathon.
- Fan-out inside the loop: "up to 500 parallel subagents" for read/search only; **1** for builds/tests (serialization as a correctness gate).
- Context degrades "around 147k-152k tokens despite 200k advertised limit."
- "There's no way in heck would I use Ralph in an existing code base."
- "Anyone claiming tools do 100% work without engineers is peddling horseshit." Expects ~90% completion; final 10% is human.
- **Worked:** greenfield, spec-driven porting, self-updating AGENT.md. **Failed:** duplicate implementations; placeholder code unless aggressively prompted; non-compiling states needing hard resets.
- **Verification:** mandatory static analysis + unit tests after each change, with documented *why* per test so future loops don't delete them.

## 2. Armin Ronacher — "Agentic Coding Things That Didn't Work"

- **URL:** https://lucumr.pocoo.org/2025/7/30/things-that-didnt-work/ — July 30, 2025
- **CLASSIFICATION:** Practitioner-testimony — pure negative-results post
- Slash commands: "there's only one way to pass arguments, and it's unstructured. This proves suboptimal in practice."
- `/fix-bug`: "no meaningful improvement over simply mentioning the GitHub issue URL."
- Hooks: "haven't seen any efficiency gains from them yet."
- Sub-agents: "tasks that don't parallelize well… create chaos."
- What replaced all of it: speech-to-text + conversation — "simply taking time to talk to the machine… outperforms elaborate pre-written prompts."

## 3. Armin Ronacher — "A Year Of Vibes"

- **URL:** https://lucumr.pocoo.org/2025/12/22/a-year-of-vibes/ — December 22, 2025
- **CLASSIFICATION:** Practitioner-testimony (year-end retrospective)
- "Almost entirely hands-off" in Claude Code — but still no multi-agent orchestration after a full year; tools sequential, not coordinated. Rejected MCP for his needs.
- "I still treat it like regular software engineering and review a lot." Unreviewed AI OSS contributions are "an insult."
- "nothing beyond vibes to back up my preference" on models; flags incentive-contaminated model discourse.
- "Agency and responsibility should remain with humans."

## 4. Simon Willison — "Embracing the parallel coding agent lifestyle"

- **URL:** https://simonwillison.net/2025/Oct/5/parallel-coding-agents/ — October 5, 2025
- **CLASSIFICATION:** Practitioner-testimony (converted skeptic)
- Prior objection: "It's tough keeping up with just a single LLM given how fast they can churn things out."
- Resolution: parallelism only for work that *doesn't* compete for review attention — research/PoCs, codebase Q&A, low-stakes maintenance, tightly specified tasks.
- Carefully specified work needs "substantially less review effort." Never endorses parallel feature development.
- Single-digit concurrency; fresh /tmp checkouts; wants containerized agents against prompt injection.
- Lead not fetched: 2026 Cursor thousand-agent FastRender experiment coverage incl. "unsurprising skepticism."

## 5. Simon Willison — "Vibe engineering"

- **URL:** https://simonwillison.net/2025/Oct/7/vibe-engineering/ — October 7, 2025
- **CLASSIFICATION:** Practitioner-testimony / framing essay
- "If your project has a robust test suite agentic coding tools can fly with it."
- Parallel agents "surprisingly effective, if mentally exhausting."
- Agents "will absolutely cheat if you give them a chance" — hence tests, preview environments, manual QA.
- The essay is a canonical solo-operator verification stack: tests, planning, docs, review, QA, previews.

## 6. Kieran Klaassen — "My AI Had Already Fixed the Code Before I Saw It" (Every.to)

- **URL:** https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it — August 18, 2025
- **CLASSIFICATION:** Practitioner-testimony (solo GM of Cora, thousands of users)
- Compound engineering = "systems with memory, where every pull request teaches the system, every bug becomes a permanent lesson."
- "AI engineering makes you faster today. Compounding engineering makes you faster tomorrow, and each day after."
- Runs **three parallel agents**: planning / development / review — the most honest count in the corpus.
- Failure→eval pipeline: silent email failure → "wrote tests that catch similar delivery lapses, updated monitoring rules… and built evaluations that continuously verify the delivery pipeline."
- TDD-first; 10x repeat runs for flakiness; review agent judges against documented preferences.
- Caveat: the Feb-2026 "Compound Engineering: The Definitive Guide" fetched as promotional (productized plugin, ~7k stars claimed; Every runs "all five of its products with single-person engineering teams") — treat the 2025 essay as testimony, the 2026 guide as marketing.

## 7. Walden Yan (Cognition/Devin) — "Don't Build Multi-Agents"

- **URL:** https://cognition.com/blog/dont-build-multi-agents — June 12, 2025
- **CLASSIFICATION:** Practitioner-testimony from a commercial agent lab; the sweep's strongest architectural negative result
- "Share context, and share full agent traces, not just individual messages."
- "Actions carry implicit decisions, and conflicting decisions carry bad results" — the Flappy Bird example: parallel subagents made incompatible implicit choices; the merger inherited both mistakes.
- Recommends single-threaded linear agents; context-compression model over parallel branching for long tasks.
- Notes Claude Code avoids parallel subagents except isolated read-only questions; early two-model edit pipelines failed on inter-model miscommunication.

## 8. Mitchell Hashimoto — "Vibing a Non-Trivial Ghostty Feature"

- **URL:** https://mitchellh.com/writing/non-trivial-vibing — October 11, 2025
- **CLASSIFICATION:** Practitioner-testimony (session-by-session, with receipts)
- One real macOS feature: **16 agent sessions, $15.98 total** — the corpus's most precise cost datapoint.
- Amp + "oracle" planning subagent; human as orchestrator.
- "Please don't ever ship AI-written code without a thorough manual review."
- **Failed:** titlebar layout + backend state — he *manually restructured the view model* to give the agent a workable foundation.

## 9. Ryan Carson — `ai-dev-tasks`

- **URL:** https://github.com/snarktank/ai-dev-tasks — ~7.8k stars
- **CLASSIFICATION:** Practitioner-authored workflow doc. **Access caveat:** the "15 agents 24/7" narrative lives in video/podcast only; no first-person prose write-up of the fleet found. The repo is the written core.
- Three-file loop: create-prd → generate-tasks → process-task-list.
- Human gate at every step: "allows you to review and approve AI-generated code at each small step" — sub-task 1.1, stop, wait for approval.
- The written artifact is materially more conservative than the talk-circuit claim; the 15-agent count is unverifiable in writing.

## 10. Peter Steinberger — "Just Talk To It — the no-bs Way of Agentic Engineering"

- **URL:** https://steipete.me/posts/just-talk-to-it — October 14, 2025
- **CLASSIFICATION:** Practitioner-testimony — the sweep's best simplification post-mortem
- Runs **3–8 agents in parallel**, "most of them in the same folder" — after trying and **abandoning**: git worktrees, branch-per-change, orchestrators (Conductor, Terragon, Sculptor), subagents, most MCPs, spec-driven development.
- "Don't waste your time on stuff like RAG, subagents… Just talk to it."
- "gpt-5-codex on mid settings. It's a great compromise of smart & speed."
- ~$1k/month across 5 subscriptions; subscriptions "by far the best deal" (~10x cheaper than API).
- Outlier on review laxity ("ships code he doesn't read" per Pragmatic Engineer coverage; later joined OpenAI) — every other practitioner here contradicts that posture.

## 11. Steve Yegge — "Revenge of the Junior Developer" (via mirrors; original 403'd)

- **Original:** https://sourcegraph.com/blog/revenge-of-the-junior-developer — 403'd on every attempt. Read via frontendmasters.com commentary and tcole.net excerpts.
- **CLASSIFICATION:** Commentary/prediction — forecasts fleets, does not document running one.
- "Agents are coming. Vast fleets of them." Six-wave model ending in agent fleets (2026) with AI supervisors managing leaf-node agents.
- **Caveat:** his widely-cited per-dev token-cost figures could not be verified from a fetched source — do not cite without getting past the 403.

## 12. Allie K. Miller — "Behind The Agentic AI Experiment"

- **URL:** https://www.alliekmiller.com/behind-the-agentic-ai-experiment — undated
- **CLASSIFICATION:** Commentary/promotional. **No substantive written version of "build the factory, not the product" found** — the framing lives in the Isenberg podcast and social posts; the 34-agent-workforce claims are unverifiable from her page.
- The page's one concrete pipeline is a *content* factory (RSS → scrape → filter → rank → summarize → **human review** → publish).
- Cite her as the framing's popularizer, not as documented practice.

---

## Cross-cutting synthesis (research agent)

1. **The claim-vs-count gap is the story.** Claimed: 15 (Carson, video), 34 (Miller, podcast), "vast fleets" (Yegge, prediction). Documented with receipts: 3 (Klaassen), 3–8 (Steinberger), single-digit (Willison), 1 loop (Huntley), 1 agent/16 sessions (Hashimoto). Written testimony runs ~4x lower than talk-circuit numbers, every time.
2. **The simplification arc is near-universal.** Steinberger abandoned orchestrators/worktrees/subagents; Ronacher abandoned commands/hooks/subagents; Cognition says don't build multi-agents; Huntley's orchestrator is a bash while-loop. Convergence: few agents, shared context, human on the seam.
3. **Where evals sit separates testimony from hype.** Klaassen (failure→test→monitor→eval), Willison (test suite as speed enabler + "they will absolutely cheat"), Huntley (typecheckers + test-rationale docs), Hashimoto (hard manual gate), Carson (per-sub-task approval). The pieces with no verification story are the pieces with the biggest agent counts.
4. **Cost discipline is subscription arbitrage + local caps:** $1k/month subs ≈ 10x cheaper than API (Steinberger); $15.98/feature (Hashimoto); $297 MVP (Huntley). Model mixing modest: cheap-fast default, rare escalation.
5. **Citable negative results:** Ronacher's scaffolding that didn't pay; Cognition's parallel-writer conflict; Steinberger's orchestrator abandonment; Huntley's duplicate-implementation and context-clipping failures; Hashimoto's human-restructured foundation; Cursor FastRender skepticism at the thousand-agent extreme.

**Gaps for follow-up:** Yegge original (needs a browser past the 403); Carson fleet specifics (video-only — `watch` skill could transcribe); Every's paywalled guide internals (public plugin repo exists).
