"""Industry Lifecycle Scoring Rule - 行业生命周期评分规则"""
from typing import Dict, Any


class LifecycleScoringRule:
    """行业生命周期评分规则 (E1c)"""

    @staticmethod
    def evaluate(
        lifecycle_stage: str,
        segment_growth_rate: float,
        segment_penetration: float,
        stage_transition_risk: bool = False,
    ) -> Dict[str, Any]:
        """
        评分逻辑:
        - 子赛道成长期(growth) → +3; 成熟期初期 → +1; 成熟期/衰退期 → -2
        - 渗透率 15-50%（S曲线陡峭段）→ +2; > 50% → 0
        - 识别到明显阶段转换风险 → -1
        - Base 5, capped [1, 10]
        """
        score = 5
        adjustments = []

        # 生命周期阶段评分
        if lifecycle_stage == "growth":
            score += 3
            adjustments.append("子赛道成长期 → +3")
        elif lifecycle_stage == "mature_early":
            score += 1
            adjustments.append("成熟期初期 → +1")
        elif lifecycle_stage in ["mature", "decline"]:
            score -= 2
            adjustments.append(f"{lifecycle_stage}期 → -2")

        # 渗透率评分 (S曲线)
        if 0.15 <= segment_penetration <= 0.50:
            score += 2
            adjustments.append(f"渗透率 {segment_penetration:.0%} 处于S曲线陡峭段 → +2")
        elif segment_penetration > 0.50:
            adjustments.append(f"渗透率 {segment_penetration:.0%} 已超过50% → 0")

        # 阶段转换风险
        if stage_transition_risk:
            score -= 1
            adjustments.append("识别到阶段转换风险 → -1")

        score = max(1, min(10, score))

        return {
            "score": score,
            "lifecycle_stage": lifecycle_stage,
            "segment_penetration": segment_penetration,
            "adjustments": adjustments,
            "rule_version": "v2.0",
        }
