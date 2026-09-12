import React from "react";

export const StatusBadge = ({ status }) => {
  const getBadgeStyle = () => {
    const s = String(status).toLowerCase();
    
    if (s === "critical") return "bg-red-50 text-red-700 border-red-200 animate-pulse font-bold";
    if (s === "high") return "bg-orange-50 text-orange-700 border-orange-200 font-bold";
    if (s === "medium") return "bg-amber-50 text-amber-700 border-amber-200 font-semibold";
    if (s === "low") return "bg-blue-50 text-blue-700 border-blue-200 font-semibold";

    if (s === "open") return "bg-rose-50 text-rose-700 border-rose-200 font-semibold";
    if (s === "assigned") return "bg-purple-50 text-purple-700 border-purple-200 font-semibold";
    if (s === "in progress") return "bg-amber-50 text-amber-700 border-amber-200 font-semibold";
    if (s === "resolved" || s === "closed") return "bg-emerald-50 text-emerald-700 border-emerald-200 font-bold";

    if (s === "active") return "bg-emerald-50 text-emerald-700 border-emerald-200 font-bold";
    if (s === "reviewed") return "bg-blue-50 text-blue-700 border-blue-200 font-semibold";
    if (s === "maintenance") return "bg-amber-50 text-amber-700 border-amber-200 font-semibold";

    return "bg-slate-100 text-slate-700 border-slate-200 font-medium";
  };

  return (
    <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs tracking-wide shadow-xs ${getBadgeStyle()}`}>
      {status}
    </span>
  );
};
