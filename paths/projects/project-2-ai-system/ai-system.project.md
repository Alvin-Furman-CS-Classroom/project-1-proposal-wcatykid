---
status: draft
rubric: "./ai-system.rubric.md"
outcomes:
  - The student will build an AI system of 5-6 modules unified by the approved proposal.
  - The student will pass each checkpoint using agent-guided reviews and instructor feedback.
---

[@github_classroom_link]: https://classroom.github.com/a/ADw683l7]

# Project 2: AI System

## Overview

You will implement the 5-6 module AI system you proposed in Project 1. Each module must be functional, testable, and integrated into the larger system. You will work in teams and use an LLM agent to plan, review, and improve your work, but you remain responsible for design decisions and code quality.

[>button: Accept the assignment][@github_classroom_link]

## Project Structure

**Team composition:** Pairs required; groups of 3 acceptable.

**Development tools:** You may use Cursor, GitHub Copilot, Claude Code, or other LLM-assisted tools. Cursor is recommended.

**Repository structure:**

```
your-repo/
├── .claude/skills/code-review/SKILL.md # rubric-based agent review
├── AGENTS.md                           # instructions for your LLM agent
└── README.md                           # system overview and checkpoints
```

**Language:** Python (primary), though other languages may be approved.

## Required Workflow (Agent Guided)

You are expected to use an AI agent to support planning and review, not to replace your own understanding. Before each module:

1. Write a short module spec in `README.md` (inputs, outputs, dependencies, tests).
2. Ask the agent to propose a plan in "Plan" mode.
3. Review and edit the plan. You must understand and approve the approach.
4. Implement and test the module.
5. Run a rubric review using the code-review skill.

## Checkpoints and Deliverables

Checkpoints follow the course schedule. See the [Course Schedule](../../resources/course.schedule.md) for dates.

At each checkpoint, your team must provide:

- Updated module spec and integration notes in `README.md`
- Working implementation for the module(s)
- Tests that validate core behavior and edge cases
- Evidence of usage (logs, screenshots, sample outputs)
- Short reflection on what changed since the previous checkpoint

## Quality Expectations

Your work will be graded with the [AI System Rubric](./ai-system.rubric.md). Each module must demonstrate:

1. **Functionality:** The module works as specified.
2. **Code elegance:** Clean, readable, well-structured code.
3. **Testing:** Unit/integration tests that pass and cover meaningful behavior.
4. **I/O clarity:** Inputs/outputs are clearly defined and easy to assess.
5. **Topic engagement:** The module meaningfully engages its AI topic.
6. **Documentation:** Clear README updates and docstrings.
7. **GitHub practices:** Meaningful commits, PRs, and issue tracking.

## Set Up Your Agent

Populate `AGENTS.md` with the information your agent needs:

- Your full project proposal (or a link to it)
- Links to APIs, libraries, and data sources
- Module plan and current milestone
- How the agent should help (planner, reviewer, debugger, etc.)

To invoke the review agent, ask it to **use the code-review skill** found at `.claude/skills/code-review/SKILL.md`. This review should happen before each checkpoint submission.

## Getting Started

[>button: Accept the assignment][@github_classroom_link]
