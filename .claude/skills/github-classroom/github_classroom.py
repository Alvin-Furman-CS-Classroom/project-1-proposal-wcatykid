#!/usr/bin/env python3
"""
GitHub Classroom API wrapper using the gh CLI for authentication.

Usage:
    python3 github_classroom.py <command> [args]

Commands:
    classrooms              List all classrooms
    classroom <id>          Get classroom details
    assignments [id]        List assignments for a classroom (uses config if no id)
    assignment <id>         Get assignment details
    accepted <id>           List accepted assignments (student repos)
    grades <id>             Get assignment grades
    create-template <project_file> <output_dir>
                            Scaffold a template repo from a project file
    push-template <template_dir> <repo_name>
                            Push template to GitHub org (from config)
    sync-template <source_dir> <repo_name>
                            Sync a local directory to a GitHub template repo
    sync-all-templates      Sync all templates defined in config.json
    sync-assignment <assignment_id> <project_file>
                            Update project frontmatter with assignment metadata
    config                  Show current configuration
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

# Config file location (same directory as this script)
CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config() -> dict:
    """Load configuration from config.json."""
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}


def show_config() -> None:
    """Display current configuration."""
    config = load_config()
    if config:
        print(json.dumps(config, indent=2))
    else:
        print(json.dumps({"error": "No config.json found", "path": str(CONFIG_PATH)}, indent=2))


def gh_api(endpoint: str, paginate: bool = False) -> Any:
    """Make a GitHub API request using the gh CLI."""
    cmd = ["gh", "api", endpoint, "--header", "Accept: application/vnd.github+json"]
    if paginate:
        cmd.append("--paginate")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Handle paginated results (multiple JSON arrays)
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


def list_classrooms() -> None:
    """List all GitHub Classrooms for the current user."""
    data = gh_api("/classrooms", paginate=True)
    print(json.dumps(data, indent=2))


def get_classroom(classroom_id: str) -> None:
    """Get details for a specific classroom."""
    data = gh_api(f"/classrooms/{classroom_id}")
    print(json.dumps(data, indent=2))


def list_assignments(classroom_id: str) -> None:
    """List all assignments for a classroom."""
    data = gh_api(f"/classrooms/{classroom_id}/assignments", paginate=True)
    print(json.dumps(data, indent=2))


def get_assignment(assignment_id: str) -> None:
    """Get details for a specific assignment."""
    data = gh_api(f"/assignments/{assignment_id}")
    print(json.dumps(data, indent=2))


def list_accepted(assignment_id: str) -> None:
    """List accepted assignments (student repositories)."""
    data = gh_api(f"/assignments/{assignment_id}/accepted_assignments", paginate=True)
    print(json.dumps(data, indent=2))


def get_grades(assignment_id: str) -> None:
    """Get grades for an assignment."""
    data = gh_api(f"/assignments/{assignment_id}/grades")
    print(json.dumps(data, indent=2))


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content.

    Returns (frontmatter_dict, body_content).
    Uses simple parsing to avoid PyYAML dependency.
    """
    frontmatter = {}
    body = content

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            # Simple YAML parsing for basic key-value pairs and lists
            current_key = None
            current_list = None
            for line in fm_text.split('\n'):
                stripped = line.strip()
                if not stripped:
                    continue
                # Check for list item
                if stripped.startswith('- ') and current_key:
                    if current_list is None:
                        current_list = []
                        frontmatter[current_key] = current_list
                    current_list.append(stripped[2:].strip().strip('"\''))
                # Check for key: value
                elif ':' in line and not line.startswith(' ') and not line.startswith('\t'):
                    key, _, value = line.partition(':')
                    current_key = key.strip()
                    value = value.strip().strip('"\'')
                    current_list = None
                    if value:
                        frontmatter[current_key] = value
            body = parts[2].lstrip('\n')

    return frontmatter, body


def write_frontmatter(frontmatter: dict, body: str) -> str:
    """Combine frontmatter and body back into markdown.

    Uses simple formatting to avoid PyYAML dependency.
    """
    if not frontmatter:
        return body

    lines = []
    for key, value in frontmatter.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                # Quote strings with special chars
                if ':' in str(item) or '\n' in str(item):
                    lines.append(f'  - "{item}"')
                else:
                    lines.append(f"  - {item}")
        elif isinstance(value, str) and (':' in value or '\n' in value):
            lines.append(f'{key}: "{value}"')
        else:
            lines.append(f"{key}: {value}")

    fm_str = '\n'.join(lines)
    return f"---\n{fm_str}\n---\n\n{body}"


