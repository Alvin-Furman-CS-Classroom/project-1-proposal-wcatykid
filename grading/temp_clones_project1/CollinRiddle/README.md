# Intelligent Trading Agent: Strategy Discovery Through Search and Adaptive Risk Management

## System Overview

This system helps users find profitable trading strategies for cryptocurrency and manages risk when executing trades. It uses five AI modules that work together, each solving a specific part of the problem.

**Phase 1: Finding Good Strategies**

First, the system needs rules for when to buy and sell. Module 1 represents these rules using propositional logic—simple "if-then" statements like "if price momentum is high AND volatility is low, then buy." Module 2 searches through thousands of possible rule variations to find ones that look promising, using A* and Beam Search to avoid testing every single combination. Module 3 takes the best candidates and improves them further using genetic algorithms—a technique that mimics evolution by combining successful strategies and introducing small changes over many generations.

**Phase 2: Trading Smartly**

Once good strategies exist, the system needs to apply them wisely. Module 4 uses supervised learning to classify whether the current market is trending up (bull), down (bear), or flat (sideways). Different strategies work better in different conditions, so this helps pick the right one. Module 5 uses reinforcement learning to decide how much money to invest in each trade. It learns through trial and error which position sizes lead to the best long-term results given current market conditions and strategy confidence.

Together, these modules form a complete pipeline: discover rules, optimize them, understand the market, and manage risk.

## Modules

### Module 1: Trading Rule Knowledge Base

**Topics:** Propositional Logic (Knowledge Bases, Inference, Forward Chaining)

**Input:** Current market indicators (RSI, MACD, MA20, MA50, Volume—see Glossary) and a set of trading rules expressed in propositional logic (CNF format).

**Output:** A trading action (BUY, SELL, or HOLD) along with the rules that fired and the logical inference chain showing how the conclusion was derived.

**Integration:** This module defines the *structure* of trading rules that Modules 2 and 3 will optimize. It receives optimized parameters from later modules and applies them to current market data. The logical framework ensures decisions are explainable—users can see exactly why the system recommended an action.

**Prerequisites:** Propositional Logic (Weeks 1-1.5): entailment, knowledge bases, inference methods, forward chaining, CNF representation.

---

### Module 2: Strategy Parameter Search

**Topics:** Informed Search (A*, Beam Search, Heuristics)

**Input:** Hard-coded parameter ranges defining the search space (e.g., "trigger buy when RSI falls between 20-40") and historical market data for evaluation.

**Output:** Top 10 candidate parameter configurations ranked by estimated **Sharpe ratio**—a metric that measures returns relative to risk (higher is better because it means more profit per unit of risk taken). Each candidate includes its parameters, score, and an explanation of why it was selected.

**Integration:** This module provides the starting population for Module 3's genetic algorithm. Rather than starting evolution from random strategies, we seed it with promising candidates discovered through search, making optimization faster and more effective.

**Prerequisites:** Informed Search (Weeks 1.5-3): A*, Beam Search, **heuristic design** (a heuristic is an educated guess that helps the algorithm prioritize which options to explore first, avoiding the need to test every possibility).

---

### Module 3: Strategy Evolution Engine

**Topics:** Advanced Search (Genetic Algorithms)

**Input:** Top 10 candidate strategies from Module 2, full historical market data, and GA parameters (population size: 20, generations: 100, mutation rate: 0.1).

**Output:** Top 5 evolved strategies with full performance metrics (Sharpe ratio, total return, win rate, max drawdown) and an evolution summary showing how strategies improved over generations.

**Integration:** This module refines search results into production-ready strategies. The top 5 are passed to Module 4, which matches them to market conditions. Unlike Module 2's quick estimates, fitness here uses full backtesting—simulating every trade across all historical data.

**Prerequisites:** Advanced Search (Weeks 4.5-5.5): Genetic algorithms, fitness functions, selection, crossover, mutation operators.

---

### Module 4: Market Regime Classifier

**Topics:** Supervised Learning (Logistic Regression, Classification)

**Input:** Current market indicators and a pre-trained classifier. Features include:
- RSI and MACD (defined in Module 1)
- **Volatility:** How much prices fluctuate—high volatility means bigger swings
- **Volume trend:** Whether trading activity is increasing or decreasing
- **Price momentum:** The rate and direction of recent price changes

