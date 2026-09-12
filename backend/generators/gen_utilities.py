import os

target = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend\src\pages\Utilities.jsx"
code = '''import React, { useState, useEffect } from "react";
import { Zap, Droplets, Flame, Plus, UploadCloud, Download, Search, Filter, Trash2 } from "lucide-react";
import { consumptionAPI, hostelsAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { Modal } from "../components/common/Modal";
import { useAuth } from "../contexts/AuthContext";

export const Utilities = () => {
  const { role } = useAuth();
  const [records, setRecords] = useState([]);
  const [hostels, setHostels] = useState([]);
  const [selectedHostel, setSelectedHostel] = useState("");
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [csvModalOpen, setCsvModalOpen] = useState(false);
  const [csvFile, setCsvFile] = useState(null);
  const [csvStatus, setCsvStatus] = useState("");
  const [formData, setFormData] = useState({
    hostel_id: "",
    date: new Date().toISOString().split("T")[0],
    water_litres: 30000,
    electricity_kwh: 1400,
    gas_kg: 42
  });

  const loadData = () => {
    setLoading(true);
    const params = selectedHostel ? { hostel_id: selectedHostel, limit: 100 } : { limit: 100 };
    Promise.all([consumptionAPI.list(params), hostelsAPI.list()])
      .then(([cRes, hRes]) => {
        setRecords(cRes.data);
        setHostels(hRes.data);
        if (hRes.data.length > 0 && !formData.hostel_id) {
          setFormData((prev) => ({ ...prev, hostel_id: hRes.data[0].id }));
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, [selectedHostel]);

  const handleSubmitRecord = async (e) => {
    e.preventDefault();
    try {
      await consumptionAPI.create(formData);
      setModalOpen(false);
      loadData();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to create record");
    }
  };

  const handleUploadCSV = async (e) => {
    e.preventDefault();
    if (!csvFile) return;
    setCsvStatus("Uploading and validating records in database...");
    const form = new FormData();
    form.append("file", csvFile);
    try {
      const res = await consumptionAPI.uploadCSV(form);
      setCsvStatus(`Successfully ingested ${res.data.inserted_records} records!`);
      setTimeout(() => {
        setCsvModalOpen(false);
        setCsvStatus("");
        setCsvFile(null);
        loadData();
      }, 1500);
    } catch (err) {
      setCsvStatus(err.response?.data?.detail || "CSV upload failed");
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this consumption entry?")) {
      try {
        await consumptionAPI.delete(id);
        loadData();
      } catch (err) {
        alert("Delete failed");
      }
    }
  };

  return (
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Utility Consumption Data & Batch Management"
        subtitle="Manage daily sub-meter logs, CSV imports, and automated cost disaggregations"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex items-center gap-3">
            <Filter className="h-4 w-4 text-sky-400" />
            <select
              value={selectedHostel}
              onChange={(e) => setSelectedHostel(e.target.value)}
              className="rounded-xl border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white focus:outline-none"
            >
              <option value="">All Hostels ({hostels.length} Blocks)</option>
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.name} ({h.block})</option>
              ))}
            </select>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <a
              href={consumptionAPI.exportCSVUrl}
              download
              className="flex items-center gap-1.5 rounded-xl border border-slate-700 bg-slate-800 px-3.5 py-2 text-xs font-bold text-slate-300 hover:bg-slate-700 hover:text-white transition-all"
            >
              <Download className="h-3.5 w-3.5" />
              <span>Export CSV</span>
            </a>
            <button
              onClick={() => setCsvModalOpen(true)}
              className="flex items-center gap-1.5 rounded-xl border border-sky-500/30 bg-sky-500/10 px-3.5 py-2 text-xs font-bold text-sky-400 hover:bg-sky-500/20 transition-all cursor-pointer"
            >
              <UploadCloud className="h-3.5 w-3.5" />
              <span>Import CSV</span>
            </button>
            <button
              onClick={() => setModalOpen(true)}
              className="flex items-center gap-1.5 rounded-xl bg-sky-500 px-3.5 py-2 text-xs font-bold text-white shadow-lg shadow-sky-500/20 hover:bg-sky-400 transition-all cursor-pointer"
            >
              <Plus className="h-3.5 w-3.5" />
              <span>Add Record</span>
            </button>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl backdrop-blur-md">
          <h3 className="text-sm font-bold text-white mb-4">Daily Telemetry & Cost Records</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/60 text-slate-400 uppercase font-semibold">
                <tr>
                  <th className="px-4 py-3 rounded-l-xl">Date</th>
                  <th className="px-4 py-3">Block</th>
                  <th className="px-4 py-3">Water (Litres)</th>
                  <th className="px-4 py-3">Electricity (kWh)</th>
                  <th className="px-4 py-3">Gas (kg)</th>
                  <th className="px-4 py-3">Per Student (W / E / G)</th>
                  <th className="px-4 py-3">Total Cost (₹)</th>
                  {role === "admin" && <th className="px-4 py-3 rounded-r-xl">Action</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {records.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-4 py-3 font-semibold text-white">{r.date}</td>
                    <td className="px-4 py-3 font-bold text-sky-400">{r.hostel_block}</td>
                    <td className="px-4 py-3 font-medium text-slate-200">{r.water_litres.toLocaleString()} L</td>
                    <td className="px-4 py-3 font-medium text-slate-200">{r.electricity_kwh.toLocaleString()} kWh</td>
                    <td className="px-4 py-3 font-medium text-slate-200">{r.gas_kg} kg</td>
                    <td className="px-4 py-3 text-slate-400">
                      <span className={r.water_per_student > 115 ? "text-amber-400 font-bold" : ""}>{r.water_per_student}L</span> /{" "}
                      <span className={r.electricity_per_student > 5.2 ? "text-amber-400 font-bold" : ""}>{r.electricity_per_student}k</span> /{" "}
                      <span>{r.gas_per_student}kg</span>
                    </td>
                    <td className="px-4 py-3 font-bold text-emerald-400">₹{r.total_cost.toLocaleString()}</td>
                    {role === "admin" && (
                      <td className="px-4 py-3">
                        <button
                          onClick={() => handleDelete(r.id)}
                          className="rounded p-1 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors cursor-pointer"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Log Daily Utility Consumption">
        <form onSubmit={handleSubmitRecord} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Hostel Block</label>
            <select
              value={formData.hostel_id}
              onChange={(e) => setFormData({ ...formData, hostel_id: parseInt(e.target.value) })}
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            >
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.name} ({h.block})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Date</label>
            <input
              type="date"
              required
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Water (Litres)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                required
                value={formData.water_litres}
                onChange={(e) => setFormData({ ...formData, water_litres: parseFloat(e.target.value) || 0 })}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Electricity (kWh)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                required
                value={formData.electricity_kwh}
                onChange={(e) => setFormData({ ...formData, electricity_kwh: parseFloat(e.target.value) || 0 })}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Gas (kg)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                required
                value={formData.gas_kg}
                onChange={(e) => setFormData({ ...formData, gas_kg: parseFloat(e.target.value) || 0 })}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
              />
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={() => setModalOpen(false)}
              className="rounded-xl border border-slate-700 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-sky-500 px-4 py-2 text-xs font-bold text-white hover:bg-sky-400 cursor-pointer"
            >
              Save Consumption Record
            </button>
          </div>
        </form>
      </Modal>

      <Modal isOpen={csvModalOpen} onClose={() => setCsvModalOpen(false)} title="Upload Utility Consumption CSV">
        <form onSubmit={handleUploadCSV} className="space-y-4">
          <p className="text-xs text-slate-400">
            Upload CSV with columns: <code className="text-sky-400 font-mono">hostel, date, water_litres, electricity_kwh, gas_kg</code>.
          </p>

          <div className="rounded-xl border-2 border-dashed border-slate-700 p-6 text-center hover:border-sky-500/50 transition-colors">
            <input
              type="file"
              accept=".csv"
              required
              onChange={(e) => setCsvFile(e.target.files[0])}
              className="block w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-sky-500 file:text-white hover:file:bg-sky-400 cursor-pointer"
            />
          </div>

          {csvStatus && (
            <p className="text-xs font-semibold text-sky-400">{csvStatus}</p>
          )}

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={() => setCsvModalOpen(false)}
              className="rounded-xl border border-slate-700 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!csvFile}
              className="rounded-xl bg-sky-500 px-4 py-2 text-xs font-bold text-white hover:bg-sky-400 disabled:opacity-50 cursor-pointer"
            >
              Process & Ingest CSV
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
'''

with open(target, "w", encoding="utf-8") as f:
    f.write(code.strip() + "\n")
print("Utilities.jsx generated.")
