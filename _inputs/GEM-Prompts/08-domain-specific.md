# Domain Specific - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - Domain Specific"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at **The Block** — a leading crypto data, news, and research company. Products include a news platform, data dashboards (The Block Data), Campus (education platform), and Simon (AI assistant). I work across product development, content, and operations. I'm a beginner coder learning fundamentals with React, Python, and Supabase.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers **industry-specific and role-specific applications** that don't fit neatly into general PM, creative, or technical categories.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - Domain Specific") contains deep research on using Claude Code for specialized domains: crypto/Web3 product development, education platform development, API product management, RevOps/AdOps automation, and AI-native product development. Sources include industry-specific guides, crypto product development resources, edtech patterns, and emerging AI product practices.

## Your Task

Analyze all sources in this notebook and generate **4-5 Claude Skills** that give Claude Code specialized domain knowledge for my specific industry and role. These skills encode knowledge that Claude may not naturally have in sufficient depth or with the right framing.

## Target Skills to Extract

### 1. Crypto & Web3 Product Context
**Priority**: High
**What to extract**: Blockchain terminology Claude should know when working on The Block's products (DeFi, NFT, L1/L2, TVL, on-chain metrics, gas fees, MEV, staking), crypto market data concepts (price feeds, order books, market cap, volume), industry-specific product patterns (wallet integration, chain indexing, token gating), regulatory awareness (key jurisdictions, compliance concepts), and crypto-specific PM vocabulary (tokenomics, governance, airdrops, liquidity).
**Trigger phrases**: "crypto", "blockchain", "The Block", "DeFi", "on-chain", "token", "Web3", "market data"

### 2. Education Platform (Campus) Patterns
**Priority**: Medium
**What to extract**: LMS (Learning Management System) feature patterns, course content structuring, student progress tracking, educational content generation (lesson outlines, quiz creation, assessment rubrics), onboarding flows for education products, and content curriculum automation. Focus on patterns relevant to The Block's Campus platform (crypto education).
**Trigger phrases**: "Campus", "education", "course content", "LMS", "quiz", "lesson", "curriculum", "learning path"

### 3. API Product Management
**Priority**: Medium
**What to extract**: API documentation generation (OpenAPI/Swagger), endpoint testing workflows, SDK scaffolding, developer experience (DX) optimization, API versioning strategies, rate limiting documentation, and developer portal content creation. Focus on data API products (like The Block Data's API).
**Trigger phrases**: "API docs", "endpoint", "SDK", "developer portal", "API documentation", "Swagger", "OpenAPI"

### 4. RevOps & AdOps Automation
**Priority**: Medium
**What to extract**: Revenue reporting automation (pipeline analysis, revenue tracking, forecast generation), ad operations workflows (campaign setup checklists, performance reporting, yield analysis), CRM integration patterns (Salesforce queries, HubSpot data), and operations metrics dashboards. Focus on automation for a media/data company's revenue operations.
**Trigger phrases**: "RevOps", "AdOps", "revenue report", "pipeline", "ad campaign", "CRM", "Salesforce", "forecast"

### 5. AI-Native Product Development
**Priority**: Lower
**What to extract**: Prompt engineering workflows for product features (designing prompts for production AI features), LLM integration patterns (API calls, streaming, error handling), AI feature development practices (evals, A/B testing AI outputs, user feedback loops), and emerging patterns for building AI-powered products. Relevant to The Block's Simon AI assistant.
**Trigger phrases**: "AI product", "prompt engineering", "LLM integration", "AI feature", "Simon", "AI assistant", "evals"

## Extraction Guidance

- **Industry accuracy matters**: Crypto terminology must be correct. A skill that confuses L1 and L2, or misdefines TVL, loses credibility. Verify domain terms against current usage.
- **The Block context**: Where possible, frame examples around The Block's products (news, data, Campus, Simon). This makes the skills immediately useful rather than generic.
- **PM perspective**: These are product management skills, not engineering skills. Focus on specifications, requirements, documentation, and analysis — not implementation details of blockchain code.
- **Regulatory caution**: For crypto content, include awareness of regulatory sensitivity without attempting to give legal advice. Flag when a PM should consult legal.
- **Data-driven**: The Block is a data company. Skills should emphasize metrics, analytics, and data-informed decision making.
- **Evolving rapidly**: Crypto and AI product development change fast. Skills should be structured to be easily updated as the landscape shifts.

## Cross-Domain Notes

- **Crypto Context** connects to PM Workflows (crypto-specific PRDs), Technical Stack (API development), and Life Optimization (crypto portfolio tracking)
- **Education Platform** connects to PM Workflows (product specs), Creative Projects (educational video content), and Remotion Mastery (course animations)
- **API Product Management** connects to Technical Stack (development), PM Workflows (documentation), and Core Features (headless mode for API testing)
- **RevOps/AdOps** connects to PM Workflows (reporting), Life Optimization (data analysis patterns), and Technical Stack (Salesforce/CRM APIs)
- **AI-Native Products** connects to Core Features (understanding Claude's capabilities), Advanced Techniques (prompt optimization), and Technical Stack (API integration)

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Use correct, current industry terminology (crypto moves fast — avoid outdated terms)
- Frame everything from a PM perspective, not an engineer's perspective
- Be specific to The Block's context where possible (news, data, Campus, Simon)
- Include glossary/terminology sections where domain vocabulary is critical
- Be maintainable — structured so terminology updates don't require full rewrites

---

## PROMPT END
