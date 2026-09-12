import React, { useState, useEffect } from "react";
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
    <div className="flex-1 min-h-screen bg-slate-50/60 pb-16">
      <Header
        title="Utility Consumption Data & Batch Management"
        subtitle="Manage daily sub-meter logs, CSV imports, and automated cost disaggregations"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-4 shadow-sm">
          <div className="flex items-center gap-3">
            <Filter className="h-4 w-4 text-sky-600" />
            <select
              value={selectedHostel}
              onChange={(e) => setSelectedHostel(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-sky-500 focus:bg-white transition-all"
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
              className="flex items-center gap-1.5 rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2 text-xs font-bold text-slate-700 hover:bg-slate-100 hover:text-slate-900 transition-all shadow-xs"
            >
              <Download className="h-3.5 w-3.5 text-slate-500" />
              <span>Export CSV</span>
            </a>
            <button
              onClick={() => setCsvModalOpen(true)}
              className="flex items-center gap-1.5 rounded-xl border border-sky-200 bg-sky-50 px-3.5 py-2 text-xs font-bold text-sky-700 hover:bg-sky-100 transition-all shadow-xs cursor-pointer"
            >
              <UploadCloud className="h-3.5 w-3.5 text-sky-600" />
              <span>Import CSV</span>
            </button>
            <button
              onClick={() => setModalOpen(true)}
              className="flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-3.5 py-2 text-xs font-bold text-white shadow-md shadow-sky-500/20 hover:from-sky-600 hover:to-indigo-700 transition-all cursor-pointer"
            >
              <Plus className="h-3.5 w-3.5" />
              <span>Add Record</span>
            </button>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm">
          <h3 className="text-sm font-extrabold text-slate-900 mb-4">Daily Telemetry & Cost Records</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50 text-slate-600 uppercase font-bold border-b border-slate-100">
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
              <tbody className="divide-y divide-slate-100">
                {records.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="px-4 py-3 font-bold text-slate-900">{r.date}</td>
                    <td className="px-4 py-3 font-extrabold text-sky-700">{r.hostel_block}</td>
                    <td className="px-4 py-3 font-semibold text-slate-800">{r.water_litres.toLocaleString()} L</td>
                    <td className="px-4 py-3 font-semibold text-slate-800">{r.electricity_kwh.toLocaleString()} kWh</td>
                    <td className="px-4 py-3 font-semibold text-slate-800">{r.gas_kg} kg</td>
                    <td className="px-4 py-3 text-slate-600">
                      <span className={r.water_per_student > 115 ? "text-amber-600 font-bold" : ""}>{r.water_per_student}L</span> /{" "}
                      <span className={r.electricity_per_student > 5.2 ? "text-amber-600 font-bold" : ""}>{r.electricity_per_student}k</span> /{" "}
                      <span>{r.gas_per_student}kg</span>
                    </td>
                    <td className="px-4 py-3 font-extrabold text-emerald-600">₹{r.total_cost.toLocaleString()}</td>
                    {role === "admin" && (
                      <td className="px-4 py-3">
                        <button
                          onClick={() => handleDelete(r.id)}
                          className="rounded p-1 text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors cursor-pointer"
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
            <label className="block text-xs font-bold text-slate-700 mb-1">Hostel Block</label>
            <select
              value={formData.hostel_id}
              onChange={(e) => setFormData({ ...formData, hostel_id: parseInt(e.target.value) })}
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            >
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.name} ({h.block})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Date</label>
            <input
              type="date"
              required
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            />
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Water (Litres)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                required
                value={formData.water_litres}
                onChange={(e) => setFormData({ ...formData, water_litres: parseFloat(e.target.value) || 0 })}
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Electricity (kWh)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                required
                value={formData.electricity_kwh}
                onChange={(e) => setFormData({ ...formData, electricity_kwh: parseFloat(e.target.value) || 0 })}
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Gas (kg)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                required
                value={formData.gas_kg}
                onChange={(e) => setFormData({ ...formData, gas_kg: parseFloat(e.target.value) || 0 })}
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              />
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setModalOpen(false)}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-md shadow-sky-500/20 hover:from-sky-600 hover:to-indigo-700 cursor-pointer"
            >
              Save Consumption Record
            </button>
          </div>
        </form>
      </Modal>

      <Modal isOpen={csvModalOpen} onClose={() => setCsvModalOpen(false)} title="Upload Utility Consumption CSV">
        <form onSubmit={handleUploadCSV} className="space-y-4">
          <p className="text-xs text-slate-500 font-medium">
            Upload CSV with columns: <code className="text-sky-700 bg-sky-50 px-1 py-0.5 rounded font-mono font-bold">hostel, date, water_litres, electricity_kwh, gas_kg</code>.
          </p>

          <div className="rounded-xl border-2 border-dashed border-slate-200 bg-slate-50/50 p-6 text-center hover:border-sky-400 transition-colors">
            <input
              type="file"
              accept=".csv"
              required
              onChange={(e) => setCsvFile(e.target.files[0])}
              className="block w-full text-xs text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-sky-50 file:text-sky-700 hover:file:bg-sky-100 cursor-pointer"
            />
          </div>

          {csvStatus && (
            <p className="text-xs font-bold text-sky-700">{csvStatus}</p>
          )}

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setCsvModalOpen(false)}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!csvFile}
              className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-md shadow-sky-500/20 hover:from-sky-600 hover:to-indigo-700 disabled:opacity-50 cursor-pointer"
            >
              Process & Ingest CSV
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
