---
type: template
template: explanation-4q
domain: [knowledge]
created: 2026-05-06
ai-context: "Comprehension artifact template — 4-question structure per Nate B Jones convention + ADR tradition. Source-of-truth scaffold for `EXPLANATION.md` files co-located with code/projects across this repo. The 4 questions force the author to make their reasoning legible to a reader who knows nothing about the artifact: what it is, why this shape, what would break it, what the non-obvious insight is. Used across the public-portfolio push to attach a comprehension layer to existing artifacts (Phase D typed reasoning edges, Phase 6 knowledge loop, intent-engineering MCP server, agentic financial-research fleet, animation pipeline, etc.)."
---

# `EXPLANATION-template.md` — 4-Question Comprehension Scaffold

> **For Sean:** Copy the block below to a new `EXPLANATION.md` co-located with the artifact (e.g., `agents-sdk/lib/concept_edges/EXPLANATION.md`). Replace placeholders. Aim for the file to be readable cold by a recruiter or fresh teammate in <90 seconds — if longer, the "What is this?" paragraph is too long; cut.

---

## Frontmatter + body to copy

```markdown
---
artifact: <slug>
created: <YYYY-MM-DD>
ai-context: "Comprehension artifact for <slug>. 4-question template per Nate B Jones / ADR convention."
---

# <Artifact Name> — Explanation

## What is this?
<2–4 sentences. What it does, where it lives, who/what it's for. Lead with the value, not the implementation. A reader should be able to repeat back what the thing does after one pass.>

## Why this approach?
<3 options considered. Chose option X because Y. Trade-offs accepted. The honesty about what was rejected is the load-bearing part — it shows judgment, not just preference.>

## What would break?
<3 named failure modes with detection signals. For each: how would you notice it broke, not just what would break. "Schema drift between the skill and the MCP tool descriptions — versioning needed" beats "could break.">

## What did I learn?
<2–3 sentences. The non-obvious insight that travels beyond this artifact — the thing a reader could apply to their own work even if they never touch this codebase. If the insight reduces to "I figured out how the API works," it's too small; keep digging.>
```

---

## How to use this template

1. **Find the artifact.** Pick a piece of work that has a stable home (a repo, a folder, a published page). The 4Q file lives next to it as `EXPLANATION.md`.
2. **Replace placeholders.** Set `artifact:` to the slug (lowercase-hyphenated). Set `created:` to today. The `ai-context:` line is fine as-is.
3. **Answer in order.** What → Why → What would break → What I learned. Resist the urge to write the "learned" section first; the first three sections force the rigor that makes the fourth section honest.
4. **Read it cold.** Open in a private browser window. Time how long it takes to grok. <90 seconds = ship. >90 seconds = cut the "What is this?" paragraph until it's <90.
5. **Co-locate.** Commit the `EXPLANATION.md` file in the same folder as the artifact it explains. The filename is uniform across the repo (`EXPLANATION.md`), so a reader scanning a folder tree always knows where the comprehension layer lives.

## Why this template exists

Comprehension is the durable PM skill in the agent era — the half of an artifact that survives when execution is cheap. The Karpathy synthesis frames "the explanation artifact in the generative era is essentially what the commit message was in the traditional software engineering era." Both Nate-2 sources land on a 4Q-style template as the practice-first move.

The template is canonical across this repo. The personal site `/transactions/` route surfaces these files publicly; recruiters read the explanation, not the code. The `community-skills/comprehension-audit/` skill (stub planned Week 4) audits a repo for missing or under-developed `EXPLANATION.md` files using this exact 4Q structure as the scoring rubric.

## Anti-patterns

- **The marketing pitch.** "What is this?" is not a sales section. State what it does, not why anyone should care.
- **The implementation walkthrough.** "Why this approach?" is not a code tour. Three options + one chosen + trade-offs. If you're writing pseudocode in this section, you've drifted.
- **The denial.** "What would break?" is not "nothing, this is bulletproof." Three named failure modes with detection signals. If you can't list three, you don't understand the artifact yet.
- **The resume bullet.** "What did I learn?" is not "I learned how to use TypeScript." The non-obvious insight that travels — something a reader could steal and apply elsewhere.
