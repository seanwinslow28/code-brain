import csv
import re
import argparse
import os
import sys

def parse_markdown_to_cards(file_path):
    """
    Parses a markdown file into Anki-compatible cards.
    
    Expected Format:
    # Deck Name (Optional)
    
    ## Basic Card: The Concept
    Back of the card explanation.
    
    ## Cloze Card: Code Example
    The function {{c1::print()}} outputs text.
    """
    
    cards = []
    current_deck = "Default"
    
    # Regex for cloze deletions {{c1::answer}}
    cloze_pattern = re.compile(r"\{\{c\d+::.*?\}\}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
        
    current_front = None
    current_back = []
    current_tags = []
    
    for line in lines:
        line = line.strip()
        
        # Tags/Deck (H1)
        if line.startswith("# "):
            current_deck = line[2:].strip()
            current_tags.append(current_deck.replace(" ", "_"))
            continue
            
        # New Card (H2)
        if line.startswith("## "):
            # Save previous
            if current_front:
                save_card(cards, current_front, current_back, current_tags, cloze_pattern)
            
            # Start new
            current_front = line[3:].strip()
            current_back = []
            continue
            
        # Content
        if current_front is not None:
            current_back.append(line)
            
    # Save last card
    if current_front:
        save_card(cards, current_front, current_back, current_tags, cloze_pattern)

    return cards

def save_card(cards, front, back_lines, tags, cloze_pattern):
    # Determine type
    full_back = "\n".join(back_lines).strip()
    full_front = front
    
    is_cloze_back = cloze_pattern.search(full_back)
    is_cloze_front = cloze_pattern.search(full_front)
    
    if is_cloze_front or is_cloze_back:
        card_type = "Cloze"
        # For Cloze, Front is the main field. Back is 'Extra'.
        # We combine H2 and body for the Text.
        text = f"{front}\n{full_back}"
        cards.append({
            "Front": text,
            "Back": "", # Extra field empty for now
            "Tags": " ".join(tags),
            "Type": "Cloze"
        })
    else:
        card_type = "Basic"
        cards.append({
            "Front": front,
            "Back": full_back,
            "Tags": " ".join(tags),
            "Type": "Basic"
        })

def write_csv(cards, output_file):
    """Writes to Anki-importable CSV (tab-separated)."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t') 
        # Anki expects: Front, Back, Tags (for Basic)
        # We are simplifying to ensure import works.
        count = 0
        for card in cards:
            writer.writerow([card["Front"], card["Back"], card["Tags"]])
            count += 1
            
    print(f"Successfully converted {count} cards to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Markdown notes to Anki CSV')
    parser.add_argument('--input', required=True, help='Input markdown file')
    parser.add_argument('--output', required=True, help='Output CSV file')
    args = parser.parse_args()
    
    cards_list = parse_markdown_to_cards(args.input)
    write_csv(cards_list, args.output)
