# Migration Guide: Research Corpus → Superuser Pack

**Purpose:** Move all 16BitFit Battle Mode research into a clean project directory inside `claude-code-superuser-pack`, organized for Claude Code session loading.

---

## New Location

```
claude-code-superuser-pack/
├── 16bitfit-battle-mode/          ← NEW top-level project directory
│   ├── CLAUDE.md                  ← NEW project-specific CLAUDE.md
│   ├── SOURCE-OF-TRUTH.md         ← Master reference (compressed from all 28 files)
│   ├── execution-blueprint.md     ← Step-by-step commands (~102.5h across 5 phases)
│   │
│   ├── docs/                      ← Active reference docs (Claude Code loads these)
│   │   ├── agent-sdk/
│   │   │   ├── phase-2-synthesis.md        ← The big 350-line spec
│   │   │   ├── tech-stack-specs.md         ← Hardware inventory, all 3 machines
│   │   │   └── agent-teams.md              ← Agent Teams (production-ready)
│   │   │
│   │   ├── sprite-pipeline/
│   │   │   ├── pipeline-CLAUDE.md          ← Implementation rules + anti-patterns
│   │   │   ├── pipeline-README.md          ← Pipeline overview, 7-stage flow
│   │   │   ├── hybrid-pipeline-plan.md     ← THE key doc: hybrid architecture spec
│   │   │   ├── workflow-operations-guide.md ← Asset counts, prompt library, step-by-step
│   │   │   ├── pixel-quantizer-kickoff.md  ← Ready-to-paste build prompt
│   │   │   └── video-model-kickoff.md      ← Ready-to-paste research prompt
│   │   │
│   │   ├── lora-autoresearch/
│   │   │   ├── rtx5080-lora-training.md    ← Complete LoRA guide for RTX 5080
│   │   │   ├── autoresearch-overview.md    ← Karpathy pattern → ComfyUI mapping
│   │   │   └── rtx5080-compatibility.md    ← Known bugs, confirmed working configs
│   │   │
│   │   └── validation/
│   │       ├── validation-audit-march-2026.md  ← 9-category stack audit
│   │       ├── opportunity-scan.md             ← 60-day landscape scan, top 5 tools
│   │       └── perplexity-prompts.md           ← The 3+1 engineered prompts (for re-runs)
│   │
│   └── _archive/                  ← Original research (read-only, for deep dives)
│       ├── council-results/
│       │   ├── consensus-analysis.md       ← Cross-model synthesis
│       │   ├── claude-opus-response.md     ← Motion transfer discovery
│       │   ├── gpt52-response.md           ← DAG render graph
│       │   ├── gemini3-response.md         ← "Quantized Motion Bridge"
│       │   └── csv/                        ← 4 comparison matrices
│       ├── original-workflow-summary.md    ← Tech stack rationale, hex architecture
│       ├── agents-sdk-architecture.md      ← SDK interactive vs autonomous layers
│       ├── pipeline-changelog.md           ← v0.1.0 release notes (Jan 21, 2026)
│       ├── lora-guide-content.md           ← Framework comparison
│       ├── lora-training-guide.pdf         ← PDF version of training guide
│       └── perplexity-ui-ux-prompt.md      ← Dashboard research prompt (not yet run)
```

---

## File Mapping (Old Path → New Path)

### Top-Level (Essential — always loaded)

| Old Location | New Location | Why It Matters |
|---|---|---|
| `SOURCE-OF-TRUTH.md` | `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` | Master reference for every session |
| `16bitfit-execution-blueprint.md` | `16bitfit-battle-mode/execution-blueprint.md` | Step-by-step commands for all 5 phases |
| *(new)* | `16bitfit-battle-mode/CLAUDE.md` | Project rules, constraints, anti-patterns |

### docs/agent-sdk/

