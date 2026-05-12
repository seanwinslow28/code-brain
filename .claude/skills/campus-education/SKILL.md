---
name: campus-education
description: Education platform and LMS development patterns for a crypto education / LMS platform. Generates course structures, lesson outlines, quiz rubrics, student progress tracking, and curriculum automation. Use when building education features, creating course content, designing learning paths, generating quizzes or assessments, or working on LMS platform specifications.
---

# Education Platform Patterns

## Purpose

Provide LMS development patterns, content generation workflows, and assessment rubrics tailored for a crypto education / LMS platform. Enable Claude to generate properly structured courses, quizzes, and curriculum specifications with crypto-domain accuracy.

## When to Use

- Designing course structures or learning paths for the LMS
- Generating lesson outlines, quiz questions, or assessment rubrics
- Specifying student progress tracking features
- Building onboarding flows for education products
- Automating curriculum content from crypto research
- Writing PRDs for LMS platform features

## Examples

**Example 1: Course structure generation**
```
User: "Create a course outline for 'Introduction to DeFi' on the LMS"
Claude: [Uses campus-education]

# Introduction to DeFi - Course Structure

## Module 1: What is DeFi? (Week 1)
- Lesson 1.1: Traditional Finance vs Decentralized Finance
- Lesson 1.2: Key DeFi Primitives (Lending, Trading, Yield)
- Lesson 1.3: Smart Contracts as Financial Infrastructure
- Quiz 1: Concept Check (5 questions, easy difficulty)

## Module 2: DEX and AMM Mechanics (Week 2)
- Lesson 2.1: How Automated Market Makers Work
- Lesson 2.2: Liquidity Pools and Impermanent Loss
- Lesson 2.3: Comparing DEX Models (Uniswap v3 vs Curve)
- Quiz 2: Applied Understanding (5 questions, medium difficulty)
- Lab: Calculate impermanent loss for a given scenario

## Module 3: Lending Protocols (Week 3)
...

## Assessment: Final Project
- Type: Analysis Report
- Prompt: "Evaluate a DeFi protocol using the Token Analysis Framework"
- Rubric: CIDPP (Clarity, Integrity, Depth, Practicality, Pertinence)
```

**Example 2: Quiz generation with rubric**
```
User: "Generate a quiz on staking for the LMS"
Claude: [Uses campus-education]

## Quiz: Proof of Stake Fundamentals

**Q1 (2pts):** What happens to a validator's staked tokens if they
produce an invalid block?
- A) Nothing, they keep validating
- B) They are "slashed" — a portion of staked tokens is destroyed [CORRECT]
- C) They receive reduced rewards for one epoch
- D) Their tokens are returned and they are removed

**Rubric:** Full marks for B. Partial credit (1pt) if student selects C
(shows awareness of penalties but incorrect mechanism).
```

## Course Structure Template

### Standard LMS Course Format

```markdown
# [Course Title]

## Course Metadata
- Duration: [N weeks]
- Difficulty: Beginner | Intermediate | Advanced
- Prerequisites: [List or "None"]
- Learning Outcomes: [3-5 measurable outcomes]

## Module [N]: [Module Title] (Week [N])

### Lesson [N.1]: [Lesson Title]
- **Type:** Reading | Video | Interactive
- **Duration:** [15-30 min]
- **Key Concepts:** [3-5 terms]
- **Content Source:** [Whitepaper / Research Report / Original]

### Lesson [N.2]: [Lesson Title]
...

### Assessment: [Quiz / Lab / Project]
- **Type:** Multiple Choice | Free Response | Analysis
- **Questions:** [N]
- **Passing Score:** [70% | 80%]
- **Rubric:** [CIDPP or custom]
```

## Assessment and Rubric System

### CIDPP Five-Dimensional Evaluation

Use this rubric framework for all LMS assessments. Score each dimension 1-5:

| Dimension | What it Measures | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|-----------|-----------------|----------|---------------|----------------|
| Clarity | Can the answer be understood? | Incoherent or jargon soup | Understandable with effort | Crystal clear, well-organized |
| Integrity | Is it factually accurate? | Contains errors | Mostly correct, minor gaps | Fully accurate, well-sourced |
| Depth | Does it go beyond surface? | Surface-level only | Shows understanding | Demonstrates nuanced insight |
| Practicality | Is it actionable? | Purely theoretical | Some applied thinking | Ready to implement |
| Pertinence | Does it answer the question? | Off-topic | Related but tangential | Directly addresses prompt |

### Quiz Question Template

```markdown
**Q[N] ([points]pts):** [Question text]
- A) [Option - include common misconception]
- B) [Option]
- C) [Correct answer] [CORRECT]
- D) [Option - plausible but wrong]

**Grading Notes:**
- Full marks: [C]
- Partial credit ([N]pt): [Condition]
- Common mistake: [What students get wrong and why]
```

### Automated Grading Prompt Template

