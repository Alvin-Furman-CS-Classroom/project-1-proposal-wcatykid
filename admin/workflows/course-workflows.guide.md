# CSC-343 Course Workflows

## Project 1: Proposal Workflow

- Add automated rubric review (student/group) before instructor review
- This would be the [elegent code rubric](../../paths/rubrics/code-elegance.rubric.md) and the project 1 rubric ([proposal.rubric.md](../../paths/projects/project-1-proposal/proposal.rubric.md))

## Goal:

Produce a report ("clean bill of health") and create a checkpoint review file e.g. `checkpoint-1-report.review.md` and pushed to repo under `feedback/`, feedback -> fix -> feedback -> fix -> ... -> push to repo

## Report format:

- A summary of the report at the top
- A rubric style table with checkboxes for each criterion and a numeric score out of 4 (using the rubrics from the project)
- Suggestions for this checkpoint
- Bridge for how to transition to the next checkpoint

  This document explains how the course infrastructure fits together and provides step-by-step workflows for common tasks.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        COURSE INFRASTRUCTURE                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐          │
│  │   PathMX     │      │    GitHub    │      │    Claude    │          │
│  │   (Content)  │─────▶│   Classroom  │◀────▶│   Skills     │          │
│  └──────────────┘      └──────────────┘      └──────────────┘          │
│         │                     │                     │                   │
│         │                     │                     │                   │
│         ▼                     ▼                     ▼                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐          │
│  │   Student    │      │   Student    │      │   Feedback   │          │
│  │   Reads      │─────▶│   Repos      │◀─────│   Harness    │          │
│  │   Assignment │      │              │      │              │          │
│  └──────────────┘      └──────────────┘      └──────────────┘          │
│                               │                     │                   │
│                               │                     │                   │
│                               ▼                     ▼                   │
│                        ┌──────────────┐      ┌──────────────┐          │
│                        │   GitHub     │      │   Instructor │          │
│                        │   Issues     │◀─────│   Review     │          │
│                        │   (Feedback) │      │              │          │
│                        └──────────────┘      └──────────────┘          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Components

