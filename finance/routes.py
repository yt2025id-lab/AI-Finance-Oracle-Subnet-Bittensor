"""
API Routes for AI Finance Oracle Subnet Demo.
Demonstrates full subnet functionality: Miners, Validators, Scoring, and Network.
"""

import random
import time
import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from .models import (
    TaskType, AssetClass, MinerTier,
    MarketConditions, FinanceSynapse,
    RiskFactor,
    MinerPrediction, ScoreBreakdown, MinerScoreResult,
    MinerRegister, MinerInfo,
    ValidatorRegister, ValidatorInfo,
    ChallengeResult, NetworkStatus, SubnetHyperparameters,
    LeaderboardEntry,
    MarketQuery, PredictionResponse,
)
from .ai import run_miner_prediction, score_prediction, get_prediction, run_demo_scenario, get_demo_scenarios_list
from . import db

router = APIRouter()


# ═══════════════════════════════════════════════════════════════
# 1. FINANCE QUERY (User-facing API)
# ═══════════════════════════════════════════════════════════════

@router.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Finance API"],
    summary="Predict Asset Price",
    description=(
        "User-facing endpoint. Submit a market query and receive AI-powered predictions "
        "from the decentralized miner network. Returns price prediction, direction, "
        "sentiment score, risk factors, and confidence."
    ),
)
def predict(query: MarketQuery):
    result = get_prediction(query)
    return PredictionResponse(**result)


# ═══════════════════════════════════════════════════════════════
# 2. MINER ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get(
    "/miners",
    response_model=List[MinerInfo],
    tags=["Miners"],
    summary="List All Miners",
    description="Get list of all registered miners on the subnet with their stats and performance.",
)
def list_miners():
    miners = db.get_miners()
    return [MinerInfo(**m) for m in miners.values()]


@router.get(
    "/miners/{uid}",
    response_model=MinerInfo,
    tags=["Miners"],
    summary="Get Miner Details",
    description="Get detailed information about a specific miner by UID.",
)
def get_miner(uid: int):
    miner = db.get_miner(uid)
    if not miner:
        raise HTTPException(status_code=404, detail=f"Miner UID {uid} not found")
    return MinerInfo(**miner)


@router.post(
    "/miners/register",
    response_model=MinerInfo,
    tags=["Miners"],
    summary="Register New Miner",
    description=(
        "Register a new miner on the subnet. Requires hotkey, coldkey, and network info. "
        "New miners start with 0 stake and enter the immunity period (5000 blocks)."
    ),
)
def register_miner(miner: MinerRegister):
    for m in db.get_miners().values():
        if m["hotkey"] == miner.hotkey:
            raise HTTPException(status_code=400, detail="Hotkey already registered")

    result = db.add_miner(miner.dict())
    return MinerInfo(**result)


@router.post(
    "/miners/{uid}/predict",
    response_model=MinerPrediction,
    tags=["Miners"],
    summary="Run Miner Prediction",
    description=(
        "Simulate a miner processing a finance challenge. "
        "The miner runs its AI model and returns price prediction, direction, "
        "sentiment, and risk factors. Response varies by miner tier."
    ),
)
def miner_predict(uid: int, synapse: FinanceSynapse):
    miner = db.get_miner(uid)
    if not miner:
        raise HTTPException(status_code=404, detail=f"Miner UID {uid} not found")

    result = run_miner_prediction(synapse.dict(), miner["tier"])
    result["miner_uid"] = uid
    result["miner_hotkey"] = miner["hotkey"]

    return MinerPrediction(**result)


# ═══════════════════════════════════════════════════════════════
# 3. VALIDATOR ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get(
    "/validators",
    response_model=List[ValidatorInfo],
    tags=["Validators"],
    summary="List All Validators",
    description="Get list of all registered validators on the subnet.",
)
def list_validators():
    validators = db.get_validators()
    return [ValidatorInfo(**v) for v in validators.values()]


@router.get(
    "/validators/{uid}",
    response_model=ValidatorInfo,
    tags=["Validators"],
    summary="Get Validator Details",
    description="Get detailed information about a specific validator by UID.",
)
def get_validator(uid: int):
    validator = db.get_validator(uid)
    if not validator:
        raise HTTPException(status_code=404, detail=f"Validator UID {uid} not found")
    return ValidatorInfo(**validator)


@router.post(
    "/validators/register",
    response_model=ValidatorInfo,
    tags=["Validators"],
    summary="Register New Validator",
    description="Register a new validator on the subnet. Requires stake to participate.",
)
def register_validator(validator: ValidatorRegister):
    for v in db.get_validators().values():
        if v["hotkey"] == validator.hotkey:
            raise HTTPException(status_code=400, detail="Hotkey already registered")

    result = db.add_validator(validator.dict())
    return ValidatorInfo(**result)


