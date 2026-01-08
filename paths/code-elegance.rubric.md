# Code Elegance Rubric

This rubric provides detailed criteria for assessing code quality. It is referenced by the Module Rubric and applies to all Python code submitted.

## Point Scale

| Score | Description                                                                        |
| ----- | ---------------------------------------------------------------------------------- |
| 4     | **Exceeds expectations.** Professional quality. No meaningful improvements needed. |
| 3     | **Meets expectations.** Solid work with minor issues.                              |
| 2     | **Partially meets expectations.** Functional but with notable weaknesses.          |
| 1     | **Below expectations.** Significant problems, but evidence of effort.              |
| 0     | **Missing or fundamentally inadequate.**                                           |

## Criteria

### 1. Naming Conventions

Are variable, function, class, and module names clear and consistent?

| Score | Description                                                                                                                                                     |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4     | Names are descriptive, consistent, and follow PEP 8 conventions. Names reveal intent without needing comments. Abbreviations avoided or universally understood. |
| 3     | Names are generally clear and consistent. Minor issues with occasional vague names or slight inconsistency.                                                     |
| 2     | Names are functional but often unclear, inconsistent, or overly abbreviated. Reader must infer meaning.                                                         |
| 1     | Names are confusing, misleading, or highly inconsistent. Single-letter variables used inappropriately.                                                          |
| 0     | Naming is incomprehensible or no meaningful code submitted.                                                                                                     |

### 2. Function and Method Design

Are functions appropriately sized with clear, single responsibilities?

| Score | Description                                                                                                                                                                               |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4     | Functions are concise and focused. Each function does one thing well. Parameters are minimal and well-chosen. No function exceeds reasonable length (roughly 20–30 lines for most cases). |
| 3     | Functions are generally well-designed. Occasional functions are slightly too long or have mixed responsibilities.                                                                         |
| 2     | Functions are often too long or try to do too much. Some refactoring would improve clarity.                                                                                               |
| 1     | Functions are monolithic. Hundreds of lines in single functions. Responsibilities unclear.                                                                                                |
| 0     | No meaningful function structure. Code is one large block or incomprehensible.                                                                                                            |

### 3. Abstraction and Modularity

Is code appropriately abstracted—neither too shallow nor over-engineered?

| Score | Description                                                                                                                                                     |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4     | Abstraction is well-judged. Classes and modules have clear purposes. Code is reusable where appropriate. No unnecessary complexity or premature generalization. |
| 3     | Abstraction is reasonable. Minor instances of under- or over-abstraction.                                                                                       |
| 2     | Abstraction issues present. Code is either too monolithic or unnecessarily complex with excessive class hierarchies.                                            |
| 1     | Significant abstraction problems. Everything in one file or conversely, trivial operations spread across many classes.                                          |
| 0     | No meaningful structure.                                                                                                                                        |

### 4. Style Consistency

Is the code style consistent throughout?

| Score | Description                                                                                                                                    |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| 4     | Consistent style throughout. Follows PEP 8. Indentation, spacing, and formatting are uniform. Would pass a linter with no or minimal warnings. |
| 3     | Generally consistent with minor deviations. A few style inconsistencies.                                                                       |
| 2     | Inconsistent style. Mixed conventions, irregular spacing, inconsistent indentation.                                                            |
| 1     | Style is chaotic. No apparent conventions followed.                                                                                            |
| 0     | Unreadable due to formatting issues.                                                                                                           |

### 5. Code Hygiene

Is the code free of dead code, duplication, and magic numbers?

| Score | Description                                                                                                                                    |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| 4     | Clean codebase. No dead code, commented-out blocks, or duplication. Constants are named and defined in one place. No magic numbers or strings. |
| 3     | Mostly clean. Minor instances of duplication or a few magic numbers.                                                                           |
| 2     | Notable hygiene issues. Dead code present, copy-paste duplication, several magic numbers scattered throughout.                                 |
| 1     | Significant hygiene problems. Large blocks of dead code, extensive duplication, magic numbers everywhere.                                      |
| 0     | Codebase is cluttered and unmaintainable.                                                                                                      |

### 6. Control Flow Clarity

Is the control flow readable and easy to follow?

| Score | Description                                                                                                                                                                          |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 4     | Control flow is clear and logical. Nesting is minimal (generally ≤3 levels). Early returns used appropriately. Complex conditions are broken into well-named variables or functions. |
| 3     | Control flow is generally clear. Occasional deep nesting or complex conditionals.                                                                                                    |
| 2     | Control flow is difficult to follow. Deep nesting, convoluted conditionals, or unclear branching logic.                                                                              |
| 1     | Control flow is confusing. Spaghetti code, goto-like patterns, or incomprehensible branching.                                                                                        |
| 0     | Control flow cannot be understood.                                                                                                                                                   |

### 7. Pythonic Idioms

Does the code use Python idioms appropriately?

| Score | Description                                                                                                                                                                                                  |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 4     | Code leverages Python idioms effectively: list comprehensions, context managers, generators, unpacking, enumerate, zip, etc. Uses standard library appropriately. Avoids reinventing built-in functionality. |
| 3     | Generally Pythonic. Uses common idioms. Occasional missed opportunities.                                                                                                                                     |
| 2     | Code works but is not idiomatic. Writes explicit loops where comprehensions would be clearer. Ignores useful standard library functions.                                                                     |
| 1     | Code fights the language. Java-style or C-style patterns. Does not leverage Python's strengths.                                                                                                              |
| 0     | Code does not demonstrate knowledge of Python.                                                                                                                                                               |

### 8. Error Handling

Are errors handled appropriately and informatively?

| Score | Description                                                                                                                                                                                       |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4     | Errors are handled thoughtfully. Exceptions are specific, caught at appropriate levels, and provide useful messages. Fails gracefully where appropriate. Does not silence errors inappropriately. |
| 3     | Error handling is reasonable. Most errors handled. Occasional bare except or overly broad exception catching.                                                                                     |
| 2     | Error handling is inconsistent. Some errors caught, others ignored. Generic exceptions used.                                                                                                      |
| 1     | Error handling is poor. Errors silenced, crashes on common inputs, or no error handling at all.                                                                                                   |
| 0     | No error handling. Code crashes unpredictably.                                                                                                                                                    |

## Overall Code Elegance Score

Calculate the average across all 8 criteria. The overall score informs the "Code Elegance and Quality" criterion in the Module Rubric.

| Average | Module Rubric Score |
| ------- | ------------------- |
| 3.5–4.0 | 4                   |
| 2.5–3.4 | 3                   |
| 1.5–2.4 | 2                   |
| 0.5–1.4 | 1                   |
| 0.0–0.4 | 0                   |
