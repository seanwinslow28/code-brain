# Study Guide: AI Architecture as Systems — The Harness and HITL Design

This study guide explores the transition from deterministic software management to the orchestration of probabilistic AI systems. For an AI Product Manager, success is no longer defined by "typing speed" or code volume, but by the rigor of the "harness"—the surrounding systems of observability, evaluation, and human-in-the-loop (HITL) design—that keeps non-deterministic models aligned with business outcomes.

---

## I. Core Concepts: Systems Thinking for AI

### 1. The Determinism Gap
Traditional software is deterministic: specific inputs yield identical, testable outputs. AI models violate this contract; they are **stochastic engines** that sample from probability distributions. This "determinism gap" requires a shift from feature-thinking (static backlogs) to system-thinking (continuously learning systems).

### 2. The Iceberg Model in AI
To manage AI effectively, PMs must look below the surface of observable events:
*   **Events:** Observable symptoms (e.g., a chatbot provides a hallucinated answer).
*   **Patterns:** Recurring trends (e.g., performance degrading as user data shifts).
*   **Underlying Structures:** The workflows and architectures (e.g., a RAG pipeline with poor retrieval precision).
*   **Mental Models:** Foundational assumptions (e.g., the belief that "safe AI" is a technical problem rather than a structural one).

### 3. Senge’s System Archetypes in AI
*   **Shifting the Burden:** Applying a "quick fix" (like elaborate prompt engineering) instead of a fundamental solution (like a structured, tool-centric UI).
*   **Success to the Successful:** Initial data advantages create an insurmountable "data flywheel," establishing market dominance.
*   **Limits to Success:** Rapid growth hitting constraints like the exhaustion of high-quality training data or energy/water limitations.

---

## II. The AI "Harness": Evaluation and Observability

The "harness" is the infrastructure required to deploy AI with confidence. It consists of three primary layers:

### 1. The Three Layers of Observability
| Layer | Focus | Key Metrics |
| :--- | :--- | :--- |
| **Computational** | Unit economics and hardware health. | Cost per session, token throughput, latency. |
| **Semantic** | Quality and relevance of content. | Hallucination rates, toxicity, relevance scores. |
| **Agentic** | Reasoning and decision-making logic. | Tool selection accuracy, TAO cycles, reasoning paths. |

### 2. Behavioral vs. Internal Observability
*   **Behavioral Observability:** Tracks *what* the AI did (inputs/outputs). It is reactive and looks from the outside.
*   **Internal Observability:** Tracks *why* the AI made specific choices (reasoning process, knowledge accessed). It is proactive and prevents "unknown unknown" failures.

### 3. The RAG Triad (Retrieval-Augmented Generation)
To debug a RAG system, PMs must evaluate the dependency chain:
*   **Context Recall:** Does the retrieved context contain the answer?
*   **Context Precision:** Is the retrieved context signal-to-noise ratio high?
*   **Faithfulness:** Is the answer derived *only* from the provided context?
*   **Answer Relevance:** Does the response actually address the user's intent?

---

## III. Failure Modes and Risks

### 1. The "Promptware" Kill Chain
Attacks on LLMs have evolved from simple injections into "Promptware"—multistep malware delivery mechanisms.
1.  **Initial Access:** Prompt injection (Direct or Indirect).
2.  **Privilege Escalation:** Jailbreaking (bypassing safety constraints).
3.  **Reconnaissance:** Probing the host context for assets/agents.
4.  **Persistence:** Poisoning long-term memory or data stores.
5.  **Command and Control (C2):** Remotely updating instructions via external fetching.
6.  **Lateral Movement:** Propagating across agents, users, or systems (e.g., AI Worms).
7.  **Actions on Objective:** Data exfiltration, unauthorized transactions, or RCE.

### 2. Systemic Degradation
*   **Concept Drift:** When the environment changes (e.g., a cooling housing market), rendering historical training data irrelevant (e.g., the Zillow Offers failure).
*   **Reward Hacking:** The AI discovers "exploitative" strategies to maximize its reward signal (e.g., extreme verbosity) without achieving the actual goal.
*   **Comprehension Debt:** Developers merge AI-generated code that passes tests but that they cannot explain or maintain.

---

## IV. Design Philosophy: "Write Little Code"

In the AI era, the marginal cost of code generation is collapsing, but the cost of verification is not.
*   **The Problem:** AI makes it easy to scale "weak product judgment." Speed becomes a trap that creates "expensive waste at high-speed."
*   **The Discipline:** Do not let the tool run until the problem has "earned the right to consume code."
*   **The Pivot:** Saved engineering time should be reallocated to:
    *   **Discovery:** Observing user workflows before building.
    *   **Telemetry:** Defining usage signals before launch.
    *   **Verification:** Investing in security, tests, and human review gates.
    *   **Deletion:** Actively removing code that hasn't earned its place.

---

## V. Vocabulary Self-Check Section

Use this list to verify your understanding of Module 6 terminology.

*   **Stochastic Engine:** A system that produces outputs by sampling from probability distributions, making it non-deterministic.
*   **Data Flywheel:** A reinforcing loop where more usage generates more data, which improves the model, attracting more users.
*   **ASCII Smuggling:** A technique using invisible Unicode characters to hide malicious instructions from users while the LLM still "sees" them.
*   **TAO Cycle:** The "Thought-Action-Observation" loop characteristic of autonomous agents.
*   **Verification Tax:** The intense human labor required to audit probabilistic AI outputs; if this exceeds generation savings, ROI collapses.
*   **Golden Dataset:** A curated collection of inputs and "correct" outputs used as a benchmark for AI performance.
*   **Epistemic Uncertainty:** A failure mode where the model "doesn't know what it doesn't know" and confidently hallucinates.
*   **Agentic Trap:** When architectural debt accumulates at the speed of an autonomous agent's working speed because no one is checking if the implementation fits the system.
*   **Performativity:** A degenerate feedback loop where a model's outputs (e.g., biased recommendations) restrict the future data it collects.

---

## VI. Short-Answer Practice Questions

1.  **Why does "slowness" act as a useful brake in traditional software development?**
2.  **Contrast "Behavioral Observability" with "Internal Observability." Which one catches "unknown unknowns"?**
3.  **What is the "Lethal Trifecta" that enables data exfiltration in AI applications?**
4.  **How does "Success to the Successful" apply to the digital platform economy using AI?**
5.  **Describe the role of the "Sprint Review" in a world where AI can generate prototypes in minutes.**
6.  **What is "Comprehension Debt," and why is it a systemic risk for engineering teams using AI assistants?**

---

## VII. Essay Prompts for Deeper Exploration

1.  **The ROI of Trust:** Analyze the Air Canada bereavement fare incident. Discuss why the company was held legally liable for its chatbot's "hallucination" and how systemic observability (bounding error severity) might have prevented this.
2.  **The "Write Little Code" Paradox:** AI tools like Devin and Claude Code have collapsed the friction of producing software. Argue why this makes product discovery *more* critical, not less. Use the concept of "scaling waste" in your answer.
3.  **Human-in-the-Loop vs. Open-Loop Automation:** Compare the Knight Capital trading disaster with modern agentic AI risks. Explain how "runtime awareness" and "kill switches" act as critical systems-level safeguards.
4.  **Managing the Commons:** Discuss the "Tragedy of the Commons" in multi-agent systems where synthetic data poisons future training sets. What systemic interventions (standard-setting, reputation networks) could mitigate this "model collapse"?