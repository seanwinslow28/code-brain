import os
import shutil
import datetime
import argparse

# Configuration
RULES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
    'Documents': ['.pdf', '.docx', '.txt', '.md', '.csv'],
    'Installers': ['.dmg', '.pkg', '.zip', '.iso'],
    'Audio': ['.mp3', '.wav'],
    'Video': ['.mp4', '.mov']
}

def organize(inbox_path, dry_run=False):
    if not os.path.exists(inbox_path):
        print(f"Error: {inbox_path} does not exist.")
        return

    print(f"Scanning {inbox_path}...")
    
    for filename in os.listdir(inbox_path):
        if filename.startswith('.'): continue # skip hidden
        
        src = os.path.join(inbox_path, filename)
        if os.path.isdir(src): continue
        
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        dest_folder = None
        for category, extensions in RULES.items():
            if ext in extensions:
                dest_folder = category
                break
        
        if dest_folder:
            # Create subfolder
            target_dir = os.path.join(inbox_path, dest_folder)
            if not os.path.exists(target_dir):
                if not dry_run:
                    os.makedirs(target_dir)
            
            # Timestamp subfolder?
            # For now, flat structure
            dest = os.path.join(target_dir, filename)
            
            print(f"Moving '{filename}' -> '{dest_folder}/'")
            if not dry_run:
                try:
                    shutil.move(src, dest)
                except Exception as e:
                    print(f"Error moving {filename}: {e}")
        else:
            print(f"Skipping '{filename}' (Unknown extension)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inbox', required=True, help='Path to inbox')
    parser.add_argument('--dry-run', action='store_true', help='Simulate only')
    args = parser.parse_args()
    
    organize(args.inbox, args.dry_run)
