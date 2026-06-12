"""Market API Schemas"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class MarketDataResponse(BaseModel):
    ticker: str
    trade_date: date
    latest_price: Optional[float] = None
    change_pct: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[float] = None
    turnover: Optional[float] = None

    class Config:
        from_attributes = True


class KlineResponse(BaseModel):
    trade_date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

    class Config:
        from_attributes = True


class ForecastResponse(BaseModel):
    ticker: str
    report_date: date
    eps_forecast_optimistic: Optional[float] = None
    eps_forecast_neutral: Optional[float] = None
    eps_forecast_pessimistic: Optional[float] = None
    net_profit_growth: Optional[float] = None
    revenue_growth: Optional[float] = None
    target_price_optimistic: Optional[float] = None
    target_price_neutral: Optional[float] = None
    target_price_pessimistic: Optional[float] = None
    source_count: Optional[int] = None
    peg: Optional[float] = None
    upside_optimistic: Optional[float] = None
    upside_neutral: Optional[float] = None
    upside_pessimistic: Optional[float] = None

    class Config:
        from_attributes = True


class ForecastSourceResponse(BaseModel):
    institution_name: str
    target_price: Optional[float] = None
    rating: Optional[str] = None
    report_date: Optional[date] = None
