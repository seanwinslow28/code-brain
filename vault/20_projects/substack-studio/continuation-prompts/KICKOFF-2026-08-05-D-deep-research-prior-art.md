# Kickoff D — Deep research: prior art for the tested-library model + mechanism #1

**Paste this into a fresh Claude Code session in `~/Code-Brain/code-brain`. BLOCKED until Kickoff A (gemini_dr.py migration) is done — verify the migration ticket is closed in `vault/00_inbox/tickets.md` before proceeding; if it is still open, stop and tell Sean to run Kickoff A first. Costed: DR tier caps $7/task, $20/day, $50/month; ALWAYS get Sean's cost confirmation before any live call.**

---

Run Gemini Deep Research (via the `gemini-deep-research` skill / `agents-sdk/scripts/gemini_dr.py`) on the prior art beneath Pencil & Prompt's two riskiest bets. Sean's standing practice: research before locking design decisions with documented prior art.

Context: the 2026-08-04 partner session loose-locked a refocus — masthead thesis "models produce competent-but-convergent output; the publication demonstrates mechanisms that escape the median, failures published honestly"; weekly "Building the Ladder" expedition posts; a public, versioned, TESTED mechanism library (per-entry beat/tied/lost verdicts + public retractions) as the product and lead magnet. Tracking ticket: "Pencil & Prompt refocus — research round before build" in `vault/00_inbox/tickets.md`.

Two DR topics (each is a single compound investigation — right-sized for DR per the repo routing rule; do NOT push these to the local LDR queue, they exceed its 900s budget and citation-grounding ceiling):

**Topic 1 — The tested mechanism library.** What exists today (post-2025 sources weighted) in: prompt/technique libraries with published evaluation results per entry; versioned prompt registries with test suites; "prompt packs" markets and why they are or are not trusted; public benchmarks for creative/divergent LLM output quality; retraction/changelog practices in prompt engineering communities. Deliverable: a landscape matrix (who, what they publish per entry, what evidence standard, gaps) + a cited answer to "does any library publish per-entry tested verdicts with honest failures?"

**Topic 2 — Divergence mechanisms: the research lineage for mechanism #1.** What is documented (papers + credible practice, 2024-2026) on: LLM output homogenization / mode collapse in creative tasks (including studies on brainstorming with LLMs reducing idea diversity); techniques shown to increase output diversity or novelty (structured prompting protocols, persona/frame forcing, adversarial or critic setups, temperature/sampling vs prompt-level interventions, corpus/context injection); and ported human creativity techniques (structured brainstorming methods applied through LLMs) with any measured results. Deliverable: a cited map of which divergence-mechanism families have EVIDENCE behind them vs which are folklore — this directly seeds which "Building the Ladder" rung ships first and what its baseline experiment must measure.

The job:

1. Verify Kickoff A landed (ticket closed, `pytest tests/test_gemini_dr.py` green). If not, stop.
2. Present both topics + tier choice + estimated cost to Sean; fire only on his explicit confirmation. (Both topics on the standard DR tier likely fit ~$7 total; DR Max only if Sean asks.)
3. Run both; outputs land per the script's vault conventions (`vault/20_projects/research/`). Copy or link the reports into `vault/20_projects/substack-studio/research/deep-dives/` with a short header note tying each to the refocus.
4. Write a one-page synthesis at `vault/20_projects/substack-studio/research/2026-08-05-prior-art-synthesis.md`: the 5-8 findings that should change what gets built first, each cited.
5. Update the refocus ticket with a one-line status.

Guardrails: public repo — no personal data. Spend logged to `vault/health/gemini-spend-{YYYY-MM}.json`, stay under caps. Evidence only; the reconvene partner session (named sidecar: `~/.creative-harness/partner-sessions/2026-08-04-pencil-and-prompt-refocus.md`) makes the calls.

Done = both reports in the vault, synthesis written, spend logged, ticket updated.
