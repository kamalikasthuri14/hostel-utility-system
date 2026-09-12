import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend", "src")

files = {}

# 1. API Client
files["services/api.js"] = '''import axios from "axios";

const API = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json"
  }
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email, password) => API.post("/auth/login", { email, password }),
  getMe: () => API.get("/auth/me")
};

export const dashboardAPI = {
  getSummary: () => API.get("/dashboard/summary"),
  getEfficiency: () => API.get("/dashboard/efficiency")
};

export const hostelsAPI = {
  list: () => API.get("/hostels"),
  get: (id) => API.get(`/hostels/${id}`),
  create: (data) => API.post("/hostels", data),
  update: (id, data) => API.put(`/hostels/${id}`, data),
  delete: (id) => API.delete(`/hostels/${id}`)
};

export const occupancyAPI = {
  list: (params) => API.get("/occupancy", { params }),
  log: (data) => API.post("/occupancy", data)
};

export const consumptionAPI = {
  list: (params) => API.get("/consumption", { params }),
  create: (data) => API.post("/consumption", data),
  update: (id, data) => API.put(`/consumption/${id}`, data),
  delete: (id) => API.delete(`/consumption/${id}`),
  uploadCSV: (formData) => API.post("/consumption/upload-csv", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  }),
  exportCSVUrl: "/api/consumption/export-csv"
};

export const analyticsAPI = {
  getWater: (params) => API.get("/analytics/water", { params }),
  getElectricity: (params) => API.get("/analytics/electricity", { params }),
  getGas: (params) => API.get("/analytics/gas", { params }),
  getPerStudent: (params) => API.get("/analytics/per-student", { params })
};

export const predictionsAPI = {
  get: (params) => API.get("/predictions", { params }),
  retrain: () => API.post("/predictions/retrain")
};

export const anomaliesAPI = {
  detect: () => API.post("/anomalies/detect")
};

export const alertsAPI = {
  list: (params) => API.get("/alerts", { params }),
  updateStatus: (id, status) => API.put(`/alerts/${id}`, { status }),
  convertToTicket: (id, data) => API.post(`/alerts/${id}/convert-to-ticket`, data)
};

export const recommendationsAPI = {
  list: (params) => API.get("/recommendations", { params })
};

export const maintenanceAPI = {
  list: (params) => API.get("/maintenance", { params }),
  create: (data) => API.post("/maintenance", data),
  update: (id, data) => API.put(`/maintenance/${id}`, data)
};

export const reportsAPI = {
  getDaily: (params) => API.get("/reports/daily", { params }),
  getWeekly: (params) => API.get("/reports/weekly", { params }),
  getMonthly: (params) => API.get("/reports/monthly", { params })
};

export const settingsAPI = {
  getRates: () => API.get("/settings/rates"),
  updateRate: (id, rate) => API.put(`/settings/rates/${id}`, { rate }),
  reseed: () => API.post("/settings/reseed")
};

export default API;
'''

# 2. Auth Context
files["contexts/AuthContext.jsx"] = '''import React, { createContext, useContext, useState, useEffect } from "react";
import { authAPI } from "../services/api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("user");
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState(() => localStorage.getItem("token") || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      authAPI.getMe()
        .then((res) => {
          setUser(res.data);
          localStorage.setItem("user", JSON.stringify(res.data));
        })
        .catch(() => {
          logout();
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (email, password) => {
    const res = await authAPI.login(email, password);
    const { access_token, user: userData } = res.data;
    localStorage.setItem("token", access_token);
    localStorage.setItem("user", JSON.stringify(userData));
    setToken(access_token);
    setUser(userData);
    return userData;
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, role: user?.role, isAuthenticated: !!token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
'''

# 3. Common UI Components: MetricCard, StatusBadge, Modal
files["components/common/MetricCard.jsx"] = '''import React from "react";
import { TrendingUp, TrendingDown } from "lucide-react";

export const MetricCard = ({ title, value, unit, change, isPositive, icon: Icon, color = "blue", subtitle }) => {
  const colorMap = {
    blue: "from-blue-500/20 to-blue-600/5 border-blue-500/30 text-blue-400",
    emerald: "from-emerald-500/20 to-emerald-600/5 border-emerald-500/30 text-emerald-400",
    amber: "from-amber-500/20 to-amber-600/5 border-amber-500/30 text-amber-400",
    purple: "from-purple-500/20 to-purple-600/5 border-purple-500/30 text-purple-400",
    rose: "from-rose-500/20 to-rose-600/5 border-rose-500/30 text-rose-400",
    cyan: "from-cyan-500/20 to-cyan-600/5 border-cyan-500/30 text-cyan-400",
  };

  return (
    <div className={`relative overflow-hidden rounded-2xl border bg-gradient-to-br p-5 shadow-lg backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-xl bg-slate-900/80 ${colorMap[color]}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</span>
        {Icon && (
          <div className="rounded-xl bg-slate-800/80 p-2.5 shadow-inner">
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
      <div className="mt-4 flex items-baseline gap-2">
        <span className="text-2xl font-bold tracking-tight text-white">{value}</span>
        {unit && <span className="text-xs font-medium text-slate-400">{unit}</span>}
      </div>
      {(subtitle || change !== undefined) && (
        <div className="mt-3 flex items-center gap-2 text-xs">
          {change !== undefined && (
            <span className={`inline-flex items-center gap-0.5 font-medium ${isPositive ? "text-emerald-400" : "text-rose-400"}`}>
              {isPositive ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
              {change}
            </span>
          )}
          {subtitle && <span className="text-slate-400">{subtitle}</span>}
        </div>
      )}
    </div>
  );
};
'''

files["components/common/StatusBadge.jsx"] = '''import React from "react";

export const StatusBadge = ({ status, type = "status" }) => {
  const getBadgeStyle = () => {
    const s = String(status).toLowerCase();
    
    // Severity
    if (s === "critical") return "bg-red-500/20 text-red-400 border-red-500/30 animate-pulse";
    if (s === "high") return "bg-orange-500/20 text-orange-400 border-orange-500/30";
    if (s === "medium") return "bg-amber-500/20 text-amber-400 border-amber-500/30";
    if (s === "low") return "bg-blue-500/20 text-blue-400 border-blue-500/30";

    // Maintenance Status
    if (s === "open") return "bg-rose-500/20 text-rose-400 border-rose-500/30";
    if (s === "assigned") return "bg-purple-500/20 text-purple-400 border-purple-500/30";
    if (s === "in progress") return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30";
    if (s === "resolved" || s === "closed") return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";

    // General Status
    if (s === "active") return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";
    if (s === "reviewed") return "bg-blue-500/20 text-blue-400 border-blue-500/30";
    if (s === "maintenance") return "bg-amber-500/20 text-amber-400 border-amber-500/30";

    return "bg-slate-700/50 text-slate-300 border-slate-600";
  };

  return (
    <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold tracking-wide ${getBadgeStyle()}`}>
      {status}
    </span>
  );
};
'''

files["components/common/Modal.jsx"] = '''import React from "react";
import { X } from "lucide-react";

export const Modal = ({ isOpen, onClose, title, children, maxWidth = "max-w-xl" }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm transition-opacity" onClick={onClose} />
      <div className={`relative w-full ${maxWidth} transform overflow-hidden rounded-2xl border border-slate-700/60 bg-slate-900 p-6 text-left shadow-2xl transition-all`}>
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <h3 className="text-lg font-bold text-white">{title}</h3>
          <button onClick={onClose} className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors">
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="mt-4">{children}</div>
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

print("Frontend base components written successfully.")
