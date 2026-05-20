---
type: claude-code-handoff
project: prj-job-hunt-2026
created: 2026-05-13
roadmap: 2026-05-06-unified-roadmap.md
covers: [Task 1 Steps 3 + 5, Task 2 Steps 3 + 5]
ai-context: "Paste-ready Claude Code prompt covering the Astro `/transactions/` route + the validate-and-commit pass for the Phase D / Phase 6 EXPLANATION.md files already on disk. Co-work session on 2026-05-12 (evening) handled Task 1 Steps 1+2+4 and Task 2 Steps 1+2+4 directly — files exist at the canonical paths and pass the <90-sec readability test. This handoff finishes the loop."
---

# Claude Code Handoff — Friday Week 1 finisher (Tasks 1 + 2)

> **Context for you, the Claude Code session:** A Cowork session on 2026-05-12 wrote four files to disk. They exist and have been read-back-verified. You don't need to recreate them. You need to (a) skeleton the personal site `/transactions/` route in the separate personal-site repo, (b) add two entries linking to the new GitHub EXPLANATION.md files, (c) run `python3 scripts/validate.py` in the Code-Brain, and (d) commit both the code-brain files and the personal-site files with the messages below.
>
> **Reference doc:** [`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md`](./2026-05-06-unified-roadmap.md) — Task 1 lines 206–256, Task 2 lines 258–285. The 4Q paste sources are §2a and §2e of [`reference-synthesis-docs/claude-nate-prompt-2-analysis.md`](./reference-synthesis-docs/claude-nate-prompt-2-analysis.md) lines 17–25 and 57–65, but you don't need them — the paste is already on disk.

---

## Pre-flight: what's already on disk

Four files. Verify they exist before doing anything else.

```bash
ls -la \
  vault/40_knowledge/templates/EXPLANATION-template.md \
  agents-sdk/lib/concept_edges/EXPLANATION.md \
  agents-sdk/agents/knowledge_loop/EXPLANATION.md
```

Expected: all three present. The fourth (Code-Brain README) is unchanged — opening paragraph already leads with "agentic engineering practitioner's toolkit" per Karpathy framing.

If anything is missing, stop and report back — do NOT regenerate from the source synthesis docs without Sean's approval. The pre-existing template at `vault/40_knowledge/templates/EXPLANATION-template.md` is canonical (Sean wrote it 2026-05-06) and is materially better than a naive scaffold.

---

## Step 1 — Find the personal-site repo

The roadmap references `<personal-site>` without naming the path. Sean's portfolio plan calls for Astro 5 + React islands. Likely candidates:

```bash
ls -la ~/Code-Brain/ | grep -iE "site|portfolio|astro|seanwinslow"
ls -la ~/Code/ 2>/dev/null | grep -iE "site|portfolio|astro|seanwinslow"
```

If you find one repo, use it. If you find more than one, **stop and ask Sean which is canonical** — do not guess. If you find none, scaffold a new one at `~/Code-Brain/sw-portfolio-site/` with `npm create astro@latest -- --template minimal --typescript strict --git` and tell Sean you're starting from scratch.

**The roadmap explicitly notes (Decision 2 in unified-roadmap.md):** if the personal site build is delayed past 2026-05-13, GitHub `EXPLANATION.md` files become canonical and Substack syndicates from GitHub raw URLs. So if scaffolding the site looks like it will eat >30 minutes, **stop and confirm with Sean** rather than burning Track-C deep-work time on it.

---

## Step 2 — Skeleton the `/transactions/` route

In the personal-site repo, create:

**`src/pages/transactions/index.astro`** (minimum viable — keep it ugly, content > polish):

```astro
---
// /transactions/ — comprehension artifacts attached to Sean's existing work.
// The 4-question template is the unit of work; this page is the index.
const artifacts = [
  {
    slug: "phase-d-typed-reasoning-edges",
    title: "Phase D — Typed Reasoning Edges",
    pitch: "A SQLite typed-edge layer that lets the nightly synthesizer detect contradictions in my Obsidian vault at zero LLM cost.",
    explanation: "https://github.com/seanwinslow28/code-brain/blob/main/agents-sdk/lib/concept_edges/EXPLANATION.md",
    code: "https://github.com/seanwinslow28/code-brain/tree/main/agents-sdk/lib/concept_edges",
    shipped: "2026-05-01",
  },
  {
    slug: "knowledge-loop-phase-6",
    title: "Phase 6 — Knowledge Loop (Producer + Consumer)",
    pitch: "Closed loop that turns Claude Code session transcripts into a queryable knowledge graph the LLM maintains and reads on every new session.",
    explanation: "https://github.com/seanwinslow28/code-brain/blob/main/agents-sdk/agents/knowledge_loop/EXPLANATION.md",
    code: "https://github.com/seanwinslow28/code-brain/tree/main/agents-sdk/agents",
    shipped: "2026-05-01",
  },
];
---

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Transactions — Sean Winslow</title>
    <meta name="description" content="Small, verifiable units of completed work with explanation attached. The 4-question artifact is the unit." />
  </head>
  <body>
    <main>
      <h1>Transactions</h1>
      <p>
        Small, verifiable units of completed work with the explanation attached.
        Each artifact answers four questions: <em>what is this, why this approach, what would break, what did I learn.</em>
      </p>

      <ul>
        {artifacts.map((a) => (
          <li>
            <h2>{a.title}</h2>
            <p>{a.pitch}</p>
            <p>
              <a href={a.explanation}>EXPLANATION.md</a>
              {" · "}
              <a href={a.code}>code</a>
              {" · "}
              <small>shipped {a.shipped}</small>
            </p>
          </li>
        ))}
      </ul>
    </main>
  </body>
</html>
```

