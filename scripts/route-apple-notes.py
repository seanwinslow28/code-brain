#!/usr/bin/env python3
"""
Phase 3: Route Apple Notes to vault destinations.

Reads classification-report.tsv, generates kebab-case filenames,
injects YAML frontmatter, and moves files to vault destinations.
Skips files already archived in Phase 2.
"""

import csv
import os
import re
import sys
import unicodedata
from pathlib import Path
from collections import defaultdict

VAULT_ROOT = Path("vault")
NOTES_DIR = VAULT_ROOT / "70_apple-notes" / "Notes"
TSV_PATH = VAULT_ROOT / "70_apple-notes" / "classification-report.tsv"

# Phase 2 archive dirs to check for already-archived files
PHASE2_ARCHIVE_DIRS = [
    VAULT_ROOT / "60_archive" / "apple-notes-empty",
    VAULT_ROOT / "60_archive" / "apple-notes-duplicates",
    VAULT_ROOT / "60_archive" / "apple-notes-expired",
]

# TSV type -> YAML type mapping
TYPE_MAP = {
    "reference": "reference",
    "project-material": "project",
    "idea": "idea",
    "ai-prompt": "reference",  # default to reference; archive override below
    "ai-session-output": "archive",
    "creative-writing": "reference",
    "code-snippet": "reference",
    "work-nyl": "archive",
    "financial": "reference",
    "personal": "archive",
    "list": "reference",
    "unknown": "reference",
}

# Destinations that imply archive type
ARCHIVE_DESTINATIONS = [
    "60_archive/apple-notes-nyl/",
    "60_archive/apple-notes-personal/",
    "60_archive/apple-notes-prompts/",
]


def get_phase2_archived_filenames():
    """Get set of filenames already archived in Phase 2."""
    archived = set()
    for d in PHASE2_ARCHIVE_DIRS:
        if d.exists():
            for f in d.glob("*.md"):
                archived.add(f.name)
    return archived


def clean_ai_hint(hint: str) -> str:
    """Clean ai_hint into a proper 1-sentence summary."""
    if not hint or hint.strip() == "":
        return "Imported Apple Note."
    # Strip leading special chars
    hint = re.sub(r'^[#\-\*\.\$@\s]+', '', hint)
    # Remove unicode ellipsis
    hint = hint.replace('…', '...')
    # Remove curly quotes
    hint = hint.replace('\u2018', "'").replace('\u2019', "'")
    hint = hint.replace('\u201c', '"').replace('\u201d', '"')
    # Capitalize first letter
    if hint:
        hint = hint[0].upper() + hint[1:]
    # Truncate to 120 chars
    if len(hint) > 117:
        hint = hint[:117] + "..."
    # Ensure ends with period
    if hint and not hint.endswith('.') and not hint.endswith('...'):
        hint += '.'
    return hint


