# Musical Theater Rehearsal Scheduler

## System Overview

This system generates optimal rehearsal schedules for musical theater productions over a four-week period, accommodating 15-20 cast members with availability varying each week. The system handles the complex structure of musical rehearsals: individual scene and song rehearsals, act runs, full show runs, and tech week constraints.

The system takes natural language input describing cast availability, scenes, songs, and rehearsal requirements, which is converted to structured data (CSV/JSON format), then validated and normalized. It encodes scheduling constraints using propositional logic (CNF), then uses A* search to find valid schedules that satisfy all requirements. The schedule is optimized to minimize "waiting time" periods when actors must be present but are not actively rehearsing. Advanced search techniques refine the solution, and first-order logic validates the final schedule and diagnoses any impossible constraints, such as two actors never being available at the same time.

This theme naturally integrates multiple AI techniques: propositional logic for constraint representation, search algorithms for schedule generation, optimization for preference handling, NLP for input parsing, and first-order logic for validation. The problem demonstrates real-world AI application where logical reasoning, search, and optimization work together to solve a complex scheduling problem with both hard constraints (availability, scene requirements) and soft preferences (minimizing idle time).

## Modules

### Module 1: Input Parser & Data Validator

**Topics:** None (data processing and validation)

**Input:** CSV files (`cast.csv`, `scenes.csv`, `songs.csv`) and JSON file (`rehearsal_config.json`). Cast file contains actor names, roles, and weekly availability strings (e.g., "Mon 7-9pm, Wed 6-8pm"). Scene and song files specify required actors and act membership. Rehearsal config file defines minimum rehearsal counts (at least one scene, at least one song, at least one sing-through, at least one act run for each act, at least one full run) and tech week specification (week 4, fixed rehearsals 5pm-10pm each day).

**Output:** Validated, normalized structured data (JSON): cast dictionary with parsed availability, scenes/songs with actor lists and act assignments, and requirements object. Validation report lists errors (missing actors, invalid time formats, conflicting information) and warnings (actors with no availability, scenes with missing actors).

**Integration:** Feeds validated structured data to Module 2 for constraint encoding. Catches data errors early, preventing invalid schedules downstream.

**Prerequisites:** None (can start immediately)

---

### Module 2: Constraint Representation (Propositional Logic)

**Topics:** Propositional Logic (CNF, Resolution)

**Input:** Validated structured data from Module 1: cast availability, scenes/songs with required actors and act assignments, and rehearsal requirements.

**Output:** List of CNF clauses (list of lists of literals). Encodes three constraint types: (1) Availability—if scene scheduled at time, required actors must be available (e.g., `[!Scene3_Mon_7pm, Alice_Mon_7pm]`). (2) Scene requirements—if scene scheduled, all required actors available (`[!Scene3_Mon_7pm, Bob_Mon_7pm]`). (3) Temporal—no rehearsals after 10pm (`[!Scene3_Tue_10pm]`). Also encodes musical structure: each scene and song scheduled at least once, sing-throughs cover all songs, act runs include all act content in order, full runs before tech week, tech week has fixed rehearsals (5pm-10pm each day).

**Integration:** Receives validated data from Module 1; outputs CNF clauses to Module 3 for search. Logical representation enables efficient constraint checking during search.

**Prerequisites:** Module 1, Propositional Logic coursework (Weeks 1-2)

---

### Module 3: A* Search Scheduler

**Topics:** Search (A*, heuristics, IDA*, Beam Search)

**Input:** CNF clauses from Module 2 representing constraints, plus original cast/scene/song data for state representation.

**Output:** Complete schedule (JSON) or `None` if impossible. Schedule includes rehearsal blocks with date, time, type (scene/song/sing-through/act-run/full-run), content (scene name, song name, or act), and required actors. Status field indicates success or failure.

**Integration:** Uses CNF constraints from Module 2 to validate states during search. State represents partial schedule; successors add rehearsal blocks. Heuristic estimates remaining work (unscheduled scenes/songs, missing sing-through coverage, missing act runs). Goal state satisfies all CNF constraints plus musical structure requirements (each scene and song scheduled at least once, sing-throughs cover all songs, act runs complete, full runs before tech week, tech week has fixed rehearsals 5pm-10pm each day). Feeds schedule to Module 4 for optimization.

**Prerequisites:** Module 2, Search algorithms coursework (Weeks 3-4)

---

### Module 4: Waiting Time Optimizer

**Topics:** Advanced Search (Optimization, Hill Climbing, Simulated Annealing)

**Input:** Schedule from Module 3 (JSON format with rehearsal blocks) or `None` if search failed.

**Output:** Optimized schedule (same JSON format) with reduced waiting time. Includes metrics: total waiting time (hours), improvement percentage, and optimization score.

**Integration:** Receives schedule from Module 3. Calculates waiting time for each actor (time between required rehearsals). Uses Hill Climbing or Simulated Annealing to iteratively improve: swaps rehearsal time slots, reorders scenes within same day, moves rehearsals to reduce gaps. Accepts moves that reduce total waiting time (with probability in Simulated Annealing to escape local optima). Feeds optimized schedule to Module 6 for validation.

