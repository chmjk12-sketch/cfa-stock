"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { ArrowLeft, TrendingUp, Loader2 } from "lucide-react";
import { StockData, SectorAnalysis } from "@/types";
import RadarChart from "./RadarChart";
import SectorADPanel from "./SectorADPanel";
import ReasoningGraph from "./ReasoningGraph";
import {
  getFullAnalysis,
  triggerAnalysis,
  type StockAnalysisResponse,
  type FinancialQualityResponse,
  type ValuationResponse,
  type GrowthResponse,
  type RiskResponse,
} from "@/lib/api";

interface StockDetailProps {
  stock: StockData;
  onBack: () => void;
}

const tabs = [
  { id: "overview", label: "综合看板" },
  { id: "financial", label: "财务质量" },
  { id: "valuation", label: "估值分析" },
  { id: "growth", label: "成长性" },
  { id: "risk", label: "风险分析" },
  { id: "sector", label: "行业分析" },
  { id: "forecast", label: "机构预测" },
];

function RatingBadge({ rating }: { rating?: string }) {
  if (!rating) return null;
  const styles = {
    buy: "badge-buy",
    hold: "badge-hold",
    sell: "badge-sell",
  };
  const labels = { buy: "BUY", hold: "HOLD", sell: "SELL" };
  return (
    <span className={`text-sm px-3 py-1 rounded-full font-bold ${styles[rating as keyof typeof styles]}`}>
      {labels[rating as keyof typeof labels]}
    </span>
  );
}

// Mock fallback data
const mockSectorAnalysis: SectorAnalysis = {
  five_forces: {
    supplier_power: "low",
    buyer_power: "medium",
    threat_entrants: "low",
    threat_substitutes: "medium",
    rivalry_intensity: "medium",
    switching_cost: "high",
    score: 9,
  },
  lifecycle: {
    lifecycle_stage: "growth",
    segment_growth_rate: 25.0,
    segment_penetration: 0.28,
    score: 9,
  },
  barriers: {
    economies_of_scale: 4,
    product_diff: 5,
    capital_req: 4,
    switching_cost: 4,
    sustainability: "high",
    score: 9,
  },
  strategy: {
    generic_strategy: "differentiation",
    strategy_consistency: "high",
    moat_from_strategy: "wide",
    score: 9,
  },
  score: 9,
};

const mockFinancial: FinancialQualityResponse = {
  roe: 18.5,
  net_margin: 12.3,
  asset_turnover: 0.85,
  equity_multiplier: 1.76,
  debt_ratio: 43.2,
  fcf_positive_3y: true,
  score: 8,
};

const mockValuation: ValuationResponse = {
  pe_ttm: 28.5,
  pb: 4.2,
  peg: 0.95,
  pe_percentile_5y: 35,
  dcf_low: 45.2,
  dcf_high: 62.8,
  margin_of_safety: 17.4,
  score: 8,
};

const mockGrowth: GrowthResponse = {
  revenue_growth_3y_cagr: 32.5,
  earnings_growth_3y_cagr: 28.3,
  fcf_growth_3y_cagr: 25.1,
  consensus_growth_next_2y: 30.2,
  moat_assessment: "wide",
  score: 9,
};

const mockRisk: RiskResponse = {
  beta: 1.15,
  debt_to_equity: 0.45,
  interest_coverage: 8.5,
  industry_cyclicality: "medium",
  policy_risk: "low",
  governance_flags: [],
  score: 7,
};

