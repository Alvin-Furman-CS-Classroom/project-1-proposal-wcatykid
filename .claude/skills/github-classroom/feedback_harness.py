#!/usr/bin/env python3
"""
Student Feedback Harness Generator for GitHub Classroom.

Usage:
    python3 feedback_harness.py <command> [args]

Commands:
    snapshot <assignment_id> [--all | --student <login>]
        Create harness file(s) for student submissions

    list-snapshots <assignment_id>
        List existing snapshots for an assignment

    create-issue <assignment_id> <student_login> <feedback_file>
        Post feedback as a GitHub issue on student's repo

    evaluate <harness_file> --rubric <rubric_file>
        Generate draft feedback using Claude API

    batch-evaluate <assignment_id> --rubric <rubric_file>
        Generate draft feedback for all students
"""

import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# Optional: anthropic SDK for evaluate command
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Configuration
HARNESS_VERSION = "1.0"
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
HARNESS_DIR = REPO_ROOT / "admin" / "harnesses"
INDEX_FILE = HARNESS_DIR / "index.json"


# --- GitHub API (reusing pattern from github_classroom.py) ---

def gh_api(endpoint: str, paginate: bool = False) -> Any:
    """Make a GitHub API request using the gh CLI."""
    cmd = ["gh", "api", endpoint, "--header", "Accept: application/vnd.github+json"]
    if paginate:
        cmd.append("--paginate")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None

    if paginate and result.stdout.strip():
        lines = result.stdout.strip().split('\n')
        all_items = []
        for line in lines:
            if line.strip():
                try:
                    data = json.loads(line)
                    if isinstance(data, list):
                        all_items.extend(data)
                    else:
                        all_items.append(data)
                except json.JSONDecodeError:
                    continue
        return all_items

    return json.loads(result.stdout) if result.stdout.strip() else {}


def get_assignment(assignment_id: str) -> dict:
    """Get assignment details."""
    return gh_api(f"/assignments/{assignment_id}") or {}


def get_accepted_assignments(assignment_id: str) -> list[dict]:
    """Get all accepted assignments for an assignment."""
    return gh_api(f"/assignments/{assignment_id}/accepted_assignments", paginate=True) or []


# --- Data Classes ---

@dataclass
class FileInfo:
    """Information about a source file."""
    path: str
    content: str
    lines: int
    last_modified: str


@dataclass
class CommitInfo:
    """Git commit information."""
    sha: str
    author: str
    date: str
    message: str


@dataclass
class HarnessData:
    """Complete harness data structure."""
    assignment_id: str
    assignment_name: str
    classroom_name: str
    repo_name: str
    repo_url: str
    branch: str
    commit_sha: str
    members: list[dict]
    readme_content: str
    source_files: list[FileInfo]
    test_files: list[FileInfo]
    commits: list[CommitInfo]
    snapshot_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))


# --- Repository Operations ---

def clone_repo(repo_full_name: str, target_dir: Path, branch: str = "main") -> bool:
    """Clone a repository to a target directory."""
    result = subprocess.run(
        ["gh", "repo", "clone", repo_full_name, str(target_dir), "--", "-b", branch],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        # Try without branch specification (might be 'master')
        result = subprocess.run(
            ["gh", "repo", "clone", repo_full_name, str(target_dir)],
            capture_output=True, text=True
        )
    return result.returncode == 0


def get_commit_log(repo_dir: Path, limit: int = 20) -> list[CommitInfo]:
    """Get recent commit history."""
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "log", f"-{limit}", "--format=%H|%an|%aI|%s"],
        capture_output=True, text=True
    )
    commits = []
    for line in result.stdout.strip().split("\n"):
        if line and "|" in line:
            parts = line.split("|", 3)
            if len(parts) >= 4:
                sha, author, date, message = parts
                commits.append(CommitInfo(sha[:7], author, date[:10], message))
    return commits


def get_current_commit(repo_dir: Path) -> str:
    """Get current HEAD commit SHA."""
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "rev-parse", "HEAD"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def get_default_branch(repo_dir: Path) -> str:
    """Get the default branch name."""
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True
    )
    return result.stdout.strip() or "main"


# --- File Discovery ---

