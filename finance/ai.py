"""
AI Finance Oracle Prediction Engine
Simulates realistic miner AI models and validator scoring for finance subnet.
Each demo scenario has specialized miners and validators with unique analysis.
"""

import random
import hashlib
import time
from datetime import datetime


# ============================================================
# SPECIALIZED MINERS & VALIDATORS PER SCENARIO
# Each scenario has dedicated miners with unique names,
# specialties, and analysis patterns — just like a real subnet.
# ============================================================

SPECIALISTS = {
    "price_prediction": {
        "miners": [
            {"name": "AlphaQuant-v3",          "hotkey": "5FHL7kQr", "tier": "high", "specialty": "Deep Learning Price Model (Transformer)"},
            {"name": "FinanceNet-Transformer",  "hotkey": "5FSnT9xP", "tier": "high", "specialty": "Multi-modal Market Prediction"},
            {"name": "PricePredict-LSTM",       "hotkey": "5FSPl3mK", "tier": "mid",  "specialty": "LSTM-based Price Forecasting"},
            {"name": "SentimentAnalyzer-v2",    "hotkey": "5FFfV2nR", "tier": "mid",  "specialty": "Gradient Boosted Price Prediction"},
            {"name": "RiskGauge-XGB",           "hotkey": "5FLsR4pT", "tier": "mid",  "specialty": "XGBoost Market Model"},
            {"name": "BasicMA-v1",              "hotkey": "5FBe1qUm", "tier": "entry","specialty": "Moving Average Price Calculator"},
        ],
        "validators": [
            {"name": "MarketTruth-Oracle",      "hotkey": "5VgT1aXp", "specialty": "Exchange API price verification"},
            {"name": "OnChain-Verifier",        "hotkey": "5VaV2bYq", "specialty": "On-chain transaction flow verification"},
            {"name": "PriceFeed-Validator",     "hotkey": "5VcT3cZr", "specialty": "Multi-exchange price feed cross-check"},
            {"name": "OrderBook-Checker",       "hotkey": "5VpD4dAs", "specialty": "Order book depth analysis validation"},
        ],
        "check_labels": ["Price Within Tolerance", "Direction Verified", "Volume Correlation Confirmed"],
        "analyses": [
            "Transformer model analysis: Predicted price based on 48,320 historical candles on BTC/USD. Applied multi-head attention to order book imbalance (bid/ask ratio: 1.23), funding rate (+0.012%), and whale wallet movements (3 large transfers detected in 24h). Model captures post-halving supply shock dynamics with 92% directional accuracy on 2h timeframe.",
            "Multi-modal prediction: Combined Binance spot order book (top 20 levels, $14.2M bid wall at $67,800), perpetual futures open interest (+$340M 24h), and social sentiment index (Fear & Greed: 72). On-chain metrics: exchange netflow -2,340 BTC (accumulation signal). Confidence interval: +/-$850 at 90% CI.",
            "LSTM sequence model: Fed 180-day rolling window of 5-minute OHLCV data. Detected bullish divergence on RSI (14) with price making higher lows. Volume profile shows strong support at $66,500 (POC). Model captures 4h cycle: historically 68% of moves from this level resolve upward within 2h.",
            "Gradient boosted model: 1,247 features including exchange flows, options Greeks, funding rates, and macro indicators. Top feature importance: BTC exchange netflow (24%), options put/call ratio (18%), DXY correlation (12%). Ensemble of 800 trees with depth 10. Out-of-sample MAE: $420.",
            "XGBoost analysis: Aggregated predictions from 500 decision trees. Key splits: funding rate sign (positive -> bullish bias), 4h RSI level (currently 58, neutral-bullish), and BTC dominance trend (rising, +0.3% 24h). Feature engineering includes 14 technical indicators and 8 on-chain metrics.",
            "Moving average calculation: SMA(20) = $67,450, SMA(50) = $65,800, SMA(200) = $58,200 -- all aligned bullish (golden cross confirmed 12 days ago). Current price above all major MAs. EMA(12)/EMA(26) MACD crossover: bullish, histogram expanding. Basic RSI(14): 62 (bullish, not overbought).",
        ],
    },
    "sentiment_analysis": {
        "miners": [
            {"name": "SentimentPro-AI",        "hotkey": "5FRs7kQr", "tier": "high", "specialty": "Multi-source Sentiment Intelligence"},
            {"name": "NewsTrader-Pro",          "hotkey": "5FTtP9xP", "tier": "high", "specialty": "Real-time News Impact Prediction"},
            {"name": "SocialPulse-Monitor",     "hotkey": "5FGmL3mK", "tier": "mid",  "specialty": "Social Media Sentiment Tracking"},
            {"name": "WhaleWatch-v3",           "hotkey": "5FPwV2nR", "tier": "mid",  "specialty": "Whale Activity & Smart Money Detection"},
            {"name": "FearGreed-Analyzer",      "hotkey": "5FSrR4pT", "tier": "mid",  "specialty": "Market Psychology Analysis"},
            {"name": "BasicSentiment-v1",       "hotkey": "5FAb1qUm", "tier": "entry","specialty": "Public Feed Sentiment Aggregator"},
        ],
        "validators": [
            {"name": "NewsAPI-Verifier",        "hotkey": "5VnW1aXp", "specialty": "Reuters/Bloomberg news event cross-check"},
            {"name": "SocialMetrics-Oracle",    "hotkey": "5VpA2bYq", "specialty": "Social media volume & engagement validation"},
            {"name": "OnChainFlow-Checker",     "hotkey": "5VnC3cZr", "specialty": "On-chain flow correlation verification"},
        ],
        "check_labels": ["News Source Verified", "Sentiment Score Calibrated", "Volume Correlation Match"],
        "analyses": [
            "Multi-source analysis: Aggregated sentiment from 12,847 tweets (4h window), 342 Reddit posts, and 28 news articles. Detected strong bullish narrative shift following ETF inflow data ($287M daily net inflow). NLP confidence: 0.89. Key entities: BlackRock (positive, 34 mentions), SEC (neutral, 12 mentions), Fed (cautious, 8 mentions).",
            "News impact prediction: Reuters reports SEC chair positive comments on crypto regulation clarity. Historical analysis of similar regulatory events shows +3.2% average BTC move within 24h (n=14 events, 79% positive). Bloomberg terminal sentiment: Moderately Bullish. Combined news impact score: 0.74 (scale -1 to 1).",
            "Social media tracking: Twitter crypto sentiment index: 0.68 (bullish). Top trending: #Bitcoin, #BTCHalving, #CryptoETF. Influencer sentiment (top 50 by followers): 72% bullish, 18% neutral, 10% bearish. Reddit r/bitcoin: post volume +45% vs 7-day avg, comment sentiment: 0.61. Discord alpha channels: 3/5 major groups bullish.",
            "Whale activity detection: 4 wallets (>1000 BTC) moved total 8,420 BTC to cold storage in last 12h -- accumulation signal. Exchange whale ratio (Binance): 0.42 (below 0.50 = bullish). Top 10 addresses net position change: +2,100 BTC (7d). Smart money index: 0.78 (strong accumulation phase).",
            "Market psychology: Fear & Greed Index: 72 (Greed, but below Extreme Greed threshold of 80). Historically, readings 65-80 correlate with continued uptrend 64% of the time. Long/short ratio: 1.85 (moderately bullish but approaching crowded long territory). Liquidation heatmap shows $890M in short liquidations above $69,000.",
            "Public feed aggregation: CoinDesk reports positive ETF flows. CryptoQuant shows decreasing exchange reserves. LunarCrush social volume: HIGH (+62% vs avg). Combined sentiment flags: 4/5 sources indicate bullish bias. Simple aggregation score: 0.58.",
        ],
    },
    "risk_assessment": {
        "miners": [
            {"name": "RiskMatrix-AI",          "hotkey": "5FRo7kQr", "tier": "high", "specialty": "Multi-factor Risk Assessment (VaR/CVaR)"},
            {"name": "VolatilityPro",           "hotkey": "5FCmP9xP", "tier": "high", "specialty": "Implied Volatility & Options Risk"},
            {"name": "MacroRisk-Analyzer",      "hotkey": "5FTpL3mK", "tier": "mid",  "specialty": "Macroeconomic Risk Intelligence"},
            {"name": "CorrelationTracker-v2",   "hotkey": "5FGrV2nR", "tier": "mid",  "specialty": "Cross-asset Correlation Risk"},
            {"name": "DrawdownPredictor",       "hotkey": "5FSsR4pT", "tier": "mid",  "specialty": "Max Drawdown Prediction"},
            {"name": "BasicRisk-v1",            "hotkey": "5FDr1qUm", "tier": "entry","specialty": "Volatility-based Risk Calculator"},
        ],
        "validators": [
            {"name": "OptionsData-Verifier",    "hotkey": "5VfP1aXp", "specialty": "Deribit/CME options data verification"},
            {"name": "MacroEvent-Validator",    "hotkey": "5VsV2bYq", "specialty": "Fed/ECB event outcome verification"},
            {"name": "Volatility-Oracle",       "hotkey": "5VcB3cZr", "specialty": "Realized vs implied volatility cross-check"},
            {"name": "Liquidation-Checker",     "hotkey": "5VeC4dAs", "specialty": "Exchange liquidation data verification"},
        ],
        "check_labels": ["Risk Score Calibrated", "Volatility Data Verified", "Correlation Matrix Valid"],
        "analyses": [
            "VaR/CVaR analysis: 1-day 95% VaR: -4.2% ($2,870 per BTC). CVaR (Expected Shortfall): -6.8%. Monte Carlo simulation (10,000 paths) using GBM with stochastic volatility. Tail risk elevated: probability of >10% drawdown in 7 days = 12.4% (normal: 5-8%). Key risk driver: upcoming FOMC meeting uncertainty premium.",
            "Options risk: BTC 25-delta risk reversal: +2.1% (call premium, bullish skew). ATM implied volatility (7-day): 58% annualized (elevated vs 30-day realized vol of 42%). Put/call open interest ratio: 0.62 (more calls than puts). Max pain: $66,000. Large options expiry in 3 days ($4.2B notional) -- expect increased volatility.",
            "Macroeconomic risk: FOMC meeting in 48 hours -- market pricing 73% probability of rate hold (CME FedWatch). DXY at 104.2 (strong dollar = crypto headwind). 10Y Treasury yield: 4.35% (risk-off signal if rises above 4.50%). Historical BTC-DXY correlation (30d): -0.68. US CPI print next week adds additional uncertainty.",
            "Cross-asset correlation: BTC-SPX correlation (30d): 0.42 (moderate, rising). BTC-Gold correlation: 0.18 (weak). BTC-ETH correlation: 0.94 (high). Portfolio diversification benefit limited during risk-off events. Stress test: if SPX drops 3%, expected BTC impact: -4.8% (based on regression analysis of 2023-2024 data).",
            "Drawdown prediction: Current drawdown from ATH: -8.2%. Historical analysis of similar drawdown levels shows: 45% probability of further 5%+ decline, 35% probability of recovery within 7 days, 20% probability of consolidation. Fibonacci retracement levels: 38.2% at $64,200 (key support), 50% at $61,800. On-chain realized price: $42,500 (far below, strong long-term support).",
            "Volatility calculation: 30-day realized volatility: 42% annualized. 7-day realized: 55% (elevated). Bollinger Bands (20,2): price near upper band (overbought territory). ATR(14): $1,850 (daily). Basic risk score: HIGH (volatility above 50% threshold). Simple max loss estimate (2 std dev): -$3,700 per BTC.",
        ],
    },
}


