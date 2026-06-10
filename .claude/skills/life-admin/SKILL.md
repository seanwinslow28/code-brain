---
name: life-admin
description: Life Admin assistant. Manages move checklists, medical provider transitions, file organization audits, address change tracking, subscription renewal reminders, and travel planning. Use this skill when the user mentions "move", "address change", "organize files", "admin tasks", "doctor", "prescription", "trip planning", "U-Haul", or "renewal reminder".
---

# Life Admin Automation

## Purpose

Reduces the cognitive load of "adulting" by tracking active life transitions (interstate moves, medical provider switches, file organization), managing recurring admin tasks, and planning upcoming events. Everything flows into the Obsidian vault for persistent tracking.

## When to Use

- **Move Tasks:** "What's left for the move?" / "Address change status?"
- **Medical:** "Help me switch doctors" / "Prescription transfer checklist"
- **File Organization:** "Audit my files" / "Organize my downloads"
- **Renewals:** "What's coming up?" / "Subscription renewal calendar"
- **Travel:** "Plan the trip" / "What do I need for [destination]?"
- **Admin:** "What admin tasks are pending?"

## Active Life Context (local-only)

The real context — current move status, medical provider details, renewal calendar with actual services and costs, upcoming events — lives in `references/life-context.md`, which is **gitignored and never committed**. Load it at runtime before answering status questions. If the file is missing (fresh clone), ask the user for their current transitions and regenerate it using the templates below.

## Core Workflows

### 1. Move Checklist Management

Track in `vault/Areas/Life-Admin/<move-name>.md`:

```markdown
# [City A] → [City B] Move — [date]

## Pre-Move
- [ ] Notify landlord / lease termination
- [ ] Notify HR (tax withholding change if crossing state lines)
- [ ] Request medical records from current provider
- [ ] Book moving van
- [ ] Set up USPS mail forwarding
- [ ] Pack tech gear / kitchen / essentials
- [ ] Complete landlord move-out checklist

## Move Day
- [ ] Load van
- [ ] Drive to destination
- [ ] Unload
- [ ] Return van

## Post-Move (First Week)
- [ ] Update address: banks + credit cards
- [ ] Update address: Amazon / Apple ID / Google account
- [ ] Confirm employer HR address updated
- [ ] Cancel old renter's insurance
- [ ] Cancel old gym membership

## Post-Move (First Month)
- [ ] Find new gym
- [ ] Schedule new doctor (in-network)
- [ ] Update voter registration
- [ ] Update driver's license (new-state DMV/RMV — proof of residency)
- [ ] Evaluate: need new renter's insurance?
```

### 2. Medical Provider Transition

The hard part is **prescription continuity**. The checklist that works:

| Step | Notes |
|------|-------|
| Request medical records summary from current provider | Ask for a "continuity of care" letter |
| Request prescription transfer letter | Must state diagnosis, medication, dosage, treatment history |
| Gather supporting docs | Prescription bottles + insurer purchase records |
| Find in-network PCP or specialist at destination | Search the insurer's provider directory |
| Schedule new-patient appointment | Bring: letter + bottles + insurer records |
| Confirm new doctor can continue prescription | Before cutting over |
| Cancel old provider's recurring appointments | Only after continuity is confirmed |

### 3. Address Change Tracker

When executing address changes, track each category:

```python
ADDRESS_CHANGES = {
    'financial': ['Bank', 'Credit cards'],
    'shopping': ['Amazon', 'Apple ID'],
    'services': ['Google Account', 'Employer HR'],
    'government': ['USPS Mail Forwarding', 'Voter Registration', "DMV (Driver's License)"],
    'insurance': ["Old renter's (cancel)", "Evaluate new-state renter's insurance"],
}
```

### 4. The Decision Matrix

When comparing options (gyms, doctors, travel, products):

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Price | | | |
| Location/Convenience | | | |
| Key Feature | | | |
| "The Catch" | | | |
| **Verdict** | | | |

Always include a "Catch" column — the hidden downside.

### 5. File Organization Audit

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

### 6. Travel Planning

**Planning checklist template** (generate when a trip approaches):
```markdown
# [Destination] Trip — [dates]

## Documents
- [ ] Passport valid? (check expiry > 6 months past return)
- [ ] Travel insurance
- [ ] Event invitation / venue details

## Booking
- [ ] Flights
- [ ] Accommodation (near event venue)
- [ ] Inter-city transport (train/car)

## Budget
- [ ] Flights: $X
- [ ] Hotels: $X
- [ ] Gifts: $X
- [ ] Food/activities: $X
- [ ] Total estimate: $X

## Before Trip
- [ ] Notify card issuers of international travel
- [ ] Download offline maps
- [ ] Check phone international plan
```

### 7. Renewal Reminder System

When Google Calendar is connected, auto-set 2-week advance reminders for every entry in the renewal calendar (real dates and services in `references/life-context.md`):

```markdown
## Subscription Renewal Reminders
- [ ] [month year]: [service] ($XXX) — evaluate keep/cancel
- [ ] [month year]: [service] ($XXX) — CANCEL before renewal
```

### 8. Vault Integration

All life-admin tracking lives in `vault/Areas/Life-Admin/`:

```
vault/Areas/Life-Admin/
├── <move-name>.md          # Move checklist + address tracker
├── medical-transition.md   # Doctor switch checklist
├── renewal-calendar.md     # Subscription renewal dates
├── file-audit/             # File org audit results
├── travel/
│   └── <trip-name>.md      # Trip planning
└── admin-inbox.md          # Catch-all for pending tasks
```

## Success Criteria

- [ ] Move checklist tracks all items with status
- [ ] Medical transition checklist includes all required documents
- [ ] Address change tracker covers all accounts
- [ ] File audit script categorizes files by type and flags duplicates
- [ ] Decision matrices always include a "Catch" column
- [ ] Renewal calendar includes all known annual subscription dates
- [ ] Travel planning generates comprehensive pre-trip checklist
- [ ] All tracking documents output to vault

## Copy/Paste Ready

```
"What's left for the move?"
"Help me switch doctors"
"Audit my files"
"What admin tasks are pending?"
"What's renewing soon?"
"Plan the trip"
"Update my address everywhere"
"Organize my downloads folder"
"Generate move-out checklist"
```
