import os

FRONTEND_SRC = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend\src"

# 1. Sidebar Component
sidebar_code = '''import React from "react";
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
    <aside className="fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-slate-200/80 bg-white shadow-xl shadow-slate-200/50 p-4 transition-all">
      {/* Brand Header */}
      <div className="flex items-center gap-3 px-2 py-3 border-b border-slate-100">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 shadow-md shadow-sky-500/20">
          <Zap className="h-5 w-5 text-white" />
        </div>
        <div>
          <h1 className="text-sm font-extrabold tracking-tight text-slate-900 flex items-center gap-1.5">
            HostelOptima <span className="rounded-md bg-sky-100 px-1.5 py-0.5 text-[10px] font-bold text-sky-600">AI</span>
          </h1>
          <p className="text-[11px] text-slate-500 font-medium">Utility Optimization</p>
        </div>
      </div>

      {/* User Role Badge */}
      <div className="my-4 rounded-xl border border-slate-100 bg-slate-50/80 p-3 shadow-sm">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-sky-100 text-sky-600 font-bold">
            <ShieldCheck className="h-4 w-4" />
          </div>
          <div className="overflow-hidden">
            <p className="truncate text-xs font-bold text-slate-900">{user?.name || "Hostel User"}</p>
            <p className="text-[11px] font-semibold capitalize text-sky-600 flex items-center gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
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
                    ? "bg-gradient-to-r from-sky-500 to-indigo-600 text-white shadow-md shadow-sky-500/25 font-bold"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
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
      <div className="border-t border-slate-100 pt-3">
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-xs font-semibold text-rose-600 transition-colors hover:bg-rose-50 hover:text-rose-700 cursor-pointer"
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
header_code = '''import React from "react";
import { Bell, Building } from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";
import { Link } from "react-router-dom";

export const Header = ({ title, subtitle, activeAlertsCount = 0 }) => {
  const { user } = useAuth();

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200/80 bg-white/80 px-8 backdrop-blur-md shadow-sm">
      <div>
        <h1 className="text-base font-extrabold tracking-tight text-slate-900">{title}</h1>
        {subtitle && <p className="text-xs text-slate-500 font-medium">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden sm:flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3.5 py-1 text-xs text-slate-600 shadow-sm font-medium">
          <Building className="h-3.5 w-3.5 text-sky-600" />
          <span>Institutional Grid: <strong className="text-slate-900">8 Blocks Active</strong></span>
        </div>

        <Link
          to="/alerts"
          className="relative rounded-xl border border-slate-200 bg-slate-50 p-2 text-slate-600 transition-colors hover:bg-slate-100 hover:text-slate-900 shadow-sm"
        >
          <Bell className="h-4 w-4" />
          {activeAlertsCount > 0 && (
            <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-[10px] font-bold text-white shadow">
              {activeAlertsCount}
            </span>
          )}
        </Link>

        <div className="flex items-center gap-2.5 rounded-xl border border-slate-200 bg-slate-50 py-1.5 pl-2.5 pr-3.5 shadow-sm">
          <div className="h-7 w-7 rounded-lg bg-sky-500 text-white flex items-center justify-center text-xs font-bold uppercase shadow-sm">
            {user?.name ? user.name.charAt(0) : "U"}
          </div>
          <div className="text-left">
            <p className="text-xs font-bold text-slate-900 leading-tight">{user?.name || "Administrator"}</p>
            <p className="text-[10px] font-semibold capitalize text-sky-600">{user?.role || "User"}</p>
          </div>
        </div>
      </div>
    </header>
  );
};
'''

# 3. MetricCard Component
metric_code = '''import React from "react";
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
'''

# 4. StatusBadge Component
badge_code = '''import React from "react";

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
'''

# 5. Modal Component
modal_code = '''import React from "react";
import { X } from "lucide-react";

export const Modal = ({ isOpen, onClose, title, children, maxWidth = "max-w-xl" }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs transition-opacity" onClick={onClose} />
      <div className={`relative w-full ${maxWidth} transform overflow-hidden rounded-2xl border border-slate-200 bg-white p-6 text-left shadow-2xl transition-all`}>
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <h3 className="text-base font-bold text-slate-900">{title}</h3>
          <button onClick={onClose} className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700 transition-colors cursor-pointer">
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="mt-4">{children}</div>
      </div>
    </div>
  );
};
'''

# 6. EfficiencyGauge Component
gauge_code = '''import React from "react";
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
'''

with open(os.path.join(FRONTEND_SRC, "components", "common", "Sidebar.jsx"), "w", encoding="utf-8") as f:
    f.write(sidebar_code.strip() + "\n")
with open(os.path.join(FRONTEND_SRC, "components", "common", "Header.jsx"), "w", encoding="utf-8") as f:
    f.write(header_code.strip() + "\n")
with open(os.path.join(FRONTEND_SRC, "components", "common", "MetricCard.jsx"), "w", encoding="utf-8") as f:
    f.write(metric_code.strip() + "\n")
with open(os.path.join(FRONTEND_SRC, "components", "common", "StatusBadge.jsx"), "w", encoding="utf-8") as f:
    f.write(badge_code.strip() + "\n")
with open(os.path.join(FRONTEND_SRC, "components", "common", "Modal.jsx"), "w", encoding="utf-8") as f:
    f.write(modal_code.strip() + "\n")
with open(os.path.join(FRONTEND_SRC, "components", "charts", "EfficiencyGauge.jsx"), "w", encoding="utf-8") as f:
    f.write(gauge_code.strip() + "\n")

print("Components updated with clean, attractive light theme styling.")
