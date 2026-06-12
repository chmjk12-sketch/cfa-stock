"""Risk Scoring Rule - 风险评分规则"""
from typing import Dict, Any, Optional, List


class RiskScoringRule:
    """风险评分规则 (E5) - 越高 = 风险越低"""

    @staticmethod
    def evaluate(
        beta: Optional[float],
        interest_coverage: Optional[float],
        governance_flags: Optional[List[str]],
        policy_risk: Optional[str],
    ) -> Dict[str, Any]:
        """
        评分逻辑:
        - Beta < 0.8 → +2; 0.8-1.2 → 0; > 1.5 → -2
        - Interest coverage > 10× → +2; 3-10× → +1; < 2× → -2
        - No governance flags → +2; minor flags → 0; major flags → -3
        - Low policy risk → +2; medium → 0; high → -2
        - Base score 5 + adjustments, capped to [1, 10]
        """
        score = 5
        adjustments = []

        # Beta 评分
        if beta is not None:
            if beta < 0.8:
                score += 2
                adjustments.append(f"Beta {beta:.2f} < 0.8 → +2")
            elif beta > 1.5:
                score -= 2
                adjustments.append(f"Beta {beta:.2f} > 1.5 → -2")
            else:
                adjustments.append(f"Beta {beta:.2f} 0.8-1.2 → 0")

        # 利息覆盖倍数
        if interest_coverage is not None:
            if interest_coverage > 10:
                score += 2
                adjustments.append(f"利息覆盖 {interest_coverage:.1f}× > 10× → +2")
            elif interest_coverage >= 3:
                score += 1
                adjustments.append(f"利息覆盖 {interest_coverage:.1f}× 3-10× → +1")
            elif interest_coverage < 2:
                score -= 2
                adjustments.append(f"利息覆盖 {interest_coverage:.1f}× < 2× → -2")

        # 治理风险
        if governance_flags is not None:
            flag_count = len(governance_flags)
            if flag_count == 0:
                score += 2
                adjustments.append("无治理风险标记 → +2")
            elif flag_count <= 2:
                adjustments.append(f"轻微治理风险 ({flag_count}项) → 0")
            else:
                score -= 3
                adjustments.append(f"重大治理风险 ({flag_count}项) → -3")

        # 政策风险
        if policy_risk == "low":
            score += 2
            adjustments.append("政策风险低 → +2")
        elif policy_risk == "high":
            score -= 2
            adjustments.append("政策风险高 → -2")
        elif policy_risk == "medium":
            adjustments.append("政策风险中等 → 0")

        score = max(1, min(10, score))

        return {
            "score": score,
            "adjustments": adjustments,
            "rule_version": "v2.0",
        }
