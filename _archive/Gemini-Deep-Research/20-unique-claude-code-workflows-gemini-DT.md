Based on the architecture of **Claude Code** (the agentic CLI) and its ecosystem (Skills, Subagents, Hooks, Plugins, MCP), here are **20 unique workflows**.

These are categorized into **Product Ops**, **Creative Pipelines**, **DevOps Automation**, and **Code Hygiene**.

---

### **I. Product Ops & Stakeholder Management**

*Focus: Bridging the gap between tickets, specs, and code.*

#### **1\. The "Ambiguity Crusher" (Spec Triage)**

* **Trigger:** Skill command `/vet-spec [path/to/PRD.md]`  
* **Workflow:**  
  1. **Skill** loads the Markdown spec.  
  2. **MCP (Jira/Linear)** fetches related historical tickets to understand context.  
  3. **Subagent (`@architect`)** cross-references the spec against the current codebase's `schema.prisma` or API types.  
  4. **Action:** Identifies logical contradictions (e.g., "Spec requires email login, but Auth0 config is SMS only") and outputs a "Clarification List" instead of code.  
* **Minimum Setup:** `jira-mcp`; Read-access to repo schema files.  
* **Biggest Risk:** Hallucinating constraints that don't exist. **Mitigation:** Require the agent to cite the specific file/line number for every objection.  
* **Success Measure:** 30% reduction in "Needs Clarification" comments on tickets.

#### **2\. The "Monday Morning" Dispatcher**

* **Trigger:** System Cron (Headless) `claude run skills/triage.md`  
* **Workflow:**  
  1. **MCP (Linear & Sentry)** fetches new bugs and crash reports from the weekend.  
  2. **Subagent (`@triage-medic`)** attempts to correlate stack traces with source files.  
  3. **Action:** Auto-labels issues as `bug`, `infra`, or `noise`. For "noise," it drafts a polite "Closing" comment citing the duplicate ID.  
* **Minimum Setup:** Headless auth token; Sentry MCP.  
* **Biggest Risk:** Auto-closing a critical P0 bug as a duplicate. **Mitigation:** Only auto-close if "Similarity Score" \> 98%; otherwise, just label.  
* **Success Measure:** Triage backlog cleared in \< 5 minutes.

#### **3\. The "Release Note" Storyteller**

* **Trigger:** Git Hook `post-tag` (e.g., v1.2.0)  
* **Workflow:**  
  1. **Skill** runs `git log` between tags.  
  2. **MCP (GitHub)** fetches the *body* of merged PRs to get non-technical context.  
  3. **Subagent (`@copywriter`)** ignores "chore" commits and rewrites technical headers into "User Value" bullet points.  
  4. **Plugin (`slack-connect`)** posts the draft to `#marketing` for approval.  
* **Minimum Setup:** GitHub MCP; `slack-connect` plugin.  
* **Biggest Risk:** Exposing internal code names/security patches to customers. **Mitigation:** Hook filters out any commit marked `[internal]` or `security`.  
* **Success Measure:** Release notes published with \< 1 human edit.

#### **4\. The "Stakeholder Simulator"**

* **Trigger:** Command `/simulate --persona="Security_CISO"`  
* **Workflow:**  
  1. **Context:** Loads the current diffs.  
  2. **Subagent (`@persona-bot`)** adopts the "CISO" persona (trained on OWASP Top 10).  
  3. **Action:** Aggressively critiques the code for missing headers, weak cyphers, or PII leaks.  
  4. **Output:** A "Risk Assessment" report saved to `artifacts/security-review.md`.  
* **Minimum Setup:** Persona prompts in `.claude/agents/`.  
* **Biggest Risk:** False positives blocking development. **Mitigation:** Output is labeled "Simulation" and does not block PR checks.  
* **Success Measure:** Pre-empting 2+ major security comments before the actual audit.

#### **5\. The "Meeting-to-Matrix" Pipeline**

* **Trigger:** `/process-meeting [transcript.txt]`  
* **Workflow:**  
  1. **Subagent** extracts "Action Items" and "Requirements" from the text.  
  2. **MCP (Google Sheets)** maps these items into a Requirement Traceability Matrix (RTM).  
  3. **Action:** Flags items that contradict existing rows in the matrix.  
* **Minimum Setup:** Google Sheets MCP; Transcript file.  
* **Biggest Risk:** Misinterpreting brainstorming as firm requirements. **Mitigation:** Output a confirmation table in the CLI before writing to Sheets.  
* **Success Measure:** 100% of meeting requirements captured in the RTM within 10 mins.

---

### **II. Creative Pipelines & Vertex AI**

*Focus: Asset generation, processing, and localized content.*

#### **6\. The "Asset Hallucinator" (Placeholder Gen)**

* **Trigger:** Hook `PreToolUse` (intercepts "File not found" error on image import)  
* **Workflow:**  
  1. **Hook** catches the error when code tries to import `hero-cyberpunk.png`.  
  2. **MCP (Vertex AI Imagen)** generates a placeholder image based on the filename keywords and CSS dimensions.  
  3. **Action:** Saves the asset to the path, allowing the build to proceed.  
