# Recipe AI System
## Elliott Chmil
## CSC 343, January 20, 2026

## System Overview

The Recipe AI System helps users discover, adapt, and generate recipes tailored to their dietary constraints, ingredient availability, and personal preferences. Users provide dietary restrictions (allergies, vegetarian, etc.), available ingredients, cuisine preferences, and desired course type (appetizer, main course, drink, dessert). The system processes a recipe database, searches for compatible recipes, adapts them with ingredient substitutions when needed, and recommends personalized options. When no suitable recipes exist, it generates new recipes from available ingredients. Optionally, it can create optimized meal plans that maximize ingredient reuse and minimize preparation time.

This theme naturally engages multiple AI concepts. **Propositional Logic** encodes dietary constraints as a knowledge base, enabling precise filtering (e.g., "if vegetarian then no meat"). **Search algorithms** retrieve and rank recipes from large databases using ingredient matching and preference scoring, making the search non-trivial through multi-criteria optimization. **Constraint Satisfaction** validates ingredient substitutions while maintaining dietary compatibility. **Machine Learning** powers content-based recommendation by matching recipe features to user preference weights learned from questionnaires. **Planning algorithms** sequence cooking steps and optimize meal plans, exploring ingredient combinations and temporal scheduling. The recipe domain provides concrete, testable problems with clear success criteria, making it ideal for demonstrating how these AI techniques integrate into a cohesive system that solves real-world personalization challenges.

## Modules

### Module 1: Recipe Database Cleaning & Preprocessing

**Topics:** Data Processing, Knowledge Representation

**Input:** Raw recipe dataset in CSV or JSON format. CSV format with columns: recipe_id, title, ingredients (comma-separated list), instructions, prep_time, cuisine_type, course_type, difficulty, nutritional_info. Alternatively, JSON format with array of recipe objects containing same fields with ingredients as arrays. May also include ingredient database (CSV or JSON) with: ingredient_name, category, allergen_info, substitution_options.

**Output:** Cleaned, structured recipe database (JSON or SQLite): normalized ingredient names, standardized units, parsed ingredient lists into structured arrays, validated prep times and difficulty levels, extracted metadata. Also outputs cleaned ingredient knowledge base with substitution rules and allergen mappings.

**Integration:** This module prepares the data foundation for all subsequent modules. Modules 3, 4, 5, and 6 all depend on this cleaned database. The ingredient knowledge base feeds into Module 4 for substitutions. Module 6 uses the database patterns for recipe generation.

**Prerequisites:** Course content on data structures, basic knowledge representation. This is a foundational module that can be started early.

---

### Module 2: Dietary Constraint Parser with Preference Weights

**Topics:** Propositional Logic

**Input:** User-provided dietary constraints via questionnaire: allergies (list of strings), dietary preferences (e.g., "vegetarian", "gluten-free"), cuisine preferences with weights (e.g., {"Italian": 0.8, "Mexican": 0.6}), preferred flavors with weights (e.g., {"spicy": 0.7, "sweet": 0.3}), and course type specification (appetizer, main course, drink, dessert).

**Output:** A knowledge base in propositional logic format (CNF clauses) encoding hard constraints. For example: `¬contains(peanuts) ∧ ¬contains(shellfish) ∧ (vegetarian → ¬contains(meat))`. Also outputs a preference weight vector (JSON object) mapping features to numerical weights (0.0-1.0) for soft preferences.

**Integration:** This module's output feeds into all recipe search, filtering, generation, and recommendation modules. Other modules query this knowledge base to verify recipe compatibility and use preference weights for ranking. Module 4 uses this to validate substitutions. Module 6 uses constraints during recipe generation.

**Prerequisites:** Course content on Propositional Logic, CNF conversion, knowledge base construction.

---

### Module 3: Ingredient-Based Recipe Search

**Topics:** Search (non-trivial: information retrieval with ranking, possibly beam search for optimal ingredient combination matching)

**Input:** Available ingredients list (array of strings), constraint knowledge base and preference weights from Module 2, optional parameters (max prep time, difficulty level, cuisine type, course type), cleaned recipe database from Module 1.

**Output:** Ranked list of recipe candidates (JSON array). Each recipe object contains: recipe_id, title, match_score (based on ingredient overlap and preference weights), missing_ingredients_count, missing_ingredients_list, prep_time, difficulty, cuisine_type, course_type, ingredients_list, instructions.

**Integration:** Uses constraints from Module 2 to filter incompatible recipes. Searches the cleaned database from Module 1. Output feeds into Module 4 (adaptation) if recipes need modification. If no good matches, triggers Module 6 (generation). Output can also feed into Module 5 (recommendation) when available.

**Prerequisites:** Course content on Search algorithms (information retrieval, ranking, beam search), Module 1 (cleaned database), Module 2 (constraint knowledge base).

---

### Module 4: Recipe Adaptation & Rule-Based Substitution

**Topics:** Constraint Satisfaction, Search (for finding valid substitutions)

