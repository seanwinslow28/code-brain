---
title: Agent Fleet Observability Dashboard Architecture and Positioning Validation
date: 2026-05-15
language: en-US
status: Final
scope: Public portfolio artifact for agent-ops validation, recruiter discovery, and dashboard information architecture
---

# Agent Fleet Observability Dashboard Validation

## Executive Take

The strongest v0 is **a static, recruiter-safe observability page on Sean’s personal domain, built as an Astro page and deployed on Vercel, with a GitHub Pages mirror as a quiet fallback**. That combination best matches the public portfolio surfaces that already look credible in this category: named-domain project pages like Damilola Elegbede’s Cortex fleet activity page, public GitHub Pages dashboards like CAS·DAM, DriftWatch, and PromptMatrix, and Vercel-hosted demos that are fast to ship but weaker as a permanent identity surface when they live only on a vendor subdomain. Claude Cowork live artifacts are useful for internal iteration and sharing, but the sandbox and publishing model make them a poor canonical home for a recruiter-facing artifact. citeturn29view0turn27view0turn25view0turn17view0turn38view0turn38view1turn38view2turn40view6turn40view7

For the first 30 seconds, the public page should not behave like an equal-weight eight-panel dashboard. The cold-open needs **three things above the fold**: a visible fleet-state summary, a clearly annotated **May 1–10 regression timeline** showing that the eval suite caught a silent failure, and a compact economics view that proves Sean can reason about model/cost tradeoffs. The recurring pattern across the strongest reference surfaces is that they lead with **state, trend, and anomaly** before they ask the viewer to read tables or logs. citeturn27view0turn3view0turn17view0turn12view2turn14view1turn40view8

The most important pre-code change is to **promote the regression window from “an annotation layer” to the central hero construct of the entire page**. Right now, the spec reads like a competent dashboard. Sean needs it to read like a memorable operational story: *an eight-agent local-first fleet drifted silently for nine days, the eval layer caught it, the operator recovered it, and the dashboard preserves the incident as proof of operational maturity.* That shift is what moves the artifact from “nice project” to “credible agent-ops signal.” citeturn27view0turn3view0turn25view0turn9view0turn7view3

## Benchmark Evidence

### Reference Dashboard Survey

I scored the survey toward **portfolio relevance first** and **vendor-product benchmarking second**. I excluded a few screenshot-only but useful references from the scored set: Oleksii Nikiforov’s **pi-kanban** and **claude-code-kanban** are excellent design references, but I did not find a public live dashboard URL for either, only public blog posts and repos, so they are better treated as screenshot-first distribution evidence than as fully verified public dashboards. The same caution applies to Kōan: the public site is reachable, and Product Hunt provides concrete feature details, but the live app exposes limited public internals without sign-in or BYOK setup. citeturn7view3turn9view0turn23search0turn23search1turn23search2

**CAS·DAM dashboard** is the closest public reference for the kind of recruiter-safe, static, explainable artifact Sean should ship. Its public dashboard leads with an urgency banner, KPI status blocks, expert commentary, recommendations, and explicit provenance/disclosure. The page is timestamped **April 25, 2026**, which makes freshness verifiable. What it gets right is not just the metrics; it tells the viewer what is wrong, why it matters, what to do next, and where the numbers come from. What it gets wrong for Sean’s use case is that it runs long below the fold and is more analyst-report than “cold-open” artifact. Sean should borrow the **incident framing and provenance honesty**, not the verbosity. citeturn27view0

**Cortex Agent Fleet — Engineering Activity** is the best public example I found of a named-person, named-fleet portfolio surface on a personal domain. Its top entry is for the **week of May 3, 2026**, and it foregrounds shipped PRs, feature counts, infrastructure changes, model-tier changes, observability work, and a visible fleet identity. What it gets right is authorship clarity: you immediately know whose work this is, what fleet it belongs to, and what changed recently. What it gets wrong for Sean’s dashboard is that it is closer to an engineering activity feed than an observability dashboard: there is not enough time-series state, anomaly surfacing, or first-glance health telemetry. Sean should copy the **identity and project-page framing**, not the feed-centric information architecture. citeturn29view0

