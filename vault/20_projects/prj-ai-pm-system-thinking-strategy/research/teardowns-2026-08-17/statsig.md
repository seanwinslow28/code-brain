# Statsig — Falsification Teardown vs Golden Loop

Date: 2026-08-17. Method: PRIMARY sources only — docs.statsig.com, statsig.com product/blog/updates pages, plus one OpenAI announcement URL. Every claim cites its URL. Goal: try to falsify the hypothesis that no incumbent gives a non-coding PM an opinionated offline-eval workflow (production failure → versioned golden dataset with improvement/holdout split → one-change champion/challenger round → holdout gate → written promote/reject decision record).

---

## 1. LLM/AI-specific eval products Statsig ships (2026)

**Product: "Statsig AI Evals"** — three parts, per the docs overview:

- **Prompts** — version-controlled LLM configs (prompt text + model provider, model, temperature). "Iterate on prompts and ship LLM changes with measurable quality." Retrieved in production via server SDKs; four version states: Live ("actively served to users"), Candidate ("don't appear to users, but Statsig still serves them to your code"), Draft, Archive.
  Source: https://docs.statsig.com/ai-evals/overview, https://docs.statsig.com/ai-evals/prompts
- **Offline Evals** — "quick, automated grading of model outputs on a fixed test set" to "catch wins and regressions before you expose changes to any real users." Workflow: create prompt → upload dataset of inputs + ideal answers → run model over dataset → grade (string comparison, text similarity, or LLM-as-judge with a rubric; all graders return "a score between 0 and 1") → compare scores across prompt versions.
  Source: https://docs.statsig.com/ai-evals/offline-evals
- **Online Evals** — "grade model output in production on real-world use cases," no ground truth required; auto-grading samples live traffic (configurable sampling rate over OpenTelemetry traces) or manual grading via `logEvalGrade`; candidate versions can shadow-run; "Each version's exposures and grader scores appear over time, with grader deltas relative to the Live baseline."
  Source: https://docs.statsig.com/ai-evals/online-evals

**SDKs**: Python and Node AI SDKs — "version prompts without shipping code, log eval grades back to Statsig for analysis, and run programmatic evaluations over your datasets." Methods: `get_prompt` / `get_live()` / `get_candidates()`, `log_eval_grade()`, `Eval()` (dataset + task + scorer, results sent to console). OTel tracing + OpenAI wrapper marked "Support is coming soon."
Source: https://docs.statsig.com/ai-evals/python, https://docs.statsig.com/ai-evals/node

**Marketing page** (statsig.com/ai-evals): "Deploy AI with confidence"; "Store LLM inputs in an AI config to track versions, manage releases, and run automatic evals on every new configuration"; "Upload datasets, invoke your model, and let Statsig score outputs automatically using LLMs - no bespoke scripts required." CTA is "Contact Us" — no self-serve signup, no pricing.
Source: https://www.statsig.com/ai-evals

**Status — critical**: docs.statsig.com/llms.txt states verbatim (verified by direct fetch, line 8 and the overview index entry):
> "AI Evals is Early Access and is not accepting new customers."
> "[AI Evals Overview](...): Early Access; not accepting new customers. Status: Early Access."
Source: https://docs.statsig.com/llms.txt

And the Statsig/Amplitude Phase-1 blog (post-June-2026): "Evals and LLM traces will be hitting GA in the next couple of months. And, AI experiment reports will be next."
Source: https://www.statsig.com/blog/statsig-amplitude-phase-1

So as of Aug 2026, AI Evals is pre-GA, closed to new customers, with traces and AI experiment reports still in flight.

## 2. Offline golden datasets: production-failure curation, versioning, holdout splits

- **Datasets exist**, but the documented input methods are **manual entry and CSV upload only** ("Upload a sample dataset with example inputs and ideal answers"). The offline-evals doc's dataset sections cover creation tables, per-row drill-in, and "break scores out by category" (dataset segments).
  Source: https://docs.statsig.com/ai-evals/offline-evals