# ── 3 PRE-BUILT DEMO SCENARIOS ──

DEMO_SCENARIOS = {
    "demo1": {
        "title": "BTC/USD Price Prediction -- 2 Hour Horizon",
        "subtitle": "Post-halving supply shock, ETF inflows strong, FOMC meeting approaching",
        "task_type": "price_prediction",
        "synapse": {
            "task_type": "price_prediction",
            "target_asset": "BTC/USD",
            "time_horizon_minutes": 120,
            "asset_class": "crypto",
            "exchange": "Binance",
            "conditions": {
                "volatility": "high",
                "trend": "bullish",
                "macro_event": "etf_inflow_surge",
            },
            "random_seed": 42001,
        },
        "ground_truth": {
            "actual_price": 69250.00,
            "actual_direction": "bullish",
            "price_change_pct": 2.1,
        },
    },
    "demo2": {
        "title": "ETH/USD Sentiment Analysis -- Market Narrative Shift",
        "subtitle": "Ethereum ETF approval rumors, Layer 2 adoption surge, DeFi TVL rising",
        "task_type": "sentiment_analysis",
        "synapse": {
            "task_type": "sentiment_analysis",
            "target_asset": "ETH/USD",
            "time_horizon_minutes": 360,
            "asset_class": "crypto",
            "exchange": "Binance",
            "conditions": {
                "volatility": "moderate",
                "trend": "bullish",
                "macro_event": "eth_etf_speculation",
            },
            "random_seed": 42002,
        },
        "ground_truth": {
            "actual_price": 3850.00,
            "actual_direction": "bullish",
            "price_change_pct": 4.8,
        },
    },
    "demo3": {
        "title": "Portfolio Risk Assessment -- Multi-asset Crypto Exposure",
        "subtitle": "FOMC rate decision imminent, DXY strengthening, options expiry approaching",
        "task_type": "risk_assessment",
        "synapse": {
            "task_type": "risk_assessment",
            "target_asset": "BTC/USD",
            "time_horizon_minutes": 1440,
            "asset_class": "crypto",
            "exchange": "Deribit",
            "conditions": {
                "volatility": "elevated",
                "trend": "uncertain",
                "macro_event": "fed_rate_decision",
            },
            "random_seed": 42003,
        },
        "ground_truth": {
            "actual_price": 66800.00,
            "actual_direction": "bearish",
            "price_change_pct": -3.2,
        },
    },
}


