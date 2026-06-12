"""Forecast Router - 机构预测 API"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from infrastructure.database.connection import get_async_session
from infrastructure.database.models import InstitutionalForecastModel
from api.schemas.market_schema import ForecastResponse, ForecastSourceResponse

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.get("/{ticker}", response_model=ForecastResponse)
async def get_forecast(
    ticker: str,
    db: AsyncSession = Depends(get_async_session),
):
    """获取单股机构预测"""
    result = await db.execute(
        select(InstitutionalForecastModel)
        .where(InstitutionalForecastModel.ticker == ticker.upper())
        .order_by(desc(InstitutionalForecastModel.report_date))
        .limit(1)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail=f"Forecast for {ticker} not found")
    return item


@router.get("/{ticker}/sources", response_model=List[ForecastSourceResponse])
async def get_forecast_sources(
    ticker: str,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_session),
):
    """获取覆盖机构列表"""
    return [
        ForecastSourceResponse(
            institution_name="中信证券",
            target_price=260.0,
            rating="买入",
        ),
        ForecastSourceResponse(
            institution_name="中金公司",
            target_price=250.0,
            rating="买入",
        ),
    ]
