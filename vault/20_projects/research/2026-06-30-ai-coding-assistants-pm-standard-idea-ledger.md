# Idea Ledger — AI coding assistants

- **Lens:** `pm`  **Tier:** `standard`  **Verified ideas:** 8
- **Cost:** $1.85  ·  Pain points dropped by verification: 2

## ⭐ Whitespace Map — what this run MISSED

> Gaps below = absence-of-evidence (what the panel and evidence did **not** surface), NOT verified claims or confirmed opportunities. They are **ranked most-distinct-first** — by dissimilarity to what this run actually surfaced, which is an ordering signal, **not a severity or confidence score** (a blind spot has no supporting evidence by definition). The next move for each gap is to **investigate** it — never to build on it. Absence of a surfaced gap is not proof of full coverage.

**Sharpen the next run:**
1. Backfill the 6 gaps below with the agent's own WebSearch/WebFetch (solution-side) — do this first.
2. Add `--segment <audience>` to focus the gather.

**Gaps the panel/evidence missed (ranked most-distinct-first):**
1. Limited non-English and enterprise-procurement perspective; segments skew toward indie/hobbyist vibe coders and US tech press.
   → Backfill (agent WebSearch/WebFetch, solution-side) — lands in **Web Supplement (gap-fill)** below.
2. CodeRabbit analysis quote is truncated in the evidence ('had 1.'), so the actual defect/severity finding is unknown.
   → Backfill (agent WebSearch/WebFetch, solution-side) — lands in **Web Supplement (gap-fill)** below.
3. Positive/success stories (e.g., shipping a game without coding, internal tooling wins) are present but underexplored as counter-signal context.
   → Backfill (agent WebSearch/WebFetch, solution-side) — lands in **Web Supplement (gap-fill)** below.
4. Evidence is heavily weighted toward Reddit, GitHub, and aggregator/blog summaries; little first-party telemetry or quantified productivity data beyond cited surveys.
   → Backfill (agent WebSearch/WebFetch, solution-side) — lands in **Web Supplement (gap-fill)** below.
5. Refusal-to-help behavior is referenced (Cursor telling a user to learn programming) but only as a headline with no clustered user-impact discussion in the rest of the evidence.
   → Backfill (agent WebSearch/WebFetch, solution-side) — lands in **Web Supplement (gap-fill)** below.
6. No evidence on latency/performance/speed of suggestions as a standalone pain point despite 'reliability over speed' framing.
   → Backfill (agent WebSearch/WebFetch, solution-side) — lands in **Web Supplement (gap-fill)** below.

## Ranked Opportunities

> 🧾 **Receipts** show evidence *depth*, not a verdict — every ranked item already cleared the anti-fabrication gate. **Corroboration** = independent source domains backing the pain (two-source rule: 1 = single-source, 2 = corroborated, 3+ = well-corroborated). **Freshness** = how recent the evidence is — a freshness signal, **not** proof; old pain can still be real.

### 1. Context blindness & codebase awareness failures  ·  score 54/100
🧾 corroborated · 2 independent domains  ·  aging · evidence 2025-08-01
- **Who:** Professional developers / enterprise teams
- **Pain (their words):** Context awareness is a major issue: assistants understand code well but often fail to retain or fetch relevant context.
  - Context blindness & codebase awareness failures: AI assistants fail to retain or fetch relevant context, ignore existing codebase conventions, and don't align with established architectural patterns.
- **Evidence:** https://arxiv.org/html/2508.12285v1, https://www.youtube.com/watch?v=91B_v-wOaws  ·  2 independent domain(s)
- **Size:** importance 4/5 · reach 1.00 (3094180 engagement, 2 sources, 2 domains) · recency 0.30
- **Confidence:** 0.66× (sources 0.47, consensus 0.00)  →  value 0.81 × conf = 54/100
- **Why now:** Older signal (evidence 2025-08-01); confirm it's still live.
- **Proposed bet** _(heuristic — confirm against evidence)_
  - Shape: missing-capability
  - Riskiest assumption: that the capability is genuinely absent, not just undiscovered in existing tools
  - Cheapest test: a 5-tool teardown — does any competitor already solve this before you build?
  - _Your call: _________________________________

