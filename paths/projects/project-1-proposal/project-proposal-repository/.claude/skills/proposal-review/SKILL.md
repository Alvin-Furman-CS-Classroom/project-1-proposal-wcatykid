# Proposal Self-Review

Review your AI System proposal against the CSC-343 Proposal Rubric before instructor feedback. Get actionable insights on all 8 rubric criteria.

## When to Use

Use this skill when:

- You've completed a draft of your proposal
- You want to self-assess before the deadline
- You're looking for specific areas to improve
- You want to verify rubric alignment before submission

## Rubric Criteria

The skill evaluates proposals against 8 criteria (each scored 0-4):

1. **Coherence of Theme** - Does the theme unify all modules?
2. **Feasibility & Course Sync** - Is the timeline realistic? Do prerequisites align?
3. **Scope Appropriateness** - Is each module neither too ambitious nor trivial?
4. **Clarity & Concision** - Is writing clear and free of verbosity?
5. **I/O Specification Quality** - Are inputs/outputs concrete and testable?
6. **System Integration** - Is data flow between modules clear?
7. **Coverage Rationale** - Is topic selection justified?
8. **Module Description Quality** - Are all required elements present?

## Process

### Step 1: Locate the proposal

Read the `README.md` file in the repository root. This contains the student's proposal.

### Step 2: Evaluate each criterion

For each of the 8 rubric criteria:

1. Review the relevant sections of the proposal
2. Identify specific strengths and weaknesses
3. Assign a preliminary score (0-4)
4. Note concrete examples from the text

### Step 3: Check hard constraints

Verify these non-negotiable requirements:

- [ ] System overview ≤ 250 words
- [ ] Each module description ≤ 250 words
- [ ] 5-6 modules present
- [ ] Each module has: title, topics, I/O specs, integration, prerequisites
- [ ] Feasibility study included
- [ ] Coverage rationale provided
- [ ] No module requires content not yet taught at its checkpoint

### Step 4: Generate feedback report

Produce structured feedback following the output format below.

## Output Format

```markdown
# Proposal Self-Review

## Summary

**Estimated Score: X / 32** (8 criteria × 4 points)

[2-3 sentence summary of overall proposal quality and readiness]

## Scores by Criterion

| Criterion                | Score | Quick Note   |
| ------------------------ | ----- | ------------ |
| 1. Coherence of Theme    | X/4   | [brief note] |
| 2. Feasibility & Sync    | X/4   | [brief note] |
| 3. Scope Appropriateness | X/4   | [brief note] |
| 4. Clarity & Concision   | X/4   | [brief note] |
| 5. I/O Specification     | X/4   | [brief note] |
| 6. System Integration    | X/4   | [brief note] |
| 7. Coverage Rationale    | X/4   | [brief note] |
| 8. Module Descriptions   | X/4   | [brief note] |

## Constraint Checklist

- [ ] System overview ≤ 250 words (actual: N words)
- [ ] All module descriptions ≤ 250 words
- [ ] 5-6 modules present (actual: N)
- [ ] All modules have required elements
- [ ] Feasibility study present
- [ ] Coverage rationale present
- [ ] Timeline alignment verified

## Strengths

[Bulleted list of specific things done well, with quotes/examples]

## Areas for Improvement

### [Criterion Name] (Score: X/4)

**Issue:** [Specific problem identified]

**Location:** [Where in the proposal]

**Current:**

> [Quote from proposal showing the issue]

**Suggestion:** [Concrete recommendation for improvement]

[Repeat for each significant issue, prioritized by impact]

## Quick Wins

These small changes would improve your score:

1. [Easy fix with high impact]
2. [Another quick improvement]
3. [Third suggestion]

## Before Submitting

1. [ ] Address the issues above
2. [ ] Re-read for concision (cut filler words)
3. [ ] Verify word counts
4. [ ] Check I/O specs are testable
5. [ ] Confirm timeline alignment
```

## Feedback Guidelines

### Be Honest

- Don't inflate scores to be encouraging
- Point out real issues that will cost points
- Better to catch problems now than in grading

### Be Specific

- Quote exact text that needs work
- Explain _why_ something doesn't meet the rubric
- Provide concrete rewrites when helpful

### Be Actionable

- Prioritize feedback by impact
- Focus on fixable issues
- Distinguish between easy wins and larger restructuring

### Be Calibrated

- A score of 3 means "solid work with minor issues"
- A score of 4 is "professional quality"
- Most good student work lands at 3; 4s are exceptional

## Common Issues to Watch For

### Theme Problems

- Theme sounds forced or artificial
- Some modules don't clearly belong
- Theme is too narrow to accommodate all topics

### Feasibility Problems

- Module scheduled before content is taught
- Unrealistic scope for the time available
- Dependencies not accounted for

### Clarity Problems

- Verbose descriptions with filler
- Vague language ("processes the data")
- Passive voice obscuring who does what

### I/O Problems

- Inputs not concrete ("user provides information")
- Outputs not testable ("produces useful results")
- Missing format specifications

### Integration Problems

- Modules described in isolation
- Data flow between modules unclear
- No system architecture evident

## Example Invocations

- "Review my proposal"
- "How does my proposal score against the rubric?"
- "What should I fix before submitting?"
- "Check if my timeline is feasible"
- "Is my I/O specification clear enough?"
