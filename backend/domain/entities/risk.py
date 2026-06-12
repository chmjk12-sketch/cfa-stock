"""Risk Entity - 风险实体"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4


@dataclass
class Risk:
    """风险实体 - 多维度风险画像"""
    stock_id: UUID
    
    # 量化风险
    beta: Optional[float] = None
    debt_to_equity: Optional[float] = None
    interest_coverage: Optional[float] = None
    
    # 定性风险
    industry_cyclicality: Optional[str] = None  # high/medium/low
    policy_risk: Optional[str] = None  # high/medium/low
    governance_flags: Optional[List[str]] = None
    
    # 评分 (越高 = 风险越低)
    score: int = 5  # 1-10
    raw_data: Optional[dict] = None
    
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "stock_id": str(self.stock_id),
            "beta": self.beta,
            "debt_to_equity": self.debt_to_equity,
            "interest_coverage": self.interest_coverage,
            "industry_cyclicality": self.industry_cyclicality,
            "policy_risk": self.policy_risk,
            "governance_flags": self.governance_flags,
            "score": self.score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
