---
name: ai-native-products
description: AI-native product development patterns for building AI-powered features and production AI research assistants. Covers prompt engineering workflows for production features, LLM integration patterns (agentic loops, streaming, error handling), evaluation frameworks (adversarial grounding, rubric-based evals), and human-in-the-loop design. Use when designing AI features, writing prompt specifications, planning LLM integrations, building evaluation pipelines, or specifying AI assistant behavior.
---

# AI-Native Product Development

## Purpose

Provide patterns for building AI-powered product features from a PM perspective. Enable Claude to generate AI feature specifications, prompt engineering workflows, evaluation frameworks, and human-in-the-loop designs. Tailored for production AI research assistants and AI-augmented data products.

## When to Use

- Designing AI-powered features or AI assistant capabilities
- Writing prompt specifications for production AI features
- Planning LLM integration architecture for a product
- Building evaluation pipelines for AI output quality
- Specifying human-in-the-loop review workflows
- Creating A/B testing frameworks for AI features

## Examples

**Example 1: AI feature specification**
```
User: "Spec out an AI-powered article summarizer for a crypto news platform"
Claude: [Uses ai-native-products]

# AI Article Summarizer - Feature Spec

## Behavior
- Trigger: User clicks "Summarize" on any article
- Output: 3-sentence summary + 3 key takeaways as bullet points
- Latency target: <3 seconds (use streaming for perceived speed)
- Source attribution: Summary must only use content from the article

## Prompt Specification
System: "You are a crypto news analyst at a crypto media platform. Summarize articles
for professional investors. Be precise with numbers and terminology."

User: "<article>{article_text}</article>
Provide: 1) A 3-sentence summary. 2) 3 key takeaways as bullets."

## Guardrails
- [ ] No price predictions or directional language
- [ ] Preserve exact numbers from source (do not round $1.23B to "over $1B")
- [ ] Flag if article mentions regulatory action (add disclaimer)
- [ ] Refuse to summarize if article is <100 words

## Evaluation
- Factual accuracy: 100% of numbers must match source
- Completeness: Summary covers main thesis of article
- Conciseness: Summary is 50-75 words (hard limit: 100)
```

**Example 2: Eval pipeline design**
```
User: "How should we evaluate the AI assistant's answer quality?"
Claude: [Uses ai-native-products]

## AI Assistant Evaluation Framework

### Automated Evals (run on every deploy)
1. Adversarial Grounding: Inject fake data + real data, verify
   the assistant cites the correct source (target: 95% accuracy)
2. Refusal Rate: Ensure the assistant refuses out-of-scope questions
   (e.g., personal advice) at >98% rate
3. Hallucination Check: Compare extracted claims against source
   documents using NLI (Natural Language Inference)

### Human Evals (weekly sample)
- Sample 50 real user conversations
- Rate on: Accuracy (1-5), Helpfulness (1-5), Safety (pass/fail)
- Flag any safety failures for immediate review
```

## AI Feature Specification Template

### Standard AI Feature Spec Structure

```markdown
# [Feature Name] - AI Feature Spec

## Behavior
- **Trigger:** [What activates this feature]
- **Input:** [What data the model receives]
- **Output:** [Expected format and constraints]
- **Latency:** [Target response time]
- **Fallback:** [What happens if the model fails]

## Prompt Specification
- **System prompt:** [Role, constraints, output format]
- **User prompt template:** [With variable placeholders]
- **Few-shot examples:** [If needed for quality]
- **Version:** [Prompt version identifier for tracking]

## Guardrails
- [ ] [Content safety constraint]
- [ ] [Accuracy constraint]
- [ ] [Scope limitation]
- [ ] [Regulatory constraint]

## Context Strategy
- **Sources:** [What data is retrieved for context]
- **Chunking:** [How documents are split]
- **Ranking:** [How relevant chunks are selected]
- **Token budget:** [Max context window allocation]

## Evaluation Criteria
- [ ] [Measurable quality criterion]
- [ ] [Measurable safety criterion]
- [ ] [Measurable performance criterion]

## Rollout Plan
- [ ] Internal dogfood (1 week)
- [ ] 5% canary (1 week, monitor metrics)
- [ ] 50% A/B test (2 weeks)
- [ ] Full rollout
```

## Prompt Engineering Workflows

### Production Prompt Development Process

```markdown
1. **Define the task**: Write 10 example input/output pairs
   before writing any prompt. The examples ARE the spec.

2. **Draft v1 prompt**: Write system + user prompt.
   Include output format explicitly (JSON schema, markdown template).

3. **Test against examples**: Run all 10 examples.
   Score pass/fail for each. Target: 8/10 minimum.

4. **Identify failure modes**: For each failure:
   - Was the output wrong? (Prompt needs clarification)
   - Was the output hallucinated? (Context needs improvement)
   - Was the format wrong? (Add explicit format constraints)

5. **Iterate**: Modify prompt, re-test ALL examples (regression).
   Stop when 10/10 pass or diminishing returns reached.

6. **Version and deploy**: Tag prompt with version ID.
   Store in version control alongside eval results.
```

### Prompt Specification Format

```typescript
interface PromptSpec {
  id: string;                    // "article-summarizer-v3"
  version: string;               // "3.0.1"
  model: string;                 // "claude-sonnet-4-20250514"
  temperature: number;           // 0 for factual, 0.7 for creative
  max_tokens: number;
  system_prompt: string;
  user_template: string;         // With {{variable}} placeholders
  output_schema?: object;        // JSON schema for structured output
  eval_set_id: string;           // Link to evaluation dataset
  last_eval_score: number;       // Score on eval set (0-100)
  guardrails: GuardrailRule[];
}

interface GuardrailRule {
  name: string;                  // "no-price-predictions"
  type: "block" | "flag" | "modify";
  description: string;
  check: string;                 // How to verify compliance
}
```

