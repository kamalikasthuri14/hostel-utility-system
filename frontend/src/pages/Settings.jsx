import React, { useState, useEffect } from "react";
import { Settings as SettingsIcon, IndianRupee, RefreshCw, CheckCircle2, ShieldAlert } from "lucide-react";
import { settingsAPI } from "../services/api";
import { Header } from "../components/common/Header";

export const Settings = () => {
  const [rates, setRates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reseedLoading, setReseedLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState("");

  const loadRates = () => {
    setLoading(true);
    settingsAPI.getRates()
      .then((res) => setRates(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadRates();
  }, []);

  const handleUpdateRate = async (id, newRate) => {
    try {
      await settingsAPI.updateRate(id, parseFloat(newRate));
      setStatusMsg("Utility tariff rate updated successfully.");
      loadRates();
      setTimeout(() => setStatusMsg(""), 3000);
    } catch (err) {
      alert("Rate update failed");
    }
  };

  const handleReseed = async () => {
    if (window.confirm("Re-seeding will recreate 8 blocks, 2,450 students, and 6 months of utility records. Proceed?")) {
      setReseedLoading(true);
      try {
        await settingsAPI.reseed();
        setStatusMsg("Database re-seeded successfully with fresh demo records!");
        loadRates();
      } catch (err) {
        alert("Reseed failed");
      } finally {
        setReseedLoading(false);
      }
    }
  };

  return (
    <div className="flex-1 min-h-screen bg-slate-50/60 pb-16">
      <Header
        title="Institutional Settings & Tariff Configuration"
        subtitle="Configure commercial billing unit rates, database state, and system diagnostics"
      />

      <main className="p-8 max-w-4xl mx-auto space-y-6">
        {statusMsg && (
          <div className="rounded-xl bg-emerald-50 border border-emerald-200 p-3 text-xs font-bold text-emerald-800">
            {statusMsg}
          </div>
        )}

        {/* Utility Tariff Rates */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm">
          <h3 className="text-sm font-extrabold text-slate-900 mb-1 flex items-center gap-2">
            <IndianRupee className="h-4 w-4 text-emerald-600" />
            Commercial Utility Tariff Rates
          </h3>
          <p className="text-xs text-slate-500 mb-6 font-medium">
            Rates applied across all consumption logs to calculate operational costs in INR (₹)
          </p>

          <div className="space-y-4">
            {rates.map((r) => (
              <div key={r.id} className="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50/70 p-4">
                <div>
                  <p className="text-sm font-bold text-slate-900">{r.resource_type}</p>
                  <p className="text-xs text-slate-500 font-medium">Billing Unit: {r.unit}</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex items-center rounded-xl border border-slate-200 bg-white px-3 py-1.5 shadow-xs">
                    <span className="text-xs text-slate-400 mr-1 font-bold">₹</span>
                    <input
                      type="number"
                      step="0.01"
                      defaultValue={r.rate}
                      onBlur={(e) => handleUpdateRate(r.id, e.target.value)}
                      className="w-20 bg-transparent text-sm font-extrabold text-slate-900 focus:outline-none"
                    />
                    <span className="text-xs text-slate-500 ml-1 font-medium">/ {r.unit}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Demo Database Re-seed */}
        <div className="rounded-2xl border border-rose-200 bg-rose-50/40 p-6 shadow-sm">
          <h3 className="text-sm font-extrabold text-rose-900 mb-1 flex items-center gap-2">
            <ShieldAlert className="h-4 w-4 text-rose-600" />
            Demo Data & Environment Reset
          </h3>
          <p className="text-xs text-rose-700 mb-4 font-medium">
            Re-populates all 8 blocks, 1,440+ historical consumption rows, pre-trains Random Forest models, and generates initial anomaly alerts.
          </p>
          <button
            onClick={handleReseed}
            disabled={reseedLoading}
            className="flex items-center gap-2 rounded-xl bg-rose-600 px-4 py-2.5 text-xs font-bold text-white hover:bg-rose-700 transition-all shadow-md shadow-rose-600/20 cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${reseedLoading ? "animate-spin" : ""}`} />
            <span>{reseedLoading ? "Re-seeding Database & Training ML..." : "Re-Seed Complete Demo Database"}</span>
          </button>
        </div>
      </main>
    </div>
  );
};
