# Teardown: Langfuse vs Golden Loop

Date: 2026-08-17. Sources: primary only — langfuse.com docs/changelog/blog/pricing, github.com/langfuse/langfuse. Every claim carries its source URL. Job A: falsify the gap (does Langfuse already give a non-coding PM the Golden Loop workflow?). Job B: feasibility-check the importer integration.

---

## 1. Datasets deep-dive

**Creation from traces — yes, one-click and bulk, in the UI.**
- UI path: `Your Project > Datasets > + New dataset`. From production traces: an `+ Add to dataset` button exists on any trace span/event/generation; the created item is linked back via `source_trace_id` and optionally `source_observation_id`. Bulk: select multiple rows in the Observations table → `Actions → Add to dataset`, with configurable field mapping (which observation fields land in item input/expected output). Source: https://langfuse.com/docs/evaluation/experiments/datasets
- Item schema: `input` (any JSON, required for experiments), `expectedOutput` (optional), `metadata` (optional), media attachments supported in all three fields. Confirmed field list in the data model: `id`, `datasetId`, `input`, `expectedOutput`, `metadata`, `status` (ACTIVE/ARCHIVED), `sourceTraceId`, `sourceObservationId`, `mediaReferences`. Sources: https://langfuse.com/docs/evaluation/experiments/datasets , https://langfuse.com/docs/evaluation/experiments/data-model
- Optional JSON Schema validation can enforce item structure on `input`/`expectedOutput`. Source: https://langfuse.com/docs/evaluation/experiments/datasets

**Versioning — first-class and recent.**
- "Every `add`, `update`, `delete`, or `archive` of dataset items produces a new dataset version"; versions are timestamp-identified; GET APIs return latest by default. Source: https://langfuse.com/docs/evaluation/experiments/datasets
- Shipped 2025-12-15 (Dataset Item Versioning): https://langfuse.com/changelog/2025-12-15-dataset-versioning
- 2026-02-11: fetch datasets at a version timestamp and run experiments on historical versions via UI/API/SDK for reproducibility and regression testing; UI toggle under `Datasets > [dataset] > Items` tab. Source: https://langfuse.com/changelog/2026-02-11-versioned-dataset-experiments
- Caveat found in UI-experiments doc: UI-launched experiments were documented as running on the latest dataset version only (the Feb 2026 changelog says versioned runs now work via UI too — docs pages are mid-migration on this point). Sources: https://langfuse.com/docs/evaluation/experiments/experiments-via-ui , https://langfuse.com/changelog/2026-02-11-versioned-dataset-experiments

**Non-engineer curation end-to-end in UI: yes.** Creation, add-from-trace, bulk add with field mapping, edit, archive, folders (slash-named virtual folders) are all UI operations; SDK is optional. Source: https://langfuse.com/docs/evaluation/experiments/datasets

## 2. Holdout / split

**No first-class split or holdout concept anywhere.**
- The dataset item schema has **no split/partition/holdout field** — confirmed against the experiments data model field list (`id, datasetId, input, expectedOutput, metadata, status, sourceTraceId, sourceObservationId, mediaReferences`). Source: https://langfuse.com/docs/evaluation/experiments/data-model
- The evaluation docs overview does not mention holdout sets, champion/challenger, or promotion workflows at all. Source: https://langfuse.com/docs/evaluation/overview
- Closest primitives: separate datasets (e.g. `golden/improvement` and `golden/holdout` via folder naming), or a `metadata` convention (`{"split": "holdout"}`) — both are user convention, with **no enforcement** that a holdout dataset was never optimized against. Sources: https://langfuse.com/docs/evaluation/experiments/datasets (folders, metadata)

**Verdict for this section: gap is real.** Split is convention-only; "never-optimized-against" is a policy Langfuse has no mechanism to express or enforce.

## 3. Experiments / evals

