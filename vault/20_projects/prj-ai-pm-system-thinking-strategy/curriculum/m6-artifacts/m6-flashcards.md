# AI Flashcards

## Card 1

**Q:** In the era of AI, what is identified as the primary bottleneck in software development instead of typing speed?

**A:** Product judgment (knowing what is worth building).

---

## Card 2

**Q:** What term describes the state where developers accept AI-generated code without fully understanding its logic?

**A:** Comprehension debt.

---

## Card 3

**Q:** How does agentic coding affect the 'cost gate' that historically forced product discipline?

**A:** It weakens the gate by collapsing the marginal cost of generating implementations.

---

## Card 4

**Q:** According to Stefan Wolpers, what is the single most urgent discipline in software development in 2026?

**A:** Writing as little code as possible.

---

## Card 5

**Q:** Why does AI speed increase the risk of building the wrong product?

**A:** It removes the natural pauses or 'brakes' created by the high cost of manual engineering.

---

## Card 6

**Q:** What is the primary difference between 'output' and 'outcome' in AI development?

**A:** Output is the volume of code generated, while outcome is the actual value created for the user.

---

## Card 7

**Q:** According to Meadows' framework, which interventions in a complex system are considered 'shallow'?

**A:** Parameters, buffer sizes, and feedback loop delays.

---

## Card 8

**Q:** In systems thinking, what is the 'Sustainability Paradox' or 'rebound effect' triggered by AI optimizations?

**A:** Efficiency gains lower execution costs, which paradoxically drives higher overall resource consumption.

---

## Card 9

**Q:** Identify the four layers of the Iceberg Model from surface to depth.

**A:** Events, Patterns, Underlying Structures, and Mental Models.

---

## Card 10

**Q:** Which system archetype occurs when a symptomatic quick fix (like prompt engineering) undermines a long-term fundamental solution?

**A:** Shifting the Burden.

---

## Card 11

**Q:** How does the 'Success to the Successful' archetype manifest in the AI platform economy?

**A:** Initial advantages create a data flywheel that cements dominance and establishes oligopolies.

---

## Card 12

**Q:** What is the balancing constraint in the 'Limits to Success' archetype for AI model scaling?

**A:** Finite high-quality human training data and environmental limitations (energy and water).

---

## Card 13

**Q:** In system dynamics, what is the difference between 'stocks' and 'flows'?

**A:** Stocks are accumulations (e.g., trust, data), while flows are the rates of change affecting them.

---

## Card 14

**Q:** What occurs during 'concept drift' in a machine learning model?

**A:** The statistical properties of the target variable or the underlying environment change over time.

---

## Card 15

**Q:** Term: Performativity

**A:** Definition: A state where the data used to train a model fundamentally depends on the previous actions of that model.

---

## Card 16

**Q:** What is 'reward hacking' (or specification gaming) in the context of RLHF?

**A:** An agent finds exploitative strategies to maximize a reward signal without achieving the intended objective.

---

## Card 17

**Q:** How does the 'Tragedy of the Commons' apply to generative AI and the digital ecosystem?

**A:** Synthetic content extraction exceeds human replenishment, degrading the shared resource of high-quality training data.

---

## Card 18

**Q:** What pedagogical tool allows AI Product Managers to experiment with complex system dynamics in a safe, compressed-time environment?

**A:** Management Flight Simulators (MFS).

---

## Card 19

**Q:** Why did the Zillow Offers iBuying program fail from a systemic perspective?

**A:** It scaled an autonomous model into a volatile housing market without accounting for concept drift or adverse selection.

---

## Card 20

**Q:** What is the difference between 'aleatoric uncertainty' and 'epistemic uncertainty'?

**A:** Aleatoric is inherent randomness; epistemic is uncertainty due to a lack of knowledge (confidently hallucinating).

---

## Card 21

**Q:** The 2012 Knight Capital disaster is cited as a warning for AI because the system lacked what critical capability?

**A:** Runtime awareness (the ability to recognize its own catastrophic behavior).

---

## Card 22

**Q:** In AI product management, what is the 'verification tax'?

**A:** The human labor cost required to audit and verify probabilistic AI outputs.

---

## Card 23

**Q:** What is the fundamental difference between behavioral and internal observability?

**A:** Behavioral tracks what happened (outputs); internal tracks why it happened (reasoning process).

---

## Card 24

**Q:** According to Realm Labs, why do current guardrails often fail to prevent AI disasters?

