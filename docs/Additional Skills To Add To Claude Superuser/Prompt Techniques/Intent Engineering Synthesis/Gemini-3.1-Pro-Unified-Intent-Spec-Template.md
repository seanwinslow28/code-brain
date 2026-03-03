Here is the synthesized Unified Intent Spec Template.

To build this, I analyzed the competing frameworks in your research—Pathmode’s IntentSpec, Huryn’s 7-Part Structure, the I-5 Framework, and the Action Schemas methodology—and mapped them directly to your specific Claude Code Superuser Pack architecture (Interactive vs. Autonomous Agents SDK).

The core architectural takeaway from your research is that **intent cannot live entirely in the prompt.** While steering guidelines belong in your SKILL.md files, hard boundaries must be enforced by architecture (Hooks returning Exit Code 2, or config.toml cost limits) to prevent catastrophic failures like the Klarna "Intent Gap" case study \[All notes 2/28/2026, Intent-Engineering-Frameworks.pdf\].

### **Framework Synthesis Matrix**

*Where the components of this unified template originate:*

| Unified Concept | Origin Framework(s) | Maturity Level | Claude Code Implementation Target |
| :---- | :---- | :---- | :---- |
| **Objective & Outcomes** | Pathmode (User Goal), Huryn (Outcomes) | **Proven Pattern** | SKILL.md (Top of file) |
| **Health Metrics** | Huryn, Klarna Case Study | **Proven Pattern** | SKILL.md & Post-run evaluation hooks |
| **Steering Constraints** | Huryn (Soft Constraints) | **Proven Pattern** | SKILL.md |
| **Hard Constraints** | I-5 Framework, Agents SDK Docs | **Proven Pattern** | Hooks (Exit Code 2\) & config.toml |
| **Autonomy & Deferral** | Huryn (Decision Types), Agents Preamble | **Promising Concept** | SKILL.md & SDK build\_preamble() |
| **Verification & Schema** | Pathmode, Action Schemas | **Emerging Practice** | SKILL.md (Bottom) & Validation Scripts |

---

### **The Unified Intent Spec Template**

Use this template when defining any new agent or skill. It specifies exactly *where* in your codebase each configuration should live.

YAML

\# \==========================================  
\# UNIFIED INTENT SPECIFICATION TEMPLATE  
\# \==========================================

\# 1\. CORE INTENT (Location: SKILL.md \- Top of file)  
\# Description: What problem is this solving, and what does success look like?  
objective:   
  \# \[Required\] The primary mission and why it matters. Include trade-off guidance.  
  \# Example: "Resolve merge conflicts. Prioritize code safety over speed."  
desired\_outcomes:  
  \# \[Required\] 2-4 observable, measurable STATES (not activities).  
  \# Example: "The vault contains a daily summary note formatted to PARA standards."

\# 2\. ALIGNMENT & SAFETY (Location: SKILL.md)  
\# Description: Guardrails against the agent optimizing for the wrong thing (Goodhart's Law).  
health\_metrics:  
  \# \[Required\] What must NOT degrade while achieving the outcome?   
  \# Example: "Do not delete any user-generated markdown files; only append."  
edge\_cases:  
  \# \[Optional\] Known boundary conditions and how to resolve them.  
  \# Example: "If the target API is down, write to a local fallback cache."

\# 3\. ARCHITECTURAL CONSTRAINTS (Location: Hooks & config.toml)  
\# Description: Non-negotiable rules enforced outside the LLM's context window.  
hard\_constraints:  
  \# \[Required\] Tools the agent is structurally forbidden from using.  
  \# Implementation: Use \`disallowedTools\` in config.toml or PreToolUse Hooks (Exit Code 2).  
  \# Example: "disallowedTools: \[Bash, FileEdit\]"   
execution\_limits:  
  \# \[Required\] Financial and compute boundaries.  
  \# Implementation: config.toml settings.  
  \# Example: "max\_turns: 15, max\_cost\_usd: 0.50"

\# 4\. AUTONOMY & ESCALATION (Location: SKILL.md & Agents SDK Preamble)  
\# Description: How the agent handles uncertainty based on its runtime environment.  
autonomy\_level:  
  \# \[Required\] Choose one: Full (Background), Guarded (Logged/Rollback), Proposal-First (Interactive), Human-Required.  
stop\_rules:  
  \# \[Required\] Exact conditions under which the agent must halt or escalate.  
  \# Example: "Halt and defer if you detect a corrupted frontmatter block."

