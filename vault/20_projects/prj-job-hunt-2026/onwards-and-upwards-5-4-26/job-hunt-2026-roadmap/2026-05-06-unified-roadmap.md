---
type: roadmap
project: prj-job-hunt-2026
status: draft
created: 2026-05-06
last_updated: 2026-05-17
synthesis_sources: [karpathy-sequoia, nate-credentials-opus, nate-credentials-gpt, nate-comprehension-opus, nate-comprehension-gpt, council-nate-jones-digest-2026-05-16]
amendments:
  - 2026-05-10: Added Task 8 (Eval Suite ship Week 2) + Task 9 (Substack-Drafter agent post-employment). Upgraded Task 6 §I from fluency-only to planned ship. Added Kerouac voice variant test to Decision 4. Updated portfolio count from 5+2 to 6+2+1. See [`2026-05-10-eval-suite-build-plan.md`](2026-05-10-eval-suite-build-plan.md).
  - 2026-05-12: **Track-C v0 SHIPPED 13 days early.** npm publish + MCP registry publish both live. `@swins/intent-engineering-mcp@0.1.0` on registry.npmjs.org; `com.seanwinslow/intent-engineering@0.1.0` on registry.modelcontextprotocol.io via DNS-verified domain namespace. Task 3 ship-gate items 1–16 closed; 17–19 (Loom + LinkedIn + Substack) remain. Added "Publish + registry flow — frozen reference" subsection to Task 3 capturing the DNS auth mechanics (Ed25519 keypair + TXT record on apex) so the flow is reproducible for the next MCP server without re-derivation.
  - 2026-05-12 (evening) — Friday Week 1 finisher closed in a Cowork session. Task 1 Steps 1+2+4 + Task 2 Steps 1+2+4 complete. Two discoveries closed steps without new writes — (a) `vault/40_knowledge/templates/EXPLANATION-template.md` confirmed already canonical (Sean wrote it 2026-05-06, more thoughtful than a naive scaffold) and (b) the Superuser Pack README opening was already in Karpathy "agentic engineering practitioner's toolkit" framing on line 3, naming the full stack and citing Karpathy explicitly. Two net-new writes — (c) `agents-sdk/lib/concept_edges/EXPLANATION.md` (Phase D typed reasoning edges 4Q, Claude-Nate-2 §2a verbatim with co-located wikilinks) and (d) `agents-sdk/agents/knowledge_loop/EXPLANATION.md` (Phase 6 producer/consumer 4Q, §2e verbatim with wikilinks). Both EXPLANATION.md files passed the <90-sec recruiter readability check before handoff. Personal-site `/transactions/` Astro route + `validate.py` + git commits across both repos handed to Claude Code via [`2026-05-13-claude-code-handoff-task-1-2.md`](2026-05-13-claude-code-handoff-task-1-2.md) with a stop-and-confirm gate on the personal-site repo (if scaffolding from scratch would exceed 30 minutes, Decision 2's fallback fires — GitHub EXPLANATION.md files become canonical and Substack syndicates from raw URLs). Loom + Substack + LinkedIn syndication deferred until full portfolio locks down per Sean's 2026-05-12 directive ("Get all of my projects locked down and then I can come back after everything is completed, write up the scripts with your help based on the projects completion state, then post the videos").
  - 2026-05-13 — **Task 6 §E (target-30 companies list) CLOSED 5 days early.** Three deliverables landed in one Cowork session — (a) [`vault/20_projects/prj-job-hunt-2026/target-companies.md`](../../target-companies.md) created with 30 rows across 3 tiers, 16 pre-loaded from the 2026-05-07 Gemini DR-Max research (JD URLs + comp ranges + portfolio-to-role mapping all cited from DR §§1-5), 14 rounded out from the job_feed watchlist (frontier labs + Larry's network). Schema per master plan Phase 5 Task 5.1 Step 3 + cross-refs to `[[job_feed]]` and `[[warm-intros]]`. Tiers reorganized vs. DR's tenure-fit tiering — uses master plan's "yes please / would consider / safety net" framing weighted by Boston-metro + remote constraint + portfolio match. (b) [`vault/20_projects/prj-job-hunt-2026/warm-intros.md`](../../warm-intros.md) created — small file by design with Larry pre-populated for Messari (strong) + Coinbase (medium), three reusable outreach patterns (inside-contact ping, warm-intro request, reactivation message), LinkedIn-sweep prompt with all 26 target slugs paste-ready. (c) [`vault/20_projects/prj-job-hunt-2026/job-feed/watchlist.yaml`](../../job-feed/watchlist.yaml) patched — added 5 slugs (`decagon` + `robinhood` to `ai_native`; `liberate` + `manifoldbio` + `pairteam` to `boston_metro`). 36 → 38 slugs total, 6 buckets. BCG X intentionally excluded with inline comment (custom careers system, not Greenhouse/Lever/Ashby — manually tracked in target-companies.md instead). `python3 scripts/validate.py` → 58 warnings / 0 errors (2 cleaner than the v3.30.1 baseline). Phase 5 Task 5.2 (5/week application cadence starting Week 3, 2026-05-19) is now unblocked.
  - 2026-05-16 — **Council Input section added** (Nate Jones Digest, premium-profile LLM council run, $0.6178 cost / 3:25 wall, Borda winner Opus 4.7 with unanimous A-first cross-rank). Five new gap-fills slotted as Tasks 12–15 + Task 1 Step 3 amendment: Judge Layer retrofit on Substack-Drafter (Task 12), Access-vs-Meaning manifesto post (Task 13), `/transactions/` ledger deployment + LinkedIn refresh (un-defers personal-site, AMENDS Task 1 Step 3), Authority/Recovery/Audit reframe (Task 14), Vault 5-Test Scorecard (Task 15). Three deprioritizations added to Task 7 STOP-DOING (most load-bearing: skip framing the 100-line HybridRouter as "Agent OS" / "runtime architecture" — Gemini Pro's credibility-risk insight). Council's core finding: stack is 80% built and 20% legible; gaps are framing surfaces + one piece of missing control architecture (the judge layer). Sequencing drops cleanly into the existing 5/17–6/13 calendar without breaking Tier-A truths. Raw transcript: [`2026-05-16-council-nate-jones-digest.md`](2026-05-16-council-nate-jones-digest.md).
  - 2026-05-16 (later) — **Council Gap-Fill 3 expanded into Task 1 Step 3.** Un-defers personal-site deployment (target Mon 2026-05-19). Architecture confirmed via visual mockup: home-page V3 card gallery unchanged + intent-engineering MCP added as 6th card; `/transactions/` becomes flat reverse-chronological table over 5 existing EXPLANATION.md files; `/transactions/{slug}/` deep-dives keep V3 card hero. Host: Vercel (consistency with agent-fleet-observability); DNS: Cloudflare orange-cloud OFF for Vercel records. [`2026-05-13-personal-site-deployment-deferred.md`](2026-05-13-personal-site-deployment-deferred.md) flipped to `status: superseded-by-gap-fill-3`. Gap-Fill 3 of 5 expanded; Gap-Fills 1, 2, 4, 5 still pending.
  - 2026-05-17 — **Council Gap-Fill 1 expanded into Task 12 (Judge Layer Retrofit on Substack-Drafter).** 9-day build target 2026-06-04; hard precondition is Task 8 Workstream B7 gate closure (5 consecutive nights of `concepts_written > 0`). Four architecture decisions locked 2026-05-16: (A) wrap substack-drafter ONLY in v0 — Daily Driver / Job Feed / vault-synthesizer / future "vault-to-build" agent are explicit expansion candidates tracked in compounding-payoff section, not v0 scope; (B) full Pydantic `ActionProposal` schema in the MVP (8 fields, `evidence_used` + `rollback_path` optional), not deferred to v0.2 — the schema *is* the portfolio artifact; (C) fail-open with Pushover alert + `JUDGE_UNAVAILABLE` ledger entry on judge-model unavailability — defense-in-depth pattern, Sean's manual publish gate stays Tier-A canonical; (D) ledger location is `vault/health/judge_log/` (matches existing telemetry pattern, NOT council's literal `vault/agents/judge_log/`); (E) `--demo-injection` CLI flag for reproducible Loom takes. Becomes the 9th flagship portfolio artifact + the policy engine cited by Gap-Fill 4 + the telemetry stream feeding Task 11 dashboard. Gap-Fill 1 of 5 expanded; Gap-Fills 2, 4, 5 still pending.
  - 2026-05-17 (final, all 5 gap-fills expanded) — **Council Gap-Fill 2 expanded into Task 13 (Access-vs-Meaning Manifesto + Spectrum Map).** 3–5 day pure-framing build, **zero new code**. Two-gate ship structure: draft-lock 2026-05-23 (Fri Week 1) + publish ~2026-06-19 (Fri Week 5 Substack Post 3 slot, behind Posts 1 + 2). Three companion artifacts: `docs/MEANING_OVER_ACCESS.md` (~1,500 words, 5 sections) + `docs/diagrams/access-meaning-spectrum.mmd` (Mermaid quadrantChart, not hand-SVG) + Substack cross-post pre-formatted. New `/essays/` IA on sw-portfolio (sibling to `/transactions/` + `/architecture/` + `/work/`); first thesis-shaped writing route with room for future essays. Voice: thesis-forward with personal-voice opener + close, sober/declarative middle (NOT pure Sedaris-mode — manifesto genre doesn't suit comedy). Becomes the URL in the email signature + the pre-read link in every recruiter contact; gives Task 10 its launch narrative for free; retroactively upgrades the intent-engineering MCP ship from "a tool" to "the first instance of a thesis." **All 5 Council gap-fills now expanded into tasks** (Task 1 Step 3 amendment + Tasks 12, 13, 14, 15). Final order in the roadmap: Task 12 (Judge Layer) → 13 (Manifesto) → 14 (Control Architecture) → 15 (Vault Scorecard) → 7 (STOP-DOING). `last_updated: 2026-05-17`.
  - 2026-05-17 (later, after Task 14) — **Council Gap-Fill 5 expanded into Task 15 (Vault as Agent Infrastructure 5-Test Scorecard).** 2–3 day build target 2026-06-03 (Week 3 council slot 5/31–6/6). Three companion artifacts: `vault/SCORECARD.md` (canonical short scoreboard, ~600 words) + `docs/VAULT_AS_AGENT_INFRASTRUCTURE.md` (long-form essay ~2,000 words) + `seanwinslow.com/architecture/vault-scorecard/` (public mirror Astro page, with new `/architecture/` IA). Plus `scripts/generate_schema.py` (concept_edges SQLite → Mermaid `erDiagram`) + fully-synthetic `examples/public_vault_fixture/` (10 notes / 15 edges / espresso-brewing topic for zero private-vault leakage risk). Preserves GPT-5.5's honesty contribution: Linear scores ABOVE the vault on Ownership + Permissions (the two failures are exactly why Task 10 + Task 12 are next). Foundation doc for Task 10 (`vault-knowledge-mcp`) — makes the MCP self-justifying. Becomes the spine for any "agent-operable knowledge" interview answer. Gap-Fill 5 of 5 expanded; Gap-Fill 2 (manifesto post) still pending.
  - 2026-05-17 (later) — **Council Gap-Fill 4 expanded into Task 14 (Authority / Recovery / Audit Reframe).** 3-day build target 2026-06-10 (Week 4 slot, alongside animation pipeline ship 6/11 + Task 11 dashboard kickoff). Pure documentation reframe of existing infrastructure — cost caps in [`config.toml`](../../../../agents-sdk/config.toml), keychain-gated keys in [`lib/keychain.py`](../../../../agents-sdk/lib/keychain.py), Pushover in [`lib/pushover.py`](../../../../agents-sdk/lib/pushover.py), JSONL ledgers across `vault/health/` — named as the Authority / Recovery / Audit trinity Nate's §3.7 calls for. New artifact set: `agents-sdk/docs/CONTROL_ARCHITECTURE.md` (~1,500 words, 3 sections + Mermaid diagram) + `tools/governance-demo/replay_budget_breach.py` (3 fixtures: allowed / over_budget / missing_auth) + `tools/governance-demo/outputs/sample_ledger.jsonl` + `agents-sdk/config/authority.example.yaml` + 4Q EXPLANATION.md + 90-sec Loom forced-breach demo + LinkedIn post tagging Anthropic FDE Boston JD. HybridRouter constrained to exactly one paragraph inside Authority section per Council Deprioritization 1 (Gemini Pro's credibility-risk insight). Closes §3.1 cost-economics zero-coverage gap + replaces Task 6 §J (enterprise-build patterns) as the FDE-shaped artifact. Pairs with Task 12 (judge = engine, this = policy content). Gap-Fill 4 of 5 expanded; Gap-Fills 2, 5 still pending.
  - 2026-05-17 (evening) — **Task 11 v1 CODE COMPLETE.** Agent Fleet Observability Dashboard shipped end-to-end in one Cowork session via the `superpowers:subagent-driven-development` skill. Live at `~/Code-Brain/agent-fleet-observability/` + `github.com/seanwinslow28/agent-fleet-observability` (public). 26 commits across 33 plan tasks (32 from plan + 1 NEW Task 8b for §4d live-wire). 55/55 pytest tests pass; ruff clean. Build wall-time **85ms** end-to-end on Mac Mini (budget: <60s). Page weight **public 32KB / private 41KB** (budget: <200KB). **Three locked decisions honored:** (1) inline SVG for every chart, Chart.js dropped entirely; (2) single `lib/render.py` with `render_public()` + `render_private()` rather than the design doc's two separate files; (3) description + footer use "multi-agent fleet" not "8-agent" (count grows over time). **§4d live-wire (Sean's 2026-05-16 decision, option 1 of 3):** added Task 8b — `read_target_companies` + `read_warm_intros` parsing [`vault/20_projects/prj-job-hunt-2026/target-companies.md`](../../target-companies.md) and [`vault/20_projects/prj-job-hunt-2026/warm-intros.md`](../../warm-intros.md) pipe tables; private below-fold panels render Tier-1/2/3 counts + by-status breakdown + Tier-1 company list + warm-intro active table LIVE instead of empty-state; `anonymize.public_pass` zeros both for public render (privacy boundary verified — 0 leaks of `Larry`/`Anthropic`/`Messari`/`vault/.job-feed` in public output). **Source-of-truth files:** plan [`2026-05-15-agent-fleet-dashboard-plan.md`](2026-05-15-agent-fleet-dashboard-plan.md) (4424 lines), design [`2026-05-15-agent-fleet-dashboard-design.md`](2026-05-15-agent-fleet-dashboard-design.md), kanban v2 deferral memory at [`vault/90_system/auto-memory/project_agent_fleet_dashboard_kanban_v2.md`](../../../../90_system/auto-memory/project_agent_fleet_dashboard_kanban_v2.md). **What's left (Sean-owned, ≈30 min):** (a) `npm i -g vercel && vercel login && vercel link && vercel deploy --prod`; (b) Cloudflare DNS CNAME `fleet` → `cname.vercel-dns.com`, **DNS-only / gray cloud OFF** (orange cloud breaks Vercel SSL); (c) `cp ~/Code-Brain/agent-fleet-observability/schedules/com.sean.agent-fleet-dashboard.plist ~/Library/LaunchAgents/ && launchctl load …`; (d) first real snapshot commit (`git add index.html kanban.html data.json && git commit -m "snapshot $(date -u +%Y-%m-%dT%H:%M:%SZ)" && git push` after Vercel deploys cleanly); (e) iPhone-shaped screenshot for Substack post 2; (f) 60-sec Loom walkthrough. Validation gate (design §9, 15 criteria): 9/15 verified locally (page-weight, all-tiles-real, regression-visible, privacy-boundary, mascot-present, build<60s, kanban-≥1-ticket-per-source, reduced-motion, full pytest); remaining 6 gate on Sean's hands-on tasks above (cold-cache TTFB, mobile screenshot, recruiter cold-open, README readability, Loom, recruiter attribution). Becomes the 3rd supporting artifact + visual hero for Substack Post 2 ("Vault said something again", target Fri 2026-05-29 if B7 gate closes by then).
  - 2026-05-13 (later) — **Task 10 + Task 11 SPECS added (research-pending).** Two new portfolio artifacts scoped via detailed build specs + deep-research prompt scaffolds, no code written yet. **Task 10:** [`2026-05-13-vault-knowledge-mcp-spec.md`](2026-05-13-vault-knowledge-mcp-spec.md) specs the second MCP server — three tools (`search_concepts`, `find_contradictions`, `get_article`) exposing the Phase D `concept_edges` SQLite table + Phase 6 knowledge_loop articles as queryable MCP surface. Reuses the existing DNS-verified `com.seanwinslow/*` namespace + Ed25519 publish key. 5–7 day build target. Designed as the 8th flagship artifact + the proof of MCP-pattern repeatability over `intent-engineering`. **Task 11:** [`2026-05-13-agent-fleet-dashboard-spec.md`](2026-05-13-agent-fleet-dashboard-spec.md) specs the Agent Fleet Observability Dashboard — single HTML file visualizing the 8-agent fleet's telemetry (cost trends, model mix, synthesizer pass counts, eval suite status, recent runs) with an explicit annotation on the 2026-05-01 → 2026-05-10 silent regression. 2–3 day build target post-research. Designed as the 3rd supporting artifact + the visual hero of Substack post 2 ("Vault said something again") + operational evidence for the Agent Ops / FDP backup track. Both specs include 10-question deep-research prompts (paste-ready for Gemini DR-Max) covering architecture, reference-implementation surveys, distribution surfaces, recruiter-resonance patterns, and an "outsized-impact recommendation" closer. **Status flips to `research-complete` only after DR results land at `vault/20_projects/research/2026-05-XX-vault-knowledge-mcp-research.md` and `2026-05-XX-agent-fleet-dashboard-research.md`.** Updated portfolio count target: **8 flagship + 3 supporting + 1 post-employment** (was 7+2+1 after 2026-05-12 Workstream C ship).
ai-context: "Unified roadmap synthesizing Karpathy + Nate × 2 articles × 2 models, mapped onto the existing Phase 0–8 master plan. Portfolio project ideas + concrete implementation plans through 2026-07-04. Amended 2026-05-10 with eval-suite + Substack-drafter additions after Step-0 error-analysis surfaced a 9-day silent regression that reshaped the eval scope."
---

# Unified Roadmap — Karpathy × Nate × 2 × 2

> Synthesis of five reference docs in [reference-synthesis-docs/](reference-synthesis-docs/), mapped onto the [master plan's](../2026-05-04-onwards-and-upwards-plan.md) Phase 0–8 structure. Treats the [operating-model](../../../05_atlas/operating-models/job-hunt-2026/operating-model.md) Tier-A truths as inviolate.

---

# PART 1 — SYNTHESIS

## 1. Consensus — Load-Bearing Signal Across All Sources

Six claims that survive triangulation across Karpathy + both Nate articles + both model interpretations.

**Claim A — Artifacts > credentials, full stop. (HIGH)**
All five sources converge. Karpathy reframes the hiring test as "build a real project with agents, deploy it secure, then survive adversarial agents." Claude-Nate-1 says credentials are noise; ChatGPT-Nate-1 corroborates with the ManpowerGroup 39,063-employer survey showing AI skills are the hardest-to-find globally. Both Nate-2 versions argue the proxy chain broke when AI made production cheap. Confidence is HIGH because corroborating market data (vibe-coding interviews now standard at Google/Netflix/Stripe/Adobe per news.aakashg.com) ratifies it.

**Claim B — MCP servers are the portable career artifact for 2026. (HIGH)**
Karpathy's single top recommendation is verbatim: "stop building skills and start building MCP servers." The Anthropic Forward Deployed Engineer listing (Boston/NYC/Chicago) explicitly names "MCP servers, sub-agents, and agent skills" as deliverables. Both Nate-2 docs land on a vault-aware MCP server as the centerpiece artifact. The 9,400+ public MCP server registry and 78% enterprise adoption (Q1 2026) make this a present-tense market reality, not a forecast. Confidence: HIGH. Track-C's 2026-05-25 ship date is correctly sized.

**Claim C — Specs and comprehension are the durable PM skill in the agent era. (HIGH)**
Karpathy: "the durable skills are taste, judgment, eval design, security, agent orchestration." Nate-1 ranks Specification Precision as skill #1. Nate-2's entire thesis is comprehension-as-currency: "the explanation artifact in the generative era is essentially what the commit message was in the traditional software engineering era." All five sources agree that what becomes valuable when execution is cheap is judgment about what to execute. Confidence: HIGH.

**Claim D — Eval design is the underbuilt next-frontier portfolio piece. (HIGH)**
Karpathy notes the $20B 2026 funding flowing into eval/agent-ops platforms. Claude-Nate-1 cites Brendan Foody's "evals are the new PRDs" framing and the Hamel Husain / Shreya Shankar 3,000-student course. ChatGPT-Nate-1 verifies with Anthropic's "two domain experts independently reach the same pass/fail verdict" North Star. Both Nate-2 docs explicitly name eval suites as the next layer beyond the 4-question artifact. Confidence: HIGH.

**Claim E — Sean's biggest leverage is publishing what he already has, not learning more. (HIGH)**
Karpathy maps Sean's existing projects (Superuser Pack, financial-research fleet, animation pipeline) as already proof-of-thesis. Claude-Nate-1: "the leverage point is publishing what he's already built, not learning more." ChatGPT-Nate-1: "don't try to become an 'AI architect' in 8 weeks; turn your existing PM, context, and Claude Code strengths into 3–4 hard-to-fake artifacts." Both Nate-2 docs pre-draft 4Q artifacts for projects that already exist. Confidence: HIGH. This is the single most actionable consensus claim.

**Claim F — Cost / token economics is Sean's only real skill gap. (MEDIUM-HIGH)**
Both Nate-1 docs explicitly name cost economics as Sean's one beginner skill on the seven-skills map. Karpathy doesn't address it directly but the eval/RL economy he describes implies fluency. The fix is small: a token-cost calculator artifact that doubles as a published portfolio piece, ~2 days of work. MEDIUM-HIGH because Karpathy isn't loud about it; otherwise the convergence is clean.

**Claim G — Live demonstration (Loom + vibe-coding rep) is non-fakeable in a way written artifacts aren't. (MEDIUM-HIGH)**
Karpathy: hand candidates "a substantial brief, give them agents and a deploy target, give them a deadline, then have adversarial agents probe for breakage." Claude-Nate-1 calls "Record yourself working with an AI system and narrate your decisions in real time" the single highest-leverage tactic in the piece — explicitly buried but most important. Claude-Nate-2 cites Aakash Gupta's research showing 45-min Bolt/v0/Cursor live builds are now the norm at Sierra and others. ChatGPT-Nate-2 corroborates via the Sierra "AI-native onsite" public spec. Confidence: MEDIUM-HIGH.

---

## 2. Cross-Model Diff — Where Opus 4.7 and GPT-5.5 DR Saw Different Things

### 2a. Article 1 (Nate's 7 Skills)

**Convergence:** Sean is 3 strong + 3 working + 1 beginner. AI PM is the primary track. Cost economics is the gap. The K-shaped market split is real but "infinite jobs" is hyperbole. CCA-F is too new to be a hiring filter today. Boston is "deep but lumpy" — plenty of postings, geography matters.

**Divergence:**

1. **Backup track.** Claude-Nate-1 → AI-Augmented Domain Specialist (Crypto/Fintech via Larry Cermak as reference). ChatGPT-Nate-1 → Agent Ops / Forward Deployed Product / Support Ops AI. **Verdict: GPT's read is more useful for Sean's situation** — Anthropic's own FDE Boston/NYC/Chicago listing literally requests MCP/sub-agent/skill deliverables, which is exactly Sean's stack. Domain Specialist is a deeper fallback inside this category if FDP doesn't land.

2. **Application volume.** Claude-Nate-1 → 15 quality apps/week, scaling to 25/wk if response rate <5% by Week 3. ChatGPT-Nate-1 → 10–12 steady, 15 in the second-wave week. **Verdict: lean on the master plan** — Phase 5 Task 5.2 says 5 quality applications per week. Both Nate-1 numbers are aspirational; the master plan's 5/wk floor with quality customization is more sustainable inside the 8:30–5:30 container without breaking the 1–2 PM mandatory break.

3. **CCA-F certification spend.** Claude-Nate-1 → "$99 is better spent on Loom Pro and Substack Pro." Explicit anti-cert through June 15. ChatGPT-Nate-1 → "optional upside, not central." **Verdict: Claude's read.** Tier-A walk-away math + the master plan's $100-by-June-11 spend cap make a $99 cert the wrong purchase right now.

4. **Eval-stack vocabulary.** Claude-Nate-1 leans Hamel/Shreya canon ("evals are the new PRDs"). ChatGPT-Nate-1 leans on Google ADK / Cohere / Anthropic system-cards / Model Spec Evals. **Verdict: both.** Hamel's frame for the publishing tone; the institutional model-card / system-card / ADR vocabulary for the actual artifact structure.

### 2b. Article 2 (Comprehension)

**Convergence:** TalentBoard is creator monetization, not durable infrastructure — don't host the canonical version there. Personal site + GitHub `EXPLANATION.md` is the right home. Evals are the next-frontier explanation artifact. The 4-question template (`What is this? / Why this approach? / What would break? / What did I learn?`) is the practice worth adopting regardless of where it lives.

**Divergence:**

1. **Pre-drafted 4Q artifacts.** Claude-Nate-2 §2 wrote five with high specificity wired to actual files (Phase D typed reasoning edges, Block ETF skill, financial-research fleet, animation pipeline, Phase 6 knowledge loop). ChatGPT-Nate-2 §2 wrote five with looser/structural framing (Superuser Pack v3.20.0 as a whole, Block PM templates, agentic fleet, animation pipeline, Phase 6 loop). **Verdict: Claude's drafts are higher-leverage** because they hook to specific code/files Sean can immediately commit; GPT's are scaffolds for the broader practice. Use Claude's verbatim where they land; use GPT's framing for any artifact Claude didn't pre-draft.

2. **Income-stream sequencing.** Claude-Nate-2 → `comprehension-mcp` as a paid product first ($10–15/seat/mo). ChatGPT-Nate-2 → "service first, kit second, tool third" with a Comprehension Review service at $150–$300 starter rate. **Verdict: GPT's sequencing fits Sean's cushion north-star better.** Service generates cash fastest with lowest infra; the cushion goal is "every win counts," not "build a $5k/mo SaaS in 8 weeks." Defer the MCP productization until repeated demand surfaces.

3. **Vibe-coding rep emphasis.** Claude-Nate-2 is loud about it (cites the Aakash Gupta research, recommends two 45-min Bolt/v0/Cursor reps per week starting Week 3). ChatGPT-Nate-2 mentions Sierra's "AI-native onsite" once but doesn't push reps as hard. **Verdict: Claude's read is correct.** Aakash's coached candidate failing on "What was the F1 score?" → "I'd have to check" → interview over is the kind of failure mode that 12 reps cheaply prevent.

4. **Substack voice.** Claude-Nate-2 → comedic register, per Sean's SOUL ("Storytelling skews comedic"). ChatGPT-Nate-2 → no specific tone push; suggests Hashnode mirroring at week 4 if Substack subs <25. **Verdict: Claude's read.** Operating-model already locked story-driven Sean Mode (Sedaris-tuned, [`writing-voice-modes`](../../../../.claude/skills/writing-voice-modes/SKILL.md)) as the tone baseline. Don't compete with Nate's sober register.

---

## 3. Divergence — The Real Decision Points

Five forks where the sources genuinely disagree. Each gets a default and a switch condition.

**Fork 1 — Skills vs. MCP servers vs. explanation artifacts as primary investment.**
Karpathy says "stop building skills, start MCP servers." Both Nate-2 docs say "every artifact needs an explanation." Both Nate-1 docs say "publish what you already have."
- **Default:** Ship one MCP server (`intent-engineering`) by 2026-05-25, then attach short (~400-word) `EXPLANATION.md` files to existing Superuser Pack artifacts in parallel. This absorbs all three positions because the MCP server *is* a publication of an existing artifact, with the explanation attached to it.
- **Switch only if:** A hot interview lead in Week 2–3 explicitly asks for a different MCP demo shape. Then re-scope `intent-engineering` v0 to that shape, but do not abandon Track-C.

**Fork 2 — Backup track: Agent Ops/FDP (GPT) vs. Domain Specialist (Claude).**
- **Default:** Agent Ops / Forward Deployed Product as backup. Anthropic's own FDE Boston listing is the proof. Apply to Anthropic FDE in Week 2 as the wildcard application.
- **Switch only if:** Weeks 3–4 show clear Domain Specialist pull from Larry's network (≥2 warm intros into crypto/fintech AI roles where Block context is the differentiator).

**Fork 3 — Comprehension-as-product vs. comprehension-as-practice.**
Claude-Nate-2 says build `comprehension-mcp` as a paid linter. ChatGPT-Nate-2 says practice the 4Q template for self even if it's never published.
- **Default:** Practice first. Ship 4Q `EXPLANATION.md` files for the existing artifacts (Phase D, Phase 6 knowledge loop, animation pipeline, financial-research fleet) through June 11. Productize only if patterns repeat.
- **Switch only if:** Three or more inbound asks for paid comprehension review service emerge organically through the Substack or LinkedIn channel.

**Fork 4 — Service-first vs. product-first cushion.**
GPT's service-first ladder (Comprehension Review → Explanation Artifact Kit → tooling) vs. Claude's MCP-product first.
- **Default:** Service-first, post-employment. Pre-employment (now through ~July 4): cushion is secondary. Focus on artifacts that double as job-search signal AND demo-able service offerings later.
- **Switch only if:** An MCP server hits 100+ GitHub stars in 14 days and inbound asks for a paid hosted version emerge.

**Fork 5 — Substack voice: comedic (Claude-Nate-2) vs. strategic-sober (no source pushes this; default genre).**
- **Default:** Comedic register — operating-model + SOUL already locked story-driven Sean Mode (Sedaris-tuned).
- **Switch only if:** After 3 posts, engagement is <10% of comparable strategic-PM Substacks AND no inbound recruiter signal in 21 days.

---

## 4. Gaps — What None of the Sources Cover That Sean's Situation Requires

Honest list of what the source set is silent on.

1. **Severance + UI claim sequencing.** Severance was signed 2026-05-05 (Phase 1.1 ✅). UI claim still unfiled (target 2026-05-05 — slipped). COBRA SEP deadline is 2026-07-03. None of the synthesis docs handle this — they assume runway is solved. The master plan handles it; this roadmap inherits the master plan's Phase 1 schedule unchanged.

2. **Boston-metro AI PM market specifics.** Both Nate-1 docs gesture at "60–80 active postings" or "deep but lumpy" but don't enumerate companies. The operating-model surfaces "target list of 30 companies" as an explicit bottleneck. None of the sources fill it. Resolution: this roadmap commits a specific Week-2 deliverable to enumerate it — see Task 6 in Part 2.

3. **Beginner-to-intermediate coder reality vs. production-grade MCP server expectations.** Karpathy and both Nate articles assume MCP servers ship cleanly. Sean self-codes as beginner-to-intermediate. Mitigation: the `intent-engineering` v0 scope must be small (3 tools, stdio transport, Claude Desktop demo). Lean on the TS SDK boilerplate. Don't try to over-engineer. Both Sean and the master plan already understand this; surfacing it explicitly so it doesn't drift.

4. **Hot-lead × Track-C collision in Week 3–4.** Tier-A truth says Track-C is protected even in offer weeks. None of the sources address what happens when a final-round interview lands the same week the MCP demo is supposed to ship. Resolution: protect Track-C, slip applications not the build. Track-C *is* the interview asset.

5. **Block IP scrub before public push.** None of the sources address the CIIA Section 2.3 obligation that three Block-named skills (`the-block-jira-ticket-writer`, `etf-page-creator`, `biweekly-jira-update`) must be sanitized or removed before any public Superuser Pack visibility push. This gates Phase 3 Task 3.3 (public announcement) and Phase 4 Task 4.3 Step 9 (publish MCP server / pin on profile). Resolution: Task 0 in Part 2 makes this an explicit Week-1 gate.

6. **Agent-fleet audit verdict.** Operating-model surfaces it as bottleneck ("what stays, what moves to Mac Mini, what gets retired?"). Sources don't engage. The MBP-intermittent Qwen3-14B synthesizer is burning Phase 6 efficiency on dry days. Resolution: a one-evening audit pass in Week 2 — see Task 6 §B.

7. **Mary as critical-path collaborator.** Operating-model names Mary, Matt, and Larry as the three critical-path collaborators. Sources are silent on Mary specifically. Resolution: the Friday retro and the 5:30 PM hard stop are the protective rituals; this roadmap respects them absolutely.

8. **The "every win counts" cushion math at job-hunt scale.** None of the sources do the actual math: what a $50/mo or $200/mo cushion-stream actually represents against Sean's monthly burn. Out of scope for this roadmap; defer to a `runway-math.md` artifact owned by Phase 1 Task 1.4.

---

## 5. Existing-Artifact Audit

Sean already has the proof-points. For each: status + the single thing that would make it interview-grade.

| # | Artifact | Public-readiness | The single thing to make it interview-grade |
|---|----------|------------------|---------------------------------------------|
| 1 | Superuser Pack v3.20.0 (117 skills, 13 hooks, 14 SDK agents, 7 active) | **Public** — needs sanitization first (3 Block-named skills) | A README "Why this exists" section in Karpathy/Nate framing + one 5-min Loom narrating one live agent run |
| 2 | Phase D typed reasoning edges (`concept_edges` SQLite + synthesizer relations) | **Public** in repo, no public framing | Commit Claude-Nate-2 §2a 4Q draft as `EXPLANATION.md` (already pre-written, just paste-and-commit) |
| 3 | Phase 6 knowledge loop (producer + consumer side) | **Public** in repo, no public framing | Commit Claude-Nate-2 §2e 4Q draft as `docs/knowledge-loop/EXPLANATION.md` (already pre-written) |
| 4 | Agentic financial-research fleet | **Private** — needs sanitization (no personal numbers, sanitize data sources) | Sanitized PRD-style writeup with 4Q template seeded from Claude-Nate-2 §2c |
| 5 | 2D animation pipeline (`sw-portfolio-animation-pipeline`) | **Private** — ships June 11 | The June 11 short itself + a production diary 4Q seeded from Claude-Nate-2 §2d |
| 6 | The Block PM templates (retained at `the-block/`) | **Private** — needs CIIA review per template | Sanitized template pack with 4Q on what each was for, when it failed, how it adapts to AI-native teams (ChatGPT-Nate-2 §2 framing) |
| 7 | The Block ETF page creator skill | **Block-owned IP per CIIA** — must sanitize before any public push | Generic version: `structured-content-publisher` pattern. Block-specific version archived. 4Q commit alongside |
| 8 | 14 SDK agents fleet (7 active) | **Public** in repo, no narrative | A 5–7 minute unedited screen recording walking through the agents with one running live (Nate-1 §5.1) |
| 9 | `writing-voice-modes` skill (Sean Mode/Sedaris-tuned) | **Public** in repo | Short post + sample voice-mode comparison output (Karpathy's "council of LLM judges for taste" anchor) |
| 10 | `intent-engineering` skill (the differentiated IP) | **Public** in repo, not yet MCP-wrapped | **MCP server v0 by 2026-05-25** — Track-C centerpiece |

Ten artifacts. Five are already public-ish and need only 4Q `EXPLANATION.md` commits. Four require either sanitization or production work. One (intent-engineering MCP) is the Track-C centerpiece.

---

# PART 2 — UNIFIED ROADMAP (writing-plans pass)

> **For Sean:** This is a plan, not a sentence. Steps use checkbox (`- [ ]`) syntax. Maps onto the existing [Phase 0–8 master plan](../2026-05-04-onwards-and-upwards-plan.md) — references existing task IDs wherever the work overlaps. Mark items done as you go.

**Goal:** Convert the existing Phase 0–8 plan into an explanation-artifact-driven sprint that ships Track-C v0 by 2026-05-25, attaches 4Q `EXPLANATION.md` files to every existing public artifact, and resolves the 9 open work items from the operating-model — without breaking any Tier-A truth or burning past 5:30 PM.

**Architecture:**
- **Canonical home for explanations:** Personal site `/transactions/` route + co-located `EXPLANATION.md` in each GitHub repo (per Claude-Nate-2 Decision 1, ChatGPT-Nate-2 Decision 1).
- **Distribution layer:** Substack as primary publishing home + LinkedIn syndication + GitHub for code (Claude-Nate-1 Decision 4).
- **Track-C:** `intent-engineering` MCP server v0 by 2026-05-25 (master plan Phase 4, operating-model Tier-A protected).
- **Cadence:** One published artifact per Friday by 5 PM (master plan Phase 7 + operating-model retro). Two flagship 1,500-word artifacts (MCP server, animation pipeline) + four short ~400-word `EXPLANATION.md` artifacts attached directly to repos.

**Tech Stack:**
- TypeScript MCP SDK (`@modelcontextprotocol/sdk`), Node 22, Anthropic SDK for `intent-engineering` MCP server
- Substack for distribution layer
- Astro 5 + React islands for personal site (already in flight per Sean's portfolio plan)
- Loom for live demos
- Claude Desktop for MCP server local testing

---

## Tasks 0–7 mapped onto Phase 0–8 of the master plan

The master plan's Phase 0–8 stays canonical. These tasks add the explanation-artifact wrapper, fill in the 9 open operating-model work items, and concretize Track-C around the synthesis findings.

---

### Task 0 — Block IP scrub (gates everything public; finishes Phase 3 + Phase 4) ✅ CLOSED 2026-05-07

> **STATUS:** All 5 steps complete. Public-push gate satisfied. Verified 2026-05-07 against repo state (audit file, sanitization commit, grep, `validate.py`, git log). The single intentional deviation from "zero hits" is the protected physical archive path (`vault/{40,60}_archive/operating-models-the-block-2026-05/`) preserved by Sean's locked Plan A decision so historical operating-model interviews still resolve to the on-disk bundle.

**Maps to:** Master plan Phase 1 [Open Threads] + Phase 4 Task 4.3 Step 9 (both also marked closed 2026-05-07).

**Files:**
- Modify: [`the-block/product-management/the-block-jira-ticket-writer/`](../../../../the-block/product-management/the-block-jira-ticket-writer/) (sanitize → generic `pm-ticket-writer-with-style-guide`)
- Modify: [`creative-studio/scripts/`](../../../../creative-studio/scripts/) ETF page creator → generic `structured-content-publisher`
- Modify: [`the-block/product-management/biweekly-jira-update/`](../../../../the-block/product-management/biweekly-jira-update/) → generic `biweekly-stakeholder-update`
- Modify: [`CHANGELOG.md`](../../../../CHANGELOG.md), [`CLAUDE.md`](../../../../CLAUDE.md), [`README.md`](../../../../README.md) — count updates per project rule

**- [x] Step 1: Audit each Block-named skill for transferable vs. Block-specific IP.** ✅ Completed 2026-05-06. Audit at [`2026-05-08-block-skills-audit.md`](../2026-05-08-block-skills-audit.md) — 11 kB line-by-line audit. Surfaced that the original 3-skill scope was incomplete: `the-block-jira-ticket-writer` had been merged into `jira-automation/` pre-audit, `biweekly-jira-update` had been merged into `stakeholder-update/` cleanly, and 4 additional contaminated skills (`api-product-management`, `jira-automation`, `work-operating-model` [3 files], `daily-driver`) were live in `.claude/skills/`. Plan A (full clean, 30 → 0) locked.

**- [x] Step 2: Rewrite each skill's frontmatter and body to remove Block-specific names.** ✅ Completed 2026-05-06 in commit `5a84069`. Sanitized 30 hits → 5 across 7 files: `etf-page-creator/SKILL.md` (Track Insight + Block SEO templates parameterized), `api-product-management/SKILL.md` (developer.theblock.co + @theblock/data-sdk → generic), `jira-automation/SKILL.md` (dead path + Campus/theblock.co example sanitized), `work-operating-model/{SKILL.md, artifact-templates.md, interview-questions.md}` (`the-block` slug renamed to `archived-employer` across 4-domain selectable list), `daily-driver/SKILL.md` (calendar archive line parameterized). `etf-page-creator` kept its name per audit deviation note (skill is ETF-specific in mechanics, the *Block-ness* is what got stripped, not the ETF-ness).

**- [x] Step 3: Verify zero Block-string contamination.** ✅ Verified 2026-05-07. Grep returns 5 hits in 1 file: `.claude/skills/work-operating-model/SKILL.md`. All 5 are the protected physical archive path string preserved by Sean's locked Plan A decision (commit `5a84069` body explicitly documents this). Functional capability of historical-interview resolution preserved; literal CIIA-protected strings removed everywhere they could be.

**- [x] Step 4: Run validate.py.** ✅ Verified 2026-05-07. `python3 scripts/validate.py` → "Validation PASSED (60 warning(s))." All 60 warnings are pre-existing secret-pattern false-positives in unrelated skills (`last30days`, `gemini-image-gen`, `react-vite-tailwind`, `mcp-integration`), not Block-related. 0 errors.

**- [x] Step 5: Commit.** ✅ Commit `5a84069` (2026-05-06): `chore(skills): full Block-string scrub across .claude/skills/ (CIIA §2.3 compliance + public-push readiness)`.

**Verification gate:** ✅ **CLOSED 2026-05-07.** [Master plan Phase 3 Task 3.3](../2026-05-04-onwards-and-upwards-plan.md) (LinkedIn announcement) and [Phase 4 Task 4.3 Step 9](../2026-05-04-onwards-and-upwards-plan.md) (publish MCP server / pin Superuser Pack on profile) are no longer gated by this task. The 3 originally-named skills (`the-block-jira-ticket-writer`, `etf-page-creator`, `biweekly-jira-update`) are all addressed: first two via merges that pre-dated the scrub, third via in-place parameterization. Plus 4 additional contaminated skills caught by the broader audit, all sanitized in the same commit.

---

### Task 1 — Set up the canonical home + 4Q template discipline (Phase 2 wrapper)

> **STATUS (2026-05-12 evening):** Steps 1, 2, 4 complete in a Cowork session. Steps 3 (personal-site `/transactions/` route) and 5 (commits) handed to Claude Code via [`2026-05-13-claude-code-handoff-task-1-2.md`](2026-05-13-claude-code-handoff-task-1-2.md). The handoff includes a stop-and-confirm gate on the personal-site repo path (Decision 2 fallback fires if scaffolding from scratch >30 min).
>
> **DEPLOYMENT GAP IDENTIFIED (2026-05-13):** During handoff execution Claude Code discovered the `/transactions/` route already existed in [`~/Code-Brain/sw-portfolio/`](https://github.com/seanwinslow28/sw-portfolio) from commit `f13a103` (2026-05-08) — so Steps 3 + 5 of the handoff were effectively pre-done. **However**, the repo is **not deployed anywhere**: no `vercel.json` / `netlify.toml` / `wrangler.toml` / `CNAME` / `.github/workflows/`, and `seanwinslow.com` (owned via Cloudflare + Namecheap) doesn't point at any live instance. Sean explicitly deferred deployment 2026-05-13 — site isn't recruiter-ready yet, no point lighting up the domain with a half-finished page. **Full fix when ready to ship is captured in [`2026-05-13-personal-site-deployment-deferred.md`](2026-05-13-personal-site-deployment-deferred.md).** Triggers to un-defer (LinkedIn link, Substack post, etc.) are listed there. Future Claude Code sessions: do NOT proactively start deploying — surface that doc when Sean signals the site is ready.
>
> **STATUS (2026-05-16) — UN-DEFERRED by Council Gap-Fill 3:** Council (premium-profile LLM run, 2026-05-16 — see [`2026-05-16-council-nate-jones-digest.md`](2026-05-16-council-nate-jones-digest.md)) reframed `/transactions/` from "gallery awaiting more entries" → "reverse-chronological ledger of shipped AI artifacts." Five `EXPLANATION.md` files already exist on disk (intent-engineering MCP, vault-synthesizer eval suite, substack-drafter gate-b-drafts, phase D typed edges, phase 6 knowledge loop) — enough for a ledger that stands alone today. The 2026-05-13 deferral remains correct for the gallery form; this amendment ships the ledger form first. Architecture confirmed via visual mockup 2026-05-16: home-page V3 card gallery unchanged + intent-engineering MCP added as a 6th card; `/transactions/` becomes a flat reverse-chronological table; `/transactions/{slug}/` deep-dives keep the V3 card hero so the design system lives where it's actually read. Host: Vercel (consistency with `agent-fleet-observability` already deploying there); DNS: Cloudflare unchanged, set to **DNS-only / orange-cloud OFF** for the Vercel records so Vercel's edge handles SSL without proxy interference. [`2026-05-13-personal-site-deployment-deferred.md`](2026-05-13-personal-site-deployment-deferred.md) frontmatter flipped to `status: superseded-by-gap-fill-3`. Target: live at seanwinslow.com **Mon 2026-05-19** + LinkedIn refresh same-day.

**Maps to:** Master plan Phase 2 Task 2.4 (GitHub README pass) and Phase 3 Task 3.3 (public announcement decision).

**Files:**
- Create: `vault/40_knowledge/templates/EXPLANATION-template.md` (the 4Q template scaffold)
- Create: `<personal-site>/src/pages/transactions/index.astro` (route stub — list of artifacts)
- Modify: [`README.md`](../../../../README.md) — add "Why this exists" section in Karpathy framing

**- [x] Step 1: Write the 4Q template scaffold.** ✅ Already canonical 2026-05-06. Verified 2026-05-12 evening — the template at `vault/40_knowledge/templates/EXPLANATION-template.md` is materially richer than the minimum scaffold this step specified (4699 bytes, frontmatter with template-slug + ai-context, copy-able body block, How-to-use section, Why-this-template section, Anti-patterns section). The template's own ai-context already names the five planned consumers (Phase D, Phase 6, intent-engineering MCP, agentic financial-research fleet, animation pipeline). No overwrite — pre-existing draft is the canonical version.
Save to `vault/40_knowledge/templates/EXPLANATION-template.md`:
```markdown
---
artifact: <slug>
created: <YYYY-MM-DD>
ai-context: "Comprehension artifact for <slug>. 4-question template per Nate B Jones / ADR convention."
---

# <Artifact Name> — Explanation

## What is this?
<2–4 sentences. What it does, where it lives, who/what it's for.>

## Why this approach?
<3 options considered. Chose option X because Y. Trade-offs accepted.>

## What would break?
<3 named failure modes with detection signals.>

## What did I learn?
<2–3 sentences. The non-obvious insight that travels beyond this artifact.>
```

**- [x] Step 2: Commit the template + add a `community-skills/comprehension-audit/` skill stub.** Template commit complete 2026-05-06 (file is on disk and canonical). The `community-skills/comprehension-audit/` skill stub remains explicitly deferred to Week 4 per the original spec ("Full implementation deferred — Sean ships the template now and adds the skill in Week 4 once 3+ artifacts have used it"); the template's own body already references this deferred Week-4 stub. No action required this week.

**- [x] Step 3 (original scope, 2026-05-08): Skeleton the personal site `/transactions/` route.** ✅ Complete via commit `f13a103` in [`~/Code-Brain/sw-portfolio/`](https://github.com/seanwinslow28/sw-portfolio) — discovered already-done during 2026-05-12 handoff execution. Route, `[slug].astro` deep-dive, content collection schema, and V3 card aesthetic all scaffolded. Two MDX entries at `src/content/transactions/` (phase-d-typed-edges + knowledge-loop-phase-6).

**- [ ] Step 3 (Gap-Fill 3 expanded scope, 2026-05-16): Ship `/transactions/` as the reverse-chronological ledger (≤4 days, target Mon 2026-05-19).**

**Files for this step:**
- Modify: [`~/Code-Brain/sw-portfolio/src/content/config.ts`](../../../../../sw-portfolio/src/content/config.ts) — extend schema with `surface` (required string), promote `shipped` from optional → required, add `repoUrl` + `explanationUrl` (optional GitHub permalinks)
- Modify: `~/Code-Brain/sw-portfolio/src/pages/transactions/index.astro` — flat reverse-chronological table (replaces card-grid index)
- Modify: `~/Code-Brain/sw-portfolio/src/pages/transactions/[slug].astro` — keep V3 card-hero deep-dive (verify rendering across all 5 entries)
- Modify: `~/Code-Brain/sw-portfolio/src/pages/index.astro` — add 6th project card: `intent-engineering MCP` (links to `/transactions/intent-engineering-mcp/`)
- Modify: `~/Code-Brain/sw-portfolio/astro.config.mjs` — `site: 'https://seanwinslow.com'` + `@astrojs/sitemap` + `@astrojs/rss` integrations
- Create: `~/Code-Brain/sw-portfolio/src/content/transactions/intent-engineering-mcp.md` (frontmatter sources [`~/Code-Brain/sw-mcp-intent-engineering/docs/EXPLANATION.md`](../../../../../sw-mcp-intent-engineering/docs/EXPLANATION.md))
- Create: `~/Code-Brain/sw-portfolio/src/content/transactions/vault-synthesizer-eval-suite.md` (sources [`evals/vault-synthesizer/EXPLANATION.md`](../../../../evals/vault-synthesizer/EXPLANATION.md))
- Create: `~/Code-Brain/sw-portfolio/src/content/transactions/substack-drafter.md` (sources [`gate-b-drafts/EXPLANATION.md`](../gate-b-drafts/EXPLANATION.md))
- Modify: [`2026-05-13-personal-site-deployment-deferred.md`](2026-05-13-personal-site-deployment-deferred.md) — frontmatter `status: superseded-by-gap-fill-3`

**- [ ] Step 3.1: Schema extension + 3 new MDX entries.** Update `src/content/config.ts` with the new required + optional fields. Bring Phase D + Phase 6 frontmatter forward to the new shape (one-line updates each). Author the 3 new MDX entries from existing EXPLANATION.md files; pitch in `valueProp` ≤140 chars; `surface` values: `"MCP server"` / `"eval harness"` / `"SDK agent"`. ~90 minutes.

**- [ ] Step 3.2: Rewrite `index.astro` as a reverse-chronological table.** Five columns: Date / Artifact / Surface (pill) / 4-Q link / Repo. Sort desc by `shipped`. Preserve V3 paper-cream background + pencil-line separator + teal/amber tokens. Keep `<BaseLayout>`. ~60 minutes.

**- [ ] Step 3.3: Verify `[slug].astro` deep-dives render for all 5 entries.** Run `npm run dev`; manually walk each of 5 routes (`/transactions/intent-engineering-mcp/`, `/vault-synthesizer-eval-suite/`, `/substack-drafter/`, `/phase-d-typed-edges/`, `/knowledge-loop-phase-6/`); confirm V3 card-hero + Loom-frame placeholder + 4-Q section all populate from frontmatter + body. Fix any schema mismatches surfaced by the schema extension. ~30 minutes.

**- [ ] Step 3.4: Add intent-engineering MCP as 6th home-page card.** Edit the `projects` array in `src/pages/index.astro`: `title: 'intent-engineering MCP'`, `slug: 'intent-engineering-mcp'`, `description: 'MCP server exposing 3 specification-engineering tools. Live on npm + the MCP registry.'`, `tags: ['MCP', 'TypeScript', 'AI Tooling']`, `placeholder: 'MCP Server'`. Link target `/transactions/intent-engineering-mcp/` (not `/work/`) — it's an AI ledger artifact, ledger-resident. Real thumbnail asset is a follow-up. ~15 minutes.

**- [ ] Step 3.5: Production config.** `site: 'https://seanwinslow.com'` in `astro.config.mjs`. Add `@astrojs/sitemap` + `@astrojs/rss` (RSS feed at `/transactions/rss.xml`). `npm run build` → verify `dist/sitemap-index.xml` + `dist/transactions/rss.xml` generate with `seanwinslow.com` URLs (not `localhost:4321`). ~30 minutes.

**- [ ] Step 3.6: Vercel deploy.** Push to `main`; Vercel dashboard → New Project → import `seanwinslow28/sw-portfolio` → framework auto-detects Astro → build command `npm run build` → output directory `dist/` → no environment variables needed → deploy. Verify the `*.vercel.app` preview URL loads: home shows 6 cards, `/transactions/` shows 5 ledger rows, all 5 deep-dives resolve cleanly. ~15 minutes.

**- [ ] Step 3.7: Attach `seanwinslow.com` apex.** Vercel → Project Settings → Domains → add `seanwinslow.com` + `www.seanwinslow.com` (www → apex redirect). Vercel returns target CNAMEs / A records. Add the records in Cloudflare DNS dashboard with the Cloudflare proxy set to **DNS only** (orange-cloud OFF) for those records — Vercel handles its own edge + SSL; the Cloudflare proxy causes SSL handshake friction if left ON. Wait ~5 min for SSL provisioning. Verify `https://seanwinslow.com` resolves with a clean certificate. ~30 minutes.

**- [ ] Step 3.8: LinkedIn refresh (Mon 5/19, same-day as deploy).** Banner: ledger screenshot of `/transactions/`. Headline: `AI PM | Agent fleet operator | seanwinslow.com/transactions`. "Open to Work" toggle: ON, **recruiter-only visibility** (not the public green frame). Update About section: one-paragraph rewrite ending with the `seanwinslow.com` URL. ~20 minutes. *Sean owns every word — agents draft / Sean sends boundary preserved.*

**- [ ] Step 3.9: Supersede the deferred-deployment doc.** Set `status: superseded-by-gap-fill-3` in [`2026-05-13-personal-site-deployment-deferred.md`](2026-05-13-personal-site-deployment-deferred.md) frontmatter. Add a one-paragraph note at the top pointing at this Task 1 Step 3 amendment as the canonical deploy record. ~5 minutes.

**Verification gate (Gap-Fill 3 binary success criteria, all must pass by Mon 2026-05-19 EOD):**
1. `https://seanwinslow.com` resolves with a clean SSL certificate; home page shows 6 cards (5 career + intent-engineering MCP).
2. `https://seanwinslow.com/transactions/` shows all 5 ledger rows in reverse-chronological order with working 4-Q + repo links.
3. All 5 deep-dive routes (`/transactions/{intent-engineering-mcp, vault-synthesizer-eval-suite, substack-drafter, phase-d-typed-edges, knowledge-loop-phase-6}/`) render the V3 card hero.
4. `https://seanwinslow.com/sitemap-index.xml` + `https://seanwinslow.com/transactions/rss.xml` both resolve.
5. LinkedIn banner + headline + Open-to-Work recruiter-only all live.
6. `python3 scripts/validate.py` in the superuser-pack repo returns ≤60 warnings / 0 errors (v3.30.1 baseline preserved).

**Compounding payoff (verbatim from council brief):** Every future ship adds a ledger row. `build_ledger.mjs` auto-crawl script deferred until ≥7 rows justify the abstraction (currently 5). Replaces the resume as the lead artifact in recruiter conversations. Each Substack post (post 1 ships Fri 2026-05-22) gets a permanent ledger target. Future Gap-Fills 1 / 4 / 5 each ship a ledger row for free.

**Demo shape:** URL in the email signature. Recruiter call opens: *"I see you saw the ledger — which row do you want me to start with?"*

**Tier-A check:** Walk-away $100k N/A. AI PM > Tech PM > Creative PM ✅ (ledger optimizes for AI-PM recruiter scan; intent-engineering MCP cross-listed at both home + ledger). Agents draft / Sean sends ✅ (LinkedIn copy + every MDX `valueProp` is Sean's hand). 5:30 PM hard stop ✅ (~4.5 hours total work fits inside two existing 8:30–5:30 containers Sat-Sun + a short Mon morning deploy block). Track-C protected ✅ (intent-engineering MCP already shipped 2026-05-12; this only makes it visible).

**- [x] Step 4: Rewrite the Superuser Pack README opening paragraph.** ✅ Already in Karpathy framing 2026-05-12 evening. Verified the current README.md line 3 reads: *"An open-source agentic engineering practitioner's toolkit — 118 skills, 13 subagents, 14 hooks, 17 autonomous SDK agents (8 currently running on launchd by default, 2 opt-in disabled-by-default, 1 manual-trigger), 3 primary domains, an Obsidian vault, and a Claude Agent SDK runtime, all auto-loaded. Every component is in active use; every scheduled agent has a launchd schedule; every skill is a prompt and every prompt has a job. If you've read Karpathy's 'agentic engineering' framing and wondered what one looks like in the wild, this is one."* This satisfies every condition this step specified — leads with "agentic engineering practitioner toolkit," names the full stack, references Karpathy explicitly. No edit applied; touching it would create merge-conflict risk for zero recruiter-readability gain. Numbers in the current README (118 skills, 17 SDK agents) supersede the older 117/14 numbers in this step's original spec — those reflected the v3.20.0 baseline; the README's are v3.33.0-accurate.

**- [ ] Step 5: Commit.** **HANDED TO CLAUDE CODE 2026-05-12 evening** via [`2026-05-13-claude-code-handoff-task-1-2.md`](2026-05-13-claude-code-handoff-task-1-2.md) Step 4 (Superuser Pack commit) + Step 5 (personal-site commit). Both commit messages are pre-written in the handoff. The handoff also runs `python3 scripts/validate.py` ahead of commit and reports back if new errors surface that weren't in the v3.30.1 baseline of 60 warnings / 0 errors.

**Verification gate:** Personal site loads at `localhost:4321/transactions/` with one populated page (2 entries: Phase D + Phase 6). README opening paragraph stands alone as a recruiter-readable pitch. The handoff doc's Step 7 (verification gate) consolidates: `validate.py` passes, both repos show new commits in `git log -1`, and `curl -s localhost:4321/transactions/ | grep -c "Phase D"` returns ≥1.

---

### Task 2 — Commit pre-drafted 4Q `EXPLANATION.md` files for two existing public artifacts (Phase 2 wrapper, ships Friday Week 1)

> **STATUS (2026-05-12 evening):** Steps 1, 2, 4 complete in a Cowork session. Both EXPLANATION.md files written and passed the <90-sec readability check before handoff. Steps 3 (`/transactions/` entries) and 5 (git commit) handed to Claude Code via [`2026-05-13-claude-code-handoff-task-1-2.md`](2026-05-13-claude-code-handoff-task-1-2.md). Substack syndication explicitly deferred until full portfolio locks down (Sean directive — Loom + Substack + LinkedIn all batched for a single post-portfolio publishing pass).

**Maps to:** Master plan Phase 2 Task 2.4 + Karpathy synthesis Part 5 ("explain what you've already built").

**Files:**
- Create: `agents-sdk/lib/concept_edges/EXPLANATION.md` (Phase D typed reasoning edges)
- Create: `agents-sdk/agents/knowledge_loop/EXPLANATION.md` (Phase 6 producer + consumer)
- Modify: `<personal-site>/src/pages/transactions/index.astro` (add 2 entries)

**- [x] Step 1: Paste Claude-Nate-2 §2a verbatim into Phase D `EXPLANATION.md`.** ✅ Done 2026-05-12 evening at [`agents-sdk/lib/concept_edges/EXPLANATION.md`](../../../../agents-sdk/lib/concept_edges/EXPLANATION.md). Source §2a pasted verbatim (lines 17–25 of [`claude-nate-prompt-2-analysis.md`](reference-synthesis-docs/claude-nate-prompt-2-analysis.md)). Frontmatter follows the Task-1 template (`artifact: phase-d-typed-reasoning-edges`, `created: 2026-05-12`, ai-context line per the 4Q convention) and adds a `related:` wikilinks block pointing at `concept_edges.py`, `vault_indexer.py`, `vault_synthesizer.py`, `knowledge_lint.py` so the file participates correctly in the Phase 6 knowledge graph the agents already maintain. Readability check passed: "What is this?" is 2 sentences / 58 words / six relation types enumerated by name.

**- [x] Step 2: Paste Claude-Nate-2 §2e verbatim into Phase 6 `EXPLANATION.md`.** ✅ Done 2026-05-12 evening at [`agents-sdk/agents/knowledge_loop/EXPLANATION.md`](../../../../agents-sdk/agents/knowledge_loop/EXPLANATION.md). Source §2e pasted verbatim (lines 57–65). Frontmatter follows the Task-1 template (`artifact: knowledge-loop-phase-6`, `created: 2026-05-12`) and adds a `related:` wikilinks block pointing at `flush.py`, `vault_indexer.py`, `vault_synthesizer.py`, `knowledge_lint.py`, `query.py`, `session-start-inject-index.sh`, `pre-compact-flush.sh` so the file documents the full producer/consumer surface. Readability check passed: "What is this?" is 3 sentences / ~95 words; producer/consumer split is load-bearing and cannot be cut further without losing the architecture.

**- [ ] Step 3: Add both to the `/transactions/` page.** **HANDED TO CLAUDE CODE 2026-05-12 evening** via [`2026-05-13-claude-code-handoff-task-1-2.md`](2026-05-13-claude-code-handoff-task-1-2.md) Step 2. The handoff carries a complete `index.astro` template with both entries pre-populated: artifact name + one-sentence pitch + GitHub permalink to the new `EXPLANATION.md` + permalink to the underlying code + ship date.

**- [x] Step 4: Verify each `EXPLANATION.md` is recruiter-readable cold.** ✅ Done 2026-05-12 evening. Both files pass the <90-second target. Phase D: 2-sentence opener, six relation types enumerated by name, three concrete failure modes with detection signals, one transferable insight (OPTIONAL fields > required fields for LLM-emitted structured data). Phase 6: 3-sentence opener with explicit producer/consumer split, three failure modes named with mitigations, one transferable insight (Claude is happy to be its own RAG layer if you give it the schema). Neither needs "What is this?" trimming.

**- [ ] Step 5: Commit.** **HANDED TO CLAUDE CODE 2026-05-12 evening** via [`2026-05-13-claude-code-handoff-task-1-2.md`](2026-05-13-claude-code-handoff-task-1-2.md) Step 4. Commit message pre-written: `docs: add 4Q comprehension artifacts for Phase D typed edges + Phase 6 knowledge loop`. Pre-flight runs `python3 scripts/validate.py` and stops if new errors appear that didn't exist in the v3.30.1 baseline.

**Verification gate:** Friday Week 1's published artifact — file commits land in repo (handed to Claude Code), `/transactions/` page surfaces both entries with working GitHub links. **Substack syndication deferred** per Sean's 2026-05-12 directive: all Looms + Substack + LinkedIn posts batch into one publishing pass after the full portfolio (Tasks 3 + 4 + 5 + 8 + animation pipeline) is locked down. Net effect: the artifact ships now; the broadcast follows after the portfolio's at-rest state is final.

---

### Task 3 — Track-C `intent-engineering` MCP server v0 (Phase 4, ship 2026-05-25)

**Maps to:** Master plan Phase 4 Tasks 4.1–4.3 (already detailed; this task adds the explanation wrapper).

**STATUS — as of 2026-05-12 (Day 6 of 19, 13 DAYS AHEAD of the 2026-05-25 ship date):** Build + publish complete. **npm AND MCP registry both live.** Ship-gate items 1–16 closed. Remaining items 17–19 are launch comms (Loom + LinkedIn + Substack) — Sean executes. 13 commits pushed to `github.com/seanwinslow28/sw-mcp-intent-engineering`.

| Build Phase | Status | Commits | Notes |
|---|---|---|---|
| 0 — Read + plan | ✅ approved 2026-05-08 | (no code) | Implementation plan reviewed against scope-lock §2–§9, approved |
| 1 — Scaffold + `ping` tool | ✅ verified 2026-05-08 | `24e4047` | Smoke-tested in Claude Desktop, `ping` returns `pong`. SDK pinned to `1.29.0`, Stdio transport, MIT license, npm scope `@swins/intent-engineering-mcp` (fallback used because `@swinslow` was taken) |
| 2 — Three real tools | ✅ verified 2026-05-08 | `b0ae1ce`, `ae5deaa`, `5835bcb`, `abad1d4` | All three tools tested in Claude Desktop with §4–§6 example inputs. Audit returned 4/25 + 3 anti-patterns on §4 spec (ship-gate item 4 ✅); scaffold returned correct YAML for all 3 `kind` values (ship-gate item 5 ✅); retrofit returned differentiated reasoning across 3 distinct SKILL.md files (ship-gate item 6 ✅) |
| 3 — Hardening Gate A | ✅ done 2026-05-08 | `bc4caa9`, `7bf479a` | Parser autonomous-loop heuristic tightened; scope-lock §6 path fix; MCP Inspector pass clean; 30k pagination round-trip works (token chain `null → 10000 → 20000 → 30000 → null` — ship-gate item 8 ✅); 5-skill audit shows real findings; `prepublishOnly` grep guard active (ship-gate item 13 ✅). **No `console.log` anywhere in `src/`** |
| 3 — Hardening Gate B | ✅ done 2026-05-12 | `d101ae6`, `1d25a54`, `456d70d` | README per §8 item 9 (single-sentence pitch, copy-paste-able `claude_desktop_config.json` block, three-tool inventory, connected-server screenshot at `docs/screenshots/intent-engineering-mcp-connected.png`). `docs/EXPLANATION.md` 4Q artifact landed. 118-skill audit CSV (`examples/superuser-pack-retrofit-assessment.csv`) folded into README + EXPLANATION — 24% L1-mvr / 36% L2-structured / 40% L3-full, zero parse errors. **Dogfood result preserved:** intent-engineering SKILL.md scored 23/25 with zero anti-patterns when audited by its own server. |
| 4 — Publish + registry | ✅ done 2026-05-12 | `95ab4b4`, `92ce6ca`, `123b324` | **npm published** at 2026-05-12T15:47:07Z: `@swins/intent-engineering-mcp@0.1.0` on registry.npmjs.org. Tarball 20.5 kB packed / 73.3 kB unpacked / 13 files. **MCP registry published** same session: `com.seanwinslow/intent-engineering@0.1.0` on registry.modelcontextprotocol.io via DNS-verified domain namespace (NOT `io.github.seanwinslow28/*` — per scope-lock §10.3). Three small fixups landed mid-publish: add `mcpName` + `server.json` (`95ab4b4`), normalize bin path (`92ce6ca`), schema corrections (`123b324`). Mechanics captured in "Publish + registry flow — frozen reference" subsection below — do not re-derive next time. |
| 5 — Launch comms | ⏳ pending Sean | — | Ship-gate items 17 (90-sec Loom), 18 (Loom plays end-to-end clean), 19 (LinkedIn tagging Anthropic + MCP team + Substack syndication). Tier-A protected; due on or before 2026-05-25. |

**Repo location (locked):** `~/Code-Brain/sw-mcp-intent-engineering/` — pushed to `github.com/seanwinslow28/sw-mcp-intent-engineering`. (Note: original roadmap referenced `~/Code/` — corrected per scope-lock §1 path note.)

**Test artifacts archived at:** [`~/Code-Brain/sw-mcp-intent-engineering/docs/claude-code-responses-and-tests/`](../../../../../sw-mcp-intent-engineering/docs/claude-code-responses-and-tests/) — all phase verification outputs from 5/7–5/8 saved there for traceability and future Loom-narration material.

**Two scope-lock corrections shipped during the build (CHANGELOG.md in the new repo):**
1. **Validation checklist count:** §3 + §4 corrected from "40-item" to "25-item" to match SKILL.md's actual structure (commit `b0ae1ce`). The "40" claim was a documentation error in scope-lock; SKILL.md is canonical per §3.
2. **§6 example path:** corrected from non-existent `format-on-edit/SKILL.md` (a hook, not a skill) to `personal-task-management/SKILL.md` (commit `bc4caa9`).

**Files:**
- Already specified in master plan: `~/Code-Brain/sw-mcp-intent-engineering/` (path corrected from `~/Code/` 2026-05-07)
- Add: `~/Code-Brain/sw-mcp-intent-engineering/docs/EXPLANATION.md` (4Q artifact) — **next session**
- Add: `<personal-site>/src/pages/transactions/intent-engineering-mcp.astro` (deep-dive page) — parallel critical-path

**- [x] Step 1–10: Execute master plan [Phase 4 Tasks 4.1–4.3](../2026-05-04-onwards-and-upwards-plan.md) as written.** ✅ Complete through Phase 4 (publish + registry). README, `EXPLANATION.md`, npm publish, and registry submit all landed 2026-05-12 — 13 days ahead of the 5/25 ship date. Remaining items (Loom, `/transactions/` embed, announcement posts) tracked in Step 12–14 below.

**- [x] Step 11: Add the pre-drafted 4Q `EXPLANATION.md` from Claude-Nate-2 §5.1.** ✅ Landed in `d101ae6` (initial 4Q) and `456d70d` (118-skill audit results folded in). The dogfood result (23/25 zero anti-patterns) and the opinionated-heading limitation both made it into the README + EXPLANATION.
Source: [`claude-nate-prompt-2-analysis.md`](reference-synthesis-docs/claude-nate-prompt-2-analysis.md) §5.1 "MCP Server: vault-knowledge-mcp" block, adapted to `intent-engineering` (swap `find_contradictions` → `analyze_intent_spec`, etc.). The 4Q structure transfers; only the tool names change.

**Two Phase 3 audit findings to incorporate** (captured 2026-05-08 — DO NOT LOSE; these are the highest-leverage talking points uncovered during Phase 3 verification):

1. **Dogfood result:** `intent-engineering/SKILL.md` scored 23/25 with zero anti-patterns when audited by its own MCP server. Two minor warns (outcome measurability, health-metric behavioral adjustments). Strong Loom + README hook — "the tool eats its own dog food." Lands naturally as a 4Q "What did I learn?" answer, or as a Loom Beat 4 swap if the daily-driver retrofit doesn't pop on screen.
2. **Opinionated heading boundary:** the v0 audit requires explicit `## Objective` / `## Desired Outcomes` headings. 4 of 5 skills tested scored 1/25 because they use different heading vocabularies (`## When to Use`, `## How to Apply`). Not a bug — it's a v0 design choice — but worth naming in README under "Limitations" so a recruiter doesn't ding you for it. v0.2 could add a heading-vocabulary mapper. Lands naturally in the 4Q "What would break?" answer AND a README "Limitations" section that demonstrates judgment about scope.

Actual draft for `intent-engineering` (paste this into `EXPLANATION.md`):
```markdown
## What is this?
An MCP server that exposes 3 tools from Sean's `intent-engineering` skill (`analyze_intent_spec`, `generate_template`, `audit_existing_spec`) over the standard MCP protocol. Any MCP-aware client (Claude Desktop, Cursor, Anti-Gravity) can call them.

## Why this approach?
MCP because it's the protocol every serious agent harness now speaks; TypeScript because the SDK has the deepest client coverage; Stdio transport because v0 only needs local runs and zero infra. Rejected alternatives: a Python CLI (no agent-harness reads CLIs natively), a REST API (not protocol-native).

## What would break?
(1) Schema drift between the skill's prompt and the MCP tool descriptions — versioning needed. (2) Long input specs hitting the MCP message-size limit — chunking-on-input needed before v1. (3) The `audit_existing_spec` tool requires file-read permission; agents without that permission silently degrade.

## What did I learn?
That MCP is essentially a contract for "I am a tool an LLM can call without me writing a wrapper" — once that landed, the server became a thin protocol adapter over the existing skill. Also: the OPTIONAL field pattern (from Phase D's relations work) translated directly; the `audit_existing_spec` `file_path` parameter is OPTIONAL, falling back to inline `spec_text`, which made the tool resilient to clients that can't pass file paths.
```

**- [ ] Step 12: Add a 90-second Loom demo.**
Show: setup, three tool invocations from Claude Desktop, the value moment ("agent reads a spec and tells you what's missing"). Master plan Phase 4 Task 4.3 Step 8 already calls this out; this task confirms the 4Q pre-draft is the script.

**- [ ] Step 13: Add to `/transactions/`.**
Deep-dive page at `<personal-site>/src/pages/transactions/intent-engineering-mcp.astro`. Embed the Loom + paste the 4Q + link to the GitHub repo.

**- [ ] Step 14: Commit + announce.**
Master plan Phase 4 Task 4.3 Step 10 covers the announce. Don't over-announce — one focused LinkedIn post tagging Anthropic + MCP folks.

**Verification gate:** 2026-05-25 ship. Loom plays. The MCP server runs in Claude Desktop end-to-end. The `EXPLANATION.md` is in the repo, the `/transactions/` page links to it. **This is the Tier-A protected artifact; ship even if applications slip in Week 3.** Build + publish legs: ✅ done 2026-05-12. Loom + announce: pending.

---

#### Publish + registry flow — frozen reference (2026-05-12 worked walkthrough)

> **Why this exists.** When `intent-engineering` shipped, the MCP registry publish leg surfaced two non-obvious gotchas (DNS-verified namespace requires a separate auth path from GitHub OAuth; `server.json` schema uses camelCase and caps `description` at 100 chars) plus one npm gotcha (npm 10+ rejects bin paths with `./` prefix). Capturing the exact sequence here so the next MCP server publish (post-employment, or v0.2 of this one) doesn't re-discover them. **If you're publishing a new MCP server, read this section first.**

##### Namespace decision tree (do this BEFORE writing server.json)

Two namespace shapes the registry supports. Pick one — it determines the auth flow.

- **`io.github.<your-handle>/<server-name>`** — derived from GitHub username. Auth via `mcp-publisher login github` (OAuth device flow). Easiest. Use when the GitHub handle is also your brand, or when domain ownership isn't worth setting up.
- **`com.<your-domain>/<server-name>`** (or `<rev-DNS>/...`) — verified via DNS TXT on a domain you control. Auth via `mcp-publisher login dns --domain <domain> --private-key <hex>`. Use when the GitHub handle has artifacts you don't want baked into a permanent public identifier (e.g., Sean's handle is `seanwinslow28` but the domain `seanwinslow.com` is the brand-facing surface). The intent-engineering MCP uses this path — locked in scope-lock §10.3.

Whichever path you pick, the value goes in **three places that must match exactly**: the `name` field in `server.json`, the `mcpName` field in `package.json`, and (for DNS) the public key in your TXT record. `mcp-publisher` verifies all three links before accepting the payload.

##### The two-leg publish (npm first, then MCP registry)

The order is non-negotiable: npm publishes the actual code; the MCP registry publishes a *pointer* to that npm package. If you flip the order, `mcp-publisher publish` 404s on the npm lookup.

###### Leg 1 — npm publish

Five gotchas surfaced 2026-05-12, all small:

1. **`package.json` must include `"mcpName": "<your-registry-name>"`** as a top-level field. This is what the MCP registry uses to verify the npm package belongs to the registry listing.
2. **`bin` field paths cannot start with `./`** in npm 10+. Use `"bin": { "<command>": "build/index.js" }`, not `"./build/index.js"`. npm auto-normalizes and warns; cleaner to get it right upfront.
3. **Scoped packages need `--access=public`** on first publish: `npm publish --access=public`. Without it, npm assumes you meant a private package and errors.
4. **2FA "auth and writes"** is the secure default. npm will prompt for an OTP interactively, OR you can inline it with `--otp=<6-digit-code-from-authenticator>`. The code rotates every 30s; type fast or paste fast.
5. **CDN propagation delay (~30s–5min) after publish.** `npm view <pkg>` may 404 immediately post-publish because edge nodes haven't refreshed. Don't panic. The website (`npmjs.com/package/<name>`) typically updates within seconds. `curl -s https://registry.npmjs.org/<pkg>` bypasses npm CLI's local cache.

###### Leg 2 — MCP registry publish via DNS auth

The flow is cryptographically rigorous (Ed25519 signature challenge), not just a shared-token TXT record. Five steps:

**Step 1 — generate an Ed25519 keypair** (one-time per domain; back up the private key forever):

```bash
mkdir -p ~/.config/mcp-publisher && chmod 700 ~/.config/mcp-publisher

node -e "
const { generateKeyPairSync } = require('crypto');
const fs = require('fs');
const { publicKey, privateKey } = generateKeyPairSync('ed25519');
const privRaw = privateKey.export({ type: 'pkcs8', format: 'der' }).subarray(-32);
const pubRaw  = publicKey.export({ type: 'spki',  format: 'der' }).subarray(-32);
fs.writeFileSync(process.env.HOME + '/.config/mcp-publisher/<your-domain>.key', privRaw.toString('hex'), { mode: 0o600 });
console.log('Private key saved to: ~/.config/mcp-publisher/<your-domain>.key (chmod 600)');
console.log('');
console.log('Add this TXT record on <your-domain>:');
console.log('  Type:    TXT');
console.log('  Name:    @  (apex)');
console.log('  Content: v=MCPv1; k=ed25519; p=' + pubRaw.toString('base64'));
console.log('  TTL:     Auto');
"
```

Format invariants:
- Private key: **64-character hex string** (raw 32-byte Ed25519 seed, hex-encoded). NOT PEM, NOT base64.
- Public key in TXT: **base64-encoded raw 32 bytes** (44 chars including `=` padding).
- TXT record value: **`v=MCPv1; k=ed25519; p=<base64-pubkey>`** — DKIM-style triple, semicolons + spaces matter.

**Step 2 — add the TXT record at the DNS provider** (apex, not a subdomain — per official docs).

For Cloudflare specifically: dash.cloudflare.com → select domain → DNS → Records → Add → Type: TXT, Name: `@`, Content: paste the full `v=MCPv1; k=ed25519; p=...` value with no outer quotes (Cloudflare adds those itself), TTL: Auto. Cloudflare propagates in ~30 seconds.

> **Hostname ambiguity (unresolved as of 2026-05-12):** the official MCP registry docs use the apex (`<your-domain>`). GitHub issue #385 shows a real-world user verifying at `_mcp-registry.<your-domain>`. Apex worked for `seanwinslow.com` 2026-05-12. If a future publish fails with "DNS verification failed" after the apex record propagates, fall back to `_mcp-registry.<your-domain>` as the host name.

**Step 3 — verify propagation:**

```bash
dig TXT <your-domain> +short
```

Look for the `"v=MCPv1; k=ed25519; p=..."` line. Other TXT records on the apex (SPF, DMARC, verification tokens) are fine.

**Step 4 — authenticate and publish:**

```bash
cd ~/Code-Brain/<repo>
mcp-publisher login dns \
  --domain <your-domain> \
  --private-key "$(cat ~/.config/mcp-publisher/<your-domain>.key)"
mcp-publisher publish
```

The `$(cat ...)` substitution keeps the raw hex out of shell history.

**Step 5 — verify the listing:**

```bash
curl -s "https://registry.modelcontextprotocol.io/v0/servers/<your-namespace>/<server-name>" | python3 -m json.tool
```

(NOT `?name=<...>` as a query param on `/v0/servers` — that endpoint is paginated alphabetically and the param doesn't filter. Use the direct `/v0/servers/<name>` path.)

##### `server.json` schema gotchas (caught by the validator)

The registry validator returns 422 with explicit error messages on bad schemas. Three gotchas worth pre-baking:

- **`description` is capped at 100 chars.** Tight. Don't write a marketing paragraph — write a sentence.
- **Field names are camelCase, not snake_case.** Specifically `registryType` (not `registry_type`) inside `packages[]`. The shape is `packages: [{ registryType, identifier, version, transport: { type } }]`.
- **`$schema` URL has a date segment** that the registry updates periodically. As of 2026-05-12 we used `https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json` and it worked. If a future publish hits "invalid schema URL," run `mcp-publisher init` in a scratch directory to see the current canonical URL.

A working `server.json` template (npm/stdio shape):

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json",
  "name": "com.<your-domain>/<server-name>",
  "description": "<sentence under 100 chars>",
  "version": "0.1.0",
  "repository": {
    "url": "https://github.com/<handle>/<repo>",
    "source": "github"
  },
  "packages": [
    {
      "registryType": "npm",
      "identifier": "@<scope>/<package>",
      "version": "0.1.0",
      "transport": { "type": "stdio" }
    }
  ]
}
```

##### Where the private key lives

`~/.config/mcp-publisher/<your-domain>.key` (chmod 600). Treat it like an SSH private key:
- **Back up to 1Password / Apple Keychain** immediately after generation. If lost, you must rotate the TXT record (generate new keypair → publish new public key → wait for propagation → re-auth).
- **Never commit it** to any repo. The keypair-gen script writes it to `~/.config/...` specifically to keep it out of working trees.
- **The same key authorizes ALL future MCP registry publishes under `com.<your-domain>/*`.** You don't re-generate per server. New server name + existing key + existing TXT record = working publish.

##### Total time budget (worked 2026-05-12)

- Keypair gen: <10 seconds
- Cloudflare TXT record add + propagation: ~2 minutes
- `dig` verification: <5 seconds
- `mcp-publisher login dns`: <5 seconds
- `mcp-publisher publish`: <5 seconds
- **Total: ~3 minutes** of active work, gated on DNS propagation.

The work isn't the rate-limiter once you've done it once. Knowing which buttons to press is.

---

### Task 4 — Sanitized `agentic financial-research fleet` artifact (Phase 2 wrapper, ships Friday Week 4)

**Maps to:** Sean-Winslow-Full-Personal-Context v2.0 "Active focus" + master plan Self-Review section (recommended a second portfolio piece).

**Files:**
- Create: `vault/30_domains/finance/agentic-research-fleet/EXPLANATION.md` (sanitized 4Q)
- Create: `<personal-site>/src/pages/transactions/agentic-research-fleet.astro` (deep-dive page)
- Optional: a public GitHub repo with sanitized config + the EXPLANATION.md (no actual data sources in the repo)

**- [ ] Step 1: Sanitization pass.**
Strip every personal financial number. Generalize data sources: "a crypto market data API," "a deep-research agent," "a synthesis layer." No reference to Sean's specific portfolio decisions. Anything that smells like financial advice goes.

**- [ ] Step 2: Paste Claude-Nate-2 §2c verbatim, then sanitize.**
Source: [`claude-nate-prompt-2-analysis.md`](reference-synthesis-docs/claude-nate-prompt-2-analysis.md) §2c. The 4Q structure stays; the data-source names get genericized.

**- [ ] Step 3: Add the architecture diagram.**
Simple SVG: queue file → router → 3 retrieval agents → synthesis → daily note. No actual data, just the topology. Karpathy's "sensors + actuators" framing is the caption.

**- [ ] Step 4: Add to `/transactions/`.**

**- [ ] Step 5: Commit.**
```bash
git add vault/30_domains/finance/agentic-research-fleet/EXPLANATION.md
git commit -m "docs: add sanitized 4Q artifact for agentic financial-research fleet"
```

**Verification gate:** A reader cannot infer Sean's actual financial position from the artifact. Recruiter can understand the system's architecture in <2 minutes.

---

### Task 5 — 14-Agent Fleet Loom + Token Cost Calculator (Phase 2 wrapper, ships Friday Weeks 2 + 3)

**Maps to:** Master plan Phase 2 Task 2.4 + closes Sean's only beginner skill gap (cost economics, per both Nate-1 docs).

**Files:**
- Create: `<personal-site>/src/pages/transactions/agent-fleet-tour.astro` (Loom embed + 4Q)
- Create: `~/Code/sw-token-cost-calculator/index.html` (single-file artifact, public Vercel)
- Create: `~/Code/sw-token-cost-calculator/EXPLANATION.md`

**- [ ] Step 1: Record the 14-agent fleet Loom (Friday Week 2).**
5–7 minutes, unedited screen recording. Show: the [`agents-sdk/`](../../../../agents-sdk/) directory, the [`config.toml`](../../../../agents-sdk/config.toml), one live run of `daily_driver.py --mode morning --dry-run`, narration of the decomposition logic, narration of one failure mode (the MBP-asleep synthesizer is the obvious one). Don't polish. Per Claude-Nate-1 §7: "the transparency is the credential."

**- [ ] Step 2: Add the Loom to a `agent-fleet-tour.astro` page on the personal site.**
4Q template alongside. The 4Q answers: What is this? (an agent fleet that runs my morning, vault, and research loops). Why this approach? (decomposition by responsibility, not by tool). What would break? (MBP-asleep synthesizer; cloud cost overrun; LDR upgrades silently fall back to gemma3:12b). What did I learn? (the queue file is the entire UX; richer interfaces kill the loop).

**- [ ] Step 3: Build the token cost calculator (Friday Week 3).**
Single HTML file. Inputs: workflow steps × model per step × expected token volume × frequency. Outputs: monthly cost across Haiku/Sonnet/Opus mix + sensitivity analysis. Optionally calls Sonnet to demo a real run (use Anthropic's API in Artifacts capability). Per Claude-Nate-1 §5.5 (this is the artifact closing the cost-economics gap).

**- [ ] Step 4: Deploy to Vercel.**
Single command: `vercel --prod`. Get a public URL. Add to `/transactions/`.

**- [ ] Step 5: Commit + 4Q EXPLANATION.md.**
Pre-drafted 4Q for the calculator:
```markdown
## What is this?
A single-file HTML calculator for modeling agent-workflow token costs across Haiku / Sonnet / Opus / local-model mixes. Inputs: workflow steps, model per step, expected token volume, frequency. Outputs: monthly cost + sensitivity analysis.

## Why this approach?
A single HTML file because it's the lowest-friction artifact a recruiter can poke at — no install, no signup, no API key. Rejected: a Notion template (no live calculation), a hosted SaaS (over-engineered for v0).

## What would break?
(1) Anthropic pricing changes — the constants are hard-coded and need a quarterly refresh. (2) The "real Sonnet call to demo" path leaks the API key if not Vercel-environment-scoped. (3) Local-model cost ($0) is a placeholder that hides electricity + hardware amortization.

## What did I learn?
That cost-economics fluency is mostly about modeling the *mix*, not the per-token rate. The interesting decisions are which steps go to local Qwen3-14B vs cloud Haiku vs cloud Sonnet vs cloud Opus — and that decision is made at design time, not runtime.
```

**Verification gate:** The fleet Loom plays end-to-end without a re-shoot. The calculator returns sensible numbers for a 1k-step / 10k-token / daily workflow.

---

### Task 6 — Resolve the 9 open work items from the operating-model

**Maps to:** [Operating-model "Current Open Questions"](../../../05_atlas/operating-models/job-hunt-2026/operating-model.md) + project tracker decision log.

Each gets a concrete decision now or a deferred-to-week-N flag.

**§A — Track-C MCP cold-start chain (name → repo → README → plan).** **DECIDED THIS WEEK.** Name: `sw-mcp-intent-engineering`. Repo: `~/Code/sw-mcp-intent-engineering/` (master plan Phase 4 Task 4.2). README: master plan Phase 4 Task 4.3 Step 7 covers the structure. Plan: this roadmap's Task 3.

**§B — Agent-fleet audit verdict.** **DECIDED THIS WEEK.** Audit pass scheduled for Saturday 2026-05-09 evening (one hour, off-the-clock-but-not-job-hunt-work). Verdict criteria: anything dependent on MBP-awake → either move to Mac Mini or retire. Specifically: the Vault Synthesizer and the Knowledge Lint Tier-2 path. Migration plan target completion: 2026-05-18.

**§C — Substack voice + first-post topic.** **DECIDED THIS WEEK; AMENDED 2026-05-10.** Voice: comedic / story-driven Sean Mode (per [`writing-voice-modes`](../../../../.claude/skills/writing-voice-modes/SKILL.md), per Claude-Nate-2 Decision 4). **First post topic AMENDED:** "The Night My Vault Said Nothing" — the eval-suite discovery story. Sedaris-tuned primary draft at [`2026-05-10-the-night-my-vault-said-nothing.md`](../substack-drafts/2026-05-10-the-night-my-vault-said-nothing.md); Kerouac variant at [`2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md`](../substack-drafts/2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md). Ships Friday Week 2 (2026-05-22) alongside the eval suite (Task 8). The 14-agent fleet Loom topic is bumped to Friday Week 3 (2026-05-29) as the follow-up post arc (post-synthesizer-fix). Rationale: the eval-suite discovery is a stronger lead piece because it dramatizes the rigor (error-analysis-first) the canon insists on, AND it pairs with a shipped artifact, where the fleet Loom is a tour without a ship.

**§D — Build-in-public cadence + format.** **DECIDED THIS WEEK.** Cadence: one Substack post per Friday by 5 PM, syndicated to LinkedIn the following Wednesday. Format: ~600 words, one artifact featured, one paragraph of editorial framing, one link to the canonical `/transactions/` page. Eight posts in eight weeks.

**§E — Target list of 30 companies.** ✅ **CLOSED 2026-05-13, 5 days ahead of deadline.** Three deliverables landed in one Cowork session: (1) [`vault/20_projects/prj-job-hunt-2026/target-companies.md`](../../target-companies.md) created with 30 rows across 3 tiers (10 + 15 + 5 per master plan Phase 5 Task 5.1 schema). 16 rows pre-loaded from the 2026-05-07 Gemini DR-Max research with verbatim JD URLs, comp ranges, and DR §5 portfolio-to-role mapping; 14 rows rounded out from the [`job_feed`](../../job-feed/) watchlist (frontier labs + Larry's network). Tiers reorganized vs. DR's tenure-fit tiering — uses master plan's "yes please / would consider / safety net" framing weighted by Boston-metro + remote constraint + portfolio match. Status legend defined (`not-applied` / `applied` / `talking` / `interview` / `offer` / `passed` / `rejected` / `tbd`) plus a week-by-week application sequence drawn from DR §7. (2) [`vault/20_projects/prj-job-hunt-2026/warm-intros.md`](../../warm-intros.md) created — small file by design with Larry pre-populated for Messari (strong) + Coinbase (medium), three reusable outreach patterns (inside-contact ping / warm-intro request / reactivation message), and a LinkedIn-sweep prompt enumerating all 26 target slugs for paste-search. (3) [`vault/20_projects/prj-job-hunt-2026/job-feed/watchlist.yaml`](../../job-feed/watchlist.yaml) patched: added 5 slugs (`decagon` + `robinhood` to `ai_native`; `liberate` + `manifoldbio` + `pairteam` to `boston_metro`). 36 → 38 slugs, 6 buckets. BCG X intentionally excluded with inline comment (custom careers system, not Greenhouse/Lever/Ashby — manually tracked in target-companies.md). `python3 scripts/validate.py` → 58 warnings / 0 errors (2 cleaner than v3.30.1 baseline). **Phase 5 Task 5.2 (5 applications/week, starting Week 3 2026-05-19) is unblocked.** Sean-owned follow-ups: LinkedIn-sweep against the 26-slug prompt → prospecting queue rows in `warm-intros.md`; Tier-1 inside-contact identification per master plan Phase 5 Task 5.1 Step 2; Larry ping to confirm Messari intro is still open and ask about Coinbase brokering.

**§F — Gmail labels pipeline.** **DECIDED THIS WEEK.** Build it Saturday 2026-05-09 alongside §B. 5 labels: `Job-Hunt/Recruiter`, `Job-Hunt/Application`, `Job-Hunt/Reference`, `Job-Hunt/Network`, `Job-Hunt/Logistics`. Filters: regex on common subject lines + sender domains. Time-box: 60 min.

**§G — YouTube as a public surface, yes/no.** **DEFERRED to Week 5.** Substack + LinkedIn + GitHub is enough for the 8-week sprint. The Loom artifacts already double as YouTube candidates if Sean wants to upload them; uploading is 5 min once the Loom exists. Don't make it a channel decision until at least 3 Looms exist.

**§H — Second portfolio artifact (after MCP v0).** **DECIDED THIS WEEK.** The June 11 animation pipeline + production diary is the second flagship artifact (ChatGPT-Nate-2 §4 "By June 11"). Already on the master plan as a non-negotiable creative deadline. The 4Q draft is Claude-Nate-2 §2d.

**§I — Agent Evals fluency.** ~~**DECIDED — this is the Week 5 deep-work focus.** Read Hamel Husain's evals canon (1.5 hours), one Anthropic engineering post on evals (30 min), then build a small `evals/` directory in the Superuser Pack with 10–15 cases for the vault synthesizer. Don't over-scope this — the goal is fluency, not a published eval framework. The published version becomes a Week-7 artifact if there's time.~~ **AMENDED 2026-05-10: UPGRADED FROM FLUENCY-ONLY TO PLANNED SHIP.** Reading + research already done (Anthropic [`Demystifying Evals`](../../../../40_knowledge/references/ref-anthropic-demystifying-agent-evals.md), Gemini DR + Perplexity primers at [`vault/20_projects/research/2026-05-09-*-ai-eval-fluency-primer-and-reference-cases.md`](../../research/)). Step-0 error analysis on real synthesizer logs already done at [`2026-05-10-evals-error-analysis-real-logs.md`](2026-05-10-evals-error-analysis-real-logs.md) — surfaced a 9-day live silent regression in the synthesizer that reshaped the eval scope. Full build plan at [`2026-05-10-eval-suite-build-plan.md`](2026-05-10-eval-suite-build-plan.md) is ready for Claude Code + `obra/superpowers` Plan Mode execution. This becomes **Task 8** below — shipped Friday Week 2 as the 6th flagship portfolio artifact.

**§J — Enterprise-build patterns.** **DEFERRED to Week 6+.** This is interview-prep territory, not a build-track item. When an interview lands, the relevant patterns get studied for that loop's prep block (master plan Phase 6 Task 6.1). Don't try to learn enterprise patterns in the abstract.

---

### Task 8 — Vault Synthesizer Eval Suite (NEW 2026-05-10 — ships Friday Week 2, 2026-05-22)

> **Status:** Step 0 (error analysis) ✅ complete 2026-05-10. Substack drafts ✅ complete (Sedaris primary + Kerouac variant). Build plan ✅ at [`2026-05-10-eval-suite-build-plan.md`](2026-05-10-eval-suite-build-plan.md). **Workstream A code shipped ✅ 2026-05-12** at [`evals/vault-synthesizer/`](../../../../evals/vault-synthesizer/) — branch `eval-suite-2026-05-12`. **Workstream B synthesizer patches shipped ✅ 2026-05-12** — suite at 7/10 post-fix (up from 1/10 pre-fix baseline). **Workstream C (Substack-Drafter agent) code shipped ✅ 2026-05-12** — C0-C8 + C10 complete; C9 (supervised pilot drafts) gated on B7. **Pushover keychain credentials added ✅ 2026-05-12** (Sean confirmed via `security add-generic-password` for `com.sean.agents.pushover_user_key` + `com.sean.agents.pushover_api_token`) — operator-action requirement for the new boot check is satisfied; live synthesizer will not fail at boot after merge. **Branch is merge-ready:** 32 commits total, all tests passing (504 unit tests + 33 substack_drafter tests + 7/10 eval suite), CHANGELOG/CLAUDE/README updated to v3.33.0. A13 (Loom) + A14 (Substack publish 2026-05-22) + C9 (3 pilot drafts after B7 gate closes) + B7 itself (5-night live-synth verification window) all remain in Sean's hands as calendar-time tasks.

**Maps to:** Master plan Phase 2 Task 2.4 (publish what already exists) + this roadmap's Task 6 §I (now upgraded to planned ship) + Karpathy synthesis Claim D (eval design as underbuilt next-frontier portfolio piece).

**Why this was unscoped originally and why it ships now:** The unified roadmap (2026-05-06) deferred eval publication to "Week 7 if there's time." Three things changed between 2026-05-06 and 2026-05-10: (1) the Gemini DR + Perplexity research primers delivered 15 pre-drafted YAML cases, eliminating the unknown-unknowns time cost; (2) doing the error-analysis-first step on real synthesizer logs surfaced a 9-day live silent regression — the failure mode the eval catches is no longer hypothetical, it's a real bug the suite would have caught on day one; (3) the resulting artifact is dramatically more interview-grade because it's grounded in a specific observed failure with a clear narrative arc, not a generic library of cases.

**Files (per build plan):**
- Create: `evals/vault-synthesizer/{README,cases.yaml,deferred-cases.yaml,runner.py,failure-modes.md,EXPLANATION.md,references.md}` + `traces/coded-traces.md`
- Modify: [`CHANGELOG.md`](../../../../CHANGELOG.md), [`CLAUDE.md`](../../../../CLAUDE.md), [`README.md`](../../../../README.md) — count updates per mandatory doc rule

**- [x] Step 0: Error analysis on real production logs.** ✅ Complete 2026-05-10 at [`2026-05-10-evals-error-analysis-real-logs.md`](2026-05-10-evals-error-analysis-real-logs.md). Six-mode failure taxonomy grounded in 17 days of synthesizer logs + stderr. Surfaced the silent-regression discovery that reshaped the eval scope.

**- [x] Step 1: Substack drafts in 2 voice modes.** ✅ Complete 2026-05-10. Sedaris primary at [`2026-05-10-the-night-my-vault-said-nothing.md`](../substack-drafts/2026-05-10-the-night-my-vault-said-nothing.md); Kerouac variant at [`2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md`](../substack-drafts/2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md).

**- [x] Step 2: Bring [`2026-05-10-eval-suite-build-plan.md`](2026-05-10-eval-suite-build-plan.md) into Claude Code + `obra/superpowers` Plan Mode.** Plan Mode produces execution graph from the build plan's Phases 0–7. Review, approve, execute phase-by-phase with verification gates. ✅ Complete 2026-05-12. 23 commits on branch `eval-suite-2026-05-12`. Build plan executed via `subagent-driven-development` skill: A0 (Phase 0 reads) → A0.5 (spike) → A1-A12 (scaffolding through doc updates). 10 cases load; runner.py is ~210 lines with conftest.py providing the agents-sdk import path; fixtures cover 6 mock notes + 3 concept stubs + index parity. CHANGELOG/CLAUDE/README updated per non-negotiable rule (v3.30.1).

**- [x] Step 3: Synthesizer fix (between Friday Week 2 and Friday Week 3).** Patch [`agents-sdk/agents/vault_synthesizer.py`](../../../../agents-sdk/agents/vault_synthesizer.py) status taxonomy + per-file exception promotion + `model_used` enum + Pushover credential health check + Daily Driver brief consumer warning path. Per build-plan Part A Phase 2. ✅ Complete 2026-05-12. Workstream B turned 6 cases green in 5 commits — B1 (model_used enum: `58c23ff`), B2 (run-level status promotion incl. partial-empty taxonomy: `79598f8`), B4 (Pushover boot-time credential check: `b88d56f`), B5 (daily-driver Vault Health WARNING render: `6dda2d9`), B6 (skip_reason refresh for vs-012/013: `2b9f59c`). All 38 existing synthesizer/pushover/daily_driver unit tests still pass; two tests were legitimately updated to assert the corrected post-fix behavior.

**- [ ] Step 4: Re-run eval suite against live patched synthesizer for 5 consecutive nights.** 5-night gate window opens 2026-05-12; earliest close 2026-05-17, realistic close 2026-05-26+. Target: `concepts_written > 0` on 5 consecutive `vault/health/synth-manifest-*.json` files AND 7+/10 on the suite each morning. Once gate closes, publish the "vault said something again" follow-up post 2026-05-29 (voice TBD per Decision 4 amendment). vs-014/012/013 remain explicitly skipped pending live-LLM infra (vs-014) and runner-path follow-ups (vs-012, vs-013). Workstream C does not depend on this gate closing — it ships default-disabled per kill-switch design.

**Execution log (2026-05-12) — FINAL:**
- **Workstream A (14 commits):** `dc90f7e` plan ingest → `783bc31` CHANGELOG/CLAUDE/README at v3.30.1. Files at `evals/vault-synthesizer/`: cases.yaml (10 cases), deferred-cases.yaml (11 cases), runner.py (~210 lines), conftest.py, failure-modes.md, EXPLANATION.md, README.md, references.md, last-run.md (auto-generated), traces/{phase-0-reads.md, phase-0.5-spike.md, baseline-run-2026-05-12.md, coded-traces.md, fixtures/}.
- **Workstream B (8 commits):** `58c23ff` model_used → `2b9f59c` skip_reason refresh. Synthesizer patches at `agents-sdk/agents/vault_synthesizer.py` (`STATUS_*` constants, `MODEL_USED_VALUES` frozenset, `_normalize_model_name`, files_attempted/succeeded counters, end-of-loop status promotion). Pushover boot check at `agents-sdk/lib/pushover.py` (`PushoverConfigurationError` + `ensure_credentials_or_raise`). Daily-driver helper at `agents-sdk/agents/daily_driver.py` (`render_vault_health` standalone, wired into `build_preamble`). All 38 existing synthesizer/pushover/daily_driver unit tests still pass; two legitimately updated to assert post-fix corrected behavior.
- **Workstream C (10 commits):** `b1775cb` [substack_drafter] config table → `37b5fde` CHANGELOG/CLAUDE/README at v3.33.0. New agent at `agents-sdk/agents/substack_drafter.py` (~370 lines: voice rotation, dryness gate, cluster picker, prompt composer, HybridRouter wrapper, draft writer, main + CLI). 33 TDD tests in `agents-sdk/tests/test_substack_drafter.py`. launchd plist at `agents-sdk/schedules/com.sean.agents.substack_drafter.plist` (Thursday 18:00, opt-in via `INSTALL_SUBSTACK_DRAFTER=1`). `_route()` wired to real HybridRouter via httpx (ollama `/api/generate` + OpenAI-compatible `/v1/chat/completions` branches). Three kill-switch layers: config flag, launchd opt-in, `--dry-run` CLI.
- **vs-014 skip rationale (decided 2026-05-12):** The output-completeness case (`concepts_written >= 1`) cannot be faithfully exercised with the offline runner. Mocking it to pass would test the formatter, not the synthesizer. Adding a hardcoded "valid concept" mock dict introduces a fake green that doesn't catch the regression the case was designed for. Honest deferral preserves the case as a real regression target for Workstream C's live-run tier. Final ship state: 7 PASS / 0 FAIL / 3 SKIP. Every skip has a `skip_reason` field naming the actual blocker.
- **Pushover keychain (operator action, 2026-05-12):** Sean added `com.sean.agents.pushover_user_key` + `com.sean.agents.pushover_api_token` to the macOS keychain. The Workstream B boot check now finds creds at synthesizer startup and proceeds normally. Without this, the live nightly synthesizer would have failed at boot every night — which is the correct vs-019 behavior, but operator-action was required to unblock the live system after merge.
- **Suite is reproducibly green at 7/10 across 5+ runs.** `last-run.md` autogenerates on every pytest invocation via the hooks in `evals/vault-synthesizer/conftest.py`.

**Verification gate:** 2026-05-22 ship. Eval suite directory exists with 7 files + 1 traces directory. `python evals/vault-synthesizer/runner.py` runs without infra errors. `EXPLANATION.md` is recruiter-readable cold in <90 seconds. Loom plays (5 min, unedited). Substack post syndicates the Sedaris draft. This is the **6th flagship portfolio artifact**, slotting between Intent-Engineering MCP (5/25) and Animation Pipeline (6/11).

---

### Task 9 — Substack-Drafter Agent (NEW 2026-05-10 — EARLY-BUILD APPROVED 2026-05-12)

> **Status:** Workstream C build approved 2026-05-12 ahead of original "post-employment" schedule. Hard precondition is Task 8 Step 4's 5-night gate (`concepts_written > 0` on 5 consecutive synth manifests), NOT employment status — once the gate closes, the agent has real concept articles to draft from. Default-disabled at three kill-switch layers (config flag, opt-in launchd install via `INSTALL_SUBSTACK_DRAFTER=1`, `--dry-run` flag) so the worst case is a draft sitting in the vault that Sean never reads. Becomes the 7th flagship portfolio artifact when it ships. Lives at `agents-sdk/agents/substack_drafter.py` — design doc at [`2026-05-10-eval-suite-build-plan.md`](2026-05-10-eval-suite-build-plan.md) Part B.

**Maps to:** Operating-model Tier-A truth "agents draft / Sean sends" + Claim G from Part 1 synthesis (live demonstration as non-fakeable interview asset) + Task 9 closes the publishing-cadence loop that Tasks 5 + 6 §D + Task 8 establish.

**Why early-build approved 2026-05-12:** The original "post-employment" framing was a constraint on Sean's time, not on the agent's design. The agent's real precondition is technical: the synthesizer must be alive and producing concept articles for the agent to have anything to draft from. That precondition is gated by Workstream B's 5-night live verification — not employment status. Once that gate closes, the agent makes the publishing cadence agent-assisted instead of hand-written, which is the rate-limiting step on the publishing strategy that drives the job hunt. Three kill-switch layers (default-disabled config flag, opt-in launchd install, `--dry-run` flag) preserve safety: the worst-case if something goes wrong is a draft file sitting in the vault that Sean never reads. The original spec (line 631-650 below) is unchanged.

**Files (per build plan Part B):**
- Create: `agents-sdk/agents/substack_drafter.py`
- Create: `agents-sdk/schedules/com.sean.substack-drafter.plist`
- Modify: [`agents-sdk/config.toml`](../../../../agents-sdk/config.toml) — `[substack_drafter]` table, default `enabled = false`
- Modify: [`agents-sdk/schedules/install_schedules.sh`](../../../../agents-sdk/schedules/install_schedules.sh) — `INSTALL_SUBSTACK_DRAFTER=1` opt-in flag

**Behavior summary:**
1. Schedule: Thursday 18:00 weekly (gives Friday morning for review + publish)
2. Default: disabled. Opt-in via env flag at install time.
3. Reads: last 7 synth-manifests + last 14 days of `vault/knowledge/concepts/`, `connections/`, `qa/` + similarity-matched references from `vault/40_knowledge/` and `vault/20_projects/research/`
4. Voice mode rotates on a 5-week cycle through Sedaris / Kerouac / Thompson / Vonnegut / Sean Mode (per [`writing-voice-modes`](../../../../.claude/skills/writing-voice-modes/SKILL.md))
5. Cost cap: $0.10/run hard
6. Output: draft markdown in `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/YYYY-MM-DD-agent-draft-{slug}.md`
7. Never publishes autonomously. Pushover ping informs Sean a draft is ready.
8. Graceful no-op when synthesizer has been dry for 3+ nights.

**Tier-A check:** Walk-away $100k N/A. AI-PM track ✅ (this is a canonical "build agents that close your own loops" demonstration). Agents draft / Sean sends ✅ explicit. Track-C protected ✅ (post-employment). 5:30 PM hard stop ✅ (agent runs on its own schedule).

**Verification gate (when implementing):** dry-run prints complete prompt; real run produces a draft file with valid frontmatter; voice mode is recognizable in 2/3 sanity-check drafts; cost <$0.10 across 5 real runs; graceful no-op when synthesizer dry; one-command disable works.

**Pre-shipping risk:** None. Spec exists. Nothing on the critical path depends on this agent shipping inside the 8-week sprint.

**Execution status (2026-05-12) — FINAL:**
- **Branch:** `eval-suite-2026-05-12` (32 commits total: Workstream A's 14 + Workstream B's 8 + Workstream C's 10).
- **Code complete:** C0 (preconditions check) ✅, C1 (`[substack_drafter]` config table) ✅, C2 (voice-rotation module, 8 tests) ✅, C3 (synthesizer-dryness gate, 7 tests) ✅, C4 (wikilink-density cluster picker, 5 tests) ✅, C5 (prompt composer with voice-skill injection + graceful degradation, 5 tests) ✅, C6 (`_route()` wired to real HybridRouter + `write_draft()` with frontmatter, 3 tests) ✅, C7 (`main()` + `--dry-run` + `_cli()` wrapper, 5 tests) ✅, C8 (launchd plist + `INSTALL_SUBSTACK_DRAFTER=1` opt-in install, plutil-lint clean) ✅, C10 (CHANGELOG/CLAUDE/README at v3.33.0) ✅.
- **C9 (pilot drafts) pending:** Gated on B7's 5-night gate closing so `vault/knowledge/concepts/` has real concept articles to draft from. Plan: flip `enabled = true` in config.toml → run `python3 agents/substack_drafter.py --dry-run` → run real → repeat 2x with `--voice sedaris` and `--voice vonnegut` → Sean reads each draft cold → if all 3 publishable-with-edits, `INSTALL_SUBSTACK_DRAFTER=1 ./agents-sdk/schedules/install_schedules.sh` installs the launchd plist for Thursday-18:00 weekly cadence.
- **Kill-switch verification:** CLI smoke-tested 2026-05-12 against the live vault. With `enabled = false` (current default), output is: `[substack_drafter] disabled in config.toml — exit 0 (set enabled = true to opt in)`. Kill-switch layer 1 works correctly.

---

### Task 10 — `vault-knowledge-mcp` (NEW 2026-05-13 — research-pending; 8th flagship artifact)

> **Status:** Build spec + deep-research prompt scaffold at [`2026-05-13-vault-knowledge-mcp-spec.md`](2026-05-13-vault-knowledge-mcp-spec.md). **No code written yet.** Deep research must return before architecture is locked. Expected DR run: Gemini DR-Max, ~$7 cost cap (within `agents-sdk/config.toml` Gemini Researcher governor). Expected research-return file: `vault/20_projects/research/2026-05-XX-vault-knowledge-mcp-research.md`.

**Maps to:** Karpathy synthesis Claim B ("MCP servers are the portable career artifact for 2026") + [[2026-05-07-target-role-specs]] §3 Anthropic FDE (literal JD ask for "MCP servers, sub-agents, agent skills") + unified roadmap Decision 1 follow-on ("two MCPs of different shapes proves the pattern is repeatable").

**Why this exists in addition to `intent-engineering`:** `intent-engineering` wraps a *skill*. `vault-knowledge-mcp` wraps a *knowledge graph with typed reasoning edges over a 17-day production-grounded vault*. Different shapes of the same primitive. Two shipped MCPs of meaningfully different shapes is the load-bearing differentiator over candidates with one or zero. Also: Phase D + Phase 6 work currently has no customer-facing surface — this MCP makes the `concept_edges` table and the synthesizer output interactively queryable from any MCP-aware client.

**Spec-level decisions already in:**
- Three tools: `search_concepts(query, limit)`, `find_contradictions(scope)`, `get_article(slug)`
- Stdio transport, TypeScript SDK 1.29.0, Node 22, MIT
- Reuses DNS-verified `com.seanwinslow/*` namespace + the Ed25519 publish key from `intent-engineering`
- npm: `@swins/vault-knowledge-mcp@0.1.0`; MCP registry: `com.seanwinslow/vault-knowledge@0.1.0`
- Read-only, local-vault, no auth, no SaaS

**Spec-level decisions OPEN — answered by deep research:**
- Embedding strategy: JS-native (Transformers.js / ONNX Runtime Web) vs. Python sidecar over the existing nomic-embed-text Ollama pipeline
- State management: read Sean's existing `vault/.vault-index.db` vs. own embedding index
- Privacy boundary: allowlist by directory vs. blocklist vs. env-var-based
- Naming: `vault-knowledge-mcp` vs. `vault-graph-mcp` vs. `comprehension-mcp` vs. `knowledge-edges-mcp`
- Tool surface count: 3 vs. 6 (one per relation type in the typed-edges schema)
- License + IP boundary: ship a public demo vault, or "bring your own vault"?

**Files (post-research):**
- Create: `~/Code-Brain/sw-mcp-vault-knowledge/` (new repo)
- Create: `~/Code-Brain/sw-mcp-vault-knowledge/docs/EXPLANATION.md` (4Q artifact)
- Modify: [`CHANGELOG.md`](../../../../CHANGELOG.md), [`CLAUDE.md`](../../../../CLAUDE.md), [`README.md`](../../../../README.md) — count updates

**- [x] Step 0: Spec + research prompt drafted.** ✅ 2026-05-13 — see [`2026-05-13-vault-knowledge-mcp-spec.md`](2026-05-13-vault-knowledge-mcp-spec.md).

**- [ ] Step 1: Run Gemini DR-Max with the §12 research prompt.** Output lands at `vault/20_projects/research/2026-05-XX-vault-knowledge-mcp-research.md`. Cost cap: $7.

**- [ ] Step 2: Review DR results, lock the 6 open architectural decisions.** Update the spec's frontmatter `status` from `research-pending` → `research-complete`. Append a `## Scope-Lock` section to the spec capturing each locked decision.

**- [ ] Step 3: Execute the build per the locked spec.** Mirror `intent-engineering`'s 5-phase build (scaffold → 3 real tools → hardening → publish → launch comms). Reuse the publish flow frozen in this roadmap's "Publish + registry flow — frozen reference" subsection.

**- [ ] Step 4: Ship.** npm publish + MCP registry publish + README + 4Q `EXPLANATION.md` + 90-sec Loom + LinkedIn announcement tagging Anthropic + MCP team.

**Verification gate:** 10 binary success criteria in the spec §8. Earliest start: Mon 2026-05-19 (post-research). Ship target: 2026-05-28 to 2026-06-04. Tier-A protected — slips do not block Track-C, animation pipeline (6/11), or eval suite Loom (5/22).

---

### Task 11 — Agent Fleet Observability Dashboard (NEW 2026-05-13 — **v1 CODE COMPLETE 2026-05-17 evening**; 3rd supporting artifact)

> **Status:** **v1 CODE COMPLETE 2026-05-17 (evening).** Repo: [`github.com/seanwinslow28/agent-fleet-observability`](https://github.com/seanwinslow28/agent-fleet-observability) (public). Working tree: `~/Code-Brain/agent-fleet-observability/`. **26 commits across 33 plan tasks** (32 from plan + 1 NEW Task 8b for §4d live-wire). **55/55 pytest tests pass; ruff clean.** Build wall-time **85ms** (budget: <60s). Page weight **public 32KB / private 41KB** (budget: <200KB). 9 of 15 design-doc §9 success criteria verified locally; remaining 6 gate on Sean's hands-on deploy + Loom (~30 min total). **Brainstorm + design + plan triad lives at:** [`2026-05-15-agent-fleet-dashboard-design.md`](2026-05-15-agent-fleet-dashboard-design.md) (locked design), [`2026-05-15-agent-fleet-dashboard-plan.md`](2026-05-15-agent-fleet-dashboard-plan.md) (4424-line execution script), [`vault/90_system/auto-memory/project_agent_fleet_dashboard_kanban_v2.md`](../../../../90_system/auto-memory/project_agent_fleet_dashboard_kanban_v2.md) (kanban v2 write-back deferral). The original [`2026-05-13-agent-fleet-dashboard-spec.md`](2026-05-13-agent-fleet-dashboard-spec.md) is superseded by the 5/15 design doc but kept for the research-prompt trail.

**Maps to:** Karpathy synthesis ("$20B 2026 funding for eval/agent-ops platforms") + ChatGPT-Nate-1 Agent Ops/FDP backup track + Claim F (cost economics as Sean's one beginner skill — closed by lived telemetry, not a separate calculator) + this roadmap's Decision 3 (backup track = Agent Ops / FDP).

**Why this exists:** Sean operates a real multi-agent fleet with real instrumentation (`agent-run-history.csv`, `synth-manifest-*.json`, `gemini-spend-*.json`, `evals/vault-synthesizer/last-run.md`, `.job-feed.db`, plus job-hunt trackers `target-companies.md` + `warm-intros.md`), but recruiters won't clone the repo to verify the claim. The dashboard converts "trust the repo" to "look at the screen for 30 seconds." Visually: 8 fleet tiles, cost trend stacked area, model mix donut, 60-night synthesizer telemetry line with the 2026-05-01 → 2026-05-10 silent regression explicitly annotated, eval case grid, recent-runs table, kanban board with live-pulse on currently-running tickets.

**Three locked decisions (Sean 2026-05-16, in flight during build):**
- **Inline SVG for every chart.** Chart.js + Grid.js dropped entirely. Page-weight discipline, deterministic build output, no CDN race on cold-cache load, charts survive screenshots. Helpers at [`lib/svg_charts.py`](../../../../../agent-fleet-observability/lib/svg_charts.py) (line_chart with annotation, sparkline, donut, stacked_area).
- **Combined `lib/render.py` over separate public/private files.** Both passes share ~90% of logic; only difference is one `anonymize.public_pass()` call before render. DRY beats the design doc's two-file split.
- **"Multi-agent fleet" not "8-agent".** Description, footer, README all drop hardcoded counts — fleet grows over time.

**§4d live-wire (NEW Task 8b per Sean's 2026-05-16 decision, option 1 of 3):** original design doc punted §4d job-hunt panels to Sean-voice empty-state because `vault/.job-feed.db` lacks the schema for them. Mac Mini pre-flight surfaced two companion markdown trackers Sean maintains — [`vault/20_projects/prj-job-hunt-2026/target-companies.md`](../../target-companies.md) (Strategic 30 table) + [`vault/20_projects/prj-job-hunt-2026/warm-intros.md`](../../warm-intros.md) (Active/Prospecting/2nd-degree tables). Added 2 new readers (`read_target_companies` + `read_warm_intros`) + 1 helper (`_parse_pipe_table`) + 5 TDD tests. Private below-fold renders Tier-1/2/3 counts + by-status breakdown + Tier-1 company list + warm-intro active table LIVE; `anonymize.public_pass` zeros both for public. Privacy boundary verified: 0 occurrences of `Larry`/`Anthropic`/`Messari`/`vault/.job-feed` in public output.

**Architecture (what shipped):**
```
Mac Mini cron (06:00 ET) → build.py
  ├─ Read vault data (12 readers: CSV/JSON/SQLite/Markdown, incl. target-companies + warm-intros)
  ├─ Aggregate (compute_all: fleet_status / KPIs / 60d synth series / regression window / cost trend / model mix)
  ├─ Compose kanban tickets (5 sources: research/lint/eval/manual/feed)
  └─ Render two passes:
     ├─ render_public(agg, tickets, REPO)  → strips job-hunt + redacts vault paths → git push → Vercel
     └─ render_private(agg, tickets, ~/Sites/agent-fleet-private/)  → full data, file:// bookmark
```

**Files in the new repo** (~1,200 lines incl. tests):
- [`build.py`](../../../../../agent-fleet-observability/build.py) — orchestrator (--dry-run / --no-push flags, $0/run, 85ms wall-time)
- [`lib/readers.py`](../../../../../agent-fleet-observability/lib/readers.py) — 12 reader functions
- [`lib/aggregations.py`](../../../../../agent-fleet-observability/lib/aggregations.py) — 9 aggregations + `compute_all` entry
- [`lib/anonymize.py`](../../../../../agent-fleet-observability/lib/anonymize.py) — `public_pass` (zero job_feed + target_companies + warm_intros, redact vault paths)
- [`lib/svg_charts.py`](../../../../../agent-fleet-observability/lib/svg_charts.py) — 4 SVG helpers + palette constants
- [`lib/kanban.py`](../../../../../agent-fleet-observability/lib/kanban.py) — `compose_tickets` + `compute_columns` (10-min `RUNNING_WINDOW` for live-pulse)
- [`lib/render.py`](../../../../../agent-fleet-observability/lib/render.py) — `render_public` + `render_private` (LOCKED DEVIATION from design §6a's two-file split)
- [`templates/`](../../../../../agent-fleet-observability/templates/) — `base.html` + `fleet.html` + `kanban.html` + 8 partials (mascot, topbar, footer, agent_grid, kpi_row, hero_regression, below_fold_public, below_fold_private, alerts_banner, kanban_board)
- [`assets/styles.css`](../../../../../agent-fleet-observability/assets/styles.css) — 235 lines (palette + mascot + responsive + kanban + live-pulse, `prefers-reduced-motion` honored)
- [`assets/kanban-filter.js`](../../../../../agent-fleet-observability/assets/kanban-filter.js) — vanilla JS chip toggle
- [`schedules/com.sean.agent-fleet-dashboard.plist`](../../../../../agent-fleet-observability/schedules/com.sean.agent-fleet-dashboard.plist) — launchd template (06:00 ET daily, PATH env per CLAUDE.md requirement)
- [`vercel.json`](../../../../../agent-fleet-observability/vercel.json) — static deploy config (24h immutable cache on /assets/, 5min cache on /(index|kanban).html)
- [`README.md`](../../../../../agent-fleet-observability/README.md) — 4Q recruiter-friendly format

**- [x] Step 0: Spec + research prompt drafted.** ✅ 2026-05-13 — original spec [`2026-05-13-agent-fleet-dashboard-spec.md`](2026-05-13-agent-fleet-dashboard-spec.md).

**- [x] Step 1: Deep research returned.** ✅ Gemini DR + ChatGPT DR returns synthesized into the 5/15 brainstorming session (see design doc references).

**- [x] Step 2: Brainstorm + design lock.** ✅ 2026-05-15 — [`2026-05-15-agent-fleet-dashboard-design.md`](2026-05-15-agent-fleet-dashboard-design.md) supersedes the 5/13 spec; kanban v2 deferred per [`vault/90_system/auto-memory/project_agent_fleet_dashboard_kanban_v2.md`](../../../../90_system/auto-memory/project_agent_fleet_dashboard_kanban_v2.md).

**- [x] Step 3: Implementation plan written.** ✅ 2026-05-15 — [`2026-05-15-agent-fleet-dashboard-plan.md`](2026-05-15-agent-fleet-dashboard-plan.md) (4424 lines, 32 tasks).

**- [x] Step 4: Build executed via `subagent-driven-development`.** ✅ 2026-05-17 evening — 33 commits across 33 tasks (32 from plan + Task 8b NEW). 55/55 tests, ruff clean. Privacy boundary smoke-tested (0 public leaks of private data). Build wall-time 85ms.

**- [ ] Step 5: Sean-owned deploy (≈30 min, hands-on):**
1. `npm i -g vercel && cd ~/Code-Brain/agent-fleet-observability && vercel login && vercel link && vercel deploy --prod`
2. Cloudflare DNS: add CNAME `fleet` → `cname.vercel-dns.com`, **DNS-only / gray cloud OFF** (orange cloud breaks Vercel SSL)
3. Cron install: `cp ~/Code-Brain/agent-fleet-observability/schedules/com.sean.agent-fleet-dashboard.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.sean.agent-fleet-dashboard.plist`
4. First real snapshot commit: `cd ~/Code-Brain/agent-fleet-observability && git add index.html kanban.html data.json && git commit -m "snapshot $(date -u +%Y-%m-%dT%H:%M:%SZ)" && git push`
5. iPhone-shaped (375×~2400) screenshot of `https://fleet.seanwinslow.com` for Substack post 2 hero
6. 60-sec Loom walkthrough (hero → KPI row → agent grid → kanban → footer); drop URL in [`distribution-assets.md`](distribution-assets.md) under a new "Agent Fleet Dashboard" section

**- [ ] Step 6: Substack post 2 ("Vault said something again") ships with the dashboard as visual hero.** Target: Friday 2026-05-29 or the following Friday, depending on B7 gate timing (synthesizer needs 5 consecutive nights of `concepts_written > 0` for the post's "recovery" claim to be live-data-backed).

**- [ ] Step 7: Recruiter attribution slot.** Per design §9 criterion #10 — add `## Agent Fleet Dashboard mentions` heading to [`target-companies.md`](../../target-companies.md) (empty for now; track as engagement happens).

**Verification gate** (design §9, 15 criteria): **9/15 verified locally** (page-weight <200KB, all 8 tiles real data, regression hero visible+annotated, privacy boundary holds, mascot CSS present, build<60s, kanban ≥1 ticket per source, prefers-reduced-motion freezes mascot, full pytest 55/55). **6/15 gate on Step 5 above** (cold-cache TTFB <2s, mobile 375px survives, 30-sec recruiter cold-open, README <90-sec readability, 60-sec Loom, recruiter attribution). Tier-A protected — slips do not block Track-C, Task 10, animation pipeline (6/11).

**Compounding payoff:** Becomes the telemetry consumer for Task 12 (Judge Layer judge-outcome distribution + judge-availability panels) and Task 14 (Authority/Recovery/Audit control-plane dashboard upgrade). Pairs with Substack post 2 as visual hero. Operational evidence for the Agent Ops / FDP backup track. Kanban v2 (interactive drag-to-reassign + agent write-back) is its own post-v1 portfolio artifact — gated on 1+ recruiter engagement attributed to v1 OR 4+ weeks live, whichever first.

---

### Task 12 — Judge Layer Retrofit on Substack-Drafter (Council Gap-Fill 1; NEW 2026-05-16 — ship target 2026-06-04)

> **Status:** Not started. Hard precondition is Task 8 Workstream B7 gate closure (5 consecutive nights of `concepts_written > 0` in synth-manifests). Earliest start: **Mon 2026-05-26**, post-Substack-post-1 ship (Fri 2026-05-22) and during the Week-2 council-sequenced slot. Ship target: 2026-06-04 (≤9 days, chairman's day-by-day estimate). Becomes the 9th flagship portfolio artifact when it ships. **This is the council's single highest-leverage piece** — the conversion from "I have agents" to "I run actors inside a control architecture."

**Maps to:** Council Gap-Fill 1 + Anthropic FDE Boston JD verbatim ("control architectures around production agent deployments") + operating-model Tier-A truth "agents draft / Sean sends" (preserved as defense-in-depth, not replaced) + this roadmap's Task 9 (Substack-Drafter Workstream C, the wrap target) + future inputs to Task 11 Agent Fleet Dashboard (judge-outcome distribution + judge-availability metric panels).

**Why this is the council's #1 pick (unanimous across 4 panelists):** Sean's stack ships, intercepts, and audits — but framed as "cost discipline" and "agent boundaries," not as **control architecture**. The judge layer is the one missing piece of named architecture between "interesting candidate" and "Tier-1 must-talk." Per chairman synthesis: *Opus 4.7 named this "the single most direct match between Nate's corpus and the Anthropic FDE Boston JD." GPT-5.5 framed it as the move that converts Sean from "I have agents" to "I run actors inside a control architecture." Grok 4.20 noted it short-circuits Sierra/Decagon agent PM loops verbatim. Gemini Pro added the crucial constraint: intercept, don't rebuild — wrap the already-code-complete Substack-Drafter rather than retrofit all 8 actors.*

**Architecture (4 decisions locked 2026-05-16):**
- **A — Scope:** Substack-Drafter ONLY. Daily-Driver + Job-Feed wraps come for free in a future gap-fill as additive policy YAML + ActionProposal subclasses (no module rewrites). Vault-Synthesizer + future "vault-to-build" agent are explicit expansion candidates — see **Compounding payoff** below.
- **B — Pydantic `ActionProposal` schema in the MVP (not deferred):** Full 8-field schema from day 1 (`intended_action`, `target_surface`, `evidence_used` optional, `authorization_basis`, `expected_consequence`, `rollback_path` optional, `exposure_level`, `human_review_required`). The schema **is** the portfolio artifact; it's what makes "ActionProposal" the load-bearing demo phrase.
- **C — Fail-mode:** Fail-open with Pushover alert + `JUDGE_UNAVAILABLE` ledger entry. Cadence preservation wins over the theoretical bypass risk because Sean's manual publish gate remains the Tier-A canonical control — the judge here is defense-in-depth, not the only review surface.
- **D — Ledger location: `vault/health/judge_log/`** (NOT `vault/agents/judge_log/` per the council brief's literal pick). Consistency with the existing telemetry pattern (`synth-manifest-{date}.json`, `gemini-spend-{month}.json`, `council-spend-*.json`); the Task 11 dashboard's data loader doesn't need a new path; better for the "control-plane dashboard" framing in Gap-Fill 4 (which depends on this gap-fill's ledger as the telemetry source).
- **E — Demo trigger: `--demo-injection` CLI flag.** Injects a synthetic prompt fragment forcing the actor to fabricate a quote attributed to a real-but-archived employer figure, making the `Revise` outcome reproducible for the Loom take while keeping the judge's response real model behavior. Production runs never see the flag.

**Files (NEW + MODIFY):**
- Create: `agents-sdk/lib/judge/__init__.py` (module exports)
- Create: `agents-sdk/lib/judge/schema.py` (Pydantic `ActionProposal` + `Outcome` enum: `ALLOW` / `BLOCK` / `REVISE` / `ESCALATE` / `JUDGE_UNAVAILABLE`)
- Create: `agents-sdk/lib/judge/judge.py` (the `evaluate(proposal, policy) -> JudgeDecision` function)
- Create: `agents-sdk/lib/judge/policy.py` (YAML policy loader + validator)
- Create: `agents-sdk/lib/judge/ledger.py` (JSONL writer with atomic FileLock, mirrors `vault/health/*-spend-*.json` pattern)
- Create: `agents-sdk/policies/substack_drafter.yaml` (declarative policy: no autonomous publishing, escalate on unprovenanced claims about named people, revise on voice/tone violations, allow only local draft-file creation)
- Create: `agents-sdk/lib/judge/EXPLANATION.md` (4Q artifact — auto-feeds the ledger row in Gap-Fill 3's content collection)
- Create: `agents-sdk/tests/test_judge_schema.py`, `test_judge_evaluate.py`, `test_judge_policy.py`, `test_judge_ledger.py`, `test_substack_drafter_judge_integration.py`
- Create: `vault/health/judge_log/.gitkeep`
- Modify: [`agents-sdk/agents/substack_drafter.py`](../../../../agents-sdk/agents/substack_drafter.py) — wire `judge.evaluate()` between [`_route()` line 237](../../../../agents-sdk/agents/substack_drafter.py#L237) and [`write_draft()` line 445](../../../../agents-sdk/agents/substack_drafter.py#L445); add `--demo-injection` flag to [`_cli()` line 404](../../../../agents-sdk/agents/substack_drafter.py#L404)
- Modify: [`agents-sdk/config.toml`](../../../../agents-sdk/config.toml) — add `[judge_layer]` table (`enabled = false` default, `model = "gemma4:e4b"`, `host = "mac_mini_ollama"`, `max_retries_on_revise = 2`, `max_cost_usd = 0.05`); add `judge_enabled = false` flag to the existing `[substack_drafter]` table
- Modify: HybridRouter task profile registry — add `judge_layer` profile routing to `gemma4:e4b` on Mac Mini Ollama with `fallback_disabled = true` (the fail-open path is explicit in `judge.py`, not a router fallback)
- Modify: [`CHANGELOG.md`](../../../../CHANGELOG.md), [`CLAUDE.md`](../../../../CLAUDE.md), [`README.md`](../../../../README.md) — count updates per mandatory doc rule (judge layer becomes a new top-level module + adds a new launchd-adjacent capability)
- Create (auto via Gap-Fill 3 ledger pipeline): `~/Code-Brain/sw-portfolio/src/content/transactions/judge-layer.md`

**- [ ] Step 1 (Days 1–2, 2026-05-26 → 2026-05-27): Module scaffold + Pydantic schema + Outcome enum.**
Create `agents-sdk/lib/judge/` with `__init__.py`, `schema.py`, and unit tests. `ActionProposal` Pydantic model with all 8 fields per Architecture B above; `evidence_used` and `rollback_path` typed `Optional` because substack-drafter can't always provide them. `Outcome` enum has 5 values (4 + `JUDGE_UNAVAILABLE`). `JudgeDecision` Pydantic model wraps an `Outcome` + optional `feedback: str` (used in `REVISE`) + optional `quarantine_reason: str` (used in `ESCALATE`) + `model_used: str` + `latency_ms: int` + `evaluated_at: datetime`. Tests cover required-field validation + serialization round-trip. ~6 hours.

**- [ ] Step 2 (Day 3, 2026-05-28): Policy YAML loader + first policy file.**
Create `policy.py` with `load_policy(name: str) -> Policy` reading from `agents-sdk/policies/<name>.yaml`. Policy schema: `name`, `agent`, `version`, `rules` (list of `{condition, outcome, feedback_template}` tuples), `fallback_outcome` (default `ALLOW`). Author `substack_drafter.yaml` with 4 rules: (a) draft contains unverifiable claim about a named person → `ESCALATE`; (b) draft asserts a fact attributable to The Block without `[citation needed]` marker → `REVISE`; (c) voice mode deviates from the configured rotation slot → `REVISE`; (d) draft contains a publish action verb (`POST`, `PUBLISH`, `SHIP IT`) at the top level → `BLOCK` (Tier-A "Sean sends" boundary). Tests cover YAML schema validation + 1 example per rule. ~4 hours.

**- [ ] Step 3 (Day 4, 2026-05-29 — Friday retro day, run inside the morning learning hour): Judge `evaluate()` function with HybridRouter integration.**
Implement `judge.evaluate(proposal: ActionProposal, policy: Policy) -> JudgeDecision`. Calls the new `judge_layer` HybridRouter task profile → `gemma4:e4b` on Mac Mini Ollama. System prompt enumerates the policy rules; user prompt is the `ActionProposal` serialized as YAML (so the local model sees a familiar structured input shape). Output is parsed as a JSON `{outcome, feedback, quarantine_reason}` blob with explicit retries on parse failure (max 3, then `JUDGE_UNAVAILABLE`). Tests mock the router and cover all 5 outcomes + parse-failure path + timeout-fallback path. ~6 hours.

**- [ ] Step 4 (Day 5, 2026-06-01): JSONL ledger writer + fail-open Pushover wiring.**
Implement `ledger.write(decision: JudgeDecision, proposal: ActionProposal, agent_name: str)` writing to `vault/health/judge_log/{YYYY-MM-DD}.jsonl` with atomic FileLock (reuse the synth-manifest pattern at [`agents-sdk/lib/`](../../../../agents-sdk/lib/)). Pushover client reuses the existing wrapper from the v3.33.0 Pushover boot check. Fail-open detection: any `CLIConnectionError` / `httpx.ConnectError` / `httpx.ReadTimeout` / `OllamaUnavailableError` from `evaluate()` → catch in the wrapper, return `Outcome.JUDGE_UNAVAILABLE`, ledger-log it, fire Pushover alert with severity `warning`, return `decision.outcome = ALLOW` to caller. Tests with mocked failure modes. ~5 hours.

**- [ ] Step 5 (Day 6, 2026-06-02): Wire judge into substack-drafter.**
Modify [`substack_drafter.py main()`](../../../../agents-sdk/agents/substack_drafter.py) to call `judge.evaluate()` between `_route()` (proposed draft text returned) and `write_draft()` (persistence). Build the `ActionProposal` from the draft + voice-mode metadata + concept cluster. Outcome handling: `ALLOW` → `write_draft()` proceeds; `REVISE` → re-call `_route()` with the judge's feedback appended to the user prompt, max 2 retries (config-driven), then escalate; `BLOCK` → no draft written, ledger entry, Pushover ping; `ESCALATE` → write to `vault/.../substack-drafts/quarantine/` subfolder, urgent Pushover. Gated by `[substack_drafter] judge_enabled = false` default + global `[judge_layer] enabled = false` default. Both flags must flip true for the layer to engage. Integration test mocks `evaluate()` and verifies the 4 dispatch paths. ~6 hours.

**- [ ] Step 6 (Day 7, 2026-06-03): `--demo-injection` flag for the Loom take.**
Add `--demo-injection` flag to `_cli()` (mutually exclusive with `--voice-override`). When set, the prompt composer in `compose_prompt()` appends a synthetic fragment instructing the actor to fabricate a specific quote attributed to a named-but-archived figure. The judge response on that draft is real (the model genuinely evaluates the actor's output against the `substack_drafter.yaml` rule (a) → `ESCALATE` with quarantine_reason citing the unverifiable claim). The fragment lives in `agents-sdk/policies/demo_injection_fragments.yaml` (NOT in source — keeps the demo content tunable without code change). Production runs without the flag never load the file. Tests verify the flag injects the fragment + production runs don't. ~3 hours.

**- [ ] Step 7 (Day 8, 2026-06-03 evening or 2026-06-04 morning): 4-Q `EXPLANATION.md` artifact.**
Author `agents-sdk/lib/judge/EXPLANATION.md` per the Task 1 Step 1 schema. Frontmatter: `artifact: judge-layer`, `created: 2026-06-XX`, `surface: control-plane`, `shipped: 2026-06-XX`, `repoUrl: https://github.com/seanwinslow28/CLAUDE-CODE-SUPERUSER-PACK/tree/main/agents-sdk/lib/judge`, `explanationUrl: <github-permalink>`, related wikilinks to `substack_drafter.py`, `policy.py`, `evaluate.py`, `ledger.py`. Body answers all 4 questions concretely — *What is this?* a Pydantic-typed control-plane interceptor for one production agent (the substack-drafter); *Why this approach?* actor-judge separation per Nate §3.5, intercept-don't-rebuild to ship in 9 days, local model for $0/decision; *What would break?* judge model unavailability (mitigated by fail-open + Pushover), policy YAML drift from actual code paths (mitigated by integration tests), judge becoming the bottleneck on the actor's retry loop; *What did I learn?* the gap between an agent that writes and an actor inside a control architecture is exactly one Pydantic schema + one YAML policy file. ~90 minutes.

**- [ ] Step 8 (Day 9, 2026-06-04): 90-second Loom + ledger row + LinkedIn post.**
Record the demo: `python3 agents-sdk/agents/substack_drafter.py --demo-injection --dry-run` → ActionProposal serialized to terminal → judge returns `REVISE` (or `ESCALATE` depending on fragment) with required-citation feedback → actor retries → `ALLOW` → JSONL ledger entry shown via `tail vault/health/judge_log/$(date +%F).jsonl` → local draft only, no Pushover (publishing gate untouched). Closing line of narration: *"Agents draft. I send. Every word."* Loom under 90 sec. Add ledger entry at `~/Code-Brain/sw-portfolio/src/content/transactions/judge-layer.md` per Gap-Fill 3's content collection schema (surface: `"control-plane interceptor"`). One LinkedIn post: ~120 words, tags Anthropic + FDE-Boston JD URL + links to seanwinslow.com/transactions/judge-layer/. Sean's hand — agents do not draft the LinkedIn copy. ~3 hours including the take + retakes.

**- [ ] Step 9 (Day 9, end of day): Verification gate + commit.**
Run the full test suite (`cd agents-sdk && PYTHONPATH=. pytest tests/ -v`); all new tests pass + zero regressions in the existing 550-passing baseline. Live one-shot dry-run with `--demo-injection` produces the expected `REVISE → retry → ALLOW` sequence + a JSONL ledger entry. CHANGELOG / CLAUDE / README updated (count bump for new module). `python3 scripts/validate.py` → ≤60 warnings / 0 errors. Commit message: `feat(judge): ship judge layer v0 — Pydantic ActionProposal + YAML policy + JSONL ledger + substack-drafter integration (Council Gap-Fill 1)`. Tag `judge-layer-v0.1.0`. ~2 hours.

**Verification gate (Task 12 binary success criteria, all must pass by 2026-06-04 EOD):**
1. New tests pass; existing 550-test baseline preserved.
2. Live `--demo-injection` dry-run produces `REVISE → retry → ALLOW` sequence (or `ESCALATE` on fragment variant) with terminal-visible ActionProposal + JudgeDecision.
3. `vault/health/judge_log/$(date +%F).jsonl` contains ≥1 demo-run entry with full schema (5-outcome enum + Pydantic-serialized proposal + model_used + latency_ms).
4. 90-second Loom recorded clean, no re-takes needed for the second half of the demo.
5. `seanwinslow.com/transactions/judge-layer/` resolves with the V3 card hero (depends on Gap-Fill 3 deployed first — hard precondition).
6. LinkedIn post published, tagging Anthropic + FDE-Boston JD; Sean's hand on every word.
7. `python3 scripts/validate.py` ≤60 warnings / 0 errors.
8. CHANGELOG / CLAUDE / README updated for the new `lib/judge/` module + new launchd-adjacent capability surface.

**Compounding payoff (council brief + Sean's 2026-05-16 expansion):**
- **Council brief literal payoff:** Same module wraps Daily Driver + Job Feed agents for free (additive policy YAMLs + ActionProposal subclasses); becomes the policy engine cited inside Council Gap-Fill 4's `CONTROL_ARCHITECTURE.md` (judge = engine, Gap-Fill 4 = the policy-content artifact wrapped around it); gives Task 11 Agent Fleet Dashboard a real telemetry stream — judge-outcome distribution panel + judge-availability % panel + "Escalation Rate" metric.
- **Sean's 2026-05-16 forward-looking expansion (expansion candidates, not in Task 12 scope):**
  - **Vault Synthesizer judge wrap** — could gate connection-article writes against contradiction-detection feedback before they hit `vault/knowledge/connections/`. Policy YAML at `agents-sdk/policies/vault_synthesizer.yaml`; ActionProposal subclass adds `contradiction_score: float` and `cluster_size: int`; ledger lives at `vault/health/judge_log/vault_synthesizer/`. Probably a 2-day add once Task 12 ships.
  - **Future "vault-to-build" agent** — the agent Sean gestured at that takes synthesizer output and triggers downstream actions (creating scaffolds, opening PRs, drafting specs from the knowledge graph). Wider action surface than any current agent (touches code + filesystem + git), so it benefits *most* from judge wrapping — policy YAML would gate every action by exposure level, with `ESCALATE` mandatory for any git-write. This is the strongest argument for shipping the judge module with a generic-enough wrap interface from day 1 — which Step 1's `ActionProposal` schema already enables.
  - Both expansions are tracked as work items, not in this gap-fill's scope.

**Demo shape (90 sec, verbatim from chairman synthesis):**
> *Draft hallucinates a claim about The Block (synthetic `--demo-injection` trigger) → ActionProposal emitted with full Pydantic schema → judge returns `Revise` with required citation → actor retries → `Allow` → JSONL ledger entry → local draft only. Narration closes: "Agents draft. I send. Every word."*

**Tier-A check:** Walk-away $100k N/A. AI PM > Tech PM > Creative PM ✅ (this is canonical Anthropic FDE Boston JD content — "control architectures around production agent deployments" matches verbatim). Agents draft / Sean sends ✅ **EXPLICITLY PRESERVED** — judge is defense-in-depth; Sean's manual publish gate stays Tier-A canonical; fail-open behavior was chosen specifically to preserve this. 5:30 PM hard stop ✅ (9-day build fits inside Week 2 8:30–5:30 containers; sacred 8:30–9:30 learning hour untouched). Track-C protected ✅ (Track-C v0 already shipped 2026-05-12; if v0.2 work emerges during this build window it takes priority and Task 12 slips a week).

**Pre-shipping risks:**
- Task 8 Workstream **B7 gate** (5 consecutive nights of `concepts_written > 0` in synth-manifests) must close before Day 1 starts. As of 2026-05-16, the gate is open — requires successful synth runs Sat 5/17 → Wed 5/21 to close by Mon 5/26 start. NY trip 2026-05-14 → 2026-05-15 is already past; remaining window is local-MBP-awake nights. If MBP travel periods or dry-night fall-throughs slip the gate, Task 12 start slips proportionally.
- `gemma4:e4b` availability on Mac Mini Ollama has been ~100% since Phase 6 ship — risk is low but the `JUDGE_UNAVAILABLE` path was specifically designed to handle the tail. Ledger-tracked from day 1 so dashboard surfaces real availability data, not vibes.
- Pydantic schema versioning becomes a live concern at the *second* agent wrap (Daily Driver or vault-synthesizer): subclassing `ActionProposal` with agent-specific required fields needs an explicit migration story before any cross-agent ledger consumer (the dashboard) treats them as fungible.

---

### Task 13 — Access-vs-Meaning Manifesto + Spectrum Map (Council Gap-Fill 2; NEW 2026-05-17 — draft-lock 2026-05-23, publish ~2026-06-19)

> **Status:** Not started. **Zero new code** — 3–5 days of pure framing work, drafted in Week 1 (now), queued behind Substack Posts 1 (5/22 "Night My Vault Said Nothing") + 2 ("Vault said something again", depends on Task 11 dashboard ship 6/8–6/15). Publishes as **Substack Post 3** (~2026-06-19 Friday Week 5 if cadence holds). Becomes the **URL in Sean's email signature** for the back half of the sprint — the pre-read link that converts "interesting candidate" → "Tier-1 must-talk."

**Maps to:** Council Gap-Fill 2 + Nate §3.4 "Access vs Meaning / Semantic Work Primitives" (2026-05-05) + this roadmap's Decision 4 (Substack voice) **AMENDED** by adding a Post-3 manifesto slot + Karpathy synthesis Claim C ("specs and comprehension are the durable PM skill"). Cross-cites Task 3 (intent-engineering MCP) + Task 10 (vault-knowledge-mcp) + Task 12 (Judge Layer) + Task 14 (Control Architecture) as the artifact map's worked examples.

**Why this works as Post 3, not Post 1 or 2:** Per council: *"theses get callbacks; tools get bookmarked."* This is Sean's **interview cold-open** — the post that lives in the email signature for the rest of the hunt. Council unanimity placed it #2 on the gap-fill priority list (behind Judge Layer), and the chairman's call was that it ships AFTER the Judge Layer + Authority/Recovery/Audit work generates the artifact map to point at. Drafting in Week 1 + publishing Week 5 gives the manifesto a richer artifact list to plot than if it shipped first.

**Architecture (locked per council brief + 2026-05-17 reads):**
- **Three companion files** — long-form essay + spectrum diagram + Substack cross-post — with the canonical Markdown source living at `docs/MEANING_OVER_ACCESS.md` and a syndicated MDX copy at `~/Code-Brain/sw-portfolio/src/content/essays/meaning-over-access.mdx` (new `/essays/` IA on the personal site — companion route to `/transactions/` + `/architecture/` + `/work/`).
- **Spectrum map is a Mermaid `quadrantChart`** (`access ↔ meaning` × `infrastructure ↔ workflow`), NOT a hand-authored SVG. Mermaid renders on GitHub + the Astro site (via `astro-mermaid`); Substack accepts the rendered PNG export. Zero Figma round-trip needed.
- **Role map is a table**, not a paragraph block — scannable for recruiters who arrive cold from the email signature.
- **Voice: thesis-forward with personal-voice opener + close**, sober/declarative middle. The manifesto genre doesn't suit pure Sedaris-mode comedy (Decision 4's default tone); the comedic register lands in the opening hook and the closing kicker, but the artifact-map + role-map sections read straight. Voice override at draft time if Sean's read says otherwise.
- **Word count: ~1,500.** Tighter than Task 15's architecture essay — this is a thesis statement, not an architecture doc.

**Files (NEW + MODIFY):**
- Create: [`docs/MEANING_OVER_ACCESS.md`](../../../../docs/) — canonical Markdown source (~1,500 words, 5 sections)
- Create: `docs/diagrams/access-meaning-spectrum.mmd` — Mermaid `quadrantChart` source (embeddable + version-controlled)
- Create: `docs/diagrams/access-meaning-spectrum.svg` — pre-rendered SVG export (via `mmdc` CLI) for Substack image embed
- Create: `~/Code-Brain/sw-portfolio/src/content/essays/meaning-over-access.mdx` — Astro syndicated copy (re-imports the Mermaid source for in-site rendering)
- Create: `~/Code-Brain/sw-portfolio/src/pages/essays/index.astro` — new `/essays/` landing page listing this + future essays
- Create: `~/Code-Brain/sw-portfolio/src/pages/essays/[slug].astro` — dynamic essay route
- Create: `~/Code-Brain/sw-portfolio/src/content/config.ts` schema update — new `essays` collection alongside `transactions` and `architecture`
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/2026-06-19-meaning-over-access-substack-cross.md` — Substack-formatted cross-post (Sean publishes from this when Post 3 slot opens)
- Create: `docs/MEANING_OVER_ACCESS_EXPLANATION.md` — 4Q artifact for the manifesto (feeds Gap-Fill 3 ledger row)
- Modify: [`CHANGELOG.md`](../../../../CHANGELOG.md), [`CLAUDE.md`](../../../../CLAUDE.md), [`README.md`](../../../../README.md) per mandatory doc rule
- Create (auto via Gap-Fill 3 ledger pipeline): `~/Code-Brain/sw-portfolio/src/content/transactions/meaning-over-access.md`

**- [ ] Step 1 (Day 1, 2026-05-19 or 2026-05-20 — slots in after Gap-Fill 3's Mon 5/19 deploy lands): Outline pass.**
Lock the 5-section outline:
1. **The bet** (~150 words, personal voice opener). Lead with one concrete hook: a moment where `access` (the agent could click the button) failed Sean's actual workflow because it didn't know what the button *meant*. Tee up the thesis: *access = reach; meaning = judgment.* Cite Nate §3.4 verbatim once.
2. **Artifact map** (~400 words + the Mermaid quadrant chart). 2D plot, two axes: `access ↔ meaning` (horizontal) × `infrastructure ↔ workflow` (vertical). Five plotted points: intent-engineering MCP (meaning + infrastructure), vault-knowledge-mcp (meaning + infrastructure), cost caps as authority primitive (meaning + workflow), judge layer as review primitive (meaning + workflow), `concept_edges` as memory primitive (meaning + infrastructure). All five live on the **meaning** side — the explicit reading is "Sean's stack is meaning-side; he's not betting on access." Two negative-space callouts on the access side: "browser-use" / "computer-use" agents (access + workflow) and "MCP HTTP transports / SaaS connectors" (access + infrastructure) — named but not endorsed.
3. **Role map** (~400 words, table format). Five rows mapping companies/JD vocabularies to where on the spectrum they buy. Cite real JDs as evidence:
   | Buyer | Spectrum position | Vocabulary tell | Example JD |
   |---|---|---|---|
   | Anthropic FDE Boston | meaning + workflow | "control architectures around production agent deployments" | [JD URL] |
   | Glean | meaning + infrastructure | "knowledge governance," "action primitives" | [JD URL] |
   | Sierra / Decagon | meaning + workflow | "agent PM loops," "structured action surfaces" | [JD URL] |
   | Cursor / Cognition | mixed | "developer workflow primitives" | [JD URL] |
   | Manus / Adept / browser-use | access + workflow | "computer-use," "browser automation" | [JD URL] |
4. **Why not browser-first** (~250 words). The argument: access-only agents are brittle because the meaning layer they assume (button labels, page structure, DOM semantics) is hostile to the agent — it changes under them. Meaning-layer agents are durable because they operate on typed work primitives the human controls. Use one concrete failure mode (e.g., Lindy clicking through a Notion page whose section header changed).
5. **The bet, restated** (~150 words, personal voice close). Echo the opener. Closing kicker — something memorable and Sean-voiced (not Sedaris-comedic, but Sean-honest). The kind of line that gets quoted back in the recruiter call: e.g., *"I don't think the durable enterprise value is agents clicking around UIs. I think it's the semantic layer: typed work objects, authorization, memory provenance, reviewable decisions. Here are the seven artifacts I've shipped to back it."* (GPT-5.5's verbatim positioning from the chairman synthesis.)

Outline ships as a section-by-section bullet list with target word counts. Sean reviews before Step 2. ~3 hours.

**- [ ] Step 2 (Day 1 evening → Day 2, 2026-05-20/21): Draft pass on the long-form essay.**
Author `docs/MEANING_OVER_ACCESS.md` to the outline. Use `agents-sdk/agents/substack_drafter.py --voice sean` for a first draft pass on Sections 1 + 5 (the personal-voice bookends), but `--voice strategic-sober` (or hand-author) Sections 2, 3, 4. The drafter is a research-grade assistant for personal voice; the analytical middle goes hand-authored. Personal voice in 1 + 5 must include at least one concrete moment from Sean's actual recent work (the synth-manifest silent-regression diagnostic from 2026-05-13, the council run from 2026-05-16, or the intent-engineering dogfood result). ~6 hours.

**- [ ] Step 3 (Day 2 evening, 2026-05-21): Spectrum diagram + render.**
Author `docs/diagrams/access-meaning-spectrum.mmd` as Mermaid `quadrantChart`. Embed inline in `MEANING_OVER_ACCESS.md`. Run `mmdc -i docs/diagrams/access-meaning-spectrum.mmd -o docs/diagrams/access-meaning-spectrum.svg -t neutral -b white` (install Mermaid CLI if needed: `npm install -g @mermaid-js/mermaid-cli`) — emit the PNG/SVG for Substack image embed. Verify rendering on GitHub preview + on a local Astro dev build. ~2 hours.

**- [ ] Step 4 (Day 3, 2026-05-22): Personal-site `/essays/` IA + syndicated MDX.**
Add `essays` collection to [`src/content/config.ts`](../../../../../sw-portfolio/src/content/config.ts) — schema: `title`, `subtitle`, `dateline`, `slug`, `excerpt`, `ogImage` (optional), `crossPostedTo` (optional URL list). Author `src/pages/essays/index.astro` (landing page listing essays, V3 design tokens) + `src/pages/essays/[slug].astro` (dynamic route, V3 card hero, body via Astro `<Content />`). Author `src/content/essays/meaning-over-access.mdx` syndicating `docs/MEANING_OVER_ACCESS.md` (build script `scripts/build_sync_essay.mjs` curls the raw GitHub URL at build time, similar to Task 15's `build_fetch_scorecard.mjs`). Wire `/essays/` into main nav alongside `/work/` + `/transactions/` + `/architecture/`. ~4 hours.

**- [ ] Step 5 (Day 3 afternoon, 2026-05-22): Substack-formatted cross-post + LinkedIn TL;DR pin.**
Author `vault/.../substack-drafts/2026-06-19-meaning-over-access-substack-cross.md` — same prose, Substack-specific formatting (image embeds rather than inline Mermaid, callout blocks instead of admonitions, footnotes shorter). Pre-draft a 280-character LinkedIn TL;DR + chart image for the day-of-publish pin. **Do NOT publish to Substack yet** — Post 3 slot opens after Posts 1 + 2 ship; Sean publishes from this file at slot time. ~3 hours.

**- [ ] Step 6 (Day 3 evening, 2026-05-22 — Friday retro day): Draft-lock review + 4Q EXPLANATION.md.**
Sean reads the full draft cold from `seanwinslow.com/essays/meaning-over-access/` (local dev build) — checks for: (a) personal-voice bookends don't feel like the analytical middle, (b) artifact map plots all five points correctly, (c) role map cites real JD URLs, (d) closing kicker is genuinely quotable, (e) no overclaiming beyond what the seven artifacts actually back. Iterate to **draft-locked** state. Author `docs/MEANING_OVER_ACCESS_EXPLANATION.md` per Task 1 Step 1 schema. *What is this?* a 1,500-word thesis statement framing seven shipped artifacts as a single meaning-over-access bet; *Why this approach?* "theses get callbacks; tools get bookmarked" — a manifesto is the recruiter-call cold-open; *What would break?* role map JD URLs going stale (mitigated by a quarterly review + `last_validated` field in essay frontmatter); the spectrum quadrant chart misreading on mobile (mitigated by image fallback for sub-768px viewports); over-claiming on the seven artifacts (mitigated by linking each plot point to its specific shipped commit); *What did I learn?* the manifesto wrote itself once Task 12 + Task 14 + Task 15 generated the artifact list — the thesis is downstream of the work, not upstream. Add ledger row at `~/Code-Brain/sw-portfolio/src/content/transactions/meaning-over-access.md` (Gap-Fill 3 schema; surface: `"manifesto / thesis"`). ~3 hours.

**- [ ] Step 7 (Day 3 night, 2026-05-22): Verification gate + commit (draft-lock).**
Run `python3 scripts/validate.py` → ≤60 warnings / 0 errors. Verify Mermaid renders on GitHub + Astro preview. Verify all role-map JD URLs return 200 OK. CHANGELOG / CLAUDE / README updated. Commit message: `feat(docs): draft-lock access-vs-meaning manifesto + spectrum chart (Council Gap-Fill 2)`. Tag `gap-fill-2-draft-locked`. ~1 hour.

**- [ ] Step 8 (deferred to Post-3 slot, target Fri 2026-06-19): Publish Substack Post 3 + LinkedIn pin.**
Copy `vault/.../substack-drafts/2026-06-19-meaning-over-access-substack-cross.md` into the Substack composer; upload the spectrum PNG; preview; publish. LinkedIn: post the 280-char TL;DR + chart image; pin to profile; update headline to reference the manifesto (e.g., `AI PM | I bet on meaning, not access | seanwinslow.com/essays/meaning-over-access`). Email signature gets the URL the same day. ~45 minutes of Sean-time on publish day.

**Verification gate (Task 13 binary success criteria — split into draft-lock and publish gates):**

*Draft-lock gate (must pass by 2026-05-22 EOD):*
1. `docs/MEANING_OVER_ACCESS.md` ships ~1,500 words across 5 named sections with embedded Mermaid quadrant chart.
2. `seanwinslow.com/essays/meaning-over-access/` resolves on the local Astro dev build (depends on `/essays/` IA shipped Step 4).
3. All role-map JD URLs return 200 OK on draft-lock day.
4. 4Q EXPLANATION.md lands; ledger row added per Gap-Fill 3 schema.
5. `python3 scripts/validate.py` ≤60 warnings / 0 errors; CHANGELOG / CLAUDE / README count bumps land.

*Publish gate (must pass by 2026-06-19 EOD):*
6. Substack Post 3 published (~5 weeks after draft-lock); LinkedIn TL;DR pinned; email signature updated.
7. `seanwinslow.com/essays/meaning-over-access/` live on production (depends on Gap-Fill 3 deployed).
8. First recruiter / hiring-manager LinkedIn impression on the pinned post — captured as Substack/LinkedIn analytics screenshot in Sean's job-hunt tracker.

**Compounding payoff:**
- **Retroactively upgrades the 2026-05-12 intent-engineering MCP ship** from "a tool" to "the first instance of a thesis." Tasks 10 + 12 + 14 + 15 ship into the same thesis frame.
- **Gives `vault-knowledge-mcp` (Task 10) its launch narrative for free** — Post 3 is the pre-published thesis the MCP plugs into when it ships ~2026-06-04.
- **Becomes the pre-read link in every recruiter email** — converts cold-recruiter contact into a primed conversation about a published bet.
- **Activates the distribution gap from §4.4** (the manifesto IS the missing distribution surface) with a single URL.
- **The "essays" IA** (new `/essays/` collection on sw-portfolio) is permanent infrastructure — future thesis-shaped writing has a home; the Task 15 architecture essay + future engineering essays slot in without IA changes.

**Demo shape (NOT a demo — the deliverable shape itself is the demo):**
> *URL in the email signature.* Recruiter screen opens: *"Did you read the meaning-over-access post? Let me show you the seven artifacts that back it."* (Verbatim from chairman synthesis.)

**Tier-A check:** Walk-away $100k N/A (manifesto infrastructure). AI PM > Tech PM > Creative PM ✅ (manifesto reads at every PM track — meaning-layer framing applies broadly). Agents draft / Sean sends ✅ (drafter assists Sections 1+5 personal-voice pass; Sean hand-authors 2+3+4; every word that hits another human's inbox is Sean's). 5:30 PM hard stop ✅ (3-day draft + later publish day, all inside 8:30–5:30 containers). Track-C protected ✅ (Track-C v0 already shipped + Task 10 is the manifesto's own downstream consumer).

**Pre-shipping risks:**
- **JD URL rot** between draft-lock (5/22) and publish (~6/19). Mitigation: Step 6 re-validates URLs on publish day; cached snapshots saved to `vault/40_knowledge/references/role-map-2026-05-22-snapshots/` at draft-lock for evidence.
- **Personal voice drift** between Sections 1+5 and the middle. Mitigation: cold-read by Sean at Step 6 explicitly checks bookend tone vs middle.
- **Over-claiming on the seven artifacts** when Tasks 10 + 12 + 14 + 15 haven't all shipped yet at draft-lock (5/22) — only Task 3 (intent-engineering MCP), Phase D, Phase 6, eval suite, substack-drafter, Gap-Fill 3 ledger have shipped. Mitigation: draft references the artifacts in **present + near-future tense** explicitly ("intent-engineering MCP shipped 2026-05-12; vault-knowledge-mcp ships 2026-06-04"); publish-day Step 8 final-pass updates any tenses to past where shipped.
- **Substack cadence dependency** — Post 3 slot only opens after Posts 1 + 2 ship cleanly. If B7 gate slips Post 1 or Task 11 dashboard slips Post 2, Post 3 publish-date slips proportionally. Mitigation: draft-lock and publish are independent steps in this task; the draft has independent value as a `seanwinslow.com/essays/` artifact even if the Substack publish slips.

---

### Task 14 — Authority / Recovery / Audit Reframe (Council Gap-Fill 4; NEW 2026-05-17 — ship target 2026-06-10)

> **Status:** Not started. No code work — pure reframing of existing infrastructure (cost caps, circuit breakers, Pushover escalation, JSONL ledgers, keychain-gated API keys) as the "Authority / Recovery / Audit" trinity Nate names in §3.7. Ships Week 4 per council sequencing, slotted alongside animation pipeline (6/11) + Task 11 dashboard kickoff. **The FDE-shaped artifact** — direct match to Anthropic FDE Boston JD; closes §3.1 cost-economics zero-coverage gap in one move.

**Maps to:** Council Gap-Fill 4 + Nate §3.7 "6 implementation-architecture components" + Nate §3.1 cost-economics gap + this roadmap's Decision 3 (backup track = Agent Ops / FDP) + replaces Task 6 §J (enterprise-build patterns, deferred — superseded by this gap-fill as the FDE-shaped artifact). Pairs with Task 12 (Judge Layer): judge = engine, this = the policy-content artifact wrapped around it.

**Why this works for $0 of new code:** Sean has **already implemented** authority + recovery — the cost-cap-and-circuit-breaker pattern lives in [`agents-sdk/config.toml`](../../../../agents-sdk/config.toml) (`monthly_cap_usd = 50.00`, `daily_cap_usd = 20.00`, per-query caps on every task profile, `fallback_disabled = true` on Job Feed) and gets enforced by code paths in [`agents-sdk/lib/keychain.py`](../../../../agents-sdk/lib/keychain.py) (keychain-gated API keys), [`agents-sdk/lib/pushover.py`](../../../../agents-sdk/lib/pushover.py) (escalation surface), and the existing spend trackers at `vault/health/{council,gemini,job-feed}-spend-*.json` / `vault/health/synth-manifest-*.json` (audit trail). It's all framed today as "cost discipline." Reframing it as the Nate trinity is a 2–3-day write-up that produces FDE-shaped portfolio evidence simultaneously.

**Architecture (locked per council brief, 2026-05-17):**
- Three sections in `CONTROL_ARCHITECTURE.md` map 1:1 to Nate §3.7's three trinity terms.
- **HybridRouter** gets exactly **one paragraph** inside the Authority section ("authority over which brain runs which task"). NO standalone runtime-architecture / Agent OS post — Task 7 STOP-DOING item explicitly enforces this. Council Deprioritization 1 (Gemini Pro's credibility-risk insight) is the load-bearing reason: Sean is a beginner-to-intermediate coder; framing 100 lines of routing logic as "Agent OS architecture" invites senior engineers in technical screens to grill him on concurrency / distributed caching / thread locking / memory leaks — fights he can't win at his coding level.
- Demo is a **forced over-budget call** that exercises all three legs in 60–90 seconds: breach → block → ledger write → Pushover ping → rollback path documented.

**Files (NEW + MODIFY):**
- Create: [`agents-sdk/docs/CONTROL_ARCHITECTURE.md`](../../../../agents-sdk/docs/) — the main artifact (~1,500 words, three sections + Mermaid sequence diagram + the worked-example walkthrough). This is the FDE bait.
- Create: `tools/governance-demo/` (new sidecar tools subdir, sibling to existing `tools/llm-council/`)
- Create: `tools/governance-demo/replay_budget_breach.py` — Python CLI that replays one of three fixture scenarios against a stubbed agent runner, exercises the real circuit-breaker + Pushover + ledger paths, exits with the documented exit code
- Create: `tools/governance-demo/fixtures/allowed.json` (a request inside budget — Allow path)
- Create: `tools/governance-demo/fixtures/over_budget.json` (a request that breaches the daily cap — Block + circuit-trip path)
- Create: `tools/governance-demo/fixtures/missing_auth.json` (a request with a stripped keychain key — keychain-gate path)
- Create: `tools/governance-demo/outputs/sample_ledger.jsonl` (sample JSONL output captured from one live `replay_budget_breach.py` run, committed for recruiter inspection without requiring a clone-and-run)
- Create: `agents-sdk/config/authority.example.yaml` (sanitized declarative policy example showing the per-query/daily/monthly budget shape + keychain-gated key pattern + fallback_disabled flag pattern; mirrors the `[gemini_researcher]` and `[job_feed]` and `[llm_council]` config blocks structurally without leaking real cost numbers)
- Create: `agents-sdk/docs/EXPLANATION.md` (4Q artifact for the control-architecture write-up — auto-feeds ledger row at `/transactions/control-architecture/` via Gap-Fill 3 content collection pipeline)
- Modify: [`CHANGELOG.md`](../../../../CHANGELOG.md), [`CLAUDE.md`](../../../../CLAUDE.md), [`README.md`](../../../../README.md) per mandatory doc rule (new top-level docs dir + new `tools/governance-demo/` sidecar)
- Create (auto via Gap-Fill 3 ledger pipeline): `~/Code-Brain/sw-portfolio/src/content/transactions/control-architecture.md`

**- [ ] Step 1 (Day 1, 2026-06-08): Authority section.**
Author the Authority section of `CONTROL_ARCHITECTURE.md`. Three subsections: **(a) per-query/daily/monthly budget caps as policy** — cite [`config.toml` line 340 monthly_cap_usd / line 341 daily_cap_usd](../../../../agents-sdk/config.toml#L340-L341) verbatim; explain the cascade (per-query cap fires first → daily aggregator catches the second-order overshoot → monthly governor is the safety net). **(b) Keychain-gated API keys** — cite [`agents-sdk/lib/keychain.py`](../../../../agents-sdk/lib/keychain.py); explain why secrets in macOS Keychain (not `.env`) is a design choice that maps to enterprise "authority over which agent holds which credential." **(c) `fallback_disabled = true` on Job Feed (config.toml line 366)** — frame as authority over which model is *not* allowed for which task; a positive-space example of routing-as-policy. Plus the **one-paragraph HybridRouter mention** — "authority over which brain runs which task" — and explicit deferral of any standalone runtime-architecture framing (link to Task 7 STOP-DOING entry as the canonical "why not"). ~6 hours including a 30-minute editorial pass.

**- [ ] Step 2 (Day 1 afternoon → Day 2 morning, 2026-06-08/09): Recovery section.**
Three subsections: **(a) Circuit-breaker exit codes** — enumerate the documented exit codes used across the fleet (`0 = allow`, `1 = error/log`, `2 = deny`, fleet-specific extensions like `7 = budget breach` from gemini_dr.py / council). Reference the [hook exit-code semantics from CLAUDE.md](../../../../CLAUDE.md) ("Hook Exit Codes" section) as the canonical anchor. **(b) Rollback paths** — the spec from each agent's "Rollback = ..." line in CLAUDE.md (Phase D, Phase 6, Tier 1/2, knowledge-loop Phase A/B/C/D); the worked-example pattern (each shipped capability has a one-shell-command rollback). **(c) SQLite state-parking + Pushover escalation** — `concept_edges` SQLite as durable state across runs; [`agents-sdk/lib/pushover.py`](../../../../agents-sdk/lib/pushover.py) as the human-loop escalation surface; tie back to Task 12's Judge Layer `JUDGE_UNAVAILABLE` ledger entry (recovery as a first-class outcome, not just an exception). ~5 hours.

**- [ ] Step 3 (Day 2 afternoon, 2026-06-09): Audit section.**
Three subsections: **(a) JSONL ledger schema** — enumerate the existing `vault/health/` artifacts (`council-spend-*.json`, `gemini-spend-*.json`, `job-feed-manifest-*.json`, `synth-manifest-*.json`) and Task 12's forthcoming `judge_log/*.jsonl`; show the consistent shape (append-only, timestamped, per-run, atomic). **(b) Git history as audit primitive** — CHANGELOG.md + per-version commit semantics + the "frozen reference" pattern (Task 3's MCP publish-flow walkthrough, this roadmap's structure). **(c) Phase D `concept_edges` provenance fields** — typed reasoning edges as a SQL-queryable audit substrate for the knowledge graph itself; cite [`agents-sdk/lib/concept_edges/`](../../../../agents-sdk/lib/concept_edges/) and the Phase D EXPLANATION.md. ~5 hours.

**- [ ] Step 4 (Day 2 evening → Day 3 morning, 2026-06-09/10): Mermaid sequence diagram + demo script.**
Embed a Mermaid sequence diagram in `CONTROL_ARCHITECTURE.md` showing the four-control-surface chain: breach → block → ledger write → Pushover ping → rollback. Author `tools/governance-demo/replay_budget_breach.py` — a Python CLI taking `--fixture {allowed,over_budget,missing_auth}` that replays the fixture against a stubbed agent runner, exercises the real circuit-breaker + ledger writer + Pushover paths (Pushover client gets a `--dry-pushover` flag to avoid actually paging Sean's phone during the demo). Authors the three fixture JSON files + captures one live run's output into `outputs/sample_ledger.jsonl`. Tests: `pytest tools/governance-demo/test_replay.py` covers all three fixtures + the dry-pushover branch. ~4 hours.

**- [ ] Step 5 (Day 3 morning, 2026-06-10): `authority.example.yaml` + 4Q EXPLANATION.md.**
Author the sanitized example YAML mirroring the structure of the real `[gemini_researcher]` / `[job_feed]` / `[llm_council]` config blocks but with generic cost numbers (e.g., `$1.00 / $10.00 / $50.00` per-query/daily/monthly). Author `agents-sdk/docs/EXPLANATION.md`: *What is this?* a 1,500-word reframing of the existing cost-discipline pattern as the Authority/Recovery/Audit trinity FDE buyers look for; *Why this approach?* 80% of the work is already shipped, the artifact is the naming + worked example; *What would break?* the demo script's stubbed agent runner drifting from the real runner's exit-code semantics (mitigated by integration test reading actual exit codes from one real Job Feed run); *What did I learn?* that control architecture is mostly the discipline of writing down what's already implemented, not building new infrastructure. ~3 hours.

**- [ ] Step 6 (Day 3 afternoon, 2026-06-10): 90-sec Loom + ledger row + LinkedIn post (Anthropic FDE-tagged).**
Loom shooting list: terminal split-pane on the left running `python3 tools/governance-demo/replay_budget_breach.py --fixture over_budget`; on the right, `tail -f vault/health/council-spend-$(date +%Y-%m).json` showing the breach landing in the ledger in real time; bottom: phone showing the Pushover notification. Total demo time: 60–90 seconds. Narration closer: *"Authority. Recovery. Audit. Four control surfaces in three seconds. This is what control architecture means in practice."* Add ledger row at `~/Code-Brain/sw-portfolio/src/content/transactions/control-architecture.md` per Gap-Fill 3 schema (`surface: "control architecture (docs)"`). One LinkedIn post: ~150 words, tags **Anthropic Forward Deployed Engineer Boston JD** + cites the Loom + links to `seanwinslow.com/transactions/control-architecture/`. Sean's hand on every word. ~3 hours including the take + retakes.

**- [ ] Step 7 (Day 3 evening, 2026-06-10): Verification gate + commit.**
Run `python3 scripts/validate.py` → ≤60 warnings / 0 errors. Run `pytest tools/governance-demo/test_replay.py` → green. Verify Mermaid diagram renders correctly on GitHub (preview the PR). Verify all four control surfaces fire in a one-shot `--fixture over_budget` run (output captured in `outputs/sample_ledger.jsonl`). CHANGELOG / CLAUDE / README updated. Commit message: `feat(docs): ship control-architecture trinity reframe — authority + recovery + audit (Council Gap-Fill 4)`. ~1 hour.

**Verification gate (Task 14 binary success criteria, all must pass by 2026-06-10 EOD):**
1. `agents-sdk/docs/CONTROL_ARCHITECTURE.md` ships with three named sections (Authority / Recovery / Audit) + Mermaid sequence diagram + exactly one HybridRouter paragraph under Authority (NOT a separate section).
2. `tools/governance-demo/replay_budget_breach.py --fixture over_budget` runs in <10 seconds, writes to `vault/health/` JSONL ledger, returns exit code `7` (budget breach), and (without `--dry-pushover`) fires a real Pushover notification.
3. All three fixtures (`allowed`, `over_budget`, `missing_auth`) exercise distinct code paths verified by `pytest`.
4. `outputs/sample_ledger.jsonl` checked in with one captured live-run entry per fixture.
5. 90-sec Loom posts cleanly; LinkedIn post tags Anthropic FDE Boston JD URL.
6. `seanwinslow.com/transactions/control-architecture/` resolves (depends on Gap-Fill 3 deployed).
7. `python3 scripts/validate.py` ≤60 warnings / 0 errors; CHANGELOG / CLAUDE / README count bumps land.

**Compounding payoff:**
- **Direct FDE artifact** for Anthropic FDE Boston referral via any warm intro (Larry's network, P&E peers).
- **Closes §3.1 cost-economics zero-coverage gap** — Sean's "one beginner skill" per both Nate-1 docs is now publicly closed with a worked example.
- **Pairs with Task 12 (Judge Layer)** to upgrade Task 11 dashboard from metrics panel → control-plane dashboard (Task 14 supplies the policy YAML format; Task 12 supplies the enforcement engine; Task 11 visualizes both as one stream).
- **Replaces Task 6 §J** (enterprise-build patterns, originally deferred to Week 6+ as interview-prep). This gap-fill IS the enterprise-build pattern artifact; §J becomes obsolete and Task 6 §J is closed out by Task 14's ship.
- **Generic enough for re-use across job titles** — same artifact reads as evidence for AI PM (cost economics fluency), Tech PM (control architectures), Creative PM (operational discipline), Agent Ops / FDP (the entire trinity, named).

**Demo shape (60–90 sec, verbatim from chairman synthesis):**
> *"Watch an agent try to exceed its $7 daily budget. Exit code 7. Keychain check logged. JSON ledger entry. Pushover ping on my phone. Four control surfaces in three seconds. This is authority-recovery-audit from your enterprise deploy stack."*

**Tier-A check:** Walk-away $100k N/A (artifact infrastructure). AI PM > Tech PM > Creative PM ✅ (artifact reads at every PM track; especially direct at Anthropic FDE Boston). Agents draft / Sean sends ✅ (LinkedIn copy + every prose section is Sean's hand; agents drafted the Mermaid diagram source string and the Python demo skeleton). 5:30 PM hard stop ✅ (3-day build fits inside Week 4's 8:30–5:30 containers; animation pipeline ships 6/11 in parallel — Task 14 finishes 6/10, leaving 6/11 untouched). Track-C protected ✅ (independent build; if Track-C v0.2 emerges, takes priority).

**Pre-shipping risks:**
- Council Deprioritization 1 (no "Agent OS" / "runtime architecture" framing) must hold across the build. Risk: drift during the Authority section into framing HybridRouter as more than one paragraph. Mitigation: Task 7 STOP-DOING entry explicitly forbids it, surface this for self-check during the Day 1 editorial pass.
- Pushover notification during the Loom take could be visually distracting if the device is angled wrong on camera. Mitigation: Loom shooting list specifies the phone position (bottom of frame, large display zoom on) and `--dry-pushover` flag for any rehearsal runs.
- The demo script `replay_budget_breach.py` calls a stubbed agent runner, not a real Gemini DR or LLM Council invocation, to avoid real spend during the demo. The fixtures are designed to be obviously synthetic; a recruiter who clones the repo and runs against the real fleet would see real cost numbers in real ledgers. The README of `tools/governance-demo/` explicitly notes the stub boundary.

---

### Task 15 — Vault as Agent Infrastructure: 5-Test Scorecard (Council Gap-Fill 5; NEW 2026-05-17 — ship target 2026-06-03)

> **Status:** Not started. 2–3 day build, Week 3 council slot (5/31–6/6). **Precursor doc for Task 10** (`vault-knowledge-mcp`) — makes that MCP self-justifying when it ships by establishing the architectural argument first. Council unanimity: Sean's vault genuinely passes all five of Nate's structural tests, and almost no public PM portfolio does. This is what distinguishes Sean from every other laid-off PM with a Notion site.

**Maps to:** Council Gap-Fill 5 + Nate §3.3 "5 structural tests for agent infrastructure" + this roadmap's Task 10 (`vault-knowledge-mcp`, the MCP this scorecard self-justifies) + supports the "agent-operable knowledge" interview answer the Anthropic FDE Boston / Glean Agent Governance loops will probe for.

**Why this works as the foundation doc:** Sean has 118 skills + 13 subagents + 14 hooks + 17 SDK agents + 8 active agents + the Phase D typed-edges schema + the Phase 6 producer/consumer loop + the synth-manifest telemetry + the qa/ tier — but no public-facing **architectural argument** for why this assembly counts as agent infrastructure rather than "elaborate Obsidian setup." The 5-test scorecard provides that argument **in Nate's vocabulary**, then earns the right to ship `vault-knowledge-mcp` (Task 10) as "the MCP wrapping the only public PM vault that passes all five tests." Per chairman synthesis: *Sean's vault genuinely passes all five tests, and almost no public PM portfolio does.*

**Architecture (locked per council brief + 2026-05-17 reads):**
- **Three companion files**, each doing one job: (1) `vault/SCORECARD.md` is the **canonical short scoreboard** (table-shaped, lives inside the actual vault); (2) `docs/VAULT_AS_AGENT_INFRASTRUCTURE.md` is the **long-form architectural essay** (1,800–2,200 words); (3) `seanwinslow.com/architecture/vault-scorecard/` is the **public mirror of the scoreboard** (Astro page rendering `vault/SCORECARD.md`).
- **Mermaid diagram is an `erDiagram`, NOT a state-machine.** Council's "state-machine diagram" wording was imprecise — `concept_edges` is a relation schema (entity types + typed edges), which renders correctly as Mermaid's `erDiagram`. Generate via `scripts/generate_schema.py` reading the live SQLite + emitting the diagram source as Markdown-embeddable.
- **`examples/public_vault_fixture/` is fully synthetic** — 10 notes about a fictitious topic domain (climbing routes / coffee brewing / something off-thesis), 15 edges, all hand-authored or generated from a clean LLM prompt. **Zero leakage from the private vault.** Sean reviews the fixture line-by-line before commit.
- **Linear scores ABOVE the vault on Ownership + Permissions** per GPT-5.5's honesty contribution. The argument is: Linear's RBAC + semantic record-ownership (assignee, watcher, project access) is genuinely more sophisticated than the vault's file-system-permission model. Naming that gap is the **exact reason** `vault-knowledge-mcp` + the Judge Layer matter — they're how the vault gets to Linear's level on the axes it currently loses.

**Files (NEW + MODIFY):**
- Create: `vault/SCORECARD.md` — the canonical 5-test scoreboard (~600 words; table-driven; lives inside Sean's actual vault as the inward-facing source of truth)
- Create: [`docs/VAULT_AS_AGENT_INFRASTRUCTURE.md`](../../../../docs/) — the long-form architectural essay (~2,000 words; outward-facing companion piece)
- Create: `scripts/generate_schema.py` — reads `vault/.vault-index.db` `concept_edges` table → emits `docs/diagrams/concept-edges-erd.mmd` (Mermaid source) + a sanitized stats summary (counts, no slug names)
- Create: `examples/public_vault_fixture/` — 10 synthetic notes + 15 synthetic edges in a stripped-down vault layout, fully off-thesis topic (e.g., a tiny vault about espresso brewing methods) so there is **zero risk** of private content leak
- Create: `examples/public_vault_fixture/README.md` — explains the fixture is synthetic + how to load it into a test vault for `vault-knowledge-mcp` smoke tests
- Create: `docs/VAULT_AS_AGENT_INFRASTRUCTURE_EXPLANATION.md` — 4Q artifact for the long-form essay (feeds Gap-Fill 3 ledger row)
- Create: `~/Code-Brain/sw-portfolio/src/pages/architecture/vault-scorecard.astro` — Astro page rendering `vault/SCORECARD.md` (raw GitHub fetch + remark transform, or build-time read; site is static)
- Create: `~/Code-Brain/sw-portfolio/src/pages/architecture/index.astro` — `/architecture/` landing page listing scorecard + future architecture artifacts
- Modify: [`CHANGELOG.md`](../../../../CHANGELOG.md), [`CLAUDE.md`](../../../../CLAUDE.md), [`README.md`](../../../../README.md) per mandatory doc rule (new top-level `examples/` dir + new `scripts/generate_schema.py` + new docs)
- Create (auto via Gap-Fill 3 ledger pipeline): `~/Code-Brain/sw-portfolio/src/content/transactions/vault-scorecard.md`

**- [ ] Step 1 (Day 1 morning, 2026-06-01): Author `vault/SCORECARD.md`.**
The canonical short artifact. Five sections, one per Nate test:
- **(a) Persistent State** — diagnostic question: *Does the system survive a process crash, machine restart, or session boundary with state intact?* Sean's vault answer: ✅ — files on disk + SQLite `concept_edges` + JSONL session-end flush; cite the [Phase 6 knowledge_loop EXPLANATION.md](../../../../agents-sdk/agents/knowledge_loop/EXPLANATION.md). Comparison row: Notion ❌ (cloud-only, no offline source of truth) / default Obsidian ⚠️ (markdown durable, but no typed-edge persistence beyond filename links) / Linear ✅ (Postgres-backed) / Sean's vault ✅✅ (markdown + SQLite + manifests).
- **(b) Defined Verbs** — diagnostic question: *Are the legal operations on the system explicitly named?* Sean's vault answer: ✅ — six relation verbs (`supports`, `contradicts`, `evolved_into`, `supersedes`, `depends_on`, `related_to`) in [Phase D concept_edges](../../../../agents-sdk/lib/concept_edges/EXPLANATION.md); cite the file. Comparison row: Notion ❌ (verbs are app-actions, not data-level) / default Obsidian ⚠️ (one implicit verb: `[[wikilink]]`) / Linear ✅ (issue states + transitions are defined verbs) / Sean's vault ✅✅ (6 typed relations + the validator enforcing them).
- **(c) Ownership** — diagnostic question: *Who owns each record, and is that ownership machine-readable?* Sean's vault answer: ⚠️ — files on disk + git history + frontmatter `author` field where present, but no per-record assignee/watcher model. Comparison row: Notion ✅ (page owner, editors, viewers) / default Obsidian ❌ (no record ownership) / Linear ✅✅ (assignee + creator + watchers; semantic and queryable) / **Sean's vault ⚠️ (loses to Linear)**. **GPT-5.5 honesty:** "Linear is genuinely better here. That gap is exactly why `vault-knowledge-mcp` matters — it's the first step toward giving the vault Linear-grade ownership semantics on the axes that matter for agent control."
- **(d) Permissions** — diagnostic question: *Can the system grant or deny access per-record, per-role?* Sean's vault answer: ⚠️ — filesystem-level only (POSIX read/write, git remotes). Comparison row: Notion ✅ (page-level permissions) / default Obsidian ❌ (filesystem only) / Linear ✅✅ (RBAC, team scopes, project access) / **Sean's vault ⚠️ (loses to Linear).** Same honesty point as (c).
- **(e) Queryable Audit History** — diagnostic question: *Can a third party reconstruct what changed, when, and why, without the human's narration?* Sean's vault answer: ✅✅ — `git log` (semantic commit messages, the v3.X.X versioning) + `concept_edges` SQLite (typed edges with `valid_until` markers per Phase D) + `vault/health/*-manifest-*.json` + `vault/.../daily-log.md` session-end flushes. Comparison row: Notion ⚠️ (page version history, but search/query is weak) / default Obsidian ❌ (only what plugins add) / Linear ✅ (API + activity log + webhooks) / Sean's vault ✅✅ (git + SQLite + JSONL, three independent audit substrates).

Closing scoreboard:
| | Persistent State | Defined Verbs | Ownership | Permissions | Audit |
|---|---|---|---|---|---|
| Notion | ❌ | ❌ | ✅ | ✅ | ⚠️ |
| default Obsidian | ⚠️ | ⚠️ | ❌ | ❌ | ❌ |
| Linear | ✅ | ✅ | ✅✅ | ✅✅ | ✅ |
| Sean's vault | ✅✅ | ✅✅ | ⚠️ | ⚠️ | ✅✅ |

Closing line: *"Three passes, two failures, and the failures are where `vault-knowledge-mcp` and the Judge Layer are going next."*

~5 hours including the honest-comparison editorial pass.

**- [ ] Step 2 (Day 1 afternoon, 2026-06-01): Author `docs/VAULT_AS_AGENT_INFRASTRUCTURE.md`.**
The long-form essay (~2,000 words). Five named sections matching SCORECARD.md but expanded with code paths + worked examples. Lead: a paragraph reframing what "agent infrastructure" means (durable, named, ownable, permissioned, auditable — not "tool integrations"). Each section: (a) Nate's diagnostic question verbatim, (b) Sean's vault answer with permalinks to ≥1 specific file or commit, (c) the comparison row in narrative form (not just the emoji table), (d) **a screenshot or code snippet** — preferred order: ER diagram for (b) via `generate_schema.py`; commit-message diff for (e); SQLite query result for (e). Closing section: "Where the vault loses, and why those losses are the roadmap." Names Task 10 + Task 12 by their work product (the MCP + the Judge Layer) and frames them as the upgrade path on ownership + permissions. ~6 hours.

**- [ ] Step 3 (Day 2 morning, 2026-06-02): `scripts/generate_schema.py` + ER diagram.**
Python script (no new deps; uses stdlib `sqlite3`) reading `vault/.vault-index.db` `concept_edges` table → emits two artifacts: `docs/diagrams/concept-edges-erd.mmd` (Mermaid `erDiagram` source) and `docs/diagrams/concept-edges-stats.md` (sanitized counts: number of edges per relation type, number of nodes, edge density — **no slug names**, no leakage). The Mermaid source embeds cleanly into `VAULT_AS_AGENT_INFRASTRUCTURE.md` via the standard ``` ```mermaid ``` ``` fence. Tests: unit test against an in-memory SQLite stub with 6 edges (one per relation type) verifying both outputs render correctly. ~3 hours.

**- [ ] Step 4 (Day 2 afternoon, 2026-06-02): Author `examples/public_vault_fixture/`.**
Hand-author or LLM-generate (then hand-review) 10 fully-synthetic notes on a topic deliberately off Sean's thesis — **espresso brewing methods** is the working pick (concrete, non-political, no risk of leaking Sean's professional context). Each note has `[[wikilinks]]`; 15 edges total spread across all six `concept_edges` relation types (so the fixture exercises the full schema). Layout mirrors a stripped-down `vault/40_knowledge/concepts/` shape (no `20_projects/`, no `health/`, no `90_system/`). Add a `README.md` explaining: (a) this is synthetic, (b) how to load it (`cp -r examples/public_vault_fixture/ /tmp/test_vault && AGENT_VAULT_PATH=/tmp/test_vault python3 ...`), (c) what `vault-knowledge-mcp` smoke tests should run against it once Task 10 ships. **Sean line-by-line review before commit** is the explicit safety gate against private-vault leakage. ~3 hours.

**- [ ] Step 5 (Day 2 evening / Day 3 morning, 2026-06-02/03): Personal-site `/architecture/vault-scorecard/` page.**
Two new Astro routes in `sw-portfolio`: `/architecture/index.astro` (landing page listing scorecard + future architecture artifacts) and `/architecture/vault-scorecard.astro` (renders `vault/SCORECARD.md`). Build-time read pattern: at site build, `scripts/build_fetch_scorecard.mjs` curls the latest `SCORECARD.md` from the superuser-pack repo's raw GitHub URL and writes it into `src/content/architecture/vault-scorecard.md`; Astro renders it with the V3 design tokens. Wire `/architecture/` into the main nav. Verify the ER diagram embeds correctly (use `astro-mermaid` integration if needed, ~5 min add). ~3 hours.

**- [ ] Step 6 (Day 3 morning, 2026-06-03): 4Q EXPLANATION.md + ledger row.**
Author `docs/VAULT_AS_AGENT_INFRASTRUCTURE_EXPLANATION.md` per Task 1 Step 1 schema. *What is this?* a 5-test architectural argument scoring four knowledge systems against Nate's structural tests; *Why this approach?* Nate's test framing is the load-bearing recruiter vocabulary for 2026; building the comparison earns the right to ship Task 10's MCP as "the MCP wrapping the only public PM vault that passes all five tests"; *What would break?* fixture drift if `concept_edges` schema evolves (mitigated by integration test against the live schema); reading my own architectural arguments as truth when they're really claims (mitigated by the explicit Linear-wins-here honesty); *What did I learn?* most "agent infrastructure" claims fail the persistent-state test on day one — the test discriminates. Add ledger row at `~/Code-Brain/sw-portfolio/src/content/transactions/vault-scorecard.md` (Gap-Fill 3 content collection; surface: `"architecture writeup"`). ~90 minutes.

**- [ ] Step 7 (Day 3 afternoon, 2026-06-03): Loom segment + Substack candidate + LinkedIn.**
Loom (60–90 sec): screen-record the SCORECARD.md table scoring (show the four rows + the closing "two failures" line) → cut to the ER diagram → cut to one synthetic-vault example query (e.g., `python3 scripts/query.py --vault examples/public_vault_fixture/ "what brewing methods compete with espresso?"` returning a `[[link]]`-cited answer using the fixture data). Closing line: *"Most people see Obsidian as content. I treat my vault as agent infrastructure. Five tests, five scores, code links to all of them. That's why my agents can write back into the vault and Lindy can't write back into yours."* Substack post **candidate** (per council Week 3 sequencing — actual ship gated on B7 + the post-2 calendar slot); pre-draft sketch at `vault/20_projects/prj-job-hunt-2026/.../substack-drafts/2026-06-03-vault-said-something-again-candidate.md` (Sean confirms voice mode before publish). LinkedIn post tagging Glean / Anthropic / the MCP team. Sean's hand on every word. ~3 hours.

**- [ ] Step 8 (Day 3 evening, 2026-06-03): Verification gate + commit.**
Run `python3 scripts/validate.py` → ≤60 warnings / 0 errors. Run `python3 scripts/generate_schema.py --self-test` → both artifacts emit correctly. Verify Mermaid diagram renders on GitHub + on the seanwinslow.com page. **Line-by-line manual review of `examples/public_vault_fixture/` for leakage** (last gate before commit). CHANGELOG / CLAUDE / README updated. Commit message: `feat(docs): ship vault-as-agent-infrastructure scorecard + synthetic public fixture (Council Gap-Fill 5)`. ~2 hours.

**Verification gate (Task 15 binary success criteria, all must pass by 2026-06-03 EOD):**
1. `vault/SCORECARD.md` ships with five sections + the four-row comparison table + the "two failures" closing.
2. `docs/VAULT_AS_AGENT_INFRASTRUCTURE.md` ships ~2,000 words with permalinks to ≥5 specific files / commits + embedded ER diagram.
3. `scripts/generate_schema.py --self-test` passes; emits both `concept-edges-erd.mmd` and `concept-edges-stats.md`.
4. `examples/public_vault_fixture/` contains 10 synthetic notes + 15 edges across all 6 relation types; Sean has reviewed line-by-line; zero private content leaked.
5. `seanwinslow.com/architecture/vault-scorecard/` resolves and renders the scoreboard + ER diagram correctly (depends on Gap-Fill 3 deployed first).
6. 60–90-sec Loom segment recorded clean; LinkedIn post lands tagging Glean / Anthropic / MCP team.
7. `python3 scripts/validate.py` ≤60 warnings / 0 errors.
8. CHANGELOG / CLAUDE / README count bumps land for new `examples/` dir + `scripts/generate_schema.py` + new docs.

**Compounding payoff:**
- **Makes Task 10 (`vault-knowledge-mcp`) launch self-justifying** — the MCP ships as "the MCP wrapping the only public PM vault that passes all five Nate tests," with the scorecard as the prior-art doc. No more "why does this MCP exist?" framing problem.
- **Foundation for any "agent-operable knowledge" interview answer** — Anthropic FDE Boston / Glean Agent Governance / Sierra-shape Agent PM loops will all probe this.
- **The synthetic fixture becomes a permanent CI artifact** — any future MCP that operates against a vault layout can run smoke tests against `examples/public_vault_fixture/` without touching real user data. Reusable.
- **Linear-wins-on-ownership-and-permissions** is the **honest-comparison artifact** that calibrates Sean's credibility upward — Tier-1 recruiters detect over-claiming; admitting the two losses signals seniority.
- **Gives the Superuser Pack Loom (if Sean records one) a 5-segment structure** — one per Nate test, with the SCORECARD as the visual spine.

**Demo shape (60–90 sec, paraphrased from chairman synthesis):**
> *"Most people see Obsidian as content. I treat my vault as agent infrastructure. Five tests, two failures, three passes. Linear beats me on permissions; the vault beats Linear on persistent state and audit history. Both fail on different axes — and the two axes where I lose are the next two things I'm shipping (Task 10 + Task 12). Code links to all five tests on screen. Compare row-by-row to Notion. That's why my agents can write back into the vault and Lindy can't write back into yours."*

**Tier-A check:** Walk-away $100k N/A. AI PM > Tech PM > Creative PM ✅ (architecture writeups are an AI PM / FDE staple genre). Agents draft / Sean sends ✅ (LinkedIn post + every prose section is Sean's hand; agents drafted the Python `generate_schema.py` skeleton and the synthetic-fixture LLM seed prompts). 5:30 PM hard stop ✅ (3-day build fits inside Week 3's 8:30–5:30 containers; B7 gate verification work + Substack post 2 calendar slot both stay clear). Track-C protected ✅ (Track-C v0 already shipped; Task 10 is downstream of this gap-fill, not competing with it).

**Pre-shipping risks:**
- **Private-vault leakage via `examples/public_vault_fixture/`** is the load-bearing risk. Mitigation: synthetic topic is deliberately off-thesis (espresso brewing); Sean reviews line-by-line before commit; the fixture's README explicitly names "synthetic, off-thesis" as the design intent so a future contributor doesn't fold in real notes.
- **Over-claiming on the scorecard** undermines the artifact. Mitigation: GPT-5.5's Linear-wins-on-ownership-and-permissions framing is preserved verbatim; the artifact's credibility is the calibration, not the score itself.
- **`scripts/generate_schema.py` reading a live database** during the build → if the script runs in CI against a stripped database, the output stats will look weird. Mitigation: script supports `--db-path` flag; CI run uses the synthetic fixture; the canonical run is local against the real `vault/.vault-index.db`.
- **The personal-site `/architecture/` route is new IA** — competes for nav real-estate with `/transactions/` + `/work/` + `/about/`. Mitigation: keep the `/architecture/` landing minimal (Scorecard for now; future architecture docs slot in cleanly).

---

### Task 7 — STOP-DOING list (3+ items)

**Maps to:** Karpathy synthesis Part 5 "Stop investing in" + operating-model "self-blocking decisions pile up."

**- [ ] Stop adding new skills to the Superuser Pack until June 11.**
117 skills is past Sean's working-memory ceiling per Karpathy. Any net-new skill idea between now and June 11 goes to a `vault/00_inbox/skill-ideas-deferred.md` file. Audit + cut comes later (post-employment Q3).

**- [ ] Stop maintaining Cursor configs.**
Anti-Gravity is the primary IDE per the v2.0 personal context. Per Karpathy synthesis Part 5: "One IDE." Delete `.cursor/` if it still exists in any active repo; archive `cursorrules` files.

**- [ ] Stop unpausing 16BitFit until either Nano Banana 3 ships or LoRA work is done.**
The April 20 pause is strategically correct per Karpathy synthesis Part 5. Don't dabble. Don't even open the repo for "just a quick look." Sprite-consistency hacking soaks up time without producing portfolio signal.

**- [ ] Stop tuning local Qwen3-14B as a serious workload.**
Per Karpathy synthesis Part 5: it's intermittent on the MBP. Frontier + Sonnet + Haiku + gemma4 covers serious work. The Qwen3-14B path stays for the synthesizer/lint loops because it's already wired, but no new tuning effort.

**- [ ] Stop refining the 14-agent fleet structurally.**
After Task 6 §B (the Mac Mini migration), the fleet is locked through July 4. Bug fixes only. New agents go to the deferred ideas list. The fleet is interview asset, not active R&D.

**Verification gate:** Each item lives as a decision-log entry in [`prj-job-hunt-2026/README.md`](../../README.md) Decisions section, dated 2026-05-06.

---

## This Week's 5 Decisions

Format matches the [operating-model SOUL convention](../../../05_atlas/operating-models/job-hunt-2026/operating-model.md): "Decision: X. Default: Y. Switch only if: Z."

**Decision 1 — Track-C MCP server scope for the 5/25 v0 ship.**
**Default:** `intent-engineering` MCP server with 3 tools (`analyze_intent_spec`, `generate_template`, `audit_existing_spec`), stdio transport, Claude Desktop demo. Scope contained because the underlying skill is done.
**Switch only if:** A Week-2 interview loop emerges where a different MCP demo shape would be more directly relevant (e.g., a recruiter explicitly asks for a vault-knowledge or eval-router demo).

**Decision 2 — Canonical home for explanation artifacts.**
**Default:** Personal site (Astro 5 + React islands) at the `/transactions/` route, with co-located `EXPLANATION.md` in each GitHub repo. Substack syndicates with editorial framing. LinkedIn distributes.
**Switch only if:** Personal site build delays past 2026-05-13 — then GitHub `EXPLANATION.md` files become canonical until the site ships, with the Substack syndicating directly from GitHub raw URLs.

**Decision 3 — Backup track for applications.**
**Default:** Agent Ops / Forward Deployed Product / Support Ops AI. Apply to Anthropic FDE Boston in Week 2 as the wildcard. Glean (Agent Security & Governance, AI Quality, FDP), Scale AI (GenAI Platform PM, Public Sector T&E PM), Sierra/Decagon agent PMs.
**Switch only if:** Weeks 3–4 show ≥2 warm intros pulling Sean toward AI-augmented Domain Specialist roles via Larry's network — then run both tracks in parallel through Week 6.

**Decision 4 — Substack voice.**
**Default:** Story-driven Sean Mode (Sedaris-tuned, per `writing-voice-modes`). Comedic register where it lands. Don't compete with Nate's strategic-sober voice.
**Switch only if:** After 3 posts, engagement is <10% of comparable strategic-PM Substacks AND no inbound recruiter signal in 21 days — then test sober voice for posts 4–6.
**Voice rotation amendment (2026-05-10):** Kerouac (Beat Flow) variant drafted alongside Sedaris primary at [`2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md`](../substack-drafts/2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md). The Sedaris draft ships first (Friday Week 2). If readers respond strongly, run Kerouac for the follow-up post (Friday Week 3) to validate a 2-mode rotation. Long-term: voice rotation becomes the configurable parameter of the Substack-Drafter agent (Task 9).

**Decision 5 — Application volume cadence.**
**Default:** 5 quality applications per week starting Week 3 (master plan Phase 5 Task 5.2). Each tailored to the JD with one custom artifact link. Tuesday + Thursday morning slots.
**Switch only if:** By end of Week 4, response rate is <5% AND there are no active interview loops — then increase to 10/week with shorter customization (title + intro line only) and broaden Tier-2 to include Forward Deployed PM and Agent Ops at second-tier AI-native companies.

**The single most important decision in this week's set:** Decision 1 — Track-C scope. Every other decision is reversible in <72 hours. The MCP server scope locks 80% of Sean's deep-work time for the next 19 days. Get the scope right Monday or Tuesday; don't drift past Wednesday.

---

## Self-Review

**Spec coverage:** Phase 1 synthesis covers all 5 required headers. Phase 2 plan covers: existing-Phase-0–8 mapping ✓, Track-C 2026-05-25 anchor ✓, 3–5 portfolio projects with 4Q artifacts ✓ (5 portfolio-grade artifacts: intent-engineering MCP, Phase D `EXPLANATION.md`, Phase 6 `EXPLANATION.md`, sanitized financial-research fleet, animation pipeline + production diary; plus 14-agent fleet Loom + token cost calculator), 9 open work items resolved ✓, Tier-A respected ✓, STOP-doing list with 5 items ✓, "5 decisions this week" in operating-model format ✓.

**Amendment 2026-05-10 — portfolio count updated:** 6 flagship artifacts + 2 supporting + 1 post-employment Q3:
1. Intent-Engineering MCP server v0 (Track-C, ships 2026-05-25)
2. Phase D Typed Reasoning Edges `EXPLANATION.md` (ships Friday Week 1)
3. Phase 6 Knowledge Loop `EXPLANATION.md` (ships Friday Week 1)
4. Sanitized Agentic Financial-Research Fleet artifact (ships Friday Week 4)
5. 2D Animation Pipeline + production diary (ships 6/11)
6. **(NEW)** Vault Synthesizer Eval Suite + 2-post Substack arc (ships Friday Week 2, 2026-05-22; follow-up Friday Week 3, 2026-05-29)
- Supporting #1: 14-Agent Fleet Loom (Friday Week 2 → bumped to Friday Week 3 post-fix per Task 6 §C amendment)
- Supporting #2: Token Cost Calculator (Friday Week 3)
- **(NEW post-employment Q3)** Substack-Drafter Agent (Task 9, specced not built)

**Amendment 2026-05-13 — portfolio count updated again:** 8 flagship + 3 supporting + 1 post-employment (was 7+2+1 after 2026-05-12 Workstream C ship). Two new artifacts added as Tasks 10 + 11, both in `research-pending` status:

7. **(2026-05-12 promoted)** Substack-Drafter Agent — was post-employment Q3 spec, code-complete on `eval-suite-2026-05-12` branch; activation gated on B7 5-night gate.
8. **(NEW research-pending)** `vault-knowledge-mcp` — Sean's second MCP server, exposing the Phase D `concept_edges` SQLite + Phase 6 knowledge_loop articles as queryable MCP tools. Spec at [`2026-05-13-vault-knowledge-mcp-spec.md`](2026-05-13-vault-knowledge-mcp-spec.md). Ship target 2026-05-28 to 2026-06-04 pending DR-Max architecture validation.
- Supporting #3: **(NEW research-pending)** Agent Fleet Observability Dashboard. Spec at [`2026-05-13-agent-fleet-dashboard-spec.md`](2026-05-13-agent-fleet-dashboard-spec.md). Pairs with Substack post 2 as visual hero. Ship target 2026-06-08 to 2026-06-15 pending DR-Max positioning validation.

**Placeholder scan:** The 4Q drafts in Tasks 2, 3, 4 reference Claude-Nate-2 §2 source blocks, but the actual paste-ready text is in those source blocks (verified). The token-cost-calculator 4Q is fully drafted inline. No "TODO" / "TBD" / "fill in details" patterns. Task 6 §G defers YouTube to Week 5 with a concrete switch condition. Task 6 §J defers enterprise patterns to Week 6+ tied to interview loops.

**Type consistency:** "MCP server v0" / "intent-engineering MCP server" / "Track-C centerpiece" all refer to the same artifact. "EXPLANATION.md" / "4Q artifact" / "comprehension artifact" all refer to the same template. "Personal site `/transactions/`" / "canonical home" all refer to the same Astro 5 surface. Phase numbers reference master plan (Phase 0–8) consistently.

**Tier-A verification:**
- Walk-away $100k: no recommendation pushes below it ✓
- 5-days-in-office no: no recommendation requires it ✓
- AI > Tech > Creative PM: backup track (Agent Ops/FDP) is inside the AI PM family ✓
- Agents draft / Sean sends: Substack syndication, LinkedIn posts, application cover notes all flow Sean → human, agents draft only ✓
- Track-C protected even in offer weeks: Decision 1 + Task 3 verification gate make this explicit ✓
- Friday 4:30 retro: untouched, master plan Phase 7 Task 7.2 stays canonical ✓
- 8:30–9:30 AM sacred learning + 1–2 PM mandatory break + 5:30 PM hard stop: all preserved; explanation-artifact load is sized to fit the comms block (15:00–17:15), not deep-work ✓
- 2026-05-25 MCP server ship target: anchored in Task 3 ✓

**Honest flags:**
- Task 4 (sanitized financial-research fleet) ships Friday Week 4 alongside the master plan's Phase 5 mid-search retro. If applications dominate Week 4, slip Task 4 to Week 5 — it's a flagship artifact but not Tier-A.
- Task 6 §B (agent-fleet audit) is a Saturday-evening item explicitly off-the-clock. If Saturday gets eaten by life, slip to Sunday morning. Don't move it to a weekday — that's deep-work time.
- The 4Q drafts pasted from Claude-Nate-2 §2 are Sean's IP to the extent they describe Sean's work. ChatGPT-Nate-2 §2 is the lower-leverage backup if any of the Claude pre-drafts feel off in tone.

---

## Council Input — Nate Jones Digest (2026-05-16)

*Source: premium-profile LLM council run (Claude Opus 4.7 + GPT-5.5 + Gemini Pro + Grok 4.20; chairman Opus 4.7). Raw transcript: [`2026-05-16-council-nate-jones-digest.md`](2026-05-16-council-nate-jones-digest.md). Brief: [`/tmp/llm-council/nate-jones-roadmap-input-2026-05-16.md`](/tmp/llm-council/nate-jones-roadmap-input-2026-05-16.md). Cost: **$0.6178** (3:25 wall). Borda winner: Opus 4.7 (A > C > B / A > C > B / A > B > C / A > B > C). Cross-rank unanimity on response A.*

**Headline finding (unanimous across 4 panelists):** Sean's stack is built; it's not legible. The gaps are not engineering gaps — they are **framing surfaces** and **one missing piece of control architecture**. Roughly 80% of the work between "interesting candidate" and "Tier-1 must-talk" is reframing existing code in Nate's 2026 vocabulary. The 20% remaining is the Judge Layer.

The five council-recommended gap-fills below are NEW work not on the existing roadmap. They DO NOT replace Tasks 0–11. They sit alongside, sequenced into the calendar windows the existing roadmap leaves open. Each slots either as a new task in the 12+ series or as an amendment to an existing task.

### Council Gap-Fill 1 → New Task 12 — Judge Layer Retrofit on Substack-Drafter

**Nate framing:** §3.5 "Judge Layer / Actor-Judge separation / 4 outcomes" (2026-05-10). Maps to **Anthropic FDE Boston** JD verbatim ("control architectures around production agent deployments"), plus Sierra / Decagon / Glean Agent Governance loops.

**Roadmap slot:** NEW Task 12. Substack-Drafter (Task 9) is the wrap target — pre-publication, structured action surface, clear policy (agents draft / Sean sends). Does NOT rebuild the fleet; intercepts one actor.

**Build sketch (≤9 days):** New `agents-sdk/lib/judge/` module — `judge.py` + Pydantic `ActionProposal` schema (intended_action, target_surface, evidence_used, authorization_basis, expected_consequence, rollback_path, exposure_level) + declarative policy YAML at `agents-sdk/policies/substack_drafter.yaml` + JSONL ledger at `vault/agents/judge_log/`. Judge runs on local `gemma4:e4b` or `phi4-mini` ($0/decision). 4 outcomes (Allow / Block / Revise / Escalate). Start with Gemini Pro's lightweight interceptor (3–5 days); expand to full Pydantic schema (day 6–9). Tier-A check: agents draft / Sean sends preserved — judge fronts Sean's review, doesn't replace it.

**Compounding payoff:** Same module wraps Daily Driver + Job Feed agents for free. Becomes the policy engine inside Council Gap-Fill 4. Gives Task 11 Agent Fleet Dashboard a real telemetry stream (judge-outcome distribution, not just costs). Creates the "Escalation Rate" panel.

**Demo shape:** 90-second Loom. Draft hallucinates a claim about The Block → `ActionProposal` emitted → judge returns *Revise* with required citation → actor retries → *Allow* → JSONL ledger entry → local draft only. Closing line: *"Agents draft. I send. Every word."* This is the council's highest-leverage single artifact.

### Council Gap-Fill 2 → New Task 13 — Access-vs-Meaning Manifesto + Spectrum Map

**Nate framing:** §3.4 "Access vs Meaning / Semantic Work Primitives" (2026-05-05). Council quote (GPT-5.5): *"theses get callbacks; tools get bookmarked."*

**Roadmap slot:** NEW Task 13. Slots as Substack post 3, behind Posts 1 (5/22) + 2 (post-B7). Does NOT compete with B7 gate. Amends Decision 4 (Substack voice) by adding a post-3 manifesto slot.

**Build sketch (3–5 days, zero new code):** `docs/MEANING_OVER_ACCESS.md` + `assets/diagrams/access-meaning-spectrum.svg` + cross-post as Substack #3. Structure: (1) the bet — access = reach, meaning = judgment; (2) 2D artifact map (access↔meaning × infrastructure↔workflow) plotting intent-engineering MCP, vault-knowledge MCP, cost caps as authority primitive, judge layer as review primitive, `concept_edges` as memory primitive; (3) role map (Anthropic FDE → enterprise control semantics; Glean → knowledge governance; Sierra/Decagon → action primitives; Cursor/Cognition → developer workflow primitives); (4) why not browser-first; (5) the bet restated.

**Compounding payoff:** Retroactively upgrades the 2026-05-12 intent-engineering MCP ship from "a tool" to "the first instance of a thesis." Gives vault-knowledge-mcp (Task 10) its launch narrative for free. Becomes the pre-read link in every recruiter email.

**Demo shape:** Not a demo — a **URL in the email signature**. Recruiter screen opens: *"Did you read the meaning-over-access post? Let me show you the seven artifacts that back it."*

### Council Gap-Fill 3 → AMENDS Task 1 Step 3 + un-defers personal-site deployment

**Nate framing:** §3.2 "Comprehension as artifact / 4-Q template / TalentBoard" (2026-04-19). Council unanimity: Sean's own first-pass instinct in the brief (gallery → ledger) was correct and underweighted.

**Roadmap slot:** AMENDS Task 1 Step 3 (personal site `/transactions/` route) + un-defers [`2026-05-13-personal-site-deployment-deferred.md`](2026-05-13-personal-site-deployment-deferred.md). The deployment trigger fires now because the ledger form *is* the recruiter-ready state, where the gallery form wasn't.

**Build sketch (3–4 days):** Refactor `/transactions/` (commit `f13a103`) from gallery layout into reverse-chronological table — *date | artifact | surface | 4-Q link | before/after diff | model/cost*. Each row links to existing `EXPLANATION.md` files — no new 4-Q writing required. Build script `scripts/build_ledger.js` crawls repos for `EXPLANATION.md`, parses 4-Q, joins git-commit timestamps, emits JSON into `src/content/transactions/` at build time (every future ship adds a row for free). Deploy `seanwinslow.com` on Vercel — Monday 5/19, 1 hour. Add RSS feed. **Same-day LinkedIn refresh:** banner = ledger screenshot; headline = "AI PM | Agent fleet operator | seanwinslow.com/transactions"; "Open to Work" ON (recruiter-only).

**Compounding payoff:** Converts the next 8 weeks of work into compounding surface area. Replaces the resume as lead artifact. Activates the distribution gap from §4.4 with one URL. Every Council Gap-Fill below ships with a row for free.

**Demo shape:** URL in email signature. Call opens: *"I see you saw the ledger — which row do you want me to start with?"*

### Council Gap-Fill 4 → New Task 14 — Authority / Recovery / Audit Reframe (FDE Bait)

**Nate framing:** §3.7 "6 implementation-architecture components" (2026-05-13) + §3.1 cost-economics gap. Council quote: *"Sean has unwittingly already implemented authority + recovery in cost-cap-and-circuit-breaker, but framed it as 'cost discipline.'"*

**Roadmap slot:** NEW Task 14. Closes the §3.1 cost-economics zero-coverage gap in one move. Pairs with Council Gap-Fill 1 (judge = engine, this = policy content). Replaces Task 6 §J (enterprise-build patterns, deferred) as the FDE-shaped artifact.

**Build sketch (2–3 days):** `agents-sdk/docs/CONTROL_ARCHITECTURE.md` + `tools/governance-demo/replay_budget_breach.py` + Mermaid sequence diagram (breach → block → ledger write → Pushover ping → rollback). Three sections mapped 1:1 to Nate: **Authority** (per-query/daily/monthly budgets as policy, keychain-gated API keys, `fallback_disabled=true` on Job Feed); **Recovery** (circuit-breaker exit codes, rollback paths, SQLite state-parking, Pushover escalation); **Audit** (JSONL ledger schema, git history, `concept_edges` provenance fields). 60–90-second Loom triggering a forced over-budget call on LLM Council. **HybridRouter inclusion:** one paragraph inside Authority ("authority over which brain runs which task") — NOT a standalone "Agent OS" post (see deprioritization 1 below).

**Compounding payoff:** Direct artifact for Anthropic FDE Boston referral via any warm intro. Closes §3.1 cost-economics gap. Pairs with Gap-Fill 1 to upgrade Task 11 dashboard from metrics panel to control-plane dashboard.

**Demo shape (90 sec):** *"Watch an agent try to exceed its $7 daily budget. Exit code 7. Keychain check logged. JSON ledger entry. Pushover ping on my phone. Four control surfaces in three seconds. This is authority-recovery-audit from your enterprise deploy stack."*

### Council Gap-Fill 5 → New Task 15 — Vault as Agent Infrastructure: 5-Test Scorecard

**Nate framing:** §3.3 "5 structural tests for agent infrastructure" (2026-05-01). Council unanimity: Sean's vault genuinely passes all five tests, and almost no public PM portfolio does. This is what distinguishes Sean from every other laid-off PM with a Notion site.

**Roadmap slot:** NEW Task 15. Precursor doc for Task 10 (vault-knowledge-mcp) — makes the MCP self-justifying when it ships. Foundation for any "agent-operable knowledge" interview answer.

**Build sketch (2–3 days):** `vault/SCORECARD.md` mirrored at `seanwinslow.com/architecture/vault-scorecard` + `docs/VAULT_AS_AGENT_INFRASTRUCTURE.md` + `scripts/generate_schema.py` (reads `concept_edges` SQLite → Mermaid state-machine diagram) + `examples/public_vault_fixture/` (10 sanitized notes, 15 edges — NOT private vault). Five sections, one per Nate test (persistent state, defined verbs, ownership, permissions, queryable audit history). Each: (a) Nate's diagnostic question, (b) Sean's vault answer with code path, (c) comparison row scoring Notion / default Obsidian / Linear / Sean's vault, (d) screenshot evidence. **GPT-5.5's honesty contribution (preserve):** score Linear *above* the vault on ownership + permissions — that gap is exactly why vault-knowledge-mcp + judge layer matter.

**Compounding payoff:** Makes vault-knowledge-mcp (Task 10) launch self-justifying. Gives the Superuser Pack Loom a 5-segment structure. Foundation for the FDE interview answer "how do you think about agent memory."

**Demo shape:** *"Most people see Obsidian as content. I treat my vault as agent infrastructure. Five tests, five passes, with code links. Compare row-by-row to Notion. That's why my agents can write back into the vault and Lindy can't write back into yours."*

### Negative-Space — what to DEPRIORITIZE (and amendments to Task 7 STOP-DOING)

**Deprioritization 1 (unanimous, sharpest insight from Gemini Pro — chairman endorsed):** Skip the OpenClaw / Runtime Architecture framing as a standalone artifact. Sean's HybridRouter is 100 lines. Framing it as "Agent OS architecture" or "model routing as architecture" invites senior engineers in technical screens to grill him on concurrency, distributed caching, thread locking, memory leaks — fights he can't win at his coding level. His stack is AI PM > Tech PM > Creative PM; platform-engineering recruiters are a fourth track he's not targeting. **Add to Task 7 STOP-DOING: "Stop framing the HybridRouter as 'Agent OS' or 'runtime architecture.' One paragraph inside Council Gap-Fill 4's Authority section is the entire public surface this code gets."**

**Deprioritization 2 (Opus 4.7 + GPT-5.5):** Don't optimize `/transactions/` toward TalentBoard's surface or wait for TalentBoard's launch. Deploy the ledger as a standalone artifact on seanwinslow.com regardless. **Add to Task 7 STOP-DOING: "Stop waiting for TalentBoard. The ledger has to stand alone on seanwinslow.com. Resist scope creep toward a 'platform.'"**

**Deprioritization 3 (Grok 4.20):** Don't stretch §3.7's full six components into separate artifacts. Own authority/recovery/audit aggressively (Gap-Fill 4) but skip data-access governance and deep workflow design write-ups — Sean's background is not enterprise mid-market, and forcing that framing reads as pattern-matching rather than authentic strength.

### Council-Recommended Sequencing (drops into existing calendar)

| Week | Calendar | Council Gap-Fill | Existing roadmap parallel |
|---|---|---|---|
| Week 1 | **5/17–5/23** | Gap-Fill 3 (ledger deploy + LinkedIn) + Gap-Fill 2 (manifesto post draft) | Substack post 1 ships 5/22. Manifesto goes into post-3 queue. B7 gate window opens. |
| Week 2 | **5/24–5/30** | Gap-Fill 1 (Judge Layer retrofit) | Task 10 vault-knowledge-mcp DR-Max + build kickoff parallels. |
| Week 3 | **5/31–6/6** | Gap-Fill 5 (5-test scorecard) + Loom walkthrough | Substack post 2 candidate. |
| Week 4 | **6/7–6/13** | Gap-Fill 4 (Authority/Recovery/Audit + 90-sec demo) | Animation pipeline ships 6/11. Task 11 dashboard kickoff. |

Total new code: ~1 module (judge layer) + 1 site deploy + 1 ledger script. Everything else is framing existing work in the language Tier-1 recruiters are reading this quarter.

### Council's Closing Position (verbatim from chairman synthesis)

> *Sean has built the system. He has not yet named it in the vocabulary of Nate's 2026 corpus. The conversion from "interesting candidate" to "Tier-1 must-talk" is roughly 80% framing surface and 20% one piece of missing control architecture (the judge layer). The single sharpest insight came from Gemini Pro: do not let Nate's OpenClaw framing tempt Sean into claiming architectural ground his coding level can't defend in a technical screen. Sean's edge is **semantic product architecture** — specs, governance, routing, memory, authority, review. Stay there.*

---

## Execution Handoff

This document is the unified roadmap. The master plan stays canonical; this layers on top. The intended starting point for Sean is:

1. **This week (May 6–11):** Task 0 (Block IP scrub), Task 1 (canonical home + 4Q template), and Decision 1 (Track-C scope lock by Wednesday). Task 2 (Phase D + Phase 6 `EXPLANATION.md` commits) ships Friday Week 1.

2. **Week 2 (May 12–22):** **AMENDED 2026-05-10.** Primary deliverable Friday Week 2 is now the **Vault Synthesizer Eval Suite (Task 8)** + Substack post 1 ("The Night My Vault Said Nothing" — Sedaris draft). Bring [`2026-05-10-eval-suite-build-plan.md`](2026-05-10-eval-suite-build-plan.md) into Claude Code + `obra/superpowers` Plan Mode early in the week; execute Phases 1–7 across the week's deep-work blocks. Task 6 §B + §F (agent-fleet audit + Gmail labels) Saturday 2026-05-09 (already past — slipped to Saturday 2026-05-16). Task 6 §E (target-30 list) still due 2026-05-18. The 14-Agent Fleet Loom (Task 5 Step 1) bumps to Friday Week 3 as the follow-up post.

3. **Weeks 3–4:** Master plan Phase 4 Tasks 4.1–4.3 (the actual MCP server build). This roadmap's Task 3 wraps it. Ship 2026-05-25.

4. **Weeks 5–8:** Inherit master plan as written. Animation pipeline ships June 11. Phase 8 (offers) lands as it lands.

The plan respects every Tier-A truth, fills the 9 operating-model gaps, and produces 5 flagship artifacts + 2 supporting artifacts in 8 weeks — all of which are publications of work Sean has already done. No new skills to learn. No credentials to chase. No platform bets that aren't reversible.

**Amendment 2026-05-10:** The plan now produces **6 flagship + 2 supporting + 1 post-employment-specced** — the eval-suite addition (Task 8) and the Substack-Drafter agent spec (Task 9). The eval suite shipped because doing the error-analysis Step 0 cheaply (one afternoon of log-reading) turned a hypothetical "Week 5 fluency" item into a concrete Week-2 ship with a stronger interview narrative than any other artifact in the set. The Substack-Drafter agent was specced because designing it now informs the voice-rotation surface of the eval-suite's published artifact and closes a real publishing-cadence risk; building it stays post-employment to protect Track-C.

Onwards.
