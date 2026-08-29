# NotebookLM cross-corpus query 3 (2026-08-29)

Notebook: Startup-Ideas-AI-Agents-Software-Factory-Notebook (57 sources; query scoped to the factory subset).

## Question

Where do EVALS sit in the factories and agent systems described across these sources — as gates that block work from shipping, as monitors observing behavior, or both? Include the Anthropic "Demystifying evals for AI agents" source, the Basis ontologies-and-evals talk, the Databricks enterprise playbook, and anything on long-horizon agent evaluation or memory harnesses. Name the source for each claim.

## Answer (NotebookLM, verbatim; [n] cite the sources listed at bottom)

Across the systems and organizations highlighted in your sources, evaluations (evals) are designed to play a dual role: they act as **both pre-deployment gates that block regressions and lower-quality code from shipping, and as continuous production monitors observing live behavior, token costs, and API loops.**

Rather than treating evaluations as static, one-time tests, the top practitioners build highly dynamic, multi-layered evaluation infrastructure integrated directly into their development lifecycles and production environments. Here is how they deploy them in practice:

---

### **1. Gating the System: CI/CD and Pre-Deployment Evals**
Automated evaluation suites are widely implemented as programmatic gates to allow developers to iterate quickly, test against hundreds of scenarios before shipping, and safely adopt new frontier models [1, 2].

*   **Anthropic's "First Line of Defense" Gating:** 
    Anthropic reports that automated evaluations act as the primary pre-launch defense mechanism in continuous integration (CI/CD) pipelines [3]. Without these gates, product teams become trapped in "reactive loops," identifying bugs only after they hit live users, where fixing one failure inadvertently triggers regressions elsewhere [1, 4]. 
    To operate this gate effectively, Anthropic separates its test suites into two distinct categories [5]:
    *   **Capability (Quality) Evals:** Highly challenging tasks where the agent initially has a low pass rate, giving the engineering team "a hill to climb" [5].
    *   **Regression Evals:** High-pass-rate suites (approaching 100% correctness) designed to block deployment if an update degrades performance [5]. Once an agent is optimized, successful capability evals "graduate" to the regression suite to be run on every commit and model upgrade [3, 6].
*   **Databricks' "Eval-First" Gating Protocol:**
    **Sandipan Bhaumik** (Databricks) outlines an enterprise playbook where **building the evaluation layer must precede writing any application code or selecting models** [7]. In a retail banking chatbot case study, his team spent **weeks 1 and 2 purely on building the evaluation database** (compiling 200 real human agent chats to represent the "golden data set") and establishing metrics before ever testing a model [8, 9]. They did not select or deploy their primary LLM until **week 7**, using the pre-built eval database to run benchmarking trials and select the most accurate, cost-effective model [8, 10].
*   **Balancing Gating Costs in CI:**
    Because running long-horizon agent trajectories against extensive evaluation datasets is extremely expensive and time-consuming, Bhaumik implements a **tiered CI gating architecture** [11]:
    *   **In-dev/CI Branch Checks:** The system runs a lightweight, representative subset of the eval data to provide fast, cost-effective feedback to developers making prompt edits [12].
    *   **Main Merge Gate:** The full, comprehensive evaluation suite is triggered strictly as a gate when merging code to the main branch [12].

---

### **2. Monitoring Behavior: Live Production Observability & Auditing**
Evaluating an agent solely based on whether its final output is "correct" is a major point of failure [13, 14]. An agent can frequently arrive at a correct final state through inefficient, expensive, or insecure trajectories [15, 16]. As a result, practitioners deploy evals as active monitors in production.

*   **Databricks' Live Multi-Layered Monitors:**
    Bhaumik establishes a **three-tier evaluation architecture** to continuously analyze live production traces [17]:
    1.  **Deterministic Checks (Layer 1):** Regex, formatting, and lightweight classification models to scan for PII breaches or format issues [17-19].
    2.  **Semantic Checks (Layer 2):** Deploying "LLM-as-a-judge" scorers (integrated via MLflow) on live traces to continuously rate the relevance, safety, and groundedness of responses [18, 20].
    3.  **Behavioral Checks (Layer 3):** Specifically auditing tool calls [14]. For example, a semantic check might confirm that an agent successfully answered a user's account balance query [14]. However, the behavioral monitor might reveal that the agent made **three duplicate, failing database API calls** to find that single answer [14, 16]. This identifies silent loops, redundant computation, and costly inefficiencies that traditional outcome evaluations miss [16, 21].
*   **The Live Feedback Loop & Incident Playbooks:**
    In the Databricks architecture, if the live automated evaluation pipeline flags a response that falls below a defined quality threshold, it acts as a trigger to **deflect the query to a human agent, apply fallback/retry limits, and initiate an incident response playbook** [9, 22-24]. 
    These real-world failures are captured, annotated by domain experts, and funneled back into the offline evaluation test library [9, 24]. This creates a **"living system"** where the evaluation database continually grows based on real production edge cases [9, 24, 25].
*   **Sonar's Agent-Centric Development Cycle (AC/DC):**
    **Tariq Shaukat** (CEO of Sonar) advocates for putting verification at the direct center of the software development loop [26]. Sonar's data shows that without continuous verification, the initial 3x to 5x velocity boost from AI coding tools completely dissipates within three months due to a dramatic spike in security, maintainability, and complexity bugs (technical debt) [27].
    To combat this, Sonar utilizes a zero-trust, multi-layered verification framework that combines **algorithmic verification** (deterministic checks on data flows, control flows, and secrets) with **agentic verification** (evaluating business intent and logic) directly within the active agentic loops and CI verification runs [28-30].

---

