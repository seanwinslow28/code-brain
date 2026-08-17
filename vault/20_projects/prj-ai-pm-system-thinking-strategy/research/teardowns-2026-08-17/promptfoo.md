# Falsification Teardown: promptfoo vs Golden Loop

**Date:** 2026-08-17 · **Method:** primary sources only (promptfoo.dev docs, github.com/promptfoo/promptfoo, pricing/press/blog pages), fetched live. Each claim carries its source URL.

**Golden Loop under test:** production failure trace → curated versioned golden dataset (improvement/holdout split) → champion/challenger round testing exactly ONE change → challenger must beat champion on never-optimized-against holdout → written promote/reject decision record. Hypothesis to falsify: incumbents are engineer-first; no opinionated end-to-end PM workflow with holdout discipline + decision records.

---

## 1. Test sets: how eval cases are defined

- **Formats:** inline YAML in `promptfooconfig.yaml`; CSV/Excel (XLSX) with `__expected`, `__description`, `__prefix`, `__suffix`, `__metadata:*` special columns; JSON/JSONL; external YAML files (`file://tests.yaml`, wildcards); programmatic JS/Python test generators; Google Sheets, SharePoint, HuggingFace Datasets, Azure Blob Storage. — https://www.promptfoo.dev/docs/configuration/test-cases/
- **Synthetic dataset generation:** `promptfoo generate dataset` "extend[s] existing datasets and help[s] make them more comprehensive and diverse" via persona-based generation (`--numPersonas`, `--numTestCasesPerPersona`); output to YAML/CSV or written into config. — https://www.promptfoo.dev/docs/configuration/datasets/
- **Production traces → test cases: NO first-class path.** Tracing is OpenTelemetry (OTLP)-based and exists to observe *what the app did during an eval*: "Promptfoo uses OpenTelemetry (OTLP) traces to show what your application did behind each response and bring that information into your evals." It can *look up* traces from Grafana Tempo, Braintrust, or Langfuse for eval context, but the docs describe no conversion of production failures into test cases. — https://www.promptfoo.dev/docs/tracing/
- The test-case configuration page makes no mention of importing tests from production traces or logs. — https://www.promptfoo.dev/docs/configuration/test-cases/
- **Versioning beyond git: none documented.** Test files are files; `promptfoo import <filepath>` / `promptfoo export eval <evalId>` move *eval result records* (JSON), not versioned datasets. — https://www.promptfoo.dev/docs/usage/command-line/
- Dataset-generation docs contain "no mention of train/test splits, data versioning, holdout concepts, or any data partitioning strategies." — https://www.promptfoo.dev/docs/configuration/datasets/

## 2. Holdout / split

- **One real but narrow split concept exists:** `promptfoo optimize --validation-split <fraction>` — "Reserves up to half of test cases for validation scoring while optimization search uses the remaining set (default: none)." And: "When `--validation-split` is omitted, optimization uses the full eval set and may overfit to the configured cases." Requires explicit `tests` (scenarios must be expanded first). — https://www.promptfoo.dev/docs/usage/command-line/
- **Assessment:** this is an anti-overfitting flag inside the *automated prompt-optimizer* command, default OFF, engineer-invoked, per-run and ephemeral. It is not a persistent, curated, never-optimized-against holdout dataset governing promotion decisions. No holdout concept exists anywhere else in test-case, dataset, CI/CD, or enterprise docs (searched; none found). — https://www.promptfoo.dev/docs/configuration/datasets/ ; https://www.promptfoo.dev/docs/integrations/ci-cd/

## 3. Comparison workflow / regressions / promotion

- **Side-by-side comparison is core:** "Compare models side-by-side (OpenAI, Anthropic, Azure, Bedrock, Ollama, and more)" (README). — https://github.com/promptfoo/promptfoo
- **Web viewer:** `promptfoo view` opens a results UI with a scatter plot to "compare two prompts head-to-head" (green/red/gray relative scoring), filtering by metrics/metadata/pass-fail, "Edit and re-run," export to YAML/CSV/JSON/DPO JSON. — https://www.promptfoo.dev/docs/usage/web-ui/
- **CI/CD regression gating:** dedicated GitHub Action; PR-triggered evals; "Catch regressions early — Test prompt changes before they reach production"; pass/fail gates by parsing results (`if [ "$FAILURES" -gt 0 ] … exit 1`); shareable URLs posted to PR comments/Slack (`jq -r '.shareableUrl'`). — https://www.promptfoo.dev/docs/integrations/ci-cd/
- **Sharing:** `promptfoo share` uploads eval snapshots; cloud (promptfoo.app) gives "private links only visible to you and your organization"; Enterprise adds "role-based permissions for shared evals" + SSO; self-host option. — https://www.promptfoo.dev/docs/usage/sharing/
- **Promotion / champion-challenger: absent.** CI/CD docs verified: "The documentation does not discuss prompt versioning, champion/challenger deployments, or decision recording mechanisms." — https://www.promptfoo.dev/docs/integrations/ci-cd/

## 4. Decision records

