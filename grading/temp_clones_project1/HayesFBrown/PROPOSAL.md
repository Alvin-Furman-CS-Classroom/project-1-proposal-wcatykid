# AI System Proposal

## System Title and Theme

**Title:** NFL Draft Class Evaluation and Talent Prediction System

**Theme:** Evaluating and predicting success of NFL draft prospects through AI-driven analysis of player statistics, performance data, and draft scenarios.

**Theme Rationale:** The NFL draft generates extensive data on prospects (college statistics, combine results, scouting reports) and requires complex decision-making under uncertainty. This domain naturally accommodates multiple AI techniques: search for finding optimal players, logic for rule-based evaluation, probabilistic reasoning for uncertainty in predictions, and learning from historical draft outcomes.

---

## System Overview

The NFL Draft Class Evaluation and Talent Prediction System integrates five AI modules to transform raw prospect data into strategic draft recommendations. The system processes draft prospects through a sequential pipeline: Module 1 (Search) filters players from a large database using uninformed and informed search algorithms, identifying prospects matching specific criteria. Module 2 (First-Order Logic) applies rule-based inference to categorize filtered players into draft value tiers (e.g., "First-Round Talent", "Day 2 Prospect") using scouting knowledge encoded as logical rules. Module 3 (Advanced Search) optimizes player rankings using hill climbing, simulated annealing, or genetic algorithms to maximize expected draft value across multiple factors. Module 4 (Game Theory) models the draft as a strategic game, determining optimal selection strategies and trade evaluations that account for competing teams' actions. Module 5 (Machine Learning) predicts NFL success probabilities by learning from historical draft outcomes, providing quantitative risk assessments.

Each module's output feeds directly into the next: search results enable logical categorization, categorized players inform optimized rankings, rankings support strategic game-theoretic analysis, and strategic assessments combine with historical data for success prediction. The integrated system produces actionable draft recommendations balancing immediate team needs, strategic value, and long-term success probability.

The NFL draft domain is ideal for exploring AI concepts because it presents real-world challenges requiring multiple techniques: large-scale data search, knowledge representation through logical rules, optimization under constraints, strategic reasoning under uncertainty, and learning from historical patterns. This theme demonstrates how diverse AI methods combine to solve complex, practical problems.

---

## Module Descriptions



### Module 1: Draft Prospect Search Engine

**Topics Covered:** Uninformed Search (BFS, DFS, Uniform Cost, Iterative Deepening), Informed Search (Heuristics, A*, IDA*, Beam Search)

**Description:** This module implements a search system to find draft prospects matching specific criteria from a large database of eligible players. The system supports uninformed and/or informed search algorithms to explore the player database efficiently.

The search space can be organized as a graph where nodes represent players and edges represent relationships (similar players, position groups, etc.), or as a tree where branches represent different filtering criteria. Heuristics guide informed search toward players most likely to match the query, reducing the number of nodes explored compared to uninformed methods.

**Input Specification:** A JSON object containing search criteria. The object includes optional fields for filtering players: position (string, e.g., "QB", "WR", "DE"), statistical thresholds (object with min/max values for stats like passing_yards, touchdowns, etc.), physical attributes (object with min/max for height_inches, weight_lbs, etc.), and search algorithm preference (string: "BFS", "DFS", "UniformCost", "IterativeDeepening", "AStar", "IDAStar", "BeamSearch"). Example: `{"position": "QB", "statistics": {"passing_yards": {"min": 3000}, "touchdowns": {"min": 25}}, "physical": {"height_inches": {"min": 72}}, "algorithm": "AStar"}`. The module also requires access to a player database (JSON array of player objects, each containing name, position, statistics, physical attributes, etc.).