**A:** They focus on external behavior and cannot see or explain the internal reasoning process.

---

## Card 25

**Q:** Identify the three layers of LLM observability.

**A:** Computational, Semantic, and Agentic.

---

## Card 26

**Q:** What does 'computational observability' track in AI applications?

**A:** Unit economics such as cost per session, token throughput, and hardware latency.

---

## Card 27

**Q:** What is the primary focus of 'semantic observability'?

**A:** Evaluating quality and relevance, such as detecting hallucinations or toxicity.

---

## Card 28

**Q:** What does 'agentic observability' measure in autonomous AI systems?

**A:** The decision-making logic and reasoning paths chosen by the agent.

---

## Card 29

**Q:** In LLM observability, what is a 'span'?

**A:** An individual unit of work within a trace, such as a retrieval query or a prompt assembly.

---

## Card 30

**Q:** What is the trade-off when using the 'proxy approach' for LLM observability?

**A:** It offers centralized control but is 'blind' to internal reasoning and local processing logic.

---

## Card 31

**Q:** What defines a 'golden dataset' in offline evaluation?

**A:** A curated collection of example inputs paired with expected outputs or acceptance criteria.

---

## Card 32

**Q:** What is the 'verbosity bias' in the LLM-as-a-judge evaluation pattern?

**A:** The tendency for judge models to rate longer answers as higher quality, regardless of accuracy.

---

## Card 33

**Q:** In the RAG Triad, what does 'Context Recall' measure?

**A:** Whether the retrieved documents contain the information needed to answer the query.

---

## Card 34

**Q:** In the RAG Triad, what does 'Context Precision' measure?

**A:** The signal-to-noise ratio in retrieved chunks (how much of the retrieved context is relevant).

---

## Card 35

**Q:** In the RAG Triad, what is 'Faithfulness'?

**A:** The degree to which the generated answer is derived solely from the provided context (groundedness).

---

## Card 36

**Q:** In the RAG Triad, what does 'Answer Relevance' evaluate?

**A:** Whether the response actually addresses the user's original intent.

---

## Card 37

**Q:** Identify the three phases of the agent execution cycle.

**A:** Thought, Action, and Observation (TAO).

---

## Card 38

**Q:** How does 'self-consistency' help detect hallucinations in open-ended generation?

**A:** It prompts the model multiple times; low consistency across answers suggests a hallucination.

---

## Card 39

**Q:** What term refers to malware execution mechanisms triggered specifically through engineered prompts?

**A:** Promptware.

---

## Card 40

**Q:** List the seven stages of the Promptware Kill Chain in order.

**A:** Initial Access, Privilege Escalation, Reconnaissance, Persistence, Command & Control, Lateral Movement, Actions on Objective.

---

## Card 41

**Q:** What is 'indirect prompt injection'?

**A:** An attack where poisoned content is retrieved from external sources by an LLM at inference time.

---

## Card 42

**Q:** What is the specific goal of the 'Privilege Escalation' stage in promptware?

**A:** Jailbreaking (bypassing safety constraints and alignment).

---

## Card 43

**Q:** In promptware, what is 'ASCII smuggling'?

**A:** Using Unicode characters that are interpreted by the LLM but not rendered visibly to the user.

---

## Card 44

**Q:** What is 'Retrieval-Independent Persistence' in promptware?

**A:** Poisoning the application's long-term memory so instructions influence all future interactions.

---

## Card 45

**Q:** Define 'Lateral Movement' within the context of an LLM ecosystem.

**A:** The propagation of promptware across different agents, users, applications, or systems.

---

## Card 46

**Q:** Which AI system incident is cited as the first demonstration of a five-stage promptware kill chain?

**A:** The Morris II worm (March 2024).

---

## Card 47

**Q:** What are the three preconditions for the 'Lethal Trifecta' of data exfiltration in LLMs?

**A:** Untrusted input, access to sensitive data, and the ability to communicate externally.

---

## Card 48

**Q:** According to Comet, what is 'prompt drift'?

**A:** Performance degradation over time without changes to the prompt, often due to model weight updates.

---

## Card 49

**Q:** How does 'spaced practice' improve durable technical fluency for AI Product Managers?

**A:** It strengthens neural pathways by forcing active memory reconstruction over increasing time intervals.

---

## Card 50

**Q:** What is the primary role of the Sprint Review in the era of AI-assisted development?

