# AI Flashcards

## Card 1

**Q:** What fundamental shift has occurred as technology moves from deterministic software to AI products?

**A:** The transition from specific inputs yielding identical outputs to probabilistic systems governed by weights and emergent behaviors.

---

## Card 2

**Q:** In Meadows' framework, what are 'leverage points'?

**A:** Places within a complex system where a small shift in one element can produce massive systemic changes.

---

## Card 3

**Q:** How do 'shallow' leverage points differ from 'deep' leverage points?

**A:** Shallow points involve parameters and buffer sizes, while deep points involve system design, rules, and overarching intent.

---

## Card 4

**Q:** What is the 'rebound effect' in AI energy efficiency optimizations?

**A:** Efficiency gains lower the cost of execution, paradoxically driving higher overall consumption and negating benefits.

---

## Card 5

**Q:** List the four layers of the Iceberg Model from surface to base.

**A:** Events, Patterns, Underlying Structures, and Mental Models.

---

## Card 6

**Q:** In the Iceberg Model, which layer represents the processes, workflows, and incentives that produce recurring trends?

**A:** Underlying Structures

---

## Card 7

**Q:** According to systemic analysis, what deepest layer drove the 2023 organizational turmoil at OpenAI?

**A:** Competing mental models regarding AI safety, speed, and profit.

---

## Card 8

**Q:** What describes Senge's 'Shifting the Burden' system archetype?

**A:** Applying a symptomatic quick fix that provides temporary relief but undermines the fundamental, long-term solution.

---

## Card 9

**Q:** In AI product management, how is 'prompt engineering' viewed through the 'Shifting the Burden' archetype?

**A:** It is a symptomatic fix that starves investment in building structured, tool-centric user interfaces.

---

## Card 10

**Q:** Which system archetype describes initial advantages compounding into systemic dominance and data flywheels?

**A:** Success to the Successful

---

## Card 11

**Q:** What constraint eventually stalls growth in the 'Limits to Success' archetype for AI model scaling?

**A:** Finite high-quality human training data and global energy/water limitations.

---

## Card 12

**Q:** What is the primary function of Causal Loop Diagrams (CLDs)?

**A:** To reveal dynamic interrelationships and circular causality rather than linear, sequential events.

---

## Card 13

**Q:** In stock-and-flow modeling, what do 'stocks' represent?

**A:** Accumulations within a system, such as accumulated training data or stakeholder trust.

---

## Card 14

**Q:** What is a 'data flywheel' in AI systems?

**A:** A recursive feedback loop where system usage generates data used to retrain and improve the underlying model.

---

## Card 15

**Q:** Define 'model drift' in machine learning.

**A:** The degradation of model performance occurring when the statistical properties of the environment change over time.

---

## Card 16

**Q:** What is the primary goal of Reinforcement Learning from Human Feedback (RLHF)?

**A:** To align Large Language Models with human expectations of politeness, helpfulness, and safety.

---

## Card 17

**Q:** In RLHF, what is 'reward hacking' (or specification gaming)?

**A:** An agent discovering unintended strategies to maximize its reward signal without achieving the intended objective.

---

## Card 18

**Q:** How does 'distribution shift' affect RLHF-aligned models in production?

**A:** Model performance degrades because the specialized deployment environment diverges from the original annotation environment.

---

## Card 19

**Q:** Term: Performativity

**A:** Definition: A state where the data used to train a model fundamentally depends on the actions of the model itself.

---

## Card 20

**Q:** What are 'degenerate feedback loops' in recommender systems?

**A:** Self-reinforcing cycles where system-driven exposure restricts future data collection, creating filter bubbles and echo chambers.

---

## Card 21

**Q:** Why is the digital content economy facing a 'Tragedy of the Commons' due to generative AI?

**A:** Individual actors optimize for volume by flooding the ecosystem with synthetic data, degrading the shared pool of training data.

---

## Card 22

**Q:** According to 2026 literature, how should AI Product Managers shift their primary focus?

**A:** From 'feature-thinking' (static backlogs) to 'system-thinking' (orchestrating continuously learning systems).

