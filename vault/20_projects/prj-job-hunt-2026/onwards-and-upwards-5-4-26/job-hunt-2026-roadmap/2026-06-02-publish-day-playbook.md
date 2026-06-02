---
type: publish-playbook
project: prj-job-hunt-2026
created: 2026-06-02
status: ready-to-execute
ai-context: "Consolidated publish playbook to clear the content-complete-but-unpublished backlog (Tasks 12/21/22/23/25 + vault-knowledge-mcp). Two blocks: (A) go-live work with no algo penalty, batched into one ~75-min session; (B) a LinkedIn drip calendar over ~2 weeks because firing 5 posts in one hour torches reach. Link targets are GitHub/npm/Substack (always live) because seanwinslow.com/transactions/* is gated on the personal-site deploy (Gap-Fill 3, not yet landed). Two new LinkedIn teasers (System Card, Data Readiness Matrix) are authored inline here."
---

# Publish-Day Playbook — clear the backlog

You have eight flagship artifacts shipped and a pile sitting content-complete but invisible. This is the one doc that makes them live. Two blocks.

## Two design calls (read first)

1. **Link to always-live surfaces, not `/transactions/*`.** `seanwinslow.com` (the portfolio) isn't deployed yet — that's Gap-Fill 3. Every first-comment link block below points at **GitHub / npm / Substack**, which are live now. When the site deploys, you can add the `/transactions/<slug>` link as a bonus; until then it would 404. (This matches the note already in your judge-layer LinkedIn draft.)
2. **Drip the LinkedIn posts; don't batch them.** Posting 5 LinkedIn posts in one hour cannibalizes every post's reach and reads as noise to your network. **Block A (go-live) all happens today. Block C (LinkedIn) is a 2-week calendar, one post every 2–3 days, Tue/Thu mornings** — your application-cadence window. The Looms get recorded today (Block B) so they're ready to attach when each post fires.

---

## BLOCK A — Make it live (today, ~75 min, no algo penalty)

Do these in order. Each is irreversible-ish (commits/pushes/publishes), so eyeball `git status` before every commit. Nothing here touches LinkedIn.

### A1 — Push the LDR Grounding-Collapse repo (~10 min)
The 5 files are staged at `~/Code-Brain/ldr-grounding-collapse/` (no `.git` yet).
```bash
cd ~/Code-Brain/ldr-grounding-collapse
git init && git add . && git commit -m "LDR grounding-collapse post-mortem: failure, diagnosis, fix, eval"
gh repo create ldr-grounding-collapse --public --source=. --remote=origin --push
```
Then swap the placeholder repo URL → live in **both**: the Substack draft (`substack-drafts/2026-05-29-ldr-grounding-collapse.md`) and the ledger row (`sw-ai-pm-portfolio/.../transactions/ldr-grounding-collapse.mdx` — already points at the right URL, just confirm it resolves once pushed).