# ── Asset & condition data ──

ASSET_DATABASE = {
    "BTC/USD": {"base_price": 67800.0, "daily_vol": 0.035, "beta": 1.0},
    "ETH/USD": {"base_price": 3670.0, "daily_vol": 0.045, "beta": 1.3},
    "SOL/USD": {"base_price": 142.0, "daily_vol": 0.055, "beta": 1.6},
    "AAPL": {"base_price": 182.0, "daily_vol": 0.015, "beta": 1.1},
    "SPY": {"base_price": 502.0, "daily_vol": 0.010, "beta": 1.0},
    "XAU/USD": {"base_price": 2340.0, "daily_vol": 0.008, "beta": 0.3},
}

VOLATILITY_IMPACTS = {
    "high": {"price_swing": 0.04, "risk_increase": 0.25},
    "elevated": {"price_swing": 0.03, "risk_increase": 0.18},
    "moderate": {"price_swing": 0.02, "risk_increase": 0.10},
    "low": {"price_swing": 0.01, "risk_increase": 0.05},
    "normal": {"price_swing": 0.015, "risk_increase": 0.08},
}

TREND_IMPACTS = {
    "bullish": {"direction_bias": 0.6, "confidence_boost": 0.10},
    "bearish": {"direction_bias": -0.6, "confidence_boost": 0.10},
    "uncertain": {"direction_bias": 0.0, "confidence_boost": -0.05},
    "neutral": {"direction_bias": 0.0, "confidence_boost": 0.0},
}

