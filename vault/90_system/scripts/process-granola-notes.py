#!/usr/bin/env python3
"""
process-granola-notes.py
Post-processes Granola-synced meeting notes for Sean's Obsidian vault.

1. Injects vault-schema YAML frontmatter (resolves type collision)
2. Renames to kebab-case with mtg- prefix and date
3. Auto-sorts into subfolders by title/attendee keywords
4. Resolves speaker names in transcripts (You→Sean, Guest→name for 1:1s)
5. Co-locates transcripts with their parent notes
6. Extracts embedded Granola notes from daily notes (--migrate mode)

Usage:
    python3 process-granola-notes.py                # Process unprocessed files
    python3 process-granola-notes.py --dry-run      # Preview changes
    python3 process-granola-notes.py --migrate      # One-time migration
"""

import argparse
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────

VAULT = Path(__file__).resolve().parent.parent.parent  # vault/90_system/scripts/ → vault/
GRANOLA_BASE = VAULT / "30_domains" / "product-management" / "the-block-meetings-granola-notes"
DAILY_DIR = VAULT / "10_timeline" / "daily"
OLD_GRANOLA = VAULT / "Granola"

# ── Speaker Name Lookup ──────────────────────────────────────────────────

SPEAKER_NAMES = {
    "erupkus@theblock.co": "Ed Rupkus",
    "ddebreczeni@theblock.co": "David Debreczeni",
    "jgragg@theblock.co": "Jeff Gragg",
    "cdaumur@theblock.co": "Claudine Daumur",
    "mvitebsky@theblock.co": "Matt Vitebsky",
    "sho@theblock.co": "Serena Ho",
    "melshahat@theblock.co": "Mohamed Elshahat",
    "jcarusi@theblock.co": "Joe Carusi",
    "kvallecillo@theblock.co": "Karla Vallecillo",
    "ldanowski@theblock.co": "Lil Danowski",
    "bmendoza@theblock.co": "Ben Mendoza",
    "mprice@theblock.co": "Mike Price",
    "mhulis@theblock.co": "Maria Hulis",
    "norobenko@theblock.co": "Nika Orobenko",
    "npivcevic@theblock.co": "Nikita Pivcevic",
    "cpaz@theblock.co": "Cesar Paz",
    "abenitez@theblock.co": "Anna Benitez",
    "mzhynko@theblock.co": "Marina Zhynko",
    "mlozuk@theblock.co": "Marina Lozuk",
    "kbaspinar@theblock.co": "Koray Baspinar",
    "bvadimovich@theblock.co": "Bogdan Vadimovich",
    "ysmagulov@theblock.co": "Yermek Smagulov",
    "akryvanosau@theblock.co": "Akira Kryvanosau",
    "koliva@theblock.co": "K. Oliva",
    "sli@theblock.co": "S. Li",
    "lli@theblock.co": "L. Li",
    "ramuald.vishneuski@ventionteams.com": "Ramuald Vishneuski",
    # Add new team members as needed
}

# ── Auto-Sort Rules ──────────────────────────────────────────────────────
# (subfolder, title_keywords, attendee_check)
# First match wins. Rules ordered by specificity.

SORT_RULES = [
    ("daily-standup", ["standup", "daily standup", "unified daily"], None),
    ("design-sync", ["design sync", "design weekly", "design alignment",
                      "product + design", "product design"], None),
    ("ed-sean-one-on-ones", ["biweekly update", "eow biweekly"], None),
    ("ed-sean-one-on-ones", ["ed "], lambda att: len(att) <= 2 and
     any("erupkus" in a for a in att)),
    ("david-sean-one-on-ones", ["david"], lambda att: len(att) <= 2 and
     any("debreczeni" in a for a in att)),
    ("all-hands", ["all hands", "all-hands", "town hall", "401k", "company"], None),
    ("adops-revops", ["adops", "revops", "salesforce", "case queue",
                       "revenue", "sales", "ad ops"], None),
    ("campus-conversations", ["campus", "sponsored course", "course catalog",
                               ".co > campus", "co campus"], None),
]


# ── YAML Frontmatter Parsing ────────────────────────────────────────────

