---
type: operating-model
artifact: schedule-recommendations
domain: [creative-studio]
status: confirmed
last_interviewed: 2026-04-21
created: 2026-04-18
review-date: null
ai-context: "Friction-derived schedule and automation rules for creative work. The extra-hour target is Vault-as-SSoT buildout. Biggest active friction: research-app context switching, three-machine sync, and the fact that the agent fleet currently doesn't function in creative-studio. Populated by the work-operating-model skill. Consumed by meeting-defender and future calendar agents."
---

# Schedule Recommendations — Creative Studio

## Protect
_When X, then Y. Calendar-level defenses for deep creative work._
- When it's **Saturday or Sunday with no plans**, then default to deep implementation — don't burn the weekend on research; research belongs to weekdays.
- When it's a **weekday between 3 PM and end-of-day**, then creative-studio is open but in research/inspiration mode — guardrail against starting heavy implementation that won't get finished.
- When a project is **close to finishing**, then apply the close-the-gap rule — protect that session against new-tool distractions until it ships.
- When the **current creative project starts to feel like grinding**, then permit a pivot to a different creative thread. Don't force focus; project-hopping is protective (respect the 16BitFit-V3 signal).
- When a **new AI tool lands mid-week**, then cap its impact — test it in a scoped sandbox, don't rebuild any pipeline around it until it's proven.

## Automate
_Manual creative-pipeline steps that should become agent-triggered. Each one traces back to a Layer 5 answer._

**Research pipeline consolidation**
- Build the **Claude Research Skill**: wire Perplexity API + Google search MCP + NotebookLM MCP (+ Gemini Deep Research API, any cheaper open-source equivalents) into Claude so research runs inside Claude Code — not across Perplexity / Gemini / NotebookLM / YouTube tabs.
- Run the **`last30days` skill weekly** — either start or end of week — to catch new models, tools, workflows without manual scouting.

**Agentic vault navigation (Vault-as-SSoT for creative-studio)**
- Build out the Obsidian vault as the central hub — inspired by Karpathy's `llm-wiki` gist (`gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`) and `coleam00/claude-memory-compiler`. Verify whether Phase 6 (`phase6-SUPER-PLAN-2026-04-17.md`) already delivered parts of this; fold in what's missing.
- Fix Obsidian Git sync to track the **vault folder only** — not the entire `code-brain` repo. Currently I'm afraid to enable full sync because of scope.
- Investigate getting Obsidian working on the Alienware (previously blocked by mac-only plugin errors). If Vault is SSoT for all 3 machines, Alienware needs parity.
- Use the Obsidian Web Clipper (Chrome extension) as the inbound content pipeline — articles, images, blogs, Substacks, tweets, GitHub repos, YouTube videos — all route into the vault, agents learn from them over time.

**Pipeline orchestration**
- Concept selection: when a batch of Nano Banana 2 concepts lands in `runs/act2-exploration/concepts/`, agent surfaces top-N options with a quick visual rubric instead of me scrolling manually.
- Seedance + per-model prompt engineering: build model-specific prompt generators that apply the empirically-right style (simplicity vs detail varies by model) rather than just what the docs say.
- 7-Layer prompt framework: auto-format raw intent into 7-Layer structure via the `image-generator-prompt-science` skill — no more by-hand.
- Retry ladder: when an audit soft-fails, agent executes the 4-step escalation automatically (original → re-anchor → tightened → stop + diagnostic).
- Asset naming enforcement: agent names every generated file with `PT_{Act}_F##_{AssetType}.{ext}` — no hand-typing.
- candidates/ → approved/ promotion: after an audit pass, agent moves the file and logs the decision.
- CHANGELOG entries: agent drafts entries after every meaningful decision for Sean to skim/approve.
- **Assistant editor for Adobe:** agent gathers frames/assets/video/audio clips and sets up Adobe project files (After Effects, Premiere) so I'm not hand-organizing.

