#!/usr/bin/env python3
"""
Apple Notes Pre-Classifier
Reads all .md files in vault/70_apple-notes/Notes/, classifies each by
domain, type, project context, and suggested destination using keyword matching.
Outputs a TSV report for review before Phase 3 batch processing.
"""

import os
import re
import csv
import sys
from pathlib import Path
from collections import Counter

VAULT = Path(__file__).resolve().parent.parent / "vault"
NOTES_DIR = VAULT / "70_apple-notes" / "Notes"
OUTPUT_TSV = VAULT / "70_apple-notes" / "classification-report.tsv"

# ── Domain keyword patterns ──────────────────────────────────────────────
# Each tuple: (domain, weight, compiled_regex)
DOMAIN_PATTERNS = [
    ("creative-studio", 3, re.compile(
        r'16bitfit|16bit.?fit|16.?bit|bitfit|sprite|pixel.?art|phaser|game.?boy|dmg|'
        r'fighter|combat|boss.?(character|spec)|animation|animate|after.?effects?|'
        r'premiere|illustrator|photoshop|remotion|video.?edit|storyboard|'
        r'comedy|sketch.?note|bane|heroes.?of.?the.?city|creatures|'
        r'veo|short.?film|chip.?tune|figma.?make|magicpath|21st.?dev|'
        r'character.?animator|sfx|music.?asset|sprite.?sheet|walk.?cycle|'
        r'idle.?pose|battle.?transition|lcd.?screen|mobile.?shell|'
        r'pixel.?purity|retro.?aesthetic|game.?boy.?color',
        re.I)),
    ("product-management", 3, re.compile(
        r'the.?block|campus|prd|product.?manage|sprint|roadmap|stakeholder|'
        r'jira|ticket|etf|crypto(?!graphy)|token.?track|bitcoin|ethereum|solana|'
        r'dogecoin|polymarket|wordpress|theblock|data.?dashboard|'
        r'ga4|looker|analytics|api.?product|research.?team|'
        r'editorial|news.?feed|price.?page|data.?api|'
        r'grayscale|21shares|bitwise|vaneck|blackrock|fidelity',
        re.I)),
    ("claude-mastery", 3, re.compile(
        r'claude.?code|claude.?skill|mcp.?server|agent.?config|'
        r'anthropic|context7|notebooklm|obsidian.?mcp|'
        r'prompt.?engineer|sub.?agent|automode|bmad|'
        r'cursor.?ide|windsurf|n8n|zapier|docker|supabase|'
        r'react.?native|expo|hook.?config|settings\.json|'
        r'deep.?think|google.?deep|gemini',
        re.I)),
    ("life-systems", 3, re.compile(
        r'finance|money|budget|rent\b|salary|401k|tax\b|insurance|'
        r'gym\b|workout|health|habit|boston|'
        r'learning|hello.?pm|aspireship|career|resume|cover.?letter|'
        r'interview.?question|job.?search|hire|customer.?success|'
        r'grocery|recipe|meal|cooking|doctor|medical',
        re.I)),
    ("design-team", 3, re.compile(
        r'figma(?!.?make)|design.?system|design.?token|'
        r'ui.?spec|ux.?spec|tailwind|css.?variable|'
        r'component.?librar|layout.?spec|typography|'
        r'color.?palette|spacing|wcag|accessibility|'
        r'style.?guide|design.?brief',
        re.I)),
    ("vault", 3, re.compile(
        r'obsidian(?!.?mcp)|vault\b|dataview|templater|'
        r'zettelkasten|knowledge.?graph|wikilink|frontmatter|'
        r'moc\b|pkm\b',
        re.I)),
]