**DriftWatch LLM Monitoring** is a useful negative-and-positive benchmark. The public GitHub Pages dashboard exposes the right primitives for a monitoring surface — prompts monitored, average drift score, peak drift, active alerts, validator status, drift history, and latest prompt results — and the associated repo shows a verifiable **v1.0.0 release on March 13, 2026**. What it gets right is the classic monitoring pattern: KPI tiles plus a time-history chart plus a latest-run slice. What it gets wrong is that the public page still presents as a generic template and, when opened publicly, shows a “Live Loading...” state and empty placeholders rather than an immediately meaningful narrative. That is almost exactly the failure Sean said he wants to avoid. citeturn3view0turn1search11

**Agent Observability / RLX-ray** is a strong “deep dive” reference but a weaker cold-open reference. The public Vercel app opens to project-level dataset choices and aggregate run counts, and the Devpost entry dates the project to **February 15, 2026** while describing searchable trajectories, sectioned traces, similar-run comparison, and failure-mode clustering. What it gets right is seriousness: it feels like an actual observability product for agent trajectories, not a vanity dashboard. What it gets wrong for Sean’s artifact is that it asks the viewer to navigate before it lands the story. For a recruiter artifact, Sean should not make the first screen a chooser or explorer. He should make it a conclusion. citeturn3view1turn4view0turn30search0

**PromptMatrix** is not pure observability, but it is highly relevant because it is a live public static demo with a professional “AI-ops” feel and a strong above-the-fold structure. The public demo shows dashboard status counters, registry/evaluation/trace/alert navigation, analytics summaries, recent prompt performance, a trace viewer, and alerts. The repo exposes a verifiable **v0.2.1 release on April 11, 2026**. What it gets right is demo legibility: it behaves like a product in one click, with no account and no backend dependence on the public page. What it gets wrong for Sean’s purpose is that the demo is explicitly simulated, which is fine for a product preview but weaker as proof of operational reality. Sean should borrow the **fast first impression and clean “demo-mode honesty”**, while keeping his data real. citeturn25view0turn31view0

**ObservAgent** is an especially relevant local-first comparator. The public landing page and repo make the value proposition explicit: real-time cost tracking, tool latency, subagent visibility, SSE streaming, local-only operation, and no telemetry, with a verifiable **v2.4.4 release on April 24, 2026**. What it gets right is perfect alignment with Sean’s local-first agent-fleet posture; it treats cost, tools, latency, and hierarchy as first-class observability concerns. What it gets wrong for recruiter sharing is that the actual dashboard remains localhost-only. That is excellent for a developer tool, but it means the public artifact must work harder through landing-page copy and screenshots. Sean’s dashboard should invert that tradeoff: public and read-only by default, with no special setup needed for the viewer. citeturn7view2turn32view0

**Vercel AI Gateway Usage / Observability** is the strongest vendor reference for above-the-fold layout. The public page exposes **Spend by Model**, **P50 TTFT by Model**, **Requests by Model**, token summaries, and a request log; the supporting docs were updated **February 26, 2026** and describe usage and request views explicitly. What it gets right is the hierarchy: totals and trends first, log table second. What it gets wrong for Sean’s use case is that the surface is authenticated product UI, not a narrative portfolio artifact, and it is impersonal by design. Sean should take the **panel hierarchy**, not the product tone. citeturn17view0turn40view5

Two vendor references are especially useful as panel-pattern checks even though they are not public-click demos in the same way. **Braintrust Monitor** organizes request counts, latency, token usage, costs, scores, and custom metrics into reusable views, while **LangSmith Observability** centers tracing, monitoring, and cost/latency/quality dashboards with online evals and alerts. Together they reinforce the same pattern seen in Vercel and DriftWatch: first-glance monitoring surfaces lead with counts, distributions, time-series, and alertable deltas — not tables of recent events. citeturn12view2turn12view3turn14view1

