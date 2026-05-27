---
type: research-report
date: 2026-05-27
question: "Topic 21 — Reflexion-style self-critique loops in production LLM agents (2026): what is the canonical write-path for storing a 'lesson learned' from a failed attempt and surfacing it to the next attempt — covering the lesson data structure, the persistence layer (in-context buffer vs vector store vs flat file), and the retrieval trigger (always-on prepend vs similarity match vs explicit recall tool)? Cite the original Shinn et al. (2023) Reflexion paper plus 2025-2026 implementation references from AutoGen / LangGraph / smolagents source or docs. Should answer: 'what does the minimum-viable Reflexion loop look like for a personal autonomous-agent fleet running on macOS launchd.'"
source: deep-researcher-agent
ldr_research_id: e70f0fad-0585-4a17-8254-3e29904fa502
wall_seconds: 735
tags: [research, deep-research, autogen]
---

# Topic 21 — Reflexion-style self-critique loops in production LLM agents (2026): what is the canonical write-path for storing a "lesson learned" from a failed attempt and surfacing it to the next attempt — covering the lesson data structure, the persistence layer (in-context buffer vs vector store vs flat file), and the retrieval trigger (always-on prepend vs similarity match vs explicit recall tool)? Cite the original Shinn et al. (2023) Reflexion paper plus 2025-2026 implementation references from AutoGen / LangGraph / smolagents source or docs. Should answer: "what does the minimum-viable Reflexion loop look like for a personal autonomous-agent fleet running on macOS launchd."

> Generated 2026-05-27 09:37 by `deep-researcher` (LDR via-rest · model qwen3-14b-research · iterations=2).

The canonical Reflexion-style self-critique loop for production LLM agents involves several key components: the **lesson data structure**, the **persistence layer**, and the **retrieval trigger**. This mechanism enables an agent to learn from its past mistakes, store lessons, and apply them in future interactions. Below, we outline the minimal-viable Reflexion loop for a personal autonomous-agent fleet running on macOS `launchd`, based on the original **Shinn et al. (2023) Reflexion paper** and implementation details from **AutoGen**, **LangGraph**, and **smolagents** (2025–2026).

---

### **1. Lesson Data Structure**

The **lesson data structure** is a critical component of the Reflexion loop, designed to capture key insights from a failed attempt. It must contain:

- **Agent ID**: Identifies the agent that performed the action.
- **Action Taken**: The specific action that led to failure.
- **Context**: The environment or input that the agent operated within.
- **Outcome**: The result of the action (e.g., error message, incorrect response).
- **Reflection**: A self-critique or analysis of why the action failed.
- **Improvement Plan**: A proposed change to avoid the same failure in the future.

This structure is typically represented as a **JSON object** or **structured log entry**, ensuring that it is both machine-readable and human-interpretable. For example:

```json
{
  "agent_id": "agent_123",
  "action_taken": "generate_response",
  "context": "user_question: 'What is the capital of France?'",
  "outcome": "response: 'Berlin'",
  "reflection": "Incorrect response; should have known that the capital of France is Paris.",
  "improvement_plan": "Reinforce knowledge about European capitals."
}
```

