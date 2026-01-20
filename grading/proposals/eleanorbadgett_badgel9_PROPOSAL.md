# Intelligent PDF Table Parser and Basic Agent

## System Overview

This system addresses the challenge of extracting and understanding complex table structures from PDF documents, with particular focus on handling nested headers and merged cells that existing solutions struggle with. The system identifies tables in PDFs, parses their hierarchical structure using logical reasoning, builds a semantic knowledge base of table content, and enables natural language question-answering about table data. Additionally, it employs reinforcement learning to continuously improve parsing accuracy based on performance feedback.

The theme naturally accommodates multiple AI techniques: Search algorithms locate table regions efficiently, First-Order Logic reasons about complex structural relationships (which cells belong to which headers, merged cell relationships), NLP techniques understand user questions, knowledge representation structures semantic understanding of table content, and reinforcement learning adapts parsing strategies over time. This problem space requires genuine AI reasoning—detecting structure where metadata is ambiguous, understanding relationships between cells, and learning from experience—making it an appropriate domain for exploring core AI concepts.

## Modules

### Module 1: Table Region Detection

**Topics:** Search (Uninformed Search: BFS, DFS, Uniform Cost, Iterative Deepening; Informed Search: Heuristics, A*, IDA*, Beam Search)

**Input:** PDF files or image files in standard formats (PDF documents or image files like PNG/JPEG containing table structures).

**Output:** Candidate table regions with bounding box coordinates (list of coordinate tuples specifying (x_min, y_min, x_max, y_max) for each detected table region, with confidence scores).

**Integration:** This is the first module in the pipeline. It locates potential table regions in PDF documents, which are then passed to Module 2 for structure parsing. The output provides the spatial boundaries needed for all subsequent processing.

**Prerequisites:** Search topics (Uninformed & Informed Search) must be covered in class. This includes understanding heuristic search, A* algorithm, beam search, and uniform cost search, as these techniques will be used to efficiently explore candidate table regions in the PDF space.

---

### Module 2: Structure Parsing - Row/Column Divisions and Complex Structures

**Topics:** Search (Advanced Search: Optimization, Beam Search), First-Order Logic (Quantifiers, Unification, Inference, Chaining)

**Input:** Table regions from Module 1 (bounding box coordinates) plus the original PDF file.

**Output:** Structured representation of complete table structure (logical representation specifying: row and column divisions/cell boundaries, which cells belong to which headers, header nesting levels, merged cell relationships, cell-to-header mappings, and row/column groupings) plus extracted cell content/text values (raw text data from each cell).

**Integration:** Uses output from Module 1 to focus parsing on detected table regions. When PDF metadata contains explicit cell boundaries, extracts boundaries directly; when metadata is missing, uses Search algorithms (beam search, optimization techniques) to infer row/column divisions. Uses First-Order Logic to reason about nested headers, merged cells, and hierarchical relationships. The parsed structure enables data extraction (utility function) and feeds into Module 3 for knowledge base construction.

**Prerequisites:** Search topics (Advanced Search, optimization techniques, beam search) and First-Order Logic topics must be covered (quantifiers, unification, inference methods). Module 1 must be completed to provide table regions. Both Search and Logic are essential: Search for inferring cell boundaries when metadata is missing, Logic for determining complex structural relationships.

---

### Module 3: Semantic Knowledge Base Construction

**Topics:** First-Order Logic / Knowledge Representation (Knowledge Bases, Inference Methods)

**Input:** Parsed table structure and cell content from Module 2 (logical representation of hierarchy plus extracted text data from each cell).

**Output:** Knowledge base containing: (1) Logical representation of table structure (from Module 2), (2) Semantic understanding of content (data types detected: dates, numbers, categories), (3) Content context/meaning (e.g., "column X contains dates", "rows represent transactions"), (4) Relationships between cells based on content (e.g., "sum of column Y", hierarchical relationships between values).

**Integration:** Builds on Module 2's structural parsing (which identifies WHAT the structure is) to add semantic understanding (WHAT the content means). While Module 2 focuses on structural relationships (rows, columns, headers, merged cells), Module 3 focuses on content semantics (data types, meanings, relationships between values). This knowledge base is used by Module 5 for question answering, enabling the system to reason about both table structure and content meaning when answering user queries.

**Prerequisites:** First-Order Logic and knowledge representation topics must be covered (knowledge bases, inference methods). Module 2 must be completed to provide parsed structure. This module requires understanding how to represent knowledge logically and make inferences about semantic relationships.

---

### Module 4: Natural Language Question Understanding

**Topics:** NLP Before LLMs (n-grams, Word Embeddings)

**Input:** Natural language questions as text strings (e.g., "What is the maximum value in column X?", "What is the sum of column Y?", "Which row has the highest value in column Z?").

**Output:** Structured query representation (dictionary/JSON format containing: column name or identifier, operation type: max/min/sum/count/average, optional filters: row conditions or value constraints).

**Integration:** Processes user questions to extract structured query information. The structured queries are passed to Module 5 for execution against the knowledge base. This module enables natural language interaction with the table data.

