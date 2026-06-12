"""Opportunities Router - 投资机会 API"""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from infrastructure.database.connection import get_async_session
from infrastructure.database.models import OpportunityModel, ConclusionModel, StockModel
from api.schemas.analysis_schema import OpportunityResponse

router = APIRouter(prefix="/opportunities", tags=["opportunities"])


@router.get("/", response_model=List[OpportunityResponse])
async def list_opportunities(
    limit: int = Query(10, ge=1, le=50),
    industry: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session),
):
    """获取投资机会列表"""
    query = select(OpportunityModel).order_by(desc(OpportunityModel.opportunity_score))
    if industry:
        query = query.where(OpportunityModel.industry == industry)
    
    query = query.limit(limit)
    result = await db.execute(query)
    opportunities = result.scalars().all()
    
    return opportunities


@router.get("/top")
async def get_top_opportunities(
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_async_session),
):
    """获取 top 投资机会（综合评分最高的股票）"""
    query = select(
        StockModel, ConclusionModel
    ).join(
        ConclusionModel, StockModel.id == ConclusionModel.stock_id
    ).where(
        ConclusionModel.rating == "buy"
    ).order_by(
        desc(ConclusionModel.composite_score)
    ).limit(limit)
    
    result = await db.execute(query)
    rows = result.all()
    
    return [
        {
            "stock": {
                "id": str(stock.id),
                "ticker": stock.ticker,
                "name": stock.name,
                "industry": stock.industry,
            },
            "composite_score": conclusion.composite_score,
            "rating": conclusion.rating,
            "conviction": conclusion.conviction,
            "target_price": [conclusion.target_price_low, conclusion.target_price_high],
        }
        for stock, conclusion in rows
    ]