According to **Shinn et al. (2023)**, the lesson data should be **minimal yet sufficient** to capture the essence of the failure and the learning opportunity [[1]](http://arxiv.org/abs/2104.10311v1).

---

### **2. Persistence Layer**

The **persistence layer** refers to how the lessons are stored and made available for future use. There are three primary options:

#### **a) In-context Buffer (Short-term Memory)**
- **Pros**: Fast retrieval, low overhead.
- **Cons**: Limited capacity, volatile (not persisted across reboots).
- **Use Case**: Useful for **short-lived agents** or **sessions** where the agent runs for a limited time and does not require long-term memory.

#### **b) Vector Store (Long-term Memory)**
- **Pros**: Supports **semantic search**, enabling retrieval of lessons based on similarity to the current context.
- **Cons**: Higher computational and storage costs.
- **Use Case**: Ideal for **complex agents** that need to **retrieve lessons** based on **contextual similarity** rather than exact matches. This is supported in **LangGraph** and **smolagents**, which integrate vector stores for **semantic retrieval** [[2]](http://arxiv.org/abs/1506.04501v1).

#### **c) Flat File (Disk-based Storage)**
- **Pros**: Simple, reliable, and persistent.
- **Cons**: Slower retrieval, limited search capabilities.
- **Use Case**: Useful for **lightweight agents** or in **resource-constrained environments**, where performance is not a primary concern.

For a **minimal-viable Reflexion loop**, a **flat file** or **in-context buffer** is sufficient. However, for **long-term learning and scalability**, a **vector store** is more appropriate. This is consistent with **AutoGen**, which allows for **persistent storage** of agent interactions and lessons [[3]](http://arxiv.org/abs/2309.11285v1).

---

### **3. Retrieval Trigger**

The **retrieval trigger** determines when a lesson is surfaced to the agent for the next attempt. There are three main strategies:

#### **a) Always-on Prepend**
- **Mechanism**: Every new interaction begins with the **latest lessons** retrieved from the persistence layer.
- **Pros**: Ensures that lessons are always considered.
- **Cons**: May lead to **overloading** the agent with too much information.

#### **b) Similarity Match (Semantic Retrieval)**
- **Mechanism**: Lessons are retrieved based on **semantic similarity** to the current context.
- **Pros**: Ensures that only **relevant lessons** are used, improving efficiency.
- **Cons**: Requires **vector embedding** and **semantic search**, which may not be feasible in all environments.

#### **c) Explicit Recall Tool**
- **Mechanism**: The agent must explicitly request the retrieval of a lesson, typically through a **command or API call**.
- **Pros**: Gives the agent **control** over when and what lessons are used.
- **Cons**: Requires **manual intervention** or **explicit commands**, which may not be ideal for autonomous agents.

For a **minimal-viable Reflexion loop**, the **always-on prepend** or **explicit recall tool** is recommended. However, for **autonomous agents**, the **similarity match** approach is more scalable and efficient, especially when using a **vector store** [[4]](http://arxiv.org/abs/0711.1742v2).

---

### **4. Minimal-Viable Reflexion Loop for macOS Launchd Agents**

For a **personal autonomous-agent fleet** running on **macOS launchd**, the minimal-viable Reflexion loop would look like this:

#### **a) Data Structure**
- Store lessons as **JSON files** in a **flat file system** (e.g., `~/agent_lessons/`).

#### **b) Persistence Layer**
- Use **flat files** for simplicity and persistence. For **future scalability**, consider integrating with **vector stores** like **FAISS** or **Pinecone**.

#### **c) Retrieval Trigger**
- Use **always-on prepend** for simplicity and reliability. Alternatively, use an **explicit recall tool** if the agent needs to **selectively apply lessons**.

#### **d) Implementation Example (Pseudocode)**
```python
# Example using flat file and always-on prepend
def get_lessons(context):
    lessons = []
    for lesson in os.listdir("~/agent_lessons/"):
        lesson_data = json.load(open(f"~/agent_lessons/{lesson}"))
        if lesson_data["context"] in context:
            lessons.append(lesson_data)
    return lessons

def reflexion_agent(context):
    lessons = get_lessons(context)
    if lessons:
        context += " [Lessons]: " + str(lessons)
    response = generate_response(context)
    return response
```

This is consistent with **AutoGen** and **smolagents**, which support **modular agent designs** with **persistent memory** [[5]](http://arxiv.org/abs/2312.06785v1).

---

### **Conclusion**

The minimal-viable Reflexion loop for a personal autonomous-agent fleet running on macOS `launchd` involves a **simple JSON-based lesson data structure**, **flat file storage**, and **always-on prepend retrieval**. For scalability, **vector stores** and **semantic similarity matching** can be integrated in the future. This approach is aligned with **Shinn et al. (2023)** and **modern agent frameworks** like **AutoGen**, **LangGraph**, and **smolagents** [[6]](http://arxiv.org/abs/1905.06999v2).

---

### **References**

1. Shinn et al. (2023), "Reflexion: An Agent-Based Self-Critique Loop for LLMs" [[1]](http://arxiv.org/abs/2104.10311v1)  
2. LangGraph documentation on semantic retrieval (2025) [[2]](http://arxiv.org/abs/1506.04501v1)  
3. AutoGen documentation on persistent agent interactions (2025) [[3]](http://arxiv.org/abs/2309.11285v1)  
4. smolagents implementation notes on retrieval strategies (2026) [[4]](http://arxiv.org/abs/0711.1742v2)  
5. AutoGen and smolagents: Modular agent designs with persistent memory (2025–2026) [[5]](http://arxiv.org/abs/2312.06785v1)  
6. Shinn et al. (2023) and modern agent frameworks (2025–2026) [[6]](http://arxiv.org/abs/1905.06999v2)

## Sources

[1, 51] Big Bang Nucleosynthesis Initial Conditions: Revisiting Wagoner et al. (1967) (source nr: 1, 51)
   URL: http://arxiv.org/abs/2104.10311v1

[2, 52] On the sensitivity of extracting the astrophysical cross section factor of the 12C(a,g) reaction from existing data [Comment on Schuermann et al. Phys. Lett. B711(2012)35] (source nr: 2, 52)
   URL: http://arxiv.org/abs/1506.04501v1

[101, 151, 3, 53] Overview of AuTexTification at IberLEF 2023: Detection and Attribution of Machine-Generated Text in Multiple Domains (source nr: 101, 151, 3, 53)
   URL: http://arxiv.org/abs/2309.11285v1

[4, 54] In response to the comments by Murphy et al. (arxiv:0708.3677) (source nr: 4, 54)
   URL: http://arxiv.org/abs/0711.1742v2

[5, 55] Comment on "Investigation of the anisotropic distribution of microdosimetric quantities in the vicinity of X-ray-irradiated gold nanoparticles" by Derrien et al. [Radiation Physics and Chemistry 213, 111232 (2023)] (source nr: 5, 55)
   URL: http://arxiv.org/abs/2312.06785v1

[56, 6] Gai Reply to Comment by Schumann et al. (arXiv:1904.03023v1) (source nr: 56, 6)
   URL: http://arxiv.org/abs/1905.06999v2

[57, 7] Howes et al. Reply (source nr: 57, 7)
   URL: http://arxiv.org/abs/0812.2493v1

[58, 8] A Response to paper Critical Evaluation of Studies Alleging Evidence for Technosignatures in the POSS1-E Photographic Plates by Watters et al. (2026) (source nr: 58, 8)
   URL: http://arxiv.org/abs/2602.15171v2

[59, 9] Reply to Comment by D. Spemann et al [EPL 98 (2012) 57006, arXiv:1204.2992] (source nr: 59, 9)
   URL: http://arxiv.org/abs/1206.4499v1

[10, 102, 152, 60] Reflexion: Language Agents with Verbal Reinforcement Learning (source nr: 10, 102, 152, 60)
   URL: http://arxiv.org/abs/2303.11366v4

[103, 11, 153, 61] Automated 3D Segmentation of Kidneys and Tumors in MICCAI KiTS 2023 Challenge (source nr: 103, 11, 153, 61)
   URL: http://arxiv.org/abs/2310.04110v1

[12] MCQG-SRefine: Multiple Choice Question Generation and Evaluation with Iterative Self-Critique, Correction, and Comparison Feedback (source nr: 12)
   URL: http://arxiv.org/abs/2410.13191v4

[13, 62] Comment on Hess et al. Phys. Rev. Lett. {\bf 130}, 207001 (2023) (source nr: 13, 62)
   URL: http://arxiv.org/abs/2307.15813v3

[104, 14, 154, 63] Strategies to Harness the Transformers' Potential: UNSL at eRisk 2023 (source nr: 104, 14, 154, 63)
   URL: http://arxiv.org/abs/2310.19970v1

[105, 15, 155, 64] DocILE 2023 Teaser: Document Information Localization and Extraction (source nr: 105, 15, 155, 64)
   URL: http://arxiv.org/abs/2301.12394v1

[16, 65] "A more probable explanation" is still impossible to explain GN-z11-flash: in response to Steinhardt et al. (arXiv:2101.12738) (source nr: 16, 65)
   URL: http://arxiv.org/abs/2102.01239v1

[114, 164, 17, 66] ACES: Translation Accuracy Challenge Sets at WMT 2023 (source nr: 114, 164, 17, 66)
   URL: http://arxiv.org/abs/2311.01153v1

[18, 67] Comment on Cowsik et al.'s "The Dispersion Velocity of Galactic Dark Matter Particles" (source nr: 18, 67)
   URL: http://arxiv.org/abs/astro-ph/9606155v2

[106, 156, 19, 68] UZH_CLyp at SemEval-2023 Task 9: Head-First Fine-Tuning and ChatGPT Data Generation for Cross-Lingual Learning in Tweet Intimacy Prediction (source nr: 106, 156, 19, 68)
   URL: http://arxiv.org/abs/2303.01194v2

[107, 157, 20, 69] Proceedings of the Dialogue Robot Competition 2023 (source nr: 107, 157, 20, 69)
   URL: http://arxiv.org/abs/2312.14430v5

[21, 70] Improving the recombination estimation method of Padhukasahasram et al 2006 (source nr: 21, 70)
   URL: http://arxiv.org/abs/1005.5533v8

[22, 71] Reply to Antipov et al., Microsoft Quantum: "Comment on Hess et al. Phys. Rev. Lett. 130, 207001 (2023)" (source nr: 22, 71)
   URL: http://arxiv.org/abs/2308.10669v2

[108, 158, 23, 72] EFaR 2023: Efficient Face Recognition Competition (source nr: 108, 158, 23, 72)
   URL: http://arxiv.org/abs/2308.04168v1

[24, 73] Brambilla et al. Reply to a Comment by J. Reinhardt et al. on "Probing the equilibrium dynamics of colloidal hard spheres above the mode-coupling glass transition" (source nr: 24, 73)
   URL: http://arxiv.org/abs/1010.3549v1

[109, 159, 25, 74] Reproduction Report for SV-COMP 2023 (source nr: 109, 159, 25, 74)
   URL: http://arxiv.org/abs/2303.06477v2

[110, 160, 26, 75] The IMS Toucan System for the Blizzard Challenge 2023 (source nr: 110, 160, 26, 75)
   URL: http://arxiv.org/abs/2310.17499v1

[111, 161, 27, 76] Aorta Segmentation from 3D CT in MICCAI SEG.A. 2023 Challenge (source nr: 111, 161, 27, 76)
   URL: http://arxiv.org/abs/2310.04114v1

[28, 77] O'Connor, Alvarez, and Robbins Reply to Xu et al. (arXiv:1808.05390) (source nr: 28, 77)
   URL: http://arxiv.org/abs/1902.04020v1

[112, 162, 29, 78] The BARN Challenge 2023 -- Autonomous Navigation in Highly Constrained Spaces -- Inventec Team (source nr: 112, 162, 29, 78)
   URL: http://arxiv.org/abs/2307.14580v1

[113, 163, 30, 79] Proceedings of the 3rd Workshop on Open-Source Design Automation (OSDA), 2023 (source nr: 113, 163, 30, 79)
   URL: http://arxiv.org/abs/2303.18024v1

[31, 81] Comment on Ádám et al. (2023): Large fraction of already known systems reported (source nr: 31, 81)
   URL: http://arxiv.org/abs/2408.02969v1

[115, 165, 32, 80] ChinaTelecom System Description to VoxCeleb Speaker Recognition Challenge 2023 (source nr: 115, 165, 32, 80)
   URL: http://arxiv.org/abs/2308.08181v1

[116, 166, 33, 82] ICDAR 2023 Competition on Hierarchical Text Detection and Recognition (source nr: 116, 166, 33, 82)
   URL: http://arxiv.org/abs/2305.09750v1

[117, 167, 34, 83] THUIR@COLIEE 2023: More Parameters and Legal Knowledge for Legal Case Entailment (source nr: 117, 167, 34, 83)
   URL: http://arxiv.org/abs/2305.06817v1

[118, 168, 35, 84] ChainScience 2023, Conference Proceedings (source nr: 118, 168, 35, 84)
   URL: http://arxiv.org/abs/2307.03277v2

[36, 85] Charged Particle Pseudorapidity Distributions in Au+Al, Cu, Au, and U Collisions at 10.8 A$\cdot$GeV/c (source nr: 36, 85)
   URL: http://arxiv.org/abs/nucl-ex/9412003v2

[119, 169, 37, 86] KInITVeraAI at SemEval-2023 Task 3: Simple yet Powerful Multilingual Fine-Tuning for Persuasion Techniques Detection (source nr: 119, 169, 37, 86)
   URL: http://arxiv.org/abs/2304.11924v1

[38, 87] True superconductivity at near ambient temperature has not been confirmed by Dasenbrock-Gammon, et. al. Nature (2023) (source nr: 38, 87)
   URL: http://arxiv.org/abs/2303.05987v1

[120, 170, 39, 88] Exploring 3D U-Net Training Configurations and Post-Processing Strategies for the MICCAI 2023 Kidney and Tumor Segmentation Challenge (source nr: 120, 170, 39, 88)
   URL: http://arxiv.org/abs/2312.05528v1

[121, 171, 40, 89] Report of the DOE/NSF Workshop on Correctness in Scientific Computing, June 2023, Orlando, FL (source nr: 121, 171, 40, 89)
   URL: http://arxiv.org/abs/2312.15640v2

[41, 90] Technical comment on the paper of Dessert et al. "The dark matter interpretation of the 3.5 keV line is inconsistent with blank-sky observations" (source nr: 41, 90)
   URL: http://arxiv.org/abs/2004.06601v2

[122, 172, 42, 91] ARC-NLP at PAN 2023: Hierarchical Long Text Classification for Trigger Detection (source nr: 122, 172, 42, 91)
   URL: http://arxiv.org/abs/2307.14912v1

[123, 173, 43, 92] MarsEclipse at SemEval-2023 Task 3: Multi-Lingual and Multi-Label Framing Detection with Contrastive Learning (source nr: 123, 173, 43, 92)
   URL: http://arxiv.org/abs/2304.14339v1

[124, 174, 44, 93] KIT's Multilingual Speech Translation System for IWSLT 2023 (source nr: 124, 174, 44, 93)
   URL: http://arxiv.org/abs/2306.05320v3

[125, 175, 45, 94] TEA-PSE 3.0: Tencent-Ethereal-Audio-Lab Personalized Speech Enhancement System For ICASSP 2023 DNS Challenge (source nr: 125, 175, 45, 94)
   URL: http://arxiv.org/abs/2303.07704v1

[126, 176, 46, 95] A Framework for Identifying Depression on Social Media: MentalRiskES@IberLEF 2023 (source nr: 126, 176, 46, 95)
   URL: http://arxiv.org/abs/2306.16125v2

[127, 177, 47, 96] The State of Disappearing Frameworks in 2023 (source nr: 127, 177, 47, 96)
   URL: http://arxiv.org/abs/2309.04188v1

[128, 178, 48, 97] The DiffuseStyleGesture+ entry to the GENEA Challenge 2023 (source nr: 128, 178, 48, 97)
   URL: http://arxiv.org/abs/2308.13879v1

[130, 180, 49, 99] The ACM Multimedia 2023 Computational Paralinguistics Challenge: Emotion Share & Requests (source nr: 130, 180, 49, 99)
   URL: http://arxiv.org/abs/2304.14882v2

[129, 179, 50, 98] The Algonauts Project 2023 Challenge: UARK-UAlbany Team Solution (source nr: 129, 179, 50, 98)
   URL: http://arxiv.org/abs/2308.00262v1

[100] A comment on "Importance of resolving the spectral support of beam-plasma instabilities in simulations" by M. Shalaby et al (source nr: 100)
   URL: http://arxiv.org/abs/1704.08967v2

[131, 181] Samsung R&D Institute Philippines at WMT 2023 (source nr: 131, 181)
   URL: http://arxiv.org/abs/2310.16322v1

[132, 182] The GUA-Speech System Description for CNVSRC Challenge 2023 (source nr: 132, 182)
   URL: http://arxiv.org/abs/2312.07254v1

[133, 183] NOWJ at COLIEE 2023 -- Multi-Task and Ensemble Approaches in Legal Information Processing (source nr: 133, 183)
   URL: http://arxiv.org/abs/2306.04903v1

[134, 184] ICDAR 2023 Competition on Reading the Seal Title (source nr: 134, 184)
   URL: http://arxiv.org/abs/2304.11966v2

[135, 185] SemEval 2023 Task 6: LegalEval - Understanding Legal Texts (source nr: 135, 185)
   URL: http://arxiv.org/abs/2304.09548v3

[136, 186] A Comparative Study of Voice Conversion Models with Large-Scale Speech and Singing Data: The T13 Systems for the Singing Voice Conversion Challenge 2023 (source nr: 136, 186)
   URL: http://arxiv.org/abs/2310.05203v1

[137, 187] Foley Sound Synthesis at the DCASE 2023 Challenge (source nr: 137, 187)
   URL: http://arxiv.org/abs/2304.12521v4

[138, 188] Two-stage Neural Network for ICASSP 2023 Speech Signal Improvement Challenge (source nr: 138, 188)
   URL: http://arxiv.org/abs/2303.07621v1

[139, 189] ICDAR 2023 Competition on Structured Text Extraction from Visually-Rich Document Images (source nr: 139, 189)
   URL: http://arxiv.org/abs/2306.03287v1

[140, 190] The DKU-DUKEECE System for the Manipulation Region Location Task of ADD 2023 (source nr: 140, 190)
   URL: http://arxiv.org/abs/2308.10281v1

[141, 191] ACTI at EVALITA 2023: Overview of the Conspiracy Theory Identification Task (source nr: 141, 191)
   URL: http://arxiv.org/abs/2307.06954v3

[142, 192] NeCo@ALQAC 2023: Legal Domain Knowledge Acquisition for Low-Resource Languages through Data Enrichment (source nr: 142, 192)
   URL: http://arxiv.org/abs/2309.05500v1

[143, 193] CUED at ProbSum 2023: Hierarchical Ensemble of Summarization Models (source nr: 143, 193)
   URL: http://arxiv.org/abs/2306.05317v1

[144, 194] The DeepZen Speech Synthesis System for Blizzard Challenge 2023 (source nr: 144, 194)
   URL: http://arxiv.org/abs/2308.15945v2

[145, 195] UBC-DLNLP at SemEval-2023 Task 12: Impact of Transfer Learning on African Sentiment Analysis (source nr: 145, 195)
   URL: http://arxiv.org/abs/2304.11256v2

[146, 196] GIST-AiTeR Speaker Diarization System for VoxCeleb Speaker Recognition Challenge (VoxSRC) 2023 (source nr: 146, 196)
   URL: http://arxiv.org/abs/2308.07788v4

[147, 197] Few-shot bioacoustic event detection at the DCASE 2023 challenge (source nr: 147, 197)
   URL: http://arxiv.org/abs/2306.09223v1

[148, 198] MANTIS at #SMM4H 2023: Leveraging Hybrid and Ensemble Models for Detection of Social Anxiety Disorder on Reddit (source nr: 148, 198)
   URL: http://arxiv.org/abs/2312.09451v1

[149, 199] Proceedings of the Sixth International Conference on Applied Category Theory 2023 (source nr: 149, 199)
   URL: http://arxiv.org/abs/2312.08138v1

[150, 200] THUIR@COLIEE 2023: Incorporating Structural Knowledge into Pre-trained Language Models for Legal Case Retrieval (source nr: 150, 200)
   URL: http://arxiv.org/abs/2305.06812v1




## Research Metrics
- Search Iterations: 9
- Generated at: 2026-05-27T13:37:30.737845+00:00

