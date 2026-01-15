---
status: draft
rubric: "./proposal.rubric.md"
outcomes:
  - The student will propose a coherent system of 7 modules unified by an overarching theme.
  - The student will describe the system and its components.
  - The student will describe how each module engages its AI topic.
  - The student will present results honestly—do not embellish or overclaim.
  - The student will be concise and well-organized.
---

# Project 1: Proposal (draft)

## Overview

You will design and build an AI System: a coherent software project comprising 7 modules, each engaging one or more topics from this course. Rather than completing pre-defined assignments, you will propose your own sequence of modules unified by an overarching theme.

An LLM agent will assist you in generating your proposal. This document provides the context the agent needs to produce a feasible, well-scoped proposal that aligns with course content and assessment criteria.

Use the link below to accept the assignment. Make sure you select your Furman email from the list it shows you.

<a href="https://classroom.github.com/a/ADw683l7" className="inline-block px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white no-underline font-semibold rounded-lg shadow-md transition-colors duration-200">Accept the Assignment</a>

## Project Structure

**Team composition:** Pairs required; groups of 3 acceptable.

**Development tools:** You may use GitHub Copilot, Claude Code, or any other LLM-assisted development tools.

**Repository structure:**

```
your-repo/
├── src/
├── unit_tests/
├── integration_tests/
└── README.md
```

**Language:** Python (primary), though other languages may be approved.

**GitHub requirements:**

- Use meaningful commit messages
- Use [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) for merging features
- Document issues and their resolution
- All team members must have visible commit history demonstrating participation

## Proposal Requirements

### Timeline

- **Draft:** Tuesday Jan 20th by 2:30pm
- **Feedback:** Thursday Jan 22nd by 5:00pm
- **Final:** Monday Jan 26th by 2:30pm

### Proposal Contents

Proposals should be generated in markdown (.md) format. Your proposal must include:

1. **System title and theme:** A unifying concept that connects all 7 modules into a coherent system.

2. **System overview:** A concise description (250 words maximum) of what the complete system will do and why the chosen theme is appropriate for exploring AI concepts.

3. **Module descriptions (7 total):** Each module description must be fewer than 250 words and include:

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

The proposal will be graded using the Proposal Rubric.

## Module Requirements

Each module must demonstrate:

1. **Functionality:** The module works as specified.

2. **Code elegance:** Clean, readable, well-structured code. See the Code Elegance Rubric.

3. **Testing:**

   - Unit tests in `unit_tests/`
   - Integration tests in `integration_tests/`
   - Tests should demonstrate correctness

4. **I/O clarity:** Inputs and outputs must be clearly defined and easily assessable. For machine learning modules, this includes evaluation metrics with clear reporting.

5. **Documentation:** Code documented according to standard Python practices (docstrings, type hints, inline comments where necessary).

6. **Topic engagement:** The module must genuinely engage with the AI concept, not merely reference it superficially.

## GitHub Practices

Your repository should demonstrate professional development practices:

- **Commit messages:** Descriptive, explaining what changed and why
- **Pull requests:** Used for merging features; include brief descriptions
- **Issues:** Track bugs, features, and tasks
- **Merge conflicts:** Resolve thoughtfully; do not simply accept all changes
- **Commit history:** All team members must contribute visibly

## Final Deliverables

During the final exam period, you will submit:

1. **Completed system:** All 7 modules functional and integrated
2. **Live demonstration:** Present your system with a working demo
3. **Paper:** Technical writeup prepared in LaTeX using Overleaf. The paper should:
   - Describe the system and its components
   - Explain how each module engages its AI topic
   - Present results honestly—do not embellish or overclaim
   - Be concise and well-organized

You may use LLM assistance for the paper and Latex, but you are responsible for accuracy and honest reporting of results.

## Assessment Overview

| Component                                  | Weight |
| ------------------------------------------ | ------ |
| Proposal                                   | 10%    |
| Modules (7 total, assessed at checkpoints) | 40%    |
| GitHub practices and participation         | 10%    |
| Presentation and demo                      | 20%    |
| Paper                                      | 20%    |

Modules are assessed using the Module Rubric. Code quality is assessed using the Code Elegance Rubric. Proposals are assessed using the Proposal Rubric.

## Constraints for LLM Proposal Generation

When using an LLM agent to generate your proposal, ensure the agent respects these constraints:

1. **Course synchronization:** No module may require content not yet covered by its due date.
2. **Scope:** Each module should be completable by a pair of students in the time between due dates.
3. **Integration:** Modules must build toward a coherent system, not be disconnected exercises.
4. **Topic coverage:** Exactly 7 modules covering topics from the course list. Topics may be combined; not all 13 topics must be covered.
5. **Concision:** Module descriptions under 250 words. No filler or unnecessary elaboration.
6. **Testability:** Each module must have clearly defined inputs and outputs amenable to unit and integration testing.
7. **Feasibility verification:** The agent must produce a feasibility study confirming schedule alignment.

## Getting Started

<!-- TODO: revise this to use Github Classroom -->

1. Fork the provided repository to your team's GitHub account.
2. Add the instructor as an owner.
3. Review this document and the rubrics.
4. Use the LLM agent (via VS Code) with this document as context to generate your proposal draft.
5. Review and refine the generated proposal—you are responsible for its quality.
6. Submit by Monday of Week 2.
7. Incorporate feedback and submit final proposal by Thursday of Week 2.
