"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { ArrowUpRight, TrendingUp } from "lucide-react";
import { StockData } from "@/types";

interface CandidateStocksProps {
  stocks: StockData[];
  onSelectStock: (stock: StockData) => void;
}

type SortOption = "composite_score" | "valuation_score" | "growth_score";

const sortLabels: Record<SortOption, string> = {
  composite_score: "综合评分",
  valuation_score: "估值性价比",
  growth_score: "成长潜力",
};

function RatingBadge({ rating }: { rating?: string }) {
  if (!rating) return null;
  const styles = {
    buy: "badge-buy",
    hold: "badge-hold",
    sell: "badge-sell",
  };
  const labels = {
    buy: "BUY",
    hold: "HOLD",
    sell: "SELL",
  };
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${styles[rating as keyof typeof styles]}`}>
      {labels[rating as keyof typeof labels]}
    </span>
  );
}

function ScoreBar({ score, label }: { score?: number; label: string }) {
  if (score === undefined) return null;
  const percentage = (score / 10) * 100;
  const color = score >= 7 ? "bg-cfa-success" : score >= 5 ? "bg-cfa-warning" : "bg-cfa-danger";
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-cfa-muted w-12">{label}</span>
      <div className="flex-1 h-1.5 bg-cfa-bg rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full`} style={{ width: `${percentage}%` }} />
      </div>
      <span className="text-xs font-medium w-6 text-right">{score}</span>
    </div>
  );
}

export default function CandidateStocks({ stocks, onSelectStock }: CandidateStocksProps) {
  const [sortBy, setSortBy] = useState<SortOption>("composite_score");

  const sortedStocks = useMemo(() => {
    return [...stocks].sort((a, b) => {
      const scoreA = a[sortBy] ?? 0;
      const scoreB = b[sortBy] ?? 0;
      return scoreB - scoreA;
    });
  }, [stocks, sortBy]);

  return (
    <div className="cfa-card p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold">候选股票池</h3>
        <div className="flex items-center gap-2">
          <span className="text-xs text-cfa-muted">排序:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as SortOption)}
            className="text-xs bg-cfa-bg border border-cfa-border rounded px-2 py-1 text-cfa-text focus:outline-none focus:border-cfa-accent"
          >
            {Object.entries(sortLabels).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="space-y-3">
        {sortedStocks.map((stock, i) => (
          <motion.div
            key={stock.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
            className="p-4 rounded-lg bg-cfa-bg/50 border border-cfa-border/50 hover:border-cfa-accent/50 cursor-pointer transition-all group"
            onClick={() => onSelectStock(stock)}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-cfa-accent/10 flex items-center justify-center">
                  <span className="text-sm font-bold text-cfa-accent">{stock.ticker.split(".")[0]}</span>
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{stock.name}</span>
                    <span className="text-xs text-cfa-muted">{stock.ticker}</span>
                  </div>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-xs text-cfa-muted">{stock.industry}</span>
                    <RatingBadge rating={stock.rating} />
                    {stock.conviction && (
                      <span className="text-xs text-cfa-muted">
                        确信度: {stock.conviction === "high" ? "高" : stock.conviction === "medium" ? "中" : "低"}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <div className="text-right">
                <div className="flex items-center gap-1">
                  <span className="text-2xl font-bold">{stock.composite_score?.toFixed(1)}</span>
                  <span className="text-sm text-cfa-muted">/10</span>
                </div>
                <div className="flex items-center gap-1 text-xs text-cfa-success">
                  <TrendingUp className="w-3 h-3" />
                  <span>+2.3%</span>
                </div>
              </div>
            </div>

            {/* Score bars */}
            <div className="mt-3 space-y-1.5">
              <ScoreBar score={stock.sector_score} label="行业" />
              <ScoreBar score={stock.financial_score} label="财务" />
              <ScoreBar score={stock.valuation_score} label="估值" />
              <ScoreBar score={stock.growth_score} label="成长" />
              <ScoreBar score={stock.risk_score} label="风险" />
            </div>

            {/* Hover arrow */}
            <div className="flex justify-end mt-2">
              <ArrowUpRight className="w-4 h-4 text-cfa-muted group-hover:text-cfa-accent transition-colors" />
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