### Distribution Surface Verdict

**Verdict: choose the hybrid path — an Astro page on Sean’s personal site, deployed on Vercel, with the static build mirrored to GitHub Pages as backup.** If I collapse that into one canonical answer, the canonical answer is **“personal domain first, Vercel-hosted Astro page”**. The hybrid part is quiet insurance, not the primary public face. citeturn29view0turn27view0turn40view6turn40view7

Why this wins on recruiter discovery is mostly an inference from the public surfaces in the survey rather than a formal recruiter study. The most legible portfolio example is Damilola’s named-domain project page, where authorship and project context are obvious in the URL and page title. By contrast, hackathon-style or standalone product subdomains like `agent-observability.vercel.app` are easy to ship, but they ask the viewer to do extra work to connect the artifact back to the person behind it. GitHub Pages is durable and cheap, but its default URL also feels more repo-centric than portfolio-centric unless it sits behind a custom domain. Put simply: **the dashboard should look like a page in Sean’s body of work, not like an orphan demo.** citeturn29view0turn3view1turn25view0turn40view7

Why this wins on ship-speed is straightforward. Astro’s default mode is static generation; Astro can deploy to Vercel with the same workflow for static sites, and Vercel serves static files directly. For Sean’s build budget of two to three working days and his desire to ship a single-file-ish page with light JS, that is the shortest path to a fast, cacheable public page without inventing new infrastructure. GitHub Pages remains useful as a mirror because it also supports custom domains and free public hosting, but Vercel is the smoother “record a Loom, paste the link, done” path. citeturn39search0turn39search8turn40view6turn39search3turn40view7

**Cowork should not be the canonical public surface.** Anthropic’s docs make clear that live artifacts are persistent HTML dashboards inside Cowork and can be published publicly, which is attractive for iteration. But the platform also has meaningful constraints for this specific use case: live artifacts are desktop-plan features inside Cowork, public publishing/unpublishing has its own lifecycle rules, and the sandbox blocks outbound `fetch`, XHR, video/audio loads, WebSockets, and even localhost requests in at least one documented issue. That is tolerable for internal dashboards and experiments; it is not where Sean should place a cold-share portfolio artifact meant to persist and be indexed. citeturn38view0turn38view1turn38view2

### Data-Loading Pattern Verdict

**Verdict: static build-time snapshot.** Sean should run one local export script that reads the CSV, nightly manifests, spend JSONs, Markdown eval summary, and SQLite job-feed data, computes a public-safe snapshot, and emits the HTML plus a small static payload. No live poll. No recruiter-facing “loading” state. No browser attempt to read local files. citeturn27view0turn29view0turn39search16

This is the strongest match to the best portfolio-grade references. CAS·DAM is fundamentally a rendered report dashboard: the page already has the answer when it loads. Damilola’s Cortex activity page is also pre-rendered and legible immediately. PromptMatrix’s public demo succeeds because it behaves like a finished surface from the first paint, even though the data is simulated. That is the right expectation to set for a recruiter artifact. citeturn27view0turn29view0turn25view0

The best argument against fetch-at-load is DriftWatch. Its public page exposes the right monitoring concepts, but the live public experience still surfaces placeholders and “Live Loading...” instead of a trustworthy first-glance state. That is fine for a true monitoring app. It is bad for Sean’s stated non-negotiable of honest empty states and no spinner-that-never-resolves behavior. A static snapshot also fits Cowork’s sandbox limitations if Sean ever exports a companion artifact there, because the published/dashboard version would not depend on runtime network fetches. citeturn3view0turn38view2