**Output Specification:** A JSON object containing: (1) "matches" - an array of player objects that satisfy all criteria, where each player object includes name (string), position (string), statistics (object), physical attributes (object), and any other stored data; (2) "search_metadata" - an object with algorithm_used (string), nodes_explored (integer), execution_time_ms (float), and total_players_searched (integer). Example: `{"matches": [{"name": "John Doe", "position": "QB", "statistics": {...}, "physical": {...}}], "search_metadata": {"algorithm_used": "AStar", "nodes_explored": 150, "execution_time_ms": 23.5, "total_players_searched": 200}}`.

**Integration with System:** 
This module serves as the foundation for the system, providing filtered player sets that subsequent modules will analyze, evaluate, and rank. It demonstrates the trade-offs between exhaustive exploration (uninformed) and goal-directed search (informed) in a data-rich domain.

**Prerequisites:** Requires course content on Search algorithms (Uninformed Search: BFS, DFS, Uniform Cost, Iterative Deepening; Informed Search: Heuristics, A*, IDA*, Beam Search) covered in weeks 1.5-3 of the course. Also requires access to a dataset of NFL draft prospects containing player information (name, position, statistics, physical attributes) in JSON format.

---

### Module 2: Rule-Based Player Categorization

**Topics Covered:** First-Order Logic (Inference, Chaining)

**Description:** This module evaluates draft prospects against a knowledge base of First-Order Logic rules to classify players into draft value categories (e.g., "First-Round Talent", "Day 2 Prospect", "Late-Round Value", "Undrafted Free Agent").

The module uses forward chaining or backward chaining inference to derive conclusions about each player. The knowledge base contains FOL rules expressing scouting criteria, such as "∀x (Quarterback(x) ∧ PassingYards(x) > 3000 ∧ Touchdowns(x) > 25 → FirstRoundTalent(x))" or "∀x (Player(x) ∧ HasInjuryHistory(x) ∧ Age(x) > 23 → LowerDraftValue(x))". 

For each player from Module 1, the inference engine applies relevant rules to determine which categories the player belongs to. The system handles complex logical relationships, including conjunctions, disjunctions, and quantified statements across player attributes. 

This module transforms raw player data into structured evaluations that subsequent modules can use for ranking, comparison, and prediction. It demonstrates how logical reasoning can encode domain knowledge (scouting expertise) into automated evaluation systems.

**Input Specification:** A JSON object containing: (1) "players" - an array of player objects from Module 1 output (each with name, position, statistics, physical attributes); (2) "knowledge_base" - a JSON object representing FOL rules, where each rule has a unique identifier, a logical formula in a structured format (e.g., {"quantifier": "forall", "variable": "x", "antecedent": {...}, "consequent": {...}}), and a category assignment. Example: `{"players": [{"name": "John Doe", "position": "QB", "statistics": {"passing_yards": 3500, "touchdowns": 28}, ...}], "knowledge_base": {"rules": [{"id": "rule1", "formula": {...}, "category": "FirstRoundTalent"}]}}`.

**Output Specification:** A JSON object containing: (1) "categorized_players" - an array where each element is an object with player data, assigned categories (array of strings), and inference trace (array of rule IDs that fired); (2) "category_summary" - an object mapping each category to the count of players assigned to it. Example: `{"categorized_players": [{"player": {...}, "categories": ["FirstRoundTalent", "HighValueQB"], "inference_trace": ["rule1", "rule5"]}], "category_summary": {"FirstRoundTalent": 15, "Day2Prospect": 42, ...}}`.

**Integration with System:** This module receives filtered players from Module 1 and applies logical evaluation to categorize them. The categorized players with their draft value classifications feed into subsequent modules for ranking, probabilistic prediction (later modules), and final draft recommendations. The inference trace provides explainability for why players received certain categorizations.

**Prerequisites:** Requires course content on First-Order Logic, specifically Inference and Chaining (forward/backward chaining). Requires Module 1 output format (array of player objects matching search criteria).

---

### Module 3: Optimized Player Ranking

**Topics Covered:** Advanced Search (Optimization, Hill Climbing, Simulated Annealing, Genetic Algorithms)

