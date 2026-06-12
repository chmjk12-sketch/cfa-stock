"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import Sidebar from "@/components/Sidebar";
import OpportunityOverview from "@/components/OpportunityOverview";
import IndustryMap from "@/components/IndustryMap";
import CandidateStocks from "@/components/CandidateStocks";
import StockDetail from "@/components/StockDetail";
import { StockData } from "@/types";
import { getStocks, searchStocks, type StockSearchResult } from "@/lib/api";

const mockStocks: StockData[] = [
  {
    id: "1",
    ticker: "300476.SZ",
    name: "胜宏科技",
    exchange: "SZ",
    industry: "电子/PCB",
    market_cap: 2800000000,
    composite_score: 9.2,
    rating: "buy",
    conviction: "high",
    sector_score: 9,
    financial_score: 8,
    valuation_score: 8,
    growth_score: 9,
    risk_score: 7,
  },
  {
    id: "2",
    ticker: "002463.SZ",
    name: "沪电股份",
    exchange: "SZ",
    industry: "电子/PCB",
    market_cap: 3200000000,
    composite_score: 8.7,
    rating: "buy",
    conviction: "high",
    sector_score: 8,
    financial_score: 8,
    valuation_score: 8,
    growth_score: 8,
    risk_score: 7,
  },
  {
    id: "3",
    ticker: "600183.SH",
    name: "生益科技",
    exchange: "SH",
    industry: "电子/PCB",
    market_cap: 4500000000,
    composite_score: 8.4,
    rating: "buy",
    conviction: "medium",
    sector_score: 8,
    financial_score: 8,
    valuation_score: 7,
    growth_score: 8,
    risk_score: 7,
  },
  {
    id: "4",
    ticker: "300474.SZ",
    name: "景嘉微",
    exchange: "SZ",
    industry: "半导体",
    market_cap: 1800000000,
    composite_score: 8.1,
    rating: "hold",
    conviction: "medium",
    sector_score: 8,
    financial_score: 7,
    valuation_score: 7,
    growth_score: 8,
    risk_score: 7,
  },
  {
    id: "5",
    ticker: "300308.SZ",
    name: "中际旭创",
    exchange: "SZ",
    industry: "光模块",
    market_cap: 5200000000,
    composite_score: 8.0,
    rating: "hold",
    conviction: "medium",
    sector_score: 8,
    financial_score: 8,
    valuation_score: 7,
    growth_score: 8,
    risk_score: 7,
  },
];

