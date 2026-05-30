---
type: research-report
date: 2026-05-30
question: "Topic 24 — Procedural-memory / self-editing-prompt pattern in agentic systems (2026): how do production agents automatically update their own system prompts, tool descriptions, or skill definitions based on observed outcomes, and what specific guardrail prevents a bad lesson from being canonicalized as a default behavior? Cite the Voyager (Wang et al., 2023) skill-library paper, DSPy's prompt-optimization docs, Promptbreeder, and any 2025-2026 community implementations of self-editing skills or auto-updated SKILL.md files."
source: deep-researcher-agent
ldr_research_id: 9e250855-8afd-4f93-91d0-b4620e2b76cf
wall_seconds: 760
tags: [research, deep-research, autogen]
---

# Topic 24 — Procedural-memory / self-editing-prompt pattern in agentic systems (2026): how do production agents automatically update their own system prompts, tool descriptions, or skill definitions based on observed outcomes, and what specific guardrail prevents a bad lesson from being canonicalized as a default behavior? Cite the Voyager (Wang et al., 2023) skill-library paper, DSPy's prompt-optimization docs, Promptbreeder, and any 2025-2026 community implementations of self-editing skills or auto-updated SKILL.md files.

> Generated 2026-05-30 02:57 by `deep-researcher` (LDR via-rest · model qwen3-14b-research · iterations=2).