MACRO_EVENT_IMPACTS = {
    "fed_rate_decision": {"vol_multiplier": 1.5, "risk_increase": 0.15},
    "etf_inflow_surge": {"vol_multiplier": 1.2, "risk_increase": 0.05},
    "eth_etf_speculation": {"vol_multiplier": 1.3, "risk_increase": 0.08},
    "cpi_release": {"vol_multiplier": 1.4, "risk_increase": 0.12},
    "none": {"vol_multiplier": 1.0, "risk_increase": 0.0},
    "normal": {"vol_multiplier": 1.0, "risk_increase": 0.0},
}


# ============================================================
# MAIN DEMO ENGINE
# ============================================================

def _generate_miner_responses(task_type, synapse, ground_truth, num_miners=6):
    """Generate specialized miner responses with unique analysis per miner."""
    spec = SPECIALISTS.get(task_type, SPECIALISTS["price_prediction"])
    pool = spec["miners"]
    num = min(num_miners, len(pool))
    selected = pool[:num]
    analyses = spec["analyses"]

    asset_key = synapse.get("target_asset", "BTC/USD")
    asset = ASSET_DATABASE.get(asset_key, {"base_price": 67800.0, "daily_vol": 0.035, "beta": 1.0})

    conditions = synapse.get("conditions") or {}
    volatility = conditions.get("volatility", "normal")
    trend = conditions.get("trend", "neutral")

    actual_price = ground_truth.get("actual_price", asset["base_price"])
    actual_direction = ground_truth.get("actual_direction", "bullish")

    miners = []
    for i, miner in enumerate(selected):
        rng = random.Random(synapse.get("random_seed", 42) + i * 7)

        tier = miner["tier"]
        if tier == "high":
            price_error_pct = rng.gauss(0, 0.008)
            score = round(rng.uniform(0.82, 0.97), 4)
            response_time = round(rng.uniform(0.3, 1.2), 2)
        elif tier == "mid":
            price_error_pct = rng.gauss(0, 0.018)
            score = round(rng.uniform(0.62, 0.82), 4)
            response_time = round(rng.uniform(0.8, 2.2), 2)
        else:
            price_error_pct = rng.gauss(0, 0.035)
            score = round(rng.uniform(0.40, 0.62), 4)
            response_time = round(rng.uniform(1.5, 3.5), 2)

        if i == 0:
            score = round(rng.uniform(0.93, 0.99), 4)
            response_time = round(rng.uniform(0.2, 0.6), 2)
            price_error_pct = rng.gauss(0, 0.003)

        predicted_price = round(actual_price * (1 + price_error_pct), 2)

        direction_correct = rng.random() < (0.85 if tier == "high" else 0.70 if tier == "mid" else 0.55)
        predicted_direction = actual_direction if direction_correct else ("bearish" if actual_direction == "bullish" else "bullish")

        sentiment = round(rng.uniform(0.3, 0.9) if predicted_direction == "bullish" else rng.uniform(-0.9, -0.3), 2)

        hk = miner["hotkey"]
        miners.append({
            "uid": i + 1,
            "hotkey": f"{hk}...{hashlib.md5(hk.encode()).hexdigest()[:6]}",
            "name": miner["name"],
            "tier": tier,
            "specialty": miner["specialty"],
            "predicted_price": predicted_price,
            "predicted_direction": predicted_direction,
            "sentiment_score": sentiment,
            "confidence": round(rng.uniform(0.6, 0.95) if tier != "entry" else rng.uniform(0.4, 0.65), 2),
            "score": score,
            "response_time_s": response_time,
            "analysis": analyses[i] if i < len(analyses) else analyses[-1],
            "rank": i + 1,
        })

    miners.sort(key=lambda m: m["score"], reverse=True)
    for i, m in enumerate(miners):
        m["rank"] = i + 1

    return miners


