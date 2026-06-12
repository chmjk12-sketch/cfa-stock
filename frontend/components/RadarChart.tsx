"use client";

import { useMemo } from "react";

interface RadarData {
  subject: string;
  A: number;
  fullMark: number;
}

interface RadarChartProps {
  data: RadarData[];
}

export default function RadarChart({ data }: RadarChartProps) {
  const size = 200;
  const center = size / 2;
  const radius = 70;
  const levels = 5;

  const angles = useMemo(() => {
    const angleSlice = (Math.PI * 2) / data.length;
    return data.map((_, i) => angleSlice * i - Math.PI / 2);
  }, [data]);

  const getPoint = (value: number, angle: number) => {
    const r = (value / 10) * radius;
    return {
      x: center + r * Math.cos(angle),
      y: center + r * Math.sin(angle),
    };
  };

  const pathData = data
    .map((d, i) => {
      const point = getPoint(d.A, angles[i]);
      return `${i === 0 ? "M" : "L"} ${point.x} ${point.y}`;
    })
    .join(" ") + " Z";

  return (
    <svg width={size} height={size} className="mx-auto">
      {Array.from({ length: levels }, (_, i) => {
        const r = ((i + 1) / levels) * radius;
        const points = angles.map((angle) => ({
          x: center + r * Math.cos(angle),
          y: center + r * Math.sin(angle),
        }));
        return (
          <polygon
            key={i}
            points={points.map((p) => `${p.x},${p.y}`).join(" ")}
            fill="none"
            stroke="#1f2937"
            strokeWidth={1}
          />
        );
      })}

      {angles.map((angle, i) => {
        const end = {
          x: center + radius * Math.cos(angle),
          y: center + radius * Math.sin(angle),
        };
        return (
          <line
            key={i}
            x1={center}
            y1={center}
            x2={end.x}
            y2={end.y}
            stroke="#1f2937"
            strokeWidth={1}
          />
        );
      })}

      <path
        d={pathData}
        fill="rgba(59, 130, 246, 0.2)"
        stroke="#3b82f6"
        strokeWidth={2}
      />

      {data.map((d, i) => {
        const point = getPoint(d.A, angles[i]);
        return (
          <circle
            key={i}
            cx={point.x}
            cy={point.y}
            r={4}
            fill="#3b82f6"
            stroke="#0a0e1a"
            strokeWidth={2}
          />
        );
      })}

      {data.map((d, i) => {
        const angle = angles[i];
        const labelRadius = radius + 20;
        const x = center + labelRadius * Math.cos(angle);
        const y = center + labelRadius * Math.sin(angle);
        return (
          <text
            key={i}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="#9ca3af"
            fontSize={11}
          >
            {d.subject}
          </text>
        );
      })}
    </svg>
  );
}