Use this prompt structure for LLM-graded free-response questions:

```markdown
**System:** You are a grading assistant for an education platform.
Grade submissions based on the rubric. Be encouraging but accurate.

**User:**
<Question>
[Question text]

<Correct Answer>
[Model answer with key points]

<Grading Rubric>
- Criterion A ([N] pts): [What to look for]
- Criterion B ([N] pts): [What to look for]
- Criterion C ([N] pts): [What to look for]

<Student Submission>
{student_text}

<Output Format>
{
  "criteria_satisfied": ["A", "C"],
  "score": [N],
  "max_score": [N],
  "feedback": "[Specific, constructive feedback]"
}
```

## Curriculum Automation Patterns

### Multi-Agent Curriculum Optimization

Use three specialized agents to continuously improve course quality:

1. **Evaluator Agent**: Assess student mastery from quiz results and interaction logs. Flag modules with pass rates below 70%.
2. **Optimizer Agent**: Refine lesson content based on Evaluator feedback. Add examples for commonly missed concepts. Adjust difficulty pacing.
3. **Analyst Agent**: Scan student submissions for recurring error patterns. Generate "Common Mistakes" addenda for problem modules.

### Content Generation from Research

Convert crypto research into educational content:

```markdown
## Content Pipeline

1. **Ingest:** Normalize source (whitepaper, research report, blog post)
   into clean Markdown with JSON metadata
2. **Structure:** Map to learning objectives using Bloom's taxonomy:
   - Remember: Vocabulary and definitions
   - Understand: Concept explanations with analogies
   - Apply: Scenario-based exercises
   - Analyze: Compare/contrast frameworks
3. **Generate:** Create lesson content hitting each taxonomy level
4. **Validate:** Cross-reference all facts against primary sources
5. **Assess:** Generate quiz questions targeting each objective
```

### Skill-Tree Progress Model

Model student progress as a directed graph, not a linear sequence:

```typescript
interface SkillNode {
  id: string;
  title: string;
  prerequisites: string[];  // IDs of required prior nodes
  assessments: Assessment[];
  mastery_threshold: number; // 0-100, score to "unlock" next nodes
  status: "locked" | "available" | "in_progress" | "mastered";
}

interface LearningPath {
  student_id: string;
  nodes: SkillNode[];
  current_mastery: Record<string, number>; // node_id -> score
}

// Example skill tree for DeFi curriculum
const defiSkillTree: SkillNode[] = [
  {
    id: "wallet-basics",
    title: "Wallet Security Fundamentals",
    prerequisites: [],
    assessments: [{ type: "quiz", questions: 5 }],
    mastery_threshold: 80,
    status: "available",
  },
  {
    id: "defi-lending",
    title: "DeFi Lending Mechanics",
    prerequisites: ["wallet-basics"],
    assessments: [{ type: "quiz", questions: 5 }, { type: "lab", task: "Calculate collateral ratio" }],
    mastery_threshold: 70,
    status: "locked",
  },
  {
    id: "smart-contract-audit",
    title: "Smart Contract Auditing Basics",
    prerequisites: ["wallet-basics", "defi-lending"],
    assessments: [{ type: "project", rubric: "CIDPP" }],
    mastery_threshold: 75,
    status: "locked",
  },
];
```

## Onboarding Flow Specification

### New Student Onboarding Template

```markdown
## Onboarding Interview Questions

1. **Experience Level:**
   - "Have you used cryptocurrency before?" (Never / Held tokens / Used DeFi / Developer)

2. **Learning Goal:**
   - "What do you want to learn?" (Investing basics / DeFi mechanics / Building on-chain / Career in crypto)

3. **Time Commitment:**
   - "How much time per week?" (1-2 hrs / 3-5 hrs / 5+ hrs)

## Path Assignment Logic

| Experience | Goal | Recommended Path |
|-----------|------|-----------------|
| Never | Investing | Crypto Fundamentals (8 weeks) |
| Never | Career | Crypto Fundamentals + Industry Overview (12 weeks) |
| Held tokens | DeFi | DeFi Deep Dive (6 weeks) |
| Used DeFi | Building | Smart Contract Basics (8 weeks) |
| Developer | Building | Advanced Protocol Development (6 weeks) |
```

## Success Criteria

- [ ] Course structures follow the standard LMS template
- [ ] All quizzes include grading rubrics with partial credit guidance
- [ ] Assessment rubrics use the CIDPP framework
- [ ] Crypto terminology is accurate and current
- [ ] Content pipeline includes fact-checking against primary sources
- [ ] Skill-tree progression model defines clear prerequisites

## Copy/Paste Ready

```
"Create a course outline for the LMS on [topic]"
"Generate a quiz with rubric for the [topic] module"
"Design a learning path for beginner crypto students"
"Write assessment criteria for a DeFi analysis project"
"Spec out the student progress dashboard for the LMS"
```
