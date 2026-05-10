"use client";

import ChartCard from "./ChartCard";
import type { FredObservation } from "../lib/fred";

interface DashboardProps {
  cpi: FredObservation[];
  unemployment: FredObservation[];
  bondYields: FredObservation[];
  shortRates: FredObservation[];
}

export default function Dashboard({ cpi, unemployment, bondYields, shortRates }: DashboardProps) {
  const charts = [
    {
      title: "CPI - last five years",
      source: "Source: U.S. Bureau of Labor Statistics via FRED®",
      data: cpi,
      yDomain: ["auto", "auto"] as ["auto", "auto"],
      tickFormatter: (v: number) => v.toFixed(0),
    },
    {
      title: "Infra-Annual Labor Statistics: Unemployment Rate Total",
      source: "Source: Organization for Economic Co-operation and Development via FRED®",
      data: unemployment,
      yDomain: [0, "auto"] as [number, "auto"],
      tickFormatter: (v: number) => `${v}%`,
    },
    {
      title: "Interest Rates: Long-Term Government Bond Yields: 10-Year",
      source: "Source: Organization for Economic Co-operation and Development via FRED®",
      data: bondYields,
      yDomain: [0, "auto"] as [number, "auto"],
      tickFormatter: (v: number) => `${v}%`,
    },
    {
      title: "Interest Rates: 3-Month or 90-Day Rates and Yields",
      source: "Source: Organization for Economic Co-operation and Development via FRED®",
      data: shortRates,
      yDomain: [0, "auto"] as [number, "auto"],
      tickFormatter: (v: number) => `${v}%`,
    },
  ];

  return (
    <div className="grid grid-cols-2 gap-5">
      {charts.map((chart) => (
        <ChartCard
          key={chart.title}
          title={chart.title}
          source={chart.source}
          data={chart.data}
          yDomain={chart.yDomain}
          tickFormatter={chart.tickFormatter}
        />
      ))}
    </div>
  );
}
