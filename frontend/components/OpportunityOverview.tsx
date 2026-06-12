"use client";

import { motion } from "framer-motion";

export default function OpportunityOverview() {
  return (
    <div className="cfa-card p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-semibold">市场机会总览</h2>
          <p className="text-xs text-cfa-muted mt-0.5">更新于: 2024-05-20</p>
        </div>
        <button className="text-cfa-muted hover:text-cfa-accent">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
      </div>

      <div className="flex items-end gap-2 mb-4">
        <motion.span
          className="text-5xl font-bold text-cfa-success"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          12
        </motion.span>
        <span className="text-lg text-cfa-muted mb-1.5">个高价值投资机会</span>
      </div>

      <div className="flex items-center gap-2 mb-4">
        <span className="text-sm text-cfa-muted">Opportunity Score</span>
        <div className="flex-1 h-2 bg-cfa-bg rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-cfa-danger via-cfa-warning to-cfa-success"
            initial={{ width: 0 }}
            animate={{ width: "82%" }}
            transition={{ duration: 1, delay: 0.3 }}
          />
        </div>
        <span className="text-lg font-bold">82</span>
        <span className="text-sm text-cfa-muted">/100</span>
      </div>

      <div className="flex gap-2">
        {["AI服务器PCB ↑", "高端模拟IC ↑", "算力电源 ↑"].map((tag, i) => (
          <span
            key={i}
            className="text-xs px-2.5 py-1 rounded-full bg-cfa-accent/10 text-cfa-accent border border-cfa-accent/20"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}
