---
name: team-styleguide
description: Team coding standards and style guide enforcer. Auto-detects project conventions from config files (ESLint, Prettier, tsconfig, .editorconfig), validates code against them, and provides language-specific rules for naming, imports, file structure, and comments. Use when asked to "check style", "review code style", "enforce standards", "format code", or "apply styleguide".
---

# Team Styleguide

## Purpose

Enforce consistent coding standards across a team's codebase. Auto-detects project conventions from configuration files, validates code against them, and provides actionable feedback. Works with any language or framework by reading the project's own config.

## When to Use

- **Code review:** "Check this code against our style guide"
- **New code:** "Does this match our conventions?"
- **Onboarding:** "What are this project's coding standards?"
- **Enforcement:** "Apply our style guide to this file"
- **Setup:** "Help set up a style guide for this project"

## Auto-Detection

Before enforcing rules, detect what the project already uses:

### Config Files to Check

| File | What It Tells You |
|------|-------------------|
| `.eslintrc.*` / `eslint.config.*` | JS/TS linting rules, import ordering |
| `.prettierrc*` | Formatting: tabs/spaces, quotes, semicolons, line width |
| `tsconfig.json` | TypeScript strictness, path aliases |
| `.editorconfig` | Indent style/size, trailing whitespace, final newline |
| `pyproject.toml` / `setup.cfg` | Python tools (black, ruff, isort, mypy) |
| `Cargo.toml` / `rustfmt.toml` | Rust formatting rules |
| `.rubocop.yml` | Ruby style rules |
| `package.json` (scripts) | Which tools are configured (lint, format, typecheck) |

### Detection Workflow

1. Check for config files in project root
2. Read existing rules from configs
3. Supplement with language defaults where configs are silent
4. Present detected conventions before enforcing

```
Detected project conventions:
- Formatter: Prettier (2-space indent, single quotes, no semicolons)
- Linter: ESLint with @typescript-eslint
- Types: TypeScript strict mode
- Import order: external → internal → relative
- No .editorconfig found — using Prettier defaults
```

## Universal Rules

These apply regardless of language:

### Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Files (components) | PascalCase | `UserProfile.tsx` |
| Files (utilities) | camelCase or kebab-case | `formatDate.ts` or `format-date.ts` |
| Files (styles) | Match component | `UserProfile.module.css` |
| Files (tests) | Match source + suffix | `UserProfile.test.tsx` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Env variables | UPPER_SNAKE_CASE | `DATABASE_URL` |

**Match the project's existing convention.** If the project uses kebab-case files, don't introduce PascalCase.

### Imports

**Order** (most common convention):

1. Built-in/Node modules (`fs`, `path`, `react`)
2. External packages (`lodash`, `axios`)
3. Internal aliases (`@/components`, `~/utils`)
4. Relative imports (`./Button`, `../utils`)
5. Style imports (`./styles.css`)

Separate each group with a blank line.

### Comments

| Do | Don't |
|----|-------|
| Explain *why* something exists | Explain *what* code does (let code speak) |
| Document non-obvious business logic | Comment every function |
| Note workarounds with issue links | Leave `// TODO` without context |
| Use JSDoc for public APIs | Comment out dead code |

### File Structure

Follow the project's existing structure. Common patterns:

```
# Feature-based (recommended for most React/Vue projects)
src/
  features/
    auth/
      components/
      hooks/
      utils/
      index.ts
    dashboard/
      ...

# Layer-based (common in backend projects)
src/
  controllers/
  services/
  models/
  middleware/
  routes/
```

## Language-Specific Rules

### TypeScript / JavaScript

| Rule | Preferred | Avoid |
|------|-----------|-------|
| Type assertions | `as Type` | `<Type>` (conflicts with JSX) |
| Null checks | Optional chaining `?.` | Nested ternaries |
| Type definitions | `interface` for objects, `type` for unions | Inconsistent mixing |
| Enums | `const enum` or string unions | Numeric enums |
| Async | `async/await` | Raw `.then()` chains |
| Equality | `===` / `!==` | `==` / `!=` |

### Python

