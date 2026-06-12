-- CFA Stock Ontology Database Initialization
-- 核心实体表

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 1. Stock 实体
CREATE TABLE stocks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticker VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    exchange VARCHAR(20) NOT NULL,
    industry VARCHAR(100),
    market_cap DECIMAL(20, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_stocks_ticker ON stocks(ticker);
CREATE INDEX idx_stocks_industry ON stocks(industry);

-- 2. Sector 实体 (含 A+D 四维子维度)
CREATE TABLE sectors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    
    -- 波特五力
    ff_score INTEGER CHECK (ff_score BETWEEN 1 AND 10),
    ff_supplier_power VARCHAR(10) CHECK (ff_supplier_power IN ('high', 'medium', 'low')),
    ff_buyer_power VARCHAR(10) CHECK (ff_buyer_power IN ('high', 'medium', 'low')),
    ff_threat_entrants VARCHAR(10) CHECK (ff_threat_entrants IN ('high', 'medium', 'low')),
    ff_threat_substitutes VARCHAR(10) CHECK (ff_threat_substitutes IN ('high', 'medium', 'low')),
    ff_rivalry_intensity VARCHAR(10) CHECK (ff_rivalry_intensity IN ('high', 'medium', 'low')),
    ff_switching_cost VARCHAR(10) CHECK (ff_switching_cost IN ('high', 'medium', 'low')),
    ff_raw JSONB,
    
    -- 行业生命周期
    lc_score INTEGER CHECK (lc_score BETWEEN 1 AND 10),
    lc_stage VARCHAR(20) CHECK (lc_stage IN ('growth', 'mature', 'decline')),
    lc_segment_growth_rate DECIMAL(5, 2),
    lc_segment_penetration DECIMAL(5, 2),
    lc_risk TEXT,
    lc_raw JSONB,
    
    -- 进入壁垒
    eb_score INTEGER CHECK (eb_score BETWEEN 1 AND 10),
    eb_economies_of_scale INTEGER CHECK (eb_economies_of_scale BETWEEN 1 AND 5),
    eb_product_diff INTEGER CHECK (eb_product_diff BETWEEN 1 AND 5),
    eb_capital_req INTEGER CHECK (eb_capital_req BETWEEN 1 AND 5),
    eb_switching_cost INTEGER CHECK (eb_switching_cost BETWEEN 1 AND 5),
    eb_sustainability VARCHAR(10) CHECK (eb_sustainability IN ('high', 'medium', 'low')),
    eb_raw JSONB,
    
    -- 竞争战略
    cp_score INTEGER CHECK (cp_score BETWEEN 1 AND 10),
    cp_generic_strategy VARCHAR(20) CHECK (cp_generic_strategy IN ('cost_leadership', 'differentiation', 'focus_cost', 'focus_diff')),
    cp_strategy_consistency VARCHAR(10) CHECK (cp_strategy_consistency IN ('high', 'medium', 'low')),
    cp_moat_from_strategy VARCHAR(10) CHECK (cp_moat_from_strategy IN ('wide', 'narrow', 'none')),
    cp_raw JSONB,
    
    -- 聚合评分
    score INTEGER CHECK (score BETWEEN 1 AND 10),
    raw_analysis JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sectors_stock_id ON sectors(stock_id);
CREATE INDEX idx_sectors_score ON sectors(score);

-- 3. FinancialQuality 实体
CREATE TABLE financial_qualities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    
    roe DECIMAL(8, 4),
    net_margin DECIMAL(8, 4),
    asset_turnover DECIMAL(8, 4),
    equity_multiplier DECIMAL(8, 4),
    debt_ratio DECIMAL(8, 4),
    fcf_positive_3y BOOLEAN,
    
    score INTEGER CHECK (score BETWEEN 1 AND 10),
    raw_data JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_fq_stock_id ON financial_qualities(stock_id);

-- 4. Valuation 实体
CREATE TABLE valuations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    
    pe_ttm DECIMAL(10, 2),
    pb DECIMAL(10, 2),
    peg DECIMAL(10, 2),
    pe_percentile_5y DECIMAL(5, 2),
    dcf_low DECIMAL(12, 2),
    dcf_high DECIMAL(12, 2),
    margin_of_safety DECIMAL(8, 4),
    
    score INTEGER CHECK (score BETWEEN 1 AND 10),
    raw_data JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_valuation_stock_id ON valuations(stock_id);

-- 5. Growth 实体
CREATE TABLE growths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    
    revenue_growth_3y_cagr DECIMAL(8, 4),
    earnings_growth_3y_cagr DECIMAL(8, 4),
    fcf_growth_3y_cagr DECIMAL(8, 4),
    consensus_growth_next_2y DECIMAL(8, 4),
    moat_assessment VARCHAR(10) CHECK (moat_assessment IN ('wide', 'narrow', 'none')),
    
    score INTEGER CHECK (score BETWEEN 1 AND 10),
    raw_data JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_growth_stock_id ON growths(stock_id);

-- 6. Risk 实体
CREATE TABLE risks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    
    beta DECIMAL(8, 4),
    debt_to_equity DECIMAL(8, 4),
    interest_coverage DECIMAL(10, 2),
    industry_cyclicality VARCHAR(10) CHECK (industry_cyclicality IN ('high', 'medium', 'low')),
    policy_risk VARCHAR(10) CHECK (policy_risk IN ('high', 'medium', 'low')),
    governance_flags JSONB,
    
    score INTEGER CHECK (score BETWEEN 1 AND 10),
    raw_data JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_risk_stock_id ON risks(stock_id);

-- 7. Conclusion 实体
CREATE TABLE conclusions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    
    composite_score DECIMAL(4, 2),
    rating VARCHAR(10) CHECK (rating IN ('buy', 'hold', 'sell')),
    conviction VARCHAR(10) CHECK (conviction IN ('high', 'medium', 'low')),
    target_price_low DECIMAL(12, 2),
    target_price_high DECIMAL(12, 2),
    
    -- 各维度评分详情
    sector_score INTEGER,
    financial_score INTEGER,
    valuation_score INTEGER,
    growth_score INTEGER,
    risk_score INTEGER,
    
    reasoning_chain JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_conclusion_stock_id ON conclusions(stock_id);
CREATE INDEX idx_conclusion_rating ON conclusions(rating);
CREATE INDEX idx_conclusion_composite ON conclusions(composite_score DESC);

-- 8. Opportunity 聚合表
CREATE TABLE opportunities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    theme VARCHAR(100) NOT NULL,
    industry VARCHAR(100),
    opportunity_score DECIMAL(5, 2),
    stock_ids UUID[],
    risks TEXT,
    conclusion TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_opportunities_score ON opportunities(opportunity_score DESC);

-- 9. Analysis Task 表 (用于异步任务追踪)
CREATE TABLE analysis_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    task_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    celery_task_id VARCHAR(100),
    result JSONB,
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tasks_stock_id ON analysis_tasks(stock_id);
CREATE INDEX idx_tasks_status ON analysis_tasks(status);

-- 触发器：自动更新 updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_stocks_updated_at BEFORE UPDATE ON stocks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sectors_updated_at BEFORE UPDATE ON sectors FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_fq_updated_at BEFORE UPDATE ON financial_qualities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_valuations_updated_at BEFORE UPDATE ON valuations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_growths_updated_at BEFORE UPDATE ON growths FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_risks_updated_at BEFORE UPDATE ON risks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_conclusions_updated_at BEFORE UPDATE ON conclusions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE ON opportunities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