Live-polling only makes sense when the artifact itself is the working console — which is how Vercel AI Gateway, AgentOps, Braintrust, and local tools like ObservAgent work. Sean’s page is different. It is a **public evidence surface**, not the control plane. The right design target is “read a recent, truthful snapshot,” not “monitor the fleet live from your browser.” citeturn17view0turn40view3turn12view3turn32view0

## Shipping Decisions

### Anonymization Pattern

**Verdict: public mode should remove exact dollars and content payloads, and present cost as an indexed/relative economics story.** In practice: keep model/provider mix percentages, trend direction, cloud-vs-local share, run counts, and cost movement; replace exact dollar figures with an indexed line, coarse spend bands, or normalized cost-per-100-runs. Publicly exposing raw prompts, agent outputs, or exact spend is unnecessary for the signal Sean is trying to send. citeturn40view2turn17view0turn14view0

The load-bearing call here is **do not show exact dollars on the public surface**. Public product dashboards that show granular spend — Vercel AI Gateway, LangSmith model pricing/cost tracking, Helicone cost breakdowns — are authenticated internal UIs or developer docs, not recruiter-safe public artifacts. By contrast, the strongest public portfolio-like references use one of three public-safe patterns: they disclose only operational summaries and provenance without raw source content (CAS·DAM), they publish high-level activity and counts rather than sensitive internals (Cortex), or they flag demo/simulated operation explicitly (PromptMatrix). Sean should take the same public-safe stance. citeturn27view0turn29view0turn25view0turn40view2turn14view0turn40view5

I would implement this as a **public-safe snapshot schema** with four privacy rules. First, strip all prompt/completion text and replace it with event type plus redacted labels. Second, convert exact dollars to either an index or a spend band. Third, hash or bucket any job-feed/company-specific values that could reveal active search behavior. Fourth, preserve only the minimal trace metadata needed to show that instrumentation exists: timestamp, agent, model/provider, success/failure, duration, and evaluation outcome. That still lets Sean show cost literacy, fleet management, and regression detection while honoring the “safe to share cold” requirement. citeturn32view0turn40view1turn40view3turn40view10

### The Three Anchor Panels

**Priority one: Fleet Health Tiles with a visible incident ribbon.** This is the fastest way to establish scale and state: how many agents are active, how many are healthy/degraded, whether the nightly synth completed, how many runs were observed in the last window, and whether the system is currently normal or in recovery. CAS·DAM does this with a top-of-page “metrics require immediate attention” construct, and Vercel AI Gateway does it with usage/request summaries before tables. Sean’s equivalent should do the same. citeturn27view0turn17view0

**Priority two: Eval Suite Status as an annotated time-series centered on the May 1–10 regression.** This is the narrative proof panel. DriftWatch’s “Drift History” is proof that time-history belongs close to the top when regressions are the story. Braintrust, LangSmith, and Grafana’s GenAI observability materials all reinforce that production AI monitoring becomes useful when the viewer can see quality and performance change over time, not just read a current score. Sean’s story is not “my eval suite exists.” It is “my eval suite caught a nine-day silent regression and the dashboard makes that legible instantly.” citeturn3view0turn12view2turn14view1turn40view8

**Priority three: Fleet Economics panel combining Cost Trends and Model Mix.** I would not leave these as two separate hero panels. Helicone, LangSmith, Langfuse, Vercel, and Grafana all treat spend, token usage, latency, and model/provider distribution as tightly related views. Sean’s artifact matters partly because it closes his cost-economics gap; hiding economics below the fold would waste one of the artifact’s strongest positioning benefits. The public-safe version can still show an indexed cost line plus a provider/model mix donut or stacked bar. citeturn40view2turn14view0turn40view0turn40view5turn40view8

Recent runs, synthesizer telemetry, and any job-hunt material belong below the fold. Tables and logs matter after the viewer is already convinced. They are not how the viewer gets convinced. RLX-ray is the clearest caution here: extremely serious internals, but too much navigation before the story lands. citeturn3view1turn4view0

### Naming Verdict

