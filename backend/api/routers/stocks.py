"""Stocks Router - 股票相关 API"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from infrastructure.database.connection import get_async_session
from infrastructure.database.models import StockModel, ConclusionModel
from api.schemas.stock_schema import StockResponse, StockSearchResult, StockListResponse

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/search", response_model=List[StockSearchResult])
async def search_stocks(
    q: str = Query(..., description="搜索关键词"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_async_session),
):
    """搜索股票"""
    query = select(StockModel, ConclusionModel).outerjoin(
        ConclusionModel, StockModel.id == ConclusionModel.stock_id
    ).where(
        (StockModel.ticker.ilike(f"%{q}%")) | 
        (StockModel.name.ilike(f"%{q}%"))
    ).limit(limit)
    
    result = await db.execute(query)
    rows = result.all()
    
    return [
        StockSearchResult(
            id=stock.id,
            ticker=stock.ticker,
            name=stock.name,
            exchange=stock.exchange,
            industry=stock.industry,
            composite_score=conclusion.composite_score if conclusion else None,
            rating=conclusion.rating if conclusion else None,
        )
        for stock, conclusion in rows
    ]


@router.get("/{ticker}", response_model=StockResponse)
async def get_stock(
    ticker: str,
    db: AsyncSession = Depends(get_async_session),
):
    """获取股票详情"""
    result = await db.execute(
        select(StockModel).where(StockModel.ticker == ticker.upper())
    )
    stock = result.scalar_one_or_none()
    
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
    
    return stock


@router.get("/", response_model=StockListResponse)
async def list_stocks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    industry: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session),
):
    """获取股票列表"""
    query = select(StockModel)
    if industry:
        query = query.where(StockModel.industry == industry)
    
    # Count total
    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar()
    
    # Get items
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return StockListResponse(total=total, items=items)
