"""skill_optimizer — autoresearch optimization harness for Claude Code skills.

Adapted from Karpathy's autoresearch pattern (March 2026). Optimizes the body
of a SKILL.md file against a hybrid eval suite (deterministic structural checks
+ LLM-judge binary evaluations) via an autonomous mutate→score→keep-or-revert
loop. See docs/superpowers/specs/2026-05-09-writing-voice-modes-autoresearch-design.md.
"""
