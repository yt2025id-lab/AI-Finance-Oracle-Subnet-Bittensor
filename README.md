# AI Finance Oracle

## Overview
A decentralized AI Finance Oracle using Bittensor subnets. Miners provide predictive financial models that generate highly accurate forecasts, sentiment analysis, and risk assessments. Validators evaluate these models against real-world market data to ensure only the highest-quality intelligence earns emissions.

## Features
- Real-time financial price predictions
- Cross-market sentiment analysis
- Decentralized, competitive model evaluation
- Bittensor subnet integration with $TAO rewards

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the API: `uvicorn main:app --reload`
3. Submit finance queries via `/predict` endpoint

## Folder Structure
- `main.py`: Entry point (FastAPI)
- `finance/`: Core logic and predictive models
- `overview/`: Full project documentation (`overview.md`)
- `pitchdeck/`: Pitchdeck materials
- `requirements.txt`: Dependencies
- `SUBNET_PROPOSAL.md`: Deep dive into subnet mechanism design

## Bittensor Subnet Design
- **Miner:** Runs financial predictive models (time-series, LLMs for sentiment), returns directional and quantitative forecasts.
- **Validator:** Evaluates predictions against actual, subsequent market data (ground truth).
- **Incentive:** $TAO rewards based on Directional Accuracy, Magnitude Accuracy (MAE), and Timeliness.

## License
MIT

## Subnet Design Proposal
See [`SUBNET_PROPOSAL.md`](SUBNET_PROPOSAL.md) for the full technical subnet design proposal, including incentive mechanism, miner/validator design, business logic, and go-to-market strategy.

## Full Documentation
See `overview/overview.md` for detailed problem/solution, architecture, and mechanism design.
