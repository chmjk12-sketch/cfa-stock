"""Growth Entity - 成长性实体"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Growth:
    """成长性实体"""
    stock_id: UUID
    
    # 历史增长
    revenue_growth_3y_cagr: Optional[float] = None  # 营收3年CAGR (%)
    earnings_growth_3y_cagr: Optional[float] = None  # 盈利3年CAGR (%)
    fcf_growth_3y_cagr: Optional[float] = None  # FCF 3年CAGR (%)
    
    # 预期增长
    consensus_growth_next_2y: Optional[float] = None  # 分析师一致预期 (%)
    
    # 护城河 (从 Sector.CompetitivePosition 填充)
    moat_assessment: Optional[str] = None  # wide/narrow/none
    
    # 评分
    score: int = 5  # 1-10
    raw_data: Optional[dict] = None
    
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "stock_id": str(self.stock_id),
            "revenue_growth_3y_cagr": self.revenue_growth_3y_cagr,
            "earnings_growth_3y_cagr": self.earnings_growth_3y_cagr,
            "fcf_growth_3y_cagr": self.fcf_growth_3y_cagr,
            "consensus_growth_next_2y": self.consensus_growth_next_2y,
            "moat_assessment": self.moat_assessment,
            "score": self.score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