# ── Type keyword patterns ────────────────────────────────────────────────
TYPE_PATTERNS = [
    ("ai-prompt", re.compile(
        r'^(please|create|generate|design|build|help|scan|analyze|provide|draft|write)\b|'
        r'i.?want.?you.?to|paste.?this|copy.?and.?paste|'
        r'i.?d.?like.?you|here.?is.?the.?prompt|'
        r'context.?files?\b|give.?me.?a|'
        r'using.?the.?following|based.?on.?this',
        re.I | re.M)),
    ("ai-session-output", re.compile(
        r'summary.?what.?just|checkpoint|update.?todos|'
        r'completed.?successfully|here.?s.?what.?happened|'
        r'task.?completed|session.?summary|'
        r'^\u23fa|^\u2705|^\u274c|^\u26a0|^\ud83d',  # emoji bullets
        re.I | re.M)),
    ("creative-writing", re.compile(
        r'(act|scene|episode)\s+(one|two|three|1|2|3)|'
        r'logline|pilot|screenplay|dialogue|'
        r'teaser|cold.?open|sketch.?note|comedy.?bit|'
        r'series.?overview|character.?arc',
        re.I)),
    ("code-snippet", re.compile(
        r'```(js|ts|py|css|json|bash|yaml|tsx|jsx)|'
        r'\.env\b.*=|config\.json|package\.json|'
        r'^(import|from|export|const|function)\s+\w',
        re.I | re.M)),
    ("work-nyl", re.compile(
        r'nyl\b|new.?york.?life|lto\b|ingest|b.?roll|'
        r'council.?president|firm.?element|media.?training|'
        r'giving.?campaign|recruiting.?video|'
        r'acpc|data.?science.?week|kickoff|'
        r'^\d{2}-\d{3,4}\b',  # job number pattern
        re.I | re.M)),
    ("financial", re.compile(
        r'expense.?ratio|charge.?to|rent\b.*\$|tax.?return|salary|'
        r'budget|401k|insurance.?premium|invoice|'
        r'\$\d{2,}',
        re.I)),
    ("personal", re.compile(
        r'journal|diary|sentimental|bio\b|pet\b|family|'
        r'friend|personal.?story|relationship|birthday|'
        r'party|vacation|trip|cabin|wedding',
        re.I)),
    ("reference", re.compile(
        r'how.?to|guide|documentation|comparison|framework|'
        r'tutorial|cheat.?sheet|reference|overview|'
        r'best.?practice|pattern|architecture',
        re.I)),
    ("idea", re.compile(
        r'\bidea\b|what.?if|brainstorm|concept|pitch|'
        r'we.?could|wouldn.?t.?it.?be|app.?idea|'
        r'possible|potential|explore',
        re.I)),
    ("list", re.compile(
        r'list\s+of|things\s+to|bring\s+to|'
        r'what\s+to\s+bring|shopping|inventory|'
        r'catalog|collection',
        re.I)),
    ("project-material", re.compile(
        r'spec|architecture|implementation|epic|story\s+\d|'
        r'mvp|milestone|requirement|technical.?design|'
        r'user.?flow|wire.?frame|prototype|'
        r'phase\s+\d|sprint\s+\d',
        re.I)),
]

# ── Project context patterns ─────────────────────────────────────────────
PROJECT_PATTERNS = [
    ("16bitfit", re.compile(
        r'16bitfit|16bit.?fit|16.?bit.?fit|bitfit|'
        r'game.?boy.*fit|fighter.*workout|combat.*exercise|'
        r'sbfg|phaser.*game|battle.?system.*workout|'
        r'boss.*(couch|warrior|iron|cardio)',
        re.I)),
    ("campus-201", re.compile(
        r'campus|lms|course.?catalog|articulate|'
        r'sponsored.?course|education.?platform|'
        r'campus.?upgrade|campus.?product',
        re.I)),
    ("boston-move", re.compile(
        r'boston|move.?to.?boston|apartment.?hunt|'
        r'moving.?checklist|relocation.?to|'
        r'boston.?move|boston.?apartment',
        re.I)),
    ("superuser-pack", re.compile(
        r'superuser|claude.?code.?skill|hook.?config|'
        r'agent.?config|export.?group|installer|'
        r'settings\.json.*claude|\.claude/|'
        r'superuser.?pack',
        re.I)),
    ("animation-pipeline", re.compile(
        r'animation.?pipeline|sprite.?pipeline|'
        r'asset.?pipeline|shot.?packet|'
        r'pixel.?purity.?pipeline',
        re.I)),
    ("personal-finance", re.compile(
        r'bank.?export|chase.*statement|bilt.*statement|'
        r'subscription.?audit|spending.?track|'
        r'personal.?finance|budget.*month',
        re.I)),
]

# ── Destination mapping ──────────────────────────────────────────────────
def determine_destination(domain, note_type, project, confidence):
    """Apply destination rules in priority order."""
    # Rule 1: Project context takes priority
    if project:
        return f"20_projects/prj-{project}/"

    # Rule 2-3: Reusable knowledge
    if note_type in ("reference", "project-material"):
        if domain == "creative-studio":
            return "40_knowledge/references/"
        return "40_knowledge/references/"

    # Rule 4: Raw data/lists
    if note_type == "list":
        return "50_sources/data/"

    # Rule 5: Financial records
    if note_type == "financial":
        return "50_sources/finance/"

    # Rule 6: Ideas
    if note_type == "idea":
        return "00_inbox/"

    # Rule 7: Personal/journal
    if note_type == "personal":
        return "60_archive/apple-notes-personal/"

    # Rule 8: Old NYL work
    if note_type == "work-nyl":
        return "60_archive/apple-notes-nyl/"

    # Rule 9: AI prompts - check if reusable
    if note_type == "ai-prompt":
        if project:
            return f"20_projects/prj-{project}/"
        if confidence == "HIGH" and domain:
            return "40_knowledge/references/"
        return "60_archive/apple-notes-prompts/"

    # Rule 9b: AI session outputs
    if note_type == "ai-session-output":
        if project:
            return f"20_projects/prj-{project}/"
        return "60_archive/apple-notes-prompts/"

    # Rule 10: Creative writing
    if note_type == "creative-writing":
        return "40_knowledge/concepts/"

    # Rule 10b: Code snippets
    if note_type == "code-snippet":
        if project:
            return f"20_projects/prj-{project}/"
        return "40_knowledge/references/"

    # Domain-based fallback
    if domain and confidence in ("HIGH", "MEDIUM"):
        if domain in ("creative-studio", "product-management", "claude-mastery"):
            return "40_knowledge/references/"
        if domain == "life-systems":
            return "00_inbox/"
        if domain == "design-team":
            return "40_knowledge/references/"
        if domain == "vault":
            return "40_knowledge/references/"

    # Default: inbox for manual review
    return "00_inbox/"