**Verdict: use “Agent Fleet Observability” as the proper name, and treat “dashboard” as the descriptor, not the brand.** My recommended H1 would be: **Agent Fleet Observability**. My recommended subtitle would be: *Read-only operations dashboard for a local-first eight-agent fleet*. citeturn14view1turn40view4turn40view0turn40view9

The reason is simple: **“observability” is the category-trigger word**. It is the vocabulary used across LangSmith Observability, Helicone OSS LLM Observability, Langfuse Observability docs, AgentOps’ “agent observability” positioning, and Grafana’s AI/GenAI Observability materials. “Fleet” is also useful because it immediately communicates multi-agent scope instead of a single chatbot or experiment harness. By contrast, “dashboard” is universal but generic; it tells you the format, not the category. citeturn14view1turn40view4turn40view0turn40view9turn40view8

This is one of the few naming claims here that has a real convention behind it rather than a vague vibe. Across multiple concrete examples, the winning pattern is **[domain object] + observability/monitoring/tracing**: *LangSmith Observability*, *Agent observability*, *LLM Observability*, *GenAI Observability*. That is enough evidence to treat “observability” as a true category word rather than a preliminary pattern. citeturn14view1turn40view4turn40view0turn40view8turn40view9

### Eval-Suite Integration Shape

**Verdict: sparkline.** More precisely: a sparkline/history strip with the latest pass count pinned into the panel header and the May 1–10 regression visibly annotated on-chart. If the choice is “pass-count number vs sparkline vs full grid vs all three,” the right answer for the public artifact is sparkline. citeturn3view0turn12view2turn17view0

The reason is that a pass count only answers “where are we now,” but Sean’s load-bearing proof lives in “what changed and when.” DriftWatch’s public surface includes a history chart near the top. Braintrust’s monitoring docs emphasize time-series, top lists, and big numbers as separate chart types, which is another way of saying: use each for the job it does best. A full grid is useful for operator drill-down but is too dense for a recruiter cold-open, and “all three” wastes precious screen real estate on a small artifact with a screenshot requirement. citeturn3view0turn12view2

If Sean wants one concession to current-state legibility, put **“Last nightly run: 47/50 passing”** directly into the sparkline card chrome. That preserves current-state clarity without giving up the time dimension that actually proves operational competence. This is an inference from the survey’s repeated preference for state-plus-trend combinations. citeturn27view0turn17view0turn40view8

## Above the Fold Design

### Substack Hero Format and Mobile Variant

**Verdict: use a single screenshot hero in the Substack post, and yes, build a dedicated screenshot/mobile variant.** The live page should remain canonical, but the distribution unit for Substack, DMs, and recruiter messages should be a **posterized view** that shows only the three anchor panels and the incident annotation. citeturn27view0turn25view0turn7view3turn9view0

This recommendation is based less on abstract mobile best practice and more on how comparable tools are actually being distributed in public. The strongest local-first and agent-workspace references in this study — pi-kanban and claude-code-kanban — are being introduced through screenshot-rich blog posts because their most meaningful interaction happens locally. PromptMatrix also succeeds in part because its public page reads like a finished screenshot the moment it loads. In other words, in this scene, **the screenshot is often the acquisition surface and the live dashboard is the confirmation surface**. citeturn7view3turn9view0turn25view0

So Sean should explicitly ship two render modes from the same data snapshot. The canonical page keeps interactivity. The **poster/mobile mode** should be 375px-safe, collapse all tables, enlarge labels, and preserve only: fleet health, eval timeline with the regression window, and economics. This is a design recommendation driven by Sean’s stated iPhone-screenshot constraint and by the screenshot-first distribution pattern in the reference set; I did not directly 375px-test every authenticated vendor dashboard. citeturn7view3turn9view0turn38view1

### Two-Purpose Surface

