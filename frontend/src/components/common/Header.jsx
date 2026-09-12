import React from "react";
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