def parse_frontmatter(content: str):
    """Parse YAML frontmatter from markdown content. Returns (metadata, body)."""
    if not content.startswith("---"):
        return {}, content

    end = content.find("\n---", 3)
    if end == -1:
        return {}, content

    yaml_block = content[4:end]
    body = content[end + 4:].lstrip("\n")

    meta = {}
    current_key = None
    current_list = None

    for line in yaml_block.split("\n"):
        # List item
        if line.startswith("  - ") and current_key:
            if current_list is None:
                current_list = []
            current_list.append(line.strip("- ").strip())
            meta[current_key] = current_list
            continue

        # Key-value pair
        match = re.match(r'^(\w[\w-]*)\s*:\s*(.*)', line)
        if match:
            if current_list is not None:
                current_list = None
            current_key = match.group(1)
            value = match.group(2).strip().strip('"').strip("'")
            if value == "[]":
                meta[current_key] = []
            elif value:
                meta[current_key] = value
            else:
                meta[current_key] = None
            current_list = None if value else []  # Prepare for list if no inline value

    return meta, body


def serialize_frontmatter(meta: dict) -> str:
    """Serialize metadata dict to YAML frontmatter string."""
    lines = ["---"]
    for key, value in meta.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
        elif value is None:
            lines.append(f"{key}:")
        elif isinstance(value, str) and any(c in value for c in ':{}[],"\'#|>&*!%@`'):
            lines.append(f'{key}: "{value}"')
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


# ── Helper Functions ─────────────────────────────────────────────────────

def to_kebab(title: str) -> str:
    """Convert a title to kebab-case, max 50 chars."""
    s = title.lower()
    s = re.sub(r'[^\w\s-]', '', s)       # Remove special chars
    s = re.sub(r'[\s_]+', '-', s)         # Spaces/underscores → hyphens
    s = re.sub(r'-+', '-', s)             # Collapse multiple hyphens
    s = s.strip('-')
    return s[:50]


def extract_date(meta: dict) -> str:
    """Extract ISO date (YYYY-MM-DD) from Granola created timestamp."""
    created = meta.get("created", "")
    if "T" in str(created):
        return str(created).split("T")[0]
    return str(created)[:10] if created else datetime.now().strftime("%Y-%m-%d")


def make_filename(title: str, date: str, is_transcript: bool = False) -> str:
    """Generate vault-convention filename: mtg-YYYY-MM-DD-title[-transcript].md"""
    slug = to_kebab(title)
    suffix = "-transcript" if is_transcript else ""
    return f"mtg-{date}-{slug}{suffix}.md"


def determine_subfolder(title: str, attendees: list) -> str:
    """Match title/attendees against sort rules. Returns subfolder name."""
    title_lower = title.lower()
    for subfolder, keywords, attendee_check in SORT_RULES:
        if any(kw in title_lower for kw in keywords):
            if attendee_check is None or attendee_check(attendees):
                return subfolder
    # Fallback: check if it's a 1:1 with Ed or David by attendee only
    if attendees and len(attendees) <= 2:
        if any("erupkus" in a for a in attendees):
            return "ed-sean-one-on-ones"
        if any("debreczeni" in a for a in attendees):
            return "david-sean-one-on-ones"
    return "other"


def generate_ai_context(title: str, attendees: list, subfolder: str,
                         is_transcript: bool = False) -> str:
    """Generate ai-context string (< 120 chars)."""
    if is_transcript:
        prefix = "Full transcript of"
    else:
        prefixes = {
            "daily-standup": "Daily standup covering",
            "design-sync": "Design sync discussing",
            "ed-sean-one-on-ones": "1:1 with Ed covering",
            "david-sean-one-on-ones": "1:1 with David covering",
            "all-hands": "All-hands meeting on",
            "adops-revops": "AdOps/RevOps meeting about",
            "campus-conversations": "Campus team sync on",
            "other": "Meeting about",
        }
        prefix = prefixes.get(subfolder, "Meeting about")

    context = f"{prefix} {title.lower()}."
    if len(context) > 120:
        context = context[:117] + "..."
    return context


def resolve_speakers(body: str, attendees: list) -> str:
    """Replace You→Sean and Guest→name (for 1:1 meetings)."""
    # Always replace You with Sean
    body = re.sub(r'^### You (\(.*?\))$', r'### Sean \1', body, flags=re.MULTILINE)

    # For 1:1 meetings (exactly 1 attendee), replace Guest with their name
    real_attendees = [a for a in attendees if a and "@" in a]
    if len(real_attendees) == 1:
        name = SPEAKER_NAMES.get(real_attendees[0], real_attendees[0].split("@")[0].title())
        body = re.sub(r'^### Guest (\(.*?\))$', rf'### {name} \1', body, flags=re.MULTILINE)
    elif len(real_attendees) > 1:
        # Add attendee list at top for multi-person meetings
        attendee_lines = []
        for a in real_attendees:
            name = SPEAKER_NAMES.get(a, a.split("@")[0])
            attendee_lines.append(f"- {name} ({a})")
        attendee_section = "## Attendees\n" + "\n".join(attendee_lines) + "\n\n"
        # Insert after the first heading
        first_heading = body.find("\n#")
        if first_heading > 0:
            body = body[:first_heading + 1] + attendee_section + body[first_heading + 1:]
        else:
            body = attendee_section + body

    return body