| Old Location | New Location |
|---|---|
| `Claude-Agents-SDK-Info/agent-sdk-upgrade-phase-2-synthesis-analysis.md` | `docs/agent-sdk/phase-2-synthesis.md` |
| `Claude-Agents-SDK-Info/tech-stack-specs.md` | `docs/agent-sdk/tech-stack-specs.md` |
| `Claude-Agents-SDK-Info/Claude-Code-Agent-Teams.md` | `docs/agent-sdk/agent-teams.md` |

### docs/sprite-pipeline/

| Old Location | New Location |
|---|---|
| `Current-Sprite-Sheet-Pipeline-Workflow-Docs/CLAUDE.md` | `docs/sprite-pipeline/pipeline-CLAUDE.md` |
| `Current-Sprite-Sheet-Pipeline-Workflow-Docs/README.md` | `docs/sprite-pipeline/pipeline-README.md` |
| `*2-12-UPDATED.../hybrid-pipeline-plan.md` *(from COUNCIL RESULTS subfolder)* | `docs/sprite-pipeline/hybrid-pipeline-plan.md` |
| `*2-12-UPDATED.../workflow-operations-guide.md` | `docs/sprite-pipeline/workflow-operations-guide.md` |
| `*2-12-UPDATED.../claude-code-kickoff-prompt.md` | `docs/sprite-pipeline/pixel-quantizer-kickoff.md` |
| `*2-12-UPDATED.../video-model-pipeline-kickoff-prompt.md` | `docs/sprite-pipeline/video-model-kickoff.md` |

### docs/lora-autoresearch/

| Old Location | New Location |
|---|---|
| `LoRA Training Research.../ref-lora-training-rtx5080-sprite-pipeline.md` | `docs/lora-autoresearch/rtx5080-lora-training.md` |
| `Autoresearch-ComfyUI-Overview.md` | `docs/lora-autoresearch/autoresearch-overview.md` |
| `LoRA Training Research.../LoRA-training-perplexity-computer-follow-up.md` | `docs/lora-autoresearch/rtx5080-compatibility.md` |

### docs/validation/

| Old Location | New Location |
|---|---|
| `validation-audit-march-2026.md` | `docs/validation/validation-audit-march-2026.md` |
| `creative-tech-opportunity-scan.md` | `docs/validation/opportunity-scan.md` |
| `Perplexity-Computer-Prompts.md` | `docs/validation/perplexity-prompts.md` |

### _archive/ (Original research — keep but don't load routinely)

| Old Location | New Location |
|---|---|
| `*SPRITE SHEET COUNCIL RESULTS/Perplexity-Final-Results-Analysis.md` | `_archive/council-results/consensus-analysis.md` |
| `*SPRITE SHEET COUNCIL RESULTS/Claude Opus 4.6 Thinking-response.md` | `_archive/council-results/claude-opus-response.md` |
| `*SPRITE SHEET COUNCIL RESULTS/GPT-5.2 Thinking-response.md` | `_archive/council-results/gpt52-response.md` |
| `*SPRITE SHEET COUNCIL RESULTS/Gemini 3 Pro-response.md` | `_archive/council-results/gemini3-response.md` |
| `*SPRITE SHEET COUNCIL RESULTS/CSV/` (4 files) | `_archive/council-results/csv/` |
| `Current-Sprite-Sheet-Pipeline-Workflow-Docs/Project_ Sprite-Sheet...Summary.md` | `_archive/original-workflow-summary.md` |
| `Claude-Agents-SDK-Info/agents-sdk.md` | `_archive/agents-sdk-architecture.md` |
| `Current-Sprite-Sheet-Pipeline-Workflow-Docs/CHANGELOG.md` | `_archive/pipeline-changelog.md` |
| `LoRA Training Research.../lora-guide-content.md` | `_archive/lora-guide-content.md` |
| `LoRA Training Research.../comfyui-lora-training-guide.pdf` | `_archive/lora-training-guide.pdf` |
| `LoRA Training Research.../perplexity-ui-ux-research-prompt.md` | `_archive/perplexity-ui-ux-prompt.md` |

