---
name: prompt-engineering
description: Engineer, write, improve, or review prompts and system prompts for Claude or other LLMs. Use when creating a new prompt, refining an existing prompt, writing system instructions, building a prompt template, debugging why a prompt produces bad output, or optimizing prompt structure. Triggers on "write a prompt", "create a prompt", "improve this prompt", "system prompt", "prompt template", "prompt engineering", "make this prompt better", "optimize prompt".
---

# Prompt Engineering

## Purpose

Systematically apply Anthropic's official prompt engineering best practices whenever writing, reviewing, or improving prompts. Run through a structured checklist of 9 techniques (ordered from most broadly effective to most specialized) to ensure every prompt is clear, well-structured, and optimized for Claude's architecture. Source: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview

## When to Use

- Writing a new prompt from scratch for any task
- Improving or debugging an existing prompt that produces poor output
- Creating system prompts or role definitions
- Building reusable prompt templates with variables
- Reviewing a prompt before deploying it in production or a Claude Project
- Writing prompts for Claude Code CLAUDE.md files or custom instructions
- Writing a skill's system prompt (SKILL.md body) or an agent system prompt
- Writing an MCP tool or skill **description** — the short trigger text a model reads to decide whether to invoke it (optimize for auto-selection: lead with the action and the *when-to-call* trigger conditions, not prose a human would enjoy)
- Helping someone learn how to prompt effectively

## Examples

**Example 1: Writing a new prompt**
```
User: "Write me a prompt that summarizes meeting notes into action items"
Claude: [Uses prompt-engineering skill] Applies the 9-technique checklist:
1. Clarity: Defines exactly what an "action item" is, who the audience is, what format to use
2. Examples: Includes 2-3 multishot examples of meeting notes → action items
3. CoT: Adds <thinking> step to identify decisions vs. tasks vs. FYIs
4. XML structure: Wraps input in <meeting_notes>, output in <action_items>
5. Role: Sets system prompt as "experienced executive assistant"
6. Validation: Adds self-check step to verify completeness
Delivers a production-ready prompt, not a casual first draft.
```

**Example 2: Improving a weak prompt**
```
User: "This prompt keeps giving me generic blog posts: 'Write a blog post about AI trends'"
Claude: [Uses prompt-engineering skill] Diagnoses issues using the checklist:
- Missing: context (audience, publication, tone, length)
- Missing: examples of good vs bad output
- Missing: negative constraints (what NOT to write)
- Missing: structured output format
Rewrites with all techniques applied, explains each change.
```

**Example 3: Building a prompt template**
```
User: "I need a reusable prompt for writing Jira tickets"
Claude: [Uses prompt-engineering skill] Creates template with:
- {{variables}} for dynamic content (feature name, user story, acceptance criteria)
- Fixed structure using XML tags for consistency
- Few-shot examples showing good ticket output with reasoning
- Validation loop to check completeness before final output
```

## The 9-Technique Checklist

Apply these in order from most to least broadly effective. Not every prompt needs all 9 — use judgment based on complexity.

For detailed explanations and examples of each technique, see techniques-guide.md.

**Calibrate to current Claude (4.x/5.x), not legacy habits.** Modern Claude models follow clear intent and structure far better than older ones, so the highest-leverage move is almost always sharper instructions, not more scaffolding. Two specific recalibrations: don't wrap everything in XML "just in case" (Technique 4 — use tags to disambiguate genuinely separate components, not as decoration), and don't lean on an elaborate role-play persona to unlock capability (Technique 5 — on modern models the persona shapes tone and framing, not raw ability; lead with a precise task description). When you catch yourself reaching for a legacy trick, check first whether one clearer sentence would do the same work.

### Technique 1: Be Clear and Direct

Think of Claude as a brilliant new employee with amnesia. Provide full context every time.

**Apply by asking:** What is the task? Who is the audience? What does good output look like? What constraints exist?

**Key rules:**
- Give contextual information (what the output will be used for, who will read it, what workflow it fits into)
- Be specific about what you want ("output only code, no explanation" vs. "write code")
- Use sequential steps when order matters
- Use negative constraints to prevent common failure modes ("Never use jargon. Never exceed 200 words.")
- Golden rule: If a colleague with no context would be confused by your prompt, so will Claude

### Technique 2: Use Examples (Multishot Prompting)

Examples are the single most effective way to get consistent, formatted output.

**Apply by asking:** Can I show Claude 2-5 examples of ideal input→output pairs?