**Prerequisites:** Module 3, Advanced Search coursework (Week 7)

---

### Module 5: NLP Input Parser

**Topics:** NLP Before LLMs (n-grams, Word Embeddings, parsing)

**Input:** Natural language text describing availability (e.g., "Alice is available Monday 7-9pm, Tuesday 6-8pm. Bob can do Wednesday evenings and Thursday 7-9pm.").

**Output:** Structured data in CSV/JSON format (same format as Module 1's input), or error report (JSON). If successful, produces CSV/JSON files with parsed cast availability, scenes, songs, and requirements. If error, lists validation issues (ambiguous input like "evenings" without specific days is rejected).

**Integration:** Converts natural language input to structured CSV/JSON format, which feeds into Module 1 for validation and normalization. Uses hybrid approach: pattern matching for structured time expressions ("Monday 7-9pm"), n-grams to identify time-related phrases ("evening", "afternoon"), word embeddings to map synonyms ("evening" ≈ "night", "7pm" ≈ "19:00"). 

**Prerequisites:** NLP coursework (Weeks 8-9)

---

### Module 6: First-Order Logic Schedule Validator

**Topics:** First-Order Logic (Quantifiers, Inference, Unification)

**Input:** Schedule from Module 4 (or `None` if Module 3 failed), original constraints, and cast/scene/song data.

**Output:** Validation report (JSON). If schedule exists: status ("valid" | "invalid"), list of satisfied constraints, list of violations (e.g., "Scene3 scheduled when Alice unavailable"). If schedule is `None`: status "impossible", list of likely conflicting constraints (e.g., "Scene3 requires Alice and Bob, but they are never available together").

**Integration:** Receives schedule from Module 4. Expresses validation rules in FOL: `∀x ∀s ∀t (Scheduled(s,t) ∧ InScene(x,s) → Available(x,t))` (all actors available), `∀x ∀t1 ∀t2 (ScheduledAt(x,t1) ∧ ScheduledAt(x,t2) ∧ Overlaps(t1,t2) → t1=t2)` (no overlaps). Checks if schedule satisfies FOL statements. If no schedule exists, uses simpler analysis (not full FOL theorem proving) to identify likely impossible constraints.

**Prerequisites:** Module 3 or 4, First-Order Logic coursework (Weeks 5-6)

---

## Feasibility Study

_A timeline showing that each module's prerequisites align with the course schedule. Verify that you are not planning to implement content before it is taught._

| Module | Required Topic(s)                    | Topic Covered By         | Checkpoint Due           |
| ------ | ------------------------------------ | ------------------------ | ------------------------ |
| 1      | None (data processing)               | Can start immediately    | Checkpoint 1 (Feb 11)    |
| 2      | Propositional Logic                  | Weeks 1-2                | Checkpoint 2 (Feb 26)    |
| 3      | Search (A*, heuristics)              | Weeks 3-4                | Checkpoint 3 (March 19)  |
| 4      | Advanced Search (Optimization)       | Week 7                   | Checkpoint 4 (April 2)   |
| 5      | NLP Before LLMs                      | Weeks 8-9                | Checkpoint 5 (April 16)  |
| 6      | First-Order Logic                    | Weeks 5-6                | Final Demo (April 23)    |

## Coverage Rationale

This proposal integrates six AI topics that naturally fit the rehearsal scheduling problem. **Propositional Logic** (Module 2) provides a clean, formal representation of scheduling constraints (availability, scene requirements, temporal limits), enabling efficient constraint checking. **Search algorithms** (Module 3) are essential for exploring the vast space of possible schedules; A* search with heuristics efficiently finds valid solutions while optimizing for completeness. **Advanced Search** (Module 4) handles the optimization aspect—minimizing waiting time through hill climbing and simulated annealing, demonstrating how search techniques adapt to preference optimization. **NLP** (Module 5) enables natural language input parsing, making the system more accessible while demonstrating how AI can bridge human communication and structured data. **First-Order Logic** (Module 6) extends propositional logic with quantifiers, allowing expressive validation rules ("for all actors in a scene, they must be available") and conflict diagnosis.

The workflow progresses from natural language input to final schedule: natural language (Module 5) converts to structured CSV/JSON format, which Module 1 validates and normalizes, then Module 2 encodes constraints, Module 3 searches for valid schedules, Module 4 optimizes waiting time, and Module 6 validates the final result. However, development does not follow this workflow order because NLP is not covered until Weeks 8-9, while Modules 1-4 and 6 can be built earlier using the topics covered in Weeks 1-7. Therefore, Module 1 receives direct CSV/JSON input during early development (Checkpoints 1-4) before Module 5 is implemented at Checkpoint 5, allowing the core scheduling system to be built and tested incrementally as topics are taught.

The trade-off considered was choosing pure search over a hybrid search+logic approach. Pure search was selected for its natural fit with optimization (waiting time minimization) and feasibility within the timeline. While a SAT-solver approach could find valid schedules, search better handles the preference optimization aspect. The system still leverages logic (propositional and first-order) for constraint representation and validation, combining the strengths of both approaches.
