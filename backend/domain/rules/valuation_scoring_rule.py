"""Valuation Scoring Rule - 估值评分规则"""
from typing import Dict, Any, Optional


class ValuationScoringRule:
    """估值评分规则 (E3)"""

    @staticmethod
    def evaluate(
        peg: Optional[float],
        pe_percentile: Optional[float],
        margin_of_safety: Optional[float],
    ) -> Dict[str, Any]:
        """
        评分逻辑:
        - PEG < 1.0 → +3; PEG 1.0-1.5 → +1; PEG > 2.0 → -2
        - PE percentile < 30% → +2; 30-70% → 0; > 70% → -2
        - Margin of safety > 20% → +3; 0-20% → +1; negative → -1
        - Base score 5 + adjustments, capped to [1, 10]
        """
        score = 5
        adjustments = []

        # PEG 评分
        if peg is not None:
            if peg < 1.0:
                score += 3
                adjustments.append(f"PEG {peg:.2f} < 1.0 → +3")
            elif peg <= 1.5:
                score += 1
                adjustments.append(f"PEG {peg:.2f} 1.0-1.5 → +1")
            elif peg > 2.0:
                score -= 2
                adjustments.append(f"PEG {peg:.2f} > 2.0 → -2")

        # PE 分位数评分
        if pe_percentile is not None:
            if pe_percentile < 30:
                score += 2
                adjustments.append(f"PE分位数 {pe_percentile:.0f}% < 30% → +2")
            elif pe_percentile > 70:
                score -= 2
                adjustments.append(f"PE分位数 {pe_percentile:.0f}% > 70% → -2")
            else:
                adjustments.append(f"PE分位数 {pe_percentile:.0f}% 30-70% → 0")

        # 安全边际评分
        if margin_of_safety is not None:
            if margin_of_safety > 20:
                score += 3
                adjustments.append(f"安全边际 {margin_of_safety:.1f}% > 20% → +3")
            elif margin_of_safety > 0:
                score += 1
                adjustments.append(f"安全边际 {margin_of_safety:.1f}% 0-20% → +1")
            else:
                score -= 1
                adjustments.append(f"安全边际 {margin_of_safety:.1f}% 为负 → -1")

        score = max(1, min(10, score))

        return {
            "score": score,
            "adjustments": adjustments,
            "rule_version": "v2.0",
        }
