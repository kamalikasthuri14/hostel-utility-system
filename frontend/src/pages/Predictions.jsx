import React, { useState, useEffect } from "react";
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
    <div className="flex-1 min-h-screen bg-slate-50/60 pb-16">
      <Header
        title="Predictive Machine Learning & Demand Forecasting"
        subtitle="Multi-step Random Forest Regressors with Linear Regression Baseline & Explainability"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Top Control Bar */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-4 shadow-sm">
          <div className="flex flex-wrap items-center gap-2">
            {["Electricity", "Water", "Gas", "Cost"].map((type) => (
              <button
                key={type}
                onClick={() => setResourceType(type)}
                className={`flex items-center gap-1.5 rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                  resourceType === type ? "bg-gradient-to-r from-sky-500 to-indigo-600 text-white shadow-md shadow-sky-500/20" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                }`}
              >
                {type === "Electricity" && <Zap className="h-3.5 w-3.5 text-amber-300" />}
                {type === "Water" && <Droplets className="h-3.5 w-3.5 text-sky-200" />}
                {type === "Gas" && <Flame className="h-3.5 w-3.5 text-rose-300" />}
                {type === "Cost" && <IndianRupee className="h-3.5 w-3.5 text-emerald-300" />}
                <span>{type} Forecast</span>
              </button>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <select
              value={selectedHostel}
              onChange={(e) => setSelectedHostel(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-sky-500 focus:bg-white transition-all"
            >
              <option value="">All Hostels (Aggregate)</option>
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.name} ({h.block})</option>
              ))}
            </select>

            <button
              onClick={handleRetrain}
              disabled={retraining}
              className="flex items-center gap-1.5 rounded-xl border border-sky-200 bg-sky-50 px-3.5 py-1.5 text-xs font-bold text-sky-700 hover:bg-sky-100 transition-all shadow-xs cursor-pointer"
            >
              <RefreshCw className={`h-3.5 w-3.5 text-sky-600 ${retraining ? "animate-spin" : ""}`} />
              {retraining ? "Retraining Models..." : "Retrain ML Models"}
            </button>
          </div>
        </div>

        {retrainMsg && (
          <div className="rounded-xl bg-emerald-50 border border-emerald-200 p-3 text-xs text-emerald-800 font-bold">
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
                color="blue"
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
            <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4 mb-4">
                <div>
                  <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-sky-600" />
                    7-Day Forward Prediction Horizon ({predData.unit})
                  </h3>
                  <p className="text-xs text-slate-500">Autoregressive Random Forest projection with seasonal calendar weights</p>
                </div>
              </div>

              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={predData.forecast} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="date" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                    <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
                    <Tooltip contentStyle={{ backgroundColor: "#ffffff", borderColor: "#e2e8f0", borderRadius: "12px", fontSize: "12px", boxShadow: "0 10px 15px -3px rgba(0,0,0,0.1)", color: "#0f172a" }} />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="predicted_value"
                      stroke="#0284c7"
                      strokeWidth={3}
                      dot={{ r: 5, fill: "#0284c7" }}
                      activeDot={{ r: 7 }}
                      name={`Predicted ${predData.resource_type} (${predData.unit})`}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Day-by-day table */}
              <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
                {predData.forecast.map((day) => (
                  <div key={day.day_number} className="rounded-xl border border-slate-200 bg-slate-50/80 p-3 text-center">
                    <p className="text-[11px] font-bold text-slate-600">{day.day_name}</p>
                    <p className="text-xs text-slate-400 font-medium">{day.date}</p>
                    <p className="mt-2 text-sm font-extrabold text-sky-700">{day.predicted_value.toLocaleString()}</p>
                    <p className="text-[10px] text-slate-500 font-medium">{day.unit}</p>
                    <p className="mt-1 text-[11px] font-bold text-emerald-700">₹{day.predicted_cost.toLocaleString()}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Model Evaluation & Explainability */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Model Comparison Table */}
              <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm">
                <h3 className="text-sm font-bold text-slate-900 mb-1 flex items-center gap-2">
                  <Cpu className="h-4 w-4 text-purple-600" />
                  Model Performance Evaluation Metrics
                </h3>
                <p className="text-xs text-slate-500 mb-4">Random Forest vs Linear Regression baseline</p>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-700">
                    <thead className="bg-slate-50 text-slate-600 uppercase font-bold border-b border-slate-100">
                      <tr>
                        <th className="px-4 py-2.5 rounded-l-xl">Algorithm</th>
                        <th className="px-4 py-2.5">R² Score</th>
                        <th className="px-4 py-2.5">MAE</th>
                        <th className="px-4 py-2.5 rounded-r-xl">RMSE</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {predData.model_evaluations.map((m, idx) => (
                        <tr key={idx} className={idx === 0 ? "bg-sky-50/60 font-semibold" : ""}>
                          <td className="px-4 py-3 text-slate-900 flex items-center gap-1.5 font-bold">
                            {idx === 0 && <CheckCircle className="h-3.5 w-3.5 text-emerald-600" />}
                            {m.model_name}
                          </td>
                          <td className="px-4 py-3 text-emerald-600 font-extrabold">{m.r2_score}</td>
                          <td className="px-4 py-3 text-slate-700">{m.mae}</td>
                          <td className="px-4 py-3 text-slate-700">{m.rmse}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Explainability Breakdown */}
              <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm">
                <h3 className="text-sm font-bold text-slate-900 mb-1 flex items-center gap-2">
                  <Brain className="h-4 w-4 text-sky-600" />
                  Machine Learning Explainability Factors
                </h3>
                <p className="text-xs text-slate-500 mb-4">Key feature contributions driving this forecast</p>

                <ul className="space-y-2.5 text-xs text-slate-700">
                  {predData.explainability.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2 rounded-xl bg-slate-50 border border-slate-100 p-2.5">
                      <span className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-sky-100 text-[10px] font-bold text-sky-700">
                        {idx + 1}
                      </span>
                      <span className="font-medium">{item}</span>
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
