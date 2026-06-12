"""Phase 3: Generate Conclusion - 结论生成工作流"""
from domain.entities import Sector, FinancialQuality, Valuation, Growth, Risk, Conclusion
from domain.ontology.edge_executor import EdgeExecutor
from domain.ontology.score_aggregator import ScoreAggregator


class Phase3Conclude:
    """Phase 3: 生成最终投资结论"""

    def __init__(self):
        self.executor = EdgeExecutor()
        self.aggregator = ScoreAggregator()

    async def generate_conclusion(
        self,
        sector: Sector,
        fq: FinancialQuality,
        valuation: Valuation,
        growth: Growth,
        risk: Risk,
    ) -> Conclusion:
        """生成投资结论"""
        # E9-E13: 合成结论
        result = self.executor.execute_e9_e13_conclusion(sector, fq, valuation, growth, risk)
        
        # 创建 Conclusion 实体
        conclusion = Conclusion(
            stock_id=sector.stock_id,
            composite_score=result["composite_score"],
            rating=result["rating"],
            conviction=result["conviction"],
            sector_score=sector.score,
            financial_score=fq.score,
            valuation_score=valuation.score,
            growth_score=growth.score,
            risk_score=risk.score,
        )
        
        # 计算目标价 (简化版 DCF)
        if valuation.dcf_low and valuation.dcf_high:
            conclusion.target_price_low = valuation.dcf_low
            conclusion.target_price_high = valuation.dcf_high
        
        # 构建推理链
        conclusion.reasoning_chain = self.aggregator.build_reasoning_chain(
            sector, fq, valuation, growth, risk, conclusion
        )
        conclusion.reasoning_chain["log"] = self.executor.get_reasoning_log()
        
        return conclusion
