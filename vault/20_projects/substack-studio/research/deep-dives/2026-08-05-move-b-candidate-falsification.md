---
title: "Move B — Named-Candidate Falsification Pass"
type: research-verification
status: complete
domain: [substack-studio]
tags: [pencil-and-prompt, refocus-2026-08, verification, prior-art, tested-library, falsification, competitive-check, executive-circle]
created: 2026-08-05
last-updated: 2026-08-05
cost_usd: 0.00
method: "Direct fetch of each candidate's primary artifact (not blog coverage of it), plus an Executive Circle MCP pass over the same question. Every verdict carries a resolvable URL, including every NO. No paid calls."
verdict: "Claim HOLDS as restated, but the nearest neighbour moved much closer. Nate Jones publishes genuine tested verdicts with honest failures in Sean's exact lane — per POST, not per ENTRY. The differentiator is now the library property, not the testing posture."
related: [2026-08-05-move-a-verification-two-named-examples, 2026-08-05-citation-tier-audit, 2026-08-05-prior-art-synthesis]
ai-context: "Clears the COVERAGE exposure Move A left open. Twelve candidates checked directly; eleven are clean NOs with URLs. The consequential finding is the twelfth: the Executive Circle pass surfaced a Nate Jones post (2026-07-15) that runs a real controlled experiment, publishes a metric, and reports that his OWN preferred artifact lost on delivery 2 runs out of 3. That is a tested verdict with an honest failure, published, in the incumbent's voice, in Sean's lane. It does NOT falsify the Move A claim (it is not a library and carries no per-entry verdicts) but it materially narrows the white space and forces the positioning to lean on CUMULATION rather than on testing posture. The reconvene must decide on this."
---

# Move B — Named-Candidate Falsification Pass

[Move A](2026-08-05-move-a-verification-two-named-examples.md) cleared the two entities the DR report named. It did not clear the field, because that report's search was 65% vendor marketing and may have missed real candidates. This is the coverage check. Cost: $0.

**The question, asked as falsification:** does the candidate publish **per-entry** tested verdicts — evaluation results, a beat/tied/lost or pass/fail judgement, or documented failure cases — attached to individual library entries?

## Verdict table

