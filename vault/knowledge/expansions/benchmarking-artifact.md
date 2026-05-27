---
title: "How to make `Benchmarking Artifact` better"
type: expansion
parent: "[[benchmarking-artifact]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-27
updated: 2026-05-27
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[benchmarking-artifact]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Benchmark Validity Threats” mode**
   - **What to add:** A validity-threat taxonomy: construct validity, internal validity, external validity, statistical conclusion validity. Your current concept names the artifact but does not classify *which kind of invalidity* is happening.
   - **Anchor:** Shadish, Cook, and Campbell, *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*.
   - **Unlock:** A reusable **benchmark postmortem template**: “This score is invalid because the harness violates construct validity, not because the model failed.” That lets you write sharper fleet decision records where the conclusion is not “devstral underperformed,” but “the test measured JSON-template compliance instead of agentic tool competence.”

2. **Add “Evaluation Harness as Interface Contract”**
   - **What to add:** Treat every benchmark prompt format as an API/interface contract, not a neutral measurement environment. The missing facet is compatibility testing between model-native affordances and evaluator expectations.
   - **Anchor:** Barbara Liskov and Jeannette Wing, “A Behavioral Notion of Subtyping” (1994).
   - **Unlock:** An **eval adapter spec** for Tier C model selection: one canonical task, multiple model-native harnesses, then compare normalized task outcomes. This would let Sean ship something stronger than a concept note: a runnable `benchmark_contract.md` + adapter interface where “Mistral-style tool calls,” “OpenAI function calls,” and “plain JSON schema” are explicit subtypes with behavioral guarantees.

3. **Add “Goodhart / Proxy Collapse” as the contradicting frame**
   - **What to add:** The concept currently says “the benchmark may be wrong.” Add the stronger frame: once benchmark scores guide deployment, models and humans optimize to the proxy, and the proxy stops representing capability.
   - **Anchor:** Charles Goodhart, “Problems of Monetary Management: The U.K. Experience” (1975); for the modern technical bridge, David Manheim and Scott Garrabrant, “Categorizing Variants of Goodhart’s Law” (2019).
   - **Unlock:** A **fleet selection policy** that separates screening metrics from promotion criteria. Example artifact: “Tier C Promotion Runbook: benchmark score is only a trigger for native-harness eval, live task replay, and failure-mode review.” This prevents the current concept from staying at “beware bad benchmarks” and turns it into an operating rule for model promotion.

## From Anti-Gravity (Gemini 3)

### 1. Grammar-Constrained Decoding (Eliminating the Artifact)
**What to add:** Grammar-Constrained Decoding (EBNF/GBNF). Your concept treats formatting failure as an unavoidable evaluation flaw ("evaluating models poorly due to format mismatch"). You can mathematically force the model's logits to only sample valid schema tokens, entirely decoupling its underlying reasoning ability from its syntax alignment.
**Who/What exemplifies it:** Rémi Louf & Brandon Willard's *Outlines* library (specifically the paper *"Efficient Guided Generation for Large Language Models"*), and Georgi Gerganov's `gbnf` grammar constraints in *llama.cpp*.
**What this unlocks:** A deterministic fallback mode for your local evaluation stack. Artifact: an `agents-sdk/evals/structured_runner.py` that passes explicit JSON-schema/GBNF grammars directly to Ollama/LM Studio. This proves `devstral`'s true reasoning ceiling on Tier C tasks, rescuing that 35% score by stripping away the formatting penalty entirely.

### 2. Chat Template Abstraction (Evaluation-Prompt Co-adaptation)
**What to add:** Chat Template Pre-Processing (Jinja2). The concept complains about generic JSON schemas clashing with Mistral-style templates but lacks an architectural solution. Your eval pipeline shouldn't hardcode prompt wrappers; it should pass raw intents through model-specific Jinja templates prior to inference to match their exact training distributions.
**Who/What exemplifies it:** *EleutherAI's LM Evaluation Harness* (specifically their architectural pivot to use Hugging Face Jinja chat templates for target-specific formatting) and Sander Schulhoff et al.'s *"The Prompt Report: A Systematic Survey of Prompting Techniques"*.
**What this unlocks:** A universal, model-agnostic benchmarking suite. Artifact: an update to `agents-sdk/config.toml` mapping model string IDs to their native Jinja templates. This allows your `meta-agent` to evaluate `gemma4` and `devstral` simultaneously against the same logical test set without triggering format-mismatch artifacts.

### 3. Format Sensitivity Measurement (Quantifying the Artifact)
**What to add:** Perturbation-Based Evaluation (Format Jittering). The concept identifies that the artifact exists but provides no mechanism to measure its magnitude. You need a formal framework to isolate how much of the failure is cognitive (reasoning collapse) versus syntactic (brittle prompt parsing).
**Who/What exemplifies it:** Percy Liang et al.'s *HELM (Holistic Evaluation of Language Models)* (specifically the section detailing their `data_augmentation` framework for measuring robustness to prompt formatting variations).
**What this unlocks:** A new, defensible metric for your fleet routing decisions. Artifact: a `vault/health/model-robustness-matrix.md` generated during Topic 20 refreshes. Instead of relying solely on peak accuracy, this lets you quantify "format variance"—justifying the selection of a model that might have a lower peak score but won't catastrophically fail when your daily-driver skill prompts subtly drift over time.