---

## Why This Structure

**The problem with the current folder:** Five subfolders with inconsistent naming (`*2-12-UPDATED...`, `*SPRITE SHEET COUNCIL RESULTS`), files scattered by when you researched them rather than what they're for, and no project-level CLAUDE.md telling Claude Code how to navigate it.

**What the new structure fixes:**
1. **Flat top-level for essentials** — SOURCE-OF-TRUTH.md, execution-blueprint.md, and CLAUDE.md are the three files Claude Code needs for ANY task. They're right at the root.
2. **docs/ organized by workstream** — matches the three workstreams in the SOT. When the Session Loading Guide says "load hybrid-pipeline-plan.md," you find it instantly in `docs/sprite-pipeline/`.
3. **_archive/ for deep dives only** — council responses, original summaries, and PDFs are still accessible but won't clutter Claude Code's context. The SOT already synthesized them.
4. **Clean names** — no asterisks, no spaces, no 50-character folder names. Every filename is descriptive and tab-completable.

---

## Steps to Execute the Migration

Run these on your MacBook Pro from the superuser pack root:

```bash
cd ~/Code-Brain/claude-code-superuser-pack

# 1. Create the directory structure
mkdir -p 16bitfit-battle-mode/{docs/{agent-sdk,sprite-pipeline,lora-autoresearch,validation},_archive/council-results/csv}

# 2. Copy essential top-level files
# (SOURCE-OF-TRUTH.md and CLAUDE.md will be created/placed separately)
cp "/path/to/Agentic-Frameworks-And-Autoresearch/16bitfit-execution-blueprint.md" \
   16bitfit-battle-mode/execution-blueprint.md

cp "/path/to/Agentic-Frameworks-And-Autoresearch/SOURCE-OF-TRUTH.md" \
   16bitfit-battle-mode/SOURCE-OF-TRUTH.md

# 3. Copy agent-sdk docs
cp "/path/to/Claude-Agents-SDK-Info/agent-sdk-upgrade-phase-2-synthesis-analysis.md" \
   16bitfit-battle-mode/docs/agent-sdk/phase-2-synthesis.md

cp "/path/to/Claude-Agents-SDK-Info/tech-stack-specs.md" \
   16bitfit-battle-mode/docs/agent-sdk/tech-stack-specs.md

cp "/path/to/Claude-Agents-SDK-Info/Claude-Code-Agent-Teams.md" \
   16bitfit-battle-mode/docs/agent-sdk/agent-teams.md

# 4. Copy sprite-pipeline docs
cp "/path/to/Current-Sprite-Sheet-Pipeline-Workflow-Docs/CLAUDE.md" \
   16bitfit-battle-mode/docs/sprite-pipeline/pipeline-CLAUDE.md

cp "/path/to/Current-Sprite-Sheet-Pipeline-Workflow-Docs/README.md" \
   16bitfit-battle-mode/docs/sprite-pipeline/pipeline-README.md

# The hybrid-pipeline-plan.md lives inside the COUNCIL RESULTS subfolder:
cp "/path/to/*2-12-UPDATED.../*SPRITE SHEET COUNCIL RESULTS/hybrid-pipeline-plan.md" \
   16bitfit-battle-mode/docs/sprite-pipeline/hybrid-pipeline-plan.md

cp "/path/to/*2-12-UPDATED.../workflow-operations-guide.md" \
   16bitfit-battle-mode/docs/sprite-pipeline/workflow-operations-guide.md

cp "/path/to/*2-12-UPDATED.../claude-code-kickoff-prompt.md" \
   16bitfit-battle-mode/docs/sprite-pipeline/pixel-quantizer-kickoff.md

cp "/path/to/*2-12-UPDATED.../video-model-pipeline-kickoff-prompt.md" \
   16bitfit-battle-mode/docs/sprite-pipeline/video-model-kickoff.md

# 5. Copy lora-autoresearch docs
cp "/path/to/LoRA Training Research.../ref-lora-training-rtx5080-sprite-pipeline.md" \
   16bitfit-battle-mode/docs/lora-autoresearch/rtx5080-lora-training.md

cp "/path/to/Autoresearch-ComfyUI-Overview.md" \
   16bitfit-battle-mode/docs/lora-autoresearch/autoresearch-overview.md

cp "/path/to/LoRA Training Research.../LoRA-training-perplexity-computer-follow-up.md" \
   16bitfit-battle-mode/docs/lora-autoresearch/rtx5080-compatibility.md

# 6. Copy validation docs
cp "/path/to/validation-audit-march-2026.md" \
   16bitfit-battle-mode/docs/validation/validation-audit-march-2026.md

cp "/path/to/creative-tech-opportunity-scan.md" \
   16bitfit-battle-mode/docs/validation/opportunity-scan.md

cp "/path/to/Perplexity-Computer-Prompts.md" \
   16bitfit-battle-mode/docs/validation/perplexity-prompts.md

# 7. Copy archive files
cp "/path/to/*SPRITE SHEET COUNCIL RESULTS/Perplexity-Final-Results-Analysis.md" \
   16bitfit-battle-mode/_archive/council-results/consensus-analysis.md

cp "/path/to/*SPRITE SHEET COUNCIL RESULTS/Claude Opus 4.6 Thinking-response.md" \
   16bitfit-battle-mode/_archive/council-results/claude-opus-response.md

cp "/path/to/*SPRITE SHEET COUNCIL RESULTS/GPT-5.2 Thinking-response.md" \
   16bitfit-battle-mode/_archive/council-results/gpt52-response.md

cp "/path/to/*SPRITE SHEET COUNCIL RESULTS/Gemini 3 Pro-response.md" \
   16bitfit-battle-mode/_archive/council-results/gemini3-response.md

cp "/path/to/*SPRITE SHEET COUNCIL RESULTS/CSV/"*.csv \
   16bitfit-battle-mode/_archive/council-results/csv/

cp "/path/to/Current-Sprite-Sheet-Pipeline-Workflow-Docs/Project_ Sprite-Sheet...Summary.md" \
   16bitfit-battle-mode/_archive/original-workflow-summary.md

cp "/path/to/Claude-Agents-SDK-Info/agents-sdk.md" \
   16bitfit-battle-mode/_archive/agents-sdk-architecture.md

cp "/path/to/Current-Sprite-Sheet-Pipeline-Workflow-Docs/CHANGELOG.md" \
   16bitfit-battle-mode/_archive/pipeline-changelog.md

cp "/path/to/LoRA Training Research.../lora-guide-content.md" \
   16bitfit-battle-mode/_archive/lora-guide-content.md

cp "/path/to/LoRA Training Research.../comfyui-lora-training-guide.pdf" \
   16bitfit-battle-mode/_archive/lora-training-guide.pdf

cp "/path/to/LoRA Training Research.../perplexity-ui-ux-research-prompt.md" \
   16bitfit-battle-mode/_archive/perplexity-ui-ux-prompt.md
```

**Note:** Replace `/path/to/` with the actual path to your `Agentic-Frameworks-And-Autoresearch` folder. The glob characters (`*`) in folder names will need shell quoting — use tab completion.

---

## After Migration: Update SOURCE-OF-TRUTH.md

The Session Loading Guide (Part 7) references old file paths. After copying, do a find-and-replace pass to update all file references to the new `docs/` paths. The CLAUDE.md you'll create handles this mapping, so this is a nice-to-have, not a blocker.

---

## Superuser Pack CLAUDE.md Update

Add this row to the Domain Workspaces table:

```markdown
| `16bitfit-battle-mode/` | 16BitFit Battle Mode: sprite pipeline, agent fleet, autoresearch | Project CLAUDE.md |
```

Update the skill/agent counts if you add any new skills for this project.
