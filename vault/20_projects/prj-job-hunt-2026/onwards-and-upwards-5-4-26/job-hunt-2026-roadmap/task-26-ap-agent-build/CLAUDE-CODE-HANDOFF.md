# Claude Code handoff — create `~/Code-Brain/enterprise-ap-agent-spec`

The full Task 26 package is staged and complete in this folder. Claude Code runs on your Mac (host), so it can reach both the staged source and the target locations — the standalone repo path isn't a Cowork-mounted folder, which is why this is a host-side step (same pattern as the `ldr-grounding-collapse` ship ticket).

**Paste the block below into a Claude Code session at `~/Code-Brain/`.**

---

```
Create and publish a new public GitHub repo called `enterprise-ap-agent-spec` from a staged package. Work carefully and stop if any verification step fails.

SOURCE (staged package, already written — do not regenerate, just copy):
~/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/task-26-ap-agent-build/

TARGET repo dir:
~/Code-Brain/enterprise-ap-agent-spec/

STEP 1 — Assemble the repo. Create the target dir and copy EXACTLY these 10 files from SOURCE into it (flat, same names):
  README.md
  EXPLANATION.md
  PRD.md
  eval-suite.yaml
  stub_agent.py
  run_evals.py
  cost-model.md
  cost_model.py
  build-vs-buy-memo.md
  governance-mapping.md
Do NOT copy: LEDGER-ENTRY-enterprise-ap-agent-spec.mdx, CLAUDE-CODE-HANDOFF.md, or __pycache__/ (those are not repo content). Add a .gitignore containing `__pycache__/` and `*.pyc`.

STEP 2 — Verify it runs (these are the gate). From inside ~/Code-Brain/enterprise-ap-agent-spec/:
  - `python3 -c "import yaml" || pip install pyyaml`
  - `python3 run_evals.py`        → expect "13 passed, 1 xfail (known stub limitation)" and exit code 0
  - `python3 run_evals.py --naive`→ expect "4 passed, 10 FAILED" and exit code 1 (this is the bite test; the non-zero exit is correct)
  - `python3 cost_model.py`       → expect a 3-scenario cost table printing
  - `wc -w PRD.md`                → expect ~4,074 words (gate requires 4,000–6,000)
  If any of these don't match, STOP and report — do not publish.

STEP 3 — Publish.
  - `git init && git add -A && git commit -m "feat: enterprise AP invoice-approval agent spec — PRD + 14-case eval suite + cost model + build-vs-buy + SOC 2 / SR 11-7 governance"`
  - `gh repo create seanwinslow28/enterprise-ap-agent-spec --public --source=. --remote=origin --push`
  - Print the live repo URL and confirm the README renders on GitHub.

STEP 4 — Report back: the repo URL, the three command results from Step 2, and the PRD word count. Do not touch the Obsidian vault (Obsidian-Git owns vault commits) — you are only reading from it and writing to the new repo.

GATED FOLLOW-UP (do ONLY after the repo above is public and its URLs resolve — tell me before doing it):
  - Copy ~/Code-Brain/code-brain/vault/.../task-26-ap-agent-build/LEDGER-ENTRY-enterprise-ap-agent-spec.mdx
    to ~/Code-Brain/sw-ai-pm-portfolio/src/content/transactions/enterprise-ap-agent-spec.mdx
  - Confirm the repoUrl/explanationUrl in its frontmatter now resolve (they 200 once the repo is public).
  - From ~/Code-Brain/sw-ai-pm-portfolio: run the content validator / `npm run build` and confirm the route /transactions/enterprise-ap-agent-spec/ resolves.
  - If green, commit in the portfolio repo: `content(transactions): add enterprise-ap-agent-spec ledger row (surface: infra)`.
  - If the actual ship date isn't 2026-06-19, update `dateline` + `shipped` in the frontmatter first.
```

---

## Notes for Sean (not part of the paste)

- **PRD word count is already verified** at 4,074 (gate: 4,000–6,000). The eval suite is verified green here (13 pass + 1 xfail) and red on the naive baseline (the bite test). So Step 2 should pass on your Mac as long as Python 3 + PyYAML are available.
- **The ledger entry is intentionally excluded from the repo** — it lives in the portfolio, not the AP-spec repo. It's gated because its `repoUrl` only resolves once the repo is public. The `shipped`/`dateline` are set to the 6/19 target; change them if you ship another day.
- **Two things Claude Code can't do — they're yours (Step 10 + the gate's last criterion):**
  - **LinkedIn critique has lead time.** The verification gate needs ≥1 substantive comment from a real enterprise AI PM. Post the draft ~5–7 days before 6/19 so there's time for a reply; you can't manufacture it on ship day.
  - **Re-verify the time-sensitive numbers before the LinkedIn post:** model pricing (cost-model.md), the vendor certifications (build-vs-buy-memo.md — OpenAI's HIPAA BAA + SSO specifics were unverified), and that the OWASP/NIST edition labels are current. All are flagged ⏱ in the files.

## Verification gate (Task 26 — definition of done)

- [ ] Repo `enterprise-ap-agent-spec` public on GitHub
- [x] PRD.md 4,000–6,000 words (4,074)
- [x] Eval cases runnable against a stub (14 cases; green on correct, red on naive)
- [x] Cost model has real per-token numbers (June 2026, cited)
- [x] Build-vs-buy memo has a defended recommendation (Anthropic platform, ratified)
- [ ] ≥1 substantive LinkedIn comment from an enterprise AI PM (Sean, post-ship)
- [ ] Transactions ledger row live on seanwinslow.com/transactions (gated follow-up)
- [x] README + EXPLANATION present; README readable in <90s
- [x] SOC 2 control IDs corrected (CC6.1 access / CC7.2 monitoring / CC8.1 change mgmt)
