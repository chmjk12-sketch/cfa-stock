"""Screen Router - 股票筛选 API"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc, asc

from infrastructure.database.connection import get_async_session
from infrastructure.database.models import (
    StockModel, MarketDataModel, InstitutionalForecastModel, ConclusionModel
)
from api.schemas.screen_schema import ScreenRequest, ScreenResponse, ScreenStockItem

router = APIRouter(prefix="/screen", tags=["screen"])


@router.post("/", response_model=ScreenResponse)
async def screen_stocks(
    request: ScreenRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """多条件筛选股票"""
    # 基础查询
    subq = (
        select(
            MarketDataModel.ticker,
            MarketDataModel.latest_price,
            MarketDataModel.change_pct,
            func.row_number()
            .over(partition_by=MarketDataModel.ticker, order_by=desc(MarketDataModel.trade_date))
            .label("rn")
        ).subquery()
    )

    latest_market = select(subq.c.ticker, subq.c.latest_price, subq.c.change_pct).where(subq.c.rn == 1).subquery()

    subq2 = (
        select(
            InstitutionalForecastModel.ticker,
            InstitutionalForecastModel.peg,
            InstitutionalForecastModel.net_profit_growth,
            InstitutionalForecastModel.revenue_growth,
            InstitutionalForecastModel.target_price_neutral,
            InstitutionalForecastModel.upside_neutral,
            func.row_number()
            .over(partition_by=InstitutionalForecastModel.ticker, order_by=desc(InstitutionalForecastModel.report_date))
            .label("rn")
        ).subquery()
    )

    latest_forecast = select(
        subq2.c.ticker, subq2.c.peg, subq2.c.net_profit_growth,
        subq2.c.revenue_growth, subq2.c.target_price_neutral, subq2.c.upside_neutral
    ).where(subq2.c.rn == 1).subquery()

    query = (
        select(StockModel, latest_market, latest_forecast, ConclusionModel)
        .outerjoin(latest_market, StockModel.ticker == latest_market.c.ticker)
        .outerjoin(latest_forecast, StockModel.ticker == latest_forecast.c.ticker)
        .outerjoin(ConclusionModel, StockModel.id == ConclusionModel.stock_id)
    )

    conditions = []

    if request.sectors:
        conditions.append(StockModel.industry.in_(request.sectors))

    if request.peg_range and len(request.peg_range) == 2:
        conditions.append(
            and_(
                latest_forecast.c.peg >= request.peg_range[0],
                latest_forecast.c.peg <= request.peg_range[1]
            )
        )

    if request.net_profit_growth_min is not None:
        conditions.append(latest_forecast.c.net_profit_growth >= request.net_profit_growth_min)

    if request.revenue_growth_min is not None:
        conditions.append(latest_forecast.c.revenue_growth >= request.revenue_growth_min)

    if request.rating:
        conditions.append(ConclusionModel.rating == request.rating.upper())

    if conditions:
        query = query.where(and_(*conditions))

    # Count
    count_subq = query.subquery()
    count_result = await db.execute(select(func.count()).select_from(count_subq))
    total = count_result.scalar() or 0

    # Sort
    sort_map = {
        "peg": latest_forecast.c.peg,
        "net_profit_growth": latest_forecast.c.net_profit_growth,
        "latest_price": latest_market.c.latest_price,
        "composite_score": ConclusionModel.composite_score,
    }
    sort_col = sort_map.get(request.sort_by, latest_forecast.c.peg)
    if request.sort_order == "desc":
        query = query.order_by(desc(sort_col))
    else:
        query = query.order_by(asc(sort_col))

    # Pagination
    skip = (request.page - 1) * request.page_size
    query = query.offset(skip).limit(request.page_size)

    result = await db.execute(query)
    rows = result.all()

    stocks = []
    for stock, market, forecast, conclusion in rows:
        stocks.append(ScreenStockItem(
            ticker=stock.ticker,
            name=stock.name,
            sector=stock.industry,
            latest_price=market.latest_price if market else None,
            change_pct=market.change_pct if market else None,
            peg=forecast.peg if forecast else None,
            net_profit_growth=forecast.net_profit_growth if forecast else None,
            target_price_neutral=forecast.target_price_neutral if forecast else None,
            upside_neutral=forecast.upside_neutral if forecast else None,
            rating=conclusion.rating if conclusion else None,
            composite_score=conclusion.composite_score if conclusion else None,
        ))

    return ScreenResponse(total=total, page=request.page, page_size=request.page_size, stocks=stocks)


@router.get("/dimensions")
async def get_dimensions():
    """获取可筛选维度列表"""
    return {
        "sectors": ["AI光模块", "AI服务器", "存储/MCU", "电子制造", "AI芯片", "面板显示", "化合物半导体"],
        "ratings": ["BUY", "HOLD", "SELL"],
        "sort_options": [
            {"value": "peg", "label": "PEG"},
            {"value": "net_profit_growth", "label": "净利润增速"},
            {"value": "latest_price", "label": "现价"},
            {"value": "composite_score", "label": "综合评分"},
        ]
    }
