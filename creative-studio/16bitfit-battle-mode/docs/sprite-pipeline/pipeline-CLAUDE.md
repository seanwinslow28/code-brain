# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Autonomous, manifest-driven sprite animation generation pipeline for 16BitFit Battle Mode. Generates frame-by-frame animations from gold anchor sprites with hard QA gates, reason-code retries, and Phaser-ready atlas exports.

**Status:** Pre-implementation (planning complete, specs locked)

## Technology Stack

- **Runtime:** Node.js LTS
- **Language:** TypeScript 5+ (Strict Mode)
- **CLI Framework:** oclif 4.x
- **Validation:** Zod
- **Logging:** Pino (JSON-first, structured)
- **Subprocess:** Execa
- **Testing:** Mocha/Chai
- **External:** `@google/generative-ai` SDK, TexturePacker CLI, Phaser (Headless via Puppeteer)

## Build & Development Commands

Once the project is initialized (Story 1.1), these commands will be available:

```bash
# Build
npm run build

# Run tests
npm test

# Run single test
npm test -- --grep "test name"

# Lint
npm run lint

# CLI commands (oclif pattern)
./bin/run pipeline:run --manifest=path/to/manifest.yaml
./bin/run pipeline:doctor
./bin/run pipeline:schema
```

## Architecture

### Directory Structure

```
src/
├── commands/       # CLI entry points (minimal logic, delegate to core)
├── core/           # Orchestrator, RetryManager, StateManager
├── adapters/       # External tool wrappers (Gemini, TexturePacker, Phaser)
├── domain/         # Interfaces, Types, Schemas, Reason Codes
└── utils/          # Logger (Pino wrapper), FS helpers

assets/prompts/     # Versioned prompt templates (never inline in code)
runs/               # Run-specific artifacts (manifests, state, audit logs)
test/               # Mirrors src/ structure
```

### Core Patterns

**Adapter Pattern:** All external tools wrapped in `src/adapters/` implementing typed interfaces. Methods accept a single `Context` object.

**Result Type:** All adapters return `Promise<Result<T, SystemError>>`. Use `Result.ok(value)` or `Result.err(error)`.

**Atomic State:** `StateManager` writes `state.json` via temp-then-rename after every task. Never use `fs.writeFileSync` for state.

**Task Queue:** Single-threaded FIFO queue for determinism.

### Pipeline Stages

1. **Manifest** - Configuration-driven run definition
2. **Choreographer** - Pose spec generation per frame
3. **Generator** - AI frame generation via Gemini with semantic interleaving
4. **Auditor** - Hard fail gates (HFxx) + soft scoring (SFxx)
5. **Retry Ladder** - Bounded retries with reason-code routing (max 4 attempts)
6. **Pack/Export** - TexturePacker to Phaser-ready atlas
7. **Validation** - Phaser micro-tests via Puppeteer

### Reason Codes

- **HFxx (Hard Fail):** Terminal - format, dims, alpha, baseline, anatomy breaks
- **SFxx (Soft Fail):** Retriable - identity drift, palette, temporal coherence
- **SYS_xx / DEP_xx:** System/dependency errors

## Critical Implementation Rules

### Naming Conventions

- **CLI Commands:** `pipeline:run`, `pipeline:doctor` (oclif colon convention)
- **Files:** `kebab-case.ts`
- **TypeScript:** `camelCase` for code/variables/types
- **External Artifacts:** `snake_case` (manifests, logs, state files)

### Generator Rules (Locked Decisions)

- **Semantic Interleaving:** Text labels precede each image in Part[] array
- **Temperature:** Lock to 1.0 (values < 1.0 cause mode collapse)
- **Reference Limit:** Max 2 images (Anchor + Previous Frame)
- **Drift Recovery:** If SF01 < 0.9, drop previous frame from reference stack

### Post-Processor Rules

- **Alignment:** Contact Patch (feet centroid), NOT geometric center
- **Resolution:** Generate at 512px, downsample to 128px with nearest-neighbor
- **Root Zone:** 15% of visible height (not canvas height)
- **Safety Valve:** Clamp shifts to ±32px

### Subprocess Rules

- Use `execa` with array args, never shell strings
- Map failures to `DEP_xx` or `SYS_xx` codes
- Always use `path.join()` for paths

### Determinism

- Sort filesystem lists before iterating
- Record tool versions in `manifest.lock.json`
- Don't assert pixel equality (stochastic); assert traceability

## Anti-Patterns (Never Do)

- Swallow errors without mapping to `SystemError`
- Write state files without atomic-write utility
- Use more than 2 positional parameters (use Context object)
- Invent reason codes outside HFxx/SFxx taxonomy
- Align sprites by bounding box center (causes "moonwalking")
- Use cubic/bilinear for pixel art downsampling
- Include drifted frames (SF01 < 0.9) in reference stack

## Key Reference Documents

- `_bmad-output/project-context.md` - AI agent implementation rules (42 rules)
- `_bmad-output/planning-artifacts/MASTER_ARCHITECTURE_LOCK.md` - Immutable architecture decisions
- `_bmad-output/planning-artifacts/prd.md` - Product requirements
- `_bmad-output/planning-artifacts/architecture.md` - System architecture
- `_bmad-output/planning-artifacts/epics.md` - Implementation epics and stories

## BMAD Method

This project uses BMAD agent workflows. Key commands available via `.bmad/`, `.cursor/commands/`, and `.claude/commands/`.
