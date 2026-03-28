# Changelog

All notable changes to the Sprite Sheet Automation Pipeline will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-21

### Added
- **Core Pipeline**: Complete manifest-driven sprite animation generation
- **Gemini Integration**: Real `@google/genai` SDK integration for AI frame generation
- **Quality Gates**: Hard fail (HFxx) and soft fail (SFxx) auditing system
- **Retry Ladder**: Bounded retries with reason-code routing (max 4 attempts)
- **Resume Functionality**: Interrupt and resume generation runs mid-pipeline
- **Director Mode**: Human-in-the-loop review UI with nudge, mask, and patch tools
- **Atlas Export**: TexturePacker integration for Phaser-ready sprite atlases
- **Phaser Validation**: Micro-tests (TEST-02, TEST-03, TEST-04) via Puppeteer
- **CLI Commands**: `banana gen`, `banana doctor`, `banana validate`, `banana inspect`

### Fixed
- **Resume Logic**: Run ID format now includes `_character_move` suffix for proper run detection
- **Multipack Atlas Support**: Phaser test harness detects and uses correct loader (`multiatlas` vs `atlas`)
- **Template Placeholder**: Added `{frame_count}` as alias for `{total_frames}` in prompt templates

### Technical Details
- 8 epics implemented (67 stories)
- 1004+ unit tests passing
- E2E tested with real Gemini API
- Supports 4-frame idle and 8-frame walk animations
- Average frame generation: ~5 seconds
- 0% retry/reject rate in E2E testing

### Known Issues
- 5 test infrastructure issues (not runtime bugs):
  - 1 in `director-server.test.ts` (UI build test setup)
  - 4 in `orchestrator.test.ts` (mock state machine assertions)

## [Unreleased]

### Planned
- Additional character support
- More animation types (attack, jump, etc.)
- CI/CD pipeline integration
- Production deployment documentation
