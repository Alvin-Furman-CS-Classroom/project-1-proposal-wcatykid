# Code Elegance Review

Review Python code against the CSC-343 Code Elegance Rubric, providing detailed feedback and scores across 8 quality criteria.

## When to Use

Use this skill when:
- A student submits code for feedback
- Reviewing code quality before a module submission
- Providing constructive feedback on Python code style and structure

## Rubric Reference

The skill evaluates code against the rubric at `paths/code-elegance.rubric.md`. The 8 criteria are:

1. **Naming Conventions** - Are names clear, consistent, and PEP 8 compliant?
2. **Function and Method Design** - Are functions focused with single responsibilities?
3. **Abstraction and Modularity** - Is abstraction well-judged (not under/over-engineered)?
4. **Style Consistency** - Is formatting uniform and PEP 8 compliant?
5. **Code Hygiene** - Is code free of dead code, duplication, magic numbers?
6. **Control Flow Clarity** - Is control flow readable with minimal nesting?
7. **Pythonic Idioms** - Does code leverage Python idioms effectively?
8. **Error Handling** - Are errors handled appropriately and informatively?

Each criterion is scored 0-4:
- **4**: Exceeds expectations (professional quality)
- **3**: Meets expectations (solid with minor issues)
- **2**: Partially meets expectations (functional but notable weaknesses)
- **1**: Below expectations (significant problems)
- **0**: Missing or fundamentally inadequate

## Process

### Step 1: Identify code to review

Accept either:
- A single file path (e.g., `src/module1/solver.py`)
- A directory path to review all Python files
- A GitHub PR URL or repo path

### Step 2: Read and analyze the code

For each Python file:
1. Read the full file content
2. Analyze against each of the 8 rubric criteria
3. Note specific examples (line numbers) for feedback

### Step 3: Generate feedback report

Produce a structured report with:
- Overall score and summary
- Per-criterion scores with specific feedback
- Concrete suggestions for improvement
- Highlighted strengths

## Output Format

```markdown
# Code Review: [filename or project name]

## Summary

**Overall Score: X.X / 4.0** (maps to Module Rubric score: Y)

[2-3 sentence summary of overall code quality]

## Scores by Criterion

| Criterion | Score | Notes |
|-----------|-------|-------|
| 1. Naming Conventions | X/4 | [brief note] |
| 2. Function Design | X/4 | [brief note] |
| 3. Abstraction & Modularity | X/4 | [brief note] |
| 4. Style Consistency | X/4 | [brief note] |
| 5. Code Hygiene | X/4 | [brief note] |
| 6. Control Flow | X/4 | [brief note] |
| 7. Pythonic Idioms | X/4 | [brief note] |
| 8. Error Handling | X/4 | [brief note] |

## Detailed Feedback

### Strengths
- [Specific positive observations with examples]

### Areas for Improvement

#### [Criterion Name] (Score: X/4)
**Issue:** [Description of the problem]
**Location:** `filename.py:line_number`
**Example:**
```python
# Current code
problematic_code_here()
```
**Suggestion:**
```python
# Improved version
better_code_here()
```

[Repeat for each significant issue]

### Quick Wins
- [Easy fixes that would improve the score]

## Next Steps
1. [Prioritized action item]
2. [Second priority]
3. [Third priority]
```

## Feedback Guidelines

### Be Constructive
- Lead with strengths before weaknesses
- Frame issues as opportunities for improvement
- Provide specific, actionable suggestions

### Be Specific
- Reference exact line numbers
- Show before/after code examples
- Explain *why* something is an issue, not just *what*

### Be Proportional
- Focus on significant issues, not nitpicks
- Prioritize feedback by impact
- Don't overwhelm with too many suggestions

### Be Educational
- Connect feedback to rubric criteria
- Explain the reasoning behind best practices
- Link to resources when helpful

## Example Invocations

- "Review the code in src/module1/"
- "Give me feedback on solver.py using the elegance rubric"
- "Check code quality for my propositional logic module"
- "Review this PR for code elegance"
