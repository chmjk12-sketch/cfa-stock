"""Phase 2: Traverse Edges - 边遍历工作流"""
from domain.entities import Sector, FinancialQuality, Valuation, Growth, Risk
from domain.ontology.edge_executor import EdgeExecutor


class Phase2Traverse:
    """Phase 2: 遍历所有推理边并计算评分"""

    def __init__(self):
        self.executor = EdgeExecutor()

    async def traverse_sector_edges(self, sector: Sector) -> None:
        """遍历 E1b-E1e: Sector 四维子维度"""
        # E1b: Five Forces
        self.executor.execute_e1b_five_forces(sector, {
            "supplier_power": sector.five_forces.supplier_power,
            "buyer_power": sector.five_forces.buyer_power,
            "threat_entrants": sector.five_forces.threat_entrants,
            "threat_substitutes": sector.five_forces.threat_substitutes,
            "rivalry_intensity": sector.five_forces.rivalry_intensity,
            "switching_cost": sector.five_forces.switching_cost,
        })

        # E1c: Lifecycle
        self.executor.execute_e1c_lifecycle(sector, {
            "lifecycle_stage": sector.lifecycle.lifecycle_stage,
            "segment_growth_rate": sector.lifecycle.segment_growth_rate,
            "segment_penetration": sector.lifecycle.segment_penetration,
        })

        # E1d: Barriers
        self.executor.execute_e1d_barriers(sector, {
            "economies_of_scale": sector.barriers.barrier_economies_of_scale,
            "product_diff": sector.barriers.barrier_product_diff,
            "capital_req": sector.barriers.barrier_capital_req,
            "switching_cost": sector.barriers.barrier_switching_cost,
            "sustainability": sector.barriers.barrier_sustainability,
        })

        # E1e: Strategy
        self.executor.execute_e1e_strategy(sector, {
            "generic_strategy": sector.strategy.generic_strategy,
            "strategy_consistency": sector.strategy.strategy_consistency,
        })

        # E1: Aggregate
        self.executor.execute_e1_sector_aggregate(sector)

    async def traverse_entity_edges(
        self,
        sector: Sector,
        fq: FinancialQuality,
        valuation: Valuation,
        growth: Growth,
        risk: Risk,
    ) -> None:
        """遍历 E2-E5: 实体评分"""
        # E2: Financial
        self.executor.execute_e2_financial(fq, {
            "roe": fq.roe,
            "fcf_positive_3y": fq.fcf_positive_3y,
            "debt_ratio": fq.debt_ratio,
        })

        # E3: Valuation
        self.executor.execute_e3_valuation(valuation, {
            "peg": valuation.peg,
            "pe_percentile": valuation.pe_percentile_5y,
            "margin_of_safety": valuation.margin_of_safety,
        })

        # E4: Growth (moat from sector strategy)
        growth.moat_assessment = sector.strategy.moat_from_strategy
        self.executor.execute_e4_growth(growth, {
            "revenue_cagr": growth.revenue_growth_3y_cagr,
            "earnings_cagr": growth.earnings_growth_3y_cagr,
            "fcf_growth_positive": True,  # TODO: from data
            "moat_assessment": growth.moat_assessment,
        })

        # E5: Risk
        self.executor.execute_e5_risk(risk, {
            "beta": risk.beta,
            "interest_coverage": risk.interest_coverage,
            "governance_flags": risk.governance_flags,
            "policy_risk": risk.policy_risk,
        })

    async def traverse_modifier_edges(
        self,
        valuation: Valuation,
        fq: FinancialQuality,
        growth: Growth,
        risk: Risk,
    ) -> None:
        """遍历 E6-E8: 修饰边"""
        self.executor.execute_e6_fq_informs_valuation(valuation, fq)
        self.executor.execute_e7_growth_adjusts_valuation(valuation, growth)
        self.executor.execute_e8_risk_discounts_valuation(valuation, risk)

    def get_reasoning_log(self) -> list:
        return self.executor.get_reasoning_log()
