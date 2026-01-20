# Module Review Rubric

This rubric assesses modules at graded checkpoints through two distinct reviews plus project-wide criteria.

---

## Participation Requirement (Mandatory)

**This requirement must be satisfied for a student to receive any credit for the checkpoint.**

All team members must demonstrate meaningful, substantive participation as evidenced by commit history. This is not merely about having commits—each student must be a substantial contributor to the project's core work.

### Automatic Zero Conditions

A student will receive **0 points for the entire checkpoint** if any of the following apply:

1. **Non-participation**: The student shows little to no evidence of meaningful contribution. Commits that are trivial, cosmetic, or artificially created to simulate participation do not satisfy this requirement.

2. **Relegated to menial tasks**: The student's contributions consist only of minor tasks (e.g., formatting, comments, renaming files) while other team members complete all substantive work. Every team member must engage with core functionality, testing, or design.

3. **Monopolizing work**: A student who completes all or nearly all of the work—thereby relegating teammates to menial tasks—will receive 0 points for failure to collaborate. Working effectively with others is a course requirement, not optional.

Commit history, pull request participation, and code authorship will be examined to assess this requirement. If concerns arise, the instructor may request additional evidence or conduct individual interviews.

---

## Part 1: Source Code Review (src/)

**Total: 27 points**

### 1.1 Functionality (8 points)

Does the module work as specified?

| Points | Description |
|--------|-------------|
| 8 | All features work correctly. Handles edge cases gracefully. No crashes or unexpected behavior. |
| 6 | Core features work correctly. Minor edge cases may be unhandled. Rare minor bugs. |
| 4 | Main functionality works but with notable bugs or missing features. |
| 2 | Partially functional. Major features broken or incomplete. |
| 0 | Non-functional or not submitted. |

### 1.2 Code Elegance and Quality (7 points)

Is the code clean, readable, and well-structured?

| Points | Description |
|--------|-------------|
| 7 | Exemplary code quality. Clear structure, excellent naming, appropriate abstraction. |
| 5 | Good code quality. Readable and organized with minor issues. |
| 3 | Acceptable code quality. Functional but messy, inconsistent, or poorly organized. |
| 1 | Poor code quality. Difficult to read, understand, or maintain. |
| 0 | Unacceptable. Incomprehensible or no meaningful code submitted. |

### 1.3 Documentation (4 points)

Is the source code documented according to standard Python practices?

| Points | Description |
|--------|-------------|
| 4 | Excellent documentation. All public functions have docstrings with parameter and return descriptions. Type hints used consistently. Complex logic has inline comments. |
| 3 | Good documentation. Most functions documented. Type hints present. Minor gaps. |
| 2 | Basic documentation. Some docstrings present but inconsistent or incomplete. |
| 1 | Minimal documentation. Little to no docstrings. Code is difficult to understand without reading implementation. |
| 0 | No documentation. |

### 1.4 I/O Clarity (3 points)

Are inputs and outputs clearly defined and easily assessable?

| Points | Description |
|--------|-------------|
| 3 | Inputs and outputs are crystal clear. Easy to verify correctness. For ML modules, metrics are well-reported and interpretable. |
| 2 | Inputs and outputs are clear with minor ambiguity. Assessment is straightforward. |
| 1 | Inputs and outputs defined but require effort to interpret or assess. |
| 0 | No clear I/O specification. Cannot assess functionality. |

### 1.5 Topic Engagement (5 points)

Does the module genuinely engage with the AI concept(s) it claims to cover?

| Points | Description |
|--------|-------------|
| 5 | Deep engagement with the topic. Demonstrates clear understanding. Implementation reflects core concepts accurately and meaningfully. |
| 4 | Solid engagement. Topic is addressed appropriately with minor superficiality. |
| 2 | Surface-level engagement. Topic is referenced but implementation does not demonstrate deep understanding. |
| 1 | Weak engagement. Topic is named but barely addressed in implementation. |
| 0 | No meaningful engagement with the stated topic. |

---

