---
name: claude-md-optimization
description: CLAUDE.md optimization and configuration. Creates effective project instruction files, maintains the configuration hierarchy, avoids context bloat anti-patterns, and uses modular imports to keep token usage efficient.
---

# CLAUDE.md Optimization

## Purpose

Create and maintain high-signal, low-noise CLAUDE.md files that give Claude Code the project context it needs without wasting tokens. Apply the configuration hierarchy correctly, avoid anti-patterns that bloat context, and use modular imports to keep the main file under 300 lines.

## When to Use

- Setting up a new project with Claude Code
- Claude keeps ignoring project-specific rules or conventions
- CLAUDE.md has grown beyond 300 lines and needs trimming
- Structuring a monorepo with per-package instructions
- Any time you mention "CLAUDE.md", "project instructions", "configure project", or "Claude keeps ignoring"

## Examples

**Example 1: New project setup**
```
User: "Set up CLAUDE.md for my Next.js e-commerce app"
Claude: [Uses claude-md-optimization]
Generates a lean CLAUDE.md with architecture map, build commands, code style
rules, and security gates. Under 300 lines. Uses @imports for database
schema and deployment docs.
```

**Example 2: Fixing ignored instructions**
```
User: "Claude keeps using npm instead of pnpm"
Claude: [Uses claude-md-optimization]
Adds "Use pnpm, never npm" to CLAUDE.md under Core Commands. Explains
the "update on friction" pattern — every correction should become a rule.
```

## The Configuration Hierarchy

Claude Code loads instruction files in a specific precedence order:

| Level | Location | Purpose | Override |
| :--- | :--- | :--- | :--- |
| Enterprise | `/etc/claude-code/CLAUDE.md` | Org-wide policies | Cannot be overridden |
| Global | `~/.claude/CLAUDE.md` | Personal defaults, security | All projects |
| Project | `./CLAUDE.md` | Team standards (committed to git) | This repo |
| Local | `CLAUDE.local.md` | Personal overrides (gitignored) | This repo, you only |
| Subdirectory | `src/api/CLAUDE.md` | Module context | Loaded only in that directory |

**Monorepo pattern:** In `root/packages/frontend`, Claude loads BOTH `root/CLAUDE.md` AND `root/packages/frontend/CLAUDE.md`. Keep the root lean and push framework-specific rules into subfolders.

## Token Budget

- **Target:** Under 300 lines
- **Allocation:** Architecture (~25 lines), decisions (~25), patterns (~25), gotchas (~20), commands (~15)
- **If a section overflows:** Move details to an external file and reference via `@import`
- **Filename:** Must be exactly `CLAUDE.md` (all caps)

## What to Include

Focus on context Claude cannot infer from the code itself:

- **Commands:** Exact strings for build, test, lint. Do not let Claude guess arguments
- **Architecture:** One-liner project description and high-level folder map
- **Non-obvious gotchas:** Weird retry logic, specific header requirements, files that must never be edited
- **Style preferences:** TypeScript strictness, naming conventions, preferred libraries
- **Security gates:** Explicit "NEVER" rules (e.g., "NEVER commit .env files")

## What NOT to Include

- Standard language conventions (Python indentation, basic React hooks)
- Tutorials or "how-to" guides
- Large file dumps (entire API specs, database schemas)
- Generic advice ("Write clean code", "Be efficient")
- Frequently changing information (active ticket numbers)

## The @import System

Keep CLAUDE.md lean by referencing external files. Claude reads them only when relevant:

```markdown
See @docs/database-schema.md for table definitions.
See @docs/deployment-procedures.md for release checklists.
```

## Template: Project Root CLAUDE.md

```markdown
# Project: ShopFront (Next.js 14 E-commerce)
Context: Next.js App Router, Stripe payments, Prisma ORM, Tailwind CSS.

## Architecture
- `/app`: Next.js App Router pages/layouts
- `/lib`: Shared utilities (Pure functions only)
- `/components/ui`: Radix UI primitives (Do not modify logic here)
- `/prisma`: Database schema

## Commands
- Dev: `npm run dev` (Port 3000)
- Test: `npm run test` (Jest)
- Lint: `npm run lint` (ESLint + Prettier)
- DB: `npx prisma migrate dev`

## Code Style
- **Strict TypeScript**: No `any`. Define interfaces in `/types`.
- **Imports**: Use named exports. Use `@/` alias for root imports.
- **Styling**: Tailwind utility classes only. No CSS modules.
- **Async**: Always use `async/await`, never `.then()` chains.

## Critical Rules
- NEVER commit `.env` files.
- Verify stripe webhook signatures in `/app/api/webhooks`.
- Images are hosted on Cloudinary, not local `/public`.
```

## Template: Global Security CLAUDE.md

Place in `~/.claude/CLAUDE.md` to apply across all projects:

```markdown
# Global Identity and Security Rules

## Identity
- Git User: "Sean Winslow"
- Email: "sean@example.com"

## SECURITY GATES (ABSOLUTE)
1. Secrets: NEVER output real API keys, passwords, or tokens in chat.
2. Environment: NEVER commit `.env` files to git. Always check `.gitignore`.
3. Deprecations: Treat deprecation warnings as build failures.
```

## CLAUDE.md vs Skills

| Aspect | CLAUDE.md | Skills |
| :--- | :--- | :--- |
| Loading | Always on (every session) | On demand (triggered by description match) |
| Use for | Rules for every interaction | Complex tasks needed occasionally |
| Token cost | Constant (every prompt) | Zero when not triggered |

If a piece of context is only needed occasionally (e.g., "Deploy to AWS"), put it in a Skill. If it applies to every interaction (formatting, commands, file structure), put it in CLAUDE.md.

## Update Cadence

1. **Start fast:** Run `/init` to generate a baseline, then delete the fluff
2. **Update on friction:** Every time you correct Claude, add the rule to CLAUDE.md immediately
3. **Review periodically:** Ask Claude: "Review this CLAUDE.md and suggest removals for redundant or obsolete instructions"

## Success Criteria

- [ ] CLAUDE.md is under 300 lines
- [ ] Every rule is actionable and specific (no generic advice)
- [ ] Heavy reference material lives in @imported files, not inline
- [ ] Security gates are defined with explicit "NEVER" rules
- [ ] Configuration hierarchy is used correctly (global vs project vs local)

## Copy/Paste Ready

```
"Create a CLAUDE.md for this project"
"Optimize my CLAUDE.md — it's too long"
"Set up the global security CLAUDE.md"
"Why does Claude keep ignoring my project rules?"
"Help me structure CLAUDE.md for a monorepo"
```
