import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { Sidebar } from "./components/common/Sidebar";
import { Login } from "./pages/Login";
import { Dashboard } from "./pages/Dashboard";
import { Hostels } from "./pages/Hostels";
import { Occupancy } from "./pages/Occupancy";
import { Utilities } from "./pages/Utilities";
import { Analytics } from "./pages/Analytics";
import { Predictions } from "./pages/Predictions";
import { Alerts } from "./pages/Alerts";
import { Recommendations } from "./pages/Recommendations";
import { Maintenance } from "./pages/Maintenance";
import { Reports } from "./pages/Reports";
import { Settings } from "./pages/Settings";

const ProtectedLayout = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center text-sky-600 font-semibold text-sm">
        Initializing Hostel Utility Grid...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-800 font-sans">
      <Sidebar />
      <div className="flex-1 pl-64 flex flex-col min-h-screen bg-slate-50/60">
        <Outlet />
      </div>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route element={<ProtectedLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/hostels" element={<Hostels />} />
            <Route path="/occupancy" element={<Occupancy />} />
            <Route path="/utilities" element={<Utilities />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/maintenance" element={<Maintenance />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/settings" element={<Settings />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
