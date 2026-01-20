#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to gather REFLECTION.md files from student GitHub repositories.
Downloads only the REFLECTION.md file from each repository.
"""

import subprocess
import sys
import shutil
import time
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Student data: email -> GitHub username
# Format: (email, github_username or None)
STUDENTS = [
    ("alvaad4@furman.edu", "alvaad4"),
    ("avende4@furman.edu", "davent4"),
    ("badgel9@furman.edu", "eleanorbadgett"),
    ("bailky1@furman.edu", "kcbailey111"),
    ("bonske0@furman.edu", "bonsakel"),
    ("brewma2@furman.edu", "madiganb55"),
    ("browha2@furman.edu", "HayesFBrown"),
    ("burrsy0@furman.edu", "sburroughs25"),
    ("chmiel5@furman.edu", "ElliottChmil"),
    ("clonbr7@furman.edu", "brodeeC"),
    ("corbth9@furman.edu", "Corbth9"),
    ("ctalvin@gmail.com", "wcatykid"),
    ("heidro8@furman.edu", "RonanHeidenreich"),
    ("henrgr2@furman.edu", "cptareb"),
    ("ibramo2@furman.edu", None),  # Unlinked user
    ("javeka6@furman.edu", "kalijavetski"),
    ("kingri8@furman.edu", "RickKing07"),
    ("linji9@furman.edu", "Linji9"),
    ("masvta0@furman.edu", "t-masvimbo"),
    ("nitme0@furman.edu", "MengsrunNit"),
    ("riddma9@furman.edu", "CollinRiddle"),
    ("riddmi1@furman.edu", "CaseRiddle056"),
    ("rowlse1@furman.edu", "SeanRowland7"),
    ("sahra1@furman.edu", "rahulranjansah"),
    ("shoeca6@furman.edu", "casenshoe"),
    ("sledch8@furman.edu", "sledgec04"),
    ("thommi2@furman.edu", "michaelhthomas"),
    ("wrigvi3@furman.edu", "wrigvi3"),
    ("zoelwi4@furman.edu", "Cereal-Seagull"),
]

GITHUB_ORG = "Alvin-Furman-CS-Classroom"
REPO_PREFIX = "project-0-setup"
OUTPUT_DIR = "reflections"
TEMP_DIR = "temp_clones"


def extract_reflection_file(username, email):
    """Clone repository, extract REFLECTION.md, and clean up."""
    repo_url = f"https://github.com/{GITHUB_ORG}/{REPO_PREFIX}-{username}.git"
    temp_repo_path = Path(TEMP_DIR) / username
    
    # Create output directory
    output_base = Path(OUTPUT_DIR)
    output_base.mkdir(exist_ok=True)
    
    # Create temp directory
    Path(TEMP_DIR).mkdir(exist_ok=True)
    
    # Check if file already exists
    email_prefix = email.split("@")[0]
    output_file = output_base / f"{username}_{email_prefix}_REFLECTION.md"
    if output_file.exists():
        print(f"Skipping {username} ({email}) - file already exists")
        return True
    
    print(f"Processing {username} ({email})...")
    
    # Remove temp directory if it exists
    if temp_repo_path.exists():
        try:
            shutil.rmtree(temp_repo_path)
        except Exception:
            pass
    
    try:
        # Clone repository
        subprocess.run(
            ["git", "clone", repo_url, str(temp_repo_path)],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Look for REFLECTION.md (case-insensitive search)
        reflection_file = None
        for possible_path in [
            temp_repo_path / "REFLECTION.md",
            temp_repo_path / "Reflection.md",
            temp_repo_path / "reflection.md",
        ]:
            if possible_path.exists():
                reflection_file = possible_path
                break
        
        # Also search recursively if not found in root
        if reflection_file is None:
            for path in temp_repo_path.rglob("REFLECTION.md"):
                reflection_file = path
                break
            for path in temp_repo_path.rglob("reflection.md"):
                reflection_file = path
                break
            for path in temp_repo_path.rglob("Reflection.md"):
                reflection_file = path
                break
        
        if reflection_file and reflection_file.exists():
            # Copy to output directory with descriptive name
            shutil.copy2(reflection_file, output_file)
            print(f"  [OK] Extracted REFLECTION.md")
            return True
        else:
            print(f"  [FAIL] REFLECTION.md not found in repository")
            return False
            
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        print(f"  [FAIL] Failed to clone: {error_msg}")
        return False
    finally:
        # Clean up temp directory with retry for Windows file locking
        if temp_repo_path.exists():
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # On Windows, files may be locked briefly
                    if attempt > 0:
                        time.sleep(0.5)
                    shutil.rmtree(temp_repo_path, ignore_errors=False)
                    break
                except (PermissionError, OSError) as e:
                    if attempt == max_retries - 1:
                        print(f"  [WARN] Could not remove temp directory: {e}")
                    else:
                        continue


def main():
    """Main function to gather all REFLECTION.md files."""
    # Check if git is available
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: git is not installed or not in PATH")
        sys.exit(1)
    
    # Process each student
    successful = 0
    failed = 0
    skipped = 0
    
    for email, username in STUDENTS:
        if username is None:
            print(f"Skipping {email} (Unlinked user)")
            skipped += 1
            continue
        
        if extract_reflection_file(username, email):
            successful += 1
        else:
            failed += 1
    
    # Clean up temp directory if empty
    try:
        temp_path = Path(TEMP_DIR)
        if temp_path.exists() and not any(temp_path.iterdir()):
            temp_path.rmdir()
    except Exception:
        pass
    
    # Summary
    print("\n" + "="*50)
    print("Summary:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Skipped: {skipped}")
    print(f"  Total: {len(STUDENTS)}")
    print(f"\nReflection files saved to: {Path(OUTPUT_DIR).absolute()}")


if __name__ == "__main__":
    main()