- **None.** No feature in docs (CI/CD, sharing, enterprise, web UI, releases) records *why* a change shipped, who approved it, or a promote/reject rationale. The nearest artifacts are shareable eval-result URLs and exported eval JSON — evidence, not decisions. — https://www.promptfoo.dev/docs/integrations/ci-cd/ ; https://www.promptfoo.dev/docs/usage/sharing/ ; https://www.promptfoo.dev/docs/enterprise/

## 5. Persona / non-code path / enterprise tier

- **Self-description is engineer-first:** "Developer-first: Fast, with features like live reload and caching"; tagline "Test your prompts, agents, and RAGs. Red teaming/pentesting/vulnerability scanning for AI." — https://github.com/promptfoo/promptfoo
- **Getting-started targets developers** (npx CLI, YAML config); partial non-code entry via `promptfoo eval setup` browser config UI, but the workflow remains CLI/YAML-anchored. — https://www.promptfoo.dev/docs/getting-started/
- **Web UI is analysis-first, not authoring-first:** viewing/filtering/comparison; docs "don't explicitly confirm that non-technical users can create initial tests through the UI alone." — https://www.promptfoo.dev/docs/usage/web-ui/
- **Enterprise adds:** RBAC, teams-based config, "Detailed reporting and analytics to monitor the security of your LLM applications," remediation suggestions, advanced eval filtering, SIEM/issue-tracker integrations, professional services + dedicated Slack. Enterprise docs "do not explicitly mention product managers, business users, or non-engineers" — the framing is security teams and developers. — https://www.promptfoo.dev/docs/enterprise/
- Pricing page framing: Community tier "perfect for individual developers and small teams"; Enterprise adds SSO, custom roles, centralized security/compliance dashboard, continuous monitoring — a **security** dashboard, not a PM decision console. — https://www.promptfoo.dev/pricing/

## 6. Pricing, license, 2026 signals

- **License:** MIT; ~24.3k GitHub stars; TypeScript. — https://github.com/promptfoo/promptfoo
- **Pricing:** Community free (OSS, core evals, 10k red-team probes/month, self-host); Enterprise custom-priced (no figures published); On-Premise custom (adds full data isolation + dedicated deployment engineer). — https://www.promptfoo.dev/pricing/
- **Biggest 2026 signal — acquired by OpenAI (announced 2026-03-09):** "Promptfoo is part of OpenAI" (press page). Blog: "We will continue to maintain the open-source suite as a best-in-class red teaming, static scanning, and evals tool"; "At OpenAI, we'll improve and integrate Promptfoo's core tech within the model and infrastructure layers." Traction cited: 350k+ developers, 130k monthly active, >25% of Fortune 500. — https://www.promptfoo.dev/press/ ; https://www.promptfoo.dev/blog/promptfoo-joining-openai/ (secondary corroboration: https://techcrunch.com/2026/03/09/openai-acquires-promptfoo-to-secure-its-ai-agents/ , https://www.cnbc.com/2026/03/09/open-ai-cybersecurity-promptfoo-ai-agents.html)
- **2026 release direction is security/provider-breadth, not PM workflow:** Jan-2026 highlights = adaptive rate limiting, video-gen providers, telecom red-team plugin, RAG source-attribution plugin, multi-input red teaming, UI filter polish. Releases page shows no non-technical authoring, dataset versioning, holdout, promotion, or decision-record features. — https://www.promptfoo.dev/docs/releases/
- **Directional read:** the acquisition points promptfoo's roadmap *toward OpenAI's model/infra security layers*, i.e., further from a vendor-neutral PM decision product — while also creating uncertainty about the OSS tool's long-term independence.

## 7. VERDICT

**Real overlap:** eval harness mechanics — declarative test sets (YAML/CSV/Sheets), side-by-side prompt/model comparison with a head-to-head scatter UI, CI regression gating with shareable results, and one genuine anti-overfitting split (`optimize --validation-split`, default off, scoped only to the auto-optimizer). — https://www.promptfoo.dev/docs/usage/web-ui/ ; https://www.promptfoo.dev/docs/usage/command-line/ ; https://www.promptfoo.dev/docs/integrations/ci-cd/

**Real gap (hypothesis NOT falsified):** no production-failure→test-case path (tracing observes evals; no conversion), no versioned/curated golden dataset beyond files-in-git, no persistent never-optimized-against holdout governing promotion, no champion/challenger or promote/reject workflow, no decision records anywhere, and an explicitly "developer-first" persona whose enterprise tier is a *security* console — with the 2026 OpenAI acquisition steering the roadmap toward infra-layer security, not PM-grade decision workflow. Golden Loop's loop (trace→curated split dataset→one-change round→holdout gate→written decision) does not exist in promptfoo. — https://www.promptfoo.dev/docs/tracing/ ; https://www.promptfoo.dev/docs/configuration/datasets/ ; https://www.promptfoo.dev/docs/enterprise/ ; https://www.promptfoo.dev/blog/promptfoo-joining-openai/

**Caveat for the build case:** promptfoo's `--validation-split` overfitting warning is primary-source proof that the *problem* Golden Loop formalizes is recognized by incumbents — nearest-neighbor evidence, and also a sign the concept could be productized by them later.
