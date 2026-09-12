import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend", "src")

files = {}

# 1. Login Page
files["pages/Login.jsx"] = '''import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Zap, Shield, UserCheck, Wrench, Lock, Mail, ArrowRight, CheckCircle2 } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = async (demoEmail, demoPassword) => {
    setEmail(demoEmail);
    setPassword(demoPassword);
    setError("");
    setLoading(true);
    try {
      await login(demoEmail, demoPassword);
      navigate("/");
    } catch (err) {
      setError("Demo login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Ambient background glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="sm:mx-auto sm:w-full sm:max-w-md z-10">
        <div className="flex justify-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 shadow-xl shadow-sky-500/25">
            <Zap className="h-7 w-7 text-white" />
          </div>
        </div>
        <h2 className="mt-4 text-center text-2xl font-extrabold tracking-tight text-white">
          HostelOptima <span className="text-sky-400">AI</span>
        </h2>
        <p className="mt-1 text-center text-xs text-slate-400">
          Automated Hostel Utility Optimization & Predictive Resource Management
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md z-10">
        <div className="bg-slate-900/90 py-8 px-6 shadow-2xl rounded-3xl sm:px-10 border border-slate-800 backdrop-blur-xl">
          {error && (
            <div className="mb-4 rounded-xl bg-rose-500/10 border border-rose-500/20 p-3 text-xs text-rose-400">
              {error}
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Institutional Email</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <Mail className="h-4 w-4" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="admin@hostel.edu"
                  className="block w-full rounded-xl border border-slate-700 bg-slate-800/80 pl-10 pr-3 py-2.5 text-sm text-white placeholder-slate-500 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <Lock className="h-4 w-4" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="block w-full rounded-xl border border-slate-700 bg-slate-800/80 pl-10 pr-3 py-2.5 text-sm text-white placeholder-slate-500 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 py-2.5 px-4 text-sm font-bold text-white shadow-lg shadow-sky-500/25 hover:from-sky-400 hover:to-indigo-500 focus:outline-none disabled:opacity-50 transition-all cursor-pointer"
            >
              {loading ? "Authenticating..." : "Sign In to Dashboard"}
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>

          {/* 1-Click Demo Accounts */}
          <div className="mt-6 border-t border-slate-800 pt-5">
            <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-3 text-center">
              Quick 1-Click Demo Credentials
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => handleDemoLogin("admin@hostel.edu", "Admin@123")}
                className="flex flex-col items-center justify-center p-2.5 rounded-xl border border-sky-500/30 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 text-xs font-semibold transition-all cursor-pointer"
              >
                <Shield className="h-4 w-4 mb-1" />
                <span>Admin</span>
              </button>
              <button
                type="button"
                onClick={() => handleDemoLogin("warden.blocka@hostel.edu", "Warden@123")}
                className="flex flex-col items-center justify-center p-2.5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 text-xs font-semibold transition-all cursor-pointer"
              >
                <UserCheck className="h-4 w-4 mb-1" />
                <span>Warden A</span>
              </button>
              <button
                type="button"
                onClick={() => handleDemoLogin("maintenance@hostel.edu", "Maint@123")}
                className="flex flex-col items-center justify-center p-2.5 rounded-xl border border-amber-500/30 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 text-xs font-semibold transition-all cursor-pointer"
              >
                <Wrench className="h-4 w-4 mb-1" />
                <span>Staff</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
'''

