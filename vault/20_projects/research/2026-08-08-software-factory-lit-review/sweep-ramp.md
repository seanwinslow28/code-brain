All sources gathered. Compiling the report.

# Ramp — First-Party Literature Sweep: AI-Assisted / Agent-Driven Software Development

## 1. "Why We Built Our Own Background Agent" — Ramp Builders Blog (first-party)
**URL:** https://engineering.ramp.com/post/why-we-built-our-background-agent — date not on page; covered by InfoQ Jan 2026, so ~Dec 2025.

- **ADOPT — Close the verification loop, not just the writing loop.** Inspect doesn't just write code; it *proves* its work the way an engineer would: runs tests, reviews telemetry, queries feature flags for backend; takes screenshots and live previews (real Chromium via VNC) for frontend, and attaches before/after screenshots to PR descriptions.
- **ADOPT — Snapshot-based sandbox freshness.** Pre-built image per repo, rebuilt every 30 minutes; filesystem snapshots freeze/restore state so every session starts near-instantly on a repo at most 30 minutes stale. Sandboxes are pre-warmed the moment a user starts typing.
- **ADOPT — Full-environment sandboxes.** Each session is a Modal VM with everything local dev has (Vite, Postgres, Temporal), wired into Sentry, Datadog, LaunchDarkly, Braintrust, GitHub, Slack, Buildkite. OpenCode is the agent runtime (chosen for server-first architecture, typed SDK, plugin system); Cloudflare Durable Objects + per-session SQLite for the API layer.
- **CONTEXT — ~30% of all merged PRs** to frontend and backend repos written by Inspect, reached "in a couple months," with zero mandated adoption — virality came from letting the agent work in public spaces (Slack) plus multi-entry-point workflows (Slack bot, web UI, Chrome extension, PR comments, voice).
- **CAUTION — Don't create a vector for unreviewed code.** They explicitly authenticate agent actions via GitHub identity so a user can't approve their own agent's changes; a warning stated in the post as a deliberate security design decision.
- **CAUTION — Sync discipline:** block file edits until repo synchronization completes; queue follow-up prompts rather than interrupting in-flight work.

## 2. Modal blog — "How Ramp built a full context background coding agent on Modal" (vendor post, but with named Ramp engineers quoted first-person)
**URL:** https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal — Feb 19, 2026.

- **CONTEXT — Adoption grew from ~30% to 50%+ of merged PRs** started by Inspect between the first-party post (~Dec 2025) and Feb 2026; 80%+ of Inspect's own codebase was written by Inspect.
- **ADOPT — Speed parity with local is the adoption gate.** Rahul Sengottuvelu (Head of Applied AI, since promoted to CTO) first-person: sandbox startup time was the make-or-break variable; they designed to be "as close to the speed of a local agent as possible."
- **ADOPT — Start tiny, iterate at low risk.** Zach Bruggeman (engineer) first-person: first version took "a few days"; his stated philosophy is that AI lets you try many things quickly at very little risk.
- **CONTEXT — Zero-setup expands users beyond engineers:** PMs and designers ship code because there's no dev-environment setup; framed as "hundreds of computers" per builder.
- **CONTEXT — Multiplayer sessions** (shared live sessions with colleagues) are treated as mission-critical, a feature Ramp claims not to have seen elsewhere.

## 3. "Meet Ramp Research: Our Agentic Data Analyst" — Ramp Builders Blog (first-party)
**URL:** https://engineering.ramp.com/post/meet-ramp-research — Sept 18, 2025 (authors Faiz Hilaly, Cesar Duran, Jay Sobel).

- **ADOPT — Give the agent inspection tools, not just retrieval.** The agent inspects actual column values, branches, and backtracks through the warehouse rather than relying on keyword/vector search over docs; row-level inspection was often required for correctness.
- **ADOPT — Curated context layer over raw metadata:** aggregated dbt/Looker/Snowflake metadata plus domain docs *maintained by named analytics owners* on a filesystem the agent can read. Generic metadata compression alone was insufficient.
- **ADOPT — Assertion-based eval on the context layer.** Human-in-the-loop validation "reintroduced the core bottleneck"; replaced with a custom Python mini-framework in the dbt project asserting final answers, intermediate steps, expected tool calls, table references, and query shape.
- **CONTEXT — Numbers:** 1,800+ questions, 1,200+ conversations, 300 users; a 4-week snapshot showed 1,476 questions in the agent channel vs 66 in the human help channel — a 10-20x increase in questions asked. Their headline lesson: collapsing question cost to near-zero changes *who* asks, *when*, and *what*.
- **CAUTION — PII explicitly excluded** from the agent's data access.

## 4. "How To Build Agents Users Can Trust" (expense/policy approval agent) — Ramp Builders Blog (first-party)
**URL:** https://builders.ramp.com/post/how-to-build-agents-users-can-trust — date not on page (~2025).

