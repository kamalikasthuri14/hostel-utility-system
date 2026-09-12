import React, { useState, useEffect } from "react";
import {
  Users,
  Building2,
  Droplets,
  Zap,
  Flame,
  IndianRupee,
  AlertTriangle,
  ShieldCheck,
  TrendingUp,
  RefreshCw,
  Plus,
  UploadCloud,
  FileSpreadsheet
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar
} from "recharts";
import { Link } from "react-router-dom";
import { dashboardAPI, anomaliesAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { MetricCard } from "../components/common/MetricCard";
import { StatusBadge } from "../components/common/StatusBadge";
import { EfficiencyGauge } from "../components/charts/EfficiencyGauge";
import { useAuth } from "../contexts/AuthContext";

export const Dashboard = () => {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("electricity");
  const [scanMessage, setScanMessage] = useState("");
  const [scanning, setScanning] = useState(false);

  const fetchDashboard = () => {
    setLoading(true);
    dashboardAPI.getSummary()
      .then((res) => setData(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleRunScan = async () => {
    setScanning(true);
    setScanMessage("");
    try {
      const res = await anomaliesAPI.detect();
      setScanMessage(res.data.message);
      fetchDashboard();
    } catch (err) {
      setScanMessage("Scan failed.");
    } finally {
      setScanning(false);
    }
  };

  if (loading || !data) {
    return (
      <div className="flex-1 min-h-screen bg-slate-50 p-8 flex items-center justify-center">
        <div className="flex items-center gap-3 text-sky-600 font-bold">
          <RefreshCw className="h-5 w-5 animate-spin" />
          <span>Loading Institutional Utility Grid Telemetry...</span>
        </div>
      </div>
    );
  }

  const { summary, efficiency_details, seven_day_trends, recent_alerts } = data;

  return (
    <div className="flex-1 min-h-screen bg-slate-50/60 pb-16">
      <Header
        title="Hostel Utility & Resource Operations Dashboard"
        subtitle={`Live monitoring for ${summary.total_hostel_blocks} Blocks • ${summary.total_students.toLocaleString()} Residents`}
        activeAlertsCount={summary.active_alerts}
      />

      <main className="p-8 space-y-8 max-w-7xl mx-auto">
        {/* Quick Scan & Action Bar */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-4 shadow-sm">
          <div className="flex items-center gap-3">
            <span className="flex h-3 w-3 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <div>
              <p className="text-xs font-bold text-slate-900">Institutional Energy & Water Grid Status: Optimal</p>
              <p className="text-[11px] text-slate-500">Telemetry synced up to {summary.latest_date}</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <button
              onClick={handleRunScan}
              disabled={scanning}
              className="flex items-center gap-2 rounded-xl border border-amber-300 bg-amber-50 px-3.5 py-2 text-xs font-bold text-amber-800 hover:bg-amber-100 transition-all shadow-xs cursor-pointer"
            >
              <RefreshCw className={`h-3.5 w-3.5 text-amber-600 ${scanning ? "animate-spin" : ""}`} />
              {scanning ? "Scanning ML Pipeline..." : "Run Anomaly Scan (Isolation Forest)"}
            </button>
            <Link
              to="/utilities"
              className="flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-3.5 py-2 text-xs font-bold text-white shadow-md shadow-sky-500/20 hover:from-sky-600 hover:to-indigo-700 transition-all"
            >
              <Plus className="h-3.5 w-3.5" />
              <span>Log Record</span>
            </Link>
          </div>
        </div>

        {scanMessage && (
          <div className="rounded-xl bg-sky-50 border border-sky-200 p-3 text-xs text-sky-800 font-medium">
            {scanMessage}
          </div>
        )}

        {/* 8 Summary Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Total Students"
            value={summary.total_students.toLocaleString()}
            subtitle={`${summary.overall_occupancy_rate}% Hostel Capacity`}
            icon={Users}
            color="cyan"
          />
          <MetricCard
            title="Today's Electricity"
            value={summary.electricity_today_kwh.toLocaleString()}
            unit="kWh"
            subtitle={`~${(summary.electricity_today_kwh / summary.total_students).toFixed(2)} kWh / resident`}
            icon={Zap}
            color="amber"
          />
          <MetricCard
            title="Today's Water"
            value={summary.water_today_litres.toLocaleString()}
            unit="Litres"
            subtitle={`~${(summary.water_today_litres / summary.total_students).toFixed(1)} L / resident`}
            icon={Droplets}
            color="blue"
          />
          <MetricCard
            title="Today's Gas"
            value={summary.gas_today_kg.toLocaleString()}
            unit="kg"
            subtitle={`~${(summary.gas_today_kg / summary.total_students).toFixed(3)} kg / resident`}
            icon={Flame}
            color="rose"
          />
          <MetricCard
            title="Estimated Cost Today"
            value={`₹${summary.estimated_cost_today.toLocaleString()}`}
            subtitle="Calculated at tariff baseline"
            icon={IndianRupee}
            color="emerald"
          />
          <MetricCard
            title="Active Alerts"
            value={summary.active_alerts}
            subtitle={summary.active_alerts > 0 ? "Requires Maintenance Review" : "No Unresolved Issues"}
            icon={AlertTriangle}
            color={summary.active_alerts > 0 ? "rose" : "emerald"}
          />
          <MetricCard
            title="Hostel Blocks"
            value={summary.total_hostel_blocks}
            subtitle={`${summary.total_capacity} Total Beds`}
            icon={Building2}
            color="purple"
          />
          <MetricCard
            title="Overall Efficiency"
            value={`${summary.efficiency_score}%`}
            subtitle={`Rating: ${summary.efficiency_rating}`}
            icon={ShieldCheck}
            color="emerald"
          />
        </div>

        {/* Efficiency Index + 7-Day Trend Chart */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <EfficiencyGauge
              score={summary.efficiency_score}
              grade={summary.efficiency_grade}
              rating={summary.efficiency_rating}
              details={efficiency_details}
            />
          </div>

          <div className="lg:col-span-2 rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm flex flex-col justify-between">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
              <div>
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-sky-600" />
                  Past 7-Day Consumption Trends
                </h3>
                <p className="text-xs text-slate-500">Institutional aggregate daily readings</p>
              </div>

              {/* Resource Tabs */}
              <div className="flex items-center gap-1 rounded-xl bg-slate-100 p-1 border border-slate-200/60">
                <button
                  onClick={() => setActiveTab("electricity")}
                  className={`rounded-lg px-3 py-1 text-xs font-bold transition-all cursor-pointer ${
                    activeTab === "electricity" ? "bg-amber-500 text-white shadow-sm" : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  Electricity
                </button>
                <button
                  onClick={() => setActiveTab("water")}
                  className={`rounded-lg px-3 py-1 text-xs font-bold transition-all cursor-pointer ${
                    activeTab === "water" ? "bg-sky-500 text-white shadow-sm" : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  Water
                </button>
                <button
                  onClick={() => setActiveTab("gas")}
                  className={`rounded-lg px-3 py-1 text-xs font-bold transition-all cursor-pointer ${
                    activeTab === "gas" ? "bg-rose-500 text-white shadow-sm" : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  Gas
                </button>
                <button
                  onClick={() => setActiveTab("cost")}
                  className={`rounded-lg px-3 py-1 text-xs font-bold transition-all cursor-pointer ${
                    activeTab === "cost" ? "bg-emerald-500 text-white shadow-sm" : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  Cost (₹)
                </button>
              </div>
            </div>

            {/* Recharts Area Chart */}
            <div className="h-64 w-full mt-4">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={seven_day_trends} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                  <defs>
                    <linearGradient id="elecGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.02} />
                    </linearGradient>
                    <linearGradient id="waterGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0284c7" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#0284c7" stopOpacity={0.02} />
                    </linearGradient>
                    <linearGradient id="gasGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#e11d48" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#e11d48" stopOpacity={0.02} />
                    </linearGradient>
                    <linearGradient id="costGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#059669" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#059669" stopOpacity={0.02} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="date" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                  <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#ffffff", borderColor: "#e2e8f0", borderRadius: "12px", fontSize: "12px", boxShadow: "0 10px 15px -3px rgba(0,0,0,0.1)", color: "#0f172a" }}
                    labelStyle={{ color: "#64748b", fontWeight: "bold" }}
                  />
                  {activeTab === "electricity" && (
                    <Area type="monotone" dataKey="electricity_kwh" stroke="#f59e0b" strokeWidth={3} fill="url(#elecGrad)" name="Electricity (kWh)" />
                  )}
                  {activeTab === "water" && (
                    <Area type="monotone" dataKey="water_litres" stroke="#0284c7" strokeWidth={3} fill="url(#waterGrad)" name="Water (Litres)" />
                  )}
                  {activeTab === "gas" && (
                    <Area type="monotone" dataKey="gas_kg" stroke="#e11d48" strokeWidth={3} fill="url(#gasGrad)" name="Gas (kg)" />
                  )}
                  {activeTab === "cost" && (
                    <Area type="monotone" dataKey="total_cost" stroke="#059669" strokeWidth={3} fill="url(#costGrad)" name="Cost (₹)" />
                  )}
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Active Alerts Preview Table */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-rose-500" />
                Active Anomaly Alerts & Action Center
              </h3>
              <p className="text-xs text-slate-500">Real-time flags detected by Isolation Forest algorithm</p>
            </div>
            <Link
              to="/alerts"
              className="text-xs font-bold text-sky-600 hover:text-sky-700 transition-colors"
            >
              View All Alerts &rarr;
            </Link>
          </div>

          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50 text-slate-600 uppercase font-bold border-b border-slate-100">
                <tr>
                  <th className="px-4 py-3 rounded-l-xl">Severity</th>
                  <th className="px-4 py-3">Hostel Block</th>
                  <th className="px-4 py-3">Resource</th>
                  <th className="px-4 py-3">Deviation %</th>
                  <th className="px-4 py-3">Description</th>
                  <th className="px-4 py-3 rounded-r-xl">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {recent_alerts.map((alert) => (
                  <tr key={alert.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="px-4 py-3">
                      <StatusBadge status={alert.severity} />
                    </td>
                    <td className="px-4 py-3 font-bold text-slate-900">
                      {alert.hostel_name} ({alert.hostel_block})
                    </td>
                    <td className="px-4 py-3 font-semibold">{alert.resource_type}</td>
                    <td className="px-4 py-3 font-extrabold text-rose-600">
                      +{alert.difference_percentage}%
                    </td>
                    <td className="px-4 py-3 text-slate-600 max-w-md truncate">
                      {alert.description}
                    </td>
                    <td className="px-4 py-3">
                      <Link
                        to="/alerts"
                        className="rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1 text-[11px] font-bold text-sky-600 hover:bg-sky-50 hover:text-sky-700 hover:border-sky-300 transition-colors shadow-xs"
                      >
                        Investigate
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
};