@router.post(
    "/validators/{uid}/generate-challenge",
    response_model=FinanceSynapse,
    tags=["Validators"],
    summary="Generate Finance Challenge",
    description=(
        "Validator generates a finance challenge (FinanceSynapse) to dispatch to miners. "
        "70% are historical challenges (past market events with known outcomes), "
        "30% are near-term challenges (active markets for forward prediction)."
    ),
)
def generate_challenge(
    uid: int,
    task_type: TaskType = Query(default=TaskType.price_prediction, description="Type of challenge"),
):
    validator = db.get_validator(uid)
    if not validator:
        raise HTTPException(status_code=404, detail=f"Validator UID {uid} not found")

    assets = ["BTC/USD", "ETH/USD", "SOL/USD", "AAPL", "SPY", "XAU/USD"]
    exchanges = ["Binance", "Coinbase", "Kraken", "Deribit", "CME"]

    volatility_levels = ["low", "moderate", "high", "elevated", "normal"]
    trends = ["bullish", "bearish", "neutral", "uncertain"]
    macro_events = ["none", "fed_rate_decision", "cpi_release", "etf_inflow_surge", "normal"]

    synapse = FinanceSynapse(
        task_type=task_type,
        target_asset=random.choice(assets),
        time_horizon_minutes=random.choice([30, 60, 120, 360, 1440]),
        asset_class=AssetClass.crypto,
        exchange=random.choice(exchanges),
        conditions=MarketConditions(
            volatility=random.choice(volatility_levels),
            trend=random.choice(trends),
            macro_event=random.choice(macro_events),
        ),
        random_seed=random.randint(10000000, 99999999),
    )

    validator["challenges_sent"] += 1
    return synapse


@router.post(
    "/validators/{uid}/run-challenge",
    response_model=ChallengeResult,
    tags=["Validators"],
    summary="Run Full Challenge Cycle",
    description=(
        "Execute a complete challenge cycle:\n"
        "1. Validator generates a challenge (FinanceSynapse)\n"
        "2. Challenge is dispatched to ALL active miners\n"
        "3. Each miner runs its prediction model\n"
        "4. Validator scores each miner's prediction against ground truth\n"
        "5. Miners are ranked and TAO rewards are distributed"
    ),
)
def run_challenge(
    uid: int,
    task_type: TaskType = Query(default=TaskType.price_prediction),
    synapse: Optional[FinanceSynapse] = None,
):
    validator = db.get_validator(uid)
    if not validator:
        raise HTTPException(status_code=404, detail=f"Validator UID {uid} not found")

    if synapse is None:
        assets = ["BTC/USD", "ETH/USD", "SOL/USD"]
        synapse = FinanceSynapse(
            task_type=task_type,
            target_asset=random.choice(assets),
            time_horizon_minutes=random.choice([60, 120, 360]),
            asset_class=AssetClass.crypto,
            exchange=random.choice(["Binance", "Coinbase", "Kraken"]),
            conditions=MarketConditions(
                volatility=random.choice(["normal", "high", "moderate"]),
                trend=random.choice(["bullish", "bearish", "neutral"]),
                macro_event=random.choice(["none", "fed_rate_decision", "normal"]),
            ),
            random_seed=random.randint(10000000, 99999999),
        )

    is_historical = random.random() < 0.7
    challenge_type = "historical" if is_historical else "near_term"

    rng = random.Random(synapse.random_seed if synapse.random_seed else int(time.time()))
    ground_truth = None
    if is_historical:
        base_price = rng.uniform(60000, 75000)
        direction = rng.choice(["bullish", "bearish"])
        ground_truth = {
            "actual_price": round(base_price, 2),
            "actual_direction": direction,
            "price_change_pct": round(rng.uniform(-5, 5), 2),
        }

    miners = db.get_miners()
    predictions = []
    for miner_uid, miner in miners.items():
        if not miner["is_active"]:
            continue
        result = run_miner_prediction(synapse.dict(), miner["tier"])
        result["miner_uid"] = miner_uid
        result["miner_hotkey"] = miner["hotkey"]
        predictions.append(MinerPrediction(**result))

    scores = []
    total_emission = db.get_state()["total_emission_per_tempo"] * 0.41
    for pred in predictions:
        if ground_truth:
            score_data = score_prediction(pred.dict(), ground_truth)
        else:
            score_data = {
                "directional_accuracy": round(rng.uniform(0.5, 0.95), 4),
                "magnitude_accuracy": round(rng.uniform(0.3, 0.9), 4),
                "confidence_calibration": round(rng.uniform(0.4, 0.85), 4),
                "latency_score": round(rng.uniform(0.7, 0.99), 4),
                "consistency": round(rng.uniform(0.6, 0.92), 4),
                "direction_bonus": False,
                "final_score": 0,
            }
            score_data["final_score"] = round(
                0.40 * score_data["directional_accuracy"]
                + 0.40 * score_data["magnitude_accuracy"]
                + 0.10 * score_data["confidence_calibration"]
                + 0.10 * score_data["latency_score"],
                4
            )

        scores.append({
            "miner_uid": pred.miner_uid,
            "miner_hotkey": pred.miner_hotkey,
            "score": ScoreBreakdown(**score_data),
            "rank": 0,
            "tau_earned": 0,
        })

    scores.sort(key=lambda s: s["score"].final_score, reverse=True)
    total_scores = sum(s["score"].final_score for s in scores)
    for rank, s in enumerate(scores, 1):
        s["rank"] = rank
        if total_scores > 0:
            s["tau_earned"] = round(total_emission * (s["score"].final_score / total_scores), 6)
        else:
            s["tau_earned"] = 0
        db.update_miner_score(s["miner_uid"], s["score"].final_score, s["tau_earned"])

    score_results = [MinerScoreResult(**s) for s in scores]

    validator["challenges_sent"] += 1
    validator["last_weight_block"] = db.get_state()["block_height"]
    db.advance_block(random.randint(1, 5))

    challenge_id = str(uuid.uuid4())[:8]
    challenge_record = {
        "challenge_id": challenge_id,
        "synapse": synapse,
        "challenge_type": challenge_type,
        "ground_truth": ground_truth,
        "miner_predictions": predictions,
        "scores": score_results,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tempo": db.get_state()["current_tempo"],
    }
    db.add_challenge(challenge_record)

    return ChallengeResult(**challenge_record)


