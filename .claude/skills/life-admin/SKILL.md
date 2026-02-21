---
name: life-admin
description: Life Admin assistant. Manages the Boston move checklist, medical provider transitions, file organization audits, address change tracking, subscription renewal reminders, and travel planning. Use this skill when the user mentions "move", "Boston", "address change", "organize files", "admin tasks", "doctor", "prescription", "Aetna", "trip planning", "Cannes", "U-Haul", or "renewal reminder".
---

# Life Admin Automation

## Purpose

Reduces the cognitive load of "adulting" by tracking Sean's active life transitions (Staten Island to Boston move, medical provider switch, file organization), managing recurring admin tasks, and planning upcoming events. Everything flows into the Obsidian vault for persistent tracking.

## When to Use

- **Move Tasks:** "What's left for the Boston move?" / "Address change status?"
- **Medical:** "Help me switch doctors" / "Prescription transfer checklist"
- **File Organization:** "Audit my files" / "Organize my downloads"
- **Renewals:** "What's coming up?" / "Subscription renewal calendar"
- **Travel:** "Plan the Cannes trip" / "What do I need for France?"
- **Admin:** "What admin tasks are pending?"

## Sean's Active Life Context

### Boston Move — March 21, 2026

**Moving from:** Staten Island, NY → **Charlestown, Boston, MA** (girlfriend's apartment)

**Status Tracker:**

| Task | Status | Notes |
|------|--------|-------|
| Notify landlord / lease termination | DONE | Landlord sent move-out checklist — follow it |
| Request tax withholding change (NY→MA) | PENDING | HR notified, waiting on instructions from Rippling |
| Rent U-Haul van | TODO | Regular van (not truck), pickup Staten Island → drop off Boston |
| Pack tech gear | TODO | 2 monitors, PC, Mac Mini, MacBook Pro, desk, computer chair |
| Pack kitchen supplies | TODO | Girlfriend has most furniture/items already |
| Forward mail (USPS) | TODO | Set up USPS mail forwarding at usps.com |
| Update address — Chase bank | TODO | Update checking, savings, credit card |
| Update address — Bilt credit card | TODO | |
| Update address — Amazon | TODO | |
| Update address — Apple ID | TODO | |
| Update address — Google account | TODO | |
| Update address — employer HR (Rippling) | TODO | Already notified, confirm address is updated |
| Cancel Lemonade Insurance (NY renter's) | TODO | After move, get new MA renter's if needed |
| Cancel YMCA membership | TODO | Find new gym in Charlestown ($100-120/mo range) |
| Update voter registration (NY→MA) | TODO | |
| Update driver's license (NY→MA DMV) | TODO | MA RMV — need proof of residency |

### Medical Provider Transition

**Current:** Medvidi (medvidi.com) — $159/visit, no insurance used
**Target:** New in-network doctor under Aetna in Charlestown/Boston area
**Prescription:** Active prescription that needs continuity

**Transition Checklist:**

| Step | Status | Notes |
|------|--------|-------|
| Request medical records summary from Medvidi | TODO | Ask for "continuity of care" letter |
| Request prescription transfer letter from Medvidi | TODO | Must state diagnosis, medication, dosage, treatment history |
| Gather supporting docs | TODO | Prescription bottles + Aetna purchase records |
| Find Aetna in-network PCP or specialist in Charlestown/Boston | TODO | Search Aetna provider directory |
| Schedule new patient appointment (after March 21) | TODO | Bring: Medvidi letter + bottles + Aetna records |
| Confirm new doctor can continue prescription | TODO | |
| Cancel Medvidi recurring appointments | TODO | After new doctor confirms continuity |

### Financial Admin (Cross-references personal-finance skill)

**Autopay:**
- All subscriptions: autopay (managed via personal-finance skill)
- Rent: manual pay via Bilt (earns points)
- Credit card payments: manual (Sean specifies amount each payment)

**Annual Renewal Calendar:**

| Service | Renewal | Cost | Action |
|---------|---------|------|--------|
| ElevenLabs | May 2026 | $240 | Evaluate — keep or cancel? |
| FantasyPros | Aug 2026 | $54 | Re-activate for football season |
| Meshy | Aug 2026 | $120 | CANCEL before renewal |
| Disney+ | Oct 2026 | $190 | Keep (split with cousin) |
| Lottiefiles | Oct 2026 | $240 | CANCEL before renewal |
| HBO Max | ~Apr 2027 | $170 | Split with girlfriend |
| LinkedIn Premium | Jan 2027 | $261 | CANCEL before renewal |

### 2025 Taxes

- **Status:** Being handled by aunt (former CPA) — all set for this year
- **Documents provided:** 2025 expense sheet, previous years' expense docs, rent/utility ledger
- **Note:** Tax withholding change to MA is pending (see move checklist)

### File Organization

**Current state:** Chaotic. Files spread across MacBook Pro, Mac Mini, and PC. Recently synced all three to Google Cloud Drive — some improvement.

**Target state:** Organized file system with Claude Code audit/inventory.

**Planned audit workflow:**
1. Scan all files across Google Drive sync
2. Categorize: keep, archive, delete
3. Organize into structure (by type: tax docs, insurance, receipts, projects, personal)
4. Move important docs to vault (`vault/Resources/Documents/`)
5. Set up ongoing organization rules

### Upcoming Events

| Event | Date | Notes |
|-------|------|-------|
| Boston move | March 21, 2026 | Primary near-term life event |
| Cannes, France trip | September 21, 2026 | Friend's wedding + Paris extension with girlfriend |

## Examples

**Example 1: Move Status Check**
```
User: "What's left for the Boston move?"
Claude: [Uses life-admin]

Boston Move — March 21, 2026 (32 days away)

DONE (2/15):
  [x] Landlord notified / lease terminated
  [x] HR notified about tax withholding change

PENDING (1):
  [ ] Tax withholding NY->MA (waiting on Rippling HR)

TODO (12):
  HIGH PRIORITY (do this week):
  [ ] Request medical records from Medvidi
  [ ] Set up USPS mail forwarding
  [ ] Book U-Haul van (Staten Island -> Boston)

  BEFORE MOVE DAY:
  [ ] Pack tech gear + kitchen supplies
  [ ] Follow landlord's move-out checklist

  AFTER MOVE:
  [ ] Update all addresses (Chase, Bilt, Amazon, Apple, Google, HR)
  [ ] Cancel Lemonade Insurance
  [ ] Cancel YMCA, find new gym
  [ ] Update voter registration
  [ ] MA driver's license (RMV)
  [ ] Schedule new doctor (Aetna in-network, Charlestown)
```

**Example 2: Medical Transition**
```
User: "Help me switch doctors for the move"
Claude: [Uses life-admin]

Medical Provider Transition Plan:

BEFORE YOU MOVE (do now):
1. Call/email Medvidi and request:
   - Medical records summary (continuity of care letter)
   - Prescription transfer letter (diagnosis + medication + dosage)
   Timeline: Allow 1-2 weeks for records

2. Gather your docs:
   - Current prescription bottles
   - Aetna account showing prescription purchases

AFTER YOU MOVE (late March):
3. Search Aetna provider directory for Charlestown/Boston
   - Look for PCP or [specialist type] accepting new patients
4. Schedule new patient appointment
   - Bring: Medvidi letter + bottles + Aetna records
5. Confirm prescription continuity
6. Cancel Medvidi recurring visits

Want me to search for Aetna providers in Charlestown now?
```

**Example 3: File Audit**
```
User: "Audit my Google Drive files"
Claude: [Uses life-admin]

Scanning Google Drive sync...

File Inventory:
- Documents: 342 files (PDFs, DOCx, TXT)
- Images: 1,203 files
- Code projects: 47 folders
- Downloads (unsorted): 189 files
- Duplicates detected: 31 files

Recommended actions:
1. DELETE: 31 duplicate files (saving 2.1 GB)
2. ARCHIVE: 89 old project files (>1 year, no recent access)
3. ORGANIZE: 189 unsorted downloads into categories
4. VAULT: Move 23 important docs (tax returns, insurance, contracts)
   to vault/Resources/Documents/

Proceed with cleanup? [y/n]
```

## Core Workflows

### 1. Move Checklist Management

Track in `vault/Areas/Life-Admin/boston-move.md`:

```markdown
# Boston Move — March 21, 2026

## Pre-Move
- [x] Notify landlord
- [x] Notify HR (tax withholding)
- [ ] Request Medvidi medical records
- [ ] Book U-Haul van
- [ ] Set up USPS mail forwarding
- [ ] Pack tech gear
- [ ] Pack kitchen supplies
- [ ] Complete landlord move-out checklist

## Move Day
- [ ] Load U-Haul (Staten Island)
- [ ] Drive to Boston
- [ ] Unload at girlfriend's apartment
- [ ] Return U-Haul

## Post-Move (First Week)
- [ ] Update address: Chase (checking + savings + CC)
- [ ] Update address: Bilt credit card
- [ ] Update address: Amazon
- [ ] Update address: Apple ID
- [ ] Update address: Google account
- [ ] Confirm HR/Rippling address updated
- [ ] Cancel Lemonade Insurance (NY renter's)
- [ ] Cancel YMCA membership

## Post-Move (First Month)
- [ ] Find new gym in Charlestown ($100-120/mo)
- [ ] Schedule new doctor (Aetna in-network)
- [ ] Update voter registration (NY -> MA)
- [ ] Get MA driver's license (RMV)
- [ ] Evaluate: need MA renter's insurance?
```

### 2. Address Change Tracker

When executing address changes, track each one:

```python
ADDRESS_CHANGES = {
    'financial': ['Chase Bank', 'Bilt Credit Card'],
    'shopping': ['Amazon', 'Apple ID'],
    'services': ['Google Account', 'Employer (Rippling)'],
    'government': ['USPS Mail Forwarding', 'Voter Registration', 'MA RMV (Driver\'s License)'],
    'insurance': ['Lemonade (cancel)', 'Evaluate MA renter\'s insurance'],
}
```

### 3. The Decision Matrix

When comparing options (gyms, doctors, travel, products):

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Price | | | |
| Location/Convenience | | | |
| Key Feature | | | |
| "The Catch" | | | |
| **Verdict** | | | |

Always include a "Catch" column — the hidden downside.

### 4. File Organization Audit

```python
import os
from pathlib import Path
from collections import Counter

def audit_directory(root_path: str) -> dict:
    """Scan directory tree and categorize files."""
    extensions = Counter()
    large_files = []
    duplicates = {}

    for path in Path(root_path).rglob('*'):
        if path.is_file():
            ext = path.suffix.lower()
            extensions[ext] += 1
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > 100:
                large_files.append((str(path), round(size_mb, 1)))

    return {
        'total_files': sum(extensions.values()),
        'by_type': dict(extensions.most_common(20)),
        'large_files': large_files,
    }

FILE_ORGANIZATION_RULES = {
    'tax_docs': {'pattern': r'tax|w2|1099|expense', 'dest': 'vault/Resources/Documents/Tax/'},
    'insurance': {'pattern': r'insurance|policy|claim', 'dest': 'vault/Resources/Documents/Insurance/'},
    'receipts': {'pattern': r'receipt|invoice', 'dest': 'vault/Resources/Documents/Receipts/'},
    'screenshots': {'ext': ['.png', '.jpg'], 'source': 'Screenshots/', 'dest': 'Archive/Screenshots/'},
    'installers': {'ext': ['.dmg', '.pkg', '.exe'], 'dest': 'Archive/Installers/'},
}
```

### 5. Travel Planning (Cannes Trip)

**Trip: Cannes, France — September 21, 2026**
- Friend's wedding
- Paris extension with girlfriend
- Budget: TBD (savings goal in personal-finance skill)

**Planning checklist** (generate when trip approaches):
```markdown
# Cannes + Paris Trip — Sep 2026

## Documents
- [ ] Passport valid? (check expiry > 6 months past return)
- [ ] Travel insurance
- [ ] Wedding invitation / venue details

## Booking
- [ ] Flights (JFK/BOS -> Nice or Paris)
- [ ] Cannes accommodation (near wedding venue)
- [ ] Paris hotel (X nights)
- [ ] Train: Cannes -> Paris (TGV, ~5.5 hours)

## Budget
- [ ] Flights: $X
- [ ] Hotels: $X
- [ ] Wedding gift: $X
- [ ] Food/activities: $X
- [ ] Total estimate: $X

## Before Trip
- [ ] Notify Chase of international travel
- [ ] Notify Bilt of international travel
- [ ] Download offline maps
- [ ] Check phone international plan
```

### 6. Renewal Reminder System

When Google Calendar is connected, auto-set reminders:

```markdown
## Subscription Renewal Reminders

Set 2-week advance reminders for:
- [ ] May 2026: ElevenLabs ($240) — evaluate keep/cancel
- [ ] Aug 2026: Meshy ($120) — CANCEL
- [ ] Aug 2026: FantasyPros ($54) — re-activate for football
- [ ] Oct 2026: Lottiefiles ($240) — CANCEL
- [ ] Oct 2026: Disney+ ($190) — auto-renew (split with cousin)
- [ ] Jan 2027: LinkedIn Premium ($261) — CANCEL
- [ ] Apr 2027: HBO Max ($170) — auto-renew (split with girlfriend)
```

### 7. Vault Integration

All life-admin tracking lives in `vault/Areas/Life-Admin/`:

```
vault/Areas/Life-Admin/
├── boston-move.md          # Move checklist + address tracker
├── medical-transition.md  # Doctor switch checklist
├── renewal-calendar.md    # Subscription renewal dates
├── file-audit/            # File org audit results
├── travel/
│   └── cannes-2026.md     # Trip planning
└── admin-inbox.md         # Catch-all for pending tasks
```

## Success Criteria

- [ ] Boston move checklist tracks all items with status
- [ ] Medical transition checklist includes all required documents
- [ ] Address change tracker covers all accounts
- [ ] File audit script categorizes files by type and flags duplicates
- [ ] Decision matrices always include a "Catch" column
- [ ] Renewal calendar includes all known annual subscription dates
- [ ] Travel planning generates comprehensive pre-trip checklist
- [ ] All tracking documents output to vault

## Copy/Paste Ready

```
"What's left for the Boston move?"
"Help me switch doctors"
"Audit my files"
"What admin tasks are pending?"
"What's renewing soon?"
"Plan the Cannes trip"
"Update my address everywhere"
"Organize my downloads folder"
"Generate move-out checklist"
```