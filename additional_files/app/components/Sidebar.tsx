"use client";

import { useState } from "react";

const navItems = [
  { label: "Key Indicators", icon: "trending" },
  { label: "Inflation", icon: "trending" },
  { label: "Employment", icon: "briefcase" },
  { label: "Interest Rates", icon: "trending-down" },
  { label: "Economic Growth", icon: "trending" },
  { label: "Exchange Rates", icon: "globe" },
  { label: "Housing", icon: "home" },
  { label: "Consumer Spending", icon: "shopping-cart" },
];

function NavIcon({ type }: { type: string }) {
  if (type === "briefcase") {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
        <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
      </svg>
    );
  }
  if (type === "globe") {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <line x1="2" y1="12" x2="22" y2="12" />
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
      </svg>
    );
  }
  if (type === "home") {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
        <polyline points="9,22 9,12 15,12 15,22" />
      </svg>
    );
  }
  if (type === "shopping-cart") {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="9" cy="21" r="1" />
        <circle cx="20" cy="21" r="1" />
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" />
      </svg>
    );
  }
  if (type === "trending-down") {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="23,18 13.5,8.5 8.5,13.5 1,6" />
        <polyline points="17,18 23,18 23,12" />
      </svg>
    );
  }
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="23,6 13.5,15.5 8.5,10.5 1,18" />
      <polyline points="17,6 23,6 23,12" />
    </svg>
  );
}

export default function Sidebar() {
  const [active, setActive] = useState("Key Indicators");

  return (
    <aside className="flex flex-col w-[195px] min-h-screen bg-white border-r border-gray-200 shrink-0">
      <div className="px-5 pt-6 pb-4">
        <h1 className="font-bold text-[15px] text-gray-900 leading-tight">FRED Indicators</h1>
        <p className="text-[12px] text-gray-500 mt-0.5">Economic Data Dashboard</p>
      </div>

      <nav className="flex-1 px-3 pb-4">
        {navItems.map((item) => {
          const isActive = item.label === active;
          return (
            <button
              key={item.label}
              onClick={() => setActive(item.label)}
              className={`w-full flex items-center gap-2 px-2.5 py-2 rounded-md mb-0.5 text-[12.5px] font-medium transition-colors text-left whitespace-nowrap ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              <span className={isActive ? "text-white" : "text-gray-500"}>
                <NavIcon type={item.icon} />
              </span>
              <span className="flex-1">{item.label}</span>
              {isActive ? (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="6,9 12,15 18,9" />
                </svg>
              ) : (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-gray-400">
                  <polyline points="9,6 15,12 9,18" />
                </svg>
              )}
            </button>
          );
        })}
      </nav>

      <div className="px-5 py-4 border-t border-gray-200">
        <p className="text-[11px] text-gray-400 leading-snug">
          Data provided by Federal Reserve Economic Data (FRED)
        </p>
      </div>
    </aside>
  );
}
