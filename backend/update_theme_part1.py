import os

FRONTEND_SRC = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend\src"
FRONTEND_ROOT = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend"

# 1. Update index.html
index_html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>HostelOptima AI - Utility Optimization & Predictive Resource Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  </head>
  <body class="bg-slate-50 text-slate-800 antialiased font-sans selection:bg-sky-500 selection:text-white">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
'''
with open(os.path.join(FRONTEND_ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html.strip() + "\n")

# 2. Update index.css
index_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-slate-50 text-slate-800 antialiased selection:bg-sky-500 selection:text-white;
    font-family: 'Plus Jakarta Sans', sans-serif;
  }
}

/* Custom modern light scrollbars */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #f1f5f9;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
'''
with open(os.path.join(FRONTEND_SRC, "index.css"), "w", encoding="utf-8") as f:
    f.write(index_css.strip() + "\n")

# 3. Update App.jsx
app_jsx = '''import React from "react";
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
'''
with open(os.path.join(FRONTEND_SRC, "App.jsx"), "w", encoding="utf-8") as f:
    f.write(app_jsx.strip() + "\n")

print("Base layout and css updated to attractive light theme.")
