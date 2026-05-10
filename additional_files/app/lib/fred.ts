export interface FredObservation {
  date: string;
  value: number;
}

interface FredApiResponse {
  observations: { date: string; value: string }[];
}

export async function fetchFredSeries(
  seriesId: string,
  startDate: string,
  keepEveryNMonths: number = 1
): Promise<FredObservation[]> {
  const apiKey = process.env.FRED_API_KEY;
  if (!apiKey) throw new Error("FRED_API_KEY is not set");

  const url = `https://api.stlouisfed.org/fred/series/observations?series_id=${seriesId}&api_key=${apiKey}&file_type=json&observation_start=${startDate}&sort_order=asc`;

  const res = await fetch(url, { next: { revalidate: 3600 } });
  if (!res.ok) throw new Error(`FRED API error ${res.status} for ${seriesId}`);

  const json: FredApiResponse = await res.json();

  return json.observations
    .filter((o) => o.value !== "." && !isNaN(parseFloat(o.value)))
    .filter((_, i) => i % keepEveryNMonths === 0)
    .map((o) => ({
      date: formatDate(o.date, keepEveryNMonths),
      value: parseFloat(parseFloat(o.value).toFixed(2)),
    }));
}

function formatDate(isoDate: string, granularity: number): string {
  const [year, month] = isoDate.split("-").map(Number);
  const shortYear = String(year).slice(2);
  const monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  const monthName = monthNames[month - 1];

  // Annual granularity: just show the year
  if (granularity >= 12) return String(year);

  // Quarterly or coarser: show "Jan 20" style
  if (granularity >= 3) return `${monthName} ${shortYear}`;

  // Monthly: show "Jan 20" style
  return `${monthName} ${shortYear}`;
}