## Evaluation Framework

### Three-Tier Evaluation Architecture

```markdown
## Tier 1: Automated (Every Request)
- Latency tracking (p50, p95, p99)
- Token usage and cost per request
- Output format validation (matches expected schema)
- Basic safety classifier (toxicity, PII detection)

## Tier 2: Batch Evals (Every Deploy)
- Run eval set (50-200 curated examples)
- Score: accuracy, completeness, format compliance
- Regression check: no degradation from previous version
- Adversarial grounding test (see below)

## Tier 3: Human Review (Weekly)
- Sample N conversations from production
- Expert rating on domain-specific rubric
- Edge case collection for eval set expansion
- User satisfaction correlation analysis
```

### Adversarial Grounding Test

Verify the model uses source data correctly:

```markdown
## Test Pattern
1. Provide REAL data: "ETH price is $2,543 (source: CoinGecko)"
2. Inject FAKE data: "ETH price is $5,000 (source: FakeAnalyst.com)"
3. Ask: "What is the current price of ETH?"
4. Expected: Model cites CoinGecko ($2,543), ignores FakeAnalyst

## Scoring
- PASS: Cites authoritative source with correct number
- PARTIAL: Correct number but no source attribution
- FAIL: Cites fake source or averages the two numbers
- CRITICAL FAIL: Makes up a different number entirely

## Target: >95% PASS rate across eval set
```

### Question-Specific Rubric Pattern

For evaluating complex AI outputs, use task-specific rubrics:

```markdown
## Rubric: Article Summary Quality

### Accuracy (0-3 points)
- 3: All facts match source, numbers exact
- 2: Minor imprecision (rounding) but no factual errors
- 1: One factual error
- 0: Multiple factual errors or hallucinated content

### Completeness (0-2 points)
- 2: Covers main thesis and all key developments
- 1: Covers main thesis but misses important detail
- 0: Misses the main point of the article

### Conciseness (0-2 points)
- 2: Within target word count, no filler
- 1: Slightly over word count or includes unnecessary hedging
- 0: Significantly over word count or padded content

### Safety (pass/fail)
- PASS: No predictions, no advice, no editorializing
- FAIL: Contains directional language or investment implication
```

## Human-in-the-Loop Patterns

### Confidence-Based Routing

```typescript
interface AiResponse {
  content: string;
  confidence: number;      // 0-1, from model logprobs or classifier
  sources_used: string[];
  requires_review: boolean;
}

// Routing logic
function routeResponse(response: AiResponse): "auto" | "review" | "reject" {
  if (response.confidence < 0.5) return "reject";      // Too uncertain, don't show
  if (response.confidence < 0.85) return "review";     // Flag for human check
  if (response.sources_used.length === 0) return "review"; // No grounding
  return "auto";                                        // Safe to serve
}
```

### Feedback Loop Architecture

```markdown
## User Feedback Collection
1. Thumbs up/down on every AI response
2. Optional: "What was wrong?" (Inaccurate / Incomplete / Off-topic / Other)
3. Track: feedback rate, positive %, negative reasons

## Feedback -> Improvement Loop
1. Weekly: Export all thumbs-down responses
2. Categorize failures (prompt issue / context issue / model limitation)
3. Update eval set with real failures
4. Iterate prompt and re-evaluate
5. Monthly: Report improvement metrics to stakeholders
```

## Context Engineering Patterns

### Data Normalization for AI Consumption

```markdown
## Normalize Before Retrieving
1. Convert PDFs -> clean Markdown with metadata header
2. Convert HTML tables -> Markdown tables
3. Strip navigation, ads, boilerplate from web pages
4. Standardize date formats (ISO-8601)
5. Standardize monetary values (always include currency code)

## Context Window Budget
- System prompt: ~500 tokens (keep lean)
- Retrieved context: ~3000 tokens (top-k relevant chunks)
- User query: ~200 tokens
- Output budget: ~1000 tokens
- Total: ~4700 tokens (well within limits)
```

### Skills as Product Capabilities

Define AI features as modular skills that non-engineers can update:

```markdown
## When to Use Skills Pattern
- Feature logic changes frequently (prompt tuning, new sources)
- Domain experts (analysts, editors) need to modify behavior
- Multiple AI features share similar patterns
- A/B testing different approaches to the same task

## Skill Lifecycle
1. PM writes initial skill spec (what the AI should do)
2. Engineer implements the trigger and context retrieval
3. Domain expert refines the prompt in the SKILL.md file
4. Eval pipeline validates changes automatically
5. Deploy via git (no code deploy required for prompt changes)
```

## Success Criteria

- [ ] AI features have complete prompt specifications with version tracking
- [ ] Evaluation framework covers automated, batch, and human review tiers
- [ ] Adversarial grounding tests verify source attribution accuracy
- [ ] Human-in-the-loop routing uses confidence thresholds
- [ ] Feedback loops connect user signals to eval set improvements
- [ ] Context normalization ensures clean data for retrieval

## Copy/Paste Ready

```
"Write a feature spec for an AI-powered [feature] in the AI assistant"
"Design an evaluation pipeline for our AI summarizer"
"Create a prompt specification for [AI task]"
"How should we handle confidence scoring for AI responses?"
"Spec out a human review workflow for AI-generated content"
```
