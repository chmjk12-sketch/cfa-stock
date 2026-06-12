"""FinancialQuality Entity - 财务质量实体"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class FinancialQuality:
    """财务质量实体 - DuPont 分解"""
    stock_id: UUID
    
    # DuPont 三因子
    roe: Optional[float] = None  # ROE (%)
    net_margin: Optional[float] = None  # 净利率 (%)
    asset_turnover: Optional[float] = None  # 资产周转率
    equity_multiplier: Optional[float] = None  # 权益乘数
    
    # 财务健康
    debt_ratio: Optional[float] = None  # 资产负债率 (%)
    fcf_positive_3y: Optional[bool] = None  # 近3年FCF是否为正
    
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
            "roe": self.roe,
            "net_margin": self.net_margin,
            "asset_turnover": self.asset_turnover,
            "equity_multiplier": self.equity_multiplier,
            "debt_ratio": self.debt_ratio,
            "fcf_positive_3y": self.fcf_positive_3y,
            "score": self.score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
