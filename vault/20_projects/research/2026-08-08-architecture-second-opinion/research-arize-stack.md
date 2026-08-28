Research complete. All findings below are from primary sources fetched today (2026-08-08) unless noted.

# Arize Stack for a Solo Founder — 2026 Research Report

## Per-source findings

**1. https://arize.com/pricing (fetched 2026-08-08)**
- **AX Free**: $0 — 25k spans/mo, 1 GB ingestion/mo, 15-day retention, unlimited users, unlimited evals.
- **AX Pro**: $50/mo — 50k spans/mo, 10 GB, 30-day retention, unlimited users/evals.
- **AX Enterprise**: custom everything; SaaS or self-hosted (VPC/Private Connect); adds managed agents, Data Fabric, Alyx, SSO, audit logs, HIPAA. Third-party sources (cekura.ai, spotsaas) put median enterprise contracts at ~$50–100k/yr with no published tier between $50/mo and enterprise.
- Startup discount program exists (application-based).

**2. https://arize.com/products/phoenix-plus-arize-ax/ (fetched 2026-08-08)**
- Shared by both: tracing, evaluation, datasets & experiments, annotations, prompt playground.
- AX-only: custom dashboards, **online evals**, **monitoring & alerting**, Alyx copilot, ML/CV support, dedicated support, managed usage settings. Phoenix = self-hosted or Phoenix Cloud; positioned for "<1TB data" teams. Documented OSS→AX migration path exists.

**3. https://github.com/Arize-ai/phoenix (fetched 2026-08-08)**
- License: **Elastic License 2.0 (ELv2), with portions under U.S. patents** — free for internal use, but you cannot offer Phoenix itself as a managed service to third parties.
- ~10.9k stars. Features: tracing (OTel/OpenInference), evals, datasets, experiments, playground, prompt management with versioning, PXI (Phoenix Intelligence agent), and a **remote MCP server that integrates with Claude Code/Cursor**.

**4. https://arize.com/docs/phoenix/self-hosting + /configuration (fetched 2026-08-08)**
- Deploy via CLI/pip, Docker (`arizephoenix/phoenix`, root/nonroot/pinned tags), K8s/Helm, CloudFormation, Cloud Run, Railway, Render. "No license fees, no usage limits, no feature gates"; air-gapped capable.
- DB: **SQLite default — in a temp folder unless `PHOENIX_WORKING_DIR` is set** (silent data loss trap); **PostgreSQL recommended for production** via `PHOENIX_SQL_DATABASE_URL`, read-replica support.
- Retention: `PHOENIX_DEFAULT_RETENTION_POLICY_DAYS` **defaults to 0 = infinite retention** (unbounded DB growth); per-project override in UI.
- Auth: local accounts, OAuth2, LDAP, RBAC, strong-password policy, CSRF origins, OAuth2 authz server for MCP clients. No published minimum resource specs — a Mac Mini/small VPS is plausible at solo-founder volume.

**5. Agent-specific features — https://arize.com/ai-agents/agent-observability/, https://arize.com/docs/ax/evaluate/session-level-evaluations, https://arize.com/docs/phoenix/tracing/tutorial/sessions, https://arize.com/blog/evals-in-ci-how-to-write-llm-evals-as-tests (fetched 2026-08-08)**
- **Agent graph/trajectory visualization is an AX feature** — interactive graph + path diagrams of multi-agent runs; Phoenix has trace/timeline views and sessions but not the managed trajectory layer.
- **Session-level evals** (coherence, context retention, goal achievement, task progression across multi-turn sessions, LLM-as-judge across all sessions) documented under AX docs; Phoenix supports session grouping + running evals locally, but continuous/automatic session evals are AX.
- **Evals-in-CI**: Phoenix now supports writing evals as ordinary **Pytest/Vitest/Jest tests**; experiment runs record traces and can assert on cost/latency/quality regressions. Pre-built judge templates benchmarked to "70–90% precision" on golden datasets; Arize publishes judge-calibration guidance (calibrate built-in prompts on your own data before trusting scores) — guidance and datasets, not an automated calibration tool in OSS.
- Framework integrations span LangGraph, CrewAI, AutoGen, Agno, smolagents, OpenAI Agents SDK via OpenInference/OTel.