def is_processed(meta: dict) -> bool:
    """Check if a file has already been processed by this script."""
    source = meta.get("source", "")
    if source in ("granola-sync", "granola-manual") and meta.get("type") == "meeting":
        return True
    if source == "granola-sync" and "granola_type" in meta:
        return True
    return False


def inject_vault_frontmatter(meta: dict, title: str, subfolder: str,
                              is_transcript: bool = False) -> dict:
    """Transform Granola frontmatter into vault-schema frontmatter."""
    date = extract_date(meta)
    attendees = meta.get("attendees", [])
    if isinstance(attendees, str):
        attendees = [a.strip() for a in attendees.split(",")]

    new_meta = {}
    # Preserve granola_id first
    if "granola_id" in meta:
        new_meta["granola_id"] = meta["granola_id"]
    # Resolve type collision
    granola_type = meta.get("type", "note")
    new_meta["granola_type"] = granola_type
    new_meta["type"] = "meeting"
    # Vault-required fields
    new_meta["domain"] = ["product-management"]
    new_meta["status"] = "active"
    new_meta["ai-context"] = generate_ai_context(
        meta.get("title", title), attendees, subfolder, is_transcript)
    new_meta["context"] = "the-block"
    new_meta["created"] = date
    new_meta["source"] = "granola-sync"
    # Preserve attendees
    if attendees:
        new_meta["attendees"] = attendees if isinstance(attendees, list) else [attendees]
    # Preserve cross-links (will be updated after rename)
    if "transcript" in meta:
        new_meta["transcript"] = meta["transcript"]
    if "note" in meta:
        new_meta["note"] = meta["note"]

    return new_meta


# ── File Processing ──────────────────────────────────────────────────────

def process_file(filepath, dry_run=False, force=False):
    """Process a single Granola note or transcript file.
    Returns action report dict or None if skipped."""
    content = filepath.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(content)

    # Skip if no granola_id (not a Granola file)
    if "granola_id" not in meta:
        return None

    # Skip if already processed (always — even in migrate mode)
    if is_processed(meta):
        return None

    # Skip files within 7-day sync window (unless force/migrate)
    if not force:
        date_str = extract_date(meta)
        try:
            file_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) - file_date < timedelta(days=7):
                return {"action": "skipped", "reason": "within 7-day sync window",
                        "file": filepath.name}
        except ValueError:
            pass

    title = meta.get("title", filepath.stem).replace(" - Transcript", "").replace("-transcript", "")
    # Strip any existing mtg- prefix to prevent double-prefixing
    title = re.sub(r'^mtg-\d{4}-\d{2}-\d{2}-', '', title)
    is_transcript = "transcript" in filepath.stem.lower() or meta.get("type") == "transcript"
    date = extract_date(meta)
    attendees = meta.get("attendees", [])
    if isinstance(attendees, str):
        attendees = [a.strip() for a in attendees.split(",")]

    # Determine target subfolder
    subfolder = determine_subfolder(title, attendees)
    target_dir = GRANOLA_BASE / subfolder

    # Generate new filename
    new_filename = make_filename(title, date, is_transcript)

    # Skip if target already exists and is processed (re-sync dedup)
    target_path = target_dir / new_filename
    if target_path.exists() and target_path != filepath:
        existing_content = target_path.read_text(encoding="utf-8")
        existing_meta, _ = parse_frontmatter(existing_content)
        if is_processed(existing_meta):
            return None

    # Build new frontmatter
    new_meta = inject_vault_frontmatter(meta, title, subfolder, is_transcript)

    # Resolve speaker names in transcripts
    if is_transcript:
        body = resolve_speakers(body, attendees)

    report = {
        "action": "process",
        "original": str(filepath.relative_to(VAULT)),
        "target": str(target_path.relative_to(VAULT)),
        "subfolder": subfolder,
        "title": title,
        "is_transcript": is_transcript,
    }

    if dry_run:
        report["action"] = "would_process"
        return report

    # Write processed file
    target_dir.mkdir(parents=True, exist_ok=True)
    new_content = serialize_frontmatter(new_meta) + "\n\n" + body
    target_path.write_text(new_content, encoding="utf-8")

    # Remove original if it moved
    if target_path != filepath:
        filepath.unlink()

    return report


