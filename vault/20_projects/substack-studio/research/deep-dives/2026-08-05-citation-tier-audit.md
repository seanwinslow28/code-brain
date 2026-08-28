---
title: "Citation Tier Audit — Kickoff D Topics 1 & 2"
type: research-audit
status: complete
domain: [substack-studio]
tags: [pencil-and-prompt, refocus-2026-08, verification, citations, evidence-quality, gemini-deep-research, methodology]
created: 2026-08-05
last-updated: 2026-08-05
cost_usd: 0.00
method: "Resolved all 108 Google grounding-redirect URLs to their destinations and classified by evidence tier. Script: scratchpad/cite_audit.py (read-only, no vault writes). Tier counts below are HAND-CORRECTED from the script output, which under-counted academic sources."
related: [2026-08-05-tested-mechanism-library-prior-art, 2026-08-05-divergence-mechanisms-evidence-map, 2026-08-05-prior-art-synthesis]
ai-context: "This audit is the reason Topic 1 should not be trusted and Topic 2 should. It also proves a reusable fact about the whole gemini_dr path: the opaque vertexaisearch grounding-redirect URLs DO resolve to real sources, so DR output is cheaply auditable and every future run should be tier-audited before its numbers are used. The headline finding is that Topic 1's two load-bearing examples are sourced entirely to the subject companies' own marketing pages."
---

# Citation Tier Audit — Kickoff D

**Cost: $0.** All 108 citations across both DR reports were resolved from their Google `vertexaisearch/grounding-api-redirect/` URLs to real destinations and classified by evidence tier.

## Finding 0 — the grounding redirects resolve

This was the open question blocking all verification. They resolve cleanly: 108/108 returned a destination URL, ~85% with HTTP 200 and the rest 403/429 (paywall or bot-block) while still revealing the final URL.

**Consequence beyond this round:** every `gemini_dr.py` report is cheaply auditable. Citation-tier auditing should become a standing step before any DR figure is quoted, not a one-off. See the [prior-art synthesis](../2026-08-05-prior-art-synthesis.md) verification-debt section.

## The split

| Tier | Topic 1 (library prior art) | Topic 2 (divergence evidence) |
|---|---|---|
| **A** — peer-reviewed / preprint / academic venue | 4 (7%) | **42 (88%)** |
| **B** — primary vendor docs, product, source code | 10 (17%) | 1 (2%) |
| **C** — vendor marketing blogs, SEO listicles | **39 (65%)** | 3 (6%) |
| **D** — Reddit, Medium, Substack, YouTube, dev.to | 7 (11%) | 2 (4%) |
| **Defensible (A+B)** | **14 / 60 = 23%** | **43 / 48 = 90%** |

Topic 2's Tier-A sources include NeurIPS 2025 posters (×2), ACL 2026, EACL 2026, AAAI, PNAS, MIT Press/TACL, INFORMS, four *Cambridge AI EDAM / Design Science* journal articles, and ~15 arXiv preprints. That is a genuine literature review.

Topic 1's are four arXiv/ResearchGate hits and a handful of GitHub repos and product docs, against 39 marketing pages.

## Why Topic 1 failed — the two specific defects

### Defect 1: one vendor supplied 15% of the entire evidence base

**Nine of Topic 1's 60 citations are `futureagi.com/blog/*`** — SEO content marketing written by Future AGI about its own product category:

> `top-prompt-management-platforms-2025` · `best-prompt-governance-platforms-for-enterprise-ai-in-2026` · `best-ai-prompt-management-tools-2026` · `best-prompt-management-tools-with-built-in-evaluation-in-2026` · `top-10-prompt-optimization-tools-2025` · `ab-testing-llm-prompts-best-practices-2026` · `evaluating-agent-memory-systems-2026` · `agentic-ai-evaluation-2025` · `open-source-vs-closed-source-evaluations-2025`

Future AGI is also the **first row of the landscape matrix**. The report ranked a vendor first using that vendor's own comparison content. Add four `springboards.ai/blog*` pages behind the "10–30× more creative diversity" claim and the pattern is systemic: the matrix is substantially a synthesis of category-defining marketing.

### Defect 2: both load-bearing examples are self-reported

The report's direct answer — *yes, someone publishes tested verdicts with honest failures* — rests on exactly two entities, and **neither has a single independent source**:

| Claim | Sources | What they actually are |
|---|---|---|
| Techpresso publishes "honest failures alongside" successes | cites 16, 17, 18 | Three `academy.techpresso.co/prompts/*` pages — the product itself |
| Aksoy Capital runs a 1-hour retraction SLA | cites 30, 31 | `aksoycapital.com/docs/ai-policy` and `/about/methodology` — the company's own policy pages |

A company's marketing page saying it publishes honest failures is a claim, not evidence that it does. **There is no third-party verification anywhere in Topic 1 for the finding the whole product bet leans on.**

## What this changes

**Topic 2: keep, verify individual figures only.** 90% defensible sourcing, real venues, and the report openly surfaces conflicting evidence rather than smoothing it. The structure and classifications stand. Individual numbers still need their primary source resolved before publication, but that is now a lookup against a named paper, not archaeology.

**Topic 1: do not cite, do not re-run as written.** 23% defensible, with the load-bearing answer self-sourced. But the failure is diagnostic, not random — the question was **market-shaped**, so the retrieval returned market-shaped content. "What exists in this category?" is the exact query shape that SEO listicles are manufactured to capture, and Deep Research swallowed them.

Note this also means the earlier "stale information" hypothesis was wrong twice over. The prompt already specified post-2025 weighting, and the sources returned were not old — `futureagi.com/blog/best-ai-prompt-management-tools-2026` is aggressively current. It is fresh marketing, which is worse than stale research, because recency filters cannot catch it.

## Recommended replacement for Topic 1

Not a re-run of the same question. Two cheaper, better-shaped moves:

1. **Targeted verification of the two named examples** — do Techpresso and Aksoy Capital actually do what they claim? Web + direct inspection. Free. Settles whether the positioning claim is "nobody does this" or "two adjacent players do."
2. **A named-candidate falsification pass** instead of a landscape survey — hand a specific list (Anthropic's prompt library, DAIR.AI, promptingguide.ai, LangSmith Hub, PromptHub, Braintrust, DSPy, OpenAI Cookbook, Awesome-* repos) and ask which, if any, publishes per-entry tested verdicts. Deep Research is structurally poor at proving a negative — it will always find *something* to answer "yes" with — but it is good at checking specific things.

This merges with refocus-ticket item 2 (per-mechanism competitive checks via Executive Circle MCP + web) rather than adding new scope.

## Standing lesson

Query shape determines source tier. A research-shaped question ("what does the literature measure") pulled 88% academic sources; a market-shaped question ("what exists in this category") pulled 65% vendor marketing. Both ran on the same model, same tier, same day, same recency instruction.

**For a publication whose product is tested verdicts: tier-audit before you cite. It costs $0 and it caught a finding that would have been embarrassing to publish.**
