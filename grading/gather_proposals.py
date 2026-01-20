#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to gather proposal README.md files from student GitHub repositories.

Source repos:
  https://github.com/Alvin-Furman-CS-Classroom/project-1-proposal-<username>

Typical file location:
  README.md (usually in the repo root, but this script also searches recursively)

Output:
  proposals/<username>_<emailPrefix>_PROPOSAL.md
"""

import argparse
import io
import shutil
import subprocess
import sys
import time
from pathlib import Path


# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# Student data: (email, github_username or None)
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
REPO_PREFIX = "project-1-proposal"
OUTPUT_DIR = "proposals"
TEMP_DIR = "temp_clones_project1"


def _safe_rmtree(path: Path, max_retries: int = 3) -> None:
    if not path.exists():
        return
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                time.sleep(0.5)
            shutil.rmtree(path, ignore_errors=False)
            return
        except (PermissionError, OSError) as e:
            if attempt == max_retries - 1:
                print(f"  [WARN] Could not remove temp directory: {e}")
            continue


def extract_proposal_file(username: str, email: str, *, force: bool) -> bool:
    """Clone repository, extract README.md, and clean up."""
    repo_url = f"https://github.com/{GITHUB_ORG}/{REPO_PREFIX}-{username}.git"
    temp_repo_path = Path(TEMP_DIR) / username

    output_base = Path(OUTPUT_DIR)
    output_base.mkdir(exist_ok=True)

    Path(TEMP_DIR).mkdir(exist_ok=True)

    email_prefix = email.split("@")[0]
    output_file = output_base / f"{username}_{email_prefix}_PROPOSAL.md"

    if output_file.exists() and not force:
        print(f"Skipping {username} ({email}) - output already exists")
        return True

    print(f"Processing {username} ({email})...")

    # Always remove any old temp clone first (helps with Windows file locking edge cases)
    _safe_rmtree(temp_repo_path)

    try:
        subprocess.run(
            ["git", "clone", repo_url, str(temp_repo_path)],
            capture_output=True,
            text=True,
            check=True,
        )

        # Look for README.md (root first)
        readme_file = None
        for possible_path in [
            temp_repo_path / "README.md",
            temp_repo_path / "Readme.md",
            temp_repo_path / "readme.md",
        ]:
            if possible_path.exists():
                readme_file = possible_path
                break

        # Fallback: search recursively (some students may nest)
        if readme_file is None:
            for path in temp_repo_path.rglob("README.md"):
                readme_file = path
                break
            if readme_file is None:
                for path in temp_repo_path.rglob("readme.md"):
                    readme_file = path
                    break
            if readme_file is None:
                for path in temp_repo_path.rglob("Readme.md"):
                    readme_file = path
                    break

        if readme_file and readme_file.exists():
            shutil.copy2(readme_file, output_file)
            print("  [OK] Extracted README.md")
            return True

        print("  [FAIL] README.md not found in repository")
        return False

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        print(f"  [FAIL] Failed to clone: {error_msg}")
        return False
    finally:
        _safe_rmtree(temp_repo_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gather student project proposals (README.md) from GitHub repos.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in the output directory.",
    )
    args = parser.parse_args()

    # Check if git is available
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: git is not installed or not in PATH")
        raise SystemExit(1)

    successful = 0
    failed = 0
    skipped = 0

    for email, username in STUDENTS:
        if username is None:
            print(f"Skipping {email} (Unlinked user)")
            skipped += 1
            continue

        if extract_proposal_file(username, email, force=args.force):
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

    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Skipped: {skipped}")
    print(f"  Total: {len(STUDENTS)}")
    print(f"\nProposal files saved to: {Path(OUTPUT_DIR).absolute()}")


if __name__ == "__main__":
    main()