| Candidate | Per-entry tested verdicts? | Evidence URL | Quoted evidence |
|---|---|---|---|
| **DAIR.AI Prompt Engineering Guide** | **N** | [github.com/dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | Self-described as "Guides, papers, lessons, notebooks and resources for prompt engineering." Entries explain techniques and link to external papers. No maintainer-run evaluation attached to any technique. |
| **promptingguide.ai** | **N** | [promptingguide.ai/techniques/cot](https://www.promptingguide.ai/techniques/cot) | The CoT page carries only (a) illustrations drawn from Wei et al. 2022, Kojima et al. 2022, Zhang et al. 2022, and (b) two toy demonstrations (odd-number addition, apple-counting). No comparative metrics, no pass/fail verdict, no failure cases from the site's own testing. It synthesizes others' research; it does not run its own. |
| **LangSmith Hub (LangChain)** | **N** | [docs.langchain.com/langsmith/manage-prompts](https://docs.langchain.com/langsmith/manage-prompts) | Hub prompts are explicitly **"user-generated and unverified"** with no LangChain review or endorsement. Searchable metadata is "name, handle, use cases, descriptions, or models." Evaluation is a separate LangSmith capability, not part of the hub entry. |
| **PromptHub** | **N** | [prompthub.us](https://www.prompthub.us/) | Public entries show title, creator, team, star count, fork count. Evaluation is an in-product feature over *your own* cases: "Run evals in a simple UI across your test cases." No eval data on public entries. |
| **PromptLayer** | **N** | [promptlayer.com](https://promptlayer.com/) | Evaluation is private and in-product: "dataset-backed tests, human review, and automated graders before prompt or workflow changes reach production." No public prompt library carrying results. |
| **Braintrust** (public artifacts) | **N** | [braintrust.dev/blog](https://www.braintrust.dev/blog) | Public output is methodology writing ("Five hard-learned lessons about AI evals"), an eval-foundations encyclopedia, OSS tools, and docs/cookbook. Evals themselves are a private in-product capability. No public catalog with per-entry verdicts. |
| **DSPy** (`stanfordnlp/dspy`) | **N** | [github.com/stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | README offers "algorithms for optimizing their prompts and weights." Optimizer output is produced per-program at *your* runtime against *your* metric. There is no published catalog of optimized signatures with attached eval scores. |
| **OpenAI Cookbook** | **N** | [developers.openai.com/cookbook](https://developers.openai.com/cookbook) | Entries carry title and description. Each recipe is a standalone guide, not a scored artifact. No per-recipe metrics, verdicts, or documented failure cases. |
| **Anthropic prompt library** | **N** *(see limitation)* | [platform.claude.com/docs/en/resources/prompt-library/library](https://platform.claude.com/docs/en/resources/prompt-library/library) | Entries carry System Prompt / User Prompt / Example Output (+ optional API code). No metrics, no verdicts, no failure cases. **Limitation:** the canonical library URL now 301-redirects to `claude-prompting-best-practices`, so the live index could not be rendered directly; this verdict rests on entry structure rather than a fresh page render. Weakest "no" in the table. |
| **awesome-chatgpt-prompts** | **N** | [github.com/f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) | "A curated collection of prompts for AI chat models." Distribution is prompts.csv / PROMPTS.md / HF dataset. Zero evaluation metadata of any kind. |
| **HF `HuggingFaceFW/finephrase`** (report cite 39, the nearest hit) | **PARTIAL, and weaker than expected** | [huggingface.co/datasets/HuggingFaceFW/finephrase](https://huggingface.co/datasets/HuggingFaceFW/finephrase) | Does document limitations honestly: outputs "may contain errors and hallucinations"; long inputs truncated; "Per-config document totals are slightly below source count due to skipped invalid requests." But evaluation is **dataset-level only**. Per-entry fields are `id`, `text`, `rollout_results`, `language_score` with **no quality verdict**, no ablation table, no failure-case documentation per sample. |
| **Nate Jones / Executive Circle** *(not on the original list — surfaced by the MCP pass)* | **PARTIAL — the real finding.** Genuine tested verdicts with honest failures, but **per post, not per entry** | [natesnewsletter.substack.com/p/ai-harness-audit](https://natesnewsletter.substack.com/p/ai-harness-audit) (2026-07-15) | See below. |

## The finding that matters: Nate Jones already does the hard part

The Executive Circle MCP pass (refocus-ticket item 2, per-mechanism competitive checks, discharged here) surfaced a candidate no vendor-marketing search would have returned, because it is not a product.

**"I gave Fable 5 five thousand extra words of instructions. It thought better and failed delivery two runs out of three."** (2026-07-15) publishes an actual controlled experiment:

> "I ran each version three times in fresh Fable 5 chats."
>
> "The full method produced richer analysis. Two blind scorers gave it an average content score of 19.67 out of 20. The compact brief averaged 17.5."
>
> "The requested output had to be valid JSON and stay under 1,400 words. The compact brief passed three times out of three. The full method passed once. One answer was invalid JSON, and another exceeded the word limit."

That is: a named comparison (742-word brief vs 5,197-word method), a stated n (3 runs each), blinded scoring, a binary delivery metric, and a result in which **his own richer artifact lost**. He then declines to over-claim from it:

> "That establishes discovery pressure. It doesn't establish that Codex routed the task incorrectly."
>
> "They don't prove that the cleaner saw the entire vendor-side harness, that a proposed change improved productivity, or that one model is better suited to a category of work."

He even ships an evidence-labelling vocabulary — `VERIFIED` / `USER_REPORTED` / `INFERRED` / `INACCESSIBLE` / `NOT_APPLICABLE`, plus `NOT_EXPOSED` for missing runtime traces.

**This is the honest-failure posture the masthead promises, already being practiced, by the incumbent the project CLAUDE.md already names as the competitor to differentiate from.**

### Why it does not falsify the claim

Three reasons, and they are the whole remaining moat:

1. **It is a post, not a library.** One experiment, one artifact, published once. There is no catalog in which each entry carries its own verdict.
2. **The verdict attaches to a configuration, not to a reusable technique entry.** "Compact brief beat full method on this audit task" is a finding about two documents, not a beat/tied/lost row against a named mechanism that a reader can look up later.
3. **Nothing accumulates or gets retracted.** There is no version, no re-test cadence, no correction path when a later model flips the result. A post is an archive entry; a library entry is a live claim.

Contrast with the counter-case from the same author: **"I Tested OpenAI's 200 Prompt Templates — They're Useless"** ([2025-10-01](https://natesnewsletter.substack.com/p/i-tested-openais-200-prompt-templatestheyre)) has "I Tested" in the title and publishes **zero** evaluation results. The verdict on OpenAI's pack is qualitative ("It is bad. It is basically a bunch of 2 sentence questions"), and the 12 replacement prompts carry a claimed benefit ("save 2-10 hours per week") with no measurement shown anywhere in the piece. Same author, same lane, ten months earlier: the rigor is real but **inconsistent and uncommitted**, because nothing in the format requires it.

That inconsistency is precisely what a library with a published measurement protocol fixes, and it is the sharpest available argument for the product.

## Verdict: the claim HOLDS, restated once more

Eleven of twelve candidates are clean NOs with URLs. The twelfth is a partial that lives one level away.

> ❌ "We publish tested verdicts with honest failures." *(No longer differentiating. Nate Jones did exactly this on 2026-07-15, well, in this lane.)*
>
> ❌ "Nobody publishes tested verdicts with honest failures." *(Falsified outright by the same post.)*
>
> ✅ **"No prompt or technique library publishes per-entry tested verdicts with honest failures. The rigor exists in three places and none of them cumulate: enterprise eval tooling has it but keeps it private (Braintrust, PromptLayer, LangSmith); algorithmic financial research has the retraction discipline but not the artifact type (Aksoy Capital); and the best practitioner writing has real experiments but ships them as posts, one at a time, with nothing to look up afterward (Nate Jones). Public libraries — Anthropic's, DAIR.AI's, promptingguide.ai's, LangSmith Hub's, awesome-* — carry no evidence standard at all. LangSmith states it plainly: its hub prompts are 'user-generated and unverified.'"**

### What this changes for the reconvene

The white space is **cumulation, not testing**. That is a real narrowing and the reconvene should feel it:

- **The pitch can no longer be "I test things and admit failures."** The nearest competitor does that, and does it with blind scorers. Claiming it as the differentiator invites an immediate and fair "Nate already does this."
- **The differentiator is the library property**: per-entry, versioned, re-tested, retractable, against a *published* measurement protocol, so a reader can look up a mechanism months later and see whether it still holds. Nobody is doing that.
- **This strengthens Finding 8's build-order inversion.** The measurement protocol is not just a credibility prerequisite; it is now the *entire* differentiation. A library of verdicts without a published protocol is just Nate's posts with worse distribution.
- **Move A's nearest-neighbour list needs a third name.** Aksoy for retraction discipline, private eval tooling for evaluation rigor, and now **Nate Jones for published experimental honesty**. Naming him is the honest posture and it is also the stronger rhetorical move: it lets the piece say *this is the standard, here is what happens when you make it cumulative*, rather than pretending the standard doesn't exist.

## Method limitations, stated

- **The Anthropic verdict is the weakest cell** in the table (canonical URL redirects; verdict rests on entry structure, not a fresh render). If the claim is published, re-check it.
- **Executive Circle covers Nate Jones's archive only.** Other practitioner newsletters running comparable experiments would not surface here. This pass reduces coverage risk substantially; it does not eliminate it.
- **Absence of a public eval catalog is not proof one doesn't exist** behind a login (Braintrust, PromptLayer). The claim is scoped to *public* artifacts, which is the right scope, but state it that way.