| Component            | Purpose                                          | Location                                                                                                              |
| -------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| **PathMX**           | Student-facing content (assignments, guides)     | `paths/`                                                                                                              |
| **GitHub Classroom** | Assignment distribution, student repos           | [Classroom Admin](https://classroom.github.com/classrooms/241321390-alvin-furman-cs-classroom-csc-343-ai-spring-2026) |
| **Claude Skills**    | Automation scripts for classroom management      | `.claude/skills/github-classroom/`                                                                                    |
| **Feedback Harness** | Snapshot student work, generate/deliver feedback | `admin/harnesses/`                                                                                                    |

---

## Workflow 1: Syncing Template Repositories

Template repositories live in the main repo (e.g., `paths/projects/project-0-setup/project-0-setup-repository/`) and need to be synced to GitHub as separate template repos.

### Sync a Single Template

```bash
python3 .claude/skills/github-classroom/github_classroom.py sync-template \
    paths/projects/project-0-setup/project-0-setup-repository \
    csc343-project-0-setup
```

This will:

- Create the repo if it doesn't exist (as a template repo)
- Update it if it already exists
- Print the template URL for use in GitHub Classroom

### Sync All Templates

Templates are configured in `.claude/skills/github-classroom/config.json`:

```bash
python3 .claude/skills/github-classroom/github_classroom.py sync-all-templates
```

---

## Workflow 2: Creating a New Assignment

### Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Admin access to the classroom organization

### Steps

#### 1. Author the project in PathMX

Create or update the project file:

```
paths/projects/project-N-name/
├── name.project.md      # Assignment spec (student-facing)
├── name.rubric.md       # Grading rubric
└── project-name-repository/  # Template repo contents
    ├── README.md
    ├── AGENTS.md        # AI agent guidance
    └── src/
```

#### 2. Sync the template repository to GitHub

```bash
python3 .claude/skills/github-classroom/github_classroom.py sync-template \
    paths/projects/project-N-name/project-name-repository \
    csc343-project-name
```

This creates or updates a **template repository** in the `Alvin-Furman-CS-Classroom` org.

#### 3. Create assignment in GitHub Classroom UI

> **Note:** GitHub Classroom API is read-only. Assignment creation must be done in the web UI.

1. Go to [GitHub Classroom](https://classroom.github.com/classrooms/241321390-alvin-furman-cs-classroom-csc-343-ai-spring-2026)
2. Click "New Assignment"
3. Set title, deadline, visibility (private)
4. Select the template repo you just synced
5. Copy the **assignment ID** from the URL after creation

#### 4. Sync assignment metadata back to project file

```bash
python3 .claude/skills/github-classroom/github_classroom.py sync-assignment \
    <assignment_id> \
    paths/projects/project-N-name/name.project.md
```

This adds `assignment_id` and `assignment_url` to the project frontmatter.

#### 5. Share with students

Students accept via the invite link (now in your project frontmatter).

---

## Workflow 3: Providing Feedback

### At checkpoint time

#### 1. Create snapshots of all student work

```bash
python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id> --all
```

This clones each student repo and creates a harness file at:

```
admin/harnesses/assignments/<assignment-slug>/<student-login>/<date>.harness.md
```

#### 2. List existing snapshots

```bash
python3 .claude/skills/github-classroom/feedback_harness.py list-snapshots <assignment_id>
```

#### 3. Review harness files

Each harness file contains:

- Student info and repo metadata
- Commit history with contribution breakdown
- README content
- All source files
- All test files

#### 4. Evaluate against rubrics

Reference:

- `paths/projects/project-1-proposal/proposal.rubric.md` - Proposal rubric
- `admin/materials/module_rubric.md` - Module rubric
- `admin/materials/code_elegance_rubric.md` - Code quality rubric

You can use Claude to assist with evaluation:

```
Please evaluate this student submission against the Proposal Rubric.
Score each criterion 0-4 with justification.
Be constructive and specific.
```

#### 5. Write feedback markdown

Create a feedback file with:

- Scores per rubric criterion
- Specific examples from student code
- Constructive suggestions for improvement
- Overall summary

#### 6. Deliver feedback as GitHub issue

```bash
python3 .claude/skills/github-classroom/feedback_harness.py create-issue \
    <assignment_id> \
    <student_login> \
    path/to/feedback.md
```

This creates an issue in the student's repo with your feedback.

---

## Workflow 4: Checking Student Activity

### Option A: Watch repos (simple)

1. Go to GitHub Classroom dashboard
2. View student repos
3. Check commit activity per student

### Option B: Bulk status check

```bash
python3 .claude/skills/github-classroom/github_classroom.py accepted <assignment_id>
```

Returns JSON with all student repos and their status.

### Option C: Get grades/autograding results

```bash
python3 .claude/skills/github-classroom/github_classroom.py grades <assignment_id>
```

---

## Directory Reference

```
csc-343-ai/
├── paths/                          # Student-facing content (PathMX)
│   ├── index.path.md               # Course index
│   └── projects/                   # Project definitions
│       └── project-N/
│           ├── name.project.md     # Assignment spec
│           ├── name.rubric.md      # Grading rubric
│           └── project-*-repository/  # Template repo
│
├── admin/                          # Instructor-only content
│   ├── workflows/                  # This documentation
│   ├── harnesses/                  # Student snapshots
│   │   └── assignments/
│   │       └── <assignment>/
│   │           └── <student>/
│   │               ├── <date>.harness.md
│   │               └── latest.harness.md → (symlink)
│   └── materials/                  # Slides, rubrics
│
└── .claude/
    └── skills/
        └── github-classroom/
            ├── github_classroom.py  # API wrapper
            ├── feedback_harness.py  # Snapshot/feedback tool
            ├── prompt.md            # Skill documentation
            └── config.json          # Org/classroom config
```

---

## Configuration

Config file: `.claude/skills/github-classroom/config.json`

```json
{
  "org": "Alvin-Furman-CS-Classroom",
  "classroom_id": 293839,
  "classroom_name": "CSC-343-AI-Spring-2026"
}
```

---

## Troubleshooting

### "Error: Could not fetch assignment"

- Verify assignment ID (check URL in GitHub Classroom)
- Ensure `gh` is authenticated: `gh auth status`

### "No accepted assignments found"

- Students haven't accepted yet
- Check assignment invite link is correct

### "Failed to clone repo"

- Student repo may be empty
- Check network connectivity
- Verify you have org admin access

### Harness file is missing content

- Student hasn't committed any code yet
- Check their commit history in GitHub

---

## See Also

- [Quick Reference](./quick-reference.guide.md) - Command cheat sheet
- [GitHub Classroom Skill Docs](/.claude/skills/github-classroom/prompt.md) - Full API documentation
