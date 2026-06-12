"use client";

import { useState } from "react";
import { motion } from "framer-motion";

interface BubbleData {
  name: string;
  x: number;
  y: number;
  size: number;
  risk: number;
  industry: string;
}

const bubbles: BubbleData[] = [
  { name: "AI服务器PCB", x: 85, y: 92, size: 35, risk: 3, industry: "电子" },
  { name: "高端模拟IC", x: 75, y: 88, size: 28, risk: 4, industry: "半导体" },
  { name: "算力电源", x: 70, y: 82, size: 30, risk: 4, industry: "电力设备" },
  { name: "光模块", x: 65, y: 78, size: 25, risk: 5, industry: "通信" },
  { name: "新能源汽车", x: 90, y: 65, size: 40, risk: 6, industry: "汽车" },
  { name: "半导体设备", x: 55, y: 72, size: 22, risk: 5, industry: "半导体" },
  { name: "工业自动化", x: 45, y: 68, size: 20, risk: 4, industry: "机械" },
  { name: "消费电子", x: 80, y: 55, size: 18, risk: 6, industry: "电子" },
  { name: "面板显示", x: 60, y: 58, size: 15, risk: 5, industry: "电子" },
  { name: "航运港口", x: 40, y: 45, size: 12, risk: 7, industry: "交运" },
];

function getRiskColor(risk: number): string {
  if (risk <= 3) return "#10b981";
  if (risk <= 5) return "#f59e0b";
  return "#ef4444";
}

export default function IndustryMap() {
  const [hoveredBubble, setHoveredBubble] = useState<string | null>(null);

  return (
    <div className="cfa-card p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold">行业机会地图</h3>
      </div>

      <div className="relative h-64 bg-cfa-bg/50 rounded-lg overflow-hidden">
        <div className="absolute inset-0">
          {[25, 50, 75].map((line) => (
            <div key={`h-${line}`}>
              <div
                className="absolute w-full border-t border-cfa-border/30"
                style={{ bottom: `${line}%` }}
              />
              <div
                className="absolute h-full border-l border-cfa-border/30"
                style={{ left: `${line}%` }}
              />
            </div>
          ))}
        </div>

        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-xs text-cfa-muted">
          行业规模 (亿元)
        </div>
        <div className="absolute left-2 top-1/2 -translate-y-1/2 -rotate-90 text-xs text-cfa-muted">
          机会评分
        </div>

        {bubbles.map((bubble, i) => (
          <motion.div
            key={bubble.name}
            className="absolute cursor-pointer"
            style={{
              left: `${bubble.x}%`,
              bottom: `${bubble.y}%`,
              transform: "translate(-50%, 50%)",
            }}
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: i * 0.05, type: "spring" }}
            onMouseEnter={() => setHoveredBubble(bubble.name)}
            onMouseLeave={() => setHoveredBubble(null)}
          >
            <div
              className="rounded-full flex items-center justify-center transition-all"
              style={{
                width: `${bubble.size * 2}px`,
                height: `${bubble.size * 2}px`,
                backgroundColor: `${getRiskColor(bubble.risk)}20`,
                border: `2px solid ${getRiskColor(bubble.risk)}`,
                boxShadow: hoveredBubble === bubble.name
                  ? `0 0 20px ${getRiskColor(bubble.risk)}40`
                  : "none",
              }}
            >
              <span className="text-xs font-medium text-center px-1" style={{ color: getRiskColor(bubble.risk) }}>
                {bubble.name}
              </span>
            </div>

            {hoveredBubble === bubble.name && (
              <motion.div
                initial={{ opacity: 0, y: 5 }}
                animate={{ opacity: 1, y: 0 }}
                className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-cfa-card border border-cfa-border rounded-lg shadow-xl whitespace-nowrap z-10"
              >
                <p className="font-medium text-sm">{bubble.name}</p>
                <p className="text-xs text-cfa-muted">机会评分: {bubble.y}</p>
                <p className="text-xs text-cfa-muted">增速: {bubble.size}%</p>
                <p className="text-xs text-cfa-muted">风险等级: {bubble.risk}/10</p>
              </motion.div>
            )}
          </motion.div>
        ))}

        <div className="absolute top-2 right-2 flex flex-col gap-1">
          <span className="text-xs text-cfa-muted">风险等级</span>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-cfa-success" />
            <span className="text-xs text-cfa-muted">低</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-cfa-warning" />
            <span className="text-xs text-cfa-muted">中</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-cfa-danger" />
            <span className="text-xs text-cfa-muted">高</span>
          </div>
        </div>
      </div>
    </div>
  );
}
