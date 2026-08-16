# AI Flashcards

## Card 1

**Q:** In 2026 practitioner discourse, what discipline is identified as the successor to prompt engineering?

**A:** Loop engineering

---

## Card 2

**Q:** According to Senior AI PMs, what component in an AI loop acts as the primary bottleneck rather than the model?

**A:** The verifier

---

## Card 3

**Q:** In the 'Model $\to$ Harness' shift, what are the three primary components that define a 'harness'?

**A:** Planning, context management, and evals

---

## Card 4

**Q:** What formula is used to calculate the quality of an AI product harness?

**A:** $\text{Harness Quality} = \text{Plan Quality} \times \text{Context Quality} \times \text{Eval Quality}$

---

## Card 5

**Q:** What is considered the most valuable telemetry or data point an AI product can collect from users?

**A:** Corrective data from expert users

---

## Card 6

**Q:** In AI product management, when does a product roadmap fundamentally become an 'eval problem'?

**A:** When the feature becomes probabilistic

---

## Card 7

**Q:** What are the three core building blocks of an AI eval?

**A:** Dataset, Task, and Scorers

---

## Card 8

**Q:** In the context of AI evals, what does a 'Dataset' represent?

**A:** A collection of inputs representing how real people interact with the product.

---

## Card 9

**Q:** In the context of AI evals, what is defined as the 'Task'?

**A:** The system being evaluated, such as a prompt chain, agent, or workflow.

---

## Card 10

**Q:** In the context of AI evals, what is the function of 'Scorers'?

**A:** They define the dimensions of quality and provide measurements (typically between 0 and 1).

---

## Card 11

**Q:** Why should PMs avoid lumping multiple quality dimensions into a single score?

**A:** It leads to accidental optimization where one dimension (like tone) improves while another (like accuracy) regresses.

---

## Card 12

**Q:** What is the primary difference between a 'benchmark' and an 'eval'?

**A:** Benchmarks measure raw model capability on fixed sets; evals measure system performance on specific application tasks.

---

## Card 13

**Q:** Which AI development stage involves millisecond-latency sanity checks on every commit?

**A:** Development (Unit Tests)

---

## Card 14

**Q:** What is the purpose of 'CI regression' testing in an AI pipeline?

**A:** To ensure every pull request that touches a prompt or model does not regress quality against a golden dataset.

---

## Card 15

**Q:** How does 'Production Monitoring' differ from 'Offline Evaluation'?

**A:** Monitoring catches changes that happen to the system (drift, provider updates), whereas offline evaluation catches changes made by the team.

---

## Card 16

**Q:** Term: Golden Dataset

**A:** Definition: A curated, trusted set of test cases used to evaluate an AI application before every meaningful change.

---

## Card 17

**Q:** What is the 'Holdout Set' in AI evaluation used to prevent?

**A:** Goodhart’s Law (optimizing only for what is measured) by using a grading set the loop never sees during development.

---

## Card 18

**Q:** In loop engineering, what are the three components of a 'stop condition'?

**A:** Target (average score), budget (max rounds/cost), and stall (lack of improvement).

---

## Card 19

**Q:** Describe the 'Champion/Challenger' pattern in loop engineering.

**A:** A new change (challenger) must beat the current version (champion) on a holdout set before being promoted.

---

## Card 20

**Q:** In the dimensions of quality, how does 'Faithfulness' differ from 'Correctness'?

**A:** Faithfulness measures if output is grounded in provided context; Correctness measures if output is factually accurate to a known truth.

---

## Card 21

**Q:** Dimension: Relevance

**A:** Definition: Whether the AI response addresses the specific intent of the user's query.

---

## Card 22

**Q:** Why are 'Binary Checks' (Pass/Fail) preferred over 1-10 Likert scales for evaluators?

**A:** Binary checks are falsifiable and resist 'vibe-based' gaming that leads to low-variance, unhelpful data.