def find_python_files(repo_dir: Path, subdir: str) -> list[Path]:
    """Find all Python files in a subdirectory."""
    target_dir = repo_dir / subdir
    if not target_dir.exists():
        return []
    return sorted(target_dir.rglob("*.py"))


def find_source_files(repo_dir: Path) -> list[Path]:
    """Find all Python files in src/ directory."""
    return find_python_files(repo_dir, "src")


def find_test_files(repo_dir: Path) -> list[Path]:
    """Find all test files in test directories."""
    test_files = []
    for test_dir in ["unit_tests", "integration_tests", "tests"]:
        test_files.extend(find_python_files(repo_dir, test_dir))
    return sorted(test_files)


def read_file_info(repo_dir: Path, file_path: Path) -> FileInfo:
    """Read file content and metadata."""
    relative_path = file_path.relative_to(repo_dir)
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        content = "(unable to read file)"

    # Get last modified date from git
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "log", "-1", "--format=%aI", "--", str(relative_path)],
        capture_output=True, text=True
    )
    last_modified = result.stdout.strip()[:10] if result.stdout.strip() else "unknown"

    return FileInfo(
        path=str(relative_path),
        content=content,
        lines=len(content.splitlines()),
        last_modified=last_modified
    )


def read_readme(repo_dir: Path) -> str:
    """Read README.md content."""
    for readme_name in ["README.md", "readme.md", "README.txt", "README"]:
        readme_path = repo_dir / readme_name
        if readme_path.exists():
            try:
                return readme_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass
    return "*No README found*"


# --- Member Extraction ---

def extract_members(accepted: dict) -> list[dict]:
    """Extract student/group member info from accepted assignment."""
    members = []
    # Group assignment
    if "students" in accepted and accepted["students"]:
        for student in accepted["students"]:
            members.append({
                "login": student.get("login", "unknown"),
                "name": student.get("name") or student.get("login", "unknown")
            })
    # Individual assignment
    elif "student" in accepted and accepted["student"]:
        student = accepted["student"]
        members.append({
            "login": student.get("login", "unknown"),
            "name": student.get("name") or student.get("login", "unknown")
        })
    return members


def get_student_slug(accepted: dict) -> str:
    """Get a slug identifier for the student/group."""
    members = extract_members(accepted)
    if len(members) == 1:
        return members[0]["login"]
    elif members:
        return "-".join(sorted(m["login"] for m in members))
    return "unknown"


# --- Harness Generation ---

def generate_harness(assignment_id: str, assignment: dict, accepted: dict, repo_dir: Path) -> HarnessData:
    """Generate harness data from a cloned repository."""
    members = extract_members(accepted)
    repo = accepted.get("repository", {})

    source_files = [read_file_info(repo_dir, f) for f in find_source_files(repo_dir)]
    test_files = [read_file_info(repo_dir, f) for f in find_test_files(repo_dir)]

    return HarnessData(
        assignment_id=assignment_id,
        assignment_name=assignment.get("title", "unknown"),
        classroom_name=assignment.get("classroom", {}).get("name", "unknown"),
        repo_name=repo.get("name", "unknown"),
        repo_url=repo.get("html_url", ""),
        branch=get_default_branch(repo_dir),
        commit_sha=get_current_commit(repo_dir),
        members=members,
        readme_content=read_readme(repo_dir),
        source_files=source_files,
        test_files=test_files,
        commits=get_commit_log(repo_dir)
    )


