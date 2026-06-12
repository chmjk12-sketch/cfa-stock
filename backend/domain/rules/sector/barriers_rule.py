"""Entry Barriers Scoring Rule - Bain 进入壁垒评分规则"""
from typing import Dict, Any


class BarriersScoringRule:
    """Bain 进入壁垒评分规则 (E1d)"""

    @staticmethod
    def evaluate(
        economies_of_scale: int,
        product_diff: int,
        capital_req: int,
        switching_cost: int,
        sustainability: str,
        capex_to_profit_ratio: float = 0.0,
    ) -> Dict[str, Any]:
        """
        评分逻辑:
        - 四类壁垒平均 ≥ 4★ → +3; 3-4★ → +1; < 3★ → -2
        - 壁垒可持续性 high（5年+不破）→ +2
        - 壁垒依赖持续高 capex（>利润50%）→ -1（维持成本警告）
        - Base 5, capped [1, 10]
        """
        score = 5
        adjustments = []

        barriers = [economies_of_scale, product_diff, capital_req, switching_cost]
        avg_barrier = sum(barriers) / len(barriers)

        # 壁垒强度评分
        if avg_barrier >= 4:
            score += 3
            adjustments.append(f"四类壁垒平均 {avg_barrier:.1f}★ ≥ 4★ → +3")
        elif avg_barrier >= 3:
            score += 1
            adjustments.append(f"四类壁垒平均 {avg_barrier:.1f}★ 3-4★ → +1")
        else:
            score -= 2
            adjustments.append(f"四类壁垒平均 {avg_barrier:.1f}★ < 3★ → -2")

        # 可持续性
        if sustainability == "high":
            score += 2
            adjustments.append("壁垒可持续性高(5年+) → +2")

        # 维持成本警告
        if capex_to_profit_ratio > 0.5:
            score -= 1
            adjustments.append(f"维持壁垒capex占利润 {capex_to_profit_ratio:.0%} → -1")

        score = max(1, min(10, score))

        return {
            "score": score,
            "avg_barrier": avg_barrier,
            "sustainability": sustainability,
            "adjustments": adjustments,
            "rule_version": "v2.0",
        }
