---
type: reference
domain:
  - creative-studio
  - claude-mastery
status: active
context: superuser-pack
ai-context: "/automode."
created: 2026-02-20
source: apple-notes-import
---

# /automode

/automode

Please create a MIGRATION_STAGING folder in the project root and copy ONLY the high-priority files identified in the ASSET_INVENTORY_SPREADSHEET.md (those marked as MUST and SHOULD). 

Organize them into these categories:
1. Critical Innovations (core code files like BridgeProtocolV2.js, CombatSystem.js)
2. Sprite Assets (all 374 sprite files)
3. Audio Assets (SFX and music) 
4. AI Generation (scripts and prompts)
5. Database Schema (SQL migrations)
6. Agent Configs (12 specialists)
7. Documentation (key docs only)

Create the following structure:
- 01_CRITICAL_INNOVATIONS/
- 02_SPRITE_ASSETS/
- 03_AUDIO_ASSETS/
- 04_AI_GENERATION/
- 05_DATABASE_SCHEMA/
- 06_AGENT_CONFIGS/
- 07_DOCUMENTATION/

Skip any files marked as COULD or WON'T in the inventory. Also create a STAGING_MANIFEST.md that lists exactly what was copied, organized by category with file counts.

Execute this task completely without asking for confirmation at each step.

Here’s an example of the folder structure:
16BitFit_Updated/
└── MIGRATION_STAGING/
    ├── 01_CRITICAL_INNOVATIONS/
    │   ├── BridgeProtocolV2.js
    │   ├── CombatSystem.js
    │   ├── Fighter.js
    │   ├── BossAI.js
    │   └── AssetManager.js
    │
    ├── 02_SPRITE_ASSETS/
    │   ├── bosses/ (45 files)
    │   ├── characters/ (120 files)
    │   ├── avatars/ (200 files)
    │   └── ui/ (69 files)
    │
    ├── 03_AUDIO_ASSETS/
    │   ├── sfx/ (80+ files)
    │   └── music/
    │
    ├── 04_AI_GENERATION/
    │   ├── generate-boss-sprites-imagen4.js
    │   ├── prompts.json
    │   └── sprite-priority-list.json
    │
    ├── 05_DATABASE_SCHEMA/
    │   └── migrations/ (4 SQL files)
    │
    ├── 06_AGENT_CONFIGS/
    │   └── agents/ (12 specialist files)
    │
    └── 07_DOCUMENTATION/
        ├── Technical_Architecture_V4.md
        ├── QA_Testing_Plan_V2.md
        ├── Asset_Generation_Pipeline.txt
        └── [other key docs]
## 