**Infrastructure**
- **MCP authorization persistence** — find a way to keep MCP servers authorized across sessions (permanent install, CLI/API alternatives that don't require browser-based re-auth each time). Currently a time sink at the start of every session.
- **Three-machine sync without always-on** — find a way for agents to reach Mac Mini / MBP / Alienware only when needed, not by requiring all three to stay powered on. Current state: no MCP connections, agents can't reach other machines reliably.
- Skill-repo sync: when a Skill is updated in one of `code-brain/.claude/skills/` or `sw-portfolio-animation-pipeline/.claude/skills/`, flag the divergence — decide consciously whether to mirror or keep distinct.

**Conversation hygiene**
- **Handoff-prompt detection:** slash command or skill that warns when a thread hits ~20–30 turns and proposes a handoff prompt for a fresh session automatically.

## Decline or Defer
- **No festival submissions** until the 2D animation pipeline clears my quality bar. No Annecy / Ottawa / SIGGRAPH / Sundance tracking right now.
- **No collaboration-tool suggestions.** Solo practice by design.
- **No overnight autoresearch runs** on unproven workflows. The 150-garbage-output incident is the policy.
- **No rebuilding pipelines around new tools** until the tool has proven itself in a scoped test.
- **Defer Adobe MCP testing** until we can enter it fully confident Claude can take advantage of it — not with setup eating most of the budget.
- **Defer ComfyUI workflow testing** unless we're testing against proven templates or have Claude Code extending them. Don't re-enter the old LoRA/SDXL tar pit.

## 20-Minutes-to-2-Minutes Candidates
High-leverage automation targets (traced from Layer 5 Q1 + Q3):
- Picking a concept from a batch of Nano Banana 2 outputs.
- Writing Seedance 2.0 prompts (60–80 words, action-focused, with the "never use" list enforced).
- Setting up a new ComfyUI workflow from scratch.
- Cross-referencing the two skill repos to see if something already exists.
- Re-describing pipeline context to a fresh Claude session (solved via handoff-prompt automation + vault-as-SSoT).
- Applying the 7-Layer prompt framework by hand.
- Running the retry ladder when an audit soft-fails.
- Model-specific prompt engineering (simplicity vs detail varies per model).
- Gathering frames/assets/clips and setting up Adobe project files.
- Re-authorizing MCP servers at session start.

## Context-Switch Costs to Minimize
- **Research-app → research-app.** The biggest single cost. Fix = Claude Research Skill consolidating Perplexity + Gemini DR + NotebookLM + Google search into one entry point.
- **IDE ↔ Adobe Suite.** Fix = Claude-as-assistant-editor for Adobe project setup so the IDE stays the driver seat.
- **Research ↔ implementation** (the weekday-research / weekend-build rhythm). Partially structural; partially solvable by vault-as-SSoT so weekend Sean opens the vault and everything's already organized.
- **Machine ↔ machine** (Mac Mini / MBP / Alienware). Fix = vault-as-SSoT with proper Git sync + real agentic mesh instead of manual repo pulls.

## Claude Code / Agent-Fleet Friction Points
- **The agent fleet doesn't work at all in creative-studio today** — no MCP connections, can't reach other machines reliably, bugs when they can. This is the single biggest build target.
- Headless SDK agents can't hit MCP servers (Adobe, Figma, Gemini interactive) — blocks interactive creative agents.
- Overnight batching is off-limits on unproven workflows.
- Vault synthesizer "intermittent — succeeds only when MBP awake" (Qwen3-14B dependency).
- Creative Skills split across `code-brain` and `sw-portfolio-animation-pipeline` with no sync signal.
- Skill drift when prompts get iterated outside a skill.
- Adobe MCP setup complexity blocking adoption.
- Obsidian vault sync is partial — can't enable full Git because it would sync the entire repo, not just the vault.

## The Extra Hour
**Build out the Vault as the central hub for creative work.** Everything else is a branch:
- Deep-work implementation gets documented there so agents can continue work while I'm busy or out.
- Hand-drawn animation practice gets photographed/scanned in so Claude tracks progress and uses it as reference for 2D animation projects.
- Screenplays go in for Claude to reference and expand on.
- Moodboards and inspiration go in for Claude to pull from on future projects.
- Web Clipper routes articles, images, blogs, Substacks, tweets, GitHub repos, YouTube videos into the vault.

**Target state:** Claude operates like an intern or new hire — absorbs the vault, learns patterns, then starts proposing ideas unprompted. Mentorship becomes creative partnership.
