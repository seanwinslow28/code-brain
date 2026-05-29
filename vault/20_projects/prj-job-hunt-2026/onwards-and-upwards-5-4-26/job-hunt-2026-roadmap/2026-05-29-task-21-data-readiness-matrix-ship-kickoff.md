---
type: kickoff
project: prj-job-hunt-2026
parent_task: task-21-data-readiness-matrix
created: 2026-05-29
target: claude-code
ai-context: "Claude Code kickoff — ship Task 21 (Enterprise Data Readiness Matrix). The four repo files + the portfolio ledger row are already authored and staged inside code-brain/staging/. Claude Code's job is the mechanical ship: stand up the standalone public repo, place the ledger row in the portfolio repo, verify, and flip the roadmap. Paste the block below into Claude Code from ~/Code-Brain/code-brain."
---

# Claude Code Kickoff — Ship Task 21 (Enterprise Data Readiness Matrix)

The content is written and staged. This is a ship + wiring task, not an authoring task. Paste the block into Claude Code from `~/Code-Brain/code-brain`.

```
You are shipping Task 21 of the job-hunt roadmap: the Enterprise Data Readiness
Matrix. The four repo files and the portfolio ledger row are ALREADY AUTHORED
and staged. Your job is the mechanical ship: stand up the standalone public
repo, place the ledger row in the portfolio repo, verify, flip the roadmap.
Do NOT rewrite the content — if you spot a substantive problem, surface it to
me, don't silently edit.

────────────────────────────────────────────────────────────────────────────
WHAT'S STAGED (already written, do not regenerate)
────────────────────────────────────────────────────────────────────────────
Standalone-repo files (4) at:
  ~/Code-Brain/code-brain/staging/enterprise-data-readiness-matrix/
    ├── README.md            (portfolio framing, <90s readable)
    ├── matrix.md            (the rubric: 5 dims × Green/Yellow/Red, floor-rule scoring)
    ├── worked-example-fortune-500-content-co.md  (scored F500 + 90-day remediation)
    └── EXPLANATION.md       (4Q artifact, frontmatter with repoUrl/explanationUrl)

Portfolio ledger row (1) at:
  ~/Code-Brain/code-brain/staging/portfolio-ledger-row/enterprise-data-readiness-matrix.mdx
    (matches the transactions collection schema — title/dateline/shipped/surface/
     status/valueProp/methods/limitations/explanationUrl/repoUrl)

Note: staging/ lives inside the code-brain repo but is untracked and outside
vault/, so Obsidian-Git won't touch it. You'll move these out and delete
staging/ so code-brain's working tree ends clean.

────────────────────────────────────────────────────────────────────────────
STEP 1 — stand up the standalone public repo
────────────────────────────────────────────────────────────────────────────
The repo lives as a SIBLING of code-brain (not inside it), per the roadmap:

  mkdir -p ~/Code-Brain/enterprise-data-readiness-matrix
  mv ~/Code-Brain/code-brain/staging/enterprise-data-readiness-matrix/* \
     ~/Code-Brain/enterprise-data-readiness-matrix/
  cd ~/Code-Brain/enterprise-data-readiness-matrix
  git init && git add -A
  git commit -m "feat: Enterprise Data Readiness Matrix v1 — 5-dimension pre-deployment rubric + worked example

A pre-deployment rubric for AI platform PMs: score whether a customer's data
layer can carry an agent before committing a launch date. Five dimensions
(canonical entity IDs, lineage/provenance, freshness, governance/eligibility,
dedup/embedding hygiene) scored Green/Yellow/Red with a floor-rule model.
Ships with a worked Fortune-500 example + 90-day Red->Yellow->Green remediation
plan and a 4Q EXPLANATION. Grounded in a 4-panel deep-research read of mid-2026
enterprise AI PM hiring criteria; green-state examples reference the author's
own agent-fleet knowledge base. Closes the 'enterprise data readiness' gap
named in 85% of Tier-1 AI PM JDs."

  gh repo create seanwinslow28/enterprise-data-readiness-matrix \
    --public --source=. --remote=origin --push \
    --description "A pre-deployment rubric for AI platform PMs: score whether a customer's data layer can carry an agent before committing a launch date."

Verify: the repo is public and the README renders. Confirm the EXPLANATION.md
frontmatter repoUrl/explanationUrl already point at this repo's real paths (they
were authored to — sanity-check they resolve once pushed).

────────────────────────────────────────────────────────────────────────────
STEP 2 — wire the ledger row into the portfolio
────────────────────────────────────────────────────────────────────────────
  mv ~/Code-Brain/code-brain/staging/portfolio-ledger-row/enterprise-data-readiness-matrix.mdx \
     ~/Code-Brain/sw-ai-pm-portfolio/src/content/transactions/enterprise-data-readiness-matrix.mdx

JUDGMENT CALL TO CONFIRM WITH ME: the ledger row sets `surface: infra`. The
transactions surface enum is [fleet, pipeline, product, writing, infra]. I chose
`infra` (data-infrastructure readiness). If you/Sean think a written strategic
framework belongs under `writing`, switch it — there's an inline comment in the
.mdx flagging this. Don't guess silently; pick one and tell me which.

Then validate + cross-link per the portfolio's own tooling (discover exact
script names; config.ts references these):
  cd ~/Code-Brain/sw-ai-pm-portfolio
  node scripts/validate_content.mjs        # or the package.json equivalent
  node scripts/derive_crosslinks.mjs       # if the repo uses it
  npm run build                            # confirm /transactions/enterprise-data-readiness-matrix/ resolves

Then commit + PR in the portfolio repo (stage ONLY the new .mdx + any
generated crosslink files; no unrelated changes):
  git checkout main && git pull
  git switch -c feat/ledger-data-readiness-matrix
  git add src/content/transactions/enterprise-data-readiness-matrix.mdx
  # + any files the crosslink script regenerated
  git commit -m "feat(transactions): add enterprise-data-readiness-matrix ledger row (Task 21)"
  git push -u origin feat/ledger-data-readiness-matrix
  gh pr create --base main --title "feat(transactions): enterprise-data-readiness-matrix ledger row" \
    --body "Ledger row for the Enterprise Data Readiness Matrix (Task 21). Repo: https://github.com/seanwinslow28/enterprise-data-readiness-matrix. Validates against the transactions schema; surface=infra (flag if it should be 'writing')."

────────────────────────────────────────────────────────────────────────────
STEP 3 — flip the roadmap (vault files — Obsidian-Git owns commits)
────────────────────────────────────────────────────────────────────────────
Edit (do not git-commit — Obsidian-Git auto-commits vault/):
  vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
    → Task 21 (~line 1288): flip Steps 1-6 to [x]. On Step 6, append a one-line
      completion note: "✅ SHIPPED 2026-05-29 — repo public at
      github.com/seanwinslow28/enterprise-data-readiness-matrix; ledger row PR
      open in sw-ai-pm-portfolio; matrix.md (5-dim floor-rule rubric) +
      worked-example (F500 + 90-day remediation) + EXPLANATION.md (4Q).
      Grounded in 2026-05-18 DR-Max research Q1/Q7."
  Same folder / unified-roadmap-completion-log.md
    → add an entry under ## Amendments Log:
      "### 2026-05-29 — Task 21 SHIPPED (Enterprise Data Readiness Matrix)"
      with a short ship narrative matching the existing entry conventions
      (artifact pointers, what it closes — the 85%-of-JDs data-readiness gap,
      the floor-rule design, the Code-Brain-as-worked-example angle).

────────────────────────────────────────────────────────────────────────────
STEP 4 — clean up + report
────────────────────────────────────────────────────────────────────────────
  rmdir ~/Code-Brain/code-brain/staging/enterprise-data-readiness-matrix \
        ~/Code-Brain/code-brain/staging/portfolio-ledger-row \
        ~/Code-Brain/code-brain/staging 2>/dev/null || true
  cd ~/Code-Brain/code-brain && git status   # confirm staging/ is gone; working tree clean of it

Report back: the standalone repo URL, the portfolio PR URL, which `surface`
value you used, whether the local portfolio build resolved
/transactions/enterprise-data-readiness-matrix/, and confirmation that
code-brain's working tree is clean. If anything in Steps 1-2 failed (gh auth,
build, schema validation), stop and show me the error before flipping the
roadmap.

VERIFICATION GATE (from the roadmap): standalone repo public; ledger row live +
validates; README readable in <90s; EXPLANATION.md passes the <90-sec recruiter
readability check.
```
