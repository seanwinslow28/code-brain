# Sweep — non-lab company engineering writing (2026-08-29)

Research-agent sweep, 9 pieces read via WebFetch. Quotes as extracted from fetched pages.
Ordered by evidentiary value. Feeds the 2026-08 delta synthesis; complements (does not
replace) the 2026-08-08 sweeps in `2026-08-08-software-factory-lit-review/`.

---

## 1. Stripe — "Minions: Stripe's one-shot, end-to-end coding agents" (Part 1)

- **URL:** https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents — Stripe Dot Dev Blog, Alistair Gray, Feb 9, 2026
- **CLASSIFICATION: Practitioner testimony** (production system, metrics, internal infra specifics)
- **Key claims:**
  - Harness is a "fork of Block's coding agent goose" customized to "interleave agent loops and deterministic code"
  - Volume: "Over a thousand pull requests merged each week at Stripe are completely minion-produced"
  - Output is "human-reviewed" but "contain[s] no human-written code"
  - Central internal MCP server: "Toolshed, which hosts more than 400 MCP tools"
  - Context is pre-gathered deterministically — relevant MCP tools run "over likely-looking links before a minion run even starts"
  - Runs on isolated devboxes pre-warmed in ~10 seconds; local linting "less than five seconds"; "at most two rounds of CI"; test autofixes "automatically applied"
- **Adopt:** deterministic pre-work around the agent loop; bounded CI iterations; pre-warmed isolated environments.
- **Evals:** GATES — lint node before push, capped CI rounds, mandatory human review before merge. No production-monitor evals described.
- **Role separation:** deterministic nodes (lint/push) vs agent nodes; CI + human as judge. No model-mixing detail.

## 2. Stripe — "Minions … Part 2"

- **URL:** https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2 — Alistair Gray, Feb 19, 2026
- **CLASSIFICATION: Practitioner testimony** (the deepest architecture piece in the sweep)
- **Key claims:**
  - "Blueprints combine the determinism of workflows with agents' flexibility in dealing with the unknown"
  - Some blueprint nodes are "fully deterministic: those particular nodes don't invoke an LLM at all"
  - Growth: "Over 1,300 Stripe pull requests…merged each week are completely minion-produced" (up from 1,000 ten days earlier)
  - Defining property: the "absence of a supervisory human" — vs Cursor-style supervised tools
  - Toolshed grew to ~500 tools, but agents get a curated "smaller box" subset to reduce errors
  - Standardized on Cursor's rule format, synced across Claude Code and minions
- **Adopt:** "Putting LLMs into contained boxes" compounds reliability; deterministic linting saves tokens; QA-environment confinement (no prod data).
- **Beware:** unconditional global rule files ("fill with rules before the agent even starts"); unbounded CI loops — "diminishing marginal returns if an LLM is running against indefinitely many rounds"; unattended runs cannot rely on "interruptibility or human-triggered commands."
- **Evals:** GATES — lint → CI round 1 with autofixes → one agent fix attempt → human on second failure. Human merge review always.
- **Role separation:** blueprint = orchestrator state machine; deterministic nodes = validators; CI + humans = judges. Explicitly no separate LLM judge.

## 3. Uber — "Running a Software Factory Efficiently at Uber Scale"

- **URL:** https://www.uber.com/us/en/blog/efficient-software-factory/ — Uday Kiran Medisetty (Distinguished Engineer), Aug 27, 2026
- **CLASSIFICATION: Practitioner testimony** — the richest cost-discipline document found; uses "software factory" verbatim
- **Key claims:**
  - "more than 70% of pull requests are attributed to local or cloud agents"
  - Feb–Aug 2026: "weekly active users across all agentic offerings grew 7x, and weekly agentic requests grew 9.4x"; "over 3,600 agent skills," "more than 30K agent skill executions per day"
  - "total AI spend has relatively stabilized since April due to optimizations"; "cost per 1,000 model requests is down almost 34%"; "cost per session is down 52% from its June peak"
  - AI Context Graph ("24 million nodes and 80 million edges"): grounded query in "38 seconds" vs "20 minutes" ungrounded and wrong
  - Managed agents handle "code review, self-healing CI failures, completing E2E PRs with visual validation, triaging on-call alerts, debugging incoming bugs"
  - Cost equation: users × sessions/user × turns/session × requests/turn × tokens/request × price/token
