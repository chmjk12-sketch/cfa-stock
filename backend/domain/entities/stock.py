"""Stock Entity - 股票基础实体"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Stock:
    """股票实体"""
    ticker: str
    name: str
    exchange: str
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "ticker": self.ticker,
            "name": self.name,
            "exchange": self.exchange,
            "industry": self.industry,
            "market_cap": self.market_cap,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
