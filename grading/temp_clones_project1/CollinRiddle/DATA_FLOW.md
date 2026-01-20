# High-Level Data Flow

## System Overview: AI-Powered Trading Strategy System

```
                    ┌─────────────────────────────────────┐
                    │ SUPPORTING FUNCTIONS (Not Modules)  │
                    │ • Data Ingestion (API → CSV)        │
                    │ • Feature Engineering (Indicators)  │
                    │ Output: Market data with RSI, MACD, │
                    │         MA20, MA50, Volume          │
                    └─────────────────────────────────────┘
                                      ↓
                         [Historical Market Data]
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ MODULE 1: TRADING RULE KNOWLEDGE BASE                                       │
│ Topic: Propositional Logic                                                  │
│                                                                             │
│ • Represents trading rules as logical propositions (CNF)                    │
│ • Knowledge base: "IF (RSI < 30) AND (MA20 > MA50) THEN BUY"                │
│ • Uses forward chaining to infer buy/sell/hold from market state            │
│                                                                             │
│ Input: Current market indicators + rule set                                 │
│ Output: Entailed trading action (BUY/SELL/HOLD) with logical justification  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
              [Rules need optimal parameters—what thresholds work best?]
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ MODULE 2: STRATEGY PARAMETER SEARCH                                         │
│ Topic: Informed Search (A*, Beam Search)                                    │
│                                                                             │
│ • Searches parameter space for promising rule configurations                │
│ • A* with heuristic = quick backtest estimate of returns                    │
│ • Beam Search explores top-k candidates in parallel                         │
│                                                                             │
│ Input: Parameter ranges (RSI: 20-40, MA periods: 10-50, etc.)               │
│ Output: Top 10 candidate parameter sets ranked by heuristic score           │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
              [Good candidates found—now evolve them for better performance]
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ MODULE 3: STRATEGY EVOLUTION ENGINE                                         │
│ Topic: Advanced Search (Genetic Algorithms)                                 │
│                                                                             │
│ • Evolves populations of trading strategies over generations                │
│ • Chromosome = [RSI_buy, RSI_sell, MA_period, volume_threshold, ...]        │
│ • Crossover: Combine successful strategies                                  │
│ • Mutation: Introduce variation                                             │
│ • Selection: Keep top performers (fitness = backtested Sharpe ratio)        │
│                                                                             │
│ Input: Initial population from Module 2 + historical data for backtesting   │
│ Output: Evolved strategies with performance metrics (return, Sharpe, etc.)  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
              [Best strategies found—but which market conditions suit them?]
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ MODULE 4: MARKET REGIME CLASSIFIER                                          │
│ Topic: Supervised Learning (Logistic Regression / Classification)           │
│                                                                             │
│ • Classifies market conditions: "bull", "bear", or "sideways"               │
│ • Trained on labeled historical data                                        │
│ • Features: RSI, MACD, volatility, volume trend, price momentum             │
│ • Different strategies perform better in different regimes                  │
│                                                                             │
│ Input: Current market indicators + pre-trained classifier                   │
│ Output: Predicted regime + confidence score + recommended strategy          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
              [Know the regime and strategy—now how much capital to risk?]
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ MODULE 5: ADAPTIVE POSITION SIZING AGENT                                    │
│ Topic: Reinforcement Learning (Q-Learning, MDP)                             │
│                                                                             │
│ • Models trading as Markov Decision Process                                 │
│ • State: (market_regime, strategy_confidence, volatility_level)             │
│ • Action: position_size_percent (1%, 5%, 10%, 15%)                          │
│ • Reward: profit/loss from trade                                            │
│ • Learns optimal sizing policy through Q-learning                           │
│                                                                             │
│ Input: Market regime (M4) + strategy metrics (M3) + available capital       │
│ Output: Recommended position size + reasoning                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
                      ┌────────────────────────────┐
                      │ TRADE EXECUTION            │
                      │ (Not a module—user action) │
                      │                            │
                      │ Strategy: RSI < 28 & MA20  │
                      │ Regime: Bull market        │
                      │ Position: 12% ($1,200)     │
                      │ Action: BUY                │
                      └────────────────────────────┘
```

## Key Integration Points

1. **Module 1 → Module 2**: Logic rules define the STRUCTURE; Search finds the PARAMETERS
2. **Module 2 → Module 3**: Search provides initial population for genetic evolution
3. **Module 3 → Module 4**: Evolved strategies are tagged with which regimes they excel in
4. **Module 4 → Module 5**: Regime classification feeds into RL state representation
5. **All modules share**: Common data pipeline (indicators computed once, used everywhere)