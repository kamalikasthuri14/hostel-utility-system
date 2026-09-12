import os

target = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend\src\pages\Analytics.jsx"
code = '''import React, { useState, useEffect } from "react";
import { Zap, Droplets, Flame, Users, BarChart3, AlertTriangle, Calendar, Filter } from "lucide-react";
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from "recharts";
import { analyticsAPI, hostelsAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { MetricCard } from "../components/common/MetricCard";

export const Analytics = () => {
  const [activeTab, setActiveTab] = useState("electricity");
  const [days, setDays] = useState(30);
  const [selectedHostel, setSelectedHostel] = useState("");
  const [hostels, setHostels] = useState([]);
  const [waterData, setWaterData] = useState(null);
  const [elecData, setElecData] = useState(null);
  const [gasData, setGasData] = useState(null);
  const [perStudentData, setPerStudentData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    hostelsAPI.list().then((res) => setHostels(res.data)).catch(console.error);
  }, []);

  const loadAnalytics = () => {
    setLoading(true);
    const params = { days, ...(selectedHostel ? { hostel_id: selectedHostel } : {}) };

    Promise.all([
      analyticsAPI.getWater(params),
      analyticsAPI.getElectricity(params),
      analyticsAPI.getGas(params),
      analyticsAPI.getPerStudent({ days })
    ])
      .then(([wRes, eRes, gRes, psRes]) => {
        setWaterData(wRes.data);
        setElecData(eRes.data);
        setGasData(gRes.data);
        setPerStudentData(psRes.data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadAnalytics();
  }, [days, selectedHostel]);

  return (
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Deep-Dive Resource & Utility Analytics"
        subtitle="Cross-hostel comparative benchmarks, diurnal distribution, and per-capita analysis"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Top Controls & Sub-tabs */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setActiveTab("electricity")}
              className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                activeTab === "electricity" ? "bg-amber-500 text-white shadow-lg shadow-amber-500/20" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              <Zap className="h-4 w-4" />
              <span>Electricity Analytics</span>
            </button>
            <button
              onClick={() => setActiveTab("water")}
              className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                activeTab === "water" ? "bg-sky-500 text-white shadow-lg shadow-sky-500/20" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              <Droplets className="h-4 w-4" />
              <span>Water Analytics</span>
            </button>
            <button
              onClick={() => setActiveTab("gas")}
              className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                activeTab === "gas" ? "bg-rose-500 text-white shadow-lg shadow-rose-500/20" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              <Flame className="h-4 w-4" />
              <span>Gas Analytics</span>
            </button>
            <button
              onClick={() => setActiveTab("per_student")}
              className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                activeTab === "per_student" ? "bg-indigo-500 text-white shadow-lg shadow-indigo-500/20" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              <Users className="h-4 w-4" />
              <span>Per-Student Benchmarking</span>
            </button>
          </div>

          <div className="flex items-center gap-3">
            <select
              value={selectedHostel}
              onChange={(e) => setSelectedHostel(e.target.value)}
              className="rounded-xl border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white focus:outline-none"
            >
              <option value="">All Hostels</option>
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.block}</option>
              ))}
            </select>
            <select
              value={days}
              onChange={(e) => setDays(parseInt(e.target.value))}
              className="rounded-xl border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white focus:outline-none"
            >
              <option value={14}>Last 14 Days</option>
              <option value={30}>Last 30 Days</option>
              <option value={60}>Last 60 Days</option>
              <option value={90}>Last 90 Days</option>
            </select>
          </div>
        </div>

        {/* Tab 1: Electricity Analytics */}
        {activeTab === "electricity" && elecData && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <MetricCard
                title="Total Electricity Used"
                value={elecData.summary.total_consumption.toLocaleString()}
                unit="kWh"
                icon={Zap}
                color="amber"
              />
              <MetricCard
                title="Daily Average Load"
                value={elecData.summary.avg_daily.toLocaleString()}
                unit="kWh/day"
                icon={BarChart3}
                color="purple"
              />
              <MetricCard
                title="Total Electricity Cost"
                value={`₹${elecData.summary.total_cost.toLocaleString()}`}
                icon={Zap}
                color="emerald"
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
                <h3 className="text-sm font-bold text-white mb-1">Electricity Daily Consumption Profile</h3>
                <p className="text-xs text-slate-400 mb-4">Time-series kWh demand over selected period</p>
                <div className="h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={elecData.daily_trends} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                      <defs>
                        <linearGradient id="elecArea" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4} />
                          <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                      <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11 }} />
                      <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                      <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "12px", fontSize: "12px" }} />
                      <Area type="monotone" dataKey="electricity_kwh" stroke="#f59e0b" strokeWidth={3} fill="url(#elecArea)" name="Electricity (kWh)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Peak Usage Disaggregation */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl flex flex-col justify-between">
                <div>
                  <h3 className="text-sm font-bold text-white mb-1">Peak-Hour Disaggregation</h3>
                  <p className="text-xs text-slate-400 mb-4">Diurnal electricity breakdown</p>
                  <div className="space-y-4">
                    {elecData.peak_breakdown.map((item, idx) => (
                      <div key={idx}>
                        <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1">
                          <span>{item.time_slot}</span>
                          <span className="font-bold text-amber-400">{item.share_pct}%</span>
                        </div>
                        <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                          <div className="h-full rounded-full bg-amber-500" style={{ width: `${item.share_pct}%` }} />
                        </div>
                        <span className="text-[10px] text-slate-500">{item.category}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <p className="text-[11px] text-slate-400 mt-4 border-t border-slate-800 pt-3">
                  💡 <strong>Insight:</strong> Evening study slots (17:00–23:00) account for 38% of total power draw.
                </p>
              </div>
            </div>

            {/* Hostel-wise comparison bar chart */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
              <h3 className="text-sm font-bold text-white mb-1">Cross-Block Total Electricity Usage</h3>
              <p className="text-xs text-slate-400 mb-4">Comparison across all residential blocks</p>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={elecData.hostel_comparison} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="block" stroke="#64748b" tick={{ fontSize: 11 }} />
                    <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                    <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "12px", fontSize: "12px" }} />
                    <Bar dataKey="total_electricity_kwh" fill="#f59e0b" radius={[6, 6, 0, 0]} name="Total kWh" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Water Analytics */}
        {activeTab === "water" && waterData && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <MetricCard
                title="Total Water Consumed"
                value={waterData.summary.total_consumption.toLocaleString()}
                unit="Litres"
                icon={Droplets}
                color="blue"
              />
              <MetricCard
                title="Daily Average Water"
                value={waterData.summary.avg_daily.toLocaleString()}
                unit="L/day"
                icon={BarChart3}
                color="cyan"
              />
              <MetricCard
                title="Total Water Cost"
                value={`₹${waterData.summary.total_cost.toLocaleString()}`}
                icon={Droplets}
                color="emerald"
              />
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
              <h3 className="text-sm font-bold text-white mb-1">Daily Water Consumption Volume</h3>
              <p className="text-xs text-slate-400 mb-4">Historical water volume in Litres</p>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={waterData.daily_trends} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                    <defs>
                      <linearGradient id="waterArea" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11 }} />
                    <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                    <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "12px", fontSize: "12px" }} />
                    <Area type="monotone" dataKey="water_litres" stroke="#0ea5e9" strokeWidth={3} fill="url(#waterArea)" name="Water (Litres)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
              <h3 className="text-sm font-bold text-white mb-1">Hostel Block-wise Water Volume</h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={waterData.hostel_comparison} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="block" stroke="#64748b" tick={{ fontSize: 11 }} />
                    <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                    <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "12px", fontSize: "12px" }} />
                    <Bar dataKey="total_water_litres" fill="#0ea5e9" radius={[6, 6, 0, 0]} name="Water (Litres)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Gas Analytics */}
        {activeTab === "gas" && gasData && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <MetricCard
                title="Total Commercial LPG Used"
                value={gasData.summary.total_consumption.toLocaleString()}
                unit="kg"
                icon={Flame}
                color="rose"
              />
              <MetricCard
                title="Daily Average Gas"
                value={gasData.summary.avg_daily.toLocaleString()}
                unit="kg/day"
                icon={BarChart3}
                color="amber"
              />
              <MetricCard
                title="Total Gas Cost"
                value={`₹${gasData.summary.total_cost.toLocaleString()}`}
                icon={Flame}
                color="emerald"
              />
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
              <h3 className="text-sm font-bold text-white mb-1">Mess Kitchen Daily Gas Usage</h3>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={gasData.daily_trends} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                    <defs>
                      <linearGradient id="gasArea" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#f43f5e" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11 }} />
                    <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                    <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "12px", fontSize: "12px" }} />
                    <Area type="monotone" dataKey="gas_kg" stroke="#f43f5e" strokeWidth={3} fill="url(#gasArea)" name="Gas (kg)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* Tab 4: Per-Student Benchmarking */}
        {activeTab === "per_student" && perStudentData && (
          <div className="space-y-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
              <h3 className="text-sm font-bold text-white mb-1">Cross-Hostel Per-Resident Consumption Benchmarks</h3>
              <p className="text-xs text-slate-400 mb-4">Identifies outlier blocks consuming significantly above per-capita baseline</p>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-300">
                  <thead className="bg-slate-800/60 text-slate-400 uppercase font-semibold">
                    <tr>
                      <th className="px-4 py-3 rounded-l-xl">Hostel Block</th>
                      <th className="px-4 py-3">Avg Students</th>
                      <th className="px-4 py-3">Water / Student (Baseline: 95L)</th>
                      <th className="px-4 py-3">Electricity / Student (Baseline: 4.2kWh)</th>
                      <th className="px-4 py-3">Gas / Student (Baseline: 0.13kg)</th>
                      <th className="px-4 py-3 rounded-r-xl">Daily Cost / Student</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {perStudentData.hostels.map((h) => (
                      <tr key={h.hostel_id} className="hover:bg-slate-800/40 transition-colors">
                        <td className="px-4 py-3 font-bold text-white">
                          {h.hostel_name} <span className="text-sky-400">({h.block})</span>
                        </td>
                        <td className="px-4 py-3 font-semibold text-slate-300">{h.avg_students}</td>
                        <td className="px-4 py-3">
                          <span className={`font-semibold ${h.water_alert ? "text-rose-400 font-bold flex items-center gap-1" : "text-slate-200"}`}>
                            {h.water_alert && <AlertTriangle className="h-3 w-3 text-rose-400" />}
                            {h.water_l_per_student} L
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <span className={`font-semibold ${h.electricity_alert ? "text-amber-400 font-bold flex items-center gap-1" : "text-slate-200"}`}>
                            {h.electricity_alert && <AlertTriangle className="h-3 w-3 text-amber-400" />}
                            {h.electricity_kwh_per_student} kWh
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <span className={`font-semibold ${h.gas_alert ? "text-rose-400 font-bold flex items-center gap-1" : "text-slate-200"}`}>
                            {h.gas_alert && <AlertTriangle className="h-3 w-3 text-rose-400" />}
                            {h.gas_kg_per_student} kg
                          </span>
                        </td>
                        <td className="px-4 py-3 font-bold text-emerald-400">
                          ₹{h.cost_per_student_daily} / day
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
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
print("Analytics.jsx generated.")
