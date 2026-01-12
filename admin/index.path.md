# CSC-343 Admin Documentation

Instructor-facing documentation for course administration.

---

## Workflows

Step-by-step guides for common instructor tasks.

| Guide                                                     | Description                                                |
| --------------------------------------------------------- | ---------------------------------------------------------- |
| [Course Workflows](./workflows/course-workflows.guide.md) | Architecture overview, assignment setup, feedback delivery |
| [Quick Reference](./workflows/quick-reference.guide.md)   | Command cheat sheet for GitHub Classroom tools             |

---

## Claude Skills

Automation tools for course management.

| Skill                                                                  | Description                                     |
| ---------------------------------------------------------------------- | ----------------------------------------------- |
| [Claude Skills Overview](./claude-skills.guide.md)                     | Guide to available Claude skills                |
| [GitHub Classroom Skill](../.claude/skills/github-classroom/prompt.md) | Full API documentation for classroom management |

---

## Materials

Reference materials and rubrics (some duplicated in `paths/` for student access).

| Material                                                           | Description                       |
| ------------------------------------------------------------------ | --------------------------------- |
| [Proposal Rubric](./materials/proposal_rubric.md)                  | Rubric for Project 1 proposals    |
| [Module Rubric](./materials/module_rubric.md)                      | Rubric for AI System modules      |
| [Code Elegance Rubric](./materials/code_elegance_rubric.md)        | Code quality assessment criteria  |
| [AI System Student Doc](./materials/ai_system_student_document.md) | Student-facing AI System overview |

---

## Harnesses

Student submission snapshots are stored in `admin/harnesses/assignments/`.

```
harnesses/
└── assignments/
    └── <assignment-slug>/
        └── <student-login>/
            ├── <date>.harness.md      # Snapshot of student work
            ├── latest.harness.md      # Symlink to most recent
            └── draft-feedback-*.md    # AI-generated feedback drafts
```

Use `feedback_harness.py` commands to manage harnesses:

- `snapshot` - Create new snapshots
- `evaluate` - Generate AI feedback drafts
- `create-issue` - Post feedback to student repos

See [Quick Reference](./workflows/quick-reference.guide.md) for commands.

---

## External Links

- [GitHub Classroom](https://classroom.github.com/classrooms/241321390-alvin-furman-cs-classroom-csc-343-ai-spring-2026) - Assignment management
- [PathMX Player](https://csc-343.path.app) - Student content delivery