def _generate_validator_results(task_type, num_validators=3):
    """Generate specialized validator verification results."""
    spec = SPECIALISTS.get(task_type, SPECIALISTS["price_prediction"])
    pool = spec["validators"]
    num = min(num_validators, len(pool))
    selected = pool[:num]
    check_labels = spec["check_labels"]

    validators = []
    for j, val in enumerate(selected):
        rng = random.Random(42 + j * 13)
        hk = val["hotkey"]
        stake = round(rng.uniform(5000, 18000), 2)
        vtrust = round(rng.uniform(0.88, 0.99), 4)

        checks = {}
        checks_passed = 0
        for label in check_labels:
            passed = rng.random() < 0.85
            checks[label] = passed
            if passed:
                checks_passed += 1

        validators.append({
            "uid": j + 1,
            "hotkey": f"{hk}...{hashlib.md5(hk.encode()).hexdigest()[:6]}",
            "name": val["name"],
            "specialty": val["specialty"],
            "stake_tao": stake,
            "vtrust": vtrust,
            "checks_passed": checks_passed,
            "checks_total": len(check_labels),
            "check_details": checks,
            "consensus": "Approved" if checks_passed >= 2 else "Disputed",
        })

    return validators


def run_demo_scenario(scenario_key: str) -> dict:
    """Run one of the 3 pre-built demo scenarios with full miner/validator output."""
    scenario = DEMO_SCENARIOS.get(scenario_key)
    if not scenario:
        return {"error": f"Unknown scenario: {scenario_key}"}

    task_type = scenario["task_type"]
    synapse = scenario["synapse"]
    ground_truth = scenario["ground_truth"]

    miner_responses = _generate_miner_responses(task_type, synapse, ground_truth, num_miners=6)
    validator_results = _generate_validator_results(task_type, num_validators=3)

    total_tao = round(random.Random(42).uniform(0.08, 0.42), 4)

    total_score = sum(m["score"] for m in miner_responses)
    for m in miner_responses:
        m["tao_earned"] = round(total_tao * 0.41 * (m["score"] / total_score), 6) if total_score > 0 else 0

    return {
        "scenario": scenario_key,
        "title": scenario["title"],
        "subtitle": scenario["subtitle"],
        "task_type": task_type,
        "synapse": synapse,
        "ground_truth": ground_truth,
        "miner_responses": miner_responses,
        "miner_nodes_consulted": len(miner_responses),
        "validator_results": validator_results,
        "validator_nodes_consulted": len(validator_results),
        "tao_reward_pool": total_tao,
        "consensus_reached": all(v["consensus"] == "Approved" for v in validator_results),
        "block_number": random.randint(2_800_000, 3_200_000),
        "tempo": random.randint(7900, 8100),
        "timestamp": datetime.utcnow().isoformat(),
        "subnet_version": "1.0.0-beta",
    }