**Key rules:**
- Include 3-5 diverse examples that cover edge cases
- Wrap examples in XML: `<examples><example><input>...</input><output>...</output></example></examples>`
- Include reasoning in examples (input → reasoning → output), not just input → output
- Make examples diverse — cover different scenarios, not just the happy path
- Anti-examples (showing what NOT to do) are powerful when paired with good examples

### Technique 3: Let Claude Think (Chain of Thought)

Give Claude space to reason before answering. This dramatically improves accuracy on complex tasks.

**Apply by asking:** Does this task require analysis, math, logic, or multi-step reasoning?

**Three levels (use the simplest that works):**
- Basic: Add "Think step-by-step" to the prompt
- Guided: Specify the exact steps to think through
- Structured: Use `<thinking>` and `<answer>` XML tags to separate reasoning from output

**Critical rule:** Claude must OUTPUT its thinking. Without outputting the thought process, no thinking occurs.

### Technique 4: Use XML Tags

XML tags are Claude's native structuring language. They prevent Claude from mixing up instructions, examples, and content.

**Apply by asking:** Does this prompt have multiple components (instructions, context, examples, input data)?

**Key rules:**
- Use tags like `<instructions>`, `<context>`, `<examples>`, `<input>`, `<output_format>`
- Be consistent — use the same tag names throughout and refer to them ("Using the document in `<source_material>` tags...")
- Nest tags for hierarchy: `<outer><inner></inner></outer>`
- Request XML in Claude's output too — makes it easy to parse programmatically
- Power move: Combine XML tags with multishot examples and CoT for maximum structure

### Technique 5: Give Claude a Role (System Prompts)

Role prompting turns Claude from a general assistant into a domain expert.

**Apply by asking:** Would a specific persona (analyst, editor, developer, advisor) produce better output?

**Key rules:**
- Set role in the system prompt, task instructions in the user turn
- Be specific: "You are a senior financial analyst at a Fortune 500 company" not "You are helpful"
- Role affects tone, depth, terminology, and focus
- Combine with constraints: "You are an editor. Rules: Preserve meaning. Improve clarity. Keep sentences under 18 words."

### Technique 6: Prefill Claude's Response (Legacy — Removed on Current Models)

Prefilling means starting Claude's response with your own text to control format and skip preamble. **On current Claude models (Opus 4.6 and the 4.7 / 4.8, Sonnet 5, and Fable 5 lines), a last-assistant-turn prefill returns a 400 error** — do not reach for it first. It remains valid only on older/legacy models.

