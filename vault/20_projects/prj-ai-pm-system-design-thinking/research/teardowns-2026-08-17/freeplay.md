# Freeplay (freeplay.ai) — Falsification Teardown vs. Golden Loop

**Date:** 2026-08-17
**Method:** Primary sources only — docs.freeplay.ai (live-fetched), freeplay.ai marketing/blog (site was serving a Framer "Site Not Found" page during this audit; where the live page was unreachable, Google-indexed titles/snippets of freeplay.ai URLs are used and flagged), investor announcement (Renegade Partners), funding press.
**Stance:** Adversarial — trying to prove the Golden Loop gap is already closed. Freeplay explicitly targets PMs/cross-functional teams, making it the most dangerous incumbent for the hypothesis.

**Access anomaly (material):** On 2026-08-17, `https://freeplay.ai/` and all marketing paths (`/pricing`, `/blog/*`) returned HTTP 404 with a Framer "Site Not Found | Framer" shell (verified via direct curl with a browser UA and via a live browser session). `docs.freeplay.ai` and `app.freeplay.ai` are up. archive.org was "Temporarily Offline" during the audit, so no snapshot fallback. Marketing-page claims below therefore rest on search-indexed snippets of those exact URLs, marked ⚠.

---

## 1. Datasets — creation from production, versioning, curation, PM-operability

**Creation from production logs (UI path, no code):** Confirmed, first-class.
- "save completions that are recorded to Freeplay straight from the Sessions view" — click "`+ Dataset` above the completion/trace view", "Optionally, make adjustments to the inputs, history or outputs", "Select the relevant dataset(s)". Bulk add: "Select the 'Completions' or 'Traces' view on Observability (instead of Sessions)" then "Click the radio buttons in the table for the rows you want."
  Source: https://docs.freeplay.ai/core-concepts/datasets/datasets
- Also CSV/JSONL upload (with downloadable CSV template) and manual authoring in-UI. Glossary: "Datasets can be created by curating examples from production logs, uploading CSV or JSONL files, or authoring directly in the Freeplay UI."
  Sources: https://docs.freeplay.ai/core-concepts/datasets/datasets ; https://docs.freeplay.ai/resources/glossary
- API endpoints also exist (create/list prompt-level and agent-level datasets) — so both UI and programmatic paths.
  Source: https://docs.freeplay.ai/llms.txt (index listing https://docs.freeplay.ai/api-reference/prompt-datasets/create-prompt-level-dataset etc.)

**Curation workflow — they use the exact "golden" framing:** Curated entries are explicitly typed as **golden outputs** ("The output represents the ideal, correct response for the given inputs") vs **failure cases** ("The output captures a real failure observed in production — such as a hallucination, incorrect answer, or off-tone response"); you can "edit the output before saving, which allows you to curate it into a golden response or preserve it as a failure case."
Source: https://docs.freeplay.ai/core-concepts/datasets/datasets
Their curation guide names the "golden set" — "a dataset consisting of examples hand-curated by humans to be the ideal output for some given input" — as "the classic example of a broad-based dataset," and prescribes a two-pronged strategy: iterate against **targeted** datasets (e.g., "Query Hallucinations"), then validate against **broad-based** datasets to prevent regression.
Source: https://docs.freeplay.ai/core-concepts/datasets/dataset-curation

**Versioning:** NOT documented. Neither the datasets page, the curation guide, nor the glossary mentions dataset versioning, version history, snapshots, or immutability. (Prompt templates are versioned; datasets are not, per the docs.) Jan 1, 2026 changelog added "Bulk Dataset Operations: Multi-select capabilities for deleting, duplicating, or moving test cases" — i.e., datasets are mutable working sets, and duplication is the only snapshot-like primitive.
Sources: https://docs.freeplay.ai/core-concepts/datasets/datasets ; https://docs.freeplay.ai/resources/glossary ; https://docs.freeplay.ai/resources/changelog

**Can a PM do it end-to-end without code?** The curation step, yes — entirely UI. But the loop's *input* (production traces) requires prior SDK instrumentation by engineers: "When you're ready to monitor production traffic or create datasets from real user interactions, see the integration guide." And dataset creation from logs has a data-shape dependency: "Creating prompt datasets from observability logs (requires `inputs` field / knowledge of variables in your prompts)."
Sources: https://docs.freeplay.ai/getting-started/start-in-ui ; https://docs.freeplay.ai/getting-started/integrate

