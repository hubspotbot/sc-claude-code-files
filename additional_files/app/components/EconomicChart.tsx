"use client";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

export interface ChartDataPoint {
  date: string;
  value: number;
}

interface EconomicChartProps {
  data: ChartDataPoint[];
  yAxisLabel?: string;
  yDomain?: [number | "auto", number | "auto"];
  tickFormatter?: (v: number) => string;
}

export default function EconomicChart({
  data,
  yDomain = ["auto", "auto"],
  tickFormatter = (v) => String(v),
}: EconomicChartProps) {
  return (
    <div className="relative w-full h-full">
      <div className="absolute top-2 left-3 z-10 bg-white border border-gray-200 rounded px-1.5 py-0.5">
        <span className="text-[10px] font-bold text-[#5b9abd] tracking-wider">FRED</span>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 28, right: 12, bottom: 4, left: 8 }}>
          <defs>
            <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#2563eb" stopOpacity={0.15} />
              <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 10, fill: "#6b7280" }}
            tickLine={false}
            axisLine={{ stroke: "#e5e7eb" }}
            interval="preserveStartEnd"
          />
          <YAxis
            tickFormatter={tickFormatter}
            tick={{ fontSize: 10, fill: "#6b7280" }}
            tickLine={false}
            axisLine={false}
            domain={yDomain}
            width={42}
          />
          <Tooltip
            contentStyle={{ fontSize: 11, borderRadius: 6, border: "1px solid #e5e7eb" }}
            formatter={(val: number) => [tickFormatter(val), ""]}
          />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#2563eb"
            strokeWidth={1.5}
            fill="url(#chartGradient)"
            dot={false}
            activeDot={{ r: 3, fill: "#2563eb" }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
