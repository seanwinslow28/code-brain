# Module 7 Study Guide: Evals, Metrics Architecture, and Loop Engineering

This study guide provides a comprehensive overview of Module 7, focusing on the transition from simple prompt engineering to the rigorous discipline of loop engineering and systematic evaluation. It is designed for AI Product Managers who must move from "vibe-based" development to data-driven systems thinking.

---

## 1. Core Concepts: The 2026 Practitioner Perspective

### The Shift from Model to Harness
In 2026, the industry consensus has shifted: the model is a commodity, while the **harness** is the product. A harness consists of planning, context management, and evals. Product quality is defined by the formula: 
`Harness Quality = Plan Quality × Context Quality × Eval Quality`. 

The core bottleneck in any AI system is no longer the model's raw capability, but the **verifier**. Consequently, an AI product roadmap eventually becomes an evaluation problem.

### The Anatomy of an Eval
An **eval** is a repeatable measurement of whether an AI's output meets the product's definition of "good." While engineers build the "plumbing" (the infrastructure to run tests), the AI PM defines the success criteria.
*   **Dataset:** A collection of inputs representing real-world interactions (Golden Dataset).
*   **Task:** The system being tested (e.g., a prompt, a chain, or a full agent).
*   **Scorers:** The dimensions of measurement (e.g., correctness, tone, safety).

### Loop Engineering
A real AI loop is a decision system, not a one-off generation. It requires nine specific components:
1.  **Goal:** The intended outcome.
2.  **Context:** The situational data provided.
3.  **Actions:** What the system can do.
4.  **Tools:** The APIs or functions available.
5.  **Evals:** The internal check on quality.
6.  **Memory:** Persistence of past states or interactions.
7.  **Guardrails:** Safety and policy boundaries.
8.  **Escalation:** When to involve a human or a higher-tier system.
9.  **Stop Condition:** A trio consisting of a **Target** (e.g., holdout score ≥ X), a **Budget** (max rounds/dollars), and a **Stall Detector** (N rounds without improvement).

### The Golden Dataset and the Holdout Split
A **Golden Dataset** is a curated, versioned set of test cases trusted by domain experts. 
*   **Small and Fresh:** 50–100 high-quality cases are better than 1,000 "noisy" ones. 
*   **Provenance:** Every item should ideally come from real production failures or expert-logged traces.
*   **The Split:** PMs must maintain an **Improvement Set** (used for iteration) and a **Holdout Set** (kept secret from the development loop). Optimizing against the holdout set is the only way to avoid "gaming the metric" (Goodhart’s Law).

---

## 2. Short-Answer Practice Questions

**Q1: Why is "Rate this 1–10" considered a weak eval?**
*   **Answer:** Models learn to "praise" or please vague judges quickly. A 1–10 scale is subjective, lacks a shared definition, and often clusters in the 3–4 range, making the data noisy and unactionable.

**Q2: What is the "One-Change Rule" in the Champion/Challenger pattern?**
*   **Answer:** In each iteration round, you propose exactly one change (the challenger). This ensures that any movement in the evaluation score can be attributed to that specific modification.

**Q3: Define "Proxy Decay" in the context of metrics architecture.**
*   **Answer:** Proxy decay occurs when an offline metric that previously correlated with a business outcome (like retention or conversion) stops being a reliable predictor due to shifts in user behavior or model drift.

**Q4: What are the three components of a Loop's "Stop Condition"?**
*   **Answer:** 1) **Target** (reaching a specific quality score), 2) **Budget** (hitting a limit on time or spend), and 3) **Stall** (failure to improve over a set number of rounds).

**Q5: What is the difference between a Trace and a Log?**
*   **Answer:** A log is a simple record of events. A trace is a structured, nested tree that captures the full execution context, including retrieved chunks, tool calls, reasoning steps, and model latency, allowing for deep diagnosis of failures.

---

## 3. Essay Prompts for Deeper Exploration

### Prompt 1: The "Diagnosis over Delivery" Framework
The curriculum emphasizes that a professional AI PM prioritizes "diagnosis over delivery." Explain why the amateur instinct is to change the model or prompt immediately upon seeing a failure, and describe the systematic steps a professional would take to cluster failures and identify structural causes before touching the system. Use the "Rechat Whack-a-Mole" case study as a reference.

### Prompt 2: Bridging the Offline–Online Gap
AI systems often exhibit a 10% gain in offline evals while showing zero movement in online product metrics. Discuss the structural causes of this gap. How should a PM design a metrics stack that accounts for "drift" and "proxy decay"? What "stop-the-line" criteria should be wired to this stack to protect user experience?

### Prompt 3: The Role of the Human in 2026 Loop Engineering
While LLM-as-a-judge allows for scale, "correctness is subjective and must be aligned with a human." Argue for the necessity of human calibration in evaluation systems. How does a PM establish "ground truth" and "epistemic humility" in an automated loop? Describe the process of aligning an evaluator model with a human domain expert using binary rubrics and critiques.

---

## 4. Vocabulary Self-Check (Glossary)

Use the following table to verify your mastery of the module's technical language.

| Term | Definition |
| :--- | :--- |
| **Eval** | A repeatable, structured measurement of AI output quality against a specific product rubric. |
| **Golden Dataset** | A curated, versioned collection of inputs and "gold" reference outputs representing real-world failure modes. |
| **Provenance** | The origin record of a test case (e.g., which production trace or user feedback session generated it). |
| **Holdout Set** | A subset of the Golden Dataset that the system/developer never sees during iteration; used for the final "title fight" evaluation. |
| **Binary Check** | A falsifiable, yes/no question used for evaluation (e.g., "Is the UUID hidden?"), which is more resistant to gaming than 1–10 scales. |
| **Champion/Challenger** | A discipline where the current best version (Champion) is baselined, and a new version (Challenger) must beat it on a holdout set to be promoted. |
| **LLM-as-a-Judge** | Using a high-capability model to score the outputs of another model/agent based on a defined rubric. |
| **Proxy Decay** | The phenomenon where a metric loses its correlation with real-world outcomes over time. |
| **Bottom-up Error Analysis** | The practice of reading actual failures, clustering them into patterns, and attacking the largest cluster rather than chasing top-level scores. |
| **Goodhart-Pair** | A set of metrics designed to balance each other (e.g., optimizing for accuracy while ensuring latency does not regress). |
| **Stop-the-line** | Automated criteria (e.g., a high safety failure rate) that trigger an immediate rollback or halt of a deployment. |
| **Stall Detector** | A mechanism in loop engineering that stops the process if the system fails to improve after a defined number of rounds. |
| **Epistemic Humility** | Acknowledging the limits of what an automated judge can reliably score without human verification. |