import EconomicChart, { ChartDataPoint } from "./EconomicChart";

interface ChartCardProps {
  title: string;
  source: string;
  data: ChartDataPoint[];
  yDomain?: [number | "auto", number | "auto"];
  tickFormatter?: (v: number) => string;
}

export default function ChartCard({ title, source, data, yDomain, tickFormatter }: ChartCardProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg flex flex-col overflow-hidden">
      <div className="px-4 pt-4 pb-2">
        <h3 className="text-[13.5px] font-semibold text-gray-900 leading-snug">{title}</h3>
      </div>
      <div className="flex-1 px-2 pb-2" style={{ minHeight: 220 }}>
        <EconomicChart
          data={data}
          yDomain={yDomain}
          tickFormatter={tickFormatter}
        />
      </div>
      <div className="px-4 pb-3 flex items-end justify-between gap-2">
        <p className="text-[10px] text-gray-400 leading-snug">{source}</p>
        <a
          href="https://fred.stlouisfed.org"
          target="_blank"
          rel="noopener noreferrer"
          className="text-[10px] text-blue-500 hover:underline whitespace-nowrap shrink-0"
        >
          fred.stlouisfed.org
        </a>
      </div>
    </div>
  );
}
