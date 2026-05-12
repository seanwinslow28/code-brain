---
type: roadmap
project: prj-job-hunt-2026
status: draft
created: 2026-05-06
last_updated: 2026-05-12
synthesis_sources: [karpathy-sequoia, nate-credentials-opus, nate-credentials-gpt, nate-comprehension-opus, nate-comprehension-gpt]
amendments:
  - 2026-05-10: Added Task 8 (Eval Suite ship Week 2) + Task 9 (Substack-Drafter agent post-employment). Upgraded Task 6 §I from fluency-only to planned ship. Added Kerouac voice variant test to Decision 4. Updated portfolio count from 5+2 to 6+2+1. See [`2026-05-10-eval-suite-build-plan.md`](2026-05-10-eval-suite-build-plan.md).
  - 2026-05-12: **Track-C v0 SHIPPED 13 days early.** npm publish + MCP registry publish both live. `@swins/intent-engineering-mcp@0.1.0` on registry.npmjs.org; `com.seanwinslow/intent-engineering@0.1.0` on registry.modelcontextprotocol.io via DNS-verified domain namespace. Task 3 ship-gate items 1–16 closed; 17–19 (Loom + LinkedIn + Substack) remain. Added "Publish + registry flow — frozen reference" subsection to Task 3 capturing the DNS auth mechanics (Ed25519 keypair + TXT record on apex) so the flow is reproducible for the next MCP server without re-derivation.
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

**Maps to:** Master plan Phase 2 Task 2.4 (GitHub README pass) and Phase 3 Task 3.3 (public announcement decision).

**Files:**
- Create: `vault/40_knowledge/templates/EXPLANATION-template.md` (the 4Q template scaffold)
- Create: `<personal-site>/src/pages/transactions/index.astro` (route stub — list of artifacts)
- Modify: [`README.md`](../../../../README.md) — add "Why this exists" section in Karpathy framing

**- [ ] Step 1: Write the 4Q template scaffold.**
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

**- [ ] Step 2: Commit the template + add a `community-skills/comprehension-audit/` skill stub.**
Stub the skill that runs the 4Q audit on a repo (per Claude-Nate-2 §5.3). Full implementation deferred — Sean ships the template now and adds the skill in Week 4 once 3+ artifacts have used it.

**- [ ] Step 3: Skeleton the personal site `/transactions/` route.**
Astro 5 + React islands per Sean's existing portfolio plan. One page, one heading ("Transactions"), an empty `<ul>` that will list the artifacts. Don't wait for polish — empty list is fine.

**- [ ] Step 4: Rewrite the Superuser Pack README opening paragraph.**
Lead with "agentic engineering practitioner toolkit" framing. One paragraph max. Karpathy's "agentic engineering" definition + Sean's specific stack (117 skills, 13 hooks, 14 SDK agents, 3 primary domains).

**- [ ] Step 5: Commit.**
```bash
git add vault/40_knowledge/templates/EXPLANATION-template.md README.md
git commit -m "feat(docs): add 4Q EXPLANATION template + reframe README for agentic-engineering positioning"
```

**Verification gate:** Personal site loads at `localhost:4321/transactions/` with one empty page. README opening paragraph stands alone as a recruiter-readable pitch.

---

### Task 2 — Commit pre-drafted 4Q `EXPLANATION.md` files for two existing public artifacts (Phase 2 wrapper, ships Friday Week 1)

**Maps to:** Master plan Phase 2 Task 2.4 + Karpathy synthesis Part 5 ("explain what you've already built").

**Files:**
- Create: `agents-sdk/lib/concept_edges/EXPLANATION.md` (Phase D typed reasoning edges)
- Create: `agents-sdk/agents/knowledge_loop/EXPLANATION.md` (Phase 6 producer + consumer)
- Modify: `<personal-site>/src/pages/transactions/index.astro` (add 2 entries)

**- [ ] Step 1: Paste Claude-Nate-2 §2a verbatim into Phase D `EXPLANATION.md`.**
Source: [`claude-nate-prompt-2-analysis.md`](reference-synthesis-docs/claude-nate-prompt-2-analysis.md) lines 17–25 (the §2a "Phase D Typed Reasoning Edges" 4Q block). Copy the four sections (`What is this?` / `Why this approach?` / `What would break?` / `What did I learn?`) into the new file with the EXPLANATION-template frontmatter from Task 1.