@router.post(
    "/validators/{uid}/score-prediction",
    response_model=MinerScoreResult,
    tags=["Validators"],
    summary="Score a Single Miner Prediction",
    description=(
        "Validator scores a specific miner's prediction against ground truth.\n\n"
        "Scoring dimensions:\n"
        "- **Directional Accuracy (40%)**\n"
        "- **Magnitude Accuracy (40%)**\n"
        "- **Confidence Calibration (10%)**\n"
        "- **Latency (10%)**"
    ),
)
def score_single_prediction(
    uid: int,
    prediction: MinerPrediction,
    actual_price: float = Query(..., description="Actual asset price"),
    actual_direction: str = Query(default="bullish", description="Actual price direction"),
):
    validator = db.get_validator(uid)
    if not validator:
        raise HTTPException(status_code=404, detail=f"Validator UID {uid} not found")

    ground_truth = {
        "actual_price": actual_price,
        "actual_direction": actual_direction,
        "price_change_pct": 0,
    }

    score_data = score_prediction(prediction.dict(), ground_truth)
    tau_earned = round(db.get_state()["total_emission_per_tempo"] * 0.41 * score_data["final_score"] / 8, 6)
    db.update_miner_score(prediction.miner_uid, score_data["final_score"], tau_earned)

    return MinerScoreResult(
        miner_uid=prediction.miner_uid,
        miner_hotkey=prediction.miner_hotkey,
        score=ScoreBreakdown(**score_data),
        rank=1,
        tau_earned=tau_earned,
    )


# ═══════════════════════════════════════════════════════════════
# 4. NETWORK & SUBNET ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get(
    "/network/status",
    response_model=NetworkStatus,
    tags=["Network"],
    summary="Subnet Network Status",
    description="Get the current status of the AI Finance Oracle subnet.",
)
def network_status():
    state = db.get_state()
    miners = db.get_miners()
    validators = db.get_validators()

    active_miners = [m for m in miners.values() if m["is_active"]]
    active_validators = [v for v in validators.values() if v["is_active"]]
    total_stake = sum(m["stake"] for m in miners.values()) + sum(v["stake"] for v in validators.values())

    top = sorted(active_miners, key=lambda m: m["avg_score"], reverse=True)[:5]

    return NetworkStatus(
        block_height=state["block_height"],
        current_tempo=state["current_tempo"],
        total_miners=len(miners),
        active_miners=len(active_miners),
        total_validators=len(validators),
        active_validators=len(active_validators),
        total_stake=round(total_stake, 2),
        total_emission_per_tempo=state["total_emission_per_tempo"],
        hyperparameters=SubnetHyperparameters(),
        top_miners=[MinerInfo(**m) for m in top],
    )


