"""
CFA Stock Ontology - 生产环境入口
整合 FastAPI API + 前端静态文件
"""
import os
import sys
import json
import uuid as uuid_module
import sqlalchemy
from sqlalchemy import TypeDecorator, String as SAString, Text as SAText, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# ── 路径 ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# ── SQLite 兼容类型 ──
class SQLiteUUID(TypeDecorator):
    impl = SAString(36)
    cache_ok = True
    def load_dialect_impl(self, dialect):
        if dialect.name == "sqlite":
            return dialect.type_descriptor(SAString(36))
        from sqlalchemy.dialects.postgresql import UUID as PG_UUID
        return dialect.type_descriptor(PG_UUID())
    def process_bind_param(self, value, dialect):
        if value is None: return None
        return str(value)
    def process_result_value(self, value, dialect):
        if value is None: return None
        if isinstance(value, uuid_module.UUID): return value
        try: return uuid_module.UUID(value)
        except: return value

class SQLiteJSON(TypeDecorator):
    impl = SAText
    cache_ok = True
    def load_dialect_impl(self, dialect):
        if dialect.name == "sqlite":
            return dialect.type_descriptor(SAText())
        return dialect.type_descriptor(sqlalchemy.JSON())
    def process_bind_param(self, value, dialect):
        if value is None: return None
        return json.dumps(value) if not isinstance(value, str) else value
    def process_result_value(self, value, dialect):
        if value is None: return None
        if isinstance(value, str):
            try: return json.loads(value)
            except: return value
        return value