# ── Daily Note Extraction (Migration) ────────────────────────────────────

def extract_from_daily_notes(dry_run: bool = False) -> list[dict]:
    """Extract embedded Granola notes from daily note files."""
    reports = []

    for daily_file in sorted(DAILY_DIR.glob("*.md")):
        content = daily_file.read_text(encoding="utf-8")

        # Find the # Granola Notes section
        granola_match = re.search(r'^# Granola Notes\s*$', content, re.MULTILINE)
        if not granola_match:
            continue

        granola_start = granola_match.start()
        granola_section = content[granola_start:]
        pre_granola = content[:granola_start].rstrip("\n")

        # Split into individual meeting blocks (## headings)
        meeting_blocks = re.split(r'^## ', granola_section, flags=re.MULTILINE)
        # First element is "# Granola Notes\n", skip it
        meeting_blocks = [b for b in meeting_blocks[1:] if b.strip()]

        extracted_links = []

        for block in meeting_blocks:
            lines = block.split("\n")
            meeting_title = lines[0].strip()

            # Parse inline metadata
            meta = {}
            body_start = 1
            for i, line in enumerate(lines[1:], 1):
                if line.startswith("**Granola ID:**"):
                    meta["granola_id"] = line.split(":**")[1].strip()
                elif line.startswith("**Type:**"):
                    meta["type"] = line.split(":**")[1].strip()
                elif line.startswith("**Created:**"):
                    meta["created"] = line.split(":**")[1].strip()
                elif line.startswith("**Updated:**"):
                    meta["updated"] = line.split(":**")[1].strip()
                elif line.startswith("**Attendees:**"):
                    att_str = line.split(":**")[1].strip()
                    meta["attendees"] = [a.strip() for a in att_str.split(",") if a.strip()]
                elif line.startswith("###") or (line.strip() and not line.startswith("**")):
                    body_start = i
                    break

            meta["title"] = meeting_title
            body = "\n".join(lines[body_start:]).strip()

            # Add heading back
            body = f"# {meeting_title}\n\n{body}"

            date = extract_date(meta)
            attendees = meta.get("attendees", [])
            subfolder = determine_subfolder(meeting_title, attendees)
            new_filename = make_filename(meeting_title, date)
            target_dir = GRANOLA_BASE / subfolder
            target_path = target_dir / new_filename

            # Skip if already extracted (idempotent re-runs)
            if target_path.exists():
                existing_content = target_path.read_text(encoding="utf-8")
                existing_meta, _ = parse_frontmatter(existing_content)
                if is_processed(existing_meta):
                    wiki_name = target_path.stem
                    extracted_links.append(f"- [[{wiki_name}]]")
                    continue

            new_meta = inject_vault_frontmatter(meta, meeting_title, subfolder)
            wiki_name = target_path.stem  # filename without .md

            report = {
                "action": "extract",
                "source": daily_file.name,
                "title": meeting_title,
                "target": str(target_path.relative_to(VAULT)),
                "subfolder": subfolder,
            }

            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                new_content = serialize_frontmatter(new_meta) + "\n\n" + body
                target_path.write_text(new_content, encoding="utf-8")

            extracted_links.append(f"- [[{wiki_name}]]")
            reports.append(report)

        # Update daily note: remove Granola section, add ## Meetings with links
        if not dry_run and extracted_links:
            # Check if ## Meetings already exists
            if "## Meetings" not in pre_granola:
                # Find insertion point (after <!-- slack-overnight --> or before ## Morning Focus)
                insert_match = re.search(
                    r'(<!-- slack-overnight -->.*?\n)', pre_granola, re.DOTALL)
                if insert_match:
                    insert_pos = insert_match.end()
                else:
                    # Insert before ## Morning Focus
                    insert_match = re.search(r'^## Morning Focus', pre_granola, re.MULTILINE)
                    insert_pos = insert_match.start() if insert_match else len(pre_granola)

                meetings_section = "\n## Meetings\n<!-- meetings -->\n" + "\n".join(extracted_links) + "\n\n"
                pre_granola = (pre_granola[:insert_pos] +
                               meetings_section +
                               pre_granola[insert_pos:])
            else:
                # Append links after <!-- meetings --> anchor
                anchor_match = re.search(r'<!-- meetings -->', pre_granola)
                if anchor_match:
                    insert_pos = anchor_match.end()
                    links_text = "\n" + "\n".join(extracted_links)
                    pre_granola = (pre_granola[:insert_pos] +
                                   links_text +
                                   pre_granola[insert_pos:])

            daily_file.write_text(pre_granola + "\n", encoding="utf-8")

    return reports