**Prerequisites:** NLP topics must be covered (n-grams, word embeddings for understanding semantic meaning of question words like "maximum", "sum", "highest"). No prior modules required—this processes user input independently, though it will be used in conjunction with Modules 3 and 5.

---

### Module 5: Question Answering

**Topics:** Logic (First-Order Logic - Inference, Reasoning about Knowledge Base)

**Input:** Structured query from Module 4 (column name, operation type, filters) plus knowledge base from Module 3 (logical representation of table structure and semantic content understanding).

**Output:** Answers to questions about table content (structured response containing: the answer value or result, explanation of how it was derived, and source information from the knowledge base).

**Integration:** Combines outputs from Modules 3 and 4 to answer user questions. Uses logical reasoning to query the knowledge base, understanding both structural relationships (from Module 2/3) and semantic content (from Module 3) to provide accurate answers about cell and table content.

**Prerequisites:** Logic topics must be covered (inference methods, reasoning about knowledge bases). Modules 3 and 4 must be completed to provide the knowledge base and structured queries. This module requires understanding how to perform logical inference over structured knowledge to answer questions.

---

### Module 6: Adaptive Parsing Improvement

**Topics:** Reinforcement Learning (Policy, MDP, Value Functions, Q-Learning)

**Input:** Previous parsing attempts from Module 2 (parsing results, detected structures), plus success metrics (accuracy of structure detection, correctness of header relationships, user feedback on extracted data quality).

**Output:** Improved parsing strategies/parameters for Module 2 (optimized heuristics for detecting merged cells, improved header hierarchy detection algorithms, refined parameters for structure parsing).

**Integration:** Learns from Module 2's performance over time to improve parsing accuracy. Outputs enhanced parsing parameters and strategies that can be fed back into Module 2 for future table parsing tasks, enabling the system to adapt and improve with experience.

**Prerequisites:** Reinforcement Learning topics must be covered (MDPs, value functions, Q-learning, policy learning). Module 2 must have been running to collect performance data. This module requires understanding how to formulate the parsing problem as a learning task and use RL to optimize parsing strategies based on reward signals from parsing accuracy.

---

## Feasibility Study

_A timeline showing that each module's prerequisites align with the course schedule. Verify that you are not planning to implement content before it is taught._

| Module | Required Topic(s) | Topic Covered By | Checkpoint Due |
| ------ | ----------------- | ---------------- | -------------- |
| 1      | Uninformed & Informed Search (BFS, DFS, Uniform Cost, A*, IDA*, Beam Search) | Weeks 2-3 (1.5 weeks) | Checkpoint 1 (Feb 11) |
| 2      | Advanced Search (Optimization, Beam Search) + First-Order Logic (Quantifiers, Unification, Inference, Chaining) | Weeks 4-5 (Advanced Search: 1 week, First-Order Logic: 1.5 weeks) | Checkpoint 2 (Feb 26) |
| 3      | First-Order Logic / Knowledge Representation | Weeks 4-5 (1.5 weeks) | Checkpoint 3 (March 19) |
| 4      | NLP Before LLMs (n-grams, Word Embeddings) | Weeks 6-7 (1.5 weeks) | Checkpoint 4 (April 2) |
| 5      | Logic (Inference, Reasoning about Knowledge Base) | Weeks 4-5 (First-Order Logic) | Checkpoint 4 (April 2) |
| 6      | Reinforcement Learning (Policy, MDP, Value Functions, Q-Learning) | Weeks 8-9 (1.5 weeks) | Checkpoint 5 (April 16) |

**Timeline Analysis:** All modules align with course coverage. Module 1 uses Search (covered Weeks 2-3, due Checkpoint 1). Module 2 uses Advanced Search and First-Order Logic (covered Weeks 4-5, both complete by end of Week 5, due Checkpoint 2). Module 3 uses First-Order Logic (covered Weeks 4-5, due Checkpoint 3). Module 4 uses NLP (covered Weeks 6-7, due Checkpoint 4). Module 5 uses Logic (covered Weeks 4-5) and requires Modules 3-4, due Checkpoint 4. Module 6 uses RL (covered Weeks 8-9, due Checkpoint 5). Module 2 will have accumulated sufficient performance data by Checkpoint 5 for Module 6's learning.

## Coverage Rationale

Each topic addresses a distinct aspect of the table parsing problem and maps to specific modules: **Search** (Modules 1, 2) locates table regions and infers cell boundaries when metadata is missing. **First-Order Logic** (Modules 2, 3, 5) reasons about structural relationships (nested headers, merged cells) and semantic content understanding. **Knowledge Representation** (Module 3) structures semantic understanding of table content. **NLP** (Module 4) enables natural language question understanding. **Reinforcement Learning** (Module 6) adapts parsing strategies over time. The theme requires genuine AI reasoning rather than pattern matching, making it appropriate for exploring core AI concepts.

**Required Topic Coverage:** Search (Module 1) satisfies the requirement using non-trivial algorithms (A*, Beam Search) to explore candidate table regions.

**Trade-offs:** Supervised Learning was considered but excluded to maintain focus and depth. The RL module requires Module 2 to accumulate data first, which is feasible and creates a natural learning feedback loop.
