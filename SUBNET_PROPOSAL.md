# AI Finance Oracle — Subnet Design Proposal

> **Bittensor Subnet Ideathon 2026**
> Team: AI Finance Oracle | Twitter: @AIFinanceOracle | Discord: aifinanceoracle

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Incentive & Mechanism Design](#2-incentive--mechanism-design)
3. [Miner Design](#3-miner-design)
4. [Validator Design](#4-validator-design)
5. [Business Logic & Market Rationale](#5-business-logic--market-rationale)
6. [Go-To-Market Strategy](#6-go-to-market-strategy)

---

## 1. Executive Summary

**AI Finance Oracle** is a Bittensor subnet that creates a competitive marketplace for financial predictive models. Miners submit and continuously improve financial forecasting models (e.g., asset price prediction, market sentiment analysis, risk assessment). Validators evaluate these models against real-time market data and historical ground truth. The best-performing models earn $TAO emissions, creating a permissionless, decentralized ecosystem that produces state-of-the-art financial intelligence — accessible to anyone.

**Digital Commodity Produced:** High-accuracy financial predictions and market analytics.

**Proof of Intelligence:** Every miner must demonstrate genuine financial forecasting capability by producing accurate predictions on validator-generated market challenges. There is no shortcut — the only way to earn rewards is to build better, more predictive models.

---

## 2. Incentive & Mechanism Design

### 2.1 Emission and Reward Logic

The subnet uses Bittensor's native emission system with the following distribution per tempo (~360 blocks, ~72 minutes):

| Recipient | Share | Description |
|-----------|-------|-------------|
| Subnet Owner | 18% | Funds ongoing development, API infrastructure, and security audits |
| Miners | 41% | Distributed proportionally to Yuma Consensus performance scores |
| Validators + Stakers | 41% | Proportional to stake and bond strength |

**Reward Flow:**

```
Block Emission ($TAO)
    └─> Subnet AMM (alpha token injection)
        └─> Tempo Distribution (every ~72 min)
            ├─> 18% → Subnet Owner
            ├─> 41% → Miners (via Yuma Consensus scores)
            └─> 41% → Validators & Stakers (via bond strength)
```

Miner emissions are determined by their **normalized weight** in the Yuma Consensus output. A miner with significantly lower Mean Absolute Error (MAE) in price predictions will earn proportionally more.

### 2.2 Incentive Alignment

**For Miners:**
- Higher predictive accuracy = higher weight from validators = more $TAO emissions.
- Multi-dimensional scoring (accuracy, timeliness, confidence calibration) ensures genuine optimization.
- Continuous model improvement is rewarded.

**For Validators:**
- Validators earn emissions proportional to their **bond strength**, which grows when their weights align with Yuma Consensus.
- Independent, honest evaluation builds stronger EMA bonds.

**For Stakers:**
- Staking $TAO directs emissions via Taoflow.
- Stakers earn a share of the 41% validator emissions.

### 2.3 Mechanisms to Discourage Low-Quality or Adversarial Behavior

| Threat | Defense Mechanism |
|--------|-------------------|
| **Miners submitting random outputs** | Multi-dimensional scoring against real market data; random outputs score near 0 |
| **Miners relying on delayed data** | Validators check timestamps and incorporate latency into scoring |
| **Colluding validators inflating a miner** | Yuma Consensus clipping — outlier weights are clipped to stake-weighted median |
| **Weight-copying validators** | Commit-reveal mechanism penalizes copiers with slower bond growth |
| **Model stagnation** | Anti-monopoly decay forces continuous improvement as market dynamics shift |
| **Sybil attacks** | Registration burn cost + immunity period |

### 2.4 Proof of Intelligence

This subnet qualifies as a genuine **Proof of Intelligence** because:

1. **Non-trivial computation:** Training and running complex financial time-series models requires significant computational resources.
2. **Verifiable output quality:** Real market data provides an undeniable ground truth for scoring predictions.
3. **Continuous improvement pressure:** Financial markets evolve; models must constantly adapt.
4. **Domain expertise required:** Financial modeling requires deep understanding of market microstructures, macroeconomics, and quantitative analysis.

### 2.5 High-Level Algorithm

```
EVERY TEMPO (~72 minutes):

  VALIDATOR LOOP:
    1. GENERATE synthetic/real market challenges:
       - Query specific assets (e.g., BTC/USD price in 2 hours)
       - Request sentiment analysis on recent news

    2. DISPATCH challenges to all registered miners:
       - Send FinanceSynapse with market parameters
       - Set strict timeout

    3. COLLECT miner responses:
       - Each response contains: prediction, confidence interval

    4. SCORE each miner response after time horizon passes:
       - accuracy_score = compute_error(prediction, actual_market_data)
       - Final score weighted by accuracy, latency, and consistency

    5. UPDATE moving averages
    6. SUBMIT weights to blockchain

  MINER LOOP:
    1. RECEIVE FinanceSynapse
    2. RUN quantitative models
    3. RETURN FinanceResponse
    4. CONTINUOUSLY retrain on live market streams
```

---

## 3. Miner Design

### 3.1 Miner Tasks

Miners operate financial predictive models. Their primary task is to **receive market queries from validators and return accurate forecasts and analytics**.

**Task Types:**

| Mechanism | Weight | Description |
|-----------|--------|-------------|
| **Price Prediction** | 60% | Forecast specific asset prices over defined time horizons (e.g., 1hr, 24hr) |
| **Sentiment Analysis** | 25% | Analyze market sentiment from news and social media streams |
| **Risk Scoring** | 15% | Evaluate volatility and downside risk for specific portfolios or assets |

### 3.2 Input → Output Format (Synapse Protocol)

```python
class FinanceSynapse(bt.Synapse):
    """Data contract between validators and miners."""

    # ── Immutable Inputs ──
    task_type: str                        # "price_prediction" | "sentiment" | "risk"
    target_asset: str                     # e.g., "BTC/USD", "AAPL"
    time_horizon_minutes: int             # Forecast horizon
    current_market_context: dict          # Recent OHLCV data, relevant news snippets

    # ── Mutable Outputs ──
    predicted_value: Optional[float] = None           # Predicted price or sentiment score
    confidence_interval: Optional[List[float]] = None # [lower_bound, upper_bound]
    reasoning: Optional[str] = None                   # Key factors driving the prediction
```

### 3.3 Performance Dimensions

| Dimension | Weight | Metric |
|-----------|--------|--------|
| **Directional Accuracy** | 40% | Did they predict the correct market direction? |
| **Magnitude Accuracy (MAE)** | 40% | How close was the quantitative prediction? |
| **Confidence Calibration** | 10% | Was the actual value within the predicted confidence interval? |
| **Response Latency** | 10% | Faster responses score higher |

### 3.4 Recommended Miner Strategy

1. Utilize state-of-the-art time-series models (e.g., LSTMs, Transformers, XGBoost).
2. Incorporate alternative data sources (on-chain metrics, order book imbalances, social sentiment).
3. Ensemble multiple models to handle different market regimes.

---

## 4. Validator Design

### 4.1 Scoring and Evaluation Methodology

Validators evaluate miners by comparing predictions against real-world, subsequently revealed market data using APIs from major exchanges and financial data providers (e.g., Binance, CCData, Alpha Vantage).

**Scoring Algorithm:**
Validators store initial predictions, wait for the specified `time_horizon_minutes`, fetch the actual market data, and score based on Mean Absolute Error (MAE) and directional accuracy.

### 4.2 Validator Incentive Alignment

Validators who independently and accurately score miners based on real market outcomes build consensus and grow their EMA bonds, yielding higher $TAO emissions. Relying on external, verifiable APIs ensures robust consensus among honest validators.

---

## 5. Business Logic & Market Rationale

### 5.1 The Problem

Financial data and predictive analytics are largely controlled by massive institutions and funds (e.g., Bloomberg, Renaissance Technologies). Retail investors and smaller funds lack access to tier-1 quantitative models. The current ecosystem is fragmented, centralized, and expensive.

### 5.2 Why This Use Case Is Well-Suited to a Bittensor Subnet

1. **Clear digital commodity:** Financial predictions are easily verifiable against public market data.
2. **High inherent value:** Accurate financial models are arguably the most highly monetizable digital commodities in the world.
3. **Decentralization benefit:** Crowdsourcing quantitative models from global talent outperforms centralized siloes (the "wisdom of the crowds" effect on steroids).

### 5.3 Path to Long-Term Adoption

- **Phase 1:** Crypto asset price predictions (highly verifiable, 24/7 markets).
- **Phase 2:** Traditional finance (equities, forex) integration.
- **Phase 3:** API monetization for DeFi protocols (e.g., dynamically adjusting lending rates or AMM fees based on subnet oracle data).

---

## 6. Go-To-Market Strategy

**Target Users:**
- DeFi Protocols (need robust, decentralized oracles for liquidations and risk engines).
- Retail Traders (subscribing to consensus signals).
- Hedge Funds (incorporating subnet consensus as an alternative data signal).

**Growth Channels:**
- Deep integration with existing Bittensor DeFi tools.
- Open-sourcing baseline quantitative models to rapidly bootstrap miner participation.
- Marketing the subnet's combined performance (Sharpe ratio, alpha generation) to the broader Web3 ecosystem.