**Description:** This module uses advanced search algorithms to optimize the ranking/ordering of draft prospects. The module treats player ranking as an optimization problem where the goal is to find an ordering that maximizes expected draft value, considering factors such as player categories from Module 2, positional value, statistical performance, and team needs.

The module explores the search space of possible player orderings using advanced search techniques. The search space consists of all permutations of players, with each state representing a different ranking. An objective function evaluates each ranking based on multiple criteria: how well high-value categories are prioritized, positional balance, statistical excellence, and alignment with typical draft strategies.

Advanced search algorithms (such as hill climbing, simulated annealing, or genetic algorithms) navigate this large search space efficiently. These methods can escape local optima and find globally better rankings than simple sorting approaches. The algorithm iteratively improves the ranking by exploring neighboring states (swapping players, reordering segments) or evolving a population of candidate rankings.

This module transforms categorized players into an optimized draft board that reflects both individual player value and strategic draft considerations. The optimized ranking serves as input for final draft recommendations and probabilistic success predictions in later modules.

**Input Specification:** A JSON object containing: (1) "categorized_players" - an array of player objects from Module 2 output, each with player data, assigned categories, and inference trace; (2) "optimization_parameters" - an object specifying weights for different factors (e.g., {"category_weight": 0.4, "positional_value_weight": 0.3, "statistical_weight": 0.2, "team_needs_weight": 0.1}), algorithm selection (string: "hill_climbing", "simulated_annealing", "genetic_algorithm"), and algorithm-specific parameters (e.g., temperature schedule for simulated annealing, population size for genetic algorithms). Example: `{"categorized_players": [...], "optimization_parameters": {"algorithm": "simulated_annealing", "weights": {...}, "temperature_initial": 100, "cooling_rate": 0.95}}`.

**Output Specification:** A JSON object containing: (1) "ranked_players" - an array of player objects in optimized order (rank 1 is first element), where each player object includes their original data, categories, and assigned rank (integer); (2) "optimization_metadata" - an object with algorithm_used (string), final_objective_value (float), iterations_performed (integer), convergence_info (object with details about search progress). Example: `{"ranked_players": [{"rank": 1, "player": {...}, "categories": [...]}, ...], "optimization_metadata": {"algorithm_used": "simulated_annealing", "final_objective_value": 87.3, "iterations_performed": 500, "convergence_info": {...}}}`.

**Integration with System:** This module receives categorized players from Module 2 and optimizes their ranking using advanced search. The optimized ranking provides a strategic ordering that balances multiple evaluation factors. This ranked list feeds into subsequent modules for probabilistic prediction of draft success and final draft recommendations, ensuring that the system's output reflects both logical categorization and optimized strategic ordering.

**Prerequisites:** Requires course content on Advanced Search algorithms (Optimization, Hill Climbing, Simulated Annealing, Genetic Algorithms). Requires Module 2 output format (categorized players with assigned categories and inference traces).

---

### Module 4: Game-Theoretic Draft Strategy

**Topics Covered:** Game Theory

**Description:** This module uses game theory to determine optimal drafting strategies by modeling the NFL draft as a strategic game with multiple competing teams. The module analyzes how a team's draft position, team needs, and anticipated actions of other teams interact to produce optimal selection strategies.