- **Adopt:** code-mode batching (>50% token cut); 1-hour prompt-cache TTL; live cost counters in status lines; dashboard cataloguing 16 spend anti-patterns; benchmark-driven Pareto model routing.
- **Beware:** MCP schema bloat ("50K-70K tokens of schema overhead" loaded upfront; one SaaS suite = "~22K tokens of schema" for 49 tools); measurement confounded because "behavior shifts with every upgrade and model family."
- **Evals: BOTH, explicitly.** Gates: uReview benchmark "built…from real pull requests with known bugs," scored on "precision, recall, and F1…plus cost per review, latency, timeouts, and noise." Monitors: production "revert rate, F1, MTTR" plus "outcome-denominated cost (cost per merged PR, cost per review)."
- **Role separation / model mixing:** primary models decompose; subagents route to "weaker, more cost-effective model[s]"; managed agents (uReview) act as specialized validators; "manager sign-off for tier upgrades" as human cost circuit-breaker. The strongest model-mixing evidence in the sweep.

## 4. Ramp (via Pragmatic Engineer) — "Why Ramp built its own in-house coding agent, Inspect"

- **URL:** https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect — Gergely Orosz w/ Jessica Salmon, Ivan Klaric, Aug 25, 2026; interviews Ramp CTO Rahul Sengottuvelu, Head of Eng Hamid Dadkhah, Principal Eng Zach Bruggeman
- **CLASSIFICATION: Practitioner testimony** (third-party publication, but first-person interviewed operators with specifics)
- **Key claims:**
  - Driver: "Local machines are limited in how many agents they can run"
  - "75%" of merged PRs authored by Inspect (May 2026); "~90%" of Inspect-repo PRs by Inspect itself; 1M+ total sessions by July 2026
  - Stack: OpenCode harness, Cloudflare Durable Objects, Modal sandboxes; env spin-up "under 5 seconds"
  - Agents get "the same tools and context that a Ramp engineer has"
  - "All Inspect sessions are public and open to collaboration"; 200+ internal agents built on the platform
  - Inspect "visually verifies its own work by providing screenshots and live previews" and "close[s] the loop" before deployment
- **Adopt:** remote sandboxes for concurrency; v1 Chrome-extension approach was abandoned for v2 remote dev environments (the pivot drove adoption).
- **Evals:** closed-loop self-verification (tests, telemetry, screenshots) — gate-shaped but informal; no benchmark/eval framework disclosed. Model choice and cost not disclosed.

## 5. Ramp/Modal — "How Ramp built a full context background coding agent on Modal"

