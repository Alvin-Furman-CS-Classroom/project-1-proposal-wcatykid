# Logic Puzzle Generation and Analysis System

## System Overview

This system provides an end-to-end pipeline for generating, solving, and analyzing logic puzzles using artificial intelligence techniques. The system begins by generating generic logic puzzle structures with entities, attributes, and constraints based on specified difficulty levels. These puzzles are then converted into propositional logic knowledge bases, where constraints become logical formulas using standard connectives. The system solves puzzles through forward and backward chaining inference, producing both complete solutions and formal proofs of the reasoning process. Solutions are verified through dual methods: checking constraint satisfaction and logical entailment validation. The system analyzes puzzle difficulty using multiple complexity metrics (constraint count, search space size, inference step count, etc.) to provide comprehensive difficulty assessments. Finally, the system generates human-readable explanations that translate formal logical proofs into step-by-step narratives, making the AI reasoning process transparent and understandable.

Logic puzzles are an ideal theme for exploring AI concepts because they naturally embody core AI principles. The puzzle constraints map directly to propositional logic, enabling exploration of knowledge representation, inference methods, and entailment checking. Puzzle generation requires constraint satisfaction techniques to ensure valid, solvable puzzles. The solving process demonstrates forward/backward chaining inference in action, while verification showcases logical entailment and satisfiability checking. Difficulty analysis provides opportunities to examine algorithmic complexity and problem space analysis. The explanation generation bridges formal logical reasoning with human understanding, illustrating knowledge representation concepts. This theme offers a coherent progression through multiple AI topics while remaining accessible and testable, with clear input/output specifications that enable rigorous module integration and validation.

## Modules

### Module 1: Puzzle Generator

**Topics:** Constraint Satisfaction Problems (CSP)

**Input:** JSON object specifying puzzle parameters:
- `grid_size` (integer): Number of entities in the puzzle (e.g., 5)
- `difficulty` (string): Difficulty level - "easy", "medium", or "hard"

The system automatically determines the number of attributes and values per attribute based on the grid size and difficulty level.

**Output:** JSON object containing:
- `puzzle_id`: Unique identifier for the puzzle
- `entities`: Array of entity identifiers (e.g., ["E1", "E2", ..., "E5"])
- `attributes`: Object mapping attribute names to arrays of possible values
- `constraints`: Array of constraint objects, each containing entity/attribute references and relation information (abstract representation)
- `solution`: Hidden solution object mapping entities to their attribute assignments

The number of constraints is determined automatically based on the difficulty level to ensure solvability and appropriate challenge.

**Integration:** The generated puzzle structure (entities, attributes, constraints) is passed to Module 2 (Logic Representation) where constraints are converted into propositional logic formulas. The hidden solution is used later by Module 4 (Solution Verification).

**Prerequisites:** Course content on Constraint Satisfaction Problems, including constraint representation and satisfaction algorithms.

---

### Module 2: Logic Representation

**Topics:** Propositional Logic (knowledge bases, logical formulas, entailment)

**Input:** JSON object from Module 1 containing:
- `entities`: Array of entity identifiers (e.g., ["E1", "E2", ..., "E5"])
- `attributes`: Object mapping attribute names to arrays of possible values
- `constraints`: Array of constraint objects with entity/attribute references and relation information

Note: The `solution` field from Module 1 is excluded from this input since it is not needed for logic representation.

**Output:** Text format knowledge base containing structured logical formulas:
- **Facts**: Base propositions representing potential assignments, encoded as proposition symbols (e.g., `Has(E1, A1, V2)` becomes proposition `E1_A1_V2`)
- **Rules**: Logical formulas expressing the puzzle constraints, using standard logical connectives (∧, ∨, ¬, →, ↔)

The knowledge base is represented as text using structured logical formulas (e.g., `P ∧ Q → R`, `¬(A ∨ B)`, etc.) where each proposition symbol represents a potential entity-attribute-value assignment.

**Integration:** The knowledge base output is passed to Module 3 (Puzzle Solving), which performs inference on the logical formulas to find the solution. The propositional representation allows Module 3 to use inference methods such as resolution, forward chaining, or model checking.

