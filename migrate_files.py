"""
Migration script to organize static folder into subdirectories.
Run this once to move existing files to the new folder structure.
"""
import os
import shutil
import json

STATIC_FOLDER = "static"
POSTERS_FOLDER = os.path.join(STATIC_FOLDER, "posters")
MUSIC_FOLDER = os.path.join(STATIC_FOLDER, "music")
QR_FOLDER = os.path.join(STATIC_FOLDER, "qr")
JSON_FOLDER = os.path.join(STATIC_FOLDER, "json")

def create_folders():
    """Create new folder structure"""
    for folder in [POSTERS_FOLDER, MUSIC_FOLDER, QR_FOLDER, JSON_FOLDER]:
        os.makedirs(folder, exist_ok=True)
        print(f"✓ Created folder: {folder}")

def move_file(src, dest_folder):
    """Move a file to destination folder"""
    if os.path.exists(src):
        filename = os.path.basename(src)
        dest = os.path.join(dest_folder, filename)
        shutil.move(src, dest)
        print(f"  Moved: {filename} -> {dest_folder}")
        return True
    return False

def migrate_files():
    """Move existing files to new structure"""
    print("\n🚀 Starting file migration...\n")
    
    # Create folders
    create_folders()
    
    # Load posters database
    posters_file = os.path.join(STATIC_FOLDER, "posters.json")
    if not os.path.exists(posters_file):
        print("⚠️  No posters.json found. Exiting.")
        return
    
    with open(posters_file, 'r', encoding='utf-8') as f:
        posters_data = json.load(f)
    
    print("\n📁 Moving files by category...\n")
    
    # Move each poster's files
    for poster in posters_data.get("posters", []):
        poster_id = poster.get("id")
        print(f"\nPoster: {poster_id}")
        
        # Move image
        if poster.get("image"):
            src = os.path.join(STATIC_FOLDER, poster["image"])
            move_file(src, POSTERS_FOLDER)
        
        # Move music
        if poster.get("music"):
            src = os.path.join(STATIC_FOLDER, poster["music"])
            move_file(src, MUSIC_FOLDER)
        
        # Move QR code
        if poster.get("qr_code"):
            src = os.path.join(STATIC_FOLDER, poster["qr_code"])
            move_file(src, QR_FOLDER)
        
        # Move sections file
        if poster.get("sections_file"):
            src = os.path.join(STATIC_FOLDER, poster["sections_file"])
            move_file(src, JSON_FOLDER)
    
    # Move posters.json to json folder
    print("\n📋 Moving database files...")
    move_file(posters_file, JSON_FOLDER)
    
    print("\n✨ Migration complete!\n")
    print("New folder structure:")
    print(f"  {POSTERS_FOLDER}/  - Poster images")
    print(f"  {MUSIC_FOLDER}/     - Music files")
    print(f"  {QR_FOLDER}/        - QR codes")
    print(f"  {JSON_FOLDER}/      - JSON databases")
    print(f"\n⚠️  Don't forget to keep style.css in {STATIC_FOLDER}/")

if __name__ == "__main__":
    migrate_files()