## Part 2: Testing Review (unit_tests/ and integration_tests/)

**Total: 15 points**

### 2.1 Test Coverage and Design (6 points)

Are unit tests and integration tests comprehensive and well-designed?

| Points | Description |
|--------|-------------|
| 6 | Comprehensive coverage. Tests cover core functionality, edge cases, and error conditions. Clear distinction between unit and integration tests. |
| 5 | Good coverage. Most important functionality tested. Minor gaps in edge cases or error handling. |
| 3 | Basic coverage. Some tests present but incomplete. Key functionality may be untested. |
| 1 | Minimal coverage. Few tests, poorly targeted, or significant gaps. |
| 0 | No tests or tests completely non-functional. |

### 2.2 Test Quality and Correctness (5 points)

Are tests meaningful, correctly implemented, and passing?

| Points | Description |
|--------|-------------|
| 5 | All tests pass. Tests are meaningful (not trivial assertions). Tests verify actual behavior, not implementation details. Test isolation is maintained. |
| 4 | Tests pass with minor issues. Most tests are meaningful. Occasional testing of implementation rather than behavior. |
| 2 | Some test failures or flaky tests. Tests may be superficial or overly coupled to implementation. |
| 1 | Many failures. Tests are trivial, redundant, or do not test what they claim. |
| 0 | Tests do not run or provide no value. |

### 2.3 Test Documentation and Organization (4 points)

Are tests organized, named clearly, and documented?

| Points | Description |
|--------|-------------|
| 4 | Excellent organization. Tests grouped logically. Clear, descriptive test names. Docstrings explain test purpose where needed. Test fixtures documented. |
| 3 | Good organization. Most tests named clearly. Structure is logical with minor issues. |
| 2 | Basic organization. Test names vague or inconsistent. Structure unclear. |
| 1 | Poor organization. Tests scattered or poorly named. |
| 0 | No organization. Tests are impossible to understand. |

---

## Part 3: GitHub Practices

**Total: 8 points**

### 3.1 Commit Quality and History (4 points)

Does the commit history reflect professional development practices?

| Points | Description |
|--------|-------------|
| 4 | Meaningful commit messages that explain *what* and *why*. Commits are appropriately sized (not too large, not trivially small). Logical progression of work is evident. |
| 3 | Good commit messages. Most commits are meaningful. Minor lapses in clarity or sizing. |
| 2 | Basic commits. Messages often vague ("fixed stuff", "updates"). Commits may be too large or inconsistent. |
| 1 | Poor commit messages. History is difficult to follow. |
| 0 | No meaningful commit history. |

### 3.2 Collaboration Practices (4 points)

Does the team use GitHub's collaboration features effectively?

| Points | Description |
|--------|-------------|
| 4 | Appropriate use of branches and pull requests. Code reviews evident. Issues or project boards used to track work. Merge conflicts resolved thoughtfully. |
| 3 | Pull requests used for most work. Some code review activity. Minor lapses in process. |
| 2 | PRs or branches underutilized. Little evidence of code review. Work merged directly to main. |
| 1 | No meaningful use of branches, PRs, or issues. Repository is disorganized. |
| 0 | No collaboration practices evident. |

---

## Scoring Summary

| Section | Points | Percentage |
|---------|--------|------------|
| **Participation Requirement** | Gate | Must pass |
| **Part 1: Source Code Review** | 27 | 54% |
| **Part 2: Testing Review** | 15 | 30% |
| **Part 3: GitHub Practices** | 8 | 16% |
| **Total** | **50** | 100% |

---

## Review Process

1. **Participation Check**: Verify that all team members meet the participation requirement. Any student who fails this check receives 0 for the checkpoint before other criteria are assessed.

2. **Source Code Review**: Evaluate all files in `src/` for functionality, quality, documentation, I/O clarity, and topic engagement.

3. **Testing Review**: Evaluate all files in `unit_tests/` and `integration_tests/` for coverage, quality, and organization.

4. **GitHub Practices Review**: Assess commit quality and collaboration practices across the entire repository.