def format_harness_markdown(data: HarnessData) -> str:
    """Format harness data as markdown."""
    lines = []

    # YAML frontmatter
    lines.append("---")
    lines.append(f'harness_version: "{HARNESS_VERSION}"')
    lines.append(f'generated: "{datetime.now().isoformat()}"')
    lines.append(f'assignment_id: "{data.assignment_id}"')
    lines.append(f'assignment_name: "{data.assignment_name}"')
    lines.append(f'classroom: "{data.classroom_name}"')
    lines.append(f'repo_name: "{data.repo_name}"')
    lines.append(f'repo_url: "{data.repo_url}"')
    lines.append(f'branch: "{data.branch}"')
    lines.append(f'commit_sha: "{data.commit_sha}"')
    lines.append(f'snapshot_date: "{data.snapshot_date}"')
    lines.append(f'type: "{"group" if len(data.members) > 1 else "individual"}"')
    lines.append("members:")
    for member in data.members:
        lines.append(f'  - login: "{member["login"]}"')
        lines.append(f'    name: "{member["name"]}"')
    lines.append("stats:")
    lines.append(f"  source_files: {len(data.source_files)}")
    lines.append(f"  test_files: {len(data.test_files)}")
    total_lines = sum(f.lines for f in data.source_files)
    lines.append(f"  total_lines: {total_lines}")
    lines.append("---")
    lines.append("")

    # Title
    if len(data.members) == 1:
        title_name = data.members[0]["name"]
    else:
        title_name = f"Team ({', '.join(m['login'] for m in data.members)})"
    lines.append(f"# Feedback Harness: {title_name} - {data.assignment_name}")
    lines.append("")
    lines.append(f"> **Assignment**: {data.assignment_name}  ")
    lines.append(f"> **Repository**: [{data.repo_name}]({data.repo_url})  ")
    lines.append(f"> **Snapshot Date**: {data.snapshot_date}  ")
    lines.append(f"> **Commit**: `{data.commit_sha[:7]}`")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Commit history
    lines.append("## Commit History (Recent 20)")
    lines.append("")
    if data.commits:
        lines.append("| Date | Author | Message | SHA |")
        lines.append("|------|--------|---------|-----|")
        for commit in data.commits:
            msg = commit.message.replace("|", "\\|")[:60]
            lines.append(f"| {commit.date} | {commit.author} | {msg} | `{commit.sha}` |")
        lines.append("")

        # Commit stats
        lines.append("### Commit Activity Summary")
        lines.append("")
        lines.append(f"- **Total commits**: {len(data.commits)}")
        author_counts: dict[str, int] = {}
        for commit in data.commits:
            author_counts[commit.author] = author_counts.get(commit.author, 0) + 1
        contrib_str = ", ".join(f"{a} ({c})" for a, c in sorted(author_counts.items(), key=lambda x: -x[1]))
        lines.append(f"- **Contributors**: {contrib_str}")
        lines.append(f"- **Date range**: {data.commits[-1].date} to {data.commits[0].date}")
    else:
        lines.append("*No commits found*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # README
    lines.append("## README")
    lines.append("")
    lines.append("<!-- BEGIN README -->")
    lines.append("```markdown")
    lines.append(data.readme_content)
    lines.append("```")
    lines.append("<!-- END README -->")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Source files
    lines.append("## Source Files")
    lines.append("")
    if data.source_files:
        lines.append("### File Tree")
        lines.append("")
        lines.append("```")
        for f in data.source_files:
            lines.append(f"  {f.path}")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

        for file_info in data.source_files:
            lines.append(f"### `{file_info.path}`")
            lines.append("")
            lines.append(f"**Lines**: {file_info.lines} | **Last Modified**: {file_info.last_modified}")
            lines.append("")
            lines.append(f"<!-- BEGIN {file_info.path} -->")
            lines.append("```python")
            lines.append(file_info.content)
            lines.append("```")
            lines.append(f"<!-- END {file_info.path} -->")
            lines.append("")
            lines.append("---")
            lines.append("")
    else:
        lines.append("*No source files found in src/*")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Test files
    lines.append("## Test Files")
    lines.append("")
    if data.test_files:
        lines.append("### Test File Listing")
        lines.append("")
        lines.append("| File | Lines |")
        lines.append("|------|-------|")
        for file_info in data.test_files:
            lines.append(f"| `{file_info.path}` | {file_info.lines} |")
        lines.append("")

        for file_info in data.test_files:
            lines.append(f"### `{file_info.path}`")
            lines.append("")
            lines.append(f"<!-- BEGIN {file_info.path} -->")
            lines.append("```python")
            lines.append(file_info.content)
            lines.append("```")
            lines.append(f"<!-- END {file_info.path} -->")
            lines.append("")
            lines.append("---")
            lines.append("")
    else:
        lines.append("*No test files found*")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Evaluation context
    lines.append("## Evaluation Context")
    lines.append("")
    lines.append("This harness should be evaluated against:")
    lines.append("")
    lines.append("1. **Module Rubric** (`admin/materials/module_rubric.md`)")
    lines.append("2. **Code Elegance Rubric** (`admin/materials/code_elegance_rubric.md`)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## End of Harness")

    return "\n".join(lines)


# --- Storage Operations ---

def save_harness(harness_md: str, assignment_slug: str, student_slug: str) -> Path:
    """Save harness to organized directory structure."""
    date_str = datetime.now().strftime("%Y-%m-%d")

    output_dir = HARNESS_DIR / "assignments" / assignment_slug / student_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{date_str}.harness.md"
    output_file.write_text(harness_md, encoding="utf-8")

    # Update latest symlink
    latest_link = output_dir / "latest.harness.md"
    if latest_link.exists() or latest_link.is_symlink():
        latest_link.unlink()
    latest_link.symlink_to(output_file.name)

    # Update index
    update_index(assignment_slug, student_slug, date_str, str(output_file.relative_to(REPO_ROOT)))

    return output_file


def update_index(assignment: str, student: str, date: str, path: str) -> None:
    """Update the harness index file."""
    index: dict = {}
    if INDEX_FILE.exists():
        try:
            index = json.loads(INDEX_FILE.read_text())
        except json.JSONDecodeError:
            index = {}

    if assignment not in index:
        index[assignment] = {}
    if student not in index[assignment]:
        index[assignment][student] = {"snapshots": []}

    index[assignment][student]["snapshots"].append({
        "date": date,
        "path": path,
        "created": datetime.now().isoformat()
    })
    index[assignment][student]["latest"] = path

    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index, indent=2))


