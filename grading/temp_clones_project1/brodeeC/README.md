# Atmospheric Conditions Advisor

## System Overview

The Atmospheric Conditions Advisor helps users make informed decisions about outdoor activities—hiking, photography, stargazing, driving, and event planning—by predicting how weather conditions will affect visual appearance and ground safety. Unlike traditional weather apps focused on temperature and precipitation, this system emphasizes atmospheric aesthetics (sunset quality, sky clarity, visibility) and practical ground conditions (wetness, snow cover, safety).

The system comprises six integrated modules: weather data acquisition from APIs, visual quality prediction for daytime atmospheric effects, stargazing quality assessment for night sky conditions, ground condition analysis using logical rules, activity optimization using beam search algorithms, and a recommendation engine that synthesizes all predictions into actionable advice. Each module operates independently but contributes to a cohesive decision-support system.

This theme naturally engages multiple AI techniques: machine learning for visual quality prediction, probabilistic reasoning for handling forecast uncertainty, propositional logic for safety rule evaluation, search algorithms for finding optimal time windows, and first-order logic for knowledge representation and reasoning in recommendation synthesis. The system addresses real-world uncertainty in weather forecasting while providing concrete, testable outputs that users can verify against actual conditions.

## Modules

### Module 1: Weather Data Acquisition

**Topics:** Data Processing (foundational)

**Input:** Location coordinates (latitude, longitude) or place name, time window (start_datetime, end_datetime), optional parameter list specifying desired weather fields.

**Output:** Structured weather data in CSV or JSON format containing: timestamp, temperature (°C), cloud_cover_pct (0-100), humidity_pct (0-100), precipitation_mm, wind_speed_kmh, visibility_km, pressure_hpa, dew_point (°C), and moon phase/position data for nighttime predictions.

**Integration:** This module serves as the data foundation for all other modules. Modules 2, 3, and 4 consume its cleaned, structured output to perform their respective predictions and analyses. The module fetches data from weather APIs (e.g., OpenWeatherMap, NOAA) and standardizes formats for downstream processing.

**Prerequisites:** Basic Python programming, API integration concepts, data structures (dictionaries, lists). No prior course topics required—this is the foundational data collection module.

---

### Module 2: Visual Quality Prediction

**Topics:** Machine Learning, Probabilistic Reasoning

**Input:** Weather data from Module 1, time_of_day (datetime), location coordinates, sun position (azimuth angle, elevation angle) calculated for the specified time.

**Output:** Dictionary/JSON containing: sunset_quality_score (float 0.0-1.0), sunset_category (string: "Poor"/"Fair"/"Good"/"Great"), sunrise_quality_score (float 0.0-1.0), visibility_probability (float 0.0-1.0), sky_color_prediction (string describing expected colors), confidence (float 0.0-1.0 indicating prediction certainty).

**Integration:** This module's predictions feed into Module 5 (Activity Optimization Search) to help identify optimal windows for photography and daytime activities. The visual quality scores are weighted factors in the search algorithm's evaluation function. Module 6 (Recommendation Engine) uses these predictions to explain why certain times are recommended.

**Prerequisites:** Module 1 (Weather Data Acquisition) must be complete. Requires course coverage of machine learning fundamentals (regression, classification) and probabilistic reasoning concepts for handling forecast uncertainty. This module is scheduled for Checkpoint 4 to align with when ML topics are covered in the course.

---

### Module 3: Stargazing Quality Prediction

**Topics:** Machine Learning, Probabilistic Reasoning

**Input:** Weather data from Module 1 (specifically nighttime hours), moon_phase (0-1, where 0=new moon, 1=full moon), moon_position (azimuth, elevation), light_pollution_level (numeric scale), time_of_night (datetime).

**Output:** Dictionary/JSON containing: stargazing_score (float 0.0-1.0), milky_way_visible (boolean), cloud_cover_night (float 0.0-1.0), seeing_conditions (string: "Poor"/"Fair"/"Good"/"Excellent"), best_time_window (dictionary with "start" and "end" datetime fields indicating optimal stargazing period).

