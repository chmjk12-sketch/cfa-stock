"""Five Forces Scoring Rule - 波特五力评分规则"""
from typing import Dict, Any


class FiveForcesScoringRule:
    """波特五力评分规则 (E1b)"""

    @staticmethod
    def evaluate(
        supplier_power: str,
        buyer_power: str,
        threat_entrants: str,
        threat_substitutes: str,
        rivalry_intensity: str,
        switching_cost: str,
        customer_concentration: float = 0.0,
    ) -> Dict[str, Any]:
        """
        评分逻辑:
        - 五力格局"良好"（≥3力为low）→ +3
        - "一般"（2力为low）→ +1
        - "差"（≤1力为low）→ -2
        - 转换成本高(switching_cost=high) → +2
        - 买方集中度风险（大客户依赖 > 40%）→ -1
        - Base 5, capped [1, 10]
        """
        forces = [supplier_power, buyer_power, threat_entrants, threat_substitutes, rivalry_intensity]
        low_count = forces.count("low")

        # 基础评分
        score = 5
        adjustments = []

        # 五力格局评分
        if low_count >= 3:
            score += 3
            adjustments.append(f"五力格局良好 ({low_count}/5 为low) → +3")
        elif low_count == 2:
            score += 1
            adjustments.append(f"五力格局一般 ({low_count}/5 为low) → +1")
        else:
            score -= 2
            adjustments.append(f"五力格局差 ({low_count}/5 为low) → -2")

        # 转换成本
        if switching_cost == "high":
            score += 2
            adjustments.append("转换成本高 → +2")

        # 买方集中度风险
        if customer_concentration > 0.4:
            score -= 1
            adjustments.append(f"买方集中度高 ({customer_concentration:.0%}) → -1")

        # 限制范围
        score = max(1, min(10, score))

        return {
            "score": score,
            "low_count": low_count,
            "switching_cost": switching_cost,
            "customer_concentration": customer_concentration,
            "adjustments": adjustments,
            "rule_version": "v2.0",
        }