# ── 数据库初始化 ──
DB_PATH = os.path.join(BASE_DIR, "cfa_prod.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

sync_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SyncSessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

ASYNC_URL = f"sqlite+aiosqlite:///{DB_PATH}"
async_engine = create_async_engine(ASYNC_URL, connect_args={"check_same_thread": False})
AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session

# ── 打补丁：替换数据库中 PostgreSQL 类型 ──
import infrastructure.database.models as db_models
for table_class in db_models.Base.registry._class_registry.values():
    if hasattr(table_class, '__table__'):
        for col in table_class.__table__.columns:
            if hasattr(col.type, '__visit_name__'):
                vname = col.type.__visit_name__
                if vname == 'UUID':
                    col.type = SQLiteUUID()
                elif vname == 'JSON':
                    col.type = SQLiteJSON()
                elif vname == 'ARRAY':
                    col.type = SQLiteJSON()

# ── 创建表 ──
db_models.Base.metadata.create_all(bind=sync_engine)

# ── 打补丁到 connection 模块 ──
import infrastructure.database.connection as conn_mod
import importlib
os.environ["DATABASE_URL"] = DATABASE_URL
importlib.reload(conn_mod)
conn_mod.get_async_session = get_async_session
conn_mod.SyncSessionLocal = SyncSessionLocal
conn_mod.AsyncSessionLocal = AsyncSessionLocal
conn_mod.sync_engine = sync_engine
conn_mod.async_engine = async_engine

# 也打补丁到 routers
import api.routers.stocks, api.routers.analysis, api.routers.opportunities, api.routers.market, api.routers.screen, api.routers.forecast
for mod in [api.routers.stocks, api.routers.analysis, api.routers.opportunities, api.routers.market, api.routers.screen, api.routers.forecast]:
    if hasattr(mod, 'get_async_session'):
        mod.get_async_session = get_async_session

# ── 种子数据（仅首次运行） ──
def seed_data():
    from infrastructure.database.models import (
        StockModel, SectorModel, FinancialQualityModel, ValuationModel,
        GrowthModel, RiskModel, ConclusionModel, OpportunityModel
    )
    from uuid import uuid4

    db = SyncSessionLocal()
    try:
        existing = db.query(StockModel).count()
        if existing > 0:
            return  # Already seeded

        stocks_data = [
            {"ticker": "300476.SZ", "name": "胜宏科技", "exchange": "SZ", "industry": "电子/PCB", "market_cap": 2800000000},
            {"ticker": "002463.SZ", "name": "沪电股份", "exchange": "SZ", "industry": "电子/PCB", "market_cap": 3200000000},
            {"ticker": "600183.SH", "name": "生益科技", "exchange": "SH", "industry": "电子/PCB", "market_cap": 4500000000},
            {"ticker": "300474.SZ", "name": "景嘉微", "exchange": "SZ", "industry": "半导体", "market_cap": 1800000000},
            {"ticker": "300308.SZ", "name": "中际旭创", "exchange": "SZ", "industry": "光模块", "market_cap": 5200000000},
        ]

        for sd in stocks_data:
            stock = StockModel(id=uuid4(), **sd)
            db.add(stock)
            db.flush()

            db.add(SectorModel(id=uuid4(), stock_id=stock.id,
                ff_score=9, ff_supplier_power="low", ff_buyer_power="medium",
                ff_threat_entrants="low", ff_threat_substitutes="medium",
                ff_rivalry_intensity="medium", ff_switching_cost="high",
                lc_score=9, lc_stage="growth", lc_segment_growth_rate=25.0, lc_segment_penetration=0.28,
                eb_score=9, eb_economies_of_scale=4, eb_product_diff=5, eb_capital_req=4, eb_switching_cost=4, eb_sustainability="high",
                cp_score=9, cp_generic_strategy="differentiation", cp_strategy_consistency="high", cp_moat_from_strategy="wide",
                score=9))
            db.add(FinancialQualityModel(id=uuid4(), stock_id=stock.id,
                roe=18.5, net_margin=12.3, asset_turnover=0.85, equity_multiplier=1.76,
                debt_ratio=43.2, fcf_positive_3y=True, score=8))
            db.add(ValuationModel(id=uuid4(), stock_id=stock.id,
                pe_ttm=28.5, pb=4.2, peg=0.95, pe_percentile_5y=35.0,
                dcf_low=45.2, dcf_high=62.8, margin_of_safety=17.4, score=8))
            db.add(GrowthModel(id=uuid4(), stock_id=stock.id,
                revenue_growth_3y_cagr=32.5, earnings_growth_3y_cagr=28.3, fcf_growth_3y_cagr=25.1,
                consensus_growth_next_2y=30.2, moat_assessment="wide", score=9))
            db.add(RiskModel(id=uuid4(), stock_id=stock.id,
                beta=1.15, debt_to_equity=0.45, interest_coverage=8.5,
                industry_cyclicality="medium", policy_risk="low", governance_flags=[], score=7))

            rating = "buy" if sd["ticker"] in ["300476.SZ", "002463.SZ", "600183.SH"] else "hold"
            conviction = "high" if rating == "buy" else "medium"
            score = 9.2 if sd["ticker"] == "300476.SZ" else (8.7 if sd["ticker"] == "002463.SZ" else 8.0)
            db.add(ConclusionModel(id=uuid4(), stock_id=stock.id,
                composite_score=score, rating=rating, conviction=conviction,
                target_price_low=45.2, target_price_high=62.8,
                sector_score=9, financial_score=8, valuation_score=8, growth_score=9, risk_score=7,
                reasoning_chain={"step1_sector": {"description": "经济/行业分析", "score": 9},
                                 "step6_conclusion": {"description": "投资决策", "composite_score": score, "rating": rating}}))

        themes = [
            {"theme": "AI服务器PCB", "industry": "电子/PCB", "opportunity_score": 92},
            {"theme": "高端模拟IC", "industry": "半导体", "opportunity_score": 85},
            {"theme": "算力电源", "industry": "电力设备", "opportunity_score": 80},
            {"theme": "光模块", "industry": "通信", "opportunity_score": 78},
            {"theme": "半导体设备", "industry": "半导体", "opportunity_score": 75},
        ]
        for t in themes:
            db.add(OpportunityModel(id=uuid4(), theme=t["theme"], industry=t["industry"],
                opportunity_score=t["opportunity_score"], risks="行业竞争加剧", conclusion="建议关注龙头企业"))

        db.commit()
        db.close()
        print("✅ 种子数据已加载")
    except Exception as e:
        db.rollback()
        db.close()
        print(f"⚠️ 种子数据加载失败: {e}")

seed_data()

# ── FastAPI 应用 ──
app = FastAPI(
    title="CFA Stock Ontology API",
    description="CFA 选股分析平台 API",
    version="2.0.0",
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 路由
app.include_router(api.routers.stocks.router, prefix="/api")
app.include_router(api.routers.analysis.router, prefix="/api")
app.include_router(api.routers.opportunities.router, prefix="/api")
app.include_router(api.routers.market.router, prefix="/api")
app.include_router(api.routers.screen.router, prefix="/api")
app.include_router(api.routers.forecast.router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "2.0.0"}

@app.get("/api/health")
async def api_health():
    return {"status": "healthy"}

# 前端静态文件（API 路由优先，其余走静态文件）
FRONTEND_DIR = os.environ.get("FRONTEND_DIR", os.path.join(BASE_DIR, "frontend/out"))
if os.path.isdir(FRONTEND_DIR):
    from fastapi.responses import FileResponse
    import os as _os

    @app.get("/{path:path}")
    async def serve_spa(path: str):
        """SPA fallback: 先尝试精确文件，再尝试 .html，最后返回 index.html"""
        # 精确文件匹配
        file_path = _os.path.join(FRONTEND_DIR, path)
        if _os.path.isfile(file_path):
            return FileResponse(file_path)
        # 目录 + index.html
        if _os.path.isdir(file_path):
            index = _os.path.join(file_path, "index.html")
            if _os.path.isfile(index):
                return FileResponse(index)
        # .html 后缀匹配
        html_path = file_path + ".html"
        if _os.path.isfile(html_path):
            return FileResponse(html_path)
        # SPA fallback
        index = _os.path.join(FRONTEND_DIR, "index.html")
        if _os.path.isfile(index):
            return FileResponse(index)
        return FileResponse(_os.path.join(FRONTEND_DIR, "404.html"), status_code=404)

    # 静态资源（_next 目录）仍然用 StaticFiles 处理
    app.mount("/_next", StaticFiles(directory=_os.path.join(FRONTEND_DIR, "_next")), name="next_static")
    print(f"✅ 前端静态目录: {FRONTEND_DIR}")
else:
    print(f"⚠️ 前端静态目录不存在: {FRONTEND_DIR}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "80"))
    uvicorn.run(app, host="0.0.0.0", port=port)
