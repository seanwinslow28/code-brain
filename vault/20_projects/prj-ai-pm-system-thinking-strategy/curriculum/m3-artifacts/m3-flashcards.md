# Systems Flashcards

## Card 1

**Q:** In a Systems Thinking context, how is a 'Stock' defined?

**A:** An accumulation of information or material over a period of time.

---

## Card 2

**Q:** In the FinOps socio-technical system, what specific entity is considered the 'Stock'?

**A:** The cost of the cloud.

---

## Card 3

**Q:** According to Donella Meadows, what is the least effective place to intervene in a system?

**A:** Constants and parameters (setting targets).

---

## Card 4

**Q:** In cloud cost management, what is the primary purpose of 'Buffers' as a leverage point?

**A:** Increasing the system's capacity to handle changes in in-flows and out-flows.

---

## Card 5

**Q:** What is the result of 'Delays' in a system relative to the rate of system change?

**A:** They create oscillations between the desired target and the actual state.

---

## Card 6

**Q:** What are the three components required for a functioning 'Balancing Feedback Loop'?

**A:** A goal, an observer to check for deviations, and a response act.

---

## Card 7

**Q:** How does a 'Vicious Cycle' manifest in cloud resource provisioning during a DDoS attack?

**A:** Attack traffic triggers auto-provisioning of resources, which invites more traffic, leading to exponential billing.

---

## Card 8

**Q:** In the 'Social Design' category of leverage points, what does 'Information Flows' refer to?

**A:** Cascading feedback information to the specific people who can act on it immediately.

---

## Card 9

**Q:** What is considered a higher leverage intervention than feedback loops or self-organization?

**A:** The goals of the system.

---

## Card 10

**Q:** According to the InfoQ article, what is the 'North Star' for optimization initiatives in cloud consumption?

**A:** Unit cost metrics (Unit Economics), such as cost per parcel processed.

---

## Card 11

**Q:** What is the highest leverage point proposed by Donella Meadows?

**A:** Transcending paradigms (looking beyond the current mindset).

---

## Card 12

**Q:** The 'Iceberg Model' layers include Events, Patterns, Underlying Structures, and _____.

**A:** Mental Models

---

## Card 13

**Q:** Which layer of the Iceberg Model represents the foundational beliefs that create system structures?

**A:** Mental Models

---

## Card 14

**Q:** Senge's 'Shifting the Burden' archetype occurs when a _____ provides temporary relief but carries side effects that undermine long-term solutions.

**A:** Symptomatic quick fix

---

## Card 15

**Q:** In AI development, the 'Success to the Successful' archetype creates an insurmountable _____ that cements competitive advantage.

**A:** Data flywheel

---

## Card 16

**Q:** What systemic risk arises when AI models are trained on synthetic, machine-generated data?

**A:** Model collapse (loss of authenticity and proliferation of misinformation).

---

## Card 17

**Q:** Term: Performativity

**A:** Definition: A state where the data used to train a model depends fundamentally on the prior actions of that same model.

---

## Card 18

**Q:** How do 'Degenerate Feedback Loops' affect content diversity in recommender systems?

**A:** They collapse diversity by reinforcing existing preferences, creating filter bubbles.

---

## Card 19

**Q:** What is 'Reward Hacking' in the context of Reinforcement Learning from Human Feedback (RLHF)?

**A:** The AI agent maximizing its reward signal through unintended strategies like sycophancy without achieving the actual goal.

---

## Card 20

**Q:** Concept: Concept Drift

**A:** Definition: A decline in model performance occurring when the statistical properties of the target variable or environment change over time.

---

## Card 21

**Q:** What systemic failure led to the collapse of 'Zillow Offers' in 2021?

**A:** Concept drift in housing markets combined with a lack of Human-In-The-Loop (HITL) verification.

---

## Card 22

**Q:** The Air Canada chatbot incident proved that companies are _____ for the fabricated outputs of their automated systems.

**A:** Legally liable

---

## Card 23

**Q:** What is 'Epistemic Uncertainty' in AI models?

**A:** A situation where a model confidently hallucinates because it does not know that it lacks the required grounding data.

---

## Card 24

**Q:** Why is the 2012 Knight Capital disaster relevant to modern agentic AI?

**A:** It illustrates the dangers of 'open-loop' automation where a system lacks runtime awareness of its own catastrophic behavior.

---

## Card 25

**Q:** The 'Rebound Effect' in Meadows' leverage points describes how efficiency gains paradoxically lead to _____.

**A:** Higher overall consumption and resource extraction.

---

## Card 26

**Q:** What is the primary objective of 'LLM Model Routing'?

**A:** Sending each request to the cheapest model capable of handling it to minimize costs.

---

## Card 27

**Q:** According to 2026 data, what is the approximate price spread between the cheapest and most capable LLMs?

**A:** Roughly $100\times$.

---

## Card 28

**Q:** What is the reported cost-saving range for teams implementing a tuned routing layer?