## 2. Holdout / split — any first-class held-out concept?

**No. This is the cleanest gap found.**
- No page in the docs defines a holdout, held-out set, or train/test split. Verified across: datasets page, dataset-curation guide, evaluations overview, eval-alignment practical guide, glossary (which defines Dataset, Test Run, Environment, Review Queue — no "Holdout", no "Golden set" entry, no "Experiment"). A `site:docs.freeplay.ai holdout OR "held-out" OR "test split"` web search returns zero Freeplay pages.
  Sources: https://docs.freeplay.ai/core-concepts/datasets/dataset-curation ; https://docs.freeplay.ai/resources/glossary ; https://docs.freeplay.ai/practical-guides/creating-and-aligning-model-graded-evals
- Closest analog: the targeted-vs-broad-based dataset strategy ("iterate against targeted datasets, then validate against broad-based datasets to prevent regression") is *directionally* an improvement/validation split — but it is advice in a guide, not a product primitive. Nothing marks the broad set as never-optimized-against; nothing stops you from running every iteration against it; there is no contamination guard.
  Source: https://docs.freeplay.ai/core-concepts/datasets/dataset-curation
- Even the eval-alignment guide — where leakage matters most — doesn't separate alignment labels from test data: "The documentation does not... mention separating alignment data from test data"; alignment labeling and benchmark testing draw on the same dataset pool ("your benchmark dataset").
  Source: https://docs.freeplay.ai/practical-guides/creating-and-aligning-model-graded-evals

## 3. Test runs / comparisons — champion/challenger? one-change discipline?

**Comparison machinery: strong, and UI-operable at component level.**
- Test Runs = "structured testing for your AI systems — aka 'evaluations', enabling you to validate performance across datasets, compare versions of your system as you make changes, and catch regressions before they reach production." Comparison model: "creating separate Test Runs for each version you want to compare, then comparing scores head to head (either in the Freeplay UI, or your code)."
  Source: https://docs.freeplay.ai/core-concepts/test-runs/test-runs
- Component-level, no-code UI path: navigate to prompt version → "click the Test button" → pick dataset, model params, name → "Freeplay processes each test case automatically". Results: overview of "scores of the different versions being tested"; "Green highlights indicate improvements while gray shows regressions"; you can "add additional comparisons to test against other versions or previous test runs."
  Source: https://docs.freeplay.ai/core-concepts/test-runs/component-level-test-runs
- End-to-end test runs **require the SDK** ("execute through the SDK in order to test your actual system" — Python/JS/Java examples; `recordings.create()`, `trace.record_output()`, `test_run_info`). A PM cannot run these alone.
  Sources: https://docs.freeplay.ai/core-concepts/test-runs/test-runs ; https://docs.freeplay.ai/core-concepts/test-runs/end-to-end-test-runs

**Champion/challenger:** Partial, informal. The e2e comparison view lets you mark a winner ("we have marked the Claude version as the winner") — a manual designation inside an analysis view, not a promotion workflow. Deployment promotion is a *separate, ungated* act: pick version → pick environment → "Deploy" ("rapidly test and iterate with the 'test' environment tag and then once a new prompt version is ready, you can promote it to staging and finally production"). The docs' bridge between testing and shipping is rhetorical, not mechanical: "Once tests pass your quality thresholds, you can deploy with confidence" — no enforced threshold, no required winning test run attached to a deploy.
Sources: https://docs.freeplay.ai/core-concepts/test-runs/end-to-end-test-runs ; https://docs.freeplay.ai/core-concepts/prompt-management/deployment-environments ; https://docs.freeplay.ai/core-concepts/test-runs/component-level-test-runs

**One-change discipline:** Absent. The only sequencing guidance is component-then-system ("Once your component changes are working well, then use end-to-end testing to validate how those changes behave within your complete system"). Nothing constrains a test run to a single variable; a new prompt version can bundle prompt text + model + hyperparameter changes (any change to any element = new version).
Sources: https://docs.freeplay.ai/core-concepts/test-runs/test-runs ; https://docs.freeplay.ai/core-concepts/prompt-management/managing-prompts

