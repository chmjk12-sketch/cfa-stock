"""Celery Tasks - 异步分析任务"""
import asyncio
from uuid import UUID

from infrastructure.data_pipeline.celery_tasks import celery_app
from infrastructure.database.connection import get_sync_session
from infrastructure.database.models import (
    StockModel, SectorModel, FinancialQualityModel, ValuationModel,
    GrowthModel, RiskModel, ConclusionModel
)
from application.workflow.phase1_populate import Phase1Populate
from application.workflow.phase2_traverse import Phase2Traverse
from application.workflow.phase3_conclude import Phase3Conclude


@celery_app.task(bind=True, max_retries=3)
def run_stock_analysis(self, ticker: str, stock_data: dict):
    """执行完整股票分析任务"""
    try:
        db = get_sync_session()
        
        # Phase 1: Populate
        phase1 = Phase1Populate()
        stock = asyncio.run(phase1.populate_stock(
            ticker=ticker,
            name=stock_data.get("name", ticker),
            exchange=stock_data.get("exchange", "SZ"),
            industry=stock_data.get("industry"),
            market_cap=stock_data.get("market_cap"),
        ))
        
        # Save stock
        stock_model = StockModel(
            id=stock.id,
            ticker=stock.ticker,
            name=stock.name,
            exchange=stock.exchange,
            industry=stock.industry,
            market_cap=stock.market_cap,
        )
        db.add(stock_model)
        db.commit()
        
        # Populate Sector
        sector = asyncio.run(phase1.populate_sector(stock.id, stock.industry, stock.ticker))
        sector_model = SectorModel(
            id=sector.id,
            stock_id=sector.stock_id,
            ff_score=sector.five_forces.score,
            ff_supplier_power=sector.five_forces.supplier_power,
            ff_buyer_power=sector.five_forces.buyer_power,
            ff_threat_entrants=sector.five_forces.threat_entrants,
            ff_threat_substitutes=sector.five_forces.threat_substitutes,
            ff_rivalry_intensity=sector.five_forces.rivalry_intensity,
            ff_switching_cost=sector.five_forces.switching_cost,
            lc_score=sector.lifecycle.score,
            lc_stage=sector.lifecycle.lifecycle_stage,
            lc_segment_growth_rate=sector.lifecycle.segment_growth_rate,
            lc_segment_penetration=sector.lifecycle.segment_penetration,
            eb_score=sector.barriers.score,
            eb_economies_of_scale=sector.barriers.barrier_economies_of_scale,
            eb_product_diff=sector.barriers.barrier_product_diff,
            eb_capital_req=sector.barriers.barrier_capital_req,
            eb_switching_cost=sector.barriers.barrier_switching_cost,
            eb_sustainability=sector.barriers.barrier_sustainability,
            cp_score=sector.strategy.score,
            cp_generic_strategy=sector.strategy.generic_strategy,
            cp_strategy_consistency=sector.strategy.strategy_consistency,
            cp_moat_from_strategy=sector.strategy.moat_from_strategy,
            score=sector.score,
        )
        db.add(sector_model)
        
        # Populate Financial
        fq = asyncio.run(phase1.populate_financial(stock.id, stock_data.get("financial", {})))
        fq_model = FinancialQualityModel(
            id=fq.id,
            stock_id=fq.stock_id,
            roe=fq.roe,
            net_margin=fq.net_margin,
            asset_turnover=fq.asset_turnover,
            equity_multiplier=fq.equity_multiplier,
            debt_ratio=fq.debt_ratio,
            fcf_positive_3y=fq.fcf_positive_3y,
            score=fq.score,
        )
        db.add(fq_model)
        
        # Populate Valuation
        valuation = asyncio.run(phase1.populate_valuation(stock.id, stock_data.get("valuation", {})))
        val_model = ValuationModel(
            id=valuation.id,
            stock_id=valuation.stock_id,
            pe_ttm=valuation.pe_ttm,
            pb=valuation.pb,
            peg=valuation.peg,
            pe_percentile_5y=valuation.pe_percentile_5y,
            dcf_low=valuation.dcf_low,
            dcf_high=valuation.dcf_high,
            margin_of_safety=valuation.margin_of_safety,
            score=valuation.score,
        )
        db.add(val_model)
        
        # Populate Growth
        growth = asyncio.run(phase1.populate_growth(stock.id, stock_data.get("growth", {})))
        growth_model = GrowthModel(
            id=growth.id,
            stock_id=growth.stock_id,
            revenue_growth_3y_cagr=growth.revenue_growth_3y_cagr,
            earnings_growth_3y_cagr=growth.earnings_growth_3y_cagr,
            fcf_growth_3y_cagr=growth.fcf_growth_3y_cagr,
            consensus_growth_next_2y=growth.consensus_growth_next_2y,
            moat_assessment=growth.moat_assessment,
            score=growth.score,
        )
        db.add(growth_model)
        
        # Populate Risk
        risk = asyncio.run(phase1.populate_risk(stock.id, stock_data.get("risk", {})))
        risk_model = RiskModel(
            id=risk.id,
            stock_id=risk.stock_id,
            beta=risk.beta,
            debt_to_equity=risk.debt_to_equity,
            interest_coverage=risk.interest_coverage,
            industry_cyclicality=risk.industry_cyclicality,
            policy_risk=risk.policy_risk,
            governance_flags=risk.governance_flags,
            score=risk.score,
        )
        db.add(risk_model)
        
        db.commit()
        
        # Phase 2: Traverse
        phase2 = Phase2Traverse()
        asyncio.run(phase2.traverse_sector_edges(sector))
        asyncio.run(phase2.traverse_entity_edges(sector, fq, valuation, growth, risk))
        asyncio.run(phase2.traverse_modifier_edges(valuation, fq, growth, risk))
        
        # Update scores after traversal
        sector_model.score = sector.score
        sector_model.ff_score = sector.five_forces.score
        sector_model.lc_score = sector.lifecycle.score
        sector_model.eb_score = sector.barriers.score
        sector_model.cp_score = sector.strategy.score
        
        fq_model.score = fq.score
        val_model.score = valuation.score
        growth_model.score = growth.score
        growth_model.moat_assessment = growth.moat_assessment
        risk_model.score = risk.score
        
        db.commit()
        
        # Phase 3: Conclude
        phase3 = Phase3Conclude()
        conclusion = asyncio.run(phase3.generate_conclusion(sector, fq, valuation, growth, risk))
        
        conclusion_model = ConclusionModel(
            id=conclusion.id,
            stock_id=conclusion.stock_id,
            composite_score=conclusion.composite_score,
            rating=conclusion.rating,
            conviction=conclusion.conviction,
            target_price_low=conclusion.target_price_low,
            target_price_high=conclusion.target_price_high,
            sector_score=conclusion.sector_score,
            financial_score=conclusion.financial_score,
            valuation_score=conclusion.valuation_score,
            growth_score=conclusion.growth_score,
            risk_score=conclusion.risk_score,
            reasoning_chain=conclusion.reasoning_chain,
        )
        db.add(conclusion_model)
        db.commit()
        
        return {
            "status": "completed",
            "stock_id": str(stock.id),
            "ticker": ticker,
            "composite_score": conclusion.composite_score,
            "rating": conclusion.rating,
        }
        
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
        raise
    finally:
        db.close()