Replace `seanwinslow28` with the actual GitHub handle if it differs. Don't add styling — empty list is fine per the roadmap. Don't add a navbar. Don't add a footer. Don't add Tailwind. **The verification gate is "page loads at localhost:4321/transactions/" — nothing more.**

Run `npm run dev` and confirm the page renders.

---

## Step 3 — Validate the Code-Brain

In `~/Code-Brain/code-brain/`:

```bash
python3 scripts/validate.py
```

Expected: `Validation PASSED` with some number of pre-existing warnings (60 as of v3.30.1). If new errors appear that didn't appear before, **stop and report back** — don't paper over them.

---

## Step 4 — Commit the Code-Brain files

In `~/Code-Brain/code-brain/`:

```bash
git status   # confirm the three files show as new
git diff --stat
```

Expected new files:
- `vault/40_knowledge/templates/EXPLANATION-template.md` (may already be tracked — Sean wrote it 2026-05-06)
- `agents-sdk/lib/concept_edges/EXPLANATION.md`
- `agents-sdk/agents/knowledge_loop/EXPLANATION.md`

Then:

```bash
git add agents-sdk/lib/concept_edges/EXPLANATION.md \
        agents-sdk/agents/knowledge_loop/EXPLANATION.md
# Only add the template if it shows as untracked — Sean may have already committed it on 5/6
git add vault/40_knowledge/templates/EXPLANATION-template.md 2>/dev/null || true

git commit -m "docs: add 4Q comprehension artifacts for Phase D typed edges + Phase 6 knowledge loop

Friday Week 1 deliverable per the unified roadmap (Task 2). Two
EXPLANATION.md files at the conventional co-located paths, each
following the 4-question template (What is this / Why this approach /
What would break / What did I learn) sourced verbatim from the
Claude-Nate-2 analysis §2a and §2e. Both pass the <90-sec recruiter
readability test.

Refs: vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md Task 2"
```

**Do NOT push yet.** Sean reviews local first. After he's looked at the commit:

```bash
git push origin main
```

(Branch may be `master` or `main` — use whichever `git symbolic-ref --short HEAD` returns.)

---

## Step 5 — Commit the personal-site files (separate repo)

In the personal-site repo (whichever path Step 1 settled on):

```bash
git status
git add src/pages/transactions/index.astro
git commit -m "feat(transactions): skeleton /transactions/ route with two initial artifacts

First two comprehension artifacts surfaced: Phase D typed reasoning
edges + Phase 6 knowledge loop. EXPLANATION.md files live in the
Code-Brain repo and this route links to them. Unstyled by design;
content > polish per the unified roadmap Task 1 Step 3."
```

---

## Step 6 — Skip the docs-update rule (it doesn't fire)

The mandatory project rule says when creating a new **Skill, Agent, Sub-Agent, Hook, or Script** you must update `CHANGELOG.md` / `CLAUDE.md` / `README.md`. `EXPLANATION.md` files are documentation, not any of those types — the rule does not fire.

**However**: if Sean wants to call out the 4Q discipline as a meaningful repo shift, suggest a CHANGELOG entry under a new minor version (v3.34.0?) at the END — only after confirming with Sean. Do not add it unilaterally.

---

## Step 7 — Verification gate

Before reporting back, confirm in order:

1. `python3 scripts/validate.py` → `Validation PASSED`
2. `git log -1 --oneline` in code-brain → shows the new commit
3. `git log -1 --oneline` in personal-site → shows the new commit
4. `curl -s localhost:4321/transactions/ | grep -c "Phase D"` → `1` or higher (page is live with the new entries)

If any of those fail, **stop and report what failed**. Don't proceed to push.

---

## What this handoff explicitly does NOT cover (per Sean's 2026-05-12 directive)

- ❌ Loom recording (deferred until all projects are locked down)
- ❌ Substack post syndication (deferred — same reason)
- ❌ LinkedIn syndication (deferred — same reason)

Sean will write the scripts and record the Looms in a single pass once the project portfolio is complete. Do not start any Loom/Substack/LinkedIn work in this session.

---

## Tier-A check (per operating-model)

- Walk-away $100k: N/A (this is unpaid build work)
- AI > Tech > Creative PM track: ✅ (Track-C adjacency)
- Agents draft / Sean sends: ✅ (you commit; Sean reviews; Sean pushes)
- Track-C protected: ✅ (intent-engineering MCP is on disk and shipped; this is downstream cleanup)
- 5:30 PM hard stop: respect it — if this session runs past 5:30, stop and resume tomorrow
- 8:30–9:30 sacred learning + 1–2 PM mandatory break: respect them