# ── Migrate Old Transcripts ─────────────────────────────────────────────

def migrate_old_transcripts(dry_run: bool = False) -> list[dict]:
    """Move transcripts from vault/Granola/Transcripts/ to vault-integrated location."""
    reports = []

    if not OLD_GRANOLA.exists():
        return reports

    for transcript_file in OLD_GRANOLA.rglob("*-transcript.md"):
        report = process_file(transcript_file, dry_run=dry_run, force=True)
        if report:
            reports.append(report)

    return reports


# ── Process Manual Notes ─────────────────────────────────────────────────

def process_manual_notes(dry_run: bool = False) -> list[dict]:
    """Process the 5 pre-plugin manual notes with different format."""
    reports = []

    # Collect files first to avoid mutating directories during iteration
    all_files = []
    for subfolder in GRANOLA_BASE.iterdir():
        if not subfolder.is_dir():
            continue
        all_files.extend(list(subfolder.glob("*.md")))

    for note_file in all_files:
            content = note_file.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(content)

            # Skip already-processed files
            if is_processed(meta):
                continue
            # Skip files with granola_id (handled by process_file)
            if "granola_id" in meta:
                continue
            # Skip empty files
            if not body.strip():
                report = {"action": "delete_empty", "file": str(note_file.relative_to(VAULT))}
                if not dry_run:
                    note_file.unlink()
                reports.append(report)
                continue

            # These are manual notes — try to extract date from filename
            date_match = re.search(r'(\d{1,2})-(\d{1,2})', note_file.stem)
            if date_match:
                month, day = date_match.groups()
                date = f"2026-{int(month):02d}-{int(day):02d}"
            else:
                date = datetime.now().strftime("%Y-%m-%d")

            # Extract title from filename or first heading
            title = note_file.stem
            title = re.sub(r'\s*-\s*\d{1,2}-\d{1,2}$', '', title)  # Remove date suffix

            # Determine subfolder (might already be in correct one)
            attendees = []
            current_subfolder = note_file.parent.name
            target_subfolder = determine_subfolder(title, attendees)

            # If file is in raw-notes, move to proper subfolder
            if current_subfolder == "raw-notes":
                target_dir = GRANOLA_BASE / target_subfolder
            else:
                target_dir = note_file.parent
                target_subfolder = current_subfolder

            new_filename = make_filename(title, date)
            target_path = target_dir / new_filename

            new_meta = {
                "type": "meeting",
                "domain": ["product-management"],
                "status": "active",
                "ai-context": generate_ai_context(title, [], target_subfolder),
                "context": "the-block",
                "created": date,
                "source": "granola-manual",
            }

            report = {
                "action": "process_manual",
                "original": str(note_file.relative_to(VAULT)),
                "target": str(target_path.relative_to(VAULT)),
                "title": title,
            }

            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                new_content = serialize_frontmatter(new_meta) + "\n\n" + body
                target_path.write_text(new_content, encoding="utf-8")
                if target_path != note_file:
                    note_file.unlink()

            reports.append(report)

    return reports


# ── Update Cross-Links ───────────────────────────────────────────────────

def update_cross_links(dry_run: bool = False) -> list[dict]:
    """Update transcript↔note wiki-links to use new filenames."""
    reports = []

    for subfolder in GRANOLA_BASE.iterdir():
        if not subfolder.is_dir():
            continue
        for md_file in subfolder.glob("mtg-*.md"):
            content = md_file.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(content)

            changed = False

            # Fix transcript links that point to old daily note anchors
            for field in ("transcript", "note"):
                link = meta.get(field, "")
                if not link:
                    continue
                # Match old format: [[2026-03-03#Meeting Title]]
                old_link_match = re.match(r'\[\[(\d{4}-\d{2}-\d{2})#(.+?)\]\]', link)
                if old_link_match:
                    link_date = old_link_match.group(1)
                    link_title = old_link_match.group(2)
                    is_transcript_link = field == "transcript"
                    new_link_name = make_filename(
                        link_title, link_date, is_transcript_link).replace(".md", "")
                    meta[field] = f"[[{new_link_name}]]"
                    changed = True

            if changed and not dry_run:
                new_content = serialize_frontmatter(meta) + "\n\n" + body
                md_file.write_text(new_content, encoding="utf-8")
                reports.append({
                    "action": "update_links",
                    "file": str(md_file.relative_to(VAULT)),
                })

    return reports