### **3. Trajectory-Level Evaluation and "Behavior Specifications" (Basis)**
In long-horizon workflows like corporate tax preparation, which can involve thousands of execution steps and multiple days of autonomous running, standard outcome metrics are insufficient [13, 31-33].

*   **Process Over Outcome:**
    **Mitch Troyanovsky** (co-founder of Basis) argues that outcome-only evals are dangerous because they fail to generalize to production [13]. An agent could easily pull a correct accounting answer out of its pre-training weights or a random blog, but a professional firm cannot trust that output because the *process* was non-compliant [15, 34].
    Troyanovsky emphasizes:
    > *"you're not a serious person if you're doing production stuff for real customers who are paying real money and you don't have mass amounts of evals"* [35].
*   **The Behavior Specification Standard (`BEHAVIOR.md`):**
    To solve this, Basis co-created an open-source standard with Braintrust called **"Behavior Specifications" (or specs)** [36, 37]. Written in Markdown by a joint team of domain experts (accountants) and ML researchers, these files act as **both a specification to align humans on product goals and a programmatic rubric to grade the agent's reasoning** [37, 38].
    Instead of relying on rigid, brittle assertions checking the exact sequence of tool calls (which Anthropic also warns suppresses valid, creative agentic behavior) [37, 39], Basis utilizes **advanced "agent judges"** [40, 41]. These judges read the entire multi-layered execution trajectory (or "lived experience") to evaluate whether the agent adhered to crucial meta-behaviors, such as citing primary sources (e.g., the IRS website) rather than Wikipedia [34, 40-42].

---

### **4. Evaluating Long-Horizon Memory Harnesses (Sakana.ai)**
When building long-running research agents, evaluations are run directly on-device to measure the stability, correctness, and token cost of different memory retrieval architectures [43-45].

*   **Memory Evals as a Financial Metric:**
    **Stefania Druga** (Sakana.ai) runs non-stop, on-device evaluations using local M3 Ultra hardware to test how different memory harnesses perform over hundreds of steps [44, 45]. Testing against established benchmarks like **Xbench** (for long-horizon retrieval outside the context window) and **Spider V2**, Sakana.ai treats the **recall policy as a first-class evaluation metric** [46, 47].
    Druga's evaluations revealed a critical financial and behavioral insight: **"bad memory is expensive because it spends more token and it can send agent the wrong way"** [47]. Her evaluations proved that when tasks fit within the active context window, memory harnesses add zero capability and merely increase token cost [46, 48]. However, in long-horizon scenarios, a structured, ranked-recall ledger dramatically **improves success rates while saving token budget** by feeding the agent only highly relevant historical states [46, 47, 49].

***

📊 Would you like to map out a structured markdown template for your own `BEHAVIOR.md` specification to help grade your agent trajectories, or examine the Pydantic schema for setting up a behavioral "LLM-as-a-judge" scanner?

## Citation map

- [1] Demystifying evals for AI agents \ Anthropic
- [2] Demystifying evals for AI agents \ Anthropic
- [3] Demystifying evals for AI agents \ Anthropic
- [4] Demystifying evals for AI agents \ Anthropic
- [5] Demystifying evals for AI agents \ Anthropic
- [6] Demystifying evals for AI agents \ Anthropic
- [7] The Production AI Playbook: Deploying Agents at Enterprise S
- [8] The Production AI Playbook: Deploying Agents at Enterprise S
- [9] The Production AI Playbook: Deploying Agents at Enterprise S
- [10] The Production AI Playbook: Deploying Agents at Enterprise S
- [11] The Production AI Playbook: Deploying Agents at Enterprise S
- [12] The Production AI Playbook: Deploying Agents at Enterprise S
- [13] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [14] The Production AI Playbook: Deploying Agents at Enterprise S
- [15] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [16] The Production AI Playbook: Deploying Agents at Enterprise S
- [17] The Production AI Playbook: Deploying Agents at Enterprise S
- [18] The Production AI Playbook: Deploying Agents at Enterprise S
- [19] The Production AI Playbook: Deploying Agents at Enterprise S
- [20] The Production AI Playbook: Deploying Agents at Enterprise S
- [21] The Production AI Playbook: Deploying Agents at Enterprise S
- [22] The Production AI Playbook: Deploying Agents at Enterprise S
- [23] The Production AI Playbook: Deploying Agents at Enterprise S
- [24] The Production AI Playbook: Deploying Agents at Enterprise S
- [25] The Production AI Playbook: Deploying Agents at Enterprise S
- [26] In the Land of AI Agents, the Verifiers Are King — Tariq Sha
- [27] In the Land of AI Agents, the Verifiers Are King — Tariq Sha
- [28] In the Land of AI Agents, the Verifiers Are King — Tariq Sha
- [29] In the Land of AI Agents, the Verifiers Are King — Tariq Sha
- [30] In the Land of AI Agents, the Verifiers Are King — Tariq Sha
- [31] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [32] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [33] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [34] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [35] Ontologies, Evals & Deployed Intelligence: Building Real AI 
- [36] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [37] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [38] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [39] Demystifying evals for AI agents \ Anthropic
- [40] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [41] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [42] How to Build Autonomous, Long-Horizon AI Agents | Basis
- [43] Memory Harnesses for Long-Running Research Agents — Stefania
- [44] Memory Harnesses for Long-Running Research Agents — Stefania
- [45] Memory Harnesses for Long-Running Research Agents — Stefania
- [46] Memory Harnesses for Long-Running Research Agents — Stefania
- [47] Memory Harnesses for Long-Running Research Agents — Stefania
- [48] Memory Harnesses for Long-Running Research Agents — Stefania
- [49] Memory Harnesses for Long-Running Research Agents — Stefania
