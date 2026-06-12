"use client";

import { useState, useEffect, useCallback } from "react";
import ScreenerPanel from "@/components/ScreenerPanel";
import ScatterChart from "@/components/ScatterChart";
import ScreenerStockList from "@/components/ScreenerStockList";
import { screenStocks, getScreenDimensions, type ScreenStockItem, type ScreenRequest } from "@/lib/api";

export default function ScreenerPage() {
  const [filters, setFilters] = useState<ScreenRequest>({
    peg_range: [0, 1],
    pe_range: [0, 200],
    net_profit_growth_min: 0.5,
    revenue_growth_min: 0.3,
    sort_by: "peg",
    sort_order: "asc",
    page: 1,
    page_size: 50,
  });

  const [stocks, setStocks] = useState<ScreenStockItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [dimensions, setDimensions] = useState<{ sectors: string[] }>({ sectors: [] });
  const [viewMode, setViewMode] = useState<"scatter" | "list">("scatter");

  useEffect(() => {
    getScreenDimensions().then((d) => setDimensions(d)).catch(() => {});
  }, []);

  const fetchStocks = useCallback(async () => {
    setLoading(true);
    try {
      const res = await screenStocks(filters);
      setStocks(res.stocks);
      setTotal(res.total);
    } catch (e) {
      console.error("筛选失败:", e);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    const timer = setTimeout(fetchStocks, 300);
    return () => clearTimeout(timer);
  }, [fetchStocks]);

  const handleFilterChange = (newFilters: Partial<ScreenRequest>) => {
    setFilters((prev) => ({ ...prev, ...newFilters, page: 1 }));
  };

  const handleScatterBrush = (range: { xMin: number; xMax: number; yMin: number; yMax: number }) => {
    handleFilterChange({
      peg_range: [range.xMin, range.xMax],
      net_profit_growth_min: range.yMin,
    });
  };

  return (
    <div className="flex h-screen bg-cfa-bg">
      <ScreenerPanel
        filters={filters}
        onChange={handleFilterChange}
        sectors={dimensions.sectors}
      />

      <div className="flex-1 flex flex-col p-6 overflow-hidden">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-xl font-semibold">策略筛选器</h1>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setViewMode("scatter")}
              className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                viewMode === "scatter" ? "bg-cfa-accent text-white" : "bg-cfa-card text-cfa-muted hover:text-cfa-text"
              }`}
            >
              散点图
            </button>
            <button
              onClick={() => setViewMode("list")}
              className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                viewMode === "list" ? "bg-cfa-accent text-white" : "bg-cfa-card text-cfa-muted hover:text-cfa-text"
              }`}
            >
              列表
            </button>
            <span className="text-sm text-cfa-muted ml-4">共 {total} 只符合条件</span>
          </div>
        </div>

        <div className="flex-1 overflow-auto">
          {viewMode === "scatter" ? (
            <ScatterChart
              stocks={stocks}
              xAxis="peg"
              yAxis="net_profit_growth"
              onBrush={handleScatterBrush}
            />
          ) : (
            <ScreenerStockList stocks={stocks} loading={loading} />
          )}
        </div>
      </div>
    </div>
  );
}
