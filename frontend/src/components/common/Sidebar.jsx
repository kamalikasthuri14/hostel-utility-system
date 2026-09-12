import React from "react";
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