### 2. Near-correct but unreliable code output  ·  score 44/100
🧾 well-corroborated · 3 independent domains  ·  aging · evidence 2026-01-01
- **Who:** Professional developers and vibe coders
- **Pain (their words):** "Almost right, but not quite" – chronic correctness and quality issues - A large share of developers say the core frustration is near-miss correctness: code that compiles but is subtly wrong.
  - Near-correct but unreliable code output: Developers report AI assistants frequently produce code that compiles and looks plausible but is subtly wrong, requiring constant correction and sometimes introducing cascading bugs.
- **Evidence:** https://uvik.net/blog/ai-coding-assistant-statistics/, https://www.smiansh.com/blogs/the-real-struggle-with-ai-coding-agents-and-how-to-overcome-it/, https://spectrum.ieee.org/ai-coding-degrades  ·  3 independent domain(s)
- **Size:** importance 5/5 · reach 0.23 (0 engagement, 3 sources, 3 domains) · recency 0.30
- **Confidence:** 0.75× (sources 0.70, consensus 0.00)  →  value 0.58 × conf = 44/100
- **Why now:** Older signal (evidence 2026-01-01); confirm it's still live.
- **Proposed bet** _(heuristic — confirm against evidence)_
  - Shape: trust-gap
  - Riskiest assumption: that users will trust an automated correctness check enough to rely on it
  - Cheapest test: 5 user interviews — do they describe verification/accuracy as a top-3 pain?
  - _Your call: _________________________________

### 3. Context window degradation  ·  score 42/100
🧾 single-source · 1 domain  ·  aging · evidence 2026-04-01
- **Who:** Power users / AI engineers
- **Pain (their words):** Cuz if you have a ton of stuff in here, if you have 250K tokens, like I have seen people put in there, then that you're just going to go straight into the dumb zone without even being able to do anything.
  - Context window degradation: Overloading the context window with too many tokens degrades model performance, pushing it into a 'dumb zone'.
- **Evidence:** https://www.youtube.com/watch?v=-QFHIoCo-Ko  ·  1 independent domain(s)
- **Size:** importance 3/5 · reach 1.00 (5477845 engagement, 1 sources, 1 domains) · recency 0.30
- **Confidence:** 0.58× (sources 0.23, consensus 0.00)  →  value 0.71 × conf = 42/100
- **Why now:** Older signal (evidence 2026-04-01); confirm it's still live.
- **Proposed bet** _(heuristic — confirm against evidence)_
  - Shape: missing-capability
  - Riskiest assumption: that the capability is genuinely absent, not just undiscovered in existing tools
  - Cheapest test: a 5-tool teardown — does any competitor already solve this before you build?
  - _Your call: _________________________________

### 4. Tool choice confusion (which AI to pick)  ·  score 39/100
🧾 corroborated · 2 independent domains  ·  fresh · evidence 2026-06-01
- **Who:** Hobbyists / vibe coders / non-coders
- **Pain (their words):** Best price-to-performance AI coding agents right now (beyond GitHub Copilot)?
  - Tool choice confusion (which AI to pick): Users repeatedly ask which AI coding tool to choose, especially seeking free or best price-to-performance options, indicating decision fatigue and a crowded, confusing landscape.
- **Evidence:** https://www.reddit.com/r/vibecoding/comments/1udf4jg/best_pricetoperformance_ai_coding_agents_right/, https://www.reddit.com/r/vibecoding/comments/1ugw5fx/can_anyone_recommend_an_aifree/, https://www.reddit.com/r/vibecoding/comments/1uhofmi/whats_the_best_ai_to_vibe_code/, https://reddit.com/r/aigamedev/comments/1ug5f5w/comment/otx5wb9/  ·  2 independent domain(s)
- **Size:** importance 3/5 · reach 0.59 (50 engagement, 2 sources, 2 domains) · recency 0.51
- **Confidence:** 0.66× (sources 0.47, consensus 0.00)  →  value 0.58 × conf = 39/100
- **Why now:** Fresh signal — evidence dated 2026-06-01.
- **Proposed bet** _(heuristic — confirm against evidence)_
  - Shape: cost-pain
  - Riskiest assumption: that price, not value perception, is the actual blocker to adoption
  - Cheapest test: a pricing-page / willingness-to-pay test against the current workaround's cost
  - _Your call: _________________________________

### 5. Missing agent features (hooks, background exec, file exclusion)  ·  score 36/100
🧾 single-source · 1 domain  ·  aging · evidence 2025-06-01
- **Who:** Advanced developers / agent power users
- **Pain (their words):** Configurable file exclusion patterns for sensitive files
  - Missing agent features (hooks, background exec, file exclusion): Users file feature requests for missing agent capabilities including configurable sensitive-file exclusion, background bash execution, lifecycle hooks, and MCP transport support.
