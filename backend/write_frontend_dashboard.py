import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend", "src")

files = {}

# 1. Sidebar Component
files["components/common/Sidebar.jsx"] = '''import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Building2,
  Users,
  Zap,
  BarChart3,
  TrendingUp,
  AlertTriangle,
  Lightbulb,
  Wrench,
  FileSpreadsheet,
  Settings,
  LogOut,
  ShieldCheck,
  Flame,
  Droplets
} from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";

export const Sidebar = () => {
  const { user, role, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const navItems = [
    { label: "Dashboard", to: "/", icon: LayoutDashboard, roles: ["admin", "warden", "maintenance"] },
    { label: "Hostels", to: "/hostels", icon: Building2, roles: ["admin", "warden"] },
    { label: "Occupancy", to: "/occupancy", icon: Users, roles: ["admin", "warden"] },
    { label: "Utilities", to: "/utilities", icon: Zap, roles: ["admin", "warden"] },
    { label: "Analytics", to: "/analytics", icon: BarChart3, roles: ["admin", "warden"] },
    { label: "Predictions (ML)", to: "/predictions", icon: TrendingUp, roles: ["admin", "warden"] },
    { label: "Alerts & Anomalies", to: "/alerts", icon: AlertTriangle, roles: ["admin", "warden", "maintenance"] },
    { label: "Smart Recommendations", to: "/recommendations", icon: Lightbulb, roles: ["admin", "warden"] },
    { label: "Maintenance Hub", to: "/maintenance", icon: Wrench, roles: ["admin", "warden", "maintenance"] },
    { label: "Reports & Audit", to: "/reports", icon: FileSpreadsheet, roles: ["admin", "warden"] },
    { label: "Settings & Rates", to: "/settings", icon: Settings, roles: ["admin"] },
  ];

  const filteredNav = navItems.filter((item) => item.roles.includes(role || "admin"));

  return (
    <aside className="fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-slate-800 bg-slate-950/95 p-4 backdrop-blur-xl transition-all">
      {/* Brand Header */}
      <div className="flex items-center gap-3 px-2 py-3 border-b border-slate-800/80">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 shadow-md shadow-sky-500/20">
          <Zap className="h-5 w-5 text-white" />
        </div>
        <div>
          <h1 className="text-sm font-bold tracking-tight text-white flex items-center gap-1.5">
            HostelOptima <span className="rounded bg-sky-500/20 px-1 py-0.5 text-[10px] font-semibold text-sky-400">AI</span>
          </h1>
          <p className="text-[11px] text-slate-400">Resource Optimization</p>
        </div>
      </div>

      {/* User Role Badge */}
      <div className="my-4 rounded-xl border border-slate-800 bg-slate-900/60 p-3">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-800 text-sky-400">
            <ShieldCheck className="h-4 w-4" />
          </div>
          <div className="overflow-hidden">
            <p className="truncate text-xs font-semibold text-white">{user?.name || "Hostel User"}</p>
            <p className="text-[11px] font-medium capitalize text-sky-400 flex items-center gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              {user?.role} {user?.assigned_hostel ? `(${user.assigned_hostel.block})` : ""}
            </p>
          </div>
        </div>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 space-y-1 overflow-y-auto pr-1">
        {filteredNav.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2.5 text-xs font-semibold transition-all ${
                  isActive
                    ? "bg-sky-500 text-white shadow-lg shadow-sky-500/20 font-bold"
                    : "text-slate-400 hover:bg-slate-900 hover:text-slate-100"
                }`
              }
            >
              <Icon className="h-4 w-4 flex-shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Logout Button */}
      <div className="border-t border-slate-800/80 pt-3">
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-xs font-semibold text-rose-400 transition-colors hover:bg-rose-500/10 hover:text-rose-300"
        >
          <LogOut className="h-4 w-4" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
};
'''