**Verdict: the public surface should not have a Job Hunt Overlay tab.** It should stay single-purpose: fleet observability. If Sean wants to tie it to the job search, do it in surrounding copy, an adjacent case-study page, or a private recruiter-only screenshot variant — not in the public tab structure. citeturn27view0turn25view0turn17view0

Why I’m confident here: the strongest public examples in the set are painfully single-purpose. CAS·DAM is about governed operational intelligence. Vercel AI Gateway is about AI usage/request observability. PromptMatrix is about prompt governance. Even Damilola’s page, which does include job-search-adjacent work in its activity log, still titles the page as **Cortex Agent Fleet — Engineering Activity** rather than reframing the surface around the job search. Single-purpose surfaces create a fast category match. Multi-purpose public tabs create doubt about what the viewer is supposed to notice. citeturn27view0turn29view0turn25view0turn17view0

There is also a trust issue. A recruiter who sees a “Job Hunt Overlay” tab on a public dashboard may read the whole artifact as self-promotional packaging rather than as an operational artifact that happened to be published by a job-seeker. Sean wants exactly the opposite read. He wants “this person thinks in agent-ops primitives” first, and “this person is available” second. citeturn29view0turn14view1turn40view4

### The Outsized-Impact Recommendation

**Replace the optional Job Hunt Overlay slot with a full-width Incident Timeline hero anchored on the May 1–10 silent regression and recovery.** That is the one pre-code change most likely to improve recruiter resonance. citeturn27view0turn3view0turn25view0turn7view3turn9view0

Here is why this matters so much. In the current spec, the regression is an annotation layer inside a broader panel collection. In the strongest references, the thing the operator wants you to understand is not hidden inside the chrome. CAS·DAM puts the operational problem at the top of the page. DriftWatch’s history chart exists because drift is the story. Screenshot-first tools like pi-kanban and claude-code-kanban rely on one visually obvious organizing idea per image. Sean’s dashboard needs that same clarity. The regression window is not supporting evidence. It is the story. citeturn27view0turn3view0turn7view3turn9view0

Concretely, I would change the above-the-fold wireframe to this: **top ribbon** with fleet state and incident status; **left hero** with the eval sparkline and the May 1–10 annotation; **right hero** with economics/model mix. Everything else becomes second-row detail. That one move would also make the Substack hero and mobile poster almost automatic, because the story would already be legible as a single image. That conclusion ties directly back to the reference survey, the anchor-panel ranking, and the screenshot-first distribution findings above. citeturn27view0turn17view0turn40view2turn40view8

## Distribution Assets

## Sources Index

### Reference dashboard survey sources

CAS·DAM dashboard — public dashboard page with KPI tiles, commentary, recommendations, provenance, and page timestamp. Accessed 2026-05-15. citeturn27view0

Cortex Agent Fleet — Engineering Activity — personal-domain public fleet activity page with week-of-May-3, 2026 top entry. Accessed 2026-05-15. citeturn29view0

Agent Observability public app — public Vercel surface showing project chooser and benchmark counts. Accessed 2026-05-15. citeturn3view1

RLX-ray Devpost entry — public project page with creation date, architecture, and dashboard description. Accessed 2026-05-15. citeturn4view0

MittelmanDaniel/agent-observability GitHub repo — public repo used to verify project existence and code surface. Accessed 2026-05-15. citeturn30search0

DriftWatch public dashboard — public GitHub Pages LLM monitoring dashboard. Accessed 2026-05-15. citeturn3view0

GenesisClawbot/llm-drift repo search result — public repo snippet showing verifiable release context. Accessed 2026-05-15. citeturn1search11

PromptMatrix live demo — public GitHub Pages live product/demo surface. Accessed 2026-05-15. citeturn25view0

PromptMatrix GitHub repo — public repo showing release v0.2.1 dated April 11, 2026. Accessed 2026-05-15. citeturn31view0

ObservAgent public landing page — public local-first observability landing page. Accessed 2026-05-15. citeturn7view2