---

## Card 23

**Q:** What is 'Position Bias' in LLM-as-a-judge systems?

**A:** The tendency of a judge model to prefer a candidate response based on its order in the prompt (e.g., first vs. second).

---

## Card 24

**Q:** What is 'Verbosity Bias' in LLM evaluation?

**A:** The tendency for judge models to give higher scores to longer outputs regardless of content quality.

---

## Card 25

**Q:** Targeting human alignment, what is the recommended 'Pearson correlation' threshold for a judge model's scores?

**A:** Above $0.7$

---

## Card 26

**Q:** In the Agent Development Lifecycle (ADLC), what is the function of the 'Monitor' stage?

**A:** To score real production traces to catch drift, safety issues, and recurring failure modes.

---

## Card 27

**Q:** What is a 'Trace' in the context of AI evaluation?

**A:** A structured log recording every step of a response, including query, retrieved context, tool calls, and reasoning.

---

## Card 28

**Q:** Why is 'structured tracing' considered a prerequisite for effective evaluation?

**A:** It allows a team to diagnose the specific cause of a failure (e.g., poor retrieval vs. model hallucination) rather than just seeing the error.

---

## Card 29

**Q:** How should a PM handle 'Proxy Decay' in metrics architecture?

**A:** By continuously validating that offline proxies still correlate with real-world online outcomes.

---

## Card 30

**Q:** What is 'Bottom-up Error Analysis'?

**A:** The process of reading actual failures, clustering them, and designing metrics/fixes to attack those specific clusters.

---

## Card 31

**Q:** In loop engineering, why is the 'one change per round' rule enforced?

**A:** To ensure that when a score moves, the specific cause of the improvement or regression is known.

---

## Card 32

**Q:** What is the role of a 'Subject Matter Expert' (SME) in AI evaluation?

**A:** To provide domain-specific labels that serve as the ground truth for subjective quality.

---

## Card 33

**Q:** In the Braintrust framework, what is an 'Experiment'?

**A:** A collection of evals run with a specific configuration, such as a new prompt or model temperature setting.

---

## Card 34

**Q:** What are the three phases of agent development described by Braintrust?

**A:** Incubation, Refinement, and Scale.

---

## Card 35

**Q:** What is the 'Incubation' phase focused on?

**A:** Defining ideal use cases and creating the initial 'golden dataset' for target personas.

---

## Card 36

**Q:** What is a 'Debug Mode' for AI agents?

**A:** The ability for PMs to inspect the agent's internal reasoning, tool calls, and context at every step.

---

## Card 37

**Q:** In the scale phase, what is the benefit of a dedicated Slack channel for 'negative signals'?

**A:** It allows PMs to read transcripts of real failures to build intuition about failure patterns dashboards might miss.

---

## Card 38

**Q:** How does 'Loop' (the Braintrust assistant) aid PM workflows?

**A:** It summarizes experiments, generates eval components, and identifies failure patterns in production data.

---

## Card 39

**Q:** What is a 'deterministic check' in evaluation?

**A:** A code-based check (e.g., 'is response under 200 words?') that does not rely on an LLM's subjective judgment.

---

## Card 40

**Q:** According to the 'Agentic AI Institute,' products in 2026 are increasingly viewed as _____ rather than just models.

**A:** Harnesses

---

## Card 41

**Q:** In the Hamel Husain framework, what is 'Level 1' evaluation?

**A:** Unit Tests (assertions using tools like pytest) that run fast and cheaply.

---

## Card 42

**Q:** Why is 'synthetic data generation' useful for new features?

**A:** It fills coverage gaps for scenarios production hasn't exercised yet, allowing testing before launch.

---

## Card 43

**Q:** Term: Prompt CI/CD

**A:** Definition: The practice of versioning, gating, and rolling out prompts with the same rigor as software code.

---

## Card 44