* **Minimum Setup:** Vertex AI MCP; Write access to `/public`.  
* **Biggest Risk:** Generating offensive content. **Mitigation:** Hardcoded negative prompts (Safety Filter) in the hook config.  
* **Success Measure:** Zero "Broken Image" icons during rapid prototyping.

#### **7\. The "Video Script" Director**

* **Trigger:** `/make-demo-script --pr=102`  
* **Workflow:**  
  1. **Subagent** analyzes the PR diff to understand the new feature.  
  2. **MCP (Vertex AI Gemini)** writes a 60-second voiceover script highlighting the "Happy Path."  
  3. **Action:** Generates an `ffmpeg` command script to stitch screen recordings (if available) or outputs TTS audio via **ElevenLabs MCP**.  
* **Minimum Setup:** Vertex AI MCP; `ffmpeg`.  
* **Biggest Risk:** Script timing mismatching the video. **Mitigation:** Agent calculates word-count-to-seconds to enforce duration limits.  
* **Success Measure:** Marketing creates "Feature Shorts" 2x faster.

#### **8\. The "Localization" Swarm**

* **Trigger:** `/localize-batch`  
* **Workflow:**  
  1. **Skill** identifies new keys in `en.json`.  
  2. **Subagents** (Spanish, French, German) run in parallel via **Vertex AI** to translate keys, preserving variable syntax `{name}`.  
  3. **Hook** checks for UI overflow (e.g., German string \> 150% length of English).  
* **Minimum Setup:** Vertex AI MCP; `i18n` structure.  
* **Biggest Risk:** Context-less translation (e.g., "Home" \= "House" vs. "Dashboard"). **Mitigation:** Feed the component code into the context window for reference.  
* **Success Measure:** Zero missing translation keys in production.

#### **9\. The "Figma-to-Test" Generator**

* **Trigger:** `/gen-visual-tests [figma_node_url]`  
* **Workflow:**  
  1. **MCP (Figma)** fetches the "Golden Master" frame properties.  
  2. **Subagent (`@qa-lead`)** writes a Playwright/Cypress test that navigates to the route and asserts those specific CSS properties.  
  3. **Action:** Saves test file to `tests/e2e/`.  
* **Minimum Setup:** Figma MCP; Playwright.  
* **Biggest Risk:** Pixel-perfect assertions failing on different OS rendering. **Mitigation:** Use "Visual Snapshot" comparison with a 5% fuzz threshold instead of strict CSS assertion.  
* **Success Measure:** Automated UI regression testing created at design time.

#### **10\. The "Brand Voice" Linter**

* **Trigger:** Hook `PreCommit` (on `*.md` or `content/*.json`)  
* **Workflow:**  
  1. **Plugin** loads `brand-guidelines.pdf`.  
  2. **Subagent (`@editor`)** scans staged content for banned words, passive voice, or incorrect product casing.  
  3. **Action:** Blocks commit and offers an auto-fixed version if violations are found.  
* **Minimum Setup:** Brand guidelines file; Git hook.  
* **Biggest Risk:** Flattening technical nuance into marketing fluff. **Mitigation:** Exclude `code` blocks and `docs/api` folders from the hook.  
* **Success Measure:** Content consistency score \> 95%.

---

### **III. Automation & DevOps (Headless)**

*Focus: CI/CD, Infrastructure, and Self-Healing.*

#### **11\. The "Self-Healing" CI Medic**

* **Trigger:** GitHub Action `on: workflow_failure` \-\> `claude -c "fix_build"`  
* **Workflow:**  
  1. **MCP (GitHub)** grabs the build logs.  
  2. **Subagent (`@debugger`)** isolates the error (e.g., "Missing dependency" or "Snapshot mismatch").  
  3. **Action:** Claude runs the fix locally (in runner), verifies it passes, and pushes a `fix/auto-ci` commit.  
* **Minimum Setup:** Headless auth; CI runner access.  
* **Biggest Risk:** Infinite commit loops. **Mitigation:** Limit to 1 attempt per failure type.  
* **Success Measure:** 40% of "chore" build failures resolved without human intervention.

#### **12\. The "Infrastructure" Cost Predictor**

* **Trigger:** Hook `PrePush` (on `*.tf` changes)  
* **Workflow:**  
  1. **Skill** runs `terraform plan`.  
  2. **MCP (AWS Pricing)** analyzes the plan to estimate the monthly cost delta.  
  3. **Action:** If cost increase \> $50/mo, blocks push and demands a confirmation flag.  
* **Minimum Setup:** Terraform; AWS Pricing MCP.  
* **Biggest Risk:** Underestimating data transfer costs. **Mitigation:** Prompt user for "Expected Traffic" volume during the check.  
* **Success Measure:** Zero "Bill Shock" incidents.

#### **13\. The "Ghost Branch" Exorcist**

