"""Stock API Schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class StockBase(BaseModel):
    ticker: str
    name: str
    exchange: str
    industry: Optional[str] = None
    market_cap: Optional[float] = None


class StockCreate(StockBase):
    pass


class StockResponse(StockBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StockSearchResult(BaseModel):
    id: UUID
    ticker: str
    name: str
    exchange: str
    industry: Optional[str]
    composite_score: Optional[float] = None
    rating: Optional[str] = None


class StockListResponse(BaseModel):
    total: int
    items: List[StockResponse]
