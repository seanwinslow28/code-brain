# Kickoff E — Verification pass: falsify the white-space claim, resolve the publishable figures

**Paste this into a fresh Claude Code session in `~/Code-Brain/code-brain`. Cost: $0 — no paid research calls. If any step tempts you toward Gemini DR, re-read §"Why not just re-run DR" below and don't.**

---

## Context (read these three first, in order)

1. [`vault/20_projects/substack-studio/research/2026-08-05-prior-art-synthesis.md`](../research/2026-08-05-prior-art-synthesis.md) — 8 findings + implied build order from the Kickoff D research round.
2. [`.../research/deep-dives/2026-08-05-citation-tier-audit.md`](../research/deep-dives/2026-08-05-citation-tier-audit.md) — why Topic 1 is untrustworthy (23% defensible sourcing, nine citations from one vendor's SEO blog, both load-bearing examples self-sourced) and Topic 2 is trustworthy (90% defensible: NeurIPS, ACL, EACL, AAAI, PNAS, TACL, INFORMS, Cambridge *AI EDAM*, ~15 arXiv).
3. [`.../research/deep-dives/2026-08-05-move-a-verification-two-named-examples.md`](../research/deep-dives/2026-08-05-move-a-verification-two-named-examples.md) — Move A, already done. Techpresso falsified; Aksoy Capital's policy real but unexercised and out-of-domain.

Kickoff D is closed. Move A is done. **This session is Moves B and C.**

## Move B — Named-candidate falsification pass

Move A cleared the two entities the DR report named. It did **not** clear the field, because that report's search was 65% vendor marketing and may have missed real candidates. Coverage is the remaining exposure on the whole product bet.

**The question, asked as falsification rather than survey:** for each named candidate below, does it publish **per-entry** tested verdicts — evaluation results, a beat/tied/lost or pass/fail judgement, or documented failure cases — attached to individual library entries?

Candidates (add any others you hit):

- Anthropic's prompt library / prompt engineering docs
- DAIR.AI Prompt Engineering Guide (`github.com/dair-ai/prompt-engineering-guide`)
- promptingguide.ai
- LangSmith Hub (LangChain)
- PromptHub
- PromptLayer
- Braintrust (public-facing artifacts, not the private product)
- DSPy (`stanfordnlp/dspy`) — optimizer reports count if published per-signature
- OpenAI Cookbook
- `awesome-prompts` / `awesome-chatgpt-prompts` class repos
- Hugging Face prompt/dataset cards carrying eval results (report cite 39, `HuggingFaceFW/finephrase`, is the nearest hit and worth a real look)

**Method:** direct fetch of the primary artifact, not blog coverage of it. Also run the **Executive Circle MCP** over the same question — this satisfies refocus-ticket item 2 (per-mechanism competitive checks) at the same time, so do not run that separately later.

**Output:** a verdict table at `.../research/deep-dives/2026-08-05-move-b-candidate-falsification.md` — candidate · does it publish per-entry verdicts (Y/N/partial) · exact evidence URL · quoted evidence. **A "no" needs a URL too.** Then one of:

- **Claim holds** → state the final publishable sentence, with the nearest neighbours named (Aksoy for retraction discipline, private eval tooling for evaluation rigor).
- **Claim falsified** → name the competitor plainly and flag that the product bet needs rework before the doc re-anchor ticket runs. This outcome is a *success*, not a failure; finding it now is much cheaper than finding it after launch.

## Move C — Resolve Topic 2's publishable figures

These six are the numbers likely to appear in posts. Each needs its primary source resolved and the figure confirmed **as stated in the paper**, not as paraphrased by the DR report.

| Figure | Claim | Where the DR report sourced it |
|---|---|---|
| 91% vs 82% | Heterogeneous vs homogeneous multi-agent debate accuracy (GSM-8K) | cites 13, 14 |
| +18.5% / +11.4% | Morphological analysis: pairwise embedding distance / solution-space coverage (iDesignGPT) | cites 15, 16 |
| *d* ≈ 1.03 | Exploration effect size, 48-participant study | cite 15 |
| *d* = 0.70 / 0.27 / 0.12 | Homogenization by task type (meta-analysis, 19 studies, 61 effect sizes) | cite 6 |
| ***d* = 0.414** | **Persistence after session end — the masthead-critical one** | cite 6 |
| D = 16.50 vs 13.60 | xRAG NoveltyBench diversity | cite 12 |

Run [`agents-sdk/scripts/audit_dr_citations.py`](../../../../agents-sdk/scripts/audit_dr_citations.py) against the Topic 2 report to get the resolved URLs, then read the actual papers. Confirm each named framework exists as described: iDesignGPT, IDEAFix, Genie, SELF-PARAM, xRAG, CreativityPrism, NoveltyBench, INFINITY-CHAT.

**Prioritise *d* = 0.414.** Finding 7 proposes re-cutting the masthead from "sameness" to "stickiness" on the strength of that single number. If it does not hold up, the masthead recommendation collapses and the reconvene needs to know before it decides.

**Output:** append a "Figures resolved" section to the Topic 2 pointer note, marking each ✅ confirmed / ⚠️ differs-from-report / ❌ unfindable, each with the primary URL.

## Why not just re-run DR

Two reasons, both learned the hard way on 2026-08-05:

1. **Query shape drives source tier.** A research-shaped question pulled 88% academic sources; a market-shaped question ("what exists in this category") pulled 65% vendor marketing — same model, same tier, same day, same recency instruction. "What exists in category X" is the exact query SEO listicles are built to capture. Move B is market-shaped, so DR will fail it the same way again.
2. **DR cannot prove a negative.** Asked whether anything exists, it will always find something to say yes with — it did, twice, and both collapsed on inspection. Falsifying a named list is the right instrument.

Note also that **"add 2026 to the prompt" would not have helped**: the original prompt already specified post-2025 weighting, and the bad sources were aggressively current 2026 marketing. Recency filters cannot catch fresh marketing.

## Guardrails

- Public repo, no personal data (code-brain CLAUDE.md Rule 9).
- **Every claim needs a resolvable primary URL.** This publication's product is tested verdicts with honest failures; it cannot ship unverified numbers in the post announcing it.
- Evidence only. The reconvene partner session (sidecar `~/.creative-harness/partner-sessions/2026-08-04-pencil-and-prompt-refocus.md`) makes the calls.
- Update the refocus ticket in `vault/00_inbox/tickets.md` when done.

**Done =** Move B verdict table written with a URL behind every yes *and* every no; Move C figures marked confirmed/differs/unfindable with primary sources; synthesis updated; ticket updated. Then the doc re-anchor ticket is genuinely unblocked.
