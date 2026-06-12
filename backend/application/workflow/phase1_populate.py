"""Phase 1: Populate Entities - 实体填充工作流"""
from uuid import UUID
from typing import Dict, Any

from domain.entities import Stock, Sector, FinancialQuality, Valuation, Growth, Risk
from application.ai_agent.sector_analyzer import SectorAnalyzer


class Phase1Populate:
    """Phase 1: 填充所有实体数据"""

    def __init__(self):
        self.sector_analyzer = SectorAnalyzer()

    async def populate_stock(self, ticker: str, name: str, exchange: str, industry: str = None, market_cap: float = None) -> Stock:
        """填充 Stock 实体"""
        return Stock(
            ticker=ticker,
            name=name,
            exchange=exchange,
            industry=industry,
            market_cap=market_cap,
        )

    async def populate_sector(self, stock_id: UUID, industry: str, ticker: str) -> Sector:
        """填充 Sector 实体 (A+D 四维分析)"""
        sector = Sector(stock_id=stock_id)
        
        # AI Agent 执行四维分析
        analysis = await self.sector_analyzer.full_sector_analysis(industry, ticker)
        
        # 填充五力
        ff = analysis["five_forces"]
        sector.five_forces.supplier_power = ff["supplier_power"]
        sector.five_forces.buyer_power = ff["buyer_power"]
        sector.five_forces.threat_entrants = ff["threat_entrants"]
        sector.five_forces.threat_substitutes = ff["threat_substitutes"]
        sector.five_forces.rivalry_intensity = ff["rivalry_intensity"]
        sector.five_forces.switching_cost = ff["switching_cost"]
        
        # 填充生命周期
        lc = analysis["lifecycle"]
        sector.lifecycle.lifecycle_stage = lc["lifecycle_stage"]
        sector.lifecycle.segment_growth_rate = lc["segment_growth_rate"]
        sector.lifecycle.segment_penetration = lc["segment_penetration"]
        
        # 填充壁垒
        eb = analysis["barriers"]
        sector.barriers.barrier_economies_of_scale = eb["economies_of_scale"]
        sector.barriers.barrier_product_diff = eb["product_diff"]
        sector.barriers.barrier_capital_req = eb["capital_req"]
        sector.barriers.barrier_switching_cost = eb["switching_cost"]
        sector.barriers.barrier_sustainability = eb["sustainability"]
        
        # 填充战略
        cp = analysis["strategy"]
        sector.strategy.generic_strategy = cp["generic_strategy"]
        sector.strategy.strategy_consistency = cp["strategy_consistency"]
        
        return sector

    async def populate_financial(self, stock_id: UUID, data: dict) -> FinancialQuality:
        """填充 FinancialQuality 实体"""
        return FinancialQuality(
            stock_id=stock_id,
            roe=data.get("roe"),
            net_margin=data.get("net_margin"),
            asset_turnover=data.get("asset_turnover"),
            equity_multiplier=data.get("equity_multiplier"),
            debt_ratio=data.get("debt_ratio"),
            fcf_positive_3y=data.get("fcf_positive_3y"),
        )

    async def populate_valuation(self, stock_id: UUID, data: dict) -> Valuation:
        """填充 Valuation 实体"""
        return Valuation(
            stock_id=stock_id,
            pe_ttm=data.get("pe_ttm"),
            pb=data.get("pb"),
            peg=data.get("peg"),
            pe_percentile_5y=data.get("pe_percentile_5y"),
            dcf_low=data.get("dcf_low"),
            dcf_high=data.get("dcf_high"),
            margin_of_safety=data.get("margin_of_safety"),
        )

    async def populate_growth(self, stock_id: UUID, data: dict) -> Growth:
        """填充 Growth 实体"""
        return Growth(
            stock_id=stock_id,
            revenue_growth_3y_cagr=data.get("revenue_growth_3y_cagr"),
            earnings_growth_3y_cagr=data.get("earnings_growth_3y_cagr"),
            fcf_growth_3y_cagr=data.get("fcf_growth_3y_cagr"),
            consensus_growth_next_2y=data.get("consensus_growth_next_2y"),
        )

    async def populate_risk(self, stock_id: UUID, data: dict) -> Risk:
        """填充 Risk 实体"""
        return Risk(
            stock_id=stock_id,
            beta=data.get("beta"),
            debt_to_equity=data.get("debt_to_equity"),
            interest_coverage=data.get("interest_coverage"),
            industry_cyclicality=data.get("industry_cyclicality"),
            policy_risk=data.get("policy_risk"),
            governance_flags=data.get("governance_flags", []),
        )
