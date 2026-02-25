from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from finance.routes import router as finance_router

app = FastAPI(
    title="AI Finance Oracle Subnet",
    description="""
## Decentralized Financial Intelligence — Powered by Bittensor & Yuma Consensus

**AI Finance Oracle** is a Bittensor subnet that creates a decentralized marketplace for financial prediction models.

### How It Works

- **Miners** compete to build AI models that accurately predict asset prices, market sentiment, and portfolio risk
- **Validators** verify predictions against actual market outcomes using exchange APIs and on-chain data
- **Rewards** ($TAO) are distributed based on prediction accuracy via Yuma Consensus

### Miner Tasks

| Task | Weight | Description |
|------|--------|-------------|
| Price Prediction | 60% | Forecast asset prices over defined time horizons (1h, 2h, 24h) |
| Sentiment Analysis | 25% | Analyze market sentiment from news, social media, on-chain data |
| Risk Assessment | 15% | Evaluate volatility, drawdown risk, and portfolio exposure |

### Scoring Formula

```
final_score = (0.40 x directional_accuracy + 0.40 x magnitude_accuracy
             + 0.10 x confidence_calibration + 0.10 x latency)
             x 1.5 if correct direction in volatile market
```

### Subnet Parameters
- **Subnet ID:** 7 | **Tempo:** 360 blocks (~72 min) | **Max UIDs:** 256
- **Emission Split:** Owner 18% | Miners 41% | Validators+Stakers 41%

---
*Subnet #7 — AI Finance Oracle | Twitter: @AIFinanceOracle*
    """,
    version="1.0.0-beta",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Finance API",
            "description": "User-facing endpoints. Query the subnet for financial predictions.",
        },
        {
            "name": "Miners",
            "description": "Miner management — register, list, and run predictions on individual miners.",
        },
        {
            "name": "Validators",
            "description": "Validator operations — generate challenges, dispatch to miners, and score predictions.",
        },
        {
            "name": "Network",
            "description": "Subnet network status, leaderboard, emission distribution, and hyperparameters.",
        },
        {
            "name": "Demo Simulation",
            "description": "Full simulation endpoints — run complete tempo cycles and compare miners side-by-side.",
        },
    ],
)

# API routes
app.include_router(finance_router)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse("static/index.html")