def create_template(project_file: str, output_dir: str) -> None:
    """Scaffold a template repository from a project file."""
    project_path = Path(project_file)
    output_path = Path(output_dir)

    if not project_path.exists():
        print(f"Error: Project file not found: {project_file}", file=sys.stderr)
        sys.exit(1)

    # Read and parse the project file
    content = project_path.read_text()
    frontmatter, body = parse_frontmatter(content)

    # Create output directory structure
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "src").mkdir(exist_ok=True)
    (output_path / "unit_tests").mkdir(exist_ok=True)
    (output_path / "integration_tests").mkdir(exist_ok=True)

    # Extract project title from first heading
    title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    title = title_match.group(1) if title_match else "Project"

    # Create README.md
    readme_content = f"""# {title}

This repository is a template for the {title} assignment.

## Project Structure

```
├── src/              # Source code
├── unit_tests/       # Unit tests
├── integration_tests/ # Integration tests
└── README.md
```

## Getting Started

1. Accept the assignment via GitHub Classroom
2. Clone your repository
3. Review the assignment requirements
4. Implement your solution in `src/`
5. Add tests in `unit_tests/` and `integration_tests/`

## Requirements

See the full assignment specification for detailed requirements.
"""

    (output_path / "README.md").write_text(readme_content)

    # Create placeholder files
    (output_path / "src" / "__init__.py").write_text('"""Source code package."""\n')
    (output_path / "unit_tests" / "__init__.py").write_text('"""Unit tests package."""\n')
    (output_path / "unit_tests" / "test_placeholder.py").write_text('''"""Placeholder test file."""

def test_placeholder():
    """Remove this test and add your own."""
    assert True
''')
    (output_path / "integration_tests" / "__init__.py").write_text('"""Integration tests package."""\n')

    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
.Python
*.so
.eggs/
*.egg-info/
*.egg