| Rule | Preferred | Avoid |
|------|-----------|-------|
| Formatter | Black (or Ruff format) | Manual formatting |
| Imports | isort ordering | Unordered imports |
| Type hints | All function signatures | Untyped public functions |
| Strings | f-strings | `.format()` or `%` |
| Docstrings | Google or NumPy style | No docstrings on public API |

### CSS / Tailwind

| Rule | Preferred | Avoid |
|------|-----------|-------|
| Class ordering | Tailwind official order plugin | Random class order |
| Custom properties | Design tokens (`--color-primary`) | Hardcoded hex values |
| Nesting | Max 3 levels | Deeply nested selectors |
| Units | `rem` for sizing, `px` for borders | Mixed units without reason |

## Review Workflow

### Step 1: Detect Conventions

Read project config files. Report what was detected.

### Step 2: Check Code

For each file under review:

```
Style Review — src/components/UserProfile.tsx

[PASS] Naming: PascalCase component file
[PASS] Imports: Correct order (react → external → internal → relative)
[WARN] Line 34: Magic number 86400 — extract to named constant
[WARN] Line 67: Commented-out code block — remove or restore
[PASS] Types: All props typed via interface
[FAIL] Line 12: Using `var` — use `const` or `let`
```

### Step 3: Provide Fixes

For each issue, provide the specific fix:

```
Line 34: Extract magic number
- const SECONDS_PER_DAY = 86400
+ const expiresIn = SECONDS_PER_DAY * 7

Line 67: Remove dead code
- // const oldHandler = () => { ... }

Line 12: Replace var
- var count = 0
+ let count = 0
```

## Setting Up a Style Guide

For projects without existing config:

### Minimal Setup (any JS/TS project)

```json
// .prettierrc
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "all",
  "printWidth": 100
}
```

```
// .editorconfig
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true
```

### Recommended Tools by Language

| Language | Formatter | Linter | Type Checker |
|----------|-----------|--------|-------------|
| TypeScript | Prettier | ESLint | tsc --strict |
| Python | Black/Ruff | Ruff | mypy/pyright |
| Rust | rustfmt | clippy | Built-in |
| Go | gofmt | golangci-lint | Built-in |

## Examples

**Example 1: Code style review**
```
User: "Check this file against our style guide"
Claude: [Uses team-styleguide]

Detecting project conventions...
Found: .prettierrc (2-space, single quotes), ESLint with TypeScript

Reviewing src/api/users.ts:
[PASS] Naming conventions followed
[WARN] Line 23: Import order — move 'axios' above internal imports
[WARN] Line 45: Function exceeds 50 lines — consider extracting
[PASS] All types declared
[PASS] No debug code

2 warnings, 0 errors. Suggested fixes provided above.
```

**Example 2: Detect conventions**
```
User: "What are this project's coding standards?"
Claude: [Uses team-styleguide]

Scanning project config files...

Detected conventions:
- Formatter: Prettier (tabs, double quotes, semicolons)
- Linter: ESLint (airbnb config + TypeScript)
- Types: TypeScript strict mode with no-any rule
- Imports: Auto-sorted by eslint-plugin-import
- Tests: Jest with .test.ts suffix
- CSS: Tailwind with custom design tokens
- Git: Conventional commits (commitlint configured)
```

**Example 3: New project setup**
```
User: "Help set up a style guide for our new Node.js project"
Claude: [Uses team-styleguide]

I'll create a minimal but effective setup:
1. .prettierrc — formatting rules
2. .eslintrc — linting rules
3. .editorconfig — editor consistency
4. package.json scripts — lint, format, typecheck commands

[Generates config files tailored to the project]
```

## Success Criteria

- [ ] Project conventions auto-detected from config files
- [ ] Style issues identified with specific line numbers
- [ ] Fixes provided as before/after code snippets
- [ ] Existing project conventions respected (don't override)
- [ ] Language-appropriate rules applied
- [ ] False positives minimized (don't flag intentional patterns)

## Copy/Paste Ready

```
"Check this code against our style guide"
"What are this project's coding standards?"
"Review this PR for style issues"
"Help set up a style guide for this project"
"Apply our conventions to this file"
"Is this naming consistent with our codebase?"
```