# Rule-Based Text Corpus Creator/Explorer with Relational Search

## System Overview

Our system lets users build and explore a custom English-first corpus to understand words through meaning, form, and history. Users enter dictionary-style data (word, definition, part of speech, optional pronunciation, etymology, example sentences). Module 1 (Propositional Logic rules) segments words into roots/affixes with confidence, producing structured records. Module 3 (NLP, Bag-of-Words) adds semantic vectors and optional phonological features. Module 2 (Search with A*/beam) ranks top-k similar words by a normalized distance per relationship type (morphological/semantic/phonological). Module 4 (rule + numeric inference) suggests low-authority semantic relations (synonym/antonym/broader/narrower/related, homophone/homograph flags, lightweight polysemy clusters) using definitions and example contexts; user facts always override. Module 5 builds a user-driven etymology graph and uses A* to find best paths between words, optionally guided by semantic heuristics and weak inferred signals (never auto-creating edges). Scope is intentionally English-first and BoW is chosen over heavier ML to match course timing and keep reasoning transparent; future versions can extend to other (including constructed) languages and richer embeddings.

Flow: User entry → M1 rules → M3 features → M2 search / M4 inference → M5 etymology paths


## Modules

### Module 1: Rule-Based Morphological Analysis

**Topics:** Knowledge Representation / Propositional Logic

**Input:** Required fields: `word` (string), `definition` (string), `part_of_speech` (string). Optional fields: `pronunciation` (string), `etymology` (string), `example_sentences` (array of strings).

**Output:** JSON object per word containing: normalized word (spelling-corrected if needed), morphological features (root, prefixes, suffixes, morpheme structure as array, confidence score 0-1), raw input data. Morphological structure inferred via logical rule application. Confidence computed based on rule match strength and whether inferred root exists in corpus.

**Integration:** Produces basic morphological analysis that feeds into Module 2 (Search) as initial feature vectors. Provides etymological relationship data (if provided) for Module 5 (etymology graph construction). Output enhanced by Module 3 with additional semantic/phonological features.

**Prerequisites:** Course content on Knowledge Representation / Propositional Logic (typically covered early in semester).

---

### Module 2: Multi-Dimensional Word Search

**Topics:** Search (A* or Beam Search)

**Input:** `start_word` (string), `relationship_type` (enum: morphological_similarity, semantic_similarity, phonological_similarity), `k` (integer, number of results), optional `distance_threshold` (float, maximum acceptable distance).

**Output:** Ranked list of tuples: `[(word: string, distance_score: float), ...]` containing top-k most similar words for the chosen relationship type. `distance_score` is normalized to 0–1 per mode (0 = identical, 1 = far); examples: morphological distance from morpheme overlap; semantic distance = 1 − cosine(BoW vectors); phonological distance from phonetic feature distance. For etymology-specific “how are these two words related?” paths, defer to Module 5.

**Integration:** Consumes feature vectors from Module 1 (morphological features) and from Module 3 (semantic/phonological embeddings) if provided. Searches through multi-dimensional embedding space using beam search or A* algorithm. Cost function: distance in relevant dimension (morphological, semantic, etc.). Heuristic: estimated similarity to guide search efficiently. Results can feed into visualization or query interface modules.

**Prerequisites:** Module 1 (requires morphological feature vectors). Module 3 is required for semantic/phonological similarity modes. Course content on Search algorithms (most likely A*, beam search).

---

### Module 3: Semantic & Phonological Feature Extraction

**Topics:** Natural Language Processing

**Input:** JSON objects from Module 1 containing word entries with definitions, example sentences, and optional pronunciation data.

**Output:** Enhanced JSON objects adding: semantic embedding (Bag-of-Words vector computed from definition and example sentences), phonological features (phonetic feature vector if pronunciation provided, null otherwise), enhanced morphological confidence scores. All embeddings in numerical vector format ready for Module 2 search operations.

**Integration:** Consumes output from Module 1, enhances it with NLP-derived features. Produces semantic embeddings for Module 2 (semantic similarity search) and Module 5 (heuristic guidance for etymology path finding). Phonological features enable phonological similarity searches in Module 2. Semantic features can suggest potential etymological relationships (marked as "suggested" rather than automatic) for Module 5.

**Prerequisites:** Module 1 (requires word entries with definitions), course content on Natural Language Processing (typically covered mid-to-late semester).

---

### Module 4: Semantic Relationship Inference from Context

**Topics:** Knowledge Representation / Propositional Logic (Inference) + NLP feature use (from Module 3)

**Input:** JSON word entries from Module 1 (including `word`, `definition`, `part_of_speech`, and optional `example_sentences`) plus Module 3 semantic/phonological features when available (Bag-of-Words vectors; pronunciation-derived features if provided).

