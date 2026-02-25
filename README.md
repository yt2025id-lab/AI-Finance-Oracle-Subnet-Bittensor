# AI Finance Oracle Subnet

**Subnet #7 — Bittensor Ideathon**

A decentralized financial intelligence oracle on Bittensor. Miners compete to build the most accurate quantitative models for price prediction, sentiment analysis, and risk assessment. Validators verify predictions against real market data from major exchanges. Rewards ($TAO) are distributed via Yuma Consensus.

## Quick Start (For Judges)

```bash
# 1. Clone & enter directory
git clone https://github.com/yt2025id-lab/bittensor-finance-oracle.git
cd bittensor-finance-oracle

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload --port 8000

# 4. Open in browser
open http://localhost:8000
```

### What You'll See

- **Interactive Web UI** at `http://localhost:8000` — click any of the 3 demo scenarios
- **Swagger API Docs** at `http://localhost:8000/docs` — test all endpoints interactively
- **ReDoc** at `http://localhost:8000/redoc` — clean API reference

### Demo Scenarios

| # | Scenario | Task Type |
|---|----------|-----------|
| 1 | BTC/USD price prediction — 2h horizon, post-halving | Price Prediction |
| 2 | ETH/USD sentiment — ETF rumors & narrative shift | Sentiment Analysis |
| 3 | Portfolio risk — FOMC & options expiry impact | Risk Assessment |

Each demo broadcasts a financial challenge to 6 simulated miners, scores their predictions through 3-4 validators, and distributes TAO rewards via Yuma Consensus.

## Features

- 6 specialized financial AI miners (QuantFlow, AlphaNet, DeepSentiment, etc.)
- 3-4 validators with market data verification pipelines
- Price prediction, directional analysis, sentiment scoring
- Real-time scoring: directional accuracy, magnitude accuracy, calibration, latency
- TAO reward distribution via Yuma Consensus
- Full miner/validator CRUD, leaderboard, and network status APIs

## Folder Structure

```
main.py                  # FastAPI entry point
finance/
  __init__.py
  ai.py                  # AI prediction engine (3 demo scenarios, 6 miners)
  db.py                  # In-memory DB (miners, validators, challenges)
  models.py              # Pydantic data models
  routes.py              # 20+ API endpoints
static/
  index.html             # Interactive demo UI
  app.js                 # Frontend logic
  style.css              # Dark theme styling
overview/overview.md     # Full technical documentation
pitchdeck/               # Pitch deck materials
SUBNET_PROPOSAL.md       # Detailed subnet design proposal
```

## Scoring Formula

```
final_score = (0.40 × directional_accuracy + 0.40 × magnitude_accuracy
             + 0.10 × confidence_calibration + 0.10 × latency)
             × 1.5 if correct direction in volatile market
```

## Subnet Parameters

- **Subnet ID:** 7 | **Tempo:** 360 blocks (~72 min) | **Max UIDs:** 256
- **Emission Split:** Owner 18% | Miners 41% | Validators+Stakers 41%

## Miner Tasks

| Task | Weight | Description |
|------|--------|-------------|
| Price Prediction | 60% | Forecast asset prices over 1h, 2h, 24h horizons |
| Sentiment Analysis | 25% | Market sentiment from news, social media, on-chain data |
| Risk Assessment | 15% | Volatility, drawdown risk, portfolio exposure |

## License

MIT

## Documentation

- [`SUBNET_PROPOSAL.md`](SUBNET_PROPOSAL.md) — Full technical subnet design proposal
- [`overview/overview.md`](overview/overview.md) — Problem/solution, architecture, mechanism design
- [`pitchdeck/`](pitchdeck/) — Pitch deck and demo video script