# 2. Dashboard Page
files["pages/Dashboard.jsx"] = '''import React, { useState, useEffect } from "react";
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
      <div className="flex-1 min-h-screen bg-slate-950 p-8 flex items-center justify-center">
        <div className="flex items-center gap-3 text-sky-400 font-semibold">
          <RefreshCw className="h-5 w-5 animate-spin" />
          <span>Loading Institutional Utility Grid Telemetry...</span>
        </div>
      </div>
    );
  }

  const { summary, efficiency_details, seven_day_trends, recent_alerts } = data;

  return (
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Hostel Utility & Resource Operations Dashboard"
        subtitle={`Live monitoring for ${summary.total_hostel_blocks} Blocks • ${summary.total_students.toLocaleString()} Residents`}
        activeAlertsCount={summary.active_alerts}
      />

      <main className="p-8 space-y-8 max-w-7xl mx-auto">
        {/* Quick Scan & Action Bar */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-4 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <span className="flex h-3 w-3 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <div>
              <p className="text-xs font-bold text-white">Institutional Energy & Water Grid Status: Optimal</p>
              <p className="text-[11px] text-slate-400">Telemetry synced up to {summary.latest_date}</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <button
              onClick={handleRunScan}
              disabled={scanning}
              className="flex items-center gap-2 rounded-xl border border-amber-500/30 bg-amber-500/10 px-3.5 py-2 text-xs font-bold text-amber-400 hover:bg-amber-500/20 transition-all cursor-pointer"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${scanning ? "animate-spin" : ""}`} />
              {scanning ? "Scanning ML Pipeline..." : "Run Anomaly Scan (Isolation Forest)"}
            </button>
            <Link
              to="/utilities"
              className="flex items-center gap-1.5 rounded-xl bg-sky-500 px-3.5 py-2 text-xs font-bold text-white shadow-lg shadow-sky-500/20 hover:bg-sky-400 transition-all"
            >
              <Plus className="h-3.5 w-3.5" />
              <span>Log Record</span>
            </Link>
          </div>
        </div>

        {scanMessage && (
          <div className="rounded-xl bg-sky-500/10 border border-sky-500/30 p-3 text-xs text-sky-400">
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

          <div className="lg:col-span-2 rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl backdrop-blur-md flex flex-col justify-between">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-sky-400" />
                  Past 7-Day Consumption Trends
                </h3>
                <p className="text-xs text-slate-400">Institutional aggregate daily readings</p>
              </div>

              {/* Resource Tabs */}
              <div className="flex items-center gap-1 rounded-xl bg-slate-800/80 p-1">
                <button
                  onClick={() => setActiveTab("electricity")}
                  className={`rounded-lg px-3 py-1 text-xs font-semibold transition-all cursor-pointer ${
                    activeTab === "electricity" ? "bg-amber-500 text-white shadow" : "text-slate-400 hover:text-white"
                  }`}
                >
                  Electricity
                </button>
                <button
                  onClick={() => setActiveTab("water")}
                  className={`rounded-lg px-3 py-1 text-xs font-semibold transition-all cursor-pointer ${
                    activeTab === "water" ? "bg-sky-500 text-white shadow" : "text-slate-400 hover:text-white"
                  }`}
                >
                  Water
                </button>
                <button
                  onClick={() => setActiveTab("gas")}
                  className={`rounded-lg px-3 py-1 text-xs font-semibold transition-all cursor-pointer ${
                    activeTab === "gas" ? "bg-rose-500 text-white shadow" : "text-slate-400 hover:text-white"
                  }`}
                >
                  Gas
                </button>
                <button
                  onClick={() => setActiveTab("cost")}
                  className={`rounded-lg px-3 py-1 text-xs font-semibold transition-all cursor-pointer ${
                    activeTab === "cost" ? "bg-emerald-500 text-white shadow" : "text-slate-400 hover:text-white"
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
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="waterGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="gasGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#f43f5e" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="costGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11 }} />
                  <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "12px", fontSize: "12px" }}
                    labelStyle={{ color: "#94a3b8" }}
                  />
                  {activeTab === "electricity" && (
                    <Area type="monotone" dataKey="electricity_kwh" stroke="#f59e0b" strokeWidth={3} fill="url(#elecGrad)" name="Electricity (kWh)" />
                  )}
                  {activeTab === "water" && (
                    <Area type="monotone" dataKey="water_litres" stroke="#0ea5e9" strokeWidth={3} fill="url(#waterGrad)" name="Water (Litres)" />
                  )}
                  {activeTab === "gas" && (
                    <Area type="monotone" dataKey="gas_kg" stroke="#f43f5e" strokeWidth={3} fill="url(#gasGrad)" name="Gas (kg)" />
                  )}
                  {activeTab === "cost" && (
                    <Area type="monotone" dataKey="total_cost" stroke="#10b981" strokeWidth={3} fill="url(#costGrad)" name="Cost (₹)" />
                  )}
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Active Alerts Preview Table */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl backdrop-blur-md">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-rose-400" />
                Active Anomaly Alerts & Action Center
              </h3>
              <p className="text-xs text-slate-400">Real-time flags detected by Isolation Forest algorithm</p>
            </div>
            <Link
              to="/alerts"
              className="text-xs font-semibold text-sky-400 hover:text-sky-300 transition-colors"
            >
              View All Alerts &rarr;
            </Link>
          </div>

          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/60 text-slate-400 uppercase font-semibold">
                <tr>
                  <th className="px-4 py-3 rounded-l-xl">Severity</th>
                  <th className="px-4 py-3">Hostel Block</th>
                  <th className="px-4 py-3">Resource</th>
                  <th className="px-4 py-3">Deviation %</th>
                  <th className="px-4 py-3">Description</th>
                  <th className="px-4 py-3 rounded-r-xl">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {recent_alerts.map((alert) => (
                  <tr key={alert.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-4 py-3">
                      <StatusBadge status={alert.severity} />
                    </td>
                    <td className="px-4 py-3 font-semibold text-white">
                      {alert.hostel_name} ({alert.hostel_block})
                    </td>
                    <td className="px-4 py-3">{alert.resource_type}</td>
                    <td className="px-4 py-3 font-bold text-rose-400">
                      +{alert.difference_percentage}%
                    </td>
                    <td className="px-4 py-3 text-slate-400 max-w-md truncate">
                      {alert.description}
                    </td>
                    <td className="px-4 py-3">
                      <Link
                        to="/alerts"
                        className="rounded-lg border border-slate-700 bg-slate-800 px-2.5 py-1 text-[11px] font-semibold text-sky-400 hover:bg-slate-700 hover:text-white transition-colors"
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
'''

for rel_path, content in files.items():
    full_path = os.path.join(FRONTEND_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

print("Login and Dashboard pages created successfully.")