**Output:** A set of inferred relationship assertions stored as structured JSON. Supported relationship types include:
- **Meaning relations**: `synonym_of(a, b)`, `antonym_of(a, b)`, `broader_than(a, b)`, `narrower_than(a, b)`, `related_to(a, b)` (some relationship, unknown/ambiguous)
- **Ambiguity relations/flags**: `homophone_of(a, b)`, `homograph_of(a, b)`, and `homonym_of(a, b)`
- **Polysemy signal**: `polysemous(word)` with internal “sense candidates” stored as clusters of example sentences (each cluster records supporting sentence IDs and an optional short label). This is a lightweight signal, not a full word-sense-disambiguation system.

Each assertion includes a confidence score (0–1) and provenance (which rule(s) fired and which definitions/sentences supported it).

**Integration:** Uses a hybrid approach: propositional rules over observed patterns (definition overlap, shared context patterns in example sentences, part-of-speech constraints) and numeric thresholds derived from Module 3 features (e.g., cosine similarity between BoW context/definition vectors) to produce candidate relations. Inferred relations are lower authority than user-entered facts and are marked as inferred; Module 2 can use them as a weak signal to re-rank/filter results rather than overriding the user’s data.

**Prerequisites:** Module 1 (needs word entries and example sentences), Module 3 (numeric semantic/phonological features), course content on knowledge bases and inference in Propositional Logic.

---

### Module 5: Etymology Graph Construction & Path Finding

**Topics:** Search (A*), Knowledge Representation

**Input:** Two words `(start_word: string, target_word: string)`, optional `max_path_length: int` (default: 10), optional `relationship_types: array` to filter which relationship types to consider.

**Output:** If a path exists, returns a structured JSON object containing: an array of path steps (each with word, relationship type, target word, and confidence level), total cost, and path length. Relationship types include: derives_from, cognate_with, borrowed_from, variant_of, compound_of. Confidence levels are: verified, conjectured, or user_created. If no path exists within max_path_length, returns null with error message: "No etymological relationship found within N steps". Else if no etymology edges exist for the given words, return null with message ‘No etymological relationship found—add or import edges to search.’”

**Integration:** Consumes etymological links from Module 1 (both user-provided and external sources). Uses semantic features from Module 3 as heuristic guidance (semantic similarity as proxy for etymological closeness). Optionally uses inferred “related_to”/similarity signals from Module 4 as an additional weak heuristic (never as automatic edge creation). Builds and maintains the etymology graph structure. Outputs paths for exploration and visualization. Semantic suggestions are marked as "suggested" rather than automatically creating edges.

**Prerequisites:** Module 1 (for etymological relationship data), Module 3 (for semantic features used in heuristic), Module 4 (optional; inferred relations used only as a weak heuristic), course content on Search algorithms (A* specifically).


## Feasibility Study

_A timeline showing that each module's prerequisites align with the course schedule. Verify that you are not planning to implement content before it is taught._

| Module | Required Topic(s)                               | Topic Covered By | Checkpoint Due (target)        |
| ------ | ----------------------------------------------- | ----------------------- | ----------------------- |
| 1      | Propositional Logic (morphology rules)          | Week 2–3                | Week 3                  |
| 2      | Search (A* / Beam); uses Module 1 features      | Week 3–5                | Week 5                  |
| 3      | NLP (Bag-of-Words, basic text features)         | Week 7–9                | Week 9                  |
| 4      | Propositional Logic + Module 3 features (NLP)   | Week 7–9                | Week 10                 |
| 5      | Search (A*), Knowledge Representation; needs 1,3| Week 8–10               | Week 11                 |

M5 will initiallys rely on unheuristic user-provided edges. 
Semantic heuristics (which M3 provides) will be added once M3 is done.

## Coverage Rationale

We focus on three core topics because they naturally fit a user-built linguistics corpus:
- **Propositional Logic / Knowledge Representation** (Modules 1, 4): Linguistic rules (morphology) and inferred semantic relations are best expressed as explicit rules with controlled, low-authority inferences.
- **Search (A* / Beam)** (Modules 2, 5): Exploring similarity across word features (vector space) and tracing etymological connections (graph space) are both non-trivial search problems.
- **NLP (BoW)** (Module 3): Definitions and example sentences are text; lightweight BoW features are feasible mid-semester and power both search heuristics and inference.

Trade-offs for feasibility and honesty:
- **English-first scope** to stay realistic with rules, data, and evaluation; future versions can generalize to other (including constructed/learned) languages.
- **BoW over heavier ML embeddings** to align with course timing and reduce complexity; keeps computation transparent for logic-based inference.
- **Inferred relations remain lower authority than user-entered facts** to avoid overclaiming and let users correct or confirm suggestions.
