import React, { useState, useEffect } from "react";
import { Lightbulb, IndianRupee, Droplets, Zap, Flame, Users, CheckCircle2, ArrowRight } from "lucide-react";
import { recommendationsAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { StatusBadge } from "../components/common/StatusBadge";

export const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    recommendationsAPI.list()
      .then((res) => setRecommendations(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const totalPotentialSavings = recommendations.reduce(
    (acc, curr) => acc + (curr.estimated_monthly_savings || 0), 0
  );

  return (
    <div className="flex-1 min-h-screen bg-slate-50/60 pb-16">
      <Header
        title="Smart Actionable Recommendations Engine"
        subtitle="Explainable rule & ML-driven interventions to eliminate utility wastage"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Banner with Total Savings */}
        <div className="rounded-2xl border border-emerald-200 bg-gradient-to-r from-emerald-50 via-white to-sky-50 p-6 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <span className="rounded-full bg-emerald-100 border border-emerald-300 px-3 py-1 text-xs font-bold text-emerald-800">
              Optimization Potential
            </span>
            <h2 className="mt-2 text-lg font-bold text-slate-900">
              Estimated Monthly Savings: <span className="text-emerald-600 font-extrabold">₹{totalPotentialSavings.toLocaleString()}</span>
            </h2>
            <p className="text-xs text-slate-500 font-medium">
              Based on historical baseline reduction across {recommendations.length} identified efficiency targets
            </p>
          </div>
          <button
            onClick={() => alert("Recommendations printed for institutional facilities committee review.")}
            className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 px-4 py-2.5 text-xs font-bold text-white shadow-md shadow-emerald-600/20 hover:from-emerald-700 hover:to-teal-700 transition-all cursor-pointer"
          >
            <Lightbulb className="h-4 w-4" />
            <span>Export Action Plan</span>
          </button>
        </div>

        {/* Recommendation Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {recommendations.map((rec) => (
            <div
              key={rec.id}
              className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow"
            >
              <div>
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <div className="flex items-center gap-2">
                    {rec.category === "Water" && <Droplets className="h-4 w-4 text-sky-500" />}
                    {rec.category === "Electricity" && <Zap className="h-4 w-4 text-amber-500" />}
                    {rec.category === "Gas" && <Flame className="h-4 w-4 text-rose-500" />}
                    {rec.category === "Occupancy" && <Users className="h-4 w-4 text-purple-500" />}
                    <span className="text-xs font-bold text-slate-900">{rec.hostel_name}</span>
                  </div>
                  <span className="rounded-full bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 text-xs font-bold text-emerald-700">
                    Save ~₹{rec.estimated_monthly_savings.toLocaleString()} / mo
                  </span>
                </div>

                <h3 className="mt-4 text-sm font-bold text-slate-900 leading-snug">{rec.title}</h3>
                <p className="mt-1 text-xs text-slate-600 leading-relaxed">{rec.description}</p>

                <div className="mt-4 rounded-xl bg-slate-50 border border-slate-100 p-3.5">
                  <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2">
                    Recommended Action Checklist:
                  </p>
                  <ul className="space-y-1.5 text-xs text-slate-700">
                    {rec.suggested_actions.map((act, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <CheckCircle2 className="h-3.5 w-3.5 text-sky-600 flex-shrink-0 mt-0.5" />
                        <span>{act}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="mt-5 border-t border-slate-100 pt-3">
                <p className="text-[11px] text-slate-500">
                  🔬 <strong>Rationale:</strong> {rec.reasoning}
                </p>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};
