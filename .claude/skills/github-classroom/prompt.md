# GitHub Classroom Management Skill

This skill helps manage GitHub Classroom tasks for course administration.

## Available Commands

Use the Python script at `.claude/skills/github-classroom/github_classroom.py` to interact with the GitHub Classroom API.

### List Classrooms
```bash
python3 .claude/skills/github-classroom/github_classroom.py classrooms
```

### Get Classroom Details
```bash
python3 .claude/skills/github-classroom/github_classroom.py classroom <classroom_id>
```

### List Assignments for a Classroom
```bash
python3 .claude/skills/github-classroom/github_classroom.py assignments <classroom_id>
```

### Get Assignment Details
```bash
python3 .claude/skills/github-classroom/github_classroom.py assignment <assignment_id>
```

### List Accepted Assignments (Student Repos)
```bash
python3 .claude/skills/github-classroom/github_classroom.py accepted <assignment_id>
```

### Get Assignment Grades
```bash
python3 .claude/skills/github-classroom/github_classroom.py grades <assignment_id>
```

### Show Configuration
```bash
python3 .claude/skills/github-classroom/github_classroom.py config
```

Configuration is stored in `.claude/skills/github-classroom/config.json`:
- `org` - GitHub organization for template repos
- `classroom_id` - Default classroom ID (used when no ID provided to `assignments`)
- `classroom_name` - Human-readable classroom name

### Create Template Repository
Scaffold a template repository structure from a project file:
```bash
python3 .claude/skills/github-classroom/github_classroom.py create-template <project_file> <output_dir>
```

Example:
```bash
python3 .claude/skills/github-classroom/github_classroom.py create-template paths/proposal.project.md /tmp/proposal-template
```

This creates:
- `README.md` - Generated from project title
- `src/` - Source code directory with `__init__.py`
- `unit_tests/` - Unit tests with placeholder test
- `integration_tests/` - Integration tests directory
- `.gitignore` - Python-focused gitignore

### Push Template to GitHub
Push a scaffolded template to the configured GitHub org:
```bash
python3 .claude/skills/github-classroom/github_classroom.py push-template <template_dir> <repo_name>
```

Example:
```bash
python3 .claude/skills/github-classroom/github_classroom.py push-template /tmp/proposal-template csc343-proposal
```

This:
- Initializes git (if needed)
- Commits all files
- Creates the repo in the configured org as a template repository
- Pushes the code

### Sync Assignment Metadata
After creating an assignment in GitHub Classroom UI, sync the assignment metadata back to the project file:
```bash
python3 .claude/skills/github-classroom/github_classroom.py sync-assignment <assignment_id> <project_file>
```

This updates the project file's YAML frontmatter with:
- `assignment_id` - The GitHub Classroom assignment ID (for feedback harness)
- `assignment_url` - The invite link (for students to accept)
- `assignment_title` - The assignment title from GitHub Classroom
- `template_repo` - The template repository URL (if set)

## Prerequisites

- GitHub CLI (`gh`) must be installed and authenticated
- User must have admin access to the GitHub Classroom organization

## Common Workflows

### Review Student Submissions
1. List classrooms to find the classroom ID
2. List assignments to find the assignment ID
3. List accepted assignments to see all student repos
4. Use `gh repo clone` to clone specific student repos for review

### Check Grades
1. Get assignment grades to see autograding results
2. Export grades for gradebook integration

### Sync Template Repository (Recommended)

For template repos that already exist in the codebase (like `paths/projects/*/project-*-repository/`), use `sync-template` to push them to GitHub:

```bash
# Sync a single template repo (creates if new, updates if exists)
python3 .claude/skills/github-classroom/github_classroom.py sync-template \
    paths/projects/project-0-setup/project-0-setup-repository \
    csc343-project-0-setup

# Sync all templates defined in config.json
python3 .claude/skills/github-classroom/github_classroom.py sync-all-templates
```

**Full workflow:**
```bash
# 1. Sync template repo to GitHub
python3 .claude/skills/github-classroom/github_classroom.py sync-template \
    paths/projects/project-0-setup/project-0-setup-repository \
    csc343-project-0-setup

# 2. Go to GitHub Classroom UI and create/update assignment
#    Use the template repo URL printed by the command

# 3. Sync assignment metadata back to project file
python3 .claude/skills/github-classroom/github_classroom.py sync-assignment \
    <assignment_id> \
    paths/projects/project-0-setup/setup.project.md
```

**Note:** GitHub Classroom API is read-only, so assignment creation/updates must be done in the web UI.

### Create Assignment from Project File (Alternative)

If you need to scaffold a new template from scratch (rather than syncing an existing directory):

1. Run `create-template` to scaffold a template repo from your project file
2. Run `push-template` to push to the configured GitHub org
3. Go to GitHub Classroom web UI and create a new assignment using the template repo
4. Run `sync-assignment` with the new assignment ID to update your project frontmatter
5. The project file now has `assignment_url` for students and `assignment_id` for the feedback harness

Example workflow:
```bash
# 1. Scaffold template
python3 .claude/skills/github-classroom/github_classroom.py create-template paths/proposal.project.md /tmp/proposal-template

# 2. Push to GitHub org
python3 .claude/skills/github-classroom/github_classroom.py push-template /tmp/proposal-template csc343-proposal

# 3. Create assignment in GitHub Classroom UI...

# 4. Sync assignment metadata back to project file
python3 .claude/skills/github-classroom/github_classroom.py sync-assignment <assignment_id> paths/proposal.project.md
```

## Feedback Harness Commands

Use `feedback_harness.py` to create snapshots of student work and deliver feedback.

### Create Snapshot for All Students
```bash
python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id> --all
```

### Create Snapshot for Specific Student
```bash
python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id> --student <login>
```

### List Students for an Assignment
```bash
python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id>
```
(Without --all or --student, lists available students)

### List Existing Snapshots
```bash
python3 .claude/skills/github-classroom/feedback_harness.py list-snapshots <assignment_id>
```

### Post Feedback as GitHub Issue
```bash
python3 .claude/skills/github-classroom/feedback_harness.py create-issue <assignment_id> <student_login> <feedback_file>
```

## Feedback Workflow

1. **Create snapshot**: Generate harness file with student's code and commit history
2. **Review harness**: Evaluate against rubrics (Module Rubric, Code Elegance Rubric)
3. **Write feedback**: Create feedback markdown file
4. **Deliver feedback**: Post as GitHub issue to student's repo

### Harness File Location

Harness files are stored at:
```
admin/harnesses/assignments/{assignment-slug}/{student-login}/{date}.harness.md
```

Each student folder also has a `latest.harness.md` symlink to the most recent snapshot.

### Example Evaluation Prompt

When evaluating a harness file with Claude:

```
Please evaluate this student submission against the Module Rubric
(admin/materials/module_rubric.md) and Code Elegance Rubric
(admin/materials/code_elegance_rubric.md).

Provide:
1. Scores for each rubric criterion with justification
2. Specific code examples supporting your assessment
3. Constructive feedback for improvement
4. Overall summary and grade
```

## Notes

- All API endpoints require administrator access
- Pagination is handled automatically (fetches all results)
- Output is JSON formatted for easy parsing