**A:** 40% to 85%

---

## Card 29

**Q:** Which peer-reviewed work demonstrated 85% cost savings while maintaining 95% of GPT-4 quality?

**A:** RouteLLM (ICLR 2025)

---

## Card 30

**Q:** How does 'Rule-based routing' compare to 'ML-classifier routing' in terms of latency overhead?

**A:** Rule-based adds $< 1$ ms, while ML-classifiers add $50$-$100$ ms.

---

## Card 31

**Q:** What is the 'Silent Quality Regression' risk in LLM routing?

**A:** Cost is reduced, but subtle drops in answer quality occur that are only discovered via delayed customer feedback.

---

## Card 32

**Q:** What mitigation strategy is recommended to claim routing savings safely?

**A:** A pre-merge CI eval gate running $50$-$500$ representative cases.

---

## Card 33

**Q:** Which tool is best for self-hosted LLM proxying with budgets and Redis-based rate limiting?

**A:** LiteLLM

---

## Card 34

**Q:** In the AI Product Management triangle, what are the three competing variables?

**A:** Quality, Latency, and Cost.

---

## Card 35

**Q:** Term: Verification Tax

**A:** Definition: The hidden cost of human labor required to audit and verify probabilistic AI outputs.

---

## Card 36

**Q:** What metric should AI PMs use instead of 'cost per output' to account for audit labor?

**A:** Cost per verified-good-output ($\$/verified-good-output$).

---

## Card 37

**Q:** How does 'Semantic Caching' break the spend flow in AI systems?

**A:** By returning stored answers for similar queries, removing the need for a new model call.

---

## Card 38

**Q:** In the context of 'Latency Budgets,' what is the risk of the 'Latency-Quality Death Spiral'?

**A:** Adding verification passes slows responses, causing users to abandon, which results in less feedback and stalled quality.

---

## Card 39

**Q:** What is 'Cognitive Offloading' as a systemic risk in AI-augmented engineering?

**A:** The atrophy of critical thinking and reasoning skills when humans over-rely on AI for output generation.

---

## Card 40

**Q:** Which pedagogical approach uses digital laboratories to compress time for practicing systemic decisions?

**A:** Management Flight Simulators (MFS)

---

## Card 41

**Q:** According to cognitive science, what learning technique involves distributing retrieval practice over increasing intervals?

**A:** Spaced Practice (or Spaced Repetition)

---

## Card 42

**Q:** What is 'Model Monoculture Risk' in the AI industry?

**A:** The risk that synchronized failures occur across an industry because everyone uses the same foundational model APIs.

---

## Card 43

**Q:** In the 'Limits to Success' archetype, what are the primary balancing constraints for AI model scaling?

**A:** Finite high-quality training data and global energy/water limitations.

---

## Card 44

**Q:** What leverage point involves changing standards, guidelines, and hosting policies?

**A:** Rules (Social Design)

---

## Card 45

**Q:** How does 'Self-Organization' function as a high leverage point?

**A:** It empowers the system to evolve its own rules, physical structures, and information flows.

---

## Card 46

**Q:** What is the 'Algorithmic Core' in market-dominant AI organizations?

**A:** A dynamic center fueled by recursive data flywheels.

---

## Card 47

**Q:** In Multi-Agent systems, what game-theoretic strategy leads to the 'Tragedy of the Commons' in the content economy?

**A:** Actors optimizing for volume by flooding the ecosystem with low-cost synthetic content.

---

## Card 48

**Q:** Which AI routing tool is specifically noted for 'ML quality-aware routing' based on preference data?

**A:** NotDiamond

---

## Card 49

**Q:** A cost cap that silently drops work is problematic because it converts a cost problem into a _____.

**A:** Trust problem

---

## Card 50

**Q:** In stock-and-flow diagrams for AI PMs, what is usually modeled as the 'Stock' for feature development?

**A:** Budget or team capacity.

---

## Card 51

**Q:** What is 'Graceful Degradation' in a cost-capped AI system?

**A:** The system continuing to function through fallback models, queued work, or clear error messages when the budget is hit.

---

## Card 52

**Q:** Why is 'Diagnosis over Delivery' a critical competency for AI PMs?

**A:** It requires identifying the exact gap between system state and user intent before applying a probabilistic fix.

---

## Card 53

**Q:** In the InfoQ FinOps framework, what determines the structure of accountability among teams?

**A:** Stock-and-flow structures.

---

## Card 54

**Q:** What is the primary benefit of 'Streaming' in LLM responses?

**A:** It improves perceived latency for the user without changing actual inference time.

---

## Card 55

**Q:** Under Meadows' leverage points, which intervention is most likely to face the highest resistance to change?

**A:** Paradigms or Mental Models (highest effectiveness).

---

## Card 56

**Q:** What is the 'Verification Tax's' impact on the 'Zero Marginal Cost' theory of AI?

**A:** It debunkes the theory by showing that human audit labor grows linearly with high-stakes output adoption.

---
