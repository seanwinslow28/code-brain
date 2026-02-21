---
name: life-admin
description: Life Admin assistant. Automates file organization (`/organize-inbox`), recurring admin tasks, and plans travel/events using comparison matrices. Use this skill when the user mentions "organize files", "trip planning", "compare options", or "admin tasks".
---

# Life Admin Automation

## Purpose

Reduces the cognitive load of "adulting" by automating file organization and structuring complex decisions (travel, purchases) into clear comparison matrices.

## When to Use

- **File Cleanup:** "My Downloads folder is a mess."
- **Travel Planning:** "Plan a trip to Japan."
- **Purchasing:** "Help me buy a new monitor."
- **Recurring Admin:** "Renew my car registration."

## Examples

**Example 1: Inbox Organization**
```
User: "Clean up my Downloads folder."
Claude: [Uses life-admin] Running `organize_inbox.py`...
- Moved 5 PDFs to `Documents/Receipts`.
- Moved 3 DMGs to `Installers` (and deleted 2 old ones).
- Moved 10 screenshots to `Desktop/Screenshots`.
Folder is now clean.
```

**Example 2: Travel Comparison (The Matrix)**
```
User: "I need a hotel in NYC for next weekend."
Claude: [Uses life-admin] I'll find options. First, what is your budget and your "vibe" (Quiet/Luxury or Central/Busy)?

User: "Under $400, Central."
Claude: Here is the **Decision Matrix**:

| Hotel | Price | Location Score | Vibe | Dealbreaker Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Ace Hotel** | $350 | 10/10 (Midtown) | Hip/Noisy | Thin walls |
| **Arlo NoMad**| $320 | 9/10 | Micro-rooms | Tiny room size |
| **CitizenM** | $290 | 8/10 | Efficient | No room service |

Recommendation: **CitizenM** for value, **Ace** for location.
```

## Admin Workflow

### 1. The Digital Librarian (`/organize-inbox`)

Use the `organize_inbox.py` script to enforce taxonomy on your files.

**Rules:**
*   **Receipts:** `YYYY-MM-DD_[Vendor]_[Amount].pdf` -> `/Finance`
*   **Installers:** `.dmg`, `.pkg` -> `/Installers` (Delete duplicates)
*   **Screenshots:** Move to `/Screenshots/YYYY-MM`

### 2. The Decision Matrix

When comparing options (flights, products, hotels), NEVER just list them.
Create a table with:
*   **Price**
*   **Feature Score** (Weighted by user pref)
*   **"The Catch"** (negative constraint)

### 3. The Travel Interview

Before searching for travel, ask:
1.  **Energy Level:** Chill vs. Adventure?
2.  **Hard Constraints:** Budget cap? Non-stop flights only?
3.  **The "Anchor":** What is the ONE thing you must do?

## Success Criteria

- [ ] File organization script correctly identifies file types and modifies paths.
- [ ] Comparison matrices always include a "Risk" or "Catch" column.
- [ ] Travel planning starts with a constraint interview.

## Copy/Paste Ready

```
"Clean up my inbox folder."
"Find me flights to [Place] and compare them."
"Help me choose a [Product]."
```