darshannere/observagent GitHub repo — public repo with feature list and release v2.4.4 dated April 24, 2026. Accessed 2026-05-15. citeturn32view0

Vercel AI Gateway public usage page — public dashboard page with spend, TTFT, request, and token sections. Accessed 2026-05-15. citeturn17view0

### Vendor observability and standard references

LangSmith Observability product page — tracing, monitoring, alerts, and dashboard metrics. Accessed 2026-05-15. citeturn14view1

LangSmith cost-tracking docs — model pricing map, token-cost computation, and tool-cost support. Accessed 2026-05-15. citeturn14view0

Braintrust dashboard docs — monitor page, chart types, views, and saved dashboard structure. Accessed 2026-05-15. citeturn12view2

Braintrust observe docs — logs, topics, dashboards, and production/eval feedback loop. Accessed 2026-05-15. citeturn12view3

Langfuse example project docs — public shared example project, traces, sessions, prompts, scores, and datasets. Accessed 2026-05-15. citeturn12view0

Langfuse observability overview — sessions, costs, tracing, evaluations, and custom dashboards. Accessed 2026-05-15. citeturn40view0

Helicone sessions docs — unified view of multi-step agent flows. Accessed 2026-05-15. citeturn40view1

Helicone cost tracking docs — session-level cost breakdown and unit economics framing. Accessed 2026-05-15. citeturn40view2

AgentOps traces docs — trace list, detail, timeline, tree view, analytics. Accessed 2026-05-15. citeturn40view3

AgentOps product page — explicit “agent observability” positioning. Accessed 2026-05-15. citeturn40view4

Vercel AI Gateway observability docs — official usage/request views, model usage, and cost monitoring. Accessed 2026-05-15. citeturn40view5

Grafana GenAI Observability docs — request, cost, token, performance, and error dashboards. Accessed 2026-05-15. citeturn40view8

Grafana AI Observability overview — OpenTelemetry-native AI observability positioning. Accessed 2026-05-15. citeturn40view9

OpenTelemetry GenAI semantic conventions — generative AI signals and stability notes. Accessed 2026-05-15. citeturn40view10

OpenTelemetry GenAI agent spans — emerging agent/framework span conventions. Accessed 2026-05-15. citeturn40view11

### Distribution and publishing references

Astro routing/static output docs — default static generation behavior. Accessed 2026-05-15. citeturn39search0

Astro deploy-to-Vercel docs — static/on-demand deployment workflow. Accessed 2026-05-15. citeturn40view6

Astro endpoints docs — static endpoints generated at build time. Accessed 2026-05-15. citeturn39search16

Vercel build-output/static files docs — static files served from build output on the edge. Accessed 2026-05-15. citeturn39search3

Vercel limits docs — static file hosting not counted as a build in the same way as framework builds. Accessed 2026-05-15. citeturn39search18

GitHub Pages custom domain docs — Pages availability and custom domain support. Accessed 2026-05-15. citeturn40view7turn39search10turn39search21

Claude Cowork live artifacts docs — persistent HTML dashboards, refresh behavior, version history. Accessed 2026-05-15. citeturn38view0

Claude artifact publishing docs — public link creation, embed support, organization-only sharing constraints, and unpublish behavior. Accessed 2026-05-15. citeturn38view1

Claude Code issue on Cowork artifact sandboxing — blocked network access from artifact sandbox. Accessed 2026-05-15. citeturn38view2

### Screenshot-first and distribution-pattern references

pi-kanban post — screenshot-rich public write-up of a read-only observability dashboard for the pi coding agent. Accessed 2026-05-15. citeturn7view3

claude-code-kanban post — screenshot-rich public write-up of a real-time Kanban dashboard for Claude Code teams. Accessed 2026-05-15. citeturn9view0

Kōan Product Hunt listing — public evidence of agent-observability positioning and live event-stream framing; treated as partially verifiable because public internals of the live app are limited without running it. Accessed 2026-05-15. citeturn23search0turn23search1turn23search2