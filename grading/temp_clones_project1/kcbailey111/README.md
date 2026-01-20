# AI-Powered Emotion-Based Trading Assistant

## System Overview

The AI-Powered Emotion-Based Trading Assistant is an intelligent system that leverages sentiment analysis and logical reasoning to make data-driven financial trading decisions. The system processes financial news and social media content to extract emotional signals (fear, greed, optimism) and market indicators, then applies risk management rules to generate trading recommendations.

The system operates through five integrated modules: a search module that retrieves relevant financial news articles for specific stocks, an NLP module that analyzes sentiment and extracts emotional indicators, a logic-based reasoning module that applies risk management rules, a decision module that validates and formats trading signals, and a reporting module that visualizes results. This theme is ideal for exploring AI concepts because it naturally combines multiple AI techniques—search algorithms for information retrieval, natural language processing for understanding human emotion in text, and propositional logic for encoding financial rules and constraints. The domain of finance provides a concrete, measurable application where AI decisions have clear outcomes, making it an excellent testbed for understanding how different AI approaches can work together in a real-world system.

## Modules

### Module 1: Financial News Search

**Topics:** Search (Uniform Cost, A*, Beam Search)

**Input:** A list of stock symbols (e.g., `["AAPL", "MSFT", "GOOGL"]`) and optional date range parameters. The module receives these as a JSON object: `{stocks: ["AAPL", "MSFT"], start_date: "2024-01-01", end_date: "2024-01-31"}`.

**Output:** A collection of relevant news articles in structured format. Each article is represented as: `{stock: "AAPL", title: "Article Title", content: "Full article text...", source: "Financial Times", date: "2024-01-15", relevance_score: 0.85}`. The output is a JSON array of article objects, sorted by relevance score.

**Integration:** This module serves as the data collection layer. Its output feeds directly into Module 2 (NLP/Sentiment Analysis), which processes the article content to extract emotional signals. The search module uses informed search algorithms (A* or beam search) to efficiently find the most relevant articles from financial news APIs/databases, prioritizing articles with high relevance to the specified stocks.

**Prerequisites:** Course content on search algorithms (A*, beam search, heuristics). No prior modules required as this is the entry point of the system.

---

### Module 2: Sentiment and Emotion Analysis

**Topics:** Natural Language Processing (NLP)

**Input:** News articles from Module 1 in the format: `[{stock: "AAPL", title: "...", content: "...", ...}, ...]`. The module processes the `title` and `content` fields of each article.

**Output:** Sentiment scores and emotional indicators for each article. Output format: `{stock: "AAPL", article_id: 1, fear: 0.3, greed: 0.7, optimism: 0.8, bullish: true, bearish: false, confidence: 0.85}`. The scores are normalized floats between 0.0 and 1.0, where higher values indicate stronger presence of that emotion. The `bullish`/`bearish` flags are boolean market indicators.

**Integration:** This module transforms raw text into structured emotional data that Module 3 (Logic/Reasoning) can process. The sentiment scores serve as inputs to propositional logic rules that determine trading actions. The module aggregates sentiment across multiple articles per stock to produce overall sentiment profiles that inform risk management decisions.

**Prerequisites:** Course content on NLP (text preprocessing, sentiment analysis, language models). Requires Module 1 output as input.

---

### Module 3: Risk Management Rule Engine

**Topics:** Propositional Logic (Knowledge Bases, Inference, CNF, Resolution)

**Input:** Aggregated sentiment data from Module 2 in format: `{stock: "AAPL", avg_fear: 0.4, avg_greed: 0.6, avg_optimism: 0.7, bullish_count: 5, bearish_count: 2}`. Also receives current portfolio state: `{cash_available: 10000, current_positions: {AAPL: 100}}` and risk parameters: `{max_position_size: 0.2, fear_threshold: 0.7, optimism_threshold: 0.6}`.

**Output:** Structured trading recommendations: `{action: "buy", stock: "AAPL", quantity: 10, reason: "high_optimism", confidence: 0.75}` or `{action: "sell", stock: "MSFT", quantity: 5, reason: "fear_threshold_exceeded", confidence: 0.85}`. The `reason` field encodes which logical rule fired (e.g., "high_optimism", "fear_threshold_exceeded", "risk_limit_reached").

**Integration:** This module applies propositional logic rules encoded as knowledge base clauses. Example rules: "IF avg_fear > fear_threshold AND current_position > 0 THEN sell", "IF avg_optimism > optimism_threshold AND cash_available > min_trade THEN buy". The logical inference engine evaluates these rules against the sentiment inputs to produce actionable trading signals that Module 4 validates and formats.

**Prerequisites:** Course content on Propositional Logic (entailment, knowledge bases, inference methods, CNF, resolution). Requires Module 2 output as input.

---

### Module 4: Trading Decision Validator

**Topics:** Knowledge Representation, Constraint Satisfaction

**Input:** Trading recommendations from Module 3: `{action: "buy", stock: "AAPL", quantity: 10, reason: "high_optimism", confidence: 0.75}`. Also receives validation constraints: `{max_trade_value: 5000, min_confidence: 0.6, trading_hours: true, account_balance: 10000}`.