---

## Card 23

**Q:** What is a 'Management Flight Simulator' (MFS)?

**A:** A mathematically grounded simulated environment used to experiment with complex system dynamics and experience long-term consequences.

---

## Card 24

**Q:** Why is 'Spaced Practice' recommended for AI PM curriculum design?

**A:** It strengthens neural pathways and move technical fluency into long-term memory by distributing learning over time.

---

## Card 25

**Q:** What caused the systemic collapse of the Zillow Offers iBuying program?

**A:** The failure to account for concept drift and adverse selection when scaling an automated algorithm into a volatile housing market.

---

## Card 26

**Q:** In AI failures like Air Canada's chatbot, what is 'epistemic uncertainty'?

**A:** The failure of a model to know 'what it does not know,' leading to authoritative hallucinations of non-existent policies.

---

## Card 27

**Q:** What was the structural cause of the Knight Capital trading disaster?

**A:** A lack of 'runtime awareness' in an open-loop automated system that executed millions of erroneous trades.

---

## Card 28

**Q:** Define the 'Verification Tax' in AI product management.

**A:** The extensive human labor required to audit and verify probabilistic outputs, which can negate the ROI of automation.

---

## Card 29

**Q:** How does 'Cognitive Offloading' pose a risk to organizational resilience?

**A:** Over-reliance on AI assistants can cause developers and managers to lose the ability to reason deeply about complex problems.

---

## Card 30

**Q:** What is 'Model Monoculture Risk'?

**A:** The danger that industry-wide reliance on the same foundational models will cause simultaneous, synchronized industry failures.

---

## Card 31

**Q:** In the AI PM Competency Map, what is the '90/10 Rule'?

**A:** The practice of establishing rigorous Human-In-The-Loop (HITL) integration to manage probabilistic judgment.

---

## Card 32

**Q:** What distinguishes 'Strong Degeneracy' from 'Weak Degeneracy' in feedback loop models?

**A:** Strong degeneracy implies the drift from the initial state approaches infinity almost surely as $t \to \infty$.

---

## Card 33

**Q:** How do 'exposure-aware' modeling techniques mitigate degenerate loops?

**A:** By conditioning preference inference on actual presentations to prevent unfair penalization of unexposed items.

---

## Card 34

**Q:** In the RLHF pipeline, what is the purpose of Supervised Fine-Tuning (SFT)?

**A:** To train the base model to imitate high-quality human demonstrations or instruction-following behaviors.

---

## Card 35

**Q:** What is the purpose of the 'KL-divergence penalty' in RLHF reinforcement learning?

**A:** To act as a tether that prevents the model from generating unusual text just to boost reward scores (preventing over-optimization).

---

## Card 36

**Q:** Give an example of 'Sycophancy' in Large Language Models.

**A:** A model wrongly admitting a mistake or matching a user's biased feedback because human preference data rewards agreement.

---

## Card 37

**Q:** Term: Bradley-Terry (BT) Model

**A:** Definition: A random utility model using a sigmoid link function to distill pairwise preference rankings into scalar rewards.

---

## Card 38

**Q:** What does the 'mixed-pair bias statistic' ($B_F(x)$) measure in reward learning?

**A:** The average implied score difference (log-odds tilt) required to explain mixed-pair win probabilities in human feedback.

---

## Card 39

**Q:** How does 'Constitutional AI' attempt to mitigate reward hacking?

**A:** By replacing direct human rewards with explicit, rule-based principles and AI-driven critiques to enforce them.

---

## Card 40

**Q:** In the Iceberg Model, what layer is most organizations' primary focus when reacting to customer complaints?

**A:** The Events layer

---

## Card 41

**Q:** Why do analysts recommend deep-leverage interventions for AI sustainability?

**A:** To ensure optimizations operate within environmental boundaries rather than merely accelerating consumption.

---

## Card 42

**Q:** What is the 'Algorithmic Core' of an organization?

**A:** The recursive data flywheels that fuel market dominance in AI-driven sectors.

---

## Card 43

**Q:** In multi-agent systems, what does 'RepuNet' aim to accomplish?