**Integration:** Similar to Module 2, this module's outputs are consumed by Module 5 (Activity Optimization Search) to identify optimal stargazing windows. The stargazing_score and best_time_window are key inputs for the search algorithm when the user's activity preference is stargazing. Module 6 uses these predictions in its recommendations.

**Prerequisites:** Module 1 (Weather Data Acquisition) must be complete. Requires course coverage of machine learning and probabilistic reasoning, similar to Module 2. Can be developed in parallel with Module 2. This module is scheduled for Checkpoint 4 to align with when ML topics are covered in the course.

---

### Module 4: Ground Condition Analysis

**Topics:** Propositional Logic

**Input:** Weather data from Module 1, recent_precipitation_history (list of precipitation amounts for last 24-48 hours), terrain_type (string: "trail"/"road"/"field"/etc.), user_activity_preference (string: "hiking"/"driving"/"photography"/"event_planning").

**Output:** Dictionary/JSON containing: surface_condition (string: "wet"/"dry"/"snow"/"ice"), hiking_safety (string: "safe"/"moderate"/"unsafe"), driving_conditions (string: "good"/"moderate"/"poor"), visibility_status (string: "clear"/"hazy"/"foggy"), activity_specific_risk (float 0.0-1.0).

**Integration:** This module's ground condition assessments are critical inputs to Module 5 (Activity Optimization Search), especially for hiking and driving activities where safety depends on surface conditions. The logical rules evaluate combinations of weather factors (e.g., "IF precipitation_recent > threshold AND temperature < freezing THEN surface_condition = ice"). Module 6 uses these outputs to provide safety warnings in recommendations.

**Prerequisites:** Module 1 (Weather Data Acquisition) must be complete. Requires course coverage of propositional logic, knowledge representation, and inference methods (chaining, rule evaluation).

---

### Module 5: Activity Optimization Search

**Topics:** Search (Beam Search)

**Input:** Activity_type (string: "hiking"/"photography"/"stargazing"/"driving"/"event_planning"), time_constraints (earliest_start datetime, latest_end datetime, duration_minutes), location coordinates, visual_predictions from Module 2, stargazing_predictions from Module 3, ground_conditions from Module 4, user_preferences (dictionary with weights for visual_quality, safety, comfort, etc.).

**Output:** List of top-k time window recommendations (beam width = k, typically 3-5): each element is a dictionary with start_time (datetime), end_time (datetime), activity (string), quality_score (float 0.0-1.0), reasoning (string explaining why this window was selected), warnings (list of strings for any safety or quality concerns).

**Integration:** This module is the core decision-making component, designed to consume outputs from Modules 2, 3, and 4. Initially (at Checkpoint 2 or 3), it can work with Module 4's ground conditions and simplified heuristics for visual/stargazing quality. Once Modules 2 and 3 are complete (Checkpoint 4), it will integrate their predictions for more accurate optimization. It uses beam search to explore the space of possible time windows, evaluating each candidate using a heuristic function that combines visual quality scores, ground safety, and user preferences. The ranked list of recommendations feeds directly into Module 6 (Recommendation Engine) for final presentation to the user.

**Prerequisites:** Modules 1 and 4 must be complete. Modules 2 and 3 enhance this module but are not strictly required for initial implementation. Requires course coverage of search algorithms, specifically beam search, heuristic functions, and state space search. This is a required topic (Search) for the proposal.

---

### Module 6: Recommendation Engine

**Topics:** First-Order Logic

**Input:** Search results from Module 5 (ranked list of time windows), all module outputs (visual predictions from Module 2, stargazing predictions from Module 3, ground conditions from Module 4), user_context (current_time datetime, location coordinates, preferences dictionary).

**Output:** Structured advice dictionary/JSON containing: primary_recommendation (dictionary with "time" string, "activity" string, "advice" string), alternatives (list of dictionaries with "time", "activity", "why" fields), warnings (list of strings for safety or quality concerns), summary (string providing overall guidance).

