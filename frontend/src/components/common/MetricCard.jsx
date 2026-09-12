import React from "react";
import { TrendingUp, TrendingDown } from "lucide-react";

export const MetricCard = ({ title, value, unit, change, isPositive, icon: Icon, color = "blue", subtitle }) => {
  const colorMap = {
    blue: "border-sky-200 bg-gradient-to-br from-sky-50/80 to-white text-sky-700 icon-bg:bg-sky-100 icon-text:text-sky-600",
    emerald: "border-emerald-200 bg-gradient-to-br from-emerald-50/80 to-white text-emerald-700 icon-bg:bg-emerald-100 icon-text:text-emerald-600",
    amber: "border-amber-200 bg-gradient-to-br from-amber-50/80 to-white text-amber-700 icon-bg:bg-amber-100 icon-text:text-amber-600",
    purple: "border-purple-200 bg-gradient-to-br from-purple-50/80 to-white text-purple-700 icon-bg:bg-purple-100 icon-text:text-purple-600",
    rose: "border-rose-200 bg-gradient-to-br from-rose-50/80 to-white text-rose-700 icon-bg:bg-rose-100 icon-text:text-rose-600",
    cyan: "border-cyan-200 bg-gradient-to-br from-cyan-50/80 to-white text-cyan-700 icon-bg:bg-cyan-100 icon-text:text-cyan-600",
  };

  const iconStyles = {
    blue: "bg-sky-100 text-sky-600",
    emerald: "bg-emerald-100 text-emerald-600",
    amber: "bg-amber-100 text-amber-600",
    purple: "bg-purple-100 text-purple-600",
    rose: "bg-rose-100 text-rose-600",
    cyan: "bg-cyan-100 text-cyan-600",
  };

  return (
    <div className={`relative overflow-hidden rounded-2xl border p-5 shadow-sm transition-all duration-300 hover:scale-[1.02] hover:shadow-md ${colorMap[color] || colorMap.blue}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-500">{title}</span>
        {Icon && (
          <div className={`rounded-xl p-2.5 shadow-sm ${iconStyles[color] || iconStyles.blue}`}>
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
      <div className="mt-3 flex items-baseline gap-2">
        <span className="text-2xl font-extrabold tracking-tight text-slate-900">{value}</span>
        {unit && <span className="text-xs font-bold text-slate-500">{unit}</span>}
      </div>
      {(subtitle || change !== undefined) && (
        <div className="mt-2.5 flex items-center gap-2 text-xs">
          {change !== undefined && (
            <span className={`inline-flex items-center gap-0.5 font-bold ${isPositive ? "text-emerald-600" : "text-rose-600"}`}>
              {isPositive ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
              {change}
            </span>
          )}
          {subtitle && <span className="text-slate-500 font-medium">{subtitle}</span>}
        </div>
      )}
    </div>
  );
};