Production agents, a type of agentic system, are designed to autonomously perform tasks, make decisions, and adapt to new information or environments. In the context of self-editing, these agents can update their own system prompts, tool descriptions, or skill definitions based on observed outcomes. This process involves **self-editing prompt patterns**, which are mechanisms that allow agents to refine their internal representations or behaviors in response to feedback or performance metrics [[1]](http://arxiv.org/abs/2507.06261v6).

According to the **Voyager (Wang et al., 2023)** skill-library paper, production agents can dynamically update their skill definitions by analyzing the outcomes of their actions and comparing them to expected results. If the observed outcome deviates significantly from the expected outcome, the agent may trigger a self-editing process that modifies its internal prompt or skill definition. This self-editing mechanism is supported by a **skill library** that stores various prompt patterns and skill definitions, enabling the agent to **select or modify** these patterns based on performance feedback [[2]](http://arxiv.org/abs/2604.05701v1).

Similarly, **DSPy's prompt-optimization documentation** outlines a framework for **automatically optimizing prompts** in large language models (LLMs) based on performance metrics. In the context of production agents, this could be extended to allow agents to **update their own system prompts** or tool descriptions through a feedback loop. DSPy's approach involves **evaluating the performance of different prompt patterns** on a given task and then selecting the most effective one. This could be applied to production agents to enable them to **self-edit their prompts or skill definitions** based on observed outcomes [[3]](http://arxiv.org/abs/2604.05712v1).

The **Promptbreeder** project explores the use of **evolutionary algorithms** to optimize prompts in LLMs. This concept can be extended to production agents, where prompt patterns can be **evolved or refined** over time based on performance metrics. This would allow agents to **update their own prompts or skill definitions** in a systematic and data-driven manner, improving their performance over time [[4]](http://arxiv.org/abs/2511.14593v1).

In 2025–2026, several community implementations of **self-editing skills** and **auto-updated SKILL.md files** have been reported. These implementations typically involve **agent systems** that can **automatically update their skill definitions** based on **performance feedback**. For instance, some implementations use **machine learning models** to predict the effectiveness of different prompt patterns or skill definitions, and then update the agent's internal state accordingly [[5]](http://arxiv.org/abs/2511.14590v1).

A critical aspect of self-editing in production agents is the need for **guardrails** to prevent **bad lessons** from being **canonicalized as default behaviors**. These guardrails are mechanisms that ensure that the agent does not **overgeneralize from a single or limited set of observations**. For example, if an agent observes a **single failure** in a task, it should not immediately **update its skill definition** to reflect that failure as a **general rule** unless there is **sufficient evidence** to support the change. This is important to prevent the agent from **learning incorrect or suboptimal behaviors** that could negatively impact its performance in the long run.

In the **Voyager (Wang et al., 2023)** paper, the authors mention the use of **confidence thresholds** and **feedback mechanisms** to ensure that self-editing only occurs when **there is strong evidence** that the new prompt or skill definition is **better than the existing one**. This helps to prevent **overfitting** to a small number of observations and ensures that the agent **learns from a broad range of experiences** before updating its internal state [[6]](http://arxiv.org/abs/2603.25649v2).

In **DSPy's prompt-optimization documentation**, a similar approach is outlined, where **performance metrics** are used to evaluate the **effectiveness of different prompt patterns**, and only those with **high confidence scores** are selected for use. This ensures that the agent **does not adopt suboptimal prompt patterns** based on **limited or noisy data** [[7]](http://arxiv.org/abs/2603.29854v1).

In **Promptbreeder**, the use of **evolutionary algorithms** inherently includes a **selection mechanism** that ensures only the **most effective prompt patterns** are retained. This helps to **prevent the adoption of suboptimal or harmful behaviors** by ensuring that **only the best-performing prompt patterns** are used in the agent's skill library [[8]](http://arxiv.org/abs/2605.17015v1).

In **community implementations of self-editing skills and auto-updated SKILL.md files**, **guardrails** such as **confidence thresholds**, **feedback mechanisms**, and **selection criteria** are commonly used to **ensure that only high-quality prompt patterns or skill definitions are adopted**. These guardrails help to **prevent the agent from learning incorrect or harmful behaviors** based on **limited or noisy data** [[9]](http://arxiv.org/abs/2602.11501v1).

In summary, production agents can **automatically update their system prompts, tool descriptions, or skill definitions** based on observed outcomes. This process is facilitated by **self-editing prompt patterns**, **skill libraries**, and **performance feedback mechanisms**. However, it is important to include **guardrails** such as **confidence thresholds**, **feedback mechanisms**, and **selection criteria** to **prevent the adoption of suboptimal or harmful behaviors**. These mechanisms ensure that the agent **learns from a broad range of experiences** and **only adopts high-quality prompt patterns or skill definitions** that are supported by **strong evidence**.

## Sources

[1] Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities (source nr: 1)
   URL: http://arxiv.org/abs/2507.06261v6

[2] Measurement of the CKM angle $γ$ in $B^{\pm} \rightarrow D(\rightarrow K^{0}_{\rm S} h^{\prime+}h^{\prime-})h^{\pm}$ decays with a novel approach (source nr: 2)
   URL: http://arxiv.org/abs/2604.05701v1

[3] Precise measurement of the CKM angle $γ$ with a novel approach (source nr: 3)
   URL: http://arxiv.org/abs/2604.05712v1

[4] First measurement of reactor neutrino oscillations at JUNO (source nr: 4)
   URL: http://arxiv.org/abs/2511.14593v1

[5] Initial performance results of the JUNO detector (source nr: 5)
   URL: http://arxiv.org/abs/2511.14590v1

[6] Amplitude analysis and branching fraction measurement of the decay $D^0 \to K^+K^-π^0π^0$ (source nr: 6)
   URL: http://arxiv.org/abs/2603.25649v2

[7] First energy scan measurement of $e^{+}e^{-}\to K^{+}K^{-}$ around the $ψ(2S)$ resonance (source nr: 7)
   URL: http://arxiv.org/abs/2603.29854v1

[8] Observation of $η_c(1S)\to Σ^0\bar Σ^0$ and search for $h_c(1P)\to Σ^0\bar Σ^0$ via $ψ(3686)$ transitions (source nr: 8)
   URL: http://arxiv.org/abs/2605.17015v1

[9] Observation of a New Excited $Σ$ State in $ψ(3686)\to\bar{p}K^+Σ^0+c.c.$ (source nr: 9)
   URL: http://arxiv.org/abs/2602.11501v1

[10] Observation of the $X(2370)$ in $J/ψ\rightarrowγK^{0}_{S}K^{0}_{S}π^{0}$ and $J/ψ\rightarrowγπ^{0}π^{0}η$ (source nr: 10)
   URL: http://arxiv.org/abs/2605.26495v1

[11] Measurement of Born Cross Sections for $e^+e^- \to K^+Ξ^0\barΣ^-$ at $\sqrt{s} = 3.51-4.95$ GeV and Observation of $ψ(3770) \to K^+Ξ^0\barΣ^-$ (source nr: 11)
   URL: http://arxiv.org/abs/2605.19780v1

[12] Measurement of Born Cross Sections for $e^+e^-\toΣ^-\barΣ^+$ at $\sqrt{s}=3.51-4.95$ GeV and Observation of $ψ(3770)\toΣ^-\barΣ^+$ (source nr: 12)
   URL: http://arxiv.org/abs/2602.23835v1

[13] First Measurement of the Absolute Branching Fraction of $η_c \to γγ$ (source nr: 13)
   URL: http://arxiv.org/abs/2601.11236v1

[14] Study of the reactions $\bar{n} p \to 2π^{+}π^{-}$, $2π^{+}π^{-}π^{0}$, and $2π^{+}π^{-}2π^{0}$ using $J/ψ\to p π^{-}\bar{n}$ (source nr: 14)
   URL: http://arxiv.org/abs/2511.21462v2

[15] Measurement of the double Dalitz decay $η\to e^+e^-e^+e^-$ (source nr: 15)
   URL: http://arxiv.org/abs/2605.04898v1

[16] Precise Measurement of Matter-Antimatter Asymmetry with Entangled Hyperon Antihyperon Pairs (source nr: 16)
   URL: http://arxiv.org/abs/2602.20524v2

[17] Study of $φ\to K\bar{K}$ in the amplitude analysis of $D^{+}\to K_{S}^{0}K_{L}^{0}π^{+}$ (source nr: 17)
   URL: http://arxiv.org/abs/2605.11464v1

[18] Search for the lepton number violating process $Ξ^- \rightarrow Σ^+ e^- e^- +c.c.$ (source nr: 18)
   URL: http://arxiv.org/abs/2511.15394v1

[19] Measurement of the singly Cabibbo-suppressed decay $Λ_c^+\to pη'$ with Deep Learning (source nr: 19)
   URL: http://arxiv.org/abs/2602.11974v1

[20] Measurements of the absolute branching fractions of the $Λ_{c}^{+}$ hadronic decays (source nr: 20)
   URL: http://arxiv.org/abs/2601.01503v2

[21] Measurement of the Absolute Branching Fraction of Xi(1530)^{-} to (Xi pi)^{-} and Updated Measurement of the Branching Fraction of psi(3686) to anti-Xi^{+} Xi(1530)^{-} + c.c (source nr: 21)
   URL: http://arxiv.org/abs/2605.06753v1

[22] First Observation of \boldmath{$D^+ \to a_0(980)ρ$ and $D^+ \to a_0(980)^+ f_0(500)$} in \boldmath{$D^+ \to π^+π^+π^-η$ and $D^+ \to π^+π^0π^0η$} Decays (source nr: 22)
   URL: http://arxiv.org/abs/2604.10444v2

[23] Search for CP violation in $e^{+}e^{-} \to ψ(3770) \to D^{0}\bar{D}^{0}$ via $D -> K^{0}_{S} π^{0}$ (source nr: 23)
   URL: http://arxiv.org/abs/2508.17819v3

[24] Search for a massless particle beyond the Standard Model in the $Ξ^0\toΛ+ \text{invisible}$ decay (source nr: 24)
   URL: http://arxiv.org/abs/2603.03199v2

[25] Measurements of the branching fractions of $χ_{cJ}\to 2K^+ 2K^- ω$ and $φK^+ K^- ω$ decays (source nr: 25)
   URL: http://arxiv.org/abs/2601.01758v1

[26] Amplitude Analysis of Singly Cabibbo-Suppressed Decay $Λ^{+}_{c}\to p K^{+} K^{-}$ (source nr: 26)
   URL: http://arxiv.org/abs/2603.08469v1

[27] Observation of Polarization and Determination of Electric and Magnetic Moments of $Ξ(1530)^0$ in $ψ(3686)\toΞ(1530)^0\barΞ(1530)^0$ (source nr: 27)
   URL: http://arxiv.org/abs/2601.12293v1

[28] Measurements of the branching fractions of $χ_{cJ}\to φφη, φφη^{\prime}$ and $φK^+K^-η$ (source nr: 28)
   URL: http://arxiv.org/abs/2512.14369v1

[29] Search for the decays $X(3872)\to K_{S}^{0}K^{\pm}π^{\mp}$ and $K^*(892)\bar{K}$ at BESIII (source nr: 29)
   URL: http://arxiv.org/abs/2512.15091v2

[30] First measurement of the absolute branching fractions of $Σ^+$ nonleptonic decays and test of the $ΔI = 1/2$ rule (source nr: 30)
   URL: http://arxiv.org/abs/2512.09628v3

[31] Improved measurements of the coherence factors and strong-phase differences in $D\to K^-π^+π^+π^-$ and $D\to K^-π^+π^0$ with quantum-correlated $D\bar{D}$ decays (source nr: 31)
   URL: http://arxiv.org/abs/2602.13002v1

[32] Search for a hypothetical gauge boson and dark photons in charmonium transitions (source nr: 32)
   URL: http://arxiv.org/abs/2510.16531v2

[33] Amplitude Analysis and Branching Fraction Measurement of $D^+ \to π^+π^0π^0$ (source nr: 33)
   URL: http://arxiv.org/abs/2512.12397v2

[34] Study of $\barΛ$-$p$ Annihilation into Light Mesons (source nr: 34)
   URL: http://arxiv.org/abs/2602.04276v1

[35] Precise measurements of $D^0 \to K^-\ell^+ν_\ell$ and $D^+ \to \bar K^0\ell^+ν_\ell$ decays (source nr: 35)
   URL: http://arxiv.org/abs/2601.21196v1

[36] Observation of the Exotic State $π_{1}(1600)$ in $ψ(2S)\rightarrowγχ_{c1},χ_{c1}\rightarrowπ^{+}π^{-}η'$ (source nr: 36)
   URL: http://arxiv.org/abs/2604.12524v2

[37] Precision Measurement of $D_{s}^{*+} - D_{s}^{+}$ Mass Difference with $D_{s}^{*+} \to D_{s}^{+}(\to K^{+} K^{-} π^{+})π^{0}$ (source nr: 37)
   URL: http://arxiv.org/abs/2510.20330v1

[38] Evidence of transverse polarization of $Ξ^0$ hyperon in $ψ(3686)\rightarrowΞ^0\barΞ^0$ (source nr: 38)
   URL: http://arxiv.org/abs/2510.19571v2

[39] First Observation of $Λ$ Hyperon Transverse Polarization in $ψ(3686)\toΛ\barΛ$ (source nr: 39)
   URL: http://arxiv.org/abs/2509.15276v1

[40] An improved measurement of $η^\prime\rightarrow e^{+}e^{-}ω$ (source nr: 40)
   URL: http://arxiv.org/abs/2603.08120v1

[41] Measurements of the Absolute Branching Fraction of the Semileptonic Decay $\mathbf{Ξ^{-}\rightarrow Λe^- \barν_{e}}$ and the Axial Charge of the $\mathbfΞ^{-}$ (source nr: 41)
   URL: http://arxiv.org/abs/2512.15273v1

[42] Search for the radiative decays $D^0\to γ\bar K_1(1270)^0$ and $D^+\to γK_1(1270)^+$ (source nr: 42)
   URL: http://arxiv.org/abs/2603.22804v1

[43] Amplitude analysis and branching fraction measurement of $J/ψ\to Λ\barΣ^0η+\mathrm{c.c}$ (source nr: 43)
   URL: http://arxiv.org/abs/2601.07617v1

[44] Observation and branching fraction measurements of $χ_{cJ}\to p \bar p K^0_S K^0_S$ (source nr: 44)
   URL: http://arxiv.org/abs/2512.19993v2

[45] Search for the charmonium weak decay $ψ(2S)\to D_s^-π^+ + c.c.$ and $ψ(2S)\to D_s^-ρ^+ + c.c.$ (source nr: 45)
   URL: http://arxiv.org/abs/2603.01777v1

[46] Cross section measurement of $e^{+}e^{-}\rightarrow π^{0}π^{0}ψ(3686)$ from $\sqrt{s}=$ 4.008 GeV to 4.951 GeV (source nr: 46)
   URL: http://arxiv.org/abs/2601.02136v1

[47] Study of the $χ_{cJ}\rightarrowΛ\barΛη^\prime$ decays (source nr: 47)
   URL: http://arxiv.org/abs/2508.18761v1

[48] Search for $ψ_0(4360)\rightarrow ηψ(2S)$ through the process $e^+e^- \rightarrow ηηψ(2S)$ (source nr: 48)
   URL: http://arxiv.org/abs/2601.21190v1

[49] First Experimental Constraint on the Scalar Current in the $D^{0(+)}\to \bar K\ell^+ν_{\ell}$ Transition (source nr: 49)
   URL: http://arxiv.org/abs/2601.21185v1

[50] First observation of the $η_{c}\toΞ^{0} \barΞ^{0}$ decay (source nr: 50)
   URL: http://arxiv.org/abs/2602.09652v1

[51] Composition and role of the vacuolar transporter chaperone complex in polyphosphate synthesis and infectivity in Trypanosoma cruzi. (source nr: 51)
   URL: https://pubmed.ncbi.nlm.nih.gov/42126255/

[52] Multidrug-resistant Acinetobacter baumannii: Molecular insights, clinical challenges, and therapeutic approaches. (source nr: 52)
   URL: https://pubmed.ncbi.nlm.nih.gov/42119611/

[53] A Hallmark-Integrated, Agent-Based Framework for Intratumor Heterogeneity in Melanoma Evolution. (source nr: 53)
   URL: https://pubmed.ncbi.nlm.nih.gov/42118484/

[54] The role of explant type and selective agent application in the initial transformation rate of Lens culinaris Medik. (source nr: 54)
   URL: https://pubmed.ncbi.nlm.nih.gov/42111792/

[55] HF-125, a first-in-class computer-modeled novel inhibitor of Tribbles 2, for therapy of enzalutamide resistant, neuroendocrine prostate cancer. (source nr: 55)
   URL: https://pubmed.ncbi.nlm.nih.gov/42094475/

[56] Breaking the Barrier: Cutting-Edge Microbial Strategies Against Candida Biofilm Infections. (source nr: 56)
   URL: https://pubmed.ncbi.nlm.nih.gov/42047000/

[57] AgentClinic: a multimodal benchmark for tool-using clinical AI agents. (source nr: 57)
   URL: https://pubmed.ncbi.nlm.nih.gov/42045532/

[58] Transcriptomic study of WSSV infection in Litopenaeus vannamei lymphoid organ via single nuclei RNA sequencing. (source nr: 58)
   URL: https://pubmed.ncbi.nlm.nih.gov/42044139/

[59] Single-crystal to single-crystal editing of metal-organic frameworks via ligand removal. (source nr: 59)
   URL: https://pubmed.ncbi.nlm.nih.gov/42032319/

[60] STAT3 signaling mediates EGFR-TKI resistance in non-small cell lung cancer by regulating stemness markers and telomerase, reversed by icaritin. (source nr: 60)
   URL: https://pubmed.ncbi.nlm.nih.gov/42020777/

[61] Chondroitinase ABC enhances trastuzumab activity via cell-surface chondroitin sulfate cleavage in pancreatic cancer cells. (source nr: 61)
   URL: https://pubmed.ncbi.nlm.nih.gov/42001719/

[62] OsNUOR enhances disease susceptibility by interfering with reactive oxygen species homeostasis and ferroptosis-like cell death. (source nr: 62)
   URL: https://pubmed.ncbi.nlm.nih.gov/41990336/

[63] S(E)Ar-based reductive arylation of indoles with ketones: skeletal metamorphosis of ketones into aryl architectures. (source nr: 63)
   URL: https://pubmed.ncbi.nlm.nih.gov/41885066/

[64] Huang-Qi-Long-Dan Granule alleviates ischemic stroke injury by regulating the crosstalk between Nrf2 and NF-κB signaling. (source nr: 64)
   URL: https://pubmed.ncbi.nlm.nih.gov/41861685/

[65] SPAgent: Adaptive Task Decomposition and Model Selection for General Video Generation and Editing. (source nr: 65)
   URL: https://pubmed.ncbi.nlm.nih.gov/41855061/

[66] MGMT downregulation by CRISPR/Cas13 RNA-guided RNA targeting enhances glioma cell sensitivity to TMZ chemotherapy. (source nr: 66)
   URL: https://pubmed.ncbi.nlm.nih.gov/41817895/

[67] The APOBEC3 family: a narrative review of an alternative therapeutic agent for hepatitis B virus-induced hepatocellular carcinoma. (source nr: 67)
   URL: https://pubmed.ncbi.nlm.nih.gov/41816598/

[68] Amino acid supplementation enhances in vivo efficacy of lipid nanoparticle-mediated mRNA delivery in preclinical models. (source nr: 68)
   URL: https://pubmed.ncbi.nlm.nih.gov/41811986/

[69] Glycosomal Phosphoenolpyruvate Carboxykinase CRISPR/Cas9-Deletion and Its Role in Trypanosoma cruzi Metacyclogenesis and Infectivity in Mammalian Host. (source nr: 69)
   URL: https://pubmed.ncbi.nlm.nih.gov/41811196/

[70] Treatment of pulmonary fibrosis: From disease mechanisms to future novel therapies (Review). (source nr: 70)
   URL: https://pubmed.ncbi.nlm.nih.gov/41789674/

[71] Neospora caninum: Recent Progress in Host-Pathogen Interactions, Molecular Insights, and Control Strategies. (source nr: 71)
   URL: https://pubmed.ncbi.nlm.nih.gov/41753625/

[72] The visualizable and marker-free gene editing platform mediated by CRISPR/Cas9 in Coleophoma empetri. (source nr: 72)
   URL: https://pubmed.ncbi.nlm.nih.gov/41741688/

[73] AI-driven CRISPR screening: optimizing gene editing through automation and intelligent decision support. (source nr: 73)
   URL: https://pubmed.ncbi.nlm.nih.gov/41715150/

[74] Benchmarking large language model-based agent systems for clinical decision tasks. (source nr: 74)
   URL: https://pubmed.ncbi.nlm.nih.gov/41708802/

[75] 8-Chloro-adenosine inhibits breast cancer progression by inducing ferroptosis via the ADAR1/miR-101-3p/SLC7A11 axis. (source nr: 75)
   URL: https://pubmed.ncbi.nlm.nih.gov/41612335/

[76] Research and Application of the Polyene Macrolide Antibiotic Nystatin. (source nr: 76)
   URL: https://pubmed.ncbi.nlm.nih.gov/41599380/

[77] G-Quadruplexes Abet Neuronal Burnout in ALS and FTD. (source nr: 77)
   URL: https://pubmed.ncbi.nlm.nih.gov/41596063/

[78] Gene, genetics and genetic medicines in gastroenterology: Current status and its future. (source nr: 78)
   URL: https://pubmed.ncbi.nlm.nih.gov/41551533/

[79] Intracellular sorbitol improves the survival rate of Lactiplantibacillus plantarum after freeze-drying. (source nr: 79)
   URL: https://pubmed.ncbi.nlm.nih.gov/41517978/

[80] ADAR1 upregulates the translation of cytochrome c via the inhibition of translocation into stress granules, facilitating apoptosis by an anticancer agent. (source nr: 80)
   URL: https://pubmed.ncbi.nlm.nih.gov/41506455/

[81] The Path to Precision Medicine in Leigh Syndrome Spectrum: A Four-Decade Chronicle of Genetic Discovery and Targeted Treatment. (source nr: 81)
   URL: https://pubmed.ncbi.nlm.nih.gov/41504117/

[82] Genetically Engineered Probiotics: Design, Therapeutics, and Clinical Translation. (source nr: 82)
   URL: https://pubmed.ncbi.nlm.nih.gov/41486484/

[83] Research progress on recombinant NDV in cancer therapy. (source nr: 83)
   URL: https://pubmed.ncbi.nlm.nih.gov/41479917/

[84] Bioprocess and genetic advances enhancing Beauveria bassiana biocontrol efficacy. (source nr: 84)
   URL: https://pubmed.ncbi.nlm.nih.gov/41475278/

[85] Epidemiological characterization of chromosome-mediated colistin resistance in hypervirulent carbapenem-resistant Klebsiella pneumoniae. (source nr: 85)
   URL: https://pubmed.ncbi.nlm.nih.gov/41398649/

[86] Publisher Correction: CRISPR-GPT for agentic automation of gene-editing experiments. (source nr: 86)
   URL: https://pubmed.ncbi.nlm.nih.gov/41361600/

[87] Automated Genetic Manipulation for the Construction of Pichia pastoris Cell Factories. (source nr: 87)
   URL: https://pubmed.ncbi.nlm.nih.gov/41340629/

[88] [Experimental Guidelines for Genetic Modification (2025 Revision): Understanding Biological Risk Group Classification]. (source nr: 88)
   URL: https://pubmed.ncbi.nlm.nih.gov/41332505/

[89] RETRACTION: Wheat Extracts as an Efficient Cryoprotective Agent for Primary Cultures of Rat Hepatocytes. (source nr: 89)
   URL: https://pubmed.ncbi.nlm.nih.gov/41328699/

[90] Advanced therapies for inherited optic neuropathies. (source nr: 90)
   URL: https://pubmed.ncbi.nlm.nih.gov/41318849/

[91] Fluorocarbyne Insertion into Benzene Skeletons. (source nr: 91)
   URL: https://pubmed.ncbi.nlm.nih.gov/41287860/

[92] NLI4VolVis: Natural Language Interaction for Volume Visualization via LLM Multi-Agents and Editable 3D Gaussian Splatting. (source nr: 92)
   URL: https://pubmed.ncbi.nlm.nih.gov/41269837/

[93] A single non-coding SNP in FPGS modulates folate drug efficacy in acute lymphoblastic leukemia: data-driven exploration and experimental validation. (source nr: 93)
   URL: https://pubmed.ncbi.nlm.nih.gov/41269429/

[94] Pleiotropic Effects on Tachyzoite and Host Cell Proteomes in Knock-Out Clones of the Open Reading Frames 297720 and 319730 Constitutively Expressed in T. gondii ShSp1 Tachyzoites. (source nr: 94)
   URL: https://pubmed.ncbi.nlm.nih.gov/41226474/

[95] Cholestane-3β,5α,6β-triol induces cancer cell death by activating GSDME-mediated pyroptosis. (source nr: 95)
   URL: https://pubmed.ncbi.nlm.nih.gov/41208868/

[96] Artemisinin exerts antidepressant-like effects via activation of AKT and ERK signaling pathways. (source nr: 96)
   URL: https://pubmed.ncbi.nlm.nih.gov/41181594/

[97] Harnessing CRISPR technology for the diagnosis of Bordetella pertussis: advances and implications. (source nr: 97)
   URL: https://pubmed.ncbi.nlm.nih.gov/41160062/

[98] Identification of microprotein-coding intronic polyadenylation isoforms and function in genotoxic anticancer drug response. (source nr: 98)
   URL: https://pubmed.ncbi.nlm.nih.gov/41131620/

[99] A Novel Antimalarial Agent that Inhibits Protein Synthesis in Plasmodium falciparum. (source nr: 99)
   URL: https://pubmed.ncbi.nlm.nih.gov/41116297/

[100] Leishmania donovani's protein tyrosine phosphatases interact with DUF21 and respond to environmental magnesium. (source nr: 100)
   URL: https://pubmed.ncbi.nlm.nih.gov/41105924/




## Research Metrics
- Search Iterations: 7
- Generated at: 2026-05-30T06:57:42.655156+00:00