* **Trigger:** `/cleanup-branches`  
* **Workflow:**  
  1. **MCP (GitHub)** lists branches stale \> 30 days.  
  2. **Subagent (`@historian`)** checks if the code was merged (squashed) or abandoned.  
  3. **Action:** DMs the author via **Slack MCP**: "Delete 'fix/header'?"  
  4. **Automation:** Deletes remote branch on "Yes".  
* **Minimum Setup:** GitHub MCP; Slack MCP.  
* **Biggest Risk:** Deleting unmerged "parked" work. **Mitigation:** Default to "Tag & Archive" instead of hard delete.  
* **Success Measure:** Active branch count maintained \< 20\.

#### **14\. The "Dependency" Bouncer**

* **Trigger:** Hook `PreToolUse` (on `npm install`)  
* **Workflow:**  
  1. **Hook** intercepts the install command.  
  2. **MCP (Snyk/Google)** checks the package for CVEs, license issues (GPL), or abandonment.  
  3. **Action:** Blocks install if criteria unmet; suggests a safe alternative.  
* **Minimum Setup:** Security data source.  
* **Biggest Risk:** Blocking internal private packages. **Mitigation:** Whitelist scope `@myorg/*`.  
* **Success Measure:** Zero high-severity CVEs in `package.json`.

#### **15\. The "Readme Rot" Detector**

* **Trigger:** Weekly Cron `claude run skills/verify-docs.md`  
* **Workflow:**  
  1. **Skill** parses code blocks from `README.md`.  
  2. **Subagent** attempts to execute them in a temporary Docker container.  
  3. **Action:** If execution fails, creates a GitHub Issue "Docs Broken" with the error log.  
* **Minimum Setup:** Docker; GitHub MCP.  
* **Biggest Risk:** Executing dangerous commands. **Mitigation:** Sandboxed container with no external network access.  
* **Success Measure:** "Time to Hello World" for new hires \< 15 mins.

---

### **IV. Code Quality & Hygiene**

*Focus: Refactoring, Testing, and Knowledge Management.*

#### **16\. The "Legacy Migration" Scout**

* **Trigger:** `/modernize [file.js]`  
* **Workflow:**  
  1. **Subagent (`@refactor`)** identifies deprecated patterns (e.g., Class Components).  
  2. **Skill** applies a codified "Migration Pattern" from `skills/migration-guide.md`.  
  3. **Hook `PostToolUse`** runs tests specifically for that file to ensure no regression.  
* **Minimum Setup:** Migration guide skill.  
* **Biggest Risk:** Subtle logic bugs during syntax translation. **Mitigation:** Require parallel test execution (old vs new).  
* **Success Measure:** 100% of legacy code migrated without production incidents.

#### **17\. The "Test Coverage" Hunter**

* **Trigger:** `/hunt-untested`  
* **Workflow:**  
  1. **Skill** parses coverage report (`coverage.json`).  
  2. **Subagent (`@qa`)** identifies "Critical Path" files with \< 80% coverage.  
  3. **Action:** Generates unit tests specifically for the uncovered lines and commits to a new branch.  
* **Minimum Setup:** Coverage tool configured.  
* **Biggest Risk:** Writing "assertionless" tests just to satisfy metrics. **Mitigation:** Prompt requires "negative test cases" and edge cases.  
* **Success Measure:** Global coverage increases 1% per week automatically.

#### **18\. The "API Contract" Lawyer**

* **Trigger:** `/validate-contract`  
* **Workflow:**  
  1. **MCP (Postman/Swagger)** fetches the live API spec.  
  2. **Subagent** scans frontend code for API calls.  
  3. **Action:** Flags "Zombie Fields" (requested but unused) or type mismatches between FE and BE.  
* **Minimum Setup:** OpenAPI spec URL.  
* **Biggest Risk:** Spec is outdated. **Mitigation:** Check "Spec Last Updated" date before alerting.  
* **Success Measure:** Runtime "400 Bad Request" errors reduced by 90%.

#### **19\. The "SQL" Safety Valve**

* **Trigger:** Hook `PreToolUse` (on `migrations/*.sql` edits)  
* **Workflow:**  
  1. **Hook** parses the SQL.  
  2. **Subagent (`@dba`)** checks for table-locking operations on large tables (e.g., `ALTER` without `CONCURRENTLY`).  
  3. **Action:** Blocks the write and suggests the non-blocking syntax.  
* **Minimum Setup:** DB Schema awareness.  
* **Biggest Risk:** Blocking legitimate emergency ops. **Mitigation:** Allow override flag `--force`.  
* **Success Measure:** Zero downtime caused by locking migrations.

#### **20\. The "Context" Compressor (Memory)**

* **Trigger:** Hook `SessionEnd`  
* **Workflow:**  
  1. **Subagent** analyzes the session transcript.  
  2. **Action:** Extracts "Learned Preferences" (e.g., "User prefers arrow functions", "API key is in .env.local") and updates `CLAUDE.md`.  
  3. **Output:** Prints a "Memory Updated" summary.  
* **Minimum Setup:** Write access to `CLAUDE.md`.  
* **Biggest Risk:** Learning bad habits. **Mitigation:** User must confirm the summary update.  
* **Success Measure:** Reduced need to re-explain project context.

