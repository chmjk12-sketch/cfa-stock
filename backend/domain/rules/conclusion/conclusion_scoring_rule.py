"""Conclusion Scoring Rule - 投资结论合成规则"""
from typing import Dict, Any


class ConclusionScoringRule:
    """投资结论合成规则 (E9-E13)"""

    WEIGHTS = {
        "sector": 0.20,
        "financial": 0.25,
        "valuation": 0.25,
        "growth": 0.15,
        "risk": 0.15,
    }

    @classmethod
    def evaluate(
        cls,
        sector_score: int,
        financial_score: int,
        valuation_score: int,
        growth_score: int,
        risk_score: int,
    ) -> Dict[str, Any]:
        """
        加权聚合:
        - Sector 20% + FinancialQuality 25% + Valuation 25% + Growth 15% + Risk 15%
        - composite_score = Σ(entity.score × weight)
        
        Rating:
        - composite ≥ 8.0 → BUY
        - 6.0 ≤ composite < 8.0 → HOLD
        - composite < 6.0 → SELL
        
        Conviction:
        - Score range (max - min) < 2 → HIGH
        - 2 ≤ range < 4 → MEDIUM
        - range ≥ 4 → LOW
        """
        scores = {
            "sector": sector_score,
            "financial": financial_score,
            "valuation": valuation_score,
            "growth": growth_score,
            "risk": risk_score,
        }

        # 加权计算
        composite = sum(
            scores[key] * cls.WEIGHTS[key]
            for key in scores
        )
        composite = round(composite, 2)

        # Rating
        if composite >= 8.0:
            rating = "buy"
        elif composite >= 6.0:
            rating = "hold"
        else:
            rating = "sell"

        # Conviction
        score_range = max(scores.values()) - min(scores.values())
        if score_range < 2:
            conviction = "high"
        elif score_range < 4:
            conviction = "medium"
        else:
            conviction = "low"

        return {
            "composite_score": composite,
            "rating": rating,
            "conviction": conviction,
            "score_range": score_range,
            "individual_scores": scores,
            "weights": cls.WEIGHTS,
            "rule_version": "v2.0",
        }