def classify_note(filepath):
    """Classify a single note file."""
    fname = filepath.name
    fname_lower = fname.lower()

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception:
        content = ""

    # Use filename + first 30 lines for classification
    first_lines = '\n'.join(content.split('\n')[:30])
    search_text = fname_lower + '\n' + first_lines.lower()
    full_text = fname_lower + '\n' + content.lower()
    line_count = len([l for l in content.split('\n') if l.strip()])

    # ── Score domains ──
    domain_scores = Counter()
    for domain, weight, pattern in DOMAIN_PATTERNS:
        matches = pattern.findall(search_text)
        if matches:
            domain_scores[domain] += len(matches) * weight
        # Also check deeper content with lower weight
        deep_matches = pattern.findall(full_text)
        if deep_matches:
            domain_scores[domain] += len(deep_matches)

    primary_domain = domain_scores.most_common(1)[0][0] if domain_scores else ""
    secondary_domains = [d for d, _ in domain_scores.most_common(3)[1:] if domain_scores[d] > 0]
    domain_list = [primary_domain] + secondary_domains if primary_domain else []

    # ── Detect type ──
    type_scores = Counter()
    for note_type, pattern in TYPE_PATTERNS:
        matches = pattern.findall(search_text)
        if matches:
            type_scores[note_type] += len(matches) * 2
        deep_matches = pattern.findall(full_text)
        if deep_matches:
            type_scores[note_type] += len(deep_matches)

    primary_type = type_scores.most_common(1)[0][0] if type_scores else "unknown"

    # ── Detect project context ──
    project = ""
    project_scores = Counter()
    for proj, pattern in PROJECT_PATTERNS:
        matches = pattern.findall(full_text)
        if matches:
            project_scores[proj] += len(matches)
    if project_scores:
        project = project_scores.most_common(1)[0][0]

    # ── Confidence ──
    total_domain_score = sum(domain_scores.values())
    total_type_score = sum(type_scores.values())
    if total_domain_score >= 10 and total_type_score >= 5:
        confidence = "HIGH"
    elif total_domain_score >= 3 or total_type_score >= 2:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    # ── Destination ──
    destination = determine_destination(primary_domain, primary_type, project, confidence)

    # ── AI context hint (first meaningful line) ──
    ai_hint = ""
    for line in content.split('\n'):
        stripped = line.strip().lstrip('#').strip()
        if stripped and len(stripped) > 5 and not stripped.startswith('---'):
            ai_hint = stripped[:120]
            break

    return {
        'filename': fname,
        'lines': line_count,
        'domain': '|'.join(domain_list) if domain_list else 'unclassified',
        'type': primary_type,
        'project': project or '',
        'destination': destination,
        'confidence': confidence,
        'ai_hint': ai_hint,
    }


def main():
    notes_dir = NOTES_DIR
    if not notes_dir.exists():
        print(f"ERROR: {notes_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    md_files = sorted(notes_dir.glob('*.md'))
    print(f"Classifying {len(md_files)} notes...", file=sys.stderr)

    results = []
    for f in md_files:
        results.append(classify_note(f))

    # Write TSV
    fields = ['filename', 'lines', 'domain', 'type', 'project', 'destination', 'confidence', 'ai_hint']
    with open(OUTPUT_TSV, 'w', newline='', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        writer.writerows(results)

    # Print summary
    dest_counts = Counter(r['destination'] for r in results)
    domain_counts = Counter(r['domain'].split('|')[0] for r in results)
    type_counts = Counter(r['type'] for r in results)
    conf_counts = Counter(r['confidence'] for r in results)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"CLASSIFICATION COMPLETE: {len(results)} notes", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    print(f"\nBy Destination:", file=sys.stderr)
    for dest, count in dest_counts.most_common():
        print(f"  {count:4d}  {dest}", file=sys.stderr)

    print(f"\nBy Domain:", file=sys.stderr)
    for dom, count in domain_counts.most_common():
        print(f"  {count:4d}  {dom}", file=sys.stderr)

    print(f"\nBy Type:", file=sys.stderr)
    for t, count in type_counts.most_common():
        print(f"  {count:4d}  {t}", file=sys.stderr)

    print(f"\nBy Confidence:", file=sys.stderr)
    for c, count in conf_counts.most_common():
        print(f"  {count:4d}  {c}", file=sys.stderr)

    print(f"\nReport written to: {OUTPUT_TSV}", file=sys.stderr)


if __name__ == '__main__':
    main()