**Dataset runs & comparison.**
- "Dataset runs are used to run a dataset through your LLM application and optionally apply evaluation methods to the results. This is often referred to as Experiment run." Source: https://langfuse.com/docs/evaluation/core-concepts (via search snippet; see also https://langfuse.com/docs/glossary)
- UI experiments: pick a dataset → `Start Experiment` → choose a prompt (from Prompt Management) + model (configured LLM connection) → run; no code required; results in an experiments table with aggregated scores. Prereqs: prompt variables matching dataset item keys, JSON inputs/expected outputs, LLM connection. Limitation: UI experiments test prompt+model only — full application/agent logic requires the SDK path. Source: https://langfuse.com/docs/evaluation/experiments/experiments-via-ui
- Comparison view: select two runs → `Compare` → side-by-side outputs per dataset item, matched on stable item identifiers, with green/red deltas for scores/cost/latency; Charts tab shows distributions. Sources: https://langfuse.com/changelog/2024-11-18-dataset-runs-comparison-view , https://langfuse.com/changelog/2025-11-06-compare-view-baseline-support

**Champion/challenger — partially, as "baseline," since 2025-11-06.**
- Baseline support in compare view: designate one run as "the production baseline," see matched baseline-vs-candidate rows, filter by score thresholds/deltas to build a regression work queue. Langfuse's own framing: "teams need to know if the candidate actually improves upon production." Source: https://langfuse.com/changelog/2025-11-06-compare-view-baseline-support
- This is comparison-only: there is **no promotion action, no promotion state, and no record of a decision** attached to the baseline concept.
- 2026-04-13, "Experiments as a First-Class Concept": experiments decoupled from datasets ("Experiments exist independently"), run against dataset items, production traces, or local data; unified experiments list; performance deltas and threshold filtering in UI. Requires Langfuse v4 (Cloud toggle; self-host upgrade from v3). Source: https://langfuse.com/changelog/2026-04-13-experiments-rebuild

**LLM-as-a-judge.**
- UI wizard (`Evaluators > + Set up Evaluator`), managed evaluator catalog (incl. Ragas-maintained), custom `{{variable}}` prompts; runs on live production traces (observation-level) AND on experiment runs over datasets. Requires an LLM connection whose default model supports structured output. Also manageable programmatically via public API (that management API is flagged "currently unstable and may change"). Source: https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge
- PM-operable: yes, the primary path is the UI wizard with live prompt preview. Same source.

**Human annotation / annotation queues.**
- Queues let domain experts score traces/observations/sessions; require a score config defining scoring dimensions; items added via UI checkbox+Actions or via API; card-based, keyboard-driven annotation UI ("Complete + next"). Source: https://langfuse.com/docs/evaluation/evaluation-methods/annotation-queues
- Experiment results can be annotated directly from the experiment compare view (UI or SDK runs). Source: https://langfuse.com/docs/evaluation/evaluation-methods/annotation-queues (cross-referenced in annotation docs, https://langfuse.com/docs/evaluation/evaluation-methods/annotation)
- Tier gating: Hobby cloud = 1 annotation queue; "Unlimited annotation queues" arrives at Pro ($199/mo). Self-host OSS: annotation queues are MIT since 2025-06-04. Sources: https://langfuse.com/pricing , https://langfuse.com/blog/2025-06-04-open-sourcing-langfuse-product

## 4. Decision records

