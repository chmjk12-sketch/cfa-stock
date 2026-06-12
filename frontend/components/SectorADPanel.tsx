"use client";

import { motion } from "framer-motion";

interface SectorAnalysis {
  five_forces: {
    supplier_power: string;
    buyer_power: string;
    threat_entrants: string;
    threat_substitutes: string;
    rivalry_intensity: string;
    switching_cost: string;
    score: number;
  };
  lifecycle: {
    lifecycle_stage: string;
    segment_growth_rate: number;
    segment_penetration: number;
    score: number;
  };
  barriers: {
    economies_of_scale: number;
    product_diff: number;
    capital_req: number;
    switching_cost: number;
    sustainability: string;
    score: number;
  };
  strategy: {
    generic_strategy: string;
    strategy_consistency: string;
    moat_from_strategy: string;
    score: number;
  };
  score: number;
}

interface SectorADPanelProps {
  analysis: SectorAnalysis;
}

function ScoreStars({ score }: { score: number }) {
  return (
    <div className="flex gap-0.5">
      {Array.from({ length: 5 }, (_, i) => (
        <div
          key={i}
          className={`w-4 h-4 rounded-sm ${
            i < Math.round(score / 2) ? "bg-cfa-accent" : "bg-cfa-border"
          }`}
        />
      ))}
    </div>
  );
}

function ForceBadge({ value }: { value: string }) {
  const colors: Record<string, string> = {
    high: "text-cfa-danger",
    medium: "text-cfa-warning",
    low: "text-cfa-success",
  };
  const labels: Record<string, string> = {
    high: "高",
    medium: "中",
    low: "低",
  };
  return (
    <span className={`text-xs font-medium ${colors[value] || "text-cfa-muted"}`}>
      {labels[value] || value}
    </span>
  );
}