export default function Home() {
  const [selectedStock, setSelectedStock] = useState<StockData | null>(null);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [stocks, setStocks] = useState<StockData[]>(mockStocks);

  // Search state
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<StockSearchResult[]>([]);
  const [showSearchDropdown, setShowSearchDropdown] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Load stocks from backend on mount
  useEffect(() => {
    getStocks()
      .then((res) => {
        if (res.items && res.items.length > 0) {
          setStocks(
            res.items.map((item) => ({
              id: item.id,
              ticker: item.ticker,
              name: item.name,
              exchange: item.exchange,
              industry: item.industry,
              composite_score: item.composite_score,
              rating: item.rating as StockData["rating"],
            }))
          );
        }
      })
      .catch(() => {
        // Fallback to mock data if API is unavailable
      });
  }, []);

  // Debounced search
  const handleSearchChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      setSearchQuery(value);

      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }

      if (!value.trim()) {
        setSearchResults([]);
        setShowSearchDropdown(false);
        setIsSearching(false);
        return;
      }

      setIsSearching(true);

      debounceTimerRef.current = setTimeout(async () => {
        try {
          const results = await searchStocks(value.trim());
          setSearchResults(results);
          setShowSearchDropdown(true);
        } catch {
          setSearchResults([]);
        } finally {
          setIsSearching(false);
        }
      }, 300);
    },
    []
  );

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node) &&
        searchInputRef.current &&
        !searchInputRef.current.contains(e.target as Node)
      ) {
        setShowSearchDropdown(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Handle selecting a search result
  const handleSelectSearchResult = useCallback(
    (result: StockSearchResult) => {
      const stock: StockData = {
        id: result.id,
        ticker: result.ticker,
        name: result.name,
        exchange: result.exchange,
        industry: result.industry,
        composite_score: result.composite_score,
        rating: result.rating as StockData["rating"],
      };
      setSelectedStock(stock);
      setSearchQuery("");
      setSearchResults([]);
      setShowSearchDropdown(false);
    },
    []
  );

  return (
    <div className="flex h-screen bg-cfa-bg">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-14 border-b border-cfa-border flex items-center px-6 justify-between bg-cfa-card">
          <div className="flex items-center gap-4">
            <h1 className="text-lg font-semibold">CFA Stock Discovery</h1>
            <span className="text-xs text-cfa-muted bg-cfa-border px-2 py-1 rounded">A股</span>
          </div>
          <div className="flex items-center gap-3 relative">
            <input
              ref={searchInputRef}
              type="text"
              placeholder="搜索行业、公司或概念..."
              value={searchQuery}
              onChange={handleSearchChange}
              onFocus={() => {
                if (searchResults.length > 0) {
                  setShowSearchDropdown(true);
                }
              }}
              className="bg-cfa-bg border border-cfa-border rounded-lg px-4 py-1.5 text-sm w-64 focus:outline-none focus:border-cfa-accent"
            />
            {isSearching && (
              <div className="absolute right-6 top-1/2 -translate-y-1/2">
                <div className="w-4 h-4 border-2 border-cfa-muted border-t-cfa-accent rounded-full animate-spin" />
              </div>
            )}

            {/* Search Results Dropdown */}
            {showSearchDropdown && (
              <div
                ref={dropdownRef}
                className="absolute top-full right-0 mt-1 w-80 bg-cfa-card border border-cfa-border rounded-lg shadow-xl z-50 overflow-hidden"
              >
                {searchResults.length > 0 ? (
                  <div className="max-h-80 overflow-y-auto">
                    {searchResults.map((result) => (
                      <button
                        key={result.id}
                        onClick={() => handleSelectSearchResult(result)}
                        className="w-full flex items-center gap-3 px-4 py-3 hover:bg-cfa-bg/80 transition-colors text-left border-b border-cfa-border/50 last:border-b-0"
                      >
                        <div className="w-9 h-9 rounded-lg bg-cfa-accent/10 flex items-center justify-center shrink-0">
                          <span className="text-xs font-bold text-cfa-accent">
                            {result.ticker.split(".")[0]}
                          </span>
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="font-medium text-sm">{result.name}</span>
                            <span className="text-xs text-cfa-muted">{result.ticker}</span>
                          </div>
                          {result.industry && (
                            <p className="text-xs text-cfa-muted truncate">{result.industry}</p>
                          )}
                        </div>
                        <div className="text-right shrink-0">
                          {result.composite_score != null && (
                            <span className="text-sm font-bold text-cfa-success">
                              {result.composite_score.toFixed(1)}
                            </span>
                          )}
                          {result.rating && (
                            <div>
                              <span
                                className={`text-xs px-1.5 py-0.5 rounded-full font-medium ${
                                  result.rating === "buy"
                                    ? "badge-buy"
                                    : result.rating === "hold"
                                    ? "badge-hold"
                                    : "badge-sell"
                                }`}
                              >
                                {result.rating.toUpperCase()}
                              </span>
                            </div>
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                ) : (
                  !isSearching && (
                    <div className="px-4 py-6 text-center text-sm text-cfa-muted">
                      未找到匹配的股票
                    </div>
                  )
                )}
              </div>
            )}
          </div>
        </header>

        <div className="flex-1 overflow-auto p-6">
          {selectedStock ? (
            <StockDetail stock={selectedStock} onBack={() => setSelectedStock(null)} />
          ) : (
            <div className="grid grid-cols-12 gap-6">
              <div className="col-span-8 space-y-6">
                <OpportunityOverview />
                <IndustryMap />
                <CandidateStocks stocks={stocks} onSelectStock={setSelectedStock} />
              </div>
              <div className="col-span-4 space-y-6">
                <div className="cfa-card p-4">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold">预警中心</h3>
                    <span className="text-xs text-cfa-muted cursor-pointer hover:text-cfa-accent">查看全部</span>
                  </div>
                  <div className="space-y-3">
                    {[
                      { title: "AI服务器PCB 机会增强", desc: "五力格局改善，壁垒评分上升", time: "3小时前" },
                      { title: "胜宏科技 触发买入信号", desc: "综合评分突破85，估值性价比提升", time: "5小时前" },
                      { title: "半导体设备 估值偏高", desc: "PE百分位达到90%，注意回调风险", time: "5小时前" },
                      { title: "新能源车 行业风险提升", desc: "生命周期评分下降至4分", time: "1天前" },
                    ].map((alert, i) => (
                      <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-cfa-bg/50">
                        <div className="flex-1">
                          <p className="text-sm font-medium">{alert.title}</p>
                          <p className="text-xs text-cfa-muted mt-0.5">{alert.desc}</p>
                        </div>
                        <span className="text-xs text-cfa-muted">{alert.time}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
