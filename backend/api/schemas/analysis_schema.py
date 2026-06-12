"""Analysis API Schemas"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# ===== Sector Schemas =====

class FiveForcesDetail(BaseModel):
    supplier_power: Optional[str]
    buyer_power: Optional[str]
    threat_entrants: Optional[str]
    threat_substitutes: Optional[str]
    rivalry_intensity: Optional[str]
    switching_cost: Optional[str]
    score: int


class LifecycleDetail(BaseModel):
    lifecycle_stage: Optional[str]
    segment_growth_rate: Optional[float]
    segment_penetration: Optional[float]
    lifecycle_risk: Optional[str]
    score: int


class BarriersDetail(BaseModel):
    economies_of_scale: int
    product_diff: int
    capital_req: int
    switching_cost: int
    sustainability: Optional[str]
    score: int


class StrategyDetail(BaseModel):
    generic_strategy: Optional[str]
    strategy_consistency: Optional[str]
    moat_from_strategy: Optional[str]
    score: int


class SectorResponse(BaseModel):
    id: UUID
    stock_id: UUID
    five_forces: FiveForcesDetail
    lifecycle: LifecycleDetail
    barriers: BarriersDetail
    strategy: StrategyDetail
    score: int

    class Config:
        from_attributes = True


# ===== Financial Quality Schemas =====

class FinancialQualityResponse(BaseModel):
    id: UUID
    stock_id: UUID
    roe: Optional[float]
    net_margin: Optional[float]
    asset_turnover: Optional[float]
    equity_multiplier: Optional[float]
    debt_ratio: Optional[float]
    fcf_positive_3y: Optional[bool]
    score: int

    class Config:
        from_attributes = True


# ===== Valuation Schemas =====

class ValuationResponse(BaseModel):
    id: UUID
    stock_id: UUID
    pe_ttm: Optional[float]
    pb: Optional[float]
    peg: Optional[float]
    pe_percentile_5y: Optional[float]
    dcf_low: Optional[float]
    dcf_high: Optional[float]
    margin_of_safety: Optional[float]
    score: int

    class Config:
        from_attributes = True


# ===== Growth Schemas =====

class GrowthResponse(BaseModel):
    id: UUID
    stock_id: UUID
    revenue_growth_3y_cagr: Optional[float]
    earnings_growth_3y_cagr: Optional[float]
    fcf_growth_3y_cagr: Optional[float]
    consensus_growth_next_2y: Optional[float]
    moat_assessment: Optional[str]
    score: int

    class Config:
        from_attributes = True


# ===== Risk Schemas =====

class RiskResponse(BaseModel):
    id: UUID
    stock_id: UUID
    beta: Optional[float]
    debt_to_equity: Optional[float]
    interest_coverage: Optional[float]
    industry_cyclicality: Optional[str]
    policy_risk: Optional[str]
    governance_flags: Optional[List[str]]
    score: int

    class Config:
        from_attributes = True


# ===== Conclusion Schemas =====

class ConclusionResponse(BaseModel):
    id: UUID
    stock_id: UUID
    composite_score: Optional[float]
    rating: Optional[str]
    conviction: Optional[str]
    target_price_low: Optional[float]
    target_price_high: Optional[float]
    sector_score: Optional[int]
    financial_score: Optional[int]
    valuation_score: Optional[int]
    growth_score: Optional[int]
    risk_score: Optional[int]
    reasoning_chain: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


# ===== Full Analysis Schema =====

class StockAnalysisResponse(BaseModel):
    stock: Dict[str, Any]
    sector: SectorResponse
    financial_quality: FinancialQualityResponse
    valuation: ValuationResponse
    growth: GrowthResponse
    risk: RiskResponse
    conclusion: ConclusionResponse
    reasoning_log: List[Dict[str, str]]


# ===== Opportunity Schema =====

class OpportunityResponse(BaseModel):
    id: UUID
    theme: str
    industry: Optional[str]
    opportunity_score: Optional[float]
    stock_ids: Optional[List[UUID]]
    risks: Optional[str]
    conclusion: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Analysis Task Schema =====

class AnalysisTaskResponse(BaseModel):
    id: UUID
    stock_id: UUID
    task_type: str
    status: str
    celery_task_id: Optional[str]
    result: Optional[Dict[str, Any]]
    error_message: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
