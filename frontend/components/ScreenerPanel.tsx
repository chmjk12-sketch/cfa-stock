"use client";

import { useState } from "react";
import { type ScreenRequest } from "@/lib/api";

interface ScreenerPanelProps {
  filters: ScreenRequest;
  onChange: (filters: Partial<ScreenRequest>) => void;
  sectors: string[];
}

export default function ScreenerPanel({ filters, onChange, sectors }: ScreenerPanelProps) {
  const [collapsed, setCollapsed] = useState(false);

  const handleSectorToggle = (sector: string) => {
    const current = filters.sectors || [];
    const updated = current.includes(sector)
      ? current.filter((s) => s !== sector)
      : [...current, sector];
    onChange({ sectors: updated });
  };

  if (collapsed) {
    return (
      <div className="w-12 bg-cfa-card border-r border-cfa-border flex flex-col items-center py-4">
        <button onClick={() => setCollapsed(false)} className="text-cfa-muted hover:text-cfa-text text-xs">▶</button>
      </div>
    );
  }

  return (
    <div className="w-72 bg-cfa-card border-r border-cfa-border flex flex-col">
      <div className="p-3 border-b border-cfa-border flex items-center justify-between">
        <span className="text-sm font-semibold">筛选条件</span>
        <button onClick={() => setCollapsed(true)} className="text-cfa-muted hover:text-cfa-text text-xs">◀</button>
      </div>

      <div className="flex-1 overflow-auto p-4 space-y-5">
        {/* 赛道 */}
        <div>
          <label className="text-xs font-medium text-cfa-muted mb-2 block uppercase tracking-wider">赛道</label>
          <div className="flex flex-wrap gap-1.5">
            {sectors.map((sector) => (
              <button
                key={sector}
                onClick={() => handleSectorToggle(sector)}
                className={`px-2 py-1 rounded text-xs transition-colors ${
                  filters.sectors?.includes(sector)
                    ? "bg-cfa-accent text-white"
                    : "bg-cfa-bg text-cfa-muted hover:text-cfa-text"
                }`}
              >
                {sector}
              </button>
            ))}
          </div>
        </div>

        {/* PEG 范围 */}
        <div>
          <label className="text-xs font-medium text-cfa-muted mb-1 block uppercase tracking-wider">
            PEG: {filters.peg_range?.[0]?.toFixed(1)} ~ {filters.peg_range?.[1]?.toFixed(1)}
          </label>
          <input
            type="range"
            min="0"
            max="3"
            step="0.1"
            value={filters.peg_range?.[1] || 3}
            onChange={(e) => onChange({ peg_range: [0, parseFloat(e.target.value)] })}
            className="w-full accent-[#6366f1]"
          />
        </div>

        {/* PE 范围 */}
        <div>
          <label className="text-xs font-medium text-cfa-muted mb-1 block uppercase tracking-wider">
            PE: {filters.pe_range?.[0]} ~ {filters.pe_range?.[1]}
          </label>
          <input
            type="range"
            min="0"
            max="200"
            step="5"
            value={filters.pe_range?.[1] || 200}
            onChange={(e) => onChange({ pe_range: [0, parseFloat(e.target.value)] })}
            className="w-full accent-[#6366f1]"
          />
        </div>

        {/* 净利润增速 */}
        <div>
          <label className="text-xs font-medium text-cfa-muted mb-1 block uppercase tracking-wider">
            净利润增速 ≥ {((filters.net_profit_growth_min || 0) * 100).toFixed(0)}%
          </label>
          <input
            type="range"
            min="0"
            max="3"
            step="0.1"
            value={filters.net_profit_growth_min || 0}
            onChange={(e) => onChange({ net_profit_growth_min: parseFloat(e.target.value) })}
            className="w-full accent-[#6366f1]"
          />
        </div>

        {/* 营收增速 */}
        <div>
          <label className="text-xs font-medium text-cfa-muted mb-1 block uppercase tracking-wider">
            营收增速 ≥ {((filters.revenue_growth_min || 0) * 100).toFixed(0)}%
          </label>
          <input
            type="range"
            min="0"
            max="3"
            step="0.1"
            value={filters.revenue_growth_min || 0}
            onChange={(e) => onChange({ revenue_growth_min: parseFloat(e.target.value) })}
            className="w-full accent-[#6366f1]"
          />
        </div>

        {/* 评级 */}
        <div>
          <label className="text-xs font-medium text-cfa-muted mb-1 block uppercase tracking-wider">评级</label>
          <select
            value={filters.rating || ""}
            onChange={(e) => onChange({ rating: e.target.value || undefined })}
            className="w-full bg-cfa-bg border border-cfa-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-cfa-accent"
          >
            <option value="">不限</option>
            <option value="BUY">BUY</option>
            <option value="HOLD">HOLD</option>
            <option value="SELL">SELL</option>
          </select>
        </div>

        {/* 重置 */}
        <button
          onClick={() =>
            onChange({
              sectors: [],
              peg_range: [0, 3],
              pe_range: [0, 200],
              net_profit_growth_min: 0,
              revenue_growth_min: 0,
              rating: undefined,
            })
          }
          className="w-full py-2 bg-cfa-bg border border-cfa-border rounded-lg text-sm hover:bg-cfa-border transition-colors text-cfa-muted"
        >
          重置条件
        </button>
      </div>
    </div>
  );
}