**Q:** What characterizes a 'Weak Judge' in AI evaluation?

**A:** A judge that provides vague, non-falsifiable scores (e.g., 'helpfulness' without a rubric) that models can easily game.

---

## Card 45

**Q:** What is the 'offline-online gap'?

**A:** The phenomenon where high performance on a curated test set does not translate to high quality for real users.

---

## Card 46

**Q:** In metrics architecture, what are 'Guardrail Metrics'?

**A:** Dimensions that must not regress (e.g., latency, cost) while optimizing for target quality metrics.

---

## Card 47

**Q:** What does 'Epistemic Humility' mean for an LLM-as-a-judge system?

**A:** The recognition of specific failure modes or domains where the model is fundamentally incapable of judging quality.

---

## Card 48

**Q:** Process: Golden Dataset Maintenance

**A:** Continually add real failures, deduplicate near-identical intents, and archive obsolete items as product behavior changes.

---

## Card 49

**Q:** What is the 'Benchmark Trap'?

**A:** Treating high scores on public benchmarks (like MMLU) as proof that a model will perform well on a specific enterprise task.

---

## Card 50

**Q:** What is 'Benchmark Contamination'?

**A:** The inclusion of benchmark test items in a model's training data, leading to artificially inflated performance scores.

---

## Card 51

**Q:** In evaluation systems, why is 'Archiving' preferred over 'Deleting' obsolete test items?

**A:** Archiving preserves version history so historical experiment runs remain interpretable.

---

## Card 52

**Q:** What is the purpose of 'Context Hub' in LangChain's ecosystem?

**A:** To manage and version the instructions, skills, and examples (context) that agents rely on separately from code.

---

## Card 53

**Q:** How do 'Sandboxes' improve evaluations for coding agents?

**A:** By allowing the eval to watch the actual execution (exit status, file changes) rather than just grading the text of the code.

---

## Card 54

**Q:** What is 'SmithDB'?

**A:** A high-performance data layer designed specifically for the nested, multi-piece nature of AI agent traces.

---

## Card 55

**Q:** In the ADLC, when is 'Human Review' most essential?

**A:** During the calibration of the judge model and for high-stakes domains like legal or clinical products.

---

## Card 56

**Q:** Why is 'binary alignment' (matching pass/fail) better than Likert agreement for calibrating judges?

**A:** Likert scales often show high agreement because both judge and human avoid extreme scores, hiding actual misalignments.

---

## Card 57

**Q:** What does a 'Stall Detector' look for in a learning loop?

**A:** It identifies when a system has gone N rounds without improvement, signaling that the current approach is exhausted.

---

## Card 58

**Q:** What is the 'Stop-the-line' criterion in AI deployments?

**A:** Pre-defined metric thresholds (e.g., safety failure rate > 0%) that automatically trigger a rollback.

---

## Card 59

**Q:** In the 2026 AI PM curriculum, what is the 'Master-Tutor' stance regarding quality?

**A:** Choosing diagnosis of structural causes over the delivery of new prompts or features.

---

## Card 60

**Q:** According to the LangChain source, what is 'Agent trajectory'?

**A:** The sequence of steps, tool calls, and reasoning paths an agent takes to arrive at a final output.

---

## Card 61

**Q:** In the Rechat case study, what was the 'Whack-a-mole' symptom?

**A:** Addressing one AI failure mode only for new ones to emerge, resulting in a performance plateau.

---

## Card 62

**Q:** Why is 'dataset schema validation' important in collaborative AI teams?

**A:** It prevents malformed items from multiple contributors from breaking experiment runs.

---

## Card 63

**Q:** What is 'Embedding-based drift detection'?

**A:** Using vector similarity to identify when incoming production queries differ meaningfully from the golden dataset.

---

## Card 64

**Q:** In the context of evals, what is a 'falsifier'?

**A:** A specific condition or result that would prove a hypothesis about a model's behavior wrong.

---