- **ADOPT — Problem-selection framework:** automate only where the task is (1) ambiguous (heuristics fail), (2) high-volume, and (3) asymmetric-upside (automation value far exceeds occasional-error cost).
- **ADOPT — LLM judgment inside deterministic rails:** dollar limits, vendor blocklists, category restrictions, and workflow hard-stops wrap the LLM; an "autonomy slider" graduates customers from suggestions → subset actions → full autonomy.
- **ADOPT — Citations as explainability:** every decision ships with reasoning plus direct links to the specific policy section; three-way bucketing (Approve/Reject/Needs Review) instead of confidence scores, because LLM confidence scores are unreliable — and "I'm not sure" is designed as a *valid, trust-building* outcome.
- **ADOPT — Evals from production:** user-flagged errors become test cases; internally-reviewed golden datasets counteract the discovered bias that human reviewers are *more lenient than written policy* (naive labeling would have taught the agent the wrong standard).
- **CONTEXT — 65%+ of Ramp's own expense approvals** are now fully handled by the agent.

## 5. Anthropic/Claude case study — "Ramp" (vendor case study with named Ramp engineers)
**URL:** https://claude.com/customers/ramp — undated (~2025). Quotes Austin Ray (Senior SWE) and Zack Field (engineer).

- **CONTEXT — Headline numbers (vendor-published, treat accordingly):** 1M+ lines of AI-suggested code implemented in 30 days; 50% weekly-active Claude Code usage across engineering; up to 80% reduction in incident-investigation time.
- **ADOPT — Autonomous test loop:** custom CLI extensions connect Claude Code to test frameworks so it analyzes failures and adjusts code in a closed cycle.
- **ADOPT — Incident-response via MCP:** Claude Code wired to Datadog/Sentry through MCP servers autonomously aggregates logs, errors, metrics for triage — the source of the 80% claim.
- **ADOPT — Parallel sessions + ticket-to-code:** multiple concurrent sessions on one codebase; direct project-tracker connections so requirements flow to implementation without manual copying.
- **CONTEXT — Grassroots, not mandate:** adoption spread engineer-to-engineer; non-technical staff (sales, risk, accounting, recruiting) query Snowflake in natural language via the same tooling.

## 6. Rahul Sengottuvelu — AI Engineer Summit talk "Rethinking how we Scaffold AI Agents" (first-person talk; only partially verifiable by fetch)
**URLs:** https://www.youtube.com/watch?v=7Xp-74yZ964 ; announcement https://x.com/aiDotEngineer/status/1902439181143699952 ; summary https://inferencebysequoia.substack.com/p/how-ramp-solved-the-fatal-flaw-in — March 2025.

- **CONTEXT — Thesis (verified from event's own framing):** stop over-engineering agents — "systems that scale with compute beat systems that don't" (bitter-lesson applied to agent scaffolding: prefer LLM-in-a-loop with generic tools over handcrafted DAGs/heuristics).
- **ADOPT — "Computer use yourself" (verified direct claim):** rather than building a bespoke tool API for every feature, let agents drive your *existing frontend* — the UI is already a complete, permissioned interface layer.
- **CAUTION — I could not fetch a full transcript**, so I am not asserting the talk's specific accuracy/cost numbers here; watch the YouTube video directly if the switching-report architecture-generations detail matters to the campaign.

---

## What Ramp's material implies for a solo founder running an agent fleet that builds and operates one product

- **Verification is the product, not the agent.** Every Ramp system that scaled (Inspect, Ramp Research, Policy Agent) wins by closing its own loop — tests, telemetry, screenshots, assertions — before a human looks. A solo fleet should invest in the proof harness before adding more agents.
- **Environment freshness beats agent cleverness.** The 30-minute snapshot rebuild + pre-warmed sandbox pattern is copyable at small scale (your Modal/worktree equivalent): agents on stale checkouts or cold environments lose to fast, current ones regardless of model.
- **Deterministic rails + explicit "unsure" outcomes are what let agents operate (not just build) a product.** Dollar-limit-style hard rules, citation-backed decisions, and a designed escape hatch replaced confidence scores — directly transferable to any agent that touches production or customers.
- **Evals should live where the context lives, and grow from production errors:** assertion tests inside the dbt project, user-flagged mistakes promoted to golden cases, and internally-reviewed golden data to avoid learning human leniency. Cheap, incremental, no eval-platform required.
- **Don't let the fleet approve itself.** Ramp's one explicit security warning — authenticate agent actions to a human identity so no path exists for unreviewed code to merge — is *more* acute for a solo operator, where you are the only reviewer.

**Coverage note:** Ramp's first-party engineering material on this topic is real but modest — roughly 3-4 substantive engineering.ramp.com/builders.ramp.com posts (background agent, Ramp Research, agent trust, plus product-ML posts like merchant matching), with the richest numbers actually living in vendor co-published pieces (Modal, Anthropic) that quote Ramp engineers first-person; talks by Sengottuvelu exist but lack fetchable transcripts.