**Input:** A recipe candidate from Module 3, available ingredients list, constraint knowledge base from Module 2, ingredient substitution rules from Module 1's knowledge base.

**Output:** Adapted recipe (JSON) with ingredient substitutions applied where needed. Includes: original_ingredients, substituted_ingredients (mapping like "butter → olive oil"), modified_ingredient_list, updated_instructions (text with substitutions noted), validation_status (confirms all substitutions satisfy Module 2's constraints).

**Integration:** Receives partial matches from Module 3. Uses rule-based substitution dictionary from Module 1. Validates each substitution against Module 2's constraint knowledge base to ensure dietary compatibility. Output can feed into Module 5 (recommendation) when available, or Module 6 (generation) if adaptation is insufficient, or Module 7 (meal planning) for final planning.

**Prerequisites:** Course content on Constraint Satisfaction, Module 1 (substitution rules), Module 2 (constraints), Module 3.

---

### Module 5: Preference Learning & Recommendation

**Topics:** Machine Learning (content-based filtering, supervised learning basics)

**Input:** User preference profile from questionnaire (cuisine preferences, flavor preferences, course type), preference weights from Module 2, recipe candidates from Modules 3/4/6, course type specification (appetizer/drink/main/dessert).

**Output:** Ranked recommendation list (JSON array) with top N recipes, each including: recipe_id, title, recommendation_score (based on preference weights and learned patterns), explanation_text (why it was recommended, e.g., "Matches your preference for Italian cuisine and spicy flavors"), course_type_match.

**Integration:** Takes recipes from Modules 3/4/6 and re-ranks them using preference weights from Module 2. Uses content-based filtering and supervised learning techniques to match recipe features (cuisine, flavors, course type) to user preferences. Output is the final recipe suggestions shown to the user. Can feed into Module 7 for meal planning.

**Prerequisites:** Course content on Machine Learning (supervised learning, content-based recommendation systems), Modules 1-4, Module 6 (optional but recommended).

---

### Module 6: Recipe Generation from Ingredients

**Topics:** Planning, Search (for step sequencing and ingredient combination, optimization)

**Input:** Available ingredients list, constraint knowledge base and preference weights from Module 2, cuisine style preference, target course type (appetizer/drink/main/dessert), cleaned recipe database from Module 1 (for pattern learning).

**Output:** Generated recipe (text format) with: ingredient list with quantities (e.g., "2 cups flour, 1 tsp salt"), ordered sequence of cooking steps (numbered steps as plain text), estimated prep time (integer minutes), difficulty level (text: "Easy", "Medium", "Hard"). Recipe must satisfy all constraints from Module 2.

**Integration:** Activated when Module 3 finds insufficient matches or when user requests recipe generation. Uses Module 1's database patterns and Module 2's constraints throughout generation. Uses planning algorithms to sequence steps optimally. Output can feed into Module 5 (recommendation) for final ranking or Module 7 (meal planning) for planning.

**Prerequisites:** Course content on Planning algorithms, Advanced Search/Optimization, Module 1, Module 2, Module 3 (for triggering).

---

### Module 7: Meal Planning & Optimization _(optional)_

**Topics:** Planning, Search (optimization)

**Input:** Selected recipes from Module 5 (or Modules 3/4/6), time constraints (e.g., "prepare 3 meals for this week"), nutritional goals (optional), ingredient reuse preferences.

**Output:** Meal plan (JSON) with: assigned recipes to days/meals, optimized shopping list (consolidated ingredients with total quantities), cooking schedule with parallelizable steps identified, total cost estimate (if price data available).

**Integration:** Takes final recipe selections and creates a cohesive meal plan. Uses planning algorithms and optimization techniques to optimize ingredient reuse and minimize prep time. This is the final output module that coordinates multiple recipes. Can work with outputs from Modules 3/4/6 directly, or with Module 5's recommendations.

**Prerequisites:** Course content on Planning, Search optimization, Modules 1-4, Module 6 (recommended), Module 5 (optional but recommended for best results).

---

## Feasibility Study

_A timeline showing that each module's prerequisites align with the course schedule. Verify that you are not planning to implement content before it is taught._

| Module | Required Topic(s) | Topic Covered By | Checkpoint Due |
| ------ | ----------------- | ---------------- | -------------- |
| 1      | Data Processing, Knowledge Representation | No specific topic required (can start immediately) | Checkpoint 1 (Feb 11) |
| 2      | Propositional Logic, CNF conversion | Week 1.5 (by ~Jan 29) | Checkpoint 1 (Feb 11) ✓ |
| 3      | Search algorithms (beam search, A*, ranking) | Week 3 (by ~Feb 12) | Checkpoint 2 (Feb 26) ✓ |
| 4      | Constraint Satisfaction, Search | Week 3 (Search by ~Feb 12); Constraint Satisfaction uses Search techniques | Checkpoint 2 (Feb 26) ✓ |
| 5      | Machine Learning (content-based filtering) | Week 10+ (Intro to Supervised Learning by ~April 16) | Checkpoint 4 (April 2) or Checkpoint 5 (April 16) |
| 6      | Planning algorithms, Search | Week 5.5 (Advanced Search/Optimization by ~March 5) | Checkpoint 3 (March 19) ✓ |

**Note:** Module 7 (Meal Planning) is optional and would use Planning and Search optimization topics (covered by week 5.5, ~March 5), making it feasible for Checkpoint 3 (March 19) or later.

**Timeline Summary (based on topic schedule):**
- **Checkpoint 1 (Feb 11):** Modules 1 & 2 complete
  - Module 1: Data Cleaning (no topic dependency)
  - Module 2: Propositional Logic (covered by week 1.5, ~Jan 29) ✓
- **Checkpoint 2 (Feb 26):** Modules 3 & 4 complete
  - Module 3: Search (covered by week 3, ~Feb 12) ✓
  - Module 4: Constraint Satisfaction (uses Search techniques from week 3) ✓
- **Checkpoint 3 (March 19):** Module 6 complete
  - Module 6: Planning (uses Advanced Search/Optimization from week 5.5, ~March 5) ✓
- **Checkpoint 4 (April 2):** Module 5 complete or in progress
  - Module 5: Machine Learning (Intro to Supervised Learning starts around week 10, ~April 16)
  - **Note:** ML topic coverage may be tight for Checkpoint 4; Checkpoint 5 (April 16) is safer
- **Checkpoint 5 (April 16):** Module 5 complete, integration, optional Module 7, final refinement

**Important Adjustments:**
- Module 5 (Machine Learning) should target Checkpoint 4 or 5, as supervised learning topics are covered later in the semester (week 10+). Consider using simpler content-based filtering that doesn't require full ML coverage, or plan for Checkpoint 5.
- Constraint Satisfaction isn't explicitly listed in topics but can be implemented using Search techniques (covered by week 3).

## Coverage Rationale

This proposal selects topics that naturally map to distinct problems in the recipe domain, creating a cohesive system where each AI technique addresses a specific challenge.

**Propositional Logic** (Module 2) is essential for encoding dietary constraints as a knowledge base. Dietary restrictions are inherently logical: "if vegetarian then no meat" or "must avoid peanuts AND shellfish" translate directly to propositional formulas. This provides precise, verifiable filtering that simple keyword matching cannot achieve. The trade-off: while more complex than rule-based if-statements, propositional logic enables querying constraints systematically and ensures sound inference.

**Search** (Module 3) becomes non-trivial when ranking recipes by multiple criteria: ingredient overlap, preference weights, prep time, and dietary compatibility. Beam search explores optimal ingredient combinations, while information retrieval techniques score and rank candidates from large databases. The trade-off: exhaustive search is too slow for large datasets, but heuristic-based search balances quality and efficiency.

**Constraint Satisfaction** (Module 4) validates ingredient substitutions while maintaining dietary compatibility—a natural constraint satisfaction problem where substitutions must satisfy both ingredient availability and dietary rules. The trade-off: while not explicitly in the course topics, it uses Search techniques (covered by week 3) to find valid substitutions, making it feasible without additional topic coverage.

**Planning** (Module 6) sequences cooking steps optimally and explores ingredient combinations for recipe generation. This demonstrates planning algorithms in a concrete domain where step ordering matters and ingredient selection requires exploration. The trade-off: full automated recipe generation is ambitious, but planning-based step sequencing and ingredient combination is achievable and demonstrates the concept effectively.

**Machine Learning** (Module 5) enables personalized recommendations by learning from user preferences. Content-based filtering matches recipe features to preference weights, while supervised learning can improve recommendations over time. The trade-off: collaborative filtering would require user interaction data we don't have, so content-based filtering is more appropriate. This also allows the module to work with questionnaire-based preferences rather than requiring historical data.

**Data Processing** (Module 1) is foundational but necessary—real recipe datasets require cleaning, normalization, and knowledge representation. This module ensures subsequent modules work with reliable data.

**Trade-offs considered:**
- **Generation complexity:** Full neural recipe generation would require advanced ML not covered early enough. Planning-based generation with pattern learning from the database is more feasible and still demonstrates planning concepts.
- **Recommendation approach:** Chose content-based over collaborative filtering because we lack user interaction history. Content-based works with preference questionnaires and recipe features.
- **Constraint Satisfaction:** Not explicitly in topics, but implementable using Search techniques, making it a natural extension that doesn't require additional topic coverage.
- **Module ordering:** Placed Planning (Module 6) before ML (Module 5) to align with topic coverage, even though ML recommendations could enhance planning. This ensures feasibility while maintaining logical system flow.

The recipe domain provides concrete, testable problems for each topic, with clear success criteria (dietary compliance, ingredient matching, user satisfaction) that make evaluation straightforward.

Ideas for Datasets linked here (some ones I found):
- https://www.kaggle.com/datasets/wilmerarltstrmberg/recipe-dataset-over-2m
- https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews
- https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions