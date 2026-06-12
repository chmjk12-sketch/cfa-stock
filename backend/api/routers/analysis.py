"""Analysis Router - 分析相关 API"""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from infrastructure.database.connection import get_async_session
from infrastructure.database.models import (
    StockModel, SectorModel, FinancialQualityModel, ValuationModel,
    GrowthModel, RiskModel, ConclusionModel
)
from api.schemas.analysis_schema import StockAnalysisResponse

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/{ticker}/full", response_model=StockAnalysisResponse)
async def get_full_analysis(
    ticker: str,
    db: AsyncSession = Depends(get_async_session),
):
    """获取股票完整分析"""
    # Get stock
    stock_result = await db.execute(
        select(StockModel).where(StockModel.ticker == ticker.upper())
    )
    stock = stock_result.scalar_one_or_none()
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
    
    # Get all related entities
    sector_result = await db.execute(
        select(SectorModel).where(SectorModel.stock_id == stock.id)
    )
    sector = sector_result.scalar_one_or_none()
    
    fq_result = await db.execute(
        select(FinancialQualityModel).where(FinancialQualityModel.stock_id == stock.id)
    )
    fq = fq_result.scalar_one_or_none()
    
    valuation_result = await db.execute(
        select(ValuationModel).where(ValuationModel.stock_id == stock.id)
    )
    valuation = valuation_result.scalar_one_or_none()
    
    growth_result = await db.execute(
        select(GrowthModel).where(GrowthModel.stock_id == stock.id)
    )
    growth = growth_result.scalar_one_or_none()
    
    risk_result = await db.execute(
        select(RiskModel).where(RiskModel.stock_id == stock.id)
    )
    risk = risk_result.scalar_one_or_none()
    
    conclusion_result = await db.execute(
        select(ConclusionModel).where(ConclusionModel.stock_id == stock.id)
    )
    conclusion = conclusion_result.scalar_one_or_none()
    
    if not all([sector, fq, valuation, growth, risk, conclusion]):
        raise HTTPException(status_code=404, detail=f"Analysis for {ticker} not complete")
    
    # Transform flat sector model into nested schema structure
    sector_nested = {
        "id": sector.id,
        "stock_id": sector.stock_id,
        "five_forces": {
            "supplier_power": sector.ff_supplier_power,
            "buyer_power": sector.ff_buyer_power,
            "threat_entrants": sector.ff_threat_entrants,
            "threat_substitutes": sector.ff_threat_substitutes,
            "rivalry_intensity": sector.ff_rivalry_intensity,
            "switching_cost": sector.ff_switching_cost,
            "score": sector.ff_score or 0,
        },
        "lifecycle": {
            "lifecycle_stage": sector.lc_stage,
            "segment_growth_rate": sector.lc_segment_growth_rate,
            "segment_penetration": sector.lc_segment_penetration,
            "lifecycle_risk": sector.lc_risk,
            "score": sector.lc_score or 0,
        },
        "barriers": {
            "economies_of_scale": sector.eb_economies_of_scale or 0,
            "product_diff": sector.eb_product_diff or 0,
            "capital_req": sector.eb_capital_req or 0,
            "switching_cost": sector.eb_switching_cost or 0,
            "sustainability": sector.eb_sustainability,
            "score": sector.eb_score or 0,
        },
        "strategy": {
            "generic_strategy": sector.cp_generic_strategy,
            "strategy_consistency": sector.cp_strategy_consistency,
            "moat_from_strategy": sector.cp_moat_from_strategy,
            "score": sector.cp_score or 0,
        },
        "score": sector.score or 0,
    }
    
    return StockAnalysisResponse(
        stock={
            "id": str(stock.id),
            "ticker": stock.ticker,
            "name": stock.name,
            "exchange": stock.exchange,
            "industry": stock.industry,
            "market_cap": stock.market_cap,
        },
        sector=sector_nested,
        financial_quality=fq,
        valuation=valuation,
        growth=growth,
        risk=risk,
        conclusion=conclusion,
        reasoning_log=conclusion.reasoning_chain.get("log", []) if conclusion.reasoning_chain else [],
    )


@router.post("/{ticker}/trigger")
async def trigger_analysis(
    ticker: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_session),
):
    """触发股票分析（异步）"""
    # Check if stock exists
    result = await db.execute(
        select(StockModel).where(StockModel.ticker == ticker.upper())
    )
    stock = result.scalar_one_or_none()
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
    
    # TODO: Trigger Celery task
    return {"message": f"Analysis triggered for {ticker}", "stock_id": str(stock.id)}
