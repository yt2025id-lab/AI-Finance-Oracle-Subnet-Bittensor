from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


# ── Enums ──

class TaskType(str, Enum):
    price_prediction = "price_prediction"
    sentiment_analysis = "sentiment_analysis"
    risk_assessment = "risk_assessment"


class AssetClass(str, Enum):
    crypto = "crypto"
    equity = "equity"
    forex = "forex"
    commodity = "commodity"
    index = "index"


class MinerTier(str, Enum):
    entry = "entry"
    mid = "mid"
    high = "high"


# ── Finance Synapse (Challenge from Validator → Miner) ──

class MarketConditions(BaseModel):
    volatility: str = Field(..., example="high")
    trend: str = Field(..., example="bullish")
    macro_event: str = Field(..., example="fed_rate_decision")


class FinanceSynapse(BaseModel):
    """Challenge dispatched by Validator to Miners via Bittensor network."""
    task_type: TaskType = Field(..., description="Type of prediction task")
    target_asset: str = Field(..., example="BTC/USD")
    time_horizon_minutes: int = Field(..., example=120)
    asset_class: AssetClass = Field(default=AssetClass.crypto)
    exchange: Optional[str] = Field(None, example="Binance")
    conditions: Optional[MarketConditions] = None
    random_seed: Optional[int] = Field(None, example=83920174)


# ── Risk Factor ──

class RiskFactor(BaseModel):
    factor: str = Field(..., example="fed_rate_hike")
    probability: float = Field(..., ge=0, le=1, example=0.35)
    impact_percent: float = Field(..., example=-2.5)


# ── Miner Response ──

class MinerPrediction(BaseModel):
    """Prediction returned by a Miner in response to a Validator challenge."""
    miner_uid: int = Field(..., description="Miner UID on the subnet")
    miner_hotkey: str = Field(..., description="Miner hotkey address")
    predicted_price: Optional[float] = Field(None, example=68500.50)
    predicted_direction: Optional[str] = Field(None, example="bullish")
    sentiment_score: Optional[float] = Field(None, ge=-1, le=1, example=0.72)
    risk_factors: Optional[List[RiskFactor]] = None
    confidence: Optional[float] = Field(None, ge=0, le=1, example=0.78)
    data_sources: Optional[List[str]] = Field(None, example=["binance_orderbook", "on_chain_metrics", "news_sentiment"])
    response_time_ms: Optional[float] = Field(None, description="Response latency in milliseconds")


# ── Validator Scoring ──

class ScoreBreakdown(BaseModel):
    directional_accuracy: float = Field(..., ge=0, le=1, description="Directional accuracy score (weight: 40%)")
    magnitude_accuracy: float = Field(..., ge=0, le=1, description="MAE-based magnitude score (weight: 40%)")
    confidence_calibration: float = Field(..., ge=0, le=1, description="Confidence calibration score (weight: 10%)")
    latency_score: float = Field(..., ge=0, le=1, description="Response latency score (weight: 10%)")
    consistency: float = Field(..., ge=0, le=1, description="Consistency EMA over 100 rounds")
    direction_bonus: bool = Field(False, description="1.5x bonus for correct direction in volatile market")
    final_score: float = Field(..., ge=0, description="Weighted final score")


class MinerScoreResult(BaseModel):
    miner_uid: int
    miner_hotkey: str
    score: ScoreBreakdown
    rank: int
    tau_earned: float = Field(..., description="Estimated TAO earned this tempo")


# ── Miner Registration & Info ──

class MinerRegister(BaseModel):
    hotkey: str = Field(..., example="5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty")
    coldkey: str = Field(..., example="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY")
    tier: MinerTier = Field(default=MinerTier.entry)
    ip: str = Field(..., example="192.168.1.100")
    port: int = Field(default=8091, example=8091)
    model_name: Optional[str] = Field(None, example="alpha-quant-v2")


class MinerInfo(BaseModel):
    uid: int
    hotkey: str
    coldkey: str
    tier: MinerTier
    ip: str
    port: int
    model_name: Optional[str]
    stake: float = Field(0.0, description="TAO staked")
    is_active: bool = True
    total_challenges: int = 0
    avg_score: float = 0.0
    total_tau_earned: float = 0.0
    last_active_block: Optional[int] = None


# ── Validator Registration & Info ──

class ValidatorRegister(BaseModel):
    hotkey: str = Field(..., example="5DAAnrj7VHTznn2AWBemMuyBwZWs6FNFjdyVXUeYum3PTXFy")
    coldkey: str = Field(..., example="5HGjWAeFDfFCWPsjFQdVV2Msvz2XtMktvgocEZcCj68kUMaw")
    ip: str = Field(..., example="192.168.1.200")
    port: int = Field(default=8092, example=8092)
    stake: float = Field(default=1000.0, example=1000.0)


class ValidatorInfo(BaseModel):
    uid: int
    hotkey: str
    coldkey: str
    ip: str
    port: int
    stake: float
    is_active: bool = True
    challenges_sent: int = 0
    last_weight_block: Optional[int] = None
    bond_strength: float = 0.0


# ── Challenge Result ──

class ChallengeResult(BaseModel):
    challenge_id: str
    synapse: FinanceSynapse
    challenge_type: str = Field(..., description="historical (70%) or near_term (30%)")
    ground_truth: Optional[dict] = Field(None, description="Actual market outcome (for historical)")
    miner_predictions: List[MinerPrediction]
    scores: List[MinerScoreResult]
    timestamp: str
    tempo: int


# ── Network Status ──

class SubnetHyperparameters(BaseModel):
    max_allowed_uids: int = 256
    max_allowed_validators: int = 64
    immunity_period: int = 5000
    weights_rate_limit: int = 100
    commit_reveal_period: int = 1
    tempo: int = 360
    subnet_owner_cut: float = 0.18
    miner_cut: float = 0.41
    validator_cut: float = 0.41


class NetworkStatus(BaseModel):
    subnet_name: str = "AI Finance Oracle Subnet"
    subnet_id: int = 7
    block_height: int
    current_tempo: int
    total_miners: int
    active_miners: int
    total_validators: int
    active_validators: int
    total_stake: float
    total_emission_per_tempo: float
    hyperparameters: SubnetHyperparameters
    top_miners: List[MinerInfo]


# ── Leaderboard ──

class LeaderboardEntry(BaseModel):
    rank: int
    miner_uid: int
    miner_hotkey: str
    tier: MinerTier
    avg_score: float
    total_challenges: int
    total_tau_earned: float
    directional_accuracy_avg: float
    magnitude_accuracy_avg: float
    streak: int = Field(0, description="Consecutive tempos in top 10")


# ── Simple Query (backward compatible) ──

class MarketQuery(BaseModel):
    user_id: str
    target_asset: str = Field(..., example="BTC/USD")
    time_horizon_minutes: int = Field(..., example=120)
    asset_class: Optional[str] = Field(None, example="crypto")
    exchange: Optional[str] = Field(None, example="Binance")


class PredictionResponse(BaseModel):
    target_asset: str
    predicted_price: float
    predicted_direction: str
    sentiment_score: float
    confidence: float
    risk_factors: List[RiskFactor]
    data_sources: List[str]
    miners_consulted: int
    timestamp: str