- **No production-failure → dataset pipeline documented.** The online-evals doc "does not address saving failing outputs into datasets for offline testing" — graded production traffic surfaces scores/deltas, but there is no documented "add this failed trace to a dataset" action. Verified by direct grep of the offline-evals doc content: zero occurrences of "holdout" and no production-import language; "version" appears only for *prompt* versions ("You can create multiple versions of the prompt as you iterate and choose which one is 'live'").
  Sources: https://docs.statsig.com/ai-evals/online-evals, https://docs.statsig.com/api/content/ai-evals/offline-evals
- **No dataset versioning documented, no improvement/holdout split anywhere.** Statsig's editorial "Perspectives" content talks about keeping "datasets and graders versioned so results remain comparable" as a *practice*, but that is SEO/editorial writing, not a documented product feature (https://www.statsig.com/perspectives/offline-evaluation-datasets-curation). The word "holdout" in Statsig's product means an *online experiment holdout* — users withheld from feature rollouts — not an eval-dataset split (https://docs.statsig.com/sdks/how-evaluation-works).

## 3. Champion/challenger: online machinery vs offline one-change rounds

- **Online**: this is Statsig's core. Full A/B experimentation with a "world-class stats engine" (their words: https://www.statsig.com/blog/statsig-amplitude-phase-1), plus Live-vs-Candidate prompt shadow runs with "grader deltas relative to the Live baseline" (https://docs.statsig.com/ai-evals/online-evals) and "Feature Gate" targeting / experimental rollouts to tie prompt versions to business metrics (https://docs.statsig.com/ai-evals/overview).
- **Offline**: there IS a version-comparison-and-promote motion — "create multiple versions of your prompts to compare scores across versions" and pick the best performer to make Live (https://docs.statsig.com/ai-evals/offline-evals). But it is *unstructured*: no round concept, no one-change-per-round discipline, no requirement that the challenger beat the champion on a never-optimized-against holdout, no documented promotion gate at all — promotion is just flipping which version is Live. The Prompts doc references "Statsig's production change control processes and versioning" (change reviews/approvals exist on the Pro plan per https://www.statsig.com/pricing), which is an approval gate, not an evidence gate.

## 4. Decision records

- **For online experiments, yes — and it's good.** "Make a Decision" ships/abandons/resets an experiment; results freeze on decision day; "From the experiment history, you can see the new log of the experiment decision" (https://docs.statsig.com/experiments/ending/make-decision; https://docs.statsig.com/experiments/ending/conclude-experiment-defer-decision). The **Experiment Decision Framework** (product update, May 20, 2025) lets templates "configure recommended actions: Roll Out Winning Group, Discuss, or Do Not Roll Out" per metric-outcome scenario, shows "a recommendation message in the Make Decision button," and assigns a reviewer "when a shipping decision doesn't align with the recommendations" (https://www.statsig.com/updates/update/ship-decision-framework).
- **For offline eval rounds, no.** Nothing in the AI Evals docs records a written promote/reject rationale when a prompt version is made Live; the decision machinery above is wired to *experiments* (online traffic), not offline eval runs (https://docs.statsig.com/ai-evals/offline-evals, https://docs.statsig.com/ai-evals/prompts).

## 5. Persona: PM-operability

**Console-operable without code (PM-friendly):** creating prompts and versions, uploading CSV datasets, configuring graders (incl. LLM-as-judge rubrics), running offline evals — "invoke your model, and let Statsig score outputs automatically using LLMs - no bespoke scripts required" (https://www.statsig.com/ai-evals) — viewing score breakdowns, and making experiment decisions in the console (https://docs.statsig.com/ai-evals/offline-evals, https://docs.statsig.com/experiments/ending/make-decision). This is consistent with Statsig's PM-facing experimentation brand.

**Code mandatory at every production seam:** serving any prompt to users requires SDK integration (`get_prompt`/`get_live()`); online evals require either OTel instrumentation of the app or engineer-written `log_eval_grade()` calls; programmatic dataset evals (`Eval()` with custom task/scorer) are Python/Node code (https://docs.statsig.com/ai-evals/python, https://docs.statsig.com/ai-evals/online-evals). So a PM can run an offline grading pass alone, but cannot close the loop to production — or feed the loop *from* production — without engineering. And today a PM can't even start: Early Access, not accepting new customers (https://docs.statsig.com/llms.txt).

## 6. Pricing and 2026 signals

**Pricing** (https://www.statsig.com/pricing): Free/Developer tier — 2M events/mo, unlimited flag checks, 50K session replays, unlimited seats, no credit card. Pro — $150/mo, 5M events then $0.05/1K, change reviews & approvals. Enterprise — custom, warehouse-native, SSO/RBAC. **No AI Evals line item on the pricing page**; the AI Evals page's CTA is "Contact Us" (https://www.statsig.com/ai-evals).

**Corporate timeline (primary sources):**
- **Sept 2, 2025** — OpenAI acquired Statsig (~$1.1B all-stock); Vijaye Raji became CTO of Applications under Fidji Simo; "Statsig will continue to provide our services and invest in our core products." Sources: https://openai.com/index/vijaye-raji-to-become-cto-of-applications-with-acquisition-of-statsig/, https://www.statsig.com/blog/openai-acquisition
- **May 5, 2026** — Statsig's own blog (note appended to the acquisition post) records that the **Statsig product, brand, and customer base transitioned to Amplitude**, while the original team stayed at OpenAI. Sources: https://www.statsig.com/blog/openai-acquisition, https://amplitude.com/blog/amplitude-and-statsig-partnership
- **Post-June 2026 roadmap under Amplitude** (https://www.statsig.com/blog/statsig-amplitude-phase-1): Phase 1 priorities are control/governance (release pipelines for experiments), **"AI-Native Workflows"** — "Evals and LLM traces will be hitting GA in the next couple of months. And, AI experiment reports will be next," built with "Amplitude's AI divisions" — and platform scale; data-layer integration with Amplitude by end of Q3 2026.
- Product-updates feed (https://www.statsig.com/updates) shows 2025–2026 AI features are console-assistant flavored (AI-Powered Experiment Summary, AI Stale Gate Cleanup, Statsig ChatGPT App Feb 2026) — no dataset-curation or golden-dataset releases.

**Direction read**: movement into offline-eval territory is real (offline evals + datasets + graders shipped; evals/traces GA imminent) but the platform changed hands twice in nine months, the builders are at OpenAI, and the surviving roadmap is Amplitude-integration-first. Nothing published points at production-failure curation, dataset versioning, holdout splits, or offline decision records.

## 7. VERDICT

**VERDICT: Partial overlap, hypothesis survives.** Statsig ships a genuinely PM-operable offline eval primitive — console-run CSV datasets, LLM-as-judge graders, prompt-version score comparison (docs.statsig.com/ai-evals/offline-evals) — which falsifies the narrow claim that "no incumbent lets a non-coder run offline evals." But every opinionated element of Golden Loop is absent from primary sources: no production-failure → dataset curation path (online-evals doc has no save-to-dataset action), no dataset versioning or improvement/holdout split (verified zero "holdout" occurrences in the offline-evals doc; "holdout" at Statsig means online user holdouts), no one-change round discipline, no holdout promotion gate, and no written promote/reject record for offline prompt promotion — Statsig's excellent decision-record machinery (Make a Decision + Decision Framework) is wired exclusively to online experiments. Compounding the gap: AI Evals is "Early Access and is not accepting new customers" (docs.statsig.com/llms.txt) and pre-GA per the Amplitude Phase-1 blog, and the product just moved OpenAI → Amplitude (May 5, 2026) with its original team staying at OpenAI. Statsig's real threat vector is the opposite direction — an unmatched *online* champion/challenger + decision layer that Golden Loop should interoperate with, not compete against.