# Virtual environments
venv/
.venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
"""
    (output_path / ".gitignore").write_text(gitignore_content)

    print(json.dumps({
        "status": "success",
        "template_dir": str(output_path.absolute()),
        "files_created": [
            "README.md",
            "src/__init__.py",
            "unit_tests/__init__.py",
            "unit_tests/test_placeholder.py",
            "integration_tests/__init__.py",
            ".gitignore"
        ]
    }, indent=2))


def push_template(template_dir: str, repo_name: str) -> None:
    """Push a template directory to GitHub as a template repository."""
    config = load_config()
    org = config.get("org")

    if not org:
        print(json.dumps({"error": "No 'org' configured in config.json"}, indent=2), file=sys.stderr)
        sys.exit(1)

    template_path = Path(template_dir)
    if not template_path.exists():
        print(f"Error: Template directory not found: {template_dir}", file=sys.stderr)
        sys.exit(1)

    full_repo = f"{org}/{repo_name}"

    # Initialize git if needed
    git_dir = template_path / ".git"
    if not git_dir.exists():
        result = subprocess.run(
            ["git", "init"],
            cwd=template_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Error initializing git: {result.stderr}", file=sys.stderr)
            sys.exit(1)

    # Add all files
    subprocess.run(["git", "add", "."], cwd=template_path, capture_output=True)

    # Check if there are changes to commit
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=template_path,
        capture_output=True,
        text=True
    )

    if status.stdout.strip():
        # Commit changes
        result = subprocess.run(
            ["git", "commit", "-m", "Initial template"],
            cwd=template_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0 and "nothing to commit" not in result.stdout:
            print(f"Error committing: {result.stderr}", file=sys.stderr)
            sys.exit(1)

    # Create repo and push using gh cli
    result = subprocess.run(
        ["gh", "repo", "create", full_repo, "--template", "--public", "--source=.", "--push"],
        cwd=template_path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        # Check if repo already exists
        if "already exists" in result.stderr:
            print(json.dumps({
                "status": "error",
                "error": "Repository already exists",
                "repo": full_repo,
                "hint": "Delete the existing repo or use a different name"
            }, indent=2), file=sys.stderr)
        else:
            print(f"Error creating repo: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    repo_url = f"https://github.com/{full_repo}"
    print(json.dumps({
        "status": "success",
        "repo": full_repo,
        "url": repo_url,
        "template": True,
        "next_step": f"Create assignment in GitHub Classroom using {repo_url} as template"
    }, indent=2))


def repo_exists(repo_full_name: str) -> bool:
    """Check if a GitHub repository exists."""
    result = subprocess.run(
        ["gh", "repo", "view", repo_full_name],
        capture_output=True, text=True
    )
    return result.returncode == 0


def sync_template(source_dir: str, repo_name: str) -> None:
    """Sync a local directory to a GitHub template repository.

    Creates the repo if it doesn't exist, otherwise updates it.
    Uses rsync-style copy to avoid git subtree complications.
    """
    config = load_config()
    org = config.get("org")

    if not org:
        print(json.dumps({"error": "No 'org' configured in config.json"}, indent=2), file=sys.stderr)
        sys.exit(1)

    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"Error: Source directory not found: {source_dir}", file=sys.stderr)
        sys.exit(1)

    if not source_path.is_dir():
        print(f"Error: Source is not a directory: {source_dir}", file=sys.stderr)
        sys.exit(1)

    full_repo = f"{org}/{repo_name}"
    repo_url = f"https://github.com/{full_repo}"

    # Check if repo exists
    exists = repo_exists(full_repo)

    with tempfile.TemporaryDirectory() as tmp_dir:
        work_dir = Path(tmp_dir) / repo_name

        if exists:
            # Clone existing repo
            print(f"Cloning existing repo: {full_repo}")
            result = subprocess.run(
                ["gh", "repo", "clone", full_repo, str(work_dir)],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Error cloning repo: {result.stderr}", file=sys.stderr)
                sys.exit(1)
        else:
            # Create new repo
            print(f"Creating new repo: {full_repo}")
            result = subprocess.run(
                ["gh", "repo", "create", full_repo, "--public", "--clone"],
                cwd=tmp_dir,
                capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Error creating repo: {result.stderr}", file=sys.stderr)
                sys.exit(1)

            # Make it a template repo via API
            print("Configuring as template repository...")
            api_result = subprocess.run(
                ["gh", "api", "-X", "PATCH", f"/repos/{full_repo}",
                 "-f", "is_template=true"],
                capture_output=True, text=True
            )
            if api_result.returncode != 0:
                print(f"Warning: Could not set as template: {api_result.stderr}", file=sys.stderr)

            # gh repo create --clone creates the dir
            if not work_dir.exists():
                work_dir.mkdir()
                subprocess.run(["git", "init"], cwd=work_dir, capture_output=True)
                subprocess.run(
                    ["git", "remote", "add", "origin", f"git@github.com:{full_repo}.git"],
                    cwd=work_dir, capture_output=True
                )

        # Sync files: delete everything except .git, then copy source
        git_dir = work_dir / ".git"

        # Remove all files except .git
        for item in work_dir.iterdir():
            if item.name != ".git":
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

        # Copy source files (excluding any .git in source)
        for item in source_path.iterdir():
            if item.name == ".git":
                continue
            dest = work_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        # Check for changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=work_dir, capture_output=True, text=True
        )

        if not result.stdout.strip():
            print(json.dumps({
                "status": "no_changes",
                "repo": full_repo,
                "url": repo_url,
                "message": "No changes to sync"
            }, indent=2))
            return

        # Stage all changes
        subprocess.run(["git", "add", "-A"], cwd=work_dir, capture_output=True)

        # Commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        commit_msg = f"Sync from main repo at {timestamp}"

        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=work_dir, capture_output=True, text=True
        )

        if result.returncode != 0 and "nothing to commit" not in result.stdout:
            print(f"Error committing: {result.stderr}", file=sys.stderr)
            sys.exit(1)

        # Push
        print(f"Pushing changes to {full_repo}...")
        result = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=work_dir, capture_output=True, text=True
        )

        # Try 'master' if 'main' fails
        if result.returncode != 0:
            result = subprocess.run(
                ["git", "push", "-u", "origin", "master"],
                cwd=work_dir, capture_output=True, text=True
            )

        if result.returncode != 0:
            print(f"Error pushing: {result.stderr}", file=sys.stderr)
            sys.exit(1)

    # Print success and next steps
    print(json.dumps({
        "status": "success",
        "repo": full_repo,
        "url": repo_url,
        "created": not exists,
        "next_steps": [
            f"1. Go to GitHub Classroom and create/update assignment",
            f"2. Use template repo: {repo_url}",
            f"3. Run sync-assignment to link metadata back to project file"
        ]
    }, indent=2))


def sync_all_templates() -> None:
    """Sync all templates defined in config.json."""
    config = load_config()
    templates = config.get("templates", {})

    if not templates:
        print("No templates configured in config.json")
        print("Add a 'templates' mapping like:")
        print(json.dumps({
            "templates": {
                "paths/projects/project-0-setup/project-0-setup-repository": "csc343-project-0-setup"
            }
        }, indent=2))
        sys.exit(1)

    results = []
    for source_dir, repo_name in templates.items():
        print(f"\n{'='*50}")
        print(f"Syncing: {source_dir} -> {repo_name}")
        print('='*50)

        try:
            sync_template(source_dir, repo_name)
            results.append({"source": source_dir, "repo": repo_name, "status": "success"})
        except SystemExit:
            results.append({"source": source_dir, "repo": repo_name, "status": "failed"})

    print(f"\n{'='*50}")
    print("Summary:")
    print('='*50)
    success = sum(1 for r in results if r["status"] == "success")
    print(f"Synced: {success}/{len(results)} templates")


def sync_assignment(assignment_id: str, project_file: str) -> None:
    """Update project file frontmatter with assignment metadata."""
    project_path = Path(project_file)

    if not project_path.exists():
        print(f"Error: Project file not found: {project_file}", file=sys.stderr)
        sys.exit(1)

    # Fetch assignment details from GitHub Classroom API
    assignment = gh_api(f"/assignments/{assignment_id}")

    if not assignment:
        print(f"Error: Could not fetch assignment {assignment_id}", file=sys.stderr)
        sys.exit(1)

    # Read and parse the project file
    content = project_path.read_text()
    frontmatter, body = parse_frontmatter(content)

    # Update frontmatter with assignment metadata
    frontmatter["assignment_id"] = assignment.get("id")
    frontmatter["assignment_url"] = assignment.get("invite_link")

    # Include additional useful metadata
    if assignment.get("title"):
        frontmatter["assignment_title"] = assignment.get("title")
    if assignment.get("starter_code_repository"):
        repo = assignment["starter_code_repository"]
        frontmatter["template_repo"] = repo.get("html_url") or repo.get("full_name")

    # Write updated content back
    updated_content = write_frontmatter(frontmatter, body)
    project_path.write_text(updated_content)

    print(json.dumps({
        "status": "success",
        "project_file": str(project_path.absolute()),
        "assignment_id": assignment.get("id"),
        "assignment_url": assignment.get("invite_link"),
        "assignment_title": assignment.get("title")
    }, indent=2))


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    # Commands: (function, min_args, max_args) - if max_args is None, uses min_args
    commands = {
        "classrooms": (list_classrooms, 0, 0),
        "classroom": (get_classroom, 1, 1),
        "assignments": (list_assignments, 0, 1),  # optional classroom_id, uses config
        "assignment": (get_assignment, 1, 1),
        "accepted": (list_accepted, 1, 1),
        "grades": (get_grades, 1, 1),
        "create-template": (create_template, 2, 2),
        "push-template": (push_template, 2, 2),
        "sync-template": (sync_template, 2, 2),
        "sync-all-templates": (sync_all_templates, 0, 0),
        "sync-assignment": (sync_assignment, 2, 2),
        "config": (show_config, 0, 0),
    }

    if command not in commands:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

    func, min_args, max_args = commands[command]
    provided_args = len(sys.argv) - 2

    if provided_args < min_args:
        print(f"Error: {command} requires at least {min_args} argument(s)")
        sys.exit(1)

    if provided_args > max_args:
        provided_args = max_args

    # Handle optional args with config defaults
    if command == "assignments" and provided_args == 0:
        config = load_config()
        classroom_id = config.get("classroom_id")
        if not classroom_id:
            print("Error: No classroom_id argument and none configured in config.json", file=sys.stderr)
            sys.exit(1)
        func(str(classroom_id))
    elif provided_args == 0:
        func()
    else:
        func(*sys.argv[2:2 + provided_args])


if __name__ == "__main__":
    main()