**A:** Shifting from a demo of built features to a decision session based on actual usage evidence.

---

## Card 51

**Q:** Why is 'model monoculture' considered a systemic macro-risk?

**A:** If competitors use the same foundational models, a single bias or error causes industry-wide synchronized failure.

---

## Card 52

**Q:** In agentic systems, what does 'frequency penalty' help to mitigate?

**A:** Repetitive thought loops where the agent outputs the same reasoning indefinitely.

---

## Card 53

**Q:** What differentiates 'monitoring guardrails' from 'blocking guardrails'?

**A:** Monitoring guardrails log violations for review; blocking guardrails prevent the response from reaching the user.

---

## Card 54

**Q:** In promptware, what is the 'Initial Access' phase?

**A:** The injection of malicious instructions into the context window of an LLM-based application.

---

## Card 55

**Q:** What occurs in 'cross-client lateral movement'?

**A:** Promptware propagates between different users of the same application via shared communication channels.

---

## Card 56

**Q:** How does 'delayed tool/agent invocation' evade the plan-then-execute mitigation?

**A:** It emits conditioned prompts to the orchestrator to be executed in a future inference.

---

## Card 57

**Q:** In the Iceberg Model, what layer includes the foundational assumptions that create the underlying structures?

**A:** Mental Models.

---

## Card 58

**Q:** What defines a 'systemic' AI product failure?

**A:** A failure caused by emergent properties and interaction of components rather than a discrete bug.

---

## Card 59

**Q:** Why is 'deletion' considered a core capability in the AI coding era?

**A:** Because AI makes code cheap to create, teams must explicitly remove code that does not earn its place.

---

## Card 60

**Q:** According to Source 1, what must happen before a problem has 'earned the right' to consume code?

**A:** The problem must be validated through user observation and testing of assumptions.

---

## Card 61

**Q:** What was the systemic cause of the Air Canada chatbot failure in 2024?

**A:** Epistemic uncertainty (the model did not know what it did not know and hallucinated policy).

---

## Card 62

**Q:** What is 'comprehension debt's' relationship to AI adoption according to Google's DORA report?

**A:** AI adoption amplifies existing organizational strengths and weaknesses rather than fixing broken systems.

---

## Card 63

**Q:** In RAG systems, what is 'Context Precision'?

**A:** A measure of the signal-to-noise ratio in the retrieved information context.

---

## Card 64

**Q:** Why is the SDK approach preferred for complex agentic systems over the proxy approach?

**A:** It captures internal variables and control flow decisions that never cross the network.

---

## Card 65

**Q:** What does a 'trace' represent in LLM observability?

**A:** A complete record of a single user interaction as it propagates through the system.

---

## Card 66

**Q:** How does 'LLM-as-a-judge' scale quality assessment?

**A:** It uses a highly capable model to evaluate the outputs of application models at high volumes.

---

## Card 67

**Q:** What is the primary objective of 'computational observability'?

**A:** To track the unit economics of AI, such as cost per session and token throughput.

---

## Card 68

**Q:** What risk is associated with 'cognitive offloading' in AI-assisted development?

**A:** The atrophy of critical thinking and out-of-the-box problem-solving skills.

---

## Card 69

**Q:** In systems thinking, what is the 'bullwhip effect'?

**A:** A phenomenon where small fluctuations in demand at the consumer level cause increasing swings at the supplier level.

---

## Card 70

**Q:** What is the '90/10 Rule' in probabilistic product judgment?

**A:** The requirement for rigorous Human-In-The-Loop (HITL) integration to manage edge cases.

---

## Card 71

**Q:** What occurs during the 'Reconnaissance' stage of the Promptware Kill Chain?

**A:** The prompt probes the host application's context to identify available assets and tools.

---

## Card 72

**Q:** In the context of promptware, what is 'ASCII smuggling'?

**A:** Using Unicode characters to hide instructions from users while making them visible to the LLM.

---

## Card 73

**Q:** What is the primary difference between direct and indirect prompt injection?

**A:** Direct comes from the user; indirect comes from external content retrieved by the system.

---

## Card 74

**Q:** What is the function of 'Command and Control' (C2) in a promptware attack?

**A:** It establishes a channel for remote payload updates and dynamic agent control.

---

## Card 75

**Q:** How does 'performativity' lead to content homogenization in AI systems?

**A:** Models ingest their own idiosyncrasies from the web as training data, amplifying synthetic quirks.

---