def get_demo_scenarios_list():
    """Return metadata for all 3 demo scenarios."""
    return [
        {
            "key": key,
            "title": s["title"],
            "subtitle": s["subtitle"],
            "task_type": s["task_type"],
            "target_asset": s["synapse"]["target_asset"],
            "time_horizon_minutes": s["synapse"]["time_horizon_minutes"],
            "exchange": s["synapse"]["exchange"],
            "conditions": s["synapse"]["conditions"],
        }
        for key, s in DEMO_SCENARIOS.items()
    ]


# ============================================================
# LEGACY FUNCTIONS (used by Swagger API endpoints)
# ============================================================

def run_miner_prediction(synapse_dict: dict, tier: str) -> dict:
    """Simulate a miner processing a finance challenge (for Swagger endpoints)."""
    rng = random.Random(synapse_dict.get("random_seed", int(time.time())))

    asset_key = synapse_dict.get("target_asset", "BTC/USD")
    asset = ASSET_DATABASE.get(asset_key, {"base_price": 67800.0, "daily_vol": 0.035, "beta": 1.0})

    conditions = synapse_dict.get("conditions") or {}
    volatility = conditions.get("volatility", "normal")
    trend = conditions.get("trend", "neutral")
    macro = conditions.get("macro_event", "none")

    vol_impact = VOLATILITY_IMPACTS.get(volatility, {"price_swing": 0.015, "risk_increase": 0.08})
    trend_impact = TREND_IMPACTS.get(trend, {"direction_bias": 0.0, "confidence_boost": 0.0})
    macro_impact = MACRO_EVENT_IMPACTS.get(macro, {"vol_multiplier": 1.0, "risk_increase": 0.0})

    if tier == "high":
        noise = rng.gauss(0, asset["daily_vol"] * 0.3)
        confidence = round(rng.uniform(0.82, 0.96), 2)
        latency = round(rng.uniform(200, 800), 0)
        data_sources = rng.randint(8, 15)
    elif tier == "mid":
        noise = rng.gauss(0, asset["daily_vol"] * 0.6)
        confidence = round(rng.uniform(0.65, 0.82), 2)
        latency = round(rng.uniform(500, 2000), 0)
        data_sources = rng.randint(4, 9)
    else:
        noise = rng.gauss(0, asset["daily_vol"] * 1.2)
        confidence = round(rng.uniform(0.40, 0.65), 2)
        latency = round(rng.uniform(1500, 4000), 0)
        data_sources = rng.randint(1, 5)

    direction_bias = trend_impact["direction_bias"]
    predicted_price = round(asset["base_price"] * (1 + noise + direction_bias * 0.01), 2)
    predicted_direction = "bullish" if predicted_price > asset["base_price"] else "bearish"

    sentiment = round(rng.uniform(0.2, 0.9) if predicted_direction == "bullish" else rng.uniform(-0.9, -0.2), 2)

    risk_factors = []
    if vol_impact["risk_increase"] > 0.1:
        risk_factors.append({"factor": volatility.replace("_", " ").title() + " Volatility", "probability": round(vol_impact["risk_increase"], 2), "impact_percent": round(-vol_impact["price_swing"] * 100, 1)})
    if macro_impact["risk_increase"] > 0:
        risk_factors.append({"factor": macro.replace("_", " ").title(), "probability": round(macro_impact["risk_increase"], 2), "impact_percent": round(-macro_impact["risk_increase"] * 10, 1)})

    return {
        "miner_uid": 0,
        "miner_hotkey": "",
        "predicted_price": predicted_price,
        "predicted_direction": predicted_direction,
        "sentiment_score": sentiment,
        "confidence": confidence,
        "risk_factors": risk_factors,
        "data_sources": data_sources,
        "response_time_ms": latency,
    }


