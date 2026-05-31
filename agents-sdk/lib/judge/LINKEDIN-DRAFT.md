---
type: linkedin-draft
artifact: judge-layer
created: 2026-05-31
ai-context: "LinkedIn post draft for the judge-layer ship (Task 12 Step 8). ~120 words, Sean's hand on the final per Tier-A. Tags Anthropic + the FDE-Boston Greenhouse JD. Two variants: A (the discovery-led story) and B (the tighter thesis). Post the artifact + repo link in the first comment, not the body (LinkedIn suppresses link-in-body reach)."
---

# Judge Layer — LinkedIn Draft

> **Tier-A note:** the roadmap says agents never draft LinkedIn copy. These are scaffolds you asked for — your hand on the final words before it posts. Read both out loud; ship the one that sounds like you.

---

## Variant A — discovery-led (recommended)

I added a control layer to one of my agents this week, and the build taught me something about my own design.

The job: intercept what an agent wants to do before it does it, judge it against a policy a non-engineer can read, and quarantine anything that breaks the rules. Four rules in YAML. A local model that judges each draft for $0. An append-only ledger of every decision.

Wiring it into a real agent exposed the gap my unit tests had hidden: the judge could parse a verdict, but it couldn't see the draft it was supposed to judge. The fix was one field — and it's now what makes the whole thing auditable.

Agents draft. I send. Every word.

#AIProductManagement #AgentArchitecture

---

## Variant B — thesis-led (tighter)

"Control architectures around production agent deployments."

That's a line from a job description. This week I shipped one.

A judge layer sits between my Substack agent's intent and its action: it reads a typed proposal, evaluates the draft against four YAML rules, and returns one of five outcomes — allow, revise, block, escalate, or judge-unavailable. It runs on a local model at $0 per decision and logs every verdict to a ledger my dashboard reads. If the judge is ever down, it falls open to me — my review stays the canonical control.

The agent drafts. I still send every word. The judge is the receipt that proves it.

#AIProductManagement #ForwardDeployed

---

## First-comment (post this as the first comment, not in the body)

> Repo: github.com/seanwinslow28/code-brain (agents-sdk/lib/judge)
> Write-up: seanwinslow.com/transactions/judge-layer  ← gated on the personal-site deploy; drop the EXPLANATION.md permalink until then
> Built toward @Anthropic's Forward Deployed Engineer role in Boston — the JD asks for MCP servers, sub-agents, and control architectures: https://job-boards.greenhouse.io/anthropic/jobs/4985877008

## Publish-day checklist

- [ ] Read the chosen variant out loud — does it sound like you, or like a press release? Cut anything that's the latter.
- [ ] Loom recorded and uploaded; thumbnail readable on mobile.
- [ ] Repo + JD links in the FIRST COMMENT, not the body.
- [ ] Tag Anthropic only once, in the comment, not the body (cleaner).
- [ ] `seanwinslow.com/transactions/judge-layer` resolves — if the deploy hasn't landed, swap to the EXPLANATION.md GitHub permalink so no link 404s.
- [ ] Post Tue or Thu morning (your application cadence window) for reach.