@router.get("/network/leaderboard", response_model=List[LeaderboardEntry], tags=["Network"], summary="Miner Leaderboard")
def leaderboard():
    miners = db.get_leaderboard()
    rng = random.Random(42)
    entries = []
    for rank, m in enumerate(miners, 1):
        entries.append(LeaderboardEntry(
            rank=rank, miner_uid=m["uid"], miner_hotkey=m["hotkey"], tier=m["tier"],
            avg_score=m["avg_score"], total_challenges=m["total_challenges"],
            total_tau_earned=m["total_tau_earned"],
            directional_accuracy_avg=round(m["avg_score"] * rng.uniform(0.9, 1.1), 3),
            magnitude_accuracy_avg=round(m["avg_score"] * rng.uniform(0.75, 1.0), 3),
            streak=max(0, int((m["avg_score"] - 0.5) * 20) + rng.randint(0, 5)),
        ))
    return entries


@router.get("/network/challenges", response_model=List[ChallengeResult], tags=["Network"], summary="Recent Challenges")
def recent_challenges(limit: int = Query(default=10, ge=1, le=50)):
    return [ChallengeResult(**c) for c in db.get_challenges(limit)]


@router.get("/network/hyperparameters", response_model=SubnetHyperparameters, tags=["Network"], summary="Subnet Hyperparameters")
def hyperparameters():
    return SubnetHyperparameters()


@router.get("/network/emission-distribution", tags=["Network"], summary="Emission Distribution")
def emission_distribution():
    state = db.get_state()
    total = state["total_emission_per_tempo"]
    miners = db.get_miners()
    top_miners = sorted(miners.values(), key=lambda m: m["avg_score"], reverse=True)[:5]
    return {
        "tempo": state["current_tempo"],
        "total_emission_tao": total,
        "distribution": {
            "subnet_owner": {"share": "18%", "amount_tao": round(total * 0.18, 6)},
            "miners_total": {"share": "41%", "amount_tao": round(total * 0.41, 6)},
            "validators_stakers_total": {"share": "41%", "amount_tao": round(total * 0.41, 6)},
        },
        "top_miner_earnings": [
            {"uid": m["uid"], "hotkey": m["hotkey"][:16] + "...", "tier": m["tier"], "score": m["avg_score"],
             "estimated_tao_this_tempo": round(total * 0.41 * m["avg_score"] / max(1, sum(mm["avg_score"] for mm in miners.values())), 6)}
            for m in top_miners
        ],
    }


