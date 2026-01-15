---
status: draft
rubric: "./proposal.rubric.md"
outcomes:
  - The student will propose a coherent system of 5-6 modules unified by an overarching theme.
  - The student will describe the system and its components.
  - The student will describe how each module engages its AI topic.
  - The student will present results honestly—do not embellish or overclaim.
  - The student will be concise and well-organized.
---

# Project 1: Proposal

## Overview

You will design and build an AI System: a coherent software project comprising 5-6 modules, each engaging one or more topics from this course. Rather than completing pre-defined assignments, you will propose your own sequence of modules unified by an overarching theme.

An LLM agent will assist you in generating your proposal. This document provides the context the agent needs to produce a feasible, well-scoped proposal that aligns with course content and assessment criteria.

Use the link below to accept the assignment. Make sure you select your Furman email from the list it shows you.

<a href="https://classroom.github.com/a/ADw683l7" className="inline-block px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white no-underline font-semibold rounded-lg shadow-md transition-colors duration-200">Accept the Assignment</a>

## Project Structure

**Team composition:** Pairs required; groups of 3 acceptable.

**Development tools:** You may use GitHub Copilot, Claude Code, or any other LLM-assisted development tools.

**Repository structure:**

```
your-repo/
├── .claude/ # Claude skill for proposal review
├── AGENTS.md # instructions for your LLM agent
└── README.md # Your final proposal
```

**Language:** Python (primary), though other languages may be approved.

**GitHub requirements:**

- Use meaningful commit messages
- Document issues and their resolution
- All team members must have visible commit history demonstrating participation

## Proposal Requirements

### Timeline

- See the [Course Schedule](../../resources/course.schedule.md) for the project timeline.

### Proposal Contents

Proposals should be created in markdown (.md) format. Your proposal must include:

1. **System title and theme:** A unifying concept that connects all 7 modules into a coherent system.

2. **System overview:** A concise description (250 words maximum) of what the complete system will do and why the chosen theme is appropriate for exploring AI concepts.

3. **Module descriptions (5-6 total):** Each module description must be fewer than 250 words and include:

   - Module title
   - Topic(s) covered from the course list
   - Clear input specification
   - Clear output specification
   - How this module integrates with the larger system
   - Prerequisites (which prior modules or course content must be complete)

4. **Feasibility study:** A timeline showing that each module's prerequisites align with the course schedule. The agent will verify that you are not planning to implement content before it is taught.

5. **Coverage rationale:** Brief justification for your choice of 7 topics from the 13 available.

### Proposal Quality Expectations

Because LLM assistance is available, proposals are expected to be high quality. Verbose or bloated proposals will be penalized. Aim for clarity and precision, not volume.

The proposal will be graded using the [Proposal Rubric](./proposal.rubric.md).

## Module Requirements

Each module must demonstrate:

1. **Functionality:** The module works as specified.

2. **Code elegance:** Clean, readable, well-structured code. See the [Code Elegance Rubric](../../rubrics/code-elegance.rubric.md).

3. **I/O clarity:** Inputs and outputs must be clearly defined and easily assessable. For machine learning modules, this includes evaluation metrics with clear reporting.

## GitHub Practices

Your repository should demonstrate professional development practices:

- **Commit messages:** Descriptive, explaining what changed and why

## Final Deliverables

Your full proposal should be delivered in the `README.md` file. Creating other support files is fine, but the proposal itself must be in `README.md`.

## Automated Review (Claude skill)

Tell your agent to `use the proposal-review claude skill` to review your proposal. Even if you are not using Claude Code your agent should know what to do.

## Constraints for LLM Proposal Generation

When using an LLM agent to generate your proposal, ensure the agent respects these constraints:

1. **Course synchronization:** No module may require content not yet covered by its due date.
2. **Scope:** Each module should be completable by a pair of students in the time between due dates.
3. **Integration:** Modules must build toward a coherent system, not be disconnected exercises.
4. **Topic coverage:** 5-6 modules covering topics from the course list. Topics may be combined; not all topics must be covered.
5. **Concision:** Module descriptions under 250 words. No filler or unnecessary elaboration.
6. **Testability:** Each module must have clearly defined inputs and outputs amenable to unit and integration testing.
7. **Feasibility verification:** The agent must produce a feasibility study confirming schedule alignment.

## Getting Started

[>button: Accept the assignment](https://classroom.github.com/a/ADw683l7)