The draft is modeled as a sequential game where teams make selections based on their position in the draft order. The module constructs payoff matrices or game trees representing the strategic interactions. It considers factors such as: which players are likely to be available at each pick (based on other teams' predicted strategies), the value of different positions given team needs, and the opportunity cost of selecting one player over another.

Game theory concepts such as Nash equilibrium, optimal response strategies, and backward induction are applied to find strategies that maximize expected value given uncertainty about other teams' actions. The module can evaluate whether to select a player at the current position, trade up to secure a higher-value player, or trade down to accumulate more picks—each decision analyzed through the lens of strategic interaction.

This module transforms the optimized player ranking from Module 3 into actionable draft strategies that account for competitive dynamics. The strategic recommendations can be expanded to evaluate specific trade scenarios, comparing the expected value of trading draft positions against staying at the current pick.

**Input Specification:** A JSON object containing: (1) "ranked_players" - an array of player objects in optimized order from Module 3, each with rank, player data, and categories; (2) "draft_context" - an object with team_draft_position (integer, 1-32), team_needs (array of position strings, e.g., ["QB", "WR"]), number_of_picks (integer), and draft_round (integer); (3) "opponent_model" - an object representing predicted strategies of other teams, including likely_position_preferences (object mapping team positions to preferred player positions) and estimated_player_valuations (object mapping team positions to their likely draft board). Example: `{"ranked_players": [...], "draft_context": {"team_draft_position": 12, "team_needs": ["QB", "DE"], "number_of_picks": 7, "draft_round": 1}, "opponent_model": {...}}`.

**Output Specification:** A JSON object containing: (1) "optimal_strategy" - an object with recommended_action (string: "select", "trade_up", "trade_down"), target_player (player object if selecting), target_draft_position (integer if trading), expected_value (float), and strategic_rationale (string explaining the game-theoretic reasoning); (2) "trade_evaluations" - an array of objects evaluating potential trades, each with trade_type (string), target_position (integer), expected_value_difference (float), and strategic_analysis (string); (3) "game_analysis" - an object with nash_equilibrium_strategy (object), payoff_matrix_summary (object), and strategic_insights (array of strings). Example: `{"optimal_strategy": {"recommended_action": "select", "target_player": {...}, "expected_value": 8.5, "strategic_rationale": "Player X is available and provides highest value given opponent strategies"}, "trade_evaluations": [...], "game_analysis": {...}}`.

**Integration with System:** This module receives optimized player rankings from Module 3 and applies game-theoretic analysis to produce strategic draft recommendations. The optimal strategy accounts for competitive dynamics and uncertainty about other teams' actions. This strategic output can feed into final draft recommendations and success prediction modules, ensuring that the system's advice reflects both player evaluation and strategic game-theoretic thinking.

**Prerequisites:** Requires course content on Game Theory (Nash equilibrium, strategic games, payoff matrices, optimal strategies). Requires Module 3 output format (ranked players in optimized order with optimization metadata).

---

### Module 5: Player Success Prediction

**Topics Covered:** Machine Learning (Supervised Learning, Reinforcement Learning)

**Description:** This module uses machine learning algorithms to predict the likelihood of NFL success for draft prospects. The module learns from historical draft data, training on past prospects whose NFL outcomes are known, to identify patterns that correlate with professional success.

The learning system uses features derived from earlier modules: player statistics, physical attributes, categorical evaluations from Module 2, optimized rankings from Module 3, and strategic assessments from Module 4. These features are combined with historical data (college stats, combine results, draft position, NFL career outcomes) to train predictive models.

The module learns the relationship between prospect characteristics and NFL success metrics (such as career length, Pro Bowl appearances, statistical achievements, or overall performance ratings). The trained model can then predict success probabilities for new prospects in the current draft class. Predictions may take the form of classification (success/failure categories), regression (expected career statistics), or probability estimates (likelihood of achieving certain milestones).

This module provides data-driven predictions that complement the logical evaluations and strategic analyses from previous modules. The success predictions enable teams to make more informed decisions by quantifying the risk and expected value of selecting different prospects.

**Input Specification:** A JSON object containing: (1) "prospects" - an array of player objects from Module 4's optimal strategy output, each including player data, categories, rank, and strategic assessment; (2) "historical_training_data" - an array of historical draft records, each with prospect features (college stats, combine results, draft position) and outcome labels (NFL success metrics such as career_length_years, pro_bowls, career_stats, success_category); (3) "prediction_parameters" - an object specifying which success metrics to predict (array of strings, e.g., ["career_length", "pro_bowl_probability", "statistical_success"]), model_type (string, kept vague: "learning_algorithm"), and training_parameters (object with algorithm-specific settings). Example: `{"prospects": [...], "historical_training_data": [{"features": {...}, "outcomes": {"career_length_years": 8, "pro_bowls": 3}}], "prediction_parameters": {"metrics": ["career_length", "pro_bowl_probability"], "model_type": "learning_algorithm", "training_parameters": {...}}}`.

**Output Specification:** A JSON object containing: (1) "success_predictions" - an array where each element corresponds to a prospect and includes player data, predicted_success_metrics (object mapping metric names to predicted values or probabilities), confidence_intervals (object with upper/lower bounds for predictions), and feature_importance (object showing which features most influenced the prediction); (2) "model_metadata" - an object with model_type (string), training_accuracy (float), validation_metrics (object with performance scores), and prediction_timestamp (string). Example: `{"success_predictions": [{"player": {...}, "predicted_success_metrics": {"career_length_years": 7.2, "pro_bowl_probability": 0.35}, "confidence_intervals": {...}, "feature_importance": {...}}], "model_metadata": {"model_type": "learning_algorithm", "training_accuracy": 0.78, "validation_metrics": {...}}}`.

**Integration with System:** This module receives strategic draft recommendations from Module 4 and applies machine learning to predict NFL success probabilities. The success predictions provide quantitative risk assessments that complement the logical categorizations, optimized rankings, and strategic analyses from earlier modules. These predictions can inform final draft recommendations, helping teams balance immediate needs, strategic value, and long-term success probability when making draft decisions.

**Prerequisites:** Requires course content on Machine Learning (Supervised Learning and/or Reinforcement Learning algorithms, training procedures, evaluation metrics). Requires Module 4 output format (optimal strategy with target players and strategic analysis).

---

## Feasibility Study

_A timeline showing that each module's prerequisites align with the course schedule. Verify that you are not planning to implement content before it is taught._

**Course Topics and Schedule:**
- [Course Topics](https://csc-343.path.app/resources/course.topics.md)
- [Course Schedule](https://csc-343.path.app/resources/course.schedule.md)

| Module | Required Topic(s) | Topic Covered By | Checkpoint Due | Feasible? |
| ------ | ----------------- | ---------------- | -------------- | --------- |
| 1      |(Un)informed Search| Weeks 2.5-3      | Wed, Feb 11    | Yes       |
| 2      | First-Order Logic | Weeks 4-5.5      | Thurs, Feb 26  | Yes       |
| 3      | Advanced Search   | Weeks 5.5 - 6.5  | Thurs March 29 | Yes       |
| 4      | Game Theory       | Weeks 6.5 - 7    | Thurs April 2  | Yes       |
| 5      | Machine Learning  | Weeks 8 - 10     | Thurs April 16 | Yes       |


This schedule leaves several weeks free, in case progress is slower than expected.

## Coverage Rationale

The selected topics work together to build a comprehensive system for evaluating NFL draft prospects and formulating optimal drafting strategies. While the earlier search topics (Module 1) represent a foundational requirement that fits less naturally with the NFL draft theme, the later topics align strongly with the domain's core challenges.

**Theme Alignment:**
The NFL draft domain naturally accommodates the later topics. First-Order Logic excels at encoding scouting expertise into evaluative rules. Advanced Search optimization directly addresses the ranking problem central to draft preparation. Game Theory models the strategic interactions between competing teams—a core aspect of draft dynamics. Machine Learning leverages historical outcomes to predict prospect success, directly serving the system's predictive goals.

**Trade-offs Considered:**
The early search module (Module 1) is less thematically integrated, as tree/graph search through a player database is somewhat artificial compared to the natural applications of later topics. However, Search is a required topic and provides essential infrastructure for filtering prospects. Alternative early topics like Propositional Logic could have been used, but Search offers more immediate utility for handling large prospect datasets. The trade-off of including Search early is justified by its foundational role and requirement fulfillment, while the strong thematic fit of later modules (Logic, Advanced Search, Game Theory, Machine Learning) demonstrates how AI techniques naturally address real-world draft evaluation challenges.