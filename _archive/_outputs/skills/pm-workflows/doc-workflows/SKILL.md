---
name: doc-workflows
description: Documentation workflow assistant for code and product documentation. Generates READMEs, API docs, knowledge base articles, and maintains doc-code sync. Use when asked to write documentation, update docs, generate a README, create API docs, build a knowledge base article, or document code changes.
---

# Documentation Workflows

## Purpose

Automate documentation generation and maintenance for codebases and products. Generate READMEs, API documentation, knowledge base articles, and keep docs in sync with code changes. Implement doc-driven development patterns where specs are written before code.

## When to Use

- User asks to write or update documentation
- User needs a README generated for a project or module
- User asks to create API documentation
- User wants to document code changes or architecture decisions
- User needs a knowledge base article or wiki page
- User asks to keep docs in sync with code
- User wants to implement llms.txt for AI-friendly documentation

## Examples

**Example 1: README generation**
```
User: "Generate a README for this project"
Claude: [Uses doc-workflows] I'll analyze the project structure:

- Detected: TypeScript/React project with Supabase backend
- Package.json scripts: dev, build, test, lint
- Environment variables: 4 required (.env.example found)

# Project Name

## Overview
[Generated from package.json description and CLAUDE.md]

## Quick Start
```bash
npm install
cp .env.example .env  # Fill in required values
npm run dev
```

## Architecture
[Generated from directory structure analysis]

## API Reference
[Generated from route files]
```

**Example 2: Doc sync after code changes**
```
User: "I just refactored the auth module, update the docs"
Claude: [Uses doc-workflows] Analyzing changes:

Files modified:
- src/auth/jwt.ts (renamed from auth.ts)
- src/auth/middleware.ts (new file)
- src/routes/login.ts (updated imports)

Documentation updates needed:
1. docs/architecture.md - Update auth module description
2. docs/api/auth.md - Add middleware documentation
3. README.md - Update project structure section

[Makes targeted edits to each doc file]
```

**Example 3: Knowledge base article**
```
User: "Write a knowledge base article on how our webhook system works"
Claude: [Uses doc-workflows]

# Webhook System

## Overview
[How it works in plain language]

## Setup Guide
[Step-by-step for new team members]

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Webhooks not firing | Missing API key | Check .env |
| Duplicate events | No idempotency key | Add event ID check |

## Architecture
[Mermaid diagram of webhook flow]
```

## README Generation Workflow

### Step 1: Analyze the Project

Scan these files to understand the project:

```
Priority order:
1. package.json / pyproject.toml / Cargo.toml (name, description, scripts)
2. CLAUDE.md (project conventions and architecture)
3. .env.example (required configuration)
4. src/ directory structure (architecture)
5. Existing docs/ directory (prior documentation)
```

### Step 2: Generate README Sections

```markdown
# [Project Name]

[1-2 sentence description from package.json or CLAUDE.md]

## Quick Start

```bash
# Prerequisites
[Detected runtime and version]

# Installation
[Package manager install command]

# Configuration
[Environment variable setup]

# Run
[Dev server command]
```

## Architecture

```
[Generated directory tree with annotations]
```

## Development

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Production build |
| `npm run test` | Run test suite |
| `npm run lint` | Lint and format |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Supabase connection string |
| `API_KEY` | Yes | External service API key |

## Contributing

[Standard contributing guidelines]
```

### Step 3: Validate

- Every command listed must exist in package.json scripts
- Every environment variable must exist in .env.example
- Directory tree must match actual structure
- No placeholder text remaining

## API Documentation Workflow

### From Route Files

Scan route handlers and generate documentation:

```markdown
## API Reference

### POST /api/v1/users

**Auth:** Bearer token required
**Rate Limit:** 100/min

**Request Body:**
```json
{
  "email": "string (required)",
  "name": "string (required)",
  "role": "admin | member (default: member)"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "email": "string",
  "createdAt": "ISO8601"
}
```

**Errors:**
| Status | Description |
|--------|-------------|
| 400 | Validation error |
| 409 | Email already exists |
```

### From OpenAPI Specs

For large APIs, refactor monolithic specs into modular files:

1. Identify common patterns (auth, pagination, error responses)
2. Extract into shared components
3. Generate human-readable docs from the spec
4. Detect breaking changes between spec versions

