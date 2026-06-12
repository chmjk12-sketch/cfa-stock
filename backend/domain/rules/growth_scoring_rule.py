"""Growth Scoring Rule - 成长性评分规则"""
from typing import Dict, Any, Optional


class GrowthScoringRule:
    """成长性评分规则 (E4)"""

    @staticmethod
    def evaluate(
        revenue_cagr: Optional[float],
        earnings_cagr: Optional[float],
        fcf_growth_positive: bool = False,
        moat_assessment: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        评分逻辑:
        - Revenue CAGR > 20% → +3; 10-20% → +1; < 5% → -2
        - Earnings CAGR > revenue CAGR → +2 (margin expansion); equal → 0; lower → -1
        - FCF growth positive all 3 years → +2
        - Wide moat → +2; narrow → +1; none → -1
        - Base score 5 + adjustments, capped to [1, 10]
        """
        score = 5
        adjustments = []

        # 营收增长评分
        if revenue_cagr is not None:
            if revenue_cagr > 20:
                score += 3
                adjustments.append(f"营收CAGR {revenue_cagr:.1f}% > 20% → +3")
            elif revenue_cagr >= 10:
                score += 1
                adjustments.append(f"营收CAGR {revenue_cagr:.1f}% 10-20% → +1")
            elif revenue_cagr < 5:
                score -= 2
                adjustments.append(f"营收CAGR {revenue_cagr:.1f}% < 5% → -2")

        # 盈利增长 vs 营收增长 (margin expansion)
        if earnings_cagr is not None and revenue_cagr is not None:
            if earnings_cagr > revenue_cagr:
                score += 2
                adjustments.append(f"盈利CAGR {earnings_cagr:.1f}% > 营收CAGR {revenue_cagr:.1f}% (margin expansion) → +2")
            elif earnings_cagr < revenue_cagr:
                score -= 1
                adjustments.append(f"盈利CAGR {earnings_cagr:.1f}% < 营收CAGR {revenue_cagr:.1f}% → -1")

        # FCF 增长
        if fcf_growth_positive:
            score += 2
            adjustments.append("FCF 3年正增长 → +2")

        # 护城河
        if moat_assessment == "wide":
            score += 2
            adjustments.append("Wide moat → +2")
        elif moat_assessment == "narrow":
            score += 1
            adjustments.append("Narrow moat → +1")
        elif moat_assessment == "none":
            score -= 1
            adjustments.append("No moat → -1")

        score = max(1, min(10, score))

        return {
            "score": score,
            "adjustments": adjustments,
            "rule_version": "v2.0",
        }
