import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import { fetchFredSeries } from "./lib/fred";

export default async function Home() {
  const fiveYearsAgo = new Date();
  fiveYearsAgo.setFullYear(fiveYearsAgo.getFullYear() - 5);
  const cpiStart = fiveYearsAgo.toISOString().split("T")[0];

  const [cpi, unemployment, bondYields, shortRates] = await Promise.all([
    fetchFredSeries("CPIAUCSL", cpiStart, 2),        // monthly CPI, every 2 months
    fetchFredSeries("UNRATE", "2010-01-01", 4),       // unemployment, every 4 months
    fetchFredSeries("GS10", "2010-01-01", 4),         // 10-year yields, every 4 months
    fetchFredSeries("TB3MS", "2010-01-01", 4),        // 3-month rates, every 4 months
  ]);

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar />
      <main className="flex-1 flex flex-col">
        <header className="bg-white border-b border-gray-200 px-8 py-6">
          <h2 className="text-[28px] font-bold text-gray-900 leading-tight">
            Economic Indicators Dashboard
          </h2>
          <p className="text-[14px] text-gray-500 mt-1">
            Real-time economic data from the Federal Reserve Economic Data (FRED) system
          </p>
        </header>
        <section className="flex-1 p-6">
          <Dashboard
            cpi={cpi}
            unemployment={unemployment}
            bondYields={bondYields}
            shortRates={shortRates}
          />
        </section>
      </main>
    </div>
  );
}
