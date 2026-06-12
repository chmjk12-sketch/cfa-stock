"""Seed Mock Data - 初始化 Mock 数据"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from uuid import uuid4
from infrastructure.database.connection import get_sync_session
from infrastructure.database.models import (
    StockModel, SectorModel, FinancialQualityModel, ValuationModel,
    GrowthModel, RiskModel, ConclusionModel
)


def seed_data():
    """Seed mock data into database"""
    db = get_sync_session()
    
    try:
        # Clear existing data
        db.query(ConclusionModel).delete()
        db.query(RiskModel).delete()
        db.query(GrowthModel).delete()
        db.query(ValuationModel).delete()
        db.query(FinancialQualityModel).delete()
        db.query(SectorModel).delete()
        db.query(StockModel).delete()
        db.commit()
        
        # Create stocks
        stocks_data = [
            {
                "ticker": "300476.SZ",
                "name": "胜宏科技",
                "exchange": "SZ",
                "industry": "电子/PCB",
                "market_cap": 2800000000,
            },
            {
                "ticker": "002463.SZ",
                "name": "沪电股份",
                "exchange": "SZ",
                "industry": "电子/PCB",
                "market_cap": 3200000000,
            },
            {
                "ticker": "600183.SH",
                "name": "生益科技",
                "exchange": "SH",
                "industry": "电子/PCB",
                "market_cap": 4500000000,
            },
        ]
        
        for stock_info in stocks_data:
            stock = StockModel(
                id=uuid4(),
                ticker=stock_info["ticker"],
                name=stock_info["name"],
                exchange=stock_info["exchange"],
                industry=stock_info["industry"],
                market_cap=stock_info["market_cap"],
            )
            db.add(stock)
            db.flush()
            
            # Create Sector
            sector = SectorModel(
                id=uuid4(),
                stock_id=stock.id,
                ff_score=9,
                ff_supplier_power="low",
                ff_buyer_power="medium",
                ff_threat_entrants="low",
                ff_threat_substitutes="medium",
                ff_rivalry_intensity="medium",
                ff_switching_cost="high",
                lc_score=9,
                lc_stage="growth",
                lc_segment_growth_rate=25.0,
                lc_segment_penetration=0.28,
                eb_score=9,
                eb_economies_of_scale=4,
                eb_product_diff=5,
                eb_capital_req=4,
                eb_switching_cost=4,
                eb_sustainability="high",
                cp_score=9,
                cp_generic_strategy="differentiation",
                cp_strategy_consistency="high",
                cp_moat_from_strategy="wide",
                score=9,
            )
            db.add(sector)
            
            # Create Financial Quality
            fq = FinancialQualityModel(
                id=uuid4(),
                stock_id=stock.id,
                roe=18.5,
                net_margin=12.3,
                asset_turnover=0.85,
                equity_multiplier=1.76,
                debt_ratio=43.2,
                fcf_positive_3y=True,
                score=8,
            )
            db.add(fq)
            
            # Create Valuation
            valuation = ValuationModel(
                id=uuid4(),
                stock_id=stock.id,
                pe_ttm=28.5,
                pb=4.2,
                peg=0.95,
                pe_percentile_5y=35.0,
                dcf_low=45.2,
                dcf_high=62.8,
                margin_of_safety=17.4,
                score=8,
            )
            db.add(valuation)
            
            # Create Growth
            growth = GrowthModel(
                id=uuid4(),
                stock_id=stock.id,
                revenue_growth_3y_cagr=32.5,
                earnings_growth_3y_cagr=28.3,
                fcf_growth_3y_cagr=25.1,
                consensus_growth_next_2y=30.2,
                moat_assessment="wide",
                score=9,
            )
            db.add(growth)
            
            # Create Risk
            risk = RiskModel(
                id=uuid4(),
                stock_id=stock.id,
                beta=1.15,
                debt_to_equity=0.45,
                interest_coverage=8.5,
                industry_cyclicality="medium",
                policy_risk="low",
                governance_flags=[],
                score=7,
            )
            db.add(risk)
            
            # Create Conclusion
            conclusion = ConclusionModel(
                id=uuid4(),
                stock_id=stock.id,
                composite_score=8.5,
                rating="buy",
                conviction="high",
                target_price_low=45.2,
                target_price_high=62.8,
                sector_score=9,
                financial_score=8,
                valuation_score=8,
                growth_score=9,
                risk_score=7,
                reasoning_chain={
                    "step1_sector": {
                        "description": "经济/行业分析",
                        "five_forces": {"score": 9, "details": "五力格局良好"},
                        "lifecycle": {"score": 9, "details": "成长期"},
                        "barriers": {"score": 9, "details": "壁垒高"},
                        "strategy": {"score": 9, "details": "差异化战略"},
                    },
                    "step6_conclusion": {
                        "description": "投资决策",
                        "composite_score": 8.5,
                        "rating": "buy",
                        "conviction": "high",
                    },
                },
            )
            db.add(conclusion)
        
        db.commit()
        print("✅ Mock data seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
