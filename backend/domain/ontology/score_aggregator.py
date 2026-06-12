"""Score Aggregator - 评分聚合器"""
from typing import Dict, Any
from domain.entities import Sector, FinancialQuality, Valuation, Growth, Risk, Conclusion


class ScoreAggregator:
    """评分聚合器 - 负责各维度评分的聚合与合成"""

    @staticmethod
    def aggregate_sector_score(sector: Sector) -> Dict[str, Any]:
        """聚合 Sector 四维评分"""
        return {
            "ff_score": sector.five_forces.score,
            "lc_score": sector.lifecycle.score,
            "eb_score": sector.barriers.score,
            "cp_score": sector.strategy.score,
            "final_score": sector.calculate_score(),
            "weights": {
                "five_forces": 0.25,
                "lifecycle": 0.25,
                "barriers": 0.25,
                "strategy": 0.25,
            }
        }

    @staticmethod
    def build_reasoning_chain(
        sector: Sector,
        fq: FinancialQuality,
        valuation: Valuation,
        growth: Growth,
        risk: Risk,
        conclusion: Conclusion,
    ) -> Dict[str, Any]:
        """构建完整推理链"""
        return {
            "step1_sector": {
                "description": "经济/行业分析",
                "five_forces": {
                    "score": sector.five_forces.score,
                    "details": sector.five_forces.raw_analysis,
                },
                "lifecycle": {
                    "score": sector.lifecycle.score,
                    "details": sector.lifecycle.raw_analysis,
                },
                "barriers": {
                    "score": sector.barriers.score,
                    "details": sector.barriers.raw_analysis,
                },
                "strategy": {
                    "score": sector.strategy.score,
                    "moat": sector.strategy.moat_from_strategy,
                    "details": sector.strategy.raw_analysis,
                },
                "aggregate_score": sector.score,
            },
            "step2_company": {
                "description": "公司分析",
                "moat_assessment": growth.moat_assessment,
            },
            "step3_financial": {
                "description": "财务分析",
                "score": fq.score,
                "details": fq.raw_data,
            },
            "step4_valuation": {
                "description": "估值分析",
                "score": valuation.score,
                "dcf_range": [valuation.dcf_low, valuation.dcf_high],
                "margin_of_safety": valuation.margin_of_safety,
                "details": valuation.raw_data,
            },
            "step5_risk": {
                "description": "风险评估",
                "score": risk.score,
                "details": risk.raw_data,
            },
            "step6_conclusion": {
                "description": "投资决策",
                "composite_score": conclusion.composite_score,
                "rating": conclusion.rating,
                "conviction": conclusion.conviction,
                "target_price": [conclusion.target_price_low, conclusion.target_price_high],
            },
        }