**A:** Counteracting the 'Tragedy of the Commons' through multi-agent reputation networks and collective accountability.

---

## Card 44

**Q:** What is 'Aleatoric Uncertainty'?

**A:** Uncertainty regarding whether a model is 'wrong' based on random variability in the data (as opposed to missing knowledge).

---

## Card 45

**Q:** Why is 'Diagnosis Over Delivery' a critical PM competency for AI?

**A:** The PM must diagnose the exact gap between system state and user intent before applying a fix to a probabilistic model.

---

## Card 46

**Q:** In the Best-of-$N$ mechanism, what does $N$ represent?

**A:** The number of candidate responses sampled from the base policy to be ranked by the reward model.

---

## Card 47

**Q:** How does 'author-coupled labeling' impact sycophancy in RLHF?

**A:** It increases sycophancy because the rater likely favors responses that match their own stated beliefs or prompt stance.

---

## Card 48

**Q:** What is 'Reward Shaping'?

**A:** Adding explicit penalty or heuristic terms (like length penalties) to a learned reward model to steer model behavior.

---

## Card 49

**Q:** Define 'Interleaving' in pedagogical design.

**A:** Mixing different topics together to force contextual recognition, resulting in more durable technical fluency.

---

## Card 50

**Q:** Which AI failure involved a chatbot advising business owners to break labor laws?

**A:** New York City's 'MyCity' chatbot

---

## Card 51

**Q:** What is the 'B1 loop' in the Taiwanese smart medical device ecosystem mapping?

**A:** The balancing loops created by clinical validation bottlenecks and siloed knowledge.

---

## Card 52

**Q:** In RLHF, what is the role of the 'Sigmoid' function in the reward model loss?

**A:** It maps the difference between rewards of two completions to a probability of one being preferred over the other.

---

## Card 53

**Q:** What is 'Reward Over-optimization'?

**A:** The policy discovering bizarre activation patterns that fool a reward model's internals while providing no actual value.

---

## Card 54

**Q:** How do 'reasoning flywheels' operate in multi-agent ecosystems?

**A:** They automatically generate synthetic tasks by learning from errors to expand the system's decision-tree complexity.

---

## Card 55

**Q:** In formal degeneracy definitions, what does the variable $\mu_t$ represent?

**A:** The user's latent interest vector at time $t$.

---

## Card 56

**Q:** What describes the 'Filter Bubble' effect in recommender systems?

**A:** A policy recurrently sampling a constrained subset of items irrespective of user dynamics.

---

## Card 57

**Q:** What role do 'Intermediary Organizations' play in AI systems mapping?

**A:** They bridge the translational gap between laboratory research and real-world application.

---

## Card 58

**Q:** What is the 'Sup-norm' used for in degeneracy models?

**A:** To quantify drift when dealing with infinite sets of items.

---

## Card 59

**Q:** What is 'Specification Gaming'?

**A:** Exploiting flaws in a reward signal to achieve high proxy rewards without meeting the true goal.

---

## Card 60

**Q:** Which training stage in LLMs is most likely to introduce style biases like 'over-politeness'?

**A:** Supervised Fine-Tuning (SFT)

---

## Card 61

**Q:** What describes the 'Advantages' ($\hat{A}$) in the PPO update step?

**A:** The estimate of how much better a specific action is compared to the average behavior of the current policy.

---

## Card 62

**Q:** What is 'Length Hacking'?

**A:** A common form of reward hacking where models generate excessively long tokens to appear more detailed.

---

## Card 63

**Q:** In the context of the Zillow failure, what is 'Adverse Selection'?

**A:** When sellers with defective or overpriced properties accept automated offers while premium property owners seek higher open-market prices.

---

## Card 64

**Q:** How does the 'Verification Tax' affect AI scalability?

**A:** If verification costs exceed the cost of human generation, the AI system destroys rather than creates value.

---

## Card 65

**Q:** What is the core objective of the 'System & Flow Architecture' competency?

**A:** To shift from linear feature roadmaps to circular, continuously learning systems.

---
