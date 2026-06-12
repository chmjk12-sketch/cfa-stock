"""Market Router - 实时行情 API"""
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from infrastructure.database.connection import get_async_session
from infrastructure.database.models import MarketDataModel, KlineDailyModel
from api.schemas.market_schema import MarketDataResponse, KlineResponse

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/realtime", response_model=List[MarketDataResponse])
async def get_realtime_market(
    tickers: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session),
):
    """获取实时行情，支持批量"""
    query = select(MarketDataModel).order_by(desc(MarketDataModel.trade_date))

    if tickers:
        ticker_list = [t.strip() for t in tickers.split(",")]
        query = query.where(MarketDataModel.ticker.in_(ticker_list))

    result = await db.execute(query)
    items = result.scalars().all()
    return items


@router.get("/realtime/{ticker}", response_model=MarketDataResponse)
async def get_stock_realtime(
    ticker: str,
    db: AsyncSession = Depends(get_async_session),
):
    """获取单股实时行情"""
    result = await db.execute(
        select(MarketDataModel)
        .where(MarketDataModel.ticker == ticker.upper())
        .order_by(desc(MarketDataModel.trade_date))
        .limit(1)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail=f"Market data for {ticker} not found")
    return item


@router.get("/kline/{ticker}", response_model=List[KlineResponse])
async def get_kline(
    ticker: str,
    period: str = "30d",
    db: AsyncSession = Depends(get_async_session),
):
    """获取历史 K 线"""
    days = int(period.replace("d", "")) if period.endswith("d") else 30
    start_date = datetime.now().date() - timedelta(days=days)

    result = await db.execute(
        select(KlineDailyModel)
        .where(
            KlineDailyModel.ticker == ticker.upper(),
            KlineDailyModel.trade_date >= start_date
        )
        .order_by(KlineDailyModel.trade_date)
    )
    items = result.scalars().all()
    return items