**- [ ] Step 2: Paste Claude-Nate-2 §2e verbatim into Phase 6 `EXPLANATION.md`.**
Source: [`claude-nate-prompt-2-analysis.md`](reference-synthesis-docs/claude-nate-prompt-2-analysis.md) lines 57–65 (the §2e "Knowledge-Loop Phase 6" 4Q block).

**- [ ] Step 3: Add both to the `/transactions/` page.**
Two entries, each with: artifact name, one-sentence value-prop, link to the GitHub `EXPLANATION.md`, link to the underlying code/folder.

**- [ ] Step 4: Verify each `EXPLANATION.md` is recruiter-readable cold.**
Open in private browser. Time how long it takes a fresh reader to understand what the artifact is and why it matters. Target: <90 seconds. If longer, the "What is this?" paragraph is too long; cut it.

**- [ ] Step 5: Commit.**
```bash
git add agents-sdk/lib/concept_edges/EXPLANATION.md agents-sdk/agents/knowledge_loop/EXPLANATION.md
git commit -m "docs: add 4Q comprehension artifacts for Phase D typed edges + Phase 6 knowledge loop"
```

**Verification gate:** This is Friday Week 1's published artifact. Substack post for Week 1 syndicates these two `EXPLANATION.md` files with one paragraph of editorial framing.

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

**§E — Target list of 30 companies.** **DECIDED THIS WEEK as a Week-2 deliverable.** Owner: Sean. Deadline: 2026-05-18 (end of master plan Phase 2). Approach: one 90-min session in Week 2 reviewing Built In Boston + LinkedIn Jobs + Anthropic/Sierra/Decagon/Glean/Robinhood/Scale/Pair careers pages. Output: `vault/20_projects/prj-job-hunt-2026/target-companies.md` with 10 Tier-1 + 15 Tier-2 + 5 Tier-3 (master plan Phase 5 Task 5.1 schema).

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

## Execution Handoff

This document is the unified roadmap. The master plan stays canonical; this layers on top. The intended starting point for Sean is:

1. **This week (May 6–11):** Task 0 (Block IP scrub), Task 1 (canonical home + 4Q template), and Decision 1 (Track-C scope lock by Wednesday). Task 2 (Phase D + Phase 6 `EXPLANATION.md` commits) ships Friday Week 1.

2. **Week 2 (May 12–22):** **AMENDED 2026-05-10.** Primary deliverable Friday Week 2 is now the **Vault Synthesizer Eval Suite (Task 8)** + Substack post 1 ("The Night My Vault Said Nothing" — Sedaris draft). Bring [`2026-05-10-eval-suite-build-plan.md`](2026-05-10-eval-suite-build-plan.md) into Claude Code + `obra/superpowers` Plan Mode early in the week; execute Phases 1–7 across the week's deep-work blocks. Task 6 §B + §F (agent-fleet audit + Gmail labels) Saturday 2026-05-09 (already past — slipped to Saturday 2026-05-16). Task 6 §E (target-30 list) still due 2026-05-18. The 14-Agent Fleet Loom (Task 5 Step 1) bumps to Friday Week 3 as the follow-up post.

3. **Weeks 3–4:** Master plan Phase 4 Tasks 4.1–4.3 (the actual MCP server build). This roadmap's Task 3 wraps it. Ship 2026-05-25.

4. **Weeks 5–8:** Inherit master plan as written. Animation pipeline ships June 11. Phase 8 (offers) lands as it lands.

The plan respects every Tier-A truth, fills the 9 operating-model gaps, and produces 5 flagship artifacts + 2 supporting artifacts in 8 weeks — all of which are publications of work Sean has already done. No new skills to learn. No credentials to chase. No platform bets that aren't reversible.

**Amendment 2026-05-10:** The plan now produces **6 flagship + 2 supporting + 1 post-employment-specced** — the eval-suite addition (Task 8) and the Substack-Drafter agent spec (Task 9). The eval suite shipped because doing the error-analysis Step 0 cheaply (one afternoon of log-reading) turned a hypothetical "Week 5 fluency" item into a concrete Week-2 ship with a stronger interview narrative than any other artifact in the set. The Substack-Drafter agent was specced because designing it now informs the voice-rotation surface of the eval-suite's published artifact and closes a real publishing-cadence risk; building it stays post-employment to protect Track-C.

Onwards.