# ═══════════════════════════════════════════════════════════════
# 5. DEMO / SIMULATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.post("/demo/full-tempo-cycle", tags=["Demo Simulation"], summary="Run Full Tempo Cycle")
def full_tempo_cycle():
    state = db.get_state()
    validators = list(db.get_validators().values())
    if not validators:
        raise HTTPException(status_code=400, detail="No validators registered")
    active_validators = [v for v in validators if v["is_active"]]
    if not active_validators:
        raise HTTPException(status_code=400, detail="No active validators")

    lead_validator = max(active_validators, key=lambda v: v["stake"])
    results = []
    task_types = [TaskType.price_prediction, TaskType.sentiment_analysis, TaskType.risk_assessment]

    for i, task_type in enumerate(task_types):
        assets = ["BTC/USD", "ETH/USD", "SOL/USD", "AAPL", "SPY", "XAU/USD"]
        synapse = FinanceSynapse(
            task_type=task_type, target_asset=assets[i % len(assets)],
            time_horizon_minutes=random.choice([60, 120, 360]), asset_class=AssetClass.crypto,
            exchange=random.choice(["Binance", "Coinbase", "Deribit"]),
            conditions=MarketConditions(
                volatility=random.choice(["normal", "high", "moderate"]),
                trend=random.choice(["bullish", "bearish", "neutral"]),
                macro_event=random.choice(["none", "fed_rate_decision", "normal"]),
            ),
            random_seed=random.randint(10000000, 99999999),
        )

        is_historical = i < 2
        rng = random.Random(synapse.random_seed)
        ground_truth = None
        if is_historical:
            ground_truth = {"actual_price": round(rng.uniform(60000, 75000), 2),
                            "actual_direction": rng.choice(["bullish", "bearish"]),
                            "price_change_pct": round(rng.uniform(-5, 5), 2)}

        miners = db.get_miners()
        predictions = []
        for miner_uid, miner in miners.items():
            if not miner["is_active"]:
                continue
            result = run_miner_prediction(synapse.dict(), miner["tier"])
            result["miner_uid"] = miner_uid
            result["miner_hotkey"] = miner["hotkey"]
            predictions.append(MinerPrediction(**result))

        scores = []
        total_emission = state["total_emission_per_tempo"] * 0.41 / 3
        for pred in predictions:
            if ground_truth:
                score_data = score_prediction(pred.dict(), ground_truth)
            else:
                score_data = {"directional_accuracy": round(rng.uniform(0.5, 0.95), 4),
                              "magnitude_accuracy": round(rng.uniform(0.3, 0.9), 4),
                              "confidence_calibration": round(rng.uniform(0.4, 0.85), 4),
                              "latency_score": round(rng.uniform(0.7, 0.99), 4),
                              "consistency": round(rng.uniform(0.6, 0.92), 4),
                              "direction_bonus": False, "final_score": 0}
                score_data["final_score"] = round(0.40 * score_data["directional_accuracy"] + 0.40 * score_data["magnitude_accuracy"] + 0.10 * score_data["confidence_calibration"] + 0.10 * score_data["latency_score"], 4)
            scores.append({"miner_uid": pred.miner_uid, "miner_hotkey": pred.miner_hotkey,
                           "score": ScoreBreakdown(**score_data), "rank": 0, "tau_earned": 0})

        scores.sort(key=lambda s: s["score"].final_score, reverse=True)
        total_scores = sum(s["score"].final_score for s in scores)
        for rank, s in enumerate(scores, 1):
            s["rank"] = rank
            if total_scores > 0:
                s["tau_earned"] = round(total_emission * (s["score"].final_score / total_scores), 6)
            db.update_miner_score(s["miner_uid"], s["score"].final_score, s["tau_earned"])

        challenge_id = str(uuid.uuid4())[:8]
        challenge_record = {"challenge_id": challenge_id, "synapse": synapse,
                            "challenge_type": "historical" if is_historical else "near_term",
                            "ground_truth": ground_truth, "miner_predictions": predictions,
                            "scores": [MinerScoreResult(**s) for s in scores],
                            "timestamp": datetime.utcnow().isoformat() + "Z", "tempo": state["current_tempo"]}
        db.add_challenge(challenge_record)
        results.append(ChallengeResult(**challenge_record))

    db.advance_tempo()
    lead_validator["challenges_sent"] += 3
    lead_validator["last_weight_block"] = state["block_height"]

    return {
        "tempo_completed": state["current_tempo"] - 1, "new_tempo": state["current_tempo"],
        "block_height": state["block_height"], "lead_validator_uid": lead_validator["uid"],
        "challenges_run": len(results), "total_tao_distributed": round(state["total_emission_per_tempo"], 6),
        "challenges": results,
        "updated_leaderboard": [
            {"rank": rank, "uid": m["uid"], "hotkey": m["hotkey"][:16] + "...", "tier": m["tier"],
             "avg_score": m["avg_score"], "total_tau": m["total_tau_earned"]}
            for rank, m in enumerate(sorted(db.get_miners().values(), key=lambda x: x["avg_score"], reverse=True), 1)
        ],
    }


@router.post("/demo/compare-miners", tags=["Demo Simulation"], summary="Compare Miners on Same Challenge")
def compare_miners(synapse: FinanceSynapse):
    miners = db.get_miners()
    comparisons = []
    for uid, miner in miners.items():
        if not miner["is_active"]:
            continue
        result = run_miner_prediction(synapse.dict(), miner["tier"])
        comparisons.append({"miner_uid": uid, "miner_hotkey": miner["hotkey"][:16] + "...",
                            "tier": miner["tier"], "model": miner["model_name"] or "unknown",
                            "predicted_price": result["predicted_price"],
                            "predicted_direction": result["predicted_direction"],
                            "sentiment_score": result["sentiment_score"],
                            "confidence": result["confidence"],
                            "response_time_ms": result["response_time_ms"]})
    comparisons.sort(key=lambda x: x["confidence"], reverse=True)
    return {"challenge": synapse.dict(), "total_miners_queried": len(comparisons), "comparisons": comparisons}


# ═══════════════════════════════════════════════════════════════
# 6. LANDING PAGE DEMO ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/api/demo-scenarios", tags=["Demo Simulation"], summary="List Demo Scenarios")
def list_demo_scenarios():
    return get_demo_scenarios_list()


@router.get("/api/demo/{scenario_key}", tags=["Demo Simulation"], summary="Run Demo Scenario")
def run_demo(scenario_key: str):
    result = run_demo_scenario(scenario_key)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
