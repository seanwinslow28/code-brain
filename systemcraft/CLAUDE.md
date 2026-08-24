# CLAUDE.md — Systemcraft

**Systemcraft — an AI PM system design studio.**

A full-practitioner studio for AI PM system design work: it plans, executes, and builds — and explains every material choice (why A over B, briefly) so the work doubles as demonstration. The machinery is public; the brain is private.

## Status

Scaffold only. The studio is being built along the [Systemcraft build map](https://github.com/seanwinslow28/code-brain/issues/142) — the wayfinder map holds the ratified decisions and the open design tickets. Nothing in this folder is final until its owning ticket closes.

## Layout

| Path | Lane | What lives here |
|---|---|---|
| `bench/` | public | Five specialist seat definitions: Design Strategist, Architecture Advisor, Interaction & Trust Designer, Evals & Evidence Architect, Ops & Economics Modeler |
| `templates/` | public | Artifact templates: PRD, ADR, failure-UX spec + model card, eval plan, ops/economics model + incident runbook |
| `lanes/` | public | Five lane manifests — topic-organized tables of contents (title + pointer + one-line when-to-read) into the private corpus. Shelf labels, never the books: an entry that paraphrases a source's substance belongs in the private lane |
| `corpus/` | **private — gitignored** | Two-layer reference corpus: free-canon distillates + book-to-skill ingests |
| `ledger/` | **private — gitignored** | The decision ledger — every design the studio produces, accreting per engagement |
| master skill | public | Lives in `.claude/skills/` per the house rule; its design is owned by the map's Master skill design ticket |

`bench/` and `templates/` are created by their own map tickets; only the scaffold exists today.

## Non-negotiable rules

1. **Public machinery, private brain.** `corpus/` and `ledger/` are local-only via the PRIVATE LAYER block in the root `.gitignore`. Never `git add` them, never weaken those rules, and never let book-derived text land in a tracked file. Assume every tracked file in this folder is read by a recruiter.
2. **Graceful degradation.** On a machine where the private lanes are absent (fresh clone, employer machine), seats say so plainly and continue on tracked knowledge — they never fabricate citations into a corpus they cannot read.
3. **Explain why.** Every material choice ships with a one-breath why-A-over-B. That behavior is the studio's teaching surface.
4. **Audits run fresh.** An audit is a fresh-context invocation that never sees the drafting conversation; cross-seat audit is preferred where lanes touch; milestone red-team gate passes run on Codex via the codex plugin.
