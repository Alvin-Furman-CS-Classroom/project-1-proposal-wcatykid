# Handwritten Music Recognition System

## System Overview

This system converts handwritten musical notation from scanned PDFs into clean, digital sheet music. The core challenge is resolving ambiguity in handwritten symbols—determining whether a smudged mark is a quarter note or half note, distinguishing a sharp from a natural, or identifying note positions on staff lines.

The system uses AI techniques to interpret ambiguous symbols, validate musical correctness, and produce polished output. Search algorithms (Beam Search, A*) explore interpretation sequences to find the most likely overall reading when symbols are ambiguous. Propositional logic encodes musical rules (e.g., "if time signature is 4/4, then measure duration must equal 4 beats") and validates compliance through logical inference. The problem domain requires handling uncertainty, making decisions under ambiguity, and ensuring output correctness—all central AI challenges.

## Modules

### Module 1: Image Preprocessing and Staff Detection

**Topics:** Basic image processing (foundational preprocessing)

**Input:** PDF file containing scanned handwritten music notation

**Output:** Preprocessed image (grayscale, noise-reduced) with JSON file containing: array of staff line coordinates (y-positions for each of 5 lines per staff), measure boundary x-coordinates, and page dimensions

**Integration:** Provides structured image data to Module 2 for symbol detection. Staff line positions are critical for determining note pitches in later modules, as note positions relative to staff lines determine their pitch values.

**Prerequisites:** Basic image processing concepts

---

### Module 2: Symbol Detection and Initial Classification

**Topics:** Basic pattern recognition (foundational preprocessing)

**Input:** Preprocessed image and staff line coordinates JSON from Module 1

**Output:** JSON array of symbol objects, each containing: bounding box (x, y, width, height), list of classification candidates with confidence scores (e.g., [{"type": "quarter_note", "confidence": 0.7}, {"type": "half_note", "confidence": 0.3}]), and staff line position (which line/space the symbol occupies)

**Integration:** Provides ambiguous symbol candidates to Module 3, which will resolve the ambiguity using search algorithms. The confidence scores and multiple candidates for each symbol create the ambiguity that Module 3's search algorithm will resolve.

**Prerequisites:** Module 1, basic pattern recognition concepts

---

### Module 3: Ambiguous Symbol Interpretation Using Search

**Topics:** Search (Beam Search, A*)

**Input:** JSON array of ambiguous symbol candidates from Module 2, where each symbol has multiple possible interpretations with confidence scores

**Output:** JSON object containing: definitive classification for each symbol (e.g., {"symbol_id": 5, "type": "quarter_note", "pitch": "E4", "duration": 1}), overall sequence score, and search path taken (for debugging)

**Integration:** Resolves ambiguity from Module 2's initial classifications using beam search to explore interpretation sequences. The search algorithm considers context (neighboring symbols, musical patterns) to find the most likely overall interpretation. Beam search maintains multiple promising paths, scoring each based on confidence scores and musical consistency. Output feeds into Module 4 for time signature validation and Module 5 for final validation.

**Prerequisites:** Module 2, Search algorithms (Beam Search, A*)

---

### Module 4: Time Signature Detection and Validation

**Topics:** Propositional Logic

**Input:** Interpreted symbol sequence JSON from Module 3, including detected time signature indicators (if visible in the image)

**Output:** JSON object with: time signature for each measure (e.g., {"measure_1": "4/4", "measure_2": "4/4"}), list of measures where note durations don't sum to the time signature (logical violations), and suggested corrections

**Integration:** Uses Module 3's interpreted symbols to determine and validate time signatures. Propositional logic encodes rules as logical statements (e.g., "time_signature(measure_1, 4/4) → duration_sum(measure_1, 4)") and uses forward chaining or resolution to validate each measure. If a measure violates its time signature, the logical inference identifies the violation. Output informs Module 5's validation checks.

**Prerequisites:** Module 3, Propositional Logic

---

### Module 5: Musical Validity Validation

**Topics:** Propositional Logic

**Input:** Interpreted symbols JSON from Module 3, time signatures and logical violations from Module 4

**Output:** Final validated musical notation JSON with: error flags for remaining logical violations (e.g., invalid accidentals, measure completeness issues), corrected symbol interpretations where logical rules suggest fixes, and validation report

**Integration:** Final validation step before output generation. Uses propositional logic to encode musical rules as logical statements (e.g., "key_signature(F#) → ∀note(note.pitch == F → note.accidental == sharp)") and applies inference methods (forward chaining, resolution) to validate rule compliance. Ensures musical correctness of Module 3's interpretations, cross-referencing with Module 4's time signature information. When violations are detected, logical inference suggests corrections.

**Prerequisites:** Module 3, Module 4, Propositional Logic

---

### Module 6: Digital Sheet Music Generation

**Topics:** Basic output formatting (no AI topic required)

**Input:** Validated musical notation JSON from Module 5

**Output:** Clean digital sheet music file in specified format (e.g., MusicXML, LilyPond format, or rendered PNG image of clean notation)

**Integration:** Final output stage. Takes validated notation from Module 5 and formats it into the desired output format. MusicXML or LilyPond formats enable import into music notation software (MuseScore, Finale), while PNG provides a visual representation of the cleaned notation.

**Prerequisites:** Module 5

---

## Feasibility Study

_A timeline showing that each module's prerequisites align with the course schedule. Verify that you are not planning to implement content before it is taught._

| Module | Required Topic(s) | Topic Covered By | Checkpoint Due |
| ------ | ----------------- | ---------------- | -------------- |
| 1      | Basic image processing | No course topic required (preprocessing) | Checkpoint 1 |
| 2      | Basic pattern recognition | No course topic required (preprocessing) | Checkpoint 1 |
| 3      | Search (Beam Search, A*) | Weeks 1.5-3 | Checkpoint 2 |
| 4      | Propositional Logic | Weeks 1-1.5 | Checkpoint 3 |
| 5      | Propositional Logic | Weeks 1-1.5 (reuses from Module 4) | Checkpoint 4 |
| 6      | Basic output formatting | No AI topic required | Checkpoint 5 |

## Coverage Rationale

The chosen topics align naturally with the core challenges of handwritten music recognition.

**Search algorithms (Beam Search, A*)** are essential for resolving ambiguity—when a handwritten symbol could be multiple things, search explores interpretation sequences to find the most likely overall reading. Beam search is particularly well-suited because it maintains multiple promising interpretation paths, allowing the system to consider context from neighboring symbols. This directly addresses the system's primary AI challenge: making decisions under uncertainty.

**Propositional Logic** appears in two modules because music notation has strict rules that can be encoded as logical statements: "if time signature is 4/4, then measure duration must equal 4 beats," "if key signature has F#, then all F notes are sharp unless overridden," etc. These logical rules can be validated using inference methods (forward chaining, resolution), making propositional logic a natural fit for musical validation. The logical framework allows systematic checking of rule compliance across the entire score.

Modules 1 and 2 use basic preprocessing techniques rather than advanced AI topics because the core AI challenge lies in interpretation and validation, not in low-level image processing. This keeps the focus on meaningful AI applications while ensuring a complete, working system.

The trade-off is that we're not using some course topics (e.g., Game Theory, Reinforcement Learning) that don't naturally fit this domain. However, the selected topics—Search and Propositional Logic—are deeply integrated into the problem and provide substantial, non-trivial AI challenges. Both topics are covered early in the course (weeks 1-3), ensuring feasibility across all checkpoints.
