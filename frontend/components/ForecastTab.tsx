"use client";

import { useState, useEffect } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, LineChart, Line, Legend,
} from "recharts";
import { getForecast, type ForecastResponse } from "@/lib/api";

interface ForecastTabProps {
  ticker: string;
}

export default function ForecastTab({ ticker }: ForecastTabProps) {
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getForecast(ticker)
      .then((f) => setForecast(f))
      .catch(() => setForecast(null))
      .finally(() => setLoading(false));
  }, [ticker]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-6 h-6 border-2 border-cfa-muted border-t-cfa-accent rounded-full animate-spin" />
      </div>
    );
  }

  if (!forecast) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-cfa-muted">
        <p className="text-lg mb-2">暂无机构预测数据</p>
        <p className="text-sm">数据将在每日收盘后自动更新</p>
      </div>
    );
  }

  // 目标价对比数据
  const targetPriceData = [
    { name: "现价", value: 158, fill: "#6366f1" },
    { name: "悲观", value: forecast.target_price_pessimistic || 0, fill: "#f59e0b" },
    { name: "中性", value: forecast.target_price_neutral || 0, fill: "#3b82f6" },
    { name: "乐观", value: forecast.target_price_optimistic || 0, fill: "#22c55e" },
  ].filter(d => d.value > 0);

  // 盈利预测趋势（模拟数据）
  const epsData = [
    { year: "2024E", optimistic: 8.5, neutral: 7.2, pessimistic: 6.0 },
    { year: "2025E", optimistic: 12.0, neutral: 10.5, pessimistic: 8.5 },
    { year: "2026E", optimistic: 18.0, neutral: 15.0, pessimistic: 12.0 },
    { year: "2027E", optimistic: 25.0, neutral: 20.0, pessimistic: 15.0 },
  ];

  return (
    <div className="space-y-6">
      {/* 汇总卡片 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="cfa-card p-4 text-center">
          <p className="text-2xl font-bold text-cfa-accent">{forecast.source_count || "-"}</p>
          <p className="text-xs text-cfa-muted mt-1">覆盖机构</p>
        </div>
        <div className="cfa-card p-4 text-center">
          <p className="text-2xl font-bold text-blue-400">
            ¥{forecast.target_price_neutral?.toFixed(0) || "-"}
          </p>
          <p className="text-xs text-cfa-muted mt-1">中性目标价</p>
        </div>
        <div className="cfa-card p-4 text-center">
          <p className="text-2xl font-bold text-green-400">
            ¥{forecast.target_price_optimistic?.toFixed(0) || "-"}
          </p>
          <p className="text-xs text-cfa-muted mt-1">乐观目标价</p>
        </div>
        <div className="cfa-card p-4 text-center">
          <p className="text-2xl font-bold text-yellow-400">
            ¥{forecast.target_price_pessimistic?.toFixed(0) || "-"}
          </p>
          <p className="text-xs text-cfa-muted mt-1">悲观目标价</p>
        </div>
      </div>

      {/* 关键指标 */}
      <div className="grid grid-cols-3 gap-4">
        <div className="cfa-card p-4">
          <p className="text-xs text-cfa-muted mb-1">PEG</p>
          <p className={`text-xl font-bold ${forecast.peg != null && forecast.peg < 1 ? "text-green-400" : "text-white"}`}>
            {forecast.peg?.toFixed(2) || "-"}
          </p>
          {forecast.peg != null && forecast.peg < 1 && (
            <p className="text-xs text-green-400/70 mt-0.5">PEG &lt; 1 低估</p>
          )}
        </div>
        <div className="cfa-card p-4">
          <p className="text-xs text-cfa-muted mb-1">净利润增速</p>
          <p className="text-xl font-bold text-white">
            {forecast.net_profit_growth != null ? `${(forecast.net_profit_growth * 100).toFixed(1)}%` : "-"}
          </p>
        </div>
        <div className="cfa-card p-4">
          <p className="text-xs text-cfa-muted mb-1">上涨空间(中性)</p>
          <p className={`text-xl font-bold ${forecast.upside_neutral != null && forecast.upside_neutral > 0 ? "text-green-400" : "text-red-400"}`}>
            {forecast.upside_neutral != null ? `${(forecast.upside_neutral * 100).toFixed(0)}%` : "-"}
          </p>
        </div>
      </div>

      {/* 目标价对比图 */}
      <div className="cfa-card p-6">
        <h3 className="font-semibold mb-4 text-sm">目标价 vs 现价</h3>
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={targetPriceData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis type="number" stroke="#888" tick={{ fill: "#888", fontSize: 12 }} />
              <YAxis dataKey="name" type="category" stroke="#888" width={50} tick={{ fill: "#888", fontSize: 12 }} />
              <Tooltip
                contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                formatter={(value: number) => [`¥${value.toFixed(0)}`, ""]}
              />
              <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                {targetPriceData.map((entry, index) => (
                  <rect key={index} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 盈利预测趋势 */}
      <div className="cfa-card p-6">
        <h3 className="font-semibold mb-4 text-sm">盈利预测趋势 (EPS)</h3>
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={epsData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="year" stroke="#888" tick={{ fill: "#888", fontSize: 12 }} />
              <YAxis stroke="#888" tick={{ fill: "#888", fontSize: 12 }} />
              <Tooltip contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }} />
              <Legend wrapperStyle={{ fontSize: 12, color: "#888" }} />
              <Line type="monotone" dataKey="optimistic" stroke="#4ade80" strokeWidth={2} name="乐观" dot={{ r: 4 }} />
              <Line type="monotone" dataKey="neutral" stroke="#8884d8" strokeWidth={2} name="中性" dot={{ r: 4 }} />
              <Line type="monotone" dataKey="pessimistic" stroke="#f87171" strokeWidth={2} name="悲观" dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