**Integration:** This module synthesizes all previous module outputs into user-friendly recommendations. It takes the search results from Module 5 and formats them with explanations drawn from Modules 2, 3, and 4. Initially (if due at Checkpoint 3), it can work with Modules 1, 4, and 5, using simplified reasoning. Once Modules 2 and 3 are complete (Checkpoint 4), it will integrate their predictions for richer recommendations. The module acts as the system's interface layer, translating technical predictions into actionable advice. Future extensions could add a feedback loop where user ratings improve Modules 2 and 3's predictions.

**Prerequisites:** Modules 1, 4, and 5 must be complete. Modules 2 and 3 enhance this module's capabilities but are not strictly required for initial implementation if scheduled for Checkpoint 3. Requires course coverage of first-order logic, knowledge representation, and inference methods for reasoning about recommendations and synthesizing information from multiple sources. This module integrates all components into a cohesive recommendation system.

---

## Feasibility Study

_A timeline showing that each module's prerequisites align with the course schedule. Verified against the actual course schedule at https://csc-343.path.app/resources/course.schedule.md._

| Module | Required Topic(s) | Topic Covered By | Checkpoint Due |
| ------ | ----------------- | ---------------- | -------------- |
| 1      | Data Processing, API Integration | Week 1 (foundational) | Checkpoint 1 (Feb 11) |
| 4      | Propositional Logic | Weeks 1-1.5 | Checkpoint 2 (Feb 26) |
| 5      | Search (Beam Search) | Weeks 1.5-3 | Checkpoint 2 (Feb 26) or Checkpoint 3 (March 19) |
| 2      | Machine Learning, Probabilistic Reasoning | Weeks 8.5-10+ | Checkpoint 4 (April 2) |
| 3      | Machine Learning, Probabilistic Reasoning | Weeks 8.5-10+ | Checkpoint 4 (April 2) |
| 6      | First-Order Logic / Planning | Weeks 3-4.5 | Checkpoint 3 (March 19) or Checkpoint 4 (April 2) |

**Timeline Rationale:** Module 1 (data acquisition) can begin immediately and is due at Checkpoint 1. Modules 4 (Propositional Logic) and 5 (Search) use topics covered in weeks 1-3, making them feasible for Checkpoint 2. However, Modules 2 and 3 require Machine Learning, which is not covered until weeks 8.5-10, so they must be scheduled for Checkpoint 4 or later. Module 6 can use First-Order Logic (weeks 3-4.5) for knowledge representation and reasoning, or planning concepts if covered, making it feasible for Checkpoint 3 or 4. This sequencing ensures no module requires content not yet taught at its checkpoint.

## Coverage Rationale

This proposal covers five core AI topics: **Search** (required), **Machine Learning**, **Probabilistic Reasoning**, **Propositional Logic**, and **First-Order Logic**. Each topic fits naturally into the weather-based decision-making theme.

**Search** (Module 5) is essential for finding optimal time windows across multiple constraints—visual quality, ground safety, and user preferences. Beam search efficiently explores the space of possible activity times while maintaining computational feasibility. This satisfies the required topic coverage.

**Machine Learning** (Modules 2 and 3) enables prediction of visual quality metrics from weather data. Historical weather patterns and user-observable outcomes (sunset quality, stargazing conditions) create natural training data. Regression models can learn relationships between cloud cover, humidity, and visual appeal.

**Probabilistic Reasoning** (Modules 2 and 3) handles forecast uncertainty. Weather predictions are inherently probabilistic, and the system must reason about likelihoods (e.g., "70% chance of clear skies") to make robust recommendations.

**Propositional Logic** (Module 4) provides a clear, testable framework for safety rules. Ground condition evaluation requires logical combinations: "IF precipitation > threshold AND temperature < freezing THEN unsafe." This makes the module's reasoning transparent and verifiable.

**First-Order Logic** (Module 6) provides the knowledge representation framework for synthesizing multiple predictions into coherent recommendations. The module uses quantified statements and inference to reason about relationships between weather conditions, user preferences, and activity suitability, producing actionable advice.

**Trade-offs considered:** We chose not to include game theory (weather doesn't involve strategic opponents) or reinforcement learning (though a feedback module could use RL in future work). The selected topics provide comprehensive coverage while maintaining focus on the core decision-making problem.