**Prerequisites:** Module 1 (Puzzle Generator) must provide the puzzle structure. Course content on Propositional Logic, including logical formulas, knowledge bases, and propositional symbols.

---

### Module 3: Puzzle Solving

**Topics:** Propositional Logic (forward chaining, backward chaining, inference)

**Input:** Knowledge base in text format from Module 2, containing structured logical formulas (facts and rules expressed using logical connectives).

**Output:** Text format containing:
- **Solution**: Full assignment mapping each entity to its attribute values, represented as text (e.g., "E1: A1=V2, A2=V4, A3=V1; E2: A1=V1, ..." or propositional format listing all true propositions)
- **Proof**: Logical derivation showing how the solution was inferred from the knowledge base, using forward chaining or backward chaining inference steps

The proof demonstrates the sequence of inference steps that lead from the initial knowledge base to the complete solution.

**Integration:** The solution output is passed to Module 4 (Solution Verification) for validation against the puzzle constraints. The proof is used by Module 6 (Solution Explanation) to generate step-by-step reasoning explanations. If Module 5 (Difficulty Analysis) measures solution complexity, it may also use information about the number of inference steps required.

**Prerequisites:** Module 2 (Logic Representation) must provide the knowledge base. Course content on Propositional Logic inference methods, specifically forward chaining and backward chaining algorithms.

---

### Module 4: Solution Verification

**Topics:** Propositional Logic (logical entailment, satisfiability checking)

**Input:**
- Solution in text format from Module 3 (full assignment mapping entities to attribute values)
- Puzzle constraints from Module 1 (original constraint objects with entity/attribute references)
- Knowledge base in text format from Module 2 (structured logical formulas)
- Hidden solution from Module 1 (for reference comparison during verification)

**Output:** Structured text report containing:
- Overall validation result (VALID or INVALID)
- Per-constraint validation results: For each constraint from Module 1, indicates whether it is satisfied or violated by the solution
- Logical entailment check: Verification that the solution logically entails (or is entailed by) the knowledge base
- Summary of any constraint violations (if invalid)

The report provides detailed information about which specific constraints are satisfied and which are not, enabling identification of solution errors.

**Integration:** The validation report confirms whether Module 3's solution is correct. If valid, the solution can be used by Module 5 (Difficulty Analysis) for measuring puzzle properties. If invalid, the report can inform Module 6 (Solution Explanation) about what went wrong in the solving process. The hidden solution from Module 1 serves as a reference for correctness checking.

**Prerequisites:** Module 1 (Puzzle Generator), Module 2 (Logic Representation), and Module 3 (Puzzle Solving) must be completed. Course content on Propositional Logic entailment and satisfiability checking.

---

### Module 5: Difficulty Analysis

**Topics:** Complexity Analysis (algorithmic complexity, problem space analysis)

**Input:**
- Puzzle structure from Module 1 (entities, attributes, constraints)
- Knowledge base in text format from Module 2 (logical formulas)
- Solution and proof in text format from Module 3 (full assignment and inference steps)
- Validation report in structured text format from Module 4

**Output:** Detailed breakdown in structured text format containing multiple difficulty metrics:
- The system automatically determines which metrics are most relevant based on the puzzle characteristics
- Possible metrics include: number of constraints, constraint complexity, size of search space, number of inference steps required in the proof, branching factor, constraint density, logical formula complexity, etc.
- Each metric includes its value and an interpretation of its contribution to overall difficulty

The output provides a comprehensive analysis of puzzle difficulty from multiple computational and logical perspectives, allowing for nuanced difficulty assessment.

**Integration:** The difficulty analysis informs Module 6 (Solution Explanation) about the puzzle characteristics, which helps explain the overall solution strategy. The analysis also validates that the puzzle generation in Module 1 produces puzzles with the intended difficulty level. The metrics may be used for categorizing puzzles or providing difficulty ratings to users.

**Prerequisites:** Modules 1-4 must be completed to provide all necessary inputs. Course content on Complexity Analysis, including time and space complexity, problem space size, and algorithmic complexity measurement.

---

### Module 6: Solution Explanation

