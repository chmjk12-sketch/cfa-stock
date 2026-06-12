"""Conclusion Entity - 投资结论实体"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Conclusion:
    """投资结论实体"""
    stock_id: UUID
    
    # 综合评分
    composite_score: Optional[float] = None  # 1-10
    rating: Optional[str] = None  # buy/hold/sell
    conviction: Optional[str] = None  # high/medium/low
    
    # 目标价
    target_price_low: Optional[float] = None
    target_price_high: Optional[float] = None
    
    # 各维度评分详情
    sector_score: Optional[int] = None
    financial_score: Optional[int] = None
    valuation_score: Optional[int] = None
    growth_score: Optional[int] = None
    risk_score: Optional[int] = None
    
    # 推理链
    reasoning_chain: Optional[dict] = None
    
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def calculate_rating(composite_score: float) -> str:
        """根据综合评分计算评级"""
        if composite_score >= 8.0:
            return "buy"
        elif composite_score >= 6.0:
            return "hold"
        else:
            return "sell"

    @staticmethod
    def calculate_conviction(scores: list) -> str:
        """根据评分离散度计算确信度"""
        score_range = max(scores) - min(scores)
        if score_range < 2:
            return "high"
        elif score_range < 4:
            return "medium"
        else:
            return "low"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "stock_id": str(self.stock_id),
            "composite_score": self.composite_score,
            "rating": self.rating,
            "conviction": self.conviction,
            "target_price_low": self.target_price_low,
            "target_price_high": self.target_price_high,
            "sector_score": self.sector_score,
            "financial_score": self.financial_score,
            "valuation_score": self.valuation_score,
            "growth_score": self.growth_score,
            "risk_score": self.risk_score,
            "reasoning_chain": self.reasoning_chain,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
