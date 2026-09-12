import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL.replace(/\/+$/, "")}/api`
  : "/api";

const API = axios.create({
  baseURL: API_BASE,
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
  exportCSVUrl: (import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace(/\/+$/, "") : "") + "/api/consumption/export-csv"
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