**Topics:** Knowledge Representation (explaining logical reasoning, knowledge structures)

**Input:**
- Solution and proof in text format from Module 3 (full assignment and inference steps)
- Knowledge base in text format from Module 2 (structured logical formulas)
- Puzzle constraints from Module 1 (original constraint objects)
- Difficulty metrics breakdown from Module 5 (multiple complexity measures)

**Output:** Structured text explanation with sections containing:
- **Overall Solution Strategy**: High-level description of the approach used to solve the puzzle, informed by the proof structure and difficulty metrics
- **Step-by-Step Reasoning**: Detailed explanation of each inference step from the proof, showing how logical reasoning led from the initial knowledge base to the solution
- Sections organized by major reasoning phases or constraint applications, with clear explanations of how each step builds on previous knowledge

The explanation translates the formal logical proof into human-readable narrative, showing how the puzzle constraints were logically applied to reach the solution.

**Integration:** The explanation helps users understand how the solution was derived, making the system's reasoning process transparent. It bridges the gap between the formal logical representation (Module 2) and the solved result (Module 3), demonstrating the solving process. The explanation can also be used for educational purposes or debugging when solutions are incorrect.

**Prerequisites:** Modules 1-5 must be completed to provide all necessary inputs. Course content on Knowledge Representation, including how to represent and explain logical reasoning processes and knowledge structures.

---

## Feasibility Study

| Module | Required Topic(s) | Topic Covered By | Checkpoint Due |
| ------ | ----------------- | ---------------- | -------------- |
| 1      | Constraint Satisfaction Problems (CSP) | Covered as part of Search topics (by ~Feb 9) | Wednesday, Feb 11 (Checkpoint 1) |
| 2      | Propositional Logic (knowledge bases, logical formulas) | Week 1-2 (by ~Jan 26) | Thursday, Feb 26 (Checkpoint 2) |
| 3      | Propositional Logic (forward chaining, backward chaining, inference) | Week 1-2 (by ~Jan 26) | Thursday, March 19 (Checkpoint 3) |
| 4      | Propositional Logic (logical entailment, satisfiability checking) | Week 1-2 (by ~Jan 26) | Thursday, April 2 (Checkpoint 4) |
| 5      | Complexity Analysis | Ongoing throughout course (general CS/AI concept) | Thursday, April 16 (Checkpoint 5) |
| 6      | Knowledge Representation | Covered as part of Propositional Logic and First-Order Logic (by ~Feb 23) | Thursday, April 23 (Final Demo) |

## Coverage Rationale

The selected topics naturally align with the logic puzzle theme, creating a coherent pipeline from generation through solving to analysis. **Propositional Logic** serves as the foundation for the system, directly representing puzzle constraints as logical formulas. This choice satisfies the required topic coverage while being essential to the theme: logic puzzles inherently involve logical relationships between entities and attributes, making propositional logic the most natural representation. The multiple Propositional Logic modules (Modules 2-4) demonstrate different aspects—knowledge representation, inference, and verification—showing the versatility of this topic within the theme.

**Constraint Satisfaction Problems (CSP)** fits naturally in puzzle generation, as generating valid, solvable puzzles requires ensuring constraint satisfiability. The CSP approach ensures generated puzzles are well-formed and have solutions. **Complexity Analysis** enables objective difficulty assessment by measuring computational properties like search space size and inference step count, providing metrics that complement subjective difficulty ratings. **Knowledge Representation** bridges formal logic and human understanding, allowing the system to generate explanations that make the AI reasoning process transparent.

**Trade-offs considered**: First-Order Logic was not chosen because propositional logic sufficiently captures the constraint relationships in logic puzzles without the added complexity of quantification. Search algorithms (A*, IDA*) were considered but ultimately not needed, as puzzle solving can be accomplished through logical inference rather than path-finding search. Game Theory topics (Minimax, MCTS) were not selected because logic puzzles are constraint-satisfaction problems rather than adversarial games. Reinforcement Learning was excluded as logic puzzles have deterministic solutions that don't benefit from learning from experience. The chosen topics create a focused, cohesive system where each module builds naturally on previous ones.