## 4. Decision records — written why-record for shipping a change?

**Nothing that functions as a promote/reject decision record.**
- Deployment environments doc: "contains no information about rollback mechanisms, approval workflows, or decision-record tracking for deployments." Deploying is one click; "Only one version per environment can be active simultaneously."
  Source: https://docs.freeplay.ai/core-concepts/prompt-management/deployment-environments
- Prompt versions carry optional `version_name` / `version_description` metadata — free-text labels, not decision artifacts; "the materials... do not describe approval workflows or mandatory change notes."
  Source: https://docs.freeplay.ai/core-concepts/prompt-management/managing-prompts
- The closest written artifact is **Review Insights / insights reports**: an agent that fires "anytime a human label is added," groups reviewed completions into "themes" and "actionable findings," and Review Queue insights reports let analysts "Share findings broadly across the organization" and "Highlight key takeaways for stakeholders." These document *failure patterns discovered*, not *why a change was shipped or rejected* — the docs "do not address whether Review Insights documents decisions about shipping changes."
  Sources: https://docs.freeplay.ai/core-concepts/ai/review-insights ; https://docs.freeplay.ai/core-concepts/review-queues

## 5. Persona walk-through — where is code mandatory?

Freeplay's own segmentation (getting-started overview):
- **UI path** — "Best for: Product managers, domain experts, or developers who want to explore Freeplay before integrating." "No code": create/iterate prompts in the playground, "Build test datasets" (playground saves, CSV/JSONL upload, manual entry), "Set up evaluations" (model-graded, auto-categorization, human labels), "Run tests to compare prompt and model changes quantitatively."
  Sources: https://docs.freeplay.ai/getting-started/overview ; https://docs.freeplay.ai/getting-started/start-in-ui
- **Code mandatory** for: (a) production observability/logging — "When you're ready to monitor production traffic or create datasets from real user interactions, see the integration guide" (SDKs: Python, TS/JS, Java, Kotlin; plus LangGraph, Vercel AI SDK, Google ADK, **OpenTelemetry** integrations); (b) end-to-end test runs (SDK-only); (c) "Code evaluations: Custom logic (requires integration)"; (d) fetching deployed prompts in the app (`get_formatted()`).
  Sources: https://docs.freeplay.ai/getting-started/start-in-ui ; https://docs.freeplay.ai/getting-started/integrate ; https://docs.freeplay.ai/core-concepts/test-runs/end-to-end-test-runs ; https://docs.freeplay.ai/core-concepts/prompt-management/deployment-environments
- Their own persona words: platform serves "Engineers, data scientists, product managers, designers, and subject matter experts"; goal is to "make Freeplay the source of truth for prompt and model configuration so non-engineers can deploy changes without code."
  Source: https://docs.freeplay.ai/getting-started/freeplay-introduction
- Investor-page framing (⚠ marketing): "as AI turns English into the most popular programming language, it's become critical to democratize evals, testing, and product improvements" so changes come "not only from developers, but also product managers, designers, and subject matter experts."
  Source: https://www.renegadepartners.com/news/freeplay-empowering-the-next-wave-of-ai-product-builders

**Net:** once engineers have instrumented once, a PM can genuinely run log→dataset→eval→component-test→compare→deploy in the UI. The PM ceiling is end-to-end/agentic testing and anything requiring code evals.

## 6. Pricing, funding, traction, 2026 releases