def score_prediction(prediction: dict, ground_truth: dict) -> dict:
    """Score a miner prediction against ground truth (for Swagger endpoints)."""
    rng = random.Random(hash(str(prediction.get("miner_hotkey", ""))) % 2**31)

    actual_price = ground_truth.get("actual_price", 67800.0)
    predicted_price = prediction.get("predicted_price", 67800.0)
    actual_direction = ground_truth.get("actual_direction", "bullish")
    predicted_direction = prediction.get("predicted_direction", "bullish")

    magnitude_accuracy = round(max(0, 1.0 - abs(predicted_price - actual_price) / (actual_price * 0.05)), 4)
    directional_accuracy = 1.0 if predicted_direction == actual_direction else 0.0
    direction_bonus = predicted_direction == actual_direction and abs(ground_truth.get("price_change_pct", 0)) > 2.0

    confidence = prediction.get("confidence", 0.5)
    price_diff_pct = abs(predicted_price - actual_price) / actual_price
    confidence_calibration = round(max(0, 1.0 - abs(confidence - (1.0 - price_diff_pct * 10))), 4)

    latency_ms = prediction.get("response_time_ms", 1000)
    latency_score = round(max(0, 1.0 - latency_ms / 10000), 4)

    consistency = round(rng.uniform(0.65, 0.95), 4)

    final = 0.40 * directional_accuracy + 0.40 * magnitude_accuracy + 0.10 * confidence_calibration + 0.10 * latency_score
    if direction_bonus:
        final *= 1.5
    final = round(min(1.0, final), 4)

    return {
        "directional_accuracy": directional_accuracy,
        "magnitude_accuracy": magnitude_accuracy,
        "confidence_calibration": confidence_calibration,
        "latency_score": latency_score,
        "consistency": consistency,
        "direction_bonus": direction_bonus,
        "final_score": final,
    }


def get_prediction(query) -> dict:
    """Process a user-facing market query (for Swagger /predict endpoint)."""
    synapse_dict = {
        "target_asset": query.target_asset,
        "time_horizon_minutes": query.time_horizon_minutes,
        "asset_class": getattr(query, "asset_class", "crypto") or "crypto",
        "exchange": getattr(query, "exchange", "Binance") or "Binance",
        "conditions": {
            "volatility": "normal",
            "trend": "neutral",
            "macro_event": "none",
        },
    }

    result = run_miner_prediction(synapse_dict, "high")

    return {
        "target_asset": query.target_asset,
        "predicted_price": result["predicted_price"],
        "predicted_direction": result["predicted_direction"],
        "sentiment_score": result["sentiment_score"],
        "confidence": result["confidence"],
        "risk_factors": result.get("risk_factors", []),
        "data_sources": ["binance_orderbook", "on_chain_metrics", "news_sentiment", "technical_indicators"],
        "miners_consulted": 6,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
