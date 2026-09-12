import os

FRONTEND_SRC = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend\src"

app_code = '''import React from "react";
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
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-sky-400 font-semibold text-sm">
        Initializing Hostel Utility Grid...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans">
      <Sidebar />
      <div className="flex-1 pl-64 flex flex-col min-h-screen">
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

          {/* Protected Routes */}
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

main_code = '''import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''

index_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-slate-950 text-slate-100 antialiased selection:bg-sky-500 selection:text-white;
    font-family: 'Plus Jakarta Sans', sans-serif;
  }
}

/* Custom modern scrollbars */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #090d16;
}
::-webkit-scrollbar-thumb {
  background: #1e293b;
  border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
  background: #334155;
}
'''

with open(os.path.join(FRONTEND_SRC, "App.jsx"), "w", encoding="utf-8") as f:
    f.write(app_code.strip() + "\n")
with open(os.path.join(FRONTEND_SRC, "main.jsx"), "w", encoding="utf-8") as f:
    f.write(main_code.strip() + "\n")
with open(os.path.join(FRONTEND_SRC, "index.css"), "w", encoding="utf-8") as f:
    f.write(index_css.strip() + "\n")

print("App.jsx, main.jsx, and index.css generated.")