**Output:** Validated and formatted trading orders: `{order_id: "ORD001", action: "buy", stock: "AAPL", quantity: 10, price_limit: null, timestamp: "2024-01-15T10:30:00", status: "approved"}` or `{order_id: "ORD002", action: "buy", stock: "MSFT", quantity: 0, status: "rejected", reason: "insufficient_funds"}`. The module ensures all orders meet financial and operational constraints before finalization.

**Integration:** This module applies constraint satisfaction techniques to validate trading recommendations against operational and financial constraints (sufficient funds, trading hours, position limits, confidence thresholds). It also employs knowledge representation to encode trading order structures and constraint relationships in a formal, machine-readable format. The validation process solves a constraint satisfaction problem: finding valid order configurations that satisfy all operational constraints. Validated orders are passed to Module 5 for reporting and visualization, completing the decision pipeline.

**Prerequisites:** Course content on Knowledge Representation (encoding information structures) and Constraint Satisfaction (constraint propagation, backtracking). Requires Module 3 output as input.

---

### Module 5: Trading Results Reporter

**Topics:** Explainable AI, Knowledge Representation

**Input:** Validated trading orders from Module 4: `[{order_id: "ORD001", action: "buy", stock: "AAPL", quantity: 10, status: "approved", ...}, ...]`. Also receives historical context: sentiment scores from Module 2, logic reasoning traces from Module 3 (including which rules fired), and order execution results.

**Output:** Explanatory reports that justify AI decisions. Text report format: `{summary: "Generated 3 buy orders, 1 sell order", orders: [...], decision_explanations: [{stock: "AAPL", action: "buy", triggered_rules: ["high_optimism"], sentiment_evidence: {...}}], risk_assessment: "moderate"}`. The module generates explanations showing which logic rules fired, what sentiment signals triggered decisions, and how inputs led to outputs. Output formats: JSON for programmatic access, structured text/HTML for human-readable explanations.

**Integration:** This module implements explainable AI principles by generating interpretable explanations of the system's decision-making process. It uses knowledge representation techniques to structure explanations (tracing logic rule applications, sentiment analysis results, and decision rationale) in a formal, queryable format. The module aggregates data from Modules 2, 3, and 4 to create comprehensive reports that explain why trading decisions were made, what sentiment signals triggered them, and what the expected outcomes are. This completes the feedback loop, allowing users to understand and refine the system's decision-making process.

**Prerequisites:** Course content on Explainable AI (interpretability, decision transparency) and Knowledge Representation (structured information presentation). Requires outputs from Modules 2, 3, and 4.

---


## Feasibility Study

_A timeline showing that each module's prerequisites align with the course schedule. Verify that you are not planning to implement content before it is taught._

**Note: Modules are ordered by dependency relationships (1→2→3→4→5), not by when topics are taught in the course.**

| Module | Required Topic(s) | Topic Covered By | Development Time | Checkpoint Due |
| ------ | ----------------- | ---------------- | ---------------- | -------------- |
| 1      | Search (A*, Beam Search) | Topic 2 (1.5 weeks, after Propositional Logic) | 2-3 weeks | Checkpoint 1 (Feb 11) |
| 2      | NLP (Sentiment Analysis) | Topic 5 (1.5 weeks, shared with Games) | 2-3 weeks | Checkpoint 2 (Feb 26) |
| 3      | Propositional Logic (Knowledge Bases, Inference) | Topic 1 (1.5 weeks, first topic) | 2-3 weeks | Checkpoint 3 (March 19) |
| 4      | Knowledge Representation, Constraint Satisfaction | Knowledge Bases from Topic 1, First-Order Logic (Topic 3, 1.5 weeks) | 2-3 weeks | Checkpoint 4 (April 2) |
| 5      | Explainable AI, Knowledge Representation | SHAP from Topic 8 (Supervised Learning section), Knowledge Representation from Topics 1 & 3 | 2-3 weeks | Checkpoint 5 (April 16) |

## Coverage Rationale

The selected topics—Search, NLP, Propositional Logic, Knowledge Representation, Constraint Satisfaction, and Explainable AI—naturally align with the emotion-based trading domain. Search algorithms are essential for efficiently retrieving relevant financial news from large databases, making A* and beam search ideal for prioritizing articles by relevance. NLP directly addresses the core challenge of extracting emotional signals (fear, greed, optimism) from unstructured text, which is fundamental to the system's purpose. Propositional Logic provides a rigorous framework for encoding risk management rules and trading constraints, enabling transparent and verifiable decision-making.

Knowledge Representation and Constraint Satisfaction are central to Module 4: the validator represents trading constraints as formal knowledge structures and solves constraint satisfaction problems (checking if trading recommendations satisfy all operational constraints simultaneously). Explainable AI is essential for Module 5: in financial applications, users must understand why the AI made specific decisions, requiring techniques to trace logic rule applications and explain decision rationale.

The integration of these topics creates a cohesive pipeline: search finds information, NLP interprets human emotion, logic applies structured reasoning, constraint satisfaction ensures validity, and explainable AI provides transparency. This combination demonstrates how different AI paradigms can complement each other in a real-world application. Trade-offs considered: Machine Learning could predict sentiment more accurately but would reduce interpretability; Reinforcement Learning could optimize trading strategies but requires more complex state spaces. The chosen approach prioritizes transparency and rule-based reasoning, which is critical in financial applications where decision explanations matter. The system balances sophistication (non-trivial search, advanced NLP) with clarity (explicit logical rules, interpretable explanations), making it both technically interesting and practically applicable.
