---
name: case-studies
description: Real-world Claude Code success stories and workflow patterns. Provides proven "Transformation Patterns" for Product Managers, Creatives, and Developers to replicate verified productivity gains.
---

# Case Studies & Pattern Library

## Purpose

Learn from verified success stories. This skill provides a library of "Transformation Patterns"—proven workflows used by power users to achieve massive productivity gains (e.g., 164% velocity increase). It connects abstract features to concrete, real-world applications in PM, Creative, and Technical domains.

## When to Use

- You want to modernize your workflow ("How do experts do this?")
- You need inspiration for a Product Management or Creative task
- You want to implement an "Agentic" workflow but don't know what that looks like
- You need to justify adopting a new feature (like Subagents) with a use case

## Examples

**Example 1: PM Workflow Transformation**
```
User: "How can I use Claude for Product Management?"
Claude: [Uses case-studies]
### 📋 Pattern: The "Spec-Driven" Architect
**Source:** Enterprise PM (2M+ users)
**Old Way:** Writing loose prompts and hoping for good code.
**New Way:**
1.  **Phase 1:** `plan.md` (Strategy) created in Plan Mode.
2.  **Phase 2:** `phases.md` (Execution steps).
3.  **Phase 3:** Create a **new thread** for each phase.
**Result:** Deterministic output for complex multi-month projects.
```

**Example 2: Creative Automation**
```
User: "Can Claude help me draft marketing copy?"
Claude: [Uses case-studies]
### 🎨 Pattern: The "Ralph Wiggum" Loop
**Source:** Content Marketer / Creative Technologist
**Workflow:**
Script a loop where Claude Researchers -> Drafts -> Critiques -> Itinerates.
**Command:** `claude -p "Research X, then draft Y. Loop until critique score > 8/10."`
**Result:** Autonomous drafting of high-quality creative assets.
```

## Transformation Patterns ("I used to... Now I do...")

| Domain | I used to... | Now I do... | Benefit |
| :--- | :--- | :--- | :--- |
| **All** | Search Google for docs | **Spin up a local MCP server** for that doc set | "Zips through" indexed docs locally, zero hallucinations. |
| **Dev** | Manually type git commits | **Use a "Commit Agent"** with `git diff` pipe | Consistent, semantic messages without friction. |
| **Dev** | Write code, then test | **Force TDD with a "Test Expert" subagent** | Catches architecture flaws before implementation. |
| **PM** | Chat casually | **Maintain a global `CLAUDE.md` "Living Spec"** | Claude acts as a specialized senior engineer, not a chatbot. |

## Domain-Specific Success Stories

### 1. Product Management
*   **The "Context Engineer":** Advanced PMs treat `CLAUDE.md` as a security gatekeeper. By defining "Authorized Paths" and "Architecture Standards" in the root file, they prevent junior-level mistakes in enterprise codebases.
*   **Automated PRDs:** Using plugins like `/prd-generator` to instantly convert conversational brainstorming into rigorous requirements documents.

### 2. Creative Projects
*   **Voice-First Coding:** Users adopting local transcription (Superwhisper) to "talk" code into existence, bypassing mechanical typing constraints for rapid prototyping.
*   **Visual Debugging:** Feeding Claude screenshots of broken designs (Figma/Maps) allows it to "see" the error and fix the underlying CSS/rendering logic.

### 3. Technical Automation
*   **Self-Healing Stack:** A C++ developer fixed a 4-year-old bug by deploying a "Code Reviewer" subagent that audited the code while a separate "Test Expert" wrote cases. The separation of concerns allowed the main agent to solve the logic puzzle without context overload.

## Success Criteria

- [ ] User adopts a "Spec-Driven" approach for complex tasks
- [ ] User implements at least one "Subagent" pattern (e.g., Tester vs Coder)
- [ ] User replaces manual documentation search with local MCP/Context7
- [ ] User utilizes "Visual Debugging" for UI/Design issues

## Copy/Paste Ready

```
"Show me a PM workflow pattern"
"How do creatives use Claude Code?"
"Give me a transformation pattern for debugging"
"What is the 'Context Engineer' pattern?"
"Example of a self-healing workflow"
```
