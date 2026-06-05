#!/usr/bin/env python3
import sys
import os
import re
from pypdf import PdfReader

def clean_text(text):
    return text.replace('\xa0', ' ').strip()

def is_page_number_line(line):
    return bool(re.match(r'^\s*\d+\.?\s*$', line))

def is_footer_header(line):
    cleaned = line.strip()
    if not cleaned:
        return True
    if "Created using Celtx" in cleaned:
        return True
    return False

def parse_pdf_to_blocks(pdf_path):
    reader = PdfReader(pdf_path)
    raw_blocks = []
    
    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text(extraction_mode="layout")
        lines = page_text.split('\n')
        
        for line in lines:
            cleaned_line = line.rstrip()
            if not cleaned_line:
                raw_blocks.append({
                    'type': 'empty',
                    'content': '',
                    'indent': 0
                })
                continue
            
            # Skip page numbers and footers
            if is_page_number_line(cleaned_line) or is_footer_header(cleaned_line):
                continue
            
            # Skip (MORE) page break indicators
            if cleaned_line.strip() == "(MORE)":
                continue
                
            indent = len(cleaned_line) - len(cleaned_line.lstrip(' '))
            content = cleaned_line.strip()
            
            # Classify line
            if content.startswith('(') and content.endswith(')'):
                raw_blocks.append({
                    'type': 'parenthetical',
                    'content': content,
                    'indent': indent
                })
            elif 18 <= indent <= 27 and content.isupper():
                char_name = content
                char_name = re.sub(r'\(CONT\'D\)', ' (CONT\'D)', char_name)
                char_name = re.sub(r'\(V\.O\)', ' (V.O)', char_name)
                char_name = re.sub(r'\s+', ' ', char_name)
                raw_blocks.append({
                    'type': 'character',
                    'content': char_name,
                    'indent': indent
                })
            elif 8 <= indent <= 17:
                raw_blocks.append({
                    'type': 'dialogue',
                    'content': content,
                    'indent': indent
                })
            elif content.isupper() and (
                content.startswith('INT.') or 
                content.startswith('EXT.') or 
                content.startswith('INT/EXT.') or 
                content.startswith('EXT/INT.') or
                content.startswith('I/E.') or
                content.startswith('INT ') or
                content.startswith('EXT ')
            ):
                raw_blocks.append({
                    'type': 'scene_heading',
                    'content': content,
                    'indent': indent
                })
            elif content.isupper() and content.endswith(':') and len(content) < 20:
                raw_blocks.append({
                    'type': 'transition',
                    'content': content,
                    'indent': indent
                })
            elif content.startswith('GRAPHIC:'):
                raw_blocks.append({
                    'type': 'graphic',
                    'content': content,
                    'indent': indent
                })
            else:
                raw_blocks.append({
                    'type': 'action',
                    'content': content,
                    'indent': indent
                })
                
    return raw_blocks

