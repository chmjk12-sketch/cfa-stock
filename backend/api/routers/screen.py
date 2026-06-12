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
    # 先获取所有股票
    query = select(StockModel)
    conditions = []

    if request.sectors:
        conditions.append(StockModel.industry.in_(request.sectors))

    if conditions:
        query = query.where(and_(*conditions))

    result = await db.execute(query)
    stocks = result.scalars().all()

    # 为每只股票获取最新行情和预测
    items = []
    for stock in stocks:
        # 获取最新行情
        mkt_result = await db.execute(
            select(MarketDataModel)
            .where(MarketDataModel.ticker == stock.ticker)
            .order_by(desc(MarketDataModel.trade_date))
            .limit(1)
        )
        market = mkt_result.scalar_one_or_none()

        # 获取最新预测
        fc_result = await db.execute(
            select(InstitutionalForecastModel)
            .where(InstitutionalForecastModel.ticker == stock.ticker)
            .order_by(desc(InstitutionalForecastModel.report_date))
            .limit(1)
        )
        forecast = fc_result.scalar_one_or_none()

        # 获取评级
        conc_result = await db.execute(
            select(ConclusionModel)
            .where(ConclusionModel.stock_id == stock.id)
            .order_by(desc(ConclusionModel.updated_at))
            .limit(1)
        )
        conclusion = conc_result.scalar_one_or_none()

        # 应用筛选条件
        if request.peg_range and len(request.peg_range) == 2:
            peg_val = forecast.peg if forecast else None
            if peg_val is None or peg_val < request.peg_range[0] or peg_val > request.peg_range[1]:
                continue

        if request.net_profit_growth_min is not None:
            npg = forecast.net_profit_growth if forecast else None
            if npg is None or npg < request.net_profit_growth_min:
                continue

        if request.revenue_growth_min is not None:
            rg = forecast.revenue_growth if forecast else None
            if rg is None or rg < request.revenue_growth_min:
                continue

        if request.rating:
            rating = conclusion.rating if conclusion else None
            if rating != request.rating.upper():
                continue

        items.append(ScreenStockItem(
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

    # 排序
    sort_key = request.sort_by or "peg"
    reverse = request.sort_order == "desc"
    items.sort(
        key=lambda x: getattr(x, sort_key) if getattr(x, sort_key) is not None else float('inf'),
        reverse=reverse
    )

    total = len(items)

    # 分页
    page = request.page or 1
    page_size = request.page_size or 50
    start = (page - 1) * page_size
    paginated = items[start:start + page_size]

    return ScreenResponse(total=total, page=page, page_size=page_size, stocks=paginated)


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
