"""SQLAlchemy Models - 数据库模型"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column, String, Float, Boolean, Integer, DateTime, 
    ForeignKey, Text, JSON, ARRAY, create_engine
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class StockModel(Base):
    __tablename__ = "stocks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    ticker = Column(String(20), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    exchange = Column(String(20), nullable=False)
    industry = Column(String(100))
    market_cap = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    sector = relationship("SectorModel", back_populates="stock", uselist=False)
    financial_quality = relationship("FinancialQualityModel", back_populates="stock", uselist=False)
    valuation = relationship("ValuationModel", back_populates="stock", uselist=False)
    growth = relationship("GrowthModel", back_populates="stock", uselist=False)
    risk = relationship("RiskModel", back_populates="stock", uselist=False)
    conclusion = relationship("ConclusionModel", back_populates="stock", uselist=False)


class SectorModel(Base):
    __tablename__ = "sectors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    
    # Five Forces
    ff_score = Column(Integer)
    ff_supplier_power = Column(String(10))
    ff_buyer_power = Column(String(10))
    ff_threat_entrants = Column(String(10))
    ff_threat_substitutes = Column(String(10))
    ff_rivalry_intensity = Column(String(10))
    ff_switching_cost = Column(String(10))
    ff_raw = Column(JSON)
    
    # Lifecycle
    lc_score = Column(Integer)
    lc_stage = Column(String(20))
    lc_segment_growth_rate = Column(Float)
    lc_segment_penetration = Column(Float)
    lc_risk = Column(Text)
    lc_raw = Column(JSON)
    
    # Barriers
    eb_score = Column(Integer)
    eb_economies_of_scale = Column(Integer)
    eb_product_diff = Column(Integer)
    eb_capital_req = Column(Integer)
    eb_switching_cost = Column(Integer)
    eb_sustainability = Column(String(10))
    eb_raw = Column(JSON)
    
    # Strategy
    cp_score = Column(Integer)
    cp_generic_strategy = Column(String(20))
    cp_strategy_consistency = Column(String(10))
    cp_moat_from_strategy = Column(String(10))
    cp_raw = Column(JSON)
    
    # Aggregate
    score = Column(Integer)
    raw_analysis = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    stock = relationship("StockModel", back_populates="sector")


class FinancialQualityModel(Base):
    __tablename__ = "financial_qualities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    
    roe = Column(Float)
    net_margin = Column(Float)
    asset_turnover = Column(Float)
    equity_multiplier = Column(Float)
    debt_ratio = Column(Float)
    fcf_positive_3y = Column(Boolean)
    
    score = Column(Integer)
    raw_data = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    stock = relationship("StockModel", back_populates="financial_quality")


class ValuationModel(Base):
    __tablename__ = "valuations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    
    pe_ttm = Column(Float)
    pb = Column(Float)
    peg = Column(Float)
    pe_percentile_5y = Column(Float)
    dcf_low = Column(Float)
    dcf_high = Column(Float)
    margin_of_safety = Column(Float)
    
    score = Column(Integer)
    raw_data = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    stock = relationship("StockModel", back_populates="valuation")


class GrowthModel(Base):
    __tablename__ = "growths"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    
    revenue_growth_3y_cagr = Column(Float)
    earnings_growth_3y_cagr = Column(Float)
    fcf_growth_3y_cagr = Column(Float)
    consensus_growth_next_2y = Column(Float)
    moat_assessment = Column(String(10))
    
    score = Column(Integer)
    raw_data = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    stock = relationship("StockModel", back_populates="growth")


class RiskModel(Base):
    __tablename__ = "risks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    
    beta = Column(Float)
    debt_to_equity = Column(Float)
    interest_coverage = Column(Float)
    industry_cyclicality = Column(String(10))
    policy_risk = Column(String(10))
    governance_flags = Column(JSON)
    
    score = Column(Integer)
    raw_data = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    stock = relationship("StockModel", back_populates="risk")


class ConclusionModel(Base):
    __tablename__ = "conclusions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    
    composite_score = Column(Float)
    rating = Column(String(10))
    conviction = Column(String(10))
    target_price_low = Column(Float)
    target_price_high = Column(Float)
    
    sector_score = Column(Integer)
    financial_score = Column(Integer)
    valuation_score = Column(Integer)
    growth_score = Column(Integer)
    risk_score = Column(Integer)
    
    reasoning_chain = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    stock = relationship("StockModel", back_populates="conclusion")


class OpportunityModel(Base):
    __tablename__ = "opportunities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    theme = Column(String(100), nullable=False)
    industry = Column(String(100))
    opportunity_score = Column(Float)
    stock_ids = Column(ARRAY(UUID(as_uuid=True)))
    risks = Column(Text)
    conclusion = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AnalysisTaskModel(Base):
    __tablename__ = "analysis_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    task_type = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    celery_task_id = Column(String(100))
    result = Column(JSON)
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
