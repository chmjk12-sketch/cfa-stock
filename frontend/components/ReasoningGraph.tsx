"use client";

import { useState } from "react";
import { motion } from "framer-motion";

interface NodeData {
  id: string;
  label: string;
  score?: number;
  details?: string;
  type: "entity" | "dimension" | "conclusion" | "modifier";
  x: number;
  y: number;
}

interface EdgeData {
  id: string;
  source: string;
  target: string;
  label?: string;
  dashed?: boolean;
}

const nodes: NodeData[] = [
  { id: "stock", label: "Stock", type: "entity", x: 400, y: 20 },
  { id: "sector", label: "Sector (A+D)", score: 9, type: "entity", x: 150, y: 120 },
  { id: "financial", label: "Financial", score: 8, type: "entity", x: 320, y: 120 },
  { id: "valuation", label: "Valuation", score: 8, type: "entity", x: 480, y: 120 },
  { id: "growth", label: "Growth", score: 9, type: "entity", x: 640, y: 120 },
  { id: "risk", label: "Risk", score: 7, type: "entity", x: 800, y: 120 },
  { id: "ff", label: "Five Forces", score: 9, type: "dimension", x: 50, y: 220 },
  { id: "lc", label: "Lifecycle", score: 9, type: "dimension", x: 130, y: 220 },
  { id: "eb", label: "Barriers", score: 9, type: "dimension", x: 210, y: 220 },
  { id: "cp", label: "Strategy", score: 9, type: "dimension", x: 290, y: 220 },
  { id: "mod1", label: "FQ → Valuation", type: "modifier", x: 350, y: 200 },
  { id: "mod2", label: "Growth → Valuation", type: "modifier", x: 560, y: 200 },
  { id: "mod3", label: "Risk → Valuation", type: "modifier", x: 720, y: 200 },
  { id: "conclusion", label: "Conclusion", score: 8.5, details: "BUY | High", type: "conclusion", x: 400, y: 340 },
];

const edges: EdgeData[] = [
  { id: "e1", source: "stock", target: "sector", label: "E1" },
  { id: "e2", source: "stock", target: "financial", label: "E2" },
  { id: "e3", source: "stock", target: "valuation", label: "E3" },
  { id: "e4", source: "stock", target: "growth", label: "E4" },
  { id: "e5", source: "stock", target: "risk", label: "E5" },
  { id: "e1b", source: "sector", target: "ff", label: "E1b" },
  { id: "e1c", source: "sector", target: "lc", label: "E1c" },
  { id: "e1d", source: "sector", target: "eb", label: "E1d" },
  { id: "e1e", source: "sector", target: "cp", label: "E1e" },
  { id: "e6", source: "financial", target: "mod1", label: "E6", dashed: true },
  { id: "e6b", source: "mod1", target: "valuation", dashed: true },
  { id: "e7", source: "growth", target: "mod2", label: "E7", dashed: true },
  { id: "e7b", source: "mod2", target: "valuation", dashed: true },
  { id: "e8", source: "risk", target: "mod3", label: "E8", dashed: true },
  { id: "e8b", source: "mod3", target: "valuation", dashed: true },
  { id: "e9", source: "sector", target: "conclusion", label: "20%" },
  { id: "e10", source: "financial", target: "conclusion", label: "25%" },
  { id: "e11", source: "valuation", target: "conclusion", label: "25%" },
  { id: "e12", source: "growth", target: "conclusion", label: "15%" },
  { id: "e13", source: "risk", target: "conclusion", label: "15%" },
];

function getNodeColor(type: string): string {
  switch (type) {
    case "entity": return "#3b82f6";
    case "dimension": return "#9ca3af";
    case "conclusion": return "#10b981";
    case "modifier": return "#f59e0b";
    default: return "#6b7280";
  }
}

export default function ReasoningGraph() {
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const selectedData = nodes.find((n) => n.id === selectedNode);

  return (
    <div className="h-[500px] cfa-card overflow-hidden relative">
      <div className="p-4 border-b border-cfa-border">
        <h3 className="font-semibold">本体推理图谱</h3>
        <p className="text-xs text-cfa-muted">点击节点查看推理详情</p>
      </div>
      <div className="h-[440px] relative bg-cfa-bg/30">
        <svg width="100%" height="100%" viewBox="0 0 900 400">
          {/* Edges */}
          {edges.map((edge) => {
            const source = nodes.find((n) => n.id === edge.source);
            const target = nodes.find((n) => n.id === edge.target);
            if (!source || !target) return null;
            return (
              <g key={edge.id}>
                <line
                  x1={source.x + 60}
                  y1={source.y + 20}
                  x2={target.x + 60}
                  y2={target.y + 20}
                  stroke={edge.dashed ? "#f59e0b" : "#1f2937"}
                  strokeWidth={2}
                  strokeDasharray={edge.dashed ? "5,5" : undefined}
                />
                {edge.label && (
                  <text
                    x={(source.x + target.x) / 2 + 60}
                    y={(source.y + target.y) / 2 + 15}
                    fill="#6b7280"
                    fontSize={10}
                    textAnchor="middle"
                  >
                    {edge.label}
                  </text>
                )}
              </g>
            );
          })}

          {/* Nodes */}
          {nodes.map((node) => (
            <g
              key={node.id}
              onClick={() => setSelectedNode(node.id)}
              className="cursor-pointer"
            >
              <rect
                x={node.x}
                y={node.y}
                width={120}
                height={node.type === "modifier" ? 30 : 50}
                rx={8}
                fill="rgba(17, 24, 39, 0.9)"
                stroke={getNodeColor(node.type)}
                strokeWidth={node.type === "modifier" ? 1 : 2}
                strokeDasharray={node.type === "modifier" ? "3,3" : undefined}
              />
              <text
                x={node.x + 60}
                y={node.y + 18}
                fill={getNodeColor(node.type)}
                fontSize={12}
                fontWeight="bold"
                textAnchor="middle"
              >
                {node.label}
              </text>
              {node.score !== undefined && (
                <text
                  x={node.x + 60}
                  y={node.y + 38}
                  fill="#f3f4f6"
                  fontSize={11}
                  textAnchor="middle"
                >
                  {node.score}/10
                </text>
              )}
            </g>
          ))}
        </svg>
      </div>

      {selectedNode && selectedData && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute bottom-4 left-4 right-4 p-4 bg-cfa-card border border-cfa-border rounded-lg shadow-xl"
        >
          <div className="flex justify-between items-start">
            <div>
              <h4 className="font-semibold">{selectedData.label}</h4>
              <p className="text-sm text-cfa-muted mt-1">
                {selectedNode === "conclusion"
                  ? "综合评分 = Sector×0.20 + Financial×0.25 + Valuation×0.25 + Growth×0.15 + Risk×0.15"
                  : selectedData.details || "点击节点查看详细推理过程"}
              </p>
            </div>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-cfa-muted hover:text-cfa-text"
            >
              ✕
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
}
