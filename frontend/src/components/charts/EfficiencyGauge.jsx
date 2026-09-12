import React from "react";
import { ShieldCheck, Droplets, Zap, Flame, AlertCircle } from "lucide-react";

export const EfficiencyGauge = ({ score = 86, grade = "A", rating = "High Efficiency", details = {} }) => {
  const getScoreColor = (val) => {
    if (val >= 85) return "text-emerald-500 stroke-emerald-500";
    if (val >= 70) return "text-sky-500 stroke-sky-500";
    if (val >= 55) return "text-amber-500 stroke-amber-500";
    return "text-rose-500 stroke-rose-500";
  };

  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-sky-600" />
            Hostel Resource Efficiency Index
          </h3>
          <p className="text-xs text-slate-500 font-medium">0–100 Weighted Composite Performance</p>
        </div>
        <span className="rounded-full bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 text-xs font-bold text-emerald-700 shadow-xs">
          Grade: {grade}
        </span>
      </div>

      <div className="mt-6 flex flex-col md:flex-row items-center justify-around gap-6">
        <div className="relative flex items-center justify-center">
          <svg className="h-36 w-36 -rotate-90 transform" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="45"
              className="stroke-slate-100"
              strokeWidth="8"
              fill="transparent"
            />
            <circle
              cx="50"
              cy="50"
              r="45"
              className={`transition-all duration-1000 ease-out ${getScoreColor(score)}`}
              strokeWidth="8"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
            />
          </svg>
          <div className="absolute flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-extrabold text-slate-900 tracking-tight">{score}</span>
            <span className="text-[10px] font-bold uppercase text-slate-400">/ 100 Score</span>
          </div>
        </div>

        <div className="w-full md:w-64 space-y-3">
          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
              <span className="flex items-center gap-1.5 text-sky-700 font-bold"><Droplets className="h-3.5 w-3.5 text-sky-500" /> Water Efficiency</span>
              <span className="font-extrabold text-slate-900">{details.water_efficiency || 88}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
              <div className="h-full rounded-full bg-sky-500 shadow-xs" style={{ width: `${details.water_efficiency || 88}%` }} />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
              <span className="flex items-center gap-1.5 text-amber-700 font-bold"><Zap className="h-3.5 w-3.5 text-amber-500" /> Electricity Efficiency</span>
              <span className="font-extrabold text-slate-900">{details.electricity_efficiency || 82}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
              <div className="h-full rounded-full bg-amber-500 shadow-xs" style={{ width: `${details.electricity_efficiency || 82}%` }} />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
              <span className="flex items-center gap-1.5 text-rose-700 font-bold"><Flame className="h-3.5 w-3.5 text-rose-500" /> Gas & Dining Efficiency</span>
              <span className="font-extrabold text-slate-900">{details.gas_efficiency || 89}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
              <div className="h-full rounded-full bg-rose-500 shadow-xs" style={{ width: `${details.gas_efficiency || 89}%` }} />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
              <span className="flex items-center gap-1.5 text-emerald-700 font-bold"><AlertCircle className="h-3.5 w-3.5 text-emerald-500" /> Wastage Control</span>
              <span className="font-extrabold text-slate-900">{details.wastage_control || 85}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
              <div className="h-full rounded-full bg-emerald-500 shadow-xs" style={{ width: `${details.wastage_control || 85}%` }} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
