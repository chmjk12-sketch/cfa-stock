"""Valuation Entity - 估值实体"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Valuation:
    """估值实体 - 绝对估值 + 相对估值"""
    stock_id: UUID
    
    # 相对估值
    pe_ttm: Optional[float] = None
    pb: Optional[float] = None
    peg: Optional[float] = None
    pe_percentile_5y: Optional[float] = None  # 5年PE分位数 (%)
    
    # 绝对估值 (DCF)
    dcf_low: Optional[float] = None  # DCF 合理区间下限
    dcf_high: Optional[float] = None  # DCF 合理区间上限
    margin_of_safety: Optional[float] = None  # 安全边际 (%)
    
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
            "pe_ttm": self.pe_ttm,
            "pb": self.pb,
            "peg": self.peg,
            "pe_percentile_5y": self.pe_percentile_5y,
            "dcf_low": self.dcf_low,
            "dcf_high": self.dcf_high,
            "margin_of_safety": self.margin_of_safety,
            "score": self.score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