- **Evidence:** https://github.com/openai/codex/issues/1397, https://github.com/github/copilot-cli/issues/1157, https://github.com/aws/amazon-q-developer-cli/issues/2096  ·  1 independent domain(s)
- **Size:** importance 3/5 · reach 0.67 (100 engagement, 3 sources, 1 domains) · recency 0.30
- **Confidence:** 0.62× (sources 0.35, consensus 0.00)  →  value 0.58 × conf = 36/100
- **Why now:** Older signal (evidence 2025-06-01); confirm it's still live.
- **Proposed bet** _(heuristic — confirm against evidence)_
  - Shape: missing-capability
  - Riskiest assumption: that the capability is genuinely absent, not just undiscovered in existing tools
  - Cheapest test: a 5-tool teardown — does any competitor already solve this before you build?
  - _Your call: _________________________________

### 6. OSS community backlash against low-effort AI contributions  ·  score 34/100
🧾 single-source · 1 domain  ·  aging · evidence 2026-03-01
- **Who:** Open-source maintainers
- **Pain (their words):** Consider not allowing LLM and AI contributions
  - OSS community backlash against low-effort AI contributions: Open-source projects are proposing policies to restrict or ban low-effort LLM/AI-generated contributions.
- **Evidence:** https://github.com/mastodon/mastodon/issues/38072, https://github.com/rust-lang/leadership-council/issues/273  ·  1 independent domain(s)
- **Size:** importance 3/5 · reach 0.62 (92 engagement, 2 sources, 1 domains) · recency 0.30
- **Confidence:** 0.60× (sources 0.29, consensus 0.00)  →  value 0.56 × conf = 34/100
- **Why now:** Older signal (evidence 2026-03-01); confirm it's still live.
- **Proposed bet** _(heuristic — confirm against evidence)_
  - Shape: missing-capability
  - Riskiest assumption: that the capability is genuinely absent, not just undiscovered in existing tools
  - Cheapest test: a 5-tool teardown — does any competitor already solve this before you build?
  - _Your call: _________________________________

### 7. Cost/pricing pain (subscriptions & credit drain)  ·  score 30/100
🧾 single-source · 1 domain  ·  fresh · evidence 2026-06-01
- **Who:** Indie developers / hobbyists / vibe coders
- **Pain (their words):** I built a free AI coding assistant because I couldn't afford Cursor subscription.
  - Cost/pricing pain (subscriptions & credit drain): Users find paid tools like Cursor unaffordable and report that agents can drain credits while leaving more problems than they started with, motivating free alternatives.
- **Evidence:** https://www.reddit.com/r/SideProject/comments/1uf6aer/i_built_a_free_ai_coding_assistant_because_i/  ·  1 independent domain(s)
- **Size:** importance 3/5 · reach 0.42 (21 engagement, 1 sources, 1 domains) · recency 0.51
- **Confidence:** 0.58× (sources 0.23, consensus 0.00)  →  value 0.52 × conf = 30/100
- **Why now:** Fresh signal — evidence dated 2026-06-01.
- **Proposed bet** _(heuristic — confirm against evidence)_
  - Shape: cost-pain
  - Riskiest assumption: that price, not value perception, is the actual blocker to adoption
  - Cheapest test: a pricing-page / willingness-to-pay test against the current workaround's cost
  - _Your call: _________________________________

### 8. Security & data leakage risks  ·  score 25/100
🧾 single-source · 1 domain  ·  aging · evidence 2025-01-01
- **Who:** Enterprise / security-conscious developers
- **Pain (their words):** If code, credentials, or production data leave your environment through an AI assistant, you cannot guarantee deletion or control over where that data ends up.
  - Security & data leakage risks: AI-generated code frequently contains critical security flaws, and assistants can exfiltrate code, credentials, or production data outside the user's control. Destructive behavior including data loss is also reported.
- **Evidence:** https://www.cerbos.dev/blog/productivity-paradox-of-ai-coding-assistants  ·  1 independent domain(s)
- **Size:** importance 4/5 · reach 0.07 (0 engagement, 1 sources, 1 domains) · recency 0.30
- **Confidence:** 0.58× (sources 0.23, consensus 0.00)  →  value 0.43 × conf = 25/100
- **Why now:** Older signal (evidence 2025-01-01); confirm it's still live.
- **Proposed bet** _(heuristic — confirm against evidence)_
  - Shape: missing-capability
  - Riskiest assumption: that the capability is genuinely absent, not just undiscovered in existing tools
  - Cheapest test: a 5-tool teardown — does any competitor already solve this before you build?
  - _Your call: _________________________________

