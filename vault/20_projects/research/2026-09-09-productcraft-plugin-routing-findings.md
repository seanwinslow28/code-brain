---
title: "Productcraft plugin-suite inventory — seat routing table (pass 3)"
date: 2026-09-09
project: productcraft
status: ratified-2026-09-09
tags: [research, productcraft, plugins, pm-skills, routing]
cost: $0 (local file reads only; no web, no model spend beyond the session)
models: "inventory, routing, install-location and drift diff: Sonnet 5 · rulings on ambiguous rows, gap triage, recommendations: Fable 5.1"
---

# Productcraft plugin-suite inventory — findings brief

**Gate:** pass 3 of L5 — map every installed pm-* skill to the seat that should own it, so lane manifests point at existing skills instead of re-authoring them.

**What was inventoried:** Paweł Huryn's `pm-skills` marketplace (productcompass.pm), nine plugins, 68 skills plus 42 chained-workflow commands, read from the on-disk copy; the six archived sw-creative-toolkit skills in the vault; the Claude Code and Cowork install locations; and the Cowork custom-skills mirror. 116 items routed.

## Headline recommendation

**Adopt the routing table below as the source for every lane manifest's toolbelt, under Systemcraft's raw-material rule (a skill's output is never the artifact). Route all seven pm-ai-shipping items to Systemcraft. Treat the seven capability gaps as template tickets on the build map, four of which are already the leadership and business seats' hard contracts. Leave the archived sw-creative-toolkit archived.**

Two housekeeping findings ride along: the Claude Code copy of the suite is one point release behind Codex, with drift confined to pm-ai-shipping (Systemcraft's plugin, so Productcraft is unaffected); and eight of the fourteen repo skills mirrored into Cowork have drifted from the repo, which is a hygiene ticket outside this studio.

## Routing table (ownership = who maintains the lane pointer; any seat may invoke any skill mid-draft)

| Seat | Count | Skills and commands |
|---|---|---|
| **1 Product Strategist** | 17 | pm-product-strategy: product-strategy, product-vision, value-proposition, business-model, lean-canvas, startup-canvas, swot-analysis, pestle-analysis, porters-five-forces, ansoff-matrix, /strategy, /value-proposition, /business-model, /market-scan · pm-market-research: competitor-analysis, /competitive-analysis · sw-creative-toolkit: innovation-strategy (archived) |
| **2 Discovery Lead** | 20 | pm-product-discovery: opportunity-solution-tree, interview-script, summarize-interview, identify-assumptions-new, identify-assumptions-existing, prioritize-assumptions, brainstorm-ideas-new, brainstorm-ideas-existing, brainstorm-experiments-new, brainstorm-experiments-existing, /discover, /interview, /brainstorm · pm-market-research: user-personas, market-segments, user-segmentation, customer-journey-map, /research-users · sw-creative-toolkit: brainstorm, design-thinking (archived) |
| **3 Growth & Distribution Architect** | 14 | pm-go-to-market: growth-loops, gtm-motions, gtm-strategy, beachhead-segment, ideal-customer-profile, competitive-battlecard, /growth-strategy, /plan-launch, /battlecard · pm-marketing-growth: positioning-ideas, value-prop-statements, marketing-ideas, product-name, /market-product |
| **4 Business & Economics Modeler** | 4 | pm-product-strategy: pricing-strategy, monetization-strategy, /pricing · pm-market-research: market-sizing |
| **5 Delivery & Execution Lead** | 29 | pm-execution: create-prd, /write-prd, outcome-roadmap, /transform-roadmap, brainstorm-okrs, /plan-okrs, user-stories, job-stories, wwas, /write-stories, sprint-plan, retro, release-notes, /sprint, pre-mortem, /pre-mortem, strategy-red-team, /red-team-prd, prioritization-frameworks, test-scenarios, /test-scenarios, summarize-meeting, /meeting-notes, dummy-dataset, /generate-data · pm-product-discovery: prioritize-features, analyze-feature-requests, /triage-requests · sw-creative-toolkit: problem-solving (archived) |
| **6 Product Leadership & Org Designer** | 10 | pm-execution: stakeholder-map, /stakeholder-map · sw-creative-toolkit: storytelling, presentation (archived) · pm-toolkit (low-confidence utilities, not leadership craft): draft-nda, privacy-policy, grammar-check, /draft-nda, /privacy-policy, /proofread |
| **7 Insights & Analytics** (pending ratification 1) | 12 | pm-data-analytics: ab-test-analysis, cohort-analysis, sql-queries, /analyze-test, /analyze-cohorts, /write-query · pm-marketing-growth: north-star-metric, /north-star · pm-product-discovery: metrics-dashboard, /setup-metrics · pm-market-research: sentiment-analysis, /analyze-feedback |
| **Systemcraft** | 7 | pm-ai-shipping, the whole plugin: intended-vs-implemented, shipping-artifacts, /ship-check, /document-app, /derive-tests, /security-audit-static, /performance-audit-static |
| **Neither studio (career)** | 3 | pm-toolkit: review-resume, /review-resume, /tailor-resume |

Two routing rulings on ambiguous rows: the three canvases (business-model, lean-canvas, startup-canvas) sit with the Strategist as strategy-shape tools, with the Business seat pointing at their revenue blocks; strategy-red-team stays listed under Delivery but is the Strategist's pre-handoff self-attack, mirroring Systemcraft's Design Strategist toolbelt.

## Findings

### 1. Most "duplicates" are structural, not accidental
Thirty-seven of the 42 commands are chained wrappers around skills in the same plugin (a command runs one or several skills in sequence). Those pairs are not defects; lane manifests should point at the **skill** for mid-draft use and at the **command** when a seat wants the whole chain. The real duplicates, where two differently named items do the same job, are thirteen:

1. write-prd (command) and create-prd (skill), same plugin, same output.
2. competitive-analysis (command) and competitor-analysis (skill), the marketplace's own name drifted.
3. user-stories, job-stories, wwas: three backlog formats for one task.
4. business-model, lean-canvas, startup-canvas: three canvases for one exercise.
5. north-star-metric and metrics-dashboard / setup-metrics: both define what to measure.
6. value-proposition (strategy definition) and value-prop-statements (marketing copy from it).
7. pre-mortem and strategy-red-team: two attack techniques on one plan.
8. market-segments and user-segmentation, near-identical.
9. ideal-customer-profile, user-personas, market-segments: three lenses on "who is the customer."
10. sw-creative-toolkit innovation-strategy duplicates the whole pm-product-strategy plugin.
11. sw-creative-toolkit design-thinking mirrors the whole pm-product-discovery plugin.
12. competitive-battlecard and competitor-analysis: sales output versus research brief.
13. grammar-check and /proofread.

Lane manifests resolve these by naming one preferred entry per job and listing the alternates as "same job, different format."

### 2. Seven capability gaps, four of them already locked as hard contracts
| Seat | Gap (no installed skill covers it) | Disposition |
|---|---|---|
| Strategist | Point-of-view statement | Template ticket |
| Growth | Activation and retention playbook (cohort curves exist under Insights; nothing interprets them into strategy) | Template ticket |
| Growth | Growth-experiment design distinct from generic assumption tests | Template ticket, co-signed by Insights |
| Business | Unit-economics model (LTV, CAC, payback) | Template ticket, part of the seat's artifact contract |
| Business | Business case / ROI document | Template ticket, part of the seat's artifact contract |
| Leadership | Decision memo | Already an L3 hard contract; template ticket |
| Leadership | Operating-model document | Already an L3 hard contract; template ticket |

The Business seat is the tool-poorest by a wide margin (4 items, none of them its core artifact). Discovery and Delivery are fully covered: every phrase in their seat descriptions maps to at least one installed skill.

### 3. Systemcraft gets one plugin, cleanly
Every pm-ai-shipping item is code-shipping machinery for AI-built software (intent-versus-implementation gaps, static security and performance audits, test-coverage maps). Nothing else in the suite touches code, model choice, or evals. Systemcraft's seat toolbelts do not yet list these; that is a Systemcraft follow-up, not a Productcraft build step.

### 4. The archived sw-creative-toolkit is the only source for three capabilities
Storytelling and presentation (Leadership) and problem-solving (Delivery) exist nowhere in the live pm-skills suite. The archive at vault/60_archive is not loadable as skills. Recommendation: do not resurrect it. The Leadership seat's narrative work is governed by its template and corpus (the six-page narrative and PR/FAQ from *Working Backwards*), not by a framework-list skill; problem-solving techniques are corpus material for the Delivery lane.

### 5. Install locations and drift
- **Claude Code / Cowork copy found** in a session-scoped plugin cache under the Claude app's Library folder (`local-agent-mode-sessions/.../rpm/plugin_<opaque-id>/`), keyed by opaque IDs, which is why name-based searches under `~/.claude/plugins` and Spotlight miss it. Version **2.0.0**; the Codex copy is **2.1.0**. Skill and command counts match exactly; 103 of 110 files are byte-identical; all seven differing files are in pm-ai-shipping. Productcraft's lanes are unaffected by the version gap.
- **Cowork custom-skills mirror** holds 41 uploaded skills and **no pm-* or sw-creative-toolkit skills**; the PM suite reaches Cowork only through the plugin cache above. Of the 14 mirrored skills that also exist in this repo, 6 match and **8 have drifted** (2d-animation-principles, creative-director, etf-page-creator, prompt-engineering, screenwriting-modes, skill-system-mastery, writing-voice-modes, wwf5d). Filed as a rule-8 hygiene ticket; not Productcraft's.

## Decisions requested (Sean)

1. Ratify the routing table as the lane-manifest toolbelt source, with the raw-material rule inherited from Systemcraft.
2. Ratify routing pm-ai-shipping to Systemcraft and filing a Systemcraft toolbelt follow-up.
3. Ratify the seven gaps as template tickets on the build map, and the Business seat flagged tool-poor.
4. Ratify leaving sw-creative-toolkit archived.

## Sources
`~/.codex/plugins/cache/pm-skills/` (2.1.0) · `~/.codex/.tmp/marketplaces/pm-skills/.claude-plugin/marketplace.json` · the Claude app plugin cache `rpm/manifest.json` (2.0.0) · `vault/60_archive/sw-creative-toolkit-bmad/skills/` · the Cowork skills-plugin mirror (see the cowork-custom-skills-local-mirror memory for the path pattern) · md5 comparisons per SKILL.md.

## Decision record (ratified by Sean, 2026-09-09)

1. **Ratified:** the routing table is the lane-manifest toolbelt source, under Systemcraft's raw-material rule.
2. **Ratified:** all seven pm-ai-shipping items route to Systemcraft; a Systemcraft toolbelt follow-up is filed as a rule-8 ticket.
3. **Ratified:** the seven capability gaps become template tickets on the build map; the Business & Economics seat is flagged tool-poor.
4. **Ratified:** sw-creative-toolkit stays archived; its storytelling, presentation, and problem-solving capabilities are covered by templates and corpus, not resurrected skills.
5. The Cowork mirror drift (8 of 14 shared skills) is filed as a rule-8 hygiene ticket outside this studio.
