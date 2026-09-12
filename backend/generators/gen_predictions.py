import os

target = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend\src\pages\Predictions.jsx"
code = '''import React, { useState, useEffect } from "react";
import { TrendingUp, RefreshCw, Cpu, Brain, CheckCircle, HelpCircle, Zap, Droplets, Flame, IndianRupee } from "lucide-react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from "recharts";
import { predictionsAPI, hostelsAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { MetricCard } from "../components/common/MetricCard";

export const Predictions = () => {
  const [resourceType, setResourceType] = useState("Electricity");
  const [selectedHostel, setSelectedHostel] = useState("");
  const [hostels, setHostels] = useState([]);
  const [predData, setPredData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);
  const [retrainMsg, setRetrainMsg] = useState("");

  useEffect(() => {
    hostelsAPI.list().then((res) => setHostels(res.data)).catch(console.error);
  }, []);

  const loadPredictions = () => {
    setLoading(true);
    const params = { resource_type: resourceType, ...(selectedHostel ? { hostel_id: selectedHostel } : {}) };
    predictionsAPI.get(params)
      .then((res) => setPredData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadPredictions();
  }, [resourceType, selectedHostel]);

  const handleRetrain = async () => {
    setRetraining(true);
    setRetrainMsg("");
    try {
      const res = await predictionsAPI.retrain();
      setRetrainMsg("Random Forest Regressors successfully retrained and updated.");
      loadPredictions();
    } catch (err) {
      setRetrainMsg("Retraining failed.");
    } finally {
      setRetraining(false);
    }
  };

  return (
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Predictive Machine Learning & Demand Forecasting"
        subtitle="Multi-step Random Forest Regressors with Linear Regression Baseline & Explainability"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Top Control Bar */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex flex-wrap items-center gap-2">
            {["Electricity", "Water", "Gas", "Cost"].map((type) => (
              <button
                key={type}
                onClick={() => setResourceType(type)}
                className={`flex items-center gap-1.5 rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                  resourceType === type ? "bg-sky-500 text-white shadow-lg shadow-sky-500/20" : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                {type === "Electricity" && <Zap className="h-3.5 w-3.5" />}
                {type === "Water" && <Droplets className="h-3.5 w-3.5" />}
                {type === "Gas" && <Flame className="h-3.5 w-3.5" />}
                {type === "Cost" && <IndianRupee className="h-3.5 w-3.5" />}
                <span>{type} Forecast</span>
              </button>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <select
              value={selectedHostel}
              onChange={(e) => setSelectedHostel(e.target.value)}
              className="rounded-xl border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white focus:outline-none"
            >
              <option value="">All Hostels (Aggregate)</option>
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.name} ({h.block})</option>
              ))}
            </select>

            <button
              onClick={handleRetrain}
              disabled={retraining}
              className="flex items-center gap-1.5 rounded-xl border border-sky-500/30 bg-sky-500/10 px-3.5 py-1.5 text-xs font-bold text-sky-400 hover:bg-sky-500/20 cursor-pointer"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${retraining ? "animate-spin" : ""}`} />
              {retraining ? "Retraining Models..." : "Retrain ML Models"}
            </button>
          </div>
        </div>

        {retrainMsg && (
          <div className="rounded-xl bg-emerald-500/10 border border-emerald-500/30 p-3 text-xs text-emerald-400">
            {retrainMsg}
          </div>
        )}

        {predData && (
          <div className="space-y-6">
            {/* KPI Summary Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <MetricCard
                title="7-Day Predicted Demand"
                value={predData.total_predicted_consumption.toLocaleString()}
                unit={predData.unit}
                icon={TrendingUp}
                color="sky"
              />
              <MetricCard
                title="Predicted 7-Day Cost"
                value={`₹${predData.total_predicted_cost.toLocaleString()}`}
                subtitle={`Current rate: ₹${predData.current_rate} / ${predData.unit}`}
                icon={IndianRupee}
                color="emerald"
              />
              <MetricCard
                title="Target Subject"
                value={predData.hostel_name.split("(")[0]}
                subtitle={predData.hostel_name}
                icon={Brain}
                color="purple"
              />
            </div>

            {/* Forecast Chart */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4 mb-4">
                <div>
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-sky-400" />
                    7-Day Forward Prediction Horizon ({predData.unit})
                  </h3>
                  <p className="text-xs text-slate-400">Autoregressive Random Forest projection with seasonal calendar weights</p>
                </div>
              </div>

              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={predData.forecast} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11 }} />
                    <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                    <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "12px", fontSize: "12px" }} />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="predicted_value"
                      stroke="#0ea5e9"
                      strokeWidth={3}
                      dot={{ r: 5, fill: "#0ea5e9" }}
                      activeDot={{ r: 7 }}
                      name={`Predicted ${predData.resource_type} (${predData.unit})`}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Day-by-day table */}
              <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
                {predData.forecast.map((day) => (
                  <div key={day.day_number} className="rounded-xl border border-slate-800 bg-slate-800/40 p-3 text-center">
                    <p className="text-[11px] font-semibold text-slate-400">{day.day_name}</p>
                    <p className="text-xs text-slate-500">{day.date}</p>
                    <p className="mt-2 text-sm font-bold text-sky-400">{day.predicted_value.toLocaleString()}</p>
                    <p className="text-[10px] text-slate-400">{day.unit}</p>
                    <p className="mt-1 text-[11px] font-semibold text-emerald-400">₹{day.predicted_cost.toLocaleString()}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Model Evaluation & Explainability */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Model Comparison Table */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
                <h3 className="text-sm font-bold text-white mb-1 flex items-center gap-2">
                  <Cpu className="h-4 w-4 text-purple-400" />
                  Model Performance Evaluation Metrics
                </h3>
                <p className="text-xs text-slate-400 mb-4">Random Forest vs Linear Regression baseline</p>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-300">
                    <thead className="bg-slate-800/60 text-slate-400 uppercase font-semibold">
                      <tr>
                        <th className="px-4 py-2.5 rounded-l-xl">Algorithm</th>
                        <th className="px-4 py-2.5">R² Score</th>
                        <th className="px-4 py-2.5">MAE</th>
                        <th className="px-4 py-2.5 rounded-r-xl">RMSE</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                      {predData.model_evaluations.map((m, idx) => (
                        <tr key={idx} className={idx === 0 ? "bg-sky-500/5 font-semibold" : ""}>
                          <td className="px-4 py-3 text-white flex items-center gap-1.5">
                            {idx === 0 && <CheckCircle className="h-3.5 w-3.5 text-emerald-400" />}
                            {m.model_name}
                          </td>
                          <td className="px-4 py-3 text-emerald-400 font-bold">{m.r2_score}</td>
                          <td className="px-4 py-3">{m.mae}</td>
                          <td className="px-4 py-3">{m.rmse}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Explainability Breakdown */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
                <h3 className="text-sm font-bold text-white mb-1 flex items-center gap-2">
                  <Brain className="h-4 w-4 text-sky-400" />
                  Machine Learning Explainability Factors
                </h3>
                <p className="text-xs text-slate-400 mb-4">Key feature contributions driving this forecast</p>

                <ul className="space-y-2.5 text-xs text-slate-300">
                  {predData.explainability.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2 rounded-xl bg-slate-800/50 p-2.5">
                      <span className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-sky-500/20 text-[10px] font-bold text-sky-400">
                        {idx + 1}
                      </span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
'''

with open(target, "w", encoding="utf-8") as f:
    f.write(code.strip() + "\n")
print("Predictions.jsx generated.")