export default function SectorADPanel({ analysis }: SectorADPanelProps) {
  return (
    <div className="cfa-card p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold">行业深度分析 (A+D 四维框架)</h3>
        <div className="flex items-center gap-2">
          <span className="text-sm text-cfa-muted">综合评分</span>
          <span className="text-2xl font-bold text-cfa-accent">{analysis.score}</span>
          <span className="text-sm text-cfa-muted">/10</span>
        </div>
      </div>

      <div className="space-y-4">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 bg-cfa-bg rounded-lg"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-cfa-accent">① 波特五力</span>
              <span className="text-xs text-cfa-muted">(Porter&apos;s Five Forces)</span>
            </div>
            <div className="flex items-center gap-2">
              <ScoreStars score={analysis.five_forces.score} />
              <span className="text-lg font-bold">{analysis.five_forces.score}</span>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-2 text-sm">
            <div className="flex justify-between">
              <span className="text-cfa-muted">供应商议价能力</span>
              <ForceBadge value={analysis.five_forces.supplier_power} />
            </div>
            <div className="flex justify-between">
              <span className="text-cfa-muted">买方议价能力</span>
              <ForceBadge value={analysis.five_forces.buyer_power} />
            </div>
            <div className="flex justify-between">
              <span className="text-cfa-muted">新进入者威胁</span>
              <ForceBadge value={analysis.five_forces.threat_entrants} />
            </div>
            <div className="flex justify-between">
              <span className="text-cfa-muted">替代品威胁</span>
              <ForceBadge value={analysis.five_forces.threat_substitutes} />
            </div>
            <div className="flex justify-between">
              <span className="text-cfa-muted">现有竞争强度</span>
              <ForceBadge value={analysis.five_forces.rivalry_intensity} />
            </div>
            <div className="flex justify-between">
              <span className="text-cfa-muted">转换成本</span>
              <ForceBadge value={analysis.five_forces.switching_cost} />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="p-4 bg-cfa-bg rounded-lg"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-cfa-accent">② 行业生命周期</span>
              <span className="text-xs text-cfa-muted">(Industry Lifecycle)</span>
            </div>
            <div className="flex items-center gap-2">
              <ScoreStars score={analysis.lifecycle.score} />
              <span className="text-lg font-bold">{analysis.lifecycle.score}</span>
            </div>
          </div>
          <div className="flex items-center gap-6 text-sm">
            <div>
              <span className="text-cfa-muted">阶段: </span>
              <span className="font-medium">
                {analysis.lifecycle.lifecycle_stage === "growth" ? "成长期" : 
                 analysis.lifecycle.lifecycle_stage === "mature" ? "成熟期" : "衰退期"}
              </span>
            </div>
            <div>
              <span className="text-cfa-muted">子赛道增速: </span>
              <span className="font-medium text-cfa-success">{analysis.lifecycle.segment_growth_rate}%</span>
            </div>
            <div>
              <span className="text-cfa-muted">渗透率: </span>
              <span className="font-medium">{(analysis.lifecycle.segment_penetration * 100).toFixed(0)}%</span>
            </div>
          </div>
          <div className="mt-3 h-16 relative">
            <svg viewBox="0 0 200 60" className="w-full h-full">
              <path
                d="M 0 50 Q 50 50 80 40 Q 110 30 130 20 Q 150 10 200 5"
                fill="none"
                stroke="#3b82f6"
                strokeWidth={2}
              />
              <circle
                cx={analysis.lifecycle.segment_penetration * 200}
                cy={50 - (analysis.lifecycle.segment_penetration * 45)}
                r={5}
                fill="#10b981"
                stroke="#0a0e1a"
                strokeWidth={2}
              />
              <text x={10} y={55} fill="#6b7280" fontSize={8}>导入期</text>
              <text x={80} y={55} fill="#6b7280" fontSize={8}>成长期</text>
              <text x={150} y={55} fill="#6b7280" fontSize={8}>成熟期</text>
            </svg>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="p-4 bg-cfa-bg rounded-lg"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-cfa-accent">③ Bain 进入壁垒</span>
              <span className="text-xs text-cfa-muted">(Entry Barriers)</span>
            </div>
            <div className="flex items-center gap-2">
              <ScoreStars score={analysis.barriers.score} />
              <span className="text-lg font-bold">{analysis.barriers.score}</span>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              { label: "规模经济", value: analysis.barriers.economies_of_scale },
              { label: "产品差异化", value: analysis.barriers.product_diff },
              { label: "资本需求", value: analysis.barriers.capital_req },
              { label: "转换成本", value: analysis.barriers.switching_cost },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between">
                <span className="text-cfa-muted">{item.label}</span>
                <div className="flex gap-0.5">
                  {Array.from({ length: 5 }, (_, i) => (
                    <div
                      key={i}
                      className={`w-3 h-3 rounded-sm ${
                        i < item.value ? "bg-cfa-accent" : "bg-cfa-border"
                      }`}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
          <div className="mt-2 text-sm">
            <span className="text-cfa-muted">可持续性: </span>
            <span className={`font-medium ${
              analysis.barriers.sustainability === "high" ? "text-cfa-success" : "text-cfa-warning"
            }`}>
              {analysis.barriers.sustainability === "high" ? "高 (5年+)" : "中等"}
            </span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="p-4 bg-cfa-bg rounded-lg"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-cfa-accent">④ Porter 竞争战略</span>
              <span className="text-xs text-cfa-muted">(Competitive Strategy)</span>
            </div>
            <div className="flex items-center gap-2">
              <ScoreStars score={analysis.strategy.score} />
              <span className="text-lg font-bold">{analysis.strategy.score}</span>
            </div>
          </div>
          <div className="flex items-center gap-6 text-sm">
            <div>
              <span className="text-cfa-muted">通用战略: </span>
              <span className="font-medium">
                {analysis.strategy.generic_strategy === "differentiation" ? "差异化" :
                 analysis.strategy.generic_strategy === "cost_leadership" ? "成本领先" : "聚焦"}
              </span>
            </div>
            <div>
              <span className="text-cfa-muted">执行一致性: </span>
              <span className={`font-medium ${
                analysis.strategy.strategy_consistency === "high" ? "text-cfa-success" : "text-cfa-warning"
              }`}>
                {analysis.strategy.strategy_consistency === "high" ? "高" : "中"}
              </span>
            </div>
            <div>
              <span className="text-cfa-muted">战略护城河: </span>
              <span className={`font-medium ${
                analysis.strategy.moat_from_strategy === "wide" ? "text-cfa-success" : 
                analysis.strategy.moat_from_strategy === "narrow" ? "text-cfa-warning" : "text-cfa-danger"
              }`}>
                {analysis.strategy.moat_from_strategy === "wide" ? "宽" :
                 analysis.strategy.moat_from_strategy === "narrow" ? "窄" : "无"}
              </span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