export default function StockDetail({ stock, onBack }: StockDetailProps) {
  const [activeTab, setActiveTab] = useState("overview");
  const [analysisData, setAnalysisData] = useState<StockAnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch full analysis from backend when stock changes
  useEffect(() => {
    let cancelled = false;

    async function fetchAnalysis() {
      setIsLoading(true);
      setError(null);

      try {
        const data = await getFullAnalysis(stock.ticker);
        if (!cancelled) {
          setAnalysisData(data);
        }
      } catch {
        if (!cancelled) {
          setError("暂无分析数据，显示默认数据");
          setAnalysisData(null);
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    fetchAnalysis();
    return () => {
      cancelled = true;
    };
  }, [stock.ticker]);

  // Merge backend data with stock prop, using mock as fallback
  const displayStock = analysisData
    ? {
        ...stock,
        name: analysisData.stock.name || stock.name,
        ticker: analysisData.stock.ticker || stock.ticker,
        industry: analysisData.stock.industry || stock.industry,
        market_cap: analysisData.stock.market_cap || stock.market_cap,
        composite_score: analysisData.conclusion.composite_score || stock.composite_score,
        rating: (analysisData.conclusion.rating as StockData["rating"]) || stock.rating,
        conviction: (analysisData.conclusion.conviction as StockData["conviction"]) || stock.conviction,
        sector_score: analysisData.conclusion.sector_score || stock.sector_score,
        financial_score: analysisData.conclusion.financial_score || stock.financial_score,
        valuation_score: analysisData.conclusion.valuation_score || stock.valuation_score,
        growth_score: analysisData.conclusion.growth_score || stock.growth_score,
        risk_score: analysisData.conclusion.risk_score || stock.risk_score,
      }
    : stock;

  const sectorAnalysis: SectorAnalysis = analysisData
    ? {
        five_forces: {
          supplier_power: analysisData.sector.five_forces.supplier_power || "medium",
          buyer_power: analysisData.sector.five_forces.buyer_power || "medium",
          threat_entrants: analysisData.sector.five_forces.threat_entrants || "medium",
          threat_substitutes: analysisData.sector.five_forces.threat_substitutes || "medium",
          rivalry_intensity: analysisData.sector.five_forces.rivalry_intensity || "medium",
          switching_cost: analysisData.sector.five_forces.switching_cost || "medium",
          score: analysisData.sector.five_forces.score,
        },
        lifecycle: {
          lifecycle_stage: analysisData.sector.lifecycle.lifecycle_stage || "growth",
          segment_growth_rate: analysisData.sector.lifecycle.segment_growth_rate || 0,
          segment_penetration: analysisData.sector.lifecycle.segment_penetration || 0,
          score: analysisData.sector.lifecycle.score,
        },
        barriers: {
          economies_of_scale: analysisData.sector.barriers.economies_of_scale || 0,
          product_diff: analysisData.sector.barriers.product_diff || 0,
          capital_req: analysisData.sector.barriers.capital_req || 0,
          switching_cost: analysisData.sector.barriers.switching_cost || 0,
          sustainability: analysisData.sector.barriers.sustainability || "medium",
          score: analysisData.sector.barriers.score,
        },
        strategy: {
          generic_strategy: analysisData.sector.strategy.generic_strategy || "cost_leadership",
          strategy_consistency: analysisData.sector.strategy.strategy_consistency || "medium",
          moat_from_strategy: analysisData.sector.strategy.moat_from_strategy || "narrow",
          score: analysisData.sector.strategy.score,
        },
        score: analysisData.sector.score,
      }
    : mockSectorAnalysis;

  const financial = analysisData?.financial_quality || mockFinancial;
  const valuation = analysisData?.valuation || mockValuation;
  const growth = analysisData?.growth || mockGrowth;
  const risk = analysisData?.risk || mockRisk;

  const radarData = [
    { subject: "行业", A: displayStock.sector_score || 0, fullMark: 10 },
    { subject: "财务", A: displayStock.financial_score || 0, fullMark: 10 },
    { subject: "估值", A: displayStock.valuation_score || 0, fullMark: 10 },
    { subject: "成长", A: displayStock.growth_score || 0, fullMark: 10 },
    { subject: "风险", A: displayStock.risk_score || 0, fullMark: 10 },
  ];

  const handleTriggerAnalysis = async () => {
    try {
      await triggerAnalysis(stock.ticker);
      // Re-fetch analysis after triggering
      const data = await getFullAnalysis(stock.ticker);
      setAnalysisData(data);
      setError(null);
    } catch {
      setError("触发分析失败，请稍后重试");
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
      <div className="flex items-center gap-4">
        <button onClick={onBack} className="p-2 rounded-lg bg-cfa-card border border-cfa-border hover:border-cfa-accent transition-colors">
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold">{displayStock.name}</h1>
            <span className="text-cfa-muted">{displayStock.ticker}</span>
            <RatingBadge rating={displayStock.rating} />
            {isLoading && <Loader2 className="w-4 h-4 animate-spin text-cfa-accent" />}
          </div>
          <p className="text-sm text-cfa-muted">{displayStock.industry}</p>
        </div>
        {!analysisData && !isLoading && (
          <button
            onClick={handleTriggerAnalysis}
            className="px-4 py-2 bg-cfa-accent text-white text-sm rounded-lg hover:bg-cfa-accent/80 transition-colors"
          >
            触发分析
          </button>
        )}
      </div>

      {error && (
        <div className="p-3 bg-cfa-warning/10 border border-cfa-warning/30 rounded-lg text-sm text-cfa-warning">
          {error}
        </div>
      )}

      <div className="flex gap-1 p-1 bg-cfa-card rounded-lg border border-cfa-border">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all ${
              activeTab === tab.id ? "bg-cfa-accent text-white" : "text-cfa-muted hover:text-cfa-text"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === "overview" && (
        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-4 space-y-4">
            <div className="cfa-card p-4">
              <h3 className="font-semibold mb-4">五维评分雷达</h3>
              <RadarChart data={radarData} />
            </div>
            <div className="cfa-card p-4">
              <h3 className="font-semibold mb-3">综合评分</h3>
              <div className="flex items-end gap-2">
                <span className="text-5xl font-bold text-cfa-success">{displayStock.composite_score?.toFixed(1)}</span>
                <span className="text-lg text-cfa-muted mb-1">/10</span>
              </div>
              <div className="mt-3 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-cfa-muted">评级</span>
                  <span className="font-medium uppercase">{displayStock.rating}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-cfa-muted">确信度</span>
                  <span className="font-medium">{displayStock.conviction === "high" ? "高" : displayStock.conviction === "medium" ? "中" : "低"}</span>
                </div>
              </div>
            </div>
          </div>
          <div className="col-span-8">
            <SectorADPanel analysis={sectorAnalysis} />
          </div>
        </div>
      )}

      {activeTab === "sector" && <SectorADPanel analysis={sectorAnalysis} />}

      {activeTab === "financial" && (
        <div className="cfa-card p-6">
          <h3 className="font-semibold mb-4">财务质量分析</h3>
          <div className="grid grid-cols-3 gap-4">
            {[
              { label: "ROE", value: financial.roe != null ? `${financial.roe.toFixed(1)}%` : "--", desc: "净资产收益率" },
              { label: "净利率", value: financial.net_margin != null ? `${financial.net_margin.toFixed(1)}%` : "--", desc: "净利润率" },
              { label: "资产周转率", value: financial.asset_turnover != null ? financial.asset_turnover.toFixed(2) : "--", desc: "总资产周转" },
              { label: "权益乘数", value: financial.equity_multiplier != null ? financial.equity_multiplier.toFixed(2) : "--", desc: "财务杠杆" },
              { label: "负债率", value: financial.debt_ratio != null ? `${financial.debt_ratio.toFixed(1)}%` : "--", desc: "资产负债率" },
              { label: "FCF", value: financial.fcf_positive_3y ? "正" : "负", desc: "近3年自由现金流" },
            ].map((item) => (
              <div key={item.label} className="p-4 bg-cfa-bg rounded-lg">
                <p className="text-xs text-cfa-muted">{item.desc}</p>
                <p className="text-2xl font-bold mt-1">{item.value}</p>
                <p className="text-xs text-cfa-accent mt-1">{item.label}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === "valuation" && (
        <div className="cfa-card p-6">
          <h3 className="font-semibold mb-4">估值分析</h3>
          <div className="space-y-4">
            <div className="grid grid-cols-4 gap-4">
              {[
                { label: "PE TTM", value: valuation.pe_ttm != null ? `${valuation.pe_ttm.toFixed(1)}x` : "--" },
                { label: "PB", value: valuation.pb != null ? `${valuation.pb.toFixed(1)}x` : "--" },
                { label: "PEG", value: valuation.peg != null ? valuation.peg.toFixed(2) : "--" },
                { label: "PE分位数", value: valuation.pe_percentile_5y != null ? `${valuation.pe_percentile_5y.toFixed(0)}%` : "--" },
              ].map((item) => (
                <div key={item.label} className="p-4 bg-cfa-bg rounded-lg text-center">
                  <p className="text-xs text-cfa-muted">{item.label}</p>
                  <p className="text-xl font-bold mt-1">{item.value}</p>
                </div>
              ))}
            </div>
            <div className="p-4 bg-cfa-bg rounded-lg">
              <p className="text-sm font-medium mb-2">DCF 估值区间</p>
              <div className="flex items-center gap-4">
                <div className="text-center">
                  <p className="text-xs text-cfa-muted">下限</p>
                  <p className="text-lg font-bold text-cfa-success">
                    {valuation.dcf_low != null ? `¥${valuation.dcf_low.toFixed(1)}` : "--"}
                  </p>
                </div>
                <div className="flex-1 h-2 bg-cfa-border rounded-full relative">
                  <div className="absolute left-1/4 right-1/4 h-full bg-cfa-accent rounded-full" />
                  <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full border-2 border-cfa-accent" />
                </div>
                <div className="text-center">
                  <p className="text-xs text-cfa-muted">上限</p>
                  <p className="text-lg font-bold text-cfa-success">
                    {valuation.dcf_high != null ? `¥${valuation.dcf_high.toFixed(1)}` : "--"}
                  </p>
                </div>
              </div>
              <p className="text-xs text-cfa-muted mt-2">
                安全边际: {valuation.margin_of_safety != null ? `${valuation.margin_of_safety.toFixed(1)}%` : "--"}
              </p>
            </div>
          </div>
        </div>
      )}

      {activeTab === "growth" && (
        <div className="cfa-card p-6">
          <h3 className="font-semibold mb-4">成长性分析</h3>
          <div className="grid grid-cols-2 gap-4">
            {[
              { label: "营收3年CAGR", value: growth.revenue_growth_3y_cagr != null ? `${growth.revenue_growth_3y_cagr.toFixed(1)}%` : "--" },
              { label: "盈利3年CAGR", value: growth.earnings_growth_3y_cagr != null ? `${growth.earnings_growth_3y_cagr.toFixed(1)}%` : "--" },
              { label: "FCF 3年CAGR", value: growth.fcf_growth_3y_cagr != null ? `${growth.fcf_growth_3y_cagr.toFixed(1)}%` : "--" },
              { label: "分析师一致预期", value: growth.consensus_growth_next_2y != null ? `${growth.consensus_growth_next_2y.toFixed(1)}%` : "--" },
            ].map((item) => (
              <div key={item.label} className="p-4 bg-cfa-bg rounded-lg flex items-center justify-between">
                <div>
                  <p className="text-xs text-cfa-muted">{item.label}</p>
                  <p className="text-xl font-bold mt-1">{item.value}</p>
                </div>
                <TrendingUp className="w-5 h-5 text-cfa-success" />
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === "risk" && (
        <div className="cfa-card p-6">
          <h3 className="font-semibold mb-4">风险分析</h3>
          <div className="space-y-3">
            {[
              { label: "Beta", value: risk.beta != null ? risk.beta.toFixed(2) : "--", level: risk.beta != null ? (risk.beta > 1.3 ? "high" : risk.beta > 1.0 ? "medium" : "low") : "low" },
              { label: "负债权益比", value: risk.debt_to_equity != null ? risk.debt_to_equity.toFixed(2) : "--", level: risk.debt_to_equity != null ? (risk.debt_to_equity > 1.0 ? "high" : risk.debt_to_equity > 0.5 ? "medium" : "low") : "low" },
              { label: "利息覆盖倍数", value: risk.interest_coverage != null ? `${risk.interest_coverage.toFixed(1)}x` : "--", level: risk.interest_coverage != null ? (risk.interest_coverage < 3 ? "high" : risk.interest_coverage < 6 ? "medium" : "low") : "low" },
              { label: "行业周期性", value: risk.industry_cyclicality || "--", level: risk.industry_cyclicality === "high" ? "high" : risk.industry_cyclicality === "medium" ? "medium" : "low" },
              { label: "政策风险", value: risk.policy_risk || "--", level: risk.policy_risk === "high" ? "high" : risk.policy_risk === "medium" ? "medium" : "low" },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between p-3 bg-cfa-bg rounded-lg">
                <span className="text-sm">{item.label}</span>
                <span className={`text-sm font-medium ${
                  item.level === "low" ? "text-cfa-success" : item.level === "medium" ? "text-cfa-warning" : "text-cfa-danger"
                }`}>
                  {item.value}
                </span>
              </div>
            ))}
            {risk.governance_flags && risk.governance_flags.length > 0 && (
              <div className="mt-4 p-3 bg-cfa-bg rounded-lg">
                <p className="text-sm font-medium mb-2">治理风险标记</p>
                <div className="flex flex-wrap gap-2">
                  {risk.governance_flags.map((flag, i) => (
                    <span key={i} className="text-xs px-2 py-1 bg-cfa-danger/10 text-cfa-danger rounded">
                      {flag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === "forecast" && (
        <div className="space-y-6">
          <p className="text-cfa-muted">机构预测数据加载中...</p>
        </div>
      )}

      <div className="mt-6">
        <ReasoningGraph />
      </div>
    </motion.div>
  );
}