**6. PII/redaction — https://arize.com/docs/ax/instrument/mask-and-redact-data, https://github.com/Arize-ai/openinference/issues/3203 (fetched 2026-08-08)**
- Two mechanisms: **masking** (TraceConfig/env vars hide whole attribute categories — all inputs, all outputs, embeddings) and **redaction** (custom span processor for patterns like emails/SSNs) — both run client-side before export.
- Open issue #3203 confirms the gap: **no single privacy preset**; you must reason about multiple individual flags, and the default is capture-everything.

**7. Alternatives (all fetched 2026-08-08)**
- **Langfuse** (langfuse.com/pricing): Hobby cloud free = **50k units/mo, 30-day access, 2 users**; Core **$29/mo** = 100k units + $8/100k overage, 90-day retention, unlimited users; Pro $199. **Self-host free, MIT-core, Docker Compose/K8s templates.** At 1M events ≈ $101/mo (morphllm comparison).
- **LangSmith** (langchain.com/pricing): free = **5k traces/mo, 1 seat, 14-day retention**; Plus $39/seat + pay-as-you-go (LCU $1.50 / LSU $1.00); self-hosting enterprise-only. Weakest free tier of the group.
- **Braintrust** (braintrust.dev/pricing): free = 1 GB processed data, 10k scores, 14-day retention, unlimited users, $10 model credits; then a **cliff straight to Pro $249/mo** (though 6–12 months free for qualifying startups).
- **W&B Weave** (wandb.ai/site/pricing): free = 1 GB/mo ingestion, tracing + evals + LLM-judge included; Pro from $60/mo, overage $0.10/MB (expensive at scale).

---

## (a) Recommended minimal Arize setup

**Phoenix OSS self-hosted in Docker on the Mac Mini, backed by PostgreSQL — $0/month.** Pin the image version, set `PHOENIX_SQL_DATABASE_URL` (not default SQLite), set `PHOENIX_DEFAULT_RETENTION_POLICY_DAYS` (e.g., 30–90), enable local auth. Instrument the fleet via OpenInference OTel exporters; run session-grouped traces + evals-as-pytest in CI; wire nightly eval runs via your existing launchd layer (substituting for AX's online evals). Optionally add an **AX Free account (25k spans/mo)** pointed only at the customer-facing product's production slice to get monitors/alerting and agent-trajectory views without paying. Total projected cost: **$0, worst case $50/mo (AX Pro)** — comfortably inside the $250/mo opex cap. Bonus fit: Phoenix ships a remote MCP server that plugs into Claude Code, which matches this repo's existing `arize-*` skill inventory.

## (b) Three biggest gotchas to design around

1. **Storage/retention footguns**: default SQLite lives in a *temp folder* (data loss on restart unless `PHOENIX_WORKING_DIR` is set) and default retention is *infinite* (DB grows unbounded). Use Postgres + explicit retention from day one. Conversely, AX Free retains only 15 days — too short to be your system of record.
2. **PII redaction is opt-in and DIY**: capture-everything is the default; there is no one-flag privacy preset (open OpenInference issue #3203). You must configure TraceConfig masking + a custom redaction span processor client-side before any span leaves the app — critical if traces carry customer data.
3. **The good agent stuff is gated, and the AX free/Pro span caps are tiny for a fleet**: online/continuous evals, alerting, dashboards, and agent-trajectory graphs are AX-only, and 25k–50k spans/mo evaporates fast when scheduled agents emit spans all night. Design span sampling/routing (what goes to AX vs local Phoenix) up front, and accept that alerting on self-hosted Phoenix is something you build (cron + eval + Pushover).

## (c) One-line verdict

**Yes — Phoenix self-hosted remains the right pick at ≤$250/mo (it's the only option with zero usage caps, full evals/experiments/CI support, and on-prem data control for $0), with Langfuse (MIT, 50k-unit free cloud, $29 Core) as the only materially credible switch if you'd rather have a managed cloud with alerting than run a container — and LangSmith/Braintrust/Weave all price out or cliff for this profile.**