**Output:** Predicted **market regime** (the overall market condition):
- **Bull:** Prices trending upward
- **Bear:** Prices trending downward
- **Sideways:** Prices moving flat, no clear trend

Also outputs confidence score (how certain the prediction is) and recommends which evolved strategy from Module 3 historically performed best in the predicted regime.

**Integration:** This module bridges strategy discovery and execution. Different strategies perform better in different conditions—a momentum strategy might excel in bull markets but fail in sideways markets. By classifying conditions, the system picks the right tool for the job.

**Prerequisites:** Supervised Learning (Weeks 7+): Logistic regression, classification, training/test splits. Training labels derived from historical price trends.

---

### Module 5: Adaptive Position Sizing Agent

**Topics:** Reinforcement Learning (MDP, Q-Learning, Policy, Value Functions)

**Input:** Market regime and confidence from Module 4, selected strategy's performance metrics from Module 3, current volatility level, and available capital (e.g., $10,000).

**Output:** 
- Recommended **position size:** What percentage of capital to invest (1%, 5%, 10%, or 15%)
- **Q-values:** Expected long-term returns for each possible position size (shows why one size was chosen over others)
- Reasoning explaining the decision
- Risk assessment (e.g., "Low risk state—aggressive position justified")

**Integration:** This is the final decision module. It determines how much capital to allocate given all upstream information. The **RL agent** learns through simulated historical trades. Unlike fixed rules, it adapts—learning to size positions aggressively when conditions favor the strategy and conservatively when uncertain.

**Prerequisites:** Reinforcement Learning (Weeks 7+): **MDP** (Markov Decision Process—a framework for modeling decisions where outcomes depend on current state and chosen action), Q-learning, state/action spaces, reward design.

---

## Feasibility Study

This timeline shows that each module's prerequisites align with the course schedule. All modules are scheduled after their prerequisite topics are taught.

| Module | Required Topic(s) | Topic Covered By | Checkpoint Target |
| ------ | ----------------- | ---------------- | ----------------- |
| 1: Trading Rule Knowledge Base | Propositional Logic | Week 1.5 | CP1 (Feb 11) |
| 2: Strategy Parameter Search | Informed Search (A*, Beam) | Week 3 | CP1 (Feb 11) |
| 3: Strategy Evolution Engine | Advanced Search (Genetic Algorithms) | Week 5.5 | CP2 (Feb 26) |
| 4: Market Regime Classifier | Supervised Learning | Week 7 | CP3 (Mar 19) |
| 5: Adaptive Position Sizing Agent | Reinforcement Learning | Week 7.5 | CP4 (Apr 2) |

## Coverage Rationale

The trading strategy problem naturally decomposes into five AI challenges, each addressed by a different technique:

1. **Propositional Logic** — Trading rules are inherently logical: "IF condition THEN action." Representing them formally enables explainable, traceable decisions.

2. **Informed Search** — Finding good strategy parameters is a search problem. With thousands of possible configurations, exhaustive testing is impractical. A* and Beam Search efficiently explore the space using heuristics.

3. **Genetic Algorithms** — Strategies can be improved through evolution. GA excels at optimization problems where the search space is large and the fitness function (backtested returns) is well-defined.

4. **Supervised Learning** — Market conditions vary, and different strategies suit different conditions. Classification learns to recognize regimes from historical patterns.

5. **Reinforcement Learning** — Position sizing is a sequential decision problem with delayed rewards. RL learns optimal risk management through experience, adapting to context rather than following fixed rules.

**Why this order?**

The modules follow both logical dependency (rules → parameters → evolution → classification → execution) and course schedule (early topics first). This ensures the system can be built incrementally, with each module tested before the next checkpoint.

---

## Glossary

**Market Indicators:**
- **RSI (Relative Strength Index):** A 0-100 score measuring if an asset is overbought (>70) or oversold (<30)
- **MACD (Moving Average Convergence Divergence):** A momentum indicator showing trend direction and strength
- **MA20/MA50 (Moving Averages):** Average prices over the last 20 or 50 days, used to identify trends
- **Volume:** How much of the asset was traded, indicating market activity
- **Volatility:** How much prices fluctuate—high volatility means bigger price swings

**Performance Metrics:**
- **Sharpe ratio:** Return per unit of risk (higher = better risk-adjusted performance)
- **Total return:** Overall profit percentage
- **Win rate:** Percentage of trades that were profitable
- **Max drawdown:** Largest peak-to-trough loss (measures worst-case scenario)