**Use these modern replacements instead:**
- **Guaranteed JSON / schema output** → structured outputs: set `output_config.format` with a JSON schema (or use the SDK's `messages.parse()`). This replaces prefilling `{` and actually *guarantees* the shape rather than nudging toward it.
- **Skip the preamble** ("Here is the summary:") → a system-prompt instruction: *"Respond directly with no preamble; do not open with 'Here is' or 'Based on'."*
- **Hold a persona / role** → set the role in the system prompt (Technique 5), not by prefilling `[ROLE_NAME]:`.

**Apply by asking:** Am I targeting a current model? If yes, use structured outputs or a system-prompt instruction. Only prefill when you have confirmed the target is a legacy model that still accepts it.

### Technique 7: Chain Complex Prompts

Break complex tasks into smaller sequential prompts where each step validates the previous one.

**Apply by asking:** Does this task have 3+ distinct steps that each need Claude's full attention?

**Key rules:**
- Each subtask should have a single, clear objective
- Use XML tags to pass outputs between prompts
- Consider self-correction chains: generate → validate → fix
- Use for: research synthesis, document analysis, iterative content creation, multi-step workflows

### Technique 8: Long Context Tips

When working with large documents (20K+ tokens), structure matters more.

**Apply by asking:** Am I providing long documents, multiple sources, or large datasets?

**Key rules:**
- Put long documents at the TOP of the prompt, query/instructions at the BOTTOM (improves quality up to 30%)
- Wrap documents in `<document>` tags with `<source>` and `<document_content>` subtags
- Ask Claude to quote relevant sections before answering (cuts through noise)
- Use `<documents>` with indexed `<document index="1">` for multiple sources

### Technique 9: Validation and Self-Checking

Add self-checking instructions to catch errors before final output.

**Apply by asking:** Is accuracy critical? Could Claude make errors that would be costly?

**Key rules:**
- Add to end of prompt: "After generating your answer: 1) Check it addresses all points, 2) Verify no contradictions, 3) Confirm format matches requirements, 4) Revise if any check fails"
- For factual tasks: "Quote the relevant source material before drawing conclusions"
- For code: "Trace through your code with a test case before presenting it"

## Debugging a Prompt That Produces Bad Output

When an existing prompt misbehaves, do NOT rewrite it from scratch and re-apply all nine techniques — that discards the parts that already work and often reintroduces the same bug. Diagnose the specific failure, change the one thing most likely responsible, and re-test.

1. **Name the failure mode precisely.** What is actually wrong with the output — not "it's bad"? Wrong format, hallucinated facts, ignored a constraint, wrong tone/voice, too long/short, or a refusal?
2. **Map the failure to its most-likely cause** and change only that:

| Failure mode | Most-likely cause → the one change to try first |
|--------------|--------------------------------------------------|
| Wrong or inconsistent format | No structured output / no example of the exact shape → add `output_config.format` (Technique 6) or 2-3 examples (Technique 2) |
| Hallucinated / made-up facts | No grounding → require "quote the source before answering" (Technique 9) or supply the source in `<document>` tags (Technique 8) |
| Ignored a constraint | Constraint buried or stated once → move it to its own line, phrase it as a negative ("Never …"), and put the most important constraints last (Technique 1) |
| Wrong tone / voice | No role or no voice example → set the role (Technique 5) and show one example in the target voice (Technique 2) |
| Too long / rambling / too terse | No length or scope bound → add an explicit limit and say what to cut ("under 150 words; drop background the reader already has") |
| Unwanted preamble | → system-prompt instruction to respond directly (see Technique 6's modern replacements) |
| Refusal on benign work | Over-aggressive framing or an ambiguous request → reframe the intent plainly and state the legitimate use; don't escalate with "you MUST" |

3. **Change one thing, then re-test on the same input that failed.** If it's fixed, stop — don't keep "improving." If not, revert that change and try the next-most-likely cause. Rewriting everything hides which constraint was actually broken; a targeted fix tells you.

## Prompt Assembly Order

When building a prompt, assemble components in this order:

1. **System prompt** (if using API): Role + constraints + rules
2. **Long context/documents** (if any): Placed at the top
3. **Task instructions**: Clear, specific, with negative constraints
4. **Output format**: XML structure or format specification
5. **Examples**: 2-5 multishot examples with reasoning
6. **Chain of thought**: Thinking instructions if task is complex
7. **Validation**: Self-check instructions at the end
8. **Query/input**: The actual content to process (at the very bottom)

## Quick-Reference: Technique Selection by Task Type

| Task Type | Must Use | Consider Adding |
|-----------|----------|-----------------|
| Simple Q&A | Clarity | — |
| Content writing | Clarity, Role, Examples | Negative constraints |
| Data extraction | XML tags, Examples, Prefill | Validation |
| Analysis/research | CoT, XML, Long context | Chaining, Validation |
| Code generation | Clarity, Examples, Validation | CoT, Prefill |
| Classification | Examples (3-5), XML output | Prefill |
| Summarization | Clarity, XML, Long context | CoT, Validation |
| Multi-step workflow | Chaining, XML handoffs | Validation per step |
| Template creation | XML, Examples, Variables | Role, Validation |

## Verify the Prompt Actually Works

A checklist-complete prompt is not the goal — a prompt that changes model behavior is. Before delivering any prompt you wrote or improved:

1. State the **one** behavior change you're targeting ("outputs valid JSON every time," "stops adding a summary paragraph," "catches the edge case it was missing").
2. Run it once on a representative input and read the output against that target — a before/after if you're improving an existing prompt.
3. If the target behavior didn't move, treat it as a debugging problem (see the section above), not a reason to pile on more instructions. Deliver only once you've seen the change you promised.

## Success Criteria

- [ ] Prompt includes sufficient context (audience, purpose, constraints)
- [ ] Negative constraints are used to prevent common failure modes
- [ ] Examples are included for any task requiring specific formatting or style
- [ ] XML tags separate distinct components (instructions, examples, input, output)
- [ ] Chain of thought is enabled for tasks requiring reasoning
- [ ] Long documents are placed at the top with query at the bottom
- [ ] A validation/self-check step is included for accuracy-critical tasks
- [ ] The prompt could be understood by someone with zero context on the task

## Copy/Paste Ready

```
"Write a prompt for [task]"
"Improve this prompt"
"Create a system prompt for [role]"
"Build a prompt template for [workflow]"
"Why is this prompt producing bad output?"
"Review this prompt against best practices"
"Help me engineer a better prompt"
"Optimize this prompt for Claude"
```
