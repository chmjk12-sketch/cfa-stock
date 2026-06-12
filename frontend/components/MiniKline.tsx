"use client";

import { useState, useEffect } from "react";
import { AreaChart, Area, ResponsiveContainer } from "recharts";
import { getKline } from "@/lib/api";

interface MiniKlineProps {
  ticker: string;
}

export default function MiniKline({ ticker }: MiniKlineProps) {
  const [data, setData] = useState<{ close: number }[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getKline(ticker, "30d")
      .then((kline) => {
        setData(kline.map((k) => ({ close: k.close })));
      })
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  }, [ticker]);

  if (loading || data.length < 2) {
    return <div className="h-8 w-16 bg-cfa-bg/50 rounded animate-pulse" />;
  }

  const isUp = data[data.length - 1].close >= data[0].close;
  const color = isUp ? "#4ade80" : "#f87171";

  return (
    <div className="h-8 w-16">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data}>
          <defs>
            <linearGradient id={`gradient-${ticker}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={color} stopOpacity={0.3} />
              <stop offset="100%" stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>
          <Area
            type="monotone"
            dataKey="close"
            stroke={color}
            fill={`url(#gradient-${ticker})`}
            strokeWidth={1.5}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
