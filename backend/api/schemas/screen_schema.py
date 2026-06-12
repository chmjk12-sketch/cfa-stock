"""Screen API Schemas"""
from pydantic import BaseModel
from typing import Optional, List


class ScreenRequest(BaseModel):
    sectors: Optional[List[str]] = None
    peg_range: Optional[List[float]] = None
    pe_range: Optional[List[float]] = None
    net_profit_growth_min: Optional[float] = None
    revenue_growth_min: Optional[float] = None
    rating: Optional[str] = None
    sort_by: Optional[str] = "peg"
    sort_order: Optional[str] = "asc"
    page: int = 1
    page_size: int = 50


class ScreenStockItem(BaseModel):
    ticker: str
    name: str
    sector: Optional[str] = None
    latest_price: Optional[float] = None
    change_pct: Optional[float] = None
    pe_ttm: Optional[float] = None
    peg: Optional[float] = None
    net_profit_growth: Optional[float] = None
    target_price_neutral: Optional[float] = None
    upside_neutral: Optional[float] = None
    rating: Optional[str] = None
    composite_score: Optional[float] = None


class ScreenResponse(BaseModel):
    total: int
    page: int
    page_size: int
    stocks: List[ScreenStockItem]
