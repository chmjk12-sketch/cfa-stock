"use client";

import { useState } from "react";
import { type ScreenStockItem } from "@/lib/api";

interface ScreenerStockListProps {
  stocks: ScreenStockItem[];
  loading: boolean;
}

export default function ScreenerStockList({ stocks, loading }: ScreenerStockListProps) {
  const [sortBy, setSortBy] = useState<string>("peg");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  const handleSort = (field: string) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortBy(field);
      setSortOrder("asc");
    }
  };

  const sortedStocks = [...stocks].sort((a, b) => {
    const aVal = (a as any)[sortBy] || 0;
    const bVal = (b as any)[sortBy] || 0;
    return sortOrder === "asc" ? (aVal as number) - (bVal as number) : (bVal as number) - (aVal as number);
  });

  const SortHeader = ({ field, label }: { field: string; label: string }) => (
    <th
      className="px-3 py-2.5 text-left text-xs font-medium text-cfa-muted cursor-pointer hover:text-cfa-text select-none"
      onClick={() => handleSort(field)}
    >
      {label} {sortBy === field && (sortOrder === "asc" ? "↑" : "↓")}
    </th>
  );

  if (loading) {
    return <div className="flex items-center justify-center h-64 text-cfa-muted">加载中...</div>;
  }

  if (stocks.length === 0) {
    return <div className="flex items-center justify-center h-64 text-cfa-muted">暂无符合条件的股票</div>;
  }

  return (
    <div className="overflow-auto rounded-lg border border-cfa-border">
      <table className="w-full text-sm">
        <thead className="bg-cfa-card sticky top-0 z-10">
          <tr className="border-b border-cfa-border">
            <th className="px-3 py-2.5 text-left text-xs font-medium text-cfa-muted w-8">#</th>
            <th className="px-3 py-2.5 text-left text-xs font-medium text-cfa-muted">股票</th>
            <SortHeader field="sector" label="赛道" />
            <SortHeader field="peg" label="PEG" />
            <SortHeader field="net_profit_growth" label="净利润增速" />
            <SortHeader field="latest_price" label="现价" />
            <SortHeader field="target_price_neutral" label="目标价" />
            <th className="px-3 py-2.5 text-left text-xs font-medium text-cfa-muted">上涨空间</th>
            <SortHeader field="rating" label="评级" />
          </tr>
        </thead>
        <tbody className="divide-y divide-cfa-border/50">
          {sortedStocks.map((stock, index) => (
            <tr key={stock.ticker} className="hover:bg-cfa-bg/50 transition-colors">
              <td className="px-3 py-2.5 text-cfa-muted text-xs">{index + 1}</td>
              <td className="px-3 py-2.5">
                <div className="font-medium text-sm">{stock.name}</div>
                <div className="text-xs text-cfa-muted">{stock.ticker}</div>
              </td>
              <td className="px-3 py-2.5 text-xs text-cfa-muted">{stock.sector || "-"}</td>
              <td className="px-3 py-2.5">
                <span className={stock.peg != null && stock.peg < 1 ? "text-green-400 font-medium" : ""}>
                  {stock.peg?.toFixed(2) || "-"}
                </span>
              </td>
              <td className="px-3 py-2.5">
                {stock.net_profit_growth != null ? `${(stock.net_profit_growth * 100).toFixed(1)}%` : "-"}
              </td>
              <td className="px-3 py-2.5 font-mono text-xs">
                ¥{stock.latest_price?.toFixed(2) || "-"}
              </td>
              <td className="px-3 py-2.5 font-mono text-xs">
                ¥{stock.target_price_neutral?.toFixed(0) || "-"}
              </td>
              <td className="px-3 py-2.5">
                {stock.upside_neutral != null ? (
                  <div className="flex items-center gap-1.5">
                    <span className={`text-xs font-medium ${stock.upside_neutral > 0 ? "text-green-400" : "text-red-400"}`}>
                      {stock.upside_neutral > 0 ? "+" : ""}{(stock.upside_neutral * 100).toFixed(0)}%
                    </span>
                    <div className="w-14 h-1.5 bg-cfa-border rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${stock.upside_neutral > 0 ? "bg-green-400" : "bg-red-400"}`}
                        style={{ width: `${Math.min(Math.abs(stock.upside_neutral) * 200, 100)}%` }}
                      />
                    </div>
                  </div>
                ) : "-"}
              </td>
              <td className="px-3 py-2.5">
                {stock.rating && (
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                    stock.rating === "BUY" ? "bg-green-500/20 text-green-400" :
                    stock.rating === "SELL" ? "bg-red-500/20 text-red-400" :
                    "bg-yellow-500/20 text-yellow-400"
                  }`}>
                    {stock.rating}
                  </span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
