"""FastAPI Main Application"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import stocks, analysis, opportunities, market, screen, forecast


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    from application.scheduler import start_scheduler
    start_scheduler()
    yield
    from application.scheduler import shutdown_scheduler
    shutdown_scheduler()


app = FastAPI(
    title="CFA Stock Ontology API",
    description="CFA 选股分析平台 API",
    version="2.0.0",
    redirect_slashes=False,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(stocks.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(opportunities.router, prefix="/api")
app.include_router(market.router, prefix="/api")
app.include_router(screen.router, prefix="/api")
app.include_router(forecast.router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "2.0.0"}


@app.get("/")
async def root():
    return {
        "message": "CFA Stock Ontology API",
        "version": "2.0.0",
        "docs": "/docs",
    }