def merge_blocks(raw_blocks):
    merged = []
    
    current_char = None
    current_dialogue = []
    current_action = []
    current_graphic = []
    intervened = False
    
    def flush_action():
        if current_action:
            action_text = " ".join(current_action)
            action_text = re.sub(r'\s+', ' ', action_text).strip()
            if action_text:
                merged.append({'type': 'action', 'content': action_text})
            current_action.clear()
            
    def flush_graphic():
        if current_graphic:
            graphic_text = " ".join(current_graphic)
            graphic_text = re.sub(r'\s+', ' ', graphic_text).strip()
            if graphic_text:
                merged.append({'type': 'graphic', 'content': graphic_text})
            current_graphic.clear()

    def flush_dialogue():
        if current_char and current_dialogue:
            merged.append({
                'type': 'character_speech',
                'character': current_char,
                'speech': list(current_dialogue)
            })
            current_dialogue.clear()

    for block in raw_blocks:
        b_type = block['type']
        b_content = block['content']
        
        if b_type == 'empty':
            flush_action()
            flush_graphic()
            
        elif b_type == 'scene_heading':
            flush_action()
            flush_graphic()
            flush_dialogue()
            current_char = None
            intervened = True
            merged.append(block)
            
        elif b_type == 'transition':
            flush_action()
            flush_graphic()
            flush_dialogue()
            current_char = None
            intervened = True
            merged.append(block)
            
        elif b_type == 'graphic':
            flush_action()
            flush_graphic()
            flush_dialogue()
            current_char = None
            intervened = True
            current_graphic.append(b_content)
            
        elif b_type == 'character':
            flush_action()
            flush_graphic()
            
            # Extract base character name by removing (CONT'D), (V.O.), etc.
            base_char = re.sub(r'\s*\((CONT\'D|CONT\b.*?|V\.O\.|V\.O)\)', '', b_content, flags=re.IGNORECASE).strip()
            
            is_continuation = False
            if current_char:
                current_base = re.sub(r'\s*\((CONT\'D|CONT\b.*?|V\.O\.|V\.O)\)', '', current_char, flags=re.IGNORECASE).strip()
                if current_base == base_char and not intervened:
                    is_continuation = True
            
            if is_continuation:
                # Update current character name (e.g. might have CONT'D now)
                current_char = b_content
            else:
                flush_dialogue()
                current_char = b_content
                intervened = False
                
        elif b_type == 'dialogue':
            flush_action()
            flush_graphic()
            if current_char:
                current_dialogue.append({'type': 'dialogue', 'content': b_content})
            else:
                current_action.append(b_content)
                intervened = True
                
        elif b_type == 'parenthetical':
            flush_action()
            flush_graphic()
            if current_char:
                current_dialogue.append({'type': 'parenthetical', 'content': b_content})
            else:
                current_action.append(b_content)
                intervened = True
                
        elif b_type == 'action':
            if current_graphic:
                current_graphic.append(b_content)
            else:
                flush_dialogue()
                current_char = None
                intervened = True
                current_action.append(b_content)
                
    # Final flushes
    flush_action()
    flush_graphic()
    flush_dialogue()
    
    return merged

def format_markdown(merged_blocks, title="Screenplay"):
    md_lines = []
    md_lines.append(f"# {title}")
    md_lines.append("")
    
    for block in merged_blocks:
        b_type = block['type']
        
        if b_type == 'scene_heading':
            md_lines.append(f"## {block['content']}")
            md_lines.append("")
        elif b_type == 'transition':
            md_lines.append(f"<p align=\"right\"><i>{block['content']}</i></p>")
            md_lines.append("")
        elif b_type == 'graphic':
            # Remove "GRAPHIC:" prefix from text, and wrap in bold
            text = block['content']
            if text.startswith('GRAPHIC:'):
                text = text[len('GRAPHIC:'):].strip()
            md_lines.append(f"**{text}**")
            md_lines.append("")
        elif b_type == 'action':
            md_lines.append(block['content'])
            md_lines.append("")
        elif b_type == 'character_speech':
            char = block['character']
            speech_elements = block['speech']
            
            md_lines.append(f"**{char}**")
            
            dialogue_text = []
            for element in speech_elements:
                if element['type'] == 'parenthetical':
                    if dialogue_text:
                        md_lines.append("> " + " ".join(dialogue_text))
                        dialogue_text = []
                    md_lines.append(f"> *{element['content']}*")
                else:
                    dialogue_text.append(element['content'])
            
            if dialogue_text:
                md_lines.append("> " + " ".join(dialogue_text))
                
            md_lines.append("")
            
    content = "\n".join(md_lines)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: convert_script.py <input_pdf_path> [output_md_path]")
        sys.exit(1)
        
    pdf_path = sys.argv[1]
    
    if len(sys.argv) >= 3:
        md_path = sys.argv[2]
    else:
        md_path = os.path.splitext(pdf_path)[0] + ".md"
        
    title = os.path.splitext(os.path.basename(pdf_path))[0]
    
    print(f"Parsing {pdf_path}...")
    raw_blocks = parse_pdf_to_blocks(pdf_path)
    print(f"Parsed {len(raw_blocks)} raw blocks.")
    
    merged_blocks = merge_blocks(raw_blocks)
    print(f"Merged into {len(merged_blocks)} screenplay elements.")
    
    markdown_content = format_markdown(merged_blocks, title=title)
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
    print(f"Successfully wrote Markdown to {md_path}")

if __name__ == "__main__":
    main()
