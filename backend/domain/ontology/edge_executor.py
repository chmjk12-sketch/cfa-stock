"""Edge Executor - 边规则执行器"""
from typing import Dict, Any, Optional
from uuid import UUID

from domain.entities import (
    Stock, Sector, FinancialQuality, Valuation, Growth, Risk, Conclusion
)
from domain.rules.sector.five_forces_rule import FiveForcesScoringRule
from domain.rules.sector.lifecycle_rule import LifecycleScoringRule
from domain.rules.sector.barriers_rule import BarriersScoringRule
from domain.rules.sector.strategy_rule import StrategyScoringRule
from domain.rules.financial_scoring_rule import FinancialScoringRule
from domain.rules.valuation_scoring_rule import ValuationScoringRule
from domain.rules.growth_scoring_rule import GrowthScoringRule
from domain.rules.risk_scoring_rule import RiskScoringRule
from domain.rules.conclusion.conclusion_scoring_rule import ConclusionScoringRule


class EdgeExecutor:
    """边执行器 - 执行 E1-E13 所有推理边"""

    def __init__(self):
        self.reasoning_log = []

    def log(self, edge: str, message: str):
        self.reasoning_log.append({"edge": edge, "message": message})

    # ===== E1: Stock → Sector (四维子维度) =====

    def execute_e1b_five_forces(self, sector: Sector, data: dict) -> dict:
        """E1b: Stock --five_forces--> Sector.FiveForces"""
        result = FiveForcesScoringRule.evaluate(
            supplier_power=data.get("supplier_power", "medium"),
            buyer_power=data.get("buyer_power", "medium"),
            threat_entrants=data.get("threat_entrants", "medium"),
            threat_substitutes=data.get("threat_substitutes", "medium"),
            rivalry_intensity=data.get("rivalry_intensity", "medium"),
            switching_cost=data.get("switching_cost", "medium"),
            customer_concentration=data.get("customer_concentration", 0.0),
        )
        sector.five_forces.score = result["score"]
        sector.five_forces.raw_analysis = result
        self.log("E1b", f"Five Forces score: {result['score']}")
        return result

    def execute_e1c_lifecycle(self, sector: Sector, data: dict) -> dict:
        """E1c: Stock --lifecycle--> Sector.IndustryLifecycle"""
        result = LifecycleScoringRule.evaluate(
            lifecycle_stage=data.get("lifecycle_stage", "mature"),
            segment_growth_rate=data.get("segment_growth_rate", 0.0),
            segment_penetration=data.get("segment_penetration", 0.0),
            stage_transition_risk=data.get("stage_transition_risk", False),
        )
        sector.lifecycle.score = result["score"]
        sector.lifecycle.raw_analysis = result
        self.log("E1c", f"Lifecycle score: {result['score']}")
        return result

    def execute_e1d_barriers(self, sector: Sector, data: dict) -> dict:
        """E1d: Stock --barriers--> Sector.EntryBarriers"""
        result = BarriersScoringRule.evaluate(
            economies_of_scale=data.get("economies_of_scale", 3),
            product_diff=data.get("product_diff", 3),
            capital_req=data.get("capital_req", 3),
            switching_cost=data.get("switching_cost", 3),
            sustainability=data.get("sustainability", "medium"),
            capex_to_profit_ratio=data.get("capex_to_profit_ratio", 0.0),
        )
        sector.barriers.score = result["score"]
        sector.barriers.raw_analysis = result
        self.log("E1d", f"Barriers score: {result['score']}")
        return result

    def execute_e1e_strategy(self, sector: Sector, data: dict) -> dict:
        """E1e: Stock --strategy--> Sector.CompetitivePosition"""
        result = StrategyScoringRule.evaluate(
            generic_strategy=data.get("generic_strategy", "differentiation"),
            strategy_consistency=data.get("strategy_consistency", "medium"),
            has_customer_lock_in=data.get("has_customer_lock_in", False),
        )
        sector.strategy.score = result["score"]
        sector.strategy.moat_from_strategy = result["moat_from_strategy"]
        sector.strategy.raw_analysis = result
        self.log("E1e", f"Strategy score: {result['score']}, Moat: {result['moat_from_strategy']}")
        return result

    def execute_e1_sector_aggregate(self, sector: Sector) -> int:
        """E1: 聚合 Sector 四维评分"""
        sector.calculate_score()
        self.log("E1", f"Sector aggregate score: {sector.score}")
        return sector.score

    # ===== E2-E5: Stock → Financial/Valuation/Growth/Risk =====

    def execute_e2_financial(self, fq: FinancialQuality, data: dict) -> dict:
        """E2: Stock --has--> FinancialQuality"""
        result = FinancialScoringRule.evaluate(
            roe=data.get("roe"),
            fcf_positive_3y=data.get("fcf_positive_3y"),
            debt_ratio=data.get("debt_ratio"),
            net_margin_trend=data.get("net_margin_trend", "stable"),
        )
        fq.score = result["score"]
        fq.raw_data = result
        self.log("E2", f"Financial score: {result['score']}")
        return result

    def execute_e3_valuation(self, valuation: Valuation, data: dict) -> dict:
        """E3: Stock --has--> Valuation"""
        result = ValuationScoringRule.evaluate(
            peg=data.get("peg"),
            pe_percentile=data.get("pe_percentile"),
            margin_of_safety=data.get("margin_of_safety"),
        )
        valuation.score = result["score"]
        valuation.raw_data = result
        self.log("E3", f"Valuation score: {result['score']}")
        return result

    def execute_e4_growth(self, growth: Growth, data: dict) -> dict:
        """E4: Stock --has--> Growth"""
        result = GrowthScoringRule.evaluate(
            revenue_cagr=data.get("revenue_cagr"),
            earnings_cagr=data.get("earnings_cagr"),
            fcf_growth_positive=data.get("fcf_growth_positive", False),
            moat_assessment=data.get("moat_assessment"),
        )
        growth.score = result["score"]
        growth.raw_data = result
        self.log("E4", f"Growth score: {result['score']}")
        return result

    def execute_e5_risk(self, risk: Risk, data: dict) -> dict:
        """E5: Stock --has--> Risk"""
        result = RiskScoringRule.evaluate(
            beta=data.get("beta"),
            interest_coverage=data.get("interest_coverage"),
            governance_flags=data.get("governance_flags", []),
            policy_risk=data.get("policy_risk"),
        )
        risk.score = result["score"]
        risk.raw_data = result
        self.log("E5", f"Risk score: {result['score']}")
        return result

    # ===== E6-E8: Modifier Edges =====

    def execute_e6_fq_informs_valuation(self, valuation: Valuation, fq: FinancialQuality) -> dict:
        """E6: FinancialQuality --informs--> Valuation"""
        # 如果 ROE 持续 > 20%，使用乐观增长轨迹
        adjustment = {}
        if fq.roe and fq.roe > 20:
            adjustment["growth_trajectory"] = "optimistic"
            adjustment["reason"] = f"ROE {fq.roe:.1f}% > 20%, 使用乐观增长轨迹"
        elif fq.roe and fq.roe < 10:
            adjustment["growth_trajectory"] = "conservative"
            adjustment["reason"] = f"ROE {fq.roe:.1f}% < 10%, 使用保守增长轨迹"
        
        self.log("E6", adjustment.get("reason", "No adjustment"))
        return adjustment

    def execute_e7_growth_adjusts_valuation(self, valuation: Valuation, growth: Growth) -> dict:
        """E7: Growth --adjusts--> Valuation"""
        adjustment = {}
        if growth.revenue_growth_3y_cagr:
            if growth.revenue_growth_3y_cagr > 25:
                adjustment["phase1_extension"] = 1
                adjustment["reason"] = f"高增长 {growth.revenue_growth_3y_cagr:.1f}%, 延长phase1"
            elif growth.revenue_growth_3y_cagr < 5:
                adjustment["phase1_shortening"] = 1
                adjustment["reason"] = f"低增长 {growth.revenue_growth_3y_cagr:.1f}%, 缩短phase1"
        
        self.log("E7", adjustment.get("reason", "No adjustment"))
        return adjustment

    def execute_e8_risk_discounts_valuation(self, valuation: Valuation, risk: Risk) -> dict:
        """E8: Risk --discounts--> Valuation"""
        adjustment = {}
        if risk.score <= 4:
            adjustment["wacc_premium"] = 0.02
            adjustment["reason"] = f"高风险 (score={risk.score}), WACC +2%"
        elif risk.score >= 8:
            adjustment["wacc_discount"] = 0.01
            adjustment["reason"] = f"低风险 (score={risk.score}), WACC -1%"
        
        self.log("E8", adjustment.get("reason", "No adjustment"))
        return adjustment

    # ===== E9-E13: Synthesis Edges =====

    def execute_e9_e13_conclusion(
        self,
        sector: Sector,
        fq: FinancialQuality,
        valuation: Valuation,
        growth: Growth,
        risk: Risk,
    ) -> dict:
        """E9-E13: All entities --informs--> Conclusion"""
        result = ConclusionScoringRule.evaluate(
            sector_score=sector.score,
            financial_score=fq.score,
            valuation_score=valuation.score,
            growth_score=growth.score,
            risk_score=risk.score,
        )
        self.log("E9-E13", f"Composite: {result['composite_score']}, Rating: {result['rating']}, Conviction: {result['conviction']}")
        return result

    def get_reasoning_log(self) -> list:
        return self.reasoning_log