\# 5\. EXECUTION & VERIFICATION (Location: SKILL.md \- Bottom of file)  
\# Description: The explicit steps and how to prove they worked.  
action\_schema:  
  \# \[Optional\] Forced output format if interfacing with other systems.  
  \# Example: "Output MUST be valid JSON matching the DailyPlanSchema."  
verification\_criteria:  
  \# \[Required\] How the agent (or a subagent) knows the job is actually done.  
  \# Example: "Run \`python3 scripts/validate.py\` and ensure 0 errors."

---

### **Completed Example: Personal Daily Planning Agent**

This example applies the unified template to the scheduled daily\_driver.py agent referenced in your architecture \[All notes 2/28/2026, agents-sdk.md\]. This is a high-risk autonomous agent because it runs on macOS launchd while you sleep, making Intent Engineering structurally mandatory.

YAML

\# \==========================================  
\# INTENT SPEC: AUTONOMOUS DAILY DRIVER  
\# \==========================================

\# 1\. CORE INTENT (-\> .claude/skills/daily-driver/SKILL.md)  
objective: \>  
  Synthesize yesterday's open tasks and today's calendar events into a   
  prioritized daily plan. Trade-off: Prioritize accurately capturing all   
  hard-scheduled meetings over creatively brainstorming new tasks.  
desired\_outcomes:  
  \- A new daily note exists in \`vault/01-Journal/\` for the current date.  
  \- The note contains a unified "Top 3 Priorities" list.  
  \- The note includes a schedule block pulling from the local calendar MCP.

\# 2\. ALIGNMENT & SAFETY (-\> .claude/skills/daily-driver/SKILL.md)  
health\_metrics:  
  \- "Data Non-Destruction: Never overwrite existing text if a note for today already exists; only append."  
  \- "Truth Anchoring: Do not hallucinate calendar events to fill empty space."  
edge\_cases:  
  \- "If the Calendar MCP fails to connect, create the note with an empty 'Schedule' section and append an \[ERROR: MCP SYNC FAILED\] tag."

\# 3\. ARCHITECTURAL CONSTRAINTS (-\> agents-sdk/config.toml & Hooks)  
hard\_constraints:  
  \# Enforced via PreToolUse hook (Returns Exit Code 2 if violated)  
  \- "Disallow \`Bash\` execution outside of the \`vault/\` directory."  
execution\_limits:  
  \# Enforced via config.toml AgentConfig  
  \- max\_turns: 10  
  \- max\_cost\_usd: 0.25

\# 4\. AUTONOMY & ESCALATION (-\> agents-sdk/agents/daily\_driver.py preamble)  
autonomy\_level: Full (Background Scheduled)  
stop\_rules:  
  \- "Zero-Interaction Mandate: Do not ask clarifying questions. You are running at 4:00 AM while the user is asleep."  
  \- "Safe Deferral Protocol: If you cannot parse the Obsidian frontmatter of yesterday's note, halt execution and create an 'Agent Error' notification note."

\# 5\. EXECUTION & VERIFICATION (-\> .claude/skills/daily-driver/SKILL.md)  
action\_schema: \>  
  \# Vault Inject Tool Args  
  { "file\_path": "vault/01-Journal/YYYY-MM-DD.md", "anchor": "\#\# Plan", "content": "..." }  
verification\_criteria:  
  \- "Use \`read\_frontmatter\` to confirm the new note has \`status: active\`."  
  \- "Verify the word count of the injected plan is \> 50 words."

### **Architectural Advice for the PM**

**1\. The "Zero-Interaction Mandate" is your most critical personal safeguard.**

Because you are running agents via macOS launchd, if a prompt is underspecified, Claude will naturally try to ask the user a clarifying question. In a background script, this causes a silent timeout hang. Explicitly defining stop\_rules and injecting the "Zero-Interaction Mandate" into the SDK's build\_preamble() is the most immediate technical fix you should implement today \[All notes 2/28/2026\].

**2\. Stop relying purely on prompts for constraints.**

If an agent deleting your Obsidian vault is a catastrophic risk, telling the LLM "do not delete files" in a SKILL.md is insufficient. The research is clear that critical constraints require architectural enforcement \[SKILL.md\]. You must map these to your PreToolUse hooks to return Exit Code 2 (Deny) if a destructive tool call is attempted \[CLAUDE.md\].