# ── Cleanup ──────────────────────────────────────────────────────────────

def cleanup_old_granola(dry_run: bool = False) -> list[dict]:
    """Remove empty vault/Granola/ directory tree."""
    reports = []

    if not OLD_GRANOLA.exists():
        return reports

    # Check if any files remain
    remaining = list(OLD_GRANOLA.rglob("*.md"))
    if remaining:
        reports.append({
            "action": "warning",
            "message": f"{len(remaining)} files still in Granola/ — skipping cleanup",
            "files": [str(f.relative_to(VAULT)) for f in remaining],
        })
        return reports

    if not dry_run:
        shutil.rmtree(OLD_GRANOLA, ignore_errors=True)
    reports.append({"action": "cleanup", "path": "Granola/"})

    return reports


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Process Granola meeting notes for vault")
    parser.add_argument("--dry-run", action="store_true", help="Preview without changes")
    parser.add_argument("--migrate", action="store_true", help="One-time full migration")
    args = parser.parse_args()

    dry_run = args.dry_run
    migrate = args.migrate

    if dry_run:
        print("=== DRY RUN — no changes will be made ===\n")

    all_reports = []

    # Step 1: Extract from daily notes (migrate only)
    if migrate:
        print("── Step 1: Extracting embedded notes from daily notes ──")
        reports = extract_from_daily_notes(dry_run)
        all_reports.extend(reports)
        for r in reports:
            print(f"  {r['action']}: {r.get('title', '')} → {r.get('target', '')}")
        if not reports:
            print("  (no embedded Granola notes found)")
        print()

    # Step 2: Migrate old transcripts (migrate only)
    if migrate:
        print("── Step 2: Migrating transcripts from Granola/Transcripts/ ──")
        reports = migrate_old_transcripts(dry_run)
        all_reports.extend(reports)
        for r in reports:
            print(f"  {r['action']}: {r.get('original', '')} → {r.get('target', '')}")
        if not reports:
            print("  (no old transcripts found)")
        print()

    # Step 3: Process manual notes (migrate only)
    if migrate:
        print("── Step 3: Processing manual notes ──")
        reports = process_manual_notes(dry_run)
        all_reports.extend(reports)
        for r in reports:
            print(f"  {r['action']}: {r.get('original', r.get('file', ''))} → {r.get('target', '')}")
        if not reports:
            print("  (no manual notes found)")
        print()

    # Step 4: Process unprocessed plugin-synced files
    print("── Step 4: Processing unprocessed Granola files ──")
    processed = 0
    for md_file in GRANOLA_BASE.rglob("*.md"):
        report = process_file(md_file, dry_run=dry_run, force=migrate)
        if report:
            all_reports.append(report)
            print(f"  {report['action']}: {report.get('original', report.get('file', ''))}"
                  f" → {report.get('target', report.get('reason', ''))}")
            processed += 1
    if not processed:
        print("  (no unprocessed files)")
    print()

    # Step 5: Update cross-links
    print("── Step 5: Updating cross-links ──")
    reports = update_cross_links(dry_run)
    all_reports.extend(reports)
    for r in reports:
        print(f"  {r['action']}: {r['file']}")
    if not reports:
        print("  (no links to update)")
    print()

    # Step 6: Cleanup (migrate only)
    if migrate:
        print("── Step 6: Cleanup ──")
        reports = cleanup_old_granola(dry_run)
        all_reports.extend(reports)
        for r in reports:
            print(f"  {r['action']}: {r.get('path', r.get('message', ''))}")
        print()

    # Summary
    action_counts = {}
    for r in all_reports:
        action = r["action"]
        action_counts[action] = action_counts.get(action, 0) + 1

    print("── Summary ──")
    for action, count in sorted(action_counts.items()):
        print(f"  {action}: {count}")
    print(f"  Total actions: {len(all_reports)}")

    if dry_run:
        print("\n=== DRY RUN COMPLETE — re-run without --dry-run to apply ===")


if __name__ == "__main__":
    main()
