# Claude Skills Guide

This document describes the Claude Code skills available for CSC-343 course administration.

## Overview

Skills are located in `.claude/skills/` and provide automated tooling for:

- GitHub Classroom management
- Student work evaluation
- Lecture content conversion

## Prerequisites

- **GitHub CLI** (`gh`): Follow install instructions [here](https://cli.github.com/)
- **Claude Code**: Skills are designed to work with Claude Code (also compatible with Cursor). Install instructions [here](https://code.claude.com/docs/en/overview).

---

## GitHub Classroom Skill

**Location**: `.claude/skills/github-classroom/`

Manages GitHub Classroom operations including listing classrooms/assignments, creating templates, and generating student feedback.

### Scripts

| Script                | Purpose                                      |
| --------------------- | -------------------------------------------- |
| `github_classroom.py` | Core GitHub Classroom API wrapper            |
| `feedback_harness.py` | Student work snapshots and feedback delivery |

### Core Commands

```bash
# List all classrooms you administer
python3 .claude/skills/github-classroom/github_classroom.py classrooms

# Get classroom details
python3 .claude/skills/github-classroom/github_classroom.py classroom <classroom_id>

# List assignments for a classroom
python3 .claude/skills/github-classroom/github_classroom.py assignments <classroom_id>

# Get assignment details
python3 .claude/skills/github-classroom/github_classroom.py assignment <assignment_id>

# List student repos for an assignment
python3 .claude/skills/github-classroom/github_classroom.py accepted <assignment_id>

# Get assignment grades
python3 .claude/skills/github-classroom/github_classroom.py grades <assignment_id>
```

### Template & Assignment Commands

```bash
# Create template repo structure from a project file
python3 .claude/skills/github-classroom/github_classroom.py create-template <project_file> <output_dir>

# Sync assignment metadata back to project file
python3 .claude/skills/github-classroom/github_classroom.py sync-assignment <assignment_id> <project_file>
```

### Feedback Harness Commands

```bash
# List students for an assignment
python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id>

# Create snapshot for all students
python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id> --all

# Create snapshot for specific student
python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id> --student <login>

# List existing snapshots
python3 .claude/skills/github-classroom/feedback_harness.py list-snapshots <assignment_id>

# Post feedback as GitHub issue
python3 .claude/skills/github-classroom/feedback_harness.py create-issue <assignment_id> <student_login> <feedback.md>
```

### Common Workflows

#### Creating a New Assignment

1. Create a project file (e.g., `paths/module-1.project.md`)
2. Generate template structure:
   ```bash
   python3 .claude/skills/github-classroom/github_classroom.py create-template paths/module-1.project.md /tmp/module-1-template
   ```
3. Push template to GitHub:
   ```bash
   cd /tmp/module-1-template
   git init && git add . && git commit -m "Initial template"
   gh repo create org/module-1-template --template --public --source=.
   git push -u origin main
   ```
4. Create assignment in GitHub Classroom web UI using the template
5. Sync metadata back:
   ```bash
   python3 .claude/skills/github-classroom/github_classroom.py sync-assignment <assignment_id> paths/module-1.project.md
   ```

#### Evaluating Student Work

1. Create snapshots:
   ```bash
   python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id> --all
   ```
2. Review harness files in `admin/harnesses/assignments/<slug>/`
3. Evaluate against rubrics (Module Rubric, Code Elegance Rubric)
4. Write feedback markdown file
5. Deliver feedback:
   ```bash
   python3 .claude/skills/github-classroom/feedback_harness.py create-issue <assignment_id> <student> feedback.md
   ```

### Harness File Format

Harness files are self-contained snapshots stored at:

```
admin/harnesses/assignments/{assignment-slug}/{student}/{date}.harness.md
```

Each harness includes:

- YAML frontmatter with metadata
- Commit history with author attribution
- README content
- Full source file contents (from `src/`)
- Full test file contents (from `unit_tests/`, `integration_tests/`)
- References to evaluation rubrics

---

## Slides to Lecture Skill

**Location**: `.claude/skills/slides-to-lecture/`

Converts exported PowerPoint slide images into PathMX `.lecture.md` files using vision analysis.

### When to Use

Ask Claude to convert slides when you want to:

- Convert exported slide images to PathMX lecture format
- Create markdown-based lecture content from visual presentations
- Extract the conceptual "spine" of a presentation

### Input Requirements

Export slides from PowerPoint as images:

1. File → Export → Change File Type → PNG
2. Save to a folder (e.g., `admin/materials/1 Propositional Logic/`)

Expected folder structure:

```
admin/materials/1 Propositional Logic/
├── 1 Propositional Logic.pptx  # Original PowerPoint
├── Slide1.png
├── Slide2.png
...
└── SlideN.png
```

### Usage

Simply ask Claude:

- "Convert the propositional logic slides to a lecture file"
- "Create a lecture from the slides in admin/materials/2 Uninformed Search"

### Output

The skill creates a self-contained lecture folder:

```
paths/lectures/propositional-logic/
├── propositional-logic.lecture.md   # The lecture markdown
└── slides/
    ├── 1 Propositional Logic.pptx   # Copied source
    ├── Slide1.png
    ├── Slide2.png
    └── ...
```

The lecture file includes:

- YAML frontmatter with metadata
- Overview paragraph
- Concept-based sections (not "Slide 1", "Slide 2")
- Key ideas extracted from each slide
- Links to slide images and PowerPoint file

### Duplicate Detection

The skill checks for existing conversions before processing. If a lecture already exists, it will ask for confirmation before overwriting.

---

## File Locations

| Path               | Description                       |
| ------------------ | --------------------------------- |
| `.claude/skills/`  | All skill definitions and scripts |
| `admin/harnesses/` | Generated student work snapshots  |
| `admin/materials/` | Source slides and rubrics         |
| `paths/lectures/`  | Generated lecture files           |

## Rubrics

Evaluation rubrics used by the feedback harness:

| Rubric          | Location                                  | Purpose                     |
| --------------- | ----------------------------------------- | --------------------------- |
| Module Rubric   | `admin/materials/module_rubric.md`        | Checkpoint grading (50 pts) |
| Code Elegance   | `admin/materials/code_elegance_rubric.md` | Code quality (8 criteria)   |
| Proposal Rubric | `admin/materials/proposal_rubric.md`      | Project proposals (32 pts)  |

---

## Troubleshooting

### GitHub CLI Authentication

```bash
# Check auth status
gh auth status

# Re-authenticate if needed
gh auth login
```

### No Classrooms Found

Ensure you have admin access to the GitHub Classroom organization.

### Snapshot Shows No Source Files

The harness looks for `.py` files in `src/`. If the student repo uses a different structure, files may not be captured.

### Issue Creation Fails

The `ai-feedback` label may not exist on the repo. The script will retry without the label automatically.