## Knowledge Base Articles

### Template

```markdown
# [Topic Title]

## Overview
[What this is and why it matters - 2-3 sentences]

## How It Works
[Technical explanation appropriate to audience]

## Setup Guide
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Common Tasks

### [Task 1]
[Step-by-step instructions]

### [Task 2]
[Step-by-step instructions]

## Troubleshooting

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| [Problem] | [Cause] | [Fix] |

## FAQ
**Q: [Common question]**
A: [Answer]

## Related Articles
- [Link to related topic]
```

## Doc-Driven Development

Write documentation before code to clarify requirements:

1. **Spec first:** Write the technical spec (use prd-generator skill)
2. **API contract:** Define endpoints, request/response schemas
3. **Test cases:** Write test descriptions from acceptance criteria
4. **Implement:** Code to match the documented spec
5. **Verify:** Compare implementation against documentation

Configure in CLAUDE.md:
```markdown
## Documentation Standards
- Always check docs/specs/ for feature definitions before proposing code changes
- All exported functions must have JSDoc comments
- API changes require docs/api/ updates in the same PR
```

## Doc-Code Sync Patterns

### PostToolUse Hook

Trigger documentation updates when code files change:

```bash
#!/bin/bash
# .claude/hooks/doc-sync.sh
# Trigger: PostToolUse on edit/write to src/ files

MODIFIED_FILE="$1"
if [[ "$MODIFIED_FILE" == src/api/* ]]; then
  echo "API file modified. Consider updating docs/api/ to match."
fi
```

### CI/CD Integration

Add documentation checks to your pipeline:

1. **Doc coverage:** Fail if new routes/components lack documentation
2. **Link checker:** Validate internal doc links on every PR
3. **Changelog:** Auto-generate from PR descriptions and commit messages
4. **Freshness:** Flag docs not updated in >90 days for review

### Architecture Decision Records (ADRs)

Document significant technical decisions:

```markdown
# ADR-[NNN]: [Decision Title]

**Date:** [Date]
**Status:** Accepted | Superseded | Deprecated

## Context
[Why this decision was needed]

## Decision
[What was decided]

## Consequences
- [Positive consequence]
- [Negative consequence or trade-off]
- [Neutral observation]
```

## llms.txt for AI-Friendly Docs

Make documentation discoverable by AI tools:

### Structure

Create two files at the project root:

**llms.txt** (index file):
```
# Project Name

> Brief description of the project

## Documentation
- [Getting Started](docs/getting-started.md): Setup and installation guide
- [API Reference](docs/api.md): Complete API documentation
- [Architecture](docs/architecture.md): System design and patterns

## Optional
- [Contributing](CONTRIBUTING.md): How to contribute
- [Changelog](CHANGELOG.md): Version history
```

**llms-full.txt** (concatenated content):
Full documentation content in a single file for LLM ingestion.

### Best Practices

- Use Markdown (token-efficient, reduces hallucination vs HTML)
- Keep llms.txt concise with one-sentence descriptions
- Update llms-full.txt when any doc file changes
- Use descriptive section headers (LLMs use these for navigation)

## Documentation Review Checklist

Run before publishing any documentation:

- [ ] **Accuracy:** Does the doc match the current code?
- [ ] **Completeness:** Are all required sections present?
- [ ] **Clarity:** Can a new team member follow this without help?
- [ ] **Currency:** Are version numbers and dependencies current?
- [ ] **Links:** Do all internal links resolve?
- [ ] **Examples:** Do code examples actually work?
- [ ] **Formatting:** Consistent heading levels, code blocks, tables?

## Success Criteria

- [ ] Documentation matches the current state of the code
- [ ] README contains working quick-start instructions
- [ ] API docs cover all public endpoints with request/response examples
- [ ] No placeholder text or TODO items in published docs
- [ ] llms.txt index is current if implemented
- [ ] ADRs exist for significant architectural decisions
- [ ] Documentation review checklist passes

## Copy/Paste Ready

```
"Generate a README for this project"
"Document the API endpoints in src/routes/"
"Write a knowledge base article about our auth system"
"Update the docs to reflect the refactoring I just did"
"Create an ADR for our decision to switch to Supabase"
"Set up llms.txt for this project"
```
