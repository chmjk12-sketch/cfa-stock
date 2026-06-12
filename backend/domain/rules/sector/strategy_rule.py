"""Competitive Strategy Scoring Rule - Porter 竞争战略评分规则"""
from typing import Dict, Any


class StrategyScoringRule:
    """Porter 竞争战略评分规则 (E1e)"""

    @staticmethod
    def evaluate(
        generic_strategy: str,
        strategy_consistency: str,
        has_customer_lock_in: bool = False,
    ) -> Dict[str, Any]:
        """
        评分逻辑:
        - 战略定位清晰且执行一致 → +3; 清晰但执行有偏差 → +1; 不清晰或摇摆 → -2
        - 差异化战略 + 客户锁定效应 → +2
        - Base 5, capped [1, 10]
        """
        score = 5
        adjustments = []

        # 战略一致性评分
        if strategy_consistency == "high":
            score += 3
            adjustments.append("战略定位清晰且执行一致 → +3")
        elif strategy_consistency == "medium":
            score += 1
            adjustments.append("战略清晰但执行有偏差 → +1")
        else:
            score -= 2
            adjustments.append("战略不清晰或摇摆 → -2")

        # 差异化 + 客户锁定
        if generic_strategy == "differentiation" and has_customer_lock_in:
            score += 2
            adjustments.append("差异化战略 + 客户锁定效应 → +2")

        # 输出 moat_from_strategy
        if score >= 8 and strategy_consistency == "high":
            moat = "wide"
        elif score >= 5:
            moat = "narrow"
        else:
            moat = "none"

        score = max(1, min(10, score))

        return {
            "score": score,
            "moat_from_strategy": moat,
            "generic_strategy": generic_strategy,
            "strategy_consistency": strategy_consistency,
            "adjustments": adjustments,
            "rule_version": "v2.0",
        }
