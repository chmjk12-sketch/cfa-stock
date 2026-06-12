export interface StockData {
  id: string;
  ticker: string;
  name: string;
  exchange: string;
  industry?: string;
  market_cap?: number;
  composite_score?: number;
  rating?: "buy" | "hold" | "sell";
  conviction?: "high" | "medium" | "low";
  sector_score?: number;
  financial_score?: number;
  valuation_score?: number;
  growth_score?: number;
  risk_score?: number;
}

export interface SectorAnalysis {
  five_forces: {
    supplier_power: string;
    buyer_power: string;
    threat_entrants: string;
    threat_substitutes: string;
    rivalry_intensity: string;
    switching_cost: string;
    score: number;
  };
  lifecycle: {
    lifecycle_stage: string;
    segment_growth_rate: number;
    segment_penetration: number;
    score: number;
  };
  barriers: {
    economies_of_scale: number;
    product_diff: number;
    capital_req: number;
    switching_cost: number;
    sustainability: string;
    score: number;
  };
  strategy: {
    generic_strategy: string;
    strategy_consistency: string;
    moat_from_strategy: string;
    score: number;
  };
  score: number;
}

export interface StockDetailData extends StockData {
  sector_analysis?: SectorAnalysis;
  financial_quality?: {
    roe: number;
    net_margin: number;
    asset_turnover: number;
    equity_multiplier: number;
    debt_ratio: number;
    fcf_positive_3y: boolean;
    score: number;
  };
  valuation?: {
    pe_ttm: number;
    pb: number;
    peg: number;
    pe_percentile_5y: number;
    dcf_low: number;
    dcf_high: number;
    margin_of_safety: number;
    score: number;
  };
  growth?: {
    revenue_growth_3y_cagr: number;
    earnings_growth_3y_cagr: number;
    fcf_growth_3y_cagr: number;
    consensus_growth_next_2y: number;
    moat_assessment: string;
    score: number;
  };
  risk?: {
    beta: number;
    debt_to_equity: number;
    interest_coverage: number;
    industry_cyclicality: string;
    policy_risk: string;
    governance_flags: string[];
    score: number;
  };
}