- **URL:** https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal — Modal blog (Greta Workman, Modal PMM; Ramp engineers quoted), Feb 19, 2026
- **CLASSIFICATION: Vendor-guidance/marketing** (Modal case study of its customer) — corroboration for #4, not primary testimony
- **Key claims:**
  - "Each Inspect session runs in a Modal Sandbox containing a full-stack development environment: Postgres, Redis, Temporal, RabbitMQ"
  - "Functions run on a cron job every 30 minutes to clone repositories, install dependencies, and build fresh filesystem snapshots"
  - "over half of all merged pull requests at Ramp" from Inspect (earlier snapshot than #4's 75%); "over 80% of Inspect itself now being written by Inspect"
  - Wired into Sentry/Datadog; before/after screenshots via Chromium
- **Beware:** no failure discussion at all — classic case-study asymmetry. Evals unstated; cost unstated.

## 6. Shopify — "Under the River"

- **URL:** https://shopify.engineering/under-the-river — Javier Moreno, Burke Libbey, and "River" (the agent credited as coauthor), May 28, 2026
- **CLASSIFICATION: Practitioner testimony**
- **Key claims:**
  - River is "an AI agent that lives in our company Slack," public channels only; Aquifer is the substrate ("session, harness, sandbox, gateway, the durable event log")
  - "one in eight merged pull requests across Shopify is coauthored by" River; 59,918 sessions / 5,170 channels / 3,536 merged PRs in 30 days
  - Session: "Durable identity. Append-only event log. Postgres-backed"; Harness: "The agent loop. Reads history, calls the model, emits tool intents. Cheap to recreate"; Sandbox: "Where the code runs… Disposable"
  - Blast-radius principle: "the agent loop is not in the same blast radius as `rm -rf`"
  - Multiplayer/public design: "One person's hard-won fix becomes the next person's starting point"
- **Adopt:** separating durable session from cheap harness from disposable sandbox; public-by-default sessions as compounding organizational memory.
- **Beware:** agent-scale load broke infra — "real breaks. CI had to scale by an order of magnitude, almost overnight"; merge queues and build caches became load-bearing.
- **Evals:** mostly SOCIAL gates — humans in Slack threads ("a second human…drops in with a constraint or a redirect") plus CI; no formal eval framework stated. Cost/model mixing not detailed (median 50 tool calls per 19-minute session is the only usage stat).

## 7. exe.dev — "Six Months of Writing Code Exclusively With Agents"

- **URL:** https://blog.exe.dev/engineering-with-ai — Maisem Ali, Aug 27, 2026
- **CLASSIFICATION: Practitioner testimony** (individual operator at an agent-sandbox company; n=1 but unusually honest)
- **Key claims:**
  - "In February of this year, I made a rule for myself: I wasn't going to write code by hand anymore."
  - Parallel agents became chaotic until he built `botd` — "one place to manage the work" across dozens of isolated VMs
  - Agents ran "YOLO mode" inside disposable VMs, but Git/Stripe/API credentials sat behind proxies agents never see
  - Verification layers: unit tests, agent-on-agent code review, CI/CD, screenshot-based manual testing, then human judgment
  - Models: GPT-5.3 and Opus 4.6 handle "larger changes with much less steering"
- **Beware (the money quote of the sweep):** "The tools could tell me that the change worked. They couldn't tell me whether it was worth adding to the system." — verification ≠ product judgment.
- **Evals:** GATES (tests, agent review, CI) with human as final judge; no production monitors. Credential-proxy pattern is the notable security/role-separation contribution.

## 8. Cloudflare — "Code Mode: the better way to use MCP"

- **URL:** https://blog.cloudflare.com/code-mode/ — Kenton Varda & Sunil Pai, Sep 26, 2025 (modified Jul 2026)
- **CLASSIFICATION: Vendor-guidance** (promotes Workers/Agents SDK) — technically substantive and independently corroborated by Uber's code-mode token savings (#3)
- **Key claims:**
  - "LLMs have an enormous amount of real-world TypeScript in their training set, but only a small set of contrived examples of tool calls"
  - "Isolates can start in a handful of milliseconds using only a few megabytes of memory"
  - Bindings give sandboxed code MCP access without general network access, so API keys can't leak
  - Companion post claims 99.9% input-token reduction for the full Cloudflare API vs raw MCP (1.17M tokens)
- **Evals:** unstated. **Cost:** token-economics argument only; Worker Loader pricing "not yet finalized."

## 9. Factory.ai — "Factory 2.0: From coding agents to software factories"

- **URL:** https://factory.ai/news/software-factory — Matan Grinberg & Eno Reyes, Jun 15, 2026
- **CLASSIFICATION: Vendor marketing** (useful mainly as the term-of-art source for "software factory")
- **Key claims:**
  - Factory loop: signals in → "built, tested, reviewed, secured, shipped, and monitored"
  - "Router to automatically (or rule-based) select the best model for any given task"; "No one model fits every need"
  - "Missions solve complex tasks over hours or days by decomposing work into parallel tracks"
  - Customer logos (NVIDIA, EY, Adobe, Adyen…) but **no quantified metrics anywhere** — the tell vs the practitioner pieces above
- **One honest caveat:** "Not every process should use long-horizon autonomous tasks."

---

## Negative findings / gaps

- **Vercel:** nothing first-person found on running internal agent fleets (published material is v0/AI SDK product content). Explicit gap.
- **Figma:** no first-person engineering post found; Figma appears only as a surface Uber drives via Figma Console MCP.
- **Databricks:** only Agent Bricks product announcements — vendor, not fleet-operations testimony.
- **Airbnb:** a third-party Medium recap claims 64% of PRs involve agentic sessions and 12+ internal MCP servers "by Nov 2026" (date internally inconsistent — treat as unverified lead, not evidence). No first-party Airbnb post found.
- **exe.dev follow-ups not read:** "How Antithesis Turned exe into a Sandbox for Agentic Software Tests," "OAuth for Agents" (blog.exe.dev).

## Cross-cutting synthesis (research agent)

1. **Convergent architecture:** every production fleet (Stripe, Ramp, Shopify, Uber) independently arrived at: remote disposable sandboxes + durable session state + deterministic scaffolding around the agent loop + curated tool subsets. Nobody runs bare agents on laptops at scale.
2. **Evals sit at gates almost everywhere; only Uber runs both gates and production monitors** (revert rate, MTTR, cost-per-merged-PR). Uber is the only org publishing a real eval methodology (real-PR benchmarks, F1 + cost + noise).
3. **Human review survives everywhere.** Stripe's tagline — human-reviewed, zero human-written code — is the common end state; Shopify substitutes public-Slack social review for some of it.
4. **Model mixing is real but thinly documented:** Uber (weak models for subagents, Pareto routing) and Factory (router) discuss it; Stripe/Ramp/Shopify don't disclose.
5. **The recurring warnings:** unbounded CI/fix loops (Stripe), MCP schema token bloat (Uber, corroborating Cloudflare's pitch), infra breaking under agent-scale load (Shopify), and verification proving "it works" but never "it's worth shipping" (exe.dev).