def to_kebab_case(filename: str, note_type: str, destination: str) -> str:
    """Convert filename to kebab-case with appropriate prefix."""
    # Remove .md extension
    name = filename
    if name.endswith('.md'):
        name = name[:-3]

    # Remove emoji and special unicode
    name = ''.join(c for c in name if not unicodedata.category(c).startswith(('So', 'Sk', 'Sc')))

    # Strip leading special chars (but keep meaningful digits like 16bitfit)
    name = re.sub(r'^[#\-\.\$@\*=\s]+', '', name)

    # Remove unicode ellipsis
    name = name.replace('\u2026', '')
    # Remove curly quotes
    for ch in ['\u2018', '\u2019', '\u201c', '\u201d']:
        name = name.replace(ch, '')
    # Remove other special punctuation
    name = name.replace('—', '-').replace('–', '-').replace('‑', '-')
    name = re.sub(r'[^\w\s\-]', '', name)

    # Convert to lowercase
    name = name.lower().strip()

    # Replace spaces and underscores with hyphens, collapse multiples
    name = re.sub(r'[\s_]+', '-', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')

    # Truncate to 60 chars
    if len(name) > 55:  # leave room for prefix
        name = name[:55].rstrip('-')

    # Add prefix based on type and destination
    is_archive = any(destination.startswith(ad) for ad in ARCHIVE_DESTINATIONS)
    if is_archive:
        prefix = ""  # No prefix for archive items
    elif note_type in ("idea",):
        prefix = "idea-"
    elif note_type in ("project-material", "project"):
        prefix = "prj-"
    else:
        prefix = "ref-"

    # Don't double-prefix
    if name.startswith(('ref-', 'prj-', 'idea-')):
        name = re.sub(r'^(ref|prj|idea)-', '', name)

    return prefix + name + ".md"


def resolve_collision(dest_path: Path, filename: str) -> str:
    """If filename exists at destination, append -2, -3, etc."""
    if not (dest_path / filename).exists():
        return filename
    base = filename[:-3]  # Remove .md
    n = 2
    while (dest_path / f"{base}-{n}.md").exists():
        n += 1
    return f"{base}-{n}.md"


def get_yaml_type(tsv_type: str, destination: str) -> str:
    """Map TSV type to YAML type, considering destination."""
    # ai-prompt going to archive → archive
    if tsv_type == "ai-prompt" and any(destination.startswith(ad) for ad in ARCHIVE_DESTINATIONS):
        return "archive"
    # ai-session-output always archive
    if tsv_type == "ai-session-output":
        return "archive"
    return TYPE_MAP.get(tsv_type, "reference")


def generate_frontmatter(row: dict) -> str:
    """Generate YAML frontmatter for a note."""
    yaml_type = get_yaml_type(row['type'], row['destination'])

    # Domain: take primary domain
    domains = row['domain'].split('|') if row['domain'] else ['unclassified']
    primary_domain = domains[0].strip() if domains[0].strip() != 'unclassified' else None

    # Valid domains only
    valid_domains = {'claude-mastery', 'product-management', 'creative-studio',
                     'life-systems', 'design-team', 'vault'}
    domain_list = [d.strip() for d in domains if d.strip() in valid_domains]
    if not domain_list:
        domain_list = ['vault']  # fallback

    ai_context = clean_ai_hint(row.get('ai_hint', ''))

    lines = ['---']
    lines.append(f'type: {yaml_type}')
    lines.append('domain:')
    for d in domain_list[:2]:  # Max 2 domains
        lines.append(f'  - {d}')
    lines.append('status: active')

    # Context (project name)
    if row.get('project'):
        lines.append(f'context: {row["project"]}')

    lines.append(f'ai-context: "{ai_context}"')
    lines.append('created: 2026-02-20')
    lines.append('source: apple-notes-import')
    lines.append('---')

    return '\n'.join(lines) + '\n'


def process_notes():
    """Main processing function."""
    os.chdir(Path(__file__).parent.parent)

    # Get already-archived filenames
    archived = get_phase2_archived_filenames()
    print(f"Phase 2 archived files: {len(archived)}")

    # Read TSV
    rows = []
    with open(TSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            rows.append(row)
    print(f"TSV rows: {len(rows)}")

    # Categorize by confidence
    tiers = {'HIGH': [], 'MEDIUM': [], 'LOW': []}
    skipped_archived = 0
    skipped_not_found = 0

    for row in rows:
        filename = row['filename']
        source_path = NOTES_DIR / filename

        # Skip if already archived in Phase 2
        if filename in archived:
            skipped_archived += 1
            continue

        # Skip if file not on disk
        if not source_path.exists():
            skipped_not_found += 1
            continue

        confidence = row.get('confidence', 'LOW').strip()
        if confidence in tiers:
            tiers[confidence].append(row)
        else:
            tiers['LOW'].append(row)

    print(f"\nSkipped (already archived): {skipped_archived}")
    print(f"Skipped (not found on disk): {skipped_not_found}")
    print(f"\nTier 1 (HIGH): {len(tiers['HIGH'])} notes")
    print(f"Tier 2 (MEDIUM): {len(tiers['MEDIUM'])} notes")
    print(f"Tier 3 (LOW): {len(tiers['LOW'])} notes")
    print(f"Total to process: {len(tiers['HIGH']) + len(tiers['MEDIUM']) + len(tiers['LOW'])}")

    # Process each tier
    all_results = {}
    for tier_name in ['HIGH', 'MEDIUM', 'LOW']:
        tier_notes = tiers[tier_name]
        if not tier_notes:
            continue

        print(f"\n{'='*60}")
        print(f"PROCESSING TIER: {tier_name} ({len(tier_notes)} notes)")
        print(f"{'='*60}")

        dest_counts = defaultdict(int)
        errors = []
        processed = 0
        batch_size = 50 if tier_name != 'LOW' else 25

        for i, row in enumerate(tier_notes):
            filename = row['filename']
            source_path = NOTES_DIR / filename
            destination = row['destination'].strip().rstrip('/')

            # Ensure destination directory exists
            dest_dir = VAULT_ROOT / destination
            dest_dir.mkdir(parents=True, exist_ok=True)

            try:
                # Read content
                content = source_path.read_text(encoding='utf-8')

                # Generate kebab-case filename
                new_filename = to_kebab_case(filename, row['type'], destination)
                new_filename = resolve_collision(dest_dir, new_filename)

                # Generate frontmatter
                frontmatter = generate_frontmatter(row)

                # Check if content already has frontmatter
                if content.startswith('---'):
                    # Skip injecting if already has frontmatter
                    new_content = content
                else:
                    new_content = frontmatter + '\n' + content

                # Write to destination
                dest_path = dest_dir / new_filename
                dest_path.write_text(new_content, encoding='utf-8')

                # Remove source file
                source_path.unlink()

                dest_counts[destination] += 1
                processed += 1

                # Batch reporting
                if (i + 1) % batch_size == 0:
                    print(f"  Batch {(i + 1) // batch_size}: {batch_size} notes processed")

            except Exception as e:
                errors.append(f"  ERROR: {filename}: {e}")

        # Tier checkpoint
        print(f"\n--- TIER {tier_name} COMPLETE ---")
        print(f"Notes processed: {processed}")
        print(f"Errors: {len(errors)}")
        print("Destination breakdown:")
        for dest, count in sorted(dest_counts.items()):
            print(f"  {dest}: {count}")
        if errors:
            print("Errors:")
            for e in errors:
                print(e)

        all_results[tier_name] = {
            'processed': processed,
            'errors': len(errors),
            'destinations': dict(dest_counts),
        }

    # Final report
    print(f"\n{'='*60}")
    print("PHASE 3 COMPLETE")
    print(f"{'='*60}")

    total_processed = sum(r['processed'] for r in all_results.values())
    total_errors = sum(r['errors'] for r in all_results.values())
    print(f"Total notes processed: {total_processed}")
    print(f"Total errors: {total_errors}")

    # Check remaining files
    remaining = list(NOTES_DIR.glob("*.md"))
    print(f"Notes remaining in Notes/: {len(remaining)}")
    if remaining:
        print("Remaining files:")
        for f in remaining[:20]:
            print(f"  {f.name}")
        if len(remaining) > 20:
            print(f"  ... and {len(remaining) - 20} more")

    # Combined destination totals
    print("\nCombined destination totals:")
    combined = defaultdict(int)
    for r in all_results.values():
        for dest, count in r['destinations'].items():
            combined[dest] += count
    for dest, count in sorted(combined.items()):
        print(f"  {dest}: {count}")


if __name__ == '__main__':
    process_notes()
