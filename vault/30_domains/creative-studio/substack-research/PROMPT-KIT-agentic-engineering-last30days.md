---
title: "Prompt Kit — Agentic Engineering / Frameworks last30days research (niche-locked)"
type: prompt-kit
domain: [creative-studio]
created: 2026-06-09
purpose: "Hand to Claude Code (which has the last30days skill + keys) to research the agentic-engineering angle and write reports matching the existing substack-research set."
niche_lock: "agentic engineering ∩ creative/SaaS/UX/marketing AI + plugins/skills/MCPs — anchored to Sean's intent-engineering + vault-knowledge MCPs. Aim at the INTENT/EVAL/GOVERNANCE layer (Sean's win); avoid orchestration-INFRASTRUCTURE (a capital/eng play, per the prior reports' own conclusion)."
related: [2026-06-09-claude-code-skills-mcp-gaps-and-opportunities, 2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days, 2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days, tool-shipping-playbook]
---

# Prompt Kit — Agentic Engineering, niche-locked

Paste this whole file to Claude Code. It runs three `last30days` passes, mines each
for the niche, and writes one report that matches the format of the existing
`substack-research/` reports. It deepens the niche (agentic engineering as the
*enabling layer* for the creative/SaaS/UX/marketing shift) instead of wandering into
generic dev-agent territory.

## Standing context for the research (read before running)

- **The niche stays locked.** We are NOT researching agent infrastructure for its own
  sake. We research the **intent → eval → governance** layer of agentic engineering —
  making agents do what a human *meant*, proving they did, and keeping a human in
  control — and specifically where that layer touches **creative / SaaS / UX /
  marketing teams**, not just backend engineers.
- **This is anchored to Sean's two shipped MCPs** (ground Part 3 in these, do not
  invent capabilities):
  - **`intent-engineering` MCP** — a 3-tool TypeScript MCP (`audit_intent_spec`,
    `generate_intent_spec_scaffold`, `assess_retrofit_level`), published to npm
    (`@swins/intent-engineering-mcp`) and the MCP registry. Thesis: *the audit IS the
    eval* — it scores a spec against the framework before that spec ships to a coding
    agent. Operationalizes "evals are the new PRDs."
  - **`vault-knowledge` MCP** — turns a personal knowledge base into queryable
    concepts joined by **typed reasoning edges** (`concept_edges`: supports /
    contradicts / evolved_into / supersedes / depends_on / related_to).
  - Plus the surrounding assets: the writing chain (storytelling-architecture →
    substack-value-engine → writing-voice-modes → writing-critique →
    writing-humanity-pass), the **VoicePrint** plugin, the **design-team agents**
    (UI Reviewer, Accessibility Checker, Design System Enforcer, Visual Polish
    Auditor), **Code-Brain** (118 skills / 17 SDK agents), and the **anima** pipeline.
- **The guardrail from the prior research (honor it):** Sean is well-positioned for the
  *judgment / intent / ownership* gaps and badly positioned for *infrastructure* gaps
  (orchestration engines = Zapier/n8n/LangGraph territory = capital/eng plays, and the
  research called them an "org-maturity problem," not a solo-builder software gap).
  When a gap is pure infra, say so and mark it NOT-Sean.
- **No-prime discipline:** keep the `last30days` queries LEAN (below). Do NOT paste
  this framing into the scrape query — it biases the pull toward confirming us. Apply
  the framing only in the post-scrape synthesis + the report, exactly like the
  existing reports did.

## Step 1 — Run these three `last30days` passes (lean queries)

```
/last30days biggest frustrations building AI agents and agentic workflows --deep
/last30days AI agent frameworks people wish existed and what is missing
/last30days spec-driven development and evals for AI agents
```

(Optional 4th, only if you want the team-adoption angle sharpened — it anchors the
niche hardest:)

```
/last30days how creative and marketing teams are adopting AI agents
```

## Step 2 — After EACH pass, run this mining follow-up (verbatim)

```
From the research you just pulled, not from what I'm telling you: what are the
loudest unmet needs and the gaps nobody is filling in AGENTIC ENGINEERING —
specifically the layer of (a) making agents reliably do what the human INTENDED
(specs / intent), (b) PROVING they did it (evals), and (c) keeping a human in
CONTROL (governance, gates, review)? Quote the exact words people use. Rank by how
often it came up × how unserved it is. Be blunt about what would be genuinely hard
to build, and about what is pure infrastructure I should NOT touch as a solo builder.

Then, separately, call out which of these gaps land on CREATIVE / SaaS / UX /
MARKETING teams specifically (people who are not backend engineers) — that is the
niche I serve, and I want the slice that helps them, not just the slice that helps
framework authors.
```

## Step 3 — Build the report (match the existing format)

Write ONE report to `vault/30_domains/creative-studio/substack-research/` named
`YYYY-MM-DD-agentic-engineering-intent-eval-governance-gaps.md`, with the same shape
as `2026-06-09-claude-code-skills-mcp-gaps-and-opportunities.md`:

- **Frontmatter** — title, type: research, domain, tags, date-range, sources,
  coverage, tool, an `ai-context` summary, and `related:` linking the three existing
  `substack-research` reports + `tool-shipping-playbook` + `voiceprint-plugin-build-spec`.
- **Quick verdict** — 3-4 sentences, the single most important finding.
- **Part 1 — What people most ask for / struggle with** (the findings, with verbatim
  quotes + engagement counts + source links).
- **Part 2 — The gaps nobody is filling**, ranked by frequency × unservedness, each
  with a verbatim quote and an honest "hard to build because…" note. Tag each gap
  **Sean-niche** (intent/eval/governance, creative-team-facing) or **NOT-Sean**
  (pure orchestration infra / capital play).
- **Part 3 — How Sean is positioned**, mapped to the REAL assets above (lead with the
  **intent-engineering MCP** for the spec/eval gaps and **vault-knowledge MCP** for
  the memory/provenance gaps; do not invent capabilities). Note honest risks.
- **Part 4 — Clean-sheet build ideas**, grounded only in the gaps, each naming the gap
  it hits + the genuinely hard part. Bias toward **gates and lenses, not generators**
  (the prior reports' conclusion).
- **Methodology & sources** — counts, raw-dump path, top voices, a confidence note,
  and `related:` cross-links.

Cross-reference the three existing reports so this reads as the agentic *deepening* of
the same niche, and flag any overlap rather than repeating it.

## Step 4 — Hand back

Paste the new report (or its path) to the Cowork session. It folds into the combined
**opportunity report** (ranked idea backlog → new-MCP shortlist adjacent to
intent-engineering + vault-knowledge → positioning brief → Substack series plan)
alongside the three existing reports.