# --- GitHub Issue Creation ---

def create_feedback_issue(repo_full_name: str, title: str, body: str) -> str:
    """Create a GitHub issue with feedback."""
    cmd = [
        "gh", "issue", "create",
        "--repo", repo_full_name,
        "--title", title,
        "--body", body,
        "--label", "ai-feedback"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        # Label might not exist, try without it
        cmd = cmd[:-2]  # Remove --label ai-feedback
        result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to create issue: {result.stderr}")

    return result.stdout.strip()


# --- Claude API Evaluation ---

def evaluate_with_claude(harness_content: str, rubric_content: str) -> str:
    """Call Claude API to evaluate student work against rubric."""
    if not ANTHROPIC_AVAILABLE:
        raise RuntimeError(
            "anthropic package not installed. Run: pip install anthropic"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable not set"
        )

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are evaluating a student submission for an AI course.

## Rubric

{rubric_content}

## Student Submission (Harness File)

{harness_content}

## Instructions

1. Evaluate the submission against each criterion in the rubric.
2. For each criterion, provide:
   - Score (0-4 as defined in the rubric)
   - Brief justification with specific examples from the submission
3. Be constructive and educational in your feedback.
4. End with an overall summary and total score.

## Format your response as:

### [Criterion Name]
**Score: X/4**
[Justification with specific examples]

...

### Overall Summary
**Total Score: X/Y**
[Summary paragraph with key strengths and areas for improvement]
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def save_draft_feedback(harness_path: Path, feedback: str) -> Path:
    """Save draft feedback alongside the harness file."""
    draft_path = harness_path.parent / f"draft-feedback-{harness_path.stem.split('.')[0]}.md"
    draft_path.write_text(feedback, encoding="utf-8")
    return draft_path


# --- Command Handlers ---

def cmd_snapshot(args: list[str]) -> None:
    """Handle the snapshot command."""
    if len(args) < 1:
        print("Usage: feedback_harness.py snapshot <assignment_id> [--all | --student <login>]")
        sys.exit(1)

    assignment_id = args[0]
    student_filter = None
    process_all = "--all" in args

    if "--student" in args:
        idx = args.index("--student")
        if idx + 1 < len(args):
            student_filter = args[idx + 1]

    # Get assignment details
    assignment = get_assignment(assignment_id)
    if not assignment:
        print(f"Error: Could not fetch assignment {assignment_id}")
        sys.exit(1)

    assignment_slug = assignment.get("slug", assignment_id)
    print(f"Assignment: {assignment.get('title', 'unknown')} ({assignment_slug})")

    # Get accepted assignments
    accepted_list = get_accepted_assignments(assignment_id)
    if not accepted_list:
        print("No accepted assignments found.")
        return

    print(f"Found {len(accepted_list)} accepted assignment(s)")

    if not process_all and not student_filter:
        print("\nUse --all to snapshot all, or --student <login> for specific student")
        print("\nStudents/groups:")
        for accepted in accepted_list:
            slug = get_student_slug(accepted)
            members = extract_members(accepted)
            names = ", ".join(m["name"] for m in members)
            print(f"  - {slug}: {names}")
        return

    # Filter if needed
    if student_filter:
        accepted_list = [a for a in accepted_list if
                        any(m["login"] == student_filter for m in extract_members(a))]
        if not accepted_list:
            print(f"No submissions found for student: {student_filter}")
            return

    # Process each
    for accepted in accepted_list:
        repo = accepted.get("repository", {})
        repo_name = repo.get("name", "unknown")
        repo_full_name = repo.get("full_name", "")
        student_slug = get_student_slug(accepted)

        print(f"\nProcessing: {student_slug} ({repo_name})")

        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_dir = Path(tmp_dir) / repo_name

            # Clone
            if not clone_repo(repo_full_name, repo_dir):
                print(f"  Failed to clone {repo_name}")
                continue

            # Generate harness
            harness_data = generate_harness(assignment_id, assignment, accepted, repo_dir)
            harness_md = format_harness_markdown(harness_data)

            # Save
            output_path = save_harness(harness_md, assignment_slug, student_slug)
            print(f"  Saved: {output_path}")


def cmd_list_snapshots(args: list[str]) -> None:
    """List existing snapshots for an assignment."""
    if len(args) < 1:
        print("Usage: feedback_harness.py list-snapshots <assignment_id>")
        sys.exit(1)

    assignment_id = args[0]

    # Get assignment to find slug
    assignment = get_assignment(assignment_id)
    assignment_slug = assignment.get("slug", assignment_id) if assignment else assignment_id

    if not INDEX_FILE.exists():
        print("No snapshots found (index file doesn't exist).")
        return

    try:
        index = json.loads(INDEX_FILE.read_text())
    except json.JSONDecodeError:
        print("Error reading index file.")
        return

    # Find matching assignment
    found = False
    for assignment_key in index:
        if assignment_id in assignment_key or assignment_key in assignment_id or assignment_slug == assignment_key:
            found = True
            print(f"\nAssignment: {assignment_key}")
            for student, data in index[assignment_key].items():
                print(f"  {student}:")
                for snapshot in data.get("snapshots", []):
                    print(f"    - {snapshot['date']}: {snapshot['path']}")

    if not found:
        print(f"No snapshots found for assignment {assignment_id}")


def cmd_create_issue(args: list[str]) -> None:
    """Handle the create-issue command."""
    if len(args) < 3:
        print("Usage: feedback_harness.py create-issue <assignment_id> <student_login> <feedback_file>")
        sys.exit(1)

    assignment_id, student_login, feedback_file = args[:3]

    # Read feedback
    feedback_path = Path(feedback_file)
    if not feedback_path.exists():
        print(f"Error: Feedback file not found: {feedback_file}")
        sys.exit(1)

    feedback_content = feedback_path.read_text(encoding="utf-8")

    # Find student's repo
    accepted_list = get_accepted_assignments(assignment_id)
    student_repo = None
    for accepted in accepted_list:
        members = extract_members(accepted)
        if any(m["login"] == student_login for m in members):
            student_repo = accepted.get("repository", {}).get("full_name")
            break

    if not student_repo:
        print(f"Error: No repository found for student {student_login}")
        sys.exit(1)

    # Create issue
    title = f"Feedback: {feedback_path.stem}"
    try:
        issue_url = create_feedback_issue(student_repo, title, feedback_content)
        print(f"Created issue: {issue_url}")
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_evaluate(args: list[str]) -> None:
    """Handle the evaluate command."""
    if len(args) < 1:
        print("Usage: feedback_harness.py evaluate <harness_file> --rubric <rubric_file>")
        sys.exit(1)

    harness_file = args[0]
    rubric_file = None

    if "--rubric" in args:
        idx = args.index("--rubric")
        if idx + 1 < len(args):
            rubric_file = args[idx + 1]

    if not rubric_file:
        print("Error: --rubric <rubric_file> is required")
        sys.exit(1)

    harness_path = Path(harness_file)
    rubric_path = Path(rubric_file)

    if not harness_path.exists():
        print(f"Error: Harness file not found: {harness_file}")
        sys.exit(1)

    if not rubric_path.exists():
        print(f"Error: Rubric file not found: {rubric_file}")
        sys.exit(1)

    print(f"Evaluating: {harness_path.name}")
    print(f"Using rubric: {rubric_path.name}")

    harness_content = harness_path.read_text(encoding="utf-8")
    rubric_content = rubric_path.read_text(encoding="utf-8")

    try:
        feedback = evaluate_with_claude(harness_content, rubric_content)
        draft_path = save_draft_feedback(harness_path, feedback)
        print(f"\nDraft feedback saved to: {draft_path}")
        print("\n--- Preview (first 500 chars) ---")
        print(feedback[:500])
        if len(feedback) > 500:
            print("...")
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_batch_evaluate(args: list[str]) -> None:
    """Handle the batch-evaluate command."""
    if len(args) < 1:
        print("Usage: feedback_harness.py batch-evaluate <assignment_id> --rubric <rubric_file>")
        sys.exit(1)

    assignment_id = args[0]
    rubric_file = None

    if "--rubric" in args:
        idx = args.index("--rubric")
        if idx + 1 < len(args):
            rubric_file = args[idx + 1]

    if not rubric_file:
        print("Error: --rubric <rubric_file> is required")
        sys.exit(1)

    rubric_path = Path(rubric_file)
    if not rubric_path.exists():
        print(f"Error: Rubric file not found: {rubric_file}")
        sys.exit(1)

    rubric_content = rubric_path.read_text(encoding="utf-8")

    # Get assignment to find slug
    assignment = get_assignment(assignment_id)
    assignment_slug = assignment.get("slug", assignment_id) if assignment else assignment_id

    # Find all harness files for this assignment
    assignment_dir = HARNESS_DIR / "assignments" / assignment_slug
    if not assignment_dir.exists():
        print(f"Error: No snapshots found for assignment {assignment_id}")
        print(f"Expected directory: {assignment_dir}")
        print("Run 'snapshot --all' first to create harness files.")
        sys.exit(1)

    # Find latest harness for each student
    student_dirs = [d for d in assignment_dir.iterdir() if d.is_dir()]
    if not student_dirs:
        print(f"No student directories found in {assignment_dir}")
        sys.exit(1)

    print(f"Found {len(student_dirs)} student(s)")
    print(f"Using rubric: {rubric_path.name}")
    print("-" * 40)

    results = []
    for student_dir in sorted(student_dirs):
        latest_link = student_dir / "latest.harness.md"
        if not latest_link.exists():
            # Try to find most recent harness
            harness_files = sorted(student_dir.glob("*.harness.md"), reverse=True)
            if not harness_files:
                print(f"  {student_dir.name}: No harness file found, skipping")
                continue
            harness_path = harness_files[0]
        else:
            harness_path = latest_link.resolve()

        print(f"  {student_dir.name}: Evaluating...")

        try:
            harness_content = harness_path.read_text(encoding="utf-8")
            feedback = evaluate_with_claude(harness_content, rubric_content)
            draft_path = save_draft_feedback(harness_path, feedback)
            results.append({
                "student": student_dir.name,
                "status": "success",
                "draft": str(draft_path)
            })
            print(f"    -> Saved: {draft_path.name}")
        except Exception as e:
            results.append({
                "student": student_dir.name,
                "status": "error",
                "error": str(e)
            })
            print(f"    -> Error: {e}")

    # Summary
    print("-" * 40)
    success = sum(1 for r in results if r["status"] == "success")
    print(f"Completed: {success}/{len(results)} students")

    if success > 0:
        print(f"\nDraft feedback files are in: {assignment_dir}/*/")
        print("Review each draft-feedback-*.md file before posting.")


# --- Main Entry Point ---

def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "snapshot": cmd_snapshot,
        "list-snapshots": cmd_list_snapshots,
        "create-issue": cmd_create_issue,
        "evaluate": cmd_evaluate,
        "batch-evaluate": cmd_batch_evaluate,
    }

    if command not in commands:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

    commands[command](args)


if __name__ == "__main__":
    main()