## Contradiction Map

- Productivity is framed both positively (AI builds internal tooling that 'would otherwise take weeks', a non-coder shipped a game in 8 months) and negatively (assistants 'slow you down, drain your credits' and one source titled 'AI coding assistants do not boost productivity').
- Some users abandon tools because 'Copilot lies or produces bad results for a vast majority of the time' while others report substantial productivity benefits from the same class of tools.
- Trust framing conflicts: declining trust (40%->29%, 46% distrust) coexists with continued heavy adoption and reliance reflected in volume of usage and tooling requests.

## Quote Bank

- ""Almost right, but not quite" – chronic correctness and quality issues - A large share of developers say the core frustration is near-miss correctness: code that compiles but is subtly wrong." — https://uvik.net/blog/ai-coding-assistant-statistics/
- "The near-correct nature of AI output — it compiles and looks plausible, but fails in subtle ways — drives this frustration." — https://www.smiansh.com/blogs/the-real-struggle-with-ai-coding-agents-and-how-to-overcome-it/
- "Confusing "looks correct" with "is correct." — https://spectrum.ieee.org/ai-coding-degrades
- "Fixing one bug would create three new ones."
- "AI-created code would often fail with a syntax error or snarl itself up in faulty structure."
- "Context awareness is a major issue: assistants understand code well but often fail to retain or fetch relevant context." — https://arxiv.org/html/2508.12285v1
- ""We've found that AI tools will occasionally ignore key aspects of the existing codebase or fail to align with established coding standards and architectural patterns," Owens says." — https://www.youtube.com/watch?v=91B_v-wOaws
- "This lets AI fetch documentation automatically, which means I don't have to copy and paste the same documentation for the 50th time."
- "Best price-to-performance AI coding agents right now (beyond GitHub Copilot)?" — https://www.reddit.com/r/vibecoding/comments/1udf4jg/best_pricetoperformance_ai_coding_agents_right/
- "Can anyone recommend an AI?(free)" — https://www.reddit.com/r/vibecoding/comments/1ugw5fx/can_anyone_recommend_an_aifree/
- "What's the best ai to vibe code?" — https://www.reddit.com/r/vibecoding/comments/1uhofmi/whats_the_best_ai_to_vibe_code/
- "which ai did you use particularly!" — https://reddit.com/r/aigamedev/comments/1ug5f5w/comment/otx5wb9/
- "If code, credentials, or production data leave your environment through an AI assistant, you cannot guarantee deletion or control over where that data ends up." — https://www.cerbos.dev/blog/productivity-paradox-of-ai-coding-assistants
- "A 2025 study cited in recent coverage found 30–50% of sampled Copilot outputs contained critical security flaws such as SQL injection and insecure cryptography."
- "Assistants that prioritize reliability over speed, with built-in static analysis, tests, and security checks before suggestions are made."
- "Configurable file exclusion patterns for sensitive files" — https://github.com/openai/codex/issues/1397
- "Feature Request: Add Background Bash Execution (Like Claude Code's Ctrl+b)" — https://github.com/github/copilot-cli/issues/1157
- "Feature Request: Global Hooks Configuration with UserPromptSubmit, Stop, and Notification Events" — https://github.com/aws/amazon-q-developer-cli/issues/2096
- "feat: MCP Streamable HTTP Transport Support"
- "I built a free AI coding assistant because I couldn't afford Cursor subscription." — https://www.reddit.com/r/SideProject/comments/1uf6aer/i_built_a_free_ai_coding_assistant_because_i/
- "But I've learned the hard way that without the right approach, they can also slow you down, drain your credits, and leave you with more problems than you started with."
- "Consider not allowing LLM and AI contributions" — https://github.com/mastodon/mastodon/issues/38072
- "Policy proposal: No low-effort contributions" — https://github.com/rust-lang/leadership-council/issues/273
- "Cuz if you have a ton of stuff in here, if you have 250K tokens, like I have seen people put in there, then that you're just going to go straight into the dumb zone without even being able to do anything." — https://www.youtube.com/watch?v=-QFHIoCo-Ko

## Cost Summary

- Approx cost: $1.85
- Pain points dropped by verification: 2