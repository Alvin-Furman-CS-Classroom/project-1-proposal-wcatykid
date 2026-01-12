# Quick Reference: GitHub Classroom Commands

All commands run from the repo root.

---

## Classroom & Assignment Info

```bash
# List all classrooms
python3 .claude/skills/github-classroom/github_classroom.py classrooms

# List assignments (uses config.json classroom_id)
python3 .claude/skills/github-classroom/github_classroom.py assignments

# Get assignment details
python3 .claude/skills/github-classroom/github_classroom.py assignment <assignment_id>

# List student repos for an assignment
python3 .claude/skills/github-classroom/github_classroom.py accepted <assignment_id>

# Get grades/autograding results
python3 .claude/skills/github-classroom/github_classroom.py grades <assignment_id>
```

---

## Creating Assignments

```bash
# 1. Scaffold template from project file
python3 .claude/skills/github-classroom/github_classroom.py create-template \
    paths/projects/project-N/name.project.md \
    /tmp/template-name

# 2. Push template to GitHub org
python3 .claude/skills/github-classroom/github_classroom.py push-template \
    /tmp/template-name \
    csc343-assignment-name

# 3. Create assignment in GitHub Classroom UI...

# 4. Sync assignment ID back to project file
python3 .claude/skills/github-classroom/github_classroom.py sync-assignment \
    <assignment_id> \
    paths/projects/project-N/name.project.md
```

---

## Feedback Harness

```bash
# List students for an assignment (without creating snapshots)
python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id>

# Create snapshots for all students
python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id> --all

# Create snapshot for one student
python3 .claude/skills/github-classroom/feedback_harness.py snapshot <assignment_id> --student <login>

# List existing snapshots
python3 .claude/skills/github-classroom/feedback_harness.py list-snapshots <assignment_id>

# Post feedback as GitHub issue
python3 .claude/skills/github-classroom/feedback_harness.py create-issue \
    <assignment_id> \
    <student_login> \
    path/to/feedback.md
```

---

## AI-Assisted Evaluation

```bash
# Generate draft feedback for one student (requires ANTHROPIC_API_KEY)
python3 .claude/skills/github-classroom/feedback_harness.py evaluate \
    admin/harnesses/assignments/<slug>/<student>/latest.harness.md \
    --rubric paths/projects/project-1-proposal/proposal.rubric.md

# Generate draft feedback for ALL students
python3 .claude/skills/github-classroom/feedback_harness.py batch-evaluate \
    <assignment_id> \
    --rubric paths/projects/project-1-proposal/proposal.rubric.md
```

Draft feedback is saved alongside harness files as `draft-feedback-*.md`.
Review and edit before posting with `create-issue`.

---

## Where Things Live

| What | Where |
|------|-------|
| Config | `.claude/skills/github-classroom/config.json` |
| Harness files | `admin/harnesses/assignments/<slug>/<student>/` |
| Proposal rubric | `paths/projects/project-1-proposal/proposal.rubric.md` |
| Module rubric | `admin/materials/module_rubric.md` |
| Code elegance rubric | `admin/materials/code_elegance_rubric.md` |

---

## Finding Assignment IDs

1. Go to [GitHub Classroom](https://classroom.github.com/classrooms/241321390-alvin-furman-cs-classroom-csc-343-ai-spring-2026)
2. Click on an assignment
3. ID is in the URL: `classroom.github.com/classrooms/.../assignments/<ID>`

Or use the API:
```bash
python3 .claude/skills/github-classroom/github_classroom.py assignments | grep '"id"'
```

---

## Typical Feedback Session

### Manual Review
```bash
# 1. Snapshot all students
python3 .claude/skills/github-classroom/feedback_harness.py snapshot 12345 --all

# 2. Review harness files in admin/harnesses/assignments/...

# 3. Write feedback.md for each student

# 4. Post feedback
python3 .claude/skills/github-classroom/feedback_harness.py create-issue 12345 studentname feedback.md
```

### AI-Assisted Review
```bash
# 1. Snapshot all students
python3 .claude/skills/github-classroom/feedback_harness.py snapshot 12345 --all

# 2. Generate draft feedback for all (requires ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=sk-...
python3 .claude/skills/github-classroom/feedback_harness.py batch-evaluate 12345 \
    --rubric paths/projects/project-1-proposal/proposal.rubric.md

# 3. Review/edit draft-feedback-*.md files in admin/harnesses/assignments/...

# 4. Post approved feedback
python3 .claude/skills/github-classroom/feedback_harness.py create-issue 12345 studentname \
    admin/harnesses/assignments/slug/studentname/draft-feedback-2026-01-20.md
```
