// Use relative path so Next.js rewrites proxy to backend
const BASE_URL = "";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const errorText = await res.text().catch(() => "Unknown error");
    throw new Error(`API Error ${res.status}: ${errorText}`);
  }

  return res.json() as Promise<T>;
}

// ===== Stock API Response Types =====

export interface StockSearchResult {
  id: string;
  ticker: string;
  name: string;
  exchange: string;
  industry?: string;
  composite_score?: number;
  rating?: string;
}

export interface StockListResponse {
  total: number;
  items: StockSearchResult[];
}

// ===== Analysis API Response Types =====

export interface FiveForcesDetail {
  supplier_power?: string;
  buyer_power?: string;
  threat_entrants?: string;
  threat_substitutes?: string;
  rivalry_intensity?: string;
  switching_cost?: string;
  score: number;
}

export interface LifecycleDetail {
  lifecycle_stage?: string;
  segment_growth_rate?: number;
  segment_penetration?: number;
  lifecycle_risk?: string;
  score: number;
}

export interface BarriersDetail {
  economies_of_scale: number;
  product_diff: number;
  capital_req: number;
  switching_cost: number;
  sustainability?: string;
  score: number;
}

export interface StrategyDetail {
  generic_strategy?: string;
  strategy_consistency?: string;
  moat_from_strategy?: string;
  score: number;
}

export interface SectorResponse {
  five_forces: FiveForcesDetail;
  lifecycle: LifecycleDetail;
  barriers: BarriersDetail;
  strategy: StrategyDetail;
  score: number;
}

export interface FinancialQualityResponse {
  roe?: number;
  net_margin?: number;
  asset_turnover?: number;
  equity_multiplier?: number;
  debt_ratio?: number;
  fcf_positive_3y?: boolean;
  score: number;
}

export interface ValuationResponse {
  pe_ttm?: number;
  pb?: number;
  peg?: number;
  pe_percentile_5y?: number;
  dcf_low?: number;
  dcf_high?: number;
  margin_of_safety?: number;
  score: number;
}

export interface GrowthResponse {
  revenue_growth_3y_cagr?: number;
  earnings_growth_3y_cagr?: number;
  fcf_growth_3y_cagr?: number;
  consensus_growth_next_2y?: number;
  moat_assessment?: string;
  score: number;
}

export interface RiskResponse {
  beta?: number;
  debt_to_equity?: number;
  interest_coverage?: number;
  industry_cyclicality?: string;
  policy_risk?: string;
  governance_flags?: string[];
  score: number;
}

export interface ConclusionResponse {
  composite_score?: number;
  rating?: string;
  conviction?: string;
  target_price_low?: number;
  target_price_high?: number;
  sector_score?: number;
  financial_score?: number;
  valuation_score?: number;
  growth_score?: number;
  risk_score?: number;
}

export interface StockAnalysisResponse {
  stock: {
    id: string;
    ticker: string;
    name: string;
    exchange: string;
    industry?: string;
    market_cap?: number;
  };
  sector: SectorResponse;
  financial_quality: FinancialQualityResponse;
  valuation: ValuationResponse;
  growth: GrowthResponse;
  risk: RiskResponse;
  conclusion: ConclusionResponse;
  reasoning_log: Array<{ step: string; reasoning: string }>;
}

// ===== Opportunity API Response Types =====

export interface OpportunityResponse {
  id: string;
  theme: string;
  industry?: string;
  opportunity_score?: number;
  stock_ids?: string[];
  risks?: string;
  conclusion?: string;
  created_at: string;
}

export interface TopOpportunityResponse {
  stock: {
    id: string;
    ticker: string;
    name: string;
    industry?: string;
  };
  composite_score: number;
  rating: string;
  conviction: string;
  target_price: [number | null, number | null];
}

// ===== API Functions =====

export function getStocks(): Promise<StockListResponse> {
  return request<StockListResponse>("/api/stocks/");
}

export function searchStocks(q: string): Promise<StockSearchResult[]> {
  return request<StockSearchResult[]>(`/api/stocks/search?q=${encodeURIComponent(q)}`);
}

export function getStockByTicker(ticker: string): Promise<StockSearchResult> {
  return request<StockSearchResult>(`/api/stocks/${encodeURIComponent(ticker)}`);
}

export function getFullAnalysis(ticker: string): Promise<StockAnalysisResponse> {
  return request<StockAnalysisResponse>(`/api/analysis/${encodeURIComponent(ticker)}/full`);
}

export function getOpportunities(): Promise<OpportunityResponse[]> {
  return request<OpportunityResponse[]>("/api/opportunities/");
}

export function getTopOpportunities(): Promise<TopOpportunityResponse[]> {
  return request<TopOpportunityResponse[]>("/api/opportunities/top");
}

export function triggerAnalysis(ticker: string): Promise<{ message: string; stock_id: string }> {
  return request<{ message: string; stock_id: string }>(`/api/analysis/${encodeURIComponent(ticker)}/trigger`, {
    method: "POST",
  });
}
