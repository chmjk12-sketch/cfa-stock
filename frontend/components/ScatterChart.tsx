"use client";

import {
  ScatterChart as ReScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Brush,
  ZAxis,
} from "recharts";
import { type ScreenStockItem } from "@/lib/api";

interface ScatterChartProps {
  stocks: ScreenStockItem[];
  xAxis: "peg" | "pe_ttm" | "latest_price" | "target_price_neutral";
  yAxis: "net_profit_growth" | "revenue_growth" | "pe_ttm";
  onBrush?: (range: { xMin: number; xMax: number; yMin: number; yMax: number }) => void;
}

export default function ScatterChart({ stocks, xAxis, yAxis, onBrush }: ScatterChartProps) {
  const data = stocks
    .filter((s) => s[xAxis] != null && s[yAxis] != null)
    .map((s) => ({
      x: s[xAxis] || 0,
      y: s[yAxis] || 0,
      z: 100,
      name: s.name,
      ticker: s.ticker,
      sector: s.sector,
      rating: s.rating,
      latest_price: s.latest_price,
      target_price_neutral: s.target_price_neutral,
      peg: s.peg,
      net_profit_growth: s.net_profit_growth,
    }));

  const handleBrushChange = (range: any) => {
    if (range && onBrush && range.startIndex != null && range.endIndex != null) {
      const filtered = data.slice(range.startIndex, range.endIndex + 1);
      if (filtered.length > 0) {
        const xValues = filtered.map((d) => d.x);
        const yValues = filtered.map((d) => d.y);
        onBrush({
          xMin: Math.min(...xValues),
          xMax: Math.max(...xValues),
          yMin: Math.min(...yValues),
          yMax: Math.max(...yValues),
        });
      }
    }
  };

  const getSectorColor = (sector?: string) => {
    const colors: Record<string, string> = {
      "AI光模块": "#8884d8",
      "AI服务器": "#82ca9d",
      "存储/MCU": "#ffc658",
      "电子制造": "#ff7300",
      "AI芯片": "#00C49F",
      "面板显示": "#FFBB28",
      "化合物半导体": "#FF8042",
    };
    return colors[sector || ""] || "#8884d8";
  };

  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-cfa-muted">
        暂无数据，请调整筛选条件
      </div>
    );
  }

  return (
    <div className="h-full">
      <ResponsiveContainer width="100%" height="100%">
        <ReScatterChart margin={{ top: 20, right: 20, bottom: 40, left: 40 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis
            type="number"
            dataKey="x"
            stroke="#888"
            tick={{ fill: "#888", fontSize: 12 }}
            label={{ value: xAxis.toUpperCase(), position: "insideBottom", offset: -15, fill: "#888", fontSize: 12 }}
          />
          <YAxis
            type="number"
            dataKey="y"
            stroke="#888"
            tick={{ fill: "#888", fontSize: 12 }}
            label={{ value: yAxis, angle: -90, position: "insideLeft", offset: -10, fill: "#888", fontSize: 12 }}
          />
          <ZAxis type="number" dataKey="z" range={[40, 300]} />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const d = payload[0].payload;
                return (
                  <div className="bg-[#1a1a2e] border border-[#333] rounded-lg p-3 shadow-xl text-sm">
                    <p className="font-semibold text-white">{d.name} ({d.ticker})</p>
                    <p className="text-gray-400">{d.sector}</p>
                    <p className="text-gray-300 mt-1">{xAxis}: {d.x?.toFixed(2)}</p>
                    <p className="text-gray-300">{yAxis}: {d.y?.toFixed(2)}</p>
                    <p className="text-gray-300">现价: ¥{d.latest_price}</p>
                    <p className="text-gray-300">目标价: ¥{d.target_price_neutral}</p>
                    <span className={`inline-block mt-1 text-xs px-1.5 py-0.5 rounded-full ${
                      d.rating === "BUY" ? "bg-green-500/20 text-green-400" :
                      d.rating === "SELL" ? "bg-red-500/20 text-red-400" :
                      "bg-yellow-500/20 text-yellow-400"
                    }`}>
                      {d.rating}
                    </span>
                  </div>
                );
              }
              return null;
            }}
          />
          <Scatter data={data} fill="#8884d8">
            {data.map((entry, index) => (
              <circle
                key={index}
                cx={0} cy={0}
                r={6}
                fill={getSectorColor(entry.sector)}
                opacity={0.8}
                stroke="#fff"
                strokeWidth={1}
              />
            ))}
          </Scatter>
          <Brush
            dataKey="x"
            height={30}
            stroke="#8884d8"
            onChange={handleBrushChange}
            tickFormatter={() => ""}
          />
        </ReScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