### A2 — Portfolio: build + commit the two new ledger rows (~10 min)
Confirms `ldr-grounding-collapse.mdx` + `mcp-security-audit.mdx` are schema-clean and resolve.
```bash
cd ~/Code-Brain/sw-ai-pm-portfolio
npm run build      # must resolve /transactions/ldr-grounding-collapse/ and /transactions/mcp-security-audit/
git add src/content/transactions/ldr-grounding-collapse.mdx src/content/transactions/mcp-security-audit.mdx
git commit -m "content(transactions): add LDR grounding-collapse + MCP security audit ledger rows"
```
If `npm run build` errors on either row, fix the flagged field before committing (don't commit a broken content collection — it breaks the eventual deploy).

### A3 — Task 12 Judge Layer: test, commit, tag (~20 min)
Per `2026-05-31-task-12-day-6-handoff.md` (paste-ready CHANGELOG block + exact commands live there).
```bash
cd ~/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. pytest tests/ -q          # expect the 2 known pre-existing fleet-memory reds ONLY
cd ~/Code-Brain/code-brain && python3 scripts/validate.py   # expect PASSED
# then commit per the handoff doc + tag:
git tag judge-layer-v0.1.0
git push --follow-tags
```

### A4 — Task 22 Code-Brain System Card: validate, build, commit (~15 min)
```bash
cd ~/Code-Brain/code-brain && python3 scripts/validate.py        # PASSED
cd ~/Code-Brain/sw-ai-pm-portfolio && npm run build               # resolves /transactions/code-brain-system-card/
# commit the card in code-brain + the ledger row in the portfolio (two repos)
```

### A5 — Task 25 Substack Post 1: voice pass + publish (~20 min) — DO THIS LAST in Block A
This is **Substack Post 1, the announcement that gates Posts 2 + 3** (the manifesto + future posts). Publishing it unblocks the whole Substack cadence.
- Run the `writing-voice-modes` skill on `substack-drafts/2026-05-29-ldr-grounding-collapse.md` (Sedaris dial check on the open + close).
- Confirm the repo URL is live (from A1).
- Read §1 and the close out loud once.
- Publish to Substack. Title: **"The Day My Research Agent Invented Microsoft."**

> After Block A: every artifact is live on GitHub/npm/Substack. The LinkedIn posts (Block C) now have real, non-404 links to point at.

---

## BLOCK B — Record the two Looms (today, ~25 min)

Only two artifacts have Looms. Record both in one sitting (terminal already set up, font large for mobile). Upload, grab the share URLs, drop them into the matching Block C rows.

| Loom | Script | The one-line demo | Length |
|---|---|---|---|
| **Judge Layer** | `agents-sdk/lib/judge/LOOM-SCRIPT.md` (primary = ESCALATE take) | `python3 agents/substack_drafter.py --demo-injection` → ActionProposal → ESCALATE → quarantine + ledger row. Close on "agents draft, I send." | 90s |
| **vault-knowledge-mcp** | `<sw-mcp-vault-knowledge>/docs/LOOM-SCRIPT.md` (lead on `find_contradictions`) | All 3 tools against the live vault; lead with `find_contradictions` returning the ~30 live contradiction edges. | 90s |

Don't-say list (from the judge script, applies to both): no "AI-powered," no "revolutionary," no "guardrails." Say "control architecture." Don't oversell the local model — the point is the architecture.

---

## BLOCK C — LinkedIn drip calendar (~2 weeks, one post every 2–3 days)

Post **Tue/Thu mornings**. Tag Anthropic **once, in the first comment, not the body**. Links in the **first comment**. Order is by impact + narrative arc (lead with the live MCPs that have Looms).

| Slot | Post | Draft source | Has Loom? | Tag |
|---|---|---|---|---|
| Day 1 (Tue) | **vault-knowledge-mcp** | `<sw-mcp-vault-knowledge>/docs/LINKEDIN-DRAFT.md` | ✅ | Anthropic |
| Day 3 (Thu) | **Judge Layer** | `agents-sdk/lib/judge/LINKEDIN-DRAFT.md` (Variant A rec.) | ✅ | Anthropic FDE |
| Day 6 (Tue) | **MCP Security Audit (Task 23)** | `sw-mcp-intent-engineering/docs/LINKEDIN-DRAFT.md` | ❌ | Anthropic |
| Day 8 (Thu) | **Code-Brain System Card (Task 22)** | inline §C1 below | ❌ | Anthropic |
| Day 10 (Tue) | **Enterprise Data Readiness Matrix (Task 21)** | inline §C2 below | ❌ | — |

(The LDR post-mortem went out as Substack Post 1 in A5; you can add a 1-line LinkedIn pointer to it on any off-day if you want, but don't let it crowd the calendar.)

### First-comment link blocks (copy-paste per post)

**vault-knowledge-mcp**
```
Loom (90s): <paste Loom URL>
npm: npmjs.com/package/@swins/vault-knowledge-mcp
Repo: github.com/seanwinslow28/sw-mcp-vault-knowledge
Built toward @Anthropic's agent-infrastructure work.
```
**Judge Layer**
```
Loom (90s): <paste Loom URL>
Repo: github.com/seanwinslow28/code-brain (agents-sdk/lib/judge)
4Q write-up: github.com/seanwinslow28/code-brain/blob/main/agents-sdk/lib/judge/EXPLANATION.md
Built toward @Anthropic's Forward Deployed Engineer role (Boston): job-boards.greenhouse.io/anthropic/jobs/4985877008
```
**MCP Security Audit**
```
Threat model + the fix: github.com/seanwinslow28/sw-mcp-intent-engineering/blob/main/docs/SECURITY.md
npm (v0.1.1): npmjs.com/package/@swins/intent-engineering-mcp
Repo: github.com/seanwinslow28/sw-mcp-intent-engineering
```
**Code-Brain System Card**
```
The card: github.com/seanwinslow28/code-brain/blob/main/docs/CODE_BRAIN_SYSTEM_CARD.md
4Q: github.com/seanwinslow28/code-brain/blob/main/docs/CODE_BRAIN_SYSTEM_CARD_EXPLANATION.md
```
**Enterprise Data Readiness Matrix**
```
Repo: github.com/seanwinslow28/enterprise-data-readiness-matrix
The floor-rule rubric: github.com/seanwinslow28/enterprise-data-readiness-matrix/blob/main/matrix.md
```

---

### §C1 — Code-Brain System Card — LinkedIn teaser (NEW, ~140 words)

> Tier-A: draft / you send. Read it out loud first.

I tiered my own AI agent fleet against the same model-risk frameworks a bank uses — SR-11-7 and the EU AI Act — and the most useful section was the one that ruled most of the regulation *out*.

That's the move I'd defend in a review: my fleet is minimal-risk, not high-risk, so the EU AI Act's high-risk obligations don't bind by their own terms. So I said that first — then mapped the discipline voluntarily anyway, and named every place the system would fail if it *were* regulated. Correctly scoping a law you don't have to follow signals more than performing compliance with one you've misread.

Twelve live components, tiered by inherent vs. residual materiality, every gap named. The card's in the first comment.

#AIGovernance #AIProductManagement

### §C2 — Enterprise Data Readiness Matrix — LinkedIn teaser (NEW, ~140 words)

> Tier-A: draft / you send. Read it out loud first.

"Four greens and a red, 80%, ship it" is exactly how you get the Air Canada outcome — the agent fails confidently on the one red seam, and the org that deployed it inherits the liability.

So I built a pre-deployment rubric that refuses to average. Five dimensions of data readiness — canonical IDs, lineage, freshness, governance, embedding hygiene — and the deployment posture is set by your *worst* dimension, not your mean. A floor, not an average.

The five dimensions aren't from a consulting deck. They're the five problems I had to solve on my own agent fleet's knowledge base before it would produce citable output. The generalization is the artifact.

Rubric + a scored Fortune-500 worked example in the first comment.

#AIStrategy #DataStrategy #EnterpriseAI

---

## Master link reference (all live surfaces in one place)

- LDR post-mortem repo: `github.com/seanwinslow28/ldr-grounding-collapse` (after A1)
- intent-engineering MCP: npm `@swins/intent-engineering-mcp` · repo `github.com/seanwinslow28/sw-mcp-intent-engineering` · SECURITY.md at `/blob/main/docs/SECURITY.md`
- vault-knowledge MCP: npm `@swins/vault-knowledge-mcp` · repo `github.com/seanwinslow28/sw-mcp-vault-knowledge`
- code-brain monorepo: `github.com/seanwinslow28/code-brain` (judge at `agents-sdk/lib/judge`, card at `docs/CODE_BRAIN_SYSTEM_CARD.md`) — **confirm this repo is public before posting**
- Data Readiness Matrix: `github.com/seanwinslow28/enterprise-data-readiness-matrix`
- Anthropic FDE Boston JD: `job-boards.greenhouse.io/anthropic/jobs/4985877008`

## Definition of done
- [ ] Block A: all 5 repos/artifacts live; 2 ledger rows build clean + committed; judge tagged `judge-layer-v0.1.0`; Substack Post 1 published.
- [ ] Block B: both Looms recorded + uploaded; URLs pasted into the C link blocks.
- [ ] Block C: calendar set; first post (vault-knowledge-mcp) fired Tue AM.
- [ ] Log the first recruiter/HM engagement attributable to any artifact in `target-companies.md` (the last open success criterion on several tasks).
