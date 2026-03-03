Here is your phased implementation roadmap to transition your Claude Code Superuser Pack to an intent-engineered architecture.

This plan is synthesized directly from the "Implementation Roadmap" and architectural guidelines in your research \[All notes 2/28/2026, Intent-Engineering-Overview.pdf, agents-sdk.md\]. It prioritizes mitigating the highest risks first—specifically, your autonomous launchd agents.

### **Phase 1: Quick Wins (This Week)**

**Goal:** Stabilize scheduled agents to prevent silent failures and secure your highest-risk interactive skills.

* **Inject the Autonomous Preamble**  
  * **Files:** agents-sdk/agents/daily\_driver.py (and any other scheduled agent scripts).  
  * **Action:** Update the build\_preamble() function to explicitly include the "Zero-Interaction Mandate" and safe deferral protocols.  
  * **Effort:** \~1 hour.  
  * **Impact:** Immediately eliminates timeout hangs caused by agents pausing to ask clarifying questions while you are asleep.  
* **Level 1 Retrofit (Minimum Viable Intent)**  
  * **Files:** Top 5 high-blast-radius skills (e.g., .claude/skills/daily-driver/SKILL.md, .claude/skills/vault-read-write/SKILL.md).  
  * **Action:** Prepend the core three sections (Objective, Desired Outcomes, Stop Rules) to the top of the files. Leave the existing step-by-step instructions intact below them.  
  * **Effort:** \~30 minutes per skill.  
  * **Impact:** Wraps your most dangerous tools in an "intent shell" without breaking their current functional logic.

---

### **Phase 2: Foundation (Next 2 Weeks)**

**Goal:** Standardize intent creation and enforce basic financial/compute boundaries.

* **Deploy the Intent Engineering Skill**  
  * **Files:** .claude/skills/intent-engineering/SKILL.md, template.md.  
  * **Action:** Save the skill we just drafted into your .claude/skills directory so you can use Claude to help author future specs.  
  * **Effort:** 15 minutes.  
  * **Impact:** Stops you from "vibe coding" future agents by forcing you to use the unified 9-part template.  
* **Enforce SDK Execution Limits**  
  * **Files:** agents-sdk/config.toml.  
  * **Action:** Define strict max\_turns and max\_cost\_usd properties for every agent registered in the config.  
  * **Effort:** \~1 hour.  
  * **Impact:** Prevents infinite reasoning loops from racking up massive API bills if an agent gets stuck.

---

### **Phase 3: Full Integration (Next Month)**

**Goal:** Move from "prompt-based" suggestions to hard architectural constraints.

* **Architectural Hard Constraints (Hooks)**  
  * **Files:** hooks/pre\_tool\_use.py (or equivalent hook files), CLAUDE.md.  
  * **Action:** Map the "Health Metrics" from your SKILL.md files to actual Python logic in your hooks. If a skill says "do not delete files," update the hook to intercept Bash or FileEdit tools targeting those directories and return **Exit Code 2** (Deny).  
  * **Effort:** 3-5 hours (requires Python coding and testing).  
  * **Impact:** Physically prevents the LLM from executing destructive actions, even if it hallucinates or ignores the SKILL.md prompt.  
* **Batch Level-2 Retrofits**  
  * **Files:** The remaining 100+ .claude/skills/\*/SKILL.md files.  
  * **Action:** Use your new intent-engineering skill to progressively update the rest of your Superuser Pack to the new standard.  
  * **Effort:** Ongoing (do this organically as you use each skill).  
  * **Impact:** Complete architectural alignment across the entire vault.

---

### **Phase 4: Evaluation (Ongoing)**

**Goal:** Assess whether agents are actually optimizing for your outcomes or just going through the motions.

* **Implement "Agent-as-a-Judge" Evaluation**  
  * **Files:** scripts/evaluate\_run.py (New file) or additions to lib/logging\_setup.py.  
  * **Action:** Build a post-run evaluation script that reads the agent's log trace and compares it against the "Verification Criteria" defined in the SKILL.md.  
  * **Effort:** 4-6 hours.  
  * **Impact:** Moves you from treating agents as "black boxes" to having an auditable trail of *why* they made specific decisions, letting you catch metric drift early \[Personal-Agentic-Intent-Engineering.pdf, Intent-Engineering-Overview.pdf\].

---

**Would you like me to draft the exact Python code to update the build\_preamble() function in your daily\_driver.py script so you can knock out the first Phase 1 Quick Win today?**