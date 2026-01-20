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

**Team composition:** Assigned groups of 2-3 by Dr. Alvin

**Development tools:** You may use Cursor, GitHub Copilot, Claude Code, or other LLM-assisted tools. Cursor is recommended.

**Repository structure:**

```
your-repo/
├── ./src/                              # main system source code 
├── ./unit_tests/                       # unit tests that parallel the structure of the .src/ directory sttructure
├── ./integration_tests/                # Integration tests; this should be easily navigable based on directory and file names
|                                       # Use a new folder for each new module 
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
4. Implement the module in a .src/ folder.
5. Unit test the module placing unit tests in a .unit_tests/ directory that will be a parallel structure to the main .src/ folder.
6. With each module beyond the first, perform integration tests linking all implemented modules. Use a new subfolder for each module.
7. Run a rubric review using the code-review skill.

## Checkpoints and Deliverables

Checkpoints follow the course schedule. See the [Course Schedule](../../resources/course.schedule.md) for dates.

At each checkpoint, your team must provide:

- Updated module spec and integration notes in `README.md`
- Working implementation for the module(s)
- Tests that validate core behavior and edge cases
- Integration tests that demonstrate proper interactivity among modules
- Evidence of usage (logs, screenshots, sample outputs)
- Short reflection on what changed since the previous checkpoint

## Quality Expectations

Your work will be graded with the [AI System Rubric](./ai-system.rubric.md).

**Participation Requirement:** All team members must demonstrate meaningful, substantive contribution. Students who do not participate—or who monopolize work and relegate teammates to menial tasks—will receive a 0 for the checkpoint.

Each module is assessed in two parts:

**Part 1: Source Code (src/)**
1. **Functionality:** The module works as specified.
2. **Code elegance:** Clean, readable, well-structured code.
3. **Documentation:** Clear docstrings with type hints.
4. **I/O clarity:** Inputs/outputs are clearly defined and easy to assess.
5. **Topic engagement:** The module meaningfully engages its AI topic.

**Part 2: Testing (unit_tests/ and integration_tests/)**
1. **Coverage & design:** Tests cover core functionality, edge cases, and error conditions.
2. **Quality & correctness:** Tests are meaningful, pass, and verify behavior (not implementation).
3. **Organization:** Tests are logically grouped with clear, descriptive names.

**GitHub Practices:** Meaningful commit messages, appropriate use of branches/PRs, and evidence of code review.

## Set Up Your Agent

Populate `AGENTS.md` with the information your agent needs:

- Your full project proposal (or a link to it)
- Links to APIs, libraries, and data sources
- Module plan and current milestone
- How the agent should help (planner, reviewer, debugger, etc.)

To invoke the review agent, ask it to **use the code-review skill** found at `.claude/skills/code-review/SKILL.md`. This review should happen before each checkpoint submission.

## Getting Started

[>button: Accept the assignment][@github_classroom_link]