**Pricing:** No public per-seat prices found in any reachable primary source. ⚠ The indexed pricing page title is "Customizable packages built for teams" (https://freeplay.ai/pricing — page currently unreachable, serving Framer 404), with search-snippet evidence of **Growth** and **Enterprise** plans ("up to 50% off Growth and Enterprise plans") — i.e., sales-shaped packaging, not published self-serve pricing. Self-serve signup exists (https://app.freeplay.ai/signup, linked from https://docs.freeplay.ai/getting-started/overview) alongside a demo/sales path (freeplay.ai/demo) and a self-host/BYOC enterprise option ("Bring Your Own Cloud... In Your Cloud" — ⚠ indexed blog title, https://freeplay.ai/blog/bring-your-own-cloud-turnkey-enterprise-grade-freeplay-deployment-option-for-ai-evals-observability-in-your-cloud). A free trial existed at least as of the public-beta launch ("Freeplay is open to all" — ⚠ indexed blog, https://freeplay.ai/blog/a-better-way-to-build-with-llms-freeplay-is-now-open-to-all).

**Funding/traction:** $3.25M seed (late 2023, Conviction + Matchstick Ventures) + $5.6M round announced June 3, 2025 led by Renegade Partners — ~$8.9M total. Founded by Ian Cairns (CEO) and Eric Ryan, ex-Twitter developer platform. Named customers: Chime, Help Scout, Maze, Raptive, Stackhawk, Postscript; claimed "strong net revenue retention and high DAU/WAU engagement."
Sources: https://www.finsmes.com/2025/06/freeplay-raises-5-6m-in-funding.html ; https://www.renegadepartners.com/news/freeplay-empowering-the-next-wave-of-ai-product-builders

**2026 releases (changelog, most recent entry Feb 6, 2026 as served):**
- Jan 1, 2026: Python/Node SDKs open-sourced (Apache-2.0); "Run All Evaluations" one-click; CSV export of traces; bulk dataset operations; model management API.
- Jan 13, 2026: Search APIs (sessions/traces/completions, compound AND/OR/NOT filters); docs refresh + llms.txt.
- Feb 6, 2026: **Freeplay MCP Server (experimental)**; Project Home Page dashboard; Claude Opus 4.6 in playground; insights API endpoints.
Source: https://docs.freeplay.ai/resources/changelog
(Note: an MCP server means agentic/PM-adjacent tools can drive Freeplay conversationally — watch this; it's the vector by which they could cheaply add opinionated workflow on top of their primitives.)

## 7. VERDICT

**Where Freeplay ALREADY IS Golden Loop (closed):**
- Production failure trace → curated dataset item, in-UI, PM-operable, with explicit golden-output vs failure-case typing and even "golden set" vocabulary (docs.freeplay.ai/core-concepts/datasets/datasets, /dataset-curation). This leg is fully closed.
- Version-vs-version test runs with head-to-head score comparison, regression highlighting, and a manual "winner" designation, no-code at component level (/core-concepts/test-runs/component-level-test-runs, /end-to-end-test-runs). Mostly closed.
- The PM persona itself: Freeplay's docs explicitly name PMs as a no-code path audience and non-engineers can deploy prompt changes without code (/getting-started/overview, /getting-started/freeplay-introduction). "No tool targets PMs" is FALSE — retire that half of the differentiation hypothesis.

**Where a genuine gap remains (evidence of absence across docs, glossary, and site-scoped search):**
1. **Holdout discipline — open.** No holdout/split primitive anywhere; datasets aren't even versioned; the improvement-vs-validation idea exists only as prose advice with no contamination guard, and eval alignment reuses the same data pool.
2. **Decision records — open.** No promote/reject artifact; deployment is a one-click ungated act with "no information about rollback mechanisms, approval workflows, or decision-record tracking." Review Insights documents failures found, not decisions made.
3. **One-change round discipline — open.** Versions bundle arbitrary changes; comparisons are freeform; no experimental-hygiene enforcement.
4. **Test→ship gate — open.** "Once tests pass your quality thresholds, you can deploy with confidence" is a sentence, not a mechanism.
5. **Accessibility/price — partially open.** Sales-shaped Growth/Enterprise packaging, no published pricing; a $0/cheap self-serve opinionated layer has room underneath. (⚠ pricing evidence is snippet-grade; site was down during audit.)

**Plain statement:** Freeplay has all the *primitives* of Golden Loop and the PM persona is already served. What it lacks — verifiably, in its own docs — is the *epistemology*: nothing in the product prevents a team from optimizing against its validation data, nothing forces one variable per round, and nothing produces a written why-we-shipped record. Golden Loop survives only as an opinionated discipline layer, and its honest pitch against Freeplay is "Freeplay gives you the lab; Golden Loop gives you the scientific method." Caveat: this is a workflow-opinion moat, not a technology moat — Freeplay (with its new MCP server and open SDKs) could ship holdout flags + decision logs in a quarter, so speed and wedge (layering on *existing* trace tooling instead of requiring Freeplay's SDK instrumentation) matter more than feature depth.
