"""Financial Quality Scoring Rule - 财务质量评分规则"""
from typing import Dict, Any, Optional


class FinancialScoringRule:
    """财务质量评分规则 (E2)"""

    @staticmethod
    def evaluate(
        roe: Optional[float],
        fcf_positive_3y: Optional[bool],
        debt_ratio: Optional[float],
        net_margin_trend: str = "stable",  # stable/improving/volatile/declining
    ) -> Dict[str, Any]:
        """
        评分逻辑:
        - ROE ≥ 20% → +3; ROE 10-15% → +1; ROE < 5% → -2
        - FCF positive last 3 years → +2; positive 2/3 → +1; otherwise → -1
        - Debt ratio < 30% → +2; 30-50% → +1; > 70% → -2
        - Net margin stable/improving 3y → +2; volatile → 0; declining → -1
        - Base score 5 + adjustments, capped to [1, 10]
        """
        score = 5
        adjustments = []

        # ROE 评分
        if roe is not None:
            if roe >= 20:
                score += 3
                adjustments.append(f"ROE {roe:.1f}% ≥ 20% → +3")
            elif roe >= 10:
                score += 1
                adjustments.append(f"ROE {roe:.1f}% 10-20% → +1")
            elif roe < 5:
                score -= 2
                adjustments.append(f"ROE {roe:.1f}% < 5% → -2")

        # FCF 评分
        if fcf_positive_3y is not None:
            if fcf_positive_3y:
                score += 2
                adjustments.append("FCF 近3年均为正 → +2")
            else:
                score -= 1
                adjustments.append("FCF 近3年有负值 → -1")

        # 负债率评分
        if debt_ratio is not None:
            if debt_ratio < 30:
                score += 2
                adjustments.append(f"负债率 {debt_ratio:.1f}% < 30% → +2")
            elif debt_ratio < 50:
                score += 1
                adjustments.append(f"负债率 {debt_ratio:.1f}% 30-50% → +1")
            elif debt_ratio > 70:
                score -= 2
                adjustments.append(f"负债率 {debt_ratio:.1f}% > 70% → -2")

        # 净利率趋势
        if net_margin_trend == "improving":
            score += 2
            adjustments.append("净利率3年改善 → +2")
        elif net_margin_trend == "volatile":
            adjustments.append("净利率波动 → 0")
        elif net_margin_trend == "declining":
            score -= 1
            adjustments.append("净利率下滑 → -1")

        score = max(1, min(10, score))

        return {
            "score": score,
            "adjustments": adjustments,
            "rule_version": "v2.0",
        }