# 2. Header Component
files["components/common/Header.jsx"] = '''import React from "react";
import { Bell, ShieldCheck, Zap, Building } from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";
import { Link } from "react-router-dom";

export const Header = ({ title, subtitle, activeAlertsCount = 0 }) => {
  const { user } = useAuth();

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-8 backdrop-blur-xl">
      <div>
        <h1 className="text-lg font-bold tracking-tight text-white">{title}</h1>
        {subtitle && <p className="text-xs text-slate-400">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-4">
        {/* Active Campus Tag */}
        <div className="hidden sm:flex items-center gap-2 rounded-full border border-slate-800 bg-slate-900/90 px-3 py-1 text-xs text-slate-300">
          <Building className="h-3.5 w-3.5 text-sky-400" />
          <span>Institutional Grid: <strong className="text-white">8 Blocks Active</strong></span>
        </div>

        {/* Notifications Bell */}
        <Link
          to="/alerts"
          className="relative rounded-xl border border-slate-800 bg-slate-900/80 p-2 text-slate-300 transition-colors hover:bg-slate-800 hover:text-white"
        >
          <Bell className="h-4 w-4" />
          {activeAlertsCount > 0 && (
            <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-[10px] font-bold text-white shadow">
              {activeAlertsCount}
            </span>
          )}
        </Link>

        {/* User Pill */}
        <div className="flex items-center gap-2.5 rounded-xl border border-slate-800 bg-slate-900/80 py-1.5 pl-2.5 pr-3">
          <div className="h-7 w-7 rounded-lg bg-sky-500/20 text-sky-400 flex items-center justify-center text-xs font-bold uppercase">
            {user?.name ? user.name.charAt(0) : "U"}
          </div>
          <div className="text-left">
            <p className="text-xs font-semibold text-white leading-tight">{user?.name || "Administrator"}</p>
            <p className="text-[10px] font-medium capitalize text-slate-400">{user?.role || "User"}</p>
          </div>
        </div>
      </div>
    </header>
  );
};
'''

# 3. Efficiency Gauge Visualizer
files["components/charts/EfficiencyGauge.jsx"] = '''import React from "react";
import { ShieldCheck, Droplets, Zap, Flame, AlertCircle } from "lucide-react";

export const EfficiencyGauge = ({ score = 86, grade = "A", rating = "High Efficiency", details = {} }) => {
  const getScoreColor = (val) => {
    if (val >= 85) return "text-emerald-400 stroke-emerald-400";
    if (val >= 70) return "text-sky-400 stroke-sky-400";
    if (val >= 55) return "text-amber-400 stroke-amber-400";
    return "text-rose-400 stroke-rose-400";
  };

  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl backdrop-blur-md">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-sky-400" />
            Hostel Resource Efficiency Index
          </h3>
          <p className="text-xs text-slate-400">0–100 Weighted Composite Performance</p>
        </div>
        <span className="rounded-full bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 text-xs font-bold text-emerald-400">
          Grade: {grade}
        </span>
      </div>

      <div className="mt-6 flex flex-col md:flex-row items-center justify-around gap-6">
        {/* Radial Circle */}
        <div className="relative flex items-center justify-center">
          <svg className="h-36 w-36 -rotate-90 transform" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="45"
              className="stroke-slate-800"
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
            <span className="text-3xl font-extrabold text-white tracking-tight">{score}</span>
            <span className="text-[10px] font-semibold uppercase text-slate-400">/ 100 Score</span>
          </div>
        </div>

        {/* Sub-Pillar Breakdown */}
        <div className="w-full md:w-64 space-y-3">
          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1">
              <span className="flex items-center gap-1.5"><Droplets className="h-3.5 w-3.5 text-sky-400" /> Water Efficiency</span>
              <span className="font-bold text-white">{details.water_efficiency || 88}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full rounded-full bg-sky-500" style={{ width: `${details.water_efficiency || 88}%` }} />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1">
              <span className="flex items-center gap-1.5"><Zap className="h-3.5 w-3.5 text-amber-400" /> Electricity Efficiency</span>
              <span className="font-bold text-white">{details.electricity_efficiency || 82}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full rounded-full bg-amber-500" style={{ width: `${details.electricity_efficiency || 82}%` }} />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1">
              <span className="flex items-center gap-1.5"><Flame className="h-3.5 w-3.5 text-rose-400" /> Gas & Dining Efficiency</span>
              <span className="font-bold text-white">{details.gas_efficiency || 89}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full rounded-full bg-rose-500" style={{ width: `${details.gas_efficiency || 89}%` }} />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1">
              <span className="flex items-center gap-1.5"><AlertCircle className="h-3.5 w-3.5 text-emerald-400" /> Wastage Control</span>
              <span className="font-bold text-white">{details.wastage_control || 85}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full rounded-full bg-emerald-500" style={{ width: `${details.wastage_control || 85}%` }} />
            </div>
          </div>
        </div>
      </div>
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

print("Frontend navigation and gauge components created.")
