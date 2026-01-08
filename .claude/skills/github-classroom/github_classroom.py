#!/usr/bin/env python3
"""
GitHub Classroom API wrapper using the gh CLI for authentication.

Usage:
    python3 github_classroom.py <command> [args]

Commands:
    classrooms              List all classrooms
    classroom <id>          Get classroom details
    assignments <id>        List assignments for a classroom
    assignment <id>         Get assignment details
    accepted <id>           List accepted assignments (student repos)
    grades <id>             Get assignment grades
    create-template <project_file> <output_dir>
                            Scaffold a template repo from a project file
    sync-assignment <assignment_id> <project_file>
                            Update project frontmatter with assignment metadata
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


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

    commands = {
        "classrooms": (list_classrooms, 0),
        "classroom": (get_classroom, 1),
        "assignments": (list_assignments, 1),
        "assignment": (get_assignment, 1),
        "accepted": (list_accepted, 1),
        "grades": (get_grades, 1),
        "create-template": (create_template, 2),
        "sync-assignment": (sync_assignment, 2),
    }

    if command not in commands:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

    func, arg_count = commands[command]

    if len(sys.argv) - 2 < arg_count:
        print(f"Error: {command} requires {arg_count} argument(s)")
        sys.exit(1)

    if arg_count == 0:
        func()
    else:
        func(*sys.argv[2:2 + arg_count])


if __name__ == "__main__":
    main()