**Nothing.** The only writable "why" surfaces are freeform: a DatasetRun has optional `description` and `metadata` fields (https://langfuse.com/docs/evaluation/experiments/data-model); scores carry a `comment` field (same source). There is no promote/reject object, no required rationale on a prompt-label change, no audit-style decision document anywhere in the evaluation docs (https://langfuse.com/docs/evaluation/overview — explicitly silent on promotion decisions). Audit Logs exist but are an Enterprise compliance feature (who-did-what), not a decision-rationale record (https://langfuse.com/pricing , https://langfuse.com/blog/2025-06-04-open-sourcing-langfuse-product). **Gap is fully real.**

## 5. Prompt management — the closest thing to champion/challenger

- Every prompt save creates a numbered version; labels (`production`, `latest`, custom like `prod-a`/`prod-b`, `staging`, tenant labels) are movable pointers. SDKs serve the `production`-labeled version by default. Promotion = assign the `production` label to a version, in the UI or via SDK. Rollback = reassign the label to a prior version, immediate. Source: https://langfuse.com/docs/prompt-management/features/prompt-version-control
- **Protected labels**: admins/owners can protect `production` so viewers/members cannot move it — an RBAC-gated promotion step. Same source.
- The docs explicitly describe running experiments to compare prompt versions on datasets "before promoting labels, enabling data-driven decisions on which version advances to production." Same source.
- Non-engineers can operate all of it in the UI. Same source.
- **How close to Golden Loop:** this IS champion/challenger *deployment mechanics* for the special case where the one-change-under-test is a prompt: version = challenger, `production` label = champion, label move = promotion, protected label = gate. What's missing: no linkage requiring a passing experiment before a label move, no holdout discipline, no recorded rationale on the move. And it only covers prompt changes — not model, tool, or agent-logic changes.

## 6. Integration feasibility

**API surface.**
- REST at `/api/public`, Basic Auth (username = public key, password = secret key), regional bases (US/EU/JP/HIPAA). OpenAPI spec: https://cloud.langfuse.com/generated/api/openapi.yml ; reference: https://api.reference.langfuse.com. Typed clients in Python (v4+), JS/TS (v5+), Java via the client's `api` property. Sources: https://langfuse.com/docs/api , https://langfuse.com/docs/api-and-data-platform/features/public-api
- Reading traces: `GET /api/public/traces` supports page/limit pagination and filters (userId, name, sessionId, tags, version, release, environment, from/toTimestamp) **but is documented as deprecated**, with migration pointing to the newer data APIs. Sources: https://langfuse.com/docs/api-and-data-platform/features/public-api , https://langfuse.com/docs/api-and-data-platform/features/query-via-sdk
- Replacement: **Observations API v2** — `GET /api/public/v2/observations`, cursor-based pagination (base64 cursor in `meta`), sorted by startTime desc, filters incl. traceId, name, type, level, environment, isRootObservation, plus an advanced JSON `filter` param and `trace_context` fields (tags, release, traceName); rows must be grouped by `traceId` to reconstruct a trace. Sources: https://langfuse.com/docs/api-and-data-platform/features/observations-api , https://langfuse.com/changelog/2026-05-15-v2-observations-trace-context
- Also current: Scores API v3 (typed values, for reading judge/human scores — i.e., the "flagged failure" signal), Metrics API v2. Source: https://langfuse.com/docs/api-and-data-platform/features/public-api
- Writing: dataset items are creatable via API/SDK with `sourceTraceId`/`sourceObservationId` linkage — exactly the importer's write path. Sources: https://langfuse.com/docs/evaluation/experiments/datasets , https://langfuse.com/docs/evaluation/experiments/data-model

**Self-hosting.**
- Docker Compose is the documented low-scale path: clone repo, set secrets, `docker compose up`, UI on `localhost:3000` in ~2-3 min. Stack: langfuse-web + langfuse-worker + Postgres (OLTP) + ClickHouse (OLAP for traces/observations/scores) + Redis/Valkey + MinIO/S3. VM guidance: "at least 4 cores and 16 GiB of memory," ~100GB storage; local Mac via Docker Desktop "can operate with less" (explicitly positioned as "the simplest way to run Langfuse to give it a try"). No HA/scaling/backup in compose. All components must run UTC. Sources: https://langfuse.com/self-hosting/deployment/docker-compose , https://langfuse.com/self-hosting
- Practical read for Sean's M-series Mac: feasible for a single-user pilot, but this is a 6-container stack with ClickHouse — heavier than a typical side-project dependency.

**Stability signals.**
- Semver with a written policy: breaking = infra changes or removal of public APIs/params (major bump); DB schema and frontend-API changes are non-breaking. Each server major aims to support current + previous SDK major. Deprecations get published schedules + migration guides. Source: https://langfuse.com/self-hosting/upgrade/versioning
- Active churn to plan around: v3→v4 transition in progress (experiments rebuild requires v4, 2026-04-13); legacy Ingestion API sunsets on Langfuse Cloud **2026-11-16**; traces GET deprecated; LLM-as-a-judge management API self-described "currently unstable." Sources: https://langfuse.com/changelog/2026-04-13-experiments-rebuild , https://langfuse.com/docs/api-and-data-platform/features/public-api , https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge
- Corporate: repo states Langfuse is "part of ClickHouse since January 2026"; 33.2k stars, active development (476 open PRs at fetch time). Acquisition = long-term-support question mark but near-term investment signal. Source: https://github.com/langfuse/langfuse

**License.**
- "This repository is MIT licensed, except for the `ee` folders." Source: https://github.com/langfuse/langfuse
- Since 2025-06-04, LLM-as-a-judge, annotation queues, prompt experiments, and playground are MIT; remaining commercial: enterprise security, SCIM, audit logs, data retention policies, enterprise support. Source: https://langfuse.com/blog/2025-06-04-open-sourcing-langfuse-product
- Everything Golden Loop needs (traces, datasets, experiments, judges, queues, prompt labels, public API) is in the MIT core on self-host, $0. Sources: above + https://langfuse.com/pricing ("open source" self-deployment at no cost)

## 7. Persona and pricing

- Pricing (cloud): Hobby free — 50k units/mo, 30-day data access, 2 users, all features, 1 annotation queue; Core $29/mo (100k units, 90-day, unlimited users); Pro $199/mo (3-year retention, unlimited annotation queues, SOC2/ISO reports, 20k req/min API); Enterprise $2,499/mo (audit logs, SCIM, dedicated engineer). Datasets, experiments, LLM-as-a-judge available on all tiers. Source: https://langfuse.com/pricing
- Persona: historically engineer-first (SDK/OTel instrumentation is unavoidable to get traces in), but the 2025-2026 arc is a visible march toward PM-operable workflow: UI experiments on datasets with LLM-as-a-judge (2024-11-22, https://langfuse.com/changelog/2024-11-22-prompt-experimentation), run comparison view (2024-11-18, https://langfuse.com/changelog/2024-11-18-dataset-runs-comparison-view), baseline compare (2025-11-06, https://langfuse.com/changelog/2025-11-06-compare-view-baseline-support), dataset versioning (2025-12-15, https://langfuse.com/changelog/2025-12-15-dataset-versioning), versioned-dataset experiments (2026-02-11, https://langfuse.com/changelog/2026-02-11-versioned-dataset-experiments), experiments as first-class (2026-04-13, https://langfuse.com/changelog/2026-04-13-experiments-rebuild). Once an engineer wires tracing + an LLM connection, a PM can run curate→experiment→judge→compare→promote-prompt-label entirely in the UI (https://langfuse.com/docs/evaluation/experiments/experiments-via-ui , https://langfuse.com/docs/prompt-management/features/prompt-version-control).
- **This roadmap direction is itself a risk to Golden Loop's differentiation**: Langfuse shipped baseline-vs-candidate and versioned datasets within the last 9 months and is clearly still building in this exact direction.

## 8. VERDICT

**Covered by Langfuse today (don't rebuild):** trace→dataset curation (one-click + bulk, UI, source-trace linkage); timestamped dataset versioning incl. experiments on historical versions; UI-run experiments (prompt+model) with LLM-as-a-judge and human annotation queues; side-by-side run comparison with a designated production **baseline** and score/cost/latency deltas; prompt version promotion via a protected `production` label with RBAC. That is roughly 70% of Golden Loop's mechanical substrate, all PM-operable in the UI after one-time engineering setup.

**Gap is real (Golden Loop's actual product):** (1) no split/holdout concept anywhere — no field, no enforcement of "never optimized against"; (2) no promotion *decision* object — baseline compare renders evidence but promotion is an unrecorded label move with no required rationale; (3) no one-change-at-a-time discipline — nothing stops a run varying prompt+model+data simultaneously; (4) no closed loop tying "challenger beat champion on holdout" to the act of promotion. Golden Loop is the *governance layer* — Langfuse is the instrument bench.

**Importer feasibility in ~1 week part-time: yes.** Read side: Scores API v3 + Observations API v2 (cursor-paginated, filterable by tags/environment/time, Basic Auth) to find flagged failures; write side: create dataset items with `sourceTraceId` — both documented, typed Python SDK available, OpenAPI spec published, MIT-licensed on a $0 docker-compose self-host that runs on a Mac. Two engineering cautions: build against Observations v2/Scores v3 (traces GET is deprecated; legacy ingestion sunsets 2026-11-16) and pin to a v4 server, since the platform is mid-v3→v4 migration.
