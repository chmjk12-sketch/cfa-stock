"""Sector Entity - A+D 四维理论框架"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class FiveForces:
    """子维度 2a: 波特五力"""
    supplier_power: Optional[str] = None  # high/medium/low
    buyer_power: Optional[str] = None
    threat_entrants: Optional[str] = None
    threat_substitutes: Optional[str] = None
    rivalry_intensity: Optional[str] = None
    switching_cost: Optional[str] = None
    score: int = 5  # 1-10
    raw_analysis: Optional[dict] = None


@dataclass
class IndustryLifecycle:
    """子维度 2b: 行业生命周期"""
    lifecycle_stage: Optional[str] = None  # growth/mature/decline
    segment_growth_rate: Optional[float] = None
    segment_penetration: Optional[float] = None
    lifecycle_risk: Optional[str] = None
    score: int = 5
    raw_analysis: Optional[dict] = None


@dataclass
class EntryBarriers:
    """子维度 2c: Bain 进入壁垒"""
    barrier_economies_of_scale: int = 3  # 1-5
    barrier_product_diff: int = 3
    barrier_capital_req: int = 3
    barrier_switching_cost: int = 3
    barrier_sustainability: Optional[str] = None  # high/medium/low
    score: int = 5
    raw_analysis: Optional[dict] = None


@dataclass
class CompetitivePosition:
    """子维度 2d: Porter 竞争战略"""
    generic_strategy: Optional[str] = None  # cost_leadership/differentiation/focus_cost/focus_diff
    strategy_consistency: Optional[str] = None  # high/medium/low
    moat_from_strategy: Optional[str] = None  # wide/narrow/none
    score: int = 5
    raw_analysis: Optional[dict] = None


@dataclass
class Sector:
    """Sector 实体 - A+D 四维框架"""
    stock_id: UUID
    five_forces: FiveForces = field(default_factory=FiveForces)
    lifecycle: IndustryLifecycle = field(default_factory=IndustryLifecycle)
    barriers: EntryBarriers = field(default_factory=EntryBarriers)
    strategy: CompetitivePosition = field(default_factory=CompetitivePosition)
    score: int = 5  # 四维加权聚合
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def calculate_score(self) -> int:
        """四维加权聚合评分"""
        self.score = round(
            self.five_forces.score * 0.25 +
            self.lifecycle.score * 0.25 +
            self.barriers.score * 0.25 +
            self.strategy.score * 0.25
        )
        self.score = max(1, min(10, self.score))
        return self.score

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "stock_id": str(self.stock_id),
            "five_forces": {
                "supplier_power": self.five_forces.supplier_power,
                "buyer_power": self.five_forces.buyer_power,
                "threat_entrants": self.five_forces.threat_entrants,
                "threat_substitutes": self.five_forces.threat_substitutes,
                "rivalry_intensity": self.five_forces.rivalry_intensity,
                "switching_cost": self.five_forces.switching_cost,
                "score": self.five_forces.score,
            },
            "lifecycle": {
                "lifecycle_stage": self.lifecycle.lifecycle_stage,
                "segment_growth_rate": self.lifecycle.segment_growth_rate,
                "segment_penetration": self.lifecycle.segment_penetration,
                "lifecycle_risk": self.lifecycle.lifecycle_risk,
                "score": self.lifecycle.score,
            },
            "barriers": {
                "economies_of_scale": self.barriers.barrier_economies_of_scale,
                "product_diff": self.barriers.barrier_product_diff,
                "capital_req": self.barriers.barrier_capital_req,
                "switching_cost": self.barriers.barrier_switching_cost,
                "sustainability": self.barriers.barrier_sustainability,
                "score": self.barriers.score,
            },
            "strategy": {
                "generic_strategy": self.strategy.generic_strategy,
                "strategy_consistency": self.strategy.strategy_consistency,
                "moat_from_strategy": self.strategy.moat_from_strategy,
                "score": self.strategy.score,
            },
            "score": self.